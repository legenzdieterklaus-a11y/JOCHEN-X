"""Encrypted backup preparation for the Security Foundation.

:class:`BackupManager` prepares the mechanism for encrypted backups of small,
structured payloads. Payloads are serialized and protected through the shared
:class:`~app.security.encryption_service.EncryptionService`, so upgrading to a
real cryptographic backend later immediately encrypts every backup without any
API change. Storage is in-memory for this phase; durable and cloud backends are
explicitly out of scope until a later version.
"""

from __future__ import annotations

import json
import logging
import time
from collections.abc import Mapping
from dataclasses import dataclass, field
from threading import RLock
from uuid import uuid4

from app.events import EventPublisher
from app.security.encryption_service import EncryptionService
from app.security.events import BackupCreated, BackupRestored
from app.security.exceptions import SecurityError

_LOGGER_NAME = "jochen_x.security.backup"
_ENCODING = "utf-8"


@dataclass(frozen=True, slots=True)
class BackupRecord:
    """Public, non-sensitive descriptor of a stored backup.

    Attributes:
        identifier: Stable, unique identifier of the backup.
        name: Human-readable label for the backup.
        created_at: Wall-clock creation timestamp in seconds since the epoch.
        size: Size of the protected payload in bytes.
    """

    identifier: str
    name: str
    created_at: float
    size: int


@dataclass(slots=True)
class _StoredBackup:
    """Internal at-rest representation of a backup."""

    record: BackupRecord
    ciphertext: bytes = field(repr=False)


class BackupManager:
    """Thread-safe manager for creating and restoring encrypted backups."""

    def __init__(
        self,
        encryption: EncryptionService,
        events: EventPublisher,
        *,
        logger: logging.Logger | None = None,
    ) -> None:
        """Create an empty backup manager.

        Args:
            encryption: Service used to protect backup payloads at rest.
            events: Publisher port used to broadcast backup events.
            logger: Optional logger for diagnostics.
        """
        self._encryption = encryption
        self._events = events
        self._logger = logger or logging.getLogger(_LOGGER_NAME)
        self._backups: dict[str, _StoredBackup] = {}
        self._lock = RLock()

    def create_backup(self, name: str, payload: Mapping[str, str]) -> BackupRecord:
        """Serialize, encrypt, and store ``payload`` under a new backup record.

        Args:
            name: Human-readable label for the backup.
            payload: The structured data to protect.

        Returns:
            The public :class:`BackupRecord` describing the stored backup.

        Raises:
            ValueError: If ``name`` is empty.
        """
        if not name:
            raise ValueError("Backup name must be a non-empty string")
        serialized = json.dumps(dict(payload), sort_keys=True).encode(_ENCODING)
        ciphertext = self._encryption.encrypt(serialized)
        record = BackupRecord(
            identifier=uuid4().hex,
            name=name,
            created_at=time.time(),
            size=len(ciphertext),
        )
        with self._lock:
            self._backups[record.identifier] = _StoredBackup(record=record, ciphertext=ciphertext)
        self._logger.info("backup.created", extra={"context": {"identifier": record.identifier}})
        BackupCreated(record.identifier).publish(self._events)
        return record

    def restore_backup(self, identifier: str) -> dict[str, str]:
        """Decrypt and return the payload of a stored backup.

        Args:
            identifier: Identifier of the backup to restore.

        Returns:
            The original payload mapping.

        Raises:
            SecurityError: If the backup does not exist.
        """
        with self._lock:
            stored = self._backups.get(identifier)
        if stored is None:
            raise SecurityError(f"Unknown backup: {identifier}")
        serialized = self._encryption.decrypt(stored.ciphertext).decode(_ENCODING)
        payload: dict[str, str] = json.loads(serialized)
        self._logger.info("backup.restored", extra={"context": {"identifier": identifier}})
        BackupRestored(identifier).publish(self._events)
        return payload

    def list_backups(self) -> tuple[BackupRecord, ...]:
        """Return all backup records, ordered by creation time."""
        with self._lock:
            return tuple(
                sorted(
                    (stored.record for stored in self._backups.values()),
                    key=lambda item: item.created_at,
                )
            )
