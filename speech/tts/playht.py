from pyht import AsyncClient
from pyht import TTSOptions

from config import PLAYHT_USER_ID, PLAYHT_API_KEY

# Jennifer - options = TTSOptions(voice=s3://voice-cloning-zero-shot/775ae416-49bb-4fb6-bd45-740f205d20a1/jennifersaad/manifest.json)
# Saul (William) - s3://mockingbird-prod/william_3_d2b62fd7-a52d-4bd1-a09a-fb2748eda979/voices/william_3/manifest.json
# Select voice option for generation
# Saul -
options = TTSOptions(voice="s3://mockingbird-prod/william_3_d2b62fd7-a52d-4bd1-a09a-fb2748eda979/voices/william_3/manifest.json")

# Take input text and generate speech in the form of a .wav file
async def generate_speech(text):
    client = AsyncClient(
        user_id=PLAYHT_USER_ID,
        api_key=PLAYHT_API_KEY
    )
    audio_buffer = b""
    
    # Open a file to save the audio
    try:
        #Create text chunk
        async for chunk in client.tts(text, options, voice_engine='PlayDialog', protocol='http'):
            if chunk: # Make sure data is received
                audio_buffer += chunk
            else: # Stop if there is an empty chunk
                break

    except Exception as e:
        print(f"Error during TTS: {e}", flush=True)

    finally:
        await client.close()

    return audio_buffer