# ADR 003: Developer platform is opt-in

**Status:** Accepted

Diagnostics are packaged separately and disabled by default. This preserves
startup performance, allows removal without affecting production composition,
and prevents developer tooling from becoming an application dependency.

## Implications for the Plugin Framework

The `PluginDiagnostics` port is consumed only by the optional Developer
Platform. When disabled (`developer_enabled = false`), no plugin diagnostic
data is collected or exposed. The `DeveloperToolsStage` is the only stage that
references `PluginDiagnostics`.

**Cross-references:** [Plugin Framework](../extensions.md) §3.7 ·
[Diagnostics](../diagnostics.md) · [Developer Platform](../developer.md)
