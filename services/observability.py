"""Low-overhead process metrics and future gaming-observation ports."""

from collections.abc import Mapping
from dataclasses import dataclass, fields
from typing import Protocol
import time


@dataclass(frozen=True, slots=True)
class MetricsSnapshot:
    """Foundation metric values; unavailable hardware measurements are `None`."""
    process_cpu_seconds: float
    process_ram_bytes: int | None
    gpu_percent: float | None = None
    vram_bytes: int | None = None
    fps: float | None = None
    fullscreen: bool | None = None
    monitor_hz: float | None = None
    game_running: bool | None = None


class GameModeDetector(Protocol):
    """Port for a future, opt-in platform-specific game-mode implementation."""
    def snapshot(self) -> MetricsSnapshot: ...


class PerformanceMonitor:
    """Samples only the current process; no background thread is created."""
    def snapshot(self) -> MetricsSnapshot:
        """Return a synchronous process snapshot suitable for explicit polling."""
        ram = None
        try:
            import resource
            ram = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss * 1024
        except ImportError:
            pass
        return MetricsSnapshot(time.process_time(), ram)


class ProcessMetricSource:
    """Publishes :class:`PerformanceMonitor` samples as metric values (FR-008).

    The adapter satisfies the ``MetricSource`` protocol of
    :mod:`core.observability_registry`, so the existing process sampling can be
    registered on the platform's metrics registry without changing either the
    :class:`MetricsSnapshot` contract or any metric already recorded. Values
    the platform cannot measure stay absent instead of being reported as zero.
    """

    __slots__ = ("_monitor",)

    def __init__(self, monitor: PerformanceMonitor | None = None) -> None:
        self._monitor = monitor or PerformanceMonitor()

    def collect(self) -> Mapping[str, float]:
        """Return the numeric fields of a fresh snapshot, skipping unset ones."""
        snapshot = self._monitor.snapshot()
        return {
            field.name: float(value)
            for field in fields(snapshot)
            if (value := getattr(snapshot, field.name)) is not None
        }
