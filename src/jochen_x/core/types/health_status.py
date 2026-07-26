"""Health status definitions for runtime component monitoring."""

from __future__ import annotations

from enum import Enum, unique

__all__ = ["HealthStatus"]


@unique
class HealthStatus(Enum):
    """Health status values for runtime components.

    Every runtime component exposes a health status.  The health
    monitor aggregates individual statuses into an overall system
    health.

    Attributes:
        HEALTHY: Component is operating normally.
        DEGRADED: Component is operational but experiencing issues.
        UNHEALTHY: Component is not functioning correctly.
        UNKNOWN: Health status has not been determined yet.

    """

    HEALTHY = "HEALTHY"
    DEGRADED = "DEGRADED"
    UNHEALTHY = "UNHEALTHY"
    UNKNOWN = "UNKNOWN"
