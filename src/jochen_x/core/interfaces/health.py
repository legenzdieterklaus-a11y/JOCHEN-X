"""Health check and health monitoring protocols."""

from __future__ import annotations

from typing import Protocol, runtime_checkable

from jochen_x.core.types.health_status import HealthStatus

__all__ = ["IHealthCheck", "IHealthMonitor"]


@runtime_checkable
class IHealthCheck(Protocol):
    """Protocol for individual component health checks.

    Every runtime component implements this protocol to report its
    own health status.  The health monitor periodically invokes these
    checks and aggregates the results.
    """

    def check_health(self) -> HealthStatus:
        """Perform a health check and return the current status.

        Returns:
            The component's current health status.

        """
        ...

    def get_component_name(self) -> str:
        """Return the name of the component being checked.

        Returns:
            A unique component identifier.

        """
        ...


@runtime_checkable
class IHealthMonitor(Protocol):
    """Protocol for the centralised health monitoring system.

    The health monitor aggregates health checks from all registered
    components, runs periodic checks via the scheduler, and emits
    health-change events through the event bus.
    """

    def register_check(self, name: str, check: IHealthCheck) -> None:
        """Register a health check for a named component.

        Args:
            name: Unique name for the component.
            check: Health check implementation to register.

        Raises:
            InputValidationError: If name is empty or already registered.

        """
        ...

    def unregister_check(self, name: str) -> None:
        """Unregister a health check.

        No-op if no check is registered under the given name.

        Args:
            name: Name of the component to unregister.

        """
        ...

    def get_status(self, name: str) -> HealthStatus:
        """Return the last known health status of a component.

        Args:
            name: Name of the component.

        Returns:
            The component's last known health status.

        Raises:
            InputValidationError: If the component is not registered.

        """
        ...

    def get_overall_status(self) -> HealthStatus:
        """Return the aggregated health status of all components.

        The overall status is the worst status among all registered
        components (UNHEALTHY > DEGRADED > UNKNOWN > HEALTHY).

        Returns:
            The aggregated health status.

        """
        ...
