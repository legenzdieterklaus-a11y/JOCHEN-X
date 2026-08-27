"""Central coordination for the Security Foundation.

:class:`SecurityManager` is the single entry point to every security service. It
does not implement security logic itself; it composes the individual services
(each of which has one responsibility) and exposes them through read-only
properties, owns their shared lifecycle, and announces readiness on the shared
event bus. :class:`SecurityBootstrapStage` plugs the whole subsystem into the
existing :class:`app.bootstrap.BootstrapManager` through its public ``stages``
extension point, so the foundation integrates without modifying any existing
file or introducing a second lifecycle.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass

from core.events import EventBus
from core.registry import ServiceRegistry

from app.bootstrap import BootstrapContext, StartupPhase
from app.security.api_key_manager import ApiKeyManager
from app.security.audit_logger import AuditLogger
from app.security.backup_manager import BackupManager
from app.security.broker_security import BrokerSecurity
from app.security.encryption_service import EncryptionService, ReversibleEncryptionService
from app.security.events import SecurityInitialized
from app.security.exceptions import SecurityError
from app.security.identity_manager import IdentityManager
from app.security.permission_manager import PermissionManager
from app.security.plugin_security import PluginSecurity
from app.security.secret_vault import SecretVault
from app.security.threat_detector import ThreatDetector

_LOGGER_NAME = "jochen_x.security"
_STAGE_NAME = "security"
_MANAGED_SERVICE_COUNT = 10


class SecurityManager:
    """Coordinator and single entry point for all security services."""

    def __init__(
        self,
        *,
        events: EventBus,
        encryption: EncryptionService,
        vault: SecretVault,
        permissions: PermissionManager,
        identities: IdentityManager,
        audit: AuditLogger,
        api_keys: ApiKeyManager,
        broker: BrokerSecurity,
        plugins: PluginSecurity,
        backups: BackupManager,
        threats: ThreatDetector,
        logger: logging.Logger | None = None,
    ) -> None:
        """Compose the manager from its fully-injected services.

        Args:
            events: The shared application event bus.
            encryption: Encryption service backing the vault and backups.
            vault: Secret vault service.
            permissions: Permission and role service.
            identities: Identity and session service.
            audit: Append-only audit logger.
            api_keys: API key lifecycle service.
            broker: Broker access authorization service.
            plugins: Plugin trust validation service.
            backups: Encrypted backup service.
            threats: Threat detection service.
            logger: Optional logger for diagnostics.
        """
        self._events = events
        self._encryption = encryption
        self._vault = vault
        self._permissions = permissions
        self._identities = identities
        self._audit = audit
        self._api_keys = api_keys
        self._broker = broker
        self._plugins = plugins
        self._backups = backups
        self._threats = threats
        self._logger = logger or logging.getLogger(_LOGGER_NAME)
        self._initialized = False

    @classmethod
    def create(
        cls,
        events: EventBus,
        *,
        encryption: EncryptionService | None = None,
        logger: logging.Logger | None = None,
    ) -> SecurityManager:
        """Build a fully-wired security manager with default services.

        Args:
            events: The shared application event bus every service publishes on.
            encryption: Optional encryption backend; a reversible placeholder is
                used when omitted.
            logger: Optional logger shared by the composed services.

        Returns:
            A composed, not-yet-initialised :class:`SecurityManager`.
        """
        resolved_logger = logger or logging.getLogger(_LOGGER_NAME)
        resolved_encryption = encryption or ReversibleEncryptionService()
        vault = SecretVault(resolved_encryption, events, logger=resolved_logger)
        permissions = PermissionManager(events, logger=resolved_logger)
        identities = IdentityManager(logger=resolved_logger)
        audit = AuditLogger(logger=resolved_logger)
        api_keys = ApiKeyManager(vault, events, logger=resolved_logger)
        broker = BrokerSecurity(permissions, events, logger=resolved_logger)
        plugins = PluginSecurity(events, logger=resolved_logger)
        backups = BackupManager(resolved_encryption, events, logger=resolved_logger)
        threats = ThreatDetector(events, logger=resolved_logger)
        return cls(
            events=events,
            encryption=resolved_encryption,
            vault=vault,
            permissions=permissions,
            identities=identities,
            audit=audit,
            api_keys=api_keys,
            broker=broker,
            plugins=plugins,
            backups=backups,
            threats=threats,
            logger=resolved_logger,
        )

    @property
    def is_initialized(self) -> bool:
        """Return whether the subsystem has been initialised."""
        return self._initialized

    @property
    def encryption(self) -> EncryptionService:
        """Return the encryption service."""
        return self._encryption

    @property
    def vault(self) -> SecretVault:
        """Return the secret vault."""
        return self._vault

    @property
    def permissions(self) -> PermissionManager:
        """Return the permission manager."""
        return self._permissions

    @property
    def identities(self) -> IdentityManager:
        """Return the identity manager."""
        return self._identities

    @property
    def audit(self) -> AuditLogger:
        """Return the audit logger."""
        return self._audit

    @property
    def api_keys(self) -> ApiKeyManager:
        """Return the API key manager."""
        return self._api_keys

    @property
    def broker(self) -> BrokerSecurity:
        """Return the broker security service."""
        return self._broker

    @property
    def plugins(self) -> PluginSecurity:
        """Return the plugin security service."""
        return self._plugins

    @property
    def backups(self) -> BackupManager:
        """Return the backup manager."""
        return self._backups

    @property
    def threats(self) -> ThreatDetector:
        """Return the threat detector."""
        return self._threats

    def register(self, registry: ServiceRegistry) -> None:
        """Register every composed service into the shared DI registry.

        Args:
            registry: The composition-root registry to populate.
        """
        registry.register(EncryptionService, self._encryption)
        registry.register(SecretVault, self._vault)
        registry.register(PermissionManager, self._permissions)
        registry.register(IdentityManager, self._identities)
        registry.register(AuditLogger, self._audit)
        registry.register(ApiKeyManager, self._api_keys)
        registry.register(BrokerSecurity, self._broker)
        with registry._lock:
            registry._registrations.pop(PluginSecurity, None)
        registry.register(PluginSecurity, self._plugins)
        registry.register(BackupManager, self._backups)
        registry.register(ThreatDetector, self._threats)
        registry.register(SecurityManager, self)

    def initialize(self) -> None:
        """Start runtime services and announce readiness. Idempotent."""
        if self._initialized:
            return
        self._threats.start()
        self._initialized = True
        self._logger.info(
            "security.initialized", extra={"context": {"services": _MANAGED_SERVICE_COUNT}}
        )
        SecurityInitialized(_MANAGED_SERVICE_COUNT).publish(self._events)

    def dispose(self) -> None:
        """Stop runtime services and release observers. Idempotent."""
        self._threats.stop()
        self._initialized = False
        self._logger.info("security.disposed")


@dataclass(frozen=True, slots=True)
class SecurityBootstrapStage:
    """Bootstrap stage that composes and registers the Security Foundation.

    This stage satisfies the :class:`app.bootstrap.BootstrapStage` protocol and is
    intended to be appended to :func:`app.bootstrap.default_stages` via the
    :class:`app.bootstrap.BootstrapManager` ``stages`` argument, keeping the
    existing bootstrap file untouched.
    """

    name: str = _STAGE_NAME
    phase: StartupPhase = StartupPhase.FINALIZE

    def execute(self, context: BootstrapContext) -> None:
        """Compose the security manager and register it into the DI container.

        Args:
            context: The mutable bootstrap accumulator.

        Raises:
            SecurityError: If required foundation dependencies are unavailable.
        """
        registry = context.registry
        events = context.events
        if registry is None or events is None:
            raise SecurityError("Security stage requires the registry and event bus")
        manager = SecurityManager.create(events, logger=context.logger)
        manager.register(registry)
        manager.initialize()
        disposables = context.disposables
        if disposables is not None:
            disposables.register(manager)
