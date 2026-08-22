# Core

The core is composed exclusively by `ApplicationHost`. `ServiceRegistry` supports singleton,
transient, scoped, typed, and factory registrations. Resolution is lazy and validates dependency
graphs with circular-dependency detection. `LifecycleManager` owns ordered start, stop, restart,
recovery, and health state without starting threads itself.

## Service Registration by Subsystem

| Subsystem | Service Keys Registered | Registered By |
|---|---|---|
| Core | `Environment`, `ConfigurationService`, `ApplicationSettings`, `Logger`, `ConnectionManager`, `SettingsRepository`, `EventBus`, `VersionManager`, `DisposableRegistry`, `Metrics` | `RegistryStage` |
| Themes | `ThemeEngine` | `ThemeStage` |
| Scheduler | `TaskScheduler` | `SchedulerStage` |
| Plugin Framework | `PluginLoader`, `PluginCatalog` | `PluginDiscoveryStage` |
| Plugin Framework | `PluginCatalog` (filtered to the admitted set), `PluginSecurity` | `PluginSecurityStage` |
| Plugin Runtime | `PluginRuntimePool`, `ActivationFailurePool`, `PluginDiagnosticsReport` | `PluginActivationStage` |
| Observability | `HealthCheckRegistry`, `MetricsRegistry` | `PluginActivationStage` |
| Security | `SecurityManager`, `SecretVault`, `PermissionManager`, `PluginSecurity`, ... | `SecurityBootstrapStage` (`app/security/security_manager.py`, opt-in) |
| Resources | `ResourceManager` | `ResourceStage` |
| Developer | `DeveloperPlatform` (optional) | `DeveloperToolsStage` |
| DI | `ServiceProvider` | `DependencyInjectionStage` |

The default bootstrap sequence (`app.bootstrap.default_stages()`) is
`EnvironmentStage → ConfigurationStage → LoggingStage → DatabaseStage →
RegistryStage → ThemeStage → SchedulerStage → PluginDiscoveryStage →
PluginSecurityStage → ResourceStage → PluginActivationStage →
DeveloperToolsStage → DependencyInjectionStage`.

## Observability Contracts

`core/observability.py` holds the metric, tracing, health and plugin-diagnostic
contracts; `core/observability_registry.py` holds their additive registration
points (`MetricsRegistry`, `HealthCheckRegistry`). Neither module samples
autonomously and neither starts a thread. See [Health](health.md),
[Performance](performance.md) and [Diagnostics](diagnostics.md).

**Cross-references:** [Foundation Architecture](architecture.md) ·
[Plugin Framework](extensions.md) · [Events](events.md) ·
[Services](services.md) · [Security](security.md)
