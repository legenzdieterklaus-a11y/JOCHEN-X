"""Runtime host protocol - the top-level runtime orchestrator."""

from __future__ import annotations

from typing import Protocol, runtime_checkable

from jochen_x.core.types.runtime_state import RuntimeState

__all__ = ["IRuntimeHost"]


@runtime_checkable
class IRuntimeHost(Protocol):
    """Protocol for the main runtime host.

    The runtime host orchestrates the entire lifecycle: bootstrap,
    start, pause, resume, stop, restart, shutdown, and recovery.
    It owns the lifecycle state machine and delegates to registered
    services for each phase.
    """

    def start(self) -> None:
        """Start the runtime, executing the full bootstrap and startup sequence.

        Transitions the state machine through CREATED -> BOOTSTRAPPING ->
        INITIALIZING -> READY -> STARTING -> RUNNING.

        Raises:
            RuntimeStartError: If the startup sequence fails.
            IllegalStateTransitionError: If already running.

        """
        ...

    def stop(self) -> None:
        """Stop the runtime, executing the shutdown sequence.

        Shuts down all components in reverse bootstrap order.

        Raises:
            RuntimeShutdownError: If the shutdown sequence encounters errors.

        """
        ...

    def restart(self) -> None:
        """Restart the runtime (stop followed by start).

        Preserves runtime state across the restart where possible.

        Raises:
            RuntimeStartError: If re-start fails after stop.

        """
        ...

    def pause(self) -> None:
        """Pause the runtime.

        Transitions from RUNNING to PAUSED.

        Raises:
            IllegalStateTransitionError: If not in RUNNING state.

        """
        ...

    def resume(self) -> None:
        """Resume the runtime from paused state.

        Transitions from PAUSED to RUNNING.

        Raises:
            IllegalStateTransitionError: If not in PAUSED state.

        """
        ...

    def get_state(self) -> RuntimeState:
        """Return the current runtime state.

        Returns:
            The current ``RuntimeState``.

        """
        ...
