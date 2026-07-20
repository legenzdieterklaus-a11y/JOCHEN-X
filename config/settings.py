"""TOML-backed configuration with a deliberately narrow schema."""

from dataclasses import asdict, dataclass
from enum import StrEnum
from pathlib import Path
import tomllib

from core.exceptions import ConfigurationError


class ThemeMode(StrEnum):
    """Supported theme-selection modes."""

    LIGHT = "light"
    DARK = "dark"
    SYSTEM = "system"


@dataclass(frozen=True, slots=True)
class ApplicationSettings:
    """Validated settings needed by the foundation host."""

    name: str
    version: str
    log_level: str
    theme_mode: ThemeMode
    database_path: str
    plugin_directory: str
    developer_enabled: bool = False

    @classmethod
    def from_mapping(cls, raw: dict[str, object]) -> "ApplicationSettings":
        """Validate required sections and create immutable settings."""
        try:
            application = raw["application"]
            database = raw["database"]
            plugins = raw["plugins"]
            if not all(isinstance(value, dict) for value in (application, database, plugins)):
                raise TypeError("sections must be tables")
            theme_mode = ThemeMode(str(application["theme_mode"]).lower())
            log_level = str(application["log_level"]).upper()
            if log_level not in {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}:
                raise ValueError("unsupported log level")
            return cls(str(application["name"]), str(application["version"]), log_level,
                       theme_mode, str(database["path"]), str(plugins["directory"]), bool(application.get("developer_enabled", False)))
        except (KeyError, TypeError, ValueError) as error:
            raise ConfigurationError(f"Invalid configuration: {error}") from error


class ConfigurationService:
    """Loads a selected profile and persists only explicit profile overrides."""

    def __init__(self, default_path: Path, profile_path: Path | None = None) -> None:
        self._default_path = default_path
        self._profile_path = profile_path

    def load(self) -> ApplicationSettings:
        """Load defaults merged with an optional profile TOML file."""
        raw = self._read(self._default_path)
        if self._profile_path and self._profile_path.exists():
            raw = self._merge(raw, self._read(self._profile_path))
        return ApplicationSettings.from_mapping(raw)

    def save_profile(self, settings: ApplicationSettings) -> None:
        """Save an explicit profile in the portable TOML subset used by this service."""
        if self._profile_path is None:
            raise ConfigurationError("No writable profile path configured")
        data = asdict(settings)
        self._profile_path.parent.mkdir(parents=True, exist_ok=True)
        self._profile_path.write_text(
            "[application]\nname = " + repr(data["name"]) + "\nversion = " + repr(data["version"]) +
            "\nlog_level = " + repr(data["log_level"]) + "\ntheme_mode = " + repr(str(data["theme_mode"])) +
            "\ndeveloper_enabled = " + repr(data["developer_enabled"]) +
            "\n\n[database]\npath = " + repr(data["database_path"]) +
            "\n\n[plugins]\ndirectory = " + repr(data["plugin_directory"]) + "\n", encoding="utf-8")

    @staticmethod
    def _read(path: Path) -> dict[str, object]:
        try:
            with path.open("rb") as handle:
                return tomllib.load(handle)
        except (OSError, tomllib.TOMLDecodeError) as error:
            raise ConfigurationError(f"Cannot load {path}: {error}") from error

    @staticmethod
    def _merge(base: dict[str, object], override: dict[str, object]) -> dict[str, object]:
        result = dict(base)
        for key, value in override.items():
            result[key] = {**result.get(key, {}), **value} if isinstance(value, dict) else value
        return result
