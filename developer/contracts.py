"""Ports consumed by the optional developer platform."""
from __future__ import annotations
from collections.abc import Iterable
from typing import Protocol
from core.events import EventDelivery
from core.registry import ServiceDescriptor
from core.observability import HealthStatus

class EventDiagnostics(Protocol):
    def delivery_history(self) -> tuple[EventDelivery, ...]: ...
class ServiceDiagnostics(Protocol):
    def descriptors(self) -> tuple[ServiceDescriptor, ...]: ...
class PluginDiagnostics(Protocol):
    def discover(self) -> Iterable[object]: ...
class HealthDiagnostics(Protocol):
    def health(self) -> Iterable[HealthStatus]: ...
