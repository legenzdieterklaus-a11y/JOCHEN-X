# Foundation Architecture

`ApplicationHost` owns the lifecycle. During bootstrap it constructs infrastructure in a
deterministic phase order managed by `BootstrapManager`:

| Phase | Stage | Responsibility |
|---|---|---|
| `INITIALIZE` | `EnvironmentStage` | Runtime paths, OS facts |
| `INITIALIZE` | `ConfigurationStage` | TOML configuration loading and validation |
| `INITIALIZE` | `LoggingStage` | Rotating file logger |
| `INITIALIZE` | `DatabaseStage` | SQLite connection and schema migration |
| `INITIALIZE` | `RegistryStage` | `ServiceRegistry` creation, core service registration |
| `INITIALIZE` | `ThemeStage` | `ThemeEngine` registration |
| `INITIALIZE` | `SchedulerStage` | `TaskScheduler` registration |
| `LOAD_PLUGINS` | `PluginDiscoveryStage` | Manifest-only plugin discovery (see [Plugin Framework](extensions.md)) |
| `LOAD_PLUGINS` | `PluginSecurityStage` | Trust verification of discovered manifests (see [ADR-011](adr/011-sdk-host-integration.md)) |
| `LOAD_RESOURCES` | `ResourceStage` | `ResourceManager` registration |
| `FINALIZE` | `PluginActivationStage` | SDK-driven plugin import, wiring, and start (see [ADR-011](adr/011-sdk-host-integration.md)) |
| `FINALIZE` | `DeveloperToolsStage` | Optional developer platform (see [Developer Platform](developer.md)) |
| `FINALIZE` | `DependencyInjectionStage` | `ServiceProvider` facade, container validation |

The `ServiceRegistry` is the only composition mechanism and is passed explicitly
to consumers. The SQLite database contains only `schema_version` and `settings`.
Configuration is validated before it reaches runtime services.

Plugin code is discovered as metadata via `PluginLoader`, which reads only
`plugin.toml` files; neither `PluginDiscoveryStage` nor `PluginSecurityStage`
imports or executes plugin code. Import, instantiation, and start happen
exclusively in `PluginActivationStage` (`FINALIZE`) and only for manifests
admitted by the preceding pipeline stages (see [Plugin Framework](extensions.md)
§2.3 and [ADR-001](adr/001-core-boundaries.md)).

## Runtime Pipeline

Plugin admission runs through an invariant stage order. `PipelineStage` names
the stages, `PIPELINE_ORDER` fixes their order, and `PIPELINE_STAGE_REFERENCES`
maps each stage to its `PL-01`..`PL-05` reference.

| `PipelineStage` | Reference | Criterion | Executed by |
|---|---|---|---|
| `DISCOVERY` | `PL-01` | Application-version compatibility (manifest-only) | `PluginDiscoveryStage` |
| `INTEGRITY` | `PL-02` | Integrity validation ([ADR-005](adr/005-plugin-integrity-validation.md)) | `PluginSecurityStage` |
| `API_VERSION_GATE` | `PL-02..PL-03` | SDK API compatibility, checked **before** any code import | `PluginSecurityStage` |
| `PERMISSION` | `PL-03` | Permission authorization, default-deny ([ADR-006](adr/006-plugin-permission-model.md)) | `PluginSecurityStage` |
| `DEPENDENCY_RESOLUTION` | `PL-04` | Graph, version constraints, cycles ([ADR-007](adr/007-plugin-dependency-resolution.md)) | `PluginSecurityStage` |
| `ACTIVATION` | `PL-05` | Import, wiring, start | `PluginActivationStage` |

A rejection at any stage is recorded as a structured `PipelineRejection`
(`identifier`, `stage`, `criterion`, `pipeline_reference`, `rejection_code`,
`reason`), not merely logged. `ValidationDiagnostic` carries the result of the
consolidated pre-import validation.

## Retrievable Diagnostics and Observability

`PluginActivationStage` publishes three registry entries that outlive the
mutable `BootstrapContext`:

| Registry key | Content |
|---|---|
| `PluginDiagnosticsReport` | Consolidated `PluginDiagnostic` entries for every stage, each with plugin identifier, stage, pipeline reference and outcome (`activated` / `rejected` / `failed`); queryable via `for_plugin()`, `for_stage()`, `with_outcome()`, `counts()` |
| `ActivationFailurePool` | `ActivationFailure` records of failed activations |
| `PluginRuntimePool` | Activated `PluginRuntime` instances in activation order |

It also publishes the two observability registration points:

| Registry key | Role |
|---|---|
| `HealthCheckRegistry` | One `PluginHealthCheck` per plugin, reading the **live** lifecycle state; `run()` evaluates them through `run_health_checks()` |
| `MetricsRegistry` | Additive registration point for `MetricSource` implementations; values are namespaced `"<source>.<metric>"` and `merge()` never mutates or overrides an existing `Metrics` instance |

A failing activation is isolated: the remaining plugins still activate and the
failure stays documented. See [Diagnostics](diagnostics.md),
[Health](health.md) and [Performance](performance.md).

**Cross-references:** [Core](core.md) · [Events](events.md) ·
[Security](security.md) · [Services](services.md) ·
[Plugin Framework](extensions.md) · [Plugin SDK](sdk.md) ·
[Diagnostics](diagnostics.md) · [Health](health.md) ·
[Performance](performance.md) · [Developer Platform](developer.md) ·
[ADR-011](adr/011-sdk-host-integration.md)

## Architecture Reference and Change Control

The binding architecture reference is
[Architecture Book v2.0](architecture-book-v2.md) — **APPROVED / FROZEN**. This
document describes the *implemented* state and is updated as the code evolves;
the Architecture Book is not. Any deviation in substance requires a new book
version plus a documented ADR in [`docs/adr/`](adr/) — changing the frozen book
itself is a baseline deviation.
