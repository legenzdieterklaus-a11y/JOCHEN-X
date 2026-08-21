"""In-memory metrics, tracing and health contracts with no autonomous sampling."""

from collections.abc import Callable, Iterator, Mapping
from dataclasses import dataclass
from enum import StrEnum
from time import perf_counter
from types import MappingProxyType
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


class DiagnosticOutcome(StrEnum):
    """Outcome a plugin reached at the pipeline stage a diagnostic refers to."""

    ACTIVATED = "activated"
    REJECTED = "rejected"
    FAILED = "failed"


_NO_CONTEXT: Mapping[str, str] = MappingProxyType({})


@dataclass(frozen=True, slots=True)
class PluginDiagnostic:
    """Structured diagnostic about one plugin at one pipeline stage (FR-007).

    Carries the plugin identifier and the affected pipeline stage (AC-007.1).
    ``stage`` is a plain string so this contract stays free of any dependency
    on the bootstrap pipeline typing; producers pass their stage value and,
    where they have one, its PL-01..PL-05 reference.
    """

    plugin_id: str
    stage: str
    outcome: DiagnosticOutcome
    reason: str = ""
    pipeline_reference: str = ""
    code: str = ""
    context: Mapping[str, str] = _NO_CONTEXT

    @property
    def succeeded(self) -> bool:
        """Return whether the diagnostic describes a successful outcome."""
        return self.outcome == DiagnosticOutcome.ACTIVATED


@dataclass(frozen=True, slots=True)
class PluginDiagnosticsReport:
    """Queryable consolidation of the plugin runtime's diagnostics (FR-007).

    The producing pipeline assembles the report once and hands it to the
    composition root, which makes the diagnostics programmatically retrievable
    after startup instead of only reconstructable from log output (AC-007.2).
    The report is read-only with respect to the plugin runtime (BI-06).
    """

    entries: tuple[PluginDiagnostic, ...] = ()

    def __iter__(self) -> Iterator[PluginDiagnostic]:
        return iter(self.entries)

    def __len__(self) -> int:
        return len(self.entries)

    def diagnostics(self) -> tuple[PluginDiagnostic, ...]:
        """Return every recorded diagnostic in pipeline order."""
        return self.entries

    def plugin_ids(self) -> tuple[str, ...]:
        """Return the covered plugin identifiers in first-seen order."""
        seen: dict[str, None] = {}
        for diagnostic in self.entries:
            seen.setdefault(diagnostic.plugin_id, None)
        return tuple(seen)

    def for_plugin(self, plugin_id: str) -> tuple[PluginDiagnostic, ...]:
        """Return every diagnostic recorded for ``plugin_id``."""
        return tuple(item for item in self.entries if item.plugin_id == plugin_id)

    def for_stage(self, stage: str) -> tuple[PluginDiagnostic, ...]:
        """Return every diagnostic recorded for ``stage``."""
        return tuple(item for item in self.entries if item.stage == stage)

    def with_outcome(self, outcome: DiagnosticOutcome) -> tuple[PluginDiagnostic, ...]:
        """Return every diagnostic that reached ``outcome``."""
        return tuple(item for item in self.entries if item.outcome == outcome)

    def counts(self) -> dict[str, float]:
        """Return the diagnostic count per outcome, including unused outcomes."""
        counts = {outcome.value: 0.0 for outcome in DiagnosticOutcome}
        for diagnostic in self.entries:
            counts[DiagnosticOutcome(diagnostic.outcome).value] += 1
        return counts


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
    "DiagnosticOutcome",
    "HealthCheck",
    "HealthStatus",
    "Metrics",
    "PluginDiagnostic",
    "PluginDiagnosticsReport",
    "PluginHealthCheck",
    "Span",
    "Tracer",
    "run_health_checks",
]
