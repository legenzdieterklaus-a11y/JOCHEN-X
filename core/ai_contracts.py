"""AI provider contracts only; no provider implementation or model loading."""

from collections.abc import AsyncIterator
from enum import StrEnum
from typing import Protocol


class AICapability(StrEnum):
    TEXT = "text"
    EMBEDDING = "embedding"
    VISION = "vision"
    TOOLS = "tools"
    STREAMING = "streaming"
    SPEECH = "speech"
    TRANSCRIPTION = "transcription"


class Model(Protocol):
    identifier: str
    capabilities: frozenset[AICapability]


class Provider(Protocol):
    identifier: str
    models: tuple[Model, ...]


class EmbeddingProvider(Protocol):
    async def embed(self, text: str) -> tuple[float, ...]: ...


class VisionProvider(Protocol):
    pass


class ToolCallingProvider(Protocol):
    pass


class StreamingProvider(Protocol):
    def stream(self, prompt: str) -> AsyncIterator[str]: ...


class SpeechProvider(Protocol):
    pass


class TranscriptionProvider(Protocol):
    pass


class ProviderRouter(Protocol):
    def select(self, capability: AICapability) -> Provider: ...
