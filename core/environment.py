"""Runtime paths and operating-system facts."""

from dataclasses import dataclass
from pathlib import Path
import platform


@dataclass(frozen=True, slots=True)
class Environment:
    """Resolved application environment with no mutable process-wide state."""

    root: Path
    os_name: str
    python_version: str

    @classmethod
    def from_root(cls, root: Path) -> "Environment":
        """Create an environment and ensure runtime-owned directories exist."""
        for directory in (root / "logs", root / "data"):
            directory.mkdir(parents=True, exist_ok=True)
        return cls(root.resolve(), platform.system(), platform.python_version())
