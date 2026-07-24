"""Public SDK exception taxonomy.

Every exception a plugin can raise or catch through the SDK derives from
:class:`PluginSDKError`. The taxonomy is deliberately shallow so plugin
authors can write meaningful ``except`` clauses without needing knowledge of
foundation-internal error types.

Framework-internal exceptions (``core.exceptions.JochenXError`` and its
subclasses) are intentionally *not* re-exported: hosts translate them into
SDK exceptions at the SDK/foundation boundary, so plugin code never depends
on internal error types.
"""

from __future__ import annotations


class PluginSDKError(Exception):
    """Root exception for every error surfaced through the Plugin SDK.

    All SDK exceptions inherit from this class so plugin authors can catch
    the entire SDK error family with a single ``except PluginSDKError``.
    """


class PluginManifestError(PluginSDKError):
    """Raised when a plugin manifest is invalid or fails validation."""


class PluginConfigurationError(PluginSDKError):
    """Raised for invalid, unloadable, or unsavable plugin configuration."""


class PluginPermissionError(PluginSDKError):
    """Raised when a plugin attempts an action it is not permitted to perform."""


class PluginLifecycleError(PluginSDKError):
    """Raised for illegal or out-of-order plugin lifecycle transitions."""


class PluginDependencyError(PluginSDKError):
    """Raised when a declared plugin dependency cannot be satisfied."""


class PluginResourceError(PluginSDKError):
    """Raised for missing, unreadable, or path-unsafe plugin resources."""


class PluginServiceNotAvailableError(PluginSDKError):
    """Raised when a plugin requests an SDK service that is not provided."""


class PluginEventError(PluginSDKError):
    """Raised for invalid event names, handlers, or subscription operations."""


__all__ = [
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
