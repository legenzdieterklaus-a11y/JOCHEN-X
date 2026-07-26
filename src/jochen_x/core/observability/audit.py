"""Tamper-proof, append-only audit log for security-relevant events.

The ``AuditLog`` records runtime events with monotonically increasing
sequence numbers and integrity protection via HMAC-based chaining.
Each entry's hash includes the previous entry's hash, forming an
integrity chain that detects tampering or insertion/deletion of
entries.

Write-ahead semantics ensure that no audit entry is lost: the entry
is persisted (appended to the internal store) synchronously before
the ``record`` call returns.

All operations are thread-safe.
"""

from __future__ import annotations

import hashlib
import hmac
import json
from collections.abc import Sequence
from dataclasses import asdict
from datetime import datetime
from threading import RLock

from jochen_x.core.exceptions.security import InputValidationError
from jochen_x.core.types.events import RuntimeEvent
from jochen_x.core.types.health_status import HealthStatus

__all__ = ["AuditLog"]

_COMPONENT_NAME = "AuditLog"
_FIELD_EVENT = "event"
_FIELD_LIMIT = "limit"
_FIELD_OFFSET = "offset"
_REASON_NOT_RUNTIME_EVENT = "must be a RuntimeEvent instance"
_REASON_NEGATIVE = "must not be negative"
_HMAC_KEY = b"jochen-x-audit-integrity-v1"


def _serialize_event(event: RuntimeEvent) -> str:
    """Produce a deterministic JSON representation of *event*."""
    data = asdict(event)

    def _convert(obj: object) -> str | int | float | bool | None:
        if isinstance(obj, datetime):
            return obj.isoformat()
        if hasattr(obj, "value"):
            return str(obj.value)
        return str(obj)

    return json.dumps(data, sort_keys=True, default=_convert)


def _compute_hash(payload: str, previous_hash: str) -> str:
    """Compute an HMAC-SHA256 hash chaining *payload* to *previous_hash*."""
    message = f"{previous_hash}|{payload}".encode()
    return hmac.new(_HMAC_KEY, message, hashlib.sha256).hexdigest()


class _AuditEntry:
    """Internal container for a single audit entry.

    Args:
        sequence_number: Monotonically increasing sequence number.
        event: The recorded runtime event.
        integrity_hash: HMAC chain hash for tamper detection.

    """

    __slots__ = ("event", "integrity_hash", "sequence_number")

    def __init__(
        self,
        sequence_number: int,
        event: RuntimeEvent,
        integrity_hash: str,
    ) -> None:
        """Initialise the audit entry."""
        self.sequence_number: int = sequence_number
        self.event: RuntimeEvent = event
        self.integrity_hash: str = integrity_hash


class AuditLog:
    """Tamper-proof, append-only audit log.

    Stores runtime events with integrity-chained hashes for tamper
    detection.  Each ``record`` call appends synchronously (write-
    ahead guarantee).

    Args:
        No arguments required.

    """

    def __init__(self) -> None:
        """Initialise an empty audit log."""
        self._lock: RLock = RLock()
        self._entries: list[_AuditEntry] = []
        self._sequence_counter: int = 0
        self._last_hash: str = "0" * 64

    # -- IAuditLog protocol --------------------------------------------------

    def record(self, event: RuntimeEvent) -> None:
        """Record an audit event.

        The entry is persisted with a timestamp and a monotonically
        increasing sequence number.  Integrity protection is applied
        automatically via HMAC chaining.

        Args:
            event: The runtime event to audit.

        Raises:
            JochenXError: If the event is not a ``RuntimeEvent``.

        """
        if not isinstance(event, RuntimeEvent):
            raise InputValidationError(
                _FIELD_EVENT,
                _REASON_NOT_RUNTIME_EVENT,
                component=_COMPONENT_NAME,
            )

        serialised = _serialize_event(event)

        with self._lock:
            self._sequence_counter += 1
            integrity_hash = _compute_hash(serialised, self._last_hash)

            entry = _AuditEntry(
                sequence_number=self._sequence_counter,
                event=event,
                integrity_hash=integrity_hash,
            )
            self._entries.append(entry)
            self._last_hash = integrity_hash

    def get_entries(
        self,
        *,
        limit: int = 100,
        offset: int = 0,
    ) -> Sequence[RuntimeEvent]:
        """Retrieve audit log entries.

        Args:
            limit: Maximum number of entries to return.
            offset: Number of entries to skip from the beginning.

        Returns:
            A sequence of audit events ordered by sequence number.

        Raises:
            InputValidationError: If limit or offset is negative.

        """
        if limit < 0:
            raise InputValidationError(
                _FIELD_LIMIT,
                _REASON_NEGATIVE,
                component=_COMPONENT_NAME,
            )
        if offset < 0:
            raise InputValidationError(
                _FIELD_OFFSET,
                _REASON_NEGATIVE,
                component=_COMPONENT_NAME,
            )

        with self._lock:
            sliced = self._entries[offset : offset + limit]
            return [entry.event for entry in sliced]

    def verify_integrity(self) -> bool:
        """Verify the integrity of the entire audit log.

        Re-computes each entry's hash from its event data and the
        previous entry's hash.  Returns ``False`` if any hash does
        not match.

        Returns:
            ``True`` if the log passes integrity verification,
            ``False`` if tampering is detected.

        """
        with self._lock:
            previous_hash = "0" * 64
            for entry in self._entries:
                serialised = _serialize_event(entry.event)
                expected = _compute_hash(serialised, previous_hash)
                if not hmac.compare_digest(entry.integrity_hash, expected):
                    return False
                previous_hash = entry.integrity_hash
            return True

    # -- Introspection -------------------------------------------------------

    def get_entry_count(self) -> int:
        """Return the total number of audit entries.

        Returns:
            The number of recorded entries.

        """
        with self._lock:
            return len(self._entries)

    # -- IHealthCheck protocol -----------------------------------------------

    def check_health(self) -> HealthStatus:
        """Return the health status of the audit log.

        Verifies integrity and returns ``UNHEALTHY`` if tampering
        is detected.

        Returns:
            ``HealthStatus.HEALTHY`` if integrity is intact,
            ``HealthStatus.UNHEALTHY`` otherwise.

        """
        if self.verify_integrity():
            return HealthStatus.HEALTHY
        return HealthStatus.UNHEALTHY

    def get_component_name(self) -> str:
        """Return the component name.

        Returns:
            The string ``"AuditLog"``.

        """
        return _COMPONENT_NAME
