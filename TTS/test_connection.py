import asyncio
import websockets
import json
import wave
import requests

AUDIO_URI = "ws://localhost:5000/ws/audio"
TEXTUAL_URI = "ws://localhost:5000/ws/textual"

# Function to handle user input and send it over the textual WebSocket
async def user_input_loop(websocket):
    while True:
        message = await asyncio.to_thread(input, "Enter message to send (or 'exit' to quit): ")

        if message.lower() == 'exit':
            print("Exiting...")
            await websocket.close()
            break
        
        await websocket.send(message)

# Function to handle the textual WebSocket
async def textual_socket():
    async with websockets.connect(TEXTUAL_URI) as websocket:
        # Start the user input loop as a background task
        asyncio.create_task(user_input_loop(websocket))

        while True:
            try:
                message = await websocket.recv()

                if message.lower() == "ping":
                    await websocket.send("pong")
                    print("Pong sent (Textual)", flush=True)
                    continue  # Ignore pings

                print(f"Server response (Textual): {message}")

            except websockets.exceptions.ConnectionClosedError as e:
                print(f"Textual WebSocket closed with error: {e}")
                break

# Function to handle the audio WebSocket
async def audio_socket(nchannels, sampwidth, framerate):
    async with websockets.connect(AUDIO_URI) as websocket:
        while True:
            try:
                message = await websocket.recv()

                if message.lower() == "ping":
                    await websocket.send("pong")
                    print("Pong sent (Audio)", flush=True)
                    continue  # Ignore pings

                audio_data = b""  # Buffer to store received audio frames

                while True:
                    chunk = await websocket.recv()
                    
                    if chunk == "END":  # Stop receiving
                        break

                    audio_data += chunk  # Append to buffer

                # Save received audio to a .wav file
                with wave.open("TTS/wav_reconstruction_text.wav", "wb") as wf:
                    wf.setnchannels(nchannels)
                    wf.setsampwidth(sampwidth)
                    wf.setframerate(framerate)
                    wf.writeframes(audio_data)

                print(".wav successfully reconstructed")

            except websockets.exceptions.ConnectionClosedError as e:
                print(f"Audio WebSocket closed with error: {e}")
                break

# Main function to launch both WebSockets
async def main():
    # Fetch config data
    config_raw = requests.get("http://localhost:5000/config")
    config = config_raw.json()
    print("Config:", config)

    # Extract audio parameters
    nchannels = config.get('nchannels')
    sampwidth = config.get('sampwidth')
    framerate = config.get('framerate')

    # Run both textual and audio WebSocket handlers concurrently
    await asyncio.gather(
        textual_socket(),
        audio_socket(nchannels, sampwidth, framerate)
    )

if __name__ == "__main__":
    asyncio.run(main())
