"""Plugin-scoped resource access.

Every plugin is given a dedicated resource root by the host at context-build
time. The :class:`PluginResources` façade is the only way for a plugin to
read icons, static assets, and translation files: it resolves paths only
within the injected root, rejects any attempt to escape it, and offers
platform-neutral helpers so plugins do not embed filesystem details.
"""

from __future__ import annotations

import json
from collections.abc import Mapping
from pathlib import Path
from typing import Any

from sdk.errors import PluginResourceError

_ICONS_DIRECTORY = "icons"
_ASSETS_DIRECTORY = "assets"
_TRANSLATIONS_DIRECTORY = "translations"
_TRANSLATION_SUFFIX = ".json"


class PluginResources:
    """Resolve and read files under a plugin's private resource root."""

    __slots__ = ("_root",)

    def __init__(self, root: Path) -> None:
        """Create the resource façade rooted at ``root``.

        Args:
            root: Existing directory that owns the plugin's static resources.
                The directory is created if missing.

        Raises:
            PluginResourceError: If ``root`` cannot be created or is not a
                directory.
        """
        try:
            resolved = Path(root)
            resolved.mkdir(parents=True, exist_ok=True)
        except OSError as error:
            raise PluginResourceError(
                f"Cannot prepare resource root: {error}"
            ) from error
        if not resolved.is_dir():
            raise PluginResourceError(f"Resource root is not a directory: {resolved}")
        self._root = resolved.resolve()

    @property
    def root(self) -> Path:
        """Return the resolved resource root path."""
        return self._root

    def path(self, *parts: str) -> Path:
        """Resolve a path beneath the resource root.

        Args:
            *parts: Path components. Absolute components and traversal
                sequences are rejected.

        Returns:
            The resolved absolute path within the resource root.

        Raises:
            PluginResourceError: If the resolved path escapes the root.
        """
        for part in parts:
            if not isinstance(part, str) or not part:
                raise PluginResourceError("Path components must be non-empty strings")
            if Path(part).is_absolute():
                raise PluginResourceError(f"Absolute paths are not allowed: {part!r}")
        candidate = self._root.joinpath(*parts).resolve()
        if candidate != self._root and self._root not in candidate.parents:
            raise PluginResourceError(
                f"Resource path escapes the plugin root: {'/'.join(parts)}"
            )
        return candidate

    def exists(self, *parts: str) -> bool:
        """Return whether the resolved resource path exists."""
        return self.path(*parts).exists()

    def read_bytes(self, *parts: str) -> bytes:
        """Read a resource as raw bytes.

        Raises:
            PluginResourceError: If the file cannot be read.
        """
        target = self.path(*parts)
        try:
            return target.read_bytes()
        except OSError as error:
            raise PluginResourceError(f"Cannot read resource {target}: {error}") from error

    def read_text(self, *parts: str, encoding: str = "utf-8") -> str:
        """Read a resource as decoded text.

        Raises:
            PluginResourceError: If the file cannot be read.
        """
        target = self.path(*parts)
        try:
            return target.read_text(encoding=encoding)
        except OSError as error:
            raise PluginResourceError(f"Cannot read resource {target}: {error}") from error

    def icon(self, name: str) -> Path:
        """Return the resolved path for ``icons/<name>``."""
        return self.path(_ICONS_DIRECTORY, name)

    def asset(self, name: str) -> Path:
        """Return the resolved path for ``assets/<name>``."""
        return self.path(_ASSETS_DIRECTORY, name)

    def translation(self, locale: str) -> Path:
        """Return the resolved path for ``translations/<locale>.json``."""
        if not locale or "/" in locale or "\\" in locale:
            raise PluginResourceError(f"Invalid locale: {locale!r}")
        return self.path(_TRANSLATIONS_DIRECTORY, f"{locale}{_TRANSLATION_SUFFIX}")

    def load_translation(self, locale: str) -> Mapping[str, str]:
        """Load ``translations/<locale>.json`` as a string-to-string mapping.

        Args:
            locale: Locale name (e.g. ``"en"``, ``"de"``); no path segments
                are allowed.

        Returns:
            A validated mapping of translation keys to translated values.

        Raises:
            PluginResourceError: If the file is missing, invalid JSON, or
                contains non-string values.
        """
        target = self.translation(locale)
        try:
            payload: Any = json.loads(target.read_text(encoding="utf-8"))
        except OSError as error:
            raise PluginResourceError(
                f"Missing translation file for locale {locale!r}: {error}"
            ) from error
        except json.JSONDecodeError as error:
            raise PluginResourceError(
                f"Malformed translation file for locale {locale!r}: {error}"
            ) from error
        if not isinstance(payload, Mapping):
            raise PluginResourceError(
                f"Translation file for {locale!r} is not a JSON object"
            )
        result: dict[str, str] = {}
        for key, value in payload.items():
            if not isinstance(key, str) or not isinstance(value, str):
                raise PluginResourceError(
                    f"Translation entries must be string-to-string ({key!r} -> {value!r})"
                )
            result[key] = value
        return result


__all__ = ["PluginResources"]
