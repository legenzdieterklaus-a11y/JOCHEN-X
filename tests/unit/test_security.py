"""Unit tests for the security subsystem (Phase 8).

Tests cover: Permission, PermissionSet, PermissionManager,
InputValidator, SecurityPolicy, PolicyDecision, and PolicyEngine.
"""

from __future__ import annotations

import re
import threading

import pytest

from jochen_x.core.exceptions.security import (
    InputValidationError,
    PermissionDeniedError,
)
from jochen_x.core.observability.audit import AuditLog
from jochen_x.core.security.permissions import (
    Permission,
    PermissionGrant,
    PermissionManager,
    PermissionSet,
)
from jochen_x.core.security.policy import (
    PolicyDecision,
    PolicyEngine,
    SecurityPolicy,
)
from jochen_x.core.security.validator import InputValidator
from jochen_x.core.types.events import SecurityViolationEvent
from jochen_x.core.types.health_status import HealthStatus

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def audit_log() -> AuditLog:
    return AuditLog()


@pytest.fixture
def permission_manager(audit_log: AuditLog) -> PermissionManager:
    return PermissionManager(audit_log=audit_log)


@pytest.fixture
def policy_engine(
    permission_manager: PermissionManager,
    audit_log: AuditLog,
) -> PolicyEngine:
    return PolicyEngine(
        permission_manager=permission_manager,
        audit_log=audit_log,
    )


@pytest.fixture
def read_perm() -> Permission:
    return Permission(name="runtime.read", description="Read access")


@pytest.fixture
def write_perm() -> Permission:
    return Permission(name="runtime.write", description="Write access")


# ---------------------------------------------------------------------------
# Permission dataclass
# ---------------------------------------------------------------------------

class TestPermission:
    def test_creation(self) -> None:
        perm = Permission(name="runtime.start", description="Start runtime")
        assert perm.name == "runtime.start"
        assert perm.description == "Start runtime"

    def test_frozen(self) -> None:
        perm = Permission(name="runtime.start")
        with pytest.raises(AttributeError):
            perm.name = "changed"  # type: ignore[misc]

    def test_equality(self) -> None:
        p1 = Permission(name="runtime.start", description="Start")
        p2 = Permission(name="runtime.start", description="Start")
        assert p1 == p2

    def test_default_description(self) -> None:
        perm = Permission(name="runtime.stop")
        assert perm.description == ""


# ---------------------------------------------------------------------------
# PermissionGrant dataclass
# ---------------------------------------------------------------------------

class TestPermissionGrant:
    def test_creation(self, read_perm: Permission) -> None:
        grant = PermissionGrant(
            principal="plugin_a",
            permission=read_perm,
            granted_by="admin",
        )
        assert grant.principal == "plugin_a"
        assert grant.permission == read_perm
        assert grant.granted_by == "admin"
        assert grant.granted_at is not None

    def test_frozen(self, read_perm: Permission) -> None:
        grant = PermissionGrant(principal="p", permission=read_perm)
        with pytest.raises(AttributeError):
            grant.principal = "changed"  # type: ignore[misc]


# ---------------------------------------------------------------------------
# PermissionSet
# ---------------------------------------------------------------------------

class TestPermissionSet:
    def test_add_and_contains(self, read_perm: Permission) -> None:
        pset = PermissionSet()
        pset.add(read_perm)
        assert pset.contains("runtime.read")
        assert not pset.contains("runtime.write")

    def test_remove(self, read_perm: Permission) -> None:
        pset = PermissionSet()
        pset.add(read_perm)
        assert pset.remove("runtime.read")
        assert not pset.contains("runtime.read")

    def test_remove_nonexistent(self) -> None:
        pset = PermissionSet()
        assert not pset.remove("nonexistent")

    def test_get_all(
        self, read_perm: Permission, write_perm: Permission,
    ) -> None:
        pset = PermissionSet()
        pset.add(read_perm)
        pset.add(write_perm)
        all_perms = pset.get_all()
        names = {p.name for p in all_perms}
        assert names == {"runtime.read", "runtime.write"}

    def test_clear(self, read_perm: Permission) -> None:
        pset = PermissionSet()
        pset.add(read_perm)
        pset.clear()
        assert pset.size() == 0

    def test_size(
        self, read_perm: Permission, write_perm: Permission,
    ) -> None:
        pset = PermissionSet()
        assert pset.size() == 0
        pset.add(read_perm)
        assert pset.size() == 1
        pset.add(write_perm)
        assert pset.size() == 2

    def test_thread_safety(self) -> None:
        pset = PermissionSet()
        errors: list[str] = []

        def add_permissions(start: int, count: int) -> None:
            for i in range(start, start + count):
                try:
                    pset.add(Permission(name=f"perm.t{i}"))
                except Exception as exc:
                    errors.append(str(exc))

        threads = [
            threading.Thread(target=add_permissions, args=(i * 100, 100))
            for i in range(4)
        ]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert not errors
        assert pset.size() == 400


# ---------------------------------------------------------------------------
# PermissionManager
# ---------------------------------------------------------------------------

class TestPermissionManager:
    def test_register_permission(
        self, permission_manager: PermissionManager, read_perm: Permission,
    ) -> None:
        permission_manager.register_permission(read_perm)
        registered = permission_manager.get_registered_permissions()
        assert any(p.name == "runtime.read" for p in registered)

    def test_register_invalid_permission_name(
        self, permission_manager: PermissionManager,
    ) -> None:
        with pytest.raises(InputValidationError):
            permission_manager.register_permission(
                Permission(name="INVALID")
            )

    def test_register_empty_permission_name(
        self, permission_manager: PermissionManager,
    ) -> None:
        with pytest.raises(InputValidationError):
            permission_manager.register_permission(Permission(name=""))

    def test_register_invalid_type(
        self, permission_manager: PermissionManager,
    ) -> None:
        with pytest.raises(InputValidationError):
            permission_manager.register_permission("not_a_permission")  # type: ignore[arg-type]

    def test_unregister_permission(
        self, permission_manager: PermissionManager, read_perm: Permission,
    ) -> None:
        permission_manager.register_permission(read_perm)
        permission_manager.grant_permission("agent_a", read_perm)
        permission_manager.unregister_permission("runtime.read")
        assert not permission_manager.check_permission(
            "agent_a", "runtime.read"
        )

    def test_grant_permission(
        self, permission_manager: PermissionManager, read_perm: Permission,
    ) -> None:
        grant = permission_manager.grant_permission(
            "agent_a", read_perm, granted_by="admin",
        )
        assert isinstance(grant, PermissionGrant)
        assert grant.principal == "agent_a"
        assert grant.granted_by == "admin"

    def test_grant_invalid_principal(
        self, permission_manager: PermissionManager, read_perm: Permission,
    ) -> None:
        with pytest.raises(InputValidationError):
            permission_manager.grant_permission("", read_perm)

    def test_grant_invalid_principal_format(
        self, permission_manager: PermissionManager, read_perm: Permission,
    ) -> None:
        with pytest.raises(InputValidationError):
            permission_manager.grant_permission("123invalid", read_perm)

    def test_check_permission_granted(
        self, permission_manager: PermissionManager, read_perm: Permission,
    ) -> None:
        permission_manager.grant_permission("agent_a", read_perm)
        assert permission_manager.check_permission("agent_a", "runtime.read")

    def test_check_permission_not_granted(
        self, permission_manager: PermissionManager,
    ) -> None:
        assert not permission_manager.check_permission(
            "agent_a", "runtime.read"
        )

    def test_default_deny(
        self, permission_manager: PermissionManager,
    ) -> None:
        assert not permission_manager.check_permission(
            "unknown_principal", "any.permission"
        )

    def test_require_permission_granted(
        self, permission_manager: PermissionManager, read_perm: Permission,
    ) -> None:
        permission_manager.grant_permission("agent_a", read_perm)
        permission_manager.require_permission("agent_a", "runtime.read")

    def test_require_permission_denied(
        self, permission_manager: PermissionManager,
    ) -> None:
        with pytest.raises(PermissionDeniedError) as exc_info:
            permission_manager.require_permission(
                "agent_a", "runtime.read", operation="start_runtime",
            )
        assert "runtime.read" in str(exc_info.value)

    def test_require_permission_denied_audit(
        self,
        audit_log: AuditLog,
        read_perm: Permission,
    ) -> None:
        mgr = PermissionManager(audit_log=audit_log)
        with pytest.raises(PermissionDeniedError):
            mgr.require_permission("agent_a", "runtime.read")
        entries = audit_log.get_entries()
        assert len(entries) >= 1
        violation = entries[-1]
        assert isinstance(violation, SecurityViolationEvent)
        assert violation.violation_type == "permission_denied"

    def test_revoke_permission(
        self, permission_manager: PermissionManager, read_perm: Permission,
    ) -> None:
        permission_manager.grant_permission("agent_a", read_perm)
        assert permission_manager.revoke_permission("agent_a", "runtime.read")
        assert not permission_manager.check_permission(
            "agent_a", "runtime.read"
        )

    def test_revoke_not_granted(
        self, permission_manager: PermissionManager,
    ) -> None:
        assert not permission_manager.revoke_permission(
            "agent_a", "runtime.read"
        )

    def test_revoke_all(
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

    def test_get_permissions(
        self,
        permission_manager: PermissionManager,
        read_perm: Permission,
        write_perm: Permission,
    ) -> None:
        permission_manager.grant_permission("agent_a", read_perm)
        permission_manager.grant_permission("agent_a", write_perm)
        perms = permission_manager.get_permissions("agent_a")
        names = {p.name for p in perms}
        assert names == {"runtime.read", "runtime.write"}

    def test_get_permissions_empty(
        self, permission_manager: PermissionManager,
    ) -> None:
        perms = permission_manager.get_permissions("agent_a")
        assert len(perms) == 0

    def test_get_principals_with_permission(
        self, permission_manager: PermissionManager, read_perm: Permission,
    ) -> None:
        permission_manager.grant_permission("agent_a", read_perm)
        permission_manager.grant_permission("agent_b", read_perm)
        principals = permission_manager.get_principals_with_permission(
            "runtime.read"
        )
        assert set(principals) == {"agent_a", "agent_b"}

    def test_health_check(
        self, permission_manager: PermissionManager,
    ) -> None:
        assert permission_manager.check_health() == HealthStatus.HEALTHY

    def test_component_name(
        self, permission_manager: PermissionManager,
    ) -> None:
        assert permission_manager.get_component_name() == "PermissionManager"

    def test_check_permission_empty_principal(
        self, permission_manager: PermissionManager,
    ) -> None:
        with pytest.raises(InputValidationError):
            permission_manager.check_permission("", "runtime.read")

    def test_check_permission_empty_permission_name(
        self, permission_manager: PermissionManager,
    ) -> None:
        with pytest.raises(InputValidationError):
            permission_manager.check_permission("agent_a", "")

    def test_check_permission_non_string_principal(
        self, permission_manager: PermissionManager,
    ) -> None:
        with pytest.raises(InputValidationError):
            permission_manager.check_permission(123, "runtime.read")  # type: ignore[arg-type]

    def test_thread_safety_grants(
        self, read_perm: Permission,
    ) -> None:
        mgr = PermissionManager()
        errors: list[str] = []

        def grant_and_check(thread_id: int) -> None:
            principal = f"agent_{thread_id}"
            try:
                mgr.grant_permission(principal, read_perm)
                assert mgr.check_permission(principal, "runtime.read")
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

    def test_revoke_all_empty_principal(
        self, permission_manager: PermissionManager,
    ) -> None:
        with pytest.raises(InputValidationError):
            permission_manager.revoke_all("")

    def test_get_principals_empty_permission(
        self, permission_manager: PermissionManager,
    ) -> None:
        with pytest.raises(InputValidationError):
            permission_manager.get_principals_with_permission("")


# ---------------------------------------------------------------------------
# InputValidator
# ---------------------------------------------------------------------------

class TestInputValidator:
    def test_validate_not_none_passes(self) -> None:
        InputValidator.validate_not_none("value", "field")

    def test_validate_not_none_fails(self) -> None:
        with pytest.raises(InputValidationError) as exc_info:
            InputValidator.validate_not_none(None, "field")
        assert exc_info.value.field_name == "field"

    def test_validate_type_passes(self) -> None:
        InputValidator.validate_type("hello", "field", str)

    def test_validate_type_fails(self) -> None:
        with pytest.raises(InputValidationError) as exc_info:
            InputValidator.validate_type(123, "field", str)
        assert "expected str" in exc_info.value.reason

    def test_validate_string_passes(self) -> None:
        InputValidator.validate_string("hello", "field", min_length=1)

    def test_validate_string_too_short(self) -> None:
        with pytest.raises(InputValidationError):
            InputValidator.validate_string("", "field", min_length=1)

    def test_validate_string_too_long(self) -> None:
        with pytest.raises(InputValidationError):
            InputValidator.validate_string("abcde", "field", max_length=3)

    def test_validate_string_not_string(self) -> None:
        with pytest.raises(InputValidationError):
            InputValidator.validate_string(123, "field")  # type: ignore[arg-type]

    def test_validate_pattern_match(self) -> None:
        pattern = re.compile(r"^[a-z]+$")
        InputValidator.validate_pattern("abc", "field", pattern)

    def test_validate_pattern_no_match(self) -> None:
        pattern = re.compile(r"^[a-z]+$")
        with pytest.raises(InputValidationError):
            InputValidator.validate_pattern("ABC", "field", pattern)

    def test_validate_non_empty_string_passes(self) -> None:
        InputValidator.validate_non_empty_string("hello", "field")

    def test_validate_non_empty_string_fails(self) -> None:
        with pytest.raises(InputValidationError):
            InputValidator.validate_non_empty_string("", "field")

    def test_validate_int_passes(self) -> None:
        InputValidator.validate_int(5, "field", min_value=0, max_value=10)

    def test_validate_int_too_low(self) -> None:
        with pytest.raises(InputValidationError):
            InputValidator.validate_int(-1, "field", min_value=0)

    def test_validate_int_too_high(self) -> None:
        with pytest.raises(InputValidationError):
            InputValidator.validate_int(11, "field", max_value=10)

    def test_validate_int_not_int(self) -> None:
        with pytest.raises(InputValidationError):
            InputValidator.validate_int("5", "field")  # type: ignore[arg-type]

    def test_validate_int_rejects_bool(self) -> None:
        bool_val: int = True  # type: ignore[assignment]
        with pytest.raises(InputValidationError):
            InputValidator.validate_int(bool_val, "field")

    def test_validate_positive_int_passes(self) -> None:
        InputValidator.validate_positive_int(1, "field")

    def test_validate_positive_int_fails_zero(self) -> None:
        with pytest.raises(InputValidationError):
            InputValidator.validate_positive_int(0, "field")

    def test_validate_positive_int_fails_negative(self) -> None:
        with pytest.raises(InputValidationError):
            InputValidator.validate_positive_int(-1, "field")

    def test_validate_non_negative_int_passes(self) -> None:
        InputValidator.validate_non_negative_int(0, "field")

    def test_validate_non_negative_int_fails(self) -> None:
        with pytest.raises(InputValidationError):
            InputValidator.validate_non_negative_int(-1, "field")

    def test_validate_float_passes(self) -> None:
        InputValidator.validate_float(3.14, "field", min_value=0.0)

    def test_validate_float_int_accepted(self) -> None:
        InputValidator.validate_float(5, "field")

    def test_validate_float_too_low(self) -> None:
        with pytest.raises(InputValidationError):
            InputValidator.validate_float(-1.0, "field", min_value=0.0)

    def test_validate_float_too_high(self) -> None:
        with pytest.raises(InputValidationError):
            InputValidator.validate_float(11.0, "field", max_value=10.0)

    def test_validate_float_rejects_nan(self) -> None:
        with pytest.raises(InputValidationError):
            InputValidator.validate_float(float("nan"), "field")

    def test_validate_float_rejects_inf(self) -> None:
        with pytest.raises(InputValidationError):
            InputValidator.validate_float(float("inf"), "field")

    def test_validate_float_not_numeric(self) -> None:
        with pytest.raises(InputValidationError):
            InputValidator.validate_float("3.14", "field")  # type: ignore[arg-type]

    def test_validate_float_rejects_bool(self) -> None:
        bool_val: float = True  # type: ignore[assignment]
        with pytest.raises(InputValidationError):
            InputValidator.validate_float(bool_val, "field")

    def test_validate_enum_value_passes(self) -> None:
        InputValidator.validate_enum_value(
            HealthStatus.HEALTHY, "status", HealthStatus,
        )

    def test_validate_enum_value_fails(self) -> None:
        with pytest.raises(InputValidationError):
            InputValidator.validate_enum_value("HEALTHY", "status", HealthStatus)  # type: ignore[arg-type]

    def test_validate_collection_not_empty_passes(self) -> None:
        InputValidator.validate_collection_not_empty([1, 2], "items")

    def test_validate_collection_not_empty_fails(self) -> None:
        with pytest.raises(InputValidationError):
            InputValidator.validate_collection_not_empty([], "items")

    def test_validate_collection_not_collection(self) -> None:
        with pytest.raises(InputValidationError):
            InputValidator.validate_collection_not_empty(42, "items")

    def test_component_propagation(self) -> None:
        with pytest.raises(InputValidationError) as exc_info:
            InputValidator.validate_not_none(
                None, "field", component="MyComponent",
            )
        assert exc_info.value.component == "MyComponent"

    def test_boundary_string_min_length_zero(self) -> None:
        InputValidator.validate_string("", "field", min_length=0)

    def test_boundary_int_at_min(self) -> None:
        InputValidator.validate_int(0, "field", min_value=0)

    def test_boundary_int_at_max(self) -> None:
        InputValidator.validate_int(10, "field", max_value=10)

    def test_boundary_float_at_min(self) -> None:
        InputValidator.validate_float(0.0, "field", min_value=0.0)

    def test_boundary_float_at_max(self) -> None:
        InputValidator.validate_float(10.0, "field", max_value=10.0)

    def test_validate_float_negative_inf(self) -> None:
        with pytest.raises(InputValidationError):
            InputValidator.validate_float(float("-inf"), "field")


# ---------------------------------------------------------------------------
# SecurityPolicy dataclass
# ---------------------------------------------------------------------------

class TestSecurityPolicy:
    def test_creation(self) -> None:
        policy = SecurityPolicy(
            policy_id="pol_001",
            description="Read access policy",
            operation="runtime.read",
            required_permissions=("runtime.read",),
        )
        assert policy.policy_id == "pol_001"
        assert policy.operation == "runtime.read"
        assert policy.enabled is True

    def test_frozen(self) -> None:
        policy = SecurityPolicy(
            policy_id="p1",
            description="d",
            operation="op",
            required_permissions=("r",),
        )
        with pytest.raises(AttributeError):
            policy.policy_id = "changed"  # type: ignore[misc]

    def test_disabled(self) -> None:
        policy = SecurityPolicy(
            policy_id="p1",
            description="d",
            operation="op",
            required_permissions=("r",),
            enabled=False,
        )
        assert not policy.enabled


# ---------------------------------------------------------------------------
# PolicyDecision dataclass
# ---------------------------------------------------------------------------

class TestPolicyDecision:
    def test_allowed(self) -> None:
        decision = PolicyDecision(
            allowed=True,
            policy_id="p1",
            reason="OK",
            principal="agent_a",
            operation="read",
        )
        assert decision.allowed
        assert decision.missing_permissions == ()

    def test_denied(self) -> None:
        decision = PolicyDecision(
            allowed=False,
            reason="Missing",
            principal="agent_a",
            operation="write",
            missing_permissions=("runtime.write",),
        )
        assert not decision.allowed
        assert "runtime.write" in decision.missing_permissions


# ---------------------------------------------------------------------------
# PolicyEngine
# ---------------------------------------------------------------------------

class TestPolicyEngine:
    def test_register_policy(self, policy_engine: PolicyEngine) -> None:
        policy = SecurityPolicy(
            policy_id="pol_001",
            description="Read",
            operation="runtime.read",
            required_permissions=("runtime.read",),
        )
        policy_engine.register_policy(policy)
        assert policy_engine.get_policy("pol_001") is not None

    def test_register_duplicate_policy(
        self, policy_engine: PolicyEngine,
    ) -> None:
        policy = SecurityPolicy(
            policy_id="pol_001",
            description="Read",
            operation="runtime.read",
            required_permissions=("runtime.read",),
        )
        policy_engine.register_policy(policy)
        with pytest.raises(InputValidationError):
            policy_engine.register_policy(policy)

    def test_register_invalid_policy_type(
        self, policy_engine: PolicyEngine,
    ) -> None:
        with pytest.raises(InputValidationError):
            policy_engine.register_policy("not_a_policy")  # type: ignore[arg-type]

    def test_register_policy_empty_id(
        self, policy_engine: PolicyEngine,
    ) -> None:
        policy = SecurityPolicy(
            policy_id="",
            description="D",
            operation="op",
            required_permissions=("r",),
        )
        with pytest.raises(InputValidationError):
            policy_engine.register_policy(policy)

    def test_register_policy_empty_operation(
        self, policy_engine: PolicyEngine,
    ) -> None:
        policy = SecurityPolicy(
            policy_id="p1",
            description="D",
            operation="",
            required_permissions=("r",),
        )
        with pytest.raises(InputValidationError):
            policy_engine.register_policy(policy)

    def test_register_policy_empty_permissions(
        self, policy_engine: PolicyEngine,
    ) -> None:
        policy = SecurityPolicy(
            policy_id="p1",
            description="D",
            operation="op",
            required_permissions=(),
        )
        with pytest.raises(InputValidationError):
            policy_engine.register_policy(policy)

    def test_unregister_policy(self, policy_engine: PolicyEngine) -> None:
        policy = SecurityPolicy(
            policy_id="pol_001",
            description="Read",
            operation="runtime.read",
            required_permissions=("runtime.read",),
        )
        policy_engine.register_policy(policy)
        assert policy_engine.unregister_policy("pol_001")
        assert policy_engine.get_policy("pol_001") is None

    def test_unregister_nonexistent(
        self, policy_engine: PolicyEngine,
    ) -> None:
        assert not policy_engine.unregister_policy("nonexistent")

    def test_get_policy_for_operation(
        self, policy_engine: PolicyEngine,
    ) -> None:
        policy = SecurityPolicy(
            policy_id="pol_001",
            description="Read",
            operation="runtime.read",
            required_permissions=("runtime.read",),
        )
        policy_engine.register_policy(policy)
        found = policy_engine.get_policy_for_operation("runtime.read")
        assert found is not None
        assert found.policy_id == "pol_001"

    def test_get_policy_for_unknown_operation(
        self, policy_engine: PolicyEngine,
    ) -> None:
        assert policy_engine.get_policy_for_operation("unknown") is None

    def test_get_all_policies(self, policy_engine: PolicyEngine) -> None:
        p1 = SecurityPolicy(
            policy_id="p1", description="D", operation="op1",
            required_permissions=("r1",),
        )
        p2 = SecurityPolicy(
            policy_id="p2", description="D", operation="op2",
            required_permissions=("r2",),
        )
        policy_engine.register_policy(p1)
        policy_engine.register_policy(p2)
        assert len(policy_engine.get_all_policies()) == 2

    def test_evaluate_allowed(
        self,
        permission_manager: PermissionManager,
        policy_engine: PolicyEngine,
        read_perm: Permission,
    ) -> None:
        permission_manager.grant_permission("agent_a", read_perm)
        policy = SecurityPolicy(
            policy_id="pol_001",
            description="Read",
            operation="runtime.read",
            required_permissions=("runtime.read",),
        )
        policy_engine.register_policy(policy)
        decision = policy_engine.evaluate("agent_a", "runtime.read")
        assert decision.allowed
        assert decision.policy_id == "pol_001"

    def test_evaluate_denied_missing_permission(
        self,
        policy_engine: PolicyEngine,
    ) -> None:
        policy = SecurityPolicy(
            policy_id="pol_001",
            description="Read",
            operation="runtime.read",
            required_permissions=("runtime.read",),
        )
        policy_engine.register_policy(policy)
        decision = policy_engine.evaluate("agent_a", "runtime.read")
        assert not decision.allowed
        assert "runtime.read" in decision.missing_permissions

    def test_evaluate_default_deny_no_policy(
        self, policy_engine: PolicyEngine,
    ) -> None:
        decision = policy_engine.evaluate("agent_a", "unregistered_op")
        assert not decision.allowed
        assert "Default Deny" in decision.reason

    def test_evaluate_disabled_policy(
        self,
        policy_engine: PolicyEngine,
    ) -> None:
        policy = SecurityPolicy(
            policy_id="pol_001",
            description="Read",
            operation="runtime.read",
            required_permissions=("runtime.read",),
            enabled=False,
        )
        policy_engine.register_policy(policy)
        decision = policy_engine.evaluate("agent_a", "runtime.read")
        assert decision.allowed
        assert "disabled" in decision.reason.lower()

    def test_evaluate_multiple_permissions(
        self,
        permission_manager: PermissionManager,
        policy_engine: PolicyEngine,
        read_perm: Permission,
        write_perm: Permission,
    ) -> None:
        permission_manager.grant_permission("agent_a", read_perm)
        policy = SecurityPolicy(
            policy_id="pol_001",
            description="ReadWrite",
            operation="runtime.readwrite",
            required_permissions=("runtime.read", "runtime.write"),
        )
        policy_engine.register_policy(policy)
        decision = policy_engine.evaluate("agent_a", "runtime.readwrite")
        assert not decision.allowed
        assert "runtime.write" in decision.missing_permissions

    def test_enforce_allowed(
        self,
        permission_manager: PermissionManager,
        policy_engine: PolicyEngine,
        read_perm: Permission,
    ) -> None:
        permission_manager.grant_permission("agent_a", read_perm)
        policy = SecurityPolicy(
            policy_id="pol_001",
            description="Read",
            operation="runtime.read",
            required_permissions=("runtime.read",),
        )
        policy_engine.register_policy(policy)
        decision = policy_engine.enforce("agent_a", "runtime.read")
        assert decision.allowed

    def test_enforce_denied_raises(
        self, policy_engine: PolicyEngine,
    ) -> None:
        policy = SecurityPolicy(
            policy_id="pol_001",
            description="Read",
            operation="runtime.read",
            required_permissions=("runtime.read",),
        )
        policy_engine.register_policy(policy)
        with pytest.raises(PermissionDeniedError):
            policy_engine.enforce("agent_a", "runtime.read")

    def test_enforce_default_deny_raises(
        self, policy_engine: PolicyEngine,
    ) -> None:
        with pytest.raises(PermissionDeniedError):
            policy_engine.enforce("agent_a", "no_such_operation")

    def test_evaluate_audit_on_denial(
        self,
        audit_log: AuditLog,
        permission_manager: PermissionManager,
    ) -> None:
        engine = PolicyEngine(
            permission_manager=permission_manager,
            audit_log=audit_log,
        )
        policy = SecurityPolicy(
            policy_id="pol_001",
            description="Read",
            operation="runtime.read",
            required_permissions=("runtime.read",),
        )
        engine.register_policy(policy)
        engine.evaluate("agent_a", "runtime.read")
        entries = audit_log.get_entries()
        violations = [
            e for e in entries if isinstance(e, SecurityViolationEvent)
        ]
        assert len(violations) >= 1
        assert violations[-1].violation_type == "policy_denied"

    def test_health_check_with_policies(
        self, policy_engine: PolicyEngine,
    ) -> None:
        policy = SecurityPolicy(
            policy_id="p1", description="D", operation="op",
            required_permissions=("r",),
        )
        policy_engine.register_policy(policy)
        assert policy_engine.check_health() == HealthStatus.HEALTHY

    def test_health_check_without_policies(
        self, policy_engine: PolicyEngine,
    ) -> None:
        assert policy_engine.check_health() == HealthStatus.DEGRADED

    def test_component_name(self, policy_engine: PolicyEngine) -> None:
        assert policy_engine.get_component_name() == "PolicyEngine"

    def test_evaluate_empty_principal(
        self, policy_engine: PolicyEngine,
    ) -> None:
        with pytest.raises(InputValidationError):
            policy_engine.evaluate("", "runtime.read")

    def test_evaluate_empty_operation(
        self, policy_engine: PolicyEngine,
    ) -> None:
        with pytest.raises(InputValidationError):
            policy_engine.evaluate("agent_a", "")

    def test_thread_safety_evaluation(
        self,
        permission_manager: PermissionManager,
        policy_engine: PolicyEngine,
        read_perm: Permission,
    ) -> None:
        permission_manager.grant_permission("agent_a", read_perm)
        policy = SecurityPolicy(
            policy_id="pol_001",
            description="Read",
            operation="runtime.read",
            required_permissions=("runtime.read",),
        )
        policy_engine.register_policy(policy)

        errors: list[str] = []

        def evaluate_repeatedly() -> None:
            for _ in range(50):
                try:
                    decision = policy_engine.evaluate(
                        "agent_a", "runtime.read",
                    )
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
