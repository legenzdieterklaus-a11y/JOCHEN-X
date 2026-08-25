# Milestone 0.9 — Implementation Plan

## Document Control

| Eigenschaft | Wert |
|---|---|
| **Titel** | Milestone 0.9 Implementation Plan |
| **Status** | APPROVED |
| **Version** | 1.1 |
| **Datum** | 2026-07-30 |
| **Specification** | [Engineering Specification v0.9.1](milestone-0.9-engineering-spec.md) (APPROVED) |
| **Architecture** | [Architecture Book v2.0](architecture-book-v2.md) (FROZEN) |
| **Development Standard** | [v1.1](development-standard-v1.1.md) |
| **ADRs** | ADR-005 (APPROVED), ADR-006 (APPROVED), ADR-007 (APPROVED) |
| **Baseline** | Release Tag `v0.8.0` |

---

## Governance Confirmation

### Architecture Freeze

Die Architektur ist eingefroren. Die folgenden Dokumente sind autoritativ:

- Architecture Book v2.0 (FROZEN)
- Development Standard v1.1 (APPROVED)
- Engineering Specification v0.9.1 (APPROVED)
- ADR-001, ADR-005, ADR-006, ADR-007, ADR-010, ADR-011

Dieser Implementierungsplan führt keine neuen Anforderungen ein, ändert keine Architektur und definiert keine neuen Akzeptanzkriterien. Jedes Arbeitspaket ist direkt auf die Engineering Specification rückverfolgbar.

### ADR Status

| ADR | Status | Datum |
|---|---|---|
| ADR-005 (Integrity Validation) | APPROVED | 2026-07-30 |
| ADR-006 (Permission Model) | APPROVED | 2026-07-29 |
| ADR-007 (Dependency Resolution) | APPROVED | 2026-07-29 |

Alle ADRs sind genehmigt. Keine ADR-bezogenen Arbeitspakete erforderlich.

---

## 1. Milestone Overview

**Milestone 0.9 — Plugin Contract Hardening**

Milestone 0.8 hat die Host-Integration etabliert (Discovery → Security → Activation → Shutdown). Der Plugin-Contract ist jedoch unvollständig: kein Permission-Modell, keine Capability-Abstraktion, minimales Manifest-Schema, keine Dependency-Resolution, keine Integrity-Validation, kein API-Version-Gate auf Manifest-Ebene, kein Reference Plugin.

Milestone 0.9 adressiert diese Lücken in elf Arbeitspaketen. SDK API bleibt bei 1.0.0 — alle Änderungen sind additiv.

**Ziel:** Vollständiger, gehärteter Plugin-Contract als Voraussetzung für produktorientierte Features.

**Scope:** Engineering Specification v0.9.1, Abschnitte 5.1–5.10, Abschnitt 7, AC-1 bis AC-11, QG-1 bis QG-12.

---

## 2. Implementation Phases

```
Phase A — Foundations (WP-01, WP-02)
    Capability Matrix, Manifest v2 TOML Parser

Phase B — Security & Resolution (WP-03, WP-04, WP-05, WP-06)
    API Version Gate, Integrity, Permissions, Dependencies

Phase C — Consolidation (WP-07, WP-08, WP-09)
    Activation Validation, Golden Reference Plugin, Observability

Phase D — Release (WP-10, WP-11)
    Version Bump, Testing & Release Gates
```

---

## 3. Work Breakdown Structure

### WP-01: Capability Matrix

| Eigenschaft | Wert |
|---|---|
| **Package ID** | WP-01 |
| **Package Name** | Capability Matrix |
| **Purpose** | Stabile Capability-Identifikatoren als Contract-Vokabular definieren |
| **Specification Sections** | §5.1 |
| **Architecture Book References** | §10.5 (Berechtigungen), §11.1 (Permission Model) |
| **Required ADRs** | ADR-006 (APPROVED) — definiert Permission-Semantik, die Capabilities referenziert |
| **Acceptance Criteria** | AC-1 |
| **Quality Gates** | QG-7 (Type Hints), QG-8 (Schichtmodell) |
| **Inputs** | Bestehender `PluginPermission` Enum (10 Werte, `sdk/manifest.py:47–64`) |
| **Outputs** | Capability-Identifikatoren als stabile String-Konstanten, Mapping zu `PluginPermission` |
| **Affected Modules** | SDK |
| **Planned Affected Files** | `sdk/manifest.py` |
| **Dependencies** | Keine |
| **Estimated Complexity** | Niedrig |
| **Estimated Test Effort** | Niedrig — 2 Unit Tests (`tests/test_capability_matrix.py`) |
| **Verification Method** | Unit Tests: `test_capability_identifiers`, `test_capability_default_deny` |
| **Definition of Done** | AC-1 erfüllt, 10 Capability-Identifikatoren definiert, Mapping dokumentiert, Tests grün |

---

### WP-02: Manifest v2 TOML Parser

| Eigenschaft | Wert |
|---|---|
| **Package ID** | WP-02 |
| **Package Name** | Manifest v2 TOML Parser |
| **Purpose** | Erweitertes `plugin.toml` Schema und Parser für alle v2 Felder |
| **Specification Sections** | §5.2 |
| **Architecture Book References** | §5.4 (Plugins Schicht), §6.6 (PluginLoader), §10.1 (Registry/Discovery), §23 (PluginManifest: 3-Feld Value Type) |
| **Required ADRs** | ADR-006 (APPROVED) — Permissions in Manifest; ADR-007 (APPROVED) — Dependencies in Manifest |
| **Acceptance Criteria** | AC-2 |
| **Quality Gates** | QG-7, QG-8, QG-11 (Manifest v1 Backwards Compatibility) |
| **Inputs** | Bestehender `PluginManifest` (3 Felder: `identifier`, `version`, `required_application_version`), `PluginMetadata` (11 Felder) |
| **Outputs** | Erweiterter `PluginManifest` mit v2 Feldern, erweiterter `PluginLoader` Parser, `PluginMetadata.from_loader_manifest()` Erweiterung |
| **Affected Modules** | Plugins, SDK |
| **Planned Affected Files** | `plugins/loader.py`, `sdk/manifest.py` |
| **Dependencies** | WP-01 (Capability Matrix) — Capability-Identifikatoren für `permissions.capabilities` |
| **Estimated Complexity** | Mittel |
| **Estimated Test Effort** | Mittel — 4 Unit Tests, 1 Integration Test (`tests/test_manifest_v2.py`) |
| **Verification Method** | Unit Tests: `test_manifest_v2_parse_full`, `test_manifest_v2_parse_minimal`, `test_manifest_v2_unknown_fields`, `test_manifest_v2_validation_errors`; Integration Test: `test_backwards_compatibility_v1_manifest` |
| **Definition of Done** | AC-2 erfüllt, alle v2 Felder geparst, v1 Backwards Compatibility gewährleistet, Tests grün |

---

### WP-03: API Version Gate

| Eigenschaft | Wert |
|---|---|
| **Package ID** | WP-03 |
| **Package Name** | API Version Gate |
| **Purpose** | API-Version-Prüfung auf Manifest-Ebene VOR Code-Import |
| **Specification Sections** | §5.3 |
| **Architecture Book References** | §7.2 (Bootstrap), §22.4 (Versionierungsstrategie) |
| **Required ADRs** | Keine direkt; nutzt `ApiVersion.is_compatible_with()` (Verified Evidence E-17) |
| **Acceptance Criteria** | AC-3 |
| **Quality Gates** | QG-12 (Kein Plugin-Code vor Validation importiert) |
| **Inputs** | `api_version` aus erweitertem `PluginManifest` (WP-02), `ApiVersion.is_compatible_with()` (`sdk/version.py:31–81`) |
| **Outputs** | Manifest-Level Kompatibilitätsprüfung in `PluginActivationStage` |
| **Affected Modules** | App |
| **Planned Affected Files** | `app/bootstrap.py` |
| **Dependencies** | WP-02 (Manifest v2) — liefert `api_version` Feld |
| **Estimated Complexity** | Niedrig |
| **Estimated Test Effort** | Niedrig — 2 Unit Tests (`tests/test_activation_validation.py`) |
| **Verification Method** | Unit Tests: `test_api_version_gate_compatible`, `test_api_version_gate_incompatible` |
| **Definition of Done** | AC-3 erfüllt, Prüfung vor Code-Import, Diagnostik bei Inkompatibilität, Tests grün |

---

### WP-04: Integrity Integration

| Eigenschaft | Wert |
|---|---|
| **Package ID** | WP-04 |
| **Package Name** | Integrity Validation Integration |
| **Purpose** | Integrity-Modell und Policy-driven Validation gemäß ADR-005 |
| **Specification Sections** | §5.9 |
| **Architecture Book References** | §11.3 (PluginSecurity/Trust Ledger), §11.4 (Trust Boundaries), §11.5 (Plugin Security) |
| **Required ADRs** | ADR-005 (APPROVED) — D1–D8: Purpose, Policy, Trust Determination, Signature Status, Validation Boundary, Failure Semantics, Audit, Separation |
| **Acceptance Criteria** | AC-9 |
| **Quality Gates** | QG-5 (ADR-005 APPROVED), QG-12 |
| **Inputs** | `PluginSecurity` Trust Ledger (`app/security/plugin_security.py:45–131`), `PluginTrustLevel` Enum (`app/security/models.py:25–31`), `SignatureStatus` Enum (`sdk/manifest.py:67–78`) |
| **Outputs** | Integrity Policy (TOML-config-driven), Integrity Validation in `PluginSecurityStage`, Trust Determination Logik |
| **Affected Modules** | App (Security) |
| **Planned Affected Files** | `app/security/plugin_security.py`, `app/bootstrap.py` |
| **Dependencies** | Keine architektonische Abhängigkeit zu WP-03/WP-05/WP-06 (ADR-005 ist APPROVED, Spec definiert Verhalten). Implementierungs-Integrations­abhängigkeit: Integrity Validation wird in die konsolidierte Bootstrap/Security-Pipeline (WP-07) integriert. |
| **Estimated Complexity** | Mittel |
| **Estimated Test Effort** | Mittel — Integrity-Tests in bestehenden Security-Tests integriert |
| **Verification Method** | Tests: Integrity-Policy-Auswertung, Trust-Level-Transitions, SignatureStatus-Nutzung |
| **Definition of Done** | AC-9 erfüllt, Integrity Policy definiert, Trust-Semantik nutzt `PluginTrustLevel`, `SignatureStatus` genutzt, ohne Krypto testbar, Tests grün |

---

### WP-05: Permission Integration

| Eigenschaft | Wert |
|---|---|
| **Package ID** | WP-05 |
| **Package Name** | Permission Model Integration |
| **Purpose** | Host-seitiges Permission Enforcement gemäß ADR-006 |
| **Specification Sections** | §5.4 |
| **Architecture Book References** | §10.5 (Berechtigungen), §11.1 (Permission Model), §6.5 (SecurityManager) |
| **Required ADRs** | ADR-006 (APPROVED) — D1–D6: Default-Deny, Three-State Resolution, Admission-Time Validation, Runtime Enforcement, Policy Source, Audit |
| **Acceptance Criteria** | AC-4 |
| **Quality Gates** | QG-3 (ADR-006 APPROVED), QG-8, QG-12 |
| **Inputs** | `PermissionManager` (`app/security/permission_manager.py:24–127`), `PermissionCheck` Callable (`sdk/events.py:83`), `ServicePermissionCheck` Callable (`sdk/services.py:31`), Capability-Identifikatoren (WP-01) |
| **Outputs** | Permission-Validation in `PluginSecurityStage`, Host-Anbindung der SDK Permission-Callables, Configuration-driven Permission Policy |
| **Affected Modules** | App, SDK (Anbindung) |
| **Planned Affected Files** | `app/bootstrap.py`, `app/security/plugin_security.py`, `sdk/events.py`, `sdk/services.py` |
| **Dependencies** | WP-01 (Capability Matrix) — Capability-Identifikatoren |
| **Estimated Complexity** | Hoch |
| **Estimated Test Effort** | Mittel — 2 Unit Tests (`tests/test_activation_validation.py`) |
| **Verification Method** | Unit Tests: `test_permission_enforcement_granted`, `test_permission_enforcement_denied`; Integration Test: `test_golden_reference_permissions` |
| **Definition of Done** | AC-4 erfüllt, Default-Deny Policy, Admission-Time Validation, SDK-Callables verbunden, Tests grün |

---

### WP-06: Dependency Integration

| Eigenschaft | Wert |
|---|---|
| **Package ID** | WP-06 |
| **Package Name** | Dependency Resolution Integration |
| **Purpose** | Dependency Graph, topologische Sortierung und Cycle Detection gemäß ADR-007 |
| **Specification Sections** | §5.5 |
| **Architecture Book References** | §8 (DI — Circular Dependency Detection Pattern), §10 (Plugin-System) |
| **Required ADRs** | ADR-007 (APPROVED) — D1–D8: Declaration, Resolution Semantics, Version Compatibility, Graph Semantics, Resolution Boundary, Activation Guarantees, Invariants, Separation |
| **Acceptance Criteria** | AC-5 |
| **Quality Gates** | QG-4 (ADR-007 APPROVED), QG-8, QG-12 |
| **Inputs** | `dependencies.requires` aus Manifest v2 (WP-02), `PluginDependency` Dataclass (`sdk/manifest.py:125–145`), `ServiceRegistry` Cycle Detection Pattern (`core/registry.py:124–130`) |
| **Outputs** | Dependency Graph Construction, topologische Sortierung, Cycle Detection, Version-Constraint-Prüfung, Dependency-geordnete Activation |
| **Affected Modules** | App |
| **Planned Affected Files** | `app/bootstrap.py` |
| **Dependencies** | WP-02 (Manifest v2) — liefert `dependencies.requires` Feld |
| **Estimated Complexity** | Hoch |
| **Estimated Test Effort** | Hoch — 4 Unit Tests, 1 Integration Test (`tests/test_dependency_resolution.py`) |
| **Verification Method** | Unit Tests: `test_dependency_graph_ordering`, `test_dependency_cycle_detection`, `test_dependency_version_constraint`, `test_dependency_missing_required`; Integration Test: `test_multiple_plugins_dependency_order` |
| **Definition of Done** | AC-5 erfüllt, Topologische Sortierung, Cycle Detection, Version-Constraints, Tests grün |

---

### WP-07: Activation Validation

| Eigenschaft | Wert |
|---|---|
| **Package ID** | WP-07 |
| **Package Name** | Activation Validation |
| **Purpose** | Konsolidierter Validierungsschritt VOR Code-Import |
| **Specification Sections** | §5.6 |
| **Architecture Book References** | §7.2 (Bootstrap), §10.4 (Isolation — Code-Import erst in FINALIZE) |
| **Required ADRs** | ADR-005, ADR-006, ADR-007 (alle APPROVED) — definieren die einzelnen Validierungsschritte |
| **Acceptance Criteria** | AC-6 |
| **Quality Gates** | QG-12 (Kein Plugin-Code vor Validation importiert) |
| **Inputs** | API Version Gate (WP-03), Permission Validation (WP-05), Dependency Validation (WP-06), Integrity Validation (WP-04) |
| **Outputs** | Konsolidierte Accept/Reject-Entscheidung mit diagnostischem Report, Code-Import NUR für validierte Plugins |
| **Affected Modules** | App |
| **Planned Affected Files** | `app/bootstrap.py` |
| **Dependencies** | WP-03 (API Version Gate), WP-04 (Integrity), WP-05 (Permissions), WP-06 (Dependencies) |
| **Estimated Complexity** | Mittel |
| **Estimated Test Effort** | Mittel — 2 Unit Tests, 1 Integration Test (`tests/test_activation_validation.py`) |
| **Verification Method** | Unit Tests: `test_activation_validation_accept`, `test_activation_validation_reject`; Integration Test: `test_mixed_valid_invalid_plugins` |
| **Definition of Done** | AC-6 erfüllt, konsolidierter Validierungsschritt, binäre Accept/Reject, abgelehnte Plugins brechen Anwendung nicht ab, Tests grün |

---

### WP-08: Golden Reference Plugin

| Eigenschaft | Wert |
|---|---|
| **Package ID** | WP-08 |
| **Package Name** | Golden Reference Plugin |
| **Purpose** | Governance-Artefakt zur end-to-end Validierung des Plugin-Contract |
| **Specification Sections** | §5.7 |
| **Architecture Book References** | §10 (Plugin-System), §19.2 (Plugin erstellen) |
| **Required ADRs** | Alle genehmigten ADRs — Plugin validiert den vollständigen Contract |
| **Acceptance Criteria** | AC-7 |
| **Quality Gates** | QG-10 (Golden Reference Plugin Lifecycle erfolgreich) |
| **Inputs** | Activation Validation (WP-07) — Plugin validiert den finalisierten Contract |
| **Outputs** | `plugins/reference/plugin.toml` (Manifest v2), `plugins/reference/__init__.py` (Implementation) |
| **Affected Modules** | Plugins (neu) |
| **Planned Affected Files** | `plugins/reference/plugin.toml` (neu), `plugins/reference/__init__.py` (neu) |
| **Dependencies** | WP-07 (Activation Validation) — Contract muss vollständig sein |
| **Estimated Complexity** | Mittel |
| **Estimated Test Effort** | Hoch — Full-Lifecycle Integration Test (`tests/test_golden_reference.py`) |
| **Verification Method** | Integration Tests: `test_golden_reference_full_lifecycle`, `test_golden_reference_manifest_v2`, `test_golden_reference_permissions` |
| **Definition of Done** | AC-7 erfüllt, Plugin in `plugins/reference/`, Manifest v2 vollständig, Full Lifecycle erfolgreich, Release Gate definiert, Tests grün |

---

### WP-09: Observability

| Eigenschaft | Wert |
|---|---|
| **Package ID** | WP-09 |
| **Package Name** | Observability |
| **Purpose** | Duration-Metrics, Plugin Health Checks und Failure Diagnostics |
| **Specification Sections** | §5.8 |
| **Architecture Book References** | §13 (Observability), §13.2 (Health), §13.3 (Metrics) |
| **Required ADRs** | Keine direkt |
| **Acceptance Criteria** | AC-8 |
| **Quality Gates** | QG-7, QG-8 |
| **Inputs** | Bestehende `Metrics` (Counter-only, `core/observability.py:19–27`), `HealthCheck` Protocol (`core/observability.py`), `Tracer`/`Span` Stubs (`core/observability.py:30–37`) |
| **Outputs** | Duration-Metrics pro Plugin, Plugin HealthCheck Implementation, Failure Diagnostics Datenstruktur |
| **Affected Modules** | Core, App |
| **Planned Affected Files** | `core/observability.py`, `app/bootstrap.py` |
| **Dependencies** | WP-07 (Activation Validation) — Observability misst die Validierungsschritte; WP-08 (Golden Reference Plugin) — Validierungsabhängigkeit (Observability wird gegen Reference Plugin validiert) |
| **Estimated Complexity** | Mittel |
| **Estimated Test Effort** | Niedrig — 2 Unit Tests (`tests/test_plugin_observability.py`) |
| **Verification Method** | Unit Tests: `test_plugin_health_check`, `test_activation_duration_metric` |
| **Definition of Done** | AC-8 erfüllt, Duration-Metrics, HealthCheck Protocol, Failure Diagnostics, Tests grün |

---

### WP-10: Version Bump

| Eigenschaft | Wert |
|---|---|
| **Package ID** | WP-10 |
| **Package Name** | Version Bump |
| **Purpose** | Versionsnummern auf 0.9.0 aktualisieren |
| **Specification Sections** | §5.10 |
| **Architecture Book References** | §22.4 (Versionierungsstrategie) |
| **Required ADRs** | Keine |
| **Acceptance Criteria** | AC-10 |
| **Quality Gates** | QG-6 (SDK API Version unverändert) |
| **Inputs** | Alle vorherigen WPs abgeschlossen |
| **Outputs** | Version `0.9.0` in drei Dateien, SDK_API_VERSION bleibt `1.0.0` |
| **Affected Modules** | Config, SDK, Projekt-Root |
| **Planned Affected Files** | `pyproject.toml`, `sdk/version.py`, `config/default.toml` |
| **Dependencies** | WP-04, WP-05, WP-06, WP-07, WP-08, WP-09 (alle Implementierungen abgeschlossen) |
| **Estimated Complexity** | Trivial |
| **Estimated Test Effort** | Trivial — Version-Assertions in bestehenden Tests |
| **Verification Method** | Manuelle Prüfung der drei Dateien |
| **Definition of Done** | AC-10 erfüllt, drei Dateien aktualisiert, SDK_API_VERSION `1.0.0`, Tests grün |

---

### WP-11: Testing & Release Gates

| Eigenschaft | Wert |
|---|---|
| **Package ID** | WP-11 |
| **Package Name** | Testing & Release Gates |
| **Purpose** | Alle Testsuiten, Quality Gates und Release-Verifikation |
| **Specification Sections** | §7 (Implementation Sequence), §9 (Test Strategy), §10 (Quality Gates) |
| **Architecture Book References** | §18 (Testarchitektur) |
| **Required ADRs** | Keine |
| **Acceptance Criteria** | AC-1 bis AC-11 |
| **Quality Gates** | QG-1 bis QG-12 |
| **Inputs** | Alle WPs abgeschlossen |
| **Outputs** | Alle Tests grün, alle Quality Gates bestanden, Release-Bereitschaft |
| **Affected Modules** | Tests |
| **Planned Affected Files** | `tests/test_capability_matrix.py` (neu), `tests/test_manifest_v2.py` (neu), `tests/test_activation_validation.py` (neu), `tests/test_golden_reference.py` (neu), `tests/test_dependency_resolution.py` (neu), `tests/test_plugin_observability.py` (neu) |
| **Dependencies** | WP-01 bis WP-10 |
| **Estimated Complexity** | Hoch (Gesamtumfang) |
| **Estimated Test Effort** | Hoch — 16 Unit Tests, 6 Integration Tests |
| **Verification Method** | `python -m pytest -q` — kompletter Testlauf |
| **Definition of Done** | Alle AC erfüllt, alle QG bestanden, Definition of Done (Spec §13) vollständig |

---

## 4. Implementation Sequence

### Build Order (Implementierungsreihenfolge)

```
S-1:  WP-01  Capability Matrix                [Phase A]
S-2:  WP-02  Manifest v2 TOML Parser          [Phase A]
S-3:  WP-03  API Version Gate                  [Phase B]
S-4:  WP-04  Integrity Integration             [Phase B]  ←── parallel zu S-3
S-5:  WP-05  Permission Integration            [Phase B]  ←── nach S-1
S-6:  WP-06  Dependency Integration            [Phase B]  ←── nach S-2
S-7:  WP-07  Activation Validation             [Phase C]  ←── nach S-3, S-4, S-5, S-6
S-8:  WP-08  Golden Reference Plugin           [Phase C]  ←── nach S-7
S-9:  WP-09  Observability                     [Phase C]  ←── parallel zu S-8
S-10: WP-10  Version Bump                      [Phase D]  ←── nach S-8, S-9
S-11: WP-11  Testing & Release Gates           [Phase D]  ←── nach S-10
```

### Build Order vs. Runtime Order

Die Build Order weicht bewusst von der Runtime Pipeline ab.

**Begründung:** Die Build Order priorisiert Dependency-freie Arbeitspakete zuerst (Capability Matrix, Manifest v2), um Parallelisierung innerhalb Phase B zu ermöglichen. Die Runtime Pipeline hingegen folgt der architektonisch definierten Ausführungsreihenfolge.

**ADR-Compliance:** Die Build Order verletzt keine Runtime-Semantik. Jedes Arbeitspaket wird so implementiert, dass es zur Runtime-Pipeline-Position korrekt funktioniert:

- WP-04 (Integrity) implementiert Validation an der korrekten Runtime-Position (nach Discovery, vor Permission Authorization) — gemäß ADR-005 D5
- WP-05 (Permissions) implementiert Validation an der korrekten Runtime-Position (nach Integrity, vor Dependency Resolution) — gemäß ADR-006 D3
- WP-06 (Dependencies) implementiert Resolution an der korrekten Runtime-Position (nach Permissions, vor Activation) — gemäß ADR-007 D5

---

## 5. Dependency Graph

```
                    WP-01 Capability Matrix
                    │
                    ▼
                    WP-02 Manifest v2 TOML Parser
                    │
          ┌─────────┼─────────┬──────────┐
          ▼         ▼         ▼          │
       WP-03     WP-05     WP-06        │
       API Gate  Permissions Dependencies │
          │         │         │          │
          │         │         │          │
          ▼         ▼         ▼          │
          └─────────┴─────────┘          │
                    │                    │
                    ▼                    │
              WP-07 Activation           │
              Validation                 │
                    │                    │
          ┌─────────┤                    │
          ▼         ▼                    │
       WP-08     WP-09                  │
       Golden    Observability           │
       Reference                        │
          │         │                    │
          └────┬────┘                    │
               ▼                        │
          WP-10 Version Bump             │
               │                        │
               ▼                        │
          WP-11 Testing &               │
          Release Gates                 │
                                        │
       WP-04 Integrity ─────────────────┘
       (parallel, keine
        Impl.-Abhängigkeit
        zu WP-02, aber
        Runtime-Integration
        in WP-07)
```

### Parallelisierungspotenzial

| Parallelisierung | Begründung |
|---|---|
| WP-05 + WP-06 parallel nach WP-02 | Permissions und Dependencies sind unabhängige Concerns mit unterschiedlichen Affected Files |
| WP-04 parallel zu WP-03/WP-05/WP-06 | Integrity hat keine Implementierungsabhängigkeit zu Manifest v2 (arbeitet auf bestehenden Trust Ledger Strukturen) |
| WP-08 + WP-09 parallel nach WP-07 | Golden Reference und Observability sind unabhängig; Observability-Validierung gegen Reference Plugin erfolgt nach Abschluss beider |

---

## 6. Runtime Pipeline

Die Runtime Pipeline folgt der genehmigten Architektur (ADR-005 D5, ADR-006 D3, ADR-007 D5):

```
┌──────────────────────────────────────────────────────────────────┐
│                        LOAD_PLUGINS Phase                        │
│                                                                  │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │  PluginDiscoveryStage                                    │    │
│  │  → Scannt plugins/*/plugin.toml                          │    │
│  │  → Parst Manifest v2 Felder (WP-02)                     │    │
│  │  → Erstellt PluginCatalog                                │    │
│  └────────────────────────┬────────────────────────────────┘    │
│                           ▼                                      │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │  PluginSecurityStage                                     │    │
│  │                                                          │    │
│  │  Step 1: Integrity Validation (WP-04 / ADR-005)         │    │
│  │     → Integrity Policy auswerten                         │    │
│  │     → Trust Determination: UNTRUSTED → VERIFIED/REJECTED │    │
│  │     → SignatureStatus setzen                             │    │
│  │     → Audit: security.integrity.verified / .rejected     │    │
│  │     → Output: Integrity-admitted Set                     │    │
│  │                                                          │    │
│  │  Step 2: Permission Authorization (WP-05 / ADR-006)     │    │
│  │     → Deklarierte Capabilities gegen Policy validieren    │    │
│  │     → Three-State Resolution: Granted/Denied/Undeclared  │    │
│  │     → Bei Denied: Plugin ablehnen                        │    │
│  │     → Audit: security.permission.granted / .denied       │    │
│  │     → Output: Admitted Set mit Granted Permissions       │    │
│  │                                                          │    │
│  │  Step 3: Dependency Resolution (WP-06 / ADR-007)        │    │
│  │     → Dependency Graph aus admitted Set konstruieren      │    │
│  │     → Topologische Sortierung                            │    │
│  │     → Cycle Detection                                    │    │
│  │     → Version-Constraint-Prüfung                         │    │
│  │     → Cascade Rejection bei Missing/Unresolved/Failed    │    │
│  │     → Output: Resolved Set mit Activation Order          │    │
│  └────────────────────────┬────────────────────────────────┘    │
└───────────────────────────┼──────────────────────────────────────┘
                            ▼
┌──────────────────────────────────────────────────────────────────┐
│                        FINALIZE Phase                             │
│                                                                  │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │  PluginActivationStage                                   │    │
│  │                                                          │    │
│  │  Pre-Import Validation (WP-07 — konsolidiert)           │    │
│  │     → Manifest-Schema-Validierung                        │    │
│  │     → API Version Gate (WP-03)                           │    │
│  │     → Permission-Validierung (verifiziert)               │    │
│  │     → Dependency-Validierung (verifiziert)               │    │
│  │     → Accept/Reject mit Diagnostik                       │    │
│  │                                                          │    │
│  │  Activation (nur für validierte Plugins)                 │    │
│  │     → Code-Import in Dependency-Reihenfolge              │    │
│  │     → Plugin-Subclass-Prüfung                            │    │
│  │     → PluginContext Construction                         │    │
│  │     → Permission-Callables binden (WP-05)                │    │
│  │     → Lifecycle: initialize() → start()                  │    │
│  │     → Observability: Duration Metrics (WP-09)            │    │
│  │     → Events: PLUGIN_ACTIVATING → PLUGIN_ACTIVATED       │    │
│  └────────────────────────┬────────────────────────────────┘    │
└───────────────────────────┼──────────────────────────────────────┘
                            ▼
                    READY State
```

---

## 7. Sprint Plan

### Sprint 1: Capability Matrix

| Eigenschaft | Wert |
|---|---|
| **Sprint ID** | SP-01 |
| **Objective** | Capability-Identifikatoren als stabile String-Konstanten definieren |
| **Work Package** | WP-01 |
| **Affected Files** | `sdk/manifest.py`, `tests/test_capability_matrix.py` (neu) |
| **Expected Deliverables** | D-1 (Capability Matrix), D-11 (Tests, anteilig) |
| **Dependencies** | Keine |
| **Definition of Done** | AC-1 erfüllt, Tests grün, `__all__` aktualisiert, Type Hints vollständig |

---

### Sprint 2: Manifest v2 TOML Parser

| Eigenschaft | Wert |
|---|---|
| **Sprint ID** | SP-02 |
| **Objective** | Erweitertes plugin.toml Schema und Parser implementieren |
| **Work Package** | WP-02 |
| **Affected Files** | `plugins/loader.py`, `sdk/manifest.py`, `tests/test_manifest_v2.py` (neu) |
| **Expected Deliverables** | D-2 (Manifest v2 Parser), D-11 (Tests, anteilig), D-12 (Integration Tests, anteilig) |
| **Dependencies** | SP-01 (Capability-Identifikatoren für `permissions.capabilities`) |
| **Definition of Done** | AC-2 erfüllt, v1 Backwards Compatibility (QG-11), Tests grün |

---

### Sprint 3: API Version Gate + Integrity Integration

| Eigenschaft | Wert |
|---|---|
| **Sprint ID** | SP-03 |
| **Objective** | API-Version-Prüfung auf Manifest-Ebene und Integrity-Modell implementieren |
| **Work Packages** | WP-03, WP-04 |
| **Affected Files** | `app/bootstrap.py`, `app/security/plugin_security.py`, `tests/test_activation_validation.py` (neu, anteilig) |
| **Expected Deliverables** | D-3 (API Version Gate), D-9 (Integrity Validation) |
| **Dependencies** | SP-02 (Manifest v2 liefert `api_version`) |
| **Definition of Done** | AC-3, AC-9 erfüllt, API-Version-Prüfung vor Code-Import, Integrity Policy definiert, Tests grün |

**Begründung für Kombination:** WP-03 und WP-04 betreffen beide `app/bootstrap.py` und werden in die konsolidierte Validation-Pipeline integriert. Die Kombination bleibt unter der 5-Dateien-Grenze.

---

### Sprint 4: Permission Integration

| Eigenschaft | Wert |
|---|---|
| **Sprint ID** | SP-04 |
| **Objective** | Host-seitiges Permission Enforcement implementieren |
| **Work Package** | WP-05 |
| **Affected Files** | `app/bootstrap.py`, `app/security/plugin_security.py`, `sdk/events.py`, `sdk/services.py` |
| **Expected Deliverables** | D-4 (Permission Model Integration) |
| **Dependencies** | SP-01 (Capability-Identifikatoren) |
| **Definition of Done** | AC-4 erfüllt, Default-Deny, SDK-Callables verbunden, Tests grün |

---

### Sprint 5: Dependency Integration

| Eigenschaft | Wert |
|---|---|
| **Sprint ID** | SP-05 |
| **Objective** | Dependency Graph, topologische Sortierung und Cycle Detection |
| **Work Package** | WP-06 |
| **Affected Files** | `app/bootstrap.py`, `tests/test_dependency_resolution.py` (neu) |
| **Expected Deliverables** | D-5 (Dependency Resolution) |
| **Dependencies** | SP-02 (Manifest v2 liefert `dependencies.requires`) |
| **Definition of Done** | AC-5 erfüllt, Topologische Sortierung, Cycle Detection, Version-Constraints, Tests grün |

**Parallelisierung:** SP-04 und SP-05 können parallel zu SP-03 durchgeführt werden, sofern die Dateikonflikte in `app/bootstrap.py` sequentiell aufgelöst werden.

---

### Sprint 6: Activation Validation

| Eigenschaft | Wert |
|---|---|
| **Sprint ID** | SP-06 |
| **Objective** | Konsolidierter Validierungsschritt vor Code-Import |
| **Work Package** | WP-07 |
| **Affected Files** | `app/bootstrap.py`, `tests/test_activation_validation.py` (Erweiterung) |
| **Expected Deliverables** | D-6 (Activation Validation) |
| **Dependencies** | SP-03, SP-04, SP-05 (alle Validierungskomponenten) |
| **Definition of Done** | AC-6 erfüllt, konsolidierter Validierungsschritt, binäre Accept/Reject, Tests grün |

---

### Sprint 7: Golden Reference Plugin + Observability

| Eigenschaft | Wert |
|---|---|
| **Sprint ID** | SP-07 |
| **Objective** | Governance-Artefakt und Plugin-Observability implementieren |
| **Work Packages** | WP-08, WP-09 |
| **Affected Files** | `plugins/reference/plugin.toml` (neu), `plugins/reference/__init__.py` (neu), `core/observability.py`, `tests/test_golden_reference.py` (neu), `tests/test_plugin_observability.py` (neu) |
| **Expected Deliverables** | D-7 (Golden Reference Plugin), D-8 (Observability) |
| **Dependencies** | SP-06 (Activation Validation) |
| **Definition of Done** | AC-7, AC-8 erfüllt, Full Lifecycle erfolgreich, Metrics verfügbar, Tests grün |

**Begründung für Kombination:** WP-08 und WP-09 können parallel implementiert werden (Spec §7, Parallelisierungspotenzial). Die Kombination bleibt unter der 5-Dateien-Grenze (5 Dateien, davon 4 neu).

**Planungshinweis:** Falls die Implementierungskomplexität den geplanten Umfang überschreitet, kann Sprint 7 in zwei Sub-Sprints aufgeteilt werden: **SP-07A** (Golden Reference Plugin, WP-08) und **SP-07B** (Observability, WP-09). Dies ist ausschließlich eine Kontingenzmaßnahme. Die geplante Implementierungsreihenfolge bleibt unverändert.

---

### Sprint 8: Version Bump + Release Gates

| Eigenschaft | Wert |
|---|---|
| **Sprint ID** | SP-08 |
| **Objective** | Version 0.9.0 setzen und alle Release Gates verifizieren |
| **Work Packages** | WP-10, WP-11 |
| **Affected Files** | `pyproject.toml`, `sdk/version.py`, `config/default.toml` |
| **Expected Deliverables** | D-10 (Version Bump), alle QG bestanden |
| **Dependencies** | SP-07 (alle Implementierungen abgeschlossen) |
| **Definition of Done** | AC-10 erfüllt, AC-11 (Backwards Compatibility) verifiziert, alle QG-1 bis QG-12 bestanden, kompletter Testlauf grün |

---

## 8. Testing Matrix

### Unit Tests

| Test | Datei | WP | AC | Beschreibung |
|---|---|---|---|---|
| `test_capability_identifiers` | `tests/test_capability_matrix.py` | WP-01 | AC-1 | 10 Capability-Identifikatoren definiert und stabile Strings |
| `test_capability_default_deny` | `tests/test_capability_matrix.py` | WP-01 | AC-1 | Nicht-gewährte Capabilities abgelehnt |
| `test_manifest_v2_parse_full` | `tests/test_manifest_v2.py` | WP-02 | AC-2 | Vollständiges v2 Manifest korrekt geparst |
| `test_manifest_v2_parse_minimal` | `tests/test_manifest_v2.py` | WP-02 | AC-2 | Minimales v1 Manifest weiterhin korrekt |
| `test_manifest_v2_unknown_fields` | `tests/test_manifest_v2.py` | WP-02 | AC-2 | Unbekannte Felder ignoriert |
| `test_manifest_v2_validation_errors` | `tests/test_manifest_v2.py` | WP-02 | AC-2 | Ungültige Identifier/Versionen erkannt |
| `test_api_version_gate_compatible` | `tests/test_activation_validation.py` | WP-03 | AC-3 | Kompatible API-Version → zugelassen |
| `test_api_version_gate_incompatible` | `tests/test_activation_validation.py` | WP-03 | AC-3 | Inkompatible API-Version → vor Code-Import abgelehnt |
| `test_permission_enforcement_granted` | `tests/test_activation_validation.py` | WP-05 | AC-4 | Deklarierte Capability → Zugriff gewährt |
| `test_permission_enforcement_denied` | `tests/test_activation_validation.py` | WP-05 | AC-4 | Nicht-deklarierte Capability → Zugriff verweigert |
| `test_dependency_graph_ordering` | `tests/test_dependency_resolution.py` | WP-06 | AC-5 | Topologische Sortierung korrekt |
| `test_dependency_cycle_detection` | `tests/test_dependency_resolution.py` | WP-06 | AC-5 | Zyklische Abhängigkeit → Ablehnung |
| `test_dependency_version_constraint` | `tests/test_dependency_resolution.py` | WP-06 | AC-5 | Version-Constraint nicht erfüllt → Ablehnung |
| `test_dependency_missing_required` | `tests/test_dependency_resolution.py` | WP-06 | AC-5 | Fehlende Dependency → Ablehnung |
| `test_activation_validation_accept` | `tests/test_activation_validation.py` | WP-07 | AC-6 | Valides Plugin → Accept |
| `test_activation_validation_reject` | `tests/test_activation_validation.py` | WP-07 | AC-6 | Invalides Plugin → Reject mit Diagnostik |
| `test_plugin_health_check` | `tests/test_plugin_observability.py` | WP-09 | AC-8 | Plugin Health Check meldet korrekten Status |
| `test_activation_duration_metric` | `tests/test_plugin_observability.py` | WP-09 | AC-8 | Duration-Metric wird erfasst |

### Integration Tests

| Test | Datei | WP | AC | Beschreibung |
|---|---|---|---|---|
| `test_golden_reference_full_lifecycle` | `tests/test_golden_reference.py` | WP-08 | AC-7 | Discovery → Security → Activation → Runtime → Shutdown |
| `test_golden_reference_manifest_v2` | `tests/test_golden_reference.py` | WP-08 | AC-2, AC-7 | Manifest v2 vollständig geparst |
| `test_golden_reference_permissions` | `tests/test_golden_reference.py` | WP-08 | AC-4, AC-7 | Permission-Deklaration korrekt validiert |
| `test_multiple_plugins_dependency_order` | `tests/test_dependency_resolution.py` | WP-06 | AC-5 | Mehrere Plugins in Dependency-Reihenfolge aktiviert |
| `test_mixed_valid_invalid_plugins` | `tests/test_activation_validation.py` | WP-07 | AC-6 | Valide aktiviert, invalide abgelehnt, Anwendung startet |
| `test_backwards_compatibility_v1_manifest` | `tests/test_manifest_v2.py` | WP-02 | AC-11 | Plugin mit v1 Manifest funktioniert weiterhin |

### Test Coverage Matrix

| AC | Unit Tests | Integration Tests | Abgedeckt |
|---|---|---|---|
| AC-1 | 2 | — | Ja |
| AC-2 | 4 | 2 | Ja |
| AC-3 | 2 | — | Ja |
| AC-4 | 2 | 1 | Ja |
| AC-5 | 4 | 1 | Ja |
| AC-6 | 2 | 1 | Ja |
| AC-7 | — | 3 | Ja |
| AC-8 | 2 | — | Ja |
| AC-9 | (in SP-03 Tests integriert) | — | Ja |
| AC-10 | (Version-Assertions) | — | Ja |
| AC-11 | — | 1 | Ja |

### Testprinzipien (gemäß Spec §9)

- Kein Qt-Event-Loop erforderlich (reine Host-/SDK-Logik)
- Plugin-Manifeste als TOML-Fixtures in `tests/fixtures/`
- `EventBus` als Spy für Event-Verifikation
- Deterministisch: keine externen Abhängigkeiten
- Jedes AC hat mindestens einen Test

---

## 9. Risk Register

### Implementation Risks

| # | Risiko | Wahrscheinlichkeit | Auswirkung | Mitigation |
|---|---|---|---|---|
| R-1 | Permission Model zu komplex für Sprint-Größe | Niedrig | Sprint-Überschreitung | Minimal Viable Permissions: nur Capability-Grant, kein Fine-Grained RBAC. SP-04 betrifft 4 Dateien — innerhalb der Grenze |
| R-2 | `app/bootstrap.py` Merge-Konflikte bei parallelen Sprints | Mittel | Integrationsverzögerung | SP-03/SP-04/SP-05 betreffen alle `app/bootstrap.py`. Sequentielle Sprints innerhalb der Datei; Parallelisierung nur bei unabhängigen Dateien |
| R-3 | Topologische Sortierung Edge Cases | Niedrig | Regression | Algorithmus vergleichbar `ServiceRegistry._resolve` (Verified Evidence E-22); umfangreiche Unit Tests |

### Integration Risks

| # | Risiko | Wahrscheinlichkeit | Auswirkung | Mitigation |
|---|---|---|---|---|
| R-4 | Manifest v2 bricht v1 Kompatibilität | Niedrig | Bestehende Plugins funktionieren nicht | Alle neuen Felder optional; v1 Parser-Pfad bleibt erhalten; Integration Test `test_backwards_compatibility_v1_manifest` |
| R-5 | Konsolidierte Validation-Pipeline zu restriktiv | Niedrig | Plugins fälschlich abgelehnt | Golden Reference Plugin (WP-08) als end-to-end Validierung; `test_mixed_valid_invalid_plugins` |

### Testing Risks

| # | Risiko | Wahrscheinlichkeit | Auswirkung | Mitigation |
|---|---|---|---|---|
| R-6 | Bestehende Tests brechen durch Bootstrap-Änderungen | Mittel | Regression | QG-1 (bestehende Tests grün) als Gate; inkrementelle Änderungen pro Sprint |
| R-7 | TOML-Fixtures unzureichend für Edge Cases | Niedrig | Ungetestete Pfade | Fixtures für: vollständig, minimal, fehlerhaft, unbekannte Felder |

### Dependency Risks

| # | Risiko | Wahrscheinlichkeit | Auswirkung | Mitigation |
|---|---|---|---|---|
| R-8 | WP-07 verzögert sich wegen Abhängigkeit auf 4 WPs | Mittel | Milestone-Verzögerung | Parallelisierung von SP-03/SP-04/SP-05 maximieren; WP-07 ist primär Konsolidierung, nicht Neuimplementierung |

### Governance Risks

| # | Risiko | Wahrscheinlichkeit | Auswirkung | Mitigation |
|---|---|---|---|---|
| R-9 | Scope Creep durch drei parallele Feature-Streams | Mittel | Milestone-Umfang wächst | Explicit Non-Goals (Spec §14); Sprint-Scope strikt an Specification gebunden |
| R-10 | Integrity Validation ohne Krypto bietet begrenzten Schutz | Mittel | False sense of security | Explizit dokumentiert: Krypto-Enforcement deferred (ADR-005 D2); Checksum als erste Stufe genügt (Spec §5.9 Explicit Deferral) |

---

## 10. Milestone Completion Checklist

### Governance

- [ ] Architecture Book v2.0 unverändert (QG-9)
- [ ] ADR-005 APPROVED und implementiert (QG-5)
- [ ] ADR-006 APPROVED und implementiert (QG-3)
- [ ] ADR-007 APPROVED und implementiert (QG-4)

### Acceptance Criteria

- [ ] AC-1: Capability Matrix — 10 stabile Identifikatoren, Default-Deny, Mapping dokumentiert
- [ ] AC-2: Manifest v2 — alle v2 Felder geparst, v1 Backwards Compatibility, Forwards Compatibility
- [ ] AC-3: API Version Gate — Manifest-Level Prüfung vor Code-Import, `is_compatible_with()`
- [ ] AC-4: Permission Model — Manifest-Deklaration, Admission Validation, Runtime Enforcement, SDK-Anbindung
- [ ] AC-5: Dependency Resolution — Graph, Topologische Sortierung, Cycle Detection, Version-Constraints
- [ ] AC-6: Activation Validation — konsolidiert, binäre Accept/Reject, abgelehnte Plugins nicht fatal
- [ ] AC-7: Golden Reference Plugin — Manifest v2, Full Lifecycle, Release Gate
- [ ] AC-8: Observability — Duration Metrics, HealthCheck, Failure Diagnostics
- [ ] AC-9: Integrity Validation — Policy definiert, `PluginTrustLevel`, `SignatureStatus`, ohne Krypto testbar
- [ ] AC-10: Version 0.9.0 in drei Dateien, SDK_API_VERSION 1.0.0
- [ ] AC-11: Backwards Compatibility — SDK API 1.0.0, bestehende Enums/Klassen unverändert

### Quality Gates

- [ ] QG-1: Alle bestehenden Tests grün
- [ ] QG-2: Alle neuen Tests grün
- [ ] QG-3: ADR-006 APPROVED
- [ ] QG-4: ADR-007 APPROVED
- [ ] QG-5: ADR-005 APPROVED
- [ ] QG-6: SDK API Version unverändert (1.0.0)
- [ ] QG-7: Type Hints auf allen öffentlichen APIs
- [ ] QG-8: Schichtmodell eingehalten
- [ ] QG-9: Architecture Book unverändert
- [ ] QG-10: Golden Reference Plugin Lifecycle erfolgreich
- [ ] QG-11: Manifest v1 Backwards Compatibility
- [ ] QG-12: Kein Plugin-Code vor Validation importiert

### Tests

- [ ] 18 Unit Tests grün (tests/test_capability_matrix.py, test_manifest_v2.py, test_activation_validation.py, test_dependency_resolution.py, test_plugin_observability.py)
- [ ] 6 Integration Tests grün (tests/test_golden_reference.py, test_dependency_resolution.py, test_activation_validation.py, test_manifest_v2.py)
- [ ] Bestehende Tests unverändert grün
- [ ] Kompletter Testlauf: `python -m pytest -q`

### Release

- [ ] `pyproject.toml` → `version = "0.9.0"`
- [ ] `sdk/version.py` → `SDK_VERSION = "0.9.0"`
- [ ] `config/default.toml` → `version = "0.9.0"`
- [ ] `SDK_API_VERSION` bleibt `"1.0.0"`
- [ ] `__all__` in jedem betroffenen Modul aktualisiert
- [ ] Type Hints auf allen öffentlichen APIs
- [ ] Keine unbegründeten TODOs
- [ ] Commit(s) thematisch sauber
- [ ] Git Tag `v0.9.0` gesetzt

### Governance Completion (gemäß Development Standard v1.1 §7)

- [ ] Independent Review durchgeführt (§9.2)
- [ ] Correction Report erstellt (falls Findings)
- [ ] Milestone Review durchgeführt (§9.6)
- [ ] Correction Sprint abgeschlossen (falls nötig)
- [ ] Final Verification bestanden (§9.3)

---

## Traceability

### Work Package → Specification → ADR → Architecture Book

| WP | Spec Section | AC | ADR | Architecture Book |
|---|---|---|---|---|
| WP-01 | §5.1 | AC-1 | ADR-006 | §10.5, §11.1 |
| WP-02 | §5.2 | AC-2 | ADR-006, ADR-007 | §5.4, §6.6, §10.1 |
| WP-03 | §5.3 | AC-3 | — | §7.2, §22.4 |
| WP-04 | §5.9 | AC-9 | ADR-005 | §11.3, §11.4, §11.5 |
| WP-05 | §5.4 | AC-4 | ADR-006 | §10.5, §11.1, §6.5 |
| WP-06 | §5.5 | AC-5 | ADR-007 | §8, §10 |
| WP-07 | §5.6 | AC-6 | ADR-005, ADR-006, ADR-007 | §7.2, §10.4 |
| WP-08 | §5.7 | AC-7 | alle | §10, §19.2 |
| WP-09 | §5.8 | AC-8 | — | §13 |
| WP-10 | §5.10 | AC-10 | — | §22.4 |
| WP-11 | §7, §9, §10 | AC-1–AC-11 | alle | §18 |

### Sprint → Work Package → Deliverable

| Sprint | Work Packages | Deliverables |
|---|---|---|
| SP-01 | WP-01 | D-1 |
| SP-02 | WP-02 | D-2 |
| SP-03 | WP-03, WP-04 | D-3, D-9 |
| SP-04 | WP-05 | D-4 |
| SP-05 | WP-06 | D-5 |
| SP-06 | WP-07 | D-6 |
| SP-07 | WP-08, WP-09 | D-7, D-8 |
| SP-08 | WP-10, WP-11 | D-10 |

---

## Approval Record

| Eigenschaft | Wert |
|---|---|
| **Approval Status** | APPROVED |
| **Approval Date** | 2026-07-30 |
| **Version Approved** | 1.1 |
| **Overall Result** | PASS |

### Governance Statement

Dieser Implementation Plan ist der autoritative Implementierungs-Masterplan für Milestone 0.9. Es gelten:

- Architecture Book v2.0 bleibt FROZEN — keine inhaltlichen Änderungen
- Engineering Specification v0.9.1 bleibt der Implementierungsvertrag
- ADR-005, ADR-006 und ADR-007 bleiben die maßgeblichen Architekturentscheidungen
- Die Implementierung beginnt mit Sprint SP-01

---

## Deferred Scope

Die folgenden Themen sind explizit NICHT Bestandteil dieses Plans (gemäß Spec §14):

- Chat UI, AI Gateway, Plugin Store, PKI Infrastructure
- IPC, Subprocess Isolation
- Hot-Reloading, UI Plugin Widget Hosting
- SDK Compatibility Reports, Developer Diagnostics, Plugin Test Harness
- Fine-Grained RBAC, Optional Dependencies Semantik
- ServiceRegistry `replace()` API
- `SecurityBootstrapStage` Timing Cleanup
