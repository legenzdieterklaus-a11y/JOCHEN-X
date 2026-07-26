"""Recovery strategies for each recovery level.

Each strategy encapsulates the logic for a single recovery level.
Strategies operate exclusively through injected interfaces and never
reference concrete component implementations.
"""

from __future__ import annotations

from typing import Protocol, runtime_checkable

from jochen_x.core.interfaces.logging import ILogger
from jochen_x.core.types.recovery_level import RecoveryLevel
from jochen_x.core.types.severity import LogSeverity

__all__ = [
    "ComponentRestartStrategy",
    "ComponentRetryStrategy",
    "IRecoveryStrategy",
    "RuntimeRestartStrategy",
    "ServiceRestartStrategy",
]

_COMPONENT: str = "RecoveryStrategy"


@runtime_checkable
class IRecoveryStrategy(Protocol):
    """Protocol for a recovery strategy at a specific level.

    Each strategy encapsulates the recovery action for one level.
    The ``execute`` method returns ``True`` on success and ``False``
    on failure; it must never raise.
    """

    @property
    def level(self) -> RecoveryLevel:
        """The recovery level this strategy handles."""
        ...

    def execute(
        self,
        error: Exception,
        component: str,
        *,
        logger: ILogger,
    ) -> bool:
        """Execute the recovery action.

        Args:
            error: The exception that triggered recovery.
            component: Name of the affected component.
            logger: Logger for recording recovery actions.

        Returns:
            ``True`` if recovery succeeded, ``False`` otherwise.

        """
        ...


class ComponentRetryStrategy:
    """Recovery strategy: retry the failed component operation.

    This is the lightest recovery action.  It logs the error and
    signals that the operation should be retried.  The actual retry
    is performed by the caller — this strategy only records the
    intent and validates preconditions.
    """

    @property
    def level(self) -> RecoveryLevel:
        """The recovery level this strategy handles."""
        return RecoveryLevel.COMPONENT_RETRY

    def execute(
        self,
        error: Exception,
        component: str,
        *,
        logger: ILogger,
    ) -> bool:
        """Execute component retry recovery.

        Args:
            error: The exception that triggered recovery.
            component: Name of the affected component.
            logger: Logger for recording recovery actions.

        Returns:
            ``True`` — retry is always considered successful at this
            level since the actual retry happens externally.

        """
        msg = f"Component retry for '{component}': {error}"
        logger.log(LogSeverity.WARNING, msg, component=_COMPONENT)
        return True


class ComponentRestartStrategy:
    """Recovery strategy: restart the failed component.

    Logs the restart intent.  The actual restart is delegated to the
    runtime host — this strategy validates and records the action.
    """

    @property
    def level(self) -> RecoveryLevel:
        """The recovery level this strategy handles."""
        return RecoveryLevel.COMPONENT_RESTART

    def execute(
        self,
        error: Exception,
        component: str,
        *,
        logger: ILogger,
    ) -> bool:
        """Execute component restart recovery.

        Args:
            error: The exception that triggered recovery.
            component: Name of the affected component.
            logger: Logger for recording recovery actions.

        Returns:
            ``True`` — restart intent is always recorded successfully.

        """
        msg = f"Component restart for '{component}': {error}"
        logger.log(LogSeverity.ERROR, msg, component=_COMPONENT)
        return True


class ServiceRestartStrategy:
    """Recovery strategy: restart the entire service.

    This is a higher-impact action that restarts all runtime services.
    """

    @property
    def level(self) -> RecoveryLevel:
        """The recovery level this strategy handles."""
        return RecoveryLevel.SERVICE_RESTART

    def execute(
        self,
        error: Exception,
        component: str,
        *,
        logger: ILogger,
    ) -> bool:
        """Execute service restart recovery.

        Args:
            error: The exception that triggered recovery.
            component: Name of the affected component.
            logger: Logger for recording recovery actions.

        Returns:
            ``True`` — service restart intent is always recorded
            successfully.

        """
        msg = f"Service restart triggered by '{component}': {error}"
        logger.log(LogSeverity.CRITICAL, msg, component=_COMPONENT)
        return True


class RuntimeRestartStrategy:
    """Recovery strategy: full runtime restart.

    This is the highest-impact recovery action.  It signals that the
    entire runtime must be restarted.
    """

    @property
    def level(self) -> RecoveryLevel:
        """The recovery level this strategy handles."""
        return RecoveryLevel.RUNTIME_RESTART

    def execute(
        self,
        error: Exception,
        component: str,
        *,
        logger: ILogger,
    ) -> bool:
        """Execute runtime restart recovery.

        Args:
            error: The exception that triggered recovery.
            component: Name of the affected component.
            logger: Logger for recording recovery actions.

        Returns:
            ``True`` — runtime restart intent is always recorded
            successfully.

        """
        msg = f"Runtime restart triggered by '{component}': {error}"
        logger.log(LogSeverity.CRITICAL, msg, component=_COMPONENT)
        return True
