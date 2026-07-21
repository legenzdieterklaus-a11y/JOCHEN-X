"""Lazy, memory-retaining host for navigation modules."""

from __future__ import annotations

import logging

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QLabel, QStackedWidget, QVBoxLayout, QWidget

from app.events import EventPublisher
from ui.navigation.navigation_events import (
    ModuleActivated,
    ModuleDeactivated,
    publish_navigation_event,
)
from ui.navigation.navigation_registry import (
    RegistryChange,
    RegistryChangeAction,
)
from ui.navigation.navigation_service import NavigationService


class ModulePlaceholder(QWidget):
    """Accessible placeholder surface for a prepared future module."""

    def __init__(self, title: str, description: str, parent: QWidget | None = None) -> None:
        """Create a centered placeholder with product context."""
        super().__init__(parent)
        self.setObjectName("modulePlaceholder")
        layout = QVBoxLayout(self)
        layout.setContentsMargins(32, 32, 32, 32)
        layout.addStretch()
        heading = QLabel(title, self)
        heading.setObjectName("moduleTitle")
        heading.setAlignment(Qt.AlignmentFlag.AlignCenter)
        detail = QLabel(description, self)
        detail.setObjectName("moduleDescription")
        detail.setWordWrap(True)
        detail.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(heading)
        layout.addWidget(detail)
        layout.addStretch()


class ModuleHost(QStackedWidget):
    """Activates one lazy module while retaining constructed modules in memory."""

    _registry_changed = Signal(object)

    def __init__(
        self,
        navigation: NavigationService,
        events: EventPublisher,
        parent: QWidget | None = None,
        logger: logging.Logger | None = None,
    ) -> None:
        """Create an empty host from injected navigation services."""
        super().__init__(parent)
        self.setObjectName("moduleHost")
        self._navigation = navigation
        self._events = events
        self._logger = logger or logging.getLogger("jochen_x.navigation.modules")
        self._modules: dict[str, QWidget] = {}
        self._active_identifier: str | None = None
        self._empty_module = QWidget(self)
        self._empty_module.setObjectName("emptyModule")
        self.addWidget(self._empty_module)
        self._registry_changed.connect(self._on_registry_changed)
        self._unsubscribe_registry = navigation.registry.subscribe(
            self._registry_changed.emit
        )
        self.destroyed.connect(lambda _: self._unsubscribe_registry())

    @property
    def active_identifier(self) -> str | None:
        """Return the currently active module identifier."""
        return self._active_identifier

    def loaded_identifiers(self) -> tuple[str, ...]:
        """Return identifiers whose module instances are retained."""
        return tuple(self._modules)

    def module(self, identifier: str) -> QWidget | None:
        """Return a loaded module without constructing it."""
        return self._modules.get(identifier)

    def activate(self, identifier: str, identity_id: str | None = None) -> QWidget:
        """Construct if necessary and activate exactly one module."""
        registration = self._navigation.resolve(identifier, identity_id)
        module = self._modules.get(identifier)
        if module is None:
            module = registration.factory()
            if not isinstance(module, QWidget):
                raise TypeError(f"Module factory did not return QWidget: {identifier}")
            self._modules[identifier] = module
            self.addWidget(module)
        previous = self._active_identifier
        if previous == identifier:
            return module
        if previous is not None:
            publish_navigation_event(
                ModuleDeactivated(previous),
                self._events,
                logger=self._logger,
            )
        self.setCurrentWidget(module)
        self._active_identifier = identifier
        publish_navigation_event(
            ModuleActivated(identifier),
            self._events,
            logger=self._logger,
        )
        return module

    def deactivate(self) -> None:
        """Deactivate the current module without destroying it."""
        if self._active_identifier is None:
            return
        previous = self._active_identifier
        self._active_identifier = None
        self.setCurrentWidget(self._empty_module)
        publish_navigation_event(
            ModuleDeactivated(previous),
            self._events,
            logger=self._logger,
        )

    def _on_registry_changed(self, change: RegistryChange) -> None:
        """Release cached widgets when their dynamic route is removed."""
        if change.action is not RegistryChangeAction.UNREGISTERED:
            return
        module = self._modules.pop(change.identifier, None)
        if module is None:
            return
        if self._active_identifier == change.identifier:
            self.deactivate()
        self.removeWidget(module)
        module.setParent(None)
        module.deleteLater()
