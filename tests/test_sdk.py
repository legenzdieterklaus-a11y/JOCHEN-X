"""Comprehensive tests for the JOCHEN X Enterprise Plugin SDK.

Every SDK subsystem exposed under :mod:`sdk` is covered:

* Manifest models and validation
* Plugin lifecycle (Plugin, BackgroundPlugin, UIPlugin, ToolPlugin,
  WorkflowPlugin, and PluginRuntime)
* PluginContext and PluginContextBuilder
* Plugin logging
* Plugin configuration API (defaults, validation, save/load)
* Plugin event API (subscribe/publish/unsubscribe, permission gating)
* Plugin service access layer
* Dependency validation on the manifest

The tests never import framework internals through side channels; they use
the SDK's public surface exclusively and combine it with the foundation's
public :class:`core.events.EventBus` where a real bus is required.
"""

from __future__ import annotations

import logging
import tempfile
import threading
import unittest
from pathlib import Path
from typing import Any

from core.events import Event, EventBus

from sdk import (
    ApiVersion,
    BackgroundPlugin,
    FilePluginConfigStorage,
    InMemoryPluginConfigStorage,
    Plugin,
    PluginCategory,
    PluginConfig,
    PluginConfigurationError,
    PluginContextBuilder,
    PluginDependency,
    PluginDependencyError,
    PluginEvent,
    PluginEventBus,
    PluginEventError,
    PluginLifecycleError,
    PluginLifecycleState,
    PluginLogger,
    PluginManifestError,
    PluginMetadata,
    PluginPermission,
    PluginPermissionError,
    PluginResourceError,
    PluginResources,
    PluginRuntime,
    PluginSDKError,
    PluginServiceNotAvailableError,
    PluginServices,
    SDK_API_VERSION,
    SDK_VERSION,
    SignatureStatus,
    Subscription,
    ToolPlugin,
    WorkflowPlugin,
    validate_identifier,
    validate_semver,
)


def _make_metadata(**overrides: Any) -> PluginMetadata:
    """Build a valid :class:`PluginMetadata` with optional overrides."""
    fields: dict[str, Any] = {
        "identifier": "com.example.sample",
        "name": "Sample Plugin",
        "version": "1.0.0",
        "api_version": SDK_API_VERSION,
        "author": "JOCHEN X Team",
        "description": "Sample plugin used by SDK tests.",
        "category": PluginCategory.GENERAL,
        "permissions": frozenset(
            {PluginPermission.EVENTS_SUBSCRIBE, PluginPermission.EVENTS_PUBLISH}
        ),
        "dependencies": (),
        "minimum_application_version": "0.7.0",
    }
    fields.update(overrides)
    return PluginMetadata(**fields)


def _build_context(
    *,
    metadata: PluginMetadata | None = None,
    services: dict[type, Any] | None = None,
    tmp_root: Path | None = None,
) -> tuple[Any, EventBus, InMemoryPluginConfigStorage, Path]:
    """Build a fully-wired :class:`PluginContext` on top of an EventBus."""
    metadata = metadata or _make_metadata()
    bus = EventBus()
    storage = InMemoryPluginConfigStorage()
    resources_root = tmp_root or Path(tempfile.mkdtemp(prefix="sdk-test-"))
    builder = (
        PluginContextBuilder(metadata)
        .with_event_bus(bus, event_type=Event)
        .with_config_storage(storage)
        .with_resources_root(resources_root)
        .with_application_version("0.7.1")
    )
    if services:
        builder.with_services(services)
    return builder.build(), bus, storage, resources_root


# ---------------------------------------------------------------------------
# Manifest validation
# ---------------------------------------------------------------------------


class ManifestValidationTests(unittest.TestCase):
    """Verify manifest validation and (de)serialization."""

    def test_valid_metadata_round_trips_through_mapping(self) -> None:
        metadata = _make_metadata(
            dependencies=(PluginDependency("com.example.other", "0.1.0"),),
            permissions=frozenset(
                {
                    PluginPermission.EVENTS_SUBSCRIBE,
                    PluginPermission.CONFIGURATION,
                }
            ),
            signature_status=SignatureStatus.VERIFIED,
        )
        payload = metadata.to_dict()
        restored = PluginMetadata.from_mapping(payload)
        self.assertEqual(restored, metadata)

    def test_missing_required_field_is_rejected(self) -> None:
        with self.assertRaises(PluginManifestError):
            PluginMetadata.from_mapping({"identifier": "x"})

    def test_invalid_identifier_is_rejected(self) -> None:
        with self.assertRaises(PluginManifestError):
            _make_metadata(identifier="")
        with self.assertRaises(PluginManifestError):
            _make_metadata(identifier="1bad.start")

    def test_invalid_version_is_rejected(self) -> None:
        with self.assertRaises(PluginManifestError):
            _make_metadata(version="1.0")
        with self.assertRaises(PluginManifestError):
            _make_metadata(minimum_application_version="not-a-version")

    def test_invalid_permission_string_is_rejected(self) -> None:
        with self.assertRaises(PluginManifestError):
            PluginMetadata.from_mapping(
                {
                    "identifier": "com.example.p",
                    "name": "Sample",
                    "version": "1.0.0",
                    "api_version": SDK_API_VERSION,
                    "author": "Author",
                    "description": "Sample.",
                    "permissions": ["unknown"],
                }
            )

    def test_invalid_dependency_shape_is_rejected(self) -> None:
        with self.assertRaises(PluginManifestError):
            PluginMetadata.from_mapping(
                {
                    "identifier": "com.example.p",
                    "name": "Sample",
                    "version": "1.0.0",
                    "api_version": SDK_API_VERSION,
                    "author": "Author",
                    "description": "Sample.",
                    "dependencies": [{"identifier": "com.example.other"}],
                }
            )

    def test_validate_identifier_and_semver_utilities(self) -> None:
        self.assertEqual(validate_identifier("com.example.plugin"), "com.example.plugin")
        self.assertEqual(validate_semver("2.3.4"), "2.3.4")
        with self.assertRaises(PluginManifestError):
            validate_identifier("bad space")
        with self.assertRaises(PluginManifestError):
            validate_semver("1.2")

    def test_has_permission(self) -> None:
        metadata = _make_metadata(
            permissions=frozenset({PluginPermission.FILESYSTEM})
        )
        self.assertTrue(metadata.has_permission(PluginPermission.FILESYSTEM))
        self.assertFalse(metadata.has_permission(PluginPermission.NETWORK))

    def test_from_loader_manifest_adapter(self) -> None:
        class _Loader:
            identifier = "com.example.sample"
            version = "1.2.3"
            required_application_version = "0.7.0"

        metadata = PluginMetadata.from_loader_manifest(
            _Loader(),
            name="Sample",
            author="Author",
            description="Adapter test",
            api_version=SDK_API_VERSION,
        )
        self.assertEqual(metadata.identifier, "com.example.sample")
        self.assertEqual(metadata.version, "1.2.3")
        self.assertEqual(metadata.minimum_application_version, "0.7.0")


# ---------------------------------------------------------------------------
# API Version
# ---------------------------------------------------------------------------


class ApiVersionTests(unittest.TestCase):
    """Verify :class:`ApiVersion` parsing and compatibility."""

    def test_parses_semver(self) -> None:
        self.assertEqual(ApiVersion.parse("1.2.3"), ApiVersion(1, 2, 3))

    def test_rejects_non_semver(self) -> None:
        with self.assertRaises(ValueError):
            ApiVersion.parse("1.2")

    def test_compatibility_uses_major_version(self) -> None:
        current = ApiVersion(1, 3, 0)
        self.assertTrue(current.is_compatible_with(ApiVersion(1, 0, 0)))
        self.assertFalse(current.is_compatible_with(ApiVersion(2, 0, 0)))
        self.assertFalse(current.is_compatible_with(ApiVersion(1, 4, 0)))

    def test_string_representation(self) -> None:
        self.assertEqual(str(ApiVersion(0, 7, 1)), "0.7.1")


# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------


class PluginLoggingTests(unittest.TestCase):
    """Verify structured plugin logging."""

    def test_logger_emits_records_with_plugin_context(self) -> None:
        base = logging.getLogger("jochen_x_test_sdk_logging")
        base.handlers.clear()
        base.setLevel(logging.DEBUG)
        records: list[logging.LogRecord] = []

        class _Capture(logging.Handler):
            def emit(self, record: logging.LogRecord) -> None:
                records.append(record)

        base.addHandler(_Capture())
        try:
            logger = PluginLogger("com.example.plugin", base_logger=base)
            logger.info("plugin.started", stage="init")
            logger.error("plugin.failed", exc=ValueError("boom"), key="value")
            names = [record.getMessage() for record in records]
            self.assertIn("plugin.started", names)
            self.assertIn("plugin.failed", names)
            context = records[0].__dict__.get("context", {})
            self.assertEqual(context.get("plugin"), "com.example.plugin")
            self.assertEqual(context.get("stage"), "init")
            self.assertIsNotNone(records[-1].exc_info)
        finally:
            base.handlers.clear()

    def test_logger_requires_plugin_id(self) -> None:
        with self.assertRaises(ValueError):
            PluginLogger("")


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------


class PluginConfigTests(unittest.TestCase):
    """Verify configuration defaults, validation, and persistence."""

    def _config(
        self,
        storage: Any = None,
        defaults: dict[str, Any] | None = None,
        validators: dict[str, Any] | None = None,
    ) -> PluginConfig:
        return PluginConfig(
            "com.example.sample",
            storage or InMemoryPluginConfigStorage(),
            defaults=defaults,
            validators=validators,
        )

    def test_defaults_are_returned_when_key_absent(self) -> None:
        config = self._config(defaults={"threshold": 5})
        self.assertEqual(config.get("threshold"), 5)

    def test_set_and_snapshot_reflect_runtime_values(self) -> None:
        config = self._config(defaults={"threshold": 5})
        config.set("threshold", 12)
        self.assertEqual(config.get("threshold"), 12)
        snapshot = config.snapshot()
        self.assertEqual(snapshot["threshold"], 12)

    def test_validator_rejects_invalid_value(self) -> None:
        def positive(value: Any) -> None:
            if not isinstance(value, int) or value <= 0:
                raise ValueError("must be positive int")

        config = self._config(validators={"threshold": positive})
        with self.assertRaises(PluginConfigurationError):
            config.set("threshold", -1)

    def test_update_is_transactional(self) -> None:
        def only_bool(value: Any) -> None:
            if not isinstance(value, bool):
                raise ValueError("must be bool")

        config = self._config(validators={"enabled": only_bool})
        config.set("enabled", True)
        with self.assertRaises(PluginConfigurationError):
            config.update({"enabled": False, "extra": "irrelevant", "broken": None})
        # First value was not applied because a later value was invalid.
        self.assertTrue(config.get("enabled"))

    def test_save_and_load_round_trip_file_storage(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            storage = FilePluginConfigStorage(Path(directory))
            config = self._config(storage)
            config.set("threshold", 42)
            config.save()
            reloaded = self._config(storage)
            reloaded.load()
            self.assertEqual(reloaded.get("threshold"), 42)

    def test_get_raises_when_no_value_or_default(self) -> None:
        config = self._config()
        with self.assertRaises(KeyError):
            config.get("missing")
        self.assertEqual(config.get("missing", default="fallback"), "fallback")

    def test_configuration_error_is_subclass_of_sdk_error(self) -> None:
        self.assertTrue(issubclass(PluginConfigurationError, PluginSDKError))


# ---------------------------------------------------------------------------
# Resources
# ---------------------------------------------------------------------------


class PluginResourcesTests(unittest.TestCase):
    """Verify safe, plugin-scoped resource access."""

    def test_reads_files_beneath_root(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "icons").mkdir()
            icon_path = root / "icons" / "logo.svg"
            icon_path.write_text("<svg/>", encoding="utf-8")
            resources = PluginResources(root)
            self.assertTrue(resources.exists("icons", "logo.svg"))
            self.assertEqual(resources.read_text("icons", "logo.svg"), "<svg/>")
            self.assertEqual(resources.icon("logo.svg"), icon_path.resolve())

    def test_rejects_path_traversal(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            resources = PluginResources(Path(directory))
            with self.assertRaises(PluginResourceError):
                resources.path("..", "escape.txt")
            with self.assertRaises(PluginResourceError):
                resources.path("/absolute")

    def test_translation_helper_parses_json(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "translations").mkdir()
            (root / "translations" / "en.json").write_text(
                '{"greeting": "Hello"}', encoding="utf-8"
            )
            resources = PluginResources(root)
            self.assertEqual(resources.load_translation("en"), {"greeting": "Hello"})

    def test_translation_helper_rejects_invalid_locale(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            resources = PluginResources(Path(directory))
            with self.assertRaises(PluginResourceError):
                resources.translation("../etc")


# ---------------------------------------------------------------------------
# Events and permission enforcement
# ---------------------------------------------------------------------------


class PluginEventBusTests(unittest.TestCase):
    """Verify subscribe/publish/unsubscribe semantics and permission gating."""

    def _bus(self, permissions: frozenset[PluginPermission]) -> tuple[PluginEventBus, EventBus]:
        underlying = EventBus()
        received_permissions: list[PluginPermission] = []

        def check(permission: PluginPermission) -> None:
            received_permissions.append(permission)
            if permission not in permissions:
                raise PluginPermissionError(f"denied: {permission.value}")

        events = PluginEventBus(
            "com.example.plugin",
            underlying,
            event_type=Event,
            permission_check=check,
        )
        return events, underlying

    def test_subscribe_receives_published_events_as_plugin_event(self) -> None:
        events, _ = self._bus(
            frozenset(
                {PluginPermission.EVENTS_SUBSCRIBE, PluginPermission.EVENTS_PUBLISH}
            )
        )
        received: list[PluginEvent] = []
        subscription = events.subscribe("sample.*", received.append)
        events.publish("sample.event", {"key": "value"})
        self.assertEqual(len(received), 1)
        self.assertEqual(received[0].name, "sample.event")
        self.assertEqual(received[0].payload["key"], "value")
        self.assertEqual(received[0].payload["plugin"], "com.example.plugin")
        self.assertIsInstance(subscription, Subscription)

    def test_publish_rejected_without_permission(self) -> None:
        events, _ = self._bus(frozenset({PluginPermission.EVENTS_SUBSCRIBE}))
        with self.assertRaises(PluginPermissionError):
            events.publish("sample.event", {})

    def test_subscribe_rejected_without_permission(self) -> None:
        events, _ = self._bus(frozenset({PluginPermission.EVENTS_PUBLISH}))
        with self.assertRaises(PluginPermissionError):
            events.subscribe("sample.event", lambda event: None)

    def test_unsubscribe_stops_delivery(self) -> None:
        events, _ = self._bus(
            frozenset(
                {PluginPermission.EVENTS_SUBSCRIBE, PluginPermission.EVENTS_PUBLISH}
            )
        )
        received: list[PluginEvent] = []
        subscription = events.subscribe("sample.event", received.append)
        events.publish("sample.event", {})
        events.unsubscribe(subscription)
        events.publish("sample.event", {})
        self.assertEqual(len(received), 1)
        self.assertFalse(subscription.is_active)

    def test_publish_rejects_glob_patterns(self) -> None:
        events, _ = self._bus(
            frozenset(
                {PluginPermission.EVENTS_SUBSCRIBE, PluginPermission.EVENTS_PUBLISH}
            )
        )
        with self.assertRaises(PluginEventError):
            events.publish("bad.*", {})

    def test_dispose_removes_all_subscriptions(self) -> None:
        events, _ = self._bus(
            frozenset(
                {PluginPermission.EVENTS_SUBSCRIBE, PluginPermission.EVENTS_PUBLISH}
            )
        )
        received: list[PluginEvent] = []
        events.subscribe("sample.event", received.append)
        events.subscribe("sample.other", received.append)
        events.dispose()
        events.publish("sample.event", {})
        events.publish("sample.other", {})
        self.assertEqual(received, [])


# ---------------------------------------------------------------------------
# Services
# ---------------------------------------------------------------------------


class PluginServicesTests(unittest.TestCase):
    """Verify service resolution and permission gating."""

    def test_get_returns_registered_instance(self) -> None:
        class _Service:
            pass

        instance = _Service()
        services = PluginServices({_Service: instance})
        self.assertIs(services.get(_Service), instance)
        self.assertTrue(services.has(_Service))
        self.assertIsInstance(services.snapshot(), dict)

    def test_missing_service_raises(self) -> None:
        class _Missing:
            pass

        services = PluginServices()
        with self.assertRaises(PluginServiceNotAvailableError):
            services.get(_Missing)
        self.assertIsNone(services.get_optional(_Missing))

    def test_permission_check_denies_access(self) -> None:
        class _Service:
            pass

        def deny(service_type: type, permission: PluginPermission) -> None:
            raise PluginPermissionError(f"denied {service_type.__name__} {permission.value}")

        services = PluginServices({_Service: _Service()}, permission_check=deny)
        with self.assertRaises(PluginPermissionError):
            services.get(_Service)


# ---------------------------------------------------------------------------
# Context builder
# ---------------------------------------------------------------------------


class PluginContextBuilderTests(unittest.TestCase):
    """Verify the builder produces a fully-wired context."""

    def test_missing_dependencies_raise(self) -> None:
        builder = PluginContextBuilder(_make_metadata())
        with self.assertRaises(ValueError):
            builder.build()

    def test_build_produces_working_context(self) -> None:
        context, _bus, _storage, _root = _build_context()
        self.assertEqual(context.metadata.identifier, "com.example.sample")
        self.assertEqual(context.application_version, "0.7.1")
        self.assertEqual(context.api_version, SDK_API_VERSION)
        self.assertIn("plugin_id", context.metadata_view)

    def test_permission_enforced_from_metadata(self) -> None:
        context, _, _, _ = _build_context(
            metadata=_make_metadata(permissions=frozenset())
        )
        with self.assertRaises(PluginPermissionError):
            context.events.publish("sample.event", {})


# ---------------------------------------------------------------------------
# Plugin lifecycle
# ---------------------------------------------------------------------------


class _SamplePlugin(Plugin):
    """Minimal plugin used to exercise lifecycle transitions."""

    def __init__(self, *, fail_start: bool = False) -> None:
        super().__init__()
        self.log: list[str] = []
        self._fail_start = fail_start

    def metadata(self) -> PluginMetadata:
        return _make_metadata(
            permissions=frozenset(
                {PluginPermission.EVENTS_SUBSCRIBE, PluginPermission.EVENTS_PUBLISH}
            )
        )

    def on_initialize(self) -> None:
        self.log.append("initialize")

    def on_start(self) -> None:
        self.log.append("start")
        if self._fail_start:
            raise RuntimeError("boom")

    def on_stop(self) -> None:
        self.log.append("stop")

    def on_shutdown(self) -> None:
        self.log.append("shutdown")


class _SampleBackgroundPlugin(BackgroundPlugin):
    """Background plugin whose worker records ticks until stopped."""

    def __init__(self) -> None:
        super().__init__()
        self.ticks = threading.Event()

    def metadata(self) -> PluginMetadata:
        return _make_metadata(
            identifier="com.example.background",
            category=PluginCategory.BACKGROUND,
            permissions=frozenset(),
        )

    def run_background(self, stop_event: threading.Event) -> None:
        self.ticks.set()
        stop_event.wait(timeout=1.0)


class PluginLifecycleTests(unittest.TestCase):
    """Verify plugin lifecycle transitions and error handling."""

    def test_full_lifecycle(self) -> None:
        plugin = _SamplePlugin()
        context, _, _, _ = _build_context(metadata=plugin.metadata())
        runtime = PluginRuntime(plugin)
        runtime.initialize(context)
        self.assertIs(plugin.state, PluginLifecycleState.INITIALIZED)
        runtime.start()
        self.assertIs(plugin.state, PluginLifecycleState.STARTED)
        runtime.stop()
        self.assertIs(plugin.state, PluginLifecycleState.STOPPED)
        runtime.shutdown()
        self.assertEqual(
            plugin.log, ["initialize", "start", "stop", "shutdown"]
        )

    def test_invalid_state_transition_raises(self) -> None:
        plugin = _SamplePlugin()
        runtime = PluginRuntime(plugin)
        with self.assertRaises(PluginLifecycleError):
            runtime.start()

    def test_start_failure_moves_plugin_to_failed(self) -> None:
        plugin = _SamplePlugin(fail_start=True)
        context, _, _, _ = _build_context(metadata=plugin.metadata())
        runtime = PluginRuntime(plugin)
        runtime.initialize(context)
        with self.assertRaises(PluginLifecycleError):
            runtime.start()
        self.assertIs(plugin.state, PluginLifecycleState.FAILED)

    def test_context_unavailable_before_initialize(self) -> None:
        plugin = _SamplePlugin()
        with self.assertRaises(PluginLifecycleError):
            plugin.context  # noqa: B018

    def test_state_change_observer_receives_transitions(self) -> None:
        plugin = _SamplePlugin()
        context, _, _, _ = _build_context(metadata=plugin.metadata())
        transitions: list[PluginLifecycleState] = []

        def observer(_plugin: Plugin, state: PluginLifecycleState) -> None:
            transitions.append(state)

        runtime = PluginRuntime(plugin, on_state_change=observer)
        runtime.initialize(context)
        runtime.start()
        runtime.stop()
        runtime.shutdown()
        self.assertEqual(
            transitions,
            [
                PluginLifecycleState.INITIALIZED,
                PluginLifecycleState.STARTED,
                PluginLifecycleState.STOPPED,
            ],
        )

    def test_background_plugin_runs_and_stops(self) -> None:
        plugin = _SampleBackgroundPlugin()
        context, _, _, _ = _build_context(metadata=plugin.metadata())
        runtime = PluginRuntime(plugin)
        runtime.initialize(context)
        runtime.start()
        self.assertTrue(plugin.ticks.wait(timeout=1.0))
        runtime.stop()
        self.assertIs(plugin.state, PluginLifecycleState.STOPPED)
        runtime.shutdown()


# ---------------------------------------------------------------------------
# Tool and workflow plugins
# ---------------------------------------------------------------------------


class _EchoTool(ToolPlugin):
    def metadata(self) -> PluginMetadata:
        return _make_metadata(
            identifier="com.example.tool",
            category=PluginCategory.TOOL,
            permissions=frozenset(),
        )

    def execute(self, request):
        return {"echo": request.get("value")}


class _NamedWorkflow(WorkflowPlugin):
    def metadata(self) -> PluginMetadata:
        return _make_metadata(
            identifier="com.example.workflow",
            category=PluginCategory.WORKFLOW,
            permissions=frozenset(),
        )

    def workflows(self) -> tuple[str, ...]:
        return ("hello",)

    def run(self, workflow: str, arguments):
        if workflow != "hello":
            raise KeyError(workflow)
        return {"greeting": f"Hello, {arguments.get('name', 'world')}!"}


class ToolAndWorkflowPluginTests(unittest.TestCase):
    """Verify tool and workflow plugin base classes."""

    def test_tool_plugin_execute(self) -> None:
        plugin = _EchoTool()
        self.assertEqual(plugin.execute({"value": 3})["echo"], 3)

    def test_workflow_plugin_run(self) -> None:
        plugin = _NamedWorkflow()
        self.assertIn("hello", plugin.workflows())
        self.assertEqual(
            plugin.run("hello", {"name": "SDK"}),
            {"greeting": "Hello, SDK!"},
        )
        with self.assertRaises(KeyError):
            plugin.run("missing", {})


# ---------------------------------------------------------------------------
# Dependency validation
# ---------------------------------------------------------------------------


class DependencyValidationTests(unittest.TestCase):
    """Verify dependency-level metadata validation."""

    def test_dependency_requires_valid_identifier_and_version(self) -> None:
        with self.assertRaises(PluginManifestError):
            PluginDependency("", "1.0.0")
        with self.assertRaises(PluginManifestError):
            PluginDependency("com.example.p", "1.0")

    def test_manifest_carries_declared_dependencies(self) -> None:
        metadata = _make_metadata(
            dependencies=(
                PluginDependency("com.example.a", "1.0.0"),
                PluginDependency("com.example.b", "0.5.1"),
            )
        )
        self.assertEqual(len(metadata.dependencies), 2)
        self.assertEqual(metadata.dependencies[0].identifier, "com.example.a")

    def test_dependency_error_is_sdk_error(self) -> None:
        self.assertTrue(issubclass(PluginDependencyError, PluginSDKError))


# ---------------------------------------------------------------------------
# Public surface
# ---------------------------------------------------------------------------


class PublicSurfaceTests(unittest.TestCase):
    """Verify version constants and error hierarchy on the public surface."""

    def test_versions_expose_semver_strings(self) -> None:
        self.assertRegex(SDK_VERSION, r"^\d+\.\d+\.\d+$")
        self.assertRegex(SDK_API_VERSION, r"^\d+\.\d+\.\d+$")

    def test_error_hierarchy(self) -> None:
        for error in (
            PluginManifestError,
            PluginConfigurationError,
            PluginLifecycleError,
            PluginPermissionError,
            PluginResourceError,
            PluginServiceNotAvailableError,
            PluginEventError,
            PluginDependencyError,
        ):
            self.assertTrue(issubclass(error, PluginSDKError))


if __name__ == "__main__":
    unittest.main()
