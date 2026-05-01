import os
from dotenv import load_dotenv
from google import genai
import json
import time


def initClient():
    load_dotenv()

    api_key = os.getenv("API_KEY")

    if not api_key:
        raise ValueError("API_KEY not found in env")

    client = genai.Client(api_key=api_key)
    return client


def closeClient(client):
    # CLose the client to release the resources
    client.close()


def sendPrompt(client, prompt, model):

    response = client.models.generate_content(model=model, contents=prompt)

    return response


def generateCardContextAI(
    client, uWords, kWords, context, model="gemini-3-flash-preview"
):
    wordPhrases = {}

    # 1. FLATTEN TARGETS: Convert {"lemma": ["word"]} -> ["word"]
    # This ensures the AI gets a clean list of strings to process
    targets = [word for list_of_words in uWords.values() for word in list_of_words]

    # 2. BATCHING: Smaller batches (5-8) usually yield higher i+1 quality
    batchSize = 8

    for i in range(0, len(targets), batchSize):
        batch = targets[i : i + batchSize]

        # 3. THE PROMPT
        # Ask for word, sentence, and translation in one shot.
        prompt = f"""
        ACT AS: Linguistic Professor (i+1 Specialist).
        CONTEXT: {context}
        KNOWN VOCAB: {list(kWords)[:100]} (Use these for the 'i' part).
        TARGET WORDS: {batch} (These are the '+1').

        TASK: For each TARGET WORD, create a very simple sentence.
        RULES:
        1. Only use 1 TARGET WORD per sentence.
        2. Keep the surrounding words extremely simple (A1/A2 level).
        3. Output MUST be valid JSON array of objects.

        FORMAT:
        [
          {{"word": "aurai", "sentence": "J'aurai une voiture demain.", "translation": "I will have a car tomorrow."}}
        ]
        """

        try:
            # 4. The response
            response = client.models.generate_content(model=model, contents=prompt)

            # Clean Markdown garbage
            clean_json = response.text.strip().replace("```json", "").replace("```", "")
            batch_result = json.loads(clean_json)

            # 5. MERGE: Structure it for your card creator
            for entry in batch_result:
                wordPhrases[entry["word"]] = {
                    "sentence": entry["sentence"],
                    "translation": entry["translation"],
                }

        except Exception as e:
            print(f"FAILED BATCH {i}: {e}. Retrying in 2s...")
            time.sleep(2)  # Prevent rate limiting
            continue

    return wordPhrases
