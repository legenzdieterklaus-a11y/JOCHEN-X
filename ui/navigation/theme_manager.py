"""Runtime theme coordinator backed exclusively by the existing ThemeEngine."""

from __future__ import annotations

from dataclasses import replace
import logging

from PySide6.QtWidgets import QApplication

from config.settings import ApplicationSettings, ConfigurationService, ThemeMode
from styles.theme import ThemeEngine, ThemeTokens

from app.events import EventPublisher, ThemeChanged


class ThemeManager:
    """Applies and persists theme choices without implementing a theme engine."""

    def __init__(
        self,
        application: QApplication,
        engine: ThemeEngine,
        configuration: ConfigurationService,
        settings: ApplicationSettings,
        events: EventPublisher,
        logger: logging.Logger | None = None,
    ) -> None:
        """Create a theme coordinator from existing foundation services."""
        self._application = application
        self._engine = engine
        self._configuration = configuration
        self._settings = settings
        self._events = events
        self._logger = logger or logging.getLogger("jochen_x.navigation.theme")
        self._custom_themes: dict[str, ThemeTokens] = {}
        self._custom_theme: str | None = None

    @property
    def current_mode(self) -> ThemeMode:
        """Return the persisted built-in theme mode."""
        return self._settings.theme_mode

    @property
    def current_custom_theme(self) -> str | None:
        """Return the active custom theme identifier."""
        return self._custom_theme

    def apply_current(self) -> None:
        """Apply the configured theme to the Qt application."""
        tokens = self._engine.select(self._settings.theme_mode)
        self._apply(tokens)

    def set_mode(self, mode: ThemeMode) -> None:
        """Persist and apply a System, Light, or Dark mode."""
        updated = replace(self._settings, theme_mode=mode)
        self._configuration.save_profile(updated)
        self._settings = updated
        self._custom_theme = None
        self.apply_current()
        self._publish_changed(mode.value)

    def register_custom(self, identifier: str, tokens: ThemeTokens) -> None:
        """Register tokens for future plugin- or user-provided themes."""
        normalized = identifier.strip()
        if not normalized:
            raise ValueError("Custom theme identifier must not be empty")
        if normalized in self._custom_themes:
            raise ValueError(f"Custom theme already registered: {normalized}")
        self._custom_themes[normalized] = tokens

    def apply_custom(self, identifier: str) -> None:
        """Apply registered custom tokens through the existing engine renderer."""
        try:
            tokens = self._custom_themes[identifier]
        except KeyError as error:
            raise LookupError(f"Custom theme is not registered: {identifier}") from error
        self._apply(tokens)
        self._custom_theme = identifier
        self._publish_changed(identifier)

    def _publish_changed(self, mode: str) -> None:
        """Notify observers without turning a completed theme change into failure."""
        try:
            ThemeChanged(mode).publish(self._events, sticky=True)
        except Exception as error:
            self._logger.error(
                "navigation.theme_event_failed",
                exc_info=error,
                extra={"context": {"mode": mode}},
            )

    def _apply(self, tokens: ThemeTokens) -> None:
        """Apply base-engine output plus desktop component presentation rules."""
        spacing = tokens.spacing
        desktop = f"""
            QToolBar#mainToolbar {{
                background: {tokens.surface};
                border: none;
                spacing: {spacing}px;
                padding: {spacing}px;
            }}
            QLineEdit#globalSearch {{
                background: {tokens.background};
                border: 1px solid {tokens.surface};
                border-radius: {spacing}px;
                padding: {spacing}px;
            }}
            QFrame#navigationSidebar {{
                background: {tokens.surface};
                border: none;
            }}
            QPushButton#navigationItem {{
                border: none;
                border-radius: {spacing}px;
                padding: {spacing}px;
                text-align: left;
            }}
            QPushButton#navigationItem:hover {{
                background: {tokens.background};
            }}
            QPushButton#navigationItem:checked {{
                background: {tokens.accent};
                color: {tokens.background};
            }}
            QLabel#pageTitle {{
                font-size: 24px;
                font-weight: 600;
            }}
            QLabel#pageSubtitle, QLabel#moduleDescription {{
                font-size: 12px;
            }}
            QLabel#moduleTitle {{
                font-size: 22px;
                font-weight: 600;
            }}
            QStatusBar#applicationStatusBar {{
                background: {tokens.surface};
            }}
        """
        self._application.setStyleSheet(self._engine.stylesheet(tokens) + desktop)
