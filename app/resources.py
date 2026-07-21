"""Application resource management with path safety and lifetime ownership.

:class:`ResourceManager` resolves on-disk resource paths beneath a single,
injected root (no hardcoded paths), guards against path traversal, and owns the
lifetime of runtime resources by delegating cleanup to a
:class:`app.di.DisposableRegistry`.
"""

from __future__ import annotations

import logging
from pathlib import Path

from core.environment import Environment
from core.exceptions import JochenXError

from app.di import Disposable, DisposableRegistry

_DEFAULT_RESOURCE_DIRECTORY = "resources"


class ResourceError(JochenXError):
    """Raised for invalid or unsafe resource access."""


class ResourceManager:
    """Resolves resource paths and owns disposable runtime resources."""

    def __init__(
        self,
        environment: Environment,
        disposables: DisposableRegistry,
        *,
        subdirectory: str = _DEFAULT_RESOURCE_DIRECTORY,
        logger: logging.Logger | None = None,
    ) -> None:
        """Create the resource manager and ensure its root exists.

        Args:
            environment: Resolved environment providing the application root.
            disposables: Registry that owns cleanup of tracked resources.
            subdirectory: Resource directory name relative to the root.
            logger: Optional logger for diagnostics.
        """
        self._disposables = disposables
        self._logger = logger or logging.getLogger("jochen_x.resources")
        self._root = (environment.root / subdirectory).resolve()
        self._root.mkdir(parents=True, exist_ok=True)

    @property
    def root(self) -> Path:
        """Return the resolved resource root directory."""
        return self._root

    def path(self, *parts: str) -> Path:
        """Resolve a resource path, rejecting any escape from the root.

        Args:
            *parts: Path components relative to the resource root.

        Returns:
            The resolved absolute path within the resource root.

        Raises:
            ResourceError: If the resolved path escapes the resource root.
        """
        candidate = self._root.joinpath(*parts).resolve()
        if candidate != self._root and self._root not in candidate.parents:
            raise ResourceError(f"Resource path escapes the resource root: {'/'.join(parts)}")
        return candidate

    def exists(self, *parts: str) -> bool:
        """Return whether the resolved resource path exists."""
        return self.path(*parts).exists()

    def read_bytes(self, *parts: str) -> bytes:
        """Read a resource as bytes.

        Raises:
            ResourceError: If the resource cannot be read.
        """
        target = self.path(*parts)
        try:
            return target.read_bytes()
        except OSError as error:
            raise ResourceError(f"Cannot read resource {target}: {error}") from error

    def read_text(self, *parts: str, encoding: str = "utf-8") -> str:
        """Read a resource as decoded text.

        Raises:
            ResourceError: If the resource cannot be read.
        """
        target = self.path(*parts)
        try:
            return target.read_text(encoding=encoding)
        except OSError as error:
            raise ResourceError(f"Cannot read resource {target}: {error}") from error

    def track(self, resource: Disposable) -> Disposable:
        """Track a disposable runtime resource for deterministic cleanup."""
        return self._disposables.register(resource)
