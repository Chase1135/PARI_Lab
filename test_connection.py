import asyncio
import websockets

async def test_connection():
    uri = "ws://192.168.1.125:5000/ws/textual" 
    async with websockets.connect(uri, ping_interval=20, ping_timeout=40) as websocket:
        while True:
            message = input("Enter message to send (or 'exit' to quit): ")
            #await websocket.send(f'{{"message": "{message}"}}')
            await websocket.send(message)

            try:
                async for chunk in websocket:
                    print(chunk, end="", flush=True)
                    if "[END OF RESPONSE]" in chunk:
                        print()
                        break
            except websockets.exceptions.ConnectionClosedError as e:
                print(f"Connection closed with error: {e}")
                break

            if message.lower() == 'exit':
                print("Exiting...")
                break

asyncio.run(test_connection())
