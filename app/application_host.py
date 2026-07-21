"""Application host: the root lifecycle orchestrator.

:class:`ApplicationHost` owns the application lifetime end to end. It creates the
shared event bus and state machine, executes the startup sequence, exposes the
resulting immutable context, owns the background worker pool and resource
lifetime, routes fatal errors, and performs graceful shutdown, restart, and
fatal-error recovery. It deliberately contains no Qt event-loop code so it can be
started and inspected headlessly; the Qt entry point lives in
:class:`app.application.Application`.
"""

from __future__ import annotations

import logging
from collections.abc import Callable
from pathlib import Path

from core.events import EventBus
from core.observability import HealthStatus
from core.registry import ServiceRegistry

from app.bootstrap import BootstrapManager
from app.concurrency import WorkerPool
from app.context import ApplicationContext
from app.di import DisposableRegistry
from app.errors import CentralErrorHandler, ErrorCategory, ErrorReport
from app.shutdown import ShutdownSequence
from app.startup import StartupSequence
from app.state_machine import ApplicationState, ApplicationStateMachine

_LOGGER_NAME = "jochen_x"


class ApplicationHost:
    """Root orchestrator owning startup, shutdown, workers, and recovery."""

    def __init__(
        self,
        root: Path,
        *,
        bootstrap_manager: BootstrapManager | None = None,
        worker_pool: WorkerPool | None = None,
        logger: logging.Logger | None = None,
    ) -> None:
        """Create the host.

        Args:
            root: The application root directory.
            bootstrap_manager: Optional bootstrap manager (default stages if omitted).
            worker_pool: Optional background worker pool.
            logger: Optional logger; defaults to the shared application logger.
        """
        self._root = root
        self._logger = logger or logging.getLogger(_LOGGER_NAME)
        self._events = EventBus(logger=self._logger)
        self._bootstrap = bootstrap_manager or BootstrapManager()
        self._workers = worker_pool or WorkerPool(logger=self._logger)
        self._state = ApplicationStateMachine(publisher=self._events, logger=self._logger)
        self._startup = self._build_startup()
        self._error_handler = CentralErrorHandler(
            logger=self._logger, publisher=self._events, on_fatal=self._on_fatal
        )
        self._context: ApplicationContext | None = None
        self._disposables: DisposableRegistry | None = None
        self._fatal: ErrorReport | None = None
        self._fatal_callback: Callable[[ErrorReport], None] | None = None

    @classmethod
    def create_default(cls) -> ApplicationHost:
        """Create a host rooted at the repository directory."""
        return cls(Path(__file__).resolve().parents[1])

    @property
    def state(self) -> ApplicationState:
        """Return the current lifecycle state."""
        return self._state.state

    @property
    def events(self) -> EventBus:
        """Return the shared application event bus."""
        return self._events

    @property
    def workers(self) -> WorkerPool:
        """Return the background worker pool."""
        return self._workers

    @property
    def error_handler(self) -> CentralErrorHandler:
        """Return the centralized error handler."""
        return self._error_handler

    @property
    def context(self) -> ApplicationContext:
        """Return the initialised application context.

        Raises:
            RuntimeError: If accessed before the host has started.
        """
        if self._context is None:
            raise RuntimeError("Application context is unavailable before start()")
        return self._context

    def set_fatal_callback(self, callback: Callable[[ErrorReport], None]) -> None:
        """Register a callback invoked when a fatal error is escalated."""
        self._fatal_callback = callback

    def start(self) -> ApplicationContext:
        """Execute the startup sequence and return the ready application context.

        Raises:
            Exception: Re-raises any startup failure after recording it as fatal.
        """
        try:
            context = self._startup.execute(self._root)
        except Exception as error:
            self._error_handler.handle(error, category=ErrorCategory.FATAL, context={"phase": "startup"})
            raise
        self._context = context
        self._disposables = context.registry.get(DisposableRegistry)
        return context

    def shutdown(self, *, exit_code: int = 0, reason: str = "requested") -> None:
        """Perform a graceful, idempotent shutdown."""
        disposables = self._disposables or DisposableRegistry(self._logger)
        sequence = ShutdownSequence(
            state_machine=self._state,
            events=self._events,
            disposables=disposables,
            worker_pool=self._workers,
            logger=self._logger,
        )
        sequence.execute(exit_code=exit_code, reason=reason)

    def restart(self) -> ApplicationContext:
        """Gracefully shut down and start a fresh application lifecycle."""
        if self._state.state is ApplicationState.READY:
            self._state.transition(ApplicationState.RESTART_REQUIRED)
        self.shutdown(reason="restart")
        self._reset()
        self._logger.info("host.restart")
        return self.start()

    def recover(self) -> ApplicationContext:
        """Recover from a fatal error by rebuilding and restarting the lifecycle.

        Raises:
            RuntimeError: If there is no fatal error to recover from.
        """
        if self._fatal is None:
            raise RuntimeError("No fatal error to recover from")
        self._logger.warning("host.recover", extra={"context": {"category": self._fatal.category.value}})
        self._fatal = None
        self._reset()
        return self.start()

    def health(self) -> tuple[HealthStatus, ...]:
        """Return health statuses for the host's key subsystems."""
        state = self._state.state
        operational = state in {ApplicationState.READY, ApplicationState.BUSY, ApplicationState.UPDATING}
        return (
            HealthStatus("lifecycle", operational, state.value),
            HealthStatus("workers", True, f"active={self._workers.active_count()}"),
            HealthStatus("errors", self._fatal is None, "ok" if self._fatal is None else self._fatal.category.value),
        )

    def _build_startup(self) -> StartupSequence:
        """Create a startup sequence bound to the current state machine."""
        return StartupSequence(
            state_machine=self._state,
            bootstrap_manager=self._bootstrap,
            events=self._events,
            logger=self._logger,
        )

    def _reset(self) -> None:
        """Rebuild per-lifecycle collaborators for a restart or recovery."""
        self._state = ApplicationStateMachine(publisher=self._events, logger=self._logger)
        self._workers = WorkerPool(logger=self._logger)
        self._startup = self._build_startup()
        self._context = None
        self._disposables = None

    def _on_fatal(self, report: ErrorReport) -> None:
        """Record a fatal error and notify any registered fatal callback."""
        self._fatal = report
        self._logger.critical("host.fatal", extra={"context": {"category": report.category.value}})
        if self._fatal_callback is not None:
            self._fatal_callback(report)
