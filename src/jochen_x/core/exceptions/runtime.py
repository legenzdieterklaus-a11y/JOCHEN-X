"""Runtime-specific exceptions."""

from __future__ import annotations

from jochen_x.core.exceptions.base import JochenXError

__all__ = [
    "RuntimeHostError",
    "RuntimeShutdownError",
    "RuntimeStartError",
    "RuntimeStateError",
]


class RuntimeHostError(JochenXError):
    """General runtime host error.

    Args:
        message: Human-readable error description.
        correlation_id: Correlation ID for cross-component tracing.
        component: Name of the component that raised the error.

    """


class RuntimeStartError(RuntimeHostError):
    """The runtime failed to start.

    Args:
        message: Human-readable error description.
        correlation_id: Correlation ID for cross-component tracing.
        component: Name of the component that raised the error.

    """


class RuntimeShutdownError(RuntimeHostError):
    """An error occurred during runtime shutdown.

    Args:
        message: Human-readable error description.
        correlation_id: Correlation ID for cross-component tracing.
        component: Name of the component that raised the error.

    """


class RuntimeStateError(RuntimeHostError):
    """The runtime is in an unexpected state for the requested operation.

    Args:
        message: Human-readable error description.
        correlation_id: Correlation ID for cross-component tracing.
        component: Name of the component that raised the error.

    """
