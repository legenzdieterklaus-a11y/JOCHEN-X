"""Base exception hierarchy for JOCHEN X Core Runtime.

Every typed exception in the runtime derives from ``JochenXError``.
This ensures a consistent interface with correlation ID and component
attribution across the entire exception hierarchy.
"""

from __future__ import annotations

from uuid import uuid4

__all__ = ["JochenXError"]


class JochenXError(Exception):
    """Base exception for all JOCHEN X runtime errors.

    Args:
        message: Human-readable error description.
        correlation_id: Correlation ID for cross-component tracing
            (auto-generated UUID when not provided or empty).
        component: Name of the component that raised the error.

    """

    def __init__(
        self,
        message: str,
        *,
        correlation_id: str = "",
        component: str = "",
    ) -> None:
        """Initialise the exception with message and tracing metadata."""
        super().__init__(message)
        self.correlation_id: str = correlation_id or str(uuid4())
        self.component: str = component
