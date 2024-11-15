import asyncio
import websockets

async def test_connection():
    uri = "ws://192.168.1.125:5000/ws/textual" 
    async with websockets.connect(uri) as websocket:
        while True:
            message = input("Enter message to send (or 'exit' to quit): ")
            
            await websocket.send(f'{{"message": "{message}"}}')
            
            response = await websocket.recv()
            print(f"Response: {response}")

            if message.lower() == 'exit':
                print("Exiting...")
                break

asyncio.run(test_connection())
