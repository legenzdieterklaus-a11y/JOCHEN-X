# Developer Platform

The Developer Platform is an optional package, disabled by default and absent from normal host
composition. Instantiate `DeveloperPlatform(enabled=True, ...)` only from a developer-only
composition root. It starts no workers and performs file I/O only when a caller requests logs.
