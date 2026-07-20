"""In-memory metrics, tracing and health contracts with no autonomous sampling."""
from dataclasses import dataclass
from time import perf_counter
from typing import Protocol
@dataclass(frozen=True, slots=True)
class HealthStatus: name: str; healthy: bool; detail: str=""
class HealthCheck(Protocol):
    def check(self) -> HealthStatus: ...
class Metrics:
    def __init__(self): self._values: dict[str,float]={}
    def increment(self, name: str, value: float=1) -> None: self._values[name]=self._values.get(name,0)+value
    def snapshot(self) -> dict[str,float]: return dict(self._values)
class Tracer:
    def start(self, name: str) -> "Span": return Span(name, perf_counter())
@dataclass(frozen=True, slots=True)
class Span: name: str; started: float
def run_health_checks(*checks: HealthCheck) -> tuple[HealthStatus,...]: return tuple(check.check() for check in checks)
