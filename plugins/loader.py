"""Manifest-only plugin discovery with compatibility validation."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
import tomllib

from core.version import Version, VersionManager


@dataclass(frozen=True, slots=True)
class PluginManifest:
    """Validated inert plugin manifest with v2 field support.

    V1 fields (identifier, version, required_application_version) are always
    present.  V2 fields are optional with safe defaults so manifests parsed
    from legacy ``plugin.toml`` files remain valid without modification.
    """

    identifier: str
    version: Version
    required_application_version: Version
    api_version: Version | None = None
    category: str = "general"
    entry_point: str = ""
    metadata: dict[str, str] = field(default_factory=dict)
    permissions: tuple[str, ...] = ()
    dependencies: tuple[dict[str, str], ...] = ()


@dataclass(frozen=True, slots=True)
class PluginCatalog:
    """Authoritative immutable snapshot of bootstrap-discovered plugins."""

    identifiers: tuple[str, ...]

    @property
    def count(self) -> int:
        """Return the number of discovered compatible plugins."""
        return len(self.identifiers)


class PluginLoader:
    """Discovers manifests but never imports or runs plugin code."""

    def __init__(self, directory: Path, versions: VersionManager) -> None:
        self._directory, self._versions = directory, versions

    def discover(self) -> tuple[PluginManifest, ...]:
        """Read compatible ``plugin.toml`` files from direct plugin directories."""
        return self.discover_report()[0]

    def discover_report(
        self,
    ) -> tuple[tuple[PluginManifest, ...], tuple[PluginManifest, ...]]:
        """Read all manifests in one manifest-only pass.

        Returns:
            A ``(compatible, incompatible)`` pair; incompatible manifests are
            those whose required application version is not satisfied. No
            plugin code is imported in either case.
        """
        if not self._directory.exists():
            return (), ()
        compatible: list[PluginManifest] = []
        incompatible: list[PluginManifest] = []
        for path in self._directory.glob("*/plugin.toml"):
            with path.open("rb") as handle:
                data = tomllib.load(handle)
            manifest = _parse_manifest(data)
            if self._versions.is_compatible(manifest.required_application_version):
                compatible.append(manifest)
            else:
                incompatible.append(manifest)
        return tuple(compatible), tuple(incompatible)


def _parse_manifest(data: dict[str, object]) -> PluginManifest:
    """Parse a v1 or v2 ``plugin.toml`` into a :class:`PluginManifest`.

    V2 manifests nest all fields under a ``[plugin]`` table.  V1 manifests
    use flat top-level keys.  Unknown fields are silently ignored (forwards
    compatibility).

    Raises:
        KeyError: When required fields (``id``, ``version``,
            ``requires_application``) are missing.
        ValueError: When a version string cannot be parsed.
    """
    plugin: dict[str, object] = (
        data["plugin"]  # type: ignore[assignment]
        if "plugin" in data and isinstance(data.get("plugin"), dict)
        else data
    )

    identifier = str(plugin["id"])
    version = Version.parse(str(plugin["version"]))
    required = Version.parse(str(plugin["requires_application"]))

    api_version: Version | None = None
    if "api_version" in plugin:
        api_version = Version.parse(str(plugin["api_version"]))

    category = str(plugin.get("category", "general"))
    entry_point = str(plugin.get("entry_point", ""))

    metadata_raw = plugin.get("metadata", {})
    metadata: dict[str, str] = {}
    if isinstance(metadata_raw, dict):
        metadata = {str(k): str(v) for k, v in metadata_raw.items()}

    permissions_raw = plugin.get("permissions", {})
    permissions: tuple[str, ...] = ()
    if isinstance(permissions_raw, dict):
        caps = permissions_raw.get("capabilities", ())
        if isinstance(caps, (list, tuple)):
            permissions = tuple(str(c) for c in caps)

    dependencies_raw = plugin.get("dependencies", {})
    dependencies: tuple[dict[str, str], ...] = ()
    if isinstance(dependencies_raw, dict):
        requires = dependencies_raw.get("requires", ())
        if isinstance(requires, (list, tuple)):
            deps: list[dict[str, str]] = []
            for dep in requires:
                if isinstance(dep, dict):
                    deps.append({
                        "id": str(dep.get("id", "")),
                        "version": str(dep.get("version", "")),
                    })
            dependencies = tuple(deps)

    return PluginManifest(
        identifier=identifier,
        version=version,
        required_application_version=required,
        api_version=api_version,
        category=category,
        entry_point=entry_point,
        metadata=metadata,
        permissions=permissions,
        dependencies=dependencies,
    )


__all__ = [
    "PluginCatalog",
    "PluginLoader",
    "PluginManifest",
]
