# Plugin SDK – Specification v0.7.1

The JOCHEN X Enterprise Plugin SDK is the sole official programming
interface for external plugin authors. It sits on top of the frozen v0.7.0
Plugin Framework and provides a stable, minimal, strictly-typed, and
independently-testable surface that never exposes framework internals.

This document is authoritative for every SDK-related topic. It complements
the [Plugin Framework](extensions.md) specification without changing it.

**Cross-references:**

| Document | Relevance |
|---|---|
| [Foundation Architecture](architecture.md) | Bootstrap order, composition root |
| [Core](core.md) | `EventBus`, `ServiceRegistry`, version model |
| [Events](events.md) | Underlying delivery semantics |
| [Plugin Framework](extensions.md) | Manifest discovery, plugin catalog |
| [Security](security.md) | Trust model, capability grants |
| [ADR-008](adr/008-plugin-context-definition.md) | Plugin context definition (resolved by this SDK) |
| [ADR-010](adr/010-plugin-sdk-architecture.md) | Plugin SDK architecture (accepted) |

---

## 1. Design Principles

The SDK is governed by these non-negotiable principles:

| Principle | Application |
|---|---|
| **Stability first** | Public SDK APIs never break within a major version. Additive changes only. |
| **Minimal surface** | Only what plugin authors need is exposed. No framework re-exports. |
| **Strict typing** | Every public API is fully typed and covered by dataclasses, enums, or protocols. |
| **Enterprise readiness** | Value objects are immutable; APIs are thread-safe by construction. |
| **Composition over inheritance** | The runtime composes plugins through `PluginRuntime`; plugin classes stay narrow. |
| **Dependency inversion** | The SDK depends on protocols; hosts inject concrete services. |
| **Zero global state** | No global singletons. Every dependency is passed explicitly. |
| **Version transparency** | SDK version and API version are separate, comparable semver values. |

---

## 2. Package Layout

```
sdk/
├── __init__.py     Re-exports the entire public SDK surface
├── version.py      SDK_VERSION, SDK_API_VERSION, ApiVersion value type
├── errors.py       PluginSDKError taxonomy
├── manifest.py     PluginMetadata, PluginCategory, PluginPermission, ...
├── logging.py      PluginLogger
├── config.py       PluginConfig, PluginConfigStorage, storage backends
├── resources.py    PluginResources
├── events.py       PluginEventBus, PluginEvent, Subscription
├── services.py     PluginServices
├── context.py      PluginContext, PluginContextBuilder
└── plugin.py       Plugin, BackgroundPlugin, UIPlugin, ToolPlugin,
                    WorkflowPlugin, PluginRuntime, PluginLifecycleState
```

The SDK is a pure Python package; importing `sdk` has no side effects on
the foundation and does not start any thread, open any file, or connect to
any service.

---

## 3. SDK Overview

The SDK exposes four thematic surfaces:

1. **Manifest** – how a plugin describes itself.
2. **Context** – what a plugin receives at runtime.
3. **Lifecycle** – how a plugin transitions from unloaded to stopped.
4. **Errors** – what a plugin may raise or catch.

Every façade in the context is a thin adapter over foundation contracts;
plugins never import from `core`, `app`, `plugins`, `developer`, `services`,
or `ui` packages directly.

---

## 4. API Reference

### 4.1 Version constants – `sdk.version`

| Symbol | Type | Description |
|---|---|---|
| `SDK_NAME` | `str` | Stable distribution identifier (`"jochen-x-sdk"`). |
| `SDK_VERSION` | `str` | Released SDK package semver (`"0.7.1"`). |
| `SDK_API_VERSION` | `str` | Public plugin API contract semver (`"1.0.0"`). |
| `SDK_VERSION_INFO` | `ApiVersion` | Parsed :class:`ApiVersion` for `SDK_VERSION`. |
| `SDK_API_VERSION_INFO` | `ApiVersion` | Parsed :class:`ApiVersion` for `SDK_API_VERSION`. |
| `ApiVersion` | `dataclass` | Immutable, comparable `major.minor.patch` value type. |

`ApiVersion.is_compatible_with(required)` implements the well-known
major-version compatibility rule shared with the foundation.

### 4.2 Manifest – `sdk.manifest`

| Symbol | Type | Description |
|---|---|---|
| `PluginCategory` | `StrEnum` | Coarse plugin classification. |
| `PluginPermission` | `StrEnum` | Declared capability the plugin requests. |
| `SignatureStatus` | `StrEnum` | Integrity classification set by the host. |
| `PluginDependency` | `dataclass` | Declared dependency on another plugin. |
| `PluginMetadata` | `dataclass` | Immutable, validated plugin metadata. |
| `validate_identifier` | `Callable` | Public identifier validator. |
| `validate_semver` | `Callable` | Public strict semver validator. |

Every `PluginMetadata` field is validated in `__post_init__`. Additional
constructors:

* `PluginMetadata.from_mapping(data)` – parse from a JSON-friendly mapping
  (e.g. a TOML-loaded dictionary).
* `PluginMetadata.from_loader_manifest(...)` – adapter that ingests the
  foundation's `plugins.loader.PluginManifest` and combines it with
  additional descriptive fields.

`PluginMetadata.to_dict()` yields a JSON-friendly mapping for serialization.

### 4.3 Errors – `sdk.errors`

All SDK exceptions inherit from `PluginSDKError`:

| Exception | Meaning |
|---|---|
| `PluginManifestError` | Invalid or incomplete manifest. |
| `PluginConfigurationError` | Invalid or unreadable/unsavable configuration. |
| `PluginPermissionError` | Operation denied by the plugin's declared capabilities. |
| `PluginLifecycleError` | Illegal or out-of-order lifecycle transition. |
| `PluginDependencyError` | Declared dependency could not be satisfied. |
| `PluginResourceError` | Missing/unreadable/path-unsafe resource. |
| `PluginServiceNotAvailableError` | Requested service is not exposed to the plugin. |
| `PluginEventError` | Invalid event name/handler/subscription operation. |

Framework-internal exceptions are never re-exported; hosts translate them
into SDK exceptions at the boundary.

### 4.4 Logging – `sdk.logging`

`PluginLogger` is a structured logger that:

* Derives from an injected base `logging.Logger` (defaults to `jochen_x`).
* Prefixes every record with the plugin identifier under
  `extra["context"]["plugin"]`.
* Emits at `debug`, `info`, `warning`, `error`, `critical`, and `exception`
  severities with exception attachments for the two highest levels.

The logger never installs its own handlers; the host controls formatting
and rotation.

### 4.5 Configuration – `sdk.config`

`PluginConfig` is the sole configuration API for plugins. It offers:

| API | Semantics |
|---|---|
| `get(key, default=...)` | Return value, then default, then caller default; else `KeyError`. |
| `set(key, value)` | Validate and store a value. |
| `update(mapping)` | Transactional multi-key update; all-or-nothing. |
| `delete(key)` | Remove a runtime override; declared default is unaffected. |
| `register_default(key, value)` | Register/replace a default value. |
| `register_validator(key, callable)` | Register/replace a validator. |
| `snapshot()` | Return a JSON-friendly copy of the effective configuration. |
| `save()` / `load()` | Persist via the injected `PluginConfigStorage`. |

Storage is defined by the `PluginConfigStorage` protocol.
`InMemoryPluginConfigStorage` and `FilePluginConfigStorage` (JSON files) are
provided. No filesystem detail is exposed to plugin code.

### 4.6 Resources – `sdk.resources`

`PluginResources` resolves paths under a plugin-private root supplied by
the host. It guarantees:

* All accesses stay inside the root (path traversal rejected).
* Absolute components are rejected.
* Convenience helpers for `icons/`, `assets/`, and `translations/*.json`.
* `load_translation(locale)` returns a validated `str → str` mapping.

### 4.7 Events – `sdk.events`

The SDK provides a plugin-scoped façade over the shared event bus:

* `PluginEvent(name, payload)` – SDK-owned value type.
* `PluginEventBus.subscribe(event_name, handler, *, priority, receive_sticky)`
  returns a `Subscription`.
* `PluginEventBus.publish(name, payload=None, *, sticky=False)` publishes a
  new event; wildcards are rejected on publish.
* `PluginEventBus.unsubscribe(subscription)` disposes of a subscription.
* `PluginEventBus.dispose()` drops every subscription owned by the wrapper.

Publish and subscribe are gated on `EVENTS_PUBLISH` and `EVENTS_SUBSCRIBE`
permissions respectively when a permission check is configured (the default
context builder wires this automatically).

### 4.8 Services – `sdk.services`

`PluginServices` is a read-only, typed façade over a host-provided mapping
of service types to instances. Plugins request services by public type or
protocol; the host decides which types are visible.

```python
class SecretsPort(Protocol):
    def get(self, name: str) -> str | None: ...

# In the plugin:
secrets = context.services.get(SecretsPort)
```

Missing services raise `PluginServiceNotAvailableError`; denied services
raise `PluginPermissionError`. Plugins can also call
`services.get_optional(type)` for opportunistic lookups.

### 4.9 Context – `sdk.context`

`PluginContext` is an immutable dataclass exposing the following fields:

| Field | Type | Description |
|---|---|---|
| `metadata` | `PluginMetadata` | Validated plugin manifest. |
| `logger` | `PluginLogger` | Structured plugin logger. |
| `events` | `PluginEventBus` | Plugin-scoped event façade. |
| `services` | `PluginServices` | Plugin-scoped service resolver. |
| `config` | `PluginConfig` | Plugin-owned configuration store. |
| `resources` | `PluginResources` | Plugin-scoped resource resolver. |
| `application_version` | `str` | Host application semver. |
| `api_version` | `str` | SDK API version implemented by the host. |
| `metadata_view` | `Mapping[str, Any]` | Informational summary safe to log. |

Hosts create contexts through `PluginContextBuilder`:

```python
context = (
    PluginContextBuilder(metadata)
    .with_event_bus(event_bus, event_type=Event)
    .with_service(SecretsPort, secrets_service)
    .with_config_storage(FilePluginConfigStorage(config_root))
    .with_resources_root(resources_root)
    .with_application_version(settings.version)
    .build()
)
```

The builder wires permission enforcement automatically based on the
plugin's declared `PluginPermission` set.

### 4.10 Plugin base classes and lifecycle – `sdk.plugin`

The SDK provides five plugin base classes and the composed runtime that
drives their lifecycle.

| Class | Extends | Extra abstract API |
|---|---|---|
| `Plugin` | `abc.ABC` | `metadata` |
| `BackgroundPlugin` | `Plugin` | `run_background(stop_event)` |
| `UIPlugin` | `Plugin` | `create_widget(parent)` |
| `ToolPlugin` | `Plugin` | `execute(request)` |
| `WorkflowPlugin` | `Plugin` | `workflows`, `run(workflow, arguments)` |

`Plugin` lifecycle hooks (all default to no-ops):

* `on_initialize()` – after context attach.
* `on_start()` – transition `INITIALIZED → STARTED`.
* `on_stop()` – transition `STARTED → STOPPED`.
* `on_shutdown()` – after stop; dispose of long-lived resources.

The state machine is exposed by `PluginLifecycleState`:

```
UNLOADED → INITIALIZED → STARTED → STOPPED
                 ↓          ↓
                FAILED    FAILED
```

Errors during any transition move the plugin to `FAILED` and abort further
progression.

`PluginRuntime` composes a plugin and drives it:

```python
runtime = PluginRuntime(plugin, on_state_change=log_transition)
runtime.initialize(context)
runtime.start()
# ... run ...
runtime.stop()
runtime.shutdown()
```

`shutdown()` is idempotent; it stops the plugin if still running, invokes
`on_shutdown`, and disposes of every live subscription the SDK owns.

---

## 5. Plugin Lifecycle

The lifecycle is the sole state machine exposed to plugin authors and never
changes across a minor SDK release.

| State | Enters After | Guarantees |
|---|---|---|
| `UNLOADED` | Plugin constructed. | No context attached. |
| `INITIALIZED` | `initialize(context)` succeeds. | Context is attached; `on_initialize` has completed. |
| `STARTED` | `start()` succeeds. | `on_start` has completed; background workers (if any) are running. |
| `STOPPED` | `stop()` succeeds. | `on_stop` has completed; workers joined. |
| `FAILED` | Any hook raises. | State is terminal; `shutdown` is still safe to invoke. |

Lifecycle transitions publish state observably through the
`on_state_change` callback registered on `PluginRuntime`; hosts typically
bridge this to a bus event or the developer platform.

---

## 6. Events

Plugins subscribe and publish through `PluginEventBus`. Event names are
free-form strings using dotted namespaces. Recommended conventions:

* Plugins publish only under their own identifier prefix:
  `<plugin_id>.<event_name>`.
* Plugins may subscribe to any documented framework namespace, subject to
  their declared `EVENTS_SUBSCRIBE` permission.

Async delivery is supported when the handler is `async def`; sticky
delivery is disabled for async handlers to preserve the foundation's
publishing semantics.

---

## 7. Services

Hosts decide which service types are exposed to a plugin by supplying a
mapping to `PluginContextBuilder.with_service` /
`.with_services`. Plugin authors:

* Should depend only on **public protocols** (SDK-provided or defined by
  their own team) so implementation changes on the host side do not affect
  plugins.
* Should call `services.has(type)` or `services.get_optional(type)` when a
  feature is optional.

---

## 8. Logging

Plugin logs share the foundation's rotating log file. Every SDK log record
includes the plugin identifier under `extra["context"]["plugin"]` so log
consumers can filter deterministically.

Recommended log field names:

| Field | Purpose |
|---|---|
| `stage` | Lifecycle stage or operation label. |
| `identifier` | Related identifier (task id, workflow id, …). |
| `duration_ms` | Measured duration. |
| `outcome` | `success` / `failure` / `denied`. |

The SDK never rotates files or opens sinks; that responsibility remains
with the host.

---

## 9. Configuration

`PluginConfig` guarantees:

* **Defaults** validate at registration time.
* **Runtime writes** validate at `set()`/`update()`.
* **Load** validates every persisted value; a rejected payload aborts the
  load without touching runtime state.
* **Save** persists exactly what `set` accepted, without mixing defaults.

Recommended patterns:

* Register defaults during `on_initialize`.
* Call `load()` immediately after registering defaults so a persisted
  profile overrides them.
* Call `save()` after every user-driven setting change; the host controls
  file rotation and location.

---

## 10. Best Practices

1. **Return metadata as a constant.** Build `PluginMetadata` once in a
   module-level function so it is validated at import time.
2. **Do not import from `core`, `app`, `plugins`, `services`, `ui`,
   `developer`.** Everything a plugin needs is exposed through `sdk`.
3. **Never spawn threads outside `BackgroundPlugin`.** Long-running work
   must be observable to the runtime so it can be stopped cleanly.
4. **Never touch the UI thread from a worker.** Always marshal back via a
   host-supplied dispatcher (exposed through `services`).
5. **Prefer typed services over strings.** Declare a protocol and use it
   as the service key.
6. **Handle `PluginServiceNotAvailableError`.** Not every host exposes
   every service; plugins should degrade gracefully.
7. **Declare every permission you use.** The context builder denies undeclared
   capabilities even when the underlying service is available.
8. **Guard `on_stop` for idempotency.** The runtime may call it more than
   once during failure recovery.

---

## 11. Example Plugin

```python
from collections.abc import Mapping
from typing import Any

from sdk import (
    Plugin,
    PluginCategory,
    PluginContext,
    PluginMetadata,
    PluginPermission,
    SDK_API_VERSION,
)


def _metadata() -> PluginMetadata:
    return PluginMetadata(
        identifier="com.example.greeter",
        name="Greeter",
        version="1.0.0",
        api_version=SDK_API_VERSION,
        author="Example Corp",
        description="Emits a greeting on demand.",
        category=PluginCategory.TOOL,
        permissions=frozenset(
            {
                PluginPermission.EVENTS_PUBLISH,
                PluginPermission.CONFIGURATION,
            }
        ),
    )


class GreeterPlugin(Plugin):
    def metadata(self) -> PluginMetadata:
        return _metadata()

    def on_initialize(self) -> None:
        self.context.config.register_default("greeting", "Hello")
        self.context.config.load()

    def on_start(self) -> None:
        greeting = self.context.config.get("greeting")
        self.context.logger.info("greeter.started", greeting=greeting)
        self.context.events.publish(
            "com.example.greeter.ready",
            {"greeting": greeting},
        )

    def on_stop(self) -> None:
        self.context.logger.info("greeter.stopped")

    def greet(self, name: str) -> str:
        greeting = self.context.config.get("greeting")
        return f"{greeting}, {name}!"
```

The host constructs the context via `PluginContextBuilder`, calls
`runtime.initialize` and `runtime.start`, and disposes of the plugin
through `runtime.shutdown` at application shutdown.

---

## 12. Versioning Strategy

The SDK ships with two independent semantic version tracks:

| Track | Constant | Governs |
|---|---|---|
| SDK release | `SDK_VERSION` | The SDK package version. Aligned with the JOCHEN X application version. |
| Plugin API | `SDK_API_VERSION` | Backwards-compatibility surface for plugins. |

**Compatibility rules:**

* Plugin metadata declares the `api_version` the plugin was built against.
* Hosts refuse to load a plugin whose `api_version` is a different major
  than the host's `SDK_API_VERSION`.
* Additive changes (new methods, new fields with defaults, new enum
  members) increment the minor version.
* Bug fixes and clarifications increment the patch version.
* Any breaking change increments the major version and, if unavoidable,
  ships with a migration guide.

**Deprecation policy:**

* A deprecated API stays available for at least one full minor version and
  is documented in the SDK release notes.
* Deprecated APIs emit `DeprecationWarning`; no silent removals.

---

## 13. Testability

Every SDK subsystem is independently testable:

| Subsystem | Test Location | Strategy |
|---|---|---|
| Manifest & validation | `tests/test_sdk.py` | Constructed metadata; error cases. |
| Version | `tests/test_sdk.py` | Semver parsing and compatibility. |
| Logging | `tests/test_sdk.py` | Attach a capture handler to the base logger. |
| Configuration | `tests/test_sdk.py` | In-memory and JSON file storage backends. |
| Resources | `tests/test_sdk.py` | Temporary directories; traversal rejection. |
| Events | `tests/test_sdk.py` | Real `core.events.EventBus`; permission gating. |
| Services | `tests/test_sdk.py` | Public protocols; missing/denied cases. |
| Context builder | `tests/test_sdk.py` | Required injections; permission-derived enforcement. |
| Plugin lifecycle | `tests/test_sdk.py` | All hooks; failure paths; observer callbacks. |
| BackgroundPlugin | `tests/test_sdk.py` | Real worker thread; cooperative stop. |
| Tool/Workflow | `tests/test_sdk.py` | Public method invocation with typed payloads. |

The SDK never requires a Qt event loop for unit tests, but `UIPlugin` is
verified by consumers who inject their own widget factory.

---

## 14. Definition of Done – v0.7.1

- [x] All plugin base classes are shipped with clearly defined lifecycles.
- [x] Manifest models cover every required field with validation.
- [x] `PluginContext` exposes only SDK-defined façades.
- [x] Event, service, logging, configuration, and resource APIs are all
      exposed exclusively through the SDK.
- [x] SDK exceptions form a shallow, publicly documented hierarchy.
- [x] `docs/sdk.md` documents the entire SDK.
- [x] `ADR-010` records the SDK architecture decision.
- [x] Comprehensive unit tests exist for every SDK subsystem.
- [x] No existing foundation module was modified.
- [x] No breaking changes to the existing public surface.
