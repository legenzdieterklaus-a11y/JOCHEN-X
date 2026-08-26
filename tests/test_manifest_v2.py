"""Unit and integration tests for WP-02 Manifest v2 TOML Parser (AC-2, AC-11).

Tests verify:
- Full v2 manifest with all fields is parsed correctly
- Minimal v1 manifest (flat keys) still works
- Unknown fields are silently ignored (forwards compatibility)
- Invalid identifiers and version strings are rejected
- Backwards compatibility: v1 manifest produces valid PluginManifest
"""

from __future__ import annotations

import tempfile
import tomllib

import pytest
from pathlib import Path

from core.version import Version, VersionManager
from plugins.loader import PluginLoader, PluginManifest, _parse_manifest
from sdk.manifest import (
    PluginCategory,
    PluginMetadata,
    PluginPermission,
)


def _parse_toml_string(content: str) -> dict[str, object]:
    """Parse a TOML string into a dict."""
    return tomllib.loads(content)


# ---------------------------------------------------------------------------
# Unit Tests
# ---------------------------------------------------------------------------


def test_manifest_v2_parse_full() -> None:
    """AC-2: Full v2 manifest with all fields is parsed correctly."""
    toml_data = _parse_toml_string("""\
[plugin]
id = "com.example.full-plugin"
version = "2.1.0"
requires_application = "0.8.0"
api_version = "1.0.0"
category = "tool"
entry_point = "main"

[plugin.metadata]
display_name = "Full Plugin"
description = "A plugin with all v2 fields"
author = "Test Author"

[plugin.permissions]
capabilities = ["filesystem", "network"]

[plugin.dependencies]
requires = [
    { id = "core-services", version = ">=1.0.0" },
    { id = "helper-lib", version = ">=0.5.0" },
]
""")

    manifest = _parse_manifest(toml_data)

    assert manifest.identifier == "com.example.full-plugin"
    assert manifest.version == Version(2, 1, 0)
    assert manifest.required_application_version == Version(0, 8, 0)
    assert manifest.api_version == Version(1, 0, 0)
    assert manifest.category == "tool"
    assert manifest.entry_point == "main"
    assert manifest.metadata == {
        "display_name": "Full Plugin",
        "description": "A plugin with all v2 fields",
        "author": "Test Author",
    }
    assert manifest.permissions == ("filesystem", "network")
    assert len(manifest.dependencies) == 2
    assert manifest.dependencies[0] == {"id": "core-services", "version": ">=1.0.0"}
    assert manifest.dependencies[1] == {"id": "helper-lib", "version": ">=0.5.0"}


def test_manifest_v2_parse_minimal() -> None:
    """AC-2: Minimal v1 manifest (flat keys only) is parsed correctly."""
    toml_data = _parse_toml_string("""\
id = "simple-plugin"
version = "1.0.0"
requires_application = "0.8.0"
""")

    manifest = _parse_manifest(toml_data)

    assert manifest.identifier == "simple-plugin"
    assert manifest.version == Version(1, 0, 0)
    assert manifest.required_application_version == Version(0, 8, 0)
    assert manifest.api_version is None
    assert manifest.category == "general"
    assert manifest.entry_point == ""
    assert manifest.metadata == {}
    assert manifest.permissions == ()
    assert manifest.dependencies == ()


def test_manifest_v2_unknown_fields() -> None:
    """AC-2: Unknown fields are silently ignored (forwards compatibility)."""
    toml_data = _parse_toml_string("""\
[plugin]
id = "future-plugin"
version = "1.0.0"
requires_application = "0.8.0"
unknown_field = "should be ignored"
future_feature = true

[plugin.metadata]
display_name = "Future"
description = "Plugin with unknown fields"
author = "Author"
custom_key = "ignored"

[plugin.unknown_section]
data = "also ignored"
""")

    manifest = _parse_manifest(toml_data)

    assert manifest.identifier == "future-plugin"
    assert manifest.version == Version(1, 0, 0)
    assert manifest.metadata["display_name"] == "Future"
    assert manifest.metadata.get("custom_key") == "ignored"


def test_manifest_v2_validation_errors() -> None:
    """AC-2: Invalid version strings are detected and rejected."""
    invalid_version = _parse_toml_string("""\
[plugin]
id = "bad-version"
version = "not-a-version"
requires_application = "0.8.0"
""")
    with pytest.raises(ValueError):
        _parse_manifest(invalid_version)

    invalid_app_version = _parse_toml_string("""\
[plugin]
id = "bad-app-version"
version = "1.0.0"
requires_application = "abc"
""")
    with pytest.raises(ValueError):
        _parse_manifest(invalid_app_version)

    invalid_api_version = _parse_toml_string("""\
[plugin]
id = "bad-api-version"
version = "1.0.0"
requires_application = "0.8.0"
api_version = "invalid"
""")
    with pytest.raises(ValueError):
        _parse_manifest(invalid_api_version)

    missing_id = _parse_toml_string("""\
[plugin]
version = "1.0.0"
requires_application = "0.8.0"
""")
    with pytest.raises(KeyError):
        _parse_manifest(missing_id)


# ---------------------------------------------------------------------------
# Integration Tests
# ---------------------------------------------------------------------------


def test_backwards_compatibility_v1_manifest() -> None:
    """AC-11: Plugin with v1 manifest (flat keys) works through full discovery."""
    with tempfile.TemporaryDirectory() as tmp:
        plugin_dir = Path(tmp) / "legacy-plugin"
        plugin_dir.mkdir()
        (plugin_dir / "plugin.toml").write_text(
            'id = "legacy-plugin"\n'
            'version = "1.0.0"\n'
            'requires_application = "0.8.0"\n',
            encoding="utf-8",
        )

        versions = VersionManager(Version(0, 8, 0))
        loader = PluginLoader(Path(tmp), versions)
        manifests = loader.discover()

        assert len(manifests) == 1
        m = manifests[0]
        assert m.identifier == "legacy-plugin"
        assert m.version == Version(1, 0, 0)
        assert m.required_application_version == Version(0, 8, 0)
        assert m.api_version is None
        assert m.category == "general"
        assert m.entry_point == ""
        assert m.metadata == {}
        assert m.permissions == ()
        assert m.dependencies == ()

        metadata = PluginMetadata.from_loader_manifest(
            m,
            name="Legacy",
            author="Author",
            description="v1 compat test",
            api_version="1.0.0",
        )
        assert metadata.identifier == "legacy-plugin"
        assert metadata.version == "1.0.0"
        assert metadata.name == "Legacy"
        assert metadata.entry_point == ""
        assert metadata.permissions == frozenset()
        assert metadata.dependencies == ()


def test_manifest_v2_discovery_full() -> None:
    """Full v2 manifest is discovered and all fields are preserved."""
    with tempfile.TemporaryDirectory() as tmp:
        plugin_dir = Path(tmp) / "full-v2"
        plugin_dir.mkdir()
        (plugin_dir / "plugin.toml").write_text(
            '[plugin]\n'
            'id = "full-v2"\n'
            'version = "2.0.0"\n'
            'requires_application = "0.8.0"\n'
            'api_version = "1.0.0"\n'
            'category = "tool"\n'
            'entry_point = "main"\n'
            '\n'
            '[plugin.metadata]\n'
            'display_name = "Full V2"\n'
            'description = "v2 test"\n'
            'author = "Test"\n'
            '\n'
            '[plugin.permissions]\n'
            'capabilities = ["filesystem", "network"]\n'
            '\n'
            '[plugin.dependencies]\n'
            'requires = [\n'
            '    { id = "dep-a", version = ">=1.0.0" },\n'
            ']\n',
            encoding="utf-8",
        )

        versions = VersionManager(Version(0, 8, 0))
        loader = PluginLoader(Path(tmp), versions)
        manifests = loader.discover()

        assert len(manifests) == 1
        m = manifests[0]
        assert m.identifier == "full-v2"
        assert m.api_version == Version(1, 0, 0)
        assert m.category == "tool"
        assert m.entry_point == "main"
        assert m.metadata["display_name"] == "Full V2"
        assert m.permissions == ("filesystem", "network")
        assert m.dependencies[0]["id"] == "dep-a"


def test_manifest_v2_from_loader_manifest_mapping() -> None:
    """V2 loader manifest fields map correctly to PluginMetadata."""
    manifest = PluginManifest(
        identifier="mapped-plugin",
        version=Version(1, 0, 0),
        required_application_version=Version(0, 8, 0),
        api_version=Version(1, 0, 0),
        category="tool",
        entry_point="main_module",
        metadata={
            "display_name": "Mapped Plugin",
            "description": "Tests v2 mapping",
            "author": "Mapper",
        },
        permissions=("filesystem", "network"),
        dependencies=({"id": "dep-x", "version": ">=2.0.0"},),
    )

    metadata = PluginMetadata.from_loader_manifest(manifest)

    assert metadata.identifier == "mapped-plugin"
    assert metadata.name == "Mapped Plugin"
    assert metadata.author == "Mapper"
    assert metadata.description == "Tests v2 mapping"
    assert metadata.api_version == "1.0.0"
    assert metadata.category == PluginCategory.TOOL
    assert metadata.entry_point == "main_module"
    assert PluginPermission.FILESYSTEM in metadata.permissions
    assert PluginPermission.NETWORK in metadata.permissions
    assert len(metadata.dependencies) == 1
    assert metadata.dependencies[0].identifier == "dep-x"
    assert metadata.dependencies[0].minimum_version == "2.0.0"


def test_manifest_v2_from_loader_manifest_keyword_override() -> None:
    """Explicit keyword args take precedence over manifest metadata."""
    manifest = PluginManifest(
        identifier="override-test",
        version=Version(1, 0, 0),
        required_application_version=Version(0, 8, 0),
        api_version=Version(1, 0, 0),
        metadata={
            "display_name": "Manifest Name",
            "author": "Manifest Author",
            "description": "Manifest Desc",
        },
    )

    metadata = PluginMetadata.from_loader_manifest(
        manifest,
        name="Override Name",
        author="Override Author",
        description="Override Desc",
        api_version="1.0.0",
    )

    assert metadata.name == "Override Name"
    assert metadata.author == "Override Author"
    assert metadata.description == "Override Desc"
