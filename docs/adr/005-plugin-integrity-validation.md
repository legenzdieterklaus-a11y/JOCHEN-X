# ADR 005: Plugin integrity validation

**Status:** Open – requires decision before implementation

## Context

The `PluginStatus` model includes a `signature_status` field (currently
hardcoded to `"unverified"`), anticipating a future integrity verification
system. No signature or hash validation exists in v0.7.0. The `PluginLoader`
reads and parses `plugin.toml` files without verifying their authenticity or
that the associated plugin code has not been tampered with.

## Decision Required

How should plugins be verified for integrity before admission?

### Option A: Cryptographic signature verification

Each plugin directory includes a detached signature file (e.g.,
`plugin.toml.sig`) signed with a known public key. The `PluginLoader` or a
dedicated `IntegrityValidator` verifies the signature before constructing the
`PluginManifest`.

### Option B: Content hash verification

Each manifest includes a `content_hash` field containing a SHA-256 hash of the
plugin's entry point or package contents. The foundation verifies the hash at
discovery time.

### Option C: Defer to external tooling

Integrity validation is performed by an external packaging or distribution
tool before plugins are placed in the plugin directory. The foundation trusts
the filesystem boundary.

## Consequences

The chosen option determines:
- Whether the foundation requires cryptographic libraries.
- The manifest schema extension (signature fields, hash fields).
- The `PluginStatus.signature_status` semantic (what values are valid).
- The performance impact of discovery (crypto operations per plugin).

**Cross-references:** [Plugin Framework](../extensions.md) §3.7 ·
[Security](../security.md)
