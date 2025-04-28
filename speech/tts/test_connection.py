import asyncio
import websockets
import json
import wave
import requests
import time
import os

# Main function to launch both WebSockets
async def main():
    # Fetch config data
    config_raw = requests.get("http://localhost:8000/config")
    config = config_raw.json()
    print("Config:", config)

    # Extract audio parameters
    nchannels = config.get('nchannels')
    sampwidth = config.get('sampwidth')
    framerate = config.get('framerate')

    while True:
        msg = input("Enter message:")

        requests.post(url="http://localhost:8000/textual", json={"data": msg})

        audio_data = b""
        while True:
            data_raw = requests.get(url="http://localhost:8000/audio", stream=True)

            if data_raw.status_code == 204:
                print("No audio ready, sleeping...")
                time.sleep(1)
                continue

            audio_data += data_raw.content
            break

        # Save received audio to a .wav file
        with wave.open("wav_reconstruction_text.wav", "wb") as wf:
            wf.setnchannels(1)
            wf.setsampwidth(sampwidth)
            wf.setframerate(framerate)
            wf.writeframes(audio_data)

        print(".wav successfully reconstructed")


# Function to send audio data to the server
def send_audio_data(wav_path="Test.wav", endpoint="http://localhost:5000/audio"):
    try:
        audio_path = os.path.abspath(wav_path)
        with wave.open(audio_path, "rb") as wf:
            frames = wf.readframes(wf.getnframes())

        response = requests.post(endpoint, data=frames)

        if response.status_code == 200:
            print("[INFO] Audio successfully sent.")
        else:
            print(f"[ERROR] Failed to send audio. Status code: {response.status_code}")
    except Exception as e:
        print(f"[ERROR] Exception while sending audio: {e}")


# Main function to test audio transmission and retrieval
async def audio_main():
    config_raw = requests.get("http://localhost:5000/config")
    config = config_raw.json()
    print("Config:", config)

    # Extract audio parameters
    nchannels = config.get('nchannels')
    sampwidth = config.get('sampwidth')
    framerate = config.get('framerate')

    # Step 1: Send the audio
    send_audio_data()

    # Step 2: Try retrieving the audio from the server
    while True:
        data_raw = requests.get(url="http://localhost:5000/audio", stream=True)

        if data_raw.status_code == 204:
            print("No audio ready, sleeping...")
            time.sleep(1)
            continue

        # Save retrieved audio
        with wave.open("TTS/wav_reconstructed_from_harvard.wav", "wb") as wf:
            wf.setnchannels(1)
            wf.setsampwidth(sampwidth)
            wf.setframerate(framerate)
            wf.writeframes(data_raw.content)

        print("[SUCCESS] .wav reconstructed from server response.")
        break
        
def inspect_wav(filepath):
    with wave.open(filepath, 'rb') as wf:
        channels = wf.getnchannels()
        sample_width = wf.getsampwidth()
        framerate = wf.getframerate()
        num_frames = wf.getnframes()
        duration = num_frames / framerate

        print(f"File: {filepath}")
        print(f"Channels: {channels}")
        print(f"Sample Width (bytes): {sample_width}")
        print(f"Frame Rate (Hz): {framerate}")
        print(f"Number of Frames: {num_frames}")
        print(f"Duration (seconds): {duration:.2f}")


def check_exr():
    import OpenEXR
    import Imath
    import numpy as np
    from PIL import Image

    # Load the .exr file
    exr_file = OpenEXR.InputFile('righteye.exr')

    # Get the image dimensions
    dw = exr_file.header()['dataWindow']
    size = (dw.max.x - dw.min.x + 1, dw.max.y - dw.min.y + 1)

    # Read RGB channels
    channels = ['R', 'G', 'B']
    exr_data = {c: exr_file.channel(c, Imath.PixelType(Imath.PixelType.FLOAT)) for c in channels}

    # Convert to numpy array
    rgb = np.zeros((size[1], size[0], 3), dtype=np.float32)
    for i, c in enumerate(channels):
        rgb[..., i] = np.frombuffer(exr_data[c], dtype=np.float32).reshape(size[1], size[0])

    # Normalize and convert to 8-bit image for viewing
    rgb_normalized = (np.clip(rgb / np.percentile(rgb, 99), 0, 1) * 255).astype(np.uint8)
    
    # Convert to a Pillow image and show it
    image = Image.fromarray(rgb_normalized, mode='RGB')  # <-- Explicitly specify RGB mode
    image.save("debug_output.jpg", format="JPEG")

    print(f"Pixel range: {np.min(rgb)} - {np.max(rgb)} (pre-normalization)")
    print(f"Normalized range: {np.min(rgb_normalized)} - {np.max(rgb_normalized)}")




if __name__ == "__main__":
    asyncio.run(main())
    #asyncio.run(audio_main())
    #inspect_wav(os.path.abspath("Test.wav"))
    #check_exr()
