from abc import ABC, abstractmethod
import OpenEXR
import Imath
import numpy as np
from utils.utils import Benchmark
from llm.response_generator import generate_response
from speech.tts.playht import generate_speech
from speech.stt.speechflow import convert_speech_to_text
from data.buffers import INBOUND_BUFFERS, OUTBOUND_BUFFERS

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

        # Temp write to file
        with open("temp.exr", "wb") as f:
            f.write(data)

        # Read temp file
        exr_file = OpenEXR.InputFile("temp.exr")
        dw = exr_file.header()['dataWindow']
        size = (dw.max.x - dw.min.x + 1, dw.max.y - dw.min.y + 1)

        # Grab RGB channels
        channels = ['R', 'G', 'B']
        exr_data = {c: exr_file.channel(c, Imath.PixelType(Imath.PixelType.FLOAT)) for c in channels}

        # Convert to numpy array
        rgb = np.zeros((size[1], size[0], 3), dtype=np.float32)
        for i, c in enumerate(channels):
            rgb[..., i] = np.frombuffer(exr_data[c], dtype=np.float32).reshape(size[1], size[0])

        # Normalize and convert to 8-bit
        rgb_normalized = (np.clip(rgb / np.percentile(rgb, 99), 0, 1) * 255).astype(np.uint8)

        INBOUND_BUFFERS["visual"].append(rgb_normalized)

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