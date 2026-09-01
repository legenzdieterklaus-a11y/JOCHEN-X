"""Monitoring state collector and bootstrap stage."""

from __future__ import annotations

import logging
from collections.abc import Callable
from dataclasses import dataclass

from app.bootstrap.types import BootstrapContext, StartupPhase
from core.events import Event, EventBus
from database.sqlite import (
    ConnectionManager,
    MonitoringState,
    MonitoringStateRepository,
)

__all__ = ["MonitoringBootstrapStage", "MonitoringStateCollector"]


class MonitoringStateCollector:
    """Subscribes to monitoring events and persists state changes."""

    def __init__(
        self,
        events: EventBus,
        repository: MonitoringStateRepository,
        logger: logging.Logger,
    ) -> None:
        self._events = events
        self._repository = repository
        self._logger = logger
        self._cache: dict[tuple[str, str], MonitoringState] = {}
        self._unsubscribe: Callable[[], None] | None = None

    def start(self) -> None:
        """Load persisted state and subscribe to monitoring events."""
        for state in self._repository.all():
            self._cache[(state.host_id, state.subject)] = state
        self._unsubscribe = self._events.subscribe(
            "monitoring.*", self._on_event, receive_sticky=False,
        )

    def stop(self) -> None:
        """Unsubscribe from the event bus."""
        if self._unsubscribe is not None:
            self._unsubscribe()
            self._unsubscribe = None

    def dispose(self) -> None:
        """Satisfy the Disposable protocol."""
        self.stop()

    def states(self) -> tuple[MonitoringState, ...]:
        """Return all cached monitoring states."""
        return tuple(self._cache.values())

    def states_for_host(self, host_id: str) -> tuple[MonitoringState, ...]:
        """Return monitoring states for a single host."""
        return tuple(s for s in self._cache.values() if s.host_id == host_id)

    def _on_event(self, event: Event) -> None:
        payload = event.payload
        host_id = payload.get("host_id", "")
        subject = payload.get("subject", "")
        status = payload.get("status", "unknown")
        timestamp = payload.get("timestamp", "")
        key = (host_id, subject)
        existing = self._cache.get(key)
        previous = existing.status if existing is not None else "unknown"

        if existing is None:
            state = MonitoringState(
                host_id=host_id,
                subject=subject,
                status=status,
                first_seen=timestamp,
                last_seen=timestamp if status == "running" else None,
                since=timestamp,
                transitions=0,
            )
        elif previous != status:
            state = MonitoringState(
                host_id=host_id,
                subject=subject,
                status=status,
                first_seen=existing.first_seen,
                last_seen=timestamp if status == "running" else existing.last_seen,
                since=timestamp,
                transitions=existing.transitions + 1,
            )
        else:
            return

        if previous != status:
            self._log_transition(host_id, subject, previous, status, timestamp)

        self._cache[key] = state
        self._repository.upsert(state)

    def _log_transition(
        self,
        host_id: str,
        subject: str,
        previous: str,
        status: str,
        timestamp: str,
    ) -> None:
        ctx = {
            "host_id": host_id,
            "subject": subject,
            "previous": previous,
            "status": status,
            "timestamp": timestamp,
        }
        if status == "unknown" or (previous == "running" and status == "missing"):
            self._logger.warning(
                "monitoring.state_changed", extra={"context": ctx},
            )
        else:
            self._logger.info(
                "monitoring.state_changed", extra={"context": ctx},
            )


@dataclass(frozen=True, slots=True)
class MonitoringBootstrapStage:
    """Registers the monitoring collector outside ``app/bootstrap/``.

    Satisfies the :class:`app.bootstrap.BootstrapStage` protocol and is
    appended to :func:`app.bootstrap.default_stages` via the
    :class:`app.bootstrap.BootstrapManager` ``stages`` argument, keeping
    the bootstrap package untouched.
    """

    name: str = "monitoring"
    phase: StartupPhase = StartupPhase.LOAD_RESOURCES

    def execute(self, context: BootstrapContext) -> None:
        registry = context.registry
        connections = context.connections
        events = context.events
        if registry is None or connections is None or events is None:
            raise RuntimeError(
                "Monitoring stage requires registry, connections, and event bus"
            )
        logger = context.logger or logging.getLogger("jochen_x")
        repository = MonitoringStateRepository(connections)
        collector = MonitoringStateCollector(events, repository, logger)
        collector.start()
        registry.register(MonitoringStateCollector, collector)
        disposables = context.disposables
        if disposables is not None:
            disposables.register(collector)
