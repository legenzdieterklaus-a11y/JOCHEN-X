"""Top application toolbar with prepared interaction surfaces."""

from __future__ import annotations

from collections.abc import Callable

from PySide6.QtCore import QSize, Signal
from PySide6.QtGui import QAction
from PySide6.QtWidgets import (
    QLineEdit,
    QSizePolicy,
    QStyle,
    QToolBar,
    QToolButton,
    QWidget,
)


class Toolbar(QToolBar):
    """Non-blocking toolbar prepared for global desktop actions."""

    search_requested = Signal(str)
    user_requested = Signal()
    notifications_requested = Signal()
    settings_requested = Signal()
    quick_actions_requested = Signal()

    def __init__(self, parent: QWidget | None = None) -> None:
        """Create toolbar controls without product feature logic."""
        super().__init__("Main toolbar", parent)
        self.setObjectName("mainToolbar")
        self.setMovable(False)
        self.setIconSize(QSize(18, 18))
        self.back_action = QAction(
            self.style().standardIcon(QStyle.StandardPixmap.SP_ArrowBack),
            "Back",
            self,
        )
        self.forward_action = QAction(
            self.style().standardIcon(QStyle.StandardPixmap.SP_ArrowForward),
            "Forward",
            self,
        )
        self.back_action.setEnabled(False)
        self.forward_action.setEnabled(False)
        self.addAction(self.back_action)
        self.addAction(self.forward_action)
        self.addSeparator()

        self.search = QLineEdit(self)
        self.search.setObjectName("globalSearch")
        self.search.setPlaceholderText("Search JOCHEN X")
        self.search.setClearButtonEnabled(True)
        self.search.setMaximumWidth(420)
        self.search.returnPressed.connect(
            lambda: self.search_requested.emit(self.search.text().strip())
        )
        self.addWidget(self.search)
        expanding = QWidget(self)
        expanding.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Preferred,
        )
        self.addWidget(expanding)
        self._add_button("Quick actions", self.quick_actions_requested.emit)
        self._add_button("Notifications", self.notifications_requested.emit)
        self._add_button("User", self.user_requested.emit)
        self._add_button("Settings", self.settings_requested.emit)

    def set_history_state(self, can_go_back: bool, can_go_forward: bool) -> None:
        """Synchronize navigation history action availability."""
        self.back_action.setEnabled(can_go_back)
        self.forward_action.setEnabled(can_go_forward)

    def _add_button(self, text: str, callback: Callable[[], None]) -> None:
        """Add a prepared toolbar button."""
        button = QToolButton(self)
        button.setText(text)
        button.setToolTip(text)
        button.setAutoRaise(True)
        button.clicked.connect(lambda checked=False: callback())
        self.addWidget(button)
