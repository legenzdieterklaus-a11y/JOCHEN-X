"""Lifecycle-specific exceptions for illegal state transitions."""

from __future__ import annotations

from jochen_x.core.exceptions.base import JochenXError
from jochen_x.core.types.runtime_state import RuntimeState

__all__ = [
    "IllegalStateTransitionError",
    "LifecycleError",
]


class LifecycleError(JochenXError):
    """General lifecycle management error.

    Args:
        message: Human-readable error description.
        correlation_id: Correlation ID for cross-component tracing.
        component: Name of the component that raised the error.

    """


class IllegalStateTransitionError(LifecycleError):
    """An illegal state transition was attempted.

    Args:
        from_state: The current state.
        to_state: The requested (illegal) target state.
        correlation_id: Correlation ID for cross-component tracing.
        component: Name of the component that raised the error.

    """

    def __init__(
        self,
        from_state: RuntimeState,
        to_state: RuntimeState,
        *,
        correlation_id: str = "",
        component: str = "",
    ) -> None:
        """Initialise with the illegal state transition details."""
        self.from_state: RuntimeState = from_state
        self.to_state: RuntimeState = to_state
        super().__init__(
            f"Illegal state transition: {from_state.value} -> {to_state.value}",
            correlation_id=correlation_id,
            component=component,
        )
