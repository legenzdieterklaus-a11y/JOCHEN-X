"""WP-002 Host Service & Extensibility tests (FR-003, FR-004).

Covers AC-003.1 (host services registered in the ServiceRegistry and
retrievable via its API), AC-003.2 (service description includes name, type,
and availability point), AC-004.1 (plugins register new functionality via
the defined extension points) and AC-004.2 (extension registration is
additive — no existing API signature or contract changes), including the
SDK-side integration through :class:`sdk.PluginExtensions`.
"""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
from typing import Any

from core.events import Event, EventBus
from core.extensions import (
    EXTENSION_POINT_CONTRACTS,
    CommandExtension,
    ExtensionPoint,
    ExtensionRegistry,
    ToolExtension,
    UIExtension,
    WorkflowExtension,
)
from core.registry import Lifetime, ServiceDescriptor, ServiceRegistry

import sdk
from sdk import (
    InMemoryPluginConfigStorage,
    PluginCategory,
    PluginContextBuilder,
    PluginExtensions,
    PluginMetadata,
    PluginPermission,
    PluginSDKError,
)
from sdk.version import SDK_API_VERSION


class _Widget:
    pass


class _ToolStub:
    identifier = "sample.tool"


def _make_metadata() -> PluginMetadata:
    return PluginMetadata(
        identifier="com.example.extender",
        name="Extender Plugin",
        version="1.0.0",
        api_version=SDK_API_VERSION,
        author="JOCHEN X Team",
        description="Plugin used by WP-002 extension tests.",
        category=PluginCategory.GENERAL,
        permissions=frozenset({PluginPermission.EVENTS_SUBSCRIBE}),
        dependencies=(),
        minimum_application_version="0.7.0",
    )


class HostServiceDescriptionTests(unittest.TestCase):
    def test_registered_services_are_retrievable_via_registry_api(self) -> None:
        registry = ServiceRegistry()
        bus = EventBus()
        registry.register(EventBus, bus)
        registry.register_type(_Widget, _Widget, lifetime=Lifetime.TRANSIENT)
        self.assertIs(registry.get(EventBus), bus)
        self.assertIsInstance(registry.get(_Widget), _Widget)

    def test_instance_description_has_name_type_and_availability(self) -> None:
        registry = ServiceRegistry()
        registry.register(EventBus, EventBus())
        descriptor = registry.describe(EventBus)
        self.assertEqual(descriptor.key, "EventBus")
        self.assertEqual(descriptor.service_type, "EventBus")
        self.assertEqual(descriptor.available_since, "registration")
        self.assertTrue(descriptor.initialized)

    def test_factory_description_has_name_type_and_availability(self) -> None:
        registry = ServiceRegistry()
        registry.register_factory(_Widget, _Widget)
        descriptor = registry.describe(_Widget)
        self.assertEqual(descriptor.key, "_Widget")
        self.assertEqual(descriptor.service_type, "_Widget")
        self.assertEqual(descriptor.available_since, "on_first_resolve")
        self.assertFalse(descriptor.initialized)

    def test_type_registration_description_names_implementation(self) -> None:
        class Implementation(_Widget):
            pass

        registry = ServiceRegistry()
        registry.register_type(_Widget, Implementation)
        descriptor = registry.describe(_Widget)
        self.assertEqual(descriptor.key, "_Widget")
        self.assertEqual(descriptor.service_type, "Implementation")

    def test_explicit_availability_label_is_kept(self) -> None:
        registry = ServiceRegistry()
        registry.register(EventBus, EventBus(), available_since="bootstrap")
        self.assertEqual(registry.describe(EventBus).available_since, "bootstrap")

    def test_every_descriptor_carries_the_full_description(self) -> None:
        registry = ServiceRegistry()
        registry.register(EventBus, EventBus())
        registry.register_type(_Widget, _Widget)
        for descriptor in registry.descriptors():
            with self.subTest(service=descriptor.key):
                self.assertTrue(descriptor.key)
                self.assertTrue(descriptor.service_type)
                self.assertTrue(descriptor.available_since)

    def test_describe_unregistered_raises_lookup_error(self) -> None:
        with self.assertRaises(LookupError):
            ServiceRegistry().describe(EventBus)

    def test_descriptor_stays_backward_compatible(self) -> None:
        descriptor = ServiceDescriptor("Legacy", Lifetime.SINGLETON, True, ())
        self.assertEqual(descriptor.service_type, "")
        self.assertEqual(descriptor.available_since, "registration")


class ExtensionPointTests(unittest.TestCase):
    def test_extension_points_are_formally_defined(self) -> None:
        self.assertEqual(set(EXTENSION_POINT_CONTRACTS), set(ExtensionPoint))
        self.assertIs(EXTENSION_POINT_CONTRACTS[ExtensionPoint.TOOLS], ToolExtension)
        self.assertIs(EXTENSION_POINT_CONTRACTS[ExtensionPoint.UI], UIExtension)
        self.assertIs(EXTENSION_POINT_CONTRACTS[ExtensionPoint.COMMANDS], CommandExtension)
        self.assertIs(EXTENSION_POINT_CONTRACTS[ExtensionPoint.WORKFLOWS], WorkflowExtension)

    def test_register_and_retrieve_extension(self) -> None:
        registry = ExtensionRegistry()
        tool = _ToolStub()
        registry.register(ExtensionPoint.TOOLS, tool)
        self.assertEqual(registry.extensions(ExtensionPoint.TOOLS), (tool,))
        self.assertIs(registry.find("tools", "sample.tool"), tool)
        self.assertIsNone(registry.find("tools", "missing"))

    def test_undefined_point_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            ExtensionRegistry().register("unknown-point", _ToolStub())

    def test_extension_without_identifier_is_rejected(self) -> None:
        with self.assertRaises(TypeError):
            ExtensionRegistry().register(ExtensionPoint.TOOLS, object())

    def test_duplicate_identifier_is_rejected(self) -> None:
        registry = ExtensionRegistry()
        registry.register(ExtensionPoint.TOOLS, _ToolStub())
        with self.assertRaises(ValueError):
            registry.register(ExtensionPoint.TOOLS, _ToolStub())

    def test_points_are_isolated(self) -> None:
        registry = ExtensionRegistry()
        registry.register(ExtensionPoint.TOOLS, _ToolStub())
        self.assertEqual(registry.extensions(ExtensionPoint.UI), ())


class SdkExtensionIntegrationTests(unittest.TestCase):
    def _build_context(self, registrar: Any | None) -> Any:
        builder = (
            PluginContextBuilder(_make_metadata())
            .with_event_bus(EventBus(), event_type=Event)
            .with_config_storage(InMemoryPluginConfigStorage())
            .with_resources_root(Path(tempfile.mkdtemp(prefix="sdk-ext-test-")))
        )
        if registrar is not None:
            builder.with_extensions(registrar)
        return builder.build()

    def test_plugin_registers_extension_through_context(self) -> None:
        host_registry = ExtensionRegistry()
        context = self._build_context(host_registry.register)
        self.assertIsInstance(context.extensions, PluginExtensions)
        tool = _ToolStub()
        context.extensions.register("tools", tool)
        self.assertIs(host_registry.find(ExtensionPoint.TOOLS, "sample.tool"), tool)

    def test_registration_errors_pass_through_unchanged(self) -> None:
        context = self._build_context(ExtensionRegistry().register)
        with self.assertRaises(ValueError):
            context.extensions.register("unknown-point", _ToolStub())
        with self.assertRaises(TypeError):
            context.extensions.register("tools", object())

    def test_context_without_registrar_rejects_registration(self) -> None:
        context = self._build_context(None)
        with self.assertRaises(PluginSDKError):
            context.extensions.register("tools", _ToolStub())

    def test_registration_changes_no_existing_contract(self) -> None:
        baseline_exports = {
            "SDK_API_VERSION", "SDK_API_VERSION_INFO", "SDK_NAME", "SDK_VERSION",
            "SDK_VERSION_INFO", "ApiVersion", "PluginCategory", "PluginDependency",
            "PluginMetadata", "PluginPermission", "SignatureStatus",
            "validate_identifier", "validate_semver", "EventBusPort",
            "FilePluginConfigStorage", "InMemoryPluginConfigStorage",
            "PermissionCheck", "PluginConfig", "PluginConfigStorage",
            "PluginContext", "PluginContextBuilder", "PluginEvent",
            "PluginEventBus", "PluginEventHandler", "PluginLogger",
            "PluginResources", "PluginServices", "ServicePermissionCheck",
            "Subscription", "Validator", "BackgroundPlugin", "Plugin",
            "PluginLifecycleState", "PluginRuntime", "ToolPlugin", "UIPlugin",
            "WorkflowPlugin", "PluginConfigurationError", "PluginDependencyError",
            "PluginEventError", "PluginLifecycleError", "PluginManifestError",
            "PluginPermissionError", "PluginResourceError", "PluginSDKError",
            "PluginServiceNotAvailableError",
        }
        self.assertTrue(baseline_exports.issubset(set(sdk.__all__)))
        host_registry = ExtensionRegistry()
        context = self._build_context(host_registry.register)
        context.extensions.register("tools", _ToolStub())
        self.assertTrue(baseline_exports.issubset(set(sdk.__all__)))
        self.assertEqual(sdk.SDK_API_VERSION, SDK_API_VERSION)


if __name__ == "__main__":
    unittest.main()
