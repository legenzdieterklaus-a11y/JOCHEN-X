# Performance

`PerformanceController` selects a policy mode: normal, gaming, idle, low-power,
benchmark, sleep, or maintenance. It does not alter hardware or spawn monitors.
Resource collection is represented by the synchronous `ResourceMonitor` port and
immutable `ResourceSnapshot`.

## Metrics

| Symbol | Module | Role |
|---|---|---|
| `Metrics` | `core/observability.py` | In-memory recorder (`increment`, `record_duration`, `snapshot`). No autonomous sampling. |
| `MetricSource` | `core/observability_registry.py` | Protocol: `collect() -> Mapping[str, float]`. |
| `CallableMetricSource` | `core/observability_registry.py` | Adapter exposing a plain callable as a `MetricSource`. |
| `MetricsRegistry` | `core/observability_registry.py` | Registration point (`register`, `unregister`, `names`, `collect`, `merge`). |
| `MetricsSnapshot` | `services/observability.py` | Frozen process/gaming sample; unavailable measurements stay `None`. |
| `PerformanceMonitor` | `services/observability.py` | Synchronous process sampling; creates no background thread. |
| `ProcessMetricSource` | `services/observability.py` | `MetricSource` adapter over `PerformanceMonitor`; publishes only the measured fields. |

Registration is strictly additive: a registered source publishes exclusively
under `"<source name>.<metric name>"`, and `MetricsRegistry.merge(metrics)`
neither mutates the passed `Metrics` instance nor overrides an existing value —
on a name collision the recorded value wins. Registering a source therefore
cannot change any metric that already exists.

The plugin pipeline records `plugin.security.validation_ms.<id>`,
`plugin.dependency.resolution_ms` and `plugin.activation.duration_ms.<id>` on
the bootstrap `Metrics` instance, and registers a `plugin.runtime` source
carrying the activated/rejected/failed counts.

## Plugin Framework Performance

The plugin pipeline is instrumented on the bootstrap `Metrics` instance. Every
duration is recorded in milliseconds:

| Metric | Recorded by | Scope |
|---|---|---|
| `plugin.security.validation_ms.<identifier>` | `PluginSecurityStage` | Per manifest, around integrity validation, the SDK API version gate and permission validation. |
| `plugin.dependency.resolution_ms` | `PluginSecurityStage` | Once, around dependency resolution over all admitted manifests. |
| `plugin.activation.duration_ms.<identifier>` | `PluginActivationStage` | Per plugin, around import and lifecycle start. |

The two per-plugin durations — `plugin.security.validation_ms.<identifier>` and
`plugin.activation.duration_ms.<identifier>` — are recorded in a `finally`
block, so a rejected or failed plugin is measured as well as a successful one.
`plugin.dependency.resolution_ms` is not: it is recorded only after the
resolution step has returned, so the metric is absent for that bootstrap run if
resolution raises.

`PluginActivationStage` additionally registers the metric source
`plugin.runtime` — a `CallableMetricSource` over `PluginDiagnosticsReport.counts`
— on the `MetricsRegistry` it publishes. It therefore exposes
`plugin.runtime.activated`, `plugin.runtime.rejected` and `plugin.runtime.failed`
under the namespacing rule above.

Plugin discovery itself carries no separate metric: it executes synchronously
during bootstrap and its duration is contained in the
`ApplicationReady.startup_ms` value. The discovery algorithm performs sequential
filesystem I/O (one `glob` call plus one TOML parse per manifest).

**Cross-references:** [Plugin Framework](extensions.md) · [Health](health.md)
