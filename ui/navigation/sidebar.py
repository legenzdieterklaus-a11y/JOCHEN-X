"""Collapsible, grouped sidebar backed by the navigation service."""

from __future__ import annotations

import logging

from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QFrame,
    QScrollArea,
    QToolButton,
    QVBoxLayout,
    QWidget,
)

from app.events import EventPublisher
from ui.navigation.navigation_events import (
    SidebarCollapsed,
    SidebarExpanded,
    publish_navigation_event,
)
from ui.navigation.navigation_models import NavigationGroup
from ui.navigation.navigation_service import NavigationService
from ui.navigation.sidebar_section import SidebarSection

_EXPANDED_WIDTH = 260
_COLLAPSED_WIDTH = 72

_GROUP_TITLES: dict[NavigationGroup, str] = {
    NavigationGroup.GENERAL: "General",
    NavigationGroup.WORKSPACE: "Workspace",
    NavigationGroup.PLATFORM: "Platform",
    NavigationGroup.SYSTEM: "System",
}


class Sidebar(QFrame):
    """Collapsible route selector supporting groups and nested entries."""

    navigation_requested = Signal(str)
    collapse_changed = Signal(bool)
    _registry_changed = Signal()

    def __init__(
        self,
        navigation: NavigationService,
        events: EventPublisher,
        parent: QWidget | None = None,
        logger: logging.Logger | None = None,
    ) -> None:
        """Create a sidebar from navigation metadata."""
        super().__init__(parent)
        self.setObjectName("navigationSidebar")
        self._navigation = navigation
        self._events = events
        self._logger = logger or logging.getLogger("jochen_x.navigation.sidebar")
        self._collapsed = False
        self._active_identifier: str | None = None
        self._sections: list[SidebarSection] = []
        self._toggle = QToolButton(self)
        self._toggle.setObjectName("sidebarToggle")
        self._toggle.setText("‹")
        self._toggle.setToolTip("Collapse sidebar")
        self._toggle.clicked.connect(self.toggle)

        root_layout = QVBoxLayout(self)
        root_layout.setContentsMargins(0, 8, 0, 8)
        root_layout.addWidget(self._toggle)
        scroll = QScrollArea(self)
        scroll.setObjectName("sidebarScroll")
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        self._content = QWidget(scroll)
        self._content_layout = QVBoxLayout(self._content)
        self._content_layout.setContentsMargins(0, 0, 0, 0)
        scroll.setWidget(self._content)
        root_layout.addWidget(scroll, 1)
        self.setFixedWidth(_EXPANDED_WIDTH)
        self._registry_changed.connect(self._rebuild)
        self._unsubscribe_registry = navigation.registry.subscribe(
            lambda _change: self._registry_changed.emit()
        )
        self.destroyed.connect(lambda _: self._unsubscribe_registry())
        self._rebuild()

    def _rebuild(self) -> None:
        """Rebuild sections after dynamic registry changes on the UI thread."""
        while self._content_layout.count():
            item = self._content_layout.takeAt(0)
            if item is None:
                break
            widget = item.widget()
            if widget is not None:
                widget.setParent(None)
                widget.deleteLater()
        self._sections.clear()
        destinations = self._navigation.destinations()
        for group in NavigationGroup:
            items = tuple(item for item in destinations if item.group is group)
            if not items:
                continue
            section = SidebarSection(
                _GROUP_TITLES[group],
                items,
                self.navigation_requested.emit,
                self._content,
            )
            section.set_collapsed(self._collapsed)
            self._content_layout.addWidget(section)
            self._sections.append(section)
        self._content_layout.addStretch()
        if self._active_identifier is not None:
            self.set_active(self._active_identifier)

    @property
    def is_collapsed(self) -> bool:
        """Return whether compact mode is active."""
        return self._collapsed

    def set_active(self, identifier: str) -> None:
        """Highlight the active destination."""
        self._active_identifier = identifier
        for section in self._sections:
            section.set_active(identifier)

    def toggle(self) -> None:
        """Toggle compact mode."""
        self.set_collapsed(not self._collapsed)

    def set_collapsed(self, collapsed: bool) -> None:
        """Apply compact or expanded mode and publish the state change."""
        if self._collapsed == collapsed:
            return
        self._collapsed = collapsed
        self.setFixedWidth(_COLLAPSED_WIDTH if collapsed else _EXPANDED_WIDTH)
        self._toggle.setText("›" if collapsed else "‹")
        self._toggle.setToolTip("Expand sidebar" if collapsed else "Collapse sidebar")
        for section in self._sections:
            section.set_collapsed(collapsed)
        if collapsed:
            event = SidebarCollapsed()
        else:
            event = SidebarExpanded()
        publish_navigation_event(event, self._events, logger=self._logger)
        self.collapse_changed.emit(collapsed)
