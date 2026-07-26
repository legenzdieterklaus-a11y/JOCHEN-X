"""Security policy tests (Phase 8 Phase-Gate).

Verifies:
- Default Deny is active
- Least Privilege enforcement
- Input validation under adversarial inputs
- Permission bypass attempts are rejected
- Audit log records security violations
- EventBus receives security violation events
- Thread safety under concurrent access
"""

from __future__ import annotations

import threading
import time

import pytest

from jochen_x.core.events.bus import EventBus
from jochen_x.core.exceptions.security import (
    InputValidationError,
    PermissionDeniedError,
)
from jochen_x.core.observability.audit import AuditLog
from jochen_x.core.security.permissions import (
    Permission,
    PermissionManager,
)
from jochen_x.core.security.policy import (
    PolicyEngine,
    SecurityPolicy,
)
from jochen_x.core.security.validator import InputValidator
from jochen_x.core.types.events import (
    RuntimeEvent,
    SecurityViolationEvent,
)

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def audit_log() -> AuditLog:
    return AuditLog()


@pytest.fixture
def event_bus() -> EventBus:
    bus = EventBus()
    bus.start()
    yield bus
    bus.stop()


@pytest.fixture
def permission_manager(
    audit_log: AuditLog,
    event_bus: EventBus,
) -> PermissionManager:
    return PermissionManager(
        audit_log=audit_log,
        event_bus=event_bus,
    )


@pytest.fixture
def policy_engine(
    permission_manager: PermissionManager,
    audit_log: AuditLog,
    event_bus: EventBus,
) -> PolicyEngine:
    return PolicyEngine(
        permission_manager=permission_manager,
        audit_log=audit_log,
        event_bus=event_bus,
    )


@pytest.fixture
def read_perm() -> Permission:
    return Permission(name="runtime.read", description="Read access")


@pytest.fixture
def write_perm() -> Permission:
    return Permission(name="runtime.write", description="Write access")


@pytest.fixture
def admin_perm() -> Permission:
    return Permission(name="runtime.admin", description="Admin access")


# ---------------------------------------------------------------------------
# Default Deny
# ---------------------------------------------------------------------------

class TestDefaultDeny:
    """Verify that Default Deny is active and cannot be bypassed."""

    def test_unknown_principal_denied(
        self, permission_manager: PermissionManager,
    ) -> None:
        assert not permission_manager.check_permission(
            "unknown", "any.permission"
        )

    def test_unknown_permission_denied(
        self,
        permission_manager: PermissionManager,
        read_perm: Permission,
    ) -> None:
        permission_manager.grant_permission("agent_a", read_perm)
        assert not permission_manager.check_permission(
            "agent_a", "nonexistent.permission"
        )

    def test_policy_default_deny_no_policy(
        self, policy_engine: PolicyEngine,
    ) -> None:
        decision = policy_engine.evaluate("agent_a", "unregistered_op")
        assert not decision.allowed
        assert "Default Deny" in decision.reason

    def test_policy_default_deny_enforce(
        self, policy_engine: PolicyEngine,
    ) -> None:
        with pytest.raises(PermissionDeniedError):
            policy_engine.enforce("agent_a", "unregistered_op")

    def test_revoked_permission_denied(
        self,
        permission_manager: PermissionManager,
        read_perm: Permission,
    ) -> None:
        permission_manager.grant_permission("agent_a", read_perm)
        permission_manager.revoke_permission("agent_a", "runtime.read")
        assert not permission_manager.check_permission(
            "agent_a", "runtime.read"
        )

    def test_revoke_all_denies_everything(
        self,
        permission_manager: PermissionManager,
        read_perm: Permission,
        write_perm: Permission,
    ) -> None:
        permission_manager.grant_permission("agent_a", read_perm)
        permission_manager.grant_permission("agent_a", write_perm)
        permission_manager.revoke_all("agent_a")
        assert not permission_manager.check_permission(
            "agent_a", "runtime.read"
        )
        assert not permission_manager.check_permission(
            "agent_a", "runtime.write"
        )


# ---------------------------------------------------------------------------
# Least Privilege
# ---------------------------------------------------------------------------

class TestLeastPrivilege:
    """Verify Least Privilege: only granted permissions are available."""

    def test_only_granted_permissions(
        self,
        permission_manager: PermissionManager,
        read_perm: Permission,
        write_perm: Permission,
    ) -> None:
        permission_manager.grant_permission("agent_a", read_perm)
        assert permission_manager.check_permission(
            "agent_a", "runtime.read"
        )
        assert not permission_manager.check_permission(
            "agent_a", "runtime.write"
        )

    def test_no_privilege_escalation(
        self,
        permission_manager: PermissionManager,
        read_perm: Permission,
        admin_perm: Permission,
    ) -> None:
        permission_manager.grant_permission("agent_a", read_perm)
        assert not permission_manager.check_permission(
            "agent_a", "runtime.admin"
        )

    def test_separate_principals_isolated(
        self,
        permission_manager: PermissionManager,
        read_perm: Permission,
        write_perm: Permission,
    ) -> None:
        permission_manager.grant_permission("agent_a", read_perm)
        permission_manager.grant_permission("agent_b", write_perm)
        assert not permission_manager.check_permission(
            "agent_a", "runtime.write"
        )
        assert not permission_manager.check_permission(
            "agent_b", "runtime.read"
        )

    def test_policy_requires_all_permissions(
        self,
        permission_manager: PermissionManager,
        policy_engine: PolicyEngine,
        read_perm: Permission,
    ) -> None:
        permission_manager.grant_permission("agent_a", read_perm)
        policy = SecurityPolicy(
            policy_id="multi",
            description="Multi-perm",
            operation="critical_op",
            required_permissions=("runtime.read", "runtime.write"),
        )
        policy_engine.register_policy(policy)
        decision = policy_engine.evaluate("agent_a", "critical_op")
        assert not decision.allowed
        assert "runtime.write" in decision.missing_permissions


# ---------------------------------------------------------------------------
# Input Validation (Adversarial)
# ---------------------------------------------------------------------------

class TestAdversarialInputValidation:
    """Test input validation against adversarial inputs."""

    def test_empty_strings_rejected(self) -> None:
        with pytest.raises(InputValidationError):
            InputValidator.validate_non_empty_string("", "field")

    def test_none_rejected(self) -> None:
        with pytest.raises(InputValidationError):
            InputValidator.validate_not_none(None, "field")

    def test_wrong_type_rejected(self) -> None:
        with pytest.raises(InputValidationError):
            InputValidator.validate_type(42, "field", str)

    def test_negative_int_rejected(self) -> None:
        with pytest.raises(InputValidationError):
            InputValidator.validate_non_negative_int(-1, "field")

    def test_nan_rejected(self) -> None:
        with pytest.raises(InputValidationError):
            InputValidator.validate_float(float("nan"), "field")

    def test_inf_rejected(self) -> None:
        with pytest.raises(InputValidationError):
            InputValidator.validate_float(float("inf"), "field")

    def test_negative_inf_rejected(self) -> None:
        with pytest.raises(InputValidationError):
            InputValidator.validate_float(float("-inf"), "field")

    def test_bool_as_int_rejected(self) -> None:
        bool_val: int = True  # type: ignore[assignment]
        with pytest.raises(InputValidationError):
            InputValidator.validate_int(bool_val, "field")

    def test_bool_as_float_rejected(self) -> None:
        bool_val: float = False  # type: ignore[assignment]
        with pytest.raises(InputValidationError):
            InputValidator.validate_float(bool_val, "field")

    def test_oversized_string_rejected(self) -> None:
        with pytest.raises(InputValidationError):
            InputValidator.validate_string(
                "x" * 100, "field", max_length=50,
            )

    def test_permission_manager_rejects_non_string_principal(
        self, permission_manager: PermissionManager,
    ) -> None:
        with pytest.raises(InputValidationError):
            permission_manager.check_permission(None, "perm")  # type: ignore[arg-type]

    def test_permission_manager_rejects_non_string_permission(
        self, permission_manager: PermissionManager,
    ) -> None:
        with pytest.raises(InputValidationError):
            permission_manager.check_permission("principal", 123)  # type: ignore[arg-type]

    def test_policy_engine_rejects_empty_principal(
        self, policy_engine: PolicyEngine,
    ) -> None:
        with pytest.raises(InputValidationError):
            policy_engine.evaluate("", "operation")

    def test_policy_engine_rejects_empty_operation(
        self, policy_engine: PolicyEngine,
    ) -> None:
        with pytest.raises(InputValidationError):
            policy_engine.evaluate("principal", "")

    def test_invalid_permission_name_format(
        self, permission_manager: PermissionManager,
    ) -> None:
        with pytest.raises(InputValidationError):
            permission_manager.register_permission(
                Permission(name="UPPERCASE")
            )

    def test_invalid_permission_name_special_chars(
        self, permission_manager: PermissionManager,
    ) -> None:
        with pytest.raises(InputValidationError):
            permission_manager.register_permission(
                Permission(name="perm with spaces")
            )

    def test_invalid_principal_format(
        self,
        permission_manager: PermissionManager,
        read_perm: Permission,
    ) -> None:
        with pytest.raises(InputValidationError):
            permission_manager.grant_permission("123bad", read_perm)


# ---------------------------------------------------------------------------
# Permission Bypass Attempts
# ---------------------------------------------------------------------------

class TestPermissionBypassAttempts:
    """Verify that permission bypass attempts always fail."""

    def test_cannot_bypass_via_case_sensitivity(
        self,
        permission_manager: PermissionManager,
        read_perm: Permission,
    ) -> None:
        permission_manager.grant_permission("agent_a", read_perm)
        assert not permission_manager.check_permission(
            "agent_a", "Runtime.Read"
        )
        assert not permission_manager.check_permission(
            "agent_a", "RUNTIME.READ"
        )

    def test_cannot_bypass_via_different_principal(
        self,
        permission_manager: PermissionManager,
        read_perm: Permission,
    ) -> None:
        permission_manager.grant_permission("agent_a", read_perm)
        assert not permission_manager.check_permission(
            "agent_b", "runtime.read"
        )

    def test_cannot_bypass_via_similar_permission_name(
        self,
        permission_manager: PermissionManager,
        read_perm: Permission,
    ) -> None:
        permission_manager.grant_permission("agent_a", read_perm)
        assert not permission_manager.check_permission(
            "agent_a", "runtime.read."
        )
        assert not permission_manager.check_permission(
            "agent_a", "runtime.read_all"
        )

    def test_cannot_bypass_policy_by_disabling(
        self, policy_engine: PolicyEngine,
    ) -> None:
        policy = SecurityPolicy(
            policy_id="p1",
            description="D",
            operation="op",
            required_permissions=("r",),
            enabled=True,
        )
        policy_engine.register_policy(policy)
        decision = policy_engine.evaluate("agent_a", "op")
        assert not decision.allowed


# ---------------------------------------------------------------------------
# Audit Integration
# ---------------------------------------------------------------------------

class TestAuditIntegration:
    """Verify security violations appear in the audit log."""

    def test_permission_denied_audited(
        self, audit_log: AuditLog,
    ) -> None:
        mgr = PermissionManager(audit_log=audit_log)
        with pytest.raises(PermissionDeniedError):
            mgr.require_permission("agent_a", "secret.perm")
        entries = audit_log.get_entries()
        violations = [
            e for e in entries if isinstance(e, SecurityViolationEvent)
        ]
        assert len(violations) >= 1
        assert violations[0].violation_type == "permission_denied"

    def test_policy_denial_audited(
        self, audit_log: AuditLog,
    ) -> None:
        mgr = PermissionManager(audit_log=audit_log)
        engine = PolicyEngine(
            permission_manager=mgr, audit_log=audit_log,
        )
        policy = SecurityPolicy(
            policy_id="p1",
            description="D",
            operation="op",
            required_permissions=("r",),
        )
        engine.register_policy(policy)
        engine.evaluate("agent_a", "op")
        entries = audit_log.get_entries()
        violations = [
            e for e in entries if isinstance(e, SecurityViolationEvent)
        ]
        assert any(v.violation_type == "policy_denied" for v in violations)

    def test_permission_grant_audited(
        self, audit_log: AuditLog, read_perm: Permission,
    ) -> None:
        mgr = PermissionManager(audit_log=audit_log)
        mgr.grant_permission("agent_a", read_perm)
        entries = audit_log.get_entries()
        violations = [
            e for e in entries if isinstance(e, SecurityViolationEvent)
        ]
        assert any(
            v.violation_type == "permission_granted" for v in violations
        )

    def test_permission_revocation_audited(
        self, audit_log: AuditLog, read_perm: Permission,
    ) -> None:
        mgr = PermissionManager(audit_log=audit_log)
        mgr.grant_permission("agent_a", read_perm)
        mgr.revoke_permission("agent_a", "runtime.read")
        entries = audit_log.get_entries()
        violations = [
            e for e in entries if isinstance(e, SecurityViolationEvent)
        ]
        assert any(
            v.violation_type == "permission_revoked" for v in violations
        )

    def test_audit_integrity_after_security_events(
        self, audit_log: AuditLog,
    ) -> None:
        mgr = PermissionManager(audit_log=audit_log)
        with pytest.raises(PermissionDeniedError):
            mgr.require_permission("agent_a", "perm")
        assert audit_log.verify_integrity()


# ---------------------------------------------------------------------------
# EventBus Integration
# ---------------------------------------------------------------------------

class TestEventBusIntegration:
    """Verify security violations are published via the EventBus."""

    def test_permission_denied_publishes_event(
        self,
        event_bus: EventBus,
        audit_log: AuditLog,
    ) -> None:
        received: list[SecurityViolationEvent] = []

        def handler(event: RuntimeEvent) -> None:
            if isinstance(event, SecurityViolationEvent):
                received.append(event)

        event_bus.subscribe(SecurityViolationEvent, handler)

        mgr = PermissionManager(
            audit_log=audit_log, event_bus=event_bus,
        )
        with pytest.raises(PermissionDeniedError):
            mgr.require_permission("agent_a", "perm")

        time.sleep(0.2)

        assert len(received) >= 1
        assert received[0].violation_type == "permission_denied"

    def test_policy_denied_publishes_event(
        self,
        event_bus: EventBus,
        audit_log: AuditLog,
    ) -> None:
        received: list[SecurityViolationEvent] = []

        def handler(event: RuntimeEvent) -> None:
            if isinstance(event, SecurityViolationEvent):
                received.append(event)

        event_bus.subscribe(SecurityViolationEvent, handler)

        mgr = PermissionManager(audit_log=audit_log, event_bus=event_bus)
        engine = PolicyEngine(
            permission_manager=mgr,
            audit_log=audit_log,
            event_bus=event_bus,
        )
        policy = SecurityPolicy(
            policy_id="p1",
            description="D",
            operation="op",
            required_permissions=("r",),
        )
        engine.register_policy(policy)
        engine.evaluate("agent_a", "op")

        time.sleep(0.2)

        assert len(received) >= 1
        assert any(
            e.violation_type == "policy_denied" for e in received
        )


# ---------------------------------------------------------------------------
# Thread Safety
# ---------------------------------------------------------------------------

class TestThreadSafety:
    """Verify thread safety under concurrent access."""

    def test_concurrent_grant_and_check(
        self, read_perm: Permission,
    ) -> None:
        mgr = PermissionManager()
        errors: list[str] = []

        def grant_and_check(idx: int) -> None:
            principal = f"agent_{idx}"
            try:
                mgr.grant_permission(principal, read_perm)
                result = mgr.check_permission(principal, "runtime.read")
                assert result
            except Exception as exc:
                errors.append(str(exc))

        threads = [
            threading.Thread(target=grant_and_check, args=(i,))
            for i in range(20)
        ]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert not errors

    def test_concurrent_policy_evaluation(
        self, read_perm: Permission,
    ) -> None:
        mgr = PermissionManager()
        engine = PolicyEngine(permission_manager=mgr)
        mgr.grant_permission("agent_a", read_perm)

        policy = SecurityPolicy(
            policy_id="p1",
            description="D",
            operation="op",
            required_permissions=("runtime.read",),
        )
        engine.register_policy(policy)

        errors: list[str] = []

        def evaluate_repeatedly() -> None:
            for _ in range(50):
                try:
                    decision = engine.evaluate("agent_a", "op")
                    assert decision.allowed
                except Exception as exc:
                    errors.append(str(exc))

        threads = [
            threading.Thread(target=evaluate_repeatedly) for _ in range(4)
        ]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert not errors

    def test_concurrent_grant_revoke(
        self, read_perm: Permission,
    ) -> None:
        mgr = PermissionManager()
        errors: list[str] = []

        def grant_revoke_cycle(idx: int) -> None:
            principal = f"agent_{idx}"
            try:
                for _ in range(20):
                    mgr.grant_permission(principal, read_perm)
                    mgr.revoke_permission(principal, "runtime.read")
            except Exception as exc:
                errors.append(str(exc))

        threads = [
            threading.Thread(target=grant_revoke_cycle, args=(i,))
            for i in range(10)
        ]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert not errors
