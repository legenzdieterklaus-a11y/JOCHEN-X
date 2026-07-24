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
| `LOAD_RESOURCES` | `ResourceStage` | `ResourceManager` registration |
| `FINALIZE` | `DeveloperToolsStage` | Optional developer platform (see [Developer Platform](developer.md)) |
| `FINALIZE` | `DependencyInjectionStage` | `ServiceProvider` facade, container validation |

The `ServiceRegistry` is the only composition mechanism and is passed explicitly
to consumers. The SQLite database contains only `schema_version` and `settings`.
Configuration is validated before it reaches runtime services.

Plugin code is discovered as metadata via `PluginLoader`; it is never imported
or executed by the foundation (see [Plugin Framework](extensions.md) §2.3 and
[ADR-001](adr/001-core-boundaries.md)).

**Cross-references:** [Core](core.md) · [Events](events.md) ·
[Security](security.md) · [Plugin Framework](extensions.md) ·
[Diagnostics](diagnostics.md) · [Developer Platform](developer.md)

## Proposed ADRs

The referenced Master Specification 1.0 was not supplied with this implementation
request, so no undocumented architectural change has been made. If it requires a
different composition root or package direction, record that as an ADR before
modifying these boundaries.
