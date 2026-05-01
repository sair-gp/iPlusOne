import ankiConnect
import os
import json
import wordComp


def sync_anki_to_json(deckName, file_path, client):

    # Get deck words
    raw_words = getDeckCards(deckName)

    # Compare against curent JSON cache to check if it's up to date or outdated

    currentJsonCache = wordComp.openWordList(file_path)

    newAnkiWords = compWordsToAnki(raw_words, currentJsonCache)

    # Send batch to Gemini

    prompt = f"""
    Analyze these words from an Anki deck. Use the language of the actual provided words, not the example. 
    Return a JSON object where each key is the Lemma and the value is a list of the words belonging to it.
    Format: {{"run": ["runs", "running"], "eat": ["eats", "eating"]}}
    Words: {list(newAnkiWords)}
    If there are no words, return an empty JSON
    """

    response = client.models.generate_content(
        model="gemini-3-flash-preview",
        contents=prompt,
    )

    # 4. Clean the response and save
    raw_json = response.text.strip().replace("```json", "").replace("```", "")
    lemma_data = json.loads(raw_json)

    # 5. Save the file
    final_vault = merge_and_save_lemmas(file_path, lemma_data)

    return final_vault


def loadDecks():
    # 1. Fetch all deck names from the Anki API
    all_decks = ankiConnect.invoke("deckNames")

    # 2. Display the tactical menu
    print("\n--- AVAILABLE ANKI DECKS ---")
    for i, name in enumerate(all_decks):
        print(f"[{i}] {name}")

    # 3. Get the user's choice
    choice = input("\nSelect a deck (Enter the number or the full name): ")

    # 4. Resolve the choice: Number vs. String
    if choice.isdigit():
        # Convert text input to an actual number
        selection_index = int(choice)
        target_deck = all_decks[selection_index]
    else:
        # Use the text exactly as typed
        target_deck = choice

    # 5. Set the path based on the selection
    deckPath = f"./data/decks/{target_deck}.json"

    print(f"\nTarget Deck: {target_deck}")
    print(f"PATH: {deckPath}")
    return target_deck, deckPath


def compDecktoWordList(deckLemmas, wordFreqDict):
    # 1. Flatten all words in the deckLemmas vault for fast lookup
    all_deck_words = {word for forms in deckLemmas.values() for word in forms}

    # 2. Filter out words that are already in the deck
    # Only look at the keys of wordFreqDict
    new_words = [word for word in wordFreqDict if word not in all_deck_words]

    # 3. Sort by frequency (highest to lowest)
    # This uses the numbers from the {word: number} JSON
    new_words.sort(key=lambda w: wordFreqDict[w], reverse=True)

    return new_words


def getDeckCards(deckName):
    # 1. Find all card IDs in the deck
    # Use a query to target the specific deck
    query = f'deck:"{deckName}"'
    card_ids = ankiConnect.invoke("findCards", query=query)

    if not card_ids:
        print(f"No cards found in deck: {deckName}. Starting with empty vault.")
        return {}

    # 2. Get the actual text from the cards
    cards_info = ankiConnect.invoke("cardsInfo", cards=card_ids)

    # Extract the 'Front' field (or 'Expression').
    raw_words = set()
    for card in cards_info:
        field_text = card["fields"]["Front"]["value"]
        # Basic cleanup: remove simple punctuation
        clean_text = field_text.replace(".", "").replace(",", "").strip()
        raw_words.add(clean_text)

    print(
        f"Captured {len(raw_words)} unique words from Anki. Sending to them Gemini..."
    )

    return raw_words


def compWordsToAnki(ankiWords, localWords):
    # 1. Flatten all surface forms from the JSON into one set
    known_forms = {word for forms in localWords.values() for word in forms}

    # 2. Return the difference: Words in Anki NOT found in the local vault
    return ankiWords - known_forms


def merge_and_save_lemmas(file_path, new_lemma_data):
    # 1. Start with an empty dictionary or the existing file content
    if os.path.exists(file_path):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                vault = json.load(f)
        except json.JSONDecodeError:
            vault = {}
    else:
        vault = {}

    # 2. Update the vault with new intelligence
    for lemma, new_words in new_lemma_data.items():
        if lemma in vault:
            # Combine existing list and new list, then use set() to kill duplicates
            combined = set(vault[lemma]) | set(new_words)
            vault[lemma] = sorted(list(combined))
        else:
            # New Lemma discovered, establish a new entry
            vault[lemma] = sorted(list(set(new_words)))

    # 3. Write the cumulative data back to the disk
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(vault, f, indent=4, ensure_ascii=False)

    print(f"Update Complete. {file_path} now contains {len(vault)} lemmas.")
    return vault

