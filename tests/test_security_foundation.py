"""Isolated tests for the JOCHEN X Security Foundation.

Every security service is verified independently and without a Qt event loop.
The integration tests compose the subsystem onto the real bootstrap pipeline and
application host through the public ``stages`` extension point, proving the
foundation plugs into the existing architecture without modifying it.
"""

from __future__ import annotations

import gc
import logging
import tempfile
import unittest
from pathlib import Path

from core.events import EventBus
from core.registry import ServiceRegistry

from app.application_host import ApplicationHost
from app.bootstrap import BootstrapManager, StartupPhase, default_stages
from app.di import DisposableRegistry
from app.security import (
    ApiKeyManager,
    AuditLogger,
    AuditOutcome,
    BackupManager,
    BrokerSecurity,
    BrokerSecurityError,
    EncryptionError,
    IdentityManager,
    Permission,
    PermissionDeniedError,
    PermissionManager,
    PluginSecurity,
    PluginSecurityError,
    PluginTrustLevel,
    ReversibleEncryptionService,
    SecretNotFoundError,
    SecretVault,
    SecurityBootstrapStage,
    SecurityEventName,
    SecurityManager,
    ThreatDetector,
)

_READ_PERMISSION = Permission("secret.read", "Read secrets")
_TRADE_PERMISSION = Permission("broker.trade", "Trade on a broker")

_DEFAULT_CONFIG = """[application]
name = "JOCHEN X"
version = "0.1.0"
log_level = "INFO"
theme_mode = "dark"
developer_enabled = false

[database]
path = "data/test.sqlite3"

[plugins]
directory = "plugins"
"""


def _reset_application_logging() -> None:
    """Release log handlers and short-lived DB connections before cleanup."""
    logger = logging.getLogger("jochen_x")
    for handler in list(logger.handlers):
        handler.close()
        logger.removeHandler(handler)
    gc.collect()


def _make_project_root(directory: str) -> Path:
    """Create a minimal, self-contained project root inside ``directory``."""
    root = Path(directory)
    config_directory = root / "config"
    config_directory.mkdir(parents=True, exist_ok=True)
    (config_directory / "default.toml").write_text(_DEFAULT_CONFIG, encoding="utf-8")
    return root


def _capture(bus: EventBus, name: SecurityEventName) -> list[dict[str, object]]:
    """Subscribe to ``name`` on ``bus`` and return a growing list of payloads."""
    captured: list[dict[str, object]] = []
    bus.subscribe(str(name), lambda event: captured.append(event.payload))
    return captured


class EncryptionServiceTests(unittest.TestCase):
    def test_round_trip_is_reversible(self) -> None:
        service = ReversibleEncryptionService()
        ciphertext = service.encrypt(b"payload")
        self.assertNotEqual(ciphertext, b"payload")
        self.assertEqual(service.decrypt(ciphertext), b"payload")

    def test_generate_key_is_unpredictable(self) -> None:
        service = ReversibleEncryptionService()
        self.assertNotEqual(service.generate_key(), service.generate_key())

    def test_invalid_ciphertext_raises(self) -> None:
        service = ReversibleEncryptionService()
        with self.assertRaises(EncryptionError):
            service.decrypt(b"not-base64-!!!")


class SecretVaultTests(unittest.TestCase):
    def _vault(self) -> tuple[SecretVault, EventBus]:
        bus = EventBus()
        return SecretVault(ReversibleEncryptionService(), bus), bus

    def test_store_read_delete_round_trip(self) -> None:
        vault, bus = self._vault()
        stored = _capture(bus, SecurityEventName.SECRET_STORED)
        read = _capture(bus, SecurityEventName.SECRET_READ)
        deleted = _capture(bus, SecurityEventName.SECRET_DELETED)

        secret = vault.store("api.token", "s3cret", metadata={"owner": "core"})
        self.assertEqual(secret.value, "s3cret")
        self.assertEqual(vault.read("api.token").value, "s3cret")
        self.assertEqual(vault.names(), ("api.token",))
        vault.delete("api.token")

        self.assertFalse(vault.contains("api.token"))
        self.assertEqual(stored, [{"name": "api.token"}])
        self.assertEqual(read, [{"name": "api.token"}])
        self.assertEqual(deleted, [{"name": "api.token"}])

    def test_missing_secret_raises(self) -> None:
        vault, _ = self._vault()
        with self.assertRaises(SecretNotFoundError):
            vault.read("absent")
        with self.assertRaises(SecretNotFoundError):
            vault.delete("absent")

    def test_empty_name_rejected(self) -> None:
        vault, _ = self._vault()
        with self.assertRaises(ValueError):
            vault.store("", "value")

    def test_names_never_leak_values(self) -> None:
        vault, _ = self._vault()
        vault.store("b", "second")
        vault.store("a", "first")
        self.assertEqual(vault.names(), ("a", "b"))


class PermissionManagerTests(unittest.TestCase):
    def test_role_grants_permission_and_emits_event(self) -> None:
        bus = EventBus()
        granted = _capture(bus, SecurityEventName.PERMISSION_GRANTED)
        manager = PermissionManager(bus)
        manager.define_role("reader", [_READ_PERMISSION])
        manager.assign_role("user-1", "reader")

        self.assertTrue(manager.has_permission("user-1", _READ_PERMISSION))
        self.assertEqual(granted, [{"identity": "user-1", "permission": "secret.read"}])
        self.assertEqual(manager.roles_of("user-1"), frozenset({"reader"}))

    def test_denied_permission_emits_and_raises(self) -> None:
        bus = EventBus()
        denied = _capture(bus, SecurityEventName.PERMISSION_DENIED)
        manager = PermissionManager(bus)

        self.assertFalse(manager.has_permission("user-1", _READ_PERMISSION))
        with self.assertRaises(PermissionDeniedError):
            manager.require("user-1", _READ_PERMISSION)
        self.assertEqual(len(denied), 2)

    def test_revoke_role_removes_permission(self) -> None:
        manager = PermissionManager(EventBus())
        manager.define_role("reader", [_READ_PERMISSION])
        manager.assign_role("user-1", "reader")
        manager.revoke_role("user-1", "reader")
        self.assertNotIn(_READ_PERMISSION, manager.permissions_of("user-1"))

    def test_assign_undefined_role_raises(self) -> None:
        manager = PermissionManager(EventBus())
        with self.assertRaises(KeyError):
            manager.assign_role("user-1", "ghost")


class IdentityManagerTests(unittest.TestCase):
    def test_create_and_session_lifecycle(self) -> None:
        manager = IdentityManager()
        identity = manager.create_identity("Operator", roles=("reader",))
        self.assertEqual(manager.get(identity.identifier).display_name, "Operator")

        session = manager.start_session(identity.identifier)
        self.assertEqual(len(manager.active_sessions()), 1)
        manager.end_session(session.session_id)
        self.assertEqual(manager.active_sessions(), ())

    def test_unknown_identity_and_session_raise(self) -> None:
        manager = IdentityManager()
        with self.assertRaises(Exception):
            manager.get("missing")
        with self.assertRaises(Exception):
            manager.start_session("missing")


class AuditLoggerTests(unittest.TestCase):
    def test_entries_are_ordered_and_immutable(self) -> None:
        logger = AuditLogger()
        first = logger.record("vault", "store", "user-1")
        second = logger.record("vault", "read", "user-1", outcome=AuditOutcome.SUCCESS)

        self.assertEqual(first.sequence, 1)
        self.assertEqual(second.sequence, 2)
        entries = logger.entries()
        self.assertEqual(logger.count(), 2)
        self.assertEqual(tuple(entry.action for entry in entries), ("store", "read"))

    def test_returned_tuple_is_defensive_copy(self) -> None:
        logger = AuditLogger()
        logger.record("vault", "store", "user-1")
        snapshot = logger.entries()
        logger.record("vault", "read", "user-1")
        self.assertEqual(len(snapshot), 1)


class ApiKeyManagerTests(unittest.TestCase):
    def _manager(self) -> tuple[ApiKeyManager, EventBus]:
        bus = EventBus()
        vault = SecretVault(ReversibleEncryptionService(), bus)
        return ApiKeyManager(vault, bus), bus

    def test_create_reveal_list_revoke(self) -> None:
        manager, bus = self._manager()
        created = _capture(bus, SecurityEventName.API_KEY_CREATED)
        revoked = _capture(bus, SecurityEventName.API_KEY_REVOKED)

        record, secret = manager.create("primary", scopes=("read",))
        self.assertTrue(record.active)
        self.assertEqual(manager.reveal_secret(record.key_id), secret)
        self.assertEqual(len(manager.list()), 1)

        deactivated = manager.revoke(record.key_id)
        self.assertFalse(deactivated.active)
        self.assertEqual(created, [{"key_id": record.key_id, "name": "primary"}])
        self.assertEqual(revoked, [{"key_id": record.key_id}])

    def test_reveal_revoked_secret_raises(self) -> None:
        manager, _ = self._manager()
        record, _secret = manager.create("primary")
        manager.revoke(record.key_id)
        with self.assertRaises(Exception):
            manager.reveal_secret(record.key_id)

    def test_unknown_key_raises(self) -> None:
        manager, _ = self._manager()
        with self.assertRaises(Exception):
            manager.get("missing")


class BrokerSecurityTests(unittest.TestCase):
    def test_authenticate_requires_permission(self) -> None:
        bus = EventBus()
        authenticated = _capture(bus, SecurityEventName.BROKER_AUTHENTICATED)
        permissions = PermissionManager(bus)
        permissions.define_role("trader", [_TRADE_PERMISSION])
        permissions.assign_role("user-1", "trader")
        broker = BrokerSecurity(permissions, bus)
        broker.register_broker("demo", required_permission=_TRADE_PERMISSION)

        self.assertTrue(broker.authenticate("demo", "user-1"))
        self.assertEqual(authenticated, [{"broker": "demo", "identity": "user-1"}])

    def test_unauthorized_and_unknown_broker_raise(self) -> None:
        bus = EventBus()
        permissions = PermissionManager(bus)
        broker = BrokerSecurity(permissions, bus)
        broker.register_broker("demo", required_permission=_TRADE_PERMISSION)
        with self.assertRaises(BrokerSecurityError):
            broker.authenticate("demo", "user-1")
        with self.assertRaises(BrokerSecurityError):
            broker.authenticate("ghost", "user-1")


class PluginSecurityTests(unittest.TestCase):
    def test_verify_allows_only_after_approval(self) -> None:
        bus = EventBus()
        verified = _capture(bus, SecurityEventName.PLUGIN_VERIFIED)
        plugins = PluginSecurity(bus)

        untrusted = plugins.verify("acme.plugin", "1.0.0")
        self.assertFalse(untrusted.allowed)
        self.assertIs(untrusted.trust, PluginTrustLevel.UNTRUSTED)

        plugins.approve("acme.plugin")
        trusted = plugins.verify("acme.plugin", "1.0.0")
        self.assertTrue(trusted.allowed)
        self.assertEqual(verified, [{"identifier": "acme.plugin", "version": "1.0.0", "trust": "trusted"}])

    def test_rejected_plugin_raises(self) -> None:
        bus = EventBus()
        rejected = _capture(bus, SecurityEventName.PLUGIN_REJECTED)
        plugins = PluginSecurity(bus)
        plugins.reject("bad.plugin", "unsigned")
        with self.assertRaises(PluginSecurityError):
            plugins.verify("bad.plugin", "1.0.0")
        self.assertEqual(rejected, [{"identifier": "bad.plugin", "reason": "unsigned"}])


class BackupManagerTests(unittest.TestCase):
    def test_backup_round_trip(self) -> None:
        bus = EventBus()
        created = _capture(bus, SecurityEventName.BACKUP_CREATED)
        restored = _capture(bus, SecurityEventName.BACKUP_RESTORED)
        manager = BackupManager(ReversibleEncryptionService(), bus)

        record = manager.create_backup("daily", {"a": "1", "b": "2"})
        self.assertEqual(manager.restore_backup(record.identifier), {"a": "1", "b": "2"})
        self.assertEqual(len(manager.list_backups()), 1)
        self.assertEqual(created, [{"identifier": record.identifier}])
        self.assertEqual(restored, [{"identifier": record.identifier}])

    def test_unknown_backup_raises(self) -> None:
        manager = BackupManager(ReversibleEncryptionService(), EventBus())
        with self.assertRaises(Exception):
            manager.restore_backup("missing")


class ThreatDetectorTests(unittest.TestCase):
    def test_detects_permission_denial_burst(self) -> None:
        bus = EventBus()
        threats = _capture(bus, SecurityEventName.THREAT_DETECTED)
        detector = ThreatDetector(bus, threshold=3, window_seconds=60.0)
        permissions = PermissionManager(bus)
        detector.start()
        try:
            for _ in range(3):
                permissions.has_permission("attacker", _READ_PERMISSION)
        finally:
            detector.stop()

        self.assertEqual(len(detector.reports()), 1)
        self.assertEqual(len(threats), 1)
        self.assertEqual(threats[0]["severity"], "high")

    def test_stop_is_idempotent_and_unsubscribes(self) -> None:
        bus = EventBus()
        detector = ThreatDetector(bus, threshold=2, window_seconds=60.0)
        detector.start()
        detector.stop()
        detector.stop()
        permissions = PermissionManager(bus)
        permissions.has_permission("attacker", _READ_PERMISSION)
        permissions.has_permission("attacker", _READ_PERMISSION)
        self.assertEqual(detector.reports(), ())

    def test_invalid_configuration_rejected(self) -> None:
        with self.assertRaises(ValueError):
            ThreatDetector(EventBus(), threshold=0)
        with self.assertRaises(ValueError):
            ThreatDetector(EventBus(), window_seconds=0.0)


class SecurityManagerTests(unittest.TestCase):
    def test_initialize_emits_event_and_wires_services(self) -> None:
        bus = EventBus()
        initialized = _capture(bus, SecurityEventName.INITIALIZED)
        manager = SecurityManager.create(bus)

        self.assertFalse(manager.is_initialized)
        manager.initialize()
        manager.initialize()

        self.assertTrue(manager.is_initialized)
        self.assertEqual(len(initialized), 1)
        self.assertIsInstance(manager.vault, SecretVault)
        self.assertIsInstance(manager.permissions, PermissionManager)
        manager.dispose()
        self.assertFalse(manager.is_initialized)

    def test_shared_bus_flows_end_to_end(self) -> None:
        bus = EventBus()
        stored = _capture(bus, SecurityEventName.SECRET_STORED)
        manager = SecurityManager.create(bus)
        manager.initialize()
        try:
            manager.vault.store("token", "value")
            self.assertEqual(stored, [{"name": "token"}])
        finally:
            manager.dispose()


class DependencyInjectionTests(unittest.TestCase):
    def test_manager_registers_all_services(self) -> None:
        bus = EventBus()
        registry = ServiceRegistry()
        registry.register(EventBus, bus)
        manager = SecurityManager.create(bus)
        manager.register(registry)

        self.assertIs(registry.get(SecurityManager), manager)
        self.assertIs(registry.get(SecretVault), manager.vault)
        self.assertIs(registry.get(ApiKeyManager), manager.api_keys)
        self.assertIs(registry.get(ThreatDetector), manager.threats)


class ApplicationFoundationIntegrationTests(unittest.TestCase):
    def _bootstrap_manager(self) -> BootstrapManager:
        return BootstrapManager(stages=(*default_stages(), SecurityBootstrapStage()))

    def test_bootstrap_stage_registers_and_initializes(self) -> None:
        with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as directory:
            root = _make_project_root(directory)
            try:
                manager = self._bootstrap_manager()
                context = manager.begin(root)
                for phase in StartupPhase:
                    manager.run_phase(context, phase)
                self.assertIsNotNone(context.registry)
                security = context.registry.get(SecurityManager)  # type: ignore[union-attr]
                self.assertTrue(security.is_initialized)
            finally:
                _reset_application_logging()

    def test_host_start_exposes_security_manager(self) -> None:
        with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as directory:
            root = _make_project_root(directory)
            try:
                host = ApplicationHost(root, bootstrap_manager=self._bootstrap_manager())
                context = host.start()
                security = context.services.get(SecurityManager)
                self.assertTrue(security.is_initialized)

                captured = _capture(context.events, SecurityEventName.SECRET_STORED)
                security.vault.store("token", "value")
                self.assertEqual(captured, [{"name": "token"}])

                host.shutdown()
                self.assertFalse(security.is_initialized)
            finally:
                _reset_application_logging()

    def test_disposable_registry_stops_threat_detector(self) -> None:
        bus = EventBus()
        disposables = DisposableRegistry()
        manager = SecurityManager.create(bus)
        manager.initialize()
        disposables.register(manager)
        disposables.dispose_all()
        self.assertFalse(manager.is_initialized)


if __name__ == "__main__":
    unittest.main()

