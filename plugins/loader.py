"""Manifest-only plugin discovery with compatibility validation."""

from dataclasses import dataclass
from pathlib import Path
import tomllib

from core.version import Version, VersionManager


@dataclass(frozen=True, slots=True)
class PluginManifest:
    """Validated inert plugin manifest."""
    identifier: str
    version: Version
    required_application_version: Version


class PluginLoader:
    """Discovers manifests but never imports or runs plugin code."""
    def __init__(self, directory: Path, versions: VersionManager) -> None:
        self._directory, self._versions = directory, versions
    def discover(self) -> tuple[PluginManifest, ...]:
        """Read compatible `plugin.toml` files from direct plugin directories."""
        if not self._directory.exists():
            return ()
        manifests: list[PluginManifest] = []
        for path in self._directory.glob("*/plugin.toml"):
            with path.open("rb") as handle:
                data = tomllib.load(handle)
            manifest = PluginManifest(str(data["id"]), Version.parse(str(data["version"])), Version.parse(str(data["requires_application"])))
            if self._versions.is_compatible(manifest.required_application_version):
                manifests.append(manifest)
        return tuple(manifests)
