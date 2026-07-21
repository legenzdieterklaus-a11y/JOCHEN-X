"""API key lifecycle management for the Security Foundation.

:class:`ApiKeyManager` issues, lists, and revokes API keys. It composes the
:class:`~app.security.secret_vault.SecretVault` for at-rest protection of the
secret material rather than reimplementing storage, keeping a single owner of
sensitive values. The secret is surfaced exactly once at creation time; all
later reads return only the public :class:`~app.security.models.ApiKey` record.
"""

from __future__ import annotations

import dataclasses
import logging
import secrets
import time
from collections.abc import Iterable
from threading import RLock
from uuid import uuid4

from app.events import EventPublisher
from app.security.events import ApiKeyCreated, ApiKeyRevoked
from app.security.exceptions import SecretNotFoundError, SecurityError
from app.security.models import ApiKey
from app.security.secret_vault import SecretVault

_LOGGER_NAME = "jochen_x.security.apikeys"
_SECRET_PREFIX = "apikey"
_SECRET_TOKEN_BYTES = 32


class ApiKeyManager:
    """Thread-safe manager for issuing, listing, and revoking API keys."""

    def __init__(
        self,
        vault: SecretVault,
        events: EventPublisher,
        *,
        logger: logging.Logger | None = None,
    ) -> None:
        """Create an empty API key manager.

        Args:
            vault: Vault used to store the sensitive key material.
            events: Publisher port used to broadcast key lifecycle events.
            logger: Optional logger for diagnostics.
        """
        self._vault = vault
        self._events = events
        self._logger = logger or logging.getLogger(_LOGGER_NAME)
        self._keys: dict[str, ApiKey] = {}
        self._lock = RLock()

    def create(self, name: str, *, scopes: Iterable[str] = ()) -> tuple[ApiKey, str]:
        """Issue a new API key and return its record together with its secret.

        Args:
            name: Human-readable label for the key.
            scopes: Capability scopes granted to the key.

        Returns:
            A tuple of the public :class:`~app.security.models.ApiKey` record and
            the generated secret. The secret is returned only here and never again.

        Raises:
            ValueError: If ``name`` is empty.
        """
        if not name:
            raise ValueError("API key name must be a non-empty string")
        key_id = uuid4().hex
        raw_secret = secrets.token_urlsafe(_SECRET_TOKEN_BYTES)
        record = ApiKey(
            key_id=key_id,
            name=name,
            created_at=time.time(),
            active=True,
            scopes=tuple(scopes),
        )
        self._vault.store(self._secret_name(key_id), raw_secret, metadata={"kind": _SECRET_PREFIX})
        with self._lock:
            self._keys[key_id] = record
        self._logger.info("apikey.created", extra={"context": {"key_id": key_id}})
        ApiKeyCreated(key_id, name).publish(self._events)
        return record, raw_secret

    def revoke(self, key_id: str) -> ApiKey:
        """Deactivate the key ``key_id`` and remove its secret material.

        Args:
            key_id: Identifier of the key to revoke.

        Returns:
            The updated, deactivated :class:`~app.security.models.ApiKey` record.

        Raises:
            SecurityError: If the key does not exist.
        """
        with self._lock:
            record = self._keys.get(key_id)
            if record is None:
                raise SecurityError(f"Unknown API key: {key_id}")
            revoked = dataclasses.replace(record, active=False)
            self._keys[key_id] = revoked
        try:
            self._vault.delete(self._secret_name(key_id))
        except SecretNotFoundError:
            self._logger.warning("apikey.secret_missing", extra={"context": {"key_id": key_id}})
        self._logger.info("apikey.revoked", extra={"context": {"key_id": key_id}})
        ApiKeyRevoked(key_id).publish(self._events)
        return revoked

    def get(self, key_id: str) -> ApiKey:
        """Return the public record for ``key_id``.

        Raises:
            SecurityError: If the key does not exist.
        """
        with self._lock:
            record = self._keys.get(key_id)
        if record is None:
            raise SecurityError(f"Unknown API key: {key_id}")
        return record

    def reveal_secret(self, key_id: str) -> str:
        """Return the stored secret for an active key.

        Args:
            key_id: Identifier of the key whose secret should be returned.

        Returns:
            The decrypted secret value.

        Raises:
            SecurityError: If the key does not exist or has been revoked.
        """
        record = self.get(key_id)
        if not record.active:
            raise SecurityError(f"API key is revoked: {key_id}")
        return self._vault.read(self._secret_name(key_id)).value

    def list(self) -> tuple[ApiKey, ...]:
        """Return all key records, ordered by creation time."""
        with self._lock:
            return tuple(sorted(self._keys.values(), key=lambda record: record.created_at))

    @staticmethod
    def _secret_name(key_id: str) -> str:
        """Return the vault name that stores the secret for ``key_id``."""
        return f"{_SECRET_PREFIX}:{key_id}"
