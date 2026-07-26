"""Typed exception hierarchy for JOCHEN X Core Runtime.

Re-exports all exception classes from their respective modules.
"""

from __future__ import annotations

from jochen_x.core.exceptions.base import JochenXError
from jochen_x.core.exceptions.bootstrap import BootstrapError, BootstrapStepError
from jochen_x.core.exceptions.concurrency import (
    SchedulerError,
    TaskExecutionError,
    WorkerPoolError,
    WorkerPoolOverloadError,
)
from jochen_x.core.exceptions.lifecycle import (
    IllegalStateTransitionError,
    LifecycleError,
)
from jochen_x.core.exceptions.plugin import (
    PluginError,
    PluginIsolationError,
    PluginLifecycleError,
    PluginLoadError,
    PluginNotFoundError,
)
from jochen_x.core.exceptions.runtime import (
    RuntimeHostError,
    RuntimeShutdownError,
    RuntimeStartError,
    RuntimeStateError,
)
from jochen_x.core.exceptions.security import (
    InputValidationError,
    PermissionDeniedError,
    SecurityViolationError,
)

__all__ = [
    "BootstrapError",
    "BootstrapStepError",
    "IllegalStateTransitionError",
    "InputValidationError",
    "JochenXError",
    "LifecycleError",
    "PermissionDeniedError",
    "PluginError",
    "PluginIsolationError",
    "PluginLifecycleError",
    "PluginLoadError",
    "PluginNotFoundError",
    "RuntimeHostError",
    "RuntimeShutdownError",
    "RuntimeStartError",
    "RuntimeStateError",
    "SchedulerError",
    "SecurityViolationError",
    "TaskExecutionError",
    "WorkerPoolError",
    "WorkerPoolOverloadError",
]
