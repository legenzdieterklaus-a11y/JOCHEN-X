"""Desktop status bar exposing application subsystem health."""

from __future__ import annotations

from collections.abc import Callable

from PySide6.QtCore import QTimer, Signal
from PySide6.QtWidgets import QLabel, QStatusBar, QWidget

from core.events import Event, EventBus

from app.events import ApplicationEventName
from app.security import SecurityEventName, SecurityManager

_WORKER_REFRESH_INTERVAL_MS = 1_000


class StatusBar(QStatusBar):
    """Displays live lifecycle, security, worker, and plugin statuses."""

    _status_received = Signal(str, str)

    def __init__(
        self,
        events: EventBus,
        *,
        application_status: str,
        security: SecurityManager | None,
        worker_count: Callable[[], int],
        plugin_count: int,
        parent: QWidget | None = None,
    ) -> None:
        """Create a status bar from injected status sources."""
        super().__init__(parent)
        self.setObjectName("applicationStatusBar")
        self._worker_count = worker_count
        self._labels = {
            "application": QLabel(self),
            "security": QLabel(self),
            "workers": QLabel(self),
            "plugins": QLabel(self),
        }
        self._status_received.connect(self.set_subsystem_status)
        self.addWidget(self._labels["application"], 1)
        self.addPermanentWidget(self._labels["security"])
        self.addPermanentWidget(self._labels["workers"])
        self.addPermanentWidget(self._labels["plugins"])
        self.set_subsystem_status("application", application_status)
        self.set_subsystem_status(
            "security",
            "Ready" if security is not None and security.is_initialized else "Unavailable",
        )
        self.set_subsystem_status("workers", self._format_worker_status())
        self.set_subsystem_status("plugins", f"{plugin_count} discovered")
        self._unsubscribers = (
            events.subscribe(
                str(ApplicationEventName.STATE_CHANGED),
                self._on_application_state,
                receive_sticky=False,
            ),
            events.subscribe(
                str(ApplicationEventName.PLUGIN_LOADED),
                self._on_plugin_event,
                receive_sticky=False,
            ),
            events.subscribe(
                str(ApplicationEventName.PLUGIN_FAILED),
                self._on_plugin_failure,
                receive_sticky=False,
            ),
            events.subscribe(
                str(SecurityEventName.INITIALIZED),
                self._on_security_initialized,
                receive_sticky=False,
            ),
            events.subscribe(
                str(SecurityEventName.THREAT_DETECTED),
                self._on_security_threat,
                receive_sticky=False,
            ),
        )
        self._worker_timer = QTimer(self)
        self._worker_timer.setInterval(_WORKER_REFRESH_INTERVAL_MS)
        self._worker_timer.timeout.connect(self._refresh_workers)
        self._worker_timer.start()

    def subsystem_status(self, subsystem: str) -> str:
        """Return displayed text for a subsystem."""
        try:
            return self._labels[subsystem].text()
        except KeyError as error:
            raise LookupError(f"Unknown status subsystem: {subsystem}") from error

    def set_subsystem_status(self, subsystem: str, status: str) -> None:
        """Update one status field."""
        try:
            label = self._labels[subsystem]
        except KeyError as error:
            raise LookupError(f"Unknown status subsystem: {subsystem}") from error
        label.setText(f"{subsystem.title()}: {status}")

    def dispose(self) -> None:
        """Stop polling and release EventBus subscriptions."""
        self._worker_timer.stop()
        for unsubscribe in self._unsubscribers:
            unsubscribe()

    def _refresh_workers(self) -> None:
        """Refresh worker activity without blocking the UI thread."""
        self.set_subsystem_status("workers", self._format_worker_status())

    def _format_worker_status(self) -> str:
        """Format the current active worker count."""
        return f"{self._worker_count()} active"

    def _on_application_state(self, event: Event) -> None:
        self._status_received.emit("application", str(event.payload.get("current", "unknown")))

    def _on_plugin_event(self, event: Event) -> None:
        self._status_received.emit("plugins", f"Loaded {event.payload.get('identifier', '')}")

    def _on_plugin_failure(self, event: Event) -> None:
        self._status_received.emit("plugins", "Discovery warning")

    def _on_security_initialized(self, event: Event) -> None:
        self._status_received.emit("security", "Ready")

    def _on_security_threat(self, event: Event) -> None:
        severity = str(event.payload.get("severity", "unknown"))
        self._status_received.emit("security", f"Alert ({severity})")
