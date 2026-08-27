"""Append-only audit logging for the Security Foundation.

:class:`AuditLogger` records security-relevant actions as an ordered, immutable
sequence. Entries can only ever be appended; there is no API to mutate or delete
a recorded entry, and callers only ever receive defensive copies. This gives the
subsystem a tamper-evident trail that later phases can persist or sign.
"""

from __future__ import annotations

import logging
import time
from collections.abc import Mapping
from threading import RLock
from types import MappingProxyType

from app.security.models import AuditEntry, AuditOutcome

_LOGGER_NAME = "jochen_x.security.audit"


class AuditLogger:
    """Thread-safe, append-only store of immutable audit entries."""

    def __init__(self, *, logger: logging.Logger | None = None) -> None:
        """Create an empty audit log.

        Args:
            logger: Optional logger for diagnostics.
        """
        self._logger = logger or logging.getLogger(_LOGGER_NAME)
        self._entries: list[AuditEntry] = []
        self._sequence = 0
        self._lock = RLock()

    def record(
        self,
        category: str,
        action: str,
        actor: str,
        *,
        outcome: AuditOutcome = AuditOutcome.SUCCESS,
        detail: Mapping[str, str] | None = None,
    ) -> AuditEntry:
        """Append a new immutable audit entry and return it.

        Args:
            category: Coarse subsystem category the action belongs to.
            action: The specific action performed.
            actor: Identifier of the principal that performed the action.
            outcome: Classified outcome of the action.
            detail: Additional non-sensitive contextual detail.

        Returns:
            The recorded :class:`~app.security.models.AuditEntry`.
        """
        frozen_detail: Mapping[str, str] = MappingProxyType(dict(detail or {}))
        with self._lock:
            self._sequence += 1
            entry = AuditEntry(
                sequence=self._sequence,
                timestamp=time.time(),
                category=category,
                action=action,
                actor=actor,
                outcome=outcome,
                detail=frozen_detail,
            )
            self._entries.append(entry)
        self._logger.info(
            "audit.recorded",
            extra={
                "context": {"sequence": entry.sequence, "action": action, "outcome": outcome.value}
            },
        )
        return entry

    def entries(self) -> tuple[AuditEntry, ...]:
        """Return a defensive, ordered copy of every recorded entry."""
        with self._lock:
            return tuple(self._entries)

    def count(self) -> int:
        """Return the number of entries recorded so far."""
        with self._lock:
            return len(self._entries)
