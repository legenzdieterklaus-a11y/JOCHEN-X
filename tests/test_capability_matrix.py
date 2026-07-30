"""Unit tests for WP-01 Capability Matrix (AC-1).

Tests verify:
- 10 stable capability identifiers are defined
- Default-deny semantics for non-granted capabilities
- Mapping to existing PluginPermission values
"""

from sdk.manifest import (
    CAPABILITY_PERMISSION_MAP,
    Capability,
    PluginPermission,
    is_capability_granted,
)


def test_capability_identifiers() -> None:
    """AC-1: 10 capability identifiers defined as stable string constants."""
    expected_identifiers = {
        "filesystem",
        "network",
        "clipboard",
        "notifications",
        "browser",
        "settings",
        "terminal",
        "ai",
        "camera",
        "audio",
    }

    assert len(Capability) == 10
    assert {c.value for c in Capability} == expected_identifiers

    assert Capability.FILESYSTEM == "filesystem"
    assert Capability.NETWORK == "network"
    assert Capability.CLIPBOARD == "clipboard"
    assert Capability.NOTIFICATIONS == "notifications"
    assert Capability.BROWSER == "browser"
    assert Capability.SETTINGS == "settings"
    assert Capability.TERMINAL == "terminal"
    assert Capability.AI == "ai"
    assert Capability.CAMERA == "camera"
    assert Capability.AUDIO == "audio"

    assert CAPABILITY_PERMISSION_MAP[Capability.FILESYSTEM] is PluginPermission.FILESYSTEM
    assert CAPABILITY_PERMISSION_MAP[Capability.NETWORK] is PluginPermission.NETWORK
    assert CAPABILITY_PERMISSION_MAP[Capability.SETTINGS] is PluginPermission.CONFIGURATION


def test_capability_default_deny() -> None:
    """AC-1: Non-granted capabilities are denied (ADR-006 D1)."""
    granted: frozenset[Capability] = frozenset(
        {Capability.FILESYSTEM, Capability.NETWORK}
    )

    assert is_capability_granted(Capability.FILESYSTEM, granted) is True
    assert is_capability_granted(Capability.NETWORK, granted) is True

    assert is_capability_granted(Capability.CLIPBOARD, granted) is False
    assert is_capability_granted(Capability.NOTIFICATIONS, granted) is False
    assert is_capability_granted(Capability.BROWSER, granted) is False
    assert is_capability_granted(Capability.SETTINGS, granted) is False
    assert is_capability_granted(Capability.TERMINAL, granted) is False
    assert is_capability_granted(Capability.AI, granted) is False
    assert is_capability_granted(Capability.CAMERA, granted) is False
    assert is_capability_granted(Capability.AUDIO, granted) is False

    empty: frozenset[Capability] = frozenset()
    for cap in Capability:
        assert is_capability_granted(cap, empty) is False
