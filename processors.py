from abc import ABC, abstractmethod
from utils import Benchmark

DATA_BUFFERS = {
    "textual": [],
    "audio": [],
    "visual": [],
    "physical": []
}

"""Base class for all processors"""
class BaseProcessor(ABC):
    @abstractmethod
    async def process(self, data):
        raise NotImplementedError("Processor not implemented.")
    
"""Default textual modality processor"""
class TextualProcessor(BaseProcessor):
    @Benchmark.time_execution
    async def process(self, data):
        print(f"Processing textual data: {data}")
        DATA_BUFFERS["textual"].append(data)

"""Default audio modality processor"""
class AudioProcessor(BaseProcessor):
    @Benchmark.time_execution
    async def process(self, data):
        print(f"Processing audio data: {data}")
        DATA_BUFFERS["audio"].append(data)

"""Default visual modality processor"""
class VisualProcessor(BaseProcessor):
    @Benchmark.time_execution
    async def process(self, data):
        print(f"Processing visual data: {data}")
        DATA_BUFFERS["visual"].append(data)

"""Default physical modality processor"""
class PhysicalProcessor(BaseProcessor):
    @Benchmark.time_execution
    async def process(self, data):
        print(f"Processing physical data: {data}")
        DATA_BUFFERS["physical"].append(data)

"""Example of a custom-built socket"""
class CustomProcessor(BaseProcessor):
    @Benchmark.time_execution
    async def process(self, data):
        return super().process(data)

DEFAULT_PROCESSORS = {
    "textual": TextualProcessor,
    "audio": AudioProcessor,
    "visual": VisualProcessor,
    "physical": PhysicalProcessor
}

CUSTOM_PROCESSORS = {
    "custom": CustomProcessor
}