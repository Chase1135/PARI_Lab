from pyht import AsyncClient
from pyht import TTSOptions
import asyncio
import wave


"""
    Chase UserID and API Key (Free Trial)
    user_id="uXE8bhiuwZTRpIpPr8rGuTdu4mJ3"
    api_key="71f90348232d48c79f4ea79ed3fe4a3d"

    Will UserID and API Key (First Tier Sub) **Only use for demonstrations purposes** 
    user_id=iEwn6pNjtRQZ7HJih01l339RI102
    api_key=86a6bbf9121049cea7ecf47d9774bccf
"""
USER_ID = "uXE8bhiuwZTRpIpPr8rGuTdu4mJ3"
API_KEY = "71f90348232d48c79f4ea79ed3fe4a3d"
# Jennifer - options = TTSOptions(voice=s3://voice-cloning-zero-shot/775ae416-49bb-4fb6-bd45-740f205d20a1/jennifersaad/manifest.json)
# Saul (William) - s3://mockingbird-prod/william_3_d2b62fd7-a52d-4bd1-a09a-fb2748eda979/voices/william_3/manifest.json
# Select voice option for generation
# Saul -
options = TTSOptions(voice="s3://mockingbird-prod/william_3_d2b62fd7-a52d-4bd1-a09a-fb2748eda979/voices/william_3/manifest.json")

# Take input text and generate speech in the form of a .wav file
async def generate_speech(text):
    client = AsyncClient(
        user_id=USER_ID,
        api_key=API_KEY
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

# Take input .wav file path and turn .wav into bytes so that it may be transmitted across websocket
def wav_to_bytes(file_path):
    try: 
        with wave.open(file_path, 'rb') as wf: # Open .wav file in read mode
            params = wf.getparams() # Grab .wav headers
            frames = wf.readframes(wf.getnframes())
            return params, frames
    
    except wave.Error as e:
        print(f"Error reading WAV file: {e}", flush=True)
    
    return None, None


if __name__ == "__main__":
    #asyncio.run(generate_speech("Sometimes it works, sometimes it doesn't."))
    asyncio.run(generate_speech("Let me think about that for a moment"))
