"""Audit log protocol for tamper-proof event recording."""

from __future__ import annotations

from collections.abc import Sequence
from typing import Protocol, runtime_checkable

from jochen_x.core.types.events import RuntimeEvent

__all__ = ["IAuditLog"]


@runtime_checkable
class IAuditLog(Protocol):
    """Protocol for the audit logging system.

    The audit log provides tamper-proof, append-only recording of
    security-relevant runtime events.  It guarantees write-ahead
    semantics (no audit entry may be lost) and integrity verification
    (tamper detection).

    Audited events include runtime start/stop/restart, recovery
    actions, security violations, and plugin lifecycle transitions.
    """

    def record(self, event: RuntimeEvent) -> None:
        """Record an audit event.

        The entry is persisted with a timestamp and a monotonically
        increasing sequence number.  Integrity protection is applied
        automatically.

        Args:
            event: The runtime event to audit.

        Raises:
            JochenXError: If the entry cannot be persisted.

        """
        ...

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
        ...

    def verify_integrity(self) -> bool:
        """Verify the integrity of the entire audit log.

        Returns:
            ``True`` if the log passes integrity verification,
            ``False`` if tampering is detected.

        """
        ...
