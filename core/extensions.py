"""Stable contracts for inert extensions; implementations are host supplied.

The formally defined extension points are enumerated in
:class:`ExtensionPoint`; each point is bound to its stable contract via
:data:`EXTENSION_POINT_CONTRACTS`. Plugins register new functionality at
these points through the host-owned :class:`ExtensionRegistry` — additively,
without altering any existing contract.
"""

from collections.abc import Mapping
from enum import StrEnum
from threading import RLock
from types import MappingProxyType
from typing import Any, Protocol


class PluginExtension(Protocol):
    identifier: str


class ToolExtension(Protocol):
    identifier: str


class UIExtension(Protocol):
    identifier: str


class CommandExtension(Protocol):
    identifier: str


class WorkflowExtension(Protocol):
    identifier: str


class ExtensionPoint(StrEnum):
    """Exhaustive set of formally defined extension points."""

    TOOLS = "tools"
    UI = "ui"
    COMMANDS = "commands"
    WORKFLOWS = "workflows"


EXTENSION_POINT_CONTRACTS: Mapping[ExtensionPoint, type] = MappingProxyType({
    ExtensionPoint.TOOLS: ToolExtension,
    ExtensionPoint.UI: UIExtension,
    ExtensionPoint.COMMANDS: CommandExtension,
    ExtensionPoint.WORKFLOWS: WorkflowExtension,
})
"""Read-only binding of each extension point to its stable contract."""


class ExtensionRegistry:
    """Thread-safe registry binding extensions to the defined extension points.

    Registration is strictly additive: the registry never mutates an
    extension and never alters the point contracts. Unknown points are
    rejected with ``ValueError`` (via :class:`ExtensionPoint`), extensions
    without a usable ``identifier`` with ``TypeError``.
    """

    def __init__(self) -> None:
        self._extensions: dict[ExtensionPoint, dict[str, Any]] = {
            point: {} for point in ExtensionPoint
        }
        self._lock = RLock()

    def register(self, point: ExtensionPoint | str, extension: Any) -> None:
        """Register ``extension`` at ``point``.

        Raises:
            ValueError: If ``point`` is not a defined extension point, or an
                extension with the same identifier is already registered there.
            TypeError: If the extension lacks a non-empty string ``identifier``.
        """
        resolved = ExtensionPoint(point)
        identifier = getattr(extension, "identifier", None)
        if not isinstance(identifier, str) or not identifier:
            raise TypeError("Extension must define a non-empty string 'identifier'")
        with self._lock:
            registered = self._extensions[resolved]
            if identifier in registered:
                raise ValueError(
                    f"Extension already registered at {resolved.value!r}: {identifier}"
                )
            registered[identifier] = extension

    def extensions(self, point: ExtensionPoint | str) -> tuple[Any, ...]:
        """Return all extensions registered at ``point``, in registration order."""
        resolved = ExtensionPoint(point)
        with self._lock:
            return tuple(self._extensions[resolved].values())

    def find(self, point: ExtensionPoint | str, identifier: str) -> Any | None:
        """Return the extension registered at ``point`` under ``identifier``."""
        resolved = ExtensionPoint(point)
        with self._lock:
            return self._extensions[resolved].get(identifier)


__all__ = [
    "CommandExtension",
    "EXTENSION_POINT_CONTRACTS",
    "ExtensionPoint",
    "ExtensionRegistry",
    "PluginExtension",
    "ToolExtension",
    "UIExtension",
    "WorkflowExtension",
]
