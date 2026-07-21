"""Graceful shutdown sequence.

:class:`ShutdownSequence` performs an idempotent, ordered teardown: it announces
the request, transitions the state machine into ``SHUTTING_DOWN``, drains
background workers, disposes owned resources in reverse order, and finally
settles in ``SHUTDOWN`` while emitting the completion event.
"""

from __future__ import annotations

import logging
from typing import Protocol

from core.events import EventBus

from app.di import DisposableRegistry
from app.events import ShutdownCompleted, ShutdownRequested
from app.state_machine import ApplicationState, ApplicationStateMachine

_DEFAULT_WORKER_TIMEOUT_SECONDS = 5.0


class SupportsShutdown(Protocol):
    """Port for a background worker pool that can be drained."""

    def shutdown(self, *, timeout: float | None = ...) -> bool:
        """Cancel outstanding work and wait for it to drain."""
        ...


class ShutdownSequence:
    """Coordinates an ordered, idempotent, graceful shutdown."""

    def __init__(
        self,
        *,
        state_machine: ApplicationStateMachine,
        events: EventBus,
        disposables: DisposableRegistry,
        worker_pool: SupportsShutdown | None = None,
        logger: logging.Logger | None = None,
        worker_timeout: float = _DEFAULT_WORKER_TIMEOUT_SECONDS,
    ) -> None:
        """Create the shutdown sequence.

        Args:
            state_machine: The lifecycle state machine to advance.
            events: The shared event bus for lifecycle events.
            disposables: Registry whose resources are released on shutdown.
            worker_pool: Optional background worker pool to drain first.
            logger: Optional logger for diagnostics.
            worker_timeout: Seconds to wait for background workers to drain.
        """
        self._state = state_machine
        self._events = events
        self._disposables = disposables
        self._worker_pool = worker_pool
        self._logger = logger or logging.getLogger("jochen_x.shutdown")
        self._worker_timeout = worker_timeout

    def execute(self, *, exit_code: int = 0, reason: str = "requested") -> None:
        """Perform a graceful shutdown; safe to call more than once.

        Args:
            exit_code: The process exit code to report in the completion event.
            reason: Human-readable reason for the shutdown.
        """
        if self._state.state is ApplicationState.SHUTDOWN:
            return
        ShutdownRequested(reason).publish(self._events)
        if self._state.state is not ApplicationState.SHUTTING_DOWN:
            self._state.transition(ApplicationState.SHUTTING_DOWN)
        try:
            if self._worker_pool is not None:
                self._worker_pool.shutdown(timeout=self._worker_timeout)
            self._disposables.dispose_all()
        finally:
            self._state.transition(ApplicationState.SHUTDOWN)
            ShutdownCompleted(exit_code).publish(self._events)
            self._logger.info("shutdown.completed", extra={"context": {"exit_code": exit_code, "reason": reason}})
