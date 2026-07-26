"""Security policy engine for declarative permission enforcement.

The ``PolicyEngine`` provides declarative security rule definitions
and evaluation.  Policies map operations to required permissions,
enabling centralised security configuration rather than scattered
permission checks in application code.

The engine follows Default Deny: if no policy exists for an
operation, the operation is denied.  All policy evaluations are
audited and security violations are published through the event bus.

All operations are thread-safe.
"""

from __future__ import annotations

import contextlib
from collections.abc import Sequence
from dataclasses import dataclass, field
from datetime import UTC, datetime
from threading import RLock
from typing import TYPE_CHECKING

from jochen_x.core.exceptions.base import JochenXError
from jochen_x.core.exceptions.security import (
    InputValidationError,
    PermissionDeniedError,
)
from jochen_x.core.types.events import SecurityViolationEvent
from jochen_x.core.types.health_status import HealthStatus

if TYPE_CHECKING:
    from jochen_x.core.interfaces.audit import IAuditLog
    from jochen_x.core.interfaces.event_bus import IEventBus
    from jochen_x.core.interfaces.logging import ILogger
    from jochen_x.core.security.permissions import PermissionManager

__all__ = [
    "PolicyDecision",
    "PolicyEngine",
    "SecurityPolicy",
]

_COMPONENT_NAME = "PolicyEngine"

_FIELD_POLICY = "policy"
_FIELD_POLICY_ID = "policy_id"
_FIELD_OPERATION = "operation"
_FIELD_PRINCIPAL = "principal"
_FIELD_REQUIRED_PERMISSIONS = "required_permissions"

_REASON_EMPTY = "must not be empty"
_REASON_NOT_STRING = "must be a string"
_REASON_NOT_POLICY = "must be a SecurityPolicy instance"
_REASON_DUPLICATE_POLICY = "policy with this ID is already registered"
_REASON_EMPTY_PERMISSIONS = "must contain at least one permission"


@dataclass(frozen=True, kw_only=True, slots=True)
class SecurityPolicy:
    """A declarative security policy mapping operations to permissions.

    Each policy defines which permissions are required for a given
    operation.  When the policy engine evaluates an operation, it
    checks the principal's grants against the required permissions.

    Args:
        policy_id: Unique identifier for the policy.
        description: Human-readable description of the policy.
        operation: The operation this policy governs.
        required_permissions: Permission names that must all be
            granted for the operation to be allowed.
        enabled: Whether the policy is currently active.

    """

    policy_id: str
    description: str
    operation: str
    required_permissions: tuple[str, ...]
    enabled: bool = True


@dataclass(frozen=True, kw_only=True, slots=True)
class PolicyDecision:
    """Result of a policy evaluation.

    Args:
        allowed: Whether the operation was allowed.
        policy_id: ID of the policy that governed the decision, or
            empty if no policy was found (Default Deny).
        reason: Human-readable explanation of the decision.
        principal: The principal whose access was evaluated.
        operation: The operation that was evaluated.
        missing_permissions: Permissions the principal lacked (empty
            if allowed).
        evaluated_at: UTC timestamp of the evaluation.

    """

    allowed: bool
    policy_id: str = ""
    reason: str = ""
    principal: str = ""
    operation: str = ""
    missing_permissions: tuple[str, ...] = ()
    evaluated_at: datetime = field(default_factory=lambda: datetime.now(UTC))


class PolicyEngine:
    """Evaluates security policies for declarative permission enforcement.

    Policies are registered with the engine and map operations to
    required permissions.  When an operation is evaluated, the engine
    looks up the applicable policy and checks the principal's
    permissions via the ``PermissionManager``.

    Default Deny: if no policy is registered for an operation, the
    operation is denied.

    Implements the ``IHealthCheck`` protocol.

    Args:
        permission_manager: The permission manager for checking grants.
        audit_log: Audit log for recording policy evaluations.
        event_bus: Event bus for publishing security events.
        logger: Logger for policy-related log messages.

    """

    def __init__(
        self,
        *,
        permission_manager: PermissionManager,
        audit_log: IAuditLog | None = None,
        event_bus: IEventBus | None = None,
        logger: ILogger | None = None,
    ) -> None:
        """Initialise the policy engine."""
        self._lock: RLock = RLock()
        self._policies: dict[str, SecurityPolicy] = {}
        self._operation_index: dict[str, str] = {}
        self._permission_manager: PermissionManager = permission_manager
        self._audit_log: IAuditLog | None = audit_log
        self._event_bus: IEventBus | None = event_bus
        self._logger: ILogger | None = logger

    # -- Policy Registration ---------------------------------------------------

    def register_policy(self, policy: SecurityPolicy) -> None:
        """Register a security policy.

        Args:
            policy: The policy to register.

        Raises:
            InputValidationError: If the policy is invalid or a
                policy with the same ID is already registered.

        """
        self._validate_policy(policy)

        with self._lock:
            if policy.policy_id in self._policies:
                raise InputValidationError(
                    _FIELD_POLICY_ID,
                    _REASON_DUPLICATE_POLICY,
                    component=_COMPONENT_NAME,
                )
            self._policies[policy.policy_id] = policy
            self._operation_index[policy.operation] = policy.policy_id

        self._log_info(
            f"Policy registered: {policy.policy_id} "
            f"for operation '{policy.operation}'"
        )

    def unregister_policy(self, policy_id: str) -> bool:
        """Unregister a security policy.

        Args:
            policy_id: ID of the policy to unregister.

        Returns:
            ``True`` if the policy was unregistered, ``False`` if it
            was not found.

        Raises:
            InputValidationError: If policy_id is empty or not a
                string.

        """
        _validate_non_empty_string(policy_id, _FIELD_POLICY_ID)

        with self._lock:
            policy = self._policies.pop(policy_id, None)
            if policy is None:
                return False
            self._operation_index.pop(policy.operation, None)

        self._log_info(f"Policy unregistered: {policy_id}")
        return True

    def get_policy(self, policy_id: str) -> SecurityPolicy | None:
        """Retrieve a policy by its ID.

        Args:
            policy_id: ID of the policy to retrieve.

        Returns:
            The policy, or ``None`` if not found.

        Raises:
            InputValidationError: If policy_id is empty or not a
                string.

        """
        _validate_non_empty_string(policy_id, _FIELD_POLICY_ID)

        with self._lock:
            return self._policies.get(policy_id)

    def get_policy_for_operation(
        self,
        operation: str,
    ) -> SecurityPolicy | None:
        """Retrieve the policy governing an operation.

        Args:
            operation: The operation to look up.

        Returns:
            The governing policy, or ``None`` if none is registered.

        Raises:
            InputValidationError: If operation is empty or not a
                string.

        """
        _validate_non_empty_string(operation, _FIELD_OPERATION)

        with self._lock:
            policy_id = self._operation_index.get(operation)
            if policy_id is None:
                return None
            return self._policies.get(policy_id)

    def get_all_policies(self) -> Sequence[SecurityPolicy]:
        """Return all registered policies.

        Returns:
            A sequence of all registered policies.

        """
        with self._lock:
            return list(self._policies.values())

    # -- Policy Evaluation -----------------------------------------------------

    def evaluate(
        self,
        principal: str,
        operation: str,
    ) -> PolicyDecision:
        """Evaluate whether a principal may perform an operation.

        Default Deny: if no policy is registered for the operation,
        the decision is ``allowed=False``.  If a policy exists but is
        disabled, the operation is allowed (policy bypass for
        maintenance).

        Args:
            principal: The principal requesting the operation.
            operation: The operation to evaluate.

        Returns:
            A ``PolicyDecision`` recording the outcome.

        Raises:
            InputValidationError: If principal or operation is empty
                or not a string.

        """
        _validate_non_empty_string(principal, _FIELD_PRINCIPAL)
        _validate_non_empty_string(operation, _FIELD_OPERATION)

        policy = self.get_policy_for_operation(operation)

        if policy is None:
            decision = PolicyDecision(
                allowed=False,
                reason="No policy registered for operation (Default Deny)",
                principal=principal,
                operation=operation,
            )
            self._record_denial(decision)
            return decision

        if not policy.enabled:
            return PolicyDecision(
                allowed=True,
                policy_id=policy.policy_id,
                reason="Policy is disabled",
                principal=principal,
                operation=operation,
            )

        missing = [
            perm_name
            for perm_name in policy.required_permissions
            if not self._permission_manager.check_permission(
                principal, perm_name
            )
        ]

        if missing:
            decision = PolicyDecision(
                allowed=False,
                policy_id=policy.policy_id,
                reason=(
                    f"Missing permissions: {', '.join(missing)}"
                ),
                principal=principal,
                operation=operation,
                missing_permissions=tuple(missing),
            )
            self._record_denial(decision)
            return decision

        return PolicyDecision(
            allowed=True,
            policy_id=policy.policy_id,
            reason="All required permissions granted",
            principal=principal,
            operation=operation,
        )

    def enforce(
        self,
        principal: str,
        operation: str,
    ) -> PolicyDecision:
        """Evaluate and enforce a policy decision.

        Like ``evaluate``, but raises ``PermissionDeniedError`` if
        the operation is denied.

        Args:
            principal: The principal requesting the operation.
            operation: The operation to evaluate.

        Returns:
            The ``PolicyDecision`` (only returned when allowed).

        Raises:
            PermissionDeniedError: If the operation is denied.
            InputValidationError: If principal or operation is empty
                or not a string.

        """
        decision = self.evaluate(principal, operation)

        if not decision.allowed:
            required = ""
            if decision.missing_permissions:
                required = decision.missing_permissions[0]
            elif decision.policy_id:
                required = f"policy:{decision.policy_id}"
            else:
                required = f"policy_for:{operation}"

            raise PermissionDeniedError(
                operation,
                required,
                component=_COMPONENT_NAME,
            )

        return decision

    # -- IHealthCheck protocol -------------------------------------------------

    def check_health(self) -> HealthStatus:
        """Return the health status of the policy engine.

        Returns:
            ``HealthStatus.HEALTHY`` if policies are registered,
            ``HealthStatus.DEGRADED`` if no policies are configured.

        """
        with self._lock:
            if self._policies:
                return HealthStatus.HEALTHY
            return HealthStatus.DEGRADED

    def get_component_name(self) -> str:
        """Return the component name.

        Returns:
            The string ``"PolicyEngine"``.

        """
        return _COMPONENT_NAME

    # -- Internal Helpers ------------------------------------------------------

    def _validate_policy(self, policy: SecurityPolicy) -> None:
        """Validate a ``SecurityPolicy`` instance."""
        if not isinstance(policy, SecurityPolicy):
            raise InputValidationError(
                _FIELD_POLICY,
                _REASON_NOT_POLICY,
                component=_COMPONENT_NAME,
            )
        if not policy.policy_id:
            raise InputValidationError(
                _FIELD_POLICY_ID,
                _REASON_EMPTY,
                component=_COMPONENT_NAME,
            )
        if not policy.operation:
            raise InputValidationError(
                _FIELD_OPERATION,
                _REASON_EMPTY,
                component=_COMPONENT_NAME,
            )
        if not policy.required_permissions:
            raise InputValidationError(
                _FIELD_REQUIRED_PERMISSIONS,
                _REASON_EMPTY_PERMISSIONS,
                component=_COMPONENT_NAME,
            )

    def _record_denial(self, decision: PolicyDecision) -> None:
        """Log, audit, and publish a policy denial."""
        details = (
            f"Policy denied: principal='{decision.principal}', "
            f"operation='{decision.operation}', "
            f"reason='{decision.reason}'"
        )

        if self._logger is not None:
            self._logger.warning(details, component=_COMPONENT_NAME)

        self._audit_security_event(details, "policy_denied")
        self._publish_violation("policy_denied", details)

    def _audit_security_event(
        self,
        details: str,
        violation_type: str,
    ) -> None:
        """Record a security event in the audit log."""
        if self._audit_log is None:
            return
        event = SecurityViolationEvent(
            violation_type=violation_type,
            details=details,
            component_name=_COMPONENT_NAME,
            source=_COMPONENT_NAME,
        )
        with contextlib.suppress(JochenXError):
            self._audit_log.record(event)

    def _publish_violation(self, violation_type: str, details: str) -> None:
        """Publish a security violation event."""
        if self._event_bus is None:
            return
        event = SecurityViolationEvent(
            violation_type=violation_type,
            details=details,
            component_name=_COMPONENT_NAME,
            source=_COMPONENT_NAME,
        )
        with contextlib.suppress(JochenXError):
            self._event_bus.publish(event)

    def _log_info(self, message: str) -> None:
        """Emit an INFO log entry."""
        if self._logger is not None:
            self._logger.info(message, component=_COMPONENT_NAME)


def _validate_non_empty_string(value: str, field_name: str) -> None:
    """Validate that *value* is a non-empty string."""
    if not isinstance(value, str):
        raise InputValidationError(
            field_name,
            _REASON_NOT_STRING,
            component=_COMPONENT_NAME,
        )
    if not value:
        raise InputValidationError(
            field_name,
            _REASON_EMPTY,
            component=_COMPONENT_NAME,
        )
