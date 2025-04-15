from abc import ABC, abstractmethod
from utils import Benchmark
import asyncio
from LLM.response_generator import generate_response
from TTS.PlayHD import generate_speech
from buffers import INBOUND_BUFFERS, OUTBOUND_BUFFERS

"""Base class for all processors"""
class BaseProcessor(ABC):
    @abstractmethod
    async def process(self, data):
        raise NotImplementedError("Processor not implemented.")
    
    async def process_pipeline(self):
        response_text = await generate_response()
        print(f"Generated response: {response_text}", flush=True)
        audio_data = await generate_speech(response_text)

        OUTBOUND_BUFFERS["textual"].append(response_text)
        OUTBOUND_BUFFERS["audio"].append(audio_data)
    
"""Default textual modality processor"""
class TextualProcessor(BaseProcessor):
    @Benchmark.time_execution
    async def process(self, data):
        print(f"Processing textual data: {data}", flush=True)
        INBOUND_BUFFERS["textual"].append(data)

        asyncio.create_task(self.process_pipeline())

"""Default audio modality processor"""
class AudioProcessor(BaseProcessor):
    @Benchmark.time_execution
    async def process(self, data):
        print(f"Processing audio data: {data}", flush=True)
        INBOUND_BUFFERS["audio"].append(data)

"""Default visual modality processor"""
class VisualProcessor(BaseProcessor):
    @Benchmark.time_execution
    async def process(self, data):
        print(f"Processing visual data: {len(data)}", flush=True)
        INBOUND_BUFFERS["visual"].append(data)

"""Default physical modality processor"""
class PhysicalProcessor(BaseProcessor):
    @Benchmark.time_execution
    async def process(self, data):
        print(f"Processing physical data: {data}", flush=True)
        INBOUND_BUFFERS["physical"].append(data)

"""Example of a custom-built socket"""
class CustomProcessor(BaseProcessor):
    @Benchmark.time_execution
    async def process(self, data):
        return super().process(data)

DEFAULT_PROCESSORS = {
    "textual": TextualProcessor(),
    "audio": AudioProcessor(),
    "visual": VisualProcessor(),
    "physical": PhysicalProcessor()
}

CUSTOM_PROCESSORS = {
    "custom": CustomProcessor()
}