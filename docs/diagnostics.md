# Diagnostics API

Developer modules depend on `EventDiagnostics`, `ServiceDiagnostics`,
`PluginDiagnostics`, and `HealthDiagnostics` ports. Core components expose safe
diagnostic snapshots (`EventDelivery` and `ServiceDescriptor`) rather than
registrations, handlers, or event payloads.

## Diagnostic Ports

| Port | Module | Satisfied By | Returns |
|---|---|---|---|
| `EventDiagnostics` | `developer.contracts` | `EventBus` | `tuple[EventDelivery, ...]` |
| `ServiceDiagnostics` | `developer.contracts` | `ServiceRegistry` | `tuple[ServiceDescriptor, ...]` |
| `PluginDiagnostics` | `developer.contracts` | `PluginLoader` | `Iterable[object]` (yields `PluginManifest`) |
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
