# Architecture Inspector

`ArchitectureInspector` evaluates public service descriptors and reports
non-invasive warnings. It never accesses the container's internal registration
map or resolves services.

The inspector can verify that Plugin Framework services (`PluginLoader`,
`PluginCatalog`) are registered with expected lifetimes and dependency graphs by
reading the `ServiceDescriptor` tuples returned by `ServiceRegistry.descriptors()`.

**Cross-references:** [Core](core.md) · [Services](services.md) ·
[Diagnostics](diagnostics.md)
