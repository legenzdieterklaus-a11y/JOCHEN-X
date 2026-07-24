"""Policy-only performance modes; adapters apply future platform controls."""

from enum import StrEnum


class PerformanceMode(StrEnum):
    NORMAL = "normal"
    GAMING = "gaming"
    IDLE = "idle"
    LOW_POWER = "low_power"
    BENCHMARK = "benchmark"
    SLEEP = "sleep"
    MAINTENANCE = "maintenance"


class PerformanceController:
    def __init__(self, mode: PerformanceMode = PerformanceMode.NORMAL) -> None:
        self._mode = mode

    @property
    def mode(self) -> PerformanceMode:
        return self._mode

    def set_mode(self, mode: PerformanceMode) -> None:
        self._mode = mode

    def permits(self, module: str) -> bool:
        return not (
            self._mode in {PerformanceMode.GAMING, PerformanceMode.SLEEP}
            and module not in {"ui", "core"}
        )
