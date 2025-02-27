import asyncio
import websockets
import json
import wave
import requests
import threading

def user_input_loop(websocket, loop):
    while True:
        message = input("Enter message to send (or 'exit' to quit): ")

        if message.lower() == 'exit':
                print("Exiting...")
                asyncio.run_coroutine_threadsafe(websocket.close(), loop)
                break
        
        asyncio.run_coroutine_threadsafe(websocket.send(message), loop)

# Test the Textual endpoint, primarily made in case of needing to demo .wav to Russ 
async def wav_test_generation():
    config_raw = requests.get("http://localhost:5000/config")
    config = config_raw.json()
    print(config)

    nchannels = config.get('nchannels')
    sampwidth = config.get('sampwidth')
    framerate = config.get('framerate')

    uri = "ws://localhost:5000/ws/textual" 
    
    async with websockets.connect(uri) as websocket:
        input_thread = threading.Thread(target=user_input_loop, args=(websocket, asyncio.get_event_loop()))
        input_thread.start()

        while True:
            try:
                metadata = await websocket.recv()

                if metadata.lower() == "ping":
                    await websocket.send("pong")
                    continue

                metadata = json.loads(metadata)
                audio_data = b"" # Buffer

                while True:
                    chunk = await websocket.recv()

                    if chunk == "END": # Stop receiving
                        break

                    audio_data += chunk # Append to buffer

                with wave.open("TTS/wav_reconstruction_text.wav", "wb") as wf:
                    wf.setnchannels(nchannels)
                    wf.setsampwidth(sampwidth)
                    wf.setframerate(framerate)
                    wf.writeframes(audio_data)

                print(".wav successfully reconstructed")

            except websockets.exceptions.ConnectionClosedError as e:
                print(f"Connection closed with error: {e}")
                break

if __name__ == "__main__":
    asyncio.run(wav_test_generation())
