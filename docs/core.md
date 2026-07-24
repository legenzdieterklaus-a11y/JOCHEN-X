# Core

The core is composed exclusively by `ApplicationHost`. `ServiceRegistry` supports singleton,
transient, scoped, typed, and factory registrations. Resolution is lazy and validates dependency
graphs with circular-dependency detection. `LifecycleManager` owns ordered start, stop, restart,
recovery, and health state without starting threads itself.

## Service Registration by Subsystem

| Subsystem | Service Keys Registered | Registered By |
|---|---|---|
| Core | `Environment`, `ConfigurationService`, `ApplicationSettings`, `Logger`, `ConnectionManager`, `SettingsRepository`, `EventBus`, `VersionManager`, `DisposableRegistry` | `RegistryStage` |
| Themes | `ThemeEngine` | `ThemeStage` |
| Scheduler | `TaskScheduler` | `SchedulerStage` |
| Plugin Framework | `PluginLoader`, `PluginCatalog` | `PluginDiscoveryStage` |
| Security | `SecurityManager`, `SecretVault`, `PermissionManager`, `PluginSecurity`, ... | `SecurityBootstrapStage` |
| Resources | `ResourceManager` | `ResourceStage` |
| Developer | `DeveloperPlatform` (optional) | `DeveloperToolsStage` |
| DI | `ServiceProvider` | `DependencyInjectionStage` |

**Cross-references:** [Foundation Architecture](architecture.md) ·
[Plugin Framework](extensions.md) · [Events](events.md) ·
[Services](services.md) · [Security](security.md)
