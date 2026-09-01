"""Monitoring overview page showing collected state per subject."""

from __future__ import annotations

from collections.abc import Callable

from PySide6.QtCore import QMetaObject, Qt, Q_ARG, Slot
from PySide6.QtWidgets import (
    QHeaderView,
    QLabel,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from core.events import Event, EventBus
from services.monitoring import MonitoringStateCollector

__all__ = ["MonitoringPage"]

_COLUMNS = ("Host", "Subject", "Status", "Since", "Transitions")


class MonitoringPage(QWidget):
    """Displays monitoring states with live event subscription."""

    def __init__(
        self,
        collector: MonitoringStateCollector,
        events: EventBus,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        self.setObjectName("monitoringPage")
        self._collector = collector
        self._events = events
        self._unsubscribe: Callable[[], None] | None = None

        layout = QVBoxLayout(self)
        layout.setContentsMargins(32, 28, 32, 28)

        title = QLabel("Monitoring", self)
        title.setObjectName("pageTitle")
        layout.addWidget(title)

        self._table = QTableWidget(0, len(_COLUMNS), self)
        self._table.setHorizontalHeaderLabels(list(_COLUMNS))
        self._table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self._table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self._table.verticalHeader().setVisible(False)
        header = self._table.horizontalHeader()
        header.setStretchLastSection(True)
        header.setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        layout.addWidget(self._table)

        self._load_states()
        self._unsubscribe = self._events.subscribe(
            "monitoring.*", self._on_event, receive_sticky=False,
        )

    def _load_states(self) -> None:
        states = self._collector.states()
        self._table.setRowCount(len(states))
        for row, state in enumerate(states):
            self._table.setItem(row, 0, QTableWidgetItem(state.host_id))
            self._table.setItem(row, 1, QTableWidgetItem(state.subject))
            self._table.setItem(row, 2, QTableWidgetItem(state.status))
            self._table.setItem(row, 3, QTableWidgetItem(state.since))
            self._table.setItem(row, 4, QTableWidgetItem(str(state.transitions)))

    def _on_event(self, event: Event) -> None:
        QMetaObject.invokeMethod(
            self, "_refresh", Qt.ConnectionType.QueuedConnection,
        )

    @Slot()
    def _refresh(self) -> None:
        self._load_states()

    def closeEvent(self, event: object) -> None:
        if self._unsubscribe is not None:
            self._unsubscribe()
            self._unsubscribe = None
        super().closeEvent(event)  # type: ignore[arg-type]
