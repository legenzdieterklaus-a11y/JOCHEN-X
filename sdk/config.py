"""Plugin-owned configuration API.

Every plugin owns a private configuration store that is:

* **typed** – values pass through registered validators before being written;
* **defaulted** – missing keys return declared default values;
* **persistent** – ``save()`` and ``load()`` round-trip through a storage
  backend provided by the host; no filesystem details are exposed to plugins;
* **thread-safe** – all mutations are guarded by a re-entrant lock so the
  store can be used from workers and UI callbacks alike.

The storage layer is defined as a :class:`PluginConfigStorage` protocol so
the SDK can be tested against an in-memory backend and the host can supply a
production backend (JSON files on disk) without leaking path handling into
plugin code.
"""

from __future__ import annotations

import json
from collections.abc import Callable, Iterable, Mapping
from pathlib import Path
from threading import RLock
from typing import Any, Protocol, TypeVar, cast, runtime_checkable

from sdk.errors import PluginConfigurationError, PluginPermissionError
from sdk.manifest import PluginPermission

Validator = Callable[[Any], None]
ConfigPermissionCheck = Callable[[PluginPermission], None]
"""A callable that raises on invalid configuration values."""

T = TypeVar("T")
_MISSING: Any = object()


@runtime_checkable
class PluginConfigStorage(Protocol):
    """Storage port for plugin configuration.

    Implementations translate between a plugin identifier and its persisted
    configuration payload. Payloads are plain, JSON-friendly mappings so
    plugins never need to know how or where their data is stored.
    """

    def read(self, plugin_id: str) -> Mapping[str, Any]:
        """Return the persisted configuration mapping for ``plugin_id``.

        Returns:
            The stored mapping or an empty mapping if none exists yet.
        """
        ...

    def write(self, plugin_id: str, data: Mapping[str, Any]) -> None:
        """Persist ``data`` as the configuration for ``plugin_id``."""
        ...


class InMemoryPluginConfigStorage:
    """A process-local :class:`PluginConfigStorage` for tests and headless use."""

    __slots__ = ("_data",)

    def __init__(self) -> None:
        """Create an empty in-memory store."""
        self._data: dict[str, dict[str, Any]] = {}

    def read(self, plugin_id: str) -> Mapping[str, Any]:
        """Return the current in-memory mapping for ``plugin_id``."""
        return dict(self._data.get(plugin_id, {}))

    def write(self, plugin_id: str, data: Mapping[str, Any]) -> None:
        """Store a deep copy of ``data`` for ``plugin_id``."""
        self._data[plugin_id] = json.loads(json.dumps(dict(data)))


class FilePluginConfigStorage:
    """JSON-file based :class:`PluginConfigStorage`.

    Configuration is written as one JSON file per plugin under the injected
    root directory. The root path is provided by the host at context-build
    time so plugins never see filesystem details.
    """

    __slots__ = ("_root",)

    def __init__(self, root: Path) -> None:
        """Create the storage rooted at ``root``.

        Args:
            root: An existing directory in which per-plugin JSON files live.
                The directory is created if it does not already exist.
        """
        self._root = Path(root)
        self._root.mkdir(parents=True, exist_ok=True)

    def read(self, plugin_id: str) -> Mapping[str, Any]:
        """Return the JSON payload stored for ``plugin_id`` or an empty mapping."""
        target = self._path_for(plugin_id)
        if not target.exists():
            return {}
        try:
            with target.open("r", encoding="utf-8") as handle:
                loaded = json.load(handle)
        except (OSError, json.JSONDecodeError) as error:
            raise PluginConfigurationError(
                f"Cannot read configuration for {plugin_id!r}: {error}"
            ) from error
        if not isinstance(loaded, dict):
            raise PluginConfigurationError(
                f"Configuration for {plugin_id!r} is not a JSON object"
            )
        return loaded

    def write(self, plugin_id: str, data: Mapping[str, Any]) -> None:
        """Persist ``data`` as pretty-printed JSON for ``plugin_id``."""
        target = self._path_for(plugin_id)
        try:
            target.write_text(
                json.dumps(dict(data), indent=2, sort_keys=True, ensure_ascii=False),
                encoding="utf-8",
            )
        except OSError as error:
            raise PluginConfigurationError(
                f"Cannot write configuration for {plugin_id!r}: {error}"
            ) from error

    def _path_for(self, plugin_id: str) -> Path:
        """Return the JSON file path used to store ``plugin_id``'s data."""
        # The plugin identifier has already been validated by PluginMetadata
        # before it reaches this point, so no path traversal is possible.
        return self._root / f"{plugin_id}.json"


class PluginConfig:
    """Plugin configuration store with defaults, validation, and persistence.

    Plugin authors interact only with this class. All state is held in
    memory until :meth:`save` is called, and :meth:`load` refreshes the
    in-memory view from the storage backend.
    """

    def __init__(
        self,
        plugin_id: str,
        storage: PluginConfigStorage,
        *,
        defaults: Mapping[str, Any] | None = None,
        validators: Mapping[str, Validator] | None = None,
        permission_check: ConfigPermissionCheck | None = None,
    ) -> None:
        """Create the configuration store.

        Args:
            plugin_id: The owning plugin identifier.
            storage: The storage backend used by :meth:`load` and :meth:`save`.
            defaults: Immutable default values returned when a key is missing.
            validators: Optional per-key validators invoked on :meth:`set`.
            permission_check: Optional callable invoked before data access.
                Raises :class:`PluginPermissionError` on denial.

        Raises:
            ValueError: If ``plugin_id`` is empty.
        """
        if not plugin_id:
            raise ValueError("plugin_id must be a non-empty string")
        self._plugin_id = plugin_id
        self._storage = storage
        self._defaults: dict[str, Any] = dict(defaults or {})
        self._validators: dict[str, Validator] = dict(validators or {})
        self._values: dict[str, Any] = {}
        self._lock = RLock()
        self._permission_check = permission_check
        for key, value in self._defaults.items():
            self._validate(key, value)

    @property
    def plugin_id(self) -> str:
        """Return the owning plugin identifier."""
        return self._plugin_id

    def keys(self) -> tuple[str, ...]:
        """Return the currently defined configuration keys (values + defaults)."""
        with self._lock:
            return tuple(sorted({*self._defaults.keys(), *self._values.keys()}))

    def has(self, key: str) -> bool:
        """Return whether ``key`` has a defined value or default."""
        with self._lock:
            return key in self._values or key in self._defaults

    def get(self, key: str, default: T | Any = _MISSING) -> Any | T:
        """Return the value for ``key``.

        Args:
            key: Configuration key.
            default: Value returned when the key is absent. Defaults to the
                registered default; raises :class:`KeyError` if neither is
                available.

        Returns:
            The stored value, the fallback default, or the caller-supplied
            default.

        Raises:
            KeyError: If ``key`` has no value, no registered default, and no
                caller-supplied default.
        """
        self._ensure_permission()
        with self._lock:
            if key in self._values:
                return self._values[key]
            if key in self._defaults:
                return self._defaults[key]
        if default is not _MISSING:
            return default
        raise KeyError(f"Configuration key not found: {key!r}")

    def set(self, key: str, value: Any) -> None:
        """Validate and store ``value`` under ``key``.

        Args:
            key: Non-empty configuration key.
            value: Value to store. Must satisfy the registered validator if any.

        Raises:
            PluginConfigurationError: If ``key`` is empty or ``value`` fails
                validation.
        """
        self._ensure_permission()
        if not key:
            raise PluginConfigurationError("Configuration key must be non-empty")
        self._validate(key, value)
        with self._lock:
            self._values[key] = value

    def update(self, values: Mapping[str, Any]) -> None:
        """Set multiple values atomically, rolling back on validation failure.

        Args:
            values: Mapping of key/value pairs to apply.

        Raises:
            PluginConfigurationError: If any value fails validation; no
                changes are applied.
        """
        self._ensure_permission()
        for key, value in values.items():
            if not key:
                raise PluginConfigurationError("Configuration key must be non-empty")
            self._validate(key, value)
        with self._lock:
            self._values.update(values)

    def delete(self, key: str) -> None:
        """Remove ``key`` from the runtime state; defaults are unaffected."""
        self._ensure_permission()
        with self._lock:
            self._values.pop(key, None)

    def register_default(self, key: str, value: Any) -> None:
        """Register (or replace) a default value for ``key``."""
        if not key:
            raise PluginConfigurationError("Configuration key must be non-empty")
        self._validate(key, value)
        with self._lock:
            self._defaults[key] = value

    def register_validator(self, key: str, validator: Validator) -> None:
        """Register a validator for ``key``; runs immediately against the current value."""
        if not key:
            raise PluginConfigurationError("Configuration key must be non-empty")
        with self._lock:
            self._validators[key] = validator
            if key in self._values:
                self._invoke_validator(key, self._values[key])
            elif key in self._defaults:
                self._invoke_validator(key, self._defaults[key])

    def snapshot(self) -> dict[str, Any]:
        """Return a JSON-friendly copy of the effective configuration.

        The snapshot merges defaults with runtime overrides. Runtime values
        take precedence over defaults for the same key.
        """
        self._ensure_permission()
        with self._lock:
            merged: dict[str, Any] = {}
            merged.update(self._defaults)
            merged.update(self._values)
            return cast(dict[str, Any], json.loads(json.dumps(merged)))

    def load(self) -> None:
        """Refresh the runtime values from the storage backend.

        Raises:
            PluginConfigurationError: If the persisted payload is not a
                mapping or contains an invalid value.
        """
        self._ensure_permission()
        data = self._storage.read(self._plugin_id)
        if not isinstance(data, Mapping):
            raise PluginConfigurationError(
                f"Persisted configuration for {self._plugin_id!r} is not a mapping"
            )
        for key, value in data.items():
            self._validate(key, value)
        with self._lock:
            self._values = dict(data)

    def save(self) -> None:
        """Persist the current runtime values via the storage backend."""
        self._ensure_permission()
        with self._lock:
            payload = dict(self._values)
        self._storage.write(self._plugin_id, payload)

    def keys_with_defaults(self) -> Iterable[str]:
        """Return the tuple of keys that have registered defaults."""
        with self._lock:
            return tuple(self._defaults.keys())

    def _ensure_permission(self) -> None:
        if self._permission_check is not None:
            self._permission_check(PluginPermission.CONFIGURATION)

    def _validate(self, key: str, value: Any) -> None:
        """Apply the registered validator for ``key`` if any is defined."""
        if value is None:
            raise PluginConfigurationError(
                f"Configuration value must not be None for key {key!r}"
            )
        validator = self._validators.get(key)
        if validator is None:
            return
        self._invoke_validator(key, value)

    def _invoke_validator(self, key: str, value: Any) -> None:
        """Run the validator, translating raised errors into SDK errors."""
        try:
            self._validators[key](value)
        except PluginConfigurationError:
            raise
        except Exception as error:  # normalise any validator failure
            raise PluginConfigurationError(
                f"Invalid value for {key!r}: {error}"
            ) from error


__all__ = [
    "FilePluginConfigStorage",
    "InMemoryPluginConfigStorage",
    "PluginConfig",
    "PluginConfigStorage",
    "Validator",
]
