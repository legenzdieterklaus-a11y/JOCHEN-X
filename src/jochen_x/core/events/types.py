"""EventBus-specific exception types."""

from __future__ import annotations

from jochen_x.core.exceptions.base import JochenXError

__all__ = [
    "EventBusError",
    "EventPublishError",
]

COMPONENT_NAME = "EventBus"


class EventBusError(JochenXError):
    """Base exception for EventBus operations.

    Args:
        message: Human-readable error description.
        correlation_id: Correlation ID for cross-component tracing.
        component: Name of the component that raised the error.

    """

    def __init__(
        self,
        message: str,
        *,
        correlation_id: str = "",
        component: str = COMPONENT_NAME,
    ) -> None:
        """Initialise with EventBus as default component."""
        super().__init__(
            message,
            correlation_id=correlation_id,
            component=component,
        )


class EventPublishError(EventBusError):
    """An event could not be published because the bus is not operational.

    Args:
        message: Human-readable error description.
        correlation_id: Correlation ID for cross-component tracing.
        component: Name of the component that raised the error.

    """
