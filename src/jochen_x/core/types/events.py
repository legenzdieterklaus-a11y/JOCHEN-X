"""Runtime event dataclasses for inter-component communication.

All events are frozen dataclasses with timestamps.  They serve as
the typed message format for the EventBus.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import Enum, unique
from threading import Lock
from uuid import uuid4

from jochen_x.core.types.health_status import HealthStatus
from jochen_x.core.types.recovery_level import RecoveryLevel
from jochen_x.core.types.runtime_state import RuntimeState

__all__ = [
    "BootstrapStepCompletedEvent",
    "ComponentStartedEvent",
    "ComponentStoppedEvent",
    "DeadLetterEvent",
    "EventHandler",
    "HealthStatusChangedEvent",
    "PluginAction",
    "PluginLifecycleEvent",
    "RecoveryCompletedEvent",
    "RecoveryEscalatedEvent",
    "RecoveryInitiatedEvent",
    "ResourceThresholdEvent",
    "RuntimeEvent",
    "RuntimeStateChangedEvent",
    "SecurityViolationEvent",
    "ShutdownStepCompletedEvent",
]


_sequence_lock = Lock()
_sequence_value = 0


def _generate_event_id() -> str:
    return str(uuid4())


def _generate_correlation_id() -> str:
    return str(uuid4())


def _utc_now() -> datetime:
    return datetime.now(UTC)


def _next_sequence_number() -> int:
    global _sequence_value  # noqa: PLW0603
    with _sequence_lock:
        _sequence_value += 1
        return _sequence_value


# ---------------------------------------------------------------------------
# Type aliases
# ---------------------------------------------------------------------------

EventHandler = Callable[["RuntimeEvent"], None]
"""Callable that processes a single runtime event."""


# ---------------------------------------------------------------------------
# Supporting enums
# ---------------------------------------------------------------------------


@unique
class PluginAction(Enum):
    """Actions in the plugin lifecycle.

    Attributes:
        LOAD: Plugin is being loaded into memory.
        INITIALIZE: Plugin is being initialised.
        ENABLE: Plugin is being enabled for operation.
        DISABLE: Plugin is being disabled.
        UNLOAD: Plugin is being unloaded from memory.

    """

    LOAD = "LOAD"
    INITIALIZE = "INITIALIZE"
    ENABLE = "ENABLE"
    DISABLE = "DISABLE"
    UNLOAD = "UNLOAD"


# ---------------------------------------------------------------------------
# Base event
# ---------------------------------------------------------------------------


@dataclass(frozen=True, kw_only=True, slots=True)
class RuntimeEvent:
    """Base class for all runtime events.

    Every event carries a unique identifier, a UTC timestamp, an
    auto-generated correlation ID for distributed tracing, a
    monotonically increasing sequence number, and the name of
    the originating component.

    Args:
        event_id: Unique event identifier (auto-generated UUID).
        timestamp: UTC timestamp of the logical event time.
        created_at: UTC timestamp of object instantiation.
        correlation_id: Correlation ID for cross-component tracing
            (auto-generated UUID, never empty).
        sequence_number: Monotonically increasing sequence number
            across all event instances in this process.
        source: Name of the component that created the event.

    """

    event_id: str = field(default_factory=_generate_event_id)
    timestamp: datetime = field(default_factory=_utc_now)
    created_at: datetime = field(default_factory=_utc_now)
    correlation_id: str = field(default_factory=_generate_correlation_id)
    sequence_number: int = field(default_factory=_next_sequence_number)
    source: str = ""


# ---------------------------------------------------------------------------
# Lifecycle events
# ---------------------------------------------------------------------------


@dataclass(frozen=True, kw_only=True, slots=True)
class RuntimeStateChangedEvent(RuntimeEvent):
    """Emitted when the runtime transitions between lifecycle states.

    Args:
        old_state: The state before the transition.
        new_state: The state after the transition.

    """

    old_state: RuntimeState
    new_state: RuntimeState


@dataclass(frozen=True, kw_only=True, slots=True)
class BootstrapStepCompletedEvent(RuntimeEvent):
    """Emitted when a bootstrap step completes successfully.

    Args:
        step_name: Name of the completed bootstrap step.
        step_index: Zero-based index of the step in the sequence.

    """

    step_name: str
    step_index: int


@dataclass(frozen=True, kw_only=True, slots=True)
class ShutdownStepCompletedEvent(RuntimeEvent):
    """Emitted when a shutdown step completes.

    Args:
        step_name: Name of the completed shutdown step.
        step_index: Zero-based index of the step in the sequence.

    """

    step_name: str
    step_index: int


# ---------------------------------------------------------------------------
# Health events
# ---------------------------------------------------------------------------


@dataclass(frozen=True, kw_only=True, slots=True)
class HealthStatusChangedEvent(RuntimeEvent):
    """Emitted when a component's health status changes.

    Args:
        component_name: Name of the affected component.
        old_status: Previous health status.
        new_status: New health status.

    """

    component_name: str
    old_status: HealthStatus
    new_status: HealthStatus


# ---------------------------------------------------------------------------
# Recovery events
# ---------------------------------------------------------------------------


@dataclass(frozen=True, kw_only=True, slots=True)
class RecoveryInitiatedEvent(RuntimeEvent):
    """Emitted when a recovery action is initiated.

    Args:
        component_name: Name of the component under recovery.
        level: Recovery level being attempted.
        reason: Human-readable reason for the recovery.

    """

    component_name: str
    level: RecoveryLevel
    reason: str


@dataclass(frozen=True, kw_only=True, slots=True)
class RecoveryCompletedEvent(RuntimeEvent):
    """Emitted when a recovery action completes.

    Args:
        component_name: Name of the component under recovery.
        level: Recovery level that was attempted.
        success: Whether recovery succeeded.

    """

    component_name: str
    level: RecoveryLevel
    success: bool


@dataclass(frozen=True, kw_only=True, slots=True)
class RecoveryEscalatedEvent(RuntimeEvent):
    """Emitted when recovery escalates to a higher level.

    Args:
        component_name: Name of the component under recovery.
        from_level: Previous recovery level.
        to_level: New, higher recovery level.

    """

    component_name: str
    from_level: RecoveryLevel
    to_level: RecoveryLevel


# ---------------------------------------------------------------------------
# Security events
# ---------------------------------------------------------------------------


@dataclass(frozen=True, kw_only=True, slots=True)
class SecurityViolationEvent(RuntimeEvent):
    """Emitted when a security violation is detected.

    Args:
        violation_type: Category of the violation.
        details: Detailed description of the violation.
        component_name: Name of the component where the violation occurred.

    """

    violation_type: str
    details: str
    component_name: str


# ---------------------------------------------------------------------------
# Plugin events
# ---------------------------------------------------------------------------


@dataclass(frozen=True, kw_only=True, slots=True)
class PluginLifecycleEvent(RuntimeEvent):
    """Emitted when a plugin transitions through its lifecycle.

    Args:
        plugin_id: Unique identifier of the plugin.
        action: Lifecycle action being performed.
        success: Whether the action completed successfully.

    """

    plugin_id: str
    action: PluginAction
    success: bool


# ---------------------------------------------------------------------------
# Resource events
# ---------------------------------------------------------------------------


@dataclass(frozen=True, kw_only=True, slots=True)
class ResourceThresholdEvent(RuntimeEvent):
    """Emitted when a monitored resource exceeds its threshold.

    Args:
        resource_name: Name of the resource (e.g. "cpu", "memory").
        current_value: Current measured value.
        threshold_value: Configured threshold that was exceeded.

    """

    resource_name: str
    current_value: float
    threshold_value: float


# ---------------------------------------------------------------------------
# EventBus events
# ---------------------------------------------------------------------------


@dataclass(frozen=True, kw_only=True, slots=True)
class DeadLetterEvent(RuntimeEvent):
    """Emitted when an event cannot be delivered to any handler.

    Args:
        original_event_id: ID of the undeliverable event.
        original_event_type: Type name of the undeliverable event.
        handler_name: Name of the handler that failed, if applicable.
        error_message: Description of the delivery failure.

    """

    original_event_id: str
    original_event_type: str
    handler_name: str
    error_message: str


# ---------------------------------------------------------------------------
# Component events
# ---------------------------------------------------------------------------


@dataclass(frozen=True, kw_only=True, slots=True)
class ComponentStartedEvent(RuntimeEvent):
    """Emitted when a runtime component starts.

    Args:
        component_name: Name of the started component.

    """

    component_name: str


@dataclass(frozen=True, kw_only=True, slots=True)
class ComponentStoppedEvent(RuntimeEvent):
    """Emitted when a runtime component stops.

    Args:
        component_name: Name of the stopped component.

    """

    component_name: str
