"""Plugin-related exceptions."""

from __future__ import annotations

from jochen_x.core.exceptions.base import JochenXError

__all__ = [
    "PluginError",
    "PluginIsolationError",
    "PluginLifecycleError",
    "PluginLoadError",
    "PluginNotFoundError",
]


class PluginError(JochenXError):
    """General plugin error.

    Args:
        message: Human-readable error description.
        plugin_id: Identifier of the affected plugin.
        correlation_id: Correlation ID for cross-component tracing.
        component: Name of the component that raised the error.

    """

    def __init__(
        self,
        message: str,
        *,
        plugin_id: str = "",
        correlation_id: str = "",
        component: str = "",
    ) -> None:
        """Initialise with plugin identifier and tracing metadata."""
        self.plugin_id: str = plugin_id
        super().__init__(
            message,
            correlation_id=correlation_id,
            component=component,
        )


class PluginLoadError(PluginError):
    """A plugin failed to load.

    Args:
        message: Human-readable error description.
        plugin_id: Identifier of the affected plugin.
        correlation_id: Correlation ID for cross-component tracing.
        component: Name of the component that raised the error.

    """


class PluginIsolationError(PluginError):
    """Plugin isolation boundary was breached.

    Args:
        message: Human-readable error description.
        plugin_id: Identifier of the affected plugin.
        correlation_id: Correlation ID for cross-component tracing.
        component: Name of the component that raised the error.

    """


class PluginLifecycleError(PluginError):
    """An illegal plugin lifecycle transition was attempted.

    Args:
        message: Human-readable error description.
        plugin_id: Identifier of the affected plugin.
        from_state: The current state of the plugin.
        to_action: The action that was attempted.
        correlation_id: Correlation ID for cross-component tracing.
        component: Name of the component that raised the error.

    """

    def __init__(  # noqa: PLR0913
        self,
        message: str,
        *,
        plugin_id: str = "",
        from_state: str = "",
        to_action: str = "",
        correlation_id: str = "",
        component: str = "",
    ) -> None:
        """Initialise with lifecycle transition details."""
        self.from_state: str = from_state
        self.to_action: str = to_action
        super().__init__(
            message,
            plugin_id=plugin_id,
            correlation_id=correlation_id,
            component=component,
        )


class PluginNotFoundError(PluginError):
    """A plugin was not found in the registry.

    Args:
        message: Human-readable error description.
        plugin_id: Identifier of the plugin that was not found.
        correlation_id: Correlation ID for cross-component tracing.
        component: Name of the component that raised the error.

    """
