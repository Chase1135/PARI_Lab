from pyht import Client
from pyht.client import TTSOptions
import asyncio
import wave

from config import PLAYHT_USER_ID, PLAYHT_API_KEY

# William voice
options = TTSOptions(voice="s3://mockingbird-prod/william_3_d2b62fd7-a52d-4bd1-a09a-fb2748eda979/voices/william_3/manifest.json")

# Generate the .wav file for the filler response
async def generate_filler_response():
    client = Client(
        user_id=PLAYHT_USER_ID,
        api_key=PLAYHT_API_KEY
    )

    filler_text = "Let me think about that for a moment!"

    try:
        with wave.open("Text-to-Speech/filler_response.wav", "wb") as wf:
            # Headers for .wav to ensure proper playback when reconstructed
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(48000)

            # Generate speech in chunks
            for chunk in client.tts(filler_text, options, voice_engine='PlayDialog', protocol='http'):
                if chunk:
                    wf.writeframes(chunk)
                else:
                    break

        print("Filler response saved as: filler_response.wav")

    except Exception as e:
        print(f"Error generating filler response: {e}")

    finally:
        client.close()

# Run the async function
if __name__ == "__main__":
    asyncio.run(generate_filler_response())