"""Health monitoring system for runtime component observation.

The ``HealthMonitor`` aggregates health checks from all registered
runtime components, emits ``HealthStatusChangedEvent`` when a
component's status changes, and computes an overall system health
status.

All operations are thread-safe.
"""

from __future__ import annotations

from threading import RLock

from jochen_x.core.exceptions.security import InputValidationError
from jochen_x.core.interfaces.health import IHealthCheck
from jochen_x.core.types.events import HealthStatusChangedEvent
from jochen_x.core.types.health_status import HealthStatus

__all__ = ["HealthMonitor"]

_COMPONENT_NAME = "HealthMonitor"
_FIELD_NAME = "name"
_FIELD_CHECK = "check"
_REASON_EMPTY_NAME = "Component name must not be empty"
_REASON_ALREADY_REGISTERED = "Component '{name}' is already registered"
_REASON_NOT_REGISTERED = "Component '{name}' is not registered"

_SEVERITY_ORDER: dict[HealthStatus, int] = {
    HealthStatus.HEALTHY: 0,
    HealthStatus.UNKNOWN: 1,
    HealthStatus.DEGRADED: 2,
    HealthStatus.UNHEALTHY: 3,
}


class HealthMonitor:
    """Central health monitoring system for the runtime.

    Maintains a registry of health-check providers and their last
    known status.  When ``run_checks`` is called the monitor invokes
    every registered health check, detects status changes, and
    returns a list of ``HealthStatusChangedEvent`` for each change.

    The caller (typically the scheduler or runtime host) is
    responsible for publishing the returned events on the EventBus.

    Args:
        No arguments required.

    """

    def __init__(self) -> None:
        """Initialise an empty health monitor."""
        self._lock: RLock = RLock()
        self._checks: dict[str, IHealthCheck] = {}
        self._statuses: dict[str, HealthStatus] = {}

    # -- IHealthMonitor protocol ---------------------------------------------

    def register_check(self, name: str, check: IHealthCheck) -> None:
        """Register a health check for a named component.

        Args:
            name: Unique name for the component.
            check: Health check implementation to register.

        Raises:
            InputValidationError: If name is empty or already registered.

        """
        if not name:
            raise InputValidationError(
                _FIELD_NAME,
                _REASON_EMPTY_NAME,
                component=_COMPONENT_NAME,
            )

        with self._lock:
            if name in self._checks:
                raise InputValidationError(
                    _FIELD_NAME,
                    _REASON_ALREADY_REGISTERED.format(name=name),
                    component=_COMPONENT_NAME,
                )
            self._checks[name] = check
            self._statuses[name] = HealthStatus.UNKNOWN

    def unregister_check(self, name: str) -> None:
        """Unregister a health check.

        No-op if no check is registered under the given name.

        Args:
            name: Name of the component to unregister.

        """
        with self._lock:
            self._checks.pop(name, None)
            self._statuses.pop(name, None)

    def get_status(self, name: str) -> HealthStatus:
        """Return the last known health status of a component.

        Args:
            name: Name of the component.

        Returns:
            The component's last known health status.

        Raises:
            InputValidationError: If the component is not registered.

        """
        with self._lock:
            status = self._statuses.get(name)
            if status is None:
                raise InputValidationError(
                    _FIELD_NAME,
                    _REASON_NOT_REGISTERED.format(name=name),
                    component=_COMPONENT_NAME,
                )
            return status

    def get_overall_status(self) -> HealthStatus:
        """Return the aggregated health status of all components.

        The overall status is the worst status among all registered
        components (UNHEALTHY > DEGRADED > UNKNOWN > HEALTHY).
        Returns ``HEALTHY`` when no components are registered.

        Returns:
            The aggregated health status.

        """
        with self._lock:
            if not self._statuses:
                return HealthStatus.HEALTHY
            return max(
                self._statuses.values(),
                key=lambda s: _SEVERITY_ORDER[s],
            )

    # -- Execution -----------------------------------------------------------

    def run_checks(self) -> list[HealthStatusChangedEvent]:
        """Execute all registered health checks and detect changes.

        Each check is invoked and its result compared to the last
        known status.  A ``HealthStatusChangedEvent`` is created for
        every status change.

        Returns:
            A list of events for all detected status changes.

        """
        with self._lock:
            snapshot = dict(self._checks)
            old_statuses = dict(self._statuses)

        events: list[HealthStatusChangedEvent] = []

        for name, check in snapshot.items():
            try:
                new_status = check.check_health()
            except Exception:  # noqa: BLE001
                new_status = HealthStatus.UNHEALTHY

            old_status = old_statuses.get(name, HealthStatus.UNKNOWN)

            if new_status != old_status:
                events.append(
                    HealthStatusChangedEvent(
                        component_name=name,
                        old_status=old_status,
                        new_status=new_status,
                        source=_COMPONENT_NAME,
                    ),
                )

            with self._lock:
                if name in self._statuses:
                    self._statuses[name] = new_status

        return events

    # -- Introspection -------------------------------------------------------

    def get_all_statuses(self) -> dict[str, HealthStatus]:
        """Return a snapshot of all component health statuses.

        Returns:
            A mapping of component names to their last known status.

        """
        with self._lock:
            return dict(self._statuses)

    def get_registered_components(self) -> list[str]:
        """Return the names of all registered components.

        Returns:
            A list of registered component names.

        """
        with self._lock:
            return list(self._checks.keys())

    def check_health(self) -> HealthStatus:
        """Return the overall health status of the monitor itself.

        Returns:
            The aggregated health status.

        """
        return self.get_overall_status()

    def get_component_name(self) -> str:
        """Return the component name of this monitor.

        Returns:
            The string ``"HealthMonitor"``.

        """
        return _COMPONENT_NAME
