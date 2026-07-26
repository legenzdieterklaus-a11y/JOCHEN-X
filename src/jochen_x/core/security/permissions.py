"""Permission system implementing Default Deny and Least Privilege.

The ``PermissionManager`` maintains a mapping of principals (identified
by string names) to their granted permissions.  Every permission check
follows Default Deny semantics: an operation is denied unless an
explicit grant exists for the requesting principal.

All operations are thread-safe.  Permission changes are audited and
published as security events through the event bus.
"""

from __future__ import annotations

import contextlib
import re
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

__all__ = [
    "Permission",
    "PermissionGrant",
    "PermissionManager",
    "PermissionSet",
]

_COMPONENT_NAME = "PermissionManager"
_PERMISSION_NAME_PATTERN = re.compile(r"^[a-z][a-z0-9_.]*$")
_PRINCIPAL_NAME_PATTERN = re.compile(r"^[a-zA-Z][a-zA-Z0-9_.\-]*$")

_FIELD_PERMISSION = "permission"
_FIELD_PRINCIPAL = "principal"
_FIELD_NAME = "name"
_FIELD_PERMISSION_NAME = "permission_name"

_REASON_EMPTY = "must not be empty"
_REASON_NOT_STRING = "must be a string"
_REASON_INVALID_PERMISSION_FORMAT = (
    "must start with lowercase letter, contain only [a-z0-9_.]"
)
_REASON_INVALID_PRINCIPAL_FORMAT = (
    "must start with a letter, contain only [a-zA-Z0-9_.-]"
)
_REASON_NOT_PERMISSION = "must be a Permission instance"


@dataclass(frozen=True, kw_only=True, slots=True)
class Permission:
    """A named permission that can be granted to principals.

    Args:
        name: Unique permission identifier (lowercase, dots and
            underscores allowed, e.g. ``runtime.start``).
        description: Human-readable description of the permission.

    """

    name: str
    description: str = ""


@dataclass(frozen=True, kw_only=True, slots=True)
class PermissionGrant:
    """Record of a permission granted to a principal.

    Args:
        principal: Identifier of the entity that received the grant.
        permission: The granted permission.
        granted_at: UTC timestamp of when the grant was created.
        granted_by: Identifier of who created the grant.

    """

    principal: str
    permission: Permission
    granted_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    granted_by: str = ""


class PermissionSet:
    """Thread-safe collection of permissions.

    Provides set-like operations for managing collections of
    ``Permission`` objects, keyed by their name.
    """

    def __init__(self) -> None:
        """Initialise an empty permission set."""
        self._lock: RLock = RLock()
        self._permissions: dict[str, Permission] = {}

    def add(self, permission: Permission) -> None:
        """Add a permission to the set.

        Args:
            permission: The permission to add.

        """
        with self._lock:
            self._permissions[permission.name] = permission

    def remove(self, permission_name: str) -> bool:
        """Remove a permission by name.

        Args:
            permission_name: Name of the permission to remove.

        Returns:
            ``True`` if the permission was removed, ``False`` if it
            was not present.

        """
        with self._lock:
            return self._permissions.pop(permission_name, None) is not None

    def contains(self, permission_name: str) -> bool:
        """Check if a permission exists in the set.

        Args:
            permission_name: Name of the permission to check.

        Returns:
            ``True`` if the permission is present.

        """
        with self._lock:
            return permission_name in self._permissions

    def get_all(self) -> Sequence[Permission]:
        """Return all permissions in the set.

        Returns:
            A list of all permissions, in no particular order.

        """
        with self._lock:
            return list(self._permissions.values())

    def clear(self) -> None:
        """Remove all permissions from the set."""
        with self._lock:
            self._permissions.clear()

    def size(self) -> int:
        """Return the number of permissions in the set.

        Returns:
            The permission count.

        """
        with self._lock:
            return len(self._permissions)


class PermissionManager:
    """Manages permission grants with Default Deny semantics.

    Every permission check returns ``False`` (denied) unless an
    explicit grant exists.  All permission changes are recorded in
    the audit log and published as security events.

    Implements the ``IHealthCheck`` protocol.

    Args:
        audit_log: Audit log for recording permission events.
        event_bus: Event bus for publishing security events.
        logger: Logger for security-related log messages.

    """

    def __init__(
        self,
        *,
        audit_log: IAuditLog | None = None,
        event_bus: IEventBus | None = None,
        logger: ILogger | None = None,
    ) -> None:
        """Initialise the permission manager."""
        self._lock: RLock = RLock()
        self._grants: dict[str, PermissionSet] = {}
        self._registered_permissions: dict[str, Permission] = {}
        self._audit_log: IAuditLog | None = audit_log
        self._event_bus: IEventBus | None = event_bus
        self._logger: ILogger | None = logger

    # -- Permission Registration -----------------------------------------------

    def register_permission(self, permission: Permission) -> None:
        """Register a permission that can be granted.

        Args:
            permission: The permission to register.

        Raises:
            InputValidationError: If the permission is invalid.

        """
        self._validate_permission_object(permission)
        with self._lock:
            self._registered_permissions[permission.name] = permission
        self._log_info(f"Permission registered: {permission.name}")

    def unregister_permission(self, permission_name: str) -> None:
        """Unregister a permission and revoke all existing grants.

        Args:
            permission_name: Name of the permission to unregister.

        Raises:
            InputValidationError: If permission_name is empty or not
                a string.

        """
        _validate_non_empty_string(permission_name, _FIELD_PERMISSION_NAME)
        with self._lock:
            self._registered_permissions.pop(permission_name, None)
            for principal_grants in self._grants.values():
                principal_grants.remove(permission_name)
        self._log_info(f"Permission unregistered: {permission_name}")

    def get_registered_permissions(self) -> Sequence[Permission]:
        """Return all registered permissions.

        Returns:
            A sequence of all registered permissions.

        """
        with self._lock:
            return list(self._registered_permissions.values())

    # -- Grant Management ------------------------------------------------------

    def grant_permission(
        self,
        principal: str,
        permission: Permission,
        *,
        granted_by: str = "",
    ) -> PermissionGrant:
        """Grant a permission to a principal.

        Args:
            principal: The principal to grant the permission to.
            permission: The permission to grant.
            granted_by: Identifier of the grantor.

        Returns:
            The created permission grant record.

        Raises:
            InputValidationError: If principal or permission is invalid.

        """
        _validate_principal(principal)
        self._validate_permission_object(permission)

        grant = PermissionGrant(
            principal=principal,
            permission=permission,
            granted_by=granted_by,
        )

        with self._lock:
            if principal not in self._grants:
                self._grants[principal] = PermissionSet()
            self._grants[principal].add(permission)

        self._log_info(
            f"Permission '{permission.name}' granted to '{principal}'"
        )
        self._audit_security_event(
            f"Permission granted: {permission.name} -> {principal}",
            "permission_granted",
        )

        return grant

    def revoke_permission(self, principal: str, permission_name: str) -> bool:
        """Revoke a permission from a principal.

        Args:
            principal: The principal to revoke from.
            permission_name: Name of the permission to revoke.

        Returns:
            ``True`` if the permission was revoked, ``False`` if it
            was not granted.

        Raises:
            InputValidationError: If principal or permission_name is
                empty or not a string.

        """
        _validate_non_empty_string(principal, _FIELD_PRINCIPAL)
        _validate_non_empty_string(permission_name, _FIELD_PERMISSION_NAME)

        with self._lock:
            perm_set = self._grants.get(principal)
            if perm_set is None:
                return False
            removed = perm_set.remove(permission_name)

        if removed:
            self._log_info(
                f"Permission '{permission_name}' revoked from '{principal}'"
            )
            self._audit_security_event(
                f"Permission revoked: {permission_name} -> {principal}",
                "permission_revoked",
            )

        return removed

    def revoke_all(self, principal: str) -> None:
        """Revoke all permissions from a principal.

        Args:
            principal: The principal whose permissions to revoke.

        Raises:
            InputValidationError: If principal is empty or not a
                string.

        """
        _validate_non_empty_string(principal, _FIELD_PRINCIPAL)

        with self._lock:
            perm_set = self._grants.pop(principal, None)

        if perm_set is not None and perm_set.size() > 0:
            self._log_info(f"All permissions revoked from '{principal}'")
            self._audit_security_event(
                f"All permissions revoked from '{principal}'",
                "permissions_revoked_all",
            )

    # -- Permission Checking (Default Deny) ------------------------------------

    def check_permission(self, principal: str, permission_name: str) -> bool:
        """Check if a principal has a specific permission.

        Implements Default Deny: returns ``False`` unless an explicit
        grant exists.

        Args:
            principal: The principal to check.
            permission_name: The permission to check for.

        Returns:
            ``True`` if the principal has the permission, ``False``
            otherwise (Default Deny).

        Raises:
            InputValidationError: If principal or permission_name is
                empty or not a string.

        """
        _validate_non_empty_string(principal, _FIELD_PRINCIPAL)
        _validate_non_empty_string(permission_name, _FIELD_PERMISSION_NAME)

        with self._lock:
            perm_set = self._grants.get(principal)
            if perm_set is None:
                return False
            return perm_set.contains(permission_name)

    def require_permission(
        self,
        principal: str,
        permission_name: str,
        *,
        operation: str = "",
    ) -> None:
        """Require a principal to have a permission or raise.

        If the principal lacks the required permission, a security
        violation is logged, audited, and published before raising.

        Args:
            principal: The principal to check.
            permission_name: The required permission.
            operation: Description of the attempted operation (used
                in the error message).

        Raises:
            PermissionDeniedError: If the principal lacks the
                permission.
            InputValidationError: If principal or permission_name is
                empty or not a string.

        """
        if not self.check_permission(principal, permission_name):
            op = operation or f"access requiring '{permission_name}'"
            self._record_permission_denial(principal, permission_name, op)
            raise PermissionDeniedError(
                op,
                permission_name,
                component=_COMPONENT_NAME,
            )

    def get_permissions(self, principal: str) -> Sequence[Permission]:
        """Return all permissions granted to a principal.

        Args:
            principal: The principal to query.

        Returns:
            Sequence of granted permissions (empty if none).

        Raises:
            InputValidationError: If principal is empty or not a
                string.

        """
        _validate_non_empty_string(principal, _FIELD_PRINCIPAL)

        with self._lock:
            perm_set = self._grants.get(principal)
            if perm_set is None:
                return []
            return perm_set.get_all()

    def get_principals_with_permission(
        self,
        permission_name: str,
    ) -> Sequence[str]:
        """Return all principals that have a specific permission.

        Args:
            permission_name: The permission to query.

        Returns:
            Sequence of principal identifiers.

        Raises:
            InputValidationError: If permission_name is empty or not
                a string.

        """
        _validate_non_empty_string(permission_name, _FIELD_PERMISSION_NAME)

        result: list[str] = []
        with self._lock:
            for principal, perm_set in self._grants.items():
                if perm_set.contains(permission_name):
                    result.append(principal)
        return result

    # -- IHealthCheck protocol -------------------------------------------------

    def check_health(self) -> HealthStatus:
        """Return the health status of the permission manager.

        Returns:
            Always ``HealthStatus.HEALTHY`` as the permission manager
            has no degraded state.

        """
        return HealthStatus.HEALTHY

    def get_component_name(self) -> str:
        """Return the component name.

        Returns:
            The string ``"PermissionManager"``.

        """
        return _COMPONENT_NAME

    # -- Internal Helpers ------------------------------------------------------

    def _validate_permission_object(self, permission: Permission) -> None:
        """Validate a ``Permission`` instance."""
        if not isinstance(permission, Permission):
            raise InputValidationError(
                _FIELD_PERMISSION,
                _REASON_NOT_PERMISSION,
                component=_COMPONENT_NAME,
            )
        if not permission.name:
            raise InputValidationError(
                _FIELD_NAME,
                _REASON_EMPTY,
                component=_COMPONENT_NAME,
            )
        if not _PERMISSION_NAME_PATTERN.match(permission.name):
            raise InputValidationError(
                _FIELD_NAME,
                _REASON_INVALID_PERMISSION_FORMAT,
                component=_COMPONENT_NAME,
            )

    def _record_permission_denial(
        self,
        principal: str,
        permission_name: str,
        operation: str,
    ) -> None:
        """Log, audit, and publish a permission denial."""
        details = (
            f"Principal '{principal}' denied '{permission_name}' "
            f"for operation '{operation}'"
        )

        if self._logger is not None:
            self._logger.warning(details, component=_COMPONENT_NAME)

        self._audit_security_event(details, "permission_denied")
        self._publish_violation("permission_denied", details)

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


def _validate_principal(principal: str) -> None:
    """Validate a principal identifier."""
    _validate_non_empty_string(principal, _FIELD_PRINCIPAL)
    if not _PRINCIPAL_NAME_PATTERN.match(principal):
        raise InputValidationError(
            _FIELD_PRINCIPAL,
            _REASON_INVALID_PRINCIPAL_FORMAT,
            component=_COMPONENT_NAME,
        )
