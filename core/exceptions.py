"""Application exception taxonomy and Qt boundary guard."""

from collections.abc import Callable
from dataclasses import dataclass
from typing import ParamSpec, TypeVar


class JochenXError(Exception):
    """Base exception for expected, user-relevant foundation failures."""


class ConfigurationError(JochenXError):
    """Raised when configuration violates the supported schema."""


class DatabaseError(JochenXError):
    """Raised for database initialization or repository failures."""


@dataclass(frozen=True, slots=True)
class TransitionRejection:
    """Structured rejection result for a denied lifecycle state transition.

    Carries the reason so callers never have to parse exception messages.
    ``target`` is ``None`` when a state expectation (not a transition request)
    was violated.
    """

    source: str
    target: str | None
    reason: str
    allowed: tuple[str, ...]


class StateTransitionError(JochenXError):
    """Raised when a lifecycle state transition is rejected.

    The structured :class:`TransitionRejection` is available as ``rejection``.
    """

    def __init__(self, rejection: TransitionRejection) -> None:
        super().__init__(rejection.reason)
        self.rejection = rejection


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
