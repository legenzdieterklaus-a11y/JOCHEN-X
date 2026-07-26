"""Bootstrap failure exceptions."""

from __future__ import annotations

from jochen_x.core.exceptions.base import JochenXError

__all__ = [
    "BootstrapError",
    "BootstrapStepError",
]


class BootstrapError(JochenXError):
    """General bootstrap sequence failure.

    Args:
        message: Human-readable error description.
        correlation_id: Correlation ID for cross-component tracing.
        component: Name of the component that raised the error.

    """


class BootstrapStepError(BootstrapError):
    """A specific bootstrap step failed.

    Args:
        step_name: Name of the failed bootstrap step.
        step_index: Zero-based index of the step in the sequence.
        message: Human-readable error description.
        correlation_id: Correlation ID for cross-component tracing.
        component: Name of the component that raised the error.

    """

    def __init__(
        self,
        step_name: str,
        step_index: int,
        message: str,
        *,
        correlation_id: str = "",
        component: str = "",
    ) -> None:
        """Initialise with the failed step details."""
        self.step_name: str = step_name
        self.step_index: int = step_index
        super().__init__(
            f"Bootstrap step '{step_name}' (index {step_index}) failed: {message}",
            correlation_id=correlation_id,
            component=component,
        )
