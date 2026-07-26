"""Isolated plugin context for runtime service access.

The ``PluginContext`` is the sole interface through which plugins
interact with the runtime.  Each plugin receives its own context
instance that provides a scoped logger, event bus access, and
service resolution through defined interfaces.

After a plugin is unloaded, its context is disposed and all
further access raises ``PluginIsolationError``.

All operations are thread-safe.
"""

from __future__ import annotations

from threading import RLock
from typing import TYPE_CHECKING, TypeVar

from jochen_x.core.exceptions.plugin import PluginIsolationError
from jochen_x.core.types.health_status import HealthStatus
from jochen_x.core.types.severity import LogSeverity

if TYPE_CHECKING:
    from jochen_x.core.interfaces.event_bus import IEventBus
    from jochen_x.core.interfaces.logging import ILogger
    from jochen_x.core.interfaces.service_registry import IServiceRegistry

__all__ = ["PluginContext"]

T = TypeVar("T")

_COMPONENT_NAME = "PluginContext"


class _ScopedLogger:
    """Logger wrapper that defaults the component to the plugin ID.

    Implements the ``ILogger`` protocol structurally.  Every log
    method delegates to the underlying logger, substituting the
    plugin's component name when the caller does not provide one.

    Args:
        delegate: The underlying logger to delegate to.
        component: The default component name (plugin identifier).

    """

    __slots__ = ("_component", "_delegate")

    def __init__(self, delegate: ILogger, component: str) -> None:
        """Initialise the scoped logger."""
        self._delegate: ILogger = delegate
        self._component: str = component

    def log(
        self,
        severity: LogSeverity,
        message: str,
        *,
        component: str = "",
        correlation_id: str = "",
    ) -> None:
        """Emit a log entry with the plugin's component name.

        Args:
            severity: Log severity level.
            message: Log message.
            component: Component override (defaults to plugin ID).
            correlation_id: Correlation ID for tracing.

        """
        self._delegate.log(
            severity,
            message,
            component=component or self._component,
            correlation_id=correlation_id,
        )

    def debug(
        self,
        message: str,
        *,
        component: str = "",
        correlation_id: str = "",
    ) -> None:
        """Log a DEBUG-level message with the plugin's component name.

        Args:
            message: Log message.
            component: Component override.
            correlation_id: Correlation ID for tracing.

        """
        self._delegate.debug(
            message,
            component=component or self._component,
            correlation_id=correlation_id,
        )

    def info(
        self,
        message: str,
        *,
        component: str = "",
        correlation_id: str = "",
    ) -> None:
        """Log an INFO-level message with the plugin's component name.

        Args:
            message: Log message.
            component: Component override.
            correlation_id: Correlation ID for tracing.

        """
        self._delegate.info(
            message,
            component=component or self._component,
            correlation_id=correlation_id,
        )

    def warning(
        self,
        message: str,
        *,
        component: str = "",
        correlation_id: str = "",
    ) -> None:
        """Log a WARNING-level message with the plugin's component name.

        Args:
            message: Log message.
            component: Component override.
            correlation_id: Correlation ID for tracing.

        """
        self._delegate.warning(
            message,
            component=component or self._component,
            correlation_id=correlation_id,
        )

    def error(
        self,
        message: str,
        *,
        component: str = "",
        correlation_id: str = "",
    ) -> None:
        """Log an ERROR-level message with the plugin's component name.

        Args:
            message: Log message.
            component: Component override.
            correlation_id: Correlation ID for tracing.

        """
        self._delegate.error(
            message,
            component=component or self._component,
            correlation_id=correlation_id,
        )

    def critical(
        self,
        message: str,
        *,
        component: str = "",
        correlation_id: str = "",
    ) -> None:
        """Log a CRITICAL-level message with the plugin's component name.

        Args:
            message: Log message.
            component: Component override.
            correlation_id: Correlation ID for tracing.

        """
        self._delegate.critical(
            message,
            component=component or self._component,
            correlation_id=correlation_id,
        )


class PluginContext:
    """Isolated context for a single plugin.

    Each plugin receives its own ``PluginContext`` during the load
    phase.  The context is the only way for a plugin to interact
    with runtime services.  It enforces isolation by gating all
    access through defined interfaces and by becoming unusable
    after the plugin is unloaded (disposal).

    Implements the ``IPluginContext`` and ``IHealthCheck`` protocols.

    Args:
        plugin_id: Unique identifier of the plugin.
        event_bus: The runtime event bus.
        logger: The runtime logger (wrapped with the plugin's
            component name).
        service_registry: The runtime service registry for service
            resolution.

    """

    __slots__ = (
        "_disposed",
        "_event_bus",
        "_lock",
        "_logger",
        "_plugin_id",
        "_service_registry",
    )

    def __init__(
        self,
        *,
        plugin_id: str,
        event_bus: IEventBus,
        logger: ILogger,
        service_registry: IServiceRegistry,
    ) -> None:
        """Initialise the plugin context."""
        self._plugin_id: str = plugin_id
        self._event_bus: IEventBus = event_bus
        self._logger: _ScopedLogger = _ScopedLogger(
            logger, f"Plugin[{plugin_id}]"
        )
        self._service_registry: IServiceRegistry = service_registry
        self._lock: RLock = RLock()
        self._disposed: bool = False

    # -- IPluginContext protocol -----------------------------------------------

    def get_event_bus(self) -> IEventBus:
        """Return the event bus for publishing and subscribing to events.

        Returns:
            The runtime event bus.

        Raises:
            PluginIsolationError: If the context has been disposed.

        """
        self._check_disposed()
        return self._event_bus

    def get_logger(self) -> ILogger:
        """Return a logger scoped to this plugin.

        The returned logger automatically sets the component name to
        the plugin's identifier unless an explicit component is
        provided.

        Returns:
            A scoped structured logger instance.

        Raises:
            PluginIsolationError: If the context has been disposed.

        """
        self._check_disposed()
        return self._logger

    def get_service(self, service_type: type[T]) -> T:
        """Resolve a runtime service by its interface type.

        Args:
            service_type: The protocol/interface type to resolve.

        Returns:
            The registered implementation of the requested service.

        Raises:
            PluginIsolationError: If the context has been disposed.
            JochenXError: If no implementation is registered.

        """
        self._check_disposed()
        return self._service_registry.resolve(service_type)

    def get_plugin_id(self) -> str:
        """Return the unique identifier of the plugin owning this context.

        Returns:
            The plugin identifier.

        """
        return self._plugin_id

    # -- Lifecycle management --------------------------------------------------

    def dispose(self) -> None:
        """Dispose the context, preventing further access.

        Called by the plugin registry when the plugin is unloaded.
        After disposal, all service access methods raise
        ``PluginIsolationError``.
        """
        with self._lock:
            self._disposed = True

    def is_disposed(self) -> bool:
        """Check whether the context has been disposed.

        Returns:
            ``True`` if the context is no longer valid.

        """
        with self._lock:
            return self._disposed

    # -- IHealthCheck protocol -------------------------------------------------

    def check_health(self) -> HealthStatus:
        """Return the health status of the context.

        Returns:
            ``HEALTHY`` if the context is active,
            ``UNHEALTHY`` if it has been disposed.

        """
        with self._lock:
            if self._disposed:
                return HealthStatus.UNHEALTHY
            return HealthStatus.HEALTHY

    def get_component_name(self) -> str:
        """Return the component name.

        Returns:
            A string of the form ``"PluginContext[<plugin_id>]"``.

        """
        return f"{_COMPONENT_NAME}[{self._plugin_id}]"

    # -- Internal helpers ------------------------------------------------------

    def _check_disposed(self) -> None:
        """Raise ``PluginIsolationError`` if the context has been disposed."""
        with self._lock:
            if self._disposed:
                msg = (
                    f"Plugin context for '{self._plugin_id}' "
                    f"has been disposed"
                )
                raise PluginIsolationError(
                    msg,
                    plugin_id=self._plugin_id,
                    component=self.get_component_name(),
                )
