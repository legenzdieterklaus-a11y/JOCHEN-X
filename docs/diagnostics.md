# Diagnostics API

Developer modules depend on `EventDiagnostics`, `ServiceDiagnostics`,
`PluginDiagnostics`, `HealthDiagnostics`, and `PluginRuntimeDiagnostics` ports.
Core components expose safe diagnostic snapshots (`EventDelivery` and
`ServiceDescriptor`) rather than registrations, handlers, or event payloads.

## Diagnostic Ports

| Port | Module | Satisfied By | Returns |
|---|---|---|---|
| `EventDiagnostics` | `developer.contracts` | `EventBus` | `tuple[EventDelivery, ...]` |
| `ServiceDiagnostics` | `developer.contracts` | `ServiceRegistry` | `tuple[ServiceDescriptor, ...]` |
| `PluginDiagnostics` | `developer.contracts` | `PluginLoader` | `Iterable[object]` (yields `PluginManifest`) |
| `PluginRuntimeDiagnostics` | `developer.contracts` | `PluginDiagnosticsReport` | `Iterable[PluginDiagnostic]` |

## Plugin Runtime Diagnostics

`PluginDiagnostic` (`core/observability.py`) is the structured diagnostic of a
single plugin at a single pipeline stage:

| Field | Meaning |
|---|---|
| `plugin_id` | The plugin the diagnostic belongs to. |
| `stage` | The affected pipeline stage, as its `PipelineStage` value. |
| `outcome` | `DiagnosticOutcome`: `activated`, `rejected`, or `failed`. |
| `reason` | Human-readable explanation. |
| `pipeline_reference` | The stage's `PL-01`..`PL-05` reference. |
| `code` | Machine-readable `RejectionCode` value, when one applies. |
| `context` | Read-only detail mapping (violated criterion, error type, phase). |

`PluginDiagnosticsReport` consolidates the entries of a whole pipeline run and
is published in the `ServiceRegistry` by `PluginActivationStage`, so the
diagnostics remain retrievable after the mutable `BootstrapContext` is gone —
they are **not** log-only. Query methods: `diagnostics()`, `plugin_ids()`,
`for_plugin()`, `for_stage()`, `with_outcome()`, `counts()`.

The report is read-only with respect to the plugin runtime: it records what the
pipeline already decided and never influences admission or activation.
`ActivationFailure` records of failed activations stay separately available
through `ActivationFailurePool`.

| `HealthDiagnostics` | `developer.contracts` | `ApplicationHost` | `Iterable[HealthStatus]` |

## Plugin Diagnostics

The `PluginDiagnostics` port is structurally satisfied by `PluginLoader`, which
implements `discover() -> Iterable[object]`. The `DeveloperPlatform` maps each
discovered `PluginManifest` to a `PluginStatus` value object for presentation.

`PluginStatus` fields `signature_status`, `permissions`, and `dependencies` are
structural placeholders for future manifest schema extensions and are currently
hardcoded to `"unverified"`, `()`, and `()` respectively.

See [Plugin Framework](extensions.md) §3.7 and §10.1 for details.

**Cross-references:** [Plugin Framework](extensions.md) ·
[Developer Platform](developer.md) ·
[ADR-003](adr/003-optional-developer-platform.md)
