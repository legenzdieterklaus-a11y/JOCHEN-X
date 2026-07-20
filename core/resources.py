"""Resource-observation ports; platform adapters provide measurements on demand."""
from dataclasses import dataclass
from typing import Protocol
@dataclass(frozen=True, slots=True)
class ResourceSnapshot:
    cpu_percent: float|None=None; ram_bytes: int|None=None; gpu_percent: float|None=None; vram_bytes: int|None=None; disk_bytes: int|None=None; battery_percent: float|None=None; network_bytes_per_second: float|None=None; temperature_celsius: float|None=None; fps: float|None=None; fullscreen: bool|None=None; game_running: bool|None=None
class ResourceMonitor(Protocol):
    def snapshot(self) -> ResourceSnapshot: ...
