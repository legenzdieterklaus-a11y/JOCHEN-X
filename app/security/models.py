"""Immutable domain models and vocabularies for the Security Foundation.

All models are frozen dataclasses so security records cannot be mutated after
creation, which is essential for auditability and thread safety. Enumerations
replace magic strings for severities, trust levels, and audit outcomes so
callers depend on a stable, typed vocabulary rather than free-form text.
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field
from enum import StrEnum


class ThreatSeverity(StrEnum):
    """Severity classification for detected security threats."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class PluginTrustLevel(StrEnum):
    """Trust classification assigned to a plugin by the security subsystem."""

    UNTRUSTED = "untrusted"
    VERIFIED = "verified"
    TRUSTED = "trusted"
    REJECTED = "rejected"


class AuditOutcome(StrEnum):
    """Outcome classification for an audited security action."""

    SUCCESS = "success"
    FAILURE = "failure"
    DENIED = "denied"


@dataclass(frozen=True, slots=True)
class Secret:
    """A named sensitive value returned from the vault in decrypted form.

    Attributes:
        name: Stable, unique identifier of the secret within the vault.
        value: The decrypted secret value.
        created_at: Wall-clock creation timestamp in seconds since the epoch.
        metadata: Optional non-sensitive descriptive metadata.
    """

    name: str
    value: str
    created_at: float
    metadata: Mapping[str, str] = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class ApiKey:
    """Public, non-sensitive record describing a managed API key.

    The secret material itself is never stored on this record; it lives in the
    :class:`~app.security.secret_vault.SecretVault` and is surfaced only once at
    creation time.

    Attributes:
        key_id: Stable public identifier of the key.
        name: Human-readable label for the key.
        created_at: Wall-clock creation timestamp in seconds since the epoch.
        active: Whether the key is currently usable.
        scopes: The capability scopes granted to the key.
    """

    key_id: str
    name: str
    created_at: float
    active: bool = True
    scopes: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class Permission:
    """A single, hashable capability that can be granted to a role.

    Attributes:
        name: Stable, dotted capability identifier (for example ``"secret.read"``).
        description: Optional human-readable description of the capability.
    """

    name: str
    description: str = ""


@dataclass(frozen=True, slots=True)
class Identity:
    """A security principal that actions can be attributed to.

    Attributes:
        identifier: Stable, unique identifier of the identity.
        display_name: Human-readable name for presentation and auditing.
        roles: The roles assigned to the identity.
        created_at: Wall-clock creation timestamp in seconds since the epoch.
    """

    identifier: str
    display_name: str
    roles: tuple[str, ...] = ()
    created_at: float = 0.0


@dataclass(frozen=True, slots=True)
class AuditEntry:
    """An immutable, ordered record of a single security-relevant action.

    Attributes:
        sequence: Monotonically increasing sequence number assigned by the logger.
        timestamp: Wall-clock timestamp in seconds since the epoch.
        category: Coarse subsystem category the action belongs to.
        action: The specific action that was performed.
        actor: Identifier of the principal that performed the action.
        outcome: The classified outcome of the action.
        detail: Additional non-sensitive contextual detail.
    """

    sequence: int
    timestamp: float
    category: str
    action: str
    actor: str
    outcome: AuditOutcome
    detail: Mapping[str, str] = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class ThreatReport:
    """An immutable report describing a detected suspicious activity.

    Attributes:
        identifier: Stable, unique identifier of the report.
        timestamp: Wall-clock detection timestamp in seconds since the epoch.
        severity: Classified severity of the threat.
        category: Coarse category describing the class of threat.
        description: Human-readable summary of what was detected.
        related_events: The event names that contributed to the detection.
    """

    identifier: str
    timestamp: float
    severity: ThreatSeverity
    category: str
    description: str
    related_events: tuple[str, ...] = ()
