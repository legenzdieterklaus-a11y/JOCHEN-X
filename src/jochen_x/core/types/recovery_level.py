"""Recovery level definitions for the escalation hierarchy."""

from __future__ import annotations

from enum import Enum, unique

__all__ = ["RecoveryLevel"]


@unique
class RecoveryLevel(Enum):
    """Recovery escalation levels, ordered from least to most impactful.

    Recovery automatically escalates through these levels when lower
    levels fail to resolve the issue.  Each level has configurable
    retry counts and cooldown periods.

    Attributes:
        COMPONENT_RETRY: Retry the failed operation within the component.
        COMPONENT_RESTART: Restart the affected component.
        SERVICE_RESTART: Restart the entire service group.
        RUNTIME_RESTART: Full runtime restart.

    """

    COMPONENT_RETRY = 1
    COMPONENT_RESTART = 2
    SERVICE_RESTART = 3
    RUNTIME_RESTART = 4
