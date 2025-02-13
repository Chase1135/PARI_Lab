from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import json, asyncio, sys, os
from response_generator import generate_response, wav_generation_test_response
from handlers import DEFAULT_HANDLERS, DEFAULT_INPUTS

sys.path.append(os.path.abspath('Text-to-Speech'))
from PlayHD import generate_speech, wav_to_bytes

CHUNK_SIZE = 4096

app = FastAPI()

async def handle_metadata(metadata: dict, websocket: WebSocket):
    name = metadata.get("name")
    modality = metadata.get("modality")
    chunked = metadata.get("chunked", False)

    # Check if there is a specific handler for the given metadata
    # If not, assign to default handler for associated modality
    if 'handler' not in metadata:
        handler = DEFAULT_HANDLERS[modality]
    else:
        handler = DEFAULT_INPUTS['handler']

    # If data is chunked, gather into a buffer
    # Otherwise, just receive the data
    if chunked:
        data = b""
        while True:
            chunk = await websocket.receive_bytes()
            if chunk == "END":
                break

            data += chunk
    else:
        data = await websocket.receive_text()

    # Call previously assigned handler with the given data
    handler(data)


@app.websocket("/ws/generic")
async def websocket_generic_endpoint(websocket: WebSocket):
    await websocket.accept()

    while True:
        try:
            message = await asyncio.wait_for(websocket.receive_text(), timeout=30.0)
            print(f"Message received: {message}", flush=True)

            if message.lower() == "pong": # Heartbeat
                    print("Received heartbeat 'pong'")
                    continue

            # Metadata will contain the name of sensory input and its modality
            # Routed to correct handler based on metadata
            try:
                metadata = json.loads(message)
                if isinstance(metadata, dict):
                    print(f"Metadata parsed: {metadata}")
                    await handle_metadata(metadata, websocket)

            except json.JSONDecodeError:
                print(f"Received text message: {message}", flush=True)

            response = await generate_response()
            await websocket.send_text(response)
            
        except asyncio.TimeoutError:
            await websocket.send_text("Ping")
            print("Ping sent", flush=True)
        except WebSocketDisconnect as e:
            print(f"Client disconnected with code {e.code}", flush=True)
            break

#TEXTUAL ENDPOINT
@app.websocket("/ws/textual")
async def websocket_textual_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            try:
                #grab data, convert to json, print to confirm
                data = await asyncio.wait_for(websocket.receive_text(), timeout=30.0)
                print(f"Received raw data: {data}", flush=True)
                if data.lower() == "pong": # Heartbeat technique, pong just keeps the socket alive
                    continue
 
                response_text = await wav_generation_test_response(data) # Generate the response from LLM
                print(f"Generated response: {response_text}", flush=True)

                # Convert generated response to .wav and then to raw PCM data
                await generate_speech(response_text)
                params, frames = wav_to_bytes("Text-to-Speech/playhtTest.wav")

                if params and frames:
                    # Convert headers to JSON format
                    metadata = {
                        "nchannels": params.nchannels,
                        "sampwidth": params.sampwidth,
                        "framerate": params.framerate,
                        "nframes": params.nframes
                    }
                    await websocket.send_text(json.dumps(metadata)) # Send headers
                    print("Sent metadata", flush=True)

                    chunk_size = 4096 # Must chunk audio frames to reduce size of message
                    for i in range(0, len(frames), chunk_size):
                        await websocket.send_bytes(frames[i:i+chunk_size])

                    await websocket.send_text("END") # Indicate end of transmission
                    print("Sent audio frames",flush=True)

            except asyncio.TimeoutError: 
                await websocket.send_text("Ping") 
                print("Ping sent",flush=True)
                
    except Exception as e:
        if type(e) is not WebSocketDisconnect:
            print(f"Error in textual endpoint: {e}", flush=True)