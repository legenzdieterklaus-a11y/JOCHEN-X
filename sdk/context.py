"""Secure plugin runtime context.

The :class:`PluginContext` is the single, immutable aggregate that a plugin
receives at attach time. It exposes only the SDK-defined façades:

* :class:`sdk.logging.PluginLogger`
* :class:`sdk.events.PluginEventBus`
* :class:`sdk.services.PluginServices`
* :class:`sdk.config.PluginConfig`
* :class:`sdk.resources.PluginResources`

The context deliberately does not expose the foundation's
:class:`app.context.ApplicationContext`, :class:`core.registry.ServiceRegistry`,
or any other framework-internal type. Hosts construct a context using
:class:`PluginContextBuilder`, which enforces the required injections and
applies permission-aware wrapping automatically.
"""

from __future__ import annotations

import logging
from collections.abc import Callable, Mapping
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from sdk.config import PluginConfig, PluginConfigStorage
from sdk.errors import PluginPermissionError
from sdk.events import EventBusPort, PluginEventBus
from sdk.logging import PluginLogger
from sdk.manifest import PluginMetadata, PluginPermission
from sdk.resources import PluginResources
from sdk.services import PluginServices
from sdk.version import SDK_API_VERSION


@dataclass(frozen=True, slots=True)
class PluginContext:
    """Immutable, fully-wired runtime context for a plugin.

    Attributes:
        metadata: The validated plugin metadata.
        logger: Plugin-scoped structured logger.
        events: Plugin-scoped event bus wrapper.
        services: Plugin-scoped service access layer.
        config: Plugin-owned configuration store.
        resources: Plugin-scoped resource resolver.
        application_version: The host application's semver.
        api_version: The SDK API version implemented by the host.
        metadata_view: Read-only informational mapping combining application
            and SDK versions with the plugin's manifest identifier.
    """

    metadata: PluginMetadata
    logger: PluginLogger
    events: PluginEventBus
    services: PluginServices
    config: PluginConfig
    resources: PluginResources
    application_version: str
    api_version: str
    metadata_view: Mapping[str, Any] = field(default_factory=dict)


class PluginContextBuilder:
    """Fluent, host-side builder that produces a :class:`PluginContext`.

    The builder validates every injection before assembling the context so
    plugins never receive a half-configured runtime. Permission enforcement
    is wired automatically: when a permission checker is registered, all
    event and service accesses are gated on the plugin's declared
    permissions.
    """

    def __init__(self, metadata: PluginMetadata) -> None:
        """Create a builder bound to a plugin's metadata.

        Args:
            metadata: The plugin metadata that will be exposed on the
                resulting context.
        """
        self._metadata = metadata
        self._event_bus: EventBusPort | None = None
        self._event_type: type | None = None
        self._service_map: dict[type, Any] = {}
        self._config_storage: PluginConfigStorage | None = None
        self._config_defaults: dict[str, Any] = {}
        self._config_validators: dict[str, Callable[[Any], None]] = {}
        self._resources_root: Path | None = None
        self._base_logger: logging.Logger | None = None
        self._application_version: str = "0.7.0"
        self._api_version: str = SDK_API_VERSION
        self._extra_view: dict[str, Any] = {}

    def with_event_bus(
        self,
        bus: EventBusPort,
        *,
        event_type: type,
    ) -> PluginContextBuilder:
        """Attach the underlying event bus and its transport event type."""
        self._event_bus = bus
        self._event_type = event_type
        return self

    def with_service(self, service_type: type, instance: Any) -> PluginContextBuilder:
        """Expose a single service to the plugin under the given key."""
        self._service_map[service_type] = instance
        return self

    def with_services(self, services: Mapping[type, Any]) -> PluginContextBuilder:
        """Expose a batch of services to the plugin."""
        self._service_map.update(services)
        return self

    def with_config_storage(self, storage: PluginConfigStorage) -> PluginContextBuilder:
        """Attach the configuration storage backend."""
        self._config_storage = storage
        return self

    def with_config_defaults(self, defaults: Mapping[str, Any]) -> PluginContextBuilder:
        """Register default configuration values."""
        self._config_defaults.update(defaults)
        return self

    def with_config_validators(
        self, validators: Mapping[str, Callable[[Any], None]]
    ) -> PluginContextBuilder:
        """Register configuration validators."""
        self._config_validators.update(validators)
        return self

    def with_resources_root(self, root: Path) -> PluginContextBuilder:
        """Attach the plugin's private resource root directory."""
        self._resources_root = Path(root)
        return self

    def with_logger(self, logger: logging.Logger) -> PluginContextBuilder:
        """Attach the base logger from which the plugin logger is derived."""
        self._base_logger = logger
        return self

    def with_application_version(self, version: str) -> PluginContextBuilder:
        """Set the host application's version string exposed on the context."""
        self._application_version = version
        return self

    def with_api_version(self, api_version: str) -> PluginContextBuilder:
        """Override the SDK API version reported on the context."""
        self._api_version = api_version
        return self

    def with_metadata_view(self, view: Mapping[str, Any]) -> PluginContextBuilder:
        """Attach an additional read-only informational view."""
        self._extra_view.update(view)
        return self

    def build(self) -> PluginContext:
        """Assemble the immutable :class:`PluginContext`.

        Returns:
            A fully-injected context wired for the target plugin.

        Raises:
            ValueError: If any mandatory injection is missing.
        """
        if self._event_bus is None or self._event_type is None:
            raise ValueError("An event bus and event_type must be provided")
        if self._config_storage is None:
            raise ValueError("A configuration storage backend must be provided")
        if self._resources_root is None:
            raise ValueError("A resource root must be provided")

        plugin_id = self._metadata.identifier
        permitted = self._metadata.permissions

        def permission_check(permission: PluginPermission) -> None:
            if permission in permitted:
                return
            raise PluginPermissionError(
                f"Plugin {plugin_id!r} lacks permission {permission.value!r}"
            )

        def service_permission_check(_service_type: type, permission: PluginPermission) -> None:
            permission_check(permission)

        logger = PluginLogger(plugin_id, base_logger=self._base_logger)
        events = PluginEventBus(
            plugin_id,
            self._event_bus,
            event_type=self._event_type,
            permission_check=permission_check,
        )
        services = PluginServices(
            self._service_map,
            permission_check=service_permission_check,
        )
        config = PluginConfig(
            plugin_id,
            self._config_storage,
            defaults=self._config_defaults,
            validators=self._config_validators,
        )
        resources = PluginResources(self._resources_root)

        metadata_view: dict[str, Any] = {
            "plugin_id": plugin_id,
            "plugin_version": self._metadata.version,
            "application_version": self._application_version,
            "api_version": self._api_version,
        }
        metadata_view.update(self._extra_view)

        return PluginContext(
            metadata=self._metadata,
            logger=logger,
            events=events,
            services=services,
            config=config,
            resources=resources,
            application_version=self._application_version,
            api_version=self._api_version,
            metadata_view=metadata_view,
        )


__all__ = ["PluginContext", "PluginContextBuilder"]
