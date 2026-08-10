"""Strongly typed application lifecycle events.

This module defines the immutable lifecycle event vocabulary for the JOCHEN X
application foundation. Every event carries a stable :class:`ApplicationEventName`
and converts to a transport-neutral :class:`core.events.Event` so it integrates
with the existing in-process :class:`core.events.EventBus` and the developer
platform event inspector without leaking payload structure into magic strings.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from typing import Any, ClassVar, Protocol, runtime_checkable

from core.events import Event

__all__ = [
    "ApplicationEventName",
    "EventPublisher",
    "ApplicationEvent",
    "ApplicationStarting",
    "ApplicationStarted",
    "ApplicationReady",
    "ApplicationStateChanged",
    "PluginLoading",
    "PluginLoaded",
    "PluginFailed",
    "PluginActivating",
    "PluginActivated",
    "ConfigurationChanged",
    "ThemeChanged",
    "BusyStarted",
    "BusyFinished",
    "ShutdownRequested",
    "ShutdownCompleted",
    "ErrorRaised",
]


class ApplicationEventName(StrEnum):
    """Canonical, stable names for every application lifecycle event."""

    STARTING = "application.starting"
    STARTED = "application.started"
    READY = "application.ready"
    STATE_CHANGED = "application.state.changed"
    PLUGIN_LOADING = "application.plugin.loading"
    PLUGIN_LOADED = "application.plugin.loaded"
    PLUGIN_FAILED = "application.plugin.failed"
    PLUGIN_ACTIVATING = "application.plugin.activating"
    PLUGIN_ACTIVATED = "application.plugin.activated"
    CONFIGURATION_CHANGED = "application.configuration.changed"
    THEME_CHANGED = "application.theme.changed"
    BUSY_STARTED = "application.busy.started"
    BUSY_FINISHED = "application.busy.finished"
    SHUTDOWN_REQUESTED = "application.shutdown.requested"
    SHUTDOWN_COMPLETED = "application.shutdown.completed"
    ERROR_RAISED = "application.error.raised"


@runtime_checkable
class EventPublisher(Protocol):
    """Narrow publishing port satisfied structurally by :class:`core.events.EventBus`."""

    def publish(self, event: Event, *, sticky: bool = False) -> None:
        """Publish a single event to synchronous subscribers."""
        ...


class ApplicationEvent:
    """Base class for immutable, typed lifecycle events.

    Subclasses are frozen dataclasses that declare their :attr:`EVENT_NAME` and
    optionally override :meth:`_payload` to expose typed data as a plain mapping
    for the transport-neutral :class:`core.events.Event`.
    """

    __slots__ = ()

    EVENT_NAME: ClassVar[ApplicationEventName]

    def _payload(self) -> dict[str, Any]:
        """Return the event payload as a JSON-serialisable mapping."""
        return {}

    def to_event(self) -> Event:
        """Convert this typed event into a transport-neutral bus event."""
        return Event(str(self.EVENT_NAME), self._payload())

    def publish(self, publisher: EventPublisher, *, sticky: bool = False) -> None:
        """Publish this event through the supplied publisher port."""
        publisher.publish(self.to_event(), sticky=sticky)


@dataclass(frozen=True, slots=True)
class ApplicationStarting(ApplicationEvent):
    """Emitted once the startup sequence begins initialising the foundation."""

    EVENT_NAME: ClassVar[ApplicationEventName] = ApplicationEventName.STARTING
    version: str

    def _payload(self) -> dict[str, Any]:
        return {"version": self.version}


@dataclass(frozen=True, slots=True)
class ApplicationStarted(ApplicationEvent):
    """Emitted after core infrastructure has been composed successfully."""

    EVENT_NAME: ClassVar[ApplicationEventName] = ApplicationEventName.STARTED
    service_count: int

    def _payload(self) -> dict[str, Any]:
        return {"service_count": self.service_count}


@dataclass(frozen=True, slots=True)
class ApplicationReady(ApplicationEvent):
    """Emitted when the application has reached the ready state."""

    EVENT_NAME: ClassVar[ApplicationEventName] = ApplicationEventName.READY
    startup_ms: float

    def _payload(self) -> dict[str, Any]:
        return {"startup_ms": round(self.startup_ms, 3)}


@dataclass(frozen=True, slots=True)
class ApplicationStateChanged(ApplicationEvent):
    """Emitted for every validated application state transition."""

    EVENT_NAME: ClassVar[ApplicationEventName] = ApplicationEventName.STATE_CHANGED
    previous: str
    current: str

    def _payload(self) -> dict[str, Any]:
        return {"previous": self.previous, "current": self.current}


@dataclass(frozen=True, slots=True)
class PluginLoading(ApplicationEvent):
    """Emitted before a discovered plugin manifest is admitted."""

    EVENT_NAME: ClassVar[ApplicationEventName] = ApplicationEventName.PLUGIN_LOADING
    identifier: str

    def _payload(self) -> dict[str, Any]:
        return {"identifier": self.identifier}


@dataclass(frozen=True, slots=True)
class PluginLoaded(ApplicationEvent):
    """Emitted once a plugin manifest has been admitted as compatible."""

    EVENT_NAME: ClassVar[ApplicationEventName] = ApplicationEventName.PLUGIN_LOADED
    identifier: str
    version: str

    def _payload(self) -> dict[str, Any]:
        return {"identifier": self.identifier, "version": self.version}


@dataclass(frozen=True, slots=True)
class PluginFailed(ApplicationEvent):
    """Emitted when plugin discovery fails for one or more manifests."""

    EVENT_NAME: ClassVar[ApplicationEventName] = ApplicationEventName.PLUGIN_FAILED
    identifier: str
    reason: str

    def _payload(self) -> dict[str, Any]:
        return {"identifier": self.identifier, "reason": self.reason}


@dataclass(frozen=True, slots=True)
class PluginActivating(ApplicationEvent):
    """Emitted before a plugin runtime is imported and started."""

    EVENT_NAME: ClassVar[ApplicationEventName] = ApplicationEventName.PLUGIN_ACTIVATING
    identifier: str

    def _payload(self) -> dict[str, Any]:
        return {"identifier": self.identifier}


@dataclass(frozen=True, slots=True)
class PluginActivated(ApplicationEvent):
    """Emitted after a plugin runtime has been successfully started."""

    EVENT_NAME: ClassVar[ApplicationEventName] = ApplicationEventName.PLUGIN_ACTIVATED
    identifier: str
    version: str

    def _payload(self) -> dict[str, Any]:
        return {"identifier": self.identifier, "version": self.version}


@dataclass(frozen=True, slots=True)
class ConfigurationChanged(ApplicationEvent):
    """Emitted when persisted configuration values change at runtime."""

    EVENT_NAME: ClassVar[ApplicationEventName] = ApplicationEventName.CONFIGURATION_CHANGED
    keys: tuple[str, ...]

    def _payload(self) -> dict[str, Any]:
        return {"keys": list(self.keys)}


@dataclass(frozen=True, slots=True)
class ThemeChanged(ApplicationEvent):
    """Emitted when the active theme mode changes."""

    EVENT_NAME: ClassVar[ApplicationEventName] = ApplicationEventName.THEME_CHANGED
    mode: str

    def _payload(self) -> dict[str, Any]:
        return {"mode": self.mode}


@dataclass(frozen=True, slots=True)
class BusyStarted(ApplicationEvent):
    """Emitted when the application enters a long-running busy region."""

    EVENT_NAME: ClassVar[ApplicationEventName] = ApplicationEventName.BUSY_STARTED
    reason: str

    def _payload(self) -> dict[str, Any]:
        return {"reason": self.reason}


@dataclass(frozen=True, slots=True)
class BusyFinished(ApplicationEvent):
    """Emitted when the application leaves a busy region."""

    EVENT_NAME: ClassVar[ApplicationEventName] = ApplicationEventName.BUSY_FINISHED
    reason: str

    def _payload(self) -> dict[str, Any]:
        return {"reason": self.reason}


@dataclass(frozen=True, slots=True)
class ShutdownRequested(ApplicationEvent):
    """Emitted when a graceful shutdown has been requested."""

    EVENT_NAME: ClassVar[ApplicationEventName] = ApplicationEventName.SHUTDOWN_REQUESTED
    reason: str

    def _payload(self) -> dict[str, Any]:
        return {"reason": self.reason}


@dataclass(frozen=True, slots=True)
class ShutdownCompleted(ApplicationEvent):
    """Emitted once shutdown has finished and resources are released."""

    EVENT_NAME: ClassVar[ApplicationEventName] = ApplicationEventName.SHUTDOWN_COMPLETED
    exit_code: int

    def _payload(self) -> dict[str, Any]:
        return {"exit_code": self.exit_code}


@dataclass(frozen=True, slots=True)
class ErrorRaised(ApplicationEvent):
    """Emitted by the centralized error handler for every handled error."""

    EVENT_NAME: ClassVar[ApplicationEventName] = ApplicationEventName.ERROR_RAISED
    category: str
    severity: str
    message: str

    def _payload(self) -> dict[str, Any]:
        return {"category": self.category, "severity": self.severity, "message": self.message}
