"""In-memory metrics, tracing and health contracts with no autonomous sampling."""

from collections.abc import Callable
from dataclasses import dataclass
from time import perf_counter
from typing import Protocol


@dataclass(frozen=True, slots=True)
class HealthStatus:
    name: str
    healthy: bool
    detail: str = ""


class HealthCheck(Protocol):
    def check(self) -> HealthStatus: ...


class Metrics:
    def __init__(self) -> None:
        self._values: dict[str, float] = {}

    def increment(self, name: str, value: float = 1) -> None:
        self._values[name] = self._values.get(name, 0) + value

    def record_duration(self, name: str, duration_ms: float) -> None:
        self._values[name] = duration_ms

    def snapshot(self) -> dict[str, float]:
        return dict(self._values)


class Tracer:
    def start(self, name: str) -> "Span":
        return Span(name, perf_counter())


@dataclass(frozen=True, slots=True)
class Span:
    name: str
    started: float


@dataclass(frozen=True, slots=True)
class ActivationFailure:
    """Structured failure diagnostic for plugin activation."""

    plugin_id: str
    phase: str
    reason: str
    context: dict[str, str]


_PLUGIN_STATE_HEALTH: dict[str, tuple[bool, str]] = {
    "started": (True, ""),
    "initialized": (True, "not yet started"),
    "failed": (False, "activation failed"),
    "stopped": (False, "degraded"),
    "unloaded": (False, "not loaded"),
}


class PluginHealthCheck:
    """HealthCheck Protocol implementation for plugin runtime status."""

    __slots__ = ("_plugin_id", "_state_supplier")

    def __init__(self, plugin_id: str, state_supplier: Callable[[], str]) -> None:
        self._plugin_id = plugin_id
        self._state_supplier = state_supplier

    def check(self) -> HealthStatus:
        state = self._state_supplier()
        healthy, detail = _PLUGIN_STATE_HEALTH.get(
            state, (False, f"unknown state: {state}"),
        )
        return HealthStatus(
            name=f"plugin.{self._plugin_id}",
            healthy=healthy,
            detail=detail,
        )


def run_health_checks(*checks: HealthCheck) -> tuple[HealthStatus, ...]:
    return tuple(check.check() for check in checks)


__all__ = [
    "ActivationFailure",
    "HealthCheck",
    "HealthStatus",
    "Metrics",
    "PluginHealthCheck",
    "Span",
    "Tracer",
    "run_health_checks",
]
