"""Event-driven threat detection for the Security Foundation.

:class:`ThreatDetector` observes the shared :class:`core.events.EventBus` and
raises :class:`~app.security.models.ThreatReport` records when it recognises a
suspicious pattern, currently a burst of permission denials for the same
identity inside a sliding time window. It subscribes to the existing bus rather
than introducing any new event channel, and publishes its findings back onto the
same bus as :class:`~app.security.events.ThreatDetected` events.
"""

from __future__ import annotations

import logging
import time
from collections import defaultdict, deque
from collections.abc import Callable
from threading import RLock
from uuid import uuid4

from core.events import Event, EventBus

from app.security.events import SecurityEventName, ThreatDetected
from app.security.models import ThreatReport, ThreatSeverity

_LOGGER_NAME = "jochen_x.security.threats"
_DEFAULT_THRESHOLD = 3
_DEFAULT_WINDOW_SECONDS = 30.0
_CATEGORY_BRUTE_FORCE = "brute_force"


class ThreatDetector:
    """Observes security events and reports suspicious permission-denial bursts."""

    def __init__(
        self,
        events: EventBus,
        *,
        logger: logging.Logger | None = None,
        threshold: int = _DEFAULT_THRESHOLD,
        window_seconds: float = _DEFAULT_WINDOW_SECONDS,
    ) -> None:
        """Create the detector.

        Args:
            events: The shared event bus to observe and publish onto.
            logger: Optional logger for diagnostics.
            threshold: Number of denials within the window that trigger a report.
            window_seconds: Length of the sliding detection window in seconds.

        Raises:
            ValueError: If ``threshold`` or ``window_seconds`` are not positive.
        """
        if threshold < 1:
            raise ValueError("threshold must be positive")
        if window_seconds <= 0:
            raise ValueError("window_seconds must be positive")
        self._events = events
        self._logger = logger or logging.getLogger(_LOGGER_NAME)
        self._threshold = threshold
        self._window_seconds = window_seconds
        self._denials: dict[str, deque[float]] = defaultdict(deque)
        self._reports: list[ThreatReport] = []
        self._unsubscribe: Callable[[], None] | None = None
        self._lock = RLock()

    def start(self) -> None:
        """Begin observing the event bus. Idempotent."""
        with self._lock:
            if self._unsubscribe is not None:
                return
            self._unsubscribe = self._events.subscribe(
                str(SecurityEventName.PERMISSION_DENIED), self._on_permission_denied
            )
        self._logger.info("threats.started")

    def stop(self) -> None:
        """Stop observing the event bus and release the subscription. Idempotent."""
        with self._lock:
            unsubscribe = self._unsubscribe
            self._unsubscribe = None
        if unsubscribe is not None:
            unsubscribe()
            self._logger.info("threats.stopped")

    def reports(self) -> tuple[ThreatReport, ...]:
        """Return a defensive copy of every threat report raised so far."""
        with self._lock:
            return tuple(self._reports)

    def _on_permission_denied(self, event: Event) -> None:
        """Handle a permission-denied event and evaluate the detection window."""
        identity = str(event.payload.get("identity", ""))
        now = time.monotonic()
        with self._lock:
            timestamps = self._denials[identity]
            timestamps.append(now)
            self._prune(timestamps, now)
            if len(timestamps) < self._threshold:
                return
            timestamps.clear()
            report = self._build_report(identity)
            self._reports.append(report)
        self._logger.warning(
            "threat.detected",
            extra={"context": {"identity": identity, "category": report.category}},
        )
        ThreatDetected(
            report.identifier, report.severity.value, report.category
        ).publish(self._events)

    def _prune(self, timestamps: deque[float], now: float) -> None:
        """Drop timestamps that fall outside the sliding window."""
        cutoff = now - self._window_seconds
        while timestamps and timestamps[0] < cutoff:
            timestamps.popleft()

    def _build_report(self, identity: str) -> ThreatReport:
        """Create a threat report for a detected permission-denial burst."""
        return ThreatReport(
            identifier=uuid4().hex,
            timestamp=time.time(),
            severity=ThreatSeverity.HIGH,
            category=_CATEGORY_BRUTE_FORCE,
            description=(
                f"Identity '{identity}' exceeded {self._threshold} permission denials "
                f"within {self._window_seconds:g}s"
            ),
            related_events=(str(SecurityEventName.PERMISSION_DENIED),),
        )
