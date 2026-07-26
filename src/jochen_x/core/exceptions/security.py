"""Security violation exceptions."""

from __future__ import annotations

from jochen_x.core.exceptions.base import JochenXError

__all__ = [
    "InputValidationError",
    "PermissionDeniedError",
    "SecurityViolationError",
]


class SecurityViolationError(JochenXError):
    """A security policy was violated.

    Args:
        message: Human-readable error description.
        correlation_id: Correlation ID for cross-component tracing.
        component: Name of the component that raised the error.

    """


class PermissionDeniedError(SecurityViolationError):
    """An operation was denied due to insufficient permissions.

    Args:
        operation: Name of the denied operation.
        required_permission: Permission that was required.
        correlation_id: Correlation ID for cross-component tracing.
        component: Name of the component that raised the error.

    """

    def __init__(
        self,
        operation: str,
        required_permission: str,
        *,
        correlation_id: str = "",
        component: str = "",
    ) -> None:
        """Initialise with the denied operation details."""
        self.operation: str = operation
        self.required_permission: str = required_permission
        super().__init__(
            f"Permission denied for '{operation}': requires '{required_permission}'",
            correlation_id=correlation_id,
            component=component,
        )


class InputValidationError(SecurityViolationError):
    """Input validation failed on a public API boundary.

    Args:
        field_name: Name of the field that failed validation.
        reason: Reason the validation failed.
        correlation_id: Correlation ID for cross-component tracing.
        component: Name of the component that raised the error.

    """

    def __init__(
        self,
        field_name: str,
        reason: str,
        *,
        correlation_id: str = "",
        component: str = "",
    ) -> None:
        """Initialise with the failed validation details."""
        self.field_name: str = field_name
        self.reason: str = reason
        super().__init__(
            f"Validation failed for '{field_name}': {reason}",
            correlation_id=correlation_id,
            component=component,
        )
