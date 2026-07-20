"""Application exception taxonomy and Qt boundary guard."""

from collections.abc import Callable
from typing import ParamSpec, TypeVar


class JochenXError(Exception):
    """Base exception for expected, user-relevant foundation failures."""


class ConfigurationError(JochenXError):
    """Raised when configuration violates the supported schema."""


class DatabaseError(JochenXError):
    """Raised for database initialization or repository failures."""


P = ParamSpec("P")
R = TypeVar("R")


def guarded(callback: Callable[P, R], report: Callable[[Exception], None]) -> Callable[P, R | None]:
    """Return a UI-safe callback that reports unexpected exceptions."""
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R | None:
        try:
            return callback(*args, **kwargs)
        except Exception as error:  # boundary intentionally protects Qt event loop
            report(error)
            return None
    return wrapper
