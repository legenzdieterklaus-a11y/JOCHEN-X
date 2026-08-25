# Milestone 0.9 Engineering Specification

## Document Control

| Eigenschaft | Wert |
|---|---|
| **Titel** | Plugin Contract Hardening |
| **Status** | APPROVED |
| **Version** | 0.9.1 |
| **Datum** | 2026-07-29 |
| **Baseline** | Release Tag `v0.8.0` |
| **Architecture** | [Architecture Book v2.0](architecture-book-v2.md) (FROZEN) |
| **Development Standard** | [v1.1](development-standard-v1.1.md) |
| **Roadmap** | [Milestone 0.9 Roadmap](milestone-0.9-roadmap.md) |
| **Predecessor** | [Milestone 0.8 Engineering Specification](milestone-0.8-engineering-spec.md) (APPROVED) |
| **ADRs** | ADR-005 (Integrity, APPROVED), ADR-006 (Permissions, APPROVED), ADR-007 (Dependencies, APPROVED) |

---

## Status

APPROVED — Independent Review completed, Correction Phase completed, Final Verification passed, Approval granted 2026-07-29.

---

## Executive Summary

Milestone 0.9 vervollständigt den Plugin-Contract, bevor produktorientierte Features eingeführt werden. Milestone 0.8 hat die Host-Integration etabliert (Discovery → Security → Activation → Shutdown). Der Contract ist jedoch unvollständig: kein Permission-Modell, keine Capability-Abstraktion, minimales Manifest-Schema, keine Dependency-Resolution, keine Integrity-Validation, kein formales API-Version-Gate, kein Reference Plugin.

Milestone 0.9 adressiert diese Lücken in elf Arbeitspaketen: Capability Matrix, Manifest v2, API Version Gate, Permission Model (ADR-006), Dependency Resolution (ADR-007), Activation Validation, Golden Reference Plugin, Observability, Integrity Validation (ADR-005), Testing und Governance Completion. SDK API bleibt bei 1.0.0 — alle Änderungen sind additiv.

Drei ADRs (005, 006, 007) sind APPROVED. Architekturentscheidungen stehen in den genehmigten ADRs.

---

## Purpose

Diese Engineering Specification ist der Implementation Contract für Milestone 0.9. Sie definiert Scope, Gap Analysis, Implementierungsreihenfolge und Akzeptanzkriterien gemäß Development Standard v1.1 §6.

---

## 1. Baseline Verification

| Eigenschaft | Wert | Evidence |
|---|---|---|
| **Release Tag** | `v0.8.0` | Verified: Milestone 0.8 APPROVED |
| **Application Version** | `0.8.0` | Verified: `pyproject.toml` → `project.version` |
| **SDK Version** | `0.8.0` | Verified: `sdk/version.py:24` → `SDK_VERSION` |
| **SDK API Version** | `1.0.0` | Verified: `sdk/version.py:28` → `SDK_API_VERSION` |
| **Architecture Freeze** | Architecture Book v2.0 — FROZEN | Verified: `docs/architecture-book-v2.md` |
| **Core Runtime** | v1.0.0 | Verified: Tag `core-runtime-v1.0.0` |
| **ADR-005** | Approved | Verified: `docs/adr/005-plugin-integrity-validation.md` |
| **ADR-006** | Approved | Verified: `docs/adr/006-plugin-permission-model.md` |
| **ADR-007** | Approved | Verified: `docs/adr/007-plugin-dependency-resolution.md` |
| **ADR-011** | Accepted | Verified: `docs/adr/011-sdk-host-integration.md` |
| **config/default.toml** | `version = "0.8.0"` | Verified: `config/default.toml:3` → `version = "0.8.0"` |

---

## 2. Scope Verification

### Completed (Milestone 0.8 Baseline)

| Item | Datei | Zeilen | Status |
|---|---|---|---|
| Plugin Discovery (manifest-only) | `app/bootstrap.py` | 228–260 | Vollständig |
| PluginSecurityStage | `app/bootstrap.py` | 274–346 | Vollständig |
| PluginActivationStage | `app/bootstrap.py` | 348–471 | Vollständig |
| PluginSecurity Trust Ledger | `app/security/plugin_security.py` | 45–131 | Vollständig |
| PluginTrustLevel Enum | `app/security/models.py` | 25–31 | Vollständig |
| PluginRuntime Lifecycle | `sdk/plugin.py` | 277–393 | Vollständig |
| PluginContextBuilder | `sdk/context.py` | — | Vollständig |
| Plugin Base Classes (5) | `sdk/plugin.py` | — | Vollständig |
| PluginMetadata (mit api_version, category, permissions, dependencies) | `sdk/manifest.py` | 148–373 | Vollständig |
| PluginPermission Enum (10 Werte) | `sdk/manifest.py` | 47–64 | Vollständig |
| PluginDependency Dataclass | `sdk/manifest.py` | 125–145 | Vollständig |
| PluginCategory Enum (8 Werte) | `sdk/manifest.py` | 34–43 | Vollständig |
| PermissionCheck Callable | `sdk/events.py` | 83 | Vollständig |
| ServicePermissionCheck Callable | `sdk/services.py` | 31 | Vollständig |
| PermissionManager (RBAC) | `app/security/permission_manager.py` | 24–127 | Vollständig |
| ServiceRegistry (mit Circular Dependency Detection) | `core/registry.py` | 22–130 | Vollständig |
| Observability Stubs (HealthCheck, Metrics, Tracer) | `core/observability.py` | 8–42 | Minimal |
| Reverse Shutdown | `app/application_host.py` | — | Vollständig |
| Application Events (PLUGIN_ACTIVATING, PLUGIN_ACTIVATED) | `app/events.py` | — | Vollständig |
| ApiVersion Compatibility Check | `sdk/version.py` | 31–81 | Vollständig |

### Partial

| Item | Status | Was fehlt |
|---|---|---|
| API Version Gate | Major-Version-Check in PluginActivationStage (`bootstrap.py:411–416`) | Kein Manifest-Level-Gate; Check erst nach Code-Import; keine Minor/Patch-Kompatibilitätsprüfung |
| Dependency Resolution | Flat Presence Check in PluginActivationStage (`bootstrap.py:418–423`) | Keine topologische Sortierung; keine Version-Constraint-Prüfung gegen `minimum_version`; keine Cycle Detection zwischen Plugins |
| Permission Enforcement | `PermissionCheck` / `ServicePermissionCheck` Callables existieren im SDK | Keine Verbindung zum Host `PermissionManager`; keine Capability-zu-Permission-Auflösung; keine Manifest-basierte Grant-Semantik |
| Manifest Schema | `PluginMetadata` hat `api_version`, `category`, `permissions`, `dependencies` | Kein `plugin.toml` v2 Parser; Manifest v1 in `plugins/loader.py` kennt nur `id`, `version`, `requires_application`; keine TOML-Deklaration der neuen Felder |
| Observability | `Metrics`, `Tracer`, `HealthCheck` Protocol existieren | Nur Counter-Metrics; kein Duration-Tracking; keine Plugin-spezifischen Health Checks; keine Failure Diagnostics |

### Missing

| Item | Beschreibung |
|---|---|
| Capability Matrix | Keine Capability-Abstraktion definiert; `PluginPermission` Enum existiert, aber referenziert direkte Zugriffsarten, keine stabilen Capabilities |
| Manifest v2 TOML Parser | Kein Parser für erweiterte `plugin.toml` Felder (permissions, dependencies, api_version, category, metadata, entry_point) |
| Activation Validation (konsolidiert) | Kein dedizierter Validierungsschritt vor Activation; Prüfungen sind verstreut innerhalb `PluginActivationStage` |
| Golden Reference Plugin | Kein Reference Plugin vorhanden; keine `plugin.toml` im Repository |
| Integrity Validation | Kein Integritätsmodell definiert; `SignatureStatus` Enum existiert, aber wird nicht geprüft |
| Plugin Dependency Graph | Keine topologische Sortierung; keine Cycle Detection zwischen Plugins |
| Plugin Health Checks | Kein `HealthCheck` Protocol für Plugin-Runtime-Status |
| Failure Diagnostics | Keine strukturierte Diagnostik bei Plugin-Activation-Fehlern |

---

## 3. Gap Analysis

### Abhängigkeitskette der Lücken

```
ADR-006 (Permission Model)                    ADR-007 (Dependency Resolution)
    │                                              │
    ▼                                              │
Capability Matrix                                  │
    │                                              │
    ▼                                              │
Manifest v2 TOML Parser ◄─────────────────────────┘
    │
    ▼
API Version Gate (Manifest-Level)
    │
    ▼
Activation Validation (konsolidiert)
    │
    ▼
Golden Reference Plugin ◆ Release Gate
    │
    ▼
Observability (Plugin Metrics + Health)
    │
    ▼
ADR-005 (Integrity Validation)
```

### Lückenbewertung

| Lücke | Schweregrad | Begründung |
|---|---|---|
| Permission Model (ADR-006) | Hoch | Ohne Permission-Modell haben Plugins theoretisch unbeschränkten Zugriff; blockiert Capability Matrix und Manifest v2 |
| Capability Matrix | Hoch | Ohne stabile Capability-Identifikatoren können Permissions nicht manifest-deklariert werden |
| Manifest v2 TOML Parser | Hoch | Ohne Parser können erweiterte Plugin-Manifeste nicht eingelesen werden; blockiert API Version Gate, Dependencies, Permissions |
| Dependency Graph (ADR-007) | Hoch | Ohne topologische Sortierung ist die Activation-Reihenfolge undefiniert; ohne Version-Constraints ist Kompatibilität nicht prüfbar |
| Activation Validation | Mittel | Prüfungen existieren verstreut, aber nicht konsolidiert; kein binärer Accept/Reject vor Code-Import |
| API Version Gate | Mittel | Major-Check existiert, aber erst nach Code-Import; sollte auf Manifest-Ebene erfolgen |
| Golden Reference Plugin | Hoch | Kein end-to-end Validierungsartefakt für den Plugin-Contract |
| Integrity Validation (ADR-005) | Mittel | Modell fehlt; `SignatureStatus` existiert als Datenstruktur, wird aber nicht validiert |
| Observability | Niedrig | Infrastruktur existiert; Plugin-spezifische Metriken und Health Checks fehlen |

---

## 4. Delta Analysis

Exakte Differenz zwischen Baseline `v0.8.0` und Zielzustand Milestone 0.9 pro Datei:

| Datei | Baseline-Zustand | Zielzustand (0.9.0) | Änderungstyp |
|---|---|---|---|
| `sdk/manifest.py` | `PluginPermission` mit 10 festen Werten; `PluginMetadata` ohne `entry_point` | Capability-basierte Permission-Deklaration; `entry_point` Feld auf `PluginMetadata`; Manifest v2 Validation Logik | Erweiterung |
| `plugins/loader.py` | Parst nur `id`, `version`, `requires_application` aus `plugin.toml` | Parst alle Manifest v2 Felder: `api_version`, `category`, `entry_point`, `metadata.*`, `permissions.capabilities`, `dependencies.requires` | Erweiterung |
| `plugins/__init__.py` | Exportiert `PluginManifest`, `PluginCatalog`, `PluginLoader` | +Erweiterte `PluginManifest` Felder | Erweiterung |
| `app/bootstrap.py` | `PluginActivationStage` mit inline Major-Version-Check und flat Dependency-Check | Manifest-Level API Version Gate vor Code-Import; konsolidierte Activation Validation; Dependency-Graph-Integration. Exakte Änderungen werden durch akzeptierte ADR-006 und ADR-007 bestimmt | Erweiterung |
| `app/security/plugin_security.py` | Trust Ledger ohne Permission-Prüfung | +Permission-Validation bei Manifest-Admission. Exakte Semantik wird durch akzeptierten ADR-006 bestimmt | Erweiterung |
| `core/observability.py` | Counter-Metrics, Stub-Tracer, HealthCheck Protocol | +Duration-Metrics für Plugin-Lifecycle; +Plugin HealthCheck Implementierung; +Failure Diagnostics Datenstruktur | Erweiterung |
| `plugins/reference/plugin.toml` | Nicht vorhanden | Neues Manifest v2 mit allen Feldern: id, version, api_version, category, entry_point, metadata, permissions, dependencies | Neu |
| `plugins/reference/__init__.py` | Nicht vorhanden | Golden Reference Plugin Implementation — nutzt alle SDK-Features | Neu |
| `tests/test_manifest_v2.py` | Nicht vorhanden | Manifest v2 Parsing und Validation Tests | Neu |
| `tests/test_capability_matrix.py` | Nicht vorhanden | Capability-Identifikator-Tests | Neu |
| `tests/test_activation_validation.py` | Nicht vorhanden | Konsolidierte Activation Validation Tests | Neu |
| `tests/test_golden_reference.py` | Nicht vorhanden | Golden Reference Plugin Full-Lifecycle Test | Neu |
| `tests/test_dependency_resolution.py` | Nicht vorhanden | Dependency Graph, Topologische Sortierung, Cycle Detection Tests | Neu |
| `tests/test_plugin_observability.py` | Nicht vorhanden | Plugin Metrics und Health Check Tests | Neu |
| `pyproject.toml` | `version = "0.8.0"` | `version = "0.9.0"` | Version Bump |
| `sdk/version.py` | `SDK_VERSION = "0.8.0"` | `SDK_VERSION = "0.9.0"`; `SDK_API_VERSION` bleibt `"1.0.0"` | Version Bump |
| `config/default.toml` | `version = "0.8.0"` | `version = "0.9.0"` | Version Bump |

**Keine Änderungen an:**
- `docs/architecture-book-v2.md` — Architecture Book bleibt FROZEN
- `core/registry.py` — ServiceRegistry bleibt unverändert
- `core/events.py` — EventBus bleibt unverändert
- `sdk/plugin.py` — Plugin Base Classes und PluginRuntime bleiben unverändert
- `sdk/context.py` — PluginContextBuilder bleibt unverändert

---

## 5. Module Work Breakdown

### 5.1 Capability Matrix

**Betroffene Module:** `sdk/manifest.py`

**Constraint:** Die Capability Matrix definiert ausschließlich Contract-Identifikatoren (architekturelles Vokabular, nicht finale Architektur). Capabilities implizieren keine Host-Implementierung. Die Enforcement-Semantik (Grant/Deny/Prompt) wird durch ADR-006 bestimmt, nicht durch diese Specification.

**Änderungen:**

1. Capability-Identifikatoren als Enum oder vergleichbare Konstanten definieren:
   - `FILESYSTEM`, `NETWORK`, `CLIPBOARD`, `NOTIFICATIONS`, `BROWSER`, `SETTINGS`, `TERMINAL`, `AI`, `CAMERA`, `AUDIO`

2. Mapping zwischen Capabilities und bestehenden `PluginPermission`-Werten dokumentieren.

3. `PluginPermission` wird nicht entfernt — Capabilities erweitern das Vokabular.

**Specification Sketch** (illustriert die erwartete Struktur, keine Implementation):

```
Capability Identifier       Typ               TOML-Referenz
─────────────────────────────────────────────────────────
"filesystem"                String-Konstante   capabilities = ["filesystem"]
"network"                   String-Konstante   capabilities = ["network"]
...
```

**Interfaces:** Capability-Identifikatoren MÜSSEN als stabile String-Konstanten referenzierbar sein (für Manifest-Deklaration in TOML).

**Abhängigkeiten:** ADR-006 (APPROVED) definiert die Permission-Semantik, die Capabilities referenziert.

### 5.2 Manifest v2 TOML Parser

**Betroffene Module:** `plugins/loader.py`, `sdk/manifest.py`

**Änderungen:**

1. `plugins/loader.py` — `PluginManifest` erweitern um:
   - `api_version: Version` (optional, Default: SDK_API_VERSION)
   - `category: str` (optional, Default: "general")
   - `entry_point: str` (optional, Default: Modulname)
   - `metadata: dict` (optional, Display-Name, Description, Author)
   - `permissions: tuple[str, ...]` (optional, Capability-Identifikatoren)
   - `dependencies: tuple[dict, ...]` (optional, {id, version})

2. `PluginLoader` — Parser für `plugin.toml` erweitern:
   - Neue TOML-Sektionen parsen: `[plugin.metadata]`, `[plugin.permissions]`, `[plugin.dependencies]`
   - Unbekannte Felder ignorieren (forwards compatibility)
   - Validation: Identifier-Format, Semver-Format, bekannte Capability-Identifikatoren

3. `sdk/manifest.py` — `PluginMetadata.from_loader_manifest()` erweitern:
   - Neue Manifest-Felder auf `PluginMetadata`-Felder abbilden
   - `entry_point` Feld zu `PluginMetadata` hinzufügen

**Specification Sketch** (illustriert die erwarteten Manifest v2 Felder, keine Implementation):

```
[plugin]
id = "example"
version = "1.0.0"
api_version = "1.0.0"          # optional, Default: SDK_API_VERSION
category = "tool"              # optional, Default: "general"
entry_point = "main"           # optional, Default: Modulname

[plugin.metadata]              # optional
display_name = "Example"
description = "..."
author = "..."

[plugin.permissions]           # optional
capabilities = ["filesystem", "notifications"]

[plugin.dependencies]          # optional
requires = [
    { id = "other-plugin", version = ">=1.0.0" }
]
```

**Backwards Compatibility:** Manifest v1 Felder (`id`, `version`, `requires_application`) bleiben erhalten. Alle neuen Felder sind optional.

**Abhängigkeiten:** Capability Matrix (5.1).

### 5.3 API Version Gate

**Betroffene Module:** `app/bootstrap.py`

**Änderungen:**

1. API-Version-Prüfung von `PluginActivationStage` (nach Code-Import) auf Manifest-Ebene verschieben (vor Code-Import).

2. `api_version` aus dem erweiterten `PluginManifest` lesen.

3. Kompatibilitätsprüfung: `ApiVersion.is_compatible_with()` verwenden statt reinem Major-Check.

4. Inkompatible Plugins VOR Code-Import ablehnen.

**Specification Sketch** (illustriert die erwartete Prüflogik, keine Implementation):

```
Manifest geladen → api_version extrahieren
    → ApiVersion.is_compatible_with(SDK_API_VERSION) aufrufen
    → Ergebnis: kompatibel → weiter zu Activation
    → Ergebnis: inkompatibel → Plugin ablehnen VOR Code-Import
       → Diagnostik: "Plugin requires API vX.Y.Z, host provides vA.B.C"
```

**Interfaces:** `PluginManifest` MUSS `api_version` enthalten (aus Manifest v2).

**Abhängigkeiten:** Manifest v2 TOML Parser (5.2).

### 5.4 ADR-006: Permission Model Integration

**Betroffene Module:** `app/bootstrap.py`, `app/security/plugin_security.py`, `sdk/events.py`, `sdk/services.py`

**Constraint:** Die architektonische Semantik des Permission-Modells wird durch den akzeptierten ADR-006 definiert. Diese Specification definiert die erforderlichen Verhaltensweisen und Akzeptanzkriterien. Die Enforcement-Semantik (einschließlich Default-Policy) wird vollständig durch ADR-006 bestimmt.

**Erforderliches Verhalten:**

1. Plugins MÜSSEN ihre benötigten Capabilities im Manifest deklarieren.
2. Der Host MUSS deklarierte Capabilities zur Admission-Zeit gegen eine Policy validieren.
3. Nicht-deklarierte Capabilities MÜSSEN zur Laufzeit verweigert werden (gemäß der Default-Policy aus ADR-006).
4. Die bestehenden `PermissionCheck` und `ServicePermissionCheck` Callables im SDK MÜSSEN mit dem Host-seitigen Enforcement verbunden werden.
5. `PermissionManager` MUSS als Enforcement-Backend dienen.

**Interfaces:**
- `PluginSecurityStage` — Permission-Validation bei Manifest-Admission
- `PluginEventBus` — Capability-Check bei `publish()`/`subscribe()`
- `PluginServices` — Capability-Check bei `resolve()`

**Abhängigkeiten:** Capability Matrix (5.1). ADR-006 (APPROVED).

### 5.5 ADR-007: Dependency Resolution Integration

**Betroffene Module:** `app/bootstrap.py`

**Constraint:** Die architektonische Semantik der Dependency Resolution wird durch den akzeptierten ADR-007 definiert. Diese Specification definiert die erforderlichen Verhaltensweisen und Akzeptanzkriterien.

**Erforderliches Verhalten:**

1. Dependency Graph MUSS aus Manifest v2 `dependencies.requires` konstruiert werden.
2. Topologische Sortierung MUSS die Activation-Reihenfolge bestimmen.
3. Zyklische Abhängigkeiten MÜSSEN erkannt und abgelehnt werden.
4. Version-Constraints (`minimum_version`) MÜSSEN geprüft werden.
5. Fehlende Required Dependencies MÜSSEN zur Ablehnung des abhängigen Plugins führen.

**Interfaces:**
- `PluginActivationStage` — Dependency-geordnete Activation
- Algorithmus: Topologische Sortierung (vergleichbar `ServiceRegistry._resolve` Cycle Detection)

**Abhängigkeiten:** Manifest v2 TOML Parser (5.2). ADR-007 (APPROVED).

### 5.6 Activation Validation

**Betroffene Module:** `app/bootstrap.py`

**Änderungen:**

1. Konsolidierten Validierungsschritt VOR Code-Import einführen:
   - Manifest-Schema-Validierung (Required Fields, Format)
   - API Version Gate (Kompatibilität)
   - Permission-Validierung (deklarierte Capabilities)
   - Dependency-Validierung (alle aufgelöst, Versionen kompatibel, keine Zyklen)

2. Binäre Accept/Reject-Entscheidung mit diagnostischem Report.

3. Code-Import erfolgt NUR für validierte Plugins.

4. Nach Code-Import: Code-Metadata-Validierung (Plugin-Subclass vorhanden).

**Specification Sketch** (illustriert den konsolidierten Validierungsablauf, keine Implementation):

```
Plugin Manifest geladen
    ├── 1. Schema-Validierung: Required Fields, Format-Prüfung
    ├── 2. API Version Gate: is_compatible_with(SDK_API_VERSION)
    ├── 3. Permission-Validierung: deklarierte Capabilities gegen Policy
    └── 4. Dependency-Validierung: Graph aufgelöst, Versionen kompatibel, keine Zyklen
         │
         ├── Alle bestanden → Accept → Code-Import → Plugin-Subclass-Prüfung
         └── Mindestens eine fehlgeschlagen → Reject mit diagnostischem Report
```

**Abhängigkeiten:** API Version Gate (5.3), ADR-006 Integration (5.4), ADR-007 Integration (5.5).

### 5.7 Golden Reference Plugin

**Betroffene Module:** `plugins/reference/` (neu)

**Änderungen:**

1. `plugins/reference/plugin.toml` — Manifest v2 mit allen Feldern.
2. `plugins/reference/__init__.py` — Plugin-Implementation, die alle SDK-Features nutzt.

**Constraint:** Das Golden Reference Plugin ist ein offizielles Governance-Artefakt (gemäß Milestone 0.9 Roadmap). Es ist kein Sample-Plugin.

**Anforderungen:**
- Nutzt alle Manifest v2 Felder (api_version, category, entry_point, metadata, permissions, dependencies)
- Nutzt Permission-deklarierte Capabilities
- Validiert den vollständig finalisierten Plugin-Contract end-to-end
- Dient als SDK Compatibility Verification, Regression Verification, Bootstrap Pipeline Validation und Developer Reference

**Mandatory Release Requirement:** Der vollständige Lifecycle MUSS bei jedem Release erfolgreich durchlaufen:
Discovery → Security Validation → Activation → Runtime Verification → Graceful Shutdown.
Ein Fehlschlag blockiert die Release-Freigabe.

**Execution Scope:** Das Golden Reference Plugin wird primär in der CI-Pipeline und als Release Gate ausgeführt. Es DARF auch im normalen Runtime geladen werden (Development Mode), ist aber kein Produktions-Plugin. Die Lifecycle-Validierung erfolgt durch den Test `test_golden_reference_full_lifecycle` in der Test-Suite.

**Abhängigkeiten:** Activation Validation (5.6) — das Plugin validiert den finalisierten Contract.

### 5.8 Observability

**Betroffene Module:** `core/observability.py`, `app/bootstrap.py`

**Änderungen:**

1. Duration-Metrics für Plugin-Lifecycle-Schritte:
   - Activation Duration (pro Plugin)
   - Dependency Resolution Time
   - Security Validation Time

2. Plugin Health Check:
   - `HealthCheck` Protocol Implementation für Plugin-Runtime-Status
   - Lifecycle-State als Health-Indikator

3. Failure Diagnostics:
   - Strukturierte Fehlermeldungen bei Activation-Fehlern
   - Diagnostischer Report mit Fehlerursache und -kontext

**Specification Sketch** (illustriert die erwarteten Metriken, keine Implementation):

```
Metrics:
    plugin.activation.duration_ms{plugin_id}      Duration-Metric pro Plugin
    plugin.dependency.resolution_ms                Dependency Resolution Gesamtzeit
    plugin.security.validation_ms{plugin_id}       Security Validation pro Plugin

HealthCheck:
    Plugin Lifecycle-State → HealthCheck.status()
    ACTIVATED → Healthy | FAILED → Unhealthy | STOPPED → Degraded

Failure Diagnostics:
    ActivationFailure { plugin_id, phase, reason, context }
```

**Interfaces:** Nutzt bestehende `Metrics`, `Tracer`, `HealthCheck` aus `core/observability.py`.

**Abhängigkeiten:** Golden Reference Plugin (5.7) — Observability wird gegen das Reference Plugin validiert. Die Abhängigkeit ist eine Validierungsabhängigkeit: das Golden Reference Plugin dient als Testfall für Observability-Metriken. Implementierung kann parallel erfolgen.

### 5.9 ADR-005: Integrity Validation Integration

**Betroffene Module:** `app/security/plugin_security.py`, `app/bootstrap.py`

**Constraint:** Die architektonische Semantik der Integrity Validation wird durch den akzeptierten ADR-005 definiert. Diese Specification definiert die erforderlichen Verhaltensweisen und Akzeptanzkriterien.

**Erforderliches Verhalten:**

1. Integrity Policy MUSS definieren, was validiert wird (Manifest, Code, beides).
2. Trust-Semantik MUSS den bestehenden `PluginTrustLevel` Enum nutzen (UNTRUSTED → VERIFIED → TRUSTED).
3. Plugins, die die Integrity-Prüfung nicht bestehen, MÜSSEN vor Activation abgelehnt werden.
4. Der bestehende `SignatureStatus` Enum (`sdk/manifest.py:67–78`) MUSS als Datenstruktur genutzt werden.

**Expliziter Aufschub:** Kryptographisches Enforcement (PKI, Signaturen) DARF auf einen zukünftigen Milestone deferred werden. Das Modell MUSS ohne kryptographische Implementierung definierbar sein.

**Abhängigkeiten:** ADR-005 (APPROVED).

### 5.10 Version Bump

**Betroffene Module:** `pyproject.toml`, `sdk/version.py`, `config/default.toml`

**Änderungen:**

1. `pyproject.toml`: `version = "0.9.0"`
2. `sdk/version.py`: `SDK_VERSION = "0.9.0"`
3. `config/default.toml`: `version = "0.9.0"`
4. `SDK_API_VERSION` bleibt `"1.0.0"` — keine Breaking Changes an Plugin-API

---

## 6. Dependency Graph

```
ADR-006 (Accepted) ──────────────────────────── ADR-007 (Accepted)
    │                                               │
    ▼                                               │
Capability Matrix (5.1)                             │
    │                                               │
    ▼                                               │
Manifest v2 TOML Parser (5.2) ◄────────────────────┘
    │
    ▼
API Version Gate (5.3)
    │
    ├──── Permission Integration (5.4) ◄──── ADR-006
    │
    ├──── Dependency Integration (5.5) ◄──── ADR-007
    │
    ▼
Activation Validation (5.6)
    │
    ├──── Golden Reference Plugin (5.7) ◆ Release Gate
    │
    ├──── Observability (5.8)  [Validation: gegen Golden Reference Plugin]
    │
    ▼
Integrity Integration (5.9) ◄──── ADR-005 (Accepted)
    │
    ▼
Version Bump (5.10)

ADR-005 (Accepted)
```

**Hinweis zur Observability-Abhängigkeit:** Observability (5.8) hängt vom Golden Reference Plugin (5.7) ausschließlich zur **Validierung** ab — das Reference Plugin dient als Testfall für die Observability-Metriken. Es besteht keine Implementierungsabhängigkeit: Observability kann parallel zum Golden Reference Plugin implementiert werden. Beide Module haben eine gemeinsame Voraussetzung in Activation Validation (5.6).

---

## 7. Implementation Sequence

| Schritt | Modul Work Breakdown | Abhängigkeit | Beschreibung |
|---|---|---|---|
| S-1 | ADR-006 (APPROVED) | — | Permission Model Architekturentscheidung |
| S-2 | ADR-007 (APPROVED) | — | Dependency Resolution Architekturentscheidung |
| S-3 | 5.1 Capability Matrix | S-1 | Capability-Identifikatoren definieren |
| S-4 | 5.2 Manifest v2 TOML Parser | S-3 | Erweitertes `plugin.toml` Schema und Parser |
| S-5 | 5.3 API Version Gate | S-4 | Manifest-Level Kompatibilitätsprüfung |
| S-6 | 5.4 Permission Integration | S-1, S-3 | Host-seitiges Permission Enforcement |
| S-7 | 5.5 Dependency Integration | S-2, S-4 | Dependency Graph und topologische Sortierung |
| S-8 | 5.6 Activation Validation | S-5, S-6, S-7 | Konsolidierter Validierungsschritt |
| S-9 | 5.7 Golden Reference Plugin | S-8 | Governance-Artefakt, Release Gate |
| S-10 | 5.8 Observability | S-8 | Plugin Metrics, Health Checks, Diagnostics (Validierung gegen Golden Reference Plugin) |
| S-11 | ADR-005 (APPROVED) | — | Integrity Validation Architekturentscheidung |
| S-12 | 5.9 Integrity Integration | S-11 | Integrity-Modell und Validation |
| S-13 | 5.10 Version Bump | S-12 | 0.9.0 in pyproject.toml, sdk/version.py, config/default.toml |
| S-14 | Testing | S-3–S-12 | Alle Test-Suiten |

**Parallelisierungspotenzial:**
- S-6 (Permissions) und S-7 (Dependencies) können parallel implementiert werden nach S-4
- S-9 (Golden Reference Plugin) und S-10 (Observability) können parallel implementiert werden nach S-8; Observability-Validierung gegen das Reference Plugin erfolgt nach Abschluss beider

---

## 8. Acceptance Criteria

### AC-1: Capability Matrix

- [ ] Capability-Identifikatoren definiert: FILESYSTEM, NETWORK, CLIPBOARD, NOTIFICATIONS, BROWSER, SETTINGS, TERMINAL, AI, CAMERA, AUDIO
- [ ] Identifikatoren sind stabile String-Konstanten
- [ ] Capabilities implizieren keine Host-Implementierung (Contract-Vokabular only)
- [ ] Nicht-gewährte Capabilities werden gemäß der Default-Policy aus ADR-006 behandelt
- [ ] Mapping zu bestehenden `PluginPermission` dokumentiert

### AC-2: Manifest v2 TOML Parser

- [ ] `plugin.toml` Parser erkennt alle v2 Felder: `api_version`, `category`, `entry_point`, `metadata.*`, `permissions.capabilities`, `dependencies.requires`
- [ ] Manifest v1 Felder (`id`, `version`, `requires_application`) bleiben erhalten
- [ ] Alle neuen Felder sind optional (Backwards Compatibility)
- [ ] Unbekannte Felder werden ignoriert (Forwards Compatibility)
- [ ] Validation: Identifier-Format, Semver-Format
- [ ] `PluginManifest` Dataclass enthält alle v2 Felder
- [ ] `PluginMetadata.from_loader_manifest()` bildet v2 Felder korrekt ab

### AC-3: API Version Gate

- [ ] API-Version-Prüfung erfolgt auf Manifest-Ebene VOR Code-Import
- [ ] `ApiVersion.is_compatible_with()` wird für Kompatibilitätsprüfung verwendet
- [ ] Inkompatible Plugins werden vor Runtime abgelehnt
- [ ] Fehlermeldung enthält erwartete und deklarierte Version

### AC-4: Permission Model (ADR-006)

- [ ] ADR-006 ist akzeptiert vor Implementierung
- [ ] Plugins deklarieren benötigte Capabilities im Manifest
- [ ] Host validiert deklarierte Capabilities bei Admission
- [ ] Nicht-deklarierte Capabilities werden zur Laufzeit gemäß der Default-Policy aus ADR-006 verweigert
- [ ] `PermissionCheck` und `ServicePermissionCheck` sind mit Host-Enforcement verbunden
- [ ] Permission-Semantik entspricht dem akzeptierten ADR-006

### AC-5: Dependency Resolution (ADR-007)

- [ ] ADR-007 ist akzeptiert vor Implementierung
- [ ] Dependency Graph wird aus Manifest v2 `dependencies.requires` konstruiert
- [ ] Topologische Sortierung bestimmt Activation-Reihenfolge
- [ ] Zyklische Abhängigkeiten werden erkannt und abgelehnt
- [ ] Version-Constraints (`minimum_version`) werden geprüft
- [ ] Fehlende Required Dependencies führen zur Ablehnung des abhängigen Plugins
- [ ] Dependency-Semantik entspricht dem akzeptierten ADR-007

### AC-6: Activation Validation

- [ ] Konsolidierter Validierungsschritt vor Code-Import
- [ ] Prüft: Manifest-Schema, API Version, Permissions, Dependencies
- [ ] Code-Import erfolgt NUR für validierte Plugins
- [ ] Nach Code-Import: Plugin-Subclass-Prüfung
- [ ] Binäre Accept/Reject-Entscheidung mit diagnostischem Report
- [ ] Abgelehnte Plugins brechen die Anwendung nicht ab

### AC-7: Golden Reference Plugin

- [ ] Plugin in `plugins/reference/` vorhanden
- [ ] Manifest v2 `plugin.toml` mit allen Feldern
- [ ] Nutzt Permissions, Dependencies, API Version deklarativ
- [ ] Vollständiger Lifecycle erfolgreich: Discovery → Security → Activation → Runtime → Shutdown
- [ ] Plugin dient als SDK Compatibility, Regression und Integration Verification
- [ ] Release Gate: Lifecycle-Fehlschlag blockiert Release

### AC-8: Observability

- [ ] Activation Duration Metrics pro Plugin verfügbar
- [ ] Dependency Resolution Time messbar
- [ ] Security Validation Time messbar
- [ ] Plugin Health Check implementiert (HealthCheck Protocol)
- [ ] Failure Diagnostics mit strukturierter Fehlerursache

### AC-9: Integrity Validation (ADR-005)

- [ ] ADR-005 ist akzeptiert vor Implementierung
- [ ] Integrity Policy definiert, was validiert wird
- [ ] Trust-Semantik nutzt bestehenden `PluginTrustLevel` Enum
- [ ] Plugins, die Integrity-Prüfung nicht bestehen, werden vor Activation abgelehnt
- [ ] `SignatureStatus` Enum wird als Datenstruktur genutzt
- [ ] Integrity-Modell ist ohne kryptographisches Enforcement definierbar und testbar (Checksum-Stufe genügt als erste Implementierung)
- [ ] Integrity-Semantik entspricht dem akzeptierten ADR-005

### AC-10: Version

- [ ] `pyproject.toml` → `version = "0.9.0"`
- [ ] `sdk/version.py` → `SDK_VERSION = "0.9.0"`
- [ ] `config/default.toml` → `version = "0.9.0"`
- [ ] `SDK_API_VERSION` bleibt `"1.0.0"`

### AC-11: Backwards Compatibility

- [ ] SDK API bleibt bei 1.0.0
- [ ] Bestehende `PluginPermission` Enum nicht entfernt
- [ ] Bestehende `PluginMetadata` Felder nicht entfernt
- [ ] Bestehende Plugin Base Classes unverändert
- [ ] Bestehende `PluginRuntime` API unverändert

---

## 9. Test Strategy

### Unit Tests

| Test | Datei | Beschreibung | AC |
|---|---|---|---|
| `test_capability_identifiers` | `tests/test_capability_matrix.py` | Capability-Identifikatoren sind definiert und stabile Strings | AC-1 |
| `test_capability_default_deny` | `tests/test_capability_matrix.py` | Nicht-gewährte Capabilities werden abgelehnt | AC-1 |
| `test_manifest_v2_parse_full` | `tests/test_manifest_v2.py` | Vollständiges v2 Manifest wird korrekt geparst | AC-2 |
| `test_manifest_v2_parse_minimal` | `tests/test_manifest_v2.py` | Minimales v1 Manifest wird weiterhin korrekt geparst | AC-2 |
| `test_manifest_v2_unknown_fields` | `tests/test_manifest_v2.py` | Unbekannte Felder werden ignoriert | AC-2 |
| `test_manifest_v2_validation_errors` | `tests/test_manifest_v2.py` | Ungültige Identifier/Versionen werden erkannt | AC-2 |
| `test_api_version_gate_compatible` | `tests/test_activation_validation.py` | Kompatible API-Version → Plugin zugelassen | AC-3 |
| `test_api_version_gate_incompatible` | `tests/test_activation_validation.py` | Inkompatible API-Version → Plugin vor Code-Import abgelehnt | AC-3 |
| `test_permission_enforcement_granted` | `tests/test_activation_validation.py` | Deklarierte Capability → Zugriff gewährt | AC-4 |
| `test_permission_enforcement_denied` | `tests/test_activation_validation.py` | Nicht-deklarierte Capability → Zugriff verweigert | AC-4 |
| `test_dependency_graph_ordering` | `tests/test_dependency_resolution.py` | Topologische Sortierung korrekt | AC-5 |
| `test_dependency_cycle_detection` | `tests/test_dependency_resolution.py` | Zyklische Abhängigkeit → Ablehnung | AC-5 |
| `test_dependency_version_constraint` | `tests/test_dependency_resolution.py` | Version-Constraint nicht erfüllt → Ablehnung | AC-5 |
| `test_dependency_missing_required` | `tests/test_dependency_resolution.py` | Fehlende Dependency → Ablehnung | AC-5 |
| `test_activation_validation_accept` | `tests/test_activation_validation.py` | Valides Plugin → Accept | AC-6 |
| `test_activation_validation_reject` | `tests/test_activation_validation.py` | Invalides Plugin → Reject mit Diagnostik | AC-6 |
| `test_plugin_health_check` | `tests/test_plugin_observability.py` | Plugin Health Check meldet korrekten Status | AC-8 |
| `test_activation_duration_metric` | `tests/test_plugin_observability.py` | Duration-Metric wird erfasst | AC-8 |

### Integration Tests

| Test | Datei | Beschreibung | AC |
|---|---|---|---|
| `test_golden_reference_full_lifecycle` | `tests/test_golden_reference.py` | Discovery → Security → Activation → Runtime → Shutdown des Golden Reference Plugin | AC-7 |
| `test_golden_reference_manifest_v2` | `tests/test_golden_reference.py` | Golden Reference Manifest v2 wird vollständig geparst | AC-2, AC-7 |
| `test_golden_reference_permissions` | `tests/test_golden_reference.py` | Permission-Deklaration wird korrekt validiert | AC-4, AC-7 |
| `test_multiple_plugins_dependency_order` | `tests/test_dependency_resolution.py` | Mehrere Plugins werden in Dependency-Reihenfolge aktiviert | AC-5 |
| `test_mixed_valid_invalid_plugins` | `tests/test_activation_validation.py` | Valide Plugins werden aktiviert, invalide abgelehnt; Anwendung startet | AC-6 |
| `test_backwards_compatibility_v1_manifest` | `tests/test_manifest_v2.py` | Plugin mit v1 Manifest funktioniert weiterhin | AC-11 |

### Test-Prinzipien

- Kein Qt-Event-Loop erforderlich (reine Host-/SDK-Logik)
- Plugin-Manifeste als TOML-Fixtures in `tests/fixtures/`
- `EventBus` als Spy für Event-Verifikation
- Deterministisch: keine externen Abhängigkeiten
- Jedes AC hat mindestens einen Test

---

## 10. Quality Gates

| Gate | Kriterium | Prüfung |
|---|---|---|
| **QG-1** | Alle bestehenden Tests grün | `python -m pytest -q` |
| **QG-2** | Alle neuen Tests grün | Alle Tests aus Abschnitt 9 |
| **QG-3** | ADR-006 APPROVED | ADR-Status in `docs/adr/006-*.md` |
| **QG-4** | ADR-007 APPROVED | ADR-Status in `docs/adr/007-*.md` |
| **QG-5** | ADR-005 APPROVED | ADR-Status in `docs/adr/005-*.md` |
| **QG-6** | SDK API Version unverändert (1.0.0) | `sdk/version.py` → `SDK_API_VERSION` |
| **QG-7** | Type Hints auf allen öffentlichen APIs | Alle neuen `__all__`-Einträge mit Type Hints |
| **QG-8** | Schichtmodell eingehalten | Keine Imports von äußeren Schichten in innere |
| **QG-9** | Architecture Book unverändert | `docs/architecture-book-v2.md` unmodifiziert |
| **QG-10** | Golden Reference Plugin Lifecycle erfolgreich | Full-Lifecycle-Test grün: Discovery → Security → Activation → Runtime → Shutdown |
| **QG-11** | Manifest v1 Backwards Compatibility | v1-Manifest-Test grün |
| **QG-12** | Kein Plugin-Code vor Validation importiert | Code-Import erfolgt erst nach Activation Validation |

---

## 11. Risks

| Risiko | Wahrscheinlichkeit | Auswirkung | Mitigation |
|---|---|---|---|
| ADR-006 Akzeptanz verzögert sich | Aufgelöst | — | ADR-006 APPROVED (2026-07-29) |
| ADR-007 Akzeptanz verzögert sich | Aufgelöst | — | ADR-007 APPROVED (2026-07-29) |
| Permission Model zu komplex | Niedrig | Implementierungsaufwand steigt | Minimal Viable Permissions: nur Capability-Grant, kein Fine-Grained RBAC |
| Manifest v2 bricht v1 Kompatibilität | Niedrig | Bestehende Plugins funktionieren nicht mehr | Alle neuen Felder optional; v1 Parser-Pfad bleibt erhalten |
| Dependency Cycles in Plugin-Ökosystem | Niedrig | Plugins nicht ladbar | Topologische Sortierung mit Cycle Detection (Algorithmus vergleichbar `ServiceRegistry`) |
| Golden Reference Plugin zu komplex | Niedrig | Test-Wartungsaufwand | Plugin nutzt nur stabile SDK-Features; keine Host-Internals |
| Integrity Validation ohne Krypto nicht aussagekräftig | Mittel | False sense of security | Explizit dokumentiert: Krypto-Enforcement deferred; Checksum als erste Stufe |
| Scope Creep durch drei parallele ADRs | Mittel | Milestone-Umfang wächst | Explicit Non-Goals dokumentiert; ADR-Scope durch Specification begrenzt |

---

## 12. Deliverables

| # | Deliverable | Datei(en) | AC |
|---|---|---|---|
| D-1 | Capability Matrix | `sdk/manifest.py` | AC-1 |
| D-2 | Manifest v2 TOML Parser | `plugins/loader.py`, `sdk/manifest.py` | AC-2 |
| D-3 | API Version Gate | `app/bootstrap.py` | AC-3 |
| D-4 | Permission Model Integration | `app/bootstrap.py`, `app/security/plugin_security.py`, `sdk/events.py`, `sdk/services.py` | AC-4 |
| D-5 | Dependency Resolution | `app/bootstrap.py` | AC-5 |
| D-6 | Activation Validation | `app/bootstrap.py` | AC-6 |
| D-7 | Golden Reference Plugin | `plugins/reference/plugin.toml`, `plugins/reference/__init__.py` | AC-7 |
| D-8 | Observability | `core/observability.py`, `app/bootstrap.py` | AC-8 |
| D-9 | Integrity Validation | `app/security/plugin_security.py`, `app/bootstrap.py` | AC-9 |
| D-10 | Version Bump | `pyproject.toml`, `sdk/version.py`, `config/default.toml` | AC-10 |
| D-11 | Unit Tests | `tests/test_capability_matrix.py`, `tests/test_manifest_v2.py`, `tests/test_activation_validation.py`, `tests/test_dependency_resolution.py`, `tests/test_plugin_observability.py` | AC-1–AC-8 |
| D-12 | Integration Tests | `tests/test_golden_reference.py`, `tests/test_dependency_resolution.py`, `tests/test_activation_validation.py`, `tests/test_manifest_v2.py` | AC-2, AC-4–AC-7, AC-11 |
| D-13 | ADR-006 (Accepted) | `docs/adr/006-plugin-permission-model.md` | AC-4 |
| D-14 | ADR-007 (Accepted) | `docs/adr/007-plugin-dependency-resolution.md` | AC-5 |
| D-15 | ADR-005 (Accepted) | `docs/adr/005-plugin-integrity-validation.md` | AC-9 |

---

## 13. Definition of Done

Milestone 0.9 gilt als abgeschlossen, wenn:

- [ ] Alle Acceptance Criteria (AC-1 bis AC-11) erfüllt
- [ ] Alle Quality Gates (QG-1 bis QG-12) bestanden
- [ ] ADR-005 akzeptiert und implementiert
- [ ] ADR-006 akzeptiert und implementiert
- [ ] ADR-007 akzeptiert und implementiert
- [ ] Golden Reference Plugin Lifecycle erfolgreich (Discovery → Security → Activation → Runtime → Shutdown)
- [ ] Alle bestehenden Tests weiterhin grün
- [ ] Alle neuen Tests grün
- [ ] SDK API Version unverändert (1.0.0)
- [ ] Manifest v1 Backwards Compatibility gewährleistet
- [ ] Architecture Book v2.0 unverändert
- [ ] Type Hints auf allen öffentlichen APIs
- [ ] `__all__` in jedem betroffenen Modul aktualisiert
- [ ] Keine unbegründeten TODOs
- [ ] Version `0.9.0` in `pyproject.toml`, `sdk/version.py`, `config/default.toml`
- [ ] Commit(s) thematisch sauber
- [ ] Independent Review durchgeführt (gemäß Development Standard v1.1 §9)
- [ ] Correction Report erstellt (falls Findings)
- [ ] Final Verification bestanden (gemäß Development Standard v1.1 §9.3)
- [ ] Git Tag `v0.9.0` gesetzt

---

## 14. Future Items

Die folgenden Arbeiten sind NICHT Bestandteil von Milestone 0.9:

### Deferred Items (Low Priority — Roadmap)

| Thema | Begründung | Roadmap-Referenz |
|---|---|---|
| Chat UI | Produkt-Feature; erfordert vollständigen Plugin-Contract | Low Priority |
| AI Gateway | Produkt-Feature; erfordert Chat UI | Low Priority |
| Plugin Store | Erfordert Integrity Validation und PKI | Low Priority |
| PKI Infrastructure | Kryptographisches Enforcement deferred; ADR-005 definiert nur das Modell | Low Priority |
| IPC | Erfordert Subprocess Isolation | Low Priority |
| Subprocess Isolation | Explicit Non-Goal per ADR-009/011 | Low Priority |

### Deferred Items (Medium Priority — Roadmap)

Die folgenden Roadmap-Items mit Medium Priority sind explizit NICHT in Milestone 0.9 integriert:

| Thema | Status | Begründung |
|---|---|---|
| SDK Compatibility Reports | Deferred | M0.9 liefert Golden Reference Plugin als primäres SDK-Compatibility-Artefakt; formale Reports sind separater Scope |
| Developer Diagnostics | Deferred | M0.9 liefert Failure Diagnostics (5.8) als Grundlage; erweiterte Developer Diagnostics sind separater Scope |
| Plugin Test Harness | Deferred | M0.9 liefert Golden Reference Plugin und Test Strategy; ein dediziertes Test-Harness-Framework ist separater Scope |

### Weitere Deferred Items

| Thema | Begründung |
|---|---|
| Hot-Reloading | Erfordert Unloading-Semantik (ADR-011 Non-goals) |
| UI Plugin Widget Hosting | Erfordert Layout-Manager-Integration |
| Service Exposure Expansion | Erfordert definiertes Permission-Modell (wird von M0.9 vorbereitet, aber Expansion ist separater Scope) |
| ServiceRegistry `replace()` API | Erfordert Architecture Book v2.1+ (Core Runtime API Freeze) |
| `SecurityBootstrapStage` Timing Cleanup | Known Technical Debt aus M0.8; nicht Scope von M0.9 |
| Fine-Grained RBAC | M0.9 implementiert Capability-Grant; fine-grained RBAC ist Future Work |
| Optional Dependencies Semantik | Wird in ADR-007 adressiert, aber Implementierung darf deferred werden |

---

## 15. Evidence Summary

| # | Aussage | Klassifikation | Referenz / Begründung |
|---|---|---|---|
| E-1 | `PluginMetadata` hat Felder `api_version`, `category`, `permissions`, `dependencies` | Verified Evidence | `sdk/manifest.py:170–178` |
| E-2 | `PluginPermission` Enum hat 10 Werte | Verified Evidence | `sdk/manifest.py:47–64` |
| E-3 | `PluginCategory` Enum hat 8 Werte | Verified Evidence | `sdk/manifest.py:34–43` |
| E-4 | `PluginDependency` hat `identifier` und `minimum_version` | Verified Evidence | `sdk/manifest.py:125–145` |
| E-5 | `PermissionCheck` ist ein Callable, kein Protocol | Verified Evidence | `sdk/events.py:83` — `Callable[[PluginPermission], None]` |
| E-6 | `ServicePermissionCheck` ist ein Callable, kein Protocol | Verified Evidence | `sdk/services.py:31` — `Callable[[type, PluginPermission], None]` |
| E-7 | `PermissionManager` implementiert RBAC mit `define_role`, `assign_role`, `has_permission`, `require` | Verified Evidence | `app/security/permission_manager.py:24–127` |
| E-8 | API-Version-Check in `PluginActivationStage` prüft nur Major-Version nach Code-Import | Verified Evidence | `app/bootstrap.py:411–416` |
| E-9 | Dependency-Resolution in `PluginActivationStage` ist flat Presence Check ohne Topologische Sortierung | Verified Evidence | `app/bootstrap.py:418–423` |
| E-10 | Keine `plugin.toml` Dateien im Repository vorhanden | Verified Evidence | Glob-Suche `**/plugin.toml` — keine Treffer |
| E-11 | `PluginManifest` (in `plugins/loader.py`) hat nur 3 Felder: `identifier`, `version`, `required_application_version` | Verified Evidence | `plugins/loader.py` |
| E-12 | `ServiceRegistry` hat Circular Dependency Detection via `_resolve` Trail | Verified Evidence | `core/registry.py:124–130` |
| E-13 | `Metrics` in `core/observability.py` bietet nur Counter-Increment | Verified Evidence | `core/observability.py:19–27` |
| E-14 | `Tracer` und `Span` sind Minimal-Stubs ohne Duration-Berechnung | Verified Evidence | `core/observability.py:30–37` |
| E-15 | `SignatureStatus` Enum existiert mit UNVERIFIED, VERIFIED, TRUSTED, REJECTED | Verified Evidence | `sdk/manifest.py:67–78` |
| E-16 | `PluginTrustLevel` Enum hat UNTRUSTED, VERIFIED, TRUSTED, REJECTED | Verified Evidence | `app/security/models.py:25–31` |
| E-17 | `ApiVersion.is_compatible_with()` existiert | Verified Evidence | `sdk/version.py:31–81` |
| E-18 | `PluginMetadata` hat kein `entry_point` Feld | Verified Evidence | `sdk/manifest.py:148–180` — Entry-Point wird dynamisch aufgelöst |
| E-19 | `PluginActivationStage` scannt Module dynamisch nach Plugin-Subclass | Verified Evidence | `app/bootstrap.py:393–403` |
| E-20 | Permission-Enforcement im SDK existiert als Callable-Slots, aber ohne Host-Anbindung | Inference | `PermissionCheck`/`ServicePermissionCheck` existieren als Type Aliases; keine Implementierung verbindet sie mit `PermissionManager`. Ableitung aus Code-Struktur. |
| E-21 | Capability Matrix als stabiles Vokabular ist realisierbar über bestehende `PluginPermission` Enum-Erweiterung | Inference | `PluginPermission` existiert als StrEnum; Erweiterung um Capability-Identifikatoren ist additiv und SDK-API-kompatibel. |
| E-22 | Topologische Sortierung für Plugin-Dependencies ist mit Algorithmus aus `ServiceRegistry` vergleichbar implementierbar | Inference | `ServiceRegistry._resolve` (core/registry.py:124–130) implementiert Trail-basierte Cycle Detection; gleicher Ansatz für Plugin-Graph anwendbar. |
| E-23 | Manifest v2 TOML Parser erfordert keine neuen Abhängigkeiten | Verified Evidence | `tomllib` ist stdlib seit Python 3.11; `plugins/loader.py` nutzt es bereits |
| E-24 | `config/default.toml` enthält `version = "0.8.0"` | Verified Evidence | `config/default.toml:3` |

---

## Appendix A: Traceability Matrix

| Roadmap Phase | Specification Section | Acceptance Criteria | Deliverable |
|---|---|---|---|
| Phase 0 — Governance Initialization | — | — | — (Governance artifact; covered by Development Standard v1.1) |
| Phase 1 — Engineering Specification | Document Control, §1–§15 | — | This document |
| Phase 3 — Capability Matrix | 5.1 | AC-1 | D-1 |
| Phase 4 — Manifest v2 | 5.2 | AC-2 | D-2 |
| Phase 5 — API Version Gate | 5.3 | AC-3 | D-3 |
| Phase 2 — ADR-006: Permission Model | 5.4 | AC-4 | D-4, D-13 |
| Phase 6 — ADR-007: Dependency Resolution | 5.5 | AC-5 | D-5, D-14 |
| Phase 7 — Activation Validation | 5.6 | AC-6 | D-6 |
| Phase 8 — Golden Reference Plugin | 5.7 | AC-7 | D-7 |
| Phase 9 — Observability | 5.8 | AC-8 | D-8 |
| Phase 10 — ADR-005: Integrity Validation | 5.9 | AC-9 | D-9, D-15 |
| Version Bump | 5.10 | AC-10 | D-10 |
| Phase 11 — Testing | 9 (Test Strategy) | AC-1–AC-8, AC-11 | D-11, D-12 |
| Phase 12 — Governance Completion | 13 (Definition of Done) | — | — |
| (Cross-cutting) | — | AC-11 | — |

## Appendix B: ADR Dependency Map

| ADR | Status | Blocks | Blocked By |
|---|---|---|---|
| ADR-006 | APPROVED | Capability Matrix (5.1), Permission Integration (5.4), Activation Validation (5.6) | — |
| ADR-007 | APPROVED | Dependency Integration (5.5), Activation Validation (5.6) | — |
| ADR-005 | APPROVED | Integrity Integration (5.9) | — |

## Appendix C: Explicit Non-Goals

| Non-Goal | Begründung |
|---|---|
| Chat UI | Produkt-Feature, nicht Contract |
| AI Gateway | Produkt-Feature, nicht Contract |
| Large UI Work | Produkt-Feature, nicht Contract |
| Architecture Redesign | Architecture Book v2.0 bleibt FROZEN |
| Subprocess Isolation | Explicit Non-Goal per ADR-009/011 |
| Plugin Store | Requires Contract Hardening first |
| PKI Infrastructure | Kryptographisches Enforcement deferred |
| IPC | Requires Subprocess Isolation |
| ServiceRegistry `replace()` API | Requires Architecture Book v2.1+ |

## Appendix D: Version Targets

| Artefakt | Baseline (v0.8.0) | Ziel (v0.9.0) | Änderungstyp |
|---|---|---|---|
| Application | 0.8.0 | 0.9.0 | Minor (additive) |
| SDK | 0.8.0 | 0.9.0 | Minor (additive) |
| SDK API | 1.0.0 | 1.0.0 | Keine Änderung |
