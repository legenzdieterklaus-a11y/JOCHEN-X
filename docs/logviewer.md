# Log Viewer

Log viewing is explicit and on-demand. Search and level filters apply after
lines are read. Known secret assignment formats are redacted before rendering or
export; callers must still avoid logging secrets in the first place.

Plugin lifecycle events (`plugins.discovered`, `plugins.discovery_failed`,
`plugin.approved`, `plugin.rejected`) appear in the application log and can be
filtered using the standard level and search mechanisms.

**Cross-references:** [Plugin Framework](extensions.md) §10.2 ·
[Developer Platform](developer.md)
