import asyncio
import websockets
import json
import wave
from PlayHD import generate_speech

async def test_connection():
    uri = "ws://localhost:5000/ws/textual" 
    async with websockets.connect(uri, ping_interval=20, ping_timeout=40) as websocket:
        while True:
            message = input("Enter message to send (or 'exit' to quit): ")

            if message.lower() == 'exit':
                print("Exiting...")
                break

            await websocket.send(message)

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

                with wave.open("Text-to-Speech/wav_reconstruction_text.wav", "wb") as wf:
                    wf.setnchannels(metadata["nchannels"])
                    wf.setsampwidth(metadata["sampwidth"])
                    wf.setframerate(metadata["framerate"])
                    wf.writeframes(audio_data)

                print(".wav successfully reconstructed")

            except websockets.exceptions.ConnectionClosedError as e:
                print(f"Connection closed with error: {e}")
                break


if __name__ == "__main__":
    asyncio.run(test_connection())
