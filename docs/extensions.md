# Plugin Framework – Specification v0.7.0

The Plugin Framework defines how JOCHEN X discovers, validates, registers, and
exposes plugins without ever importing or executing plugin code at the foundation
level. The framework follows a **manifest-only** design: plugins declare their
metadata in a `plugin.toml` file and the foundation treats them as inert data
throughout their lifecycle.

This document is the authoritative specification for all plugin-related
architecture in JOCHEN X v0.7.0. It consolidates the requirements, architecture,
design, API surface, and testability contracts for the Plugin Framework into a
single source of truth.

> **Plugin author guidelines** (manifest schema, lifecycle contract,
> permission model) are consolidated in a single place:
> [Plugin SDK — §15 Plugin Author Guidelines](sdk.md#15-plugin-author-guidelines-autorenvorgaben).
> This framework specification does not redefine them.

**Cross-references:**

| Document | Relevance |
|---|---|
| [Foundation Architecture](architecture.md) | Bootstrap order, composition root |
| [Core](core.md) | `ServiceRegistry`, `LifecycleManager` |
| [Events](events.md) | `EventBus` delivery semantics |
| [Security](security.md) | Capability-based trust model |
| [Diagnostics](diagnostics.md) | `PluginDiagnostics` port |
| [Developer Platform](developer.md) | Plugin inspection UI |
| [ADR-001](adr/001-core-boundaries.md) | Core boundary rule |
| [ADR-003](adr/003-optional-developer-platform.md) | Developer platform opt-in |
| [ADR-004](adr/004-plugin-security-integration.md) | Security validation timing |
| [ADR-005](adr/005-plugin-integrity-validation.md) | Integrity & signature validation |
| [ADR-006](adr/006-plugin-permission-model.md) | Plugin capability requests |
| [ADR-007](adr/007-plugin-dependency-resolution.md) | Inter-plugin dependencies |
| [ADR-008](adr/008-plugin-context-definition.md) | Plugin runtime context |
| [ADR-009](adr/009-plugin-isolation-strategy.md) | Code execution isolation |

---

## 1. Design Principles

The Plugin Framework is governed by these non-negotiable principles, derived from
the existing JOCHEN X architecture:

| Principle | Application |
|---|---|
| **Plugin-First** | Every feature beyond the foundation is extensible through plugin protocols. |
| **Manifest-Only Discovery** | Plugins are discovered via `plugin.toml` manifests; plugin code is never imported by the foundation. |
| **Inert Extensions** | Extension protocols define contracts; the foundation never instantiates extension implementations. |
| **Zero Trust** | No plugin is admitted without explicit trust validation via `PluginSecurity`. |
| **Least Privilege** | Plugins declare required capabilities; the foundation grants only what is explicitly permitted. |
| **Single Responsibility** | Each framework component has exactly one responsibility (discovery, validation, registry, diagnostics). |
| **Dependency Inversion** | The foundation depends on plugin abstractions (`Protocol`), never on plugin implementations. |
| **Composition over Inheritance** | Plugins compose with the foundation through the `ServiceRegistry`; no class inheritance required. |
| **Event-Driven Communication** | All plugin lifecycle transitions are broadcast on the `EventBus`. |
| **Clean Architecture** | Plugin-related code respects layer boundaries: core → app → plugins. |

---

## 2. Architecture Overview

### 2.1 Layer Responsibility

```
┌─────────────────────────────────────────────────────────┐
│  core/extensions.py          Core Layer (Stable)        │
│  - PluginExtension Protocol                             │
│  - ToolExtension Protocol                               │
│  - UIExtension Protocol                                 │
│  - CommandExtension Protocol                            │
│  - WorkflowExtension Protocol                           │
├─────────────────────────────────────────────────────────┤
│  core/version.py             Core Layer (Stable)        │
│  - Version                                              │
│  - VersionManager                                       │
├─────────────────────────────────────────────────────────┤
│  plugins/loader.py           Plugin Layer (Foundation)  │
│  - PluginManifest                                       │
│  - PluginCatalog                                        │
│  - PluginLoader                                         │
├─────────────────────────────────────────────────────────┤
│  app/bootstrap.py            Application Layer          │
│  - PluginDiscoveryStage                                 │
├─────────────────────────────────────────────────────────┤
│  app/security/plugin_security.py   Application Layer    │
│  - PluginSecurity                                       │
│  - PluginVerdict                                        │
├─────────────────────────────────────────────────────────┤
│  app/events.py               Application Layer          │
│  - PluginLoading                                        │
│  - PluginLoaded                                         │
│  - PluginFailed                                         │
├─────────────────────────────────────────────────────────┤
│  app/security/events.py      Application Layer          │
│  - PluginVerified                                       │
│  - PluginRejected                                       │
├─────────────────────────────────────────────────────────┤
│  app/errors.py               Application Layer          │
│  - PluginError                                          │
├─────────────────────────────────────────────────────────┤
│  app/security/exceptions.py  Application Layer          │
│  - PluginSecurityError                                  │
├─────────────────────────────────────────────────────────┤
│  developer/contracts.py      Developer Layer (Optional) │
│  - PluginDiagnostics Protocol                           │
├─────────────────────────────────────────────────────────┤
│  developer/models.py         Developer Layer (Optional) │
│  - PluginStatus                                         │
└─────────────────────────────────────────────────────────┘
```

### 2.2 Dependency Direction

All dependencies point inward according to Clean Architecture:

```
Developer Layer  →  Application Layer  →  Core Layer
(optional)          (plugin lifecycle)     (stable contracts)
```

- **Core Layer** defines extension protocols and version semantics. It has no
  dependencies on the application or plugin layers.
- **Plugin Layer** (`plugins/`) depends only on the core layer (`core.version`).
- **Application Layer** depends on core and plugin layers for bootstrap
  integration, security validation, and event emission.
- **Developer Layer** depends on contracts satisfied by the plugin layer
  through the `PluginDiagnostics` protocol.

### 2.3 Core Boundary Rule

Per [ADR-001](adr/001-core-boundaries.md), plugins and extensions remain outside
the core startup path. The foundation discovers plugin metadata and registers it
in the `ServiceRegistry`, but it never:

- imports plugin Python modules,
- instantiates plugin classes,
- executes plugin code, or
- adds plugins to the `LifecycleManager`.

This boundary is enforced structurally: `PluginLoader` reads only TOML files and
produces immutable `PluginManifest` value objects.

---

## 3. Components

### 3.1 Plugin Manifest

**Module:** `plugins.loader.PluginManifest`

The manifest is an immutable, frozen dataclass representing the parsed and
validated metadata from a single `plugin.toml` file.

**Fields:**

| Field | Type | Source (`plugin.toml` key) | Description |
|---|---|---|---|
| `identifier` | `str` | `id` | Unique, stable plugin identifier. |
| `version` | `Version` | `version` | Semantic version of the plugin (`major.minor.patch`). |
| `required_application_version` | `Version` | `requires_application` | Minimum compatible application version. |

**Invariants:**

- All fields are required; a manifest with missing fields raises `KeyError`
  during TOML parsing.
- The `identifier` is derived from `str(data["id"])`.
- Both version fields are parsed via `Version.parse()`, which enforces the
  exact `major.minor.patch` format.
- The manifest is a frozen dataclass with `slots=True` for immutability and
  memory efficiency.

**Manifest file schema** (`plugin.toml`):

```toml
id = "com.example.my-plugin"
version = "1.0.0"
requires_application = "0.7.0"
```

All three keys are mandatory. The file must be valid TOML and is parsed with
Python's `tomllib` (standard library, Python 3.11+).

> **OPEN ARCHITECTURE DECISION:** The manifest schema currently supports only
> three fields. Additional fields (description, author, permissions,
> dependencies, entry point, capabilities) are anticipated but not yet
> specified. See [ADR-006](adr/006-plugin-permission-model.md) and
> [ADR-007](adr/007-plugin-dependency-resolution.md).

### 3.2 Plugin Loader (Discovery)

**Module:** `plugins.loader.PluginLoader`

The `PluginLoader` is responsible for filesystem-based manifest discovery. It
scans a configured plugin directory for subdirectories containing a
`plugin.toml` file, parses each manifest, and filters for version compatibility.

**Constructor:**

| Parameter | Type | Description |
|---|---|---|
| `directory` | `Path` | Root plugin directory to scan. |
| `versions` | `VersionManager` | Evaluates application version compatibility. |

**Public API:**

| Method | Signature | Description |
|---|---|---|
| `discover` | `() -> tuple[PluginManifest, ...]` | Reads all compatible `plugin.toml` files from direct subdirectories. |

**Discovery algorithm:**

1. If the plugin directory does not exist, return an empty tuple (no error).
2. Glob for `*/plugin.toml` (one level of subdirectories only).
3. For each found manifest file:
   a. Open and parse the TOML content via `tomllib.load()`.
   b. Construct a `PluginManifest` from the parsed data.
   c. Evaluate version compatibility via `VersionManager.is_compatible()`.
   d. Include the manifest only if the required application version is compatible.
4. Return all compatible manifests as an immutable tuple.

**Version compatibility rule** (from `VersionManager.is_compatible()`):

A plugin is compatible if and only if:
- `required.major == application.major` (same major version), AND
- `required <= application` (the required version does not exceed the application version).

**Thread safety:** The `PluginLoader` holds no mutable state after construction
and is therefore inherently thread-safe.

**Error handling:** If a single manifest file is malformed (invalid TOML, missing
keys, invalid version format), the error propagates from `discover()`. The
caller (`PluginDiscoveryStage`) wraps the entire discovery in a try/except and
degrades gracefully to an empty catalog.

### 3.3 Plugin Catalog (Registry)

**Module:** `plugins.loader.PluginCatalog`

The `PluginCatalog` is the authoritative, immutable snapshot of all plugins
discovered during bootstrap. It is registered in the `ServiceRegistry` and
serves as the single point of truth for "which plugins exist."

**Fields:**

| Field | Type | Description |
|---|---|---|
| `identifiers` | `tuple[str, ...]` | Ordered tuple of discovered plugin identifiers. |

**Properties:**

| Property | Type | Description |
|---|---|---|
| `count` | `int` | Number of discovered compatible plugins. |

**Invariants:**

- The catalog is a frozen dataclass with `slots=True`.
- Once constructed during bootstrap, it cannot be modified.
- The catalog is registered in the `ServiceRegistry` as a singleton.

### 3.4 Plugin Discovery Stage (Bootstrap Integration)

**Module:** `app.bootstrap.PluginDiscoveryStage`

The `PluginDiscoveryStage` is a `BootstrapStage` that runs during the
`LOAD_PLUGINS` phase (phase 2 of 4) of the application bootstrap sequence.

**Bootstrap phase:** `StartupPhase.LOAD_PLUGINS`

**Execution flow:**

1. Resolve dependencies from the `BootstrapContext`:
   - `environment` (for root path)
   - `settings` (for `plugin_directory` configuration)
   - `versions` (for compatibility evaluation)
   - `registry` (for service registration)
   - `events` (for lifecycle event emission)
   - `logger` (for structured diagnostics)
2. Construct a `PluginLoader` with the configured plugin directory.
3. Register the `PluginLoader` in the `ServiceRegistry`.
4. Call `loader.discover()` within a try/except block.
5. **On success:**
   - For each discovered manifest, emit `PluginLoading` then `PluginLoaded` events.
   - Store manifests on the bootstrap context.
   - Register a `PluginCatalog` with all discovered identifiers.
   - Log the count of discovered plugins.
6. **On failure (any exception):**
   - Log the error at ERROR level.
   - Emit a `PluginFailed` event with an empty identifier and the error message.
   - Register an empty `PluginCatalog`.
   - Continue bootstrap with no plugins (graceful degradation).

**Relationship to startup sequence:**

The `StartupSequence` drives the state machine through these transitions:

```
STARTING → INITIALIZING → LOADING_PLUGINS → LOADING_RESOURCES → READY
              Phase 1          Phase 2           Phase 3       Phase 4
```

The `PluginDiscoveryStage` executes during the `LOADING_PLUGINS` transition.
The application lifecycle event `PluginLoading` is emitted before each manifest
is processed, and `PluginLoaded` after successful processing.

**Registered services after execution:**

| Service Key | Instance | Lifetime |
|---|---|---|
| `PluginLoader` | The constructed loader | Singleton |
| `PluginCatalog` | Immutable identifier snapshot | Singleton |

### 3.5 Extension Protocols

**Module:** `core.extensions`

The core layer defines five structural typing protocols that represent the
extension surface of the Plugin Framework. These protocols are the stable
contracts that future plugin implementations will satisfy.

| Protocol | Required Attribute | Description |
|---|---|---|
| `PluginExtension` | `identifier: str` | General-purpose plugin contract. |
| `ToolExtension` | `identifier: str` | Tool integration contract. |
| `UIExtension` | `identifier: str` | User interface extension contract. |
| `CommandExtension` | `identifier: str` | Command palette extension contract. |
| `WorkflowExtension` | `identifier: str` | Workflow automation extension contract. |

**Design rationale:**

- All protocols are defined with `Protocol` from `typing`, enabling structural
  subtyping (duck typing with static analysis support).
- The `identifier` attribute is the only required member, ensuring maximum
  flexibility for future protocol evolution.
- Protocols are defined in the core layer to maintain stability guarantees:
  they may only be extended, never broken.
- Each protocol targets a different extension category, supporting the
  plugin-first architecture where every feature dimension is extensible.

**API stability:** These protocols are part of the public, stable API surface.
New attributes may be added to protocols in future versions, but existing
attributes will not be removed or have their types changed.

### 3.6 Plugin Security

**Module:** `app.security.plugin_security`

The `PluginSecurity` service implements the Zero Trust principle for plugins.
No plugin is admitted unless it has been explicitly approved or verified.

#### 3.6.1 Trust Model

Trust levels are defined in `app.security.models.PluginTrustLevel`:

| Level | Value | Admitted | Description |
|---|---|---|---|
| `UNTRUSTED` | `"untrusted"` | No | Default state for unknown plugins. |
| `VERIFIED` | `"verified"` | Yes | Plugin has passed verification checks. |
| `TRUSTED` | `"trusted"` | Yes | Plugin has been explicitly approved by an operator. |
| `REJECTED` | `"rejected"` | No (raises) | Plugin has been explicitly rejected; cannot be silently readmitted. |

The allowed trust levels that permit admission are:
`frozenset({PluginTrustLevel.VERIFIED, PluginTrustLevel.TRUSTED})`

#### 3.6.2 PluginVerdict

**Module:** `app.security.plugin_security.PluginVerdict`

The verdict is an immutable, frozen dataclass returned by every security
evaluation:

| Field | Type | Description |
|---|---|---|
| `identifier` | `str` | The evaluated plugin's identifier. |
| `version` | `str` | The evaluated plugin's version string. |
| `trust` | `PluginTrustLevel` | The assigned trust level. |
| `allowed` | `bool` | Whether the plugin may be admitted. |

#### 3.6.3 PluginSecurity API

| Method | Signature | Description |
|---|---|---|
| `approve` | `(identifier: str) -> None` | Mark a plugin as fully trusted. |
| `mark_verified` | `(identifier: str) -> None` | Mark a plugin as verified (allowed, pending full trust). |
| `reject` | `(identifier: str, reason: str) -> None` | Mark a plugin as rejected and emit a `PluginRejected` event. |
| `trust_level` | `(identifier: str) -> PluginTrustLevel` | Return the current trust level (default: `UNTRUSTED`). |
| `verify` | `(identifier: str, version: str) -> PluginVerdict` | Evaluate admission and emit verdict events. |
| `verify_manifest` | `(manifest: PluginManifest) -> PluginVerdict` | Convenience method delegating to `verify()`. |

**Invariants:**

- A rejected plugin always raises `PluginSecurityError` on `verify()`.
- An untrusted plugin returns a verdict with `allowed=False` but does not raise.
- Only verified or trusted plugins emit `PluginVerified` events.
- Empty identifiers raise `ValueError` on any trust mutation.
- All trust operations are thread-safe via `RLock`.

**Event integration:**

| Action | Event Emitted | Event Name |
|---|---|---|
| Plugin verified/trusted and admitted | `PluginVerified` | `security.plugin.verified` |
| Plugin explicitly rejected | `PluginRejected` | `security.plugin.rejected` |

> **OPEN ARCHITECTURE DECISION:** The `PluginDiscoveryStage` currently does not
> invoke `PluginSecurity` during bootstrap. The `SecurityBootstrapStage` runs
> in the `FINALIZE` phase, which is after `LOAD_PLUGINS`. This means discovered
> plugins are not security-validated at discovery time. See
> [ADR-004](adr/004-plugin-security-integration.md).

### 3.7 Plugin Diagnostics

**Module:** `developer.contracts.PluginDiagnostics`

The `PluginDiagnostics` protocol is consumed by the optional Developer Platform
(see [Developer Platform](developer.md)) to expose plugin information in
developer tooling.

```python
class PluginDiagnostics(Protocol):
    def discover(self) -> Iterable[object]: ...
```

**Current implementation:** `PluginLoader` structurally satisfies this protocol
because its `discover()` method returns `tuple[PluginManifest, ...]`, which is
`Iterable[object]`.

**Diagnostic model** (`developer.models.PluginStatus`):

| Field | Type | Source | Description |
|---|---|---|---|
| `identifier` | `str` | `PluginManifest.identifier` | Plugin identifier. |
| `version` | `str` | `PluginManifest.version` | Plugin version string. |
| `api_version` | `str` | `PluginManifest.required_application_version` | Required application version. |
| `enabled` | `bool` | Hardcoded `True` | Whether the plugin is active. |
| `signature_status` | `str` | Hardcoded `"unverified"` | Integrity verification status. |
| `permissions` | `tuple[str, ...]` | Hardcoded `()` | Declared plugin permissions. |
| `dependencies` | `tuple[str, ...]` | Hardcoded `()` | Declared plugin dependencies. |

> **Note:** The fields `signature_status`, `permissions`, and `dependencies` are
> structural placeholders for future capabilities. They are not backed by
> manifest data in v0.7.0. See [ADR-005](adr/005-plugin-integrity-validation.md),
> [ADR-006](adr/006-plugin-permission-model.md), and
> [ADR-007](adr/007-plugin-dependency-resolution.md).

---

## 4. Lifecycle

### 4.1 Plugin Lifecycle States

In v0.7.0, a plugin transitions through the following states during the
application bootstrap:

```
                ┌──────────────┐
                │  UNDISCOVERED │
                └──────┬───────┘
                       │  PluginLoader.discover()
                       ▼
                ┌──────────────┐
                │  DISCOVERED  │  PluginLoading event
                └──────┬───────┘
                       │  Version compatibility check passed
                       ▼
                ┌──────────────┐
                │  COMPATIBLE  │  PluginLoaded event
                └──────┬───────┘
                       │  PluginCatalog created
                       ▼
                ┌──────────────┐
                │  REGISTERED  │  Available via ServiceRegistry
                └──────────────┘
```

**Failure path:**

```
                ┌──────────────┐
                │  UNDISCOVERED │
                └──────┬───────┘
                       │  Discovery fails (IOException, parse error)
                       ▼
                ┌──────────────┐
                │    FAILED    │  PluginFailed event, empty catalog
                └──────────────┘
```

### 4.2 Bootstrap Integration

The plugin lifecycle is driven by the `StartupSequence`, which advances the
`ApplicationStateMachine` and delegates to `BootstrapManager.run_phase()`:

| Step | State Machine Transition | Bootstrap Phase | Plugin Activity |
|---|---|---|---|
| 1 | `STARTING → INITIALIZING` | `INITIALIZE` | Infrastructure created (registry, events, versions) |
| 2 | `INITIALIZING → LOADING_PLUGINS` | `LOAD_PLUGINS` | `PluginDiscoveryStage` executes |
| 3 | `LOADING_PLUGINS → LOADING_RESOURCES` | `LOAD_RESOURCES` | No plugin activity |
| 4 | — | `FINALIZE` | Developer tools (if enabled) access `PluginDiagnostics` |
| 5 | `→ READY` | — | Application ready, plugin catalog frozen |

### 4.3 Event Timeline

During a successful bootstrap with discovered plugins, the following events are
emitted in order:

| # | Event | Source | Bus Name |
|---|---|---|---|
| 1 | `ApplicationStarting` | `StartupSequence` | `application.starting` |
| 2 | `ApplicationStarted` | `StartupSequence` | `application.started` |
| 3 | `ApplicationStateChanged` | `ApplicationStateMachine` | `application.state.changed` |
| 4 | `PluginLoading` | `PluginDiscoveryStage` | `application.plugin.loading` |
| 5 | `PluginLoaded` | `PluginDiscoveryStage` | `application.plugin.loaded` |
| 6 | `ApplicationReady` | `StartupSequence` | `application.ready` |

Steps 4–5 repeat for each discovered compatible manifest.

---

## 5. EventBus Integration

All plugin lifecycle events flow over the shared `EventBus` (see
[Events](events.md)). Events are published synchronously via
`EventPublisher.publish()` and carry typed payloads.

### 5.1 Application Lifecycle Events

Defined in `app.events`:

| Event Class | Bus Name | Payload |
|---|---|---|
| `PluginLoading` | `application.plugin.loading` | `{"identifier": str}` |
| `PluginLoaded` | `application.plugin.loaded` | `{"identifier": str, "version": str}` |
| `PluginFailed` | `application.plugin.failed` | `{"identifier": str, "reason": str}` |

### 5.2 Security Events

Defined in `app.security.events`:

| Event Class | Bus Name | Payload |
|---|---|---|
| `PluginVerified` | `security.plugin.verified` | `{"identifier": str, "version": str, "trust": str}` |
| `PluginRejected` | `security.plugin.rejected` | `{"identifier": str, "reason": str}` |

### 5.3 Subscription Patterns

Consumers can subscribe to plugin events using exact names or glob patterns:

```python
bus.subscribe("application.plugin.*", handler)      # All plugin lifecycle events
bus.subscribe("security.plugin.*", handler)          # All plugin security events
bus.subscribe("application.plugin.loaded", handler)  # Specific event
```

All plugin events inherit from `ApplicationEvent` or `SecurityEvent` and convert
to transport-neutral `Event` instances via `.to_event()`, ensuring a single
event system without parallel taxonomies.

---

## 6. Error Handling

### 6.1 Exception Hierarchy

```
JochenXError (core.exceptions)
├── PluginError (app.errors)
│   └── Recoverable plugin discovery or activation failures
└── SecurityError (app.security.exceptions)
    └── PluginSecurityError
        └── Plugin fails security validation or is explicitly rejected
```

### 6.2 Error Classification

The `CentralErrorHandler` classifies plugin errors as follows:

| Exception Type | Category | Severity | Fatal |
|---|---|---|---|
| `PluginError` | `PLUGIN` | `RECOVERABLE` | No |
| `PluginSecurityError` | `RECOVERABLE` | `RECOVERABLE` | No |

Plugin errors are never fatal. Discovery failures result in graceful degradation
to an empty `PluginCatalog`, and the application continues to operate without
plugins.

### 6.3 Recovery Strategy

- **Discovery failure:** The `PluginDiscoveryStage` catches all exceptions from
  `discover()`, logs the error, emits a `PluginFailed` event, and registers an
  empty `PluginCatalog`. The bootstrap continues normally.
- **Security rejection:** `PluginSecurity.verify()` raises `PluginSecurityError`
  for rejected plugins. This is a normal control flow path, not a crash.
- **Malformed manifest:** Individual malformed manifests cause `discover()` to
  fail. This is a known limitation; see the note below.

> **Note:** In v0.7.0, a single malformed manifest file causes the entire
> discovery to fail because exceptions from TOML parsing or `Version.parse()`
> propagate uncaught from the loop in `PluginLoader.discover()`. This means one
> invalid `plugin.toml` prevents all plugins from loading. This is documented
> behavior in the current implementation, not a bug. Future versions may
> implement per-manifest error isolation.

---

## 7. Dependency Injection

### 7.1 Service Registration

The Plugin Framework registers two services during bootstrap:

| Service Key | Provider | Lifetime | Registered By |
|---|---|---|---|
| `PluginLoader` | Instance | Singleton | `PluginDiscoveryStage` |
| `PluginCatalog` | Instance | Singleton | `PluginDiscoveryStage` |

The `PluginSecurity` service is registered separately by the
`SecurityBootstrapStage` as part of the `SecurityManager` composition:

| Service Key | Provider | Lifetime | Registered By |
|---|---|---|---|
| `PluginSecurity` | Instance | Singleton | `SecurityBootstrapStage` |

### 7.2 ApplicationContext Integration

The `ApplicationContext` exposes the `PluginLoader` via its `plugins` field:

```python
@dataclass(frozen=True, slots=True)
class ApplicationContext:
    plugins: PluginLoader
```

This provides callers with the ability to re-run discovery if needed, though the
canonical plugin list is the `PluginCatalog` registered in the `ServiceRegistry`.

### 7.3 Configuration

Plugin-related configuration is part of `ApplicationSettings`:

| Setting | Type | Source (`default.toml`) | Description |
|---|---|---|---|
| `plugin_directory` | `str` | `[plugins] directory` | Relative path to the plugin scan directory. |

Default configuration:

```toml
[plugins]
directory = "plugins"
```

---

## 8. Thread Safety

| Component | Mechanism | Guarantee |
|---|---|---|
| `PluginManifest` | Frozen dataclass | Immutable; inherently thread-safe. |
| `PluginCatalog` | Frozen dataclass | Immutable; inherently thread-safe. |
| `PluginLoader` | No mutable state | Stateless after construction; thread-safe. |
| `PluginSecurity` | `RLock` | All trust mutations and reads are serialized. |
| `PluginVerdict` | Frozen dataclass | Immutable; inherently thread-safe. |
| `EventBus` | `RLock` | All subscription and publishing operations are serialized. |
| `ServiceRegistry` | `RLock` | All registration and resolution operations are serialized. |

---

## 9. Versioning and Compatibility

### 9.1 Application Version Compatibility

The `VersionManager` implements major-version compatibility:

```python
def is_compatible(self, required: Version) -> bool:
    return required.major == self.application_version.major \
        and required <= self.application_version
```

**Rules:**
- A plugin targeting major version `N` is only compatible with application
  major version `N`.
- The required version must not exceed the current application version
  (forward compatibility is not supported).
- Minor and patch version differences within the same major are permitted.

**Examples:**

| App Version | Required | Compatible | Reason |
|---|---|---|---|
| `0.7.0` | `0.7.0` | Yes | Exact match |
| `0.7.0` | `0.6.0` | Yes | Same major, lower minor |
| `0.7.0` | `0.8.0` | No | Same major, but exceeds app version |
| `0.7.0` | `1.0.0` | No | Different major version |

### 9.2 Semantic Versioning

`Version` follows strict semantic versioning with `major.minor.patch` format:

- **major:** Breaking changes to the plugin API surface.
- **minor:** Backwards-compatible additions.
- **patch:** Backwards-compatible bug fixes.

Pre-release and build metadata identifiers are not supported.

### 9.3 API Stability Guarantees

| API Surface | Stability | Rule |
|---|---|---|
| Extension protocols (`core.extensions`) | **Stable** | May be extended, never broken. |
| `PluginManifest` fields | **Stable** | New fields may be added; existing fields are permanent. |
| `PluginCatalog` fields | **Stable** | New fields may be added; existing fields are permanent. |
| Plugin lifecycle events | **Stable** | New events may be added; existing event names are permanent. |
| `PluginSecurity` API | **Stable** | New methods may be added; existing signatures are permanent. |
| `PluginDiagnostics` protocol | **Provisional** | May change in coordination with the Developer Platform. |
| `PluginStatus` model | **Provisional** | Fields may change as manifest schema evolves. |

---

## 10. Diagnostics, Monitoring, and Health

### 10.1 Plugin Diagnostics Port

The `PluginDiagnostics` protocol (see [Diagnostics](diagnostics.md)) is consumed
by the optional Developer Platform when `developer_enabled = true`:

```python
class PluginDiagnostics(Protocol):
    def discover(self) -> Iterable[object]: ...
```

`PluginLoader` structurally satisfies this protocol. The Developer Platform
calls `discover()` and maps each result to a `PluginStatus` for UI presentation.

### 10.2 Structured Logging

All plugin operations emit structured log entries using the `extra={"context": ...}`
pattern:

| Logger Name | Log Event | Level | Context |
|---|---|---|---|
| `jochen_x` | `plugins.discovered` | INFO | `{"count": int}` |
| `jochen_x` | `plugins.discovery_failed` | ERROR | (exception info) |
| `jochen_x.security.plugins` | `plugin.approved` | INFO | `{"identifier": str}` |
| `jochen_x.security.plugins` | `plugin.marked_verified` | INFO | `{"identifier": str}` |
| `jochen_x.security.plugins` | `plugin.rejected` | WARNING | `{"identifier": str, "reason": str}` |

### 10.3 Health Integration

Plugin health is surfaced through the `ApplicationHost.health()` method, which
returns `HealthStatus` tuples for key subsystems. Plugin count is displayed in
the UI status bar via the `StatusBar` widget (`"Plugins: N discovered"`).

The `PluginCatalog.count` property provides the canonical plugin count without
requiring re-discovery.

---

## 11. Testability

### 11.1 Test Strategy

Every Plugin Framework component is independently testable without a Qt event
loop, database, or filesystem (except for `PluginLoader`, which requires a
temporary directory).

| Component | Test Location | Strategy |
|---|---|---|
| `PluginLoader` | `tests/test_foundation.py` | Temporary directory with synthetic `plugin.toml` |
| `PluginManifest` | `tests/test_foundation.py` | Constructed from known TOML data |
| `PluginCatalog` | `tests/test_navigation.py` | Verified via `ServiceRegistry` after bootstrap |
| Extension protocols | `tests/test_core.py` | Protocol `_is_protocol` flag verification |
| `PluginSecurity` | `tests/test_security_foundation.py` | Unit tests for trust lifecycle |
| `PluginError` | `tests/test_application_foundation.py` | Error classification verification |
| `PluginDiscoveryStage` | `tests/test_application_foundation.py` | Full bootstrap integration test |
| Plugin events | `tests/test_application_foundation.py` | Event capture and payload verification |

### 11.2 Test Isolation

- `PluginLoader` tests use `tempfile.TemporaryDirectory` with synthetic
  manifests, avoiding any dependency on the real plugin directory.
- `PluginSecurity` tests use an in-memory `EventBus` and verify events via
  capture lists.
- Bootstrap integration tests create a throwaway project root with minimal
  configuration.

---

## 12. Extensibility

### 12.1 Bootstrap Extension

The `BootstrapManager` accepts custom stages through its `stages` parameter.
New plugin-related stages can be added without modifying existing files:

```python
BootstrapManager(stages=(*default_stages(), CustomPluginStage()))
```

This is the pattern used by `SecurityBootstrapStage` and the desktop navigation
framework's `DesktopBootstrapStage`.

### 12.2 Event Extension

New plugin event types can be added by subclassing `ApplicationEvent` or
`SecurityEvent` and defining a stable `EVENT_NAME`. The `EventBus` glob-pattern
subscriptions (`application.plugin.*`) automatically capture new events in the
same namespace.

### 12.3 Protocol Extension

New extension protocols can be added to `core/extensions.py` alongside the
existing five protocols. Existing protocols may be extended with new optional
attributes (methods with defaults or properties).

---

## 13. Open Architecture Decisions

The following decisions are explicitly deferred and require ADRs before
implementation:

| ADR | Topic | Impact |
|---|---|---|
| [ADR-004](adr/004-plugin-security-integration.md) | When does `PluginSecurity` validate discovered manifests? | Bootstrap phase ordering, trust enforcement timing |
| [ADR-005](adr/005-plugin-integrity-validation.md) | How are plugins verified for integrity (signatures, hashes)? | `PluginStatus.signature_status`, trust pipeline |
| [ADR-006](adr/006-plugin-permission-model.md) | What capabilities can a plugin request and how are they enforced? | Manifest schema, `PluginStatus.permissions` |
| [ADR-007](adr/007-plugin-dependency-resolution.md) | How are inter-plugin dependencies declared and resolved? | Manifest schema, load ordering, `PluginStatus.dependencies` |
| [ADR-008](adr/008-plugin-context-definition.md) | What services and APIs are exposed to loaded plugin code? | Plugin SDK, sandboxing boundary |
| [ADR-009](adr/009-plugin-isolation-strategy.md) | How is plugin code isolated during execution? | Process model, resource limits, fault containment |

---

## 14. Definition of Done – v0.7.0

Version 0.7.0 of the Plugin Framework is considered complete when:

- [x] All components are implemented and documented.
- [x] All extension protocols are defined and stable.
- [x] The manifest schema is specified.
- [x] The discovery algorithm is documented.
- [x] The bootstrap integration is documented.
- [x] All lifecycle states and transitions are defined.
- [x] All events and their payloads are documented.
- [x] The security trust model is fully specified.
- [x] Error handling and recovery strategies are documented.
- [x] Thread safety guarantees are documented for every component.
- [x] Versioning and compatibility rules are documented.
- [x] Dependency injection registrations are documented.
- [x] Diagnostics and monitoring integration is documented.
- [x] Testability strategy and test locations are documented.
- [x] Extensibility points are documented.
- [x] All cross-references to related documents are provided.
- [x] All open architecture decisions are identified and tracked as ADRs.
- [x] No undocumented architectural assumptions exist.
