from abc import ABC, abstractmethod
from utils import Benchmark
from LLM.response_generator import generate_response
from TTS.PlayHD import generate_speech
from STT.SpeechFlow import convert_speech_to_text
from buffers import INBOUND_BUFFERS, OUTBOUND_BUFFERS

from config import MAX_VISUAL_HISTORY, MAX_PHYSICAL_HISTORY

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

        await self.process_pipeline()

"""Default audio modality processor"""
class AudioProcessor(BaseProcessor):
    @Benchmark.time_execution
    async def process(self, data):
        print(f"Processing audio data: {len(data)} bytes", flush=True)
        INBOUND_BUFFERS["audio"].append(data)

        converted_speech = await convert_speech_to_text()
        INBOUND_BUFFERS["textual"].append(converted_speech)

        await self.process_pipeline()

"""Default visual modality processor"""
class VisualProcessor(BaseProcessor):
    @Benchmark.time_execution
    async def process(self, data):
        print(f"Processing visual data: {len(data)} bytes", flush=True)
        INBOUND_BUFFERS["visual"].append(data)

        if len(INBOUND_BUFFERS["visual"]) > MAX_VISUAL_HISTORY:
            INBOUND_BUFFERS["visual"].pop(0)

"""Default physical modality processor"""
class PhysicalProcessor(BaseProcessor):
    @Benchmark.time_execution
    async def process(self, data):
        print(f"Processing physical data: {data}", flush=True)
        INBOUND_BUFFERS["physical"].append(data)

        if len(INBOUND_BUFFERS["physical"]) > MAX_PHYSICAL_HISTORY:
            INBOUND_BUFFERS["physical"].pop(0)

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