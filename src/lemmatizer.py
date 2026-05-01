import wordComp
import json
import utils.ankiUtils as ankiUtils
import utils.genaiClient as gc

client = gc.initClient()

# Let the user pick the target
target_name, target_path = ankiUtils.loadDecks()

# Sync the chosen deck's data to the JSON vault
deckLemmas = ankiUtils.sync_anki_to_json(target_name, target_path, client)

wordList = wordComp.openWordList("data/commonWords.json")

print(f"Word list: {wordList}")

newWords = ankiUtils.compDecktoWordList(deckLemmas, wordList)

prompt = f"Generate text in JSON format that show the lemmas of the given words. The format is lemma:[array of words belonging to that lemma].No introductury text or conclussion. Only provided what was requested. Here are the words: {newWords}"

print(f"New words: {newWords}")
response = gc.sendPrompt(client, prompt, "gemini-3-flash-preview")
print(f"AI response: {response.text}")


raw = response.text.strip()
file_path = f"./data/lemmanized/newLemmasFor{target_name}.json"
if raw.startswith("```"):
    raw = raw.split("```")[1]  # remove code fences

data = json.loads(raw)


try:
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)
        print(f"Json file '{file_path}' was created.")
except FileExistsError:
    print("That file already exists!")

gc.closeClient(client)
