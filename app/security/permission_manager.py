"""Role-based access control for the Security Foundation.

:class:`PermissionManager` owns the mapping of roles to permissions and of
identities to roles, and answers authorization questions. It is the single place
access decisions are made, keeping every other component free of authorization
logic. Each decision emits a typed event so observers (such as the threat
detector and audit logger) never need to poll.
"""

from __future__ import annotations

import logging
from collections.abc import Iterable
from threading import RLock

from app.events import EventPublisher
from app.security.events import PermissionDenied, PermissionGranted
from app.security.exceptions import PermissionDeniedError
from app.security.models import Permission

_LOGGER_NAME = "jochen_x.security.permissions"


class PermissionManager:
    """Thread-safe role and permission registry with event-emitting checks."""

    def __init__(self, events: EventPublisher, *, logger: logging.Logger | None = None) -> None:
        """Create an empty permission manager.

        Args:
            events: Publisher port used to broadcast authorization decisions.
            logger: Optional logger for diagnostics.
        """
        self._events = events
        self._logger = logger or logging.getLogger(_LOGGER_NAME)
        self._roles: dict[str, frozenset[Permission]] = {}
        self._assignments: dict[str, set[str]] = {}
        self._lock = RLock()

    def define_role(self, role: str, permissions: Iterable[Permission]) -> None:
        """Define or replace ``role`` with the given set of permissions.

        Args:
            role: Stable role name.
            permissions: The permissions the role grants.

        Raises:
            ValueError: If ``role`` is empty.
        """
        if not role:
            raise ValueError("Role name must be a non-empty string")
        with self._lock:
            self._roles[role] = frozenset(permissions)
        self._logger.info("permissions.role_defined", extra={"context": {"role": role}})

    def assign_role(self, identity_id: str, role: str) -> None:
        """Assign ``role`` to ``identity_id``.

        Args:
            identity_id: Identifier of the principal receiving the role.
            role: A previously defined role name.

        Raises:
            KeyError: If ``role`` has not been defined.
        """
        with self._lock:
            if role not in self._roles:
                raise KeyError(f"Undefined role: {role}")
            self._assignments.setdefault(identity_id, set()).add(role)
        self._logger.info(
            "permissions.role_assigned", extra={"context": {"identity": identity_id, "role": role}}
        )

    def revoke_role(self, identity_id: str, role: str) -> None:
        """Remove ``role`` from ``identity_id`` if present."""
        with self._lock:
            roles = self._assignments.get(identity_id)
            if roles is not None:
                roles.discard(role)
        self._logger.info(
            "permissions.role_revoked", extra={"context": {"identity": identity_id, "role": role}}
        )

    def roles_of(self, identity_id: str) -> frozenset[str]:
        """Return the set of roles currently assigned to ``identity_id``."""
        with self._lock:
            return frozenset(self._assignments.get(identity_id, set()))

    def permissions_of(self, identity_id: str) -> frozenset[Permission]:
        """Return the union of permissions granted by ``identity_id``'s roles."""
        with self._lock:
            granted: set[Permission] = set()
            for role in self._assignments.get(identity_id, set()):
                granted.update(self._roles.get(role, frozenset()))
            return frozenset(granted)

    def has_permission(self, identity_id: str, permission: Permission) -> bool:
        """Check ``permission`` for ``identity_id`` and emit the decision event.

        Args:
            identity_id: Identifier of the principal being checked.
            permission: The capability being requested.

        Returns:
            ``True`` if the identity holds the permission, otherwise ``False``.
        """
        granted = permission in self.permissions_of(identity_id)
        if granted:
            PermissionGranted(identity_id, permission.name).publish(self._events)
        else:
            PermissionDenied(identity_id, permission.name).publish(self._events)
        return granted

    def require(self, identity_id: str, permission: Permission) -> None:
        """Enforce ``permission`` for ``identity_id``.

        Args:
            identity_id: Identifier of the principal being checked.
            permission: The capability being required.

        Raises:
            PermissionDeniedError: If the identity does not hold the permission.
        """
        if not self.has_permission(identity_id, permission):
            raise PermissionDeniedError(
                f"Identity '{identity_id}' lacks permission '{permission.name}'"
            )
