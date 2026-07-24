"""Public SDK version constants and semantic version primitives.

The SDK ships with its own, deliberately narrow ``ApiVersion`` value type so
that plugin developers depend on a single, stable public type rather than on
any framework-internal version model. The SDK version and the plugin API
version follow independent semantic-versioning tracks:

* :data:`SDK_VERSION` describes the released SDK package.
* :data:`SDK_API_VERSION` describes the compatibility promise made to plugins
  built against this SDK; it changes only when the plugin-facing surface is
  extended (minor) or broken (major).

All comparisons and parsing go through :class:`ApiVersion`; no plugin needs
to import framework-internal version types.
"""

from __future__ import annotations

from dataclasses import dataclass

SDK_NAME: str = "jochen-x-sdk"
"""Stable, machine-readable SDK distribution name."""

SDK_VERSION: str = "0.7.1"
"""Released SDK package version (semantic version, ``major.minor.patch``)."""

SDK_API_VERSION: str = "1.0.0"
"""Public plugin API contract version implemented by this SDK release."""


@dataclass(frozen=True, order=True, slots=True)
class ApiVersion:
    """Immutable, comparable semantic version (``major.minor.patch``).

    ``ApiVersion`` is the sole public version type the SDK exposes; it is not
    a re-export of any framework-internal version type, keeping the SDK
    surface decoupled from the foundation implementation.
    """

    major: int
    minor: int
    patch: int

    @classmethod
    def parse(cls, value: str) -> ApiVersion:
        """Parse a strict ``major.minor.patch`` version string.

        Args:
            value: The version string to parse.

        Returns:
            The parsed :class:`ApiVersion` instance.

        Raises:
            ValueError: If ``value`` is not a strict ``major.minor.patch``
                string of non-negative decimal integers.
        """
        parts = value.split(".") if isinstance(value, str) else []
        if len(parts) != 3 or not all(part.isdigit() for part in parts):
            raise ValueError(f"Invalid semantic version: {value!r}")
        return cls(*(int(part) for part in parts))

    def __str__(self) -> str:
        """Render the version in canonical ``major.minor.patch`` form."""
        return f"{self.major}.{self.minor}.{self.patch}"

    def is_compatible_with(self, required: ApiVersion) -> bool:
        """Return whether this version satisfies ``required`` under semver.

        Compatibility follows the well-known major-version rule used across
        the JOCHEN X ecosystem: the major numbers must match exactly and the
        current version must be at least the required version.

        Args:
            required: The minimum required version.

        Returns:
            ``True`` when this version can safely be used by callers that
            depend on ``required``.
        """
        return self.major == required.major and self >= required


SDK_API_VERSION_INFO: ApiVersion = ApiVersion.parse(SDK_API_VERSION)
"""Parsed :class:`ApiVersion` for the shipped :data:`SDK_API_VERSION`."""

SDK_VERSION_INFO: ApiVersion = ApiVersion.parse(SDK_VERSION)
"""Parsed :class:`ApiVersion` for the shipped :data:`SDK_VERSION`."""
