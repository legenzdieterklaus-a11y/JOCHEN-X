# ADR 002: Explicit event delivery modes

**Status:** Accepted

The bus retains synchronous publishing for deterministic short notifications and
provides an async entry point for non-blocking delivery. Consumers, rather than
the core, own executor or UI-loop integration because the core cannot safely
assume a running event loop.

## Implications for the Plugin Framework

All plugin lifecycle events (`PluginLoading`, `PluginLoaded`, `PluginFailed`)
and security events (`PluginVerified`, `PluginRejected`) are published
synchronously during bootstrap because they are brief, in-process notifications
that must complete before the next bootstrap phase begins.

**Cross-references:** [Plugin Framework](../extensions.md) §5 ·
[Events](../events.md)
