"""Plugin context protocol - the sandboxed runtime interface for plugins."""

from __future__ import annotations

from typing import TYPE_CHECKING, Protocol, TypeVar, runtime_checkable

if TYPE_CHECKING:
    from jochen_x.core.interfaces.event_bus import IEventBus
    from jochen_x.core.interfaces.logging import ILogger

__all__ = ["IPluginContext"]

T = TypeVar("T")


@runtime_checkable
class IPluginContext(Protocol):
    """Protocol for the isolated plugin context.

    Each plugin receives its own context instance.  The context is the
    only way for a plugin to interact with runtime services.  It
    enforces plugin isolation and provides access to runtime
    capabilities through defined interfaces only.
    """

    def get_event_bus(self) -> IEventBus:
        """Return the event bus for publishing and subscribing to events.

        Returns:
            The runtime event bus.

        """
        ...

    def get_logger(self) -> ILogger:
        """Return a logger scoped to this plugin.

        Returns:
            A structured logger instance.

        """
        ...

    def get_service(self, service_type: type[T]) -> T:
        """Resolve a runtime service by its interface type.

        Args:
            service_type: The protocol/interface type to resolve.

        Returns:
            The registered implementation of the requested service.

        Raises:
            JochenXError: If no implementation is registered.

        """
        ...

    def get_plugin_id(self) -> str:
        """Return the unique identifier of the plugin owning this context.

        Returns:
            The plugin identifier.

        """
        ...
