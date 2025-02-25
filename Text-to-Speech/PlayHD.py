from pyht import Client
from pyht.client import TTSOptions
import asyncio
import wave

# Jennifer - s3://voice-cloning-zero-shot/775ae416-49bb-4fb6-bd45-740f205d20a1/jennifersaad/manifest.json
# Saul (William) - s3://mockingbird-prod/william_3_d2b62fd7-a52d-4bd1-a09a-fb2748eda979/voices/william_3/manifest.json
# Select voice option for generation
# Saul -
options = TTSOptions(voice="s3://mockingbird-prod/william_3_d2b62fd7-a52d-4bd1-a09a-fb2748eda979/voices/william_3/manifest.json")

# Take input text and generate speech in the form of a .wav file
async def generate_speech(text):
    client = Client(
        user_id="I9inKjkH0CRfUbpQbRahudvCDZ92",
        api_key="af968b25edf8435bb65e2a9acb93e345"
    )

    # Open a file to save the audio
    try:
        with wave.open("Text-to-Speech/playhtTest.wav", "wb") as wf:
            
            # Headers for .wav to ensure proper playback when reconstructed
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(48000)

            #Create text chunk
            for chunk in client.tts(text, options, voice_engine='PlayDialog', protocol='http'):
                if chunk: # Make sure data is received
                    # Write the audio chunk to the file
                    wf.writeframes(chunk)
                else: # Stop if there is an empty chunk
                    break

        print("Audio saved as playhtTest.wav")

    except Exception as e:
        print(f"Error during TTS: {e}")

    finally:
        print("TTS complete")
        client.close()

# Take input .wav file path and turn .wav into bytes so that it may be transmitted across websocket
def wav_to_bytes(file_path):
    try: 
        with wave.open(file_path, 'rb') as wf: # Open .wav file in read mode
            params = wf.getparams() # Grab .wav headers
            print(params)
            frames = wf.readframes(wf.getnframes())
            return params, frames
    
    except wave.Error as e:
        print(f"Error reading WAV file: {e}")
    
    return None, None

# Converts bytes given to a .wav file, mainly for testing
def bytes_to_wav(params, frames, file_path):
    try:
        with wave.open(file_path, 'wb') as wf:
            wf.setparams(params)
            wf.writeframes(frames)

        print(f"Successfully wrote audio to {file_path}")
    
    except wave.Error as e:
        print(f"Error writing WAV file: {e}")


if __name__ == "__main__":
    asyncio.run(generate_speech("Sometimes it works, sometimes it doesn't."))

    params, frames = wav_to_bytes("Text-to-Speech/playhtTest.wav")
    if frames:
        print(f"Successfully read {len(frames)} bytes")

    bytes_to_wav(params, frames, "Text-to-Speech/bytes-to-wav-test.wav")