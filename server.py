import asyncio
from fastapi import FastAPI, APIRouter, Request, Response
from pydantic import BaseModel
from data.processors import DEFAULT_PROCESSORS, CUSTOM_PROCESSORS
from data.buffers import OUTBOUND_BUFFERS
from abc import ABC, abstractmethod
from utils.utils import Benchmark

from config import SERVER_HOST, SERVER_PORT, ENDPOINTS, GET_MODALITIES, NCHANNELS, SAMPWIDTH, FRAMERATE, VISUAL_INTERVAL, PHYSICAL_INTERVAL
from data.mongodb import store_config

app = FastAPI()

"""Config endpoint to transmit necessary parameters to Unreal Engine"""
@app.get("/config")
async def get_config():
    # Grab the name of each endpoint
    open_endpoints = [endpoint["name"] for endpoint in ENDPOINTS]
    post_intervals = {
        "visual": VISUAL_INTERVAL,
        "physical": PHYSICAL_INTERVAL
    }
    get_modalities = GET_MODALITIES

    # Parameters that Unreal Engine needsa
    CONFIG_DATA = {
        "open_endpoints": open_endpoints,
        "post_intervals": post_intervals,
        "get_modalities": get_modalities,
        "nchannels": NCHANNELS,
        "sampwidth": SAMPWIDTH,
        "framerate": FRAMERATE
    }

    store_config()
        
    return CONFIG_DATA

class TextPayload(BaseModel):
    data: str

class BaseRESTHandler(ABC):
    def __init__(self, name: str, modality: str):
        self.name = name
        self.modality = modality
        self.router = APIRouter()
        self.processor = CUSTOM_PROCESSORS.get(name, DEFAULT_PROCESSORS[modality])
        self.register_routes()

    @abstractmethod
    def register_routes(self):
        pass

    async def process(self, data):
        await self.processor.process(data)

class TextualRESTHandler(BaseRESTHandler):
    def register_routes(self):
        @self.router.post(f"/{self.name}")
        async def receive_data(payload: TextPayload):
            print(f"[{self.name}] Received payload: {payload}", flush=True)
            asyncio.create_task(self.process(payload.data))
            return {"status": "received"}

        @self.router.get(f"/{self.name}")
        async def get_response():
            return Response(content=b"", status_code=204)

class AudioRESTHandler(BaseRESTHandler):
    def register_routes(self):
        @self.router.post(f"/{self.name}")
        async def receive_data(payload: Request):
            raw_audio = await payload.body()
            print(f"[{self.name}] Received audio data of length: {len(raw_audio)} bytes", flush=True)

            asyncio.create_task(self.process(raw_audio))
            return {"status": "received", "length": len(raw_audio)} 

        @self.router.get(f"/{self.name}")
        async def get_response():
            if OUTBOUND_BUFFERS["audio"]:
                raw_audio = OUTBOUND_BUFFERS["audio"].pop(0)
                print(f"Sending full audio of length: {len(raw_audio)} bytes")
                return Response(content=raw_audio, media_type="application/octet-stream")
            
            return Response(status_code=204)

class VisualRESTHandler(BaseRESTHandler):
    def register_routes(self):
        @self.router.post(f"/{self.name}")
        async def receive_data(payload: Request):
            raw_image = await payload.body()
            print(f"[{self.name}] Received visual data: {len(raw_image)} bytes")

            asyncio.create_task(self.process(raw_image))
            return {"status": "received", "size": len(raw_image)}

        @self.router.get(f"/{self.name}")
        async def get_response():
            return Response(content=b"", status_code=204)

class PhysicalRESTHandler(BaseRESTHandler):
    def register_routes(self):
        @self.router.post(f"/{self.name}")
        async def receive_data(payload: dict):
            print(f"[{self.name}] Received payload: {payload}", flush=True)
            asyncio.create_task(self.process(payload))
            return {"status": "received"}   

        @self.router.get(f"/{self.name}")
        async def get_response():
            return Response(content=b"", status_code=204)

# Defines the set of default receivers for each modality
DEFAULT_HANDLERS = {
    "textual": TextualRESTHandler,
    "audio": AudioRESTHandler,
    "visual": VisualRESTHandler,
    "physical": PhysicalRESTHandler
}
# Defines the set of custom receivers mapping to SOCKETS['receiver']
CUSTOM_HANDLERS = {
    "custom": TextualRESTHandler
}

def initialize_endpoints():
    for config in ENDPOINTS:
        name = config["name"]
        modality = config["modality"]
        handler_class = CUSTOM_HANDLERS.get(config.get("handler"), DEFAULT_HANDLERS[modality])
        handler = handler_class(name=name, modality=modality)
        app.include_router(handler.router)
        print(f"Registered REST Endpoint: /{name} (modality: {modality}) (handler: {handler.__class__.__name__})", flush=True)


initialize_endpoints()