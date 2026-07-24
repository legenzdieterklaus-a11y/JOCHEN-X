# Performance

`PerformanceController` selects a policy mode: normal, gaming, idle, low-power,
benchmark, sleep, or maintenance. It does not alter hardware or spawn monitors.
Resource collection is represented by the synchronous `ResourceMonitor` port and
immutable `ResourceSnapshot`.

## Plugin Framework Performance

The Plugin Framework has no dedicated performance monitoring in v0.7.0. Plugin
discovery executes synchronously during bootstrap and its duration is included
in the `ApplicationReady.startup_ms` metric. The discovery algorithm performs
sequential filesystem I/O (one `glob` call plus one TOML parse per manifest) and
completes in negligible time for typical plugin counts.

**Cross-references:** [Plugin Framework](extensions.md) · [Health](health.md)
