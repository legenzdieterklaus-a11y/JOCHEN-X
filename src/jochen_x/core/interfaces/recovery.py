"""Recovery handler protocol for error recovery and escalation."""

from __future__ import annotations

from typing import Protocol, runtime_checkable

from jochen_x.core.types.recovery_level import RecoveryLevel

__all__ = ["IRecoveryHandler"]


@runtime_checkable
class IRecoveryHandler(Protocol):
    """Protocol for the recovery handling system.

    The recovery handler implements a multi-level escalation strategy.
    When a component fails, recovery starts at the lowest applicable
    level and automatically escalates when lower levels do not resolve
    the issue.

    Recovery levels (ascending): Component Retry -> Component Restart
    -> Service Restart -> Runtime Restart.

    Each recovery action is documented in the audit log.  A circuit
    breaker prevents thrashing between levels by enforcing configurable
    cooldown periods.
    """

    def handle_error(
        self,
        error: Exception,
        *,
        component: str = "",
        level: RecoveryLevel = RecoveryLevel.COMPONENT_RETRY,
    ) -> bool:
        """Handle an error at the specified recovery level.

        Args:
            error: The exception that triggered recovery.
            component: Name of the affected component.
            level: Recovery level to attempt.

        Returns:
            ``True`` if recovery succeeded, ``False`` if it failed
            and escalation is required.

        Raises:
            JochenXError: If recovery itself fails fatally.

        """
        ...

    def escalate(
        self,
        component: str,
        from_level: RecoveryLevel,
    ) -> RecoveryLevel:
        """Escalate to the next recovery level.

        Args:
            component: Name of the affected component.
            from_level: The current recovery level that failed.

        Returns:
            The next higher recovery level.

        Raises:
            JochenXError: If already at the highest level.

        """
        ...

    def reset(self, component: str) -> None:
        """Reset recovery state for a component after successful recovery.

        Args:
            component: Name of the recovered component.

        """
        ...
