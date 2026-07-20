"""Ordered lifecycle coordination without background workers."""
from __future__ import annotations
from collections.abc import Callable
from enum import StrEnum
from threading import RLock

class LifecycleState(StrEnum): NEW="new"; RUNNING="running"; STOPPED="stopped"; FAILED="failed"
class LifecycleManager:
    def __init__(self) -> None: self._state=LifecycleState.NEW; self._modules: list[tuple[str, Callable[[], None], Callable[[], None]]]=[]; self._lock=RLock()
    @property
    def state(self) -> LifecycleState: return self._state
    def register_module(self, name: str, start: Callable[[], None], stop: Callable[[], None]) -> None:
        with self._lock:
            if self._state is LifecycleState.RUNNING: raise RuntimeError("Cannot register while running")
            if any(item[0] == name for item in self._modules): raise ValueError(f"Duplicate module: {name}")
            self._modules.append((name,start,stop))
    def start(self) -> None:
        with self._lock:
            if self._state is LifecycleState.RUNNING: return
            started=[]
            try:
                for module in self._modules: module[1](); started.append(module)
                self._state=LifecycleState.RUNNING
            except Exception:
                for module in reversed(started): module[2]()
                self._state=LifecycleState.FAILED; raise
    def shutdown(self) -> None:
        with self._lock:
            if self._state is not LifecycleState.RUNNING: return
            for module in reversed(self._modules): module[2]()
            self._state=LifecycleState.STOPPED
    def restart(self) -> None: self.shutdown(); self.start()
    def recover(self) -> None:
        if self._state is LifecycleState.FAILED: self.start()
    def health(self) -> dict[str, str]: return {name: self._state for name,_,_ in self._modules}
