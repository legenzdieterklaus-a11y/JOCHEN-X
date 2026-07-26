"""Recovery level configuration and registry.

Defines per-level configuration (max retries, cooldown) and a registry
that maps each ``RecoveryLevel`` to its configuration.
"""

from __future__ import annotations

import threading
from dataclasses import dataclass, field
from datetime import UTC, datetime

from jochen_x.core.exceptions.security import InputValidationError
from jochen_x.core.types.recovery_level import RecoveryLevel

__all__ = [
    "RecoveryLevelConfig",
    "RecoveryLevelRegistry",
]

_DEFAULT_MAX_RETRIES: dict[RecoveryLevel, int] = {
    RecoveryLevel.COMPONENT_RETRY: 3,
    RecoveryLevel.COMPONENT_RESTART: 2,
    RecoveryLevel.SERVICE_RESTART: 2,
    RecoveryLevel.RUNTIME_RESTART: 1,
}

_DEFAULT_COOLDOWN_SECONDS: dict[RecoveryLevel, float] = {
    RecoveryLevel.COMPONENT_RETRY: 1.0,
    RecoveryLevel.COMPONENT_RESTART: 5.0,
    RecoveryLevel.SERVICE_RESTART: 15.0,
    RecoveryLevel.RUNTIME_RESTART: 30.0,
}

_CIRCUIT_BREAKER_WINDOW_SECONDS: float = 60.0
_CIRCUIT_BREAKER_THRESHOLD: int = 5

_FIELD_MAX_RETRIES: str = "max_retries"
_FIELD_COOLDOWN: str = "cooldown_seconds"
_FIELD_CB_THRESHOLD: str = "circuit_breaker_threshold"
_FIELD_CB_WINDOW: str = "circuit_breaker_window_seconds"
_REASON_MIN_ONE: str = "must be at least 1"
_REASON_NOT_NEGATIVE: str = "must not be negative"
_REASON_POSITIVE: str = "must be positive"
_CONFIG_COMPONENT: str = "RecoveryLevelConfig"


@dataclass(frozen=True, slots=True, kw_only=True)
class RecoveryLevelConfig:
    """Configuration for a single recovery level.

    Attributes:
        level: The recovery level this configuration applies to.
        max_retries: Maximum number of recovery attempts at this level
            before escalation.
        cooldown_seconds: Minimum time in seconds between recovery
            attempts at this level.
        circuit_breaker_threshold: Number of failures within the
            circuit-breaker window that triggers escalation.
        circuit_breaker_window_seconds: Time window in seconds for the
            circuit breaker.

    """

    level: RecoveryLevel
    max_retries: int
    cooldown_seconds: float
    circuit_breaker_threshold: int = _CIRCUIT_BREAKER_THRESHOLD
    circuit_breaker_window_seconds: float = _CIRCUIT_BREAKER_WINDOW_SECONDS

    def __post_init__(self) -> None:
        """Validate configuration values."""
        if self.max_retries < 1:
            raise InputValidationError(
                _FIELD_MAX_RETRIES,
                _REASON_MIN_ONE,
                component=_CONFIG_COMPONENT,
            )
        if self.cooldown_seconds < 0.0:
            raise InputValidationError(
                _FIELD_COOLDOWN,
                _REASON_NOT_NEGATIVE,
                component=_CONFIG_COMPONENT,
            )
        if self.circuit_breaker_threshold < 1:
            raise InputValidationError(
                _FIELD_CB_THRESHOLD,
                _REASON_MIN_ONE,
                component=_CONFIG_COMPONENT,
            )
        if self.circuit_breaker_window_seconds <= 0.0:
            raise InputValidationError(
                _FIELD_CB_WINDOW,
                _REASON_POSITIVE,
                component=_CONFIG_COMPONENT,
            )


@dataclass(slots=True)
class _ComponentLevelState:
    """Mutable per-component, per-level recovery tracking state.

    Attributes:
        attempt_count: Number of recovery attempts at this level.
        failure_timestamps: Timestamps of recent failures for
            circuit-breaker evaluation.
        last_attempt_time: Timestamp of the most recent recovery
            attempt.

    """

    attempt_count: int = 0
    failure_timestamps: list[datetime] = field(default_factory=list)
    last_attempt_time: datetime | None = None


class RecoveryLevelRegistry:
    """Registry that maps recovery levels to their configuration.

    Thread-safe.  Provides state tracking per component per level and
    circuit-breaker evaluation.

    Args:
        configs: Optional mapping of recovery levels to their
            configuration.  Missing levels receive default
            configuration.

    """

    def __init__(
        self,
        configs: dict[RecoveryLevel, RecoveryLevelConfig] | None = None,
    ) -> None:
        """Initialise the registry with optional custom configs."""
        self._lock: threading.RLock = threading.RLock()
        self._configs: dict[RecoveryLevel, RecoveryLevelConfig] = {}
        for level in RecoveryLevel:
            if configs and level in configs:
                self._configs[level] = configs[level]
            else:
                self._configs[level] = RecoveryLevelConfig(
                    level=level,
                    max_retries=_DEFAULT_MAX_RETRIES[level],
                    cooldown_seconds=_DEFAULT_COOLDOWN_SECONDS[level],
                )
        self._states: dict[
            str, dict[RecoveryLevel, _ComponentLevelState]
        ] = {}

    def get_config(
        self, level: RecoveryLevel,
    ) -> RecoveryLevelConfig:
        """Return the configuration for the given recovery level.

        Args:
            level: The recovery level to look up.

        Returns:
            The configuration for the requested level.

        """
        with self._lock:
            return self._configs[level]

    def get_state(
        self, component: str, level: RecoveryLevel,
    ) -> _ComponentLevelState:
        """Return the mutable state for a component at a given level.

        Creates the state entry if it does not exist.

        Args:
            component: Name of the component.
            level: The recovery level.

        Returns:
            The tracking state for the component/level pair.

        """
        with self._lock:
            comp_states = self._states.setdefault(component, {})
            if level not in comp_states:
                comp_states[level] = _ComponentLevelState()
            return comp_states[level]

    def record_attempt(
        self,
        component: str,
        level: RecoveryLevel,
        *,
        now: datetime | None = None,
    ) -> None:
        """Record a recovery attempt for a component at a level.

        Args:
            component: Name of the component.
            level: The recovery level attempted.
            now: Optional explicit timestamp (for testing determinism).

        """
        ts = now or datetime.now(UTC)
        with self._lock:
            state = self.get_state(component, level)
            state.attempt_count += 1
            state.last_attempt_time = ts

    def record_failure(
        self,
        component: str,
        level: RecoveryLevel,
        *,
        now: datetime | None = None,
    ) -> None:
        """Record a recovery failure for circuit-breaker tracking.

        Args:
            component: Name of the component.
            level: The recovery level that failed.
            now: Optional explicit timestamp (for testing determinism).

        """
        ts = now or datetime.now(UTC)
        with self._lock:
            state = self.get_state(component, level)
            state.failure_timestamps.append(ts)

    def is_cooldown_active(
        self,
        component: str,
        level: RecoveryLevel,
        *,
        now: datetime | None = None,
    ) -> bool:
        """Check whether the cooldown period is still active.

        Args:
            component: Name of the component.
            level: The recovery level to check.
            now: Optional explicit timestamp.

        Returns:
            ``True`` if the cooldown has not yet elapsed.

        """
        ts = now or datetime.now(UTC)
        with self._lock:
            state = self.get_state(component, level)
            if state.last_attempt_time is None:
                return False
            config = self._configs[level]
            elapsed = (ts - state.last_attempt_time).total_seconds()
            return elapsed < config.cooldown_seconds

    def is_circuit_open(
        self,
        component: str,
        level: RecoveryLevel,
        *,
        now: datetime | None = None,
    ) -> bool:
        """Check whether the circuit breaker has tripped.

        The circuit is open when the number of failures within the
        configured window exceeds the threshold.

        Args:
            component: Name of the component.
            level: The recovery level to check.
            now: Optional explicit timestamp.

        Returns:
            ``True`` if the circuit breaker is open.

        """
        ts = now or datetime.now(UTC)
        with self._lock:
            state = self.get_state(component, level)
            config = self._configs[level]
            cutoff = ts.timestamp() - config.circuit_breaker_window_seconds
            recent = [
                t for t in state.failure_timestamps
                if t.timestamp() >= cutoff
            ]
            state.failure_timestamps = recent
            return len(recent) >= config.circuit_breaker_threshold

    def has_retries_remaining(
        self, component: str, level: RecoveryLevel,
    ) -> bool:
        """Check whether retries remain at this level.

        Args:
            component: Name of the component.
            level: The recovery level to check.

        Returns:
            ``True`` if the attempt count is below ``max_retries``.

        """
        with self._lock:
            state = self.get_state(component, level)
            config = self._configs[level]
            return state.attempt_count < config.max_retries

    def reset_component(self, component: str) -> None:
        """Reset all recovery state for a component.

        Args:
            component: Name of the component to reset.

        """
        with self._lock:
            self._states.pop(component, None)

    def reset_all(self) -> None:
        """Reset all recovery state for all components."""
        with self._lock:
            self._states.clear()

    def get_attempt_count(
        self, component: str, level: RecoveryLevel,
    ) -> int:
        """Return the current attempt count for a component at a level.

        Args:
            component: Name of the component.
            level: The recovery level.

        Returns:
            Number of recorded attempts.

        """
        with self._lock:
            state = self.get_state(component, level)
            return state.attempt_count
