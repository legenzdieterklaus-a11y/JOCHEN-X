"""JOCHEN X Security Foundation.

This core module is the long-term security base for every sensitive subsystem
(trading, AI, plugins, marketplace, developer center, settings, brokers,
database, and cloud services). It extends the existing application foundation:
it reuses the shared event bus, dependency-injection registry, disposable
lifecycle, and bootstrap pipeline rather than introducing any parallel
infrastructure.

The public surface is intentionally small: consumers obtain a
:class:`~app.security.security_manager.SecurityManager` (typically resolved from
the DI registry) and reach every service through it.
"""

from __future__ import annotations

from app.security.api_key_manager import ApiKeyManager
from app.security.audit_logger import AuditLogger
from app.security.backup_manager import BackupManager, BackupRecord
from app.security.broker_security import BrokerAccessPolicy, BrokerSecurity
from app.security.encryption_service import EncryptionService, ReversibleEncryptionService
from app.security.events import (
    ApiKeyCreated,
    ApiKeyRevoked,
    BackupCreated,
    BackupRestored,
    BrokerAuthenticated,
    PermissionDenied,
    PermissionGranted,
    PluginRejected,
    PluginVerified,
    SecretDeleted,
    SecretRead,
    SecretStored,
    SecurityEvent,
    SecurityEventName,
    SecurityInitialized,
    ThreatDetected,
)
from app.security.exceptions import (
    BrokerSecurityError,
    EncryptionError,
    PermissionDeniedError,
    PluginSecurityError,
    SecretNotFoundError,
    SecurityError,
)
from app.security.identity_manager import IdentityManager, Session
from app.security.models import (
    ApiKey,
    AuditEntry,
    AuditOutcome,
    Identity,
    Permission,
    PluginTrustLevel,
    Secret,
    ThreatReport,
    ThreatSeverity,
)
from app.security.permission_manager import PermissionManager
from app.security.plugin_security import PluginSecurity, PluginVerdict
from app.security.secret_vault import SecretVault
from app.security.security_manager import SecurityBootstrapStage, SecurityManager
from app.security.threat_detector import ThreatDetector

__all__ = [
    "ApiKey",
    "ApiKeyCreated",
    "ApiKeyManager",
    "ApiKeyRevoked",
    "AuditEntry",
    "AuditLogger",
    "AuditOutcome",
    "BackupCreated",
    "BackupManager",
    "BackupRecord",
    "BackupRestored",
    "BrokerAccessPolicy",
    "BrokerAuthenticated",
    "BrokerSecurity",
    "BrokerSecurityError",
    "EncryptionError",
    "EncryptionService",
    "Identity",
    "IdentityManager",
    "Permission",
    "PermissionDenied",
    "PermissionDeniedError",
    "PermissionGranted",
    "PermissionManager",
    "PluginRejected",
    "PluginSecurity",
    "PluginSecurityError",
    "PluginTrustLevel",
    "PluginVerdict",
    "PluginVerified",
    "ReversibleEncryptionService",
    "Secret",
    "SecretDeleted",
    "SecretNotFoundError",
    "SecretRead",
    "SecretStored",
    "SecretVault",
    "SecurityBootstrapStage",
    "SecurityError",
    "SecurityEvent",
    "SecurityEventName",
    "SecurityInitialized",
    "SecurityManager",
    "Session",
    "ThreatDetected",
    "ThreatDetector",
    "ThreatReport",
    "ThreatSeverity",
]
