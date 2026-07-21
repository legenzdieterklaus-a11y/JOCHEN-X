"""Broker access authorization preparation for the Security Foundation.

:class:`BrokerSecurity` prepares the security perimeter around broker access. It
does not talk to any broker API; it only registers broker access requirements
and validates, via the :class:`~app.security.permission_manager.PermissionManager`,
that a principal is authorized before a future integration layer would connect.
This keeps authorization decisions centralized and broker integrations thin.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from threading import RLock

from app.events import EventPublisher
from app.security.events import BrokerAuthenticated
from app.security.exceptions import BrokerSecurityError
from app.security.models import Permission
from app.security.permission_manager import PermissionManager

_LOGGER_NAME = "jochen_x.security.broker"


@dataclass(frozen=True, slots=True)
class BrokerAccessPolicy:
    """Immutable policy describing what a broker access requires.

    Attributes:
        broker: Stable broker identifier.
        required_permission: Permission a principal must hold to authenticate.
    """

    broker: str
    required_permission: Permission


class BrokerSecurity:
    """Thread-safe registry and authorizer for prepared broker accesses."""

    def __init__(
        self,
        permissions: PermissionManager,
        events: EventPublisher,
        *,
        logger: logging.Logger | None = None,
    ) -> None:
        """Create an empty broker security registry.

        Args:
            permissions: Authorization authority consulted before authentication.
            events: Publisher port used to broadcast broker events.
            logger: Optional logger for diagnostics.
        """
        self._permissions = permissions
        self._events = events
        self._logger = logger or logging.getLogger(_LOGGER_NAME)
        self._policies: dict[str, BrokerAccessPolicy] = {}
        self._lock = RLock()

    def register_broker(self, broker: str, *, required_permission: Permission) -> BrokerAccessPolicy:
        """Register the access policy required for a broker.

        Args:
            broker: Stable broker identifier.
            required_permission: Permission required to authenticate to the broker.

        Returns:
            The registered :class:`BrokerAccessPolicy`.

        Raises:
            ValueError: If ``broker`` is empty.
        """
        if not broker:
            raise ValueError("Broker identifier must be a non-empty string")
        policy = BrokerAccessPolicy(broker=broker, required_permission=required_permission)
        with self._lock:
            self._policies[broker] = policy
        self._logger.info("broker.registered", extra={"context": {"broker": broker}})
        return policy

    def authenticate(self, broker: str, identity_id: str) -> bool:
        """Authorize ``identity_id`` for ``broker`` and emit the result.

        This performs authorization only; establishing an actual broker
        connection is intentionally out of scope for this phase.

        Args:
            broker: Identifier of a previously registered broker.
            identity_id: Identifier of the principal requesting access.

        Returns:
            ``True`` when authorization succeeds.

        Raises:
            BrokerSecurityError: If the broker is unknown or the principal is
                not authorized.
        """
        with self._lock:
            policy = self._policies.get(broker)
        if policy is None:
            raise BrokerSecurityError(f"Unknown broker: {broker}")
        if not self._permissions.has_permission(identity_id, policy.required_permission):
            raise BrokerSecurityError(
                f"Identity '{identity_id}' is not authorized for broker '{broker}'"
            )
        self._logger.info(
            "broker.authenticated", extra={"context": {"broker": broker, "identity": identity_id}}
        )
        BrokerAuthenticated(broker, identity_id).publish(self._events)
        return True

    def brokers(self) -> tuple[str, ...]:
        """Return the identifiers of all registered brokers."""
        with self._lock:
            return tuple(sorted(self._policies))
