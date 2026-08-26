"""Public plugin service access layer.

Plugins never see the foundation's :class:`core.registry.ServiceRegistry`.
Instead, the host provides a whitelisted mapping of SDK-visible service
types to their live instances, and plugins resolve them through
:class:`PluginServices`. The layer is typed, immutable-in-intent, and
permission-aware.

Design notes
------------

* Service *keys* are Python types (classes or protocols) so plugin authors
  keep static typing benefits.
* The mapping is built by the host during context construction; plugins can
  never mutate it and cannot enumerate services beyond what the host
  intentionally exposes.
* Permission enforcement is delegated to an injected callable so this
  module contains no policy of its own and stays cleanly testable.
"""

from __future__ import annotations

from collections.abc import Callable, Mapping
from typing import Any, TypeVar, cast

from sdk.errors import PluginPermissionError, PluginServiceNotAvailableError
from sdk.manifest import PluginPermission

T = TypeVar("T")

ServicePermissionCheck = Callable[[type, PluginPermission], None]
"""Callable invoked before each service resolution.

Implementations should raise :class:`PluginPermissionError` when access to
``service_type`` is denied.
"""


class PluginServices:
    """Read-only, typed service resolution façade for plugins.

    Instances are typically constructed by :class:`sdk.context.PluginContextBuilder`
    and passed to the plugin through the :class:`sdk.context.PluginContext`.
    """

    __slots__ = ("_permission_check", "_services")

    def __init__(
        self,
        services: Mapping[type, Any] | None = None,
        *,
        permission_check: ServicePermissionCheck | None = None,
    ) -> None:
        """Create the service façade.

        Args:
            services: Immutable mapping of service type keys to instances.
                Entries are copied into a private dict so mutations to the
                original mapping never affect the plugin's view.
            permission_check: Optional callback consulted before each
                :meth:`get` call. Receives the requested service type and
                :class:`PluginPermission.SERVICES`.
        """
        self._services: dict[type, Any] = dict(services or {})
        self._permission_check = permission_check

    def has(self, service_type: type) -> bool:
        """Return whether ``service_type`` is available to the plugin."""
        return service_type in self._services

    def keys(self) -> tuple[type, ...]:
        """Return the tuple of exposed service type keys."""
        return tuple(self._services.keys())

    def get(self, service_type: type[T]) -> T:
        """Resolve and return the service registered under ``service_type``.

        Args:
            service_type: Public service type or protocol.

        Returns:
            The registered service instance.

        Raises:
            PluginServiceNotAvailableError: If no service is registered for
                ``service_type``.
            PluginPermissionError: If a permission check rejects access.
        """
        self._ensure_permission(service_type)
        try:
            return cast(T, self._services[service_type])
        except KeyError as error:
            raise PluginServiceNotAvailableError(
                f"Service is not available to this plugin: {service_type.__name__}"
            ) from error

    def get_optional(self, service_type: type[T]) -> T | None:
        """Resolve ``service_type`` if available; return ``None`` otherwise.

        Raises:
            PluginPermissionError: If a permission check rejects access.
        """
        self._ensure_permission(service_type)
        return self._services.get(service_type)

    def snapshot(self) -> dict[str, str]:
        """Return a diagnostic mapping of service name to type name.

        The snapshot never returns instances; it only describes which
        services are visible so plugins can log or audit their available
        surface without leaking references.
        """
        return {key.__name__: type(value).__name__ for key, value in self._services.items()}

    def _ensure_permission(self, service_type: type) -> None:
        """Delegate to the injected permission check when configured."""
        if self._permission_check is None:
            return
        try:
            self._permission_check(service_type, PluginPermission.SERVICES)
        except PluginPermissionError:
            raise
        except Exception as error:  # normalise any check failure to SDK error
            raise PluginPermissionError(
                f"Permission check failed for service {service_type.__name__}: {error}"
            ) from error


__all__ = ["PluginServices", "ServicePermissionCheck"]
