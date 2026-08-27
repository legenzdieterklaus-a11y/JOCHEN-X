"""Versioned, JSON-backed runtime settings with atomic persistence.

:class:`SettingsProvider` stores mutable runtime settings separately from the
immutable TOML application configuration handled by
:class:`config.settings.ConfigurationService`. It provides schema versioning with
ordered migrations, pluggable validation, defaults, atomic writes (temp file plus
``os.replace``), automatic backups, and restore.
"""

from __future__ import annotations

import json
import logging
import os
from collections.abc import Callable, Mapping
from pathlib import Path
from typing import Any, Protocol

from core.exceptions import JochenXError

_VERSION_KEY = "version"
_DATA_KEY = "settings"
_BACKUP_SUFFIX = ".bak"
_TEMP_SUFFIX = ".tmp"

Migration = Callable[[dict[str, Any]], dict[str, Any]]


class SettingsError(JochenXError):
    """Raised for settings persistence, migration, or validation failures."""


class SettingsValidator(Protocol):
    """Port validating a settings mapping before it is persisted or returned."""

    def validate(self, data: Mapping[str, Any]) -> None:
        """Raise :class:`SettingsError` if ``data`` is invalid."""
        ...


class RequiredKeysValidator:
    """Validator ensuring every required key is present in the settings."""

    def __init__(self, required_keys: tuple[str, ...]) -> None:
        """Create a validator.

        Args:
            required_keys: Keys that must be present in the settings mapping.
        """
        self._required_keys = required_keys

    def validate(self, data: Mapping[str, Any]) -> None:
        """Raise :class:`SettingsError` when a required key is missing."""
        missing = tuple(key for key in self._required_keys if key not in data)
        if missing:
            raise SettingsError(f"Missing required settings keys: {', '.join(missing)}")


class SettingsProvider:
    """Loads and persists a single versioned JSON settings document."""

    def __init__(
        self,
        path: Path,
        *,
        version: int,
        defaults: Mapping[str, Any],
        migrations: Mapping[int, Migration] | None = None,
        validator: SettingsValidator | None = None,
        logger: logging.Logger | None = None,
    ) -> None:
        """Create the provider.

        Args:
            path: Destination file for the settings document.
            version: The current schema version of ``defaults``.
            defaults: Values used when no file exists or a key is absent.
            migrations: Mapping of source-version to a migration callable that
                upgrades a settings mapping by exactly one version.
            validator: Optional validator applied on load and save.
            logger: Optional logger for diagnostics.

        Raises:
            SettingsError: If ``version`` is not positive.
        """
        if version < 1:
            raise SettingsError("Schema version must be a positive integer")
        self._path = path
        self._version = version
        self._defaults = dict(defaults)
        self._migrations = dict(migrations or {})
        self._validator = validator
        self._logger = logger or logging.getLogger("jochen_x.settings")

    @property
    def path(self) -> Path:
        """Return the settings file path."""
        return self._path

    def load(self) -> dict[str, Any]:
        """Load, migrate, validate, and return the settings mapping.

        A missing file yields the defaults, which are persisted immediately so a
        canonical document always exists after the first load.

        Returns:
            The current settings merged over the defaults.

        Raises:
            SettingsError: If the document is corrupt or fails validation.
        """
        if not self._path.exists():
            self._logger.info(
                "settings.defaults_created", extra={"context": {"path": str(self._path)}}
            )
            self.save(self._defaults)
            return dict(self._defaults)
        document = self._read_document()
        stored_version = int(document.get(_VERSION_KEY, 1))
        data = dict(document.get(_DATA_KEY, {}))
        if stored_version > self._version:
            raise SettingsError(f"Unsupported settings version: {stored_version}")
        if stored_version < self._version:
            data = self._migrate(data, stored_version)
            merged = {**self._defaults, **data}
            self._validate(merged)
            self._write_document(merged)
            return merged
        merged = {**self._defaults, **data}
        self._validate(merged)
        return merged

    def save(self, data: Mapping[str, Any]) -> None:
        """Validate and atomically persist ``data`` at the current version."""
        merged = {**self._defaults, **data}
        self._validate(merged)
        self._write_document(merged)

    def update(self, **values: Any) -> dict[str, Any]:
        """Merge ``values`` into the current settings, persist, and return them."""
        current = self.load()
        current.update(values)
        self.save(current)
        return current

    def reset(self) -> dict[str, Any]:
        """Restore defaults, persist them, and return the default mapping."""
        self.save(self._defaults)
        return dict(self._defaults)

    def backup(self) -> Path:
        """Copy the current settings file to its backup path.

        Returns:
            The backup path.

        Raises:
            SettingsError: If there is no settings file to back up.
        """
        if not self._path.exists():
            raise SettingsError("No settings file to back up")
        backup_path = self._backup_path()
        backup_path.write_bytes(self._path.read_bytes())
        return backup_path

    def restore(self) -> dict[str, Any]:
        """Restore settings from the backup file and return the loaded mapping.

        Raises:
            SettingsError: If no backup file exists.
        """
        backup_path = self._backup_path()
        if not backup_path.exists():
            raise SettingsError("No settings backup available to restore")
        self._path.write_bytes(backup_path.read_bytes())
        self._logger.info("settings.restored", extra={"context": {"path": str(self._path)}})
        return self.load()

    def _migrate(self, data: dict[str, Any], from_version: int) -> dict[str, Any]:
        """Apply ordered single-step migrations from ``from_version``."""
        current = data
        for source in range(from_version, self._version):
            migration = self._migrations.get(source)
            if migration is None:
                raise SettingsError(f"No migration registered for version {source}")
            current = migration(current)
            self._logger.info(
                "settings.migrated", extra={"context": {"from": source, "to": source + 1}}
            )
        return current

    def _validate(self, data: Mapping[str, Any]) -> None:
        """Run the configured validator, if any."""
        if self._validator is not None:
            self._validator.validate(data)

    def _read_document(self) -> dict[str, Any]:
        """Read and parse the settings document."""
        try:
            raw = json.loads(self._path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as error:
            raise SettingsError(f"Cannot read settings file {self._path}: {error}") from error
        if not isinstance(raw, dict):
            raise SettingsError("Settings document must be a JSON object")
        return raw

    def _write_document(self, data: Mapping[str, Any]) -> None:
        """Atomically write the versioned settings document with a backup."""
        self._path.parent.mkdir(parents=True, exist_ok=True)
        if self._path.exists():
            self._backup_path().write_bytes(self._path.read_bytes())
        document = {_VERSION_KEY: self._version, _DATA_KEY: dict(data)}
        temp_path = self._path.with_name(self._path.name + _TEMP_SUFFIX)
        try:
            temp_path.write_text(json.dumps(document, indent=2, sort_keys=True), encoding="utf-8")
            os.replace(temp_path, self._path)
        except OSError as error:
            if temp_path.exists():
                temp_path.unlink(missing_ok=True)
            raise SettingsError(f"Cannot write settings file {self._path}: {error}") from error

    def _backup_path(self) -> Path:
        """Return the backup file path for the settings document."""
        return self._path.with_name(self._path.name + _BACKUP_SUFFIX)
