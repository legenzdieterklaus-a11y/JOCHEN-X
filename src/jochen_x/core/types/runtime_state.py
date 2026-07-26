"""Runtime state definitions for the JOCHEN X lifecycle state machine."""

from __future__ import annotations

from enum import Enum, unique

__all__ = ["RuntimeState"]


@unique
class RuntimeState(Enum):
    """Represents the current state of the runtime lifecycle.

    The state machine enforces a strict transition table.  Only the
    transitions listed in the specification are permitted; any other
    transition raises ``IllegalStateTransitionError``.

    Attributes:
        CREATED: Initial state after construction, before bootstrap.
        BOOTSTRAPPING: Bootstrap sequence is executing.
        INITIALIZING: Post-bootstrap initialisation in progress.
        READY: Initialisation complete, ready to start.
        STARTING: Services are being started.
        RUNNING: Runtime is fully operational.
        PAUSED: Runtime is temporarily suspended.
        STOPPING: Shutdown sequence is executing.
        STOPPED: All services have been stopped.
        SHUTDOWN: Terminal state - runtime has been fully shut down.
        FAILED: An unhandled error occurred; recovery required.

    """

    CREATED = "CREATED"
    BOOTSTRAPPING = "BOOTSTRAPPING"
    INITIALIZING = "INITIALIZING"
    READY = "READY"
    STARTING = "STARTING"
    RUNNING = "RUNNING"
    PAUSED = "PAUSED"
    STOPPING = "STOPPING"
    STOPPED = "STOPPED"
    SHUTDOWN = "SHUTDOWN"
    FAILED = "FAILED"
