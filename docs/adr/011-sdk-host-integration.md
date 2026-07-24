# ADR 011: SDK-Host-Integration

**Status:** Accepted (v0.8.0)

## Context

The Plugin SDK (v0.7.1, [ADR-010](010-plugin-sdk-architecture.md)) ships a
complete, independently-testable programming surface for plugin authors. It
defines plugin base classes, lifecycle states, a context builder, and
facade APIs for events, services, configuration, resources, and logging.

However, no host-side code references the SDK today. The gap:

| What exists | What is missing |
|---|---|
| `PluginLoader` discovers `PluginManifest` (3-field TOML value type) | No stage imports or instantiates plugin classes |
| `PluginCatalog` holds identifiers of compatible manifests | No mapping from catalog entries to `PluginRuntime` instances |
| `PluginSecurity` can verify manifests | Verification is not called during bootstrap ([ADR-004](004-plugin-security-integration.md) still open) |
| `PluginContextBuilder` can produce a wired `PluginContext` | No bootstrap code invokes the builder |
| `PluginRuntime` drives plugin lifecycle | No host code creates a runtime |
| `core.extensions` defines inert protocols | No connection to SDK plugin base classes |

Two manifest representations coexist:

1. **`plugins.loader.PluginManifest`** — 3-field frozen dataclass
   (`identifier`, `version`, `required_application_version`). Produced by
   TOML-only discovery. Lives in the plugin layer, depends only on
   `core.version`. This is the ADR-001 manifest-only discovery contract.

2. **`sdk.manifest.PluginMetadata`** — 11-field enterprise model with full
   validation, categories, permissions, dependencies, and signature status.
   Lives in the SDK, depends only on `sdk.errors`. This is the plugin
   author's self-description returned by `Plugin.metadata()`.

The question this ADR resolves: how does the host connect manifest
discovery to SDK-driven plugin activation?

---

## Decision

### D1: Adapter, not replacement

`plugins.loader.PluginManifest` remains the output of manifest-only
discovery. `sdk.manifest.PluginMetadata` remains the plugin author's
self-description. The two are connected by the existing adapter
`PluginMetadata.from_loader_manifest()`, which reads only the three
public attributes from `PluginManifest` and combines them with the
additional fields that plugin code supplies.

**Rationale:**

* **Dependency direction preserved.** `PluginLoader` depends on
  `core.version`, not on `sdk`. The SDK depends on nothing outside
  itself. Replacing `PluginManifest` with `PluginMetadata` would invert
  the dependency: the plugin layer would import the SDK, violating
  [ADR-001](001-core-boundaries.md).
* **Separation of concerns.** Discovery answers "which compatible plugins
  exist?" (3 fields, TOML). Activation answers "what does the plugin
  need?" (11 fields, code). These are different questions at different
  lifecycle moments.
* **No TOML schema inflation.** Plugin authors should not have to
  duplicate their metadata between `plugin.toml` and `Plugin.metadata()`.
  The TOML file stays minimal (identity + compatibility); the SDK
  metadata is authoritative for everything else.

### D2: Two-phase plugin lifecycle in bootstrap

Plugin activation is split into two new bootstrap stages that slot into
the existing phase model without modifying any existing stage:

```
Phase               Stage                        Responsibility
─────────────────────────────────────────────────────────────────────
LOAD_PLUGINS        PluginDiscoveryStage         (existing) Manifest-only discovery
LOAD_PLUGINS        PluginSecurityStage      [NEW] Verify each manifest via PluginSecurity
LOAD_RESOURCES      ResourceStage                (existing)
FINALIZE            PluginActivationStage    [NEW] Import, instantiate, wire, start plugins
FINALIZE            DeveloperToolsStage          (existing)
FINALIZE            DependencyInjectionStage     (existing)
```

This resolves [ADR-004](004-plugin-security-integration.md) (Option A
variant): `PluginSecurity` is constructed early, during `LOAD_PLUGINS`,
so that security validation happens immediately after discovery. Only
admitted plugins proceed to activation.

This resolves [ADR-009](009-plugin-isolation-strategy.md) (Option C):
plugins run in dedicated threads within the main process. The SDK's
`PluginRuntime` already enforces lifecycle ordering, `BackgroundPlugin`
spawns daemon threads, and the `PluginContext` restricts accessible APIs
by permission. Subprocess isolation (Option B) is deferred as a future
opt-in for untrusted plugins; in-process isolation is the default.

### D3: PluginSecurityStage contract

`PluginSecurityStage` runs in `LOAD_PLUGINS`, after `PluginDiscoveryStage`:

1. Constructs `PluginSecurity` with the event bus (available since
   `RegistryStage`).
2. Iterates over discovered manifests in `context.manifests`.
3. Calls `PluginSecurity.verify_manifest(manifest)` for each.
4. Partitions into admitted and rejected manifests.
5. Stores admitted manifests on the bootstrap context.
6. Emits `PluginRejected` events for rejected manifests.
7. Registers the filtered `PluginCatalog` (replaces the unfiltered one
   from `PluginDiscoveryStage`).

The stage never imports plugin code. It only evaluates trust.

### D4: PluginActivationStage contract

`PluginActivationStage` runs in `FINALIZE`, before `DeveloperToolsStage`:

1. Reads the admitted manifests from the bootstrap context.
2. For each admitted manifest, resolves the plugin's entry point
   (module path derived from plugin directory + manifest identifier).
3. Imports the plugin module and locates the `Plugin` subclass.
4. Instantiates the plugin.
5. Calls `Plugin.metadata()` to obtain the authoritative
   `PluginMetadata`.
6. Validates API version compatibility:
   `PluginMetadata.api_version` major must match `SDK_API_VERSION` major.
7. Resolves declared dependencies against the set of admitted plugins.
8. Builds a `PluginContext` via `PluginContextBuilder`:
   - Event bus: the foundation's `EventBus` (satisfies `EventBusPort`).
   - Event type: `core.events.Event`.
   - Services: host-controlled whitelist (initially: logger).
   - Config storage: `FilePluginConfigStorage` rooted at
     `<plugin_dir>/<identifier>/config.json`.
   - Resources root: `<plugin_dir>/<identifier>/resources/`.
   - Application version: from `ApplicationSettings.version`.
9. Creates a `PluginRuntime(plugin, on_state_change=...)`.
10. Calls `runtime.initialize(context)` then `runtime.start()`.
11. Registers the running `PluginRuntime` in the `ServiceRegistry`
    under a namespaced key.
12. On any failure, emits `PluginFailed`, logs the error, and continues
    with the next plugin. One plugin's failure must never abort the
    application.

### D5: Shutdown integration

`ApplicationHost.shutdown()` iterates over registered `PluginRuntime`
instances in reverse activation order and calls `runtime.shutdown()` for
each. This is idempotent (already guaranteed by `PluginRuntime`).

### D6: `core.extensions` protocols remain inert

The protocols in `core.extensions` (`PluginExtension`, `ToolExtension`,
`UIExtension`, `CommandExtension`, `WorkflowExtension`) remain as they
are. They are not replaced by SDK base classes. Their purpose is
different: they are structural contracts for the foundation's type
system. SDK base classes are implementation contracts for plugin authors.
A future version may verify that an activated plugin satisfies the
matching extension protocol, but this is not required for v0.8.0.

### D7: New bootstrap context fields

`BootstrapContext` gains two new optional fields:

```python
admitted_manifests: tuple[PluginManifest, ...] = ()
plugin_runtimes: tuple[PluginRuntime, ...] = ()
```

### D8: New application events

Two new events extend `ApplicationEventName`:

| Event | Emitted when |
|---|---|
| `PLUGIN_ACTIVATING` | Before a plugin is imported and instantiated |
| `PLUGIN_ACTIVATED` | After a plugin has been started successfully |

These complement the existing `PLUGIN_LOADING`, `PLUGIN_LOADED`, and
`PLUGIN_FAILED` events.

### D9: Version alignment

The activation implementation ships as v0.8.0 (`pyproject.toml` and
`SDK_VERSION`). The SDK API version stays at 1.0.0 — no plugin-facing
API changes are introduced.

---

## Complete Plugin Lifecycle

```
                     ┌─────────────────────────────────────────────┐
                     │              BOOTSTRAP                      │
                     ├─────────────────────────────────────────────┤
                     │                                             │
  plugin.toml ──────►│  1. PluginDiscoveryStage (LOAD_PLUGINS)    │
                     │     → PluginManifest (3 fields)             │
                     │     → PluginCatalog (identifiers only)      │
                     │     → events: PLUGIN_LOADING, PLUGIN_LOADED │
                     │                                             │
                     │  2. PluginSecurityStage (LOAD_PLUGINS)      │
                     │     → PluginSecurity.verify_manifest()      │
                     │     → admitted vs rejected partition         │
                     │     → events: PluginVerified/PluginRejected │
                     │                                             │
                     ├─────────────────────────────────────────────┤
                     │                                             │
                     │  3. PluginActivationStage (FINALIZE)        │
                     │     → import plugin module                  │
                     │     → instantiate Plugin subclass            │
                     │     → Plugin.metadata() → PluginMetadata    │
                     │     → API version check                     │
                     │     → dependency resolution                 │
                     │     → PluginContextBuilder.build()          │
                     │     → PluginRuntime.initialize(context)     │
                     │     → PluginRuntime.start()                 │
                     │     → events: PLUGIN_ACTIVATING,            │
                     │                PLUGIN_ACTIVATED              │
                     │                                             │
                     └─────────────────────────────────────────────┘

                     ┌─────────────────────────────────────────────┐
                     │              RUNTIME                         │
                     ├─────────────────────────────────────────────┤
                     │                                             │
                     │  Plugin is STARTED                          │
                     │  ├── context.events → PluginEventBus        │
                     │  ├── context.services → PluginServices      │
                     │  ├── context.config → PluginConfig           │
                     │  ├── context.resources → PluginResources    │
                     │  ├── context.logger → PluginLogger          │
                     │  └── BackgroundPlugin: daemon thread active  │
                     │                                             │
                     └─────────────────────────────────────────────┘

                     ┌─────────────────────────────────────────────┐
                     │              SHUTDOWN                        │
                     ├─────────────────────────────────────────────┤
                     │                                             │
                     │  ApplicationHost.shutdown()                 │
                     │  → PluginRuntime.shutdown() (reverse order) │
                     │    → Plugin.on_stop()                       │
                     │    → Plugin.on_shutdown()                   │
                     │    → PluginEventBus.dispose()               │
                     │                                             │
                     └─────────────────────────────────────────────┘
```

---

## Consequences

### Positive

* **The SDK becomes operational.** Plugins are discovered, verified,
  imported, wired, started, and stopped through a single, tested
  pipeline.
* **ADR-004 and ADR-009 are resolved.** Security validation runs before
  activation; in-process thread isolation is the default strategy.
* **No existing stage is modified.** `PluginDiscoveryStage` continues to
  produce `PluginManifest` and `PluginCatalog`. The two new stages are
  additive.
* **Graceful degradation.** A failing plugin is logged and skipped; the
  application starts normally with the remaining plugins.
* **Clean dependency direction.** The activation stage imports from `sdk`
  (which is a leaf package). No foundation module gains a dependency on
  the SDK except the two new stages — both live in `app/bootstrap.py`,
  the application layer, where SDK imports are architecturally permitted.

### Negative / Trade-offs

* **First plugin import happens at `FINALIZE`.** Discovery is still
  inert (TOML-only), but activation now runs Python code. This is the
  explicit intent of the plugin system, but it introduces a new failure
  surface during bootstrap.
* **Thread isolation is not process isolation.** A misbehaving plugin can
  corrupt shared process state. This is mitigated by the SDK's
  permission model and the `PluginContext` facade, but it is not a hard
  boundary. [ADR-009](009-plugin-isolation-strategy.md) Option B
  (subprocess) remains available as a future escalation.
* **Dependency resolution is greedy.** All admitted plugins are loaded
  simultaneously; lazy loading is not supported in v0.8.0. This is
  acceptable because the manifest-only discovery already filters to
  compatible plugins only, and the expected plugin count for a local
  desktop assistant is single-digit.

### Risks

| Risk | Mitigation |
|---|---|
| Plugin import raises at startup | Catch per-plugin, emit `PluginFailed`, continue |
| Plugin.metadata() returns incompatible API version | Reject before context building, emit `PluginFailed` |
| Circular plugin dependencies | Dependency graph is validated before activation; cycles are rejected |
| Plugin corrupts EventBus state | PluginEventBus facade restricts access; publish errors are caught |
| Slow plugin blocks startup | BackgroundPlugin.on_start() spawns a thread; startup is not blocked |

---

## Non-goals for v0.8.0

* Hot-reloading plugins at runtime (requires unloading semantics).
* Plugin marketplace or remote installation.
* Subprocess isolation (deferred; see ADR-009).
* UI plugin widget hosting (requires layout manager integration,
  tracked separately).
* Service exposure beyond the initial whitelist (expanded per
  documented plugin need).

---

## Implementation Order

1. **`PluginSecurityStage`** — construct `PluginSecurity` early, verify
   manifests, partition into admitted/rejected, update `PluginCatalog`.
   Resolves ADR-004.
2. **`PluginActivationStage`** — import, instantiate, wire, start.
   Resolves ADR-009.
3. **Shutdown integration** — reverse-order `runtime.shutdown()` in
   `ApplicationHost`.
4. **New application events** — `PLUGIN_ACTIVATING`, `PLUGIN_ACTIVATED`.
5. **Bootstrap context fields** — `admitted_manifests`, `plugin_runtimes`.
6. **Tests** — unit tests for both stages, integration test for the
   full discovery → security → activation → shutdown pipeline.
7. **Version bump** — `pyproject.toml` and `sdk/version.py` to 0.8.0.

---

## Cross-references

* [Plugin SDK](../sdk.md) — SDK specification.
* [Plugin Framework](../extensions.md) — Manifest-only discovery contract.
* [Foundation Architecture](../architecture.md) — Bootstrap phase model.
* [Security](../security.md) — Trust model and capability grants.
* [ADR-001](001-core-boundaries.md) — Core boundary rule (preserved).
* [ADR-004](004-plugin-security-integration.md) — Security timing (resolved by D3).
* [ADR-008](008-plugin-context-definition.md) — Plugin context (resolved by ADR-010 + this ADR).
* [ADR-009](009-plugin-isolation-strategy.md) — Isolation strategy (resolved by D2, Option C).
* [ADR-010](010-plugin-sdk-architecture.md) — SDK architecture (prerequisite).
