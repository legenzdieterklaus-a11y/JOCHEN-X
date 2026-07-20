"""Version parsing and compatibility checks."""

from dataclasses import dataclass


@dataclass(frozen=True, order=True, slots=True)
class Version:
    """Comparable semantic version without pre-release semantics."""

    major: int
    minor: int
    patch: int

    @classmethod
    def parse(cls, value: str) -> "Version":
        """Parse an exact `major.minor.patch` version."""
        parts = value.split(".")
        if len(parts) != 3 or any(not part.isdigit() for part in parts):
            raise ValueError(f"Invalid semantic version: {value}")
        return cls(*(int(part) for part in parts))

    def __str__(self) -> str:
        return f"{self.major}.{self.minor}.{self.patch}"


class VersionManager:
    """Evaluates major-version compatibility for extension boundaries."""

    def __init__(self, application_version: Version) -> None:
        self.application_version = application_version

    def is_compatible(self, required: Version) -> bool:
        """Return whether an extension targets the current major version."""
        return required.major == self.application_version.major and required <= self.application_version
