"""Ordered lifecycle coordination without background workers.

Every state change of the :class:`LifecycleManager` is validated against the
explicit transition table exposed via :func:`transition_table`; transitions
outside the table are rejected with a structured
:class:`core.exceptions.StateTransitionError`.
"""

from __future__ import annotations

from collections.abc import Callable, Mapping
from enum import StrEnum
from threading import RLock
from types import MappingProxyType

from core.exceptions import StateTransitionError, TransitionRejection


class LifecycleState(StrEnum):
    NEW = "new"
    RUNNING = "running"
    STOPPED = "stopped"
    FAILED = "failed"


_TRANSITIONS: dict[LifecycleState, frozenset[LifecycleState]] = {
    LifecycleState.NEW: frozenset({LifecycleState.RUNNING, LifecycleState.FAILED}),
    LifecycleState.RUNNING: frozenset({LifecycleState.STOPPED}),
    LifecycleState.STOPPED: frozenset({LifecycleState.RUNNING, LifecycleState.FAILED}),
    LifecycleState.FAILED: frozenset({LifecycleState.RUNNING, LifecycleState.FAILED}),
}


def transition_table() -> Mapping[LifecycleState, frozenset[LifecycleState]]:
    """Return the complete, read-only lifecycle transition table.

    Every state appears as a key; the value is the exhaustive set of permitted
    target states. Transitions outside this table are rejected.
    """
    return MappingProxyType(_TRANSITIONS)


class LifecycleManager:
    def __init__(self) -> None:
        self._state = LifecycleState.NEW
        self._modules: list[tuple[str, Callable[[], None], Callable[[], None]]] = []
        self._lock = RLock()

    @property
    def state(self) -> LifecycleState:
        return self._state

    def _transition(self, target: LifecycleState) -> None:
        """Validate against the transition table, then apply the transition."""
        allowed = _TRANSITIONS[self._state]
        if target not in allowed:
            raise StateTransitionError(
                TransitionRejection(
                    source=self._state.value,
                    target=target.value,
                    reason=(
                        f"Illegal lifecycle transition: '{self._state.value}' -> '{target.value}'"
                    ),
                    allowed=tuple(sorted(state.value for state in allowed)),
                )
            )
        self._state = target

    def register_module(
        self, name: str, start: Callable[[], None], stop: Callable[[], None]
    ) -> None:
        with self._lock:
            if self._state is LifecycleState.RUNNING:
                raise RuntimeError("Cannot register while running")
            if any(item[0] == name for item in self._modules):
                raise ValueError(f"Duplicate module: {name}")
            self._modules.append((name, start, stop))

    def start(self) -> None:
        with self._lock:
            if self._state is LifecycleState.RUNNING:
                return
            started = []
            try:
                for module in self._modules:
                    module[1]()
                    started.append(module)
                self._transition(LifecycleState.RUNNING)
            except StateTransitionError:
                raise
            except Exception:
                for module in reversed(started):
                    module[2]()
                self._transition(LifecycleState.FAILED)
                raise

    def shutdown(self) -> None:
        with self._lock:
            if self._state is not LifecycleState.RUNNING:
                return
            for module in reversed(self._modules):
                module[2]()
            self._transition(LifecycleState.STOPPED)

    def restart(self) -> None:
        self.shutdown()
        self.start()

    def recover(self) -> None:
        if self._state is LifecycleState.FAILED:
            self.start()

    def health(self) -> dict[str, str]:
        return {name: self._state for name, _, _ in self._modules}
