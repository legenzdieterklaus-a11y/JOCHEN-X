# ADR 009: Plugin isolation strategy

**Status:** Open – requires decision before implementation

## Context

In v0.7.0, plugin isolation is achieved structurally: the foundation never
imports or executes plugin code (see [ADR-001](001-core-boundaries.md)). When
plugins are activated in a future version, a runtime isolation strategy will
be needed to contain faults, limit resources, and prevent plugins from
interfering with the foundation or with each other.

## Decision Required

How should plugin code be isolated during execution?

### Option A: In-process isolation with module-level sandboxing

Plugins run in the same Python process but in isolated module namespaces.
A custom import hook restricts which foundation modules plugins can access.
Fault containment relies on exception boundaries and watchdog timeouts.

### Option B: Subprocess isolation

Each plugin runs in a separate Python subprocess. Communication with the
foundation uses a defined IPC mechanism (e.g., pipes, shared memory, or
JSON-RPC). This provides strong fault containment and resource limits via
OS-level process controls.

### Option C: Thread-based isolation with capability restrictions

Plugins run in dedicated threads within the main process. A restricted
`PluginContext` limits accessible APIs. Fault containment relies on
thread-level exception handling and watchdog monitoring.

## Consequences

The chosen option determines:
- The plugin activation model (import, subprocess spawn, thread start).
- The communication mechanism between plugin and foundation.
- The resource limit enforcement (memory, CPU, I/O).
- The fault containment boundary (process, thread, exception).
- The performance overhead per plugin.
- The complexity of the Plugin SDK.

**Cross-references:** [Plugin Framework](../extensions.md) §2.3 ·
[ADR-001](001-core-boundaries.md) ·
[ADR-008](008-plugin-context-definition.md)
