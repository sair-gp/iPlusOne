import asyncio
import edge_tts

TEXT = "Turning text into speech without the cloud-price tag."
VOICE = "en-US-GuyNeural"  # You can change this to French, etc.
OUTPUT_FILE = "mission_briefing.mp3"


async def generate_speech():
    # 1. Create the communication object
    communicate = edge_tts.Communicate(TEXT, VOICE)

    # 2. Save the audio to a file
    print(f"Generating audio...")
    await communicate.save(OUTPUT_FILE)
    print(f"Success: {OUTPUT_FILE} created.")


if __name__ == "__main__":
    # 3. Run the async function
    asyncio.run(generate_speech())
