"""JOCHEN X Enterprise Plugin SDK.

This package is the sole official programming interface for JOCHEN X plugin
authors. Every public API a plugin needs is re-exported here:

* Version and API constants (:data:`SDK_VERSION`, :data:`SDK_API_VERSION`).
* Plugin base classes (:class:`Plugin`, :class:`BackgroundPlugin`,
  :class:`UIPlugin`, :class:`ToolPlugin`, :class:`WorkflowPlugin`).
* Manifest models (:class:`PluginMetadata`, :class:`PluginCategory`,
  :class:`PluginPermission`, :class:`PluginDependency`,
  :class:`SignatureStatus`).
* Runtime context (:class:`PluginContext`, :class:`PluginContextBuilder`).
* Access façades (:class:`PluginLogger`, :class:`PluginEventBus`,
  :class:`PluginServices`, :class:`PluginConfig`, :class:`PluginResources`).
* Exception hierarchy under :class:`PluginSDKError`.

The package intentionally does not export any foundation-internal type:
plugin code that stays inside ``sdk`` never breaks when the foundation
implementation evolves.
"""

from __future__ import annotations

from sdk.config import (
    FilePluginConfigStorage,
    InMemoryPluginConfigStorage,
    PluginConfig,
    PluginConfigStorage,
    Validator,
)
from sdk.context import PluginContext, PluginContextBuilder
from sdk.errors import (
    PluginConfigurationError,
    PluginDependencyError,
    PluginEventError,
    PluginLifecycleError,
    PluginManifestError,
    PluginPermissionError,
    PluginResourceError,
    PluginSDKError,
    PluginServiceNotAvailableError,
)
from sdk.events import (
    EventBusPort,
    PermissionCheck,
    PluginEvent,
    PluginEventBus,
    PluginEventHandler,
    Subscription,
)
from sdk.logging import PluginLogger
from sdk.manifest import (
    PluginCategory,
    PluginDependency,
    PluginMetadata,
    PluginPermission,
    SignatureStatus,
    validate_identifier,
    validate_semver,
)
from sdk.plugin import (
    BackgroundPlugin,
    Plugin,
    PluginLifecycleState,
    PluginRuntime,
    ToolPlugin,
    UIPlugin,
    WorkflowPlugin,
)
from sdk.resources import PluginResources
from sdk.services import PluginServices, ServicePermissionCheck
from sdk.version import (
    SDK_API_VERSION,
    SDK_API_VERSION_INFO,
    SDK_NAME,
    SDK_VERSION,
    SDK_VERSION_INFO,
    ApiVersion,
)

__all__ = [
    # Version constants
    "SDK_API_VERSION",
    "SDK_API_VERSION_INFO",
    "SDK_NAME",
    "SDK_VERSION",
    "SDK_VERSION_INFO",
    "ApiVersion",
    # Manifest
    "PluginCategory",
    "PluginDependency",
    "PluginMetadata",
    "PluginPermission",
    "SignatureStatus",
    "validate_identifier",
    "validate_semver",
    # Runtime context and façades
    "EventBusPort",
    "FilePluginConfigStorage",
    "InMemoryPluginConfigStorage",
    "PermissionCheck",
    "PluginConfig",
    "PluginConfigStorage",
    "PluginContext",
    "PluginContextBuilder",
    "PluginEvent",
    "PluginEventBus",
    "PluginEventHandler",
    "PluginLogger",
    "PluginResources",
    "PluginServices",
    "ServicePermissionCheck",
    "Subscription",
    "Validator",
    # Plugin base classes and lifecycle
    "BackgroundPlugin",
    "Plugin",
    "PluginLifecycleState",
    "PluginRuntime",
    "ToolPlugin",
    "UIPlugin",
    "WorkflowPlugin",
    # Error taxonomy
    "PluginConfigurationError",
    "PluginDependencyError",
    "PluginEventError",
    "PluginLifecycleError",
    "PluginManifestError",
    "PluginPermissionError",
    "PluginResourceError",
    "PluginSDKError",
    "PluginServiceNotAvailableError",
]

__version__ = SDK_VERSION
"""Convenience alias mirroring :data:`SDK_VERSION` for tooling compatibility."""
