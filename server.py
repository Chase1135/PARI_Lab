from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import json, asyncio
from LLM.response_generator import generate_response, wav_generation_test_response
from processors import DEFAULT_PROCESSORS, CUSTOM_PROCESSORS
from TTS.PlayHD import generate_speech, wav_to_bytes
from abc import ABC, abstractmethod
from utils import Benchmark

app = FastAPI()

"""List of sockets to be opened within a given run"""
SOCKETS = [
    {"name": "textual", "modality": "textual"},
    {"name": "audio", "modality": "audio", "handler": "audio"},
    {"name": "visual", "modality": "visual"},
    {"name": "physical", "modality": "physical", "handler": "physical"}
]

CHUNK_SIZE = 4096 # Size of chunks to transmit audio frames

"""Audio Headers"""
NCHANNELS = 1 # Number of channels (i.e. Monoaudio)
SAMPWIDTH = 2 # Number of bytes per sample
FRAMERATE = 48000 # Rate of play

"""Config endpoint to transmit necessary parameters to Unreal Engine"""
@app.get("/config")
async def get_config():
    # Grab the name of each endpoint
    open_sockets = [socket["name"] for socket in SOCKETS]

    # Parameters that Unreal Engine needsa
    CONFIG_DATA = {
        "open_sockets": open_sockets,
        "nchannels": NCHANNELS,
        "sampwidth": SAMPWIDTH,
        "framerate": FRAMERATE
    }
        
    return CONFIG_DATA

"""Base class for WebSocket handlers"""
class BaseSocketHandler(ABC):
    def __init__(self, websocket: WebSocket, socket_name, modality):
        self.websocket = websocket
        self.socket_name = socket_name
        self.modality = modality

        # Assign processor function dynamically
        self.processor = CUSTOM_PROCESSORS.get(socket_name, DEFAULT_PROCESSORS[modality])

    async def accept_connection(self):
        """Accepts the WebSocket connection"""
        await self.websocket.accept()
        asyncio.create_task(self.keep_alive())

    async def keep_alive(self, interval: int = 20):
        """Sends periodic pings to keep the WebSocket alive"""
        while True:
            try:
                await self.websocket.send_text("Ping")
                print("Ping sent", flush=True)
                await asyncio.sleep(interval)
            except WebSocketDisconnect:
                break
            except Exception as e:
                print(f"Error: {e}", flush=True)
                break

    async def process_data(self, data):
        print(f"Received message for {self.socket_name} ({self.modality})")
        self.processor.process(data)

    @abstractmethod
    async def handle_message(self):
        raise NotImplementedError("Handler not implemented.")

"""Handles textual WebSocket connections"""
class TextualSocket(BaseSocketHandler):
    async def handle_message(self):
        await self.accept_connection()

        """
        while True:
            try:
                data = await self.websocket.receive_text()
                print(f"Received raw data: {data}", flush=True)
                if data.lower() == "pong": # Heartbeat technique, pong just keeps the socket alive
                    print("Pong received", flush=True)
                    continue

                await self.process_data(data=data)

                response_text = await generate_response()

                await generate_speech(response_text)
                params, frames = wav_to_bytes("TTS/playhtTest.wav")

                if params and frames:
                    # Convert headers to JSON format
                    metadata = {
                        "nchannels": params.nchannels,
                        "sampwidth": params.sampwidth,
                        "framerate": params.framerate,
                        "nframes": params.nframes
                    }

                await self.websocket.send_text(json.dumps(metadata)) # Send headers

                chunk_size = 4096 # Must chunk audio frames to reduce size of message
                for i in range(0, len(frames), chunk_size):
                    await self.websocket.send_bytes(frames[i:i+chunk_size])

                await self.websocket.send_text("END") # Indicate end of transmission
                print(f"Total processing time for this iteration: {Benchmark.get_total_time():.6f} seconds")

            except Exception as e:
                print(f"Error in textual endpoint: {e}", flush=True)
                break

            finally:
                if self.websocket.client_state == 1:
                    await self.websocket.close()
        """
        
        try:
            while True:
                try:
                    #grab data, convert to json, print to confirm
                    data = await self.websocket.receive_text()
                    print(f"Received raw data: {data}", flush=True)
                    if data.lower() == "pong": # Heartbeat technique, pong just keeps the socket alive
                        print("Pong received", flush=True)
                        continue
    
                    # Generate response
                    response_text = await wav_generation_test_response(data) # Generate the response from LLM
                    print(f"Generated response: {response_text}", flush=True)
                    

                    # Convert generated response to .wav and then to raw PCM data
                    await generate_speech(response_text)
                    params, frames = wav_to_bytes("TTS/playhtTest.wav")

                    if params and frames:
                        # Convert headers to JSON format
                        metadata = {
                            "nchannels": params.nchannels,
                            "sampwidth": params.sampwidth,
                            "framerate": params.framerate,
                            "nframes": params.nframes
                        }

                        await self.websocket.send_text(json.dumps(metadata)) # Send headers

                        chunk_size = 4096 # Must chunk audio frames to reduce size of message
                        for i in range(0, len(frames), chunk_size):
                            await self.websocket.send_bytes(frames[i:i+chunk_size])

                        await self.websocket.send_text("END") # Indicate end of transmission

                except asyncio.TimeoutError: 
                    await self.websocket.send_text("Ping") 
                    print("Ping sent",flush=True)
                    
        except Exception as e:
            if type(e) is not WebSocketDisconnect:
                print(f"Error in textual endpoint: {e}", flush=True)
        
        
    
"""Handles audio WebSocket connections"""
class AudioSocket(BaseSocketHandler):
    async def handle_message(self):
        return await super().handle_message()
    
"""Handles visual WebSocket connections"""
class VisualSocket(BaseSocketHandler):
    async def handle_message(self):
        return await super().handle_message()
    
"""Handles physical WebSocket connections"""
class PhysicalSocket(BaseSocketHandler):
    async def handle_message(self):
        return await super().handle_message()

"""Example of a custom-built socket"""
class CustomSocket(BaseSocketHandler):
    async def handle_message(self):
        return await super().handle_message()


# Defines the set of default receivers for each modality
DEFAULT_HANDLERS = {
    "textual": TextualSocket,
    "audio": AudioSocket,
    "visual": VisualSocket,
    "physical": PhysicalSocket
}
# Defines the set of custom receivers mapping to SOCKETS['receiver']
CUSTOM_HANDLERS = {
    "audio": CustomSocket,
    "physical": CustomSocket
}

# Initializes the sockets listed in SOCKETS, sets their handler
def initialize_sockets():
    for socket in SOCKETS:
        input_name = socket["name"]
        modality = socket["modality"]

        # Check for custom receiver defined
        # If not, use default modality receiver
        handler_class = CUSTOM_HANDLERS.get(socket.get("handler"), DEFAULT_HANDLERS[modality])
        
        # Register route
        async def websocket_handler(websocket: WebSocket, handler_class=handler_class):
            handler = handler_class(websocket, input_name, modality)
            await handler.handle_message()

        app.add_api_websocket_route(f"/ws/{input_name}", websocket_handler)
        print(f"Endpoint registered: {input_name}", flush=True)


initialize_sockets()




"""
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
"""
