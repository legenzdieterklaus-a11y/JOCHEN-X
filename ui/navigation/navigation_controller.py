"""Routing controller with deterministic back and forward history."""

from __future__ import annotations

import logging

from PySide6.QtCore import QObject, Signal

from app.events import EventPublisher
from ui.navigation.module_host import ModuleHost
from ui.navigation.navigation_events import (
    NavigationChanged,
    publish_navigation_event,
)
from ui.navigation.navigation_registry import RegistryChange, RegistryChangeAction
from ui.navigation.navigation_service import NavigationService


class NavigationController(QObject):
    """Coordinates route activation, history, and navigation events."""

    navigation_changed = Signal(str)
    history_changed = Signal(bool, bool)
    _registry_changed = Signal(object)

    def __init__(
        self,
        navigation: NavigationService,
        module_host: ModuleHost,
        events: EventPublisher,
        *,
        default_identifier: str,
        identity_id: str | None = None,
        parent: QObject | None = None,
        logger: logging.Logger | None = None,
    ) -> None:
        """Create the controller from existing application services."""
        super().__init__(parent)
        navigation.resolve(default_identifier, identity_id)
        self._navigation = navigation
        self._module_host = module_host
        self._events = events
        self._logger = logger or logging.getLogger("jochen_x.navigation.controller")
        self._default_identifier = default_identifier
        self._identity_id = identity_id
        self._history: list[str] = []
        self._history_index = -1
        self._registry_changed.connect(self._on_registry_changed)
        self._unsubscribe_registry = navigation.registry.subscribe(
            self._registry_changed.emit
        )
        self.destroyed.connect(lambda _: self._unsubscribe_registry())

    @property
    def current_identifier(self) -> str | None:
        """Return the active route identifier."""
        return self._module_host.active_identifier

    @property
    def can_go_back(self) -> bool:
        """Return whether a previous history entry exists."""
        return self._history_index > 0

    @property
    def can_go_forward(self) -> bool:
        """Return whether a forward history entry exists."""
        return 0 <= self._history_index < len(self._history) - 1

    @property
    def history(self) -> tuple[str, ...]:
        """Return an immutable history snapshot."""
        return tuple(self._history)

    def start(self) -> None:
        """Activate the default page if no route is active."""
        if self.current_identifier is None:
            self.navigate(self._default_identifier)

    def navigate(self, identifier: str) -> None:
        """Navigate to a route and append it to history."""
        if identifier == self.current_identifier:
            return
        self._navigation.resolve(identifier, self._identity_id)
        self._activate(identifier)
        if self.can_go_forward:
            del self._history[self._history_index + 1 :]
        self._history.append(identifier)
        self._history_index = len(self._history) - 1
        self._emit_history_state()

    def back(self) -> bool:
        """Activate the previous history entry."""
        if not self.can_go_back:
            return False
        target_index = self._history_index - 1
        self._activate(self._history[target_index])
        self._history_index = target_index
        self._emit_history_state()
        return True

    def forward(self) -> bool:
        """Activate the next history entry."""
        if not self.can_go_forward:
            return False
        target_index = self._history_index + 1
        self._activate(self._history[target_index])
        self._history_index = target_index
        self._emit_history_state()
        return True

    def home(self) -> None:
        """Navigate to the configured default page."""
        self.navigate(self._default_identifier)

    def _activate(
        self,
        identifier: str,
        *,
        announced_previous: str | None = None,
    ) -> None:
        """Activate and announce a resolved route."""
        previous = announced_previous or self.current_identifier
        self._module_host.activate(identifier, self._identity_id)
        publish_navigation_event(
            NavigationChanged(previous, identifier),
            self._events,
            logger=self._logger,
            sticky=True,
        )
        self.navigation_changed.emit(identifier)

    def _emit_history_state(self) -> None:
        """Announce committed history availability."""
        self.history_changed.emit(self.can_go_back, self.can_go_forward)

    def _on_registry_changed(self, change: RegistryChange) -> None:
        """Repair route history after a dynamic destination is removed."""
        if change.action is not RegistryChangeAction.UNREGISTERED:
            return
        current_history = (
            self._history[self._history_index]
            if 0 <= self._history_index < len(self._history)
            else None
        )
        if current_history == change.identifier:
            self._history.clear()
            self._history_index = -1
            if (
                change.identifier != self._default_identifier
                and self._navigation.registry.contains(self._default_identifier)
            ):
                self._activate(
                    self._default_identifier,
                    announced_previous=change.identifier,
                )
                self._history.append(self._default_identifier)
                self._history_index = 0
                self._emit_history_state()
            else:
                self._emit_history_state()
            return
        removed_before = sum(
            1
            for identifier in self._history[: self._history_index]
            if identifier == change.identifier
        )
        self._history = [
            identifier for identifier in self._history if identifier != change.identifier
        ]
        if self._history_index >= 0:
            self._history_index -= removed_before
            self._history_index = min(self._history_index, len(self._history) - 1)
        self._emit_history_state()
