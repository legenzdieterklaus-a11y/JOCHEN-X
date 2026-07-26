"""Service lifetime scopes for the dependency injection container."""

from __future__ import annotations

from enum import Enum, unique

__all__ = ["ServiceScope"]


@unique
class ServiceScope(Enum):
    """Lifetime scope controlling how service instances are managed.

    Attributes:
        SINGLETON: Exactly one instance for the entire container lifetime.
            Created lazily on first resolution.
        TRANSIENT: A new instance is created for every resolution request.
        SCOPED: One instance per scope context.  Must be resolved within
            a ``ScopedContainer``.

    """

    SINGLETON = "SINGLETON"
    TRANSIENT = "TRANSIENT"
    SCOPED = "SCOPED"
