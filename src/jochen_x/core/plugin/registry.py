"""Plugin registry for lifecycle management and isolation.

The ``PluginRegistry`` manages the complete plugin lifecycle
(Load → Initialize → Enable → Disable → Unload), creates
isolated contexts and sandboxes for each plugin, emits lifecycle
events, records audit entries, and integrates with the health
monitoring system.

Every lifecycle transition is validated against an explicit
state machine.  Illegal transitions raise
``PluginLifecycleError``.

All operations are thread-safe.
"""

from __future__ import annotations

import contextlib
from collections.abc import Callable, Sequence
from enum import Enum, unique
from threading import RLock
from typing import TYPE_CHECKING, Protocol, runtime_checkable

from jochen_x.core.exceptions.base import JochenXError
from jochen_x.core.exceptions.plugin import (
    PluginError,
    PluginLifecycleError,
    PluginLoadError,
    PluginNotFoundError,
)
from jochen_x.core.exceptions.security import InputValidationError
from jochen_x.core.plugin.context import PluginContext
from jochen_x.core.plugin.sandbox import PluginSandbox
from jochen_x.core.types.events import PluginAction, PluginLifecycleEvent
from jochen_x.core.types.health_status import HealthStatus

if TYPE_CHECKING:
    from jochen_x.core.interfaces.audit import IAuditLog
    from jochen_x.core.interfaces.event_bus import IEventBus
    from jochen_x.core.interfaces.health import IHealthMonitor
    from jochen_x.core.interfaces.logging import ILogger
    from jochen_x.core.interfaces.plugin_context import IPluginContext
    from jochen_x.core.interfaces.service_registry import IServiceRegistry

__all__ = [
    "IPlugin",
    "PluginRegistry",
    "PluginState",
]


# ---------------------------------------------------------------------------
# Plugin Protocol
# ---------------------------------------------------------------------------


@runtime_checkable
class IPlugin(Protocol):
    """Protocol that plugins must implement.

    Defines the lifecycle callbacks invoked by the plugin registry
    during each phase of the plugin lifecycle.

    """

    def on_load(self, context: IPluginContext) -> None:
        """Handle the load phase of the plugin lifecycle.

        Args:
            context: The isolated plugin context providing access
                to runtime services.

        """
        ...

    def on_initialize(self) -> None:
        """Handle the initialisation phase after loading."""
        ...

    def on_enable(self) -> None:
        """Activate the plugin for operation."""
        ...

    def on_disable(self) -> None:
        """Deactivate the plugin."""
        ...

    def on_unload(self) -> None:
        """Handle the unload phase of the plugin lifecycle."""
        ...


# ---------------------------------------------------------------------------
# Plugin State
# ---------------------------------------------------------------------------


@unique
class PluginState(Enum):
    """Lifecycle states of a managed plugin.

    Attributes:
        UNLOADED: Plugin is not loaded.
        LOADED: Plugin has been loaded and received its context.
        INITIALIZED: Plugin has been initialised.
        ENABLED: Plugin is active and operational.
        DISABLED: Plugin is loaded but not active.

    """

    UNLOADED = "UNLOADED"
    LOADED = "LOADED"
    INITIALIZED = "INITIALIZED"
    ENABLED = "ENABLED"
    DISABLED = "DISABLED"


# ---------------------------------------------------------------------------
# Transition table
# ---------------------------------------------------------------------------

_VALID_TRANSITIONS: dict[PluginState, dict[PluginAction, PluginState]] = {
    PluginState.UNLOADED: {
        PluginAction.LOAD: PluginState.LOADED,
    },
    PluginState.LOADED: {
        PluginAction.INITIALIZE: PluginState.INITIALIZED,
        PluginAction.UNLOAD: PluginState.UNLOADED,
    },
    PluginState.INITIALIZED: {
        PluginAction.ENABLE: PluginState.ENABLED,
        PluginAction.UNLOAD: PluginState.UNLOADED,
    },
    PluginState.ENABLED: {
        PluginAction.DISABLE: PluginState.DISABLED,
    },
    PluginState.DISABLED: {
        PluginAction.ENABLE: PluginState.ENABLED,
        PluginAction.UNLOAD: PluginState.UNLOADED,
    },
}


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

_COMPONENT_NAME = "PluginRegistry"

_FIELD_PLUGIN_ID = "plugin_id"
_FIELD_PLUGIN = "plugin"
_REASON_EMPTY = "must not be empty"
_REASON_NOT_STRING = "must be a string"
_REASON_NOT_PLUGIN = "must implement the IPlugin protocol"


# ---------------------------------------------------------------------------
# Internal entry
# ---------------------------------------------------------------------------


class _PluginEntry:
    """Internal tracking record for a registered plugin."""

    __slots__ = ("context", "plugin", "plugin_id", "sandbox", "state")

    def __init__(
        self,
        *,
        plugin_id: str,
        plugin: IPlugin,
        context: PluginContext,
        sandbox: PluginSandbox,
    ) -> None:
        """Initialise the plugin entry."""
        self.plugin_id: str = plugin_id
        self.plugin: IPlugin = plugin
        self.context: PluginContext = context
        self.sandbox: PluginSandbox = sandbox
        self.state: PluginState = PluginState.UNLOADED


# ---------------------------------------------------------------------------
# Registry
# ---------------------------------------------------------------------------


class PluginRegistry:
    """Manages plugin lifecycle, isolation, and health.

    Creates isolated ``PluginContext`` and ``PluginSandbox``
    instances for each plugin, manages lifecycle transitions via
    an explicit state machine, emits ``PluginLifecycleEvent`` on
    every transition, and records all transitions in the audit log.

    Implements the ``IHealthCheck`` protocol.

    Args:
        event_bus: Event bus for publishing lifecycle events.
        audit_log: Audit log for recording lifecycle transitions.
        logger: Logger for recording plugin operations.
        service_registry: Service registry for plugin contexts.
        health_monitor: Health monitor for registering per-plugin
            health checks (optional).

    """

    __slots__ = (
        "_audit_log",
        "_event_bus",
        "_health_monitor",
        "_lock",
        "_logger",
        "_plugins",
        "_service_registry",
    )

    def __init__(
        self,
        *,
        event_bus: IEventBus,
        audit_log: IAuditLog,
        logger: ILogger,
        service_registry: IServiceRegistry,
        health_monitor: IHealthMonitor | None = None,
    ) -> None:
        """Initialise the plugin registry."""
        self._event_bus: IEventBus = event_bus
        self._audit_log: IAuditLog = audit_log
        self._logger: ILogger = logger
        self._service_registry: IServiceRegistry = service_registry
        self._health_monitor: IHealthMonitor | None = health_monitor
        self._lock: RLock = RLock()
        self._plugins: dict[str, _PluginEntry] = {}

    # -- Plugin Lifecycle ------------------------------------------------------

    def load_plugin(self, plugin_id: str, plugin: IPlugin) -> None:
        """Load a plugin into the registry.

        Creates an isolated context and sandbox, invokes
        ``plugin.on_load``, and transitions the plugin to the
        ``LOADED`` state.

        Args:
            plugin_id: Unique identifier for the plugin.
            plugin: The plugin instance to load.

        Raises:
            InputValidationError: If *plugin_id* is empty or
                *plugin* does not implement ``IPlugin``.
            PluginError: If a plugin with the same ID is already
                loaded.
            PluginLoadError: If the plugin fails during
                ``on_load``.

        """
        self._validate_plugin_id(plugin_id)
        self._validate_plugin(plugin)

        with self._lock:
            if plugin_id in self._plugins:
                msg = f"Plugin '{plugin_id}' is already loaded"
                raise PluginError(
                    msg,
                    plugin_id=plugin_id,
                    component=_COMPONENT_NAME,
                )

        context = PluginContext(
            plugin_id=plugin_id,
            event_bus=self._event_bus,
            logger=self._logger,
            service_registry=self._service_registry,
        )

        sandbox = PluginSandbox(
            plugin_id=plugin_id,
            logger=self._logger,
        )

        entry = _PluginEntry(
            plugin_id=plugin_id,
            plugin=plugin,
            context=context,
            sandbox=sandbox,
        )

        success = sandbox.execute(
            PluginAction.LOAD,
            lambda: plugin.on_load(context),
        )

        if not success:
            context.dispose()
            self._emit_lifecycle_event(
                plugin_id, PluginAction.LOAD, success=False
            )
            self._audit_lifecycle(
                plugin_id, PluginAction.LOAD, success=False
            )
            msg = f"Plugin '{plugin_id}' failed during load"
            raise PluginLoadError(
                msg,
                plugin_id=plugin_id,
                component=_COMPONENT_NAME,
            )

        entry.state = PluginState.LOADED

        with self._lock:
            self._plugins[plugin_id] = entry

        if self._health_monitor is not None:
            with contextlib.suppress(JochenXError):
                self._health_monitor.register_check(
                    f"Plugin[{plugin_id}]",
                    sandbox,
                )

        self._emit_lifecycle_event(
            plugin_id, PluginAction.LOAD, success=True
        )
        self._audit_lifecycle(
            plugin_id, PluginAction.LOAD, success=True
        )
        loaded_msg = f"Plugin '{plugin_id}' loaded"
        self._logger.info(loaded_msg, component=_COMPONENT_NAME)

    def initialize_plugin(self, plugin_id: str) -> None:
        """Initialise a loaded plugin.

        Transitions the plugin from ``LOADED`` to ``INITIALIZED``.

        Args:
            plugin_id: Identifier of the plugin to initialise.

        Raises:
            PluginNotFoundError: If the plugin is not loaded.
            PluginLifecycleError: If the transition is invalid.
            PluginError: If the plugin fails during
                ``on_initialize``.

        """
        self._transition(plugin_id, PluginAction.INITIALIZE)

    def enable_plugin(self, plugin_id: str) -> None:
        """Enable a plugin for operation.

        Transitions the plugin from ``INITIALIZED`` or ``DISABLED``
        to ``ENABLED``.

        Args:
            plugin_id: Identifier of the plugin to enable.

        Raises:
            PluginNotFoundError: If the plugin is not loaded.
            PluginLifecycleError: If the transition is invalid.
            PluginError: If the plugin fails during ``on_enable``.

        """
        self._transition(plugin_id, PluginAction.ENABLE)

    def disable_plugin(self, plugin_id: str) -> None:
        """Disable an active plugin.

        Transitions the plugin from ``ENABLED`` to ``DISABLED``.

        Args:
            plugin_id: Identifier of the plugin to disable.

        Raises:
            PluginNotFoundError: If the plugin is not loaded.
            PluginLifecycleError: If the transition is invalid.
            PluginError: If the plugin fails during ``on_disable``.

        """
        self._transition(plugin_id, PluginAction.DISABLE)

    def unload_plugin(self, plugin_id: str) -> None:
        """Unload a plugin and dispose its resources.

        Invokes ``on_unload`` (best-effort), disposes the plugin
        context, unregisters its health check, and removes the
        plugin from the registry.

        An enabled plugin must be disabled before it can be
        unloaded.

        Args:
            plugin_id: Identifier of the plugin to unload.

        Raises:
            PluginNotFoundError: If the plugin is not loaded.
            PluginLifecycleError: If the plugin is currently
                enabled.

        """
        self._validate_plugin_id(plugin_id)

        with self._lock:
            entry = self._plugins.get(plugin_id)
            if entry is None:
                msg = f"Plugin '{plugin_id}' is not loaded"
                raise PluginNotFoundError(
                    msg,
                    plugin_id=plugin_id,
                    component=_COMPONENT_NAME,
                )

            allowed = _VALID_TRANSITIONS.get(entry.state, {})
            if PluginAction.UNLOAD not in allowed:
                msg = (
                    f"Cannot unload plugin '{plugin_id}' "
                    f"from state {entry.state.value}"
                )
                raise PluginLifecycleError(
                    msg,
                    plugin_id=plugin_id,
                    from_state=entry.state.value,
                    to_action=PluginAction.UNLOAD.value,
                    component=_COMPONENT_NAME,
                )

        callback_success = entry.sandbox.execute(
            PluginAction.UNLOAD,
            entry.plugin.on_unload,
        )

        entry.context.dispose()

        if self._health_monitor is not None:
            with contextlib.suppress(JochenXError):
                self._health_monitor.unregister_check(
                    f"Plugin[{plugin_id}]"
                )

        with self._lock:
            self._plugins.pop(plugin_id, None)

        self._emit_lifecycle_event(
            plugin_id, PluginAction.UNLOAD, success=callback_success
        )
        self._audit_lifecycle(
            plugin_id, PluginAction.UNLOAD, success=callback_success
        )
        unloaded_msg = f"Plugin '{plugin_id}' unloaded"
        self._logger.info(unloaded_msg, component=_COMPONENT_NAME)

    # -- Introspection ---------------------------------------------------------

    def get_plugin_state(self, plugin_id: str) -> PluginState:
        """Return the current lifecycle state of a plugin.

        Args:
            plugin_id: Identifier of the plugin.

        Returns:
            The plugin's current lifecycle state.

        Raises:
            PluginNotFoundError: If the plugin is not loaded.

        """
        self._validate_plugin_id(plugin_id)
        with self._lock:
            entry = self._plugins.get(plugin_id)
            if entry is None:
                msg = f"Plugin '{plugin_id}' is not loaded"
                raise PluginNotFoundError(
                    msg,
                    plugin_id=plugin_id,
                    component=_COMPONENT_NAME,
                )
            return entry.state

    def get_plugin_context(self, plugin_id: str) -> IPluginContext:
        """Return the context of a loaded plugin.

        Args:
            plugin_id: Identifier of the plugin.

        Returns:
            The plugin's isolated context.

        Raises:
            PluginNotFoundError: If the plugin is not loaded.

        """
        self._validate_plugin_id(plugin_id)
        with self._lock:
            entry = self._plugins.get(plugin_id)
            if entry is None:
                msg = f"Plugin '{plugin_id}' is not loaded"
                raise PluginNotFoundError(
                    msg,
                    plugin_id=plugin_id,
                    component=_COMPONENT_NAME,
                )
            return entry.context

    def get_plugin_ids(self) -> Sequence[str]:
        """Return all currently loaded plugin identifiers.

        Returns:
            A sequence of plugin identifiers.

        """
        with self._lock:
            return list(self._plugins.keys())

    def has_plugin(self, plugin_id: str) -> bool:
        """Check whether a plugin is loaded.

        Args:
            plugin_id: Identifier to check.

        Returns:
            ``True`` if the plugin is loaded.

        """
        with self._lock:
            return plugin_id in self._plugins

    def get_loaded_count(self) -> int:
        """Return the number of loaded plugins.

        Returns:
            The plugin count.

        """
        with self._lock:
            return len(self._plugins)

    # -- IHealthCheck protocol -------------------------------------------------

    def check_health(self) -> HealthStatus:
        """Return the aggregated health status of all plugins.

        Returns:
            ``HEALTHY`` if all plugins are healthy or none are
            loaded, ``DEGRADED`` if any plugin is degraded or
            unhealthy.

        """
        with self._lock:
            if not self._plugins:
                return HealthStatus.HEALTHY
            statuses = [
                entry.sandbox.check_health()
                for entry in self._plugins.values()
            ]

        if any(s == HealthStatus.UNHEALTHY for s in statuses):
            return HealthStatus.DEGRADED
        if any(s == HealthStatus.DEGRADED for s in statuses):
            return HealthStatus.DEGRADED
        return HealthStatus.HEALTHY

    def get_component_name(self) -> str:
        """Return the component name.

        Returns:
            The string ``"PluginRegistry"``.

        """
        return _COMPONENT_NAME

    # -- Internal helpers ------------------------------------------------------

    def _transition(self, plugin_id: str, action: PluginAction) -> None:
        """Execute a lifecycle transition.

        Validates the transition, invokes the plugin callback via
        the sandbox, and updates the plugin state on success.

        Args:
            plugin_id: The plugin to transition.
            action: The lifecycle action to perform.

        Raises:
            PluginNotFoundError: If the plugin is not loaded.
            PluginLifecycleError: If the transition is not valid
                from the current state.
            PluginError: If the plugin callback fails.

        """
        self._validate_plugin_id(plugin_id)

        with self._lock:
            entry = self._plugins.get(plugin_id)
            if entry is None:
                msg = f"Plugin '{plugin_id}' is not loaded"
                raise PluginNotFoundError(
                    msg,
                    plugin_id=plugin_id,
                    component=_COMPONENT_NAME,
                )

            target = _VALID_TRANSITIONS.get(entry.state, {}).get(action)
            if target is None:
                msg = (
                    f"Cannot perform {action.value} on plugin "
                    f"'{plugin_id}' in state {entry.state.value}"
                )
                raise PluginLifecycleError(
                    msg,
                    plugin_id=plugin_id,
                    from_state=entry.state.value,
                    to_action=action.value,
                    component=_COMPONENT_NAME,
                )

        callback = self._get_callback(entry.plugin, action)
        success = entry.sandbox.execute(action, callback)

        self._emit_lifecycle_event(plugin_id, action, success=success)
        self._audit_lifecycle(plugin_id, action, success=success)

        if success:
            with self._lock:
                entry.state = target
            info_msg = f"Plugin '{plugin_id}' transitioned to {target.value}"
            self._logger.info(info_msg, component=_COMPONENT_NAME)
        else:
            msg = f"Plugin '{plugin_id}' failed during {action.value}"
            raise PluginError(
                msg,
                plugin_id=plugin_id,
                component=_COMPONENT_NAME,
            )

    @staticmethod
    def _get_callback(
        plugin: IPlugin,
        action: PluginAction,
    ) -> Callable[[], None]:
        """Map a lifecycle action to its plugin callback.

        Args:
            plugin: The plugin instance.
            action: The lifecycle action.

        Returns:
            The bound callback method.

        Raises:
            PluginError: If the action has no mapped callback.

        """
        if action is PluginAction.INITIALIZE:
            return plugin.on_initialize
        if action is PluginAction.ENABLE:
            return plugin.on_enable
        if action is PluginAction.DISABLE:
            return plugin.on_disable
        msg = f"No callback mapped for action {action.value}"
        raise PluginError(msg, component=_COMPONENT_NAME)

    def _validate_plugin_id(self, plugin_id: str) -> None:
        """Validate a plugin identifier."""
        if not isinstance(plugin_id, str):
            raise InputValidationError(
                _FIELD_PLUGIN_ID,
                _REASON_NOT_STRING,
                component=_COMPONENT_NAME,
            )
        if not plugin_id:
            raise InputValidationError(
                _FIELD_PLUGIN_ID,
                _REASON_EMPTY,
                component=_COMPONENT_NAME,
            )

    def _validate_plugin(self, plugin: IPlugin) -> None:
        """Validate that *plugin* implements the ``IPlugin`` protocol."""
        if not isinstance(plugin, IPlugin):
            raise InputValidationError(
                _FIELD_PLUGIN,
                _REASON_NOT_PLUGIN,
                component=_COMPONENT_NAME,
            )

    def _emit_lifecycle_event(
        self,
        plugin_id: str,
        action: PluginAction,
        *,
        success: bool,
    ) -> None:
        """Publish a plugin lifecycle event on the event bus."""
        event = PluginLifecycleEvent(
            plugin_id=plugin_id,
            action=action,
            success=success,
            source=_COMPONENT_NAME,
        )
        with contextlib.suppress(JochenXError):
            self._event_bus.publish(event)

    def _audit_lifecycle(
        self,
        plugin_id: str,
        action: PluginAction,
        *,
        success: bool,
    ) -> None:
        """Record a lifecycle event in the audit log."""
        event = PluginLifecycleEvent(
            plugin_id=plugin_id,
            action=action,
            success=success,
            source=_COMPONENT_NAME,
        )
        with contextlib.suppress(JochenXError):
            self._audit_log.record(event)
