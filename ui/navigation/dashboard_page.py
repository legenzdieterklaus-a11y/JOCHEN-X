"""Dashboard start page for the JOCHEN X desktop shell."""

from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QFrame, QGridLayout, QLabel, QVBoxLayout, QWidget

from app.context import ApplicationContext
from app.events import EventPublisher
from app.security import SecurityManager
from ui.navigation.navigation_events import DashboardLoaded, publish_navigation_event


class DashboardPage(QWidget):
    """Lightweight overview of the initialized application foundation."""

    def __init__(
        self,
        context: ApplicationContext,
        security: SecurityManager | None,
        plugin_count: int,
        events: EventPublisher,
        parent: QWidget | None = None,
    ) -> None:
        """Create the dashboard from immutable runtime context."""
        super().__init__(parent)
        self.setObjectName("dashboardPage")
        layout = QVBoxLayout(self)
        layout.setContentsMargins(32, 28, 32, 28)
        title = QLabel("Dashboard", self)
        title.setObjectName("pageTitle")
        subtitle = QLabel(
            f"{context.settings.name} {context.settings.version} is ready.",
            self,
        )
        subtitle.setObjectName("pageSubtitle")
        layout.addWidget(title)
        layout.addWidget(subtitle)
        cards = QGridLayout()
        cards.setSpacing(16)
        cards.addWidget(
            self._card("Application", context.runtime_state.state.value),
            0,
            0,
        )
        cards.addWidget(
            self._card(
                "Security",
                "Ready" if security is not None and security.is_initialized else "Unavailable",
            ),
            0,
            1,
        )
        cards.addWidget(
            self._card("Plugins", f"{plugin_count} discovered"),
            1,
            0,
        )
        cards.addWidget(
            self._card("Theme", context.settings.theme_mode.value.title()),
            1,
            1,
        )
        layout.addLayout(cards)
        layout.addStretch()
        publish_navigation_event(
            DashboardLoaded(),
            events,
            logger=context.logger,
        )

    def _card(self, title: str, value: str) -> QFrame:
        """Build one theme-compatible dashboard status card."""
        card = QFrame(self)
        card.setObjectName("surface")
        card.setFrameShape(QFrame.Shape.StyledPanel)
        layout = QVBoxLayout(card)
        label = QLabel(title, card)
        label.setObjectName("dashboardCardTitle")
        value_label = QLabel(value, card)
        value_label.setObjectName("dashboardCardValue")
        value_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(label)
        layout.addWidget(value_label)
        return card
