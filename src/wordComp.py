import ankiConnect
import json
import sys


def openWordList(
    filePath,
):
    try:
        with open(filePath, "r") as f:
            data = json.load(f)
            return data
    except FileNotFoundError:
        print("File not found")
    except json.JSONDecodeError:
        print("Invalid JSON format")
    except PermissionError:
        print("You don't have permissions to read this file")
    except Exception as e:
        print(f"Unexpected error: {e}")


def saveJsonCache(file_path, data):
    try:
        with open(file_path, "w") as file:
            json.dump(data, file, indent=4)
            print(f"Json file '{file_path}' was created")
    except FileExistsError:
        print("That file already exists!")


def compareWords(wordList, deckWords):
    # Turn both JSON files into sets for easier and faster operations
    wordListSet = set(wordList)
    deckWordsSet = set(deckWords)

    # Now let's compare them, getting the intersection

    diff = wordListSet.difference(deckWordsSet)

    # print(diff)
    return diff


def get_diff():
    deckWords = {}

    # 1. Gather notes info
    notes_data = ankiConnect.invoke("notesInfo", query="deck:current")
    if isinstance(notes_data, dict):
        notes_data = notes_data.get("result", [])

    if not isinstance(notes_data, list):
        print("Unexpected notes_data format")
        return []

    # 2. Extract card IDs safely
    card_ids = []
    for note in notes_data:
        cards = note.get("cards", [])
        if isinstance(cards, list):
            card_ids.extend(cards)
        elif cards:
            card_ids.append(cards)

    if not card_ids:
        print("Deck has no cards!")
        return []

    # 3. Query cards info
    card_stats = ankiConnect.invoke("cardsInfo", cards=card_ids)
    if isinstance(card_stats, dict):
        card_stats = card_stats.get("result", [])

    if not isinstance(card_stats, list):
        print("Unexpected card_stats format")
        return []

    # 4. Build deckWords
    for card in card_stats:
        interval = card.get("interval", 0)

        word = card.get("fields", {}).get("Front", {}).get("value", "")

        if not word:
            continue

        word = word.lower()
        status = "Mastered" if interval >= 21 else "In-Training"

        deckWords[word] = interval
        print(f"[+] Word: {word} | Interval: {interval} days | Status: {status}")

    if not deckWords:
        print("Deck has no valid words!")
        return []

    print("Deck has contents. Saving to the JSON cache now.")
    # saveJsonCache("data/deckCache.json", deckWords)

    # 5. Load word list
    wordList = openWordList("data/commonWords.json")
    if wordList is None:
        print("Failed to load file")
        return []

    print("Loaded successfully (even if empty)")
    print("Starting comparison phase.")

    # 6. Compare
    diff = compareWords(wordList, deckWords)

    print("Final intersection size:", len(diff))
    print(diff)

    return diff


# get_diff()
