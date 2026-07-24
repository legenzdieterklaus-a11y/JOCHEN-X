# ADR 001: Explicit core boundaries

**Status:** Accepted

Core modules expose ports and value types and are assembled by the application
host. This preserves dependency inversion, avoids global state, and allows
platform or feature implementations to remain outside the low-overhead startup
path.

## Implications for the Plugin Framework

Plugin code is never imported or executed by the foundation. The `PluginLoader`
reads only TOML manifest files and produces immutable `PluginManifest` value
objects. Extension protocols (`PluginExtension`, `ToolExtension`, etc.) are
defined in the core layer as stable contracts that plugin implementations will
satisfy structurally.

**Cross-references:** [Plugin Framework](../extensions.md) §2.3 ·
[Foundation Architecture](../architecture.md)
