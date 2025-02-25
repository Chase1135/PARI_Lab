from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from contextlib import asynccontextmanager
import json, asyncio, sys, os, httpx, time
from response_generator import generate_response, wav_generation_test_response, preload_llm
from handlers import DEFAULT_HANDLERS, DEFAULT_INPUTS

sys.path.append(os.path.abspath('Text-to-Speech'))
from PlayHD import generate_speech, wav_to_bytes

CHUNK_SIZE = 4096

app = FastAPI()

# Pings startup endpoint to preload LLM
async def notify_startup():
    await asyncio.sleep(2)
    async with httpx.AsyncClient() as client:
        try:
            await client.get("http://localhost:5000/startup")
            print("Ollama preloaded", flush=True)
            
        except httpx.ConnectError:
            print("Failed to reach startup endpoint.", flush=True)

# Specifies events to take place at app startup and shutdown
@asynccontextmanager
async def lifespan(app: FastAPI):
    #asyncio.create_task(notify_startup())
    yield # Events after yield occur at shutdown
    print("Shutting down...", flush=True)

app.router.lifespan_context = lifespan

# Processes metadata received to route data to correct handler, along with
# utilizing correct method to receive data (i.e. whether data is chunked or not)
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

# Startup endpoint to handle Ollama initialization
@app.get("/startup")
async def startup():
    await preload_llm()
    return "Ollama preloading..."

# Generic Endpoint
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

            # Generate response from LLM
            response = await generate_response()

            # Generate .wav file from response
            print(f"LLM Generated Response: {response}")
            await generate_speech(response)

            # Convert .wav file to raw PCM data
            params, frames = wav_to_bytes("Text-to-Speech/playhtTest.wav")

            # Grab headers to send as metadata
            if params and frames:
                metadata = {
                    "nchannels": params.nchannels,
                    "sampwidth": params.sampwidth,
                    "framerate": params.framerate,
                    "nframes": params.nframes
                }

            # Send .wav headers
            await websocket.send_text(json.dumps(metadata))

            # Send audio frames
            for i in range(0, len(frames), CHUNK_SIZE):
                await websocket.send_bytes(frames[i:i+CHUNK_SIZE])

            # Send "END" indicating end of transmission
            await websocket.send_text("END")
            
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
 
                # Generate response
                start_llm = time.perf_counter()
                response_text = await wav_generation_test_response(data) # Generate the response from LLM
                llm_time = time.perf_counter() - start_llm
                print(f"LLM Response Time: {llm_time:.6f} seconds", flush=True)
                print(f"Generated response: {response_text}", flush=True)
                

                # Convert generated response to .wav and then to raw PCM data
                start_speech = time.perf_counter()
                await generate_speech(response_text)
                speech_time = time.perf_counter() - start_speech
                print(f"Speech Generation Time: {speech_time:.6f} seconds", flush=True)

                start_wav = time.perf_counter()
                params, frames = wav_to_bytes("Text-to-Speech/playhtTest.wav")
                wav_time = time.perf_counter() - start_wav
                print(f"WAV Processing Time: {wav_time:.6f} seconds", flush=True)

                if params and frames:
                    # Convert headers to JSON format
                    metadata = {
                        "nchannels": params.nchannels,
                        "sampwidth": params.sampwidth,
                        "framerate": params.framerate,
                        "nframes": params.nframes
                    }

                    start_transmission = time.perf_counter()
                    await websocket.send_text(json.dumps(metadata)) # Send headers

                    chunk_size = 4096 # Must chunk audio frames to reduce size of message
                    for i in range(0, len(frames), chunk_size):
                        await websocket.send_bytes(frames[i:i+chunk_size])

                    await websocket.send_text("END") # Indicate end of transmission
                    transmission_time = time.perf_counter() - start_transmission
                    print(f"Transmission Time: {transmission_time:.6f} seconds", flush=True)

                    total_time = llm_time + speech_time + wav_time + transmission_time
                    print(f"Total Time: {total_time:.6f} seconds", flush=True)

            except asyncio.TimeoutError: 
                await websocket.send_text("Ping") 
                print("Ping sent",flush=True)
                
    except Exception as e:
        if type(e) is not WebSocketDisconnect:
            print(f"Error in textual endpoint: {e}", flush=True)