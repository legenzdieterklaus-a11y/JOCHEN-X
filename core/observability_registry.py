"""Additive registration points for the platform's observability system.

The module carries the extension surface required by FR-008 while every
contract in :mod:`core.observability` stays exactly as it is: metric sources
are registered under their own namespace and never replace a value recorded on
an existing :class:`~core.observability.Metrics` instance (AC-008.1), and
health checks are registered as implementations of the existing
:class:`~core.observability.HealthCheck` protocol and evaluated through the
existing :func:`~core.observability.run_health_checks` helper (AC-008.2).

Both registries are pure registration points: they own no thread, sample
nothing on their own, and only read what a registered source or check
reports when they are asked.
"""

from __future__ import annotations

from collections.abc import Callable, Mapping
from threading import RLock
from typing import Protocol

from core.observability import HealthCheck, HealthStatus, Metrics, run_health_checks


class MetricSource(Protocol):
    """Provider of supplementary metric values."""

    def collect(self) -> Mapping[str, float]:
        """Return this source's current values keyed by metric name."""
        ...


class CallableMetricSource:
    """Adapter exposing a plain callable as a :class:`MetricSource`."""

    __slots__ = ("_collect",)

    def __init__(self, collect: Callable[[], Mapping[str, float]]) -> None:
        self._collect = collect

    def collect(self) -> Mapping[str, float]:
        """Return the values produced by the wrapped callable."""
        return self._collect()


class MetricsRegistry:
    """Registration point for supplementary metric sources (FR-008 / AC-008.1).

    A registered source contributes new metric names only: its values are
    published under ``"<source name>.<metric name>"``, and merging treats an
    existing :class:`Metrics` instance as read-only, so neither the names nor
    the values of already recorded metrics can change through a registration.
    """

    __slots__ = ("_lock", "_sources")

    def __init__(self) -> None:
        self._sources: dict[str, MetricSource] = {}
        self._lock = RLock()

    def register(self, name: str, source: MetricSource) -> None:
        """Register ``source`` under the metric namespace ``name``.

        Raises:
            ValueError: If ``name`` is empty or already registered.
        """
        if not name:
            raise ValueError("Metric source name must not be empty")
        with self._lock:
            if name in self._sources:
                raise ValueError(f"Metric source already registered: {name}")
            self._sources[name] = source

    def unregister(self, name: str) -> bool:
        """Remove the source registered under ``name`` and report whether it existed."""
        with self._lock:
            return self._sources.pop(name, None) is not None

    def names(self) -> tuple[str, ...]:
        """Return the registered namespaces in registration order."""
        with self._lock:
            return tuple(self._sources)

    def collect(self) -> dict[str, float]:
        """Return the namespaced values of every registered source."""
        with self._lock:
            sources = tuple(self._sources.items())
        collected: dict[str, float] = {}
        for name, source in sources:
            for key, value in source.collect().items():
                collected[f"{name}.{key}"] = float(value)
        return collected

    def merge(self, metrics: Metrics) -> dict[str, float]:
        """Return the collected values combined with the snapshot of ``metrics``.

        ``metrics`` is neither mutated nor overridden: on a name collision the
        existing metric wins, which is what keeps the extension additive.
        """
        merged = self.collect()
        merged.update(metrics.snapshot())
        return merged


class HealthCheckRegistry:
    """Registration point for health checks (FR-008 / AC-008.2).

    Entries are implementations of the existing
    :class:`~core.observability.HealthCheck` protocol —
    :class:`~core.observability.PluginHealthCheck` among them — and they are
    evaluated through the existing
    :func:`~core.observability.run_health_checks` helper, so the established
    contracts are reused instead of replaced.
    """

    __slots__ = ("_checks", "_lock")

    def __init__(self) -> None:
        self._checks: dict[str, HealthCheck] = {}
        self._lock = RLock()

    def register(self, name: str, check: HealthCheck) -> None:
        """Register ``check`` under ``name``.

        Raises:
            ValueError: If ``name`` is empty or already registered.
        """
        if not name:
            raise ValueError("Health check name must not be empty")
        with self._lock:
            if name in self._checks:
                raise ValueError(f"Health check already registered: {name}")
            self._checks[name] = check

    def unregister(self, name: str) -> bool:
        """Remove the check registered under ``name`` and report whether it existed."""
        with self._lock:
            return self._checks.pop(name, None) is not None

    def names(self) -> tuple[str, ...]:
        """Return the registered check names in registration order."""
        with self._lock:
            return tuple(self._checks)

    def checks(self) -> tuple[HealthCheck, ...]:
        """Return the registered checks in registration order."""
        with self._lock:
            return tuple(self._checks.values())

    def run(self) -> tuple[HealthStatus, ...]:
        """Return the status of every registered check."""
        return run_health_checks(*self.checks())


__all__ = [
    "CallableMetricSource",
    "HealthCheckRegistry",
    "MetricSource",
    "MetricsRegistry",
]
