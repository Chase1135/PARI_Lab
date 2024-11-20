import asyncio
import websockets

async def test_connection():
    uri = "ws://192.168.1.125:5000/ws/textual" 
    async with websockets.connect(uri, ping_interval=10, ping_timeout=20) as websocket:
        while True:
            message = input("Enter message to send (or 'exit' to quit): ")
            await websocket.send(f'{{"message": "{message}"}}')
            
            try:
                response = await websocket.recv()
                print(f"Response: {response}")
            except websockets.exceptions.ConnectionClosedError as e:
                print(f"Connection closed with error: {e}")
                break

            if message.lower() == 'exit':
                print("Exiting...")
                break

asyncio.run(test_connection())
