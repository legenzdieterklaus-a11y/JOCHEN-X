"""Strongly typed security event vocabulary.

This module defines the immutable security event vocabulary for JOCHEN X. Each
event carries a stable :class:`SecurityEventName` and converts to a
transport-neutral :class:`core.events.Event`, so it flows over the existing
in-process :class:`core.events.EventBus` without any second event system. The
narrow :class:`app.events.EventPublisher` port is deliberately reused rather than
redefined to guarantee a single publishing contract across the application.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from typing import Any, ClassVar

from core.events import Event

from app.events import EventPublisher

__all__ = [
    "SecurityEventName",
    "SecurityEvent",
    "SecurityInitialized",
    "SecretStored",
    "SecretRead",
    "SecretDeleted",
    "PermissionGranted",
    "PermissionDenied",
    "ApiKeyCreated",
    "ApiKeyRevoked",
    "PluginVerified",
    "PluginRejected",
    "ThreatDetected",
    "BackupCreated",
    "BackupRestored",
    "BrokerAuthenticated",
]


class SecurityEventName(StrEnum):
    """Canonical, stable names for every security event."""

    INITIALIZED = "security.initialized"
    SECRET_STORED = "security.secret.stored"
    SECRET_READ = "security.secret.read"
    SECRET_DELETED = "security.secret.deleted"
    PERMISSION_GRANTED = "security.permission.granted"
    PERMISSION_DENIED = "security.permission.denied"
    API_KEY_CREATED = "security.apikey.created"
    API_KEY_REVOKED = "security.apikey.revoked"
    PLUGIN_VERIFIED = "security.plugin.verified"
    PLUGIN_REJECTED = "security.plugin.rejected"
    THREAT_DETECTED = "security.threat.detected"
    BACKUP_CREATED = "security.backup.created"
    BACKUP_RESTORED = "security.backup.restored"
    BROKER_AUTHENTICATED = "security.broker.authenticated"


class SecurityEvent:
    """Base class for immutable, typed security events.

    Subclasses are frozen dataclasses that declare their :attr:`EVENT_NAME` and
    optionally override :meth:`_payload` to expose typed data as a plain mapping
    for the transport-neutral :class:`core.events.Event`. Payloads never carry
    secret material; they carry only identifiers and classifications.
    """

    __slots__ = ()

    EVENT_NAME: ClassVar[SecurityEventName]

    def _payload(self) -> dict[str, Any]:
        """Return the event payload as a JSON-serialisable mapping."""
        return {}

    def to_event(self) -> Event:
        """Convert this typed event into a transport-neutral bus event."""
        return Event(str(self.EVENT_NAME), self._payload())

    def publish(self, publisher: EventPublisher, *, sticky: bool = False) -> None:
        """Publish this event through the supplied publisher port."""
        publisher.publish(self.to_event(), sticky=sticky)


@dataclass(frozen=True, slots=True)
class SecurityInitialized(SecurityEvent):
    """Emitted once the Security Foundation has fully composed its services."""

    EVENT_NAME: ClassVar[SecurityEventName] = SecurityEventName.INITIALIZED
    service_count: int

    def _payload(self) -> dict[str, Any]:
        return {"service_count": self.service_count}


@dataclass(frozen=True, slots=True)
class SecretStored(SecurityEvent):
    """Emitted when a secret is created or replaced in the vault."""

    EVENT_NAME: ClassVar[SecurityEventName] = SecurityEventName.SECRET_STORED
    name: str

    def _payload(self) -> dict[str, Any]:
        return {"name": self.name}


@dataclass(frozen=True, slots=True)
class SecretRead(SecurityEvent):
    """Emitted when a secret is read from the vault."""

    EVENT_NAME: ClassVar[SecurityEventName] = SecurityEventName.SECRET_READ
    name: str

    def _payload(self) -> dict[str, Any]:
        return {"name": self.name}


@dataclass(frozen=True, slots=True)
class SecretDeleted(SecurityEvent):
    """Emitted when a secret is removed from the vault."""

    EVENT_NAME: ClassVar[SecurityEventName] = SecurityEventName.SECRET_DELETED
    name: str

    def _payload(self) -> dict[str, Any]:
        return {"name": self.name}


@dataclass(frozen=True, slots=True)
class PermissionGranted(SecurityEvent):
    """Emitted when an identity is confirmed to hold a checked permission."""

    EVENT_NAME: ClassVar[SecurityEventName] = SecurityEventName.PERMISSION_GRANTED
    identity: str
    permission: str

    def _payload(self) -> dict[str, Any]:
        return {"identity": self.identity, "permission": self.permission}


@dataclass(frozen=True, slots=True)
class PermissionDenied(SecurityEvent):
    """Emitted when an identity is refused a checked permission."""

    EVENT_NAME: ClassVar[SecurityEventName] = SecurityEventName.PERMISSION_DENIED
    identity: str
    permission: str

    def _payload(self) -> dict[str, Any]:
        return {"identity": self.identity, "permission": self.permission}


@dataclass(frozen=True, slots=True)
class ApiKeyCreated(SecurityEvent):
    """Emitted when a new API key is created."""

    EVENT_NAME: ClassVar[SecurityEventName] = SecurityEventName.API_KEY_CREATED
    key_id: str
    name: str

    def _payload(self) -> dict[str, Any]:
        return {"key_id": self.key_id, "name": self.name}


@dataclass(frozen=True, slots=True)
class ApiKeyRevoked(SecurityEvent):
    """Emitted when an API key is revoked."""

    EVENT_NAME: ClassVar[SecurityEventName] = SecurityEventName.API_KEY_REVOKED
    key_id: str

    def _payload(self) -> dict[str, Any]:
        return {"key_id": self.key_id}


@dataclass(frozen=True, slots=True)
class PluginVerified(SecurityEvent):
    """Emitted when a plugin passes security validation."""

    EVENT_NAME: ClassVar[SecurityEventName] = SecurityEventName.PLUGIN_VERIFIED
    identifier: str
    version: str
    trust: str

    def _payload(self) -> dict[str, Any]:
        return {"identifier": self.identifier, "version": self.version, "trust": self.trust}


@dataclass(frozen=True, slots=True)
class PluginRejected(SecurityEvent):
    """Emitted when a plugin is rejected by the security subsystem."""

    EVENT_NAME: ClassVar[SecurityEventName] = SecurityEventName.PLUGIN_REJECTED
    identifier: str
    reason: str

    def _payload(self) -> dict[str, Any]:
        return {"identifier": self.identifier, "reason": self.reason}


@dataclass(frozen=True, slots=True)
class ThreatDetected(SecurityEvent):
    """Emitted when the threat detector identifies suspicious activity."""

    EVENT_NAME: ClassVar[SecurityEventName] = SecurityEventName.THREAT_DETECTED
    identifier: str
    severity: str
    category: str

    def _payload(self) -> dict[str, Any]:
        return {"identifier": self.identifier, "severity": self.severity, "category": self.category}


@dataclass(frozen=True, slots=True)
class BackupCreated(SecurityEvent):
    """Emitted when an encrypted backup is created."""

    EVENT_NAME: ClassVar[SecurityEventName] = SecurityEventName.BACKUP_CREATED
    identifier: str

    def _payload(self) -> dict[str, Any]:
        return {"identifier": self.identifier}


@dataclass(frozen=True, slots=True)
class BackupRestored(SecurityEvent):
    """Emitted when an encrypted backup is restored."""

    EVENT_NAME: ClassVar[SecurityEventName] = SecurityEventName.BACKUP_RESTORED
    identifier: str

    def _payload(self) -> dict[str, Any]:
        return {"identifier": self.identifier}


@dataclass(frozen=True, slots=True)
class BrokerAuthenticated(SecurityEvent):
    """Emitted when a broker access is authenticated (preparation layer)."""

    EVENT_NAME: ClassVar[SecurityEventName] = SecurityEventName.BROKER_AUTHENTICATED
    broker: str
    identity: str

    def _payload(self) -> dict[str, Any]:
        return {"broker": self.broker, "identity": self.identity}
