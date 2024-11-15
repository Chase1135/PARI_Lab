import asyncio
import websockets

async def test_connection():
    uri = "ws://localhost:5000/ws/textual"  # Change to your WebSocket endpoint
    async with websockets.connect(uri) as websocket:
        while True:
            # Ask for user input or send a message automatically
            message = input("Enter message to send (or 'exit' to quit): ")
            
            # If the user types 'exit', break the loop and close the connection
            if message.lower() == 'exit':
                print("Exiting...")
                break
            
            # Send the message
            await websocket.send(f'{{"message": "{message}"}}')
            
            # Receive and print the response
            response = await websocket.recv()
            print(f"Response: {response}")

asyncio.run(test_connection())
