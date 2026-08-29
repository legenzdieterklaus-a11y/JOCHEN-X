# Plugin SDK – Specification v0.9.0

The JOCHEN X Enterprise Plugin SDK is the sole official programming
interface for external plugin authors. It sits on top of the
[Plugin Framework](extensions.md) and provides a stable, minimal,
strictly-typed, and independently-testable surface that never exposes
framework internals.

This specification describes `SDK_VERSION` **0.9.0** implementing
`SDK_API_VERSION` **1.0.0**; both constants are defined in
[`sdk/version.py`](../sdk/version.py) and are authoritative over any prose
in this document.

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
├── context.py      PluginContext, PluginContextBuilder,
│                   PluginExtensions, ExtensionRegistrar
└── plugin.py       Plugin, BackgroundPlugin, UIPlugin, ToolPlugin,
                    WorkflowPlugin, PluginRuntime, PluginLifecycleState
```

The SDK is a pure Python package; importing `sdk` has no side effects on
the foundation and does not start any thread, open any file, or connect to
any service.

---

## 3. SDK Overview

The SDK exposes five thematic surfaces:

1. **Manifest** – how a plugin describes itself.
2. **Context** – what a plugin receives at runtime.
3. **Extension points** – where a plugin contributes functionality.
4. **Lifecycle** – how a plugin transitions from unloaded to stopped.
5. **Errors** – what a plugin may raise or catch.

Every façade in the context is a thin adapter over foundation contracts;
plugins never import from `core`, `app`, `plugins`, `developer`, `services`,
or `ui` packages directly.

---

## 4. API Reference

### 4.1 Version constants – `sdk.version`

| Symbol | Type | Description |
|---|---|---|
| `SDK_NAME` | `str` | Stable distribution identifier (`"jochen-x-sdk"`). |
| `SDK_VERSION` | `str` | Released SDK package semver (`"0.9.0"`). |
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

| Symbol | Type | Description |
|---|---|---|
| `PluginConfig` | `class` | The configuration store itself. |
| `PluginConfigStorage` | `Protocol` | Persistence port implemented by the backends below. |
| `InMemoryPluginConfigStorage` | `class` | Non-persistent backend, primarily for tests. |
| `FilePluginConfigStorage` | `class` | JSON-file backend rooted at a host-supplied directory. |
| `Validator` | `Callable[[Any], None]` | Validation callable passed to `register_validator`; raises on an invalid value. |

A `Validator` receives the candidate value and raises any exception to
reject it; `PluginConfig` normalises the rejection into
`PluginConfigurationError`.

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

| Symbol | Type | Description |
|---|---|---|
| `PluginEvent` | `dataclass` | SDK-owned event value type (`name`, `payload`). |
| `PluginEventBus` | `class` | Plugin-scoped publish/subscribe façade. |
| `Subscription` | `class` | Opaque, idempotently disposable subscription handle. |
| `PluginEventHandler` | `Callable[[PluginEvent], None \| Awaitable[None]]` | Handler signature accepted by `subscribe`; may be `async def`. |
| `EventBusPort` | `Protocol` | Narrow, runtime-checkable port listing only the bus methods the SDK calls. The foundation `EventBus` satisfies it structurally, so hosts inject it directly and the SDK never imports `core`. |
| `PermissionCheck` | `Callable[[PluginPermission], None]` | Gate consulted before publish/subscribe; raises `PluginPermissionError` when denied. |

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

| Symbol | Type | Description |
|---|---|---|
| `PluginServices` | `class` | Read-only, typed service façade (`has`, `keys`, `get`, `get_optional`, `snapshot`). |
| `ServicePermissionCheck` | `Callable[[type, PluginPermission], None]` | Gate consulted before each resolution; receives the requested service type together with `PluginPermission.SERVICES` and raises `PluginPermissionError` when denied. |

The host controls the whitelist: only service types it places into the
mapping during context construction are visible, and `snapshot()` returns
type *names* only — never instances.

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
| `extensions` | `PluginExtensions \| None` | Extension-point façade; `None` when the host exposes no registrar. |

Hosts create contexts through `PluginContextBuilder`:

```python
context = (
    PluginContextBuilder(metadata)
    .with_event_bus(event_bus, event_type=Event)
    .with_service(SecretsPort, secrets_service)
    .with_config_storage(FilePluginConfigStorage(config_root))
    .with_resources_root(resources_root)
    .with_extensions(registrar)
    .with_application_version(settings.version)
    .build()
)
```

The builder wires permission enforcement automatically based on the
plugin's declared `PluginPermission` set.

#### Extension points

| Symbol | Type | Description |
|---|---|---|
| `PluginExtensions` | `class` | Plugin-facing façade for registering functionality at host-defined extension points. |
| `ExtensionRegistrar` | `Callable[[str, Any], None]` | Host-supplied registration callable injected through `PluginContextBuilder.with_extensions`. |

The set of extension points is **host-defined**; a plugin addresses a point
by name (for example `"tools"`, `"ui"`, `"commands"`, `"workflows"`):

```python
context.extensions.register("tools", MyTool())
```

Contract:

* Registration is **strictly additive** — it never alters an existing API
  signature or contract.
* `register` raises `PluginSDKError` when the host supplied no registrar,
  `ValueError` for an undefined extension point, and `TypeError` for an
  extension without a usable identifier. The SDK passes the host's
  `ValueError`/`TypeError` through unchanged so plugin authors need no
  framework-internal imports.
* `PluginContext.extensions` is `None` when the host exposes no registrar;
  plugins that use extension points must handle that case.

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

| Track | Constant | Current value | Governs |
|---|---|---|---|
| SDK release | `SDK_VERSION` | `0.9.0` | The SDK package version. Aligned with the JOCHEN X application version (`pyproject.toml` → `project.version`). |
| Plugin API | `SDK_API_VERSION` | `1.0.0` | Backwards-compatibility surface for plugins. |

The two tracks move independently: the SDK release version has advanced to
`0.9.0` while the plugin API contract has remained at `1.0.0` — every change
since the first `1.0.0` API has been additive.

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
| Extension points | `tests/test_host_services_extensions.py` | Registrar injection; undefined point and missing-registrar cases. |
| Documentation currency | `tests/test_documentation_currency.py` | Every `sdk.__all__` symbol is documented; version constants match the prose. |

The SDK never requires a Qt event loop for unit tests, but `UIPlugin` is
verified by consumers who inject their own widget factory.

---

## 14. Definition of Done – v0.9.0

- [x] All plugin base classes are shipped with clearly defined lifecycles.
- [x] Manifest models cover every required field with validation.
- [x] `PluginContext` exposes only SDK-defined façades.
- [x] Event, service, logging, configuration, and resource APIs are all
      exposed exclusively through the SDK.
- [x] Extension points are exposed through `PluginExtensions` and are
      strictly additive.
- [x] SDK exceptions form a shallow, publicly documented hierarchy.
- [x] `docs/sdk.md` documents **every** symbol in `sdk.__all__`.
- [x] The documented version constants match `sdk/version.py`.
- [x] `ADR-010` records the SDK architecture decision.
- [x] Comprehensive unit tests exist for every SDK subsystem.
- [x] No existing foundation module was modified.
- [x] No breaking changes to the existing public surface.

---

## 15. Plugin Author Guidelines (Autorenvorgaben)

> **This chapter is the single authoritative place for all plugin author
> guidelines** (FR-005 / AC-005.1): manifest schema, lifecycle contract, and
> permission model. Other documents (`extensions.md`, `CONTRIBUTING.md`)
> reference this chapter and do not redefine its content. The canonical
> working example is the Golden Reference Plugin
> (`plugins/reference/plugin.toml`, `plugins/reference/__init__.py`).

### 15.1 Manifest Schema (`plugin.toml`, v2)

Every plugin ships a `plugin.toml` in its own directory below the plugin
root. Discovery is manifest-only (PL-01): the foundation never imports
plugin code before validation. Fields as parsed by `plugins.loader`:

| Table / Key | Required | Meaning |
|---|---|---|
| `[plugin] id` | yes | Unique plugin identifier (also the import package name) |
| `[plugin] version` | yes | Plugin semver |
| `[plugin] requires_application` | yes | Minimum compatible application version |
| `[plugin] api_version` | no | SDK API version the plugin was built against (major must match the host's `SDK_API_VERSION`) |
| `[plugin] category` | no | One of the `PluginCategory` values (default `general`) |
| `[plugin] entry_point` | no | Entry module hint |
| `[plugin.metadata]` | no | Free-form string map (`display_name`, `author`, `description`, …) |
| `[plugin.permissions] capabilities` | no | List of declared permissions (see 15.3) |
| `[plugin.dependencies] requires` | no | List of `{ id, version }` dependency entries (`version` as `>=x.y.z`) |

V1 manifests with flat top-level keys remain valid; unknown fields are
ignored for forwards compatibility.

### 15.2 Lifecycle Contract

Plugins derive from `Plugin` (or `BackgroundPlugin`, `UIPlugin`,
`ToolPlugin`, `WorkflowPlugin`) and are driven by `PluginRuntime` through
the ordered lifecycle (`PluginLifecycleState`):

```
unloaded → initialized → started → stopped
                     └──────────→ failed
```

| Hook | Called | Contract |
|---|---|---|
| `metadata()` | always | Returns validated `PluginMetadata`; must be constant |
| `on_initialize()` | once, after context attach (`unloaded` → `initialized`) | One-time setup; no running behaviour |
| `on_start()` | `initialized` → `started` | Begin operation; long-running work only via `BackgroundPlugin.run_background` |
| `on_stop()` | `started` → `stopped` | Release resources; **must be idempotent** |
| `on_shutdown()` | once, after stop | Release resources that outlive normal operation |

Any exception in a hook moves the plugin to `failed` and aborts further
lifecycle progression. Activation by the host occurs exclusively after the
fully successful security pipeline (PL-05).

### 15.3 Permission Model

Permissions are declared in the manifest (`capabilities`) and mirrored as
`PluginPermission` values in `PluginMetadata.permissions`. The host policy
is **default-deny** (ADR-006): a capability that is neither wildcard- nor
plugin-granted is denied, and plugins with denied capabilities are rejected
before activation (PL-03). Declared permissions gate `PluginEventBus`
(`events.publish`, `events.subscribe`) and `PluginServices` (`services`) —
undeclared capabilities are refused at these façades even when the
underlying service exists. `PluginConfig` and `PluginResources` do not
enforce permission checks at runtime. The remaining five permissions
(`network`, `filesystem`, `credentials`, `system_observation`, `ui`) have
no corresponding SDK façade that could serve as an enforcement point.

| `PluginPermission` | Value | Grants |
|---|---|---|
| `NETWORK` | `network` | Outbound network access |
| `FILESYSTEM` | `filesystem` | File-system access beyond the plugin's resource root |
| `CREDENTIALS` | `credentials` | Access to secret storage |
| `SYSTEM_OBSERVATION` | `system_observation` | Read access to system/host diagnostics |
| `UI` | `ui` | Contributing UI widgets |
| `EVENTS_PUBLISH` | `events.publish` | Publishing events on the plugin event bus |
| `EVENTS_SUBSCRIBE` | `events.subscribe` | Subscribing to events on the plugin event bus |
| `CONFIGURATION` | `configuration` | Plugin configuration store access |
| `RESOURCES` | `resources` | Plugin resource root access |
| `SERVICES` | `services` | Resolving host services via `PluginServices` |

Rejections anywhere in the runtime pipeline produce a structured result
carrying the triggering pipeline stage and the violated criterion with its
reference to the invariant pipeline order PL-01..PL-05 (FR-006).
