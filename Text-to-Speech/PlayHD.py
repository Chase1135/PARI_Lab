from pyht import Client
from pyht.client import TTSOptions

client = Client(
    user_id="iEwn6pNjtRQZ7HJih01l339RI102",
    api_key="86a6bbf9121049cea7ecf47d9774bccf"
)

# Jennifer - s3://voice-cloning-zero-shot/775ae416-49bb-4fb6-bd45-740f205d20a1/jennifersaad/manifest.json
# Select voice option for generation
options = TTSOptions(voice="s3://mockingbird-prod/william_3_d2b62fd7-a52d-4bd1-a09a-fb2748eda979/voices/william_3/manifest.json")


# Text to be translated
text = ("lmaoo")

# Open a file to save the audio
with open("playhtTestChase.wav", "wb") as audio_file:
    #Create text chunk
    for chunk in client.tts(text, options, voice_engine='PlayDialog', protocol='http'):
        # Write the audio chunk to the file
        audio_file.write(chunk)

print("Audio saved as playhtTest.wav")
