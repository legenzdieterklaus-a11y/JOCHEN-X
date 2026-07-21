"""In-memory, encryption-backed secret storage.

:class:`SecretVault` is the single owner of sensitive values inside the running
process. Values are held only in their encrypted representation and decrypted on
demand, so switching :class:`~app.security.encryption_service.EncryptionService`
to a real cryptographic backend later immediately protects data at rest without
any change to callers. Every mutation and read emits a typed security event via
the shared event bus.
"""

from __future__ import annotations

import logging
import time
from collections.abc import Mapping
from dataclasses import dataclass, field
from threading import RLock
from types import MappingProxyType

from app.events import EventPublisher
from app.security.encryption_service import EncryptionService
from app.security.events import SecretDeleted, SecretRead, SecretStored
from app.security.exceptions import SecretNotFoundError
from app.security.models import Secret

_LOGGER_NAME = "jochen_x.security.vault"
_ENCODING = "utf-8"


@dataclass(slots=True)
class _VaultEntry:
    """Internal at-rest representation of a stored secret."""

    ciphertext: bytes
    created_at: float
    metadata: Mapping[str, str] = field(default_factory=dict)


class SecretVault:
    """Thread-safe, in-memory vault that stores secrets in encrypted form."""

    def __init__(
        self,
        encryption: EncryptionService,
        events: EventPublisher,
        *,
        logger: logging.Logger | None = None,
    ) -> None:
        """Create an empty vault.

        Args:
            encryption: Service used to protect values at rest.
            events: Publisher port used to broadcast vault events.
            logger: Optional logger for diagnostics.
        """
        self._encryption = encryption
        self._events = events
        self._logger = logger or logging.getLogger(_LOGGER_NAME)
        self._entries: dict[str, _VaultEntry] = {}
        self._lock = RLock()

    def store(self, name: str, value: str, *, metadata: Mapping[str, str] | None = None) -> Secret:
        """Encrypt and store ``value`` under ``name``, replacing any existing secret.

        Args:
            name: Unique identifier for the secret.
            value: The sensitive value to protect.
            metadata: Optional non-sensitive descriptive metadata.

        Returns:
            The stored :class:`~app.security.models.Secret` with its plaintext value.

        Raises:
            ValueError: If ``name`` is empty.
        """
        if not name:
            raise ValueError("Secret name must be a non-empty string")
        frozen_metadata: Mapping[str, str] = MappingProxyType(dict(metadata or {}))
        ciphertext = self._encryption.encrypt(value.encode(_ENCODING))
        created_at = time.time()
        with self._lock:
            self._entries[name] = _VaultEntry(ciphertext, created_at, frozen_metadata)
        self._logger.info("vault.stored", extra={"context": {"name": name}})
        SecretStored(name).publish(self._events)
        return Secret(name=name, value=value, created_at=created_at, metadata=frozen_metadata)

    def read(self, name: str) -> Secret:
        """Return the decrypted secret stored under ``name``.

        Args:
            name: Identifier of the secret to read.

        Returns:
            The decrypted :class:`~app.security.models.Secret`.

        Raises:
            SecretNotFoundError: If no secret exists for ``name``.
        """
        with self._lock:
            entry = self._entries.get(name)
        if entry is None:
            raise SecretNotFoundError(f"Secret not found: {name}")
        value = self._encryption.decrypt(entry.ciphertext).decode(_ENCODING)
        SecretRead(name).publish(self._events)
        return Secret(name=name, value=value, created_at=entry.created_at, metadata=entry.metadata)

    def delete(self, name: str) -> None:
        """Remove the secret stored under ``name``.

        Args:
            name: Identifier of the secret to remove.

        Raises:
            SecretNotFoundError: If no secret exists for ``name``.
        """
        with self._lock:
            if name not in self._entries:
                raise SecretNotFoundError(f"Secret not found: {name}")
            del self._entries[name]
        self._logger.info("vault.deleted", extra={"context": {"name": name}})
        SecretDeleted(name).publish(self._events)

    def contains(self, name: str) -> bool:
        """Return whether a secret exists for ``name`` without decrypting it."""
        with self._lock:
            return name in self._entries

    def names(self) -> tuple[str, ...]:
        """Return the sorted names of all stored secrets, never their values."""
        with self._lock:
            return tuple(sorted(self._entries))
