# Services

Registrations belong only in the composition root. Singleton instances are
constructed on first use, transient registrations construct per resolution, and
scoped registrations require an explicit `ServiceScope`. `validate()` resolves
the graph during bootstrap when eager verification is wanted.

## Service Lifetimes

| Lifetime | Construction | Scope Requirement | Use Case |
|---|---|---|---|
| `SINGLETON` | Once (on first resolution) | None | Shared infrastructure (e.g., `EventBus`, `PluginLoader`) |
| `TRANSIENT` | Every resolution | None | Stateless or short-lived instances |
| `SCOPED` | Once per `ServiceScope` | Requires explicit scope | Request-scoped or session-scoped services |

## Plugin Framework Services

The plugin pipeline registers eight distinct service keys during bootstrap, all
as singleton instances:

| Service key | Registered by | Content |
|---|---|---|
| `PluginLoader` | `PluginDiscoveryStage` | Manifest discovery service. |
| `PluginCatalog` | `PluginDiscoveryStage` | Immutable snapshot of the discovered, version-compatible identifiers. |
| `PluginSecurity` | `PluginSecurityStage` | Trust ledger and manifest validation, registered unless an earlier stage supplied one. |
| `PluginCatalog` (replaced) | `PluginSecurityStage` | The discovery snapshot is replaced by the admitted set, so the registered catalog is the admission result. |
| `PluginRuntimePool` | `PluginActivationStage` | Activated `PluginRuntime` instances in activation order. |
| `ActivationFailurePool` | `PluginActivationStage` | `ActivationFailure` records of failed activations. |
| `PluginDiagnosticsReport` | `PluginActivationStage` | Consolidated `PluginDiagnostic` entries of the whole pipeline run. |
| `HealthCheckRegistry` | `PluginActivationStage` | One `PluginHealthCheck` per plugin. |
| `MetricsRegistry` | `PluginActivationStage` | Additive metric-source registration point carrying the `plugin.runtime` source. |

Because `PluginCatalog` is registered twice, the nine registration calls yield
eight distinct keys.

See [Plugin Framework](extensions.md) §7 for the same table with lifetimes.

**Cross-references:** [Core](core.md) · [Plugin Framework](extensions.md) ·
[Foundation Architecture](architecture.md)
