"""Persistent main-window geometry and layout state management."""

from __future__ import annotations

import logging

from PySide6.QtCore import QByteArray, QSettings
from PySide6.QtWidgets import QMainWindow

from app.events import EventPublisher
from ui.navigation.layout_manager import LayoutManager
from ui.navigation.navigation_events import (
    WindowStateChanged,
    publish_navigation_event,
)

_GEOMETRY_KEY = "main_window/geometry"
_DOCK_STATE_KEY = "main_window/dock_state"
_SPLITTER_STATE_KEY = "main_window/splitter_state"
_MAXIMIZED_KEY = "main_window/maximized"
_WINDOW_STATE_VERSION = 1


class WindowState:
    """Saves and restores desktop window state through injected QSettings."""

    def __init__(
        self,
        settings: QSettings,
        events: EventPublisher,
        layout: LayoutManager,
        logger: logging.Logger | None = None,
    ) -> None:
        """Create a state manager."""
        self._settings = settings
        self._events = events
        self._layout = layout
        self._logger = logger or logging.getLogger("jochen_x.navigation.window")

    def restore(self, window: QMainWindow) -> bool:
        """Restore available geometry, docks, and splitter state."""
        restored = False
        geometry = self._settings.value(_GEOMETRY_KEY)
        if isinstance(geometry, QByteArray) and not geometry.isEmpty():
            restored = window.restoreGeometry(geometry)
        dock_state = self._settings.value(_DOCK_STATE_KEY)
        if isinstance(dock_state, QByteArray) and not dock_state.isEmpty():
            window.restoreState(dock_state, _WINDOW_STATE_VERSION)
        splitter_state = self._settings.value(_SPLITTER_STATE_KEY)
        if isinstance(splitter_state, QByteArray):
            self._layout.restore_state(splitter_state)
        maximized = self._settings.value(_MAXIMIZED_KEY, False, type=bool)
        if maximized:
            window.showMaximized()
        return restored

    def save(self, window: QMainWindow) -> None:
        """Persist current geometry and publish a typed state event."""
        self._settings.setValue(_GEOMETRY_KEY, window.saveGeometry())
        self._settings.setValue(
            _DOCK_STATE_KEY,
            window.saveState(_WINDOW_STATE_VERSION),
        )
        self._settings.setValue(
            _SPLITTER_STATE_KEY,
            self._layout.save_state(),
        )
        self._settings.setValue(_MAXIMIZED_KEY, window.isMaximized())
        self._settings.sync()
        publish_navigation_event(
            WindowStateChanged(
                maximized=window.isMaximized(),
                width=window.width(),
                height=window.height(),
            ),
            self._events,
            logger=self._logger,
            sticky=True,
        )
