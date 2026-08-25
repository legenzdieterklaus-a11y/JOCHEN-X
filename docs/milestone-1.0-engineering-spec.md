# Milestone 1.0 Engineering Specification

## 1. Dokumentenkontrolle

| Eigenschaft | Wert |
|---|---|
| **Dokument-ID** | ES-1.0 |
| **Revision** | R1 — Contract Hardening |
| **Titel** | Platform Maturation |
| **Status** | APPROVED |
| **Version** | 1.0 |
| **Datum** | 2026-08-02 |
| **Baseline** | Bootstrap Baseline 1.0 (APPROVED, 2026-08-01) |
| **Architecture** | [Architecture Book v2.0](architecture-book-v2.md) — APPROVED / FROZEN (2026-07-26) |
| **Development Standard** | [v1.1](development-standard-v1.1.md) (APPROVED) |
| **Charter** | [Milestone 1.0 Charter](milestone-1.0-charter.md) (APPROVED, 2026-08-02) |
| **Predecessor** | [Milestone 0.9 Engineering Specification v0.9.1](milestone-0.9-engineering-spec.md) (APPROVED) |

### 1.1 Status

APPROVED — Revision R1 (Contract Hardening). Genehmigt am 2026-08-03 auf Grundlage des Supplementary Governance Review und WAIVER-DEV-001 (APPROVED). Nachweis: [Engineering Specification 1.0 — Approval Record](governance/engineering-specification-1.0-approval-record.md).

### 1.2 Revisionshistorie

| Version | Datum | Änderung |
|---|---|---|
| 1.0 | 2026-08-02 | Erstfassung |
| R1 | 2026-08-02 | Contract Hardening — 31 Findings adressiert (29 geschlossen, 2 offen als DEV-001/DEV-002) |

### 1.3 Zweck

Diese Engineering Specification ist der Implementation Contract für Milestone 1.0. Sie definiert Scope, Gap Analysis, Functional Requirements, Acceptance Criteria, Quality Gates und die Implementierungsreihenfolge gemäß Development Standard v1.1 §6.

### 1.4 Executive Summary

Milestone 1.0 macht JOCHEN X zu einer belastbaren Anwendungsplattform für den produktiven Einsatz. Die vorhandene Architektur wird gehärtet, die Host-Fähigkeiten werden ausgebaut und die Entwicklererfahrung für Plugin-Autoren wird verbessert — ohne die bestehende Architektur oder das SDK zu destabilisieren.

Die Spezifikation umfasst 7 Engineering Goals, 14 Functional Requirements, 10 Non-Functional Requirements, 29 Acceptance Criteria, 8 Quality Gates und 7 Work Packages. Alle Anforderungen sind auf die 6 genehmigten Charter Objectives rückverfolgbar.

### 1.5 Selbstbeschränkung

Diese Spezifikation definiert den vertraglichen Rahmen. Sie enthält keine Implementierungsdetails, keine Codebeispiele, keine Dateireferenzen und keine Sprintplanung. Diese Inhalte sind dem Implementation Plan zugewiesen (Charter §8, zweistufiger Prozess).

---

## 2. Referenzen

### 2.1 Governance-Dokumente

| ID | Dokument | Status | Pfad |
|---|---|---|---|
| GOV-001 | Architecture Book v2.0 | APPROVED / FROZEN (2026-07-26) | `docs/architecture-book-v2.md` |
| GOV-002 | Development Standard v1.1 | APPROVED | `docs/development-standard-v1.1.md` |
| GOV-003 | RDR-001 Bootstrap Modularization | APPROVED | `docs/rdr/001-bootstrap-modularization-approval-record.md` |
| GOV-004 | Bootstrap Baseline 1.0 | APPROVED | `docs/baselines/bootstrap-baseline-1.0.md` |
| GOV-005 | Milestone 1.0 Charter | APPROVED (2026-08-02) | `docs/milestone-1.0-charter.md` |
| GOV-006 | Charter Approval Record | APPROVED | `docs/governance/milestone-1.0-charter-approval-record.md` |
| GOV-007 | Milestone 0.9 Engineering Specification v0.9.1 | APPROVED | `docs/milestone-0.9-engineering-spec.md` |
| ADR-005 | Plugin Integrity Validation | APPROVED | `docs/adr/005-plugin-integrity-validation.md` |
| ADR-006 | Plugin Permission Model | APPROVED | `docs/adr/006-plugin-permission-model.md` |
| ADR-007 | Plugin Dependency Resolution | APPROVED | `docs/adr/007-plugin-dependency-resolution.md` |
| ADR-011 | SDK Host Integration | APPROVED | `docs/adr/011-sdk-host-integration.md` |

### 2.2 Referenzhierarchie

Bei Widersprüchen zwischen Dokumenten gilt die folgende Hierarchie gemäß Development Standard v1.1 §3.3:

| Rang | Dokument |
|---|---|
| 1 | Architecture Book v2.0 |
| 2 | ADRs |
| 3 | Development Standard v1.1 |
| 4 | Bootstrap Baseline 1.0 / Milestone 1.0 Charter (milestone-bindend) |
| 5 | Engineering Specification (dieses Dokument) |
| 6 | Review Reports |
| 7 | Correction Reports |

Bootstrap Baseline 1.0 und Milestone 1.0 Charter sind als milestone-bindende Artefakte zwischen Development Standard und Engineering Specification eingeordnet. Die Rangfolge zwischen Baseline und Charter ist über Charter §8 (Baseline-Governance) begründet.

---

## 3. Baseline-Verifikation

### 3.1 Baseline-Daten

| Eigenschaft | Wert | Evidenz |
|---|---|---|
| **Release Tag** | `v0.9.0` | Verified: Milestone 0.9 APPROVED |
| **Application Version** | `0.9.0` | Verified: `pyproject.toml` → `project.version` (E-08) |
| **SDK Version** | `0.9.0` | Verified: `sdk/version.py` → `SDK_VERSION` (E-09) |
| **SDK API Version** | `1.0.0` | Verified: `sdk/version.py` → `SDK_API_VERSION` (E-06) |
| **Core Runtime** | `v1.0.0` | Verified: Tag `core-runtime-v1.0.0` (E-07) |
| **Architecture Freeze** | Architecture Book v2.0 — APPROVED / FROZEN (2026-07-26) | Verified: `docs/architecture-book-v2.md` (E-05) |
| **Bootstrap Baseline** | 1.0 | Verified: `docs/baselines/bootstrap-baseline-1.0.md` (E-03, E-04) |
| **Tests** | 1019 bestanden, 0 Regressionen | Verified: Bootstrap Baseline 1.0 §7 (E-10) |

### 3.2 Referenzdokument-Status

| Dokument | Status | Verifiziert |
|---|---|---|
| ADR-005 | APPROVED | `docs/adr/005-plugin-integrity-validation.md` (E-12) |
| ADR-006 | APPROVED | `docs/adr/006-plugin-permission-model.md` (E-13) |
| ADR-007 | APPROVED | `docs/adr/007-plugin-dependency-resolution.md` (E-14) |
| ADR-011 | APPROVED | `docs/adr/011-sdk-host-integration.md` |
| RDR-001 | APPROVED | `docs/rdr/001-bootstrap-modularization-approval-record.md` |

### 3.3 Plugin-Runtime-Pipeline

Die verbindliche Pipeline-Reihenfolge gemäß Bootstrap Baseline 1.0 §5.2:

```
Discovery (Manifest-Erkennung)
         ↓
Integrity Validation (ADR-005)
         ↓
Permission Authorization (ADR-006)
         ↓
Dependency Resolution (ADR-007)
         ↓
Activation (Import, Instantiation, Wiring, Start)
```

Diese Reihenfolge ist sicherheitskritisch und unveränderlich (Baseline §4, Invariante 6).

### 3.4 Baseline Constraints

Die folgenden Einschränkungen gelten für alle Arbeiten im Rahmen dieser Spezifikation:

- Keine Änderungen an der Architecture Book v2.0 eingefrorenen API-Oberfläche
- Keine Änderungen an der Bootstrap-Phasensequenz (Baseline §4, Invariante 5)
- Keine Änderungen an der Plugin-Runtime-Pipeline-Reihenfolge (Baseline §4, Invariante 6)
- Keine Änderungen an den Public Exports des Bootstrap-Pakets ohne genehmigte Governance (Baseline §8)
- Keine Breaking Changes an SDK-Verträgen
- Keine neuen externen Abhängigkeiten

### 3.5 Architecture Freeze

Der Architecture Freeze gemäß Architecture Book v2.0 §22 ist für die Zulässigkeit von Erweiterungen maßgeblich:

- **§22.1 Freeze-Scope**: Die eingefrorenen APIs und Contracts sind unveränderlich.
- **§22.2 Additive Erweiterungen**: Neue optionale Felder, neue Stages und Bugfixes erfordern keine ADR (E-15).
- **§22.3 ADR-pflichtige Änderungen**: Entfernung eingefrorener Symbole, Lifecycle-Änderungen, Major-Version-Bumps.

### 3.6 Baseline-Versionen

| Artefakt | Baseline-Version | Quelle |
|---|---|---|
| Anwendung | 0.9.0 | `pyproject.toml` (E-08) |
| SDK | 0.9.0 | `sdk/version.py` (E-09) |
| SDK API | 1.0.0 | `sdk/version.py` (E-06) |

Die Versionsangaben wurden gegen die Projekt-Build-Metadaten und SDK-Versionskonstanten verifiziert. Sie weichen vom eingefrorenen Architecture Book v2.0 §22.4 ab (dort 0.7.0 / 0.7.1 / 1.0.0), da das Architecture Book auf dem Stand des Architecture Freeze eingefroren ist. Die Abweichung ist erklärbar und stellt keinen Widerspruch dar.

### 3.7 Version Targets

- **SDK API Version**: Verbleibt bei 1.0.0. Eine Änderung wäre nach Architecture Book v2.0 §22.3 ADR-pflichtig.
- **Anwendungsversion und SDK-Version**: Werden im Implementation Plan festgelegt (FI-008).
- **Major-Version-Bumps**: Ausgeschlossen für diesen Milestone.

---

## 4. Charter-Objectives

Die sechs Objectives wurden wörtlich aus Milestone 1.0 Charter §4 übernommen. Sie bilden den normativen Ausgangspunkt für alle Engineering Goals und Functional Requirements.

| ID | Charter Objective | Quelle |
|---|---|---|
| CO-001 | Anwendungsplattform stärken | Charter §4.1 |
| CO-002 | Erweiterbarkeit verbessern | Charter §4.2 |
| CO-003 | Host-Fähigkeiten erweitern | Charter §4.3 |
| CO-004 | Entwicklererfahrung verbessern | Charter §4.4 |
| CO-005 | Zuverlässigkeit erhöhen | Charter §4.5 |
| CO-006 | SDK-Stabilität bewahren | Charter §4.6 |

---

## 5. Scope & Gap Analysis

### 5.1 Scope-Kategorien

Die folgenden sechs Kategorien gemäß Charter §5 gehören zum Umfang dieses Milestones:

| Kategorie | Charter-Referenz |
|---|---|
| Plattform-Härtung | Charter §5, Bullet 1 |
| Host-Service-Erweiterung | Charter §5, Bullet 2 |
| Plugin-Ökosystem | Charter §5, Bullet 3 |
| Observability | Charter §5, Bullet 4 |
| Testabdeckung | Charter §5, Bullet 5 |
| Dokumentation | Charter §5, Bullet 6 |

### 5.2 Out of Scope

Gemäß Charter §6:

- Architektur-Redesign
- Bootstrap-Redesign (Bootstrap Baseline 1.0 ist Referenz)
- SDK Breaking Changes
- Experimentelle Features
- UI-Redesign
- Externe Abhängigkeiten (ohne explizite Governance-Entscheidung)

### 5.3 Scope Verification

| Scope-Kategorie | Status | Adressiert durch |
|---|---|---|
| Plattform-Härtung | Addressed | EG-001, EG-006 → FR-001, FR-002, FR-009, FR-010 |
| Host-Service-Erweiterung | Addressed | EG-002 → FR-003, FR-004 |
| Plugin-Ökosystem | Addressed | EG-004 → FR-005, FR-006 |
| Observability | Addressed | EG-005 → FR-007, FR-008 |
| Testabdeckung | Addressed | NFR-005, QG-007 |
| Dokumentation | Addressed | EG-007 → FR-011, FR-012 |

Alle sechs Charter-Kategorien sind durch mindestens ein Engineering Goal und die zugehörigen Functional Requirements abgedeckt.

**Einschränkung (DEV-002):** Diese Scope Verification führt keine Dateireferenzen (Datei, Zeile, Status) gemäß Development Standard v1.1 §6.2 Abschnitt 2. Die Aufnahme von Dateireferenzen setzt die Delta Analysis voraus, die gemäß DEV-001 dem Implementation Plan zugewiesen ist.

### 5.4 Preservation Areas

Die folgenden Bereiche sind Erhaltungsbereiche. Sie werden durch Baseline Constraints (3.4) und Non-Functional Requirements geschützt, nicht durch Scope-Erweiterung:

| Bereich | Schutzmechanismus |
|---|---|
| Bootstrap-Paket | NFR-002, Baseline §4 (7 Invarianten), Baseline §8 (Change Control) |
| Plugin-Sicherheitspipeline | NFR-006, Baseline §5.2 |
| Plugin-Runtime | Baseline §4, Invariante 6 |
| Architektur | NFR-001, Architecture Freeze §22 |

### 5.5 Gap Assessment

| Scope-Kategorie | Baseline-Stand | Gap |
|---|---|---|
| Plattform-Härtung | Deterministischer Bootstrap, Phasensequenz stabil | Lifecycle-Übergänge nicht vollständig definiert; Ablehnungsverhalten nicht formalisiert |
| Host-Service-Erweiterung | ServiceRegistry operativ | Host-Services nicht vollständig beschrieben; Erweiterungspunkte nicht formal definiert |
| Plugin-Ökosystem | Plugin-Runtime-Pipeline vollständig | Autorenvorgaben verstreut; Rejection-Feedback unstrukturiert |
| Observability | Grundlegende Metrics und HealthCheck Protocols | Keine plugin-spezifischen Diagnostics; Metriken nicht erweiterbar |
| Testabdeckung | 1019 Tests, 0 Regressionen | Erweiterung für neue FRs erforderlich |
| Dokumentation | Architecture Book v2.0 eingefroren; ADRs genehmigt | SDK-Dokumentation nicht vollständig; Architekturdokumentation erfordert Aktualisierung |

### 5.6 Scope Constraints

- Keine Architekturänderungen an Core, App, SDK oder UI-Schicht
- Keine Implementierungsdetails in dieser Spezifikation (→ 1.5)
- Keine neuen externen Abhängigkeiten (NFR-007)
- Keine Breaking Changes an bestehenden SDK-Verträgen (NFR-003)

---

## 6. Engineering Goals

### 6.1 Übersicht

Sieben Engineering Goals adressieren die sechs Charter Objectives. Jedes Goal ist mindestens einem Objective zugeordnet. Jedes Objective besitzt mindestens ein Goal.

### 6.2 CO-zu-EG-Zuordnung

| Charter Objective | Engineering Goals |
|---|---|
| CO-001 — Anwendungsplattform stärken | EG-001, EG-006 |
| CO-002 — Erweiterbarkeit verbessern | EG-002 |
| CO-003 — Host-Fähigkeiten erweitern | EG-002 |
| CO-004 — Entwicklererfahrung verbessern | EG-004, EG-007 |
| CO-005 — Zuverlässigkeit erhöhen | EG-005, EG-006 |
| CO-006 — SDK-Stabilität bewahren | EG-003, EG-007 |

### 6.3 Goal-Katalog

**EG-001 — Platform Robustness** (CO-001)

Die Robustheit der Kern-Infrastruktur erhöhen. Lifecycle-Übergänge sind vollständig definiert und deterministisch. Unzulässige Übergänge werden explizit abgelehnt.

**EG-002 — Host Service & Extensibility** (CO-002, CO-003)

Die Host-Fähigkeiten gezielt ergänzen und die Erweiterbarkeit für Plugins ausbauen, ohne bestehende Verträge zu verändern.

**EG-003 — SDK Contract Preservation** (CO-006)

Bestehende SDK-Verträge bewahren. Alle Erweiterungen erfolgen additiv. Bestehende Konsumenten werden nicht beeinträchtigt.

**EG-004 — Developer Experience** (CO-004)

Plugin-Autoren erhalten bessere Werkzeuge, vollständige Dokumentation und strukturiertes Feedback bei Pipeline-Ablehnungen.

**EG-005 — Observability & Diagnostics** (CO-005)

Diagnostik und Beobachtbarkeit der Plattform werden gestärkt. Plugin-spezifische Metriken und Gesundheitsprüfungen werden ermöglicht.

**EG-006 — Reliability & Recovery** (CO-001, CO-005)

Fehlerbehandlung und Ausfallsicherheit werden verbessert. Fehler in Einzelkomponenten führen zu definiertem Wiederherstellungsverhalten. Plugin-Ausfälle werden isoliert.

**EG-007 — Documentation Quality** (CO-004, CO-006)

Die technische Dokumentation wird aktualisiert und vervollständigt. SDK-Dokumentation und Architekturdokumentation reflektieren den implementierten Stand.

### 6.4 Regeln

- Jedes Engineering Goal besitzt mindestens einen Functional Requirement.
- Kein Engineering Goal ohne zugeordnetes Charter Objective.
- Auf Goal-Ebene ist eine Zuordnung zu mehreren Objectives zulässig, sofern jeder abgeleitete Functional Requirement genau einem dieser Objectives zugeordnet ist.

---

## 7. Functional Requirements

### 7.1 Regeln

- Jeder Functional Requirement ist genau einem Charter Objective und genau einem Engineering Goal zugeordnet.
- Jeder Functional Requirement ist lösungsneutral formuliert und beschreibt einen überprüfbaren fachlichen Outcome.
- Jeder Functional Requirement besitzt mindestens zwei Acceptance Criteria (Ausnahme: FR-001 besitzt drei).

### 7.2 FR-Katalog

**FR-001 — Platform Lifecycle Determinism** (CO-001, EG-001, WP-001)

Jeder Zustandsübergang der Anwendungsplattform folgt einer vollständig definierten Zustandsmaschine. Kein Übergang findet ohne explizite Berechtigung statt.

**FR-002 — Lifecycle Control Enhancement** (CO-001, EG-001, WP-001)

Die Menge der zulässigen Zustandsübergänge ist vollständig bestimmt. Übergänge, die nicht in dieser Menge enthalten sind, werden mit einem definierten Ablehnungsergebnis zurückgewiesen.

**FR-003 — Host Service Description** (CO-003, EG-002, WP-002)

Die Dienste, die der Host Plugins bereitstellt, sind in einer zentralen Registrierung vollständig beschrieben und programmatisch abrufbar.

**FR-004 — Plugin Extension Points** (CO-002, EG-002, WP-002)

Plugins können die Plattform über definierte Erweiterungspunkte erweitern, ohne bestehende Verträge zu verändern.

**FR-005 — Plugin Author Documentation** (CO-004, EG-004, WP-003)

Plugin-Autoren verfügen über vollständige, widerspruchsfreie Vorgaben, die an einer einzigen definierten Stelle verfügbar sind.

**FR-006 — Pipeline Rejection Feedback** (CO-004, EG-004, WP-003)

Bei Ablehnung eines Plugins durch die Runtime-Pipeline wird die auslösende Pipelinestufe und das verletzte Kriterium ausgewiesen.

**FR-007 — Diagnostic Reporting** (CO-005, EG-005, WP-004)

Die Plattform stellt strukturierte Diagnoseinformationen über den Zustand der Plugin-Runtime bereit.

**FR-008 — Observability Extension** (CO-005, EG-005, WP-004)

Das Observability-System der Plattform ist um plugin-spezifische Metriken und Gesundheitsprüfungen erweiterbar.

**FR-009 — Error Recovery** (CO-001, EG-006, WP-005)

Fehler in einzelnen Plattformkomponenten oder Plugins führen zu einem definierten Wiederherstellungsverhalten, nicht zu einem undefinierten Zustand.

**FR-010 — Failure Isolation** (CO-005, EG-006, WP-005)

Der Ausfall eines einzelnen Plugins beeinträchtigt weder die Plattform noch andere Plugins.

**FR-011 — SDK Documentation Completeness** (CO-004, EG-007, WP-007)

Die SDK-Dokumentation beschreibt alle öffentlichen APIs, Erweiterungspunkte und Lifecycle-Verträge vollständig und aktuell.

**FR-012 — Architecture Documentation Currency** (CO-006, EG-007, WP-007)

Die technische Architekturdokumentation reflektiert den implementierten Stand zum Zeitpunkt des Milestone-Abschlusses.

**FR-013 — Additive Extension Rule** (CO-006, EG-003, WP-006)

Alle Erweiterungen der Plattform und des SDK erfolgen additiv. Keine Erweiterung entfernt, umbenennt oder verändert das Verhalten bestehender öffentlicher Symbole.

FR-013 und FR-014 sind vertragserhaltende Anforderungen zu CO-006. Sie sind ausdrücklich nicht scope-eröffnend.

**FR-014 — Consumer Compatibility Assurance** (CO-006, EG-003, WP-006)

Bestehende Plugins, die gegen SDK API 1.0.0 entwickelt wurden, funktionieren ohne Änderung nach Abschluss des Milestones.

### 7.3 Vollständigkeit

14 Functional Requirements verteilt auf 7 Engineering Goals und 7 Work Packages. Jeder FR ist genau einem CO, einem EG und einem WP zugeordnet.

---

## 8. Non-Functional Requirements

### 8.1 Regeln

- Jeder Non-Functional Requirement ist mindestens einem Quality Gate zugeordnet.
- Non-Functional Requirements definieren Rahmenbedingungen, keine funktionalen Ergebnisse.

### 8.2 NFR-Katalog

**NFR-001 — Architecture Freeze Compliance**

Alle API-Contracts und Symbole, die in Architecture Book v2.0 §22 eingefroren sind, bleiben unverändert. Additive Erweiterungen gemäß §22.2 sind zulässig.

**NFR-002 — Bootstrap Baseline Invariants**

Die sieben Architectural Invariants aus Bootstrap Baseline 1.0 §4 bleiben unverändert. Änderungen an Paketstruktur, Runtime-Pipeline, Public Exports, BootstrapManager oder default_stages() erfordern eine genehmigte Governance-Entscheidung gemäß Baseline §8.

**NFR-003 — SDK API Backward Compatibility**

Die SDK API Version verbleibt bei 1.0.0. Alle SDK-Erweiterungen sind additiv. Bestehende Symbole, Signaturen und Verträge bleiben unverändert.

**NFR-004 — Performance Non-Degradation**

Der Milestone führt keine messbaren Performance-Regressionen gegenüber der Bootstrap Baseline 1.0 ein.

**NFR-005 — Test Regression Baseline**

Die 1019 bestehenden Tests der Bootstrap Baseline 1.0 bleiben vollständig grün. Keine Regressionen.

**NFR-006 — Security Pipeline Compliance**

Die Plugin-Runtime-Pipeline gemäß Bootstrap Baseline 1.0 §5.2 (Discovery → Integrity Validation → Permission Authorization → Dependency Resolution → Activation) wird nicht verändert. Die Reihenfolge ist sicherheitskritisch (Baseline §4, Invariante 6).

**NFR-007 — No External Dependencies**

Keine neuen externen Bibliotheken werden eingeführt. Die einzige externe Abhängigkeit bleibt PySide6 ≥ 6.8.

**NFR-008 — Deterministic Behavior**

Bootstrap-Sequenz und Plugin-Lifecycle verhalten sich deterministisch. Gleiche Eingaben führen zu gleichen Ergebnissen.

**NFR-009 — Error Handling & Graceful Degradation**

Fehler in einzelnen Plugins oder Stages dürfen nicht die Stabilität der Gesamtplattform beeinträchtigen. Die Plattform degradiert kontrolliert.

**NFR-010 — Documentation Currency**

Technische Dokumentation (Architecture Book, ADRs, SDK-Dokumentation) reflektiert den implementierten Stand bei Milestone-Abschluss.

### 8.3 Vollständigkeit

10 Non-Functional Requirements. Jeder NFR ist mindestens einem Quality Gate zugeordnet.

### 8.4 Bezugsgrößen

| NFR | Bezugsgröße |
|---|---|
| NFR-001 | Architecture Book v2.0 §22 (E-05) |
| NFR-002 | Bootstrap Baseline 1.0 §4, 7 Invarianten (E-11) |
| NFR-003 | SDK API Version 1.0.0 (E-06) |
| NFR-005 | 1019 bestehende Tests (E-10) |
| NFR-006 | Bootstrap Baseline 1.0 §5.2 (E-02) |

### 8.5 NFR-zu-QG-Zuordnung

| NFR | Quality Gates |
|---|---|
| NFR-001 | QG-003 |
| NFR-002 | QG-001, QG-006 |
| NFR-003 | QG-003 |
| NFR-004 | QG-001 |
| NFR-005 | QG-007 |
| NFR-006 | QG-006 |
| NFR-007 | QG-008 |
| NFR-008 | QG-001 |
| NFR-009 | QG-007 |
| NFR-010 | QG-005 |

---

## 9. Traceability

### 9.1 Kanonische Verifikationskette

```
Charter Objective → Engineering Goal → Functional Requirement → Acceptance Criterion → Quality Gate
```

Work Packages sind die organisatorische Bündelung der Functional Requirements. Sie sind keine Ebene der Verifikationskette.

### 9.2 Traceability-Regeln

1. Jedes Charter Objective besitzt mindestens ein Engineering Goal. Kein Goal ohne Objective.
2. Jedes Engineering Goal besitzt mindestens einen Functional Requirement. Die FR-Menge ist vollständig und überschneidungsfrei partitioniert.
3. Jeder Functional Requirement ist genau einem Charter Objective, einem Engineering Goal und einem Work Package zugeordnet. Kein Work Package ohne Functional Requirement.
4. Auf Goal-Ebene ist eine Zuordnung zu mehreren Objectives zulässig, sofern jeder abgeleitete FR genau einem dieser Objectives zugeordnet ist.
5. Jeder Functional Requirement besitzt mindestens ein Acceptance Criterion. Jedes AC gehört zu genau einem FR. Keine doppelten AC-IDs.
6. Jedes Acceptance Criterion besitzt mindestens ein Quality Gate. Jedes Quality Gate prüft mindestens ein Acceptance Criterion.
7. Jeder Non-Functional Requirement ist mindestens einem Quality Gate zugeordnet.
8. Der Work-Package-Abhängigkeitsgraph ist azyklisch und frei von Selbstbezügen.
9. Die Typzuordnung der Work Packages folgt zwingend aus der Abhängigkeitsmatrix.

### 9.3 Kennzahlen

| Artefakt | Anzahl |
|---|---|
| Charter Objectives | 6 |
| Engineering Goals | 7 |
| Functional Requirements | 14 |
| Non-Functional Requirements | 10 |
| Work Packages | 7 |
| Acceptance Criteria | 29 |
| Quality Gates | 8 |

### 9.4 CO → EG Matrix

| Charter Objective | Engineering Goals |
|---|---|
| CO-001 | EG-001, EG-006 |
| CO-002 | EG-002 |
| CO-003 | EG-002 |
| CO-004 | EG-004, EG-007 |
| CO-005 | EG-005, EG-006 |
| CO-006 | EG-003, EG-007 |

### 9.5 EG → FR Matrix

| Engineering Goal | Functional Requirements |
|---|---|
| EG-001 — Platform Robustness | FR-001, FR-002 |
| EG-002 — Host Service & Extensibility | FR-003, FR-004 |
| EG-003 — SDK Contract Preservation | FR-013, FR-014 |
| EG-004 — Developer Experience | FR-005, FR-006 |
| EG-005 — Observability & Diagnostics | FR-007, FR-008 |
| EG-006 — Reliability & Recovery | FR-009, FR-010 |
| EG-007 — Documentation Quality | FR-011, FR-012 |

### 9.6 FR → WP Matrix

| Functional Requirement | Work Package |
|---|---|
| FR-001 | WP-001 |
| FR-002 | WP-001 |
| FR-003 | WP-002 |
| FR-004 | WP-002 |
| FR-005 | WP-003 |
| FR-006 | WP-003 |
| FR-007 | WP-004 |
| FR-008 | WP-004 |
| FR-009 | WP-005 |
| FR-010 | WP-005 |
| FR-011 | WP-007 |
| FR-012 | WP-007 |
| FR-013 | WP-006 |
| FR-014 | WP-006 |

### 9.7 FR → AC Matrix (normativ)

| Functional Requirement | Acceptance Criteria |
|---|---|
| FR-001 | AC-001.1, AC-001.2, AC-001.3 |
| FR-002 | AC-002.1, AC-002.2 |
| FR-003 | AC-003.1, AC-003.2 |
| FR-004 | AC-004.1, AC-004.2 |
| FR-005 | AC-005.1, AC-005.2 |
| FR-006 | AC-006.1, AC-006.2 |
| FR-007 | AC-007.1, AC-007.2 |
| FR-008 | AC-008.1, AC-008.2 |
| FR-009 | AC-009.1, AC-009.2 |
| FR-010 | AC-010.1, AC-010.2 |
| FR-011 | AC-011.1, AC-011.2 |
| FR-012 | AC-012.1, AC-012.2 |
| FR-013 | AC-013.1, AC-013.2 |
| FR-014 | AC-014.1, AC-014.2 |

### 9.8 AC → QG Matrix (normativ)

| Acceptance Criterion | Quality Gates |
|---|---|
| AC-001.1 | QG-001 |
| AC-001.2 | QG-001 |
| AC-001.3 | QG-001 |
| AC-002.1 | QG-001 |
| AC-002.2 | QG-001 |
| AC-003.1 | QG-002, QG-008 |
| AC-003.2 | QG-002 |
| AC-004.1 | QG-002 |
| AC-004.2 | QG-002 |
| AC-005.1 | QG-004 |
| AC-005.2 | QG-004 |
| AC-006.1 | QG-004 |
| AC-006.2 | QG-004, QG-006 |
| AC-007.1 | QG-006 |
| AC-007.2 | QG-006 |
| AC-008.1 | QG-006 |
| AC-008.2 | QG-006 |
| AC-009.1 | QG-007 |
| AC-009.2 | QG-007 |
| AC-010.1 | QG-007 |
| AC-010.2 | QG-007 |
| AC-011.1 | QG-005 |
| AC-011.2 | QG-005 |
| AC-012.1 | QG-005 |
| AC-012.2 | QG-005, QG-008 |
| AC-013.1 | QG-003 |
| AC-013.2 | QG-003, QG-008 |
| AC-014.1 | QG-003 |
| AC-014.2 | QG-003, QG-008 |

### 9.9 WP → AC Sicht (abgeleitet, nicht normativ)

Diese Sicht ist aus den normativen Matrizen 9.6 und 9.7 abgeleitet. Work Packages erben die Acceptance Criteria ihrer Functional Requirements. Die normative Zuordnung bleibt FR → AC (9.7).

| Work Package | Functional Requirements | Acceptance Criteria (abgeleitet) |
|---|---|---|
| WP-001 | FR-001, FR-002 | AC-001.1, AC-001.2, AC-001.3, AC-002.1, AC-002.2 |
| WP-002 | FR-003, FR-004 | AC-003.1, AC-003.2, AC-004.1, AC-004.2 |
| WP-003 | FR-005, FR-006 | AC-005.1, AC-005.2, AC-006.1, AC-006.2 |
| WP-004 | FR-007, FR-008 | AC-007.1, AC-007.2, AC-008.1, AC-008.2 |
| WP-005 | FR-009, FR-010 | AC-009.1, AC-009.2, AC-010.1, AC-010.2 |
| WP-006 | FR-013, FR-014 | AC-013.1, AC-013.2, AC-014.1, AC-014.2 |
| WP-007 | FR-011, FR-012 | AC-011.1, AC-011.2, AC-012.1, AC-012.2 |

---

## 10. Implementation Sequence

### 10.1 Phasen

Die Implementierung erfolgt in zwei Phasen, abgeleitet aus dem Work-Package-Abhängigkeitsgraphen (12.4).

**Phase 1 — Unabhängige Arbeitspakete** (parallel durchführbar):

| Reihenfolge | Work Package | Typ |
|---|---|---|
| 1a | WP-001 — Platform Hardening | Provider |
| 1b | WP-002 — Host Service & Extensibility | Provider |
| 1c | WP-003 — Developer Experience | Provider |
| 1d | WP-004 — Observability | Provider |
| 1e | WP-005 — Reliability | Provider |
| 1f | WP-007 — Documentation | Provider |

**Phase 2 — Abhängiges Arbeitspaket** (nach Abschluss aller Phase-1-Pakete):

| Reihenfolge | Work Package | Typ | Abhängigkeiten |
|---|---|---|---|
| 2 | WP-006 — SDK Contract Verification | Dependent | WP-001, WP-002, WP-003, WP-004, WP-005, WP-007 |

### 10.2 Begründung

WP-006 (SDK Contract Verification) verifiziert, dass alle Erweiterungen aus Phase 1 die SDK-Verträge nicht verletzen. Diese Verifikation setzt den Abschluss aller Phase-1-Arbeitspakete voraus.

---

## 11. Acceptance Criteria

### 11.1 Zweck

Acceptance Criteria sind die normativen Prüfaussagen für die Abnahme der Functional Requirements. Jedes Criterion ist eine eigenständige, unabhängig bewertbare Aussage.

### 11.2 Regeln

- Jedes Acceptance Criterion gehört zu genau einem Functional Requirement.
- Jedes Acceptance Criterion ist einzeln entscheidbar (bestanden / nicht bestanden).
- Jedes Acceptance Criterion ist mindestens einem Quality Gate zugeordnet (9.8).
- Acceptance Criteria werden durch die kanonische Kette CO → EG → FR → AC → QG verifiziert. Work Packages sind keine Quelle der Acceptance Criteria.

### 11.3 AC-Katalog

#### FR-001 — Platform Lifecycle Determinism

**AC-001.1**: Die Zustandsmaschine der Anwendungsplattform definiert alle zulässigen Übergänge in einer vollständigen Übergangstabelle.

**AC-001.2**: Kein Zustandsübergang wird ausgeführt, der nicht in der Übergangstabelle enthalten ist.

**AC-001.3**: Die Übergangstabelle ist durch mindestens einen Test pro Übergang abgesichert.

#### FR-002 — Lifecycle Control Enhancement

**AC-002.1**: Die Menge der zulässigen Zustandsübergänge ist explizit definiert und vollständig dokumentiert.

**AC-002.2**: Ein Übergang, der nicht in der zulässigen Menge enthalten ist, wird mit einem strukturierten Ablehnungsergebnis zurückgewiesen, das den Grund enthält.

#### FR-003 — Host Service Description

**AC-003.1**: Alle Host-Services sind in der ServiceRegistry registriert und über deren API abrufbar.

**AC-003.2**: Die Beschreibung jedes Host-Services umfasst Name, Typ und Verfügbarkeitszeitpunkt.

#### FR-004 — Plugin Extension Points

**AC-004.1**: Plugins können über die definierten Erweiterungspunkte neue Funktionalität registrieren.

**AC-004.2**: Die Erweiterung durch ein Plugin verändert keine bestehende API-Signatur und keinen bestehenden Vertrag.

#### FR-005 — Plugin Author Documentation

**AC-005.1**: Alle Autorenvorgaben (Manifest-Schema, Lifecycle-Vertrag, Permission-Modell) sind an einer einzigen Stelle dokumentiert.

**AC-005.2**: Die Dokumentation ist widerspruchsfrei gegenüber den implementierten Verträgen in `sdk/`.

#### FR-006 — Pipeline Rejection Feedback

**AC-006.1**: Bei Ablehnung eines Plugins enthält das Ergebnis die auslösende Pipelinestufe.

**AC-006.2**: Bei Ablehnung eines Plugins enthält das Ergebnis das verletzte Kriterium mit Bezug auf die Pipeline-Reihenfolge gemäß Bootstrap Baseline 1.0 §5.2.

#### FR-007 — Diagnostic Reporting

**AC-007.1**: Diagnoseinformationen enthalten den Plugin-Identifikator und die betroffene Pipelinestufe.

**AC-007.2**: Diagnoseinformationen sind programmatisch abrufbar und nicht nur als Logausgabe verfügbar.

#### FR-008 — Observability Extension

**AC-008.1**: Neue Metriken können registriert werden, ohne bestehende Metriken zu verändern.

**AC-008.2**: Plugin-spezifische Gesundheitsprüfungen können über das bestehende HealthCheck-Protocol registriert werden.

#### FR-009 — Error Recovery

**AC-009.1**: Ein Fehler in einer einzelnen Bootstrap-Stage führt zu einem definierten Fehlerzustand, nicht zu einem unbehandelten Abbruch.

**AC-009.2**: Nach einem fehlgeschlagenen Stage-Durchlauf befinden sich alle bereits initialisierten Komponenten in einem konsistenten Zustand.

#### FR-010 — Failure Isolation

**AC-010.1**: Der Ausfall eines Plugins während der Aktivierung verhindert nicht die Aktivierung anderer Plugins.

**AC-010.2**: Die Plattform dokumentiert fehlgeschlagene Plugin-Aktivierungen und setzt den Betrieb mit den erfolgreich aktivierten Plugins fort.

#### FR-011 — SDK Documentation Completeness

**AC-011.1**: Jedes öffentliche Symbol in `sdk/__all__` ist in der SDK-Dokumentation beschrieben.

**AC-011.2**: Die SDK-Dokumentation referenziert die korrekte SDK-API-Version (1.0.0 zum Zeitpunkt dieser Spezifikation).

#### FR-012 — Architecture Documentation Currency

**AC-012.1**: Die Architekturdokumentation benennt alle Module, deren öffentliche APIs und die geltenden Verträge.

**AC-012.2**: Keine Aussage der Architekturdokumentation widerspricht dem implementierten Code zum Zeitpunkt des Milestone-Abschlusses.

#### FR-013 — Additive Extension Rule

**AC-013.1**: Keine Erweiterung im Scope dieses Milestones entfernt oder umbenennt ein öffentliches Symbol.

**AC-013.2**: Jede Erweiterung ist als additiv klassifizierbar gemäß Architecture Book v2.0 §22.2.

#### FR-014 — Consumer Compatibility Assurance

**AC-014.1**: Ein Plugin, das ausschließlich Symbole aus SDK API 1.0.0 verwendet, besteht ohne Codeänderung alle seine Tests nach Abschluss des Milestones.

**AC-014.2**: Die Rückwärtskompatibilität wird durch einen dedizierten Kompatibilitätstest nachgewiesen.

---

## 12. Work Packages & Dependency Graph

### 12.1 Übersicht

7 Work Packages bündeln die 14 Functional Requirements organisatorisch. Die Zuordnung FR → WP ist in 9.6 normativ geführt.

### 12.2 Regeln

- Kein Work Package ohne mindestens einen Functional Requirement.
- Zirkuläre Abhängigkeiten sind nicht zulässig.
- Selbstbezügliche Abhängigkeiten sind nicht zulässig.
- Die Typzuordnung folgt zwingend aus der Abhängigkeitsmatrix (12.3).

### 12.3 Kategorien

| Kategorie | Definition |
|---|---|
| **Provider** | Keine eingehenden Abhängigkeiten; mindestens ein anderes Work Package hängt von den Ergebnissen ab. |
| **Dependent** | Mindestens eine eingehende Abhängigkeit von einem anderen Work Package. |

Die Kategorien sind disjunkt und vollständig.

### 12.4 WP-Katalog

| ID | Titel | FRs | Kategorie | Abhängigkeiten |
|---|---|---|---|---|
| WP-001 | Platform Hardening | FR-001, FR-002 | Provider | — |
| WP-002 | Host Service & Extensibility | FR-003, FR-004 | Provider | — |
| WP-003 | Developer Experience | FR-005, FR-006 | Provider | — |
| WP-004 | Observability | FR-007, FR-008 | Provider | — |
| WP-005 | Reliability | FR-009, FR-010 | Provider | — |
| WP-006 | SDK Contract Verification | FR-013, FR-014 | Dependent | WP-001, WP-002, WP-003, WP-004, WP-005, WP-007 |
| WP-007 | Documentation | FR-011, FR-012 | Provider | — |

### 12.5 Dependency Graph

```
WP-001 ──┐
WP-002 ──┤
WP-003 ──┤
WP-004 ──┼──► WP-006
WP-005 ──┤
WP-007 ──┘
```

Der Graph ist azyklisch und frei von Selbstbezügen (maschinell verifiziert).

---

## 13. Test Strategy

### 13.1 Teststufen

| Stufe | Verzeichnis | Zweck |
|---|---|---|
| Unit Tests | `tests/`, `tests/unit/` | Einzelne Komponenten isoliert prüfen |
| Integration Tests | `tests/integration/` | Zusammenspiel mehrerer Komponenten |
| Security Tests | `tests/security/` | Default Deny, Adversarial Input, Permission Bypass |
| Recovery Tests | `tests/recovery/` | Escalation, Retry, Determinismus |
| Compatibility Tests | `tests/` | SDK-Rückwärtskompatibilität (AC-014.2) |

### 13.2 Testprinzipien

- Kein Qt-Event-Loop erforderlich (außer UI-Tests)
- Deterministisch: kein `time.sleep()`, keine externen Abhängigkeiten
- Isolation: jeder Test erstellt eigene Instanzen
- Thread Safety wird explizit getestet
- `QT_QPA_PLATFORM=offscreen` für UI-Tests

### 13.3 Test-Anforderungen

- Jedes Acceptance Criterion (AC) hat mindestens einen Test
- Fehlerszenarien explizit testen
- Bestehende 1019 Tests dürfen nicht brechen (NFR-005)
- Neue Tests für alle neuen FRs

### 13.4 Abdeckung

| AC-Gruppe | Teststufe | Prüfmethode |
|---|---|---|
| AC-001.x, AC-002.x | Unit, Integration | Zustandsmaschine-Tests |
| AC-003.x, AC-004.x | Integration | ServiceRegistry-Tests |
| AC-005.x | Review | Dokumentationsprüfung |
| AC-006.x | Unit, Integration | Pipeline-Rejection-Tests |
| AC-007.x, AC-008.x | Unit, Integration | Observability-Tests |
| AC-009.x, AC-010.x | Recovery | Error-Handling-Tests |
| AC-011.x, AC-012.x | Review | Dokumentationsprüfung |
| AC-013.x, AC-014.x | Compatibility | Rückwärtskompatibilitäts-Tests |

---

## 14. Quality Gates

### 14.1 Zweck

Quality Gates sind formale Freigabepunkte. Jedes Gate prüft eine definierte Menge von Acceptance Criteria und Non-Functional Requirements.

### 14.2 Regeln

- Jedes Quality Gate prüft mindestens ein Acceptance Criterion.
- Jedes Acceptance Criterion ist mindestens einem Quality Gate zugeordnet.
- Kein Quality Gate ohne Prüfmethode.
- Quality Gates werden durch die kanonische Kette CO → EG → FR → AC → QG verifiziert.

### 14.3 Kanonische Kette

Die Quality Gates bilden den Endpunkt der Verifikationskette:

```
Charter Objective → Engineering Goal → Functional Requirement → Acceptance Criterion → Quality Gate
```

### 14.4 QG-Katalog

**QG-001 — Platform Stability**

| Eigenschaft | Wert |
|---|---|
| Prüfmethode | Automatisierte Testsuite, manuelle Verifikation der Zustandsmaschine |
| Prüft AC | AC-001.1, AC-001.2, AC-001.3, AC-002.1, AC-002.2 |
| Prüft NFR | NFR-002, NFR-004, NFR-008 |
| Kriterium | Alle zugeordneten AC bestanden; keine Performance-Regression; deterministische Übergänge |

**QG-002 — Host Service Availability**

| Eigenschaft | Wert |
|---|---|
| Prüfmethode | Integration Tests, ServiceRegistry-Verifikation |
| Prüft AC | AC-003.1, AC-003.2, AC-004.1, AC-004.2 |
| Kriterium | Alle Host-Services registriert und abrufbar; Erweiterungspunkte operativ |

**QG-003 — Architecture Freeze Compliance**

| Eigenschaft | Wert |
|---|---|
| Prüfmethode | API-Surface-Vergleich gegen eingefrorene Baseline, Review |
| Prüft AC | AC-013.1, AC-013.2, AC-014.1, AC-014.2 |
| Prüft NFR | NFR-001, NFR-003 |
| Kriterium | Keine eingefrorenen Symbole entfernt oder umbenannt; alle Erweiterungen additiv; Rückwärtskompatibilität nachgewiesen |

**QG-004 — Developer Feedback Quality**

| Eigenschaft | Wert |
|---|---|
| Prüfmethode | Verifikation der Rejection-Nachrichten, Dokumentationsprüfung |
| Prüft AC | AC-005.1, AC-005.2, AC-006.1, AC-006.2 |
| Kriterium | Autorenvorgaben vollständig und widerspruchsfrei; Ablehnungen enthalten Pipelinestufe und Kriterium |

**QG-005 — Traceability Completeness**

| Eigenschaft | Wert |
|---|---|
| Prüfmethode | Dokumentenprüfung, Vollständigkeitsabgleich |
| Prüft AC | AC-011.1, AC-011.2, AC-012.1, AC-012.2 |
| Prüft NFR | NFR-010 |
| Kriterium | SDK-Dokumentation vollständig; Architekturdokumentation aktuell; keine Widersprüche zum implementierten Code |

**QG-006 — Pipeline Security Compliance**

| Eigenschaft | Wert |
|---|---|
| Prüfmethode | Pipeline-Verifikation gegen Bootstrap Baseline 1.0 §5.2, Tests |
| Prüft AC | AC-006.2, AC-007.1, AC-007.2, AC-008.1, AC-008.2 |
| Prüft NFR | NFR-002, NFR-006 |
| Kriterium | Pipeline-Reihenfolge unverändert; Diagnoseinformationen mit Pipelinestufe; Observability erweiterbar |

**QG-007 — Test Coverage Maintenance**

| Eigenschaft | Wert |
|---|---|
| Prüfmethode | Automatisierte Testsuite (`python -m pytest -q`) |
| Prüft AC | AC-009.1, AC-009.2, AC-010.1, AC-010.2 |
| Prüft NFR | NFR-005, NFR-009 |
| Kriterium | 1019 Baseline-Tests plus neue Tests grün; Fehlerbehandlung und Isolation nachgewiesen |

**QG-008 — Governance Compliance**

| Eigenschaft | Wert |
|---|---|
| Prüfmethode | Governance-Audit, Dokumentenprüfung |
| Prüft AC | AC-003.1, AC-012.2, AC-013.2, AC-014.2 |
| Prüft NFR | NFR-007 |
| Kriterium | Keine Governance-Verletzungen; alle Änderungen rückverfolgbar; keine neuen externen Abhängigkeiten; RDR-001 unversehrt |

---

## 15. Definition of Done

Eine Aufgabe im Rahmen dieses Milestones gilt als abgeschlossen, wenn:

- [ ] Alle zugeordneten Acceptance Criteria sind bestanden
- [ ] Alle zugeordneten Quality Gates sind bestanden
- [ ] Alle bestehenden Tests (1019 Baseline) sind weiterhin grün
- [ ] Alle neuen Tests sind grün
- [ ] Nur genehmigter Scope ist implementiert
- [ ] Architecture Book v2.0 Freeze-Scope ist unverändert
- [ ] Bootstrap Baseline 1.0 Invarianten sind unverändert
- [ ] SDK API Version verbleibt bei 1.0.0
- [ ] Schichtmodell eingehalten (Abhängigkeiten nach innen)
- [ ] Type Hints auf allen öffentlichen APIs
- [ ] `__all__` in jedem betroffenen Modul aktualisiert
- [ ] Keine unbegründeten TODOs
- [ ] Commit thematisch sauber
- [ ] Keine Secrets oder unnötigen Dateien im Commit
- [ ] Dokumentation aktualisiert (falls erforderlich)

Die Definition of Done wird durch die kanonische Verifikationskette CO → EG → FR → AC → QG nachgewiesen.

---

## 16. ES Validation

### 16.1 Zweck

Dieses Kapitel prüft die interne Vollständigkeit und Konsistenz der Engineering Specification.

### 16.2 Verifikationskette

Die kanonische Verifikationskette für alle Prüfaussagen:

```
Charter Objective → Engineering Goal → Functional Requirement → Acceptance Criterion → Quality Gate
```

### 16.3 Vollständigkeitstabelle

| # | Kapitel | Dev Standard §6.2 | Status |
|---|---|---|---|
| 1 | Dokumentenkontrolle | — | Erfüllt |
| 2 | Referenzen | — | Erfüllt |
| 3 | Baseline-Verifikation | §6.2 #1 Baseline Verification | Erfüllt |
| 4 | Charter-Objectives | — | Erfüllt |
| 5 | Scope & Gap Analysis | §6.2 #2 Scope Verification, §6.2 #3 Gap Analysis | Erfüllt (DEV-002: ohne Dateireferenzen) |
| 6 | Engineering Goals | — | Erfüllt |
| 7 | Functional Requirements | — | Erfüllt |
| 8 | Non-Functional Requirements | — | Erfüllt |
| 9 | Traceability | — | Erfüllt |
| 10 | Implementation Sequence | §6.2 #7 Implementation Sequence | Erfüllt |
| 11 | Acceptance Criteria | §6.2 #8 Acceptance Criteria | Erfüllt |
| 12 | Work Packages & Dependency Graph | §6.2 #6 Dependency Graph | Erfüllt |
| 13 | Test Strategy | §6.2 #9 Test Strategy | Erfüllt |
| 14 | Quality Gates | §6.2 #10 Quality Gates | Erfüllt |
| 15 | Definition of Done | §6.2 #13 Definition of Done | Erfüllt |
| 16 | ES Validation | — | Erfüllt |
| 17 | Risks | §6.2 #11 Risks | Erfüllt |
| 18 | Deliverables | §6.2 #12 Deliverables | Erfüllt |
| 19 | Future Items | §6.2 #14 Future Items | Erfüllt |
| 20 | Evidence Summary | §6.2 #15 Evidence Summary | Erfüllt |
| 21 | Exit & Authorization | — | Erfüllt |
| — | §6.2 #4 Delta Analysis | — | Offen — DEV-001 |
| — | §6.2 #5 Module Work Breakdown | — | Offen — DEV-001 |

### 16.4 Referenzverifikation

| Referenz | Ergebnis |
|---|---|
| Milestone 1.0 Charter | Konsistent. Alle 6 Objectives und alle 6 Scope-Kategorien abgedeckt. Kein FR widerspricht Charter §6 (Out of Scope). Autorisierungsgrenzen (21.4) entsprechen dem Charter Approval Record. |
| Bootstrap Baseline 1.0 | Konsistent. Alle 7 Architectural Invariants in NFR-002 und Baseline Constraints (3.4) verankert. Change-Control-Regel §8 in FI-002 abgebildet. Pipeline-Reihenfolge §5.2 in 3.3 und NFR-006 verankert. |
| RDR-001 | Konsistent. Als GOV-003 referenziert; Unverletztheit als Nachweis von QG-008. |
| Architecture Book v2.0 | Konsistent. Architecture Freeze §22 über NFR-001 und QG-003 verankert. §22.2 (additive Erweiterungen ohne ADR) stützt FR-013 (E-15). |
| Development Standard v1.1 | Konsistent, mit Ausnahme der offenen Abweichungen DEV-001 und DEV-002 zu §6.2. Referenzhierarchie gemäß §3.3 (E-16). |
| ADR-005 | Konsistent. Integrity Validation als Pipelinestufe unverändert; in NFR-006 und AC-006.2 verankert. |
| ADR-006 | Konsistent. Permission Authorization als Pipelinestufe unverändert; Default-Deny unberührt. |
| ADR-007 | Konsistent. Dependency Resolution als Pipelinestufe unverändert; Aktivierungsreihenfolge unberührt. |
| ADR-011 | Konsistent. Bezeichnung „SDK Host Integration" entspricht dem Quelldokument. |

### 16.5 Invariantenprüfung

| # | Invariante | Ergebnis |
|---|---|---|
| 1 | Jedes Charter Objective besitzt mindestens ein Engineering Goal; kein Goal ohne Objective | Bestanden |
| 2 | Kapitel 9.4 und 9.5 sind wechselseitig konsistent | Bestanden |
| 3 | Jedes Engineering Goal besitzt mindestens einen FR; die FR-Menge ist vollständig und überschneidungsfrei partitioniert | Bestanden |
| 4 | Jeder FR ist genau einem Objective, einem Goal und einem Work Package zugeordnet; kein WP ohne FR | Bestanden |
| 5 | Jeder FR besitzt mindestens ein AC; jedes AC gehört zu genau einem FR; keine doppelten AC-IDs | Bestanden |
| 6 | Jedes AC besitzt mindestens ein QG; jedes QG prüft mindestens ein AC; Kapitel 9.8 und 14.4 sind wechselseitig konsistent | Bestanden |
| 7 | Jeder NFR ist mindestens einem QG zugeordnet | Bestanden |
| 8 | Der Work-Package-Abhängigkeitsgraph ist azyklisch und frei von Selbstbezügen | Bestanden |
| 9 | Die Typzuordnung der Work Packages folgt zwingend aus der Abhängigkeitsmatrix | Bestanden |

### 16.6 Traceability-Audit-Ergebnis

| Prüfkriterium | Ergebnis |
|---|---|
| Kein Charter Objective ohne Engineering Goal | Erfüllt |
| Kein Engineering Goal ohne Charter Objective | Erfüllt |
| Kein Engineering Goal ohne Functional Requirement | Erfüllt |
| Kein Functional Requirement ohne Acceptance Criterion | Erfüllt |
| Kein Acceptance Criterion ohne Quality Gate | Erfüllt |
| Kein Quality Gate ohne Acceptance Criterion | Erfüllt |
| Kein Work Package ohne Functional Requirement | Erfüllt |
| Keine doppelten Zuordnungen | Erfüllt |
| Keine widersprüchlichen Zuordnungen | Erfüllt |
| Keine Zuordnung widerspricht dem Charter | Erfüllt |

### 16.7 Scope-Neutralitätsprüfung

| Prüfung | Baseline | Spezifikation | Ergebnis |
|---|---|---|---|
| Functional Requirements | 14 | 14 | Unverändert |
| Non-Functional Requirements | 10 | 10 | Unverändert |
| Work Packages | 7 | 7 | Unverändert |
| Quality Gates | 8 | 8 | Unverändert |
| Engineering Goals | 7 | 7 | Unverändert |
| Acceptance Criteria | — | 29 | Präzisierung, keine neuen Anforderungen |
| Neue Features | — | keine | Erfüllt |
| Architekturänderungen | — | keine | Erfüllt |
| ADR-Änderungen | — | keine | Erfüllt |

### 16.8 Review-Bereitschaft

| Kriterium | Bewertung |
|---|---|
| Vollständig ausgearbeitet | Erfüllt. Alle 21 Kapitel sind vollständig; keine Platzhalter, keine vorläufigen Zuordnungen. |
| Intern auf Konsistenz geprüft | Erfüllt. Neun Invariantenklassen geprüft, alle bestanden. |
| Für Independent Review bereitstehend | Erfüllt. Offene Findings sind dokumentiert und benötigen eine Governance-Entscheidung, keine weitere Ausarbeitung. |
| Versioniert und eindeutig identifizierbar | Erfüllt. ES-1.0, Revision R1 — Contract Hardening. |

### 16.9 Genehmigungsreife

| Kriterium | Bewertung |
|---|---|
| Alle Kapitel vollständig | Erfüllt |
| Alle Traceability-Regeln erfüllt | Erfüllt |
| Keine Critical Findings | Nicht erfüllt — DEV-001 |
| Keine High Findings | Erfüllt |
| Medium/Low Findings dokumentiert und bewertet | Erfüllt |
| Verpflichtende Referenzen korrekt eingebunden | Erfüllt |
| Deviation Register entschieden | Nicht erfüllt |

### 16.10 Empfehlung

READY FOR INDEPENDENT REVIEW. NOT READY FOR APPROVAL.

DEV-001 ist ein Zielkonflikt zwischen zwei genehmigten Governance-Dokumenten — Development Standard v1.1 §6.2 setzt einen einstufigen Prozess voraus, Milestone 1.0 Charter §8 etabliert einen zweistufigen. Dieser Konflikt ist auf Ebene der Engineering Specification nicht auflösbar. Das Independent Review ist das vorgesehene Forum für diese Entscheidung.

### 16.11 Optionen für DEV-001

**Option A — Abweichung genehmigen** (empfohlen): Die Delta Analysis und das Module Work Breakdown werden formal dem Implementation Plan 1.0 zugewiesen. Geringster Aufwand; erfordert eine dokumentierte Waiver-Entscheidung. Entspricht dem vom Charter genehmigten zweistufigen Prozess.

**Option B — Development Standard anpassen**: Eine Version v1.2 bildet den zweistufigen Prozess ab und verteilt die fünfzehn Pflichtabschnitte auf Engineering Specification und Implementation Plan. Höherer Aufwand; beseitigt die Ursache dauerhaft.

**Option C — Abschnitte ergänzen** (nicht empfohlen): Die Engineering Specification wird um implementierungsnahe Inhalte erweitert. Dies widerspricht Kapitel 1.5 und dem Charter Approval Record, der ausschließlich die Engineering Specification Phase autorisiert.

### 16.12 Deviation Register

| ID | Finding | Schweregrad | Status | Erforderliche Entscheidung |
|---|---|---|---|---|
| DEV-001 | Delta Analysis und Module Work Breakdown nach Development Standard v1.1 §6.2 fehlen. | Critical | Offen | Genehmigung der Abweichung (Option A), Anpassung des Development Standard (Option B) oder Scope-Erweiterung mit erneutem Review (Option C). |
| DEV-002 | Scope Verification führt keine Dateireferenzen nach §6.2 Abschnitt 2. | Medium | Offen | Abhängig von der Entscheidung zu DEV-001. |

---

## 17. Risks

| ID | Risiko | Wahrscheinlichkeit | Auswirkung | Mitigation |
|---|---|---|---|---|
| R-001 | Scope Creep | Mittel | Hoch | NFR-001 (Architecture Freeze), QG-003, QG-008; Definition of Done; alle Erweiterungen müssen auf Charter §4 rückverfolgbar sein |
| R-002 | SDK-Kompatibilitätsbruch | Niedrig | Kritisch | NFR-003 (SDK API 1.0.0), FR-013, FR-014, QG-003; Kompatibilitätstest (AC-014.2) |
| R-003 | Baseline-Drift | Niedrig | Hoch | NFR-002 (Baseline Invariants), QG-006; Baseline Change Control (Baseline §8) |
| R-004 | Governance-Overhead | Mittel | Mittel | Charter §8 (zweistufiger Prozess); Independent Review nach Development Standard v1.1 §9 |
| R-005 | Abhängigkeit von Milestone 0.9 Stabilität | Niedrig | Mittel | NFR-005 (1019 Tests); Bootstrap Baseline 1.0 als verifizierter Ausgangspunkt |

Risiken R-001 bis R-005 sind den fünf Risiken aus Charter §9 entnommen. Die Mitigationen sind aus den in dieser Spezifikation definierten NFRs, Quality Gates und Acceptance Criteria abgeleitet.

---

## 18. Deliverables

| # | Deliverable | Typ | Nachweis |
|---|---|---|---|
| D-001 | WP-001: Platform Hardening | Implementation | Tests, QG-001 |
| D-002 | WP-002: Host Service & Extensibility | Implementation | Tests, QG-002 |
| D-003 | WP-003: Developer Experience | Implementation | Tests, QG-004 |
| D-004 | WP-004: Observability | Implementation | Tests, QG-006 |
| D-005 | WP-005: Reliability | Implementation | Tests, QG-007 |
| D-006 | WP-006: SDK Contract Verification | Verification | Kompatibilitätstest, QG-003 |
| D-007 | WP-007: Documentation | Documentation | Review, QG-005 |
| D-008 | Implementation Plan 1.0 | Governance | Development Standard v1.1 §7, Charter §8 |
| D-009 | Sprint Reports | Governance | Development Standard v1.1 §8 |
| D-010 | Milestone Review Report | Governance | Development Standard v1.1 §9.6 |

---

## 19. Future Items

Die folgenden Themen sind explizit ausgeschlossen und als Folgearbeiten dokumentiert:

| ID | Item | Quelle | Begründung |
|---|---|---|---|
| FI-001 | Architektur-Redesign | Charter §6 | Außerhalb Milestone 1.0 Scope |
| FI-002 | Bootstrap-Redesign | Charter §6 | Bootstrap Baseline 1.0 Change Control (§8) |
| FI-003 | SDK Breaking Changes | Charter §6 | SDK API bleibt bei 1.0.0 |
| FI-004 | Experimentelle Features | Charter §6 | Nicht spezifiziert, nicht im Scope |
| FI-005 | UI-Redesign | Charter §6 | Außerhalb Milestone 1.0 Scope |
| FI-006 | Externe Abhängigkeiten | Charter §6 | Erfordert explizite Governance-Entscheidung |
| FI-007 | Delta Analysis & Module Work Breakdown | DEV-001 | Dem Implementation Plan zugewiesen (Charter §8, zweistufiger Prozess) |
| FI-008 | Zielversionen (Application, SDK) | ES 3.7 | Im Implementation Plan festzulegen; Major-Version-Bumps ausgeschlossen |

---

## 20. Evidence Summary

### 20.1 Klassifikation

Gemäß Development Standard v1.1 §4 (Evidence First) werden alle technischen Aussagen dieser Spezifikation klassifiziert.

### 20.2 Verified Evidence (17)

| ID | Aussage | Quelle |
|---|---|---|
| E-01 | Bootstrap-Phasensequenz INITIALIZE → LOAD_PLUGINS → LOAD_RESOURCES → FINALIZE | Bootstrap Baseline 1.0 §5.1 |
| E-02 | Plugin-Runtime-Pipeline Discovery → Integrity → Permission → Dependency → Activation | Bootstrap Baseline 1.0 §5.2 |
| E-03 | 20 Public API Symbole im Bootstrap-Paket | Bootstrap Baseline 1.0 §3.1 |
| E-04 | 7 Module im Bootstrap-Paket | Bootstrap Baseline 1.0 §2 |
| E-05 | Architecture Freeze gemäß Architecture Book v2.0 §22 | Tag: `architecture-book-v2.0` |
| E-06 | SDK API Version 1.0.0 | `sdk/version.py` → `SDK_API_VERSION` |
| E-07 | Core Runtime v1.0.0 | Tag: `core-runtime-v1.0.0` |
| E-08 | Application Version 0.9.0 | `pyproject.toml` → `project.version` |
| E-09 | SDK Version 0.9.0 | `sdk/version.py` → `SDK_VERSION` |
| E-10 | 1019 Tests bestanden, 0 Regressionen | Bootstrap Baseline 1.0 §7 |
| E-11 | 7 Architectural Invariants | Bootstrap Baseline 1.0 §4 |
| E-12 | ADR-005 Plugin Integrity Validation — APPROVED | `docs/adr/005-plugin-integrity-validation.md` |
| E-13 | ADR-006 Plugin Permission Model — APPROVED | `docs/adr/006-plugin-permission-model.md` |
| E-14 | ADR-007 Plugin Dependency Resolution — APPROVED | `docs/adr/007-plugin-dependency-resolution.md` |
| E-15 | Additive Erweiterungen ohne ADR zulässig | Architecture Book v2.0 §22.2 |
| E-16 | Referenzhierarchie gemäß Development Standard v1.1 §3.3 | Development Standard v1.1 §3.3 |
| E-17 | Charter-Objectives vollständig aus Milestone 1.0 Charter §4 übernommen | Milestone 1.0 Charter §4 |

### 20.3 Inference (3)

| ID | Aussage | Ableitung |
|---|---|---|
| E-18 | Scope-Kategorien decken alle Charter-Objectives ab | Abgeleitet aus der CO → EG → FR-Kette (9.4, 9.5) und der Scope Verification (5.3) |
| E-19 | Die Implementation Sequence respektiert die WP-Abhängigkeiten | Abgeleitet aus dem Abhängigkeitsgraphen (12.5); Phase-2-Eintritt erst nach Phase-1-Abschluss |
| E-20 | Die Test Strategy deckt alle Acceptance Criteria ab | Abgeleitet aus der AC-zu-QG-Zuordnung (9.8) und den Prüfmethoden in 14.4 |

### 20.4 Open Blocker (3)

| ID | Aussage | Blocker |
|---|---|---|
| E-21 | Delta Analysis fehlt | DEV-001 — Dem Implementation Plan zugewiesen |
| E-22 | Scope Verification ohne Dateireferenzen | DEV-002 — Abhängig von DEV-001 |
| E-23 | Zielversionen für Application und SDK nicht festgelegt | FI-008 — Im Implementation Plan festzulegen |

---

## 21. Exit & Authorization

### 21.1 Nächste Governance-Schritte

Nach Genehmigung dieser Engineering Specification:

1. **Governance-Entscheidung zu DEV-001** — Wahl zwischen Option A, B oder C (16.11)
2. **Implementation Plan 1.0** — Strukturierter Umsetzungsplan gemäß Charter §8
3. **ADRs** — Falls architekturrelevante Änderungen notwendig werden (Charter §8)
4. **Sprint Planning** — Planung der Umsetzungs-Sprints

### 21.2 Governance-Kette

```
Milestone 1.0 Charter (APPROVED)
        ↓
Engineering Specification 1.0 (dieses Dokument)
        ↓
Independent Review
        ↓
Corrections
        ↓
Approval
        ↓
Implementation Plan 1.0
        ↓
Implementation (Sprints)
```

### 21.3 Autorisierungsgrenzen

Dieses Dokument autorisiert:

- Die Definition von Scope, Requirements und Acceptance Criteria für Milestone 1.0
- Die Festlegung der Quality Gates und der Definition of Done
- Die Vorbereitung des Implementation Plans

Dieses Dokument autorisiert **nicht**:

- Produktionscode-Änderungen
- ADR-Implementierung ohne separate ADR-Genehmigung
- Sprint-Implementierung ohne genehmigten Implementation Plan
- Änderungen an der Bootstrap Baseline ohne genehmigte Governance (Baseline §8)
- Änderungen am Architecture Freeze ohne neue Architecture Book Version

### 21.4 Referenz auf Charter Approval Record

Die Autorisierungsgrenzen entsprechen dem Charter Approval Record (GOV-006), der die Implementation Authorization ausschließlich für die Engineering Specification Phase erteilt hat.
