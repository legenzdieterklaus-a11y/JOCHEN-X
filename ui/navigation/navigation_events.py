"""Typed events emitted by the navigation presentation framework."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
import logging
from typing import Any, ClassVar

from core.events import Event

from app.events import EventPublisher, ThemeChanged


class NavigationEventName(StrEnum):
    """Canonical event names for navigation and desktop-window changes."""

    NAVIGATION_CHANGED = "navigation.changed"
    MODULE_ACTIVATED = "navigation.module.activated"
    MODULE_DEACTIVATED = "navigation.module.deactivated"
    SIDEBAR_COLLAPSED = "navigation.sidebar.collapsed"
    SIDEBAR_EXPANDED = "navigation.sidebar.expanded"
    DASHBOARD_LOADED = "navigation.dashboard.loaded"
    WINDOW_STATE_CHANGED = "navigation.window.state.changed"


class NavigationEvent:
    """Base class converting typed navigation events to bus events."""

    __slots__ = ()

    EVENT_NAME: ClassVar[NavigationEventName]

    def _payload(self) -> dict[str, Any]:
        """Return a transport-neutral payload."""
        return {}

    def to_event(self) -> Event:
        """Convert this value to the shared EventBus representation."""
        return Event(str(self.EVENT_NAME), self._payload())

    def publish(self, publisher: EventPublisher, *, sticky: bool = False) -> None:
        """Publish through the existing application event bus."""
        publisher.publish(self.to_event(), sticky=sticky)


@dataclass(frozen=True, slots=True)
class NavigationChanged(NavigationEvent):
    """Emitted after the active destination changes."""

    EVENT_NAME: ClassVar[NavigationEventName] = NavigationEventName.NAVIGATION_CHANGED
    previous: str | None
    current: str

    def _payload(self) -> dict[str, Any]:
        return {"previous": self.previous, "current": self.current}


@dataclass(frozen=True, slots=True)
class ModuleActivated(NavigationEvent):
    """Emitted after a module becomes visible."""

    EVENT_NAME: ClassVar[NavigationEventName] = NavigationEventName.MODULE_ACTIVATED
    identifier: str

    def _payload(self) -> dict[str, Any]:
        return {"identifier": self.identifier}


@dataclass(frozen=True, slots=True)
class ModuleDeactivated(NavigationEvent):
    """Emitted before the previous module is hidden."""

    EVENT_NAME: ClassVar[NavigationEventName] = NavigationEventName.MODULE_DEACTIVATED
    identifier: str

    def _payload(self) -> dict[str, Any]:
        return {"identifier": self.identifier}


@dataclass(frozen=True, slots=True)
class SidebarCollapsed(NavigationEvent):
    """Emitted when the sidebar enters compact mode."""

    EVENT_NAME: ClassVar[NavigationEventName] = NavigationEventName.SIDEBAR_COLLAPSED


@dataclass(frozen=True, slots=True)
class SidebarExpanded(NavigationEvent):
    """Emitted when the sidebar leaves compact mode."""

    EVENT_NAME: ClassVar[NavigationEventName] = NavigationEventName.SIDEBAR_EXPANDED


@dataclass(frozen=True, slots=True)
class DashboardLoaded(NavigationEvent):
    """Emitted once the dashboard has initialized."""

    EVENT_NAME: ClassVar[NavigationEventName] = NavigationEventName.DASHBOARD_LOADED


@dataclass(frozen=True, slots=True)
class WindowStateChanged(NavigationEvent):
    """Emitted after desktop geometry or layout state is persisted."""

    EVENT_NAME: ClassVar[NavigationEventName] = NavigationEventName.WINDOW_STATE_CHANGED
    maximized: bool
    width: int
    height: int

    def _payload(self) -> dict[str, Any]:
        return {"maximized": self.maximized, "width": self.width, "height": self.height}


def publish_navigation_event(
    event: NavigationEvent,
    publisher: EventPublisher,
    *,
    logger: logging.Logger | None = None,
    sticky: bool = False,
) -> None:
    """Publish a UI notification without allowing observers to corrupt UI state."""
    resolved_logger = logger or logging.getLogger("jochen_x.navigation.events")
    try:
        event.publish(publisher, sticky=sticky)
    except Exception as error:
        resolved_logger.error(
            "navigation.event_delivery_failed",
            exc_info=error,
            extra={"context": {"event": str(event.EVENT_NAME)}},
        )


__all__ = [
    "DashboardLoaded",
    "ModuleActivated",
    "ModuleDeactivated",
    "NavigationChanged",
    "NavigationEvent",
    "NavigationEventName",
    "SidebarCollapsed",
    "SidebarExpanded",
    "ThemeChanged",
    "WindowStateChanged",
    "publish_navigation_event",
]
