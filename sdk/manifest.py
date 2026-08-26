"""Typed plugin manifest models and validation.

The manifest is the sole authoritative description of a plugin. It is
represented by immutable, frozen dataclasses so a validated manifest cannot
be mutated after construction, and every field has a stable, typed
representation instead of an unstructured mapping.

The models here are intentionally decoupled from
:class:`plugins.loader.PluginManifest`: that value type describes the
foundation's manifest-only discovery contract (see ADR-001), whereas
:class:`PluginMetadata` describes the enterprise-grade metadata surface that
plugin authors implement through the SDK. An adapter,
:meth:`PluginMetadata.from_loader_manifest`, bridges the two without leaking
foundation types into plugin code.
"""

from __future__ import annotations

import re
from collections.abc import Iterable, Mapping
from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any

from sdk.errors import PluginManifestError
from sdk.version import SDK_API_VERSION

_IDENTIFIER_PATTERN = re.compile(r"^[a-zA-Z][a-zA-Z0-9]*(?:[._-][a-zA-Z0-9]+)*$")
"""Reverse-DNS friendly identifier pattern: ``com.example.plugin-name``."""

_SEMVER_PATTERN = re.compile(r"^\d+\.\d+\.\d+$")
"""Strict ``major.minor.patch`` semantic version pattern."""


class PluginCategory(StrEnum):
    """Coarse classification of a plugin's primary responsibility."""

    GENERAL = "general"
    BACKGROUND = "background"
    UI = "ui"
    TOOL = "tool"
    WORKFLOW = "workflow"
    INTEGRATION = "integration"
    AI = "ai"
    DEVELOPER = "developer"


class PluginPermission(StrEnum):
    """Capabilities a plugin can declare in its manifest.

    Permissions are declarative: they describe the intent of the plugin so
    the host can enforce least-privilege policies at runtime. They do not
    themselves grant access; the SDK context enforces them.
    """

    NETWORK = "network"
    FILESYSTEM = "filesystem"
    CREDENTIALS = "credentials"
    SYSTEM_OBSERVATION = "system_observation"
    UI = "ui"
    EVENTS_PUBLISH = "events.publish"
    EVENTS_SUBSCRIBE = "events.subscribe"
    CONFIGURATION = "configuration"
    RESOURCES = "resources"
    SERVICES = "services"


class Capability(StrEnum):
    """Stable capability identifiers for the plugin permission system.

    Capabilities are the canonical vocabulary for manifest-level permission
    declarations (ADR-006). Plugins reference these string constants in
    their manifests; the host evaluates them against its permission policy
    at admission time. Capabilities that are not granted are denied
    (default-deny, ADR-006 D1).
    """

    FILESYSTEM = "filesystem"
    NETWORK = "network"
    CLIPBOARD = "clipboard"
    NOTIFICATIONS = "notifications"
    BROWSER = "browser"
    SETTINGS = "settings"
    TERMINAL = "terminal"
    AI = "ai"
    CAMERA = "camera"
    AUDIO = "audio"


CAPABILITY_PERMISSION_MAP: dict[Capability, PluginPermission] = {
    Capability.FILESYSTEM: PluginPermission.FILESYSTEM,
    Capability.NETWORK: PluginPermission.NETWORK,
    Capability.SETTINGS: PluginPermission.CONFIGURATION,
}
"""Mapping from capability identifiers to existing PluginPermission values.

Only capabilities with a direct semantic correspondence are mapped.
Capabilities without a mapping (e.g. CLIPBOARD, CAMERA) represent
contract vocabulary that does not yet have a host-side permission
equivalent.
"""


def is_capability_granted(
    capability: Capability,
    granted: frozenset[Capability],
) -> bool:
    """Check whether a capability is granted under default-deny semantics.

    Returns ``True`` only if *capability* is explicitly present in the
    *granted* set. All capabilities not in the set are denied (ADR-006 D1).
    """
    return capability in granted


class SignatureStatus(StrEnum):
    """Integrity classification assigned to a plugin at admission time.

    Signature status is descriptive metadata attached to a manifest by the
    host; plugin authors report it as ``UNVERIFIED`` and the host promotes it
    after integrity validation.
    """

    UNVERIFIED = "unverified"
    VERIFIED = "verified"
    TRUSTED = "trusted"
    REJECTED = "rejected"


def validate_identifier(value: str) -> str:
    """Validate and return a plugin or dependency identifier.

    Args:
        value: The identifier to validate.

    Returns:
        The validated identifier.

    Raises:
        PluginManifestError: If ``value`` is empty, not a string, or does
            not match the identifier pattern.
    """
    if not isinstance(value, str) or not value:
        raise PluginManifestError("Identifier must be a non-empty string")
    if not _IDENTIFIER_PATTERN.match(value):
        raise PluginManifestError(f"Invalid identifier: {value!r}")
    return value


def validate_semver(value: str, *, field_name: str = "version") -> str:
    """Validate and return a strict ``major.minor.patch`` semver string.

    Args:
        value: The semver string to validate.
        field_name: Field name used in the error message for clarity.

    Returns:
        The validated semver string.

    Raises:
        PluginManifestError: If ``value`` is not a strict semver string.
    """
    if not isinstance(value, str) or not _SEMVER_PATTERN.match(value):
        raise PluginManifestError(f"Invalid {field_name}: {value!r}")
    return value


def _validate_non_empty_string(value: object, *, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise PluginManifestError(f"{field_name} must be a non-empty string")
    return value


@dataclass(frozen=True, slots=True)
class PluginDependency:
    """Declared dependency on another plugin.

    Attributes:
        identifier: Stable identifier of the required plugin.
        minimum_version: Minimum semver of the dependency that satisfies
            the requirement (major-version compatible, patch-tolerant).
    """

    identifier: str
    minimum_version: str

    def __post_init__(self) -> None:
        """Validate the identifier and minimum version at construction time.

        Raises:
            PluginManifestError: If either field is invalid.
        """
        validate_identifier(self.identifier)
        validate_semver(self.minimum_version, field_name="dependency version")


@dataclass(frozen=True, slots=True)
class PluginMetadata:
    """Immutable, validated plugin metadata.

    Every plugin returns a :class:`PluginMetadata` from :meth:`Plugin.metadata`.
    Validation runs in :meth:`__post_init__`; a plugin that returns invalid
    metadata is rejected at attach time and never reaches the running state.

    Attributes:
        identifier: Stable, unique plugin identifier (reverse DNS style).
        name: Human-readable display name.
        version: The plugin's own semver.
        api_version: SDK API version the plugin was built against.
        author: Author name or organisation.
        description: One-line human-readable description.
        category: Primary plugin category.
        permissions: Declarative set of requested capabilities.
        dependencies: Ordered tuple of declared dependencies.
        minimum_application_version: Minimum host semver supported.
        signature_status: Integrity classification assigned by the host.
    """

    identifier: str
    name: str
    version: str
    api_version: str
    author: str
    description: str
    category: PluginCategory = PluginCategory.GENERAL
    permissions: frozenset[PluginPermission] = field(default_factory=frozenset)
    dependencies: tuple[PluginDependency, ...] = ()
    minimum_application_version: str = "0.7.0"
    signature_status: SignatureStatus = SignatureStatus.UNVERIFIED
    entry_point: str = ""

    def __post_init__(self) -> None:
        """Validate every field and raise :class:`PluginManifestError` on error."""
        validate_identifier(self.identifier)
        _validate_non_empty_string(self.name, field_name="name")
        validate_semver(self.version, field_name="version")
        validate_semver(self.api_version, field_name="api_version")
        _validate_non_empty_string(self.author, field_name="author")
        _validate_non_empty_string(self.description, field_name="description")
        if not isinstance(self.category, PluginCategory):
            raise PluginManifestError(f"Invalid category: {self.category!r}")
        if not isinstance(self.permissions, frozenset):
            raise PluginManifestError("permissions must be a frozenset")
        if not all(isinstance(item, PluginPermission) for item in self.permissions):
            raise PluginManifestError("permissions must contain PluginPermission values")
        if not isinstance(self.dependencies, tuple) or not all(
            isinstance(item, PluginDependency) for item in self.dependencies
        ):
            raise PluginManifestError("dependencies must be a tuple of PluginDependency")
        validate_semver(
            self.minimum_application_version, field_name="minimum_application_version"
        )
        if not isinstance(self.signature_status, SignatureStatus):
            raise PluginManifestError(
                f"Invalid signature_status: {self.signature_status!r}"
            )

    def has_permission(self, permission: PluginPermission) -> bool:
        """Return whether ``permission`` is declared in this manifest."""
        return permission in self.permissions

    def to_dict(self) -> dict[str, Any]:
        """Return a plain, JSON-friendly mapping of the metadata.

        Returns:
            A dictionary that mirrors the manifest field names and values.
        """
        result = {
            "identifier": self.identifier,
            "name": self.name,
            "version": self.version,
            "api_version": self.api_version,
            "author": self.author,
            "description": self.description,
            "category": self.category.value,
            "permissions": sorted(item.value for item in self.permissions),
            "dependencies": [
                {"identifier": item.identifier, "minimum_version": item.minimum_version}
                for item in self.dependencies
            ],
            "minimum_application_version": self.minimum_application_version,
            "signature_status": self.signature_status.value,
        }
        if self.entry_point:
            result["entry_point"] = self.entry_point
        return result

    @classmethod
    def from_mapping(cls, data: Mapping[str, Any]) -> PluginMetadata:
        """Construct a validated :class:`PluginMetadata` from a mapping.

        Args:
            data: Raw mapping typically parsed from a manifest file. Unknown
                keys are ignored so future extensions do not break older
                SDKs; missing required keys raise :class:`PluginManifestError`.

        Returns:
            A validated :class:`PluginMetadata` instance.

        Raises:
            PluginManifestError: When required fields are missing or when a
                field fails validation.
        """
        if not isinstance(data, Mapping):
            raise PluginManifestError("Manifest data must be a mapping")
        try:
            identifier = str(data["identifier"])
            name = str(data["name"])
            version = str(data["version"])
            api_version = str(data["api_version"])
            author = str(data["author"])
            description = str(data["description"])
        except KeyError as error:
            raise PluginManifestError(f"Missing manifest field: {error.args[0]}") from error

        category_raw = data.get("category", PluginCategory.GENERAL.value)
        try:
            category = PluginCategory(str(category_raw))
        except ValueError as error:
            raise PluginManifestError(f"Invalid category: {category_raw!r}") from error

        permissions_raw = data.get("permissions", ())
        if isinstance(permissions_raw, (str, bytes)) or not isinstance(
            permissions_raw, Iterable
        ):
            raise PluginManifestError("permissions must be an iterable of strings")
        try:
            permissions = frozenset(PluginPermission(str(item)) for item in permissions_raw)
        except ValueError as error:
            raise PluginManifestError(f"Invalid permission: {error}") from error

        dependencies_raw = data.get("dependencies", ())
        if isinstance(dependencies_raw, (str, bytes)) or not isinstance(
            dependencies_raw, Iterable
        ):
            raise PluginManifestError("dependencies must be an iterable of tables")
        dependencies: list[PluginDependency] = []
        for item in dependencies_raw:
            if not isinstance(item, Mapping):
                raise PluginManifestError("Each dependency must be a mapping")
            try:
                dependencies.append(
                    PluginDependency(
                        identifier=str(item["identifier"]),
                        minimum_version=str(item["minimum_version"]),
                    )
                )
            except KeyError as error:
                raise PluginManifestError(
                    f"Missing dependency field: {error.args[0]}"
                ) from error

        minimum_application_version = str(
            data.get("minimum_application_version", "0.7.0")
        )
        signature_raw = data.get("signature_status", SignatureStatus.UNVERIFIED.value)
        try:
            signature_status = SignatureStatus(str(signature_raw))
        except ValueError as error:
            raise PluginManifestError(
                f"Invalid signature_status: {signature_raw!r}"
            ) from error

        entry_point = str(data.get("entry_point", ""))

        return cls(
            identifier=identifier,
            name=name,
            version=version,
            api_version=api_version,
            author=author,
            description=description,
            category=category,
            permissions=permissions,
            dependencies=tuple(dependencies),
            minimum_application_version=minimum_application_version,
            signature_status=signature_status,
            entry_point=entry_point,
        )

    @classmethod
    def from_loader_manifest(
        cls,
        loader_manifest: Any,
        *,
        name: str = "",
        author: str = "",
        description: str = "",
        api_version: str = "",
        category: PluginCategory = PluginCategory.GENERAL,
    ) -> PluginMetadata:
        """Adapt a foundation ``plugins.loader.PluginManifest`` to SDK metadata.

        Reads the public attributes documented by the foundation's manifest
        contract and combines them with either the v2 manifest fields
        (metadata, permissions, dependencies, entry_point) or the explicit
        keyword arguments supplied by the caller.

        Explicit keyword arguments take precedence over manifest values when
        both are available.  When neither a keyword argument nor a manifest
        value is present, safe defaults are used.

        Args:
            loader_manifest: A ``plugins.loader.PluginManifest`` instance.
            name: Human-readable plugin name (overrides manifest metadata).
            author: Author or organisation name (overrides manifest metadata).
            description: One-line description (overrides manifest metadata).
            api_version: SDK API version (overrides manifest api_version).
            category: Primary plugin category.

        Returns:
            A validated :class:`PluginMetadata` describing the same plugin.

        Raises:
            PluginManifestError: If the adapted fields fail validation.
        """
        identifier = getattr(loader_manifest, "identifier", None)
        version = getattr(loader_manifest, "version", None)
        required = getattr(loader_manifest, "required_application_version", None)
        if identifier is None or version is None or required is None:
            raise PluginManifestError(
                "loader_manifest is missing required public attributes"
            )

        manifest_metadata: dict[str, str] = getattr(
            loader_manifest, "metadata", {}
        )
        manifest_api_version = getattr(loader_manifest, "api_version", None)
        manifest_category = getattr(loader_manifest, "category", "general")
        manifest_entry_point = getattr(loader_manifest, "entry_point", "")
        manifest_permissions: tuple[str, ...] = getattr(
            loader_manifest, "permissions", ()
        )
        manifest_dependencies: tuple[dict[str, str], ...] = getattr(
            loader_manifest, "dependencies", ()
        )

        resolved_name = name or manifest_metadata.get("display_name", "") or str(identifier)
        resolved_author = author or manifest_metadata.get("author", "") or "Unknown"
        resolved_description = (
            description
            or manifest_metadata.get("description", "")
            or "No description"
        )

        resolved_api_version = api_version
        if not resolved_api_version and manifest_api_version is not None:
            resolved_api_version = str(manifest_api_version)
        if not resolved_api_version:
            resolved_api_version = SDK_API_VERSION

        resolved_category = category
        if category == PluginCategory.GENERAL and manifest_category != "general":
            try:
                resolved_category = PluginCategory(manifest_category)
            except ValueError:
                pass

        permissions: frozenset[PluginPermission] = frozenset()
        if manifest_permissions:
            perm_set: set[PluginPermission] = set()
            for cap_str in manifest_permissions:
                try:
                    perm_set.add(PluginPermission(cap_str))
                except ValueError:
                    pass
            permissions = frozenset(perm_set)

        deps: list[PluginDependency] = []
        for dep_dict in manifest_dependencies:
            if isinstance(dep_dict, dict):
                dep_id = dep_dict.get("id", "")
                dep_ver = dep_dict.get("version", "")
                if dep_ver.startswith(">="):
                    dep_ver = dep_ver[2:]
                if dep_id and dep_ver:
                    deps.append(
                        PluginDependency(
                            identifier=dep_id, minimum_version=dep_ver
                        )
                    )

        return cls(
            identifier=str(identifier),
            name=resolved_name,
            version=str(version),
            api_version=resolved_api_version,
            author=resolved_author,
            description=resolved_description,
            category=resolved_category,
            permissions=permissions,
            dependencies=tuple(deps),
            minimum_application_version=str(required),
            entry_point=manifest_entry_point,
        )


__all__ = [
    "CAPABILITY_PERMISSION_MAP",
    "Capability",
    "PluginCategory",
    "PluginDependency",
    "PluginMetadata",
    "PluginPermission",
    "SignatureStatus",
    "is_capability_granted",
    "validate_identifier",
    "validate_semver",
]
