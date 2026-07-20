"""Low-overhead process metrics and future gaming-observation ports."""

from dataclasses import dataclass
from typing import Protocol
import os
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
            import resource  # type: ignore[import-not-found]
            ram = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss * 1024
        except ImportError:
            pass
        return MetricsSnapshot(time.process_time(), ram)
