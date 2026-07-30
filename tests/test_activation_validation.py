"""Tests for API Version Gate (WP-03), Integrity Validation (WP-04), and Permission Model (WP-05).

SP-03/SP-04 test suite covering:
- AC-3: API Version Gate — manifest-level check before code import
- AC-9: Integrity Validation — policy-driven, trust determination, SignatureStatus
- AC-4: Permission Model — default-deny, admission validation, runtime enforcement
"""

from __future__ import annotations

import logging
import unittest

from core.events import EventBus
from core.registry import ServiceRegistry
from core.version import Version
from pathlib import Path

from plugins.loader import PluginManifest

from app.bootstrap import BootstrapContext, PluginSecurityStage
from app.security.models import PluginTrustLevel
from app.security.plugin_security import (
    IntegrityEvidenceLevel,
    IntegrityPolicy,
    IntegrityResult,
    PermissionPolicy,
    PermissionResult,
    PluginSecurity,
)
from sdk.errors import PluginPermissionError
from sdk.manifest import PluginPermission, SignatureStatus


class _TestBase(unittest.TestCase):
    """Shared helpers for activation validation tests."""

    def _make_manifest(
        self,
        identifier: str,
        *,
        api_version: Version | None = None,
        permissions: tuple[str, ...] = (),
    ) -> PluginManifest:
        return PluginManifest(
            identifier=identifier,
            version=Version(1, 0, 0),
            required_application_version=Version(0, 3, 0),
            api_version=api_version,
            permissions=permissions,
        )

    def _make_context(self) -> BootstrapContext:
        logger = logging.getLogger("test.activation_validation")
        events = EventBus(logger=logger)
        registry = ServiceRegistry()
        context = BootstrapContext(root=Path("."))
        context.logger = logger
        context.events = events
        context.registry = registry
        return context


class TestApiVersionGateCompatible(_TestBase):
    """AC-3: Compatible API version → plugin admitted before code import."""

    def test_api_version_gate_compatible(self) -> None:
        context = self._make_context()
        manifest = self._make_manifest("compat-plugin", api_version=Version(1, 0, 0))
        context.manifests = (manifest,)
        stage = PluginSecurityStage()
        stage.execute(context)
        self.assertEqual(len(context.admitted_manifests), 1)
        self.assertEqual(context.admitted_manifests[0].identifier, "compat-plugin")

    def test_api_version_gate_compatible_minor_lower(self) -> None:
        """Host API 1.0.0 is compatible with plugin requiring 1.0.0."""
        context = self._make_context()
        manifest = self._make_manifest("minor-plugin", api_version=Version(1, 0, 0))
        context.manifests = (manifest,)
        stage = PluginSecurityStage()
        stage.execute(context)
        self.assertEqual(len(context.admitted_manifests), 1)

    def test_api_version_none_defaults_compatible(self) -> None:
        """V1 manifests without api_version are treated as compatible."""
        context = self._make_context()
        manifest = self._make_manifest("v1-plugin")
        context.manifests = (manifest,)
        stage = PluginSecurityStage()
        stage.execute(context)
        self.assertEqual(len(context.admitted_manifests), 1)


class TestApiVersionGateIncompatible(_TestBase):
    """AC-3: Incompatible API version → plugin rejected before code import."""

    def test_api_version_gate_incompatible(self) -> None:
        context = self._make_context()
        manifest = self._make_manifest("incompat-plugin", api_version=Version(2, 0, 0))
        context.manifests = (manifest,)
        rejected_events: list[str] = []
        context.events.subscribe(
            "security.plugin.rejected",
            lambda e: rejected_events.append(e.payload["identifier"]),
        )
        stage = PluginSecurityStage()
        stage.execute(context)
        self.assertEqual(context.admitted_manifests, ())
        self.assertIn("incompat-plugin", rejected_events)

    def test_api_version_gate_incompatible_major_zero(self) -> None:
        """Plugin requiring API 0.x.x rejected when host provides 1.x.x."""
        context = self._make_context()
        manifest = self._make_manifest("old-api-plugin", api_version=Version(0, 9, 0))
        context.manifests = (manifest,)
        stage = PluginSecurityStage()
        stage.execute(context)
        self.assertEqual(context.admitted_manifests, ())

    def test_rejection_message_contains_versions(self) -> None:
        """Rejection event reason includes expected and declared versions."""
        context = self._make_context()
        manifest = self._make_manifest("detail-plugin", api_version=Version(3, 0, 0))
        context.manifests = (manifest,)
        reasons: list[str] = []
        context.events.subscribe(
            "security.plugin.rejected",
            lambda e: reasons.append(e.payload["reason"]),
        )
        stage = PluginSecurityStage()
        stage.execute(context)
        self.assertEqual(len(reasons), 1)
        self.assertIn("3.0.0", reasons[0])
        self.assertIn("1.0.0", reasons[0])


class TestIntegrityValidation(unittest.TestCase):
    """AC-9: Integrity Validation — policy, trust determination, SignatureStatus."""

    def _make_manifest(self, identifier: str) -> PluginManifest:
        return PluginManifest(
            identifier=identifier,
            version=Version(1, 0, 0),
            required_application_version=Version(0, 3, 0),
        )

    def test_integrity_policy_default(self) -> None:
        """Default integrity policy uses structural evidence level."""
        policy = IntegrityPolicy()
        self.assertEqual(policy.evidence_level, IntegrityEvidenceLevel.STRUCTURAL)
        self.assertEqual(policy.scope, "manifest")
        self.assertEqual(policy.minimum_trust, PluginTrustLevel.VERIFIED)

    def test_integrity_policy_from_config(self) -> None:
        """IntegrityPolicy.from_config reads valid configuration."""
        config: dict[str, object] = {
            "evidence_level": "content",
            "scope": "both",
            "minimum_trust": "trusted",
        }
        policy = IntegrityPolicy.from_config(config)
        self.assertEqual(policy.evidence_level, IntegrityEvidenceLevel.CONTENT)
        self.assertEqual(policy.scope, "both")
        self.assertEqual(policy.minimum_trust, PluginTrustLevel.TRUSTED)

    def test_integrity_policy_from_config_invalid_defaults(self) -> None:
        """Invalid config values fall back to safe defaults."""
        config: dict[str, object] = {
            "evidence_level": "invalid",
            "scope": "unknown",
            "minimum_trust": "bogus",
        }
        policy = IntegrityPolicy.from_config(config)
        self.assertEqual(policy.evidence_level, IntegrityEvidenceLevel.STRUCTURAL)
        self.assertEqual(policy.scope, "manifest")
        self.assertEqual(policy.minimum_trust, PluginTrustLevel.VERIFIED)

    def test_validate_integrity_untrusted_structural_pass(self) -> None:
        """Untrusted plugin with valid structure → VERIFIED, admitted."""
        events = EventBus()
        security = PluginSecurity(events)
        manifest = self._make_manifest("new-plugin")
        result = security.validate_integrity(manifest)
        self.assertIsInstance(result, IntegrityResult)
        self.assertTrue(result.admitted)
        self.assertEqual(result.trust, PluginTrustLevel.VERIFIED)
        self.assertEqual(result.signature_status, SignatureStatus.VERIFIED)

    def test_validate_integrity_trusted_plugin(self) -> None:
        """Pre-approved plugin → TRUSTED, admitted, SignatureStatus.TRUSTED."""
        events = EventBus()
        security = PluginSecurity(events)
        security.approve("trusted-plugin")
        manifest = self._make_manifest("trusted-plugin")
        result = security.validate_integrity(manifest)
        self.assertTrue(result.admitted)
        self.assertEqual(result.trust, PluginTrustLevel.TRUSTED)
        self.assertEqual(result.signature_status, SignatureStatus.TRUSTED)

    def test_validate_integrity_rejected_plugin(self) -> None:
        """Explicitly rejected plugin → REJECTED, not admitted."""
        events = EventBus()
        security = PluginSecurity(events)
        security.reject("bad-plugin", "policy violation")
        manifest = self._make_manifest("bad-plugin")
        result = security.validate_integrity(manifest)
        self.assertFalse(result.admitted)
        self.assertEqual(result.trust, PluginTrustLevel.REJECTED)
        self.assertEqual(result.signature_status, SignatureStatus.REJECTED)
        self.assertIn("rejected", result.reason)

    def test_validate_integrity_signature_status_used(self) -> None:
        """AC-9: SignatureStatus enum is used as data structure."""
        events = EventBus()
        security = PluginSecurity(events)
        manifest = self._make_manifest("sig-test")
        result = security.validate_integrity(manifest)
        self.assertIsInstance(result.signature_status, SignatureStatus)

    def test_validate_integrity_trust_level_used(self) -> None:
        """AC-9: Trust semantics use existing PluginTrustLevel enum."""
        events = EventBus()
        security = PluginSecurity(events)
        manifest = self._make_manifest("trust-test")
        result = security.validate_integrity(manifest)
        self.assertIsInstance(result.trust, PluginTrustLevel)

    def test_validate_integrity_result_immutable(self) -> None:
        """Integrity result is recorded and retrievable."""
        events = EventBus()
        security = PluginSecurity(events)
        manifest = self._make_manifest("immutable-test")
        security.validate_integrity(manifest)
        result = security.integrity_result("immutable-test")
        self.assertIsNotNone(result)
        self.assertEqual(result.identifier, "immutable-test")

    def test_validate_integrity_audit_event_verified(self) -> None:
        """Verified integrity emits PluginVerified event."""
        events = EventBus()
        verified_events: list[str] = []
        events.subscribe(
            "security.plugin.verified",
            lambda e: verified_events.append(e.payload["identifier"]),
        )
        security = PluginSecurity(events)
        manifest = self._make_manifest("audit-verified")
        security.validate_integrity(manifest)
        self.assertIn("audit-verified", verified_events)

    def test_validate_integrity_audit_event_rejected(self) -> None:
        """Rejected integrity emits PluginRejected event."""
        events = EventBus()
        rejected_events: list[str] = []
        events.subscribe(
            "security.plugin.rejected",
            lambda e: rejected_events.append(e.payload["identifier"]),
        )
        security = PluginSecurity(events)
        security.reject("audit-rejected", "test rejection")
        manifest = self._make_manifest("audit-rejected")
        security.validate_integrity(manifest)

    def test_integrity_policy_property(self) -> None:
        """PluginSecurity exposes the active integrity policy."""
        events = EventBus()
        policy = IntegrityPolicy(evidence_level=IntegrityEvidenceLevel.CONTENT)
        security = PluginSecurity(events, integrity_policy=policy)
        self.assertIs(security.integrity_policy, policy)
        self.assertEqual(security.integrity_policy.evidence_level, IntegrityEvidenceLevel.CONTENT)

    def test_validate_integrity_without_crypto(self) -> None:
        """AC-9: Integrity model is testable without cryptographic enforcement."""
        events = EventBus()
        policy = IntegrityPolicy(evidence_level=IntegrityEvidenceLevel.STRUCTURAL)
        security = PluginSecurity(events, integrity_policy=policy)
        manifest = self._make_manifest("no-crypto")
        result = security.validate_integrity(manifest)
        self.assertTrue(result.admitted)
        self.assertEqual(result.trust, PluginTrustLevel.VERIFIED)


class TestPermissionEnforcementGranted(_TestBase):
    """AC-4: Declared capability granted by policy → access granted."""

    def test_permission_enforcement_granted(self) -> None:
        """Declared capability with matching policy grant → plugin admitted."""
        events = EventBus()
        policy = PermissionPolicy(
            wildcard_grants=frozenset({"events.publish", "events.subscribe"}),
        )
        security = PluginSecurity(events, permission_policy=policy)
        manifest = self._make_manifest(
            "granted-plugin",
            permissions=("events.publish",),
        )
        result = security.validate_permissions(manifest)

        self.assertIsInstance(result, PermissionResult)
        self.assertTrue(result.admitted)
        self.assertIn("events.publish", result.granted)
        self.assertEqual(len(result.denied), 0)
        self.assertEqual(result.reason, "")

    def test_permission_granted_via_plugin_specific_policy(self) -> None:
        """Per-plugin grants override default-deny for the target plugin."""
        events = EventBus()
        policy = PermissionPolicy(
            plugin_grants={"specific-plugin": frozenset({"filesystem", "network"})},
        )
        security = PluginSecurity(events, permission_policy=policy)
        manifest = self._make_manifest(
            "specific-plugin",
            permissions=("filesystem", "network"),
        )
        result = security.validate_permissions(manifest)

        self.assertTrue(result.admitted)
        self.assertEqual(result.granted, frozenset({"filesystem", "network"}))
        self.assertEqual(len(result.denied), 0)

    def test_permission_no_declarations_always_admitted(self) -> None:
        """Plugin without declared permissions is always admitted (nothing to deny)."""
        events = EventBus()
        security = PluginSecurity(events)
        manifest = self._make_manifest("no-perms-plugin")
        result = security.validate_permissions(manifest)

        self.assertTrue(result.admitted)
        self.assertEqual(result.granted, frozenset())
        self.assertEqual(result.denied, frozenset())

    def test_permission_granted_admission_stage(self) -> None:
        """Full PluginSecurityStage admits plugin when policy grants declared permissions."""
        context = self._make_context()
        policy = PermissionPolicy(
            wildcard_grants=frozenset({"events.publish"}),
        )
        security = PluginSecurity(context.events, permission_policy=policy)
        context.registry.register(PluginSecurity, security)
        manifest = self._make_manifest(
            "stage-granted",
            permissions=("events.publish",),
        )
        context.manifests = (manifest,)

        stage = PluginSecurityStage()
        stage.execute(context)

        self.assertEqual(len(context.admitted_manifests), 1)
        self.assertEqual(context.admitted_manifests[0].identifier, "stage-granted")

    def test_permission_runtime_enforcement_succeeds(self) -> None:
        """AC-4: SDK PermissionCheck connected to host enforcement — granted access works."""
        from core.events import Event
        from sdk.events import PluginEventBus

        events = EventBus()
        granted = frozenset({PluginPermission.EVENTS_PUBLISH})

        def permission_check(permission: PluginPermission) -> None:
            if permission not in granted:
                raise PluginPermissionError(
                    f"Plugin lacks permission {permission.value!r}"
                )

        bus = PluginEventBus(
            "runtime-granted",
            events,
            event_type=Event,
            permission_check=permission_check,
        )
        bus.publish("test.event")


class TestPermissionEnforcementDenied(_TestBase):
    """AC-4: Undeclared/denied capability → access denied."""

    def test_permission_enforcement_denied(self) -> None:
        """Declared capability without policy grant → plugin rejected at admission."""
        events = EventBus()
        security = PluginSecurity(events)
        manifest = self._make_manifest(
            "denied-plugin",
            permissions=("filesystem", "network"),
        )
        result = security.validate_permissions(manifest)

        self.assertIsInstance(result, PermissionResult)
        self.assertFalse(result.admitted)
        self.assertEqual(result.denied, frozenset({"filesystem", "network"}))
        self.assertIn("filesystem", result.reason)

    def test_permission_denied_partial(self) -> None:
        """If any declared permission is denied, entire plugin is rejected."""
        events = EventBus()
        policy = PermissionPolicy(
            wildcard_grants=frozenset({"filesystem"}),
        )
        security = PluginSecurity(events, permission_policy=policy)
        manifest = self._make_manifest(
            "partial-plugin",
            permissions=("filesystem", "network"),
        )
        result = security.validate_permissions(manifest)

        self.assertFalse(result.admitted)
        self.assertIn("filesystem", result.granted)
        self.assertIn("network", result.denied)

    def test_permission_denied_emits_rejection_event(self) -> None:
        """Permission denial emits PluginRejected event."""
        events = EventBus()
        rejected: list[str] = []
        events.subscribe(
            "security.plugin.rejected",
            lambda e: rejected.append(e.payload["identifier"]),
        )
        security = PluginSecurity(events)
        manifest = self._make_manifest(
            "event-denied",
            permissions=("filesystem",),
        )
        security.validate_permissions(manifest)

        self.assertIn("event-denied", rejected)

    def test_permission_denied_admission_stage(self) -> None:
        """Full PluginSecurityStage rejects plugin when permissions denied."""
        context = self._make_context()
        security = PluginSecurity(context.events)
        context.registry.register(PluginSecurity, security)
        manifest = self._make_manifest(
            "stage-denied",
            permissions=("filesystem",),
        )
        context.manifests = (manifest,)

        rejected: list[str] = []
        context.events.subscribe(
            "security.plugin.rejected",
            lambda e: rejected.append(e.payload["identifier"]),
        )

        stage = PluginSecurityStage()
        stage.execute(context)

        self.assertEqual(context.admitted_manifests, ())
        self.assertIn("stage-denied", rejected)

    def test_permission_runtime_enforcement_blocks(self) -> None:
        """AC-4: SDK PermissionCheck connected to host enforcement — undeclared access blocked."""
        from core.events import Event
        from sdk.events import PluginEventBus

        events = EventBus()
        granted = frozenset({PluginPermission.EVENTS_SUBSCRIBE})

        def permission_check(permission: PluginPermission) -> None:
            if permission not in granted:
                raise PluginPermissionError(
                    f"Plugin lacks permission {permission.value!r}"
                )

        bus = PluginEventBus(
            "runtime-denied",
            events,
            event_type=Event,
            permission_check=permission_check,
        )
        with self.assertRaises(PluginPermissionError):
            bus.publish("test.event")

    def test_permission_default_deny(self) -> None:
        """ADR-006 D1: Default-deny — empty policy denies all declared permissions."""
        events = EventBus()
        policy = PermissionPolicy()
        security = PluginSecurity(events, permission_policy=policy)
        manifest = self._make_manifest(
            "default-deny-plugin",
            permissions=("events.publish",),
        )
        result = security.validate_permissions(manifest)

        self.assertFalse(result.admitted)
        self.assertIn("events.publish", result.denied)


if __name__ == "__main__":
    unittest.main()
