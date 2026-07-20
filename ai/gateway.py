"""Provider-independent AI gateway metadata and routing infrastructure."""

from dataclasses import dataclass, field
from enum import StrEnum


class Capability(StrEnum):
    """Future model capabilities advertised without invoking a model."""
    TEXT = "text"
    VISION = "vision"
    EMBEDDING = "embedding"


@dataclass(frozen=True, slots=True)
class ModelDescriptor:
    """A provider model's static identity and capabilities."""
    provider_id: str
    model_id: str
    capabilities: frozenset[Capability]


@dataclass(frozen=True, slots=True)
class ProviderDescriptor:
    """Provider metadata; credentials and execution are intentionally absent."""
    identifier: str
    display_name: str
    models: tuple[ModelDescriptor, ...] = field(default_factory=tuple)


class ProviderRegistry:
    """Owns provider descriptors and rejects ambiguous identifiers."""
    def __init__(self) -> None:
        self._providers: dict[str, ProviderDescriptor] = {}
    def register(self, provider: ProviderDescriptor) -> None:
        if provider.identifier in self._providers:
            raise ValueError(f"Provider already registered: {provider.identifier}")
        self._providers[provider.identifier] = provider
    def all(self) -> tuple[ProviderDescriptor, ...]:
        return tuple(self._providers.values())


class RoutingEngine:
    """Selects registered model metadata by required capability only."""
    def __init__(self, providers: ProviderRegistry) -> None:
        self._providers = providers
    def candidates(self, capability: Capability) -> tuple[ModelDescriptor, ...]:
        return tuple(model for provider in self._providers.all() for model in provider.models if capability in model.capabilities)
