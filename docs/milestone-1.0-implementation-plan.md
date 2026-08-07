# Milestone 1.0 Implementation Plan

> **Dokumentstatus:** APPROVED (2026-08-06) — genehmigt gemäß
> [Approval Decision W-6](governance/implementation-plan-1.0-approval-decision-w6.md)
> und dokumentiert im
> [Approval Record (W-7)](governance/implementation-plan-1.0-approval-record.md).
> Der frühere Status DRAFT galt bis zum Durchlaufen des Genehmigungsprozesses
> gemäß Kapitel 10.4.
> Das Dokument umfasst die Kapitel 1 (Document Control), 2 (Planning Framework),
> 3 (Baseline Verification), 4 (Delta Analysis), 5 (Module Work Breakdown),
> 6 (Work Package Sequencing & Dependency Planning), 7 (Implementation
> Strategy), 8 (Verification Planning), 9 (Test Strategy), 10 (Completion,
> Approval & Readiness), 11 (Risk Management), 12 (Migration Strategy) und
> 13 (Rollout Strategy) sowie die Anhänge A und B. Sämtliche
> Planungsgegenstände gemäß Kapitel 2.3 sind behandelt (Kapitel 10.8,
> CC-11 bis CC-13). Der Status DRAFT besteht fort, bis der
> Genehmigungsprozess gemäß Kapitel 10.4 durchlaufen ist.

---

## 1. Document Control

### 1.1 Document Metadata

| Eigenschaft | Wert |
|---|---|
| **Dokumenttitel** | Milestone 1.0 Implementation Plan |
| **Dokument-ID** | IP-1.0 |
| **Version** | 1.0 |
| **Revision** | R1.2 — Correction Cycle R2 |
| **Status** | **APPROVED** (2026-08-06, W-6 / Approval Record W-7) |
| **Datum** | 2026-08-05 |
| **Autor** | Lead Software Architect / Implementation Planner |
| **Governance Authority** | Governance Architect / Release Authority |
| **Autorisierung** | [Engineering Specification 1.0 — Approval Record](governance/engineering-specification-1.0-approval-record.md) §11 — *AUTHORIZED: Implementation Plan 1.0 (DRAFT) — ONLY* |
| **Specification** | [Engineering Specification 1.0](milestone-1.0-engineering-spec.md), Revision R1 (APPROVED, 2026-08-03) |
| **Charter** | [Milestone 1.0 Charter](milestone-1.0-charter.md) (APPROVED, 2026-08-02) |
| **Baseline** | Bootstrap Baseline 1.0 (APPROVED, 2026-08-01) |
| **Architecture** | [Architecture Book v2.0](architecture-book-v2.md) — APPROVED / FROZEN (2026-07-26) |
| **Development Standard** | [v1.1](development-standard-v1.1.md) (APPROVED) |
| **Waiver** | [WAIVER-DEV-001](governance/waiver-dev-001.md) (APPROVED, 2026-08-02), präzisiert durch [WAIVER-AMENDMENT-001](governance/waiver-amendment-001.md) (APPROVED, 2026-08-05) |
| **Vorgängerdokument** | [Milestone 0.9 Implementation Plan v1.1](milestone-0.9-implementation-plan.md) (APPROVED) |

#### Revisionshistorie

Die Historie führt jeden abgeschlossenen Erstellungs- und Korrekturzyklus.
Die Zwischenstände R0.1 bis R0.6 sind aus den zugehörigen Prüfartefakten in
`docs/audits/` rekonstruiert; sie waren zum Zeitpunkt ihrer Entstehung nicht
protokolliert. Die Rekonstruktion ist als solche gekennzeichnet und wird
nicht als zeitgleiche Aufzeichnung ausgegeben.

| Revision | Datum | Änderung | Auslöser / Prüfartefakt |
|---|---|---|---|
| R0 | 2026-08-03 | Initial Draft — Kapitel 1 (Document Control) | Approval Record ES 1.0 §11 |
| R0.1 | 2026-08-03/04 | Kapitel 2 bis 9 sowie Anhang A ergänzt (kapitelweise Erstellung gemäß PP-07) — *rekonstruiert* | — |
| R0.2 | 2026-08-04 | Korrekturen aus dem Consistency Audit zu Kapitel 9 (F9-001 bis F9-007); Anhang B — Performance Measurement Methodology erstellt (F9-004, SC-06) — *rekonstruiert* | `audits/implementation-plan-1.0-chapter-9-consistency-audit.md` |
| R0.3 | 2026-08-04 | Kapitel 10 (Completion, Approval & Readiness) ergänzt — *rekonstruiert* | `audits/implementation-plan-1.0-chapter-10-independent-review.md`; GP-001 bis GP-005 eröffnet |
| R0.4 | 2026-08-04 | Kapitel 11 (Risk Management) ergänzt; GR-001 nach 11.10 überführt — *rekonstruiert* | `audits/implementation-plan-1.0-chapter-11-independent-review.md`; GP-003 geschlossen |
| R0.5 | 2026-08-04 | Kapitel 12 (Migration Strategy) ergänzt — *rekonstruiert* | `audits/implementation-plan-1.0-chapter-12-independent-review.md` |
| R0.6 | 2026-08-04 | Kapitel 13 (Rollout Strategy) ergänzt; 10.7 und 10.8 fortgeschrieben — *rekonstruiert* | `audits/implementation-plan-1.0-chapter-13-independent-review.md`; GP-001 und GP-002 geschlossen |
| **R1** | **2026-08-05** | **Correction Cycle R1** — Abarbeitung des Global Consistency Audit (W-2, R1): H-02, M-01 bis M-08, L-01 bis L-07, E-01 bis E-04. H-01 ohne Textkorrektur an die Governance übergeben (GDR-001). | `audits/implementation-plan-1.0-global-consistency-audit.md`; `audits/implementation-plan-1.0-correction-report-r1.md` |
| **R1.1** | **2026-08-05** | **Editorial synchronization after GDR-001 and WAIVER-AMENDMENT-001.** Keine fachlichen Änderungen. | `governance/gdr-001-waiver-closing-criteria.md`; `governance/waiver-amendment-001.md`; `audits/implementation-plan-1.0-editorial-synchronization-report-r1-1.md` |
| **R1.2** | **2026-08-05** | **Correction Cycle R2** — Abarbeitung der Findings des Independent Review (W-3): W3-M-01 (Korrektur der Exportanzahl in API-01 von 20 auf 22 an vier Stellen; Symbolmenge unverändert) und W3-E-01 (Registerregel 3 um klassenbezogene Präfixe ergänzt). Keine inhaltlichen Änderungen. | `audits/implementation-plan-1.0-independent-review-w3.md`; `audits/implementation-plan-1.0-correction-report-r2.md` |

Ab R1 wird die Historie fortlaufend geführt. Jede weitere Änderung erhält
eine eigene Zeile mit Auslöser und Prüfartefakt.

---

### 1.2 Purpose

#### Zweck des Implementation Plans

Der Implementation Plan 1.0 ist der strukturierte Umsetzungsplan für
Milestone 1.0. Er beantwortet die Frage, **in welcher Reihenfolge und mit
welcher Vorgehensweise** die bereits genehmigten Anforderungen umgesetzt
werden.

Die Rollenverteilung in der Governance-Kette ist eindeutig:

| Dokument | Leitfrage |
|---|---|
| Milestone 1.0 Charter | Warum wird dieser Milestone durchgeführt? |
| Engineering Specification 1.0 | Was muss erfüllt werden? |
| **Implementation Plan 1.0** | **In welcher Reihenfolge und wie wird umgesetzt?** |

Der Implementation Plan ist damit ein reines Planungsartefakt. Er trifft keine
Entscheidungen über Ziele, Anforderungen oder Architektur — diese sind in den
vorgelagerten, genehmigten Dokumenten abschließend festgelegt.

#### Beziehung zur Engineering Specification

Die Engineering Specification 1.0 (Revision R1) ist der Implementation
Contract. Sie wurde am 2026-08-03 genehmigt und definiert 7 Engineering Goals,
14 Functional Requirements, 10 Non-Functional Requirements, 29 Acceptance
Criteria, 8 Quality Gates und 7 Work Packages.

Der Implementation Plan steht zu diesem Vertrag in einem strikt abgeleiteten
Verhältnis:

- Jeder Planungsinhalt MUSS auf die Engineering Specification rückverfolgbar
  sein.
- Der Plan darf den Vertrag konkretisieren, aber nicht erweitern, einschränken
  oder umdeuten.
- Bei Widersprüchen zwischen Implementation Plan und Engineering Specification
  hat die Engineering Specification Vorrang (Development Standard v1.1 §3.3).

#### Umsetzung bereits genehmigter Anforderungen

Dieser Plan führt **keine neuen Anforderungen** ein. Er plant ausschließlich
die Umsetzung von Anforderungen, die durch die Engineering Specification 1.0
bereits genehmigt sind.

Zusätzlich erfüllt der Implementation Plan die durch WAIVER-DEV-001
zugewiesenen Pflichtabschnitte des Development Standard v1.1 §6.2:

| Zugewiesener Abschnitt | Quelle | Verbindlichkeit |
|---|---|---|
| Delta Analysis (§6.2 #4) | WAIVER-DEV-001 §3.1 (4) | MUSS enthalten sein |
| Module Work Breakdown (§6.2 #5) | WAIVER-DEV-001 §3.1 (5) | MUSS enthalten sein |
| Scope Verification mit Dateireferenzen (§6.2 #2) | WAIVER-DEV-001 §9 (4) | MUSS enthalten sein |
| Performance-Messmethodik | Independent Review Finding F-004 | MUSS definiert werden |

Diese Zuweisungen sind die verbindlichen Closing Criteria von WAIVER-DEV-001.
Der Waiver bleibt aktiv, bis der Independent Review des Implementation Plans
ihre Vollständigkeit bestätigt hat.

---

### 1.3 Scope

Der Scope des Dokuments setzt sich aus zwei Quellen zusammen, die getrennt
gehalten werden, weil sie unterschiedliche Verbindlichkeitsgrundlagen haben:

| Quelle | Inhalt | Normative Festlegung |
|---|---|---|
| **Planungsscope** | Die Planungsgegenstände PS-01 bis PS-06 | **Kapitel 2.3 — abschließend und normativ** |
| **Waiver-Pflichtabschnitte** | Delta Analysis, Module Work Breakdown, Scope Verification mit Dateireferenzen, Performance-Messmethodik | Kapitel 1.2, WAIVER-DEV-001 §3.1 und §9 |

Die folgende Übersicht ist die **Zusammenfassung beider Quellen** auf
Dokumentebene. Sie ist keine eigenständige Scope-Definition und tritt nicht
neben Kapitel 2.3; bei Abweichung gilt Kapitel 2.3.

| # | Gegenstand | Quelle | Fundstelle |
|---|---|---|---|
| 1 | **Umsetzungsplanung** | Rahmen der Planungsgegenstände PS-01 bis PS-06 | Kapitel 6, 7 |
| 2 | **Reihenfolge** | PS-01 | Kapitel 6 |
| 3 | **Abhängigkeiten** | PS-02 | Kapitel 6.4 |
| 4 | **Verifikation** | PS-03 | Kapitel 8, 9 |
| 5 | **Migration** | PS-04 | Kapitel 12 |
| 6 | **Rollout** | PS-05 | Kapitel 13 |
| 7 | **Risiken** | PS-06 | Kapitel 11 |
| 8 | **Delta Analysis** | Waiver-Pflichtabschnitt | Kapitel 4 |
| 9 | **Module Work Breakdown** | Waiver-Pflichtabschnitt | Kapitel 5 |
| 10 | **Scope Verification mit Dateireferenzen** | Waiver-Pflichtabschnitt | Kapitel 5.5 |
| 11 | **Performance-Messmethodik** | Auflage aus Finding F-004 | Anhang B |

Sämtliche Vollständigkeitsaussagen des Plans gegenüber dem **Planungsscope**
— AP-09, RL-00, CC-11 bis CC-13, Kapitel 10.7, Abbruchbedingung AB-03 —
beziehen sich ausschließlich auf PS-01 bis PS-06 gemäß Kapitel 2.3. Die
Vollständigkeit gegenüber den **Waiver-Pflichtabschnitten** wird gesondert
über Kapitel 5.5.1, CC-08 und SC-03 bis SC-05 geführt.

#### Nicht im Scope

Der Implementation Plan enthält **keine Architektur**. Architekturentscheidungen
sind abschließend im Architecture Book v2.0 (FROZEN) und in den genehmigten
ADRs festgelegt. Sollte während der Planung ein architekturrelevanter Bedarf
erkannt werden, ist dieser als Governance-Befund zu eskalieren und über einen
separaten ADR zu entscheiden — nicht im Implementation Plan zu lösen
(Charter §8, Schritt 2).

Ebenfalls außerhalb des Scope: Zieldefinition (Charter), Anforderungsdefinition
(Engineering Specification), Sprint-Durchführung sowie jede Form von
Implementierung.

---

### 1.4 Authoritative Inputs

Die folgenden Dokumente sind die **normativen Eingaben** dieses Implementation
Plans. Ausschließlich diese Dokumente sind autoritativ. Andere Quellen sind für
die Planung nicht zulässig.

| ID | Dokument | Status | Pfad | Rolle als normative Eingabe |
|---|---|---|---|---|
| IN-01 | Engineering Specification 1.0, Revision R1 | APPROVED (2026-08-03) | `docs/milestone-1.0-engineering-spec.md` | **Primäre normative Eingabe.** Implementation Contract — Scope, Requirements, Acceptance Criteria, Quality Gates, Work Packages |
| IN-02 | Engineering Specification 1.0 — Approval Record | APPROVED (2026-08-03) | `docs/governance/engineering-specification-1.0-approval-record.md` | Autorisierungsgrundlage dieses Dokuments; Findings-Status; Authorized Next Phase |
| IN-03 | Engineering Specification 1.0 — Governance Closing Summary | CLOSED (2026-08-03) | `docs/governance/engineering-specification-1.0-governance-closing-summary.md` | Governance-Kette; Implementation Authorization; Autorisierungsgrenzen |
| IN-04 | Milestone 1.0 Charter | APPROVED (2026-08-02) | `docs/milestone-1.0-charter.md` | Milestone-Ziele, Scope-Grenzen, zweistufiger Governance-Prozess (§8) |
| IN-05 | Bootstrap Baseline 1.0 | APPROVED (2026-08-01) | `docs/baselines/bootstrap-baseline-1.0.md` | Verbindliche technische Baseline; Ausgangszustand der Delta Analysis |
| IN-06 | Architecture Book v2.0 | APPROVED / FROZEN (2026-07-26) | `docs/architecture-book-v2.md` | Verbindliche Architekturreferenz; unveränderlich |
| IN-07 | Development Standard v1.1 | APPROVED | `docs/development-standard-v1.1.md` | Normative Struktur- und Prozessvorgaben; Lifecycle (§7); Sprint Rules (§8) |
| IN-08 | WAIVER-DEV-001, präzisiert durch WAIVER-AMENDMENT-001 | APPROVED (2026-08-02) / APPROVED (2026-08-05) | `docs/governance/waiver-dev-001.md`; `docs/governance/waiver-amendment-001.md` | Zuweisung von Delta Analysis und Module Work Breakdown; Closing Criteria (§9) in der durch WAIVER-AMENDMENT-001 §4 verbindlich präzisierten Auslegung |
| IN-09 | ADR-005 — Plugin Integrity Validation | APPROVED | `docs/adr/005-plugin-integrity-validation.md` | Verbindliche Entscheidung; unverändert zu berücksichtigen |
| IN-10 | ADR-006 — Plugin Permission Model | APPROVED | `docs/adr/006-plugin-permission-model.md` | Verbindliche Entscheidung; unverändert zu berücksichtigen |
| IN-11 | ADR-007 — Plugin Dependency Resolution | APPROVED | `docs/adr/007-plugin-dependency-resolution.md` | Verbindliche Entscheidung; unverändert zu berücksichtigen |
| IN-12 | ADR-011 — SDK Host Integration | APPROVED | `docs/adr/011-sdk-host-integration.md` | Verbindliche Entscheidung; unverändert zu berücksichtigen |

#### Referenzhierarchie

Bei Widersprüchen gilt die Rangfolge gemäß Development Standard v1.1 §3.3,
erweitert um die milestone-bindenden Artefakte gemäß Engineering Specification
1.0 §2.2:

| Rang | Dokument |
|---|---|
| 1 | Architecture Book v2.0 |
| 2 | ADRs |
| 3 | Development Standard v1.1 |
| 4 | Bootstrap Baseline 1.0 / Milestone 1.0 Charter (milestone-bindend) |
| 5 | Engineering Specification 1.0 |
| 6 | **Implementation Plan 1.0 (dieses Dokument)** |
| 7 | Review Reports |
| 8 | Correction Reports |

Der Implementation Plan ist damit das rangniedrigste normative Artefakt der
Kette. Er kann kein höherrangiges Dokument überschreiben.

---

### 1.5 Governance Constraints

Für diesen Implementation Plan gelten die folgenden Beschränkungen
verbindlich und ausnahmslos:

| # | Constraint | Grundlage |
|---|---|---|
| GC-01 | **Keine neuen Functional Requirements.** Es werden ausschließlich die genehmigten FR-001..FR-014 umgesetzt. | ES-1.0 §7; WAIVER-DEV-001 §5.2 |
| GC-02 | **Keine neuen Acceptance Criteria.** Es gelten ausschließlich die 29 genehmigten Acceptance Criteria. | ES-1.0 §11; WAIVER-DEV-001 §5.2 |
| GC-03 | **Keine neuen Quality Gates.** Es gelten ausschließlich QG-001..QG-008. | ES-1.0 §14; WAIVER-DEV-001 §5.2 |
| GC-04 | **Keine Architekturänderung.** Das Architecture Book v2.0 ist FROZEN. | Architecture Book v2.0; ES-1.0 §21.3 |
| GC-05 | **Keine ADR-Änderung.** ADR-005, ADR-006, ADR-007 und ADR-011 bleiben unverändert. Neue ADRs erfordern separate Governance. | Charter §8 (2); ES-1.0 §21.3 |
| GC-06 | **Keine Bootstrap-Änderung.** Änderungen an der Bootstrap Baseline 1.0 erfordern einen genehmigten ADR oder RDR vor der Implementierung. | Charter §8 (Baseline-Governance); Baseline §8 |
| GC-07 | **Keine Scope-Erweiterung.** Der Scope ist durch Charter §4/§6 und ES-1.0 §5 abschließend definiert. | Charter §6; ES-1.0 §5; NFR-001 |

Zusätzlich gilt: Non-Functional Requirements (NFR-001..NFR-010), Engineering
Goals (EG-001..EG-007), Work Packages (WP-001..WP-007) und Deliverables
(D-001..D-010) werden unverändert aus der Engineering Specification
übernommen. Der Implementation Plan konkretisiert deren Umsetzung, verändert
sie aber nicht.

Wird während der Planung ein Bedarf erkannt, der eine dieser Beschränkungen
verletzen würde, ist die Planung an dieser Stelle zu unterbrechen und der
Bedarf als Governance-Befund zu eskalieren. Eine eigenmächtige Auflösung durch
den Implementation Plan ist unzulässig.

---

### 1.6 Authorization Boundary

**Dieses Dokument autorisiert keine Implementierung.**

Der Implementation Plan 1.0 befindet sich im Status DRAFT und dient
ausschließlich der Planungsphase.

#### Autorisiert

- Die Erstellung, Prüfung und Korrektur dieses Planungsdokuments
- Die Analyse des bestehenden Zustands zum Zweck der Delta Analysis
- Die Planung von Reihenfolge, Abhängigkeiten, Verifikation und Rollout

#### Nicht autorisiert

| Aktivität | Status |
|---|---|
| Produktionscode | **NOT AUTHORIZED** |
| Sprint Implementation | **NOT AUTHORIZED** |
| ADR Implementation | **NOT AUTHORIZED** |
| Feature Development | **NOT AUTHORIZED** |
| Runtime Changes | **NOT AUTHORIZED** |
| Änderungen an der Bootstrap Baseline | **NOT AUTHORIZED** |
| Änderungen am Architecture Freeze | **NOT AUTHORIZED** |

Produktionscode bleibt weiterhin nicht autorisiert. Die Autorisierung zur
Implementierung entsteht erst durch die explizite Genehmigung dieses
Implementation Plans nach durchlaufenem Governance-Prozess — Independent
Review, Correction Phase und Approval gemäß Development Standard v1.1 §7 und
Milestone 1.0 Charter §8 (Schritte 4 und 5) — gefolgt von der Sprint Planning
Phase (Charter §8, Schritt 6).

Die Genehmigung dieses Plans setzt zusätzlich die Erfüllung der Closing
Criteria von WAIVER-DEV-001 §9 voraus.

---

## 2. Planning Framework

Dieses Kapitel definiert den fachlichen Planungsrahmen: Ziel, Umfang, Grenzen
und die verbindlichen Prinzipien der Planung. Es enthält keine Delta Analysis
und kein Module Work Breakdown — diese Inhalte stehen in Kapitel 4 und
Kapitel 5.

### 2.1 Planning Objectives

#### PO-01 — Zweck des Implementation Plans

Der Implementation Plan überführt den genehmigten Implementation Contract in
einen ausführbaren, prüfbaren Umsetzungsplan. Er legt fest, in welcher
Reihenfolge, unter welchen Abhängigkeiten und mit welcher Vorgehensweise die
bereits genehmigten Anforderungen umgesetzt werden.

Der Plan ist ein Planungsartefakt, kein Entscheidungsartefakt. Ziele,
Anforderungen und Architektur sind vorgelagert und abschließend entschieden.

#### PO-02 — Umsetzung der genehmigten Engineering Specification

Der Plan setzt die Engineering Specification 1.0 (Revision R1, APPROVED)
vollständig und unverändert um. Verbindlicher Umfang:

| Element | Anzahl | Behandlung im Plan |
|---|---|---|
| Charter Objectives | 6 | Ziel der Rückverfolgbarkeit |
| Engineering Goals | 7 | Unverändert übernommen |
| Functional Requirements | 14 | Unverändert übernommen, Umsetzung geplant |
| Non-Functional Requirements | 10 | Unverändert übernommen, Einhaltung geplant |
| Acceptance Criteria | 29 | Unverändert übernommen, Nachweis geplant |
| Quality Gates | 8 | Unverändert übernommen, Prüfung geplant |
| Work Packages | 7 | Unverändert übernommen, Reihenfolge und Abhängigkeiten geplant |
| Deliverables | 10 | Unverändert übernommen |

Der Plan konkretisiert die Umsetzung dieser Elemente. Er verändert sie nicht.

#### PO-03 — Erfüllung der Waiver-Auflagen

Der Plan erfüllt die durch WAIVER-DEV-001 dem Implementation Plan zugewiesenen
Pflichtinhalte sowie die aus dem Independent Review übernommene Auflage zur
Performance-Messmethodik. Diese Auflagen sind Genehmigungsvoraussetzung für den
Plan selbst.

#### PO-04 — Vorbereitung der späteren Sprintplanung

Der Plan schafft die Grundlage für die Sprint Planning Phase gemäß Milestone
1.0 Charter §8 (Schritt 6). Er liefert dazu eine geschlossene Reihenfolge, eine
aufgelöste Abhängigkeitsstruktur und definierte Verifikationspunkte.

Der Plan enthält selbst **keine** Sprintplanung. Sprintzuschnitt, Kapazitäts-
und Terminplanung sind der nachgelagerten Phase zugewiesen.

---

### 2.2 Planning Principles

Die folgenden Prinzipien sind für die gesamte Planung verbindlich. Sie gelten
für jedes Kapitel dieses Dokuments und für jede spätere Revision.

| ID | Prinzip | Verbindliche Bedeutung |
|---|---|---|
| PP-01 | **Traceability First** | Jeder Planungsinhalt MUSS auf ein genehmigtes Element der Engineering Specification rückverfolgbar sein. Planungsinhalte ohne Rückverfolgbarkeit sind unzulässig und zu entfernen. Die kanonische Kette Charter Objective → Engineering Goal → Functional Requirement → Work Package → Acceptance Criterion → Quality Gate bleibt durchgängig erhalten; sie ist in Kapitel 8.4 als Verifikationskette ausgeführt und um den Nachweisknoten Evidence ergänzt. |
| PP-02 | **Baseline Preservation** | Bootstrap Baseline 1.0 ist der verbindliche Ausgangszustand. Die Baseline-Invarianten bleiben erhalten. Jede Planung, die die Baseline verändern würde, erfordert einen genehmigten ADR oder RDR vor der Umsetzung und ist als Governance-Befund zu eskalieren. |
| PP-03 | **Architecture Freeze** | Architecture Book v2.0 ist FROZEN. Die Planung bewegt sich ausschließlich innerhalb der bestehenden Architektur. Additive Erweiterungen sind nur im Rahmen der durch das Architecture Book selbst zugelassenen Grenzen planbar. Architekturänderungen sind unzulässig. |
| PP-04 | **Governance First** | Kein Planungsschritt nimmt eine noch nicht erteilte Genehmigung vorweg. Der Plan bleibt DRAFT, bis der Governance-Prozess abgeschlossen ist. Erkannte Governance-Konflikte werden eskaliert, nicht im Plan aufgelöst. |
| PP-05 | **No Scope Expansion** | Der Scope ist durch Charter und Engineering Specification abschließend definiert. Der Plan erweitert ihn nicht — weder explizit noch durch Nebenwirkungen der Umsetzungsplanung. Erkannter Zusatzbedarf wird als Future Item dokumentiert, nicht eingeplant. |
| PP-06 | **No Requirement Changes** | Functional Requirements, Non-Functional Requirements, Acceptance Criteria und Quality Gates werden weder ergänzt noch verändert, verschärft, abgeschwächt oder umgedeutet. Der Plan darf sie ausschließlich in Umsetzungsschritte übersetzen. |
| PP-07 | **Incremental Planning** | Die Planung erfolgt kapitelweise und prüfbar. Jedes Kapitel ist eigenständig auditierbar und wird abgeschlossen, bevor das nächste begonnen wird. Dies erhält die Nachvollziehbarkeit und ermöglicht unabhängige Prüfung einzelner Planungsteile. |

#### Konfliktregel

Stehen zwei Prinzipien im Einzelfall in Spannung, gilt die Reihenfolge
PP-04 → PP-03 → PP-02 → PP-01 → PP-06 → PP-05 → PP-07. Governance und
Architekturschutz haben Vorrang vor Planungsökonomie.

---

### 2.3 Planning Scope

**Dieser Abschnitt ist die abschließende und normative Definition des
Planungsscope.** Die Übersicht in Kapitel 1.3 fasst ihn gemeinsam mit den
Waiver-Pflichtabschnitten auf Dokumentebene zusammen; bei Abweichung gilt
dieser Abschnitt.

Der Implementation Plan behandelt als Planungsgegenstände ausschließlich:

| ID | Gegenstand | Planungsinhalt |
|---|---|---|
| PS-01 | **Reihenfolge** | Verbindliche Ausführungsreihenfolge der genehmigten Work Packages einschließlich Phasenbildung und Eintrittsbedingungen je Phase |
| PS-02 | **Abhängigkeiten** | Abhängigkeiten zwischen Work Packages, deren Auflösung, Reihenfolgezwänge und Parallelisierbarkeit |
| PS-03 | **Verifikation** | Vorgehen zum Nachweis der genehmigten Acceptance Criteria und Quality Gates: Prüfmethoden, Nachweisführung, Zuordnung der Prüfpunkte zur Reihenfolge |
| PS-04 | **Migration** | Vorgehen zur Überführung vom Baseline-Zustand in den Zielzustand ohne Bruch der Baseline-Invarianten und ohne Kompatibilitätsbruch |
| PS-05 | **Rollout** | Vorgehen zur Einführung des Milestone-Ergebnisses einschließlich Reihenfolge der Freigabeschritte |
| PS-06 | **Risiken** | Umsetzungsbezogene Risiken der Planung sowie deren Mitigation, abgeleitet aus den genehmigten Risiken der Engineering Specification |

Diese Gegenstände werden auf Planungsebene behandelt. Der Plan beschreibt das
**Vorgehen**, nicht die **Ausführung**. Implementierungsdetails sind kein
Bestandteil dieses Kapitels und werden — soweit der Development Standard sie
für den Plan vorschreibt — ausschließlich in den dafür vorgesehenen Kapiteln
behandelt.

---

### 2.4 Out of Scope

Die folgenden Inhalte sind ausdrücklich vom Implementation Plan ausgeschlossen:

| ID | Ausgeschlossen | Begründung |
|---|---|---|
| OS-01 | Neue Functional Requirements | Abschließend in der Engineering Specification genehmigt (PP-06) |
| OS-02 | Neue Acceptance Criteria | Abschließend in der Engineering Specification genehmigt (PP-06) |
| OS-03 | Neue Quality Gates | Abschließend in der Engineering Specification genehmigt (PP-06) |
| OS-04 | Architekturänderungen | Architecture Book v2.0 ist FROZEN (PP-03) |
| OS-05 | ADR-Änderungen und neue ADRs | Erfordern separate Governance gemäß Charter §8 (PP-04) |
| OS-06 | Coding | Der Plan autorisiert keine Implementierung (Kapitel 1.6) |
| OS-07 | Sprintimplementierung | Nachgelagerte Phase; erfordert genehmigten Plan und Sprint Planning |
| OS-08 | Runtime Changes | Nicht autorisiert (Kapitel 1.6) |

Wird während der Planung Bedarf an einem dieser Inhalte erkannt, ist der Bedarf
als Governance-Befund zu dokumentieren und zu eskalieren. Eine eigenmächtige
Aufnahme in den Plan ist unzulässig.

---

### 2.5 Planning Constraints

Alle Planungsbeschränkungen werden ausschließlich aus den folgenden
normativen Eingaben abgeleitet. Andere Quellen sind nicht zulässig.

| ID | Constraint | Ableitungsquelle |
|---|---|---|
| PC-01 | Umfang und Inhalt der Umsetzung sind durch die genehmigten Requirements, Acceptance Criteria, Quality Gates und Work Packages abschließend bestimmt. | Engineering Specification 1.0 |
| PC-02 | Jeder Planungsinhalt ist auf die Engineering Specification rückverfolgbar. | Engineering Specification 1.0 |
| PC-03 | Der Ausgangszustand der Planung ist Bootstrap Baseline 1.0. Die Baseline-Invarianten bleiben erhalten; Baseline-Änderungen erfordern separate Governance. | Bootstrap Baseline 1.0 |
| PC-04 | Die Planung bewegt sich innerhalb der eingefrorenen Architektur. Schichtmodell, Bootstrap-Phasenfolge und Plugin-Runtime-Pipeline bleiben unverändert. | Architecture Book v2.0 |
| PC-05 | Struktur, Lifecycle und Prüfvorgaben des Plans folgen den normativen Vorgaben des Development Standard. | Development Standard v1.1 |
| PC-06 | Der Plan MUSS die durch den Waiver zugewiesenen Pflichtinhalte vollständig enthalten. Der Waiver bleibt aktiv, bis der Independent Review deren Vollständigkeit bestätigt. | WAIVER-DEV-001 |
| PC-07 | Der Waiver gilt ausschließlich für Milestone 1.0 und begründet keinen Präzedenzfall für spätere Milestones. | WAIVER-DEV-001 |

Die in Kapitel 1.5 dokumentierten Governance Constraints GC-01 bis GC-07 gelten
unverändert fort und sind Bestandteil der Planungsbeschränkungen.

---

### 2.6 Success Criteria

Die folgenden Kriterien gelten für den Implementation Plan **als Dokument**.
Sie sind keine Erfolgskriterien für den Milestone — diese sind abschließend in
Charter und Engineering Specification definiert.

Der Implementation Plan 1.0 gilt als erfolgreich, wenn alle folgenden Kriterien
erfüllt sind:

| ID | Kriterium | Nachweis |
|---|---|---|
| SC-01 | **Vollständige Abdeckung aller Work Packages.** Alle 7 genehmigten Work Packages sind geplant; keines ist ausgelassen oder zusammengefasst. | Abdeckungsprüfung gegen Engineering Specification |
| SC-02 | **Vollständige Rückverfolgbarkeit.** Jeder Planungsinhalt ist auf ein genehmigtes Element der Engineering Specification zurückführbar; jedes genehmigte Element ist im Plan adressiert. | Traceability-Audit in beide Richtungen |
| SC-03 | **Vollständige Delta Analysis.** Die Delta Analysis gemäß der Waiver-Zuweisung ist vollständig und deckt den gesamten Milestone-Scope ab. | Vollständigkeitsprüfung im Independent Review |
| SC-04 | **Vollständiges Module Work Breakdown.** Das Module Work Breakdown gemäß der Waiver-Zuweisung ist für jedes Work Package vollständig. | Vollständigkeitsprüfung im Independent Review |
| SC-05 | **Vollständige Scope Verification.** Die Scope Verification ist vollständig und erfüllt die im Waiver dokumentierte Auflage. | Vollständigkeitsprüfung im Independent Review |
| SC-06 | **Definierte Performance-Messmethodik.** Die aus dem Independent Review der Engineering Specification übernommene Auflage ist erfüllt. | Prüfung gegen Finding F-004 |
| SC-07 | **Keine Verletzung der Planungsprinzipien.** PP-01 bis PP-07 sind durchgängig eingehalten; kein ausgeschlossener Inhalt gemäß 2.4 ist enthalten. | Constraint-Prüfung |
| SC-08 | **Erfolgreicher Independent Review.** Der Independent Review ist durchlaufen und alle Findings sind geschlossen. | Review Report; Correction Report |
| SC-09 | **Closing Criteria WAIVER-DEV-001 erfüllt.** Der Independent Review bestätigt die Vollständigkeit der zugewiesenen Abschnitte. | Bestätigung im Review Report |
| SC-10 | **Governance-Kette lückenlos.** Approval Record und Governance Closing Summary liegen vor; der Statuswechsel DRAFT → APPROVED ist dokumentiert. | Governance-Artefakte |

Erst nach Erfüllung sämtlicher Kriterien SC-01 bis SC-10 ist der Plan
genehmigungsfähig. Vorher entsteht keine Implementierungsautorisierung.

---

## 3. Baseline Verification

Dieses Kapitel beantwortet ausschließlich die Frage: **Was ist der genehmigte
Ausgangszustand?**

Es dokumentiert den verbindlichen Referenzzustand, gegen den die spätere Delta
Analysis geführt wird, und legt fest, welche Eigenschaften dieses Zustands vor
Beginn der Umsetzung zu bestätigen sind. Die Delta Analysis selbst ist nicht
Bestandteil dieses Kapitels.

**Darstellungshinweis:** Die zu bestätigende Public API wird über Paket- und
Symbolnamen benannt, weil sie ausschließlich in dieser Form prüfbar ist.
Dateireferenzen, Implementierungsdetails und Aufgabenzuschnitte sind nicht
Bestandteil dieses Kapitels.

---

### 3.1 Referenz auf Bootstrap Baseline 1.0

| Eigenschaft | Wert |
|---|---|
| **Baseline ID** | BOOTSTRAP-BASELINE-1.0 |
| **Status** | APPROVED |
| **Genehmigungsdatum** | 2026-08-01 |
| **Autorität** | Bootstrap Modularization Final Audit |
| **Grundlage** | RDR-001 Bootstrap Modularization (APPROVED) |
| **Geltung** | Verbindliche technische Baseline für alle Bootstrap-Entwicklungen ab Milestone 1.0 |

Bootstrap Baseline 1.0 ist gemäß Milestone 1.0 Charter §8 die verbindliche
technische Baseline für sämtliche Engineering-Arbeiten des Milestone 1.0. Die
Engineering Specification 1.0 hat diese Baseline in ihrer Baseline-Verifikation
bestätigt.

Die Baseline ist damit für diesen Plan **gesetzt und nicht verhandelbar**. Sie
wird in diesem Kapitel referenziert und bestätigt, nicht neu bewertet.

#### Baseline-Kenndaten

| Eigenschaft | Wert | Herkunft |
|---|---|---|
| Release Tag | `v0.9.0` | Engineering Specification 1.0, Baseline-Verifikation |
| Application Version | `0.9.0` | Engineering Specification 1.0, Baseline-Verifikation |
| SDK Version | `0.9.0` | Engineering Specification 1.0, Baseline-Verifikation |
| SDK API Version | `1.0.0` | Engineering Specification 1.0, Baseline-Verifikation |
| Core Runtime | `v1.0.0` | Engineering Specification 1.0, Baseline-Verifikation |
| Architecture Freeze | Architecture Book v2.0, APPROVED / FROZEN (2026-07-26) | Engineering Specification 1.0, Baseline-Verifikation |
| Regressionsbasis | 1019 Tests bestanden, 0 Regressionen | Bootstrap Baseline 1.0, Regression Baseline |
| Import-Kompatibilität | Verifiziert | Bootstrap Baseline 1.0, Regression Baseline |
| Consumer-Kompatibilität | Verifiziert | Bootstrap Baseline 1.0, Regression Baseline |

---

### 3.2 Verifikation des Ist-Zustands

#### Zweck

Die Baseline-Verifikation stellt vor Beginn der Umsetzungsplanung sicher, dass
der dokumentierte Baseline-Zustand mit dem tatsächlichen Ist-Zustand
übereinstimmt. Ohne diese Übereinstimmung ist eine belastbare Delta Analysis
nicht möglich — die Differenz wäre gegen einen unbestätigten Ausgangszustand
gebildet.

#### Verifikationsstufen

| Stufe | Bedeutung |
|---|---|
| **Dokumentenverifiziert** | Durch ein genehmigtes Governance-Dokument bestätigt. Keine erneute Prüfung erforderlich. |
| **Zu bestätigen** | Vor Beginn der Delta Analysis gegen den Ist-Zustand zu prüfen und zu protokollieren. |

#### Verifikationsstatus

| Bereich | Stufe | Grundlage bzw. Prüfweg |
|---|---|---|
| Baseline-Kenndaten (Versionen, Tags, Architecture Freeze) | Dokumentenverifiziert | Engineering Specification 1.0, Baseline-Verifikation |
| Regressionsbasis (1019 Tests, 0 Regressionen) | Dokumentenverifiziert | Bootstrap Baseline 1.0, Regression Baseline |
| Baseline-Invarianten (3.3) | Zu bestätigen | Strukturprüfung gegen die Baseline-Dokumentation |
| Public API (3.4) | Zu bestätigen | Abgleich der exportierten Symbolmenge gegen die Baseline-Dokumentation |
| Bootstrap-Phasen (3.5) | Zu bestätigen | Abgleich der Phasen- und Stage-Reihenfolge gegen die Baseline-Dokumentation |
| Plugin-Pipeline (3.6) | Zu bestätigen | Abgleich der Pipeline-Reihenfolge gegen Baseline und ADRs |
| Governance-Invarianten (3.7) | Zu bestätigen | Statusprüfung der normativen Eingaben |

#### Verfahrensregeln

1. Die Bestätigung erfolgt vor Beginn der Delta Analysis.
2. Jede Bestätigung wird mit Ergebnis protokolliert.
3. Wird eine Abweichung zwischen dokumentierter Baseline und Ist-Zustand
   festgestellt, ist die Planung zu unterbrechen und die Abweichung als
   Governance-Befund zu eskalieren. Eine Anpassung der Baseline durch diesen
   Plan ist unzulässig (PP-02, PP-04).
4. Die Verifikation ist eine Feststellung des Zustands. Sie umfasst keine
   Änderung, keine Korrektur und keine Implementierung.

---

### 3.3 Zu bestätigende Baseline-Invarianten

Die folgenden sieben architektonischen Invarianten sind Bestandteil der
genehmigten Baseline. Sie sind zu bestätigen und über den gesamten Milestone
zu bewahren.

| ID | Invariante | Bestätigungsgegenstand |
|---|---|---|
| BI-01 | **Deklarative Paket-Fassade** | Die Paket-Fassade enthält ausschließlich Imports und die Export-Deklaration, keine Logik. |
| BI-02 | **Azyklischer Import-Graph** | Die internen Module bilden einen gerichteten azyklischen Graphen in der durch die Baseline festgelegten Richtung. |
| BI-03 | **BootstrapManager als Orchestrator** | Der `BootstrapManager` ist der einzige Einstiegspunkt der Bootstrap-Ausführung; Stages werden nicht direkt aufgerufen. |
| BI-04 | **`default_stages()` bewahrt die Stage-Reihenfolge** | Die Funktion liefert eine deterministische, geordnete Sequenz aller Stages. |
| BI-05 | **StartupPhase-Reihenfolge bewahrt** | Die Phasenwerte INITIALIZE (1) → LOAD_PLUGINS (2) → LOAD_RESOURCES (3) → FINALIZE (4) sind unverändert. |
| BI-06 | **Plugin-Runtime-Pipeline bewahrt** | Die sicherheitskritische Pipeline-Reihenfolge ist unverändert (Detail in 3.6). |
| BI-07 | **Keine internen Imports durch Consumer** | Consumer importieren ausschließlich über die Paket-Fassade, nicht aus internen Modulen. |

Änderungen an BI-01 bis BI-07 erfordern eine genehmigte Governance-Entscheidung
in Form eines ADR oder RDR vor der Umsetzung (Bootstrap Baseline 1.0, Change
Control).

---

### 3.4 Zu bestätigende Public API

#### API-01 — Öffentliche Exports (22 Symbole)

Die stabile Paket-Fassade `app.bootstrap` exportiert die folgenden
zweiundzwanzig Symbole. Die Vollständigkeit und Unverändertheit dieser Menge
ist zu bestätigen.

| Gruppe | Symbole | Anzahl |
|---|---|---|
| Types & Protocols | `BootstrapContext`, `BootstrapError`, `BootstrapStage`, `StartupPhase`, `RejectionCode`, `ValidationDiagnostic` | 6 |
| Manager & Konfiguration | `BootstrapManager`, `default_stages()` | 2 |
| INITIALIZE-Phase Stages | `EnvironmentStage`, `ConfigurationStage`, `LoggingStage`, `DatabaseStage`, `RegistryStage`, `ThemeStage`, `SchedulerStage` | 7 |
| Plugin-Pipeline Stages | `PluginDiscoveryStage`, `PluginSecurityStage`, `PluginActivationStage`, `PluginRuntimePool` | 4 |
| Late-Phase Stages | `ResourceStage`, `DeveloperToolsStage`, `DependencyInjectionStage` | 3 |
| **Summe** | | **22** |

#### API-02 — Interne Re-Exports (2 Symbole)

`_require` und `_validate_for_activation` werden re-exportiert, sind **nicht**
Bestandteil der öffentlichen Export-Deklaration und gelten **nicht** als stabile
API. Zu bestätigen ist, dass dieser Status unverändert ist.

#### API-03 — Consumer-Import-Kompatibilität

Zu bestätigen ist, dass alle Consumer ausschließlich über die Paket-Fassade
importieren. Direkte Imports aus internen Modulen sind nicht Teil der stabilen
API und dürfen nicht vorausgesetzt werden.

#### API-04 — Änderungsschutz

Jede Änderung an der öffentlichen Exportmenge, an der Paketstruktur, an der
`BootstrapManager`-Signatur oder an der Zusammensetzung von `default_stages()`
erfordert eine genehmigte Governance-Entscheidung vor der Umsetzung (Bootstrap
Baseline 1.0, Change Control).

---

### 3.5 Zu bestätigende Bootstrap-Phasen

Die Phasensequenz der Baseline ist unverändert zu bestätigen:

```
INITIALIZE
    EnvironmentStage
    ConfigurationStage
    LoggingStage
    DatabaseStage
    RegistryStage
    ThemeStage
    SchedulerStage
         ↓
LOAD_PLUGINS
    PluginDiscoveryStage
    PluginSecurityStage
         ↓
LOAD_RESOURCES
    ResourceStage
         ↓
FINALIZE
    PluginActivationStage
    DeveloperToolsStage
    DependencyInjectionStage
```

| ID | Bestätigungsgegenstand |
|---|---|
| BP-01 | Die vier Phasen und ihre Reihenfolge INITIALIZE → LOAD_PLUGINS → LOAD_RESOURCES → FINALIZE sind unverändert. |
| BP-02 | Die Zuordnung jeder Stage zu ihrer Phase ist unverändert. |
| BP-03 | Die Reihenfolge der Stages innerhalb jeder Phase ist unverändert. |
| BP-04 | Die Ausführung erfolgt ausschließlich über den `BootstrapManager` (BI-03). |

Die Phasensequenz ist zugleich in der Architekturreferenz und in der
Engineering Specification verankert. Eine Änderung berührt damit sowohl den
Architecture Freeze als auch die Baseline Change Control.

---

### 3.6 Zu bestätigende Plugin-Pipeline

Die Plugin-Runtime-Pipeline ist sicherheitskritisch. Ihre Reihenfolge ist
unverändert zu bestätigen:

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

| ID | Bestätigungsgegenstand | Normative Verankerung |
|---|---|---|
| PL-01 | Discovery erfolgt manifest-only; die Foundation importiert keinen Plugin-Code vor der Validierung. | Architecture Book v2.0 |
| PL-02 | Integrity Validation erfolgt vor jeder weiteren Verarbeitung. | ADR-005 |
| PL-03 | Permission Authorization erfolgt nach Integrity und vor Dependency Resolution. | ADR-006 |
| PL-04 | Dependency Resolution erfolgt vor der Aktivierung. | ADR-007 |
| PL-05 | Activation erfolgt ausschließlich nach vollständig erfolgreicher Sicherheitsprüfung. | ADR-005, ADR-006, ADR-007, ADR-011 |

Die Reihenfolge darf nicht umgestellt, verkürzt oder umgangen werden. Sie ist
Bestandteil der Baseline-Invariante BI-06 und zugleich sicherheitsrelevant.

---

### 3.7 Zu bestätigende Governance-Invarianten

Die folgenden Governance-Zustände bilden den genehmigten Ausgangszustand der
Planung. Ihre Gültigkeit ist zu bestätigen.

| ID | Governance-Invariante | Erwarteter Zustand |
|---|---|---|
| GI-01 | Architecture Book v2.0 | APPROVED / FROZEN — unverändert |
| GI-02 | Development Standard v1.1 | APPROVED — unverändert |
| GI-03 | Milestone 1.0 Charter | APPROVED — unverändert |
| GI-04 | Engineering Specification 1.0, Revision R1 | APPROVED — unverändert, keine offenen Findings |
| GI-05 | Bootstrap Baseline 1.0 | APPROVED — unverändert |
| GI-06 | RDR-001 Bootstrap Modularization | APPROVED — unverändert |
| GI-07 | ADR-005 Plugin Integrity Validation | APPROVED — unverändert |
| GI-08 | ADR-006 Plugin Permission Model | APPROVED — unverändert |
| GI-09 | ADR-007 Plugin Dependency Resolution | APPROVED — unverändert |
| GI-10 | ADR-011 SDK-Host-Integration | APPROVED — unverändert |
| GI-11 | WAIVER-DEV-001 | APPROVED — aktiv; Closing Criteria offen und durch diesen Plan zu erfüllen |
| GI-12 | Autorisierungsgrenze | Ausschließlich Implementation Plan 1.0 (DRAFT) autorisiert; Produktionscode nicht autorisiert |

#### Bekannte Bezeichnungsdifferenz

Bootstrap Baseline 1.0 führt ADR-011 in ihrer Referenztabelle unter der
Bezeichnung „Plugin Lifecycle Stages". Die verbindliche Bezeichnung des ADR
lautet „SDK-Host-Integration"; Engineering Specification 1.0 und Milestone 1.0
Charter verwenden diese korrekte Bezeichnung.

**Einstufung:** Es handelt sich um eine **redaktionelle Feststellung**, nicht
um einen Governance-Befund im Sinne von AP-01 und GV-08.

| Prüfpunkt | Feststellung |
|---|---|
| Inhaltlicher Widerspruch | Keiner. Referenzierte ADR-Nummer, Geltung und Verbindlichkeit sind in allen Dokumenten identisch. |
| Wirkung auf Planungsinhalte | Keine. Kein Delta, kein Module-Work-Breakdown-Eintrag und kein Nachweis hängt von der Bezeichnung ab. |
| Wirkung auf GI-10 | Keine. GI-10 bestätigt ADR-011 nach Nummer und Status, nicht nach Titel. |
| Wirkung auf AP-01 / GV-08 | Keine. Die Feststellung erzeugt keinen Findings-Status und keinen Entscheidungsbedarf innerhalb dieses Milestones. |
| Registerführung | Keine Aufnahme in das konsolidierte Register (Kapitel 11.11). Eine Registrierung wäre ohne Risikogehalt und würde die Registerlage verzerren (RP-03). |

Die Nachführung der Bezeichnung betrifft die Bootstrap Baseline und liegt
außerhalb der Autorisierungsgrenze dieses Plans (PP-02, PP-04). Sie ist hier
festgehalten, damit die Differenz bei einer künftigen Fortschreibung der
Baseline nicht erneut ermittelt werden muss.

---

### 3.8 Baseline Confirmation Statement

| Feststellung | Inhalt |
|---|---|
| **Genehmigter Ausgangszustand** | Bootstrap Baseline 1.0 (APPROVED, 2026-08-01) auf Release Tag `v0.9.0` |
| **Bestätigungsumfang** | BI-01..BI-07, API-01..API-04, BP-01..BP-04, PL-01..PL-05, GI-01..GI-12 |
| **Bestätigungszeitpunkt** | Vor Beginn der Delta Analysis |
| **Wirkung** | Der bestätigte Zustand ist der Referenzpunkt jeder Differenzbildung im weiteren Verlauf dieses Plans |
| **Bei Abweichung** | Unterbrechung der Planung, Eskalation als Governance-Befund; keine Anpassung der Baseline durch diesen Plan |

Dieses Kapitel enthält bewusst keine Delta Analysis, kein Module Work
Breakdown, keine Implementierungsreihenfolge, keine Work Packages, keine
Dateireferenzen und keine Aufgabenlisten.

---

## 4. Delta Analysis

### 4.1 Zweck und Abgrenzung

Die Delta Analysis beantwortet ausschließlich die Frage:

> **Welche Unterschiede bestehen zwischen der bestätigten Baseline (Kapitel 3)
> und dem durch die Engineering Specification 1.0 definierten Zielzustand?**

Sie beschreibt Unterschiede auf Ebene der **genehmigten Anforderungen**, nicht
auf Codeebene. Sie enthält **keine Lösungsbeschreibung**.

Nicht beantwortet werden: wie umgesetzt wird, in welchem Modul, in welcher
Datei, in welcher Klasse, in welcher Reihenfolge und in welchem Sprint. Die
Modul- und Dateizuordnung erfolgt in Kapitel 5, die Reihenfolge in Kapitel 6,
die Umsetzungsgrundsätze in Kapitel 7; die Sprintzuordnung ist der Sprint
Planning Phase zugewiesen (Charter §8, Schritt 6).

Dieses Kapitel ist der erste durch WAIVER-DEV-001 dem Implementation Plan
zugewiesene Pflichtabschnitt.

---

### 4.2 Methodik

#### Delta-Ermittlung

| Schritt | Inhalt | Quelle |
|---|---|---|
| 1 | Feststellung des bestätigten Ausgangszustands | Kapitel 3 (Baseline Verification) |
| 2 | Feststellung des genehmigten Zielzustands | Engineering Specification 1.0 — Functional Requirements, Non-Functional Requirements |
| 3 | Bildung der Differenz je genehmigtem Zielelement | Engineering Specification 1.0 — Gap Assessment |
| 4 | Klassifikation der Änderungsart | Klassifikation gemäß 4.3 |
| 5 | Zuordnung zu Engineering Goals, Functional Requirements und Work Packages | Engineering Specification 1.0 — Traceability |
| 6 | Bewertung der Traceability-Auswirkung | Planungsprinzip PP-01 |

#### Regeln

1. Jedes Delta ist auf mindestens ein genehmigtes Element der Engineering
   Specification rückverfolgbar (PP-01).
2. Kein Delta führt neue Anforderungen ein (PP-06). Deltas beschreiben
   ausschließlich die Differenz zu bereits genehmigten Zielzuständen.
3. Bereiche ohne Delta werden ausdrücklich als Null-Delta ausgewiesen (4.7).
   Ein nicht genanntes Element gilt nicht als geprüft.
4. Deltas werden ohne Lösungsvorschlag formuliert. Die Formulierung endet an
   der Feststellung des Unterschieds.
5. Die Deltabildung setzt die Bestätigung der Baseline gemäß Kapitel 3 voraus.
   Ohne diese Bestätigung ist die Analyse vorläufig.

---

### 4.3 Klassifikation der Änderungsarten

| Art | Definition |
|---|---|
| **Erweiterung** | Eine in der Baseline vorhandene Fähigkeit wird in ihrem Umfang oder ihrer Bestimmtheit vergrößert. Der bestehende Vertrag bleibt erhalten. |
| **Ergänzung** | Eine im Zielzustand geforderte Fähigkeit ist in der Baseline nicht vorhanden und wird additiv hinzugefügt. |
| **Verifikation** | Es besteht keine funktionale Differenz. Gefordert ist der Nachweis, dass eine Eigenschaft der Baseline erhalten bleibt. |
| **Aktualisierung** | Ein dokumentierter Zustand weicht vom implementierten Zustand ab und ist nachzuführen. Keine funktionale Differenz. |

Die vier Arten sind disjunkt. Jedem Delta ist genau eine Art zugeordnet.

---

### 4.4 Delta-Übersicht

| ID | Delta | Art | EG | FR | WP |
|---|---|---|---|---|---|
| DA-001 | Bestimmtheit der Lifecycle-Zustandsmaschine | Erweiterung | EG-001 | FR-001 | WP-001 |
| DA-002 | Formalisierung des Ablehnungsverhaltens bei Zustandsübergängen | Ergänzung | EG-001 | FR-002 | WP-001 |
| DA-003 | Vollständige Beschreibung und Abrufbarkeit der Host-Dienste | Ergänzung | EG-002 | FR-003 | WP-002 |
| DA-004 | Formale Definition der Erweiterungspunkte | Ergänzung | EG-002 | FR-004 | WP-002 |
| DA-005 | Konsolidierung der Vorgaben für Plugin-Autoren | Ergänzung | EG-004 | FR-005 | WP-003 |
| DA-006 | Strukturierung des Ablehnungs-Feedbacks der Pipeline | Erweiterung | EG-004 | FR-006 | WP-003 |
| DA-007 | Plugin-spezifische Diagnoseinformationen | Ergänzung | EG-005 | FR-007 | WP-004 |
| DA-008 | Erweiterbarkeit des Observability-Systems | Erweiterung | EG-005 | FR-008 | WP-004 |
| DA-009 | Definiertes Wiederherstellungsverhalten bei Fehlern | Ergänzung | EG-006 | FR-009 | WP-005 |
| DA-010 | Isolation von Plugin-Ausfällen | Ergänzung | EG-006 | FR-010 | WP-005 |
| DA-011 | Vollständigkeit der SDK-Dokumentation | Aktualisierung | EG-007 | FR-011 | WP-007 |
| DA-012 | Aktualität der Architekturdokumentation | Aktualisierung | EG-007 | FR-012 | WP-007 |
| DA-013 | Nachweis der Additivität aller Erweiterungen | Verifikation | EG-003 | FR-013 | WP-006 |
| DA-014 | Nachweis der Consumer-Kompatibilität | Verifikation | EG-003 | FR-014 | WP-006 |
| DA-015 | Erweiterung der Testbasis auf den Zielzustand | Erweiterung | — | — | WP-001..WP-007 |

15 Deltas. DA-001 bis DA-014 sind eineindeutig den 14 Functional Requirements
zugeordnet. DA-015 ist kein FR-Delta und wird in 4.5 gesondert begründet.

---

### 4.5 Delta-Katalog

#### DA-001 — Bestimmtheit der Lifecycle-Zustandsmaschine

| Feld | Inhalt |
|---|---|
| Baseline-Zustand | Bootstrap-Phasensequenz und Stage-Reihenfolge sind deterministisch und stabil (BP-01..BP-04). Die Lifecycle-Übergänge der Anwendungsplattform sind nicht vollständig definiert. |
| Zielzustand | FR-001 — Jeder Zustandsübergang folgt einer vollständig definierten Zustandsmaschine; kein Übergang ohne explizite Berechtigung. |
| Art der Änderung | Erweiterung |
| Engineering Goals | EG-001 |
| Functional Requirements | FR-001 |
| Work Packages | WP-001 |
| Traceability-Auswirkung | Keine Änderung der Kette CO-001 → EG-001 → FR-001 → WP-001. Der Nachweis erfolgt über die dem FR-001 zugeordneten Acceptance Criteria. |
| Berührte Baseline-Invarianten | BI-05 (Phasenreihenfolge) ist zu bewahren; das Delta liegt oberhalb der Phasensequenz. |

#### DA-002 — Formalisierung des Ablehnungsverhaltens bei Zustandsübergängen

| Feld | Inhalt |
|---|---|
| Baseline-Zustand | Ablehnungsverhalten bei unzulässigen Zustandsübergängen ist nicht formalisiert. |
| Zielzustand | FR-002 — Die Menge zulässiger Übergänge ist vollständig bestimmt; nicht enthaltene Übergänge werden mit definiertem Ablehnungsergebnis zurückgewiesen. |
| Art der Änderung | Ergänzung |
| Engineering Goals | EG-001 |
| Functional Requirements | FR-002 |
| Work Packages | WP-001 |
| Traceability-Auswirkung | Keine Änderung der Kette CO-001 → EG-001 → FR-002 → WP-001. |
| Berührte Baseline-Invarianten | Keine. Additive Ergänzung ohne Eingriff in BI-01..BI-07. |

#### DA-003 — Vollständige Beschreibung und Abrufbarkeit der Host-Dienste

| Feld | Inhalt |
|---|---|
| Baseline-Zustand | Die zentrale Dienstregistrierung ist operativ. Die vom Host bereitgestellten Dienste sind nicht vollständig beschrieben und nicht programmatisch abrufbar. |
| Zielzustand | FR-003 — Host-Dienste sind zentral vollständig beschrieben und programmatisch abrufbar. |
| Art der Änderung | Ergänzung |
| Engineering Goals | EG-002 |
| Functional Requirements | FR-003 |
| Work Packages | WP-002 |
| Traceability-Auswirkung | Keine Änderung der Kette CO-003 → EG-002 → FR-003 → WP-002. |
| Berührte Baseline-Invarianten | Keine. Die Dienstregistrierung selbst bleibt unverändert. |

#### DA-004 — Formale Definition der Erweiterungspunkte

| Feld | Inhalt |
|---|---|
| Baseline-Zustand | Erweiterungspunkte für Plugins sind nicht formal definiert. |
| Zielzustand | FR-004 — Plugins erweitern die Plattform über definierte Erweiterungspunkte, ohne bestehende Verträge zu verändern. |
| Art der Änderung | Ergänzung |
| Engineering Goals | EG-002 |
| Functional Requirements | FR-004 |
| Work Packages | WP-002 |
| Traceability-Auswirkung | Keine Änderung der Kette CO-002 → EG-002 → FR-004 → WP-002. Abhängigkeit zu DA-013 (Additivitätsnachweis). |
| Berührte Baseline-Invarianten | BI-07 (Import ausschließlich über die Paket-Fassade) ist zu bewahren. |

#### DA-005 — Konsolidierung der Vorgaben für Plugin-Autoren

| Feld | Inhalt |
|---|---|
| Baseline-Zustand | Vorgaben für Plugin-Autoren sind über mehrere Quellen verstreut; es existiert keine einzelne definierte Stelle. |
| Zielzustand | FR-005 — Vollständige, widerspruchsfreie Vorgaben an einer einzigen definierten Stelle. |
| Art der Änderung | Ergänzung |
| Engineering Goals | EG-004 |
| Functional Requirements | FR-005 |
| Work Packages | WP-003 |
| Traceability-Auswirkung | Keine Änderung der Kette CO-004 → EG-004 → FR-005 → WP-003. Inhaltliche Überschneidung mit DA-011 ist bei der Verifikation zu berücksichtigen; die FR-Zuordnung bleibt disjunkt. |
| Berührte Baseline-Invarianten | Keine. |

#### DA-006 — Strukturierung des Ablehnungs-Feedbacks der Pipeline

| Feld | Inhalt |
|---|---|
| Baseline-Zustand | Strukturierte Ablehnungsgründe und Validierungsdiagnostik sind als öffentliche Typen vorhanden (API-01). Das Feedback weist die auslösende Pipelinestufe und das verletzte Kriterium nicht durchgängig aus. |
| Zielzustand | FR-006 — Bei Ablehnung werden auslösende Pipelinestufe und verletztes Kriterium ausgewiesen. |
| Art der Änderung | Erweiterung |
| Engineering Goals | EG-004 |
| Functional Requirements | FR-006 |
| Work Packages | WP-003 |
| Traceability-Auswirkung | Keine Änderung der Kette CO-004 → EG-004 → FR-006 → WP-003. |
| Berührte Baseline-Invarianten | BI-06 und PL-01..PL-05: Die Pipeline-Reihenfolge bleibt unverändert. Das Delta betrifft ausschließlich das Ergebnisformat der Ablehnung, nicht den Ablauf. |

#### DA-007 — Plugin-spezifische Diagnoseinformationen

| Feld | Inhalt |
|---|---|
| Baseline-Zustand | Grundlegende Metrik- und Gesundheitsprüfungsverträge sind vorhanden. Plugin-spezifische Diagnostik fehlt. |
| Zielzustand | FR-007 — Strukturierte Diagnoseinformationen über den Zustand der Plugin-Runtime. |
| Art der Änderung | Ergänzung |
| Engineering Goals | EG-005 |
| Functional Requirements | FR-007 |
| Work Packages | WP-004 |
| Traceability-Auswirkung | Keine Änderung der Kette CO-005 → EG-005 → FR-007 → WP-004. |
| Berührte Baseline-Invarianten | Keine. |

#### DA-008 — Erweiterbarkeit des Observability-Systems

| Feld | Inhalt |
|---|---|
| Baseline-Zustand | Das Observability-System ist vorhanden, aber nicht um plugin-spezifische Metriken und Gesundheitsprüfungen erweiterbar. |
| Zielzustand | FR-008 — Das Observability-System ist um plugin-spezifische Metriken und Gesundheitsprüfungen erweiterbar. |
| Art der Änderung | Erweiterung |
| Engineering Goals | EG-005 |
| Functional Requirements | FR-008 |
| Work Packages | WP-004 |
| Traceability-Auswirkung | Keine Änderung der Kette CO-005 → EG-005 → FR-008 → WP-004. Abhängigkeit zu DA-013 (Additivitätsnachweis). |
| Berührte Baseline-Invarianten | Keine. |

#### DA-009 — Definiertes Wiederherstellungsverhalten bei Fehlern

| Feld | Inhalt |
|---|---|
| Baseline-Zustand | Ein definiertes Wiederherstellungsverhalten bei Fehlern in Plattformkomponenten oder Plugins ist nicht durchgängig festgelegt. |
| Zielzustand | FR-009 — Fehler führen zu einem definierten Wiederherstellungsverhalten, nicht zu einem undefinierten Zustand. |
| Art der Änderung | Ergänzung |
| Engineering Goals | EG-006 |
| Functional Requirements | FR-009 |
| Work Packages | WP-005 |
| Traceability-Auswirkung | Keine Änderung der Kette CO-001 → EG-006 → FR-009 → WP-005. |
| Berührte Baseline-Invarianten | BI-03 (Orchestrator als einziger Einstiegspunkt) ist zu bewahren. |

#### DA-010 — Isolation von Plugin-Ausfällen

| Feld | Inhalt |
|---|---|
| Baseline-Zustand | Die Auswirkung eines einzelnen Plugin-Ausfalls auf Plattform und andere Plugins ist nicht abschließend begrenzt. |
| Zielzustand | FR-010 — Der Ausfall eines einzelnen Plugins beeinträchtigt weder die Plattform noch andere Plugins. |
| Art der Änderung | Ergänzung |
| Engineering Goals | EG-006 |
| Functional Requirements | FR-010 |
| Work Packages | WP-005 |
| Traceability-Auswirkung | Keine Änderung der Kette CO-005 → EG-006 → FR-010 → WP-005. |
| Berührte Baseline-Invarianten | BI-06 und PL-05: Die Aktivierung erfolgt weiterhin ausschließlich nach vollständig erfolgreicher Sicherheitsprüfung. |

#### DA-011 — Vollständigkeit der SDK-Dokumentation

| Feld | Inhalt |
|---|---|
| Baseline-Zustand | Die SDK-Dokumentation ist nicht vollständig; öffentliche APIs, Erweiterungspunkte und Lifecycle-Verträge sind nicht durchgängig beschrieben. |
| Zielzustand | FR-011 — Vollständige und aktuelle Beschreibung aller öffentlichen APIs, Erweiterungspunkte und Lifecycle-Verträge. |
| Art der Änderung | Aktualisierung |
| Engineering Goals | EG-007 |
| Functional Requirements | FR-011 |
| Work Packages | WP-007 |
| Traceability-Auswirkung | Keine Änderung der Kette CO-004 → EG-007 → FR-011 → WP-007. Abhängig vom Endzustand der Deltas DA-003, DA-004 und DA-008. |
| Berührte Baseline-Invarianten | Keine. Die dokumentierte öffentliche API bleibt gemäß API-01..API-04 unverändert. |

#### DA-012 — Aktualität der Architekturdokumentation

| Feld | Inhalt |
|---|---|
| Baseline-Zustand | Die technische Architekturdokumentation bildet den implementierten Stand nicht vollständig ab. |
| Zielzustand | FR-012 — Die Architekturdokumentation reflektiert den implementierten Stand zum Zeitpunkt des Milestone-Abschlusses. |
| Art der Änderung | Aktualisierung |
| Engineering Goals | EG-007 |
| Functional Requirements | FR-012 |
| Work Packages | WP-007 |
| Traceability-Auswirkung | Keine Änderung der Kette CO-006 → EG-007 → FR-012 → WP-007. |
| Berührte Baseline-Invarianten | GI-01: Architecture Book v2.0 ist APPROVED / FROZEN. Das Delta betrifft die Aktualität der Dokumentation, nicht den Inhalt der eingefrorenen Architekturreferenz. Die Abgrenzung zwischen aktualisierbarer technischer Dokumentation und eingefrorener Architekturreferenz ist bei der Umsetzung verbindlich einzuhalten (PP-03) und gemäß Kapitel 8 nachzuweisen (EV-D04, GV-03). |

#### DA-013 — Nachweis der Additivität aller Erweiterungen

| Feld | Inhalt |
|---|---|
| Baseline-Zustand | Die öffentliche API ist gemäß API-01..API-04 dokumentiert und stabil. Ein Nachweis der Additivität für die Erweiterungen dieses Milestones existiert naturgemäß noch nicht. |
| Zielzustand | FR-013 — Alle Erweiterungen erfolgen additiv; keine Erweiterung entfernt, benennt um oder verändert das Verhalten bestehender öffentlicher Symbole. |
| Art der Änderung | Verifikation |
| Engineering Goals | EG-003 |
| Functional Requirements | FR-013 |
| Work Packages | WP-006 |
| Traceability-Auswirkung | Keine Änderung der Kette CO-006 → EG-003 → FR-013 → WP-006. Querbezug zu allen Deltas der Arten Erweiterung und Ergänzung; FR-013 ist ausdrücklich nicht scope-eröffnend. |
| Berührte Baseline-Invarianten | API-01..API-04 und BI-01..BI-07 sind vollständig zu bewahren. |

#### DA-014 — Nachweis der Consumer-Kompatibilität

| Feld | Inhalt |
|---|---|
| Baseline-Zustand | Import- und Consumer-Kompatibilität sind zum Baseline-Stand verifiziert. Ein Nachweis für den Zielzustand existiert noch nicht. |
| Zielzustand | FR-014 — Bestehende Plugins gegen SDK API 1.0.0 funktionieren nach Milestone-Abschluss ohne Änderung. |
| Art der Änderung | Verifikation |
| Engineering Goals | EG-003 |
| Functional Requirements | FR-014 |
| Work Packages | WP-006 |
| Traceability-Auswirkung | Keine Änderung der Kette CO-006 → EG-003 → FR-014 → WP-006. |
| Berührte Baseline-Invarianten | API-03 (Consumer-Import-Kompatibilität) ist zu bewahren; SDK API 1.0.0 bleibt unverändert. |

#### DA-015 — Erweiterung der Testbasis auf den Zielzustand

| Feld | Inhalt |
|---|---|
| Baseline-Zustand | 1019 Tests bestanden, 0 Regressionen (Regressionsbasis gemäß 3.1). |
| Zielzustand | Erweiterung der Testbasis auf die im Zielzustand hinzukommenden Anforderungen bei unveränderter Regressionsfreiheit. |
| Art der Änderung | Erweiterung |
| Engineering Goals | — (kein eigenes Engineering Goal) |
| Functional Requirements | — (kein eigener Functional Requirement) |
| Work Packages | WP-001 bis WP-007 (querschnittlich) |
| Traceability-Auswirkung | Rückverfolgbar auf NFR-005 und QG-007 der Engineering Specification sowie auf die Scope-Kategorie Testabdeckung. Kein FR-Bezug, da die Engineering Specification die Testabdeckung ausdrücklich über NFR und Quality Gate führt, nicht über einen Functional Requirement. |
| Begründung der Aufnahme | Ohne DA-015 wäre die Delta Analysis gegenüber den sechs Scope-Kategorien der Engineering Specification unvollständig (4.6). |

---

### 4.6 Abdeckung der Scope-Kategorien

| Scope-Kategorie | Deltas | Abdeckung |
|---|---|---|
| Plattform-Härtung | DA-001, DA-002, DA-009, DA-010 | Vollständig |
| Host-Service-Erweiterung | DA-003, DA-004 | Vollständig |
| Plugin-Ökosystem | DA-005, DA-006 | Vollständig |
| Observability | DA-007, DA-008 | Vollständig |
| Testabdeckung | DA-015 | Vollständig |
| Dokumentation | DA-011, DA-012 | Vollständig |
| Vertragserhaltung (querschnittlich) | DA-013, DA-014 | Vollständig |

Alle sechs Scope-Kategorien der Engineering Specification sind durch mindestens
ein Delta abgedeckt. Die vertragserhaltenden Deltas DA-013 und DA-014 sind
querschnittlich und keiner einzelnen Kategorie zugeordnet.

---

### 4.7 Null-Deltas (Erhaltungsbereiche)

Die folgenden Bereiche weisen **kein Delta** auf. Sie sind Erhaltungsbereiche
und werden ausdrücklich als unverändert ausgewiesen.

| Bereich | Feststellung | Schutz |
|---|---|---|
| Bootstrap-Paketstruktur | Kein Delta | BI-01, BI-02, Change Control |
| Öffentliche Exportmenge (22 Symbole) | Kein Delta | API-01, API-04 |
| Status der internen Re-Exports | Kein Delta | API-02 |
| Consumer-Import-Kompatibilität | Kein Delta | API-03, DA-014 (Nachweis) |
| Bootstrap-Phasenreihenfolge | Kein Delta | BI-05, BP-01..BP-04 |
| Stage-Zuordnung und Stage-Reihenfolge | Kein Delta | BP-02, BP-03 |
| Plugin-Runtime-Pipeline (Reihenfolge) | Kein Delta | BI-06, PL-01..PL-05 |
| Architektur (Schichtmodell, Architecture Book v2.0) | Kein Delta | GI-01, PP-03 |
| SDK API 1.0.0 | Kein Delta | DA-014, PP-06 |
| ADR-005, ADR-006, ADR-007, ADR-011 | Kein Delta | GI-07..GI-10 |
| Charter Objectives, Engineering Goals, Functional Requirements, Acceptance Criteria, Quality Gates | Kein Delta | PP-05, PP-06 |

Ein Delta in einem dieser Bereiche wäre eine Baseline- oder Scope-Änderung und
erforderte eine separate Governance-Entscheidung vor der Umsetzung.

---

### 4.8 Traceability-Auswirkungen

#### Gesamtbewertung

| Prüfpunkt | Ergebnis |
|---|---|
| Neue Charter Objectives | Keine |
| Neue Engineering Goals | Keine |
| Neue Functional Requirements | Keine |
| Neue Acceptance Criteria | Keine |
| Neue Quality Gates | Keine |
| Neue Work Packages | Keine |
| Änderung bestehender Traceability-Ketten | Keine |
| Zusätzliche Traceability-Ebene | Ja — die Ebene Delta (DA-xxx) wird zwischen Baseline und Work Package eingezogen |

#### Erweiterte Traceability-Kette

```
Charter Objective
        ↓
Engineering Goal
        ↓
Functional Requirement
        ↓
Delta (DA-xxx)   ← durch dieses Kapitel eingeführt
        ↓
Work Package
        ↓
Acceptance Criterion / Quality Gate
```

Die Delta-Ebene ist rein additiv. Sie ergänzt die genehmigte Kette um einen
Nachweisknoten und verändert keine bestehende Zuordnung.

#### Deltas mit Querbezug

| Delta | Querbezug | Art des Bezugs |
|---|---|---|
| DA-013 | Alle Deltas der Arten Erweiterung und Ergänzung | Nachweispflicht der Additivität |
| DA-014 | API-03, SDK API 1.0.0 | Nachweispflicht der Kompatibilität |
| DA-011 | DA-003, DA-004, DA-008 | Dokumentationsstand hängt vom Endzustand dieser Deltas ab |
| DA-015 | DA-001 bis DA-014 | Testbasis deckt die hinzukommenden Anforderungen ab |
| DA-005 | DA-011 | Inhaltliche Überschneidung; FR-Zuordnung bleibt disjunkt |

Diese Querbezüge sind Nachweisbeziehungen, keine Umsetzungsreihenfolgen. Die
Ableitung der Reihenfolge erfolgt in Kapitel 6, die Behandlung der optionalen
Bezüge in Kapitel 6.4.

---

### 4.9 Vollständigkeitsnachweis

| Prüfung | Soll | Ist | Ergebnis |
|---|---|---|---|
| Functional Requirements mit mindestens einem Delta | 14 | 14 | Vollständig |
| Deltas mit genau einem zugeordneten FR | 14 | 14 | Vollständig |
| Deltas ohne FR-Zuordnung (mit Begründung) | — | 1 (DA-015) | Begründet in 4.5 |
| Engineering Goals mit mindestens einem Delta | 7 | 7 | Vollständig |
| Work Packages mit mindestens einem Delta | 7 | 7 | Vollständig |
| Scope-Kategorien mit mindestens einem Delta | 6 | 6 | Vollständig |
| Deltas mit genau einer Änderungsart | 15 | 15 | Vollständig |
| Deltas ohne Rückverfolgbarkeit | 0 | 0 | Erfüllt (PP-01) |
| Durch Deltas eingeführte neue Anforderungen | 0 | 0 | Erfüllt (PP-06) |
| Erhaltungsbereiche ausdrücklich als Null-Delta ausgewiesen | 11 | 11 | Vollständig |

#### Verteilung nach Änderungsart

| Art | Anzahl | Deltas |
|---|---|---|
| Erweiterung | 4 | DA-001, DA-006, DA-008, DA-015 |
| Ergänzung | 7 | DA-002, DA-003, DA-004, DA-005, DA-007, DA-009, DA-010 |
| Aktualisierung | 2 | DA-011, DA-012 |
| Verifikation | 2 | DA-013, DA-014 |
| **Summe** | **15** | |

---

### 4.10 Abgrenzung

Dieses Kapitel enthält bewusst keine Dateinamen, keine Klassen, keine Methoden,
keine Modulstruktur, keine Sprintzuordnung, keine Implementierungsreihenfolge,
kein Module Work Breakdown, keine Architekturänderungen und keine
Coding-Details.

Der Vorbehalt aus 4.2 Regel 5 gilt: Die Delta Analysis ist vorläufig, bis die
Baseline-Bestätigung gemäß Kapitel 3 protokolliert vorliegt.

---

## 5. Module Work Breakdown

### 5.1 Zweck und Abgrenzung

#### Zweck

Das Module Work Breakdown beantwortet ausschließlich die Frage:

> **Welche Module, Artefakte und Dateien sind von jedem genehmigten Delta
> betroffen?**

Es ordnet jedem Delta aus Kapitel 4 die betroffenen Module und Dateien zu. Es
beschreibt keine Umsetzung.

| Kapitel | Frage |
|---|---|
| Kapitel 4 — Delta Analysis | **Was** muss geändert werden? |
| **Kapitel 5 — Module Work Breakdown** | **Wo** findet die Änderung statt? |

Nicht beantwortet werden: wie implementiert wird, welche Klassen entstehen,
welcher Code geschrieben wird und welche Algorithmen verwendet werden.

#### Beziehung zur Delta Analysis

Das Module Work Breakdown ist vollständig aus Kapitel 4 abgeleitet. Es enthält
genau einen Eintrag je Delta DA-001 bis DA-015. Es erzeugt keine zusätzlichen
Deltas und lässt keines aus.

#### Beziehung zur Engineering Specification

Jeder Eintrag ist über sein Delta auf einen Functional Requirement und ein Work
Package der Engineering Specification 1.0 rückverfolgbar. Ausnahme ist MWB-015,
das gemäß Kapitel 4 über NFR-005 und QG-007 verankert ist.

#### Beziehung zu WAIVER-DEV-001

Dieses Kapitel ist der zweite durch WAIVER-DEV-001 dem Implementation Plan
zugewiesene Pflichtabschnitt (Development Standard v1.1 §6.2 #5). Zusammen mit
Kapitel 4 erfüllt es die Closing Criteria des Waivers zu Delta Analysis,
Module Work Breakdown und Dateireferenzen (5.5).

---

### 5.2 Methodik

#### Planungsprozess

| Schritt | Inhalt |
|---|---|
| 1 | Übernahme der genehmigten Deltas DA-001 bis DA-015 aus Kapitel 4 |
| 2 | Bestimmung des betroffenen Moduls je Delta anhand der bestehenden Paketstruktur |
| 3 | Bestimmung der betroffenen Artefakte und Dateien innerhalb des Moduls |
| 4 | Feststellung des Änderungsstatus je Datei (bestehend / neu / unverändert) |
| 5 | Feststellung der Änderungsbeziehung je Datei (primär / sekundär / Nachweis) |
| 6 | Feststellung der berührten Baseline-Invarianten |
| 7 | Rückverfolgbarkeitsnachweis auf Work Package und Engineering Specification |

#### Verbindliche Regeln

| # | Regel |
|---|---|
| 1 | **Ableitung ausschließlich aus genehmigten Deltas.** Kein Eintrag ohne zugeordnetes Delta aus Kapitel 4. |
| 2 | **Keine neuen Anforderungen.** Weder Functional Requirements noch Non-Functional Requirements noch Acceptance Criteria werden ergänzt (PP-06). |
| 3 | **Keine neuen Work Packages.** Es gelten ausschließlich WP-001 bis WP-007 der Engineering Specification. |
| 4 | **Keine Architekturänderungen.** Die Zuordnung erfolgt innerhalb der bestehenden Schichten- und Paketstruktur (PP-03). |
| 5 | **Keine Scope-Erweiterung.** Es werden keine Module einbezogen, die außerhalb des genehmigten Scope liegen (PP-05). |
| 6 | **Keine Priorisierung.** Die Reihenfolge der Einträge ist die Delta-Reihenfolge und drückt keine Rangfolge aus. |
| 7 | **Keine Sprintplanung.** Zeitliche und kapazitive Zuordnung erfolgt in der Sprint Planning Phase. |
| 8 | **Keine neuen Module.** Es wird kein Modul und kein Paket eingeführt, das nicht bereits besteht. |
| 9 | **Keine Erfindung von Dateien.** Wo eine additive Ergänzung eine neue Datei erfordern kann, wird das Modul benannt und die Datei ausdrücklich als im Rahmen der Umsetzung festzulegen ausgewiesen. |

#### Statuswerte

| Status | Bedeutung |
|---|---|
| **Bestehend — betroffen** | Die Datei existiert und ist vom Delta betroffen. |
| **Bestehend — Nachweis** | Die Datei existiert und dient als Nachweisträger; keine inhaltliche Änderung aus dem Delta abgeleitet. |
| **Bestehend — unverändert** | Die Datei existiert, ist Bezugspunkt der Prüfung und bleibt unverändert. |
| **Neu — festzulegen** | Das Modul ist zugeordnet; ob und welche neue Datei entsteht, wird im Rahmen der Umsetzung festgelegt. |

#### Änderungsbeziehungen

| Beziehung | Bedeutung |
|---|---|
| **Primär** | Die Datei trägt den Kern des Deltas. |
| **Sekundär** | Die Datei ist mittelbar betroffen. |
| **Nachweis** | Die Datei dient dem Nachweis, nicht der Änderung. |

---

### 5.3 Module Work Breakdown Übersicht

| MWB-ID | Delta | Work Package | Betroffenes Modul | Status | Änderungsart |
|---|---|---|---|---|---|
| MWB-001 | DA-001 | WP-001 | `app/`, `core/` | Bestehend — betroffen | Erweiterung |
| MWB-002 | DA-002 | WP-001 | `app/`, `core/` | Bestehend — betroffen | Ergänzung |
| MWB-003 | DA-003 | WP-002 | `core/`, `app/`, `sdk/` | Bestehend — betroffen | Ergänzung |
| MWB-004 | DA-004 | WP-002 | `core/`, `sdk/` | Bestehend — betroffen | Ergänzung |
| MWB-005 | DA-005 | WP-003 | `docs/`, `sdk/`, `plugins/` | Bestehend — betroffen | Ergänzung |
| MWB-006 | DA-006 | WP-003 | `app/bootstrap/`, `app/security/`, `plugins/` | Bestehend — betroffen | Erweiterung |
| MWB-007 | DA-007 | WP-004 | `core/`, `developer/`, `app/bootstrap/` | Bestehend — betroffen | Ergänzung |
| MWB-008 | DA-008 | WP-004 | `core/`, `services/` | Bestehend — betroffen; Neu — festzulegen | Erweiterung |
| MWB-009 | DA-009 | WP-005 | `app/`, `core/` | Bestehend — betroffen | Ergänzung |
| MWB-010 | DA-010 | WP-005 | `app/bootstrap/`, `app/`, `sdk/` | Bestehend — betroffen | Ergänzung |
| MWB-011 | DA-011 | WP-007 | `docs/`, `sdk/` | Bestehend — betroffen | Aktualisierung |
| MWB-012 | DA-012 | WP-007 | `docs/`, Repository-Wurzel | Bestehend — betroffen | Aktualisierung |
| MWB-013 | DA-013 | WP-006 | `app/bootstrap/`, `sdk/`, `core/`, `plugins/`, `tests/` | Bestehend — unverändert; Nachweis | Verifikation |
| MWB-014 | DA-014 | WP-006 | `sdk/`, `plugins/`, `tests/` | Bestehend — unverändert; Nachweis | Verifikation |
| MWB-015 | DA-015 | WP-001..WP-007 | `tests/` | Bestehend — betroffen; Neu — festzulegen | Erweiterung |

---

### 5.4 Module Work Breakdown Katalog

#### MWB-001 — Bestimmtheit der Lifecycle-Zustandsmaschine

| Feld | Inhalt |
|---|---|
| MWB-ID | MWB-001 |
| Delta | DA-001 |
| Work Package | WP-001 — Platform Hardening |
| Betroffenes Modul | `app/` (Application Lifecycle), `core/` (Lifecycle-Vertrag) |
| Betroffene Dateien | `app/state_machine.py` (Primär), `core/lifecycle.py` (Primär), `app/startup.py` (Sekundär), `app/shutdown.py` (Sekundär), `app/application_host.py` (Sekundär) |
| Änderungsstatus | Bestehend — betroffen |
| Änderungsart | Erweiterung |
| Betroffene Baseline-Invarianten | BI-03, BI-05 — zu bewahren; das Delta liegt oberhalb der Bootstrap-Phasensequenz |
| Traceability | DA-001 → MWB-001 → WP-001 → FR-001 → EG-001 → CO-001 |
| Verweis Engineering Specification | FR-001 — Platform Lifecycle Determinism |
| Verweis Delta Analysis | Kapitel 4.5, DA-001 |

#### MWB-002 — Formalisierung des Ablehnungsverhaltens bei Zustandsübergängen

| Feld | Inhalt |
|---|---|
| MWB-ID | MWB-002 |
| Delta | DA-002 |
| Work Package | WP-001 — Platform Hardening |
| Betroffenes Modul | `app/` (Application Lifecycle), `core/` (Fehlerverträge) |
| Betroffene Dateien | `app/state_machine.py` (Primär), `core/lifecycle.py` (Sekundär), `app/errors.py` (Sekundär), `core/exceptions.py` (Sekundär) |
| Änderungsstatus | Bestehend — betroffen |
| Änderungsart | Ergänzung |
| Betroffene Baseline-Invarianten | Keine. Additiv ohne Eingriff in BI-01..BI-07 |
| Traceability | DA-002 → MWB-002 → WP-001 → FR-002 → EG-001 → CO-001 |
| Verweis Engineering Specification | FR-002 — Lifecycle Control Enhancement |
| Verweis Delta Analysis | Kapitel 4.5, DA-002 |

#### MWB-003 — Vollständige Beschreibung und Abrufbarkeit der Host-Dienste

| Feld | Inhalt |
|---|---|
| MWB-ID | MWB-003 |
| Delta | DA-003 |
| Work Package | WP-002 — Host Service & Extensibility |
| Betroffenes Modul | `core/` (Dienstregistrierung), `app/` (Kompositionswurzel), `sdk/` (Zugang für Plugins) |
| Betroffene Dateien | `core/registry.py` (Primär), `app/host.py` (Sekundär), `app/di.py` (Sekundär), `app/application_host.py` (Sekundär), `sdk/services.py` (Sekundär) |
| Änderungsstatus | Bestehend — betroffen |
| Änderungsart | Ergänzung |
| Betroffene Baseline-Invarianten | Keine. Die Dienstregistrierung als Kompositionsmechanismus bleibt unverändert |
| Traceability | DA-003 → MWB-003 → WP-002 → FR-003 → EG-002 → CO-003 |
| Verweis Engineering Specification | FR-003 — Host Service Description |
| Verweis Delta Analysis | Kapitel 4.5, DA-003 |

#### MWB-004 — Formale Definition der Erweiterungspunkte

| Feld | Inhalt |
|---|---|
| MWB-ID | MWB-004 |
| Delta | DA-004 |
| Work Package | WP-002 — Host Service & Extensibility |
| Betroffenes Modul | `core/` (Extension-Verträge), `sdk/` (Autorenschnittstelle) |
| Betroffene Dateien | `core/extensions.py` (Primär), `sdk/plugin.py` (Sekundär), `sdk/context.py` (Sekundär), `sdk/__init__.py` (Sekundär) |
| Änderungsstatus | Bestehend — betroffen |
| Änderungsart | Ergänzung |
| Betroffene Baseline-Invarianten | BI-07, API-03 — Zugang ausschließlich über die jeweilige Paket-Fassade; API-04 (Änderungsschutz der Exportmenge) |
| Traceability | DA-004 → MWB-004 → WP-002 → FR-004 → EG-002 → CO-002 |
| Verweis Engineering Specification | FR-004 — Plugin Extension Points |
| Verweis Delta Analysis | Kapitel 4.5, DA-004; Querbezug DA-013 |
| Hinweis | Der Dokumentationsbezug (`docs/extensions.md`) wird über MWB-011 geführt, nicht hier. |

#### MWB-005 — Konsolidierung der Vorgaben für Plugin-Autoren

| Feld | Inhalt |
|---|---|
| MWB-ID | MWB-005 |
| Delta | DA-005 |
| Work Package | WP-003 — Developer Experience |
| Betroffenes Modul | `docs/` (Autorenvorgaben), `sdk/` (Einstiegspunkt), `plugins/` (Referenzplugin) |
| Betroffene Dateien | `docs/sdk.md` (Primär), `docs/extensions.md` (Sekundär), `CONTRIBUTING.md` (Sekundär), `sdk/__init__.py` (Sekundär), `plugins/reference/plugin.toml` (Sekundär), `plugins/reference/__init__.py` (Sekundär) |
| Änderungsstatus | Bestehend — betroffen |
| Änderungsart | Ergänzung |
| Betroffene Baseline-Invarianten | Keine |
| Traceability | DA-005 → MWB-005 → WP-003 → FR-005 → EG-004 → CO-004 |
| Verweis Engineering Specification | FR-005 — Plugin Author Documentation |
| Verweis Delta Analysis | Kapitel 4.5, DA-005; Überschneidung mit DA-011 dort ausgewiesen |

#### MWB-006 — Strukturierung des Ablehnungs-Feedbacks der Pipeline

| Feld | Inhalt |
|---|---|
| MWB-ID | MWB-006 |
| Delta | DA-006 |
| Work Package | WP-003 — Developer Experience |
| Betroffenes Modul | `app/bootstrap/` (Pipeline-Stages und Typen), `app/security/` (Prüfung), `plugins/` (Discovery) |
| Betroffene Dateien | `app/bootstrap/stages_plugin.py` (Primär), `app/bootstrap/types.py` (Primär), `app/security/plugin_security.py` (Sekundär), `plugins/loader.py` (Sekundär) |
| Änderungsstatus | Bestehend — betroffen |
| Änderungsart | Erweiterung |
| Betroffene Baseline-Invarianten | BI-06 und PL-01..PL-05 — Pipeline-Reihenfolge unverändert; API-01, API-02, API-04 — die Baseline-Symbole in `app/bootstrap/types.py` unterliegen dem Änderungsschutz, Erweiterungen sind additiv zu führen (Nachweis über MWB-013) |
| Traceability | DA-006 → MWB-006 → WP-003 → FR-006 → EG-004 → CO-004 |
| Verweis Engineering Specification | FR-006 — Pipeline Rejection Feedback |
| Verweis Delta Analysis | Kapitel 4.5, DA-006 |

#### MWB-007 — Plugin-spezifische Diagnoseinformationen

| Feld | Inhalt |
|---|---|
| MWB-ID | MWB-007 |
| Delta | DA-007 |
| Work Package | WP-004 — Observability |
| Betroffenes Modul | `core/` (Observability-Verträge), `developer/` (Diagnostik-Ports), `app/bootstrap/` (Zustandsquelle der Plugin-Runtime) |
| Betroffene Dateien | `core/observability.py` (Primär), `developer/contracts.py` (Sekundär), `developer/inspector.py` (Sekundär), `developer/platform.py` (Sekundär), `app/bootstrap/stages_plugin.py` (Sekundär) |
| Änderungsstatus | Bestehend — betroffen |
| Änderungsart | Ergänzung |
| Betroffene Baseline-Invarianten | BI-06 — die Pipeline bleibt unverändert; die Diagnostik ist lesend |
| Traceability | DA-007 → MWB-007 → WP-004 → FR-007 → EG-005 → CO-005 |
| Verweis Engineering Specification | FR-007 — Diagnostic Reporting |
| Verweis Delta Analysis | Kapitel 4.5, DA-007 |

#### MWB-008 — Erweiterbarkeit des Observability-Systems

| Feld | Inhalt |
|---|---|
| MWB-ID | MWB-008 |
| Delta | DA-008 |
| Work Package | WP-004 — Observability |
| Betroffenes Modul | `core/` (Observability-Verträge), `services/` (Observability-Dienste) |
| Betroffene Dateien | `core/observability.py` (Primär), `services/observability.py` (Primär), `sdk/services.py` (Sekundär), Modul `core/` bzw. `services/` — Neu, Datei im Rahmen der Umsetzung festzulegen |
| Änderungsstatus | Bestehend — betroffen; Neu — festzulegen |
| Änderungsart | Erweiterung |
| Betroffene Baseline-Invarianten | API-04 — Änderungen an öffentlichen Exportmengen sind additiv zu führen (Nachweis über MWB-013) |
| Traceability | DA-008 → MWB-008 → WP-004 → FR-008 → EG-005 → CO-005 |
| Verweis Engineering Specification | FR-008 — Observability Extension |
| Verweis Delta Analysis | Kapitel 4.5, DA-008; Querbezug DA-013 |

#### MWB-009 — Definiertes Wiederherstellungsverhalten bei Fehlern

| Feld | Inhalt |
|---|---|
| MWB-ID | MWB-009 |
| Delta | DA-009 |
| Work Package | WP-005 — Reliability |
| Betroffenes Modul | `app/` (Fehlerbehandlung, Host), `core/` (Fehlerverträge) |
| Betroffene Dateien | `app/errors.py` (Primär), `app/application_host.py` (Sekundär), `app/shutdown.py` (Sekundär), `app/bootstrap/manager.py` (Sekundär), `core/exceptions.py` (Sekundär) |
| Änderungsstatus | Bestehend — betroffen |
| Änderungsart | Ergänzung |
| Betroffene Baseline-Invarianten | BI-03 — der Orchestrator bleibt einziger Einstiegspunkt der Bootstrap-Ausführung; BI-04 — die Stage-Reihenfolge bleibt deterministisch |
| Traceability | DA-009 → MWB-009 → WP-005 → FR-009 → EG-006 → CO-001 |
| Verweis Engineering Specification | FR-009 — Error Recovery |
| Verweis Delta Analysis | Kapitel 4.5, DA-009 |

#### MWB-010 — Isolation von Plugin-Ausfällen

| Feld | Inhalt |
|---|---|
| MWB-ID | MWB-010 |
| Delta | DA-010 |
| Work Package | WP-005 — Reliability |
| Betroffenes Modul | `app/bootstrap/` (Plugin-Runtime), `app/` (Fehlerbehandlung), `sdk/` (Plugin-Vertrag) |
| Betroffene Dateien | `app/bootstrap/stages_plugin.py` (Primär), `app/bootstrap/manager.py` (Sekundär), `app/errors.py` (Sekundär), `sdk/plugin.py` (Sekundär) |
| Änderungsstatus | Bestehend — betroffen |
| Änderungsart | Ergänzung |
| Betroffene Baseline-Invarianten | BI-06, PL-05 — Aktivierung ausschließlich nach vollständig erfolgreicher Sicherheitsprüfung; Pipeline-Reihenfolge unverändert |
| Traceability | DA-010 → MWB-010 → WP-005 → FR-010 → EG-006 → CO-005 |
| Verweis Engineering Specification | FR-010 — Failure Isolation |
| Verweis Delta Analysis | Kapitel 4.5, DA-010 |

#### MWB-011 — Vollständigkeit der SDK-Dokumentation

| Feld | Inhalt |
|---|---|
| MWB-ID | MWB-011 |
| Delta | DA-011 |
| Work Package | WP-007 — Documentation |
| Betroffenes Modul | `docs/` (SDK-Dokumentation), `sdk/` (Versionsanker) |
| Betroffene Dateien | `docs/sdk.md` (Primär), `docs/extensions.md` (Sekundär), `sdk/__init__.py` (Sekundär), `sdk/version.py` (Nachweis — unverändert) |
| Änderungsstatus | Bestehend — betroffen |
| Änderungsart | Aktualisierung |
| Betroffene Baseline-Invarianten | Keine. Die dokumentierte öffentliche API bleibt gemäß API-01..API-04 unverändert |
| Traceability | DA-011 → MWB-011 → WP-007 → FR-011 → EG-007 → CO-004 |
| Verweis Engineering Specification | FR-011 — SDK Documentation Completeness |
| Verweis Delta Analysis | Kapitel 4.5, DA-011; abhängig vom Endzustand von DA-003, DA-004, DA-008 |
| Festgestellter Ausgangsbefund | `docs/sdk.md` weist in der Überschrift die Spezifikationsversion v0.7.1 aus, während die Baseline SDK-Version 0.9.0 und SDK-API-Version 1.0.0 führt (3.1). Der Befund ist Bestandteil des Deltas, keine neue Anforderung. |

#### MWB-012 — Aktualität der Architekturdokumentation

| Feld | Inhalt |
|---|---|
| MWB-ID | MWB-012 |
| Delta | DA-012 |
| Work Package | WP-007 — Documentation |
| Betroffenes Modul | `docs/` (technische Dokumentation), Repository-Wurzel (Kurzübersicht) |
| Betroffene Dateien | `ARCHITECTURE.md` (Primär), `docs/architecture.md` (Primär), `docs/core.md` (Sekundär), `docs/events.md` (Sekundär), `docs/security.md` (Sekundär), `docs/services.md` (Sekundär), `docs/developer.md` (Sekundär), `docs/diagnostics.md` (Sekundär), `docs/health.md` (Sekundär), `docs/performance.md` (Sekundär) |
| Ausdrücklich ausgeschlossen | `docs/architecture-book-v2.md` — APPROVED / FROZEN (GI-01). Keine Änderung durch dieses Delta. |
| Änderungsstatus | Bestehend — betroffen |
| Änderungsart | Aktualisierung |
| Betroffene Baseline-Invarianten | GI-01 — der Architecture Freeze bleibt unberührt. Die Trennung zwischen aktualisierbarer technischer Dokumentation und eingefrorener Architekturreferenz ist verbindlich einzuhalten (PP-03). |
| Traceability | DA-012 → MWB-012 → WP-007 → FR-012 → EG-007 → CO-006 |
| Verweis Engineering Specification | FR-012 — Architecture Documentation Currency |
| Verweis Delta Analysis | Kapitel 4.5, DA-012 |

#### MWB-013 — Nachweis der Additivität aller Erweiterungen

| Feld | Inhalt |
|---|---|
| MWB-ID | MWB-013 |
| Delta | DA-013 |
| Work Package | WP-006 — SDK Contract Verification |
| Betroffenes Modul | `app/bootstrap/`, `sdk/`, `core/`, `plugins/` (Prüfgegenstand), `tests/` (Nachweisträger) |
| Betroffene Dateien | `app/bootstrap/__init__.py` (Bestehend — unverändert, Prüfgegenstand), `sdk/__init__.py` (Bestehend — unverändert, Prüfgegenstand), `core/observability.py` (Bestehend — unverändert, Prüfgegenstand), `plugins/loader.py` (Bestehend — unverändert, Prüfgegenstand), `tests/test_sdk.py` (Nachweis), `tests/test_core.py` (Nachweis) |
| Änderungsstatus | Bestehend — unverändert; Nachweis |
| Änderungsart | Verifikation |
| Betroffene Baseline-Invarianten | API-01, API-02, API-04 sowie BI-01 bis BI-07 — vollständig zu bewahren |
| Traceability | DA-013 → MWB-013 → WP-006 → FR-013 → EG-003 → CO-006 |
| Verweis Engineering Specification | FR-013 — Additive Extension Rule (ausdrücklich nicht scope-eröffnend) |
| Verweis Delta Analysis | Kapitel 4.5, DA-013; Querbezug zu allen Deltas der Arten Erweiterung und Ergänzung |

#### MWB-014 — Nachweis der Consumer-Kompatibilität

| Feld | Inhalt |
|---|---|
| MWB-ID | MWB-014 |
| Delta | DA-014 |
| Work Package | WP-006 — SDK Contract Verification |
| Betroffenes Modul | `sdk/` (Versionsvertrag), `plugins/` (Referenzplugin), `tests/` (Nachweisträger) |
| Betroffene Dateien | `sdk/version.py` (Bestehend — unverändert, Prüfgegenstand), `plugins/reference/plugin.toml` (Nachweis), `plugins/reference/__init__.py` (Nachweis), `tests/test_sdk.py` (Nachweis), `tests/test_golden_reference.py` (Nachweis), `tests/integration/test_plugin_integration.py` (Nachweis) |
| Änderungsstatus | Bestehend — unverändert; Nachweis |
| Änderungsart | Verifikation |
| Betroffene Baseline-Invarianten | API-03 — Consumer-Import-Kompatibilität; SDK API 1.0.0 bleibt unverändert |
| Traceability | DA-014 → MWB-014 → WP-006 → FR-014 → EG-003 → CO-006 |
| Verweis Engineering Specification | FR-014 — Consumer Compatibility Assurance |
| Verweis Delta Analysis | Kapitel 4.5, DA-014 |

#### MWB-015 — Erweiterung der Testbasis auf den Zielzustand

| Feld | Inhalt |
|---|---|
| MWB-ID | MWB-015 |
| Delta | DA-015 |
| Work Package | WP-001 bis WP-007 (querschnittlich) |
| Betroffenes Modul | `tests/` |
| Betroffene Dateien | `tests/test_application_foundation.py` (Sekundär), `tests/test_core.py` (Sekundär), `tests/test_sdk.py` (Sekundär), `tests/test_activation_validation.py` (Sekundär), `tests/test_plugin_observability.py` (Sekundär), `tests/test_golden_reference.py` (Sekundär), `tests/integration/test_plugin_integration.py` (Sekundär), Modul `tests/` — Neu, Dateien im Rahmen der Umsetzung festzulegen |
| Änderungsstatus | Bestehend — betroffen; Neu — festzulegen |
| Änderungsart | Erweiterung |
| Betroffene Baseline-Invarianten | Regressionsbasis gemäß 3.1 — 1019 Tests, 0 Regressionen; die Regressionsfreiheit bleibt erhalten |
| Traceability | DA-015 → MWB-015 → WP-001..WP-007 → NFR-005, QG-007 |
| Verweis Engineering Specification | NFR-005, QG-007; Scope-Kategorie Testabdeckung |
| Verweis Delta Analysis | Kapitel 4.5, DA-015 einschließlich der dort dokumentierten Begründung des fehlenden FR-Bezugs |

---

### 5.5 Dateireferenzen

#### 5.5.1 Erfüllung des Waiver-Kriteriums

**Kapitel 4 (Delta Analysis) und Kapitel 5 (Module Work Breakdown) erfüllen
gemeinsam das Closing Criterion aus WAIVER-DEV-001 bezüglich der
Dateireferenzen.**

Der Begriff **Dateireferenz** ist durch WAIVER-AMENDMENT-001 §4.1 verbindlich
präzisiert: Datei, Änderungsbereich, Traceability und Nachweis. Klassen- und
Methodenimplementierungen, Codebeispiele, Produktionscode und Sprint-Artefakte
sind gemäß §4.2 im Implementation Plan nicht erforderlich und gemäß §4.3 der
autorisierten Implementierungsphase zugewiesen.

| # | Waiver Closing Criterion | Adressiert durch | Status |
|---|---|---|---|
| §9 (1) | Vollständige Delta Analysis mit Dateireferenzen (Datei, Status) | Kapitel 4 (Deltas) in Verbindung mit 5.5.2 (Dateireferenzen je Delta) und 5.5.3 (Zeilenanker, soweit stabil verifiziert) | Adressiert; Bewertung durch Independent Review |
| §9 (2) | Vollständiges Module Work Breakdown je Work Package | Kapitel 5.3 und 5.4 | Adressiert; Bewertung durch Independent Review |
| §9 (3) | Der Independent Review des Implementation Plans bestätigt die Vollständigkeit der zugewiesenen Abschnitte als Bestandteil der IP-Genehmigung | Workflow-Schritt W-3 (Kapitel 10.4); Voraussetzung AP-07; Completion Condition CC-14 | **Ausstehend** — prozessual, durch Planinhalt nicht erfüllbar |
| §9 (4) | Scope Verification mit Dateireferenzen | 5.5.2 in Verbindung mit der Scope-Abdeckung in 4.6 | Adressiert; Bewertung durch Independent Review |

Kapitel 4 führt die Differenz auf Anforderungsebene, Kapitel 5 die Zuordnung
auf Datei- und Modulebene. Die Trennung ist bewusst: Sie hält die Delta
Analysis lösungsneutral und bündelt sämtliche Dateireferenzen an einer
prüfbaren Stelle.

**Bewertungsvorbehalt.** Dieser Abschnitt stellt fest, **wo** die Closing
Criteria adressiert sind. Er stellt nicht fest, **dass** sie erfüllt sind.
Die Feststellung der Erfüllung obliegt ausschließlich dem Independent Review
(§9 (3) selbst). Der zuvor bestehende Entscheidungsbedarf zum Verhältnis
zwischen dem Wortlaut von §9 (1) und §9 (2), dem über WAIVER-DEV-001 §3.1
inkorporierten Development Standard v1.1 §6.2 #4/#5 und der
Autorisierungsgrenze dieses Plans (Kapitel 1.6, ST-10) ist mit
**GDR-001** (`docs/governance/gdr-001-waiver-closing-criteria.md`) entschieden
und durch **WAIVER-AMENDMENT-001** (`docs/governance/waiver-amendment-001.md`)
umgesetzt. WAIVER-DEV-001 bleibt aktiv, bis §9 (3) erfüllt ist.

#### 5.5.2 Dateireferenzen je Änderung

| Datei | Status | Artefakt | Änderungsbeziehung | MWB |
|---|---|---|---|---|
| `app/state_machine.py` | Bestehend — betroffen | Quellmodul | Primär | MWB-001, MWB-002 |
| `core/lifecycle.py` | Bestehend — betroffen | Quellmodul | Primär / Sekundär | MWB-001, MWB-002 |
| `app/startup.py` | Bestehend — betroffen | Quellmodul | Sekundär | MWB-001 |
| `app/shutdown.py` | Bestehend — betroffen | Quellmodul | Sekundär | MWB-001, MWB-009 |
| `app/application_host.py` | Bestehend — betroffen | Quellmodul | Sekundär | MWB-001, MWB-003, MWB-009 |
| `core/exceptions.py` | Bestehend — betroffen | Quellmodul | Sekundär | MWB-002, MWB-009 |
| `app/errors.py` | Bestehend — betroffen | Quellmodul | Primär / Sekundär | MWB-002, MWB-009, MWB-010 |
| `core/registry.py` | Bestehend — betroffen | Quellmodul | Primär | MWB-003 |
| `app/host.py` | Bestehend — betroffen | Quellmodul | Sekundär | MWB-003 |
| `app/di.py` | Bestehend — betroffen | Quellmodul | Sekundär | MWB-003 |
| `sdk/services.py` | Bestehend — betroffen | Quellmodul | Sekundär | MWB-003, MWB-008 |
| `core/extensions.py` | Bestehend — betroffen | Quellmodul | Primär | MWB-004 |
| `sdk/plugin.py` | Bestehend — betroffen | Quellmodul | Sekundär | MWB-004, MWB-010 |
| `sdk/context.py` | Bestehend — betroffen | Quellmodul | Sekundär | MWB-004 |
| `sdk/__init__.py` | Bestehend — betroffen / unverändert | Paket-Fassade | Sekundär / Prüfgegenstand | MWB-004, MWB-005, MWB-011, MWB-013 |
| `docs/sdk.md` | Bestehend — betroffen | Dokumentationsartefakt | Primär | MWB-005, MWB-011 |
| `docs/extensions.md` | Bestehend — betroffen | Dokumentationsartefakt | Sekundär | MWB-005, MWB-011 |
| `CONTRIBUTING.md` | Bestehend — betroffen | Dokumentationsartefakt | Sekundär | MWB-005 |
| `plugins/reference/plugin.toml` | Bestehend — Nachweis | Referenzplugin (Manifest) | Sekundär / Nachweis | MWB-005, MWB-014 |
| `plugins/reference/__init__.py` | Bestehend — Nachweis | Referenzplugin | Sekundär / Nachweis | MWB-005, MWB-014 |
| `app/bootstrap/stages_plugin.py` | Bestehend — betroffen | Quellmodul (Pipeline-Stages) | Primär / Sekundär | MWB-006, MWB-007, MWB-010 |
| `app/bootstrap/types.py` | Bestehend — betroffen | Quellmodul (Baseline-Typen) | Primär | MWB-006 |
| `app/security/plugin_security.py` | Bestehend — betroffen | Quellmodul | Sekundär | MWB-006 |
| `plugins/loader.py` | Bestehend — betroffen / unverändert | Quellmodul | Sekundär / Prüfgegenstand | MWB-006, MWB-013 |
| `core/observability.py` | Bestehend — betroffen / unverändert | Quellmodul | Primär / Prüfgegenstand | MWB-007, MWB-008, MWB-013 |
| `developer/contracts.py` | Bestehend — betroffen | Quellmodul (Diagnostik-Ports) | Sekundär | MWB-007 |
| `developer/inspector.py` | Bestehend — betroffen | Quellmodul | Sekundär | MWB-007 |
| `developer/platform.py` | Bestehend — betroffen | Quellmodul | Sekundär | MWB-007 |
| `services/observability.py` | Bestehend — betroffen | Quellmodul | Primär | MWB-008 |
| `app/bootstrap/manager.py` | Bestehend — betroffen | Quellmodul (Orchestrator) | Sekundär | MWB-009, MWB-010 |
| `ARCHITECTURE.md` | Bestehend — betroffen | Dokumentationsartefakt | Primär | MWB-012 |
| `docs/architecture.md` | Bestehend — betroffen | Dokumentationsartefakt | Primär | MWB-012 |
| `docs/core.md` | Bestehend — betroffen | Dokumentationsartefakt | Sekundär | MWB-012 |
| `docs/events.md` | Bestehend — betroffen | Dokumentationsartefakt | Sekundär | MWB-012 |
| `docs/security.md` | Bestehend — betroffen | Dokumentationsartefakt | Sekundär | MWB-012 |
| `docs/services.md` | Bestehend — betroffen | Dokumentationsartefakt | Sekundär | MWB-012 |
| `docs/developer.md` | Bestehend — betroffen | Dokumentationsartefakt | Sekundär | MWB-012 |
| `docs/diagnostics.md` | Bestehend — betroffen | Dokumentationsartefakt | Sekundär | MWB-012 |
| `docs/health.md` | Bestehend — betroffen | Dokumentationsartefakt | Sekundär | MWB-012 |
| `docs/performance.md` | Bestehend — betroffen | Dokumentationsartefakt | Sekundär | MWB-012 |
| `docs/architecture-book-v2.md` | Bestehend — unverändert | Architekturreferenz (FROZEN) | Ausgeschlossen | MWB-012 |
| `app/bootstrap/__init__.py` | Bestehend — unverändert | Paket-Fassade | Prüfgegenstand | MWB-013 |
| `sdk/version.py` | Bestehend — unverändert | Versionsvertrag | Prüfgegenstand / Nachweis | MWB-011, MWB-014 |
| `tests/test_sdk.py` | Bestehend — Nachweis | Testartefakt | Nachweis / Sekundär | MWB-013, MWB-014, MWB-015 |
| `tests/test_core.py` | Bestehend — Nachweis | Testartefakt | Nachweis / Sekundär | MWB-013, MWB-015 |
| `tests/test_golden_reference.py` | Bestehend — Nachweis | Testartefakt | Nachweis / Sekundär | MWB-014, MWB-015 |
| `tests/integration/test_plugin_integration.py` | Bestehend — Nachweis | Testartefakt | Nachweis / Sekundär | MWB-014, MWB-015 |
| `tests/test_application_foundation.py` | Bestehend — betroffen | Testartefakt | Sekundär | MWB-015 |
| `tests/test_activation_validation.py` | Bestehend — betroffen | Testartefakt | Sekundär | MWB-015 |
| `tests/test_plugin_observability.py` | Bestehend — betroffen | Testartefakt | Sekundär | MWB-015 |
| `core/` bzw. `services/` — Datei festzulegen | Neu — festzulegen | Quellmodul | Primär | MWB-008 |
| `tests/` — Dateien festzulegen | Neu — festzulegen | Testartefakt | Primär | MWB-015 |

50 referenzierte bestehende Artefakte, zwei ausdrücklich als noch festzulegen
ausgewiesene Positionen. Alle 50 als bestehend geführten Dateien wurden gegen
den Repository-Stand geprüft und sind vorhanden (Regel 9, Kapitel 5.2).

#### 5.5.3 Verifizierte Zeilenanker

Zeilenangaben werden ausschließlich dort geführt, wo ein stabiler,
verifizierter Anker vorliegt. Für Änderungen, deren Ort erst durch die
Umsetzung bestimmt wird, werden keine Zeilenangaben ausgewiesen.

| Datei | Zeile | Anker | Relevanz |
|---|---|---|---|
| `app/bootstrap/__init__.py` | 45 | Öffentliche Exportdeklaration | API-01, API-04, MWB-013 |
| `sdk/__init__.py` | 81 | Öffentliche Exportdeklaration | API-04, MWB-013 |
| `core/observability.py` | 89 | Öffentliche Exportdeklaration | MWB-008, MWB-013 |
| `plugins/loader.py` | 132 | Öffentliche Exportdeklaration | MWB-013 |
| `app/bootstrap/types.py` | 54 | Definitionsort eines Baseline-Symbols gemäß API-01 | MWB-006 |
| `app/bootstrap/types.py` | 71 | Definitionsort eines Baseline-Symbols gemäß API-01 | MWB-006 |
| `sdk/version.py` | 24 | SDK-Versionskonstante (`0.9.0`) | 3.1, MWB-014 |
| `sdk/version.py` | 27 | SDK-API-Versionskonstante (`1.0.0`) | 3.1, MWB-014 |
| `docs/sdk.md` | 1 | Dokumentversionsangabe (v0.7.1) | MWB-011, Ausgangsbefund |

#### 5.5.4 Nicht zugeordnete Artefaktbereiche

Die folgenden Bereiche des Repositorys sind keinem Delta zugeordnet. Die
Nichtzuordnung wird ausdrücklich ausgewiesen, damit sie nicht als Auslassung
gewertet wird.

| Bereich | Begründung der Nichtzuordnung |
|---|---|
| `ui/**` | UI-Redesign ist gemäß Charter ausgeschlossen (Future Item FI-005). Kein Delta in Kapitel 4. |
| `ai/**`, `database/**`, `config/**`, `styles/**` | Kein Delta in Kapitel 4; nicht Gegenstand der genehmigten Scope-Kategorien. |
| `app/security/**` außer der in MWB-006 genannten Datei | Kein weiteres Delta; die Sicherheitspipeline ist Erhaltungsbereich (4.7). |
| `src/jochen_x/**` | Nicht Bestandteil der Bootstrap Baseline 1.0 und vom Anwendungseinstiegspunkt nicht referenziert. Siehe Governance-Befund unten. |

**Governance-Befund GB-001 — Paralleler Artefaktbaum.** Der Befund ist als
Risiko **GR-001** in das konsolidierte Risikoregister (Kapitel 11.11)
aufgenommen und dort mit Klasse, Kritikalität, Owner und Status geführt; die
normative Pending Resolution PR-001 steht in Anhang A. Das Repository enthält
neben der von Bootstrap Baseline 1.0 und Architecture Book v2.0 beschriebenen
Paketstruktur einen zweiten, in sich geschlossenen Artefaktbaum unter
`src/jochen_x/**` mit eigenem Testbestand. Dieser Baum wird vom
Anwendungseinstiegspunkt nicht referenziert und ist in keiner normativen
Eingabe dieses Plans beschrieben.

Die Deltas dieses Plans sind ausschließlich der baseline-geführten Struktur
zugeordnet. Die Klärung des Status von `src/jochen_x/**` liegt außerhalb der
Autorisierungsgrenze dieses Plans (Kapitel 1.6) und erfordert eine separate
Governance-Entscheidung. Der Befund wird hier dokumentiert, nicht aufgelöst
(PP-04).

Solange GR-001 den Status PENDING DECISION trägt, bestehen zwei Auswirkungen:
die Regressionsbasis von 1019 Tests umfasst Testartefakte beider Bäume, und die
Zuordnung in MWB-015 ist auf die baseline-geführte Struktur beschränkt.

---

### 5.6 Vollständigkeitsprüfung

| Prüfung | Soll | Ist | Ergebnis |
|---|---|---|---|
| Deltas mit genau einem MWB-Eintrag | 15 | 15 | Vollständig |
| MWB-Einträge ohne zugeordnetes Delta | 0 | 0 | Erfüllt |
| Work Packages mit mindestens einem MWB-Eintrag | 7 | 7 | Vollständig |
| MWB-Einträge mit zugeordnetem Modul | 15 | 15 | Vollständig |
| MWB-Einträge mit mindestens einer Dateireferenz | 15 | 15 | Vollständig |
| Doppelte MWB-IDs | 0 | 0 | Keine Dubletten |
| Deltas ohne MWB-Eintrag | 0 | 0 | Keine Lücken |
| Neu eingeführte Module oder Pakete | 0 | 0 | Erfüllt (Regel 8) |
| Neue Functional Requirements | 0 | 0 | Erfüllt (PP-06) |
| Neue Engineering Goals | 0 | 0 | Erfüllt (PP-06) |
| Neue Work Packages | 0 | 0 | Erfüllt (Regel 3) |
| Neue Acceptance Criteria / Quality Gates | 0 | 0 | Erfüllt (PP-06) |
| Neue Deliverables | 0 | 0 | Erfüllt |
| Neue ADRs | 0 | 0 | Erfüllt |
| Änderungen an Bootstrap Baseline oder Architecture Book | 0 | 0 | Erfüllt (PP-02, PP-03) |
| Als bestehend geführte Dateien gegen Repository-Stand geprüft | 50 | 50 | Erfüllt |
| Ausdrücklich als festzulegen ausgewiesene Positionen | — | 2 | Ausgewiesen (Regel 9) |

#### Work-Package-Abdeckung

| Work Package | MWB-Einträge |
|---|---|
| WP-001 — Platform Hardening | MWB-001, MWB-002, MWB-015 |
| WP-002 — Host Service & Extensibility | MWB-003, MWB-004, MWB-015 |
| WP-003 — Developer Experience | MWB-005, MWB-006, MWB-015 |
| WP-004 — Observability | MWB-007, MWB-008, MWB-015 |
| WP-005 — Reliability | MWB-009, MWB-010, MWB-015 |
| WP-006 — SDK Contract Verification | MWB-013, MWB-014, MWB-015 |
| WP-007 — Documentation | MWB-011, MWB-012, MWB-015 |

Alle sieben Work Packages sind abgedeckt. MWB-015 ist querschnittlich und
allen Work Packages zugeordnet.

---

### 5.7 Traceability

#### Kette

```
Delta (DA-xxx)
        ↓
Module Work Breakdown (MWB-xxx)
        ↓
Work Package (WP-xxx)
        ↓
Engineering Specification (FR / NFR / QG)
```

Es wird **keine neue Traceability-Ebene** erzeugt. Die Ebene MWB ist die in
Kapitel 4.8 bereits eingeführte Delta-Ebene in ihrer Modul- und
Dateizuordnung; sie tritt an die Stelle einer zusätzlichen Ebene, nicht neben
sie.

#### Vollständige Zuordnung

| MWB | Delta | WP | Engineering Specification |
|---|---|---|---|
| MWB-001 | DA-001 | WP-001 | FR-001 |
| MWB-002 | DA-002 | WP-001 | FR-002 |
| MWB-003 | DA-003 | WP-002 | FR-003 |
| MWB-004 | DA-004 | WP-002 | FR-004 |
| MWB-005 | DA-005 | WP-003 | FR-005 |
| MWB-006 | DA-006 | WP-003 | FR-006 |
| MWB-007 | DA-007 | WP-004 | FR-007 |
| MWB-008 | DA-008 | WP-004 | FR-008 |
| MWB-009 | DA-009 | WP-005 | FR-009 |
| MWB-010 | DA-010 | WP-005 | FR-010 |
| MWB-011 | DA-011 | WP-007 | FR-011 |
| MWB-012 | DA-012 | WP-007 | FR-012 |
| MWB-013 | DA-013 | WP-006 | FR-013 |
| MWB-014 | DA-014 | WP-006 | FR-014 |
| MWB-015 | DA-015 | WP-001..WP-007 | NFR-005, QG-007 |

Jeder der 14 Functional Requirements ist über genau einen MWB-Eintrag
adressiert. MWB-015 ist gemäß Kapitel 4.5 über NFR-005 und QG-007 verankert.

---

### 5.8 Abgrenzung

Dieses Kapitel enthält ausdrücklich **nicht**:

| Ausgeschlossen | Zuordnung |
|---|---|
| Coding und Implementierungsdetails | Nicht autorisiert (Kapitel 1.6) |
| Klassen, Methoden, Algorithmen, Codebeispiele | Nicht Gegenstand der Planungsphase |
| Architektur und Architekturentscheidungen | Architecture Book v2.0, FROZEN (PP-03) |
| Sprintplanung | Sprint Planning Phase (Charter §8, Schritt 6) |
| Umsetzungsreihenfolge | Kapitel 6 |
| Tests (Inhalt, Fälle, Strategie) | Engineering Specification (Test Strategy); Kapitel 8 und Kapitel 9 |
| Acceptance Criteria | Engineering Specification, unverändert |
| Performance (Messmethodik, Ziele) | Anhang B — Performance Measurement Methodology (SC-06) |
| Runtime-Verhalten | Nicht Gegenstand dieses Kapitels |
| Deployment und Rollout | Kapitel 13 (PS-05); Deployment ist auch dort ausgeschlossen (13.1, 13.4) |

Die in 5.3 und 5.4 geführte Reihenfolge der Einträge ist die Delta-Reihenfolge
aus Kapitel 4. Sie drückt keine Priorität, keine Abhängigkeit und keine
Umsetzungsreihenfolge aus.

---

## 6. Work Package Sequencing & Dependency Planning

### 6.1 Purpose

#### Zweck der Work-Package-Sequenzierung

Dieses Kapitel beantwortet ausschließlich:

> **In welcher fachlich und technisch begründeten Reihenfolge werden die
> bereits genehmigten Work Packages umgesetzt?**

Es legt die **logische** Reihenfolge fest, nicht die zeitliche. Die
Phasenordnung folgt in Kapitel 7.3, ihre Überführungssicht in Kapitel 12.7.
Sprints, Termine und Ressourcen sind der Sprint Planning Phase zugewiesen
(Charter §8, Schritt 6) und in keinem Kapitel dieses Plans enthalten
(ST-07 bis ST-09).

Nicht beantwortet werden: wie implementiert wird, welche Klassen entstehen,
welche Dateien geändert werden, welcher Sprint welches Work Package umsetzt und
welche Algorithmen verwendet werden.

#### Zusammenhang mit der Engineering Specification

Die Reihenfolge ist vollständig aus der Engineering Specification 1.0
abgeleitet. Die Engineering Specification führt in ihrer Implementation
Sequence eine zweiphasige Reihenfolge und in ihrem Work-Package-Katalog einen
azyklischen Abhängigkeitsgraphen. Beide sind genehmigt und werden hier
übernommen, nicht neu bestimmt.

Dieses Kapitel erzeugt keine Reihenfolge, die von der Engineering Specification
abweicht. Es macht die dort festgelegte Reihenfolge prüfbar und begründet jede
Position.

#### Zusammenhang mit der Delta Analysis

Die Delta Analysis (Kapitel 4) ordnet jedem Delta ein Work Package zu. Die
Sequenzierung erbt diese Zuordnung. Die in Kapitel 4.8 dokumentierten
Querbezüge zwischen Deltas sind **Nachweisbeziehungen**; sie werden in 6.4 als
optionale, nicht blockierende Abhängigkeiten geführt und verändern den
genehmigten Abhängigkeitsgraphen nicht.

#### Zusammenhang mit dem Module Work Breakdown

Das Module Work Breakdown (Kapitel 5) ordnet jedem Delta Module und Artefakte
zu. Diese Zuordnung ist ausdrücklich ohne Reihenfolgeaussage erstellt
(Kapitel 5.8). Die Reihenfolge entsteht erst hier — aus Abhängigkeiten, nicht
aus der Artefaktverteilung.

#### Ausdrückliche Abgrenzung

Es erfolgt **keine Priorisierung nach Aufwand** und **keine Sprintplanung**.
Aufwand, Kapazität und Termine sind in diesem Kapitel keine
Ordnungskriterien.

---

### 6.2 Sequencing Methodology

#### Vorgehen

| Schritt | Inhalt |
|---|---|
| 1 | Übernahme der 7 genehmigten Work Packages aus der Engineering Specification |
| 2 | Übernahme des genehmigten Abhängigkeitsgraphen und der Kategorien Provider / Dependent |
| 3 | Übernahme der genehmigten zweiphasigen Implementation Sequence |
| 4 | Bestimmung der Vorbedingungen je Work Package aus Abhängigkeiten, Baseline und Governance |
| 5 | Feststellung optionaler, nicht blockierender Abhängigkeiten aus den Querbezügen der Delta Analysis |
| 6 | Bestimmung des kritischen Pfades auf struktureller Grundlage |
| 7 | Bewertung der Parallelisierbarkeit auf Grundlage von Abhängigkeiten, Traceability, Governance und Baseline |
| 8 | Verifikation gegen Engineering Specification, Baseline und WAIVER-DEV-001 |

#### Ordnungskriterien

| Kriterium | Anwendung |
|---|---|
| **Abhängigkeit** | Primäres Ordnungskriterium. Ein Work Package folgt jedem Work Package, von dessen Ergebnis es abhängt. |
| **Governance Constraints** | Kein Reihenfolgeschritt nimmt eine ausstehende Genehmigung vorweg (PP-04, GC-01..GC-07). |
| **Baseline** | Kein Reihenfolgeschritt verletzt eine Baseline-Invariante oder die Change Control (PP-02). |
| **Traceability** | Jede Position ist auf ein genehmigtes Element der Engineering Specification rückverfolgbar (PP-01). |

#### Ausgeschlossene Ordnungskriterien

| Kriterium | Begründung des Ausschlusses |
|---|---|
| Aufwand, Story Points, Schätzungen | Nicht Gegenstand der Planungsphase; keine autorisierte Eingabe |
| Entwicklerkapazität, Verfügbarkeit | Ressourcenplanung, spätere Phase |
| Termine, Sprintgrenzen | Sprint Planning Phase (Charter §8, Schritt 6) |
| Artefaktverteilung aus Kapitel 5 | Ausdrücklich ohne Reihenfolgeaussage erstellt (5.8) |

#### Verbindliche Regeln

| # | Regel |
|---|---|
| 1 | **Ableitung ausschließlich aus der Engineering Specification.** Keine Reihenfolgeaussage ohne Grundlage in Abhängigkeitsgraph oder Implementation Sequence. |
| 2 | **Keine neuen Work Packages.** Es gelten ausschließlich WP-001 bis WP-007. |
| 3 | **Keine Architekturänderungen.** Die Reihenfolge bewegt sich innerhalb der eingefrorenen Architektur (PP-03). |
| 4 | **Keine Zyklen.** Der genehmigte Graph ist azyklisch und bleibt es. |
| 5 | **Keine Umdeutung genehmigter Abhängigkeiten.** Optionale Bezüge werden als solche gekennzeichnet und ändern den normativen Graphen nicht. |
| 6 | **Keine Scope-Erweiterung und keine neuen Anforderungen** (PP-05, PP-06). |

---

### 6.3 Work Package Sequence

Die verbindliche Reihenfolge folgt der genehmigten zweiphasigen Implementation
Sequence der Engineering Specification.

#### Phasenübersicht

| Phase | Inhalt | Charakter |
|---|---|---|
| **Phase 1** | WP-001, WP-002, WP-003, WP-004, WP-005, WP-007 | Provider — untereinander ohne blockierende Abhängigkeiten |
| **Phase 2** | WP-006 | Dependent — setzt den Abschluss aller Phase-1-Pakete voraus |

Die Positionsbezeichnungen 1a bis 1f entsprechen der Engineering Specification.
Sie sind **Bezeichner, keine Rangfolge**: Innerhalb von Phase 1 besteht keine
verbindliche Ordnung.

#### Sequenz-Katalog

##### Position 1a — WP-001 Platform Hardening

| Feld | Inhalt |
|---|---|
| Reihenfolge | Phase 1, Position 1a — ohne verbindliche Ordnung innerhalb der Phase |
| Zweck | Bestimmtheit und Ablehnungsverhalten der Plattform-Zustandsübergänge herstellen (FR-001, FR-002) |
| Begründung der Position | Provider ohne eingehende Abhängigkeiten. Wirkt auf die Plattformschicht oberhalb der Bootstrap-Phasensequenz und benötigt kein Ergebnis eines anderen Work Package. |
| Vorbedingungen | Baseline-Bestätigung gemäß Kapitel 3 protokolliert; BI-03 und BI-05 als Erhaltungsvorgabe verstanden |
| Ergebnis der Phase | Die zulässigen Zustandsübergänge sind vollständig bestimmt; unzulässige Übergänge führen zu einem definierten Ablehnungsergebnis. Nachweisgrundlage für die zugeordneten Acceptance Criteria und für WP-006. |

##### Position 1b — WP-002 Host Service & Extensibility

| Feld | Inhalt |
|---|---|
| Reihenfolge | Phase 1, Position 1b — ohne verbindliche Ordnung innerhalb der Phase |
| Zweck | Host-Dienste vollständig beschreiben und abrufbar machen; Erweiterungspunkte formal definieren (FR-003, FR-004) |
| Begründung der Position | Provider ohne eingehende Abhängigkeiten. Liefert Ergebnisse, auf die WP-007 inhaltlich und WP-006 als Prüfgegenstand Bezug nehmen. |
| Vorbedingungen | Baseline-Bestätigung gemäß Kapitel 3 protokolliert; API-Änderungsschutz gemäß API-04 als Erhaltungsvorgabe verstanden |
| Ergebnis der Phase | Host-Dienste sind zentral beschrieben und abrufbar; Erweiterungspunkte sind definiert. Grundlage für den Additivitätsnachweis in WP-006. |

##### Position 1c — WP-003 Developer Experience

| Feld | Inhalt |
|---|---|
| Reihenfolge | Phase 1, Position 1c — ohne verbindliche Ordnung innerhalb der Phase |
| Zweck | Vorgaben für Plugin-Autoren konsolidieren; Ablehnungs-Feedback der Pipeline strukturieren (FR-005, FR-006) |
| Begründung der Position | Provider ohne eingehende Abhängigkeiten. Setzt die bestehende Plugin-Runtime-Pipeline voraus, die Bestandteil der bestätigten Baseline ist und nicht Ergebnis eines anderen Work Package. |
| Vorbedingungen | Baseline-Bestätigung gemäß Kapitel 3 protokolliert; PL-01 bis PL-05 als unveränderliche Pipeline-Reihenfolge verstanden |
| Ergebnis der Phase | Autorenvorgaben sind an einer definierten Stelle verfügbar; Ablehnungen weisen Stufe und verletztes Kriterium aus. |

##### Position 1d — WP-004 Observability

| Feld | Inhalt |
|---|---|
| Reihenfolge | Phase 1, Position 1d — ohne verbindliche Ordnung innerhalb der Phase |
| Zweck | Plugin-spezifische Diagnoseinformationen bereitstellen; Observability erweiterbar machen (FR-007, FR-008) |
| Begründung der Position | Provider ohne eingehende Abhängigkeiten. Die Diagnostik ist lesend gegenüber der Plugin-Runtime und erfordert kein vorheriges Work Package. |
| Vorbedingungen | Baseline-Bestätigung gemäß Kapitel 3 protokolliert; BI-06 als Erhaltungsvorgabe verstanden |
| Ergebnis der Phase | Strukturierte Diagnoseinformationen liegen vor; das Observability-System ist erweiterbar. Prüfgegenstand für den Additivitätsnachweis in WP-006. |

##### Position 1e — WP-005 Reliability

| Feld | Inhalt |
|---|---|
| Reihenfolge | Phase 1, Position 1e — ohne verbindliche Ordnung innerhalb der Phase |
| Zweck | Definiertes Wiederherstellungsverhalten herstellen; Plugin-Ausfälle isolieren (FR-009, FR-010) |
| Begründung der Position | Provider ohne eingehende Abhängigkeiten. Wirkt auf Fehlerbehandlung und Plugin-Runtime, ohne das Ergebnis eines anderen Work Package vorauszusetzen. |
| Vorbedingungen | Baseline-Bestätigung gemäß Kapitel 3 protokolliert; BI-03, BI-04, BI-06 und PL-05 als Erhaltungsvorgaben verstanden |
| Ergebnis der Phase | Fehler führen zu definiertem Wiederherstellungsverhalten; Plugin-Ausfälle bleiben isoliert. |

##### Position 1f — WP-007 Documentation

| Feld | Inhalt |
|---|---|
| Reihenfolge | Phase 1, Position 1f — ohne verbindliche Ordnung innerhalb der Phase |
| Zweck | SDK-Dokumentation vervollständigen; Architekturdokumentation nachführen (FR-011, FR-012) |
| Begründung der Position | Die Engineering Specification führt WP-007 als Provider ohne eingehende Abhängigkeiten. Die Position in Phase 1 ist damit normativ vorgegeben. Inhaltlich bestehen nicht blockierende Bezüge zu WP-002 und WP-004 (6.4). |
| Vorbedingungen | Baseline-Bestätigung gemäß Kapitel 3 protokolliert; Architecture Freeze gemäß GI-01 als unverrückbare Grenze verstanden |
| Ergebnis der Phase | SDK- und Architekturdokumentation reflektieren den Stand zum Milestone-Abschluss. Voraussetzung für die Abschlussprüfung in WP-006. |

##### Position 2 — WP-006 SDK Contract Verification

| Feld | Inhalt |
|---|---|
| Reihenfolge | Phase 2, Position 2 — nach vollständigem Abschluss aller Phase-1-Pakete |
| Zweck | Additivität aller Erweiterungen und Consumer-Kompatibilität nachweisen (FR-013, FR-014) |
| Begründung der Position | Dependent mit eingehenden Abhängigkeiten zu WP-001, WP-002, WP-003, WP-004, WP-005 und WP-007. Die Verifikation prüft das Gesamtergebnis der Phase 1 und ist erst nach dessen Vorliegen aussagefähig. Eine vorgezogene Prüfung wäre unvollständig und damit ohne Nachweiswert. |
| Vorbedingungen | Alle Phase-1-Pakete abgeschlossen; API-01 bis API-04 unverändert; SDK API 1.0.0 unverändert |
| Ergebnis der Phase | Nachweis, dass alle Erweiterungen additiv erfolgt sind und bestehende Konsumenten unverändert funktionieren. Abschluss der Umsetzungssequenz. |

---

### 6.4 Dependency Matrix

#### Normative Abhängigkeiten

| Work Package | Kategorie | Direkte Vorgänger | Direkte Nachfolger | Blockierende Abhängigkeiten | Optionale Abhängigkeiten | Parallelisierbar mit |
|---|---|---|---|---|---|---|
| WP-001 | Provider | — | WP-006 | Keine | Keine | WP-002, WP-003, WP-004, WP-005, WP-007 |
| WP-002 | Provider | — | WP-006 | Keine | Keine | WP-001, WP-003, WP-004, WP-005, WP-007 |
| WP-003 | Provider | — | WP-006 | Keine | Keine | WP-001, WP-002, WP-004, WP-005, WP-007 |
| WP-004 | Provider | — | WP-006 | Keine | Keine | WP-001, WP-002, WP-003, WP-005, WP-007 |
| WP-005 | Provider | — | WP-006 | Keine | Keine | WP-001, WP-002, WP-003, WP-004, WP-007 |
| WP-006 | Dependent | WP-001, WP-002, WP-003, WP-004, WP-005, WP-007 | — | WP-001, WP-002, WP-003, WP-004, WP-005, WP-007 | Keine | Keine |
| WP-007 | Provider | — | WP-006 | Keine | WP-002, WP-004 (inhaltlich, nicht blockierend) | WP-001, WP-002, WP-003, WP-004, WP-005 |

#### Optionale Abhängigkeiten

Optionale Abhängigkeiten sind inhaltliche Bezüge, die die Reihenfolge **nicht**
erzwingen. Sie sind aus den Querbezügen der Delta Analysis (Kapitel 4.8)
abgeleitet und ändern den genehmigten Abhängigkeitsgraphen nicht.

| Von | Nach | Art des Bezugs | Wirkung |
|---|---|---|---|
| WP-007 | WP-002 | Der Dokumentationsstand hängt vom Endzustand der Host-Dienste und Erweiterungspunkte ab (Verweis: Kapitel 4.8, DA-011) | Nicht blockierend. WP-007 kann beginnen; die abschließende Fassung setzt den Endstand von WP-002 voraus. |
| WP-007 | WP-004 | Der Dokumentationsstand hängt vom Endzustand der Observability-Erweiterung ab (Verweis: Kapitel 4.8, DA-011) | Nicht blockierend. Wirkung wie vorstehend. |

Die Engineering Specification führt WP-007 als Provider ohne eingehende
Abhängigkeiten. Diese Einstufung bleibt maßgeblich (Regel 5). Die hier
dokumentierten Bezüge sind Hinweise für die Ausführung, keine
Reihenfolgeänderung.

#### Graph

```
WP-001 ──┐
WP-002 ──┤
WP-003 ──┤
WP-004 ──┼──► WP-006
WP-005 ──┤
WP-007 ──┘

optional, nicht blockierend:
WP-002 ┄┄► WP-007
WP-004 ┄┄► WP-007
```

#### Zyklenfreiheit

| Prüfung | Ergebnis |
|---|---|
| Zyklische Abhängigkeiten im normativen Graphen | Keine |
| Selbstbezügliche Abhängigkeiten | Keine |
| Zyklen unter Einbeziehung der optionalen Bezüge | Keine — die optionalen Kanten laufen ausschließlich auf WP-007 zu, das keine ausgehenden Kanten außer zu WP-006 besitzt |

---

### 6.5 Critical Path

#### Bestimmungsgrundlage

Der kritische Pfad wird **strukturell** bestimmt, nicht zeitlich. Aufwands- und
Dauerangaben sind in diesem Kapitel ausgeschlossen; eine zeitliche
Kritikalitätsaussage ist daher weder möglich noch zulässig.

#### Kritischer Pfad

```
Baseline-Bestätigung (Kapitel 3)
        ↓
Vollständiger Abschluss aller Phase-1-Pakete
   (WP-001, WP-002, WP-003, WP-004, WP-005, WP-007)
        ↓
WP-006 — SDK Contract Verification
        ↓
Abschluss der Umsetzungssequenz
```

Die strukturell längste Kette verläuft über die optionalen Bezüge:

```
WP-002 / WP-004  ┄┄►  WP-007  ──►  WP-006
```

#### Warum dieser Pfad kritisch ist

| Grund | Erläuterung |
|---|---|
| WP-006 liegt auf jedem Pfad | Jedes Phase-1-Paket ist direkter Vorgänger von WP-006. Es gibt keinen Weg zum Abschluss, der WP-006 umgeht. |
| WP-006 ist nicht teilbar wirksam | Der Nachweis der Additivität bezieht sich auf das Gesamtergebnis der Phase 1. Eine Teilprüfung liefert keinen tragfähigen Nachweis. |
| Jedes Phase-1-Paket ist gleichrangig kritisch | Da alle sechs Provider blockierende Vorgänger von WP-006 sind, verzögert der Abschluss eines beliebigen von ihnen den Eintritt in Phase 2. Es gibt in Phase 1 kein unkritisches Paket. |
| WP-007 trägt die längste Kette | Über die optionalen Bezüge zu WP-002 und WP-004 entsteht die strukturell längste Abfolge. WP-007 ist damit der wahrscheinlichste Engpass innerhalb von Phase 1. |

#### Auswirkungen von Verzögerungen

| Verzögertes Element | Auswirkung |
|---|---|
| Baseline-Bestätigung (Kapitel 3) | Die gesamte Sequenz verschiebt sich; die Delta Analysis bleibt bis dahin unter Vorbehalt (4.2, Regel 5). |
| Ein beliebiges Phase-1-Paket | Phase 2 kann nicht beginnen. Die übrigen Phase-1-Pakete sind nicht betroffen und laufen weiter. |
| WP-002 oder WP-004 | Zusätzlich zur Wirkung auf Phase 2 verzögert sich die abschließende Fassung von WP-007 (optionaler Bezug). |
| WP-007 | Phase 2 kann nicht beginnen; zugleich bleibt die Dokumentationsgrundlage für die Abschlussprüfung unvollständig. |
| WP-006 | Die Umsetzungssequenz bleibt ohne Abschluss; die Nachweise zu FR-013 und FR-014 liegen nicht vor. |

#### Governance-Auswirkungen

| Auswirkung | Erläuterung |
|---|---|
| Quality Gates | Ohne Abschluss von WP-006 fehlen die Nachweise zu den vertragserhaltenden Anforderungen. Die zugehörigen Quality Gates können nicht bestanden werden. |
| Definition of Done | Die Definition of Done der Engineering Specification ist erst mit vollständigem Abschluss der Sequenz erfüllbar. |
| Baseline-Vorbehalt | Eine ausbleibende Baseline-Bestätigung hält die Planungsgrundlage im Vorbehalt und wirkt auf alle Positionen zurück. |
| GR-001 | Solange GR-001 den Status PENDING DECISION trägt, steht die Modulzuordnung unter Vorbehalt. Auf die **Reihenfolge** wirkt sich GR-001 nicht aus, da diese ausschließlich aus dem genehmigten Abhängigkeitsgraphen abgeleitet ist. |

#### Auswirkungen auf nachfolgende Kapitel

| Kapitel | Gegenstand | Auswirkung |
|---|---|---|
| Kapitel 8, 9 | Verifikation (PS-03) | Die Nachweispunkte sind entlang der hier festgelegten Sequenz anzuordnen; die Abschlussprüfung liegt in Phase 2. |
| Kapitel 12 | Migration (PS-04) | Die Überführung setzt die Phasenordnung voraus (12.7, Sequenzregel 4). |
| Kapitel 13 | Rollout (PS-05) | Der Rollout setzt den Abschluss von Phase 2 voraus (13.7, RS-01). |
| Kapitel 11 | Risiken (PS-06) | Die gleichrangige Kritikalität aller Phase-1-Pakete ist als Risikofaktor zu führen; abgebildet über Klasse RK-09 und RK-08 (11.4). |
| Sprint Planning Phase | Charter §8, Schritt 6 | Die Sprintbildung darf die Phasenordnung nicht durchbrechen; innerhalb von Phase 1 ist sie frei. |

---

### 6.6 Parallelization Assessment

#### Parallel vorbereitbar

| Work Packages | Begründung |
|---|---|
| WP-001, WP-002, WP-003, WP-004, WP-005, WP-007 | **Abhängigkeiten:** Sämtlich Provider ohne eingehende blockierende Abhängigkeiten (6.4). **Traceability:** Jedes Paket ist über eigene Functional Requirements und eigene Deltas verankert; es bestehen keine gemeinsamen Nachweisknoten, die eine Ordnung erzwingen. **Governance:** Keine Governance Constraint fordert eine Ordnung innerhalb von Phase 1. **Baseline:** Alle sechs Pakete setzen ausschließlich den bestätigten Baseline-Zustand voraus, nicht das Ergebnis eines anderen Pakets. |

#### Ausschließlich sequenziell

| Beziehung | Begründung |
|---|---|
| Phase 1 → WP-006 | **Abhängigkeiten:** WP-006 besitzt sechs blockierende Vorgänger (6.4). **Traceability:** FR-013 verlangt den Nachweis der Additivität über alle Erweiterungen; dieser Nachweis ist ohne das Gesamtergebnis der Phase 1 nicht führbar. **Governance:** FR-013 und FR-014 sind vertragserhaltende Anforderungen und ausdrücklich nicht scope-eröffnend; eine vorgezogene Teilprüfung würde den Prüfgegenstand verändern. **Baseline:** Der Nachweis bezieht sich auf die unveränderte öffentliche API und die Consumer-Kompatibilität — Prüfgegenstände, die erst nach Abschluss aller Erweiterungen abschließend bewertbar sind. |
| Baseline-Bestätigung → Phase 1 | **Baseline:** Ohne protokollierte Bestätigung gemäß Kapitel 3 fehlt der Referenzpunkt jeder Differenzbildung. **Governance:** PP-02 und PP-04 untersagen die Umsetzung gegen einen unbestätigten Ausgangszustand. |

#### Eingeschränkt parallel

| Beziehung | Begründung |
|---|---|
| WP-007 gegenüber WP-002 und WP-004 | **Abhängigkeiten:** Optionaler, nicht blockierender Bezug (6.4). Die Vorbereitung von WP-007 ist uneingeschränkt parallel möglich; die abschließende Fassung setzt den Endstand von WP-002 und WP-004 voraus. **Traceability:** Der Bezug ist als Nachweisbeziehung in Kapitel 4.8 dokumentiert. **Governance:** Die Einstufung von WP-007 als Provider bleibt unverändert (Regel 5). |

#### Nicht herangezogene Kriterien

Entwicklerkapazität, Verfügbarkeit, Aufwand und Termine sind für diese
Bewertung ausdrücklich **nicht** herangezogen worden. Die Parallelisierbarkeit
beschreibt eine strukturelle Zulässigkeit, keine Empfehlung zur gleichzeitigen
Ausführung.

---

### 6.7 Sequencing Constraints

Für dieses Kapitel gelten die folgenden Beschränkungen verbindlich:

| ID | Constraint | Grundlage |
|---|---|---|
| SQ-01 | **Keine neuen Functional Requirements.** Es gelten ausschließlich FR-001 bis FR-014. | PP-06, GC-01 |
| SQ-02 | **Keine neuen Acceptance Criteria.** Es gelten ausschließlich die 29 genehmigten Kriterien. | PP-06, GC-02 |
| SQ-03 | **Keine neuen Quality Gates.** Es gelten ausschließlich QG-001 bis QG-008. | PP-06, GC-03 |
| SQ-04 | **Keine neuen Work Packages.** Es gelten ausschließlich WP-001 bis WP-007. | GC-01, Regel 2 |
| SQ-05 | **Keine Architekturänderungen.** Die Reihenfolge bewegt sich innerhalb der eingefrorenen Architektur. | PP-03, GC-04 |
| SQ-06 | **Keine Scope-Erweiterung.** Die Sequenzierung erweitert den Umfang nicht. | PP-05, GC-07 |
| SQ-07 | **Keine Sprintplanung.** Zeitliche und kapazitive Zuordnung erfolgt in der Sprint Planning Phase. | Charter §8, Schritt 6 |
| SQ-08 | **Keine Implementierungsdetails.** Keine Dateireferenzen, kein Modulbezug, kein Klassendesign, keine Methoden, keine Algorithmen. | Kapitel 1.6, PP-04 |

Zusätzlich gilt: Die Positionsbezeichnungen 1a bis 1f begründen keine
Rangfolge. Eine Ableitung von Priorität aus der Nummerierung ist unzulässig.

---

### 6.8 Sequencing Verification

| Prüfung | Soll | Ist | Ergebnis |
|---|---|---|---|
| Work Packages in der Sequenz berücksichtigt | 7 | 7 | Vollständig |
| Work Packages mit dokumentierter Position | 7 | 7 | Vollständig |
| Work Packages mit dokumentiertem Zweck, Begründung, Vorbedingungen und Ergebnis | 7 | 7 | Vollständig |
| Work Packages in der Dependency Matrix | 7 | 7 | Vollständig |
| Dokumentierte blockierende Abhängigkeiten | 6 | 6 | Vollständig (alle auf WP-006 gerichtet) |
| Dokumentierte optionale Abhängigkeiten | 2 | 2 | Vollständig und als nicht blockierend gekennzeichnet |
| Zyklische Abhängigkeiten | 0 | 0 | Keine Zyklen |
| Selbstbezügliche Abhängigkeiten | 0 | 0 | Keine |
| Kritischer Pfad identifiziert | 1 | 1 | Identifiziert und strukturell begründet. Der Pfad besteht aus der verbindlichen Kette (Baseline-Bestätigung → Phase 1 → WP-006) und der innerhalb von Phase 1 strukturell längsten Teilkette über die optionalen Bezüge; beide sind in 6.5 als **ein** Pfad dargestellt, nicht als zwei konkurrierende. |
| Abweichungen von der genehmigten Implementation Sequence | 0 | 0 | Keine |
| Abweichungen vom genehmigten Abhängigkeitsgraphen | 0 | 0 | Keine |
| Neue Work Packages | 0 | 0 | Erfüllt (SQ-04) |
| Neue Functional Requirements / Acceptance Criteria / Quality Gates | 0 | 0 | Erfüllt (SQ-01..SQ-03) |
| Verletzungen der Bootstrap Baseline | 0 | 0 | Erfüllt (PP-02) |
| Verletzungen des Architecture Freeze | 0 | 0 | Erfüllt (PP-03, SQ-05) |
| Verletzungen von WAIVER-DEV-001 | 0 | 0 | Erfüllt — der Waiver trifft keine Reihenfolgeaussage; seine Closing Criteria sind über Kapitel 4 und 5 adressiert |
| Enthaltene Aufwands-, Kapazitäts- oder Terminaussagen | 0 | 0 | Erfüllt (SQ-07) |

#### Traceability der Sequenz

| Position | Work Package | Functional Requirements | Engineering Goals | Charter Objectives |
|---|---|---|---|---|
| 1a | WP-001 | FR-001, FR-002 | EG-001 | CO-001 |
| 1b | WP-002 | FR-003, FR-004 | EG-002 | CO-002, CO-003 |
| 1c | WP-003 | FR-005, FR-006 | EG-004 | CO-004 |
| 1d | WP-004 | FR-007, FR-008 | EG-005 | CO-005 |
| 1e | WP-005 | FR-009, FR-010 | EG-006 | CO-001, CO-005 |
| 1f | WP-007 | FR-011, FR-012 | EG-007 | CO-004, CO-006 |
| 2 | WP-006 | FR-013, FR-014 | EG-003 | CO-006 |

Alle 14 Functional Requirements, alle 7 Engineering Goals und alle 6 Charter
Objectives sind über die Sequenz abgedeckt. Es wird keine neue
Traceability-Ebene erzeugt; die Sequenz ordnet die bestehende Ebene Work
Package.

---

## 7. Implementation Strategy

### 7.1 Purpose

#### Zweck der Implementierungsstrategie

Dieses Kapitel beantwortet ausschließlich:

> **Nach welchen strategischen Prinzipien wird die genehmigte Engineering
> Specification umgesetzt?**

Es legt Grundsätze fest, keine Umsetzung. Nicht beantwortet werden: wie
einzelne Funktionen implementiert werden, welche Klassen oder Methoden
entstehen, welche Dateien geändert werden, welcher Sprint welche Aufgaben
übernimmt und welche Ressourcen oder Termine eingeplant werden.

#### Beziehung zur Engineering Specification

Die Strategie ist vollständig aus der Engineering Specification 1.0 abgeleitet.
Sie ordnet den genehmigten Anforderungen, Acceptance Criteria und Quality Gates
eine Umsetzungslogik zu, ohne deren Inhalt zu verändern. Sie erzeugt keine
Anforderung und keine Prüfbedingung.

#### Beziehung zu Kapitel 6

Kapitel 6 legt die **Reihenfolge** fest. Kapitel 7 legt die **Grundsätze** fest,
nach denen innerhalb dieser Reihenfolge gearbeitet wird. Die Strategie
respektiert die Sequenz vollständig; sie ordnet nicht um und führt keine
zusätzliche Ordnung ein.

| Kapitel | Frage |
|---|---|
| Kapitel 4 | Was muss geändert werden? |
| Kapitel 5 | Wo findet die Änderung statt? |
| Kapitel 6 | In welcher Reihenfolge? |
| **Kapitel 7** | **Nach welchen Grundsätzen?** |

#### Beziehung zu den nachfolgenden Kapiteln

| Nachfolgendes Kapitel | Gegenstand | Beitrag dieses Kapitels |
|---|---|---|
| Kapitel 8, 9 | Verifikation (PS-03) | 7.5 legt fest, **wann** Nachweise entstehen; Kapitel 8 legt fest, **womit** sie geführt werden, Kapitel 9 **mit welchen Testarten**. |
| Kapitel 12 | Migration (PS-04) | Die Prinzipien SP-03 (Baseline Preservation) und SP-07 (No Breaking Changes) bilden den Rahmen; übernommen als MP-01 und MP-03. |
| Kapitel 13 | Rollout (PS-05) | SP-06 (Verification Driven) bestimmt, dass keine Freigabefeststellung vor abgeschlossener Verifikation erfolgt; übernommen als RPR-04. |
| Kapitel 11 | Risiken (PS-06) | 7.6 liefert den Eskalationsweg für governance-relevante Risiken; in 11.5 als alleinige Schnittstelle bestätigt. |
| Sprint Planning Phase | Charter §8, Schritt 6 | SP-05 (Incremental Implementation) und SP-08 (Controlled Change) binden die Sprintbildung, ohne sie vorwegzunehmen. |

---

### 7.2 Strategic Principles

Die folgenden acht Prinzipien sind für die Umsetzung verbindlich. Sie
konkretisieren die Planungsprinzipien PP-01 bis PP-07 für die
Umsetzungsphase; sie ersetzen diese nicht.

| ID | Prinzip | Bedeutung und Begründung |
|---|---|---|
| SP-01 | **Governance First** | Kein Umsetzungsschritt nimmt eine ausstehende Genehmigung vorweg. Begründung: Die Autorisierung reicht derzeit ausschließlich bis zum Implementation Plan (Kapitel 1.6). Jede Vorwegnahme entwertet die Governance-Kette und den Approval Record. |
| SP-02 | **Traceability First** | Jede Umsetzungshandlung ist auf ein genehmigtes Element der Engineering Specification rückführbar. Begründung: Nicht rückverfolgbare Arbeit ist nicht prüfbar und kann kein Quality Gate bestehen (QG-005, QG-008). |
| SP-03 | **Baseline Preservation** | Bootstrap Baseline 1.0 bleibt in allen bestätigten Eigenschaften erhalten. Begründung: Die Baseline ist der Referenzpunkt jeder Differenzbildung; ihre Veränderung entwertet Delta Analysis und Regressionsaussage (Kapitel 3, Kapitel 4). |
| SP-04 | **Architecture Preservation** | Die Umsetzung bewegt sich innerhalb der eingefrorenen Architektur. Begründung: Architecture Book v2.0 ist APPROVED / FROZEN; Abweichungen erfordern eine neue Dokumentversion und einen ADR (GI-01, PP-03). |
| SP-05 | **Incremental Implementation** | Die Umsetzung erfolgt in abgeschlossenen, einzeln prüfbaren Schritten entlang der Work Packages. Begründung: Nur abgeschlossene Schritte erzeugen belastbare Nachweise; große, verschränkte Änderungen sind weder prüfbar noch rückholbar. |
| SP-06 | **Verification Driven** | Ein Arbeitsschritt gilt erst mit vorliegendem Nachweis als abgeschlossen. Begründung: Die Engineering Specification bindet den Abschluss an Acceptance Criteria und Quality Gates, nicht an die Fertigstellung von Arbeit. |
| SP-07 | **No Breaking Changes** | Alle Erweiterungen erfolgen additiv; bestehende öffentliche Symbole und Verträge bleiben unverändert. Begründung: FR-013 und FR-014 sind vertragserhaltende Anforderungen; API-01 bis API-04 stehen unter Änderungsschutz. |
| SP-08 | **Controlled Change** | Änderungen erfolgen ausschließlich innerhalb des genehmigten Scope und in dokumentierter Form. Begründung: Scope Creep ist als Risiko R-001 der Engineering Specification geführt und wird durch NFR-001, QG-003 und QG-008 kontrolliert. |

#### Konfliktregel

Stehen Prinzipien im Einzelfall in Spannung, gilt die Reihenfolge
SP-01 → SP-04 → SP-03 → SP-07 → SP-02 → SP-06 → SP-08 → SP-05. Governance,
Architektur- und Vertragsschutz haben Vorrang vor Umsetzungsökonomie. Die Regel
ist die Fortschreibung der Konfliktregel aus Kapitel 2.2.

---

### 7.3 Implementation Phases

Die strategischen Phasen entsprechen der genehmigten Implementation Sequence
und ihrer governance-seitigen Einfassung. Es werden **keine
Implementierungsphasen eingeführt, die über die genehmigte zweiphasige Sequenz
hinausgehen**: Phase B und Phase C sind die Phasen 1 und 2 der Engineering
Specification. Phase A und Phase D sind Governance-Phasen, die aus Kapitel 3
und dem Development Standard abgeleitet sind und keine Umsetzungsinhalte
enthalten.

Keine Phase enthält Sprintnummern, Zeit- oder Aufwandsangaben.

#### Phase A — Baseline Confirmation

| Feld | Inhalt |
|---|---|
| Ziel | Bestätigung des genehmigten Ausgangszustands |
| Zweck | Sicherstellen, dass der dokumentierte Baseline-Zustand mit dem Ist-Zustand übereinstimmt, bevor eine Differenz umgesetzt wird |
| Erwartetes Ergebnis | Protokollierte Bestätigung des Bestätigungsumfangs gemäß Kapitel 3.8; Aufhebung des Vorbehalts aus Kapitel 4.2 |
| Übergang zur nächsten Phase | Vollständige und protokollierte Bestätigung. Bei festgestellter Abweichung: Eskalation gemäß 7.6, kein Übergang. |
| Governance-Bezug | Kapitel 3; SP-01, SP-03 |

#### Phase B — Provider Implementation

| Feld | Inhalt |
|---|---|
| Ziel | Umsetzung der sechs Provider-Work-Packages (WP-001, WP-002, WP-003, WP-004, WP-005, WP-007) |
| Zweck | Herstellung der in der Engineering Specification geforderten Zielzustände in den voneinander unabhängigen Arbeitspaketen |
| Erwartetes Ergebnis | Alle sechs Work Packages abgeschlossen; die jeweils zugeordneten Acceptance Criteria nachgewiesen; die paketbezogenen Quality Gates prüfbar |
| Übergang zur nächsten Phase | Vollständiger Abschluss **aller** sechs Pakete. Ein Teilabschluss berechtigt nicht zum Übergang (Kapitel 6.5). |
| Governance-Bezug | Engineering Specification, Implementation Sequence Phase 1; Kapitel 6.3; SP-05, SP-06 |

#### Phase C — Contract Verification

| Feld | Inhalt |
|---|---|
| Ziel | Umsetzung von WP-006 — Nachweis von Additivität und Consumer-Kompatibilität |
| Zweck | Feststellung, dass das Gesamtergebnis der Phase B die bestehenden Verträge nicht verletzt |
| Erwartetes Ergebnis | Nachweise zu FR-013 und FR-014; QG-003 prüfbar; keine Verletzung von API-01 bis API-04 und SDK API 1.0.0 |
| Übergang zur nächsten Phase | Vollständig geführter Nachweis. Ein negatives Ergebnis führt zur Rückkehr in Phase B für die betroffenen Inhalte, nicht zur Fortsetzung. |
| Governance-Bezug | Engineering Specification, Implementation Sequence Phase 2; Kapitel 6.3; SP-06, SP-07 |

#### Phase D — Governance Closure

| Feld | Inhalt |
|---|---|
| Ziel | Formaler Abschluss des Milestones gemäß Governance-Prozess |
| Zweck | Prüfung sämtlicher Quality Gates und der Definition of Done sowie Erstellung der governance-seitigen Deliverables |
| Erwartetes Ergebnis | Alle Quality Gates geprüft; Definition of Done erfüllt; Milestone Review durchgeführt |
| Übergang zur nächsten Phase | Abschluss des Milestones. Offene Findings führen zurück in den Governance-Prozess (7.6). |
| Governance-Bezug | Development Standard v1.1, Lifecycle; Engineering Specification, Definition of Done und Deliverables; SP-01, SP-02 |

#### Phasenfolge

```
Phase A — Baseline Confirmation
        ↓
Phase B — Provider Implementation   (ES Phase 1)
        ↓
Phase C — Contract Verification     (ES Phase 2)
        ↓
Phase D — Governance Closure
```

---

### 7.4 Work Package Execution Strategy

Die folgenden Angaben sind strategisch. Sie enthalten keine technischen
Implementierungsdetails.

#### WP-001 — Platform Hardening

| Feld | Inhalt |
|---|---|
| Strategisches Ziel | Bestimmtheit der Plattform-Zustandsübergänge herstellen (FR-001, FR-002) |
| Voraussetzungen | Phase A abgeschlossen; BI-03 und BI-05 als Erhaltungsvorgabe; Baseline-Messreihe gemäß Anhang B.2 erhoben |
| Abschlusskriterium | Die zugeordneten Acceptance Criteria sind nachgewiesen; der AC-bezogene Anteil von QG-001 ist prüfbar. Der auf NFR-004 bezogene Anteil von QG-001 ist erst am Ende von Phase B prüfbar (Anhang B.12) und ist **nicht** Abschlusskriterium dieses Work Package. |
| Übergabe an nachfolgende Work Packages | Ergebnis geht als Prüfgegenstand in WP-006 ein (Additivitätsnachweis) |

#### WP-002 — Host Service & Extensibility

| Feld | Inhalt |
|---|---|
| Strategisches Ziel | Host-Dienste beschreibbar und abrufbar machen; Erweiterungspunkte definieren (FR-003, FR-004) |
| Voraussetzungen | Phase A abgeschlossen; API-04 als Änderungsschutz |
| Abschlusskriterium | Die zugeordneten Acceptance Criteria sind nachgewiesen; QG-002 ist prüfbar |
| Übergabe an nachfolgende Work Packages | Ergebnis geht in WP-006 (Prüfgegenstand) und inhaltlich in WP-007 ein (optionaler Bezug, Kapitel 6.4) |

#### WP-003 — Developer Experience

| Feld | Inhalt |
|---|---|
| Strategisches Ziel | Autorenvorgaben konsolidieren; Ablehnungs-Feedback strukturieren (FR-005, FR-006) |
| Voraussetzungen | Phase A abgeschlossen; PL-01 bis PL-05 unverändert |
| Abschlusskriterium | Die zugeordneten Acceptance Criteria sind nachgewiesen; QG-004 ist prüfbar; der pipelinebezogene Anteil an QG-006 ist erfüllt |
| Übergabe an nachfolgende Work Packages | Ergebnis geht als Prüfgegenstand in WP-006 ein |

#### WP-004 — Observability

| Feld | Inhalt |
|---|---|
| Strategisches Ziel | Plugin-Diagnostik bereitstellen; Observability erweiterbar machen (FR-007, FR-008) |
| Voraussetzungen | Phase A abgeschlossen; BI-06 unverändert |
| Abschlusskriterium | Die zugeordneten Acceptance Criteria sind nachgewiesen; QG-006 ist prüfbar |
| Übergabe an nachfolgende Work Packages | Ergebnis geht in WP-006 (Prüfgegenstand) und inhaltlich in WP-007 ein (optionaler Bezug, Kapitel 6.4) |

#### WP-005 — Reliability

| Feld | Inhalt |
|---|---|
| Strategisches Ziel | Wiederherstellungsverhalten definieren; Plugin-Ausfälle isolieren (FR-009, FR-010) |
| Voraussetzungen | Phase A abgeschlossen; BI-03, BI-04, BI-06 und PL-05 unverändert |
| Abschlusskriterium | Die zugeordneten Acceptance Criteria sind nachgewiesen; QG-007 ist prüfbar |
| Übergabe an nachfolgende Work Packages | Ergebnis geht als Prüfgegenstand in WP-006 ein |

#### WP-007 — Documentation

| Feld | Inhalt |
|---|---|
| Strategisches Ziel | SDK-Dokumentation vervollständigen; Architekturdokumentation nachführen (FR-011, FR-012) |
| Voraussetzungen | Phase A abgeschlossen; Architecture Freeze als unverrückbare Grenze; Endstand von WP-002 und WP-004 für die abschließende Fassung (nicht blockierend für den Beginn) |
| Abschlusskriterium | Die zugeordneten Acceptance Criteria sind nachgewiesen; QG-005 ist prüfbar |
| Übergabe an nachfolgende Work Packages | Ergebnis ist Voraussetzung der Abschlussprüfung in WP-006 und Nachweisgrundlage für QG-005 |

#### WP-006 — SDK Contract Verification

| Feld | Inhalt |
|---|---|
| Strategisches Ziel | Additivität und Consumer-Kompatibilität nachweisen (FR-013, FR-014) |
| Voraussetzungen | Vollständiger Abschluss aller sechs Provider-Work-Packages; API-01 bis API-04 und SDK API 1.0.0 unverändert |
| Abschlusskriterium | Die zugeordneten Acceptance Criteria sind nachgewiesen; QG-003 ist prüfbar |
| Übergabe an nachfolgende Work Packages | Keine. WP-006 schließt die Umsetzungssequenz ab und übergibt an Phase D. |

#### Übergabelogik

```
WP-001 ┐
WP-002 ┤ (auch inhaltlich ┄► WP-007)
WP-003 ┤
WP-004 ┤ (auch inhaltlich ┄► WP-007)
WP-005 ┤
WP-007 ┘ ──► WP-006 ──► Phase D
```

---

### 7.5 Verification Strategy

#### Grundsatz

Nachweise entstehen **mit** der Umsetzung, nicht nach ihr (SP-06). Ein
Arbeitsschritt ohne Nachweis gilt als nicht abgeschlossen.

Dieses Kapitel legt ausschließlich den **Zeitpunkt** der Nachweisführung fest.
Prüfmethoden, Testfälle und Testimplementierung sind nicht Gegenstand dieses
Kapitels.

#### Wann Nachweise entstehen

| Zeitpunkt | Nachweis |
|---|---|
| Ende Phase A | Protokoll der Baseline-Bestätigung (Kapitel 3.8) |
| Während jedes Work Package | Laufende Nachweisführung zu den dem Work Package zugeordneten Acceptance Criteria |
| Ende jedes Work Package | Vollständigkeit der paketbezogenen Nachweise als Abschlussbedingung (7.4) |
| Ende Phase B | Vollständigkeit der Nachweise aller sechs Provider-Pakete als Eintrittsbedingung in Phase C |
| Ende Phase C | Nachweise zu FR-013 und FR-014 |
| Phase D | Gesamtprüfung aller Quality Gates und der Definition of Done |

#### Wann Acceptance Criteria überprüft werden

Acceptance Criteria werden dem Work Package zugeordnet geprüft, dem ihr
Functional Requirement zugewiesen ist. Die Prüfung erfolgt spätestens zum
Abschluss dieses Work Package. Eine Verschiebung in eine spätere Phase ist
unzulässig, da sie die Abschlussbedingung des Work Package entwertet.

#### Wann Quality Gates überprüft werden

Die Prüfzeitpunkte ergeben sich aus dem Prüfumfang, den der
Quality-Gate-Katalog der Engineering Specification je Gate festlegt — also aus
den geprüften Acceptance Criteria **und** den geprüften Non-Functional
Requirements. Sie werden hier zugeordnet, nicht bestimmt.

| Quality Gate | Prüft AC aus | Prüft NFR | Frühestmöglicher Prüfzeitpunkt | Begründung |
|---|---|---|---|---|
| QG-001 — Platform Stability | WP-001 | NFR-002, NFR-004, NFR-008 | AC-Anteil: Abschluss WP-001 — **abschließend: Ende Phase B** | Der AC-Anteil und die auf NFR-002 und NFR-008 bezogenen Anteile sind mit Abschluss von WP-001 prüfbar. Der auf **NFR-004** bezogene Anteil setzt die Vergleichsmessreihe voraus, die gemäß Anhang B.8 am Ende von Phase B erhoben wird; vorher ist er nicht beurteilbar (Anhang B.12). |
| QG-002 — Host Service Availability | WP-002 | — | Abschluss WP-002 | Prüft ausschließlich Acceptance Criteria aus WP-002 |
| QG-004 — Developer Feedback Quality | WP-003 | — | Abschluss WP-003 | Prüft ausschließlich Acceptance Criteria aus WP-003 |
| QG-005 — Traceability Completeness | WP-007 | NFR-010 | Abschluss WP-007 | Prüft Acceptance Criteria aus WP-007; NFR-010 ist mit dem Dokumentationsstand desselben Work Package beurteilbar |
| QG-006 — Pipeline Security Compliance | WP-003, WP-004 | NFR-002, NFR-006 | Abschluss WP-003 **und** WP-004 | Prüft Acceptance Criteria aus beiden Work Packages; vor deren Abschluss nicht abschließend prüfbar |
| QG-007 — Test Coverage Maintenance | WP-005 | NFR-005, NFR-009 | Abschluss WP-005; abschließend am Ende von Phase B | Prüft Acceptance Criteria aus WP-005 sowie die Regressionsfreiheit gegenüber der Baseline, die erst nach Abschluss aller Provider-Pakete abschließend beurteilbar ist |
| QG-003 — Architecture Freeze Compliance | WP-006 | NFR-001, NFR-003 | Abschluss WP-006 | Prüft das Gesamtergebnis auf Additivität und Rückwärtskompatibilität |
| QG-008 — Governance Compliance | mehrere | NFR-007 | Phase D | Querschnittlich; prüft Acceptance Criteria aus mehreren Work Packages sowie die Governance-Konformität insgesamt |

**Feststellung:** **QG-001**, QG-006, QG-007 und QG-008 sind nicht innerhalb
eines einzelnen Work Package abschließbar. Diese Gates sind bei der Planung
der Nachweisführung gesondert zu führen; ihr Abschluss ist keine Bedingung für
den Abschluss eines einzelnen Work Package, sondern für den Abschluss der
jeweiligen Phase.

**Klarstellung zu QG-001.** Die Aufnahme von QG-001 in diese Feststellung ist
keine Änderung des Gate-Kriteriums. Der Quality-Gate-Katalog der Engineering
Specification weist QG-001 seit jeher NFR-004 („keine Performance-Regression")
zu; Anhang B macht ausschließlich das zugehörige Messverfahren nachweisbar
(Finding F-004, SC-06). Die Zuordnung eines geteilten Prüfzeitpunkts führt
weder ein neues Quality Gate noch ein neues Kriterium ein (ST-03, VC-03), sie
führt den Prüfzeitpunkt an den bereits genehmigten Prüfumfang heran.

#### Wann Governance überprüft wird

| Zeitpunkt | Governance-Prüfung |
|---|---|
| Vor Phase A | Genehmigung dieses Implementation Plans einschließlich Independent Review und Closing Criteria von WAIVER-DEV-001 |
| Übergang Phase A → B | Vorliegen der protokollierten Baseline-Bestätigung |
| Übergang Phase B → C | Vollständiger Abschluss aller Provider-Pakete |
| Übergang Phase C → D | Vollständig geführter Vertragsnachweis |
| Phase D | Governance-Audit (QG-008), Definition of Done, Milestone Review |
| Bei jedem festgestellten Verstoß | Eskalation gemäß 7.6, unabhängig vom Zeitpunkt |

---

### 7.6 Governance Escalation Strategy

#### Grundsatz

Bei jedem der nachstehenden Ereignisse wird die betroffene Arbeit
**unterbrochen** und der Sachverhalt eskaliert. Die Eskalation dokumentiert den
Sachverhalt; sie entscheidet ihn nicht. Dieses Kapitel gibt **keine Lösungen**
vor.

#### Eskalationstatbestände

| Tatbestand | Eskalationsweg | Entscheidungsinstanz | Rückkehr in den Governance-Prozess |
|---|---|---|---|
| **Governance-Verstoß** | Feststellung → Unterbrechung der betroffenen Arbeit → Dokumentation als Governance-Befund → Vorlage | Governance Architect / Release Authority | Nach dokumentierter Entscheidung; Fortsetzung erst nach Freigabe |
| **Baseline-Abweichung** | Feststellung → Unterbrechung → Dokumentation gegen den Bestätigungsumfang (Kapitel 3.8) → Vorlage | Governance-Entscheidung in Form eines ADR oder RDR (Baseline Change Control) | Nach Genehmigung des ADR oder RDR; die Baseline bleibt bis dahin maßgeblich |
| **Traceability-Verlust** | Feststellung → Dokumentation der betroffenen Kette → Vorlage | Independent Review im Rahmen der Plan- oder Milestone-Prüfung | Nach Wiederherstellung der Rückverfolgbarkeit; nicht rückverfolgbare Arbeit gilt als nicht abgeschlossen (SP-02) |
| **Architekturkonflikt** | Feststellung → Unterbrechung → Dokumentation des Konflikts gegen Architecture Book v2.0 → Vorlage | Governance Architect; Auflösung ausschließlich über eine neue Architecture-Book-Version und einen ADR | Nach Genehmigung; der Architecture Freeze bleibt bis dahin unverändert (SP-04) |
| **ADR-Konflikt** | Feststellung → Unterbrechung → Dokumentation gegen den betroffenen ADR → Vorlage | Governance Architect; Auflösung über einen neuen oder geänderten ADR | Nach Genehmigung des ADR; der bestehende ADR bleibt bis dahin maßgeblich |
| **Scope-Erweiterung** | Feststellung → Dokumentation als Future Item oder Governance-Befund → Vorlage | Governance Architect / Release Authority auf Grundlage von Charter und Engineering Specification | Nach Entscheidung; ohne Entscheidung keine Aufnahme in die Umsetzung (SP-08) |

#### Verbindliche Regeln

| # | Regel |
|---|---|
| 1 | Eine Eskalation wird dokumentiert, bevor die betroffene Arbeit fortgesetzt wird. |
| 2 | Die Umsetzung löst keinen Governance-Konflikt eigenständig auf (PP-04, SP-01). |
| 3 | Ein eskalierter Sachverhalt bleibt bis zur dokumentierten Entscheidung offen; ein Verstreichen ersetzt keine Entscheidung. |
| 4 | Nicht betroffene Arbeit läuft weiter. Eine Eskalation unterbricht den Milestone nicht insgesamt, sondern den betroffenen Umfang. |
| 5 | Offene Eskalationen sind bei jeder Governance-Prüfung des Milestones auszuweisen. |

#### Angewandtes Beispiel

GR-001 (Kapitel 11.10; Pending Resolution in Anhang A) ist nach diesem Muster
behandelt: festgestellt während der Planung, dokumentiert, mit Owner und
Review-Zuordnung versehen, Status **PENDING DECISION**, Entscheidung
ausdrücklich außerhalb der Autorisierungsgrenze dieses Plans. Der Eintrag löst
den Sachverhalt nicht auf.

Nach demselben Muster ist der aus dem Global Consistency Audit hervorgegangene
Entscheidungsbedarf zu den Closing Criteria von WAIVER-DEV-001 behandelt
worden: als **GDR-001** dokumentiert, der Entscheidungsinstanz vorgelegt,
nicht durch diesen Plan aufgelöst und am 2026-08-05 durch die zuständige
Instanz entschieden; die Umsetzung erfolgte über WAIVER-AMENDMENT-001
(Kapitel 5.5.1). Der Vorgang belegt den vollständigen Durchlauf des
Eskalationswegs von der Feststellung bis zur dokumentierten Entscheidung.

---

### 7.7 Strategy Constraints

| ID | Constraint | Grundlage |
|---|---|---|
| ST-01 | **Keine neuen Functional Requirements.** | PP-06, GC-01, SQ-01 |
| ST-02 | **Keine neuen Acceptance Criteria.** | PP-06, GC-02, SQ-02 |
| ST-03 | **Keine neuen Quality Gates.** | PP-06, GC-03, SQ-03 |
| ST-04 | **Keine Architekturänderungen.** | SP-04, PP-03, GC-04 |
| ST-05 | **Keine ADR-Änderungen und keine neuen ADRs.** | GC-05, Charter §8 |
| ST-06 | **Keine Scope-Erweiterung.** | SP-08, PP-05, GC-07 |
| ST-07 | **Keine Sprintplanung.** | Charter §8, Schritt 6 |
| ST-08 | **Keine Ressourcenplanung.** | Spätere Projektplanung; nicht Gegenstand des Plans |
| ST-09 | **Keine Zeitplanung.** | Spätere Projektplanung; Kapitel 6.5 (strukturelle statt zeitlicher Betrachtung) |
| ST-10 | **Keine Implementierungsdetails.** Keine Dateireferenzen, kein Moduldesign, keine Klassen, keine Methoden, keine Algorithmen, keine Testfälle, kein Deployment, kein Rollout. | Kapitel 1.6, PP-04 |

Zusätzlich gilt: Die strategischen Phasen A bis D begründen keine neuen
Umsetzungsinhalte. Phase B und C sind die genehmigten Phasen 1 und 2 der
Engineering Specification; Phase A und D enthalten ausschließlich
Governance-Handlungen.

---

### 7.8 Strategy Verification

| Prüfung | Soll | Ist | Ergebnis |
|---|---|---|---|
| Strategische Prinzipien mit Begründung | 8 | 8 | Vollständig |
| Prinzipien ohne Grundlage in genehmigten Dokumenten | 0 | 0 | Erfüllt |
| Strategische Phasen mit Ziel, Zweck, Ergebnis und Übergang | 4 | 4 | Vollständig |
| Phasen mit Umsetzungsinhalt über die genehmigte Sequenz hinaus | 0 | 0 | Erfüllt (ST-06) |
| Work Packages mit Ausführungsstrategie | 7 | 7 | Vollständig |
| Work Packages mit Voraussetzungen, Abschlusskriterium und Übergabe | 7 | 7 | Vollständig |
| Quality Gates mit zugeordnetem Prüfzeitpunkt | 8 | 8 | Vollständig |
| Eskalationstatbestände mit Weg, Instanz und Rückkehr | 6 | 6 | Vollständig |
| Ableitbarkeit aus der Engineering Specification | vollständig | vollständig | Erfüllt |
| Ableitbarkeit aus Kapitel 6 | vollständig | vollständig | Erfüllt — keine Abweichung von Sequenz oder Abhängigkeitsgraph |
| Neue Inhalte | 0 | 0 | Erfüllt |
| Neue Anforderungen | 0 | 0 | Erfüllt (ST-01..ST-03) |
| Neue Architekturentscheidungen | 0 | 0 | Erfüllt (ST-04, ST-05) |
| Verletzungen der Bootstrap Baseline | 0 | 0 | Erfüllt (SP-03) |
| Verletzungen von WAIVER-DEV-001 | 0 | 0 | Erfüllt — der Waiver trifft keine Strategieaussage; seine Closing Criteria sind über Kapitel 4 und 5 adressiert |
| Enthaltene Sprint-, Ressourcen- oder Terminaussagen | 0 | 0 | Erfüllt (ST-07..ST-09) |
| Enthaltene Implementierungsdetails | 0 | 0 | Erfüllt (ST-10) |

#### Reviewfähigkeit

| Kriterium | Bewertung |
|---|---|
| Jede Aussage auf ein genehmigtes Dokument oder ein vorangehendes Kapitel zurückführbar | Erfüllt |
| Prinzipien, Phasen, Work Packages, Verifikationszeitpunkte und Eskalationswege eindeutig identifiziert | Erfüllt |
| Keine offenen Platzhalter | Erfüllt |
| Offene Punkte ausgewiesen statt aufgelöst | Erfüllt — GR-001 (Kapitel 11.10, Anhang A), weiterhin offen; GDR-001 (Kapitel 5.5.1), ausgewiesen und inzwischen durch die Governance entschieden; Vorbehalt der Baseline-Bestätigung (Kapitel 4.2) |
| Für Independent Governance Review geeignet | Erfüllt |

---

## 8. Verification Planning

### 8.1 Purpose

#### Zweck

Dieses Kapitel definiert die Verifikationsplanung des Milestone 1.0. Es
beschreibt ausschließlich:

- welche Nachweise zu erbringen sind,
- wann diese entstehen,
- auf welcher Ebene sie geprüft werden,
- wie ihre Vollständigkeit festgestellt wird.

#### Abgrenzung

Dieses Kapitel beschreibt **nicht**: Testfälle, Implementierungsdetails,
Sprintplanung, Code, Ressourcenplanung, Terminplanung.

Die eigentliche Teststrategie wird in Kapitel 9 beschrieben.

#### Verhältnis zu Kapitel 7

Kapitel 7.5 legt die **Zeitpunkte** der Nachweisführung strategisch fest.
Kapitel 8 führt diese Festlegung aus: Es benennt die Nachweise, ordnet sie den
Engineering-Elementen zu und definiert ihre Abschlussbedingungen. Es weicht von
den Zeitpunkten aus 7.5 nicht ab.

---

### 8.2 Verification Objectives

| ID | Ziel |
|---|---|
| VO-01 | Vollständiger Nachweis aller genehmigten Functional Requirements |
| VO-02 | Vollständiger Nachweis aller Acceptance Criteria |
| VO-03 | Vollständiger Nachweis aller Quality Gates |
| VO-04 | Vollständige Traceability der gesamten Governance-Kette |
| VO-05 | Nachweis der Einhaltung aller Baseline-Invarianten |
| VO-06 | Nachweis der Erfüllung aller Closing Criteria von WAIVER-DEV-001 |
| VO-07 | Vorbereitung des Independent Reviews |

Die Ziele sind kumulativ. Kein Ziel ersetzt ein anderes; VO-01 bis VO-07 sind
sämtlich Voraussetzung des Milestone-Abschlusses.

---

### 8.3 Verification Levels

Der Nachweis erfolgt auf vier Ebenen. Jede Ebene besitzt eigene Nachweise.
**Keine Ebene ersetzt eine andere.**

| Ebene | Gegenstand | Prüfgegenstand | Ergebnis der Ebene |
|---|---|---|---|
| **VL-01** | Dokumente | Governance-Artefakte, Baseline-Bestätigung, Dokumentationsstand, Traceability | Dokumentarische Nachweise |
| **VL-02** | Work Packages | Acceptance Criteria je Work Package | Paketbezogene Nachweise |
| **VL-03** | Integration | Zusammenwirken über Work-Package-Grenzen, Regressionsfreiheit, API-Oberfläche, Pipeline | Übergreifende Nachweise |
| **VL-04** | Governance | Unverändertheit der normativen Eingaben, Waiver-Erfüllung, offene Findings | Governance-Nachweise |

#### Ebenenzuordnung der Verifikationsziele

| Ziel | VL-01 | VL-02 | VL-03 | VL-04 |
|---|---|---|---|---|
| VO-01 — Functional Requirements | — | ✓ | ✓ | — |
| VO-02 — Acceptance Criteria | — | ✓ | ✓ | — |
| VO-03 — Quality Gates | ✓ | ✓ | ✓ | ✓ |
| VO-04 — Traceability | ✓ | — | — | ✓ |
| VO-05 — Baseline-Invarianten | ✓ | — | ✓ | ✓ |
| VO-06 — Waiver Closing Criteria | ✓ | — | — | ✓ |
| VO-07 — Independent Review | ✓ | — | — | ✓ |

---

### 8.4 Verification Matrix

#### Kette

```
Charter Objective
        ↓
Engineering Goal
        ↓
Functional Requirement
        ↓
Work Package
        ↓
Acceptance Criteria
        ↓
Quality Gate
        ↓
Verification Evidence
```

Es werden **keine neuen Beziehungen eingeführt**. Die Kette entspricht der
kanonischen Verifikationskette der Engineering Specification, erweitert um den
Nachweisknoten Verification Evidence, der in 8.5 definiert wird.

#### Matrix

| CO | EG | FR | WP | Acceptance Criteria | Quality Gate | Evidence |
|---|---|---|---|---|---|---|
| CO-001 | EG-001 | FR-001 | WP-001 | AC-001.1, AC-001.2, AC-001.3 | QG-001 | EV-W01 |
| CO-001 | EG-001 | FR-002 | WP-001 | AC-002.1, AC-002.2 | QG-001 | EV-W01 |
| CO-003 | EG-002 | FR-003 | WP-002 | AC-003.1, AC-003.2 | QG-002, QG-008 | EV-W02, EV-G01 |
| CO-002 | EG-002 | FR-004 | WP-002 | AC-004.1, AC-004.2 | QG-002 | EV-W02 |
| CO-004 | EG-004 | FR-005 | WP-003 | AC-005.1, AC-005.2 | QG-004 | EV-W03 |
| CO-004 | EG-004 | FR-006 | WP-003 | AC-006.1, AC-006.2 | QG-004, QG-006 | EV-W03, EV-I02 |
| CO-005 | EG-005 | FR-007 | WP-004 | AC-007.1, AC-007.2 | QG-006 | EV-W04, EV-I02 |
| CO-005 | EG-005 | FR-008 | WP-004 | AC-008.1, AC-008.2 | QG-006 | EV-W04, EV-I02 |
| CO-001 | EG-006 | FR-009 | WP-005 | AC-009.1, AC-009.2 | QG-007 | EV-W05, EV-I01 |
| CO-005 | EG-006 | FR-010 | WP-005 | AC-010.1, AC-010.2 | QG-007 | EV-W05, EV-I01 |
| CO-004 | EG-007 | FR-011 | WP-007 | AC-011.1, AC-011.2 | QG-005 | EV-W07, EV-D04 |
| CO-006 | EG-007 | FR-012 | WP-007 | AC-012.1, AC-012.2 | QG-005, QG-008 | EV-W07, EV-D04, EV-G01 |
| CO-006 | EG-003 | FR-013 | WP-006 | AC-013.1, AC-013.2 | QG-003, QG-008 | EV-W06, EV-I03, EV-G01 |
| CO-006 | EG-003 | FR-014 | WP-006 | AC-014.1, AC-014.2 | QG-003, QG-008 | EV-W06, EV-I04, EV-G01 |

29 Acceptance Criteria, 14 Functional Requirements, 7 Work Packages, 8 Quality
Gates, 6 Charter Objectives, 7 Engineering Goals — vollständig abgebildet.

**Lesehinweis zur Evidence-Spalte.** Die Matrix ist FR-zentriert: Sie führt je
Functional Requirement die Nachweise seiner Acceptance Criteria. Quality Gates
prüfen nach dem Katalog der Engineering Specification zusätzlich
Non-Functional Requirements; deren Nachweise erscheinen daher nicht in dieser
Matrix, sondern in der Gate-Zuordnung in 8.5. Betroffen sind QG-001
(NFR-004 → EV-I01), QG-006, QG-007 und QG-008. Die vollständige
Evidence-Zuordnung je Gate steht ausschließlich in 8.5.

#### Mehrfach zugeordnete Acceptance Criteria

Die folgenden Acceptance Criteria werden von mehr als einem Quality Gate
geprüft. Sie sind erst mit Abschluss **aller** zugeordneten Gates vollständig
nachgewiesen.

| Acceptance Criterion | Quality Gates |
|---|---|
| AC-003.1 | QG-002, QG-008 |
| AC-006.2 | QG-004, QG-006 |
| AC-012.2 | QG-005, QG-008 |
| AC-013.2 | QG-003, QG-008 |
| AC-014.2 | QG-003, QG-008 |

---

### 8.5 Verification Evidence

Es werden ausschließlich **Nachweise** geplant. Keine Testfälle.

Die Prüfmethoden sind unverändert aus dem Quality-Gate-Katalog der Engineering
Specification übernommen. Verantwortlichkeiten sind als **Funktionen**
benannt; die personelle Zuordnung ist nicht Gegenstand dieses Plans (VC-09).

#### VL-01 — Dokumentenebene

| Evidence-ID | Quelle | Nachweisart | Verantwortlichkeit | Zeitpunkt | Prüfmethode | Abschlussbedingung |
|---|---|---|---|---|---|---|
| EV-D01 | Kapitel 3.8 — Bestätigungsumfang | Bestätigungsprotokoll der Baseline | Governance Architect | Ende Phase A | Dokumentenprüfung, Vollständigkeitsabgleich | BI-01..BI-07, API-01..API-04, BP-01..BP-04, PL-01..PL-05, GI-01..GI-12 protokolliert bestätigt |
| EV-D02 | WAIVER-DEV-001 §9 | Erfüllungsnachweis der Closing Criteria | Independent Review | Vor Phase A (Plangenehmigung) | Dokumentenprüfung | Alle vier Closing Criteria bestätigt (Kapitel 5.5.1) |
| EV-D03 | Kapitel 8.4 — Verification Matrix | Traceability-Audit | Independent Review | Phase D | Vollständigkeitsabgleich | Kette CO → EG → FR → WP → AC → QG → Evidence in beide Richtungen lückenlos |
| EV-D04 | WP-007 Ergebnis | Dokumentationsstand | Independent Review | Abschluss WP-007 | Dokumentenprüfung | SDK-Dokumentation vollständig; Architekturdokumentation aktuell; keine Widersprüche zum implementierten Stand |
| EV-D05 | Kapitel 11.11 — konsolidiertes Risikoregister; Anhang A — Pending Resolution GR-001; Findings-Übersicht 10.7 | Findings- und Risikoregisterstand | Governance Architect | Fortlaufend; abschließend Phase D | Dokumentenprüfung | Keine offenen Findings ohne dokumentierte Entscheidung; sämtliche Registereinträge CLOSED oder ACCEPTED |

#### VL-02 — Work-Package-Ebene

| Evidence-ID | Quelle | Nachweisart | Verantwortlichkeit | Zeitpunkt | Prüfmethode | Abschlussbedingung |
|---|---|---|---|---|---|---|
| EV-W01 | WP-001 | AC-Nachweis | Umsetzungsverantwortung WP-001 | Abschluss WP-001 | Automatisierte Testsuite, manuelle Verifikation der Zustandsmaschine | AC-001.1..AC-002.2 im Status VERIFIED. Der auf NFR-004 bezogene Anteil von QG-001 wird **nicht** über EV-W01, sondern über EV-I01 geführt (Anhang B.10). |
| EV-W02 | WP-002 | AC-Nachweis | Umsetzungsverantwortung WP-002 | Abschluss WP-002 | Integration Tests, ServiceRegistry-Verifikation | AC-003.1..AC-004.2 im Status VERIFIED |
| EV-W03 | WP-003 | AC-Nachweis | Umsetzungsverantwortung WP-003 | Abschluss WP-003 | Verifikation der Rejection-Nachrichten, Dokumentationsprüfung | AC-005.1..AC-006.2 im Status VERIFIED |
| EV-W04 | WP-004 | AC-Nachweis | Umsetzungsverantwortung WP-004 | Abschluss WP-004 | Pipeline-Verifikation, Tests | AC-007.1..AC-008.2 im Status VERIFIED |
| EV-W05 | WP-005 | AC-Nachweis | Umsetzungsverantwortung WP-005 | Abschluss WP-005 | Automatisierte Testsuite | AC-009.1..AC-010.2 im Status VERIFIED |
| EV-W06 | WP-006 | AC-Nachweis | Umsetzungsverantwortung WP-006 | Abschluss WP-006 | API-Surface-Vergleich, Review | AC-013.1..AC-014.2 im Status VERIFIED |
| EV-W07 | WP-007 | AC-Nachweis | Umsetzungsverantwortung WP-007 | Abschluss WP-007 | Dokumentenprüfung, Vollständigkeitsabgleich | AC-011.1..AC-012.2 im Status VERIFIED |

#### VL-03 — Integrationsebene

| Evidence-ID | Quelle | Nachweisart | Verantwortlichkeit | Zeitpunkt | Prüfmethode | Abschlussbedingung |
|---|---|---|---|---|---|---|
| EV-I01 | Regressionsbasis gemäß Kapitel 3.1; Baseline-Messreihe gemäß Anhang B.2 | Regressionsnachweis (funktional und performancebezogen) | Umsetzungsverantwortung, übergreifend | Ende Phase B | Automatisierte Testsuite; Vergleichsmessreihe und Regressionsbewertung gemäß Anhang B.8 | Baseline-Tests und hinzugekommene Tests bestanden; keine funktionale Regression; keine Performance-Regression gemäß Anhang B.8 |
| EV-I02 | Bootstrap Baseline 1.0, Plugin-Runtime-Pipeline | Pipeline-Nachweis | Umsetzungsverantwortung, übergreifend | Nach Abschluss WP-003 und WP-004 | Pipeline-Verifikation gegen die Baseline, Tests | Pipeline-Reihenfolge unverändert; Diagnoseinformationen mit Pipelinestufe; Observability erweiterbar |
| EV-I03 | API-01..API-04 | API-Oberflächenvergleich | Umsetzungsverantwortung WP-006 | Phase C | API-Surface-Vergleich gegen die eingefrorene Baseline | Keine eingefrorenen Symbole entfernt oder umbenannt; alle Erweiterungen additiv |
| EV-I04 | SDK API 1.0.0, Referenzplugin | Kompatibilitätsnachweis | Umsetzungsverantwortung WP-006 | Phase C | Kompatibilitätsprüfung, Review | Bestehende Konsumenten funktionieren unverändert |

#### VL-04 — Governance-Ebene

| Evidence-ID | Quelle | Nachweisart | Verantwortlichkeit | Zeitpunkt | Prüfmethode | Abschlussbedingung |
|---|---|---|---|---|---|---|
| EV-G01 | Normative Eingaben IN-01..IN-12 | Governance-Audit | Governance Architect | Phase D | Governance-Audit, Dokumentenprüfung | Keine Governance-Verletzungen; alle Änderungen rückverfolgbar; keine neuen externen Abhängigkeiten |
| EV-G02 | Engineering Specification, Definition of Done | Abschlussnachweis | Release Authority | Phase D | Dokumentenprüfung | Definition of Done vollständig erfüllt |
| EV-G03 | Development Standard v1.1, Lifecycle | Milestone Review | Independent Review | Phase D | Review | Milestone Review durchgeführt und dokumentiert |
| EV-G04 | Kapitel 3.7 — Governance-Invarianten | Unverändertheitsnachweis | Governance Architect | Phase D | Statusprüfung | GI-01..GI-12 unverändert; Abweichungen dokumentiert und entschieden |

#### Zuordnung Evidence zu Quality Gates

| Quality Gate | Evidence | Anmerkung |
|---|---|---|
| QG-001 | EV-W01, **EV-I01** | EV-W01 trägt den AC-Anteil, EV-I01 den auf NFR-004 bezogenen Anteil (Anhang B.10, B.12) |
| QG-002 | EV-W02 | — |
| QG-003 | EV-W06, EV-I03, EV-I04 | — |
| QG-004 | EV-W03 | — |
| QG-005 | EV-W07, EV-D04 | — |
| QG-006 | EV-W03, EV-W04, EV-I02 | — |
| QG-007 | EV-W05, EV-I01 | EV-I01 trägt den funktionalen Regressionsanteil |
| QG-008 | EV-G01, EV-G02, **EV-G03**, EV-G04, EV-D03, EV-D05 | EV-G03 (Milestone Review) ist Bestandteil der Governance-Verifikation in Phase D und in der Traceability von R-004 geführt |

#### Nachweise ohne Gate-Zuordnung

Zwei der zwanzig Nachweise sind keinem Quality Gate zugeordnet, weil sie außerhalb
der Gate-Prüfung wirken. Ihre Verwendung ist dennoch vollständig bestimmt:

| Evidence | Verwendung | Fundstelle |
|---|---|---|
| EV-D01 | Bestätigungspunkt GV-04 (Bootstrap Baseline unverändert); Austrittsbedingung Phase A; Eintrittsbedingung der Migrationssequenz MS-01 | 8.8, 7.3, 12.7 |
| EV-D02 | Bestätigungspunkt GV-06 (WAIVER-DEV-001 erfüllt); Voraussetzung der Plangenehmigung, nicht des Milestone-Abschlusses | 8.8, 10.3 (AP-02) |

Damit ist jeder der zwanzig Nachweise entweder einem Quality Gate oder einem
Governance-Bestätigungspunkt zugeordnet; kein Nachweis bleibt ohne Verwendung.

---

### 8.6 Acceptance Verification

Alle Acceptance Criteria werden unabhängig geprüft.

#### Regeln

| # | Regel |
|---|---|
| 1 | Jedes Acceptance Criterion besitzt einen Nachweis. |
| 2 | Jeder Nachweis besitzt einen Prüfer. |
| 3 | Jeder Prüfer dokumentiert das Ergebnis. |
| 4 | Jedes Acceptance Criterion besitzt genau einen Abschlussstatus. |

#### Statuswerte

| Status | Bedeutung |
|---|---|
| **NOT VERIFIED** | Nachweis noch nicht geführt. Ausgangsstatus jedes Acceptance Criterion. |
| **VERIFIED** | Nachweis vollständig geführt und dokumentiert. |
| **FAILED** | Nachweis geführt, Kriterium nicht erfüllt. |

Ein Acceptance Criterion im Status FAILED blockiert den Abschluss des
zugeordneten Work Package. Der Sachverhalt wird gemäß Kapitel 7.6 behandelt.

#### Statusübersicht zum Planungszeitpunkt

| Work Package | Acceptance Criteria | Anzahl | Status |
|---|---|---|---|
| WP-001 | AC-001.1, AC-001.2, AC-001.3, AC-002.1, AC-002.2 | 5 | NOT VERIFIED |
| WP-002 | AC-003.1, AC-003.2, AC-004.1, AC-004.2 | 4 | NOT VERIFIED |
| WP-003 | AC-005.1, AC-005.2, AC-006.1, AC-006.2 | 4 | NOT VERIFIED |
| WP-004 | AC-007.1, AC-007.2, AC-008.1, AC-008.2 | 4 | NOT VERIFIED |
| WP-005 | AC-009.1, AC-009.2, AC-010.1, AC-010.2 | 4 | NOT VERIFIED |
| WP-006 | AC-013.1, AC-013.2, AC-014.1, AC-014.2 | 4 | NOT VERIFIED |
| WP-007 | AC-011.1, AC-011.2, AC-012.1, AC-012.2 | 4 | NOT VERIFIED |
| **Summe** | | **29** | **NOT VERIFIED** |

Der Ausgangsstatus NOT VERIFIED ist der planmäßige Zustand vor Beginn der
Umsetzung. Er stellt kein Defizit dar.

---

### 8.7 Quality Gate Verification

#### Prüfregeln je Gate

| Quality Gate | Prüfebene | Abschlussregel |
|---|---|---|
| QG-001 — Platform Stability | VL-02, VL-03 | **Nicht innerhalb WP-001 abschließbar.** Der AC-Anteil ist mit Abschluss WP-001 prüfbar; der auf NFR-004 bezogene Anteil setzt EV-I01 voraus (Ende Phase B, Anhang B.12) |
| QG-002 — Host Service Availability | VL-02 | Innerhalb WP-002 abschließbar |
| QG-003 — Architecture Freeze Compliance | VL-02, VL-03 | Innerhalb WP-006 abschließbar; setzt den Abschluss aller Provider-Pakete voraus |
| QG-004 — Developer Feedback Quality | VL-02 | Innerhalb WP-003 abschließbar |
| QG-005 — Traceability Completeness | VL-01, VL-02 | Innerhalb WP-007 abschließbar |
| QG-006 — Pipeline Security Compliance | VL-02, VL-03 | **Querschnittlich.** Abschluss erst nach Abschluss aller abhängigen Work Packages (WP-003, WP-004) |
| QG-007 — Test Coverage Maintenance | VL-02, VL-03 | Abschluss erst nach vollständiger Regressionsprüfung (EV-I01, Ende Phase B) |
| QG-008 — Governance Compliance | VL-01, VL-04 | Abschluss ausschließlich nach vollständiger Governance-Verifikation (Phase D) |

#### Verbindliche Grundregel

> **Ein Quality Gate darf niemals geschlossen werden, solange abhängige Work
> Packages noch offen sind.**

Die Regel gilt ausnahmslos. Ein vorzeitig geschlossenes Gate ist ein
Governance-Verstoß und wird gemäß Kapitel 7.6 eskaliert.

#### Abhängige Work Packages je Gate

| Quality Gate | Abhängige Work Packages | Frühestmöglicher Abschluss |
|---|---|---|
| QG-001 | WP-001 sowie alle Provider-Pakete (Bezug NFR-004 über die Vergleichsmessreihe) | Ende Phase B |
| QG-002 | WP-002 | Abschluss WP-002 |
| QG-004 | WP-003 | Abschluss WP-003 |
| QG-005 | WP-007 | Abschluss WP-007 |
| QG-006 | WP-003, WP-004 | Abschluss beider Pakete |
| QG-007 | WP-005 sowie alle Provider-Pakete (Regressionsbezug) | Ende Phase B |
| QG-003 | WP-006 und damit mittelbar alle Provider-Pakete | Ende Phase C |
| QG-008 | Alle sieben Work Packages | Phase D |

---

### 8.8 Governance Verification

Vor dem Abschluss des Milestones sind die folgenden Punkte zu bestätigen.

| # | Bestätigungspunkt | Bezug | Evidence |
|---|---|---|---|
| GV-01 | Milestone 1.0 Charter unverändert | GI-03 | EV-G04 |
| GV-02 | Engineering Specification 1.0 unverändert | GI-04 | EV-G04 |
| GV-03 | Architecture Book v2.0 unverändert | GI-01 | EV-G04 |
| GV-04 | Bootstrap Baseline 1.0 unverändert | GI-05 | EV-D01, EV-G04 |
| GV-05 | ADR-005, ADR-006, ADR-007, ADR-011 unverändert | GI-07..GI-10 | EV-G04 |
| GV-06 | WAIVER-DEV-001 vollständig erfüllt | GI-11 | EV-D02 |
| GV-07 | Traceability vollständig | VO-04 | EV-D03 |
| GV-08 | Keine offenen Governance Findings | Kapitel 10.7 (Findings-Übersicht); Kapitel 11.11; Anhang A | EV-D05 |

#### Bedingung

Alle acht Punkte müssen bestätigt sein. Ein offener Punkt verhindert den
Milestone-Abschluss und wird gemäß Kapitel 7.6 behandelt.

**Hinweis zu GV-08:** GR-001 trägt zum Planungszeitpunkt den Status
**PENDING DECISION** (Kapitel 11.6, 11.11). Die Bestätigung von GV-08 setzt
eine dokumentierte Entscheidung zu GR-001 voraus. Diese Entscheidung liegt
außerhalb der Autorisierungsgrenze dieses Plans (Kapitel 1.6).

---

### 8.9 Verification Completion

Die Verifikationsplanung gilt als vollständig, wenn sämtliche folgenden
Bedingungen erfüllt sind:

| # | Bedingung | Soll | Ist | Ergebnis |
|---|---|---|---|---|
| 1 | Alle Work Packages besitzen einen Nachweis | 7 | 7 | Erfüllt |
| 2 | Alle Functional Requirements sind zugeordnet | 14 | 14 | Erfüllt |
| 3 | Alle Acceptance Criteria sind geplant | 29 | 29 | Erfüllt |
| 4 | Alle Quality Gates sind geplant | 8 | 8 | Erfüllt |
| 5 | Alle Closing Criteria von WAIVER-DEV-001 sind berücksichtigt | 4 | 4 | Erfüllt (EV-D02) |
| 6 | Alle Baseline-Invarianten sind berücksichtigt | BI, API, BP, PL, GI | vollständig | Erfüllt (EV-D01, EV-G04) |
| 7 | Keine ungeprüften Elemente verbleiben | 0 | 0 | Erfüllt |
| 8 | Alle Verifikationsziele sind einer Ebene zugeordnet | 7 | 7 | Erfüllt (8.3) |
| 9 | Alle Evidence-Einträge besitzen Quelle, Art, Verantwortlichkeit, Zeitpunkt, Prüfmethode und Abschlussbedingung | 20 | 20 | Erfüllt |
| 10 | Alle Quality Gates besitzen zugeordnete Evidence | 8 | 8 | Erfüllt |

#### Feststellung

Die Verifikationsplanung ist vollständig. Kapitel 9 (Test Strategy) setzt auf
dieser Planung auf und konkretisiert die Prüfmethoden; es verändert die hier
festgelegten Nachweise, Zeitpunkte und Abschlussbedingungen nicht.

---

### 8.10 Verification Constraints

| ID | Constraint | Grundlage |
|---|---|---|
| VC-01 | Keine neuen Functional Requirements | PP-06, GC-01, ST-01 |
| VC-02 | Keine neuen Acceptance Criteria | PP-06, GC-02, ST-02 |
| VC-03 | Keine neuen Quality Gates | PP-06, GC-03, ST-03 |
| VC-04 | Keine Erweiterung der Traceability | PP-01; die Kette bleibt die kanonische Kette der Engineering Specification |
| VC-05 | Keine Architekturentscheidungen | SP-04, PP-03, ST-04 |
| VC-06 | Keine Implementierungsentscheidungen | Kapitel 1.6, ST-10 |
| VC-07 | Keine Testfälle | Kapitel 9 |
| VC-08 | Keine Sprintplanung | Charter §8, Schritt 6; ST-07 |
| VC-09 | Keine Ressourcenplanung | ST-08; Verantwortlichkeiten sind als Funktion, nicht als Person benannt |
| VC-10 | Keine Terminplanung | ST-09; Zeitpunkte sind Phasen- und Abschlussbezüge, keine Termine |

**Klarstellung zu VC-04:** Der in 8.4 eingeführte Knoten Verification Evidence
ist keine neue Traceability-Ebene, sondern die Nachweisseite der bestehenden
Kette. Er verändert keine genehmigte Zuordnung.

**Klarstellung zu VC-10:** Sämtliche Zeitangaben dieses Kapitels sind
Bezugspunkte in der Phasen- und Work-Package-Folge (Kapitel 6, Kapitel 7.3).
Kalendarische Termine sind nicht enthalten.

---

## 9. Test Strategy

### 9.1 Purpose

#### Zweck

Dieses Kapitel definiert die Teststrategie des Milestone 1.0. Es beschreibt:

- welche Arten von Tests durchgeführt werden,
- welche Ziele die Tests verfolgen,
- wie die Quality Gates unterstützt werden,
- welche Nachweise erzeugt werden.

#### Abgrenzung

Dieses Kapitel beschreibt **nicht**: Testimplementierungen, Testcode, einzelne
Testfälle, Testskripte, Framework-Konfigurationen.

#### Verhältnis zu Kapitel 8

Kapitel 8 legt fest, **welche Nachweise** zu erbringen sind und **wann** sie
entstehen. Kapitel 9 legt fest, **mit welchen Testarten** diese Nachweise
geführt werden. Die in Kapitel 8 definierten Evidence-Einträge, Zeitpunkte und
Abschlussbedingungen bleiben unverändert.

Die Teststufen und Testprinzipien der Engineering Specification sind
unverändert übernommen. Dieses Kapitel ordnet sie den Verifikationszielen zu;
es definiert keine eigenen.

---

### 9.2 Test Objectives

| ID | Ziel | Bezug |
|---|---|---|
| TO-01 | Nachweis aller Functional Requirements | FR-001..FR-014 |
| TO-02 | Nachweis aller Acceptance Criteria | 29 Acceptance Criteria |
| TO-03 | Nachweis aller Quality Gates | QG-001..QG-008 |
| TO-04 | Nachweis aller Non-Functional Requirements | NFR-001..NFR-010 |
| TO-05 | Nachweis der vollständigen Regression gegenüber Bootstrap Baseline 1.0 | NFR-005; Regressionsbasis gemäß Kapitel 3.1 |
| TO-06 | Nachweis der Consumer-Kompatibilität | FR-014, NFR-003, API-03 |
| TO-07 | Nachweis der Architekturkonformität | NFR-001, NFR-002, NFR-006; GI-01 |
| TO-08 | Nachweis sämtlicher Closing Criteria von WAIVER-DEV-001 | WAIVER-DEV-001 §9 |

#### Verhältnis zu den Verifikationszielen

| Test Objective | Verifikationsziel (Kapitel 8.2) |
|---|---|
| TO-01, TO-02 | VO-01, VO-02 |
| TO-03 | VO-03 |
| TO-04, TO-05, TO-06, TO-07 | VO-03, VO-05 |
| TO-08 | VO-06 |

TO-01 bis TO-08 erzeugen keine neuen Ziele. Sie sind die testseitige Sicht auf
VO-01 bis VO-07.

---

### 9.3 Test Levels

Vier Testebenen. **Keine Ebene ersetzt eine andere.**

| Ebene | Bezeichnung | Gegenstand | Teststufen der Engineering Specification |
|---|---|---|---|
| **TL-01** | Component Verification | Einzelne Komponenten isoliert | Unit Tests |
| **TL-02** | Integration Verification | Zusammenspiel mehrerer Komponenten, Pipeline, Fehlerverhalten | Integration Tests, Security Tests, Recovery Tests |
| **TL-03** | Regression Verification | Unverändertheit des bestehenden Verhaltens und der bestehenden Verträge | Gesamte Testsuite, Compatibility Tests |
| **TL-04** | Governance Verification | Dokumentenstand, Traceability, Unverändertheit der normativen Eingaben | Review, Dokumentenprüfung, Governance-Audit |

#### Zuordnung zu den Verifikationsebenen

| Testebene | Verifikationsebene (Kapitel 8.3) |
|---|---|
| TL-01 | VL-02 |
| TL-02 | VL-02, VL-03 |
| TL-03 | VL-03 |
| TL-04 | VL-01, VL-04 |

#### Testprinzipien

Die Testprinzipien der Engineering Specification gelten unverändert:
kein Qt-Event-Loop außer für UI-Tests, deterministisches Verhalten ohne
Wartezeiten und externe Abhängigkeiten, Isolation je Test, explizite Prüfung
der Thread-Sicherheit.

Die Zuordnung zu Testverzeichnissen ist in der Engineering Specification und
in Kapitel 5 geführt und wird hier nicht wiederholt.

---

### 9.4 Test Categories

| ID | Kategorie | Zweck | Testebene | Abgedeckte Acceptance Criteria |
|---|---|---|---|---|
| **TC-01** | Functional Tests | Nachweis des geforderten fachlichen Verhaltens | TL-01, TL-02 | AC-001.x, AC-002.x, AC-003.x, AC-004.x, AC-006.x, AC-007.x, AC-008.x, AC-009.x, AC-010.x |
| **TC-02** | Regression Tests | Nachweis der Unverändertheit bestehenden Verhaltens | TL-03 | Querschnittlich; Bezugsgröße ist die Regressionsbasis |
| **TC-03** | Compatibility Tests | Nachweis der Rückwärtskompatibilität für bestehende Konsumenten | TL-03 | AC-013.x, AC-014.x |
| **TC-04** | Documentation Verification | Nachweis von Vollständigkeit und Aktualität der Dokumentation | TL-04 | AC-005.x, AC-011.x, AC-012.x |
| **TC-05** | Architecture Verification | Nachweis der Konformität mit Architecture Freeze und Baseline | TL-03, TL-04 | AC-013.x; querschnittlich zu NFR-001, NFR-002, NFR-006 |
| **TC-06** | Governance Verification | Nachweis der Governance-Konformität und Traceability | TL-04 | AC-003.1, AC-012.2, AC-013.2, AC-014.2 |

#### Kategorien je Quality Gate

| Quality Gate | Testkategorien |
|---|---|
| QG-001 — Platform Stability | TC-01, TC-02 |
| QG-002 — Host Service Availability | TC-01 |
| QG-003 — Architecture Freeze Compliance | TC-03, TC-05 |
| QG-004 — Developer Feedback Quality | TC-01, TC-04 |
| QG-005 — Traceability Completeness | TC-04 |
| QG-006 — Pipeline Security Compliance | TC-01, TC-05 |
| QG-007 — Test Coverage Maintenance | TC-01, TC-02 |
| QG-008 — Governance Compliance | TC-06 |

#### Non-Functional Requirements je Kategorie

| NFR | Prüfende Kategorie | Zugeordnetes Quality Gate |
|---|---|---|
| NFR-001 — Architecture Freeze Compliance | TC-05 | QG-003 |
| NFR-002 — Bootstrap Baseline Invariants | TC-05 | QG-001, QG-006 |
| NFR-003 — SDK API Backward Compatibility | TC-03 | QG-003 |
| NFR-004 — Performance Non-Degradation | TC-02 | QG-001 |
| NFR-005 — Test Regression Baseline | TC-02 | QG-007 |
| NFR-006 — Security Pipeline Compliance | TC-05 | QG-006 |
| NFR-007 — No External Dependencies | TC-06 | QG-008 |
| NFR-008 — Deterministic Behavior | TC-01 | QG-001 |
| NFR-009 — Error Handling & Graceful Degradation | TC-01 | QG-007 |
| NFR-010 — Documentation Currency | TC-04 | QG-005 |

Alle zehn Non-Functional Requirements sind einer Kategorie und einem Quality
Gate zugeordnet (TO-04).

**Hinweis zu NFR-004:** Die Messmethodik für den Nachweis der
Performance-Nichtverschlechterung ist gemäß Finding F-004 des Independent
Review der Engineering Specification in diesem Plan zu definieren. Die
Festlegung erfolgt in **Anhang B — Performance Measurement Methodology**
(SC-06) und nicht hier; dieses Kapitel weist ausschließlich die Zuordnung aus.

---

### 9.5 Test Traceability

#### Kette

```
Charter Objective
        ↓
Engineering Goal
        ↓
Functional Requirement
        ↓
Acceptance Criterion
        ↓
Quality Gate
        ↓
Test Category
        ↓
Evidence
```

**Keine neue Governance-Ebene.** Die Testkategorie ist eine Prüfsicht auf die
bestehende Kette, kein zusätzlicher Genehmigungsknoten. Sie steht zwischen
Quality Gate und Evidence und ersetzt keine bestehende Zuordnung.

#### Traceability-Tabelle

| FR | AC-Gruppe | Quality Gate | Test Category | Testebene | Evidence |
|---|---|---|---|---|---|
| FR-001 | AC-001.x | QG-001 | TC-01, TC-02 | TL-01, TL-02 | EV-W01 |
| FR-002 | AC-002.x | QG-001 | TC-01 | TL-01, TL-02 | EV-W01 |
| FR-003 | AC-003.x | QG-002, QG-008 | TC-01, TC-06 | TL-02, TL-04 | EV-W02, EV-G01 |
| FR-004 | AC-004.x | QG-002 | TC-01 | TL-02 | EV-W02 |
| FR-005 | AC-005.x | QG-004 | TC-04 | TL-04 | EV-W03 |
| FR-006 | AC-006.x | QG-004, QG-006 | TC-01, TC-05 | TL-01, TL-02 | EV-W03, EV-I02 |
| FR-007 | AC-007.x | QG-006 | TC-01, TC-05 | TL-01, TL-02 | EV-W04, EV-I02 |
| FR-008 | AC-008.x | QG-006 | TC-01, TC-05 | TL-01, TL-02 | EV-W04, EV-I02 |
| FR-009 | AC-009.x | QG-007 | TC-01, TC-02 | TL-02, TL-03 | EV-W05, EV-I01 |
| FR-010 | AC-010.x | QG-007 | TC-01, TC-02 | TL-02, TL-03 | EV-W05, EV-I01 |
| FR-011 | AC-011.x | QG-005 | TC-04 | TL-04 | EV-W07, EV-D04 |
| FR-012 | AC-012.x | QG-005, QG-008 | TC-04, TC-06 | TL-04 | EV-W07, EV-D04, EV-G01 |
| FR-013 | AC-013.x | QG-003, QG-008 | TC-05, TC-06 | TL-03, TL-04 | EV-W06, EV-I03, EV-G01 |
| FR-014 | AC-014.x | QG-003, QG-008 | TC-03, TC-06 | TL-03, TL-04 | EV-W06, EV-I04, EV-G01 |

Alle 14 Functional Requirements sind einer Testkategorie und einem Nachweis
zugeordnet (TO-01, TO-02).

Die Tabelle ist wie die Matrix in 8.4 FR-zentriert. Die auf Non-Functional
Requirements bezogenen Anteile der Quality Gates sind in 9.4 („Non-Functional
Requirements je Kategorie") geführt und in 8.5 den Nachweisen zugeordnet — für
QG-001 insbesondere NFR-004 über TC-02 und EV-I01.

---

### 9.6 Regression Strategy

#### Grundlage

Bootstrap Baseline 1.0 — Regressionsbasis gemäß Kapitel 3.1: 1019 Tests
bestanden, 0 Regressionen, Import- und Consumer-Kompatibilität verifiziert.

#### Ziel

**Keine Regressionen.**

#### Regeln

| # | Regel | Bezug |
|---|---|---|
| 1 | **Bestehende Funktionen bleiben erhalten.** Kein bestehendes Verhalten wird entfernt oder verändert. | SP-07, NFR-005 |
| 2 | **Bestehende APIs bleiben erhalten.** Keine öffentlichen Symbole werden entfernt, umbenannt oder in ihrem Verhalten verändert. | API-01..API-04, NFR-001, NFR-003 |
| 3 | **Bestehende Plugins bleiben kompatibel.** Konsumenten gegen SDK API 1.0.0 funktionieren unverändert. | FR-014, API-03, NFR-003 |
| 4 | **Bestehende Tests bleiben gültig.** Kein Baseline-Test wird entfernt oder abgeschwächt, um eine Änderung zu ermöglichen. | NFR-005 |

#### Wirkung

Der Regressionsnachweis (EV-I01) ist Voraussetzung für den Abschluss von
QG-007 und damit für den Übergang von Phase B nach Phase C. Ein Bruch einer
der vier Regeln ist keine Testfrage, sondern eine Baseline- oder
Vertragsabweichung und wird gemäß Kapitel 7.6 eskaliert.

#### Offener Bezug

Der Umfang der Regressionsbasis steht unter dem Vorbehalt von GR-001
(Kapitel 11.10; Pending Resolution in Anhang A), das den Status PENDING
DECISION trägt: Der Testbestand umfasst Artefakte beider in Kapitel 5.5.4
genannter Strukturen. Die Bezugsgröße des Regressionsnachweises ist mit der
Entscheidung zu GR-001 eindeutig festzulegen.

---

### 9.7 Verification Evidence

Für jede Testkategorie ist der Nachweis wie folgt geplant. Die Evidence-IDs
verweisen auf die in Kapitel 8.5 definierten Nachweise; es werden keine
zusätzlichen Nachweise eingeführt.

| Kategorie | Evidence-ID | Quelle | Nachweis | Prüfer | Status | Review | Archivierung |
|---|---|---|---|---|---|---|---|
| TC-01 — Functional Tests | EV-W01, EV-W02, EV-W03, EV-W04, EV-W05 | Work Packages WP-001 bis WP-005 | Ergebnis der automatisierten Testsuite und der Integrationsprüfungen je Work Package | Umsetzungsverantwortung des Work Package | NOT VERIFIED | Sprint Review | Sprint Reports (D-009) |
| TC-02 — Regression Tests | EV-I01 | Regressionsbasis gemäß Kapitel 3.1 | Ergebnis der vollständigen Testsuite ohne Regression | Umsetzungsverantwortung, übergreifend | NOT VERIFIED | Milestone Review | Milestone Review Report (D-010) |
| TC-03 — Compatibility Tests | EV-I04, EV-W06 | SDK API 1.0.0, Referenzplugin | Nachweis der unveränderten Funktion bestehender Konsumenten | Umsetzungsverantwortung WP-006 | NOT VERIFIED | Milestone Review | Milestone Review Report (D-010) |
| TC-04 — Documentation Verification | EV-W07, EV-D04 | WP-007, Dokumentationsstand | Dokumentenprüfung und Vollständigkeitsabgleich | Independent Review | NOT VERIFIED | Independent Review | Milestone Review Report (D-010) |
| TC-05 — Architecture Verification | EV-I02, EV-I03 | Architecture Book v2.0, Bootstrap Baseline 1.0 | API-Oberflächenvergleich und Pipeline-Verifikation gegen die eingefrorenen Referenzen | Umsetzungsverantwortung WP-006, Governance Architect | NOT VERIFIED | Independent Review | Milestone Review Report (D-010) |
| TC-06 — Governance Verification | EV-G01, EV-G02, EV-G03, EV-G04, EV-D01, EV-D02, EV-D03, EV-D05 | Normative Eingaben IN-01..IN-12, WAIVER-DEV-001, Kapitel 11.11, Anhang A | Governance-Audit, Traceability-Audit, Unverändertheits- und Erfüllungsnachweise | Governance Architect, Independent Review, Release Authority | NOT VERIFIED | Independent Review | Milestone Review Report (D-010) |

#### Regeln zur Nachweisführung

| # | Regel |
|---|---|
| 1 | Jeder Nachweis trägt genau einen Abschlussstatus: NOT VERIFIED, VERIFIED oder FAILED (Kapitel 8.6). |
| 2 | Der Ausgangsstatus sämtlicher Nachweise ist NOT VERIFIED. Dies ist der planmäßige Zustand vor Beginn der Umsetzung. |
| 3 | Ein Nachweis im Status FAILED blockiert das zugeordnete Quality Gate. |
| 4 | Nachweise werden mit dem Ergebnis dokumentiert, nicht nur mit dem Umstand ihrer Durchführung. |
| 5 | Die Archivierung erfolgt in den governance-seitigen Deliverables der Engineering Specification; es werden keine neuen Ablageartefakte eingeführt. |

---

### 9.8 Test Completion

Die Teststrategie gilt als vollständig, wenn sämtliche folgenden Bedingungen
erfüllt sind:

| # | Bedingung | Soll | Ist | Ergebnis |
|---|---|---|---|---|
| 1 | Alle Functional Requirements abgedeckt | 14 | 14 | Erfüllt (9.5) |
| 2 | Alle Acceptance Criteria abgedeckt | 29 | 29 | Erfüllt (9.4, 9.5) |
| 3 | Alle Quality Gates abgedeckt | 8 | 8 | Erfüllt (9.4) |
| 4 | Alle Non-Functional Requirements berücksichtigt | 10 | 10 | Erfüllt (9.4) |
| 5 | Vollständige Regression geplant | 1 | 1 | Erfüllt (9.6) |
| 6 | Vollständige Traceability vorhanden | 14 Ketten | 14 Ketten | Erfüllt (9.5) |
| 7 | Evidence vollständig definiert | 6 Kategorien | 6 Kategorien | Erfüllt (9.7) |
| 8 | Testebenen ohne Überschneidungsersatz | 4 | 4 | Erfüllt (9.3) |
| 9 | Testziele auf Verifikationsziele zurückgeführt | 8 | 8 | Erfüllt (9.2) |
| 10 | Neue Nachweise gegenüber Kapitel 8 eingeführt | 0 | 0 | Erfüllt (9.7) |

#### Offener Bezug

Bedingung 5 steht unter dem in 9.6 dokumentierten Vorbehalt zu GR-001. Die
Planung ist vollständig; die Bezugsgröße des Regressionsnachweises ist mit der
Entscheidung zu GR-001 festzulegen.

---

### 9.9 Test Constraints

| ID | Constraint | Grundlage |
|---|---|---|
| TCN-01 | Keine neuen Functional Requirements | PP-06, VC-01 |
| TCN-02 | Keine neuen Acceptance Criteria | PP-06, VC-02 |
| TCN-03 | Keine neuen Quality Gates | PP-06, VC-03 |
| TCN-04 | Keine neuen Testziele außerhalb der Engineering Specification | ES Test Strategy; TO-01..TO-08 sind vollständig abgeleitet |
| TCN-05 | Keine Implementierung von Tests | Kapitel 1.6 — nicht autorisiert |
| TCN-06 | Keine Testfälle | 9.1 |
| TCN-07 | Keine Testskripte | 9.1 |
| TCN-08 | Keine Framework-Konfiguration | 9.1 |
| TCN-09 | Keine Sprintplanung | Charter §8, Schritt 6; ST-07 |
| TCN-10 | Keine Terminplanung | ST-09; Zeitangaben sind Phasen- und Abschlussbezüge |

---

### 9.10 Security Test Readiness

Dieser Abschnitt schafft die Grundlage für spätere Sicherheitsverifikation,
**ohne neue Sicherheitsanforderungen einzuführen**. Er begründet keinen
zusätzlichen Scope.

| ID | Festlegung |
|---|---|
| **STR-01** | Der Implementation Plan weist nach, dass zukünftige sicherheitsrelevante Anforderungen **separat** verifiziert werden können: Die Testebene TL-02 und die Kategorien TC-05 und TC-06 sind so geschnitten, dass eine eigenständige Sicherheitsverifikation ohne Änderung der bestehenden Zuordnung ergänzt werden kann. |
| **STR-02** | Sicherheitsprüfungen **ersetzen keine** bestehenden Functional Requirements, sondern ergänzen sie. Die Nachweise zu FR-001 bis FR-014 bleiben in Umfang und Abschlussbedingung unverändert. |
| **STR-03** | Security Tests werden **erst nach** Definition einer Security Architecture und der zugehörigen Security ADRs konkretisiert. Vorher entstehen weder Sicherheitsanforderungen noch Sicherheitsprüfkriterien. |
| **STR-04** | Bis dahin bleiben die vorhandenen Governance-Artefakte die **alleinige Autorität**: Architecture Book v2.0, ADR-005, ADR-006, ADR-007, ADR-011, Bootstrap Baseline 1.0 und die Engineering Specification 1.0. |

#### Bestandsschutz der bestehenden Sicherheitsprüfung

Die Engineering Specification führt Security Tests bereits als Teststufe
(Default Deny, Adversarial Input, Permission Bypass). Diese bestehende
Prüfebene ist Bestandteil der Baseline und bleibt unverändert. Sie ist in
TL-02 abgebildet und über NFR-006 an QG-006 gebunden.

STR-01 bis STR-04 begründen keine Erweiterung dieser Prüfebene. Sie stellen
ausschließlich sicher, dass eine spätere Erweiterung anschlussfähig ist, ohne
die genehmigte Struktur zu verändern.

---

## 10. Completion, Approval & Readiness

### 10.1 Purpose

#### Zweck

Dieses Kapitel beschreibt ausschließlich den Übergang von der
**Implementation Planning** in die **Implementation Authorization**.

Es beantwortet:

> **Wann ist der Implementation Plan vollständig genehmigungsfähig, und unter
> welchen Bedingungen darf die Umsetzung beginnen?**

#### Abgrenzung

Dieses Kapitel ist keine Sprintplanung, keine Implementierung, keine
Testplanung, kein Deployment und kein Release. Es verändert keine Architektur.

Es definiert den Genehmigungsübergang und die daraus entstehende
Autorisierung — nicht deren Ausführung.

#### Beziehung zu Kapitel 8

Kapitel 8 definiert die Nachweise und ihre Abschlussbedingungen. Kapitel 10
bestimmt, welche dieser Nachweise **vor** der Genehmigung des Plans vorliegen
müssen und welche erst in der Umsetzung entstehen. Es verändert keine Evidence
und keinen Prüfzeitpunkt.

#### Beziehung zu Kapitel 9

Kapitel 9 definiert die Testarten zur Nachweisführung. Kapitel 10 setzt diese
Planung als Genehmigungsvoraussetzung an, ohne sie zu erweitern. Die in Kapitel
9 dokumentierten Vorbehalte gehen unverändert in die Completion Conditions ein.

#### Beziehung zum Development Standard

Der Development Standard v1.1 legt die verbindliche Lifecycle-Reihenfolge fest
und untersagt das Überspringen von Phasen. Kapitel 10 bildet die für den
Implementation Plan maßgeblichen Phasen — Review, Corrections, Approval — ab
und bindet die Autorisierung an deren vollständigen Durchlauf.

---

### 10.2 Approval Objectives

Die Genehmigungsziele sind aus den Engineering Goals, den Quality Gates und den
Governance-Prinzipien abgeleitet. Sie sind Ziele der **Plangenehmigung**, nicht
des Milestones.

| ID | Ziel | Ableitung |
|---|---|---|
| AO-01 | Der Plan bildet den genehmigten Umfang der Engineering Specification vollständig ab. | EG-001 bis EG-007; SC-01, SC-02 |
| AO-02 | Die Closing Criteria von WAIVER-DEV-001 sind erfüllt und nachgewiesen. | WAIVER-DEV-001 §9; SC-03, SC-04, SC-05 |
| AO-03 | Die Traceability ist in beide Richtungen lückenlos. | PP-01, SP-02; QG-005, QG-008 |
| AO-04 | Baseline und Architecture Freeze sind unversehrt. | PP-02, PP-03, SP-03, SP-04; QG-003, QG-006 |
| AO-05 | Für jedes nachzuweisende Element ist ein Nachweis geplant. | VO-01 bis VO-07; QG-001 bis QG-008 |
| AO-06 | Der Governance-Prozess ist vollständig und in der vorgeschriebenen Reihenfolge durchlaufen. | PP-04, SP-01; Development Standard v1.1, Lifecycle |
| AO-07 | Die Autorisierungsgrenze ist eindeutig und abschließend bestimmt. | Kapitel 1.6; Engineering Specification Approval Record |
| AO-08 | Der Plan ist unabhängig auditierbar. | SC-07, SC-08; Development Standard v1.1 |

Die Ziele sind kumulativ. Kein Ziel ersetzt ein anderes.

---

### 10.3 Approval Preconditions

Die folgenden Voraussetzungen müssen **vor** der Genehmigung des
Implementation Plans erfüllt sein.

| ID | Voraussetzung | Erfüllt durch | Status |
|---|---|---|---|
| AP-01 | **Offene Findings** — Kein Finding ohne dokumentierte Entscheidung oder dokumentierten Vorbehalt | Sämtliche Prüfartefakte gemäß der Findings-Übersicht in 10.7 | Erfüllt — jedes Finding trägt einen dokumentierten Status. Keine offenen Critical- oder High-Findings. Verbleibend: ein Editorial Finding (R2-E-01) sowie ein Entscheidungsbedarf im Zustand Pending Decision (GR-001) |
| AP-02 | **Offene Waiver** — Die Closing Criteria von WAIVER-DEV-001 sind adressiert | Kapitel 4, Kapitel 5.5.1 | Erfüllt — Bestätigung durch Independent Review ausstehend (§9 (3)) |
| AP-03 | **Governance** — Der Plan verletzt keine Governance Constraint | GC-01..GC-07, SQ-01..SQ-08, ST-01..ST-10, VC-01..VC-10, TCN-01..TCN-10 | Erfüllt |
| AP-04 | **Baseline** — Bootstrap Baseline 1.0 ist referenziert, ihr Bestätigungsumfang ist definiert | Kapitel 3 | Erfüllt — die Bestätigung selbst erfolgt in Phase A |
| AP-05 | **Architecture Freeze** — Keine Architekturänderung, keine ADR-Änderung | PP-03, SP-04, GI-01, GI-07..GI-10 | Erfüllt |
| AP-06 | **Evidence** — Für jedes nachzuweisende Element ist ein Nachweis definiert | Kapitel 8.5, Kapitel 9.7, Anhang B.10 | Erfüllt |
| AP-07 | **Review** — Independent Review des Plans ist durchgeführt | Development Standard v1.1, Lifecycle | **Ausstehend** |
| AP-08 | **Correction** — Sämtliche Review-Findings sind adressiert | Correction Phase | **Ausstehend** — abhängig von AP-07 |
| AP-09 | **Consistency** — Der Plan ist in sich widerspruchsfrei und vollständig gegenüber seinem eigenen Planungsscope | Kapitel 2.3 (PS-01..PS-06), Kapitel 10.7 | Erfüllt seit Kapitel 13 — sämtliche sechs Planungsgegenstände behandelt. Das Gesamtkonsistenzaudit (W-2) ist in den Revisionen R1 und R2 durchgeführt; sämtliche Findings sind abgearbeitet: 20 in Correction Cycle R1, H-01 durch WAIVER-AMENDMENT-001 |

Eine nicht erfüllte Voraussetzung verhindert die Genehmigung. Ein
dokumentierter Vorbehalt ist keine Nichterfüllung, sofern er normativ
ausgewiesen und mit Frist versehen ist.

---

### 10.4 Approval Workflow

#### Prozessschritte

| Schritt | Phase | Inhalt | Ergebnis |
|---|---|---|---|
| W-1 | Draft | Erstellung des Plans in kapitelweiser Abfolge | Vollständiger Plan im Status DRAFT |
| W-2 | Consistency Audit | Kapitelbezogene und gesamthafte Konsistenzprüfung durch den Ersteller | Audit Report je geprüftem Umfang |
| W-3 | Independent Review | Unabhängige Prüfung des Gesamtplans einschließlich der Closing Criteria von WAIVER-DEV-001 | Review Report mit Findings |
| W-4 | Correction | Adressierung sämtlicher Findings | Correction Report |
| W-5 | Re-Review | Erneute Prüfung der korrigierten Fassung und Bestätigung der Schließung | Supplementary Review Report |
| W-6 | Approval | Formale Genehmigungsentscheidung | Approval Record |
| W-7 | Statuswechsel | Überführung des Dokumentstatus DRAFT → APPROVED | Aktualisierte Dokumentenkontrolle |
| W-8 | Authorization | Erteilung der Autorisierung gemäß 10.6 und 10.10 | Governance Closing Summary |

Die Reihenfolge ist verbindlich. Kein Schritt darf übersprungen werden.

#### Freigabe

Die Freigabe entsteht ausschließlich durch W-6 in Verbindung mit W-7 und W-8.
Weder der Abschluss eines Kapitels noch das Ergebnis eines Consistency Audits
noch eine Review-Empfehlung erzeugen für sich genommen eine Freigabe.

#### Abbruchbedingungen

| ID | Bedingung | Wirkung |
|---|---|---|
| AB-01 | Ein Finding der Schweregrade Critical oder High ist offen | Kein Übergang nach W-6 |
| AB-02 | Eine Closing Criterion von WAIVER-DEV-001 ist nicht erfüllt | Kein Übergang nach W-6 |
| AB-03 | Der Plan deckt seinen eigenen Planungsscope nicht vollständig ab | Kein Übergang nach W-3; Rückkehr nach W-1 |
| AB-04 | Eine Baseline- oder Architekturabweichung ist festgestellt und nicht entschieden | Kein Übergang nach W-6; Eskalation gemäß Kapitel 7.6 |
| AB-05 | Eine Traceability-Kette ist unterbrochen | Kein Übergang nach W-6 |
| AB-06 | Der Plan führt neue Anforderungen, Kriterien oder Gates ein | Rückkehr nach W-1 mit Entfernung des unzulässigen Inhalts |

#### Rollback

| Ausgangslage | Rückkehrpunkt | Bedingung der Wiederaufnahme |
|---|---|---|
| Finding in W-3 oder W-5 | W-4 | Finding dokumentiert adressiert |
| Scope-Lücke gemäß AB-03 | W-1 | Fehlender Planungsinhalt ergänzt, anschließend erneut W-2 |
| Unzulässiger Inhalt gemäß AB-06 | W-1 | Inhalt entfernt, Auswirkung auf abhängige Kapitel geprüft |
| Baseline- oder Architekturabweichung gemäß AB-04 | Aussetzung des Workflows | Dokumentierte Governance-Entscheidung, gegebenenfalls ADR oder RDR |
| Genehmigung erteilt, nachträglicher Governance-Verstoß festgestellt | W-3 | Erneuter Review; die erteilte Autorisierung ruht bis zur Entscheidung |

Ein Rollback ist kein Fehlerfall, sondern der vorgesehene Weg zur Wahrung der
Governance-Kette.

---

### 10.5 Readiness Levels

Die Readiness Levels sind aufsteigend und werden ausschließlich vollständig
erreicht. Ein Teilerreichen ist nicht vorgesehen.

#### RL-00 — Planning

| Feld | Inhalt |
|---|---|
| Beschreibung | Der Plan befindet sich in kapitelweiser Erstellung. |
| Eintritt | Erteilung der Autorisierung zur Erstellung des Implementation Plan 1.0 (DRAFT) |
| Austritt | Sämtliche Planungsgegenstände gemäß Kapitel 2.3 sind behandelt |
| Kriterien | PS-01 bis PS-06 vollständig abgedeckt; keine offenen Kapitelzusagen |
| Nachweise | Kapitelbestand des Plans; Consistency Audits |

#### RL-01 — Review Ready

| Feld | Inhalt |
|---|---|
| Beschreibung | Der Plan ist vollständig und intern konsistent; er kann unabhängig geprüft werden. |
| Eintritt | Austritt aus RL-00 |
| Austritt | Independent Review durchgeführt |
| Kriterien | AP-01 bis AP-06 und AP-09 erfüllt; Gesamtkonsistenzaudit ohne offene Critical- oder High-Findings |
| Nachweise | Consistency Audit Reports; Vollständigkeitsnachweise der Kapitel |

#### RL-02 — Correction Complete

| Feld | Inhalt |
|---|---|
| Beschreibung | Sämtliche Findings des Independent Review sind adressiert. |
| Eintritt | Vorliegen des Review Reports |
| Austritt | Bestätigung der Schließung durch das Re-Review |
| Kriterien | Jedes Finding trägt einen dokumentierten Status; offene Punkte sind als normative Pending Resolution geführt |
| Nachweise | Correction Report; Supplementary Review Report |

#### RL-03 — Approval Ready

| Feld | Inhalt |
|---|---|
| Beschreibung | Der Plan ist genehmigungsfähig. |
| Eintritt | Austritt aus RL-02 |
| Austritt | Genehmigungsentscheidung getroffen |
| Kriterien | AP-01 bis AP-09 vollständig erfüllt; keine Abbruchbedingung gemäß 10.4 einschlägig |
| Nachweise | Approval Record |

#### RL-04 — Authorized for Sprint Planning

| Feld | Inhalt |
|---|---|
| Beschreibung | Die Sprintplanung darf auf Grundlage des genehmigten Plans beginnen. |
| Eintritt | Dokumentstatus APPROVED; Governance Closing Summary erstellt |
| Austritt | Genehmigte Sprintplanung liegt vor |
| Kriterien | Zusätzlich zu RL-03: dokumentierte Entscheidung zu GR-001 gemäß PR-001.7 |
| Nachweise | Approval Record; Governance Closing Summary; Entscheidung zu GR-001 |

#### RL-05 — Authorized for Implementation

| Feld | Inhalt |
|---|---|
| Beschreibung | Die Umsetzung darf beginnen. |
| Eintritt | Genehmigte Sprintplanung; protokollierte Baseline-Bestätigung gemäß Kapitel 3.8 |
| Austritt | Abschluss der Umsetzungssequenz gemäß Kapitel 6 |
| Kriterien | Vollständige Erfüllung von RL-04; Abschluss der Phase A gemäß Kapitel 7.3 |
| Nachweise | EV-D01; Sprintplanungsdokument; Freigabe gemäß 10.6 |

#### Aktueller Stand

| Readiness Level | Status |
|---|---|
| RL-00 | **Verlassen** seit Kapitel 13 — sämtliche Planungsgegenstände gemäß Kapitel 2.3 sind behandelt |
| RL-01 | **Erreicht** — das Gesamtkonsistenzaudit (W-2) ist in den Revisionen R1 und R2 durchgeführt; 20 Findings sind in Correction Cycle R1 geschlossen, das High-Finding **H-01** durch **WAIVER-AMENDMENT-001** (Entscheidung zu GDR-001). Es bestehen keine offenen Critical- oder High-Findings; AP-01 bis AP-06 und AP-09 sind erfüllt. CC-14 bleibt prozessbedingt offen und wird durch W-3 geschlossen. |
| RL-02 bis RL-05 | Nicht erreicht |

---

### 10.6 Authorization Criteria

#### Sprint Planning

Die Sprintplanung darf beginnen, wenn **sämtliche** folgenden Bedingungen
erfüllt sind:

| # | Bedingung |
|---|---|
| 1 | Der Implementation Plan trägt den Status APPROVED |
| 2 | Approval Record und Governance Closing Summary liegen vor |
| 3 | Sämtliche Findings des Independent Review sind geschlossen oder als normative Pending Resolution mit Frist dokumentiert |
| 4 | Die Closing Criteria von WAIVER-DEV-001 sind durch den Independent Review bestätigt |
| 5 | Zu GR-001 liegt eine dokumentierte Entscheidung vor |
| 6 | Readiness Level RL-04 ist erreicht |

#### Coding

Die Umsetzung von Produktionscode darf beginnen, wenn **zusätzlich** sämtliche
folgenden Bedingungen erfüllt sind:

| # | Bedingung |
|---|---|
| 7 | Eine genehmigte Sprintplanung liegt vor |
| 8 | Die Baseline-Bestätigung gemäß Kapitel 3.8 ist protokolliert (Phase A abgeschlossen) |
| 9 | Readiness Level RL-05 ist erreicht |

#### Ausschlüsse

Die Umsetzung darf **nicht** beginnen, solange eine der folgenden Lagen
besteht:

| # | Ausschlussgrund |
|---|---|
| 1 | Der Plan trägt den Status DRAFT |
| 2 | Der Independent Review ist nicht durchgeführt oder nicht abgeschlossen |
| 3 | Ein Finding der Schweregrade Critical oder High ist offen |
| 4 | Eine Closing Criterion von WAIVER-DEV-001 ist unerfüllt |
| 5 | Die Baseline-Bestätigung liegt nicht protokolliert vor |
| 6 | Zu GR-001 liegt keine dokumentierte Entscheidung vor |
| 7 | Der Plan deckt seinen Planungsscope nicht vollständig ab |
| 8 | Eine Baseline- oder Architekturabweichung ist festgestellt und nicht entschieden |

Ein einzelner Ausschlussgrund genügt. Die Ausschlüsse wirken unabhängig
voneinander.

---

### 10.7 Completion Verification

#### Abschnittsbezogene Prüfung

Die Übersicht führt Kapitel und Anhänge gemeinsam. Die Anhänge sind keine
Kapitel des Plans (Anhang A, Präambel); sie werden hier ausschließlich zur
Vollständigkeit der Prüfung aufgeführt.

| Abschnitt | Gegenstand | Vollständig | Konsistent | Traceability | Befund |
|---|---|---|---|---|---|
| Kapitel 1 | Document Control | Ja | Ja | Ja | Keiner |
| Kapitel 2 | Planning Framework | Ja | Ja | Ja | Keiner |
| Kapitel 3 | Baseline Verification | Ja | Ja | Ja | Bestätigung erfolgt in Phase A; redaktionelle Feststellung zu ADR-011 (3.7) ohne Findings-Charakter |
| Kapitel 4 | Delta Analysis | Ja | Ja | Ja | Vorbehalt gemäß 4.2 Regel 5 |
| Kapitel 5 | Module Work Breakdown | Ja | Ja | Ja | GB-001 ausgewiesen und als GR-001 registriert; Auslegung der Waiver Closing Criteria durch WAIVER-AMENDMENT-001 verbindlich geklärt (5.5.1) |
| Kapitel 6 | Work Package Sequencing | Ja | Ja | Ja | Keiner |
| Kapitel 7 | Implementation Strategy | Ja | Ja | Ja | Keiner |
| Kapitel 8 | Verification Planning | Ja | Ja | Ja | GV-08 abhängig von GR-001 |
| Kapitel 9 | Test Strategy | Ja | Ja | Ja | Bezugsgröße des Regressionsnachweises abhängig von GR-001 (9.6, 9.8) |
| Kapitel 10 | Completion, Approval & Readiness | Ja | Ja | Ja | CC-14 prozessbedingt offen |
| Kapitel 11 | Risk Management | Ja | Ja | Ja | GR-001 PENDING DECISION |
| Kapitel 12 | Migration Strategy | Ja | Ja | Ja | Migrationsumfang abhängig von GR-001 |
| Kapitel 13 | Rollout Strategy | Ja | Ja | Ja | Keiner |
| Anhang A | Pending Governance Resolution GR-001 | Ja | Ja | Ja | GR-001 PENDING DECISION |
| Anhang B | Performance Measurement Methodology | Ja | Ja | Ja | F-004 CLOSED, Bestätigung ausstehend |

#### Findings-Übersicht

Die Übersicht führt sämtliche Findings aus allen abgeschlossenen Prüfungen
dieses Plans. Sie ersetzt keine Prüfartefakte; sie macht deren Stand an einer
Stelle darstellbar (RO-07).

| Prüfartefakt | Findings | Geschlossen | Offen | Offene Punkte |
|---|---|---|---|---|
| Consistency Audit Kapitel 9 | F9-001 bis F9-007 | 6 | 1 | F9-005 — als GR-001 registriert und über PR-001 normativ geführt |
| Independent Review Kapitel 10 | F10-001 ff.; planweite Befunde GP-001 bis GP-005 eröffnet | — | — | siehe planweite Befunde |
| Independent Review Kapitel 11 | kapitelbezogen | alle | 0 | GP-003 geschlossen |
| Independent Review Kapitel 12 | kapitelbezogen | alle | 0 | — |
| Independent Review Kapitel 13 | kapitelbezogen | alle | 0 | GP-001 und GP-002 geschlossen |
| **Planweite Befunde** | GP-001 bis GP-005 | 3 (GP-001, GP-002, GP-003) | 2 | GP-004 — identisch mit GR-001; GP-005 — externe Bestätigung durch W-3 ausstehend |
| Global Consistency Audit (W-2, R1) | 0 Critical, 2 High, 8 Medium, 7 Low, 4 Editorial | 21 | 0 | H-02 und M/L/E in Correction Cycle R1; **H-01** durch WAIVER-AMENDMENT-001 (Entscheidung zu GDR-001) |
| Global Consistency Audit (W-2, R2) | 1 Editorial neu | 0 | 1 | **R2-E-01** — Registerregel 3 deckt die Kennungspräfixe MGR und ROR nicht ab; terminologisch, nicht blockierend |

| Bewertung | Feststellung |
|---|---|
| Findings ohne dokumentierten Status | **0** |
| Offene Critical Findings | **0** |
| Offene High Findings | **0** |
| Offene Editorial Findings | **1** — R2-E-01, nicht blockierend |
| Findings mit offenem Entscheidungsbedarf | **1** — GR-001 (PENDING DECISION, Instanz und Frist gemäß PR-001.7) |
| Prozessbedingt offen | **1** — GP-005 / CC-14: Independent Review (W-3) |

Der verbleibende Entscheidungsbedarf ist ausgewiesen, nicht aufgelöst (PP-04);
er ist durch diesen Plan nicht entscheidbar. Der zuvor daneben geführte
Entscheidungsbedarf GDR-001 ist durch die zuständige Instanz entschieden und
über WAIVER-AMENDMENT-001 umgesetzt.

#### Deliverable-Abdeckung

Die zehn Deliverables der Engineering Specification werden unverändert
übernommen (PO-02). Der Plan erzeugt keines von ihnen; er ordnet jedem den
Planungsinhalt zu, aus dem es entsteht, und den Nachweis, über den es belegt
wird.

| Deliverable | Typ | Zuordnung im Plan | Nachweis |
|---|---|---|---|
| D-001 — WP-001 Platform Hardening | Implementation | MU-01 / RU-01; Kapitel 6.3 (1a), 7.4 | EV-W01; QG-001 |
| D-002 — WP-002 Host Service & Extensibility | Implementation | MU-02 / RU-02; Kapitel 6.3 (1b), 7.4 | EV-W02; QG-002 |
| D-003 — WP-003 Developer Experience | Implementation | MU-03 / RU-03; Kapitel 6.3 (1c), 7.4 | EV-W03; QG-004 |
| D-004 — WP-004 Observability | Implementation | MU-04 / RU-04; Kapitel 6.3 (1d), 7.4 | EV-W04; QG-006 |
| D-005 — WP-005 Reliability | Implementation | MU-05 / RU-05; Kapitel 6.3 (1e), 7.4 | EV-W05; QG-007 |
| D-006 — WP-006 SDK Contract Verification | Verification | MU-06 / RU-06; Kapitel 6.3 (2), 7.4 | EV-W06, EV-I03, EV-I04; QG-003 |
| D-007 — WP-007 Documentation | Documentation | MU-07 / RU-07; Kapitel 6.3 (1f), 7.4 | EV-W07, EV-D04; QG-005 |
| D-008 — Implementation Plan 1.0 | Governance | Dieses Dokument; Workflow W-1 bis W-8 (10.4) | Approval Record; Governance Closing Summary |
| D-009 — Sprint Reports | Governance | Archivierungsort der Nachweisführung (9.7); erzeugt in der Sprint Planning Phase | Kapitel 9.7, Regel 5 |
| D-010 — Milestone Review Report | Governance | Archivierungsort (9.7); Phase D (7.3) | EV-G03; QG-008 |

Alle zehn Deliverables sind zugeordnet. Es entsteht kein neues Deliverable
(Kapitel 5.6).

#### Gesamtprüfung

| Prüfgegenstand | Ergebnis |
|---|---|
| **Vollständigkeit gegenüber der Engineering Specification** | Vollständig — 6 CO, 7 EG, 14 FR, 10 NFR, 29 AC, 8 QG, 7 WP und 10 Deliverables abgebildet; Deliverable-Zuordnung siehe oben |
| **Vollständigkeit gegenüber dem eigenen Planungsscope** | Vollständig seit Kapitel 13 — PS-01 bis PS-06 gemäß der normativen Scope-Definition in Kapitel 2.3 sämtlich behandelt |
| **Konsistenz** | Widerspruchsfrei nach Correction Cycle R1; abweichende Darstellungen sind als Prüfsicht deklariert |
| **Governance** | Konform; sämtliche Constraint-Sätze eingehalten. Der Entscheidungsbedarf zu den Closing Criteria von WAIVER-DEV-001 war als GDR-001 vorgelegt und nicht durch den Plan aufgelöst; er ist durch WAIVER-AMENDMENT-001 entschieden |
| **Traceability** | Lückenlos über CO → EG → FR → DA → MWB → WP → AC → QG → Evidence |
| **Referenzen** | Aufgelöst; keine toten Verweise |
| **Evidence** | 20 Nachweise definiert; 18 einem Quality Gate, 2 einem Governance-Bestätigungspunkt zugeordnet (8.5) |
| **Requirements** | Unverändert; keine Ergänzung |
| **Quality Gates** | Unverändert; Prüfzeitpunkte zugeordnet, einschließlich der geteilten Prüfzeitpunkte von QG-001 und QG-007 |
| **Waiver** | Closing Criteria §9 (1), (2), (4) adressiert; §9 (3) prozessbedingt ausstehend; Bestätigung durch Independent Review ausstehend |
| **Findings** | Sämtliche Findings mit dokumentiertem Status; keine offenen Critical- oder High-Findings; ein Editorial Finding (R2-E-01) und ein offener Entscheidungsbedarf (GR-001) ausgewiesen — siehe Findings-Übersicht |
| **Architecture** | Unverändert; Architecture Freeze unberührt |

---

### 10.8 Completion Conditions

| ID | Bedingung | Soll | Ist | Nachweis | Evidence | Review |
|---|---|---|---|---|---|---|
| CC-01 | Functional Requirements abgebildet | 14 | 14 | Kapitel 4, 5, 6, 9 | EV-D03 | Independent Review |
| CC-02 | Non-Functional Requirements berücksichtigt | 10 | 10 | Kapitel 9.4 | EV-D03 | Independent Review |
| CC-03 | Acceptance Criteria geplant | 29 | 29 | Kapitel 8.4, 8.6 | EV-D03 | Independent Review |
| CC-04 | Quality Gates geplant | 8 | 8 | Kapitel 8.7, 9.4 | EV-D03 | Independent Review |
| CC-05 | Work Packages abgedeckt | 7 | 7 | Kapitel 5.6, 6.8, 7.4 | EV-D03 | Independent Review |
| CC-06 | Deltas mit Modulzuordnung | 15 | 15 | Kapitel 5.6 | EV-D02 | Independent Review |
| CC-07 | Evidence definiert | 20 | 20 | Kapitel 8.5 | EV-D03 | Independent Review |
| CC-08 | Closing Criteria WAIVER-DEV-001 adressiert | 4 | 4 | Kapitel 5.5.1 | EV-D02 | Independent Review |
| CC-09 | Performance-Messmethodik definiert | 1 | 1 | Anhang B | EV-D01, EV-I01 | Independent Review |
| CC-10 | Findings ohne dokumentierten Status | 0 | 0 | Findings-Übersicht in 10.7 (sämtliche Prüfartefakte) | EV-D05 | Independent Review |
| CC-11 | Planungsgegenstand Migration behandelt (PS-04) | 1 | 1 | Kapitel 12 | EV-D03 | Independent Review |
| CC-12 | Planungsgegenstand Rollout behandelt (PS-05) | 1 | 1 | Kapitel 13 | EV-D03 | Independent Review |
| CC-13 | Planungsgegenstand Risiken behandelt (PS-06) | 1 | 1 | Kapitel 11 | EV-D03 | Independent Review |
| CC-14 | Independent Review durchgeführt | 1 | **0** | — | EV-D03 | Independent Review |

#### Bewertung

| Kategorie | Anzahl | Bedingungen |
|---|---|---|
| Erfüllt | 13 | CC-01 bis CC-13 |
| Nicht erfüllt | 1 | CC-14 |

CC-11 bis CC-13 sind mit den Kapiteln 11, 12 und 13 geschlossen. Der Plan deckt
seinen eigenen Planungsscope seither vollständig ab; Abbruchbedingung AB-03 ist
nicht mehr einschlägig.

CC-14 ist prozessbedingt offen und wird durch den Workflow-Schritt W-3
geschlossen. Das vorgelagerte Gesamtkonsistenzaudit (W-2) ist durchgeführt;
sein Ergebnis ist in der Findings-Übersicht in 10.7 geführt.

**Folge:** Der Implementation Plan ist zum Zeitpunkt dieser Fassung **noch
nicht genehmigungsfähig**, weil der Independent Review aussteht. Readiness
Level RL-00 ist verlassen; **RL-01 ist erreicht** (10.5). Das
Gesamtkonsistenzaudit ist durchgeführt und sämtliche Findings sind
abgearbeitet; es bestehen keine offenen Critical- oder High-Findings.

---

### 10.9 Constraints

| ID | Constraint |
|---|---|
| ACN-01 | Keine neue Architektur. Der Architecture Freeze bleibt unberührt. |
| ACN-02 | Keine neuen Requirements — weder funktional noch nicht-funktional. |
| ACN-03 | Keine neuen Acceptance Criteria. |
| ACN-04 | Keine neuen Quality Gates. |
| ACN-05 | Keine neue Governance. Es entstehen keine zusätzlichen Genehmigungsinstanzen, Prozessschritte oder Entscheidungsebenen über die des Development Standard und des Charter hinaus. |
| ACN-06 | Keine Sprintplanung, keine Ressourcenplanung, keine Terminplanung. |
| ACN-07 | Keine Implementierung, keine Tests, kein Deployment, kein Release. |
| ACN-08 | Keine Vorwegnahme einer Genehmigung. Statusaussagen dieses Kapitels sind Feststellungen, keine Entscheidungen. |
| ACN-09 | Keine Absenkung bestehender Bedingungen. Voraussetzungen, Kriterien und Ausschlüsse dürfen nicht zur Herstellung der Genehmigungsfähigkeit gelockert werden. |
| ACN-10 | Keine Auflösung offener Governance-Punkte durch dieses Kapitel. Offene Punkte werden ausgewiesen und mit Frist versehen. |

---

### 10.10 Final Authorization Statement

#### Autorisierung, die durch den genehmigten Implementation Plan entsteht

| # | Autorisierung |
|---|---|
| 1 | Beginn der Sprintplanung auf Grundlage der in Kapitel 6 festgelegten Reihenfolge und der in Kapitel 7 festgelegten Grundsätze — vorbehaltlich der Bedingungen aus 10.6 |
| 2 | Durchführung der Baseline-Bestätigung gemäß Kapitel 3 (Phase A) |
| 3 | Erhebung der Baseline-Messreihe gemäß Anhang B |
| 4 | Nach genehmigter Sprintplanung: Umsetzung ausschließlich der in Kapitel 4 dokumentierten Deltas innerhalb der in Kapitel 5 zugeordneten Module |
| 5 | Führung der in Kapitel 8 definierten Nachweise nach der in Kapitel 9 festgelegten Teststrategie |

#### Autorisierung, die ausdrücklich NICHT entsteht

| # | Nicht autorisiert |
|---|---|
| 1 | Umsetzung von Produktionscode vor Erreichen von RL-05 |
| 2 | Beginn der Sprintplanung vor Erreichen von RL-04 |
| 3 | Änderung der Bootstrap Baseline 1.0 in einer ihrer bestätigten Eigenschaften |
| 4 | Änderung des Architecture Book v2.0 oder eines genehmigten ADR |
| 5 | Erstellung neuer ADRs ohne eigenes Governance-Verfahren |
| 6 | Änderung, Ergänzung oder Auslegung der Engineering Specification 1.0 |
| 7 | Erweiterung des Scope über Charter und Engineering Specification hinaus |
| 8 | Umsetzung von Inhalten des parallelen Artefaktbaums vor Entscheidung zu GR-001 |
| 9 | Abschluss eines Quality Gate vor Abschluss seiner abhängigen Work Packages |
| 10 | Release, Deployment oder Auslieferung |

#### Normative Feststellung

Der Implementation Plan erteilt keine Autorisierung aus sich heraus. Die
Autorisierung entsteht ausschließlich durch die Genehmigungsentscheidung
gemäß Workflow-Schritt W-6 in Verbindung mit W-7 und W-8 und ist auf den in
diesem Abschnitt bezeichneten Umfang begrenzt.

Zum Zeitpunkt dieser Fassung trägt der Plan den Status **DRAFT**. Es besteht
**keine** Implementierungsautorisierung.

---

*Ende Kapitel 10.*

---

## 11. Risk Management

### 11.1 Purpose

#### Zweck

Dieses Kapitel definiert das **Engineering Risk Management Framework** für
Milestone 1.0. Es regelt die Planung des Umgangs mit Risiken während Planung,
Implementierung und Verifikation.

Es ist kein Risikoregister. Es ist der normative Rahmen, innerhalb dessen
Risiken erkannt, bewertet, gemindert, geprüft, geschlossen und archiviert
werden — und in den die aus genehmigten Dokumenten übernommenen Risiken
eingeordnet sind.

#### Abgrenzung

Dieses Kapitel behandelt **nicht**: Incident Management, Betrieb, Monitoring,
Security Operations, Runtime-Verhalten und Produktionssupport. Risiken, die
ausschließlich im Betrieb eines ausgelieferten Systems entstehen, sind kein
Gegenstand dieses Frameworks.

Es führt keine Requirements, Acceptance Criteria, Quality Gates,
Governance-Ebenen, Evidence-Artefakte, Architekturaussagen oder ADRs ein. Es
konkretisiert ausschließlich die genehmigte Engineering Specification.

#### Verhältnis zu anderen Kapiteln und Dokumenten

| Bezug | Verhältnis |
|---|---|
| Kapitel 6 — Sequencing | Die Abhängigkeitsstruktur bestimmt, welche Risiken Folgewirkung auf nachgelagerte Work Packages entfalten. Risiken ändern die Reihenfolge nicht. |
| Kapitel 8 — Verification Planning | Mitigationen werden über die dort definierten Nachweise belegt. Es entstehen keine risikospezifischen Nachweise. |
| Kapitel 9 — Test Strategy | Die Testkategorien sind das Mittel der Mitigationsprüfung, soweit eine Mitigation testseitig belegbar ist. |
| Kapitel 10 — Completion, Approval & Readiness | Offene Risiken wirken über die Completion Conditions und die Autorisierungskriterien. Kein Risiko erzeugt eine eigene Genehmigungsstufe. |
| Kapitel 12 — Migration | Empfängt die Risikoklassen und die Bewertungsregeln dieses Kapitels (11.13). |
| Kapitel 13 — Rollout | Empfängt die Risikoklassen und die Bewertungsregeln dieses Kapitels (11.13). |
| Development Standard v1.1 | Der Lifecycle bestimmt die Prüf- und Schließungszeitpunkte; das Framework legt keine abweichenden fest. |
| Engineering Specification 1.0 | Quelle der Risiken R-001 bis R-005 und ihrer Mitigationen; unverändert übernommen (11.8). |

---

### 11.2 Risk Objectives

| ID | Ziel | Ableitung |
|---|---|---|
| RO-01 | Jedes erkannte Risiko ist dokumentiert, bewertet und einem Owner zugeordnet. | PP-04, SP-01; QG-008 |
| RO-02 | Jedes Risiko besitzt eine Mitigation, die auf einen Planungsinhalt zurückgeführt ist. | PP-01, SP-02; QG-005 |
| RO-03 | Die Wirksamkeit jeder Mitigation ist über einen bestehenden Nachweis belegbar. | VO-03, VO-05; QG-001 bis QG-008 |
| RO-04 | Kein Risiko gefährdet unbemerkt die Unversehrtheit von Baseline oder Architektur. | NFR-001, NFR-002, NFR-006; EG-003; QG-003, QG-006 |
| RO-05 | Kein Risiko führt zu einer Scope-Erweiterung oder zu einer Absenkung genehmigter Bedingungen. | PP-05, PP-06, SP-08, ACN-09 |
| RO-06 | Restrisiken sind ausgewiesen und ausdrücklich angenommen, nicht stillschweigend getragen. | PP-04; EG-006 |
| RO-07 | Die Risikolage ist zu jedem Governance-Prüfpunkt vollständig darstellbar. | VO-07; QG-008; Development Standard v1.1 |
| RO-08 | Die Risikobehandlung erhält die Regressionsfreiheit und die Vertragstreue. | NFR-003, NFR-005; EG-003; QG-003, QG-007 |

Die Ziele sind kumulativ und gelten über sämtliche Phasen gemäß Kapitel 7.3.

---

### 11.3 Risk Principles

| ID | Grundsatz | Normative Bedeutung |
|---|---|---|
| RP-01 | **Prevention** | Risiken werden vorrangig durch Gestaltung des Vorgehens vermieden, nicht durch nachgelagerte Behandlung. Eine Mitigation, die erst nach Eintritt wirkt, ist als solche zu kennzeichnen. |
| RP-02 | **Early Detection** | Jedes Risiko wird dem frühestmöglichen Prüfpunkt zugeordnet, an dem sein Eintritt erkennbar ist. Eine spätere Zuordnung ist zu begründen. |
| RP-03 | **Risk Transparency** | Die Risikolage wird vollständig ausgewiesen. Eine Darstellung, die den Umfang eines Risikos verkürzt, ist unzulässig. |
| RP-04 | **No Hidden Risks** | Ein erkanntes Risiko wird dokumentiert, bevor die betroffene Arbeit fortgesetzt wird. Kenntnis ohne Dokumentation gilt als Verstoß gegen dieses Framework. |
| RP-05 | **Traceability** | Jedes Risiko, jede Mitigation und jeder Nachweis sind auf genehmigte Elemente rückführbar. Nicht rückführbare Risikoaussagen sind zu entfernen oder zu verankern. |
| RP-06 | **Governance First** | Kein Risiko wird durch Absenkung einer Bedingung, Änderung einer Baseline-Eigenschaft oder Umgehung des Genehmigungswegs behandelt. |
| RP-07 | **Residual Risk Documentation** | Verbleibendes Risiko wird benannt, bewertet und ausdrücklich angenommen. Eine Annahme ohne Dokumentation existiert nicht. |
| RP-08 | **Ownership** | Jedes Risiko trägt genau einen Owner. Geteilte Verantwortung ist unzulässig. |
| RP-09 | **Review Before Closure** | Kein Risiko wird ohne Prüfung geschlossen. Das Ausbleiben des Eintritts ist für sich kein Schließungsgrund. |

#### Konfliktregel

Stehen Grundsätze im Einzelfall in Spannung, gilt die Reihenfolge
RP-06 → RP-04 → RP-03 → RP-05 → RP-08 → RP-09 → RP-07 → RP-02 → RP-01.
Governance und Transparenz haben Vorrang vor Vermeidungsökonomie. Die Regel
ist die Fortschreibung der Konfliktregeln aus Kapitel 2.2 und Kapitel 7.2.

---

### 11.4 Risk Classification

Die Klassifikation ist abschließend. Jedes Risiko trägt genau eine Klasse.
Berührt ein Sachverhalt mehrere Klassen, ist die Klasse maßgeblich, die den
Eintrittsmechanismus beschreibt, nicht die Folge.

| ID | Klasse | Gegenstand |
|---|---|---|
| RK-01 | **Strategic** | Gefährdung der Zielerreichung des Milestones gegenüber Charter Objectives |
| RK-02 | **Technical** | Gefährdung der fachlichen Zielzustände der Functional Requirements |
| RK-03 | **Architectural** | Gefährdung der eingefrorenen Architektur oder ihrer Verträge |
| RK-04 | **Governance** | Gefährdung der Governance-Kette, der Autorisierungsgrenze oder der Entscheidungsordnung |
| RK-05 | **Planning** | Gefährdung der Vollständigkeit, Konsistenz oder Rückverfolgbarkeit der Planung |
| RK-06 | **Verification** | Gefährdung der Nachweisführung oder der Aussagekraft eines Nachweises |
| RK-07 | **Quality** | Gefährdung des Bestehens eines Quality Gate |
| RK-08 | **Schedule** | Verzögerungswirkung innerhalb der Phasen- und Abhängigkeitsstruktur. Diese Klasse beschreibt ausschließlich Reihenfolge- und Abhängigkeitswirkungen; sie enthält keine Termine und begründet keine Terminplanung (ST-09). |
| RK-09 | **Dependency** | Gefährdung durch Abhängigkeiten zwischen Work Packages oder gegenüber Vorgängerergebnissen |
| RK-10 | **Migration** | Gefährdung der Überführung vom Baseline- in den Zielzustand |
| RK-11 | **Rollout** | Gefährdung der Einführung des Milestone-Ergebnisses |
| RK-12 | **Performance** | Gefährdung der Performance-Nichtverschlechterung gemäß NFR-004 |
| RK-13 | **Regression** | Gefährdung der Regressionsfreiheit gegenüber der Baseline |
| RK-14 | **Security** | Gefährdung der bestehenden Sicherheitsprüfebene und der sicherheitskritischen Pipeline-Reihenfolge. Diese Klasse begründet keine neuen Sicherheitsanforderungen (STR-01 bis STR-04). |
| RK-15 | **Documentation** | Gefährdung von Vollständigkeit oder Aktualität der Dokumentation |
| RK-16 | **External** | Gefährdung durch Sachverhalte außerhalb des Milestone-Scope und außerhalb der Entscheidungsgewalt der beteiligten Funktionen |

#### Ausgeschlossene Klassen

Runtime-, Betriebs-, Incident- und Supportrisiken sind ausdrücklich keine
Klassen dieses Frameworks. Ein Sachverhalt, der ausschließlich im Betrieb
eines ausgelieferten Systems eintreten kann, ist nicht Gegenstand des
Engineering Risk Management und wird nicht in dieses Framework aufgenommen.

---

### 11.5 Risk Ownership & Decision Authority

**Einordnung.** RC-01 und RC-02 fordern einen Owner je Mitigation und eine
ausdrückliche Annahme von Restrisiken durch die Release Authority. Ohne
benannte Funktionen und Entscheidungsinstanzen sind diese Beschränkungen nicht
prüfbar. Die hier geführten Funktionen sind unverändert aus Kapitel 7.6 und
Kapitel 8.5 übernommen; es entsteht keine neue Entscheidungsebene (ACN-05).

#### Funktionen

| Funktion | Verantwortung im Risikoframework |
|---|---|
| **Governance Architect** | Owner für Risiken der Klassen RK-01, RK-03, RK-04, RK-05, RK-16. Führung des konsolidierten Registers. Feststellung der Risikolage zu jedem Governance-Prüfpunkt. |
| **Release Authority** | Annahme von Restrisiken. Entscheidung über Risiken, deren Behandlung die Autorisierungsgrenze berührt. |
| **Umsetzungsverantwortung des Work Package** | Owner für Risiken der Klassen RK-02, RK-06, RK-07, RK-09, RK-12, RK-13, soweit einem Work Package zugeordnet. Führung der Mitigationsnachweise. |
| **Independent Review** | Prüfung der Risikolage, der Mitigationswirksamkeit und der Schließungsvoraussetzungen. Keine Owner-Funktion. |

Die personelle Besetzung ist nicht Gegenstand dieses Plans (ST-08, VC-09).

#### Entscheidungsinstanzen

| Entscheidung | Instanz |
|---|---|
| Aufnahme eines Risikos in das Register | Owner der zutreffenden Klasse |
| Änderung der Bewertung | Owner, mit Dokumentation der Begründung |
| Anerkennung einer Mitigation als wirksam | Independent Review |
| Schließung eines Risikos | Independent Review auf Vorlage des Owners |
| Annahme eines Restrisikos | Release Authority |
| Behandlung eines Risikos, das eine Baseline- oder Architekturabweichung erfordert | Governance Architect; Auflösung ausschließlich über ADR oder RDR |

#### Schnittstelle zur Eskalation

Wird ein Risiko zu einem Eskalationstatbestand gemäß Kapitel 7.6, gilt
ausschließlich das dort geregelte Verfahren. Dieses Kapitel begründet keinen
abweichenden Eskalationsweg und wiederholt ihn nicht.

---

### 11.6 Risk Lifecycle

Der Lebenszyklus ist verbindlich und wird vollständig durchlaufen. Ein
Überspringen von Stufen ist unzulässig.

| Stufe | Inhalt | Abschlussbedingung der Stufe |
|---|---|---|
| **L-1 Erkennen** | Feststellung eines Sachverhalts, der ein Ziel, einen Nachweis, eine Bedingung oder eine Invariante gefährden kann. Aufnahme in das konsolidierte Register unter Angabe von Quelle und Klasse. | Risiko dokumentiert, Klasse zugeordnet, Owner benannt |
| **L-2 Bewerten** | Bestimmung von Eintrittswahrscheinlichkeit, Auswirkung und Kritikalität gemäß 11.7. | Bewertung dokumentiert und begründet |
| **L-3 Mitigation planen** | Zuordnung einer Mitigation zu einem bestehenden Planungsinhalt und Bestimmung des Nachweises, über den ihre Wirksamkeit belegt wird. | Mitigation und Nachweis zugeordnet |
| **L-4 Wirksamkeit prüfen** | Prüfung, ob der zugeordnete Nachweis die Mitigation tatsächlich belegt. | Prüfergebnis dokumentiert |
| **L-5 Review** | Unabhängige Prüfung von Bewertung, Mitigation und Wirksamkeit. | Reviewurteil dokumentiert |
| **L-6 Schließen** | Feststellung, dass das Risiko nicht mehr eintreten kann oder dass sein verbleibender Anteil ausdrücklich angenommen ist. | Schließungsentscheidung dokumentiert |
| **L-7 Archivieren** | Überführung des vollständigen Risikoverlaufs in die Deliverables der Engineering Specification. | Verlauf archiviert |

#### Zulässige Zustände

| Status | Bedeutung |
|---|---|
| **OPEN** | Erkannt, noch nicht abschließend behandelt |
| **MITIGATED** | Mitigation zugeordnet und als wirksam geprüft; Eintritt weiterhin möglich |
| **ACCEPTED** | Verbleibender Anteil ausdrücklich angenommen (RP-07) |
| **CLOSED** | Geschlossen nach Review (RP-09) |
| **PENDING DECISION** | Behandlung erfordert eine Entscheidung außerhalb der Autorisierungsgrenze dieses Plans |

#### Zustandsregeln

| # | Regel |
|---|---|
| 1 | Der Eintritt in einen Zustand erfolgt ausschließlich über die zugehörige Lifecycle-Stufe. |
| 2 | Der Übergang nach CLOSED setzt L-5 voraus. Zeitablauf, Phasenwechsel oder Nichteintritt begründen keine Schließung. |
| 3 | Der Zustand ACCEPTED setzt eine Entscheidung der Release Authority voraus. |
| 4 | Der Zustand PENDING DECISION verpflichtet zur Angabe der Entscheidungsinstanz und der spätesten notwendigen Entscheidung. |
| 5 | Ein neu während der Umsetzung erkanntes Risiko tritt in L-1 ein und durchläuft den Zyklus vollständig; eine verkürzte Behandlung ist unzulässig. |

---

### 11.7 Risk Assessment

Die Bewertung ist ordinal und begründungspflichtig. Es werden keine
Prozentwerte, Punktzahlen oder Rechenmodelle verwendet.

#### Eintrittswahrscheinlichkeit

| Stufe | Definition |
|---|---|
| **Niedrig** | Der Eintritt setzt eine Verkettung mehrerer für sich unwahrscheinlicher Umstände voraus. |
| **Mittel** | Der Eintritt ist bei ungünstigem, aber plausiblem Verlauf zu erwarten. |
| **Hoch** | Der Eintritt ist ohne wirksame Mitigation zu erwarten. |
| **Eingetreten** | Der Sachverhalt ist bereits eingetreten. Die Wahrscheinlichkeitsstufe entfällt; die Kritikalität ergibt sich allein aus der Auswirkung und entspricht der Zeile der Auswirkungsstufe in der Spalte Hoch. |

#### Auswirkung

| Stufe | Definition |
|---|---|
| **Niedrig** | Auswirkung auf einen einzelnen Planungsinhalt ohne Wirkung auf Nachweise oder Bedingungen. |
| **Mittel** | Auswirkung auf einen Nachweis oder auf den Abschluss eines Work Package. |
| **Hoch** | Auswirkung auf ein Quality Gate, auf eine Phasenbedingung oder auf die Vollständigkeit des Plans. |
| **Kritisch** | Auswirkung auf eine Baseline-Invariante, auf einen genehmigten Vertrag, auf die Architektur oder auf die Governance-Kette. |

#### Kritikalität

Die Kritikalität ergibt sich normativ aus der Kombination beider Größen. Sie
ist keine Berechnung, sondern eine Zuordnungsregel.

| Auswirkung ↓ / Wahrscheinlichkeit → | Niedrig | Mittel | Hoch |
|---|---|---|---|
| **Kritisch** | Hoch | Kritisch | Kritisch |
| **Hoch** | Erhöht | Hoch | Kritisch |
| **Mittel** | Beobachtung | Erhöht | Hoch |
| **Niedrig** | Beobachtung | Beobachtung | Erhöht |

#### Priorisierung

| Kritikalität | Behandlungsregel |
|---|---|
| **Kritisch** | Mitigation ist vor Eintritt in die betroffene Phase wirksam nachzuweisen. Ein Phasenübergang ohne Nachweis ist unzulässig. |
| **Hoch** | Mitigation ist zugeordnet und ihre Wirksamkeit spätestens zum Abschluss des betroffenen Work Package nachzuweisen. |
| **Erhöht** | Mitigation ist zugeordnet; die Wirksamkeitsprüfung erfolgt im Rahmen des regulären Reviews. |
| **Beobachtung** | Keine gesonderte Mitigation erforderlich; das Risiko bleibt registriert und wird zu jedem Prüfpunkt neu bewertet. |

Die Priorisierung ordnet Behandlungstiefe zu, keine Reihenfolge der Umsetzung.
Die Umsetzungsreihenfolge ergibt sich ausschließlich aus Kapitel 6.

#### Restrisiko

| Regel | Festlegung |
|---|---|
| Definition | Der nach wirksamer Mitigation verbleibende Anteil eines Risikos. |
| Ausweispflicht | Das Restrisiko wird mit eigener Bewertung ausgewiesen; die Bewertung des Ausgangsrisikos wird nicht überschrieben. |
| Annahme | Ausschließlich durch die Release Authority und ausschließlich in dokumentierter Form. |
| Unzulässig | Eine Annahme durch Unterlassen, durch Zeitablauf oder durch Nichterwähnung. |

#### Reassessment

Eine erneute Bewertung ist verbindlich bei:

| # | Anlass |
|---|---|
| 1 | Jedem Phasenübergang gemäß Kapitel 7.3 |
| 2 | Jedem Abschluss eines Work Package |
| 3 | Jeder Feststellung, die eine Bewertungsgrundlage verändert |
| 4 | Jeder Entscheidung zu einem Risiko im Zustand PENDING DECISION |
| 5 | Jedem Independent Review |

Das Ergebnis eines Reassessments wird dokumentiert, auch wenn es die
Bewertung bestätigt.

---

### 11.8 Engineering Specification Risk Mapping

Die fünf Risiken der Engineering Specification werden unverändert überführt.
Bewertung, Beschreibung und Mitigation sind aus der Engineering Specification
übernommen; ergänzt sind ausschließlich Klasse, Kritikalität, Zuordnung,
Nachweis, Owner, Status und Completion.

#### R-001 — Scope Creep

| Feld | Inhalt |
|---|---|
| Beschreibung | Ausweitung des Umfangs über den genehmigten Scope hinaus |
| Ursprung | Engineering Specification 1.0, Risikoregister |
| Klasse | RK-01 Strategic |
| Wahrscheinlichkeit / Auswirkung | Mittel / Hoch |
| Kritikalität | **Hoch** |
| Mitigation | NFR-001 (Architecture Freeze), QG-003, QG-008, Definition of Done; Rückverfolgbarkeit aller Erweiterungen auf die Charter Objectives |
| Work Package | Querschnittlich — WP-001 bis WP-007 |
| Quality Gate | QG-003, QG-008 |
| Evidence | EV-D03, EV-G01 |
| Review | Independent Review; Governance-Audit in Phase D |
| Owner | Governance Architect |
| Status | **MITIGATED** |
| Traceability | R-001 → PP-05, SP-08, ACN-09 → QG-003, QG-008 → EV-D03, EV-G01 |
| Completion | Phase D, mit Bestätigung von GV-07 |

#### R-002 — SDK-Kompatibilitätsbruch

| Feld | Inhalt |
|---|---|
| Beschreibung | Bruch bestehender SDK-Verträge gegenüber Konsumenten |
| Ursprung | Engineering Specification 1.0, Risikoregister |
| Klasse | RK-03 Architectural |
| Wahrscheinlichkeit / Auswirkung | Niedrig / Kritisch |
| Kritikalität | **Hoch** |
| Mitigation | NFR-003 (SDK API 1.0.0), FR-013, FR-014, QG-003; Kompatibilitätsnachweis |
| Work Package | WP-006 |
| Quality Gate | QG-003 |
| Evidence | EV-W06, EV-I03, EV-I04 |
| Review | Independent Review; Milestone Review |
| Owner | Umsetzungsverantwortung WP-006 |
| Status | **MITIGATED** |
| Traceability | R-002 → SP-07, DA-013, DA-014 → MWB-013, MWB-014 → WP-006 → AC-013.x, AC-014.x → QG-003 → EV-W06, EV-I03, EV-I04 |
| Completion | Ende Phase C |

#### R-003 — Baseline-Drift

| Feld | Inhalt |
|---|---|
| Beschreibung | Unbemerkte Abweichung vom bestätigten Baseline-Zustand |
| Ursprung | Engineering Specification 1.0, Risikoregister |
| Klasse | RK-03 Architectural |
| Wahrscheinlichkeit / Auswirkung | Niedrig / Hoch |
| Kritikalität | **Erhöht** |
| Mitigation | NFR-002 (Baseline Invariants), QG-006, Baseline Change Control |
| Work Package | Querschnittlich — WP-001 bis WP-007 |
| Quality Gate | QG-006; mittelbar QG-001 über NFR-002 |
| Evidence | EV-D01, EV-I02, EV-G04 |
| Review | Independent Review; Governance-Audit in Phase D |
| Owner | Governance Architect |
| Status | **MITIGATED** |
| Traceability | R-003 → PP-02, SP-03 → BI-01..BI-07, API-01..API-04, BP-01..BP-04, PL-01..PL-05 → QG-006 → EV-D01, EV-I02, EV-G04 |
| Completion | Phase D, mit Bestätigung von GV-04 |

#### R-004 — Governance-Overhead

| Feld | Inhalt |
|---|---|
| Beschreibung | Beeinträchtigung des Fortschritts durch den Umfang des Governance-Verfahrens |
| Ursprung | Engineering Specification 1.0, Risikoregister |
| Klasse | RK-04 Governance |
| Wahrscheinlichkeit / Auswirkung | Mittel / Mittel |
| Kritikalität | **Erhöht** |
| Mitigation | Zweistufiger Governance-Prozess gemäß Charter; Independent Review gemäß Development Standard |
| Work Package | Kein Work Package — Governance-Risiko der Planungs- und Genehmigungsphase |
| Quality Gate | QG-008 |
| Evidence | EV-D03, EV-G01, EV-G03 |
| Review | Independent Review |
| Owner | Governance Architect |
| Status | **MITIGATED** |
| Traceability | R-004 → PP-04, SP-01 → W-1..W-8 → QG-008 → EV-G01, EV-G03 |
| Completion | Phase D |

#### R-005 — Abhängigkeit von der Stabilität des Vorgängermilestones

| Feld | Inhalt |
|---|---|
| Beschreibung | Beeinträchtigung durch Instabilität des als Baseline übernommenen Zustands |
| Ursprung | Engineering Specification 1.0, Risikoregister |
| Klasse | RK-13 Regression |
| Wahrscheinlichkeit / Auswirkung | Niedrig / Mittel |
| Kritikalität | **Beobachtung** |
| Mitigation | NFR-005 (Regressionsbasis); Bootstrap Baseline 1.0 als verifizierter Ausgangspunkt |
| Work Package | Querschnittlich — WP-001 bis WP-007 |
| Quality Gate | QG-007 |
| Evidence | EV-D01, EV-I01 |
| Review | Milestone Review |
| Owner | Umsetzungsverantwortung, übergreifend |
| Status | **MITIGATED**, mit Vorbehalt gemäß GR-001 |
| Traceability | R-005 → DA-015 → MWB-015 → QG-007 → EV-D01, EV-I01 |
| Completion | Ende Phase B; abhängig von der Entscheidung zu GR-001 |

---

### 11.9 Waiver Risk Mapping

**Einordnung.** WAIVER-DEV-001 führt vier Risiken, deren Mitigationen
ausdrücklich dem Implementation Plan zugewiesen sind. Ihre Überführung ist zur
Vollständigkeit gegenüber einem genehmigten Governance-Artefakt erforderlich.
Es erfolgt ausschließlich eine Überführung, keine Neubewertung (RC-11).

| ID | Beschreibung | Klasse | W / A | Kritikalität | Mitigation | Nachweis | Owner | Status |
|---|---|---|---|---|---|---|---|---|
| WR-1 | Der Implementation Plan enthält die zugewiesenen Pflichtabschnitte nicht | RK-05 Planning | Niedrig / Hoch | Erhöht | Closing Criteria des Waivers; Kapitel 4 und Kapitel 5 | EV-D02 | Governance Architect | **MITIGATED** — Bestätigung durch Independent Review ausstehend |
| WR-2 | Der Waiver wird als Präzedenzfall herangezogen | RK-04 Governance | Niedrig / Mittel | Beobachtung | Ausdrückliche Begrenzung der Geltung auf Milestone 1.0; PC-07 | EV-G01 | Governance Architect | **MITIGATED** |
| WR-3 | Governance-Lücke zwischen Engineering Specification und Implementation Plan | RK-04 Governance | Niedrig / Mittel | Beobachtung | Der Implementation Plan ist als Pflicht-Deliverable der Engineering Specification geführt | EV-D03 | Governance Architect | **MITIGATED** |
| WR-4 | Die Konformitätsprüfung gegen den Development Standard schlägt fehl | RK-04 Governance | Niedrig / Niedrig | Beobachtung | Der Waiver dokumentiert die genehmigte Abweichung | EV-G01 | Governance Architect | **MITIGATED** |

#### Nicht überführte Waiver-Risiken

WAIVER-DEV-001 führt zusätzlich drei Risiken für den Fall der
**Nichtgenehmigung** des Waivers. Der Waiver ist genehmigt; diese Risiken
können nicht mehr eintreten und werden nicht in das Register überführt. Die
Feststellung ersetzt die Überführung.

---

### 11.10 Governance Risk Transfer — GR-001

GR-001 wird gemäß der Ankündigung in Anhang A in dieses Kapitel überführt. Die
Überführung ist eine Verortung, keine Entscheidung. Sachverhalt, Bewertung,
Owner, Fristen und Auswirkungen bleiben unverändert; die Pending Resolution
PR-001.1 bis PR-001.9 in Anhang A bleibt maßgeblich.

| Feld | Inhalt |
|---|---|
| Beschreibung | Paralleler Artefaktbaum außerhalb der normativen Baseline |
| Ursprung | Module Work Breakdown, Governance-Befund GB-001 |
| Klasse | RK-04 Governance |
| Wahrscheinlichkeit / Auswirkung | Eingetreten / Hoch |
| Kritikalität | **Hoch** |
| Mitigation | Keine risikomindernde Maßnahme möglich. Der Sachverhalt erfordert eine Entscheidung, keine Mitigation. |
| Work Package | Kein Work Package — wirkt auf die Bezugsgröße der Nachweisführung |
| Quality Gate | QG-007 über die Regressionsbezugsgröße; QG-008 über GV-08 |
| Evidence | EV-D01, EV-I01, EV-D05, EV-G04 |
| Review | Implementation Plan Independent Review |
| Owner | Governance Architect |
| Entscheidungsinstanz | Governance Architect / Release Authority; bei Baseline-Berührung zusätzlich ADR oder RDR |
| Status | **PENDING DECISION** |
| Späteste notwendige Entscheidung | Vor Beginn der Sprintplanung; Rückfallgrenzen Ende Phase B und vor Phase D |
| Traceability | GR-001 → Kapitel 5.5.4, 6.5, 7.6, 7.8, 8.8, 9.6, 9.8 → QG-007, QG-008 → EV-D01, EV-I01, EV-D05, EV-G04 → PR-001 |
| Completion | Mit dokumentierter Entscheidung und anschließender Festlegung der Regressionsbezugsgröße |

#### Verortung

| Vor der Überführung | Nach der Überführung |
|---|---|
| Anhang A als Einzelregister mit eigenem Statuseintrag | Kapitel 11.11 — konsolidiertes Register, alleinige Registerführung (Registerregel 1) |
| Statusbezeichner OPEN | Statusbezeichner **PENDING DECISION** gemäß 11.6; einheitlich in sämtlichen Fundstellen (Registerregel 6) |
| PR-001 als normative Pending Resolution | Unverändert maßgeblich; Anhang A bleibt Fundstelle der Resolution |
| Ankündigung der Überführung in Anhang A | Erfüllt durch diesen Abschnitt |

Anhang A wird durch die Überführung nicht aufgehoben. Er ist ausschließlich die
Fundstelle der Pending Resolution und führt kein Register; die Registerführung
liegt vollständig in Kapitel 11.11.

---

### 11.11 Consolidated Risk Register

**Einordnung.** Das Kapitel führt Risiken aus fünf Quellen zusammen. Ohne
konsolidierte Sicht ist die Vollständigkeitsprüfung in 11.15 nicht führbar und
ein Prüfer müsste die Risikolage aus mehreren Abschnitten rekonstruieren.
Reine Aggregation ohne eigenen Inhalt.

**Dieser Abschnitt führt den verbindlichen Gesamtstand.** Er enthält sämtliche
Einträge des Milestones, einschließlich der in Kapitel 12.9 und Kapitel 13.9
hergeleiteten. Die Herleitung eines Eintrags steht an seiner Fundstelle; seine
Registerführung steht ausschließlich hier.

| ID | Titel | Klasse | Kritikalität | Owner | Status | Quelle | Fundstelle |
|---|---|---|---|---|---|---|---|
| R-001 | Scope Creep | RK-01 | Hoch | Governance Architect | MITIGATED | Engineering Specification | 11.8 |
| R-002 | SDK-Kompatibilitätsbruch | RK-03 | Hoch | Umsetzungsverantwortung WP-006 | MITIGATED | Engineering Specification | 11.8 |
| R-003 | Baseline-Drift | RK-03 | Erhöht | Governance Architect | MITIGATED | Engineering Specification | 11.8 |
| R-004 | Governance-Overhead | RK-04 | Erhöht | Governance Architect | MITIGATED | Engineering Specification | 11.8 |
| R-005 | Abhängigkeit von der Vorgängerstabilität | RK-13 | Beobachtung | Umsetzungsverantwortung, übergreifend | MITIGATED | Engineering Specification | 11.8 |
| WR-1 | Pflichtabschnitte im Plan fehlen | RK-05 | Erhöht | Governance Architect | MITIGATED | WAIVER-DEV-001 | 11.9 |
| WR-2 | Waiver als Präzedenzfall | RK-04 | Beobachtung | Governance Architect | MITIGATED | WAIVER-DEV-001 | 11.9 |
| WR-3 | Governance-Lücke ES zu IP | RK-04 | Beobachtung | Governance Architect | MITIGATED | WAIVER-DEV-001 | 11.9 |
| WR-4 | Konformitätsprüfung Development Standard | RK-04 | Beobachtung | Governance Architect | MITIGATED | WAIVER-DEV-001 | 11.9 |
| GR-001 | Paralleler Artefaktbaum | RK-04 | Hoch | Governance Architect | **PENDING DECISION** | Module Work Breakdown | 11.10; Anhang A |
| MGR-001 | Teilmigrierter Zustand über eine Sequenzgrenze | RK-10 | Erhöht | Umsetzungsverantwortung WP-006 | MITIGATED | Implementation Plan Kapitel 12 | 12.9 |
| MGR-002 | Ausgangszustand nicht wiederherstellbar | RK-10 | Erhöht | Umsetzungsverantwortung des Work Package | MITIGATED | Implementation Plan Kapitel 12 | 12.9 |
| MGR-003 | Überführung gegen unbestätigten Ausgangszustand | RK-10 | Hoch | Governance Architect | MITIGATED | Implementation Plan Kapitel 12 | 12.9 |
| ROR-001 | Freigabe auf unvollständigem Gegenstand | RK-11 | Hoch | Governance Architect | MITIGATED | Implementation Plan Kapitel 13 | 13.9 |
| ROR-002 | Freigabe vor Abschluss phasenübergreifender Gates | RK-11 | Hoch | Governance Architect | MITIGATED | Implementation Plan Kapitel 13 | 13.9 |
| ROR-003 | Verlust der Rücknehmbarkeit | RK-11 | Erhöht | Governance Architect | MITIGATED | Implementation Plan Kapitel 13 | 13.9 |

#### Zusammensetzung

| Quelle | Einträge | Quellenseitige Vollständigkeitsprüfung |
|---|---|---|
| Engineering Specification (R-001..R-005) | 5 | RCC-01 |
| WAIVER-DEV-001 (WR-1..WR-4) | 4 | RCC-02 |
| Governance-Befund GB-001 (GR-001) | 1 | RCC-03 |
| Implementation Plan Kapitel 12 (MGR-001..003) | 3 | MCC-07, MCC-08 |
| Implementation Plan Kapitel 13 (ROR-001..003) | 3 | ROC-06, ROC-07 |
| **Summe** | **16** | RCC-04 bis RCC-08 |

#### Verteilung

| Kritikalität | Anzahl |
|---|---|
| Kritisch | 0 |
| Hoch | 6 |
| Erhöht | 6 |
| Beobachtung | 4 |
| **Summe** | **16** |

| Status | Anzahl |
|---|---|
| OPEN | 0 |
| MITIGATED | 15 |
| ACCEPTED | 0 |
| CLOSED | 0 |
| PENDING DECISION | 1 |
| **Summe** | **16** |

#### Registerregeln

| # | Regel |
|---|---|
| 1 | Das konsolidierte Register ist die alleinige Registerführung des Milestones. Es enthält sämtliche Einträge; ein Eintrag, der hier nicht geführt ist, existiert für den Milestone nicht. |
| 2 | Ein Risiko wird ausschließlich unter seiner ursprünglichen Kennung geführt. Eine Neunummerierung bei Überführung ist unzulässig, da sie die Rückverfolgbarkeit zur Quelle unterbricht. |
| 3 | Ein neu erkanntes Risiko wird unter einer fortlaufenden Kennung aufgenommen und trägt die Quelle „Implementation" oder „Review". Zulässig sind sowohl eine rahmenweite Kennung als auch ein klassenbezogenes Präfix — verwendet werden **MGR** für die Klasse RK-10 und **ROR** für die Klasse RK-11. Die Quellenangabe benennt das erzeugende Kapitel. |
| 4 | Der Registerstand wird zu jedem Reassessment-Anlass gemäß 11.7 fortgeschrieben. |
| 5 | Kapitel 12.9 und 13.9 **leiten** Einträge her und begründen sie; sie führen kein eigenes Register. Jeder dort hergeleitete Eintrag ist in der Tabelle dieses Abschnitts geführt. Abweichende Registerstände in anderen Kapiteln sind ausgeschlossen; im Zweifel gilt dieser Abschnitt. |
| 6 | Ein Zustand wird ausschließlich mit den fünf Bezeichnern aus 11.6 geführt. Insbesondere sind OPEN und PENDING DECISION verschiedene Zustände und keine Synonyme; GR-001 trägt in sämtlichen Fundstellen den Zustand PENDING DECISION. |

---

### 11.12 Risk Traceability

#### Kette

```
Risk
  ↓
Mitigation
  ↓
Work Package
  ↓
Quality Gate
  ↓
Evidence
  ↓
Review
  ↓
Completion
```

**Keine neue Traceability-Ebene.** Sämtliche Knoten der Kette bestehen
bereits: Mitigationen sind Planungsinhalte der Kapitel 4 bis 9, Work Packages
und Quality Gates stammen aus der Engineering Specification, Evidence aus
Kapitel 8.5, Review und Completion aus Kapitel 8 und Kapitel 10. Das Risiko
tritt als Einstiegsknoten hinzu und verändert keine bestehende Zuordnung.

#### Nachweis der Lückenlosigkeit

Die Prüfung bezieht sich auf den Gesamtstand des Registers gemäß 11.11
(16 Einträge), einschließlich der in Kapitel 12.9 und 13.9 hergeleiteten
Einträge.

| Prüfung | Soll | Ist |
|---|---|---|
| Risiken mit zugeordneter Klasse | 16 | 16 |
| Risiken mit Bewertung und Kritikalität | 16 | 16 |
| Risiken mit Owner | 16 | 16 |
| Risiken mit Mitigation oder dokumentierter Begründung ihrer Unmöglichkeit | 16 | 16 |
| Risiken mit zugeordnetem Quality Gate | 16 | 16 |
| Risiken mit zugeordneter Evidence | 16 | 16 |
| Risiken mit Review-Zuordnung | 16 | 16 |
| Risiken mit Completion-Bedingung | 16 | 16 |
| Risiken ohne Rückführung auf eine genehmigte Quelle oder auf einen Planungsinhalt dieses Plans | 0 | 0 |

#### Risiken ohne Work-Package-Bezug

R-004, WR-1 bis WR-4 und GR-001 sind keinem Work Package zugeordnet. Sie
betreffen die Planungs- und Genehmigungsebene, nicht die Umsetzung. MGR-002,
MGR-003 sowie ROR-001 bis ROR-003 sind querschnittlich über WP-001 bis WP-007
geführt und damit keinem einzelnen Work Package zugeordnet. Die Traceability
verläuft für diese Risiken über Quality Gate und Evidence unmittelbar zur
Review- und Completion-Stufe. Die Auslassung beziehungsweise Verallgemeinerung
des Work-Package-Knotens ist keine Lücke, sondern die zutreffende Abbildung des
Wirkungsorts.

---

### 11.13 Interfaces to Migration and Rollout

**Einordnung.** Dieses Kapitel ist die Risikogrundlage der Kapitel 12 und 13.
Ohne definierte Anschlussstellen müssten jene Kapitel eigene Risikoklassen und
Bewertungsregeln bilden, was RC-09 und die Einheit der Registerführung
verletzen würde. Der Abschnitt definiert ausschließlich die Übernahmepflicht,
keine Inhalte der Folgekapitel.

| Empfangendes Kapitel | Zu übernehmen | Nicht zu bilden |
|---|---|---|
| Kapitel 12 — Migration | Klasse RK-10 sowie die Bewertungs-, Lifecycle- und Ownership-Regeln dieses Kapitels; Registerführung gemäß 11.11 | Eigene Risikoklassen, eigene Bewertungsmaßstäbe, eigenes Register, eigene Statuswerte |
| Kapitel 13 — Rollout | Klasse RK-11 sowie die Bewertungs-, Lifecycle- und Ownership-Regeln dieses Kapitels; Registerführung gemäß 11.11 | Eigene Risikoklassen, eigene Bewertungsmaßstäbe, eigenes Register, eigene Statuswerte |

#### Regeln

| # | Regel |
|---|---|
| 1 | Migrations- und Rolloutrisiken werden in das konsolidierte Register aufgenommen und dort geführt. |
| 2 | Klasse RK-10 ist durch Kapitel 12.9 befüllt, Klasse RK-11 durch Kapitel 13.9. Beide Schnittstellen sind erfüllt. |
| 3 | Ein Migrations- oder Rolloutrisiko, das eine Baseline-Invariante oder einen genehmigten Vertrag berührt, wird nicht in Kapitel 12 oder 13 behandelt, sondern nach RP-06 eskaliert. |

---

### 11.14 Risk Constraints

| ID | Beschränkung |
|---|---|
| RC-01 | Kein Risiko wird stillschweigend akzeptiert. Eine Annahme ohne dokumentierte Entscheidung der Release Authority existiert nicht. |
| RC-02 | Keine Mitigation ohne Owner. Geteilte Verantwortung ist unzulässig. |
| RC-03 | Keine Schließung ohne Review. Nichteintritt, Zeitablauf und Phasenwechsel sind keine Schließungsgründe. |
| RC-04 | Keine Umgehung der Governance. Ein Risiko wird niemals durch Absenkung einer Bedingung, Verkürzung eines Nachweises oder Übergehen eines Prüfschritts behandelt. |
| RC-05 | Keine Änderung der Architektur. Ein Risiko, dessen Behandlung eine Architekturänderung erfordert, wird eskaliert und nicht im Rahmen dieses Frameworks aufgelöst. |
| RC-06 | Keine Änderung der Bootstrap Baseline. Für baselineberührende Behandlungen gilt ausschließlich die Change Control. |
| RC-07 | Keine neuen Requirements, Acceptance Criteria oder Quality Gates zur Risikobehandlung. |
| RC-08 | Keine risikospezifischen Evidence-Artefakte. Die Wirksamkeit von Mitigationen wird über bestehende Nachweise belegt. |
| RC-09 | Keine Runtime-, Betriebs- oder Incidentrisiken. Sachverhalte dieser Art werden nicht in das Register aufgenommen. |
| RC-10 | Keine Terminaussagen. Fristen dieses Kapitels sind Phasen- und Prozessbezüge, keine Kalendertermine. |
| RC-11 | Keine Neubewertung übernommener Risiken ohne dokumentierte Begründung. Die Bewertungen der Engineering Specification und des Waivers sind unverändert übernommen. |
| RC-12 | Keine Entscheidung über Risiken im Zustand PENDING DECISION durch dieses Kapitel. |

---

### 11.15 Completion Conditions

| ID | Bedingung | Soll | Ist | Nachweis | Review | Evidence | Owner |
|---|---|---|---|---|---|---|---|
| RCC-01 | Risiken der Engineering Specification überführt | 5 | 5 | 11.8 | Independent Review | EV-D03 | Governance Architect |
| RCC-02 | Risiken des Waivers überführt | 4 | 4 | 11.9 | Independent Review | EV-D02 | Governance Architect |
| RCC-03 | Governance-Risiken überführt | 1 | 1 | 11.10 | Independent Review | EV-D05 | Governance Architect |
| RCC-04 | Risiken mit Klasse, Bewertung und Kritikalität | 16 | 16 | 11.11 | Independent Review | EV-D03 | Governance Architect |
| RCC-05 | Risiken mit Owner | 16 | 16 | 11.11 | Independent Review | EV-D03 | Governance Architect |
| RCC-06 | Risiken mit Mitigation oder begründeter Unmöglichkeit | 16 | 16 | 11.8, 11.9, 11.10, 12.9, 13.9 | Independent Review | EV-D03 | Governance Architect |
| RCC-07 | Risiken mit Nachweiszuordnung | 16 | 16 | 11.12 | Independent Review | EV-D03 | Governance Architect |
| RCC-08 | Risiken mit Completion-Bedingung | 16 | 16 | 11.8, 11.9, 11.10, 12.9, 13.9 | Independent Review | EV-D03 | Governance Architect |
| RCC-09 | Klassifikationsmodell vollständig und abschließend | 16 | 16 | 11.4 | Independent Review | EV-D03 | Governance Architect |
| RCC-10 | Lifecycle mit Zuständen und Übergangsregeln definiert | 7 Stufen, 5 Zustände | 7 / 5 | 11.6 | Independent Review | EV-D03 | Governance Architect |
| RCC-11 | Bewertungsmodell ohne Rechenmodell und ohne erfundene Kennzahlen | 1 | 1 | 11.7 | Independent Review | EV-D03 | Governance Architect |
| RCC-12 | Schnittstellen zu Migration und Rollout definiert | 2 | 2 | 11.13 | Independent Review | EV-D03 | Governance Architect |
| RCC-13 | Risiken im Zustand PENDING DECISION mit Instanz und Frist | 1 | 1 | 11.10; PR-001.7 | Independent Review | EV-D05 | Governance Architect |
| RCC-14 | Neue Requirements, Kriterien, Gates, Evidence oder Governance-Ebenen | 0 | 0 | 11.14 | Independent Review | EV-G01 | Governance Architect |

#### Bewertung

Vierzehn von vierzehn Completion Conditions sind erfüllt. Das Framework ist
vollständig; die Risikolage umfasst 16 Registereinträge, davon einen im Zustand
PENDING DECISION, dessen Behandlung ordnungsgemäß außerhalb dieses Kapitels
verortet ist.

RCC-01 bis RCC-03 prüfen die **quellenseitige** Vollständigkeit der aus
genehmigten Dokumenten übernommenen Risiken (5 + 4 + 1). RCC-04 bis RCC-08
prüfen den **Gesamtstand** des Registers (16). Die quellenseitige Prüfung der
sechs im Plan selbst entstandenen Einträge erfolgt über MCC-07, MCC-08,
ROC-06 und ROC-07; die Zusammensetzung ist in 11.11 ausgewiesen.

---

### 11.16 Final Risk Statement

#### Normative Feststellung

Engineering Risks des Milestone 1.0 gelten als **kontrolliert** — nicht als
eliminiert —, wenn sämtliche folgenden Bedingungen erfüllt sind:

| # | Bedingung |
|---|---|
| 1 | Jedes bekannte Risiko ist im konsolidierten Register geführt, klassifiziert und bewertet. |
| 2 | Jedes Risiko trägt genau einen Owner. |
| 3 | Jedes Risiko besitzt eine Mitigation oder eine dokumentierte Begründung, warum eine Mitigation nicht möglich ist. |
| 4 | Die Wirksamkeit jeder Mitigation ist über einen bestehenden Nachweis belegbar. |
| 5 | Jedes Restrisiko ist ausgewiesen und durch die Release Authority ausdrücklich angenommen. |
| 6 | Jedes Risiko im Zustand PENDING DECISION trägt Entscheidungsinstanz und späteste notwendige Entscheidung. |
| 7 | Kein Risiko ist durch Absenkung einer genehmigten Bedingung behandelt. |
| 8 | Die Risikolage ist zu jedem Governance-Prüfpunkt vollständig darstellbar. |

#### Abgrenzung zur Risikofreiheit

Kontrolliert bedeutet nicht risikofrei. Ein kontrolliertes Risiko kann
eintreten. Das Framework stellt sicher, dass ein Eintritt erkannt, zugeordnet,
bewertet und ordnungsgemäß behandelt wird — nicht, dass er ausgeschlossen ist.

Eine Aussage über Risikofreiheit ist innerhalb dieses Frameworks unzulässig.

#### Feststellung zum Zeitpunkt dieser Fassung

| Gegenstand | Feststellung |
|---|---|
| Bedingungen 1 bis 4, 6 bis 8 | Erfüllt |
| Bedingung 5 | Gegenstandslos — kein Restrisiko zur Annahme vorgelegt |
| Risikolage | 16 Registereinträge: 15 MITIGATED, 1 PENDING DECISION (GR-001). Kein Eintrag im Zustand OPEN. |
| Gesamtbewertung | Die Engineering Risks des Milestone 1.0 gelten als **kontrolliert**, vorbehaltlich der ausstehenden Entscheidung zu GR-001 und der Bestätigung durch den Independent Review. |

---

*Ende Kapitel 11.*

---

## 12. Migration Strategy

### 12.1 Purpose

#### Zweck

Dieses Kapitel definiert das **Engineering Migration Framework** für Milestone
1.0. Es regelt die Planung der Überführung vom bestätigten
Bootstrap-Baseline-Zustand in den durch die Engineering Specification
definierten Zielzustand.

Es beantwortet, **unter welchen Bedingungen und in welcher Ordnung** eine
Überführung erfolgt — nicht, wie sie technisch ausgeführt wird.

#### Abgrenzung

Dieses Kapitel behandelt **nicht**: Implementierung, Coding, Deployment,
Release, Runtime-Verhalten, Betriebsmigration, Datenmigration,
Kundenmigration und Infrastrukturmigration.

Migration bezeichnet in diesem Framework ausschließlich die
**Zustandsüberführung des Engineering-Artefaktbestands** von einem
genehmigten Ausgangszustand in einen spezifizierten Zielzustand.

Es führt keine Requirements, Acceptance Criteria, Quality Gates,
Governance-Ebenen, Evidence-Artefakte oder Architekturaussagen ein.

#### Verhältnis zu anderen Kapiteln und Dokumenten

| Bezug | Verhältnis |
|---|---|
| Kapitel 3 — Baseline Verification | Liefert den bestätigten Ausgangszustand. Ohne protokollierte Bestätigung ist keine Migrationseinheit eintrittsfähig. |
| Kapitel 4 — Delta Analysis | Bestimmt den Umfang der Überführung. Die Migration überführt genau die dort dokumentierten Deltas — keine weiteren. |
| Kapitel 6 — Sequencing | Liefert die verbindliche Reihenfolge. Die Migrationssequenz bildet sie ab und ordnet ihr nichts über. |
| Kapitel 8 — Verification Planning | Liefert die Nachweise, über die Austrittsbedingungen belegt werden. Es entstehen keine migrationsspezifischen Nachweise. |
| Kapitel 10 — Completion, Approval & Readiness | Bestimmt die Autorisierungslage. Migration setzt Readiness Level RL-05 voraus. |
| Kapitel 11 — Risk Management | Liefert Klassifikation, Bewertung, Lifecycle, Ownership und Register. Migrationsrisiken werden dort geführt (12.9). |
| Kapitel 13 — Rollout | Empfängt die Übergabe gemäß 12.14. |
| Bootstrap Baseline 1.0 | Bestimmt den Ausgangszustand und die unverrückbaren Invarianten. |
| Engineering Specification 1.0 | Bestimmt den Zielzustand über Functional Requirements und Acceptance Criteria. |
| Development Standard v1.1 | Bestimmt die Lifecycle-Ordnung; das Framework legt keine abweichende fest. |

---

### 12.2 Migration Objectives

| ID | Ziel | Ableitung |
|---|---|---|
| MO-01 | Die Überführung erfolgt ausschließlich vom bestätigten Baseline-Zustand aus. | Kapitel 3.8; SP-03 |
| MO-02 | Die Überführung umfasst genau die genehmigten Deltas. | Kapitel 4; PP-05, SP-08 |
| MO-03 | Jede Migrationseinheit ist einzeln abschließbar und einzeln nachweisbar. | SP-05; WP-001..WP-007 |
| MO-04 | Kein Überführungsschritt verletzt eine Baseline-Invariante oder einen genehmigten Vertrag. | NFR-001, NFR-002, NFR-003, NFR-006; QG-003, QG-006 |
| MO-05 | Die Regressionsfreiheit bleibt über jeden Überführungsschritt erhalten. | NFR-005; QG-007 |
| MO-06 | Kein Übergang erfolgt vor Vorliegen des zugeordneten Nachweises. | SP-06; VO-01 bis VO-03 |
| MO-07 | Jede Migrationseinheit ist bis zu ihrem Abschluss in den Ausgangszustand rückführbar. | MP-08; Kapitel 12.8 |
| MO-08 | Migrationsrisiken werden im bestehenden Framework geführt, nicht gesondert. | Kapitel 11.13; RK-10 |

---

### 12.3 Migration Principles

| ID | Grundsatz | Normative Bedeutung |
|---|---|---|
| MP-01 | **Baseline Preservation** | Die bestätigten Eigenschaften der Baseline bleiben über jeden Überführungsschritt erhalten. Eine Abweichung ist kein Migrationsschritt, sondern eine Baseline-Änderung. |
| MP-02 | **Incremental Migration** | Die Überführung erfolgt in abgeschlossenen Einheiten. Ein Zustand, in dem mehrere Einheiten unvollständig überführt sind, ist zu vermeiden und, wenn unvermeidbar, zu dokumentieren. |
| MP-03 | **Compatibility** | Bestehende Konsumenten bleiben über jeden Überführungsschritt funktionsfähig. Kompatibilität ist keine Eigenschaft des Endzustands, sondern jedes Zwischenzustands. |
| MP-04 | **No Architecture Change** | Die Überführung bewegt sich innerhalb der eingefrorenen Architektur. Ein Migrationsbedarf, der eine Architekturänderung erfordert, wird eskaliert. |
| MP-05 | **Traceability** | Jede Migrationseinheit ist auf Deltas, Work Package, Acceptance Criteria und Nachweis rückführbar. |
| MP-06 | **Governance First** | Kein Überführungsschritt nimmt eine ausstehende Genehmigung vorweg. |
| MP-07 | **Verification Before Transition** | Der Austritt aus einer Migrationseinheit setzt den Nachweis voraus, nicht die Fertigstellung der Arbeit. |
| MP-08 | **Rollback Preparedness** | Vor Eintritt in eine Migrationseinheit ist bestimmt, wie ihr Ausgangszustand wiederhergestellt wird. Eine Einheit ohne bestimmte Rückführung ist nicht eintrittsfähig. |
| MP-09 | **No Scope Expansion** | Die Überführung erweitert den Umfang nicht. Ein während der Migration erkannter Zusatzbedarf wird dokumentiert, nicht überführt. |
| MP-10 | **Single Source of Truth** | Der Zielzustand ergibt sich ausschließlich aus der Engineering Specification. Migrationsentscheidungen leiten sich nicht aus dem vorgefundenen Artefaktbestand ab. |

#### Konfliktregel

Stehen Grundsätze in Spannung, gilt die Reihenfolge
MP-06 → MP-04 → MP-01 → MP-03 → MP-07 → MP-08 → MP-05 → MP-10 → MP-09 →
MP-02. Governance-, Architektur- und Vertragsschutz haben Vorrang vor
Überführungsökonomie.

---

### 12.4 Migration Scope

#### Gegenstand der Migration

| # | Gegenstand | Grundlage |
|---|---|---|
| 1 | Überführung der in Kapitel 4 dokumentierten Deltas DA-001 bis DA-015 | Delta Analysis |
| 2 | Überführung innerhalb der in Kapitel 5 zugeordneten Module und Artefakte | Module Work Breakdown |
| 3 | Erhaltung sämtlicher in Kapitel 4.7 ausgewiesenen Null-Delta-Bereiche | Erhaltungsbereiche |
| 4 | Nachweisführung je Migrationseinheit über die Nachweise aus Kapitel 8.5 | Verification Planning |

#### Ausdrücklich nicht Gegenstand

| Ausschluss | Begründung |
|---|---|
| Datenmigration | Kein Delta betrifft Datenbestände; die Datenbasis ist Erhaltungsbereich der Messbedingungen (Anhang B.4) |
| Betriebs-, Infrastruktur- und Kundenmigration | Außerhalb des Engineering-Scope; kein Charter Objective und kein Functional Requirement |
| Deployment und Release | Nicht autorisiert (Kapitel 10.10) |
| Runtime-Zustandsüberführung | Kein Gegenstand des Engineering Migration Framework |
| Überführung des in Kapitel 5.5.4 genannten parallelen Artefaktbaums | Nicht zugeordnet; Entscheidung steht aus (GR-001) |
| Architekturüberführung | Architecture Book v2.0 ist FROZEN (MP-04) |

---

### 12.5 Migration Units

#### Bildungsregel

Eine Migrationseinheit entspricht genau einem genehmigten Work Package.

Die Eins-zu-eins-Zuordnung ist bewusst gewählt: Jede feinere Zerlegung würde
eine Planungsentität schaffen, die weder in der Engineering Specification noch
im Module Work Breakdown besteht. Eine gröbere Zerlegung würde die einzelne
Abschließbarkeit nach MO-03 aufheben. Es entstehen **keine neuen Module und
keine neuen Planungsentitäten**.

#### Katalog

| ID | Migrationseinheit | Work Package | Deltas | Kategorie |
|---|---|---|---|---|
| MU-01 | Platform Hardening | WP-001 | DA-001, DA-002 | Provider |
| MU-02 | Host Service & Extensibility | WP-002 | DA-003, DA-004 | Provider |
| MU-03 | Developer Experience | WP-003 | DA-005, DA-006 | Provider |
| MU-04 | Observability | WP-004 | DA-007, DA-008 | Provider |
| MU-05 | Reliability | WP-005 | DA-009, DA-010 | Provider |
| MU-06 | SDK Contract Verification | WP-006 | DA-013, DA-014 | Dependent |
| MU-07 | Documentation | WP-007 | DA-011, DA-012 | Provider |

#### Querschnittliches Delta

DA-015 (Testbasis) ist keinem einzelnen Work Package zugeordnet und bildet
daher keine eigene Migrationseinheit. Es wird in jeder Einheit als
Nachweisbestandteil geführt und über die Regressionsprüfung am Ende der
Provider-Überführung abschließend belegt.

---

### 12.6 Migration Unit States

**Einordnung.** Readiness (12.12) und Completion (12.13) definieren Endpunkte;
ohne definierten Zustandsraum sind die Bedingungen dazwischen nicht eindeutig
prüfbar. Die Zustandslogik folgt dem Muster aus Kapitel 11.6 und führt keine
neue Governance ein (ACN-05).

| Status | Bedeutung | Eintrittsvoraussetzung |
|---|---|---|
| **BASELINE** | Die Einheit befindet sich unverändert im bestätigten Ausgangszustand. | Protokollierte Baseline-Bestätigung |
| **READY** | Sämtliche Readiness-Bedingungen gemäß 12.12 sind erfüllt. | MR-01 bis MR-07 |
| **IN TRANSITION** | Die Überführung ist begonnen und nicht abgeschlossen. | Eintritt gemäß 12.7 |
| **VERIFIED** | Die zugeordneten Nachweise liegen vollständig vor. | Nachweise gemäß 12.11 |
| **MIGRATED** | Die Einheit ist abgeschlossen und ihr Zielzustand ist festgestellt. | Austritt gemäß 12.7 |
| **REVERTED** | Die Einheit wurde in den Ausgangszustand zurückgeführt. | Rückführung gemäß 12.8 |

#### Zustandsregeln

| # | Regel |
|---|---|
| 1 | Der Zustandsübergang erfolgt ausschließlich in der Folge BASELINE → READY → IN TRANSITION → VERIFIED → MIGRATED. |
| 2 | Aus IN TRANSITION und VERIFIED ist der Übergang nach REVERTED zulässig. Aus MIGRATED ist er es nicht; eine Rückführung nach Abschluss ist eine Änderung und unterliegt der Governance. |
| 3 | Der Zustand VERIFIED wird nicht durch Fertigstellung der Arbeit erreicht, sondern durch Vorliegen des Nachweises (MP-07). |
| 4 | Eine Einheit im Zustand IN TRANSITION blockiert keinen anderen Zustandsübergang, sofern keine Abhängigkeit besteht. |
| 5 | Zum Zeitpunkt dieser Fassung befinden sich sämtliche Migrationseinheiten im Zustand BASELINE. |

---

### 12.7 Migration Sequence

Die Sequenz bildet die genehmigte Reihenfolge aus Kapitel 6 und die
Phasenordnung aus Kapitel 7.3 ab. Sie enthält keine Sprintzuordnung und keine
Termine.

#### MS-01 — Baseline-Fixierung

| Feld | Inhalt |
|---|---|
| Gegenstand | Feststellung und Protokollierung des Ausgangszustands |
| Eintrittsbedingung | Readiness Level RL-05 erreicht |
| Austrittsbedingung | Bestätigungsumfang gemäß Kapitel 3.8 vollständig protokolliert; Baseline-Messreihe gemäß Anhang B.2 erhoben |
| Abhängigkeiten | Keine |
| Wirkung | Sämtliche Migrationseinheiten werden eintrittsfähig |
| Nachweis | EV-D01 |

#### MS-02 — Überführung der Provider-Einheiten

| Feld | Inhalt |
|---|---|
| Gegenstand | MU-01, MU-02, MU-03, MU-04, MU-05, MU-07 |
| Eintrittsbedingung | MS-01 abgeschlossen; je Einheit Zustand READY |
| Austrittsbedingung | Sämtliche sechs Einheiten im Zustand MIGRATED; Regressionsnachweis geführt |
| Abhängigkeiten | Untereinander keine blockierenden Abhängigkeiten; inhaltlicher, nicht blockierender Bezug von MU-07 zu MU-02 und MU-04 |
| Wirkung | MU-06 wird eintrittsfähig |
| Nachweis | EV-W01, EV-W02, EV-W03, EV-W04, EV-W05, EV-W07, EV-I01, EV-I02 |

#### MS-03 — Vertragsverifikation

| Feld | Inhalt |
|---|---|
| Gegenstand | MU-06 |
| Eintrittsbedingung | MS-02 vollständig abgeschlossen |
| Austrittsbedingung | MU-06 im Zustand MIGRATED; Additivität und Consumer-Kompatibilität nachgewiesen |
| Abhängigkeiten | Sämtliche Provider-Einheiten |
| Wirkung | Die Überführung ist inhaltlich abgeschlossen |
| Nachweis | EV-W06, EV-I03, EV-I04 |

#### MS-04 — Migrationsfeststellung

| Feld | Inhalt |
|---|---|
| Gegenstand | Feststellung des Zielzustands über alle Einheiten |
| Eintrittsbedingung | MS-03 abgeschlossen |
| Austrittsbedingung | Completion Conditions gemäß 12.13 erfüllt |
| Abhängigkeiten | MS-01 bis MS-03 |
| Wirkung | Übergabe an Kapitel 13 gemäß 12.14 |
| Nachweis | EV-G01, EV-G04 |

#### Sequenzregeln

| # | Regel |
|---|---|
| 1 | Die Reihenfolge MS-01 → MS-02 → MS-03 → MS-04 ist verbindlich. |
| 2 | Innerhalb von MS-02 besteht keine verbindliche Ordnung der sechs Einheiten. |
| 3 | Ein Teilabschluss von MS-02 berechtigt nicht zum Eintritt in MS-03. |
| 4 | Die Sequenz ordnet der Reihenfolge aus Kapitel 6 nichts über und weicht von ihr nicht ab. |

---

### 12.8 Reversibility & Rollback Preparedness

**Einordnung.** Das Prinzip MP-08 (Rollback Preparedness) ist ohne Regelwerk
nicht prüfbar. Der Abschnitt bleibt auf Engineering-Ebene und berührt weder
Deployment noch Betrieb (MC-10).

#### Gegenstand

Reversibilität bezeichnet die Fähigkeit, eine Migrationseinheit vor ihrem
Abschluss in den bestätigten Ausgangszustand zurückzuführen.

Sie ist keine Betriebs- oder Deploymentmaßnahme, sondern eine Bedingung der
Eintrittsfähigkeit.

#### Regeln

| # | Regel |
|---|---|
| 1 | Vor Eintritt einer Einheit in den Zustand IN TRANSITION ist bestimmt, wie ihr Ausgangszustand wiederhergestellt wird. |
| 2 | Die Rückführung stellt den Zustand BASELINE her, nicht einen Zwischenzustand. |
| 3 | Eine Rückführung ist zu dokumentieren und einschließlich ihres Anlasses zu begründen. |
| 4 | Eine zurückgeführte Einheit durchläuft die Readiness-Prüfung erneut vollständig. |
| 5 | Die Rückführung einer Einheit berührt die Zustände anderer Einheiten nicht, sofern keine Abhängigkeit besteht. |
| 6 | Nach Erreichen des Zustands MIGRATED ist die Rückführung keine Migrationshandlung mehr, sondern eine Änderung und unterliegt der Governance. |

#### Anlässe

| Anlass | Wirkung |
|---|---|
| Nachweis nicht führbar | Rückführung oder Verbleib in IN TRANSITION bis zur Klärung |
| Verletzung einer Baseline-Invariante festgestellt | Rückführung verbindlich; zusätzlich Eskalation gemäß Kapitel 7.6 |
| Regressionsbefund | Rückführung verbindlich, sofern die Ursache nicht innerhalb der Einheit behoben werden kann |
| Governance-Entscheidung | Rückführung nach Weisung der Entscheidungsinstanz |

---

### 12.9 Migration Risk Mapping

**Einordnung.** Der Abschnitt erfüllt die Übernahmepflicht aus Kapitel 11.13
für die Klasse RK-10. Es wird ausschließlich das Framework aus Kapitel 11
angewandt; es entsteht keine eigene Klassifikation, keine eigene
Bewertungsregel und **kein eigenes Register**.

#### Übernahme

Migrationsrisiken werden ausschließlich unter der Klasse **RK-10** geführt,
nach den Bewertungsregeln aus Kapitel 11.7 bewertet, nach dem Lifecycle aus
Kapitel 11.6 behandelt und im konsolidierten Register aus Kapitel 11.11
geführt. Bestehende Bewertungen werden nicht verändert.

#### MGR-001 — Teilmigrierter Zustand über eine Sequenzgrenze hinaus

| Feld | Inhalt |
|---|---|
| Beschreibung | Eintritt in MS-03 bei unvollständig abgeschlossener MS-02; die Vertragsverifikation prüft dann einen unvollständigen Gegenstand. |
| Ursprung | Implementation Plan, Kapitel 12 |
| Klasse | RK-10 Migration |
| Wahrscheinlichkeit / Auswirkung | Niedrig / Hoch |
| Kritikalität | **Erhöht** |
| Mitigation | Sequenzregel 3; Austrittsbedingung von MS-02; Eintrittsbedingung von MS-03 |
| Work Package | WP-006 |
| Quality Gate | QG-003 |
| Evidence | EV-W06, EV-I03 |
| Review | Independent Review; Milestone Review |
| Owner | Umsetzungsverantwortung WP-006 |
| Status | **MITIGATED** |
| Completion | Ende MS-03 |

#### MGR-002 — Ausgangszustand einer Einheit nicht wiederherstellbar

| Feld | Inhalt |
|---|---|
| Beschreibung | Eine Einheit tritt in IN TRANSITION ein, ohne dass ihre Rückführung bestimmt ist; eine Rückführung ist im Bedarfsfall nicht mehr möglich. |
| Ursprung | Implementation Plan, Kapitel 12 |
| Klasse | RK-10 Migration |
| Wahrscheinlichkeit / Auswirkung | Niedrig / Hoch |
| Kritikalität | **Erhöht** |
| Mitigation | MP-08; Reversibilitätsregel 1; Readiness-Bedingung MR-06 |
| Work Package | Querschnittlich — WP-001 bis WP-007 |
| Quality Gate | QG-006 |
| Evidence | EV-D01, EV-I02 |
| Review | Independent Review |
| Owner | Umsetzungsverantwortung des Work Package |
| Status | **MITIGATED** |
| Completion | Ende MS-02 |

#### MGR-003 — Überführung gegen einen unbestätigten Ausgangszustand

| Feld | Inhalt |
|---|---|
| Beschreibung | Beginn einer Überführung, bevor die Baseline-Bestätigung protokolliert vorliegt; sämtliche Differenzaussagen wären dann ohne Referenzpunkt. |
| Ursprung | Implementation Plan, Kapitel 12 |
| Klasse | RK-10 Migration |
| Wahrscheinlichkeit / Auswirkung | Niedrig / Kritisch |
| Kritikalität | **Hoch** |
| Mitigation | MO-01; Eintrittsbedingung von MS-02; Readiness-Bedingung MR-01; Kapitel 4.2 Regel 5 |
| Work Package | Querschnittlich — WP-001 bis WP-007 |
| Quality Gate | QG-006, QG-008 |
| Evidence | EV-D01, EV-G04 |
| Review | Independent Review; Governance-Audit |
| Owner | Governance Architect |
| Status | **MITIGATED** |
| Completion | Ende MS-01 |

#### Abgrenzung zu bestehenden Risiken

| Bestehendes Risiko | Abgrenzung |
|---|---|
| R-002 — SDK-Kompatibilitätsbruch | Betrifft den Endzustand der Verträge. MGR-001 betrifft die Vollständigkeit des Prüfgegenstands. Keine Überschneidung. |
| R-003 — Baseline-Drift | Betrifft die unbemerkte Abweichung vom Baseline-Zustand. MGR-003 betrifft die fehlende Bestätigung des Ausgangszustands. Keine Überschneidung. |
| R-005 — Abhängigkeit von der Vorgängerstabilität | Betrifft die Stabilität des übernommenen Zustands. MGR-002 betrifft die Rückführbarkeit während der Überführung. Keine Überschneidung. |

#### Übergabe an die Registerführung

Die drei Einträge sind in das konsolidierte Register in **Kapitel 11.11**
aufgenommen und werden dort geführt. Dieser Abschnitt leitet sie her und
begründet sie; er führt kein eigenes Register (Registerregel 5).

| ID | Klasse | Kritikalität | Owner | Status | Registerführung |
|---|---|---|---|---|---|
| MGR-001 | RK-10 | Erhöht | Umsetzungsverantwortung WP-006 | MITIGATED | Kapitel 11.11 |
| MGR-002 | RK-10 | Erhöht | Umsetzungsverantwortung des Work Package | MITIGATED | Kapitel 11.11 |
| MGR-003 | RK-10 | Hoch | Governance Architect | MITIGATED | Kapitel 11.11 |

| Beitrag dieses Kapitels zum Register | Wert |
|---|---|
| Hergeleitete Einträge | 3 |
| Klasse RK-10 | Befüllt — 3 Einträge |
| Verbindlicher Gesamtstand | Kapitel 11.11 (16 Einträge) |

Die Bewertungen der Einträge R-001 bis R-005, WR-1 bis WR-4 und GR-001 bleiben
unverändert (RC-11).

---

### 12.10 Migration Constraints

| ID | Beschränkung |
|---|---|
| MC-01 | Keine Änderung der Bootstrap Baseline ohne genehmigte Governance-Entscheidung. Für baselineberührende Sachverhalte gilt ausschließlich die Change Control. |
| MC-02 | Keine Architekturänderung. Ein Migrationsbedarf, der eine Architekturänderung erfordert, wird eskaliert und nicht überführt. |
| MC-03 | Keine Umgehung eines Quality Gate. Ein Gate wird nicht vorzeitig geschlossen, um einen Sequenzübergang zu ermöglichen. |
| MC-04 | Keine Umgehung der Risikoregeln aus Kapitel 11. Migrationsrisiken unterliegen unverändert Lifecycle, Bewertung, Ownership und Registerführung dieses Frameworks. |
| MC-05 | Keine Überführung außerhalb der in Kapitel 4 dokumentierten Deltas. |
| MC-06 | Keine neuen Module, Artefakte oder Planungsentitäten. |
| MC-07 | Keine neuen Requirements, Acceptance Criteria oder Quality Gates. |
| MC-08 | Keine migrationsspezifischen Evidence-Artefakte. Nachweise stammen ausschließlich aus Kapitel 8.5. |
| MC-09 | Keine Sprintzuordnung, keine Termine, keine Ressourcenaussagen. |
| MC-10 | Keine Deployment-, Release-, Betriebs- oder Datenmigrationsaussagen. |
| MC-11 | Keine Überführung von Artefakten, deren Zugehörigkeit ungeklärt ist. Solange GR-001 den Status PENDING DECISION trägt, ist der parallele Artefaktbaum nicht überführungsfähig. |
| MC-12 | Keine Absenkung einer Readiness- oder Completion-Bedingung zur Herstellung der Eintrittsfähigkeit. |

---

### 12.11 Migration Traceability

#### Kette

```
Migration
    ↓
Work Package
    ↓
Acceptance Criteria
    ↓
Quality Gate
    ↓
Evidence
    ↓
Review
    ↓
Completion
```

**Keine neue Traceability-Ebene.** Die Migrationseinheit ist deckungsgleich
mit dem Work Package und bildet keinen zusätzlichen Knoten; sie ist die
Überführungssicht auf eine bestehende Entität.

#### Zuordnung

| MU | Work Package | Acceptance Criteria | Quality Gate | Evidence | Completion |
|---|---|---|---|---|---|
| MU-01 | WP-001 | AC-001.1..AC-002.2 | QG-001 | EV-W01 | Ende MS-02 |
| MU-02 | WP-002 | AC-003.1..AC-004.2 | QG-002 | EV-W02 | Ende MS-02 |
| MU-03 | WP-003 | AC-005.1..AC-006.2 | QG-004, QG-006 | EV-W03, EV-I02 | Ende MS-02 |
| MU-04 | WP-004 | AC-007.1..AC-008.2 | QG-006 | EV-W04, EV-I02 | Ende MS-02 |
| MU-05 | WP-005 | AC-009.1..AC-010.2 | QG-007 | EV-W05, EV-I01 | Ende MS-02 |
| MU-06 | WP-006 | AC-013.1..AC-014.2 | QG-003 | EV-W06, EV-I03, EV-I04 | Ende MS-03 |
| MU-07 | WP-007 | AC-011.1..AC-012.2 | QG-005 | EV-W07, EV-D04 | Ende MS-02 |

Sämtliche 29 Acceptance Criteria, alle acht Quality Gates und alle sieben
Work Packages sind über die Migrationseinheiten abgedeckt.

Die Spalten Quality Gate und Evidence führen den **einheitenbezogenen** Anteil.
Die phasenbezogenen Anteile von QG-001 (NFR-004), QG-006 und QG-007 sowie
QG-008 insgesamt werden nicht je Einheit, sondern über die Austrittsbedingungen
der Migrationssequenz geführt: EV-I01 und EV-I02 sind in MS-02 als Nachweis
ausgewiesen (12.7). Die Completion-Angabe „Ende MS-02" ist damit für sämtliche
Einheiten der Provider-Überführung zutreffend.

---

### 12.12 Migration Readiness

Eine Migrationseinheit ist eintrittsfähig, wenn **sämtliche** folgenden
Bedingungen erfüllt sind.

| ID | Bedingung | Nachweis |
|---|---|---|
| MR-01 | Die Baseline-Bestätigung liegt protokolliert vor (MS-01 abgeschlossen). | EV-D01 |
| MR-02 | Die der Einheit zugeordneten Deltas sind vollständig dokumentiert. | Kapitel 4 |
| MR-03 | Die betroffenen Module und Artefakte sind zugeordnet. | Kapitel 5 |
| MR-04 | Die zugeordneten Acceptance Criteria und Quality Gates sind bestimmt. | Kapitel 8.4, 12.11 |
| MR-05 | Die Nachweise für den Austritt sind bestimmt. | Kapitel 8.5 |
| MR-06 | Die Rückführung des Ausgangszustands ist bestimmt. | 12.8 Regel 1 |
| MR-07 | Sämtliche blockierenden Vorgänger der Einheit befinden sich im Zustand MIGRATED. | Kapitel 6.4; 12.7 |

#### Regeln

| # | Regel |
|---|---|
| 1 | Die Readiness-Prüfung erfolgt je Einheit und wird dokumentiert. |
| 2 | Eine teilweise erfüllte Readiness begründet keine Eintrittsfähigkeit. |
| 3 | Readiness ist kein Runtime-Zustand und keine Betriebsbereitschaft, sondern eine Planungsfeststellung. |
| 4 | Eine zurückgeführte Einheit wird vollständig erneut geprüft (12.8 Regel 4). |

---

### 12.13 Migration Completion

| ID | Bedingung | Soll | Ist | Evidence | Review | Owner |
|---|---|---|---|---|---|---|
| MCC-01 | Migrationseinheiten definiert und Work Packages zugeordnet | 7 | 7 | EV-D03 | Independent Review | Governance Architect |
| MCC-02 | Deltas den Einheiten zugeordnet | 15 | 15 | EV-D03 | Independent Review | Governance Architect |
| MCC-03 | Migrationssequenz mit Ein- und Austrittsbedingungen definiert | 4 | 4 | EV-D03 | Independent Review | Governance Architect |
| MCC-04 | Zustandsraum je Einheit definiert | 6 | 6 | EV-D03 | Independent Review | Governance Architect |
| MCC-05 | Readiness-Bedingungen definiert | 7 | 7 | EV-D03 | Independent Review | Governance Architect |
| MCC-06 | Reversibilitätsregeln definiert | 6 | 6 | EV-D03 | Independent Review | Governance Architect |
| MCC-07 | Migrationsrisiken im Register geführt | 3 | 3 | EV-D05 | Independent Review | Governance Architect |
| MCC-08 | Klasse RK-10 befüllt | 1 | 1 | EV-D05 | Independent Review | Governance Architect |
| MCC-09 | Traceability je Einheit lückenlos | 7 | 7 | EV-D03 | Independent Review | Governance Architect |
| MCC-10 | Acceptance Criteria über Einheiten abgedeckt | 29 | 29 | EV-D03 | Independent Review | Governance Architect |
| MCC-11 | Quality Gates über Einheiten abgedeckt | 8 | 8 | EV-D03 | Independent Review | Governance Architect |
| MCC-12 | Schnittstelle zu Kapitel 13 definiert | 1 | 1 | EV-D03 | Independent Review | Governance Architect |
| MCC-13 | Neue Requirements, Kriterien, Gates, Evidence, Module oder Governance-Ebenen | 0 | 0 | EV-G01 | Independent Review | Governance Architect |
| MCC-14 | Bestehende Risikobewertungen unverändert — geprüft gegen die 10 vor Kapitel 12 bestehenden Einträge | 10 | 10 | EV-D05 | Independent Review | Governance Architect |

Vierzehn von vierzehn Bedingungen erfüllt. Die Migrationsplanung ist
vollständig.

---

### 12.14 Interfaces to Rollout

#### Übergabe

| Gegenstand der Übergabe | Inhalt |
|---|---|
| Migrationsergebnis | Zustand MIGRATED sämtlicher Einheiten nach Abschluss von MS-03 |
| Nachweislage | Vollständigkeit der Nachweise gemäß 12.11 |
| Risikolage | Stand der Klasse RK-10 im konsolidierten Register |
| Offene Vorbehalte | GR-001 im Zustand PENDING DECISION, soweit die Regressionsbezugsgröße betroffen ist |

#### Regeln

| # | Regel |
|---|---|
| 1 | Kapitel 13 setzt auf dem Zustand MIGRATED auf. Ein Rollout auf Grundlage eines Zwischenzustands ist ausgeschlossen. |
| 2 | Kapitel 13 bildet keine eigenen Migrationseinheiten und keine eigene Migrationssequenz. |
| 3 | Rolloutrisiken werden unter Klasse RK-11 geführt; eine Umwidmung von RK-10-Einträgen ist unzulässig. |
| 4 | Dieses Kapitel nimmt keine Rollout-Regel vorweg. Die Übergabe beschreibt ausschließlich, was Kapitel 13 vorfindet. |

---

### 12.15 Final Migration Statement

#### Normative Feststellung

Die Migration des Milestone 1.0 gilt als **vollständig geplant** — nicht als
durchgeführt —, wenn sämtliche folgenden Bedingungen erfüllt sind:

| # | Bedingung |
|---|---|
| 1 | Jede Migrationseinheit ist bestimmt und einem genehmigten Work Package zugeordnet. |
| 2 | Jedes genehmigte Delta ist genau einer Einheit oder ausdrücklich der querschnittlichen Führung zugeordnet. |
| 3 | Die Reihenfolge der Überführung ist mit Ein- und Austrittsbedingungen bestimmt und weicht von der genehmigten Sequenz nicht ab. |
| 4 | Der Zustandsraum jeder Einheit ist definiert und die Übergänge sind geregelt. |
| 5 | Für jede Einheit ist die Rückführung ihres Ausgangszustands bestimmt. |
| 6 | Für jede Einheit sind Acceptance Criteria, Quality Gate und Nachweis zugeordnet. |
| 7 | Migrationsrisiken sind im bestehenden Framework geführt. |
| 8 | Die Übergabe an den Rollout ist bestimmt. |

#### Abgrenzung

Vollständig geplant bedeutet nicht durchgeführt. Dieses Kapitel erzeugt keine
Migrationshandlung und keine Autorisierung dazu. Die Autorisierung ergibt sich
ausschließlich aus Kapitel 10.6 und setzt Readiness Level RL-05 voraus.

#### Feststellung zum Zeitpunkt dieser Fassung

| Gegenstand | Feststellung |
|---|---|
| Bedingungen 1 bis 8 | Erfüllt |
| Zustand sämtlicher Migrationseinheiten | BASELINE |
| Migrationsrisiken | Drei Einträge, sämtlich MITIGATED |
| Gesamtbewertung | Die Migration des Milestone 1.0 ist **vollständig geplant**. Eine Durchführung ist nicht autorisiert. |

---

*Ende Kapitel 12.*

---

## 13. Rollout Strategy

### 13.1 Purpose

#### Zweck

Dieses Kapitel definiert das **Engineering Rollout Framework** für Milestone
1.0. Es bestimmt, unter welchen Voraussetzungen, in welcher Reihenfolge und
mit welchen Freigabebedingungen das Ergebnis der Migration für die
nachgelagerte Sprint- und Implementierungsphase freigegeben werden darf.

#### Begriffsbestimmung

**Rollout** bezeichnet in diesem Framework ausschließlich die **planerische
Freigabe eines festgestellten Migrationsergebnisses** zur weiteren
Verwendung innerhalb des genehmigten Governance-Prozesses.

Der Begriff bezeichnet in diesem Kapitel **nicht** die Verteilung, Auslieferung
oder Inbetriebnahme von Software. Jede Lesart, die Rollout als
Verteilungsvorgang versteht, ist mit diesem Kapitel unvereinbar.

Diese Begriffsbestimmung ist normativ und gilt für sämtliche Verweise auf
Kapitel 13 innerhalb des Plans.

#### Abgrenzung

Dieses Kapitel behandelt **nicht**: Deployment, Release Management, CI/CD,
Infrastruktur, Produktionsbetrieb, Runtime-Verhalten, Kunden-Rollout,
Versionierung und Softwareverteilung.

Es führt keine Requirements, Acceptance Criteria, Quality Gates,
Governance-Ebenen, Evidence-Artefakte oder Architekturaussagen ein.

#### Verhältnis zu anderen Kapiteln und Dokumenten

| Bezug | Verhältnis |
|---|---|
| Kapitel 6 — Sequencing | Bestimmt die Abhängigkeitsstruktur, aus der die Vollständigkeit des Freigabegegenstands folgt. |
| Kapitel 8 — Verification Planning | Liefert die Nachweise, über die Freigabebedingungen belegt werden. Es entstehen keine rolloutspezifischen Nachweise. |
| Kapitel 10 — Completion, Approval & Readiness | Empfängt die Übergabe gemäß 13.14. Die Freigabeentscheidung selbst wird dort getroffen, nicht hier. |
| Kapitel 11 — Risk Management | Liefert Klassifikation, Bewertung, Lifecycle, Ownership und Registerführung. Rolloutrisiken werden dort geführt (13.9). |
| Kapitel 12 — Migration Strategy | Liefert den Freigabegegenstand. Rollout setzt auf dem Zustand MIGRATED sämtlicher Migrationseinheiten auf. |
| Engineering Specification 1.0 | Bestimmt Acceptance Criteria und Quality Gates, deren Abschluss Freigabevoraussetzung ist. |
| Development Standard v1.1 | Bestimmt die Lifecycle-Ordnung; das Framework legt keine abweichende fest. |

---

### 13.2 Rollout Objectives

| ID | Ziel | Ableitung |
|---|---|---|
| ROO-01 | Die Freigabe erfolgt ausschließlich auf einem vollständig festgestellten Migrationsergebnis. | Kapitel 12.15; MO-03 |
| ROO-02 | Kein Teilergebnis wird freigegeben. | RPR-02; Kapitel 6.5 |
| ROO-03 | Sämtliche Quality Gates sind vor der Freigabe abgeschlossen. | QG-001 bis QG-008; Kapitel 8.7 |
| ROO-04 | Sämtliche Acceptance Criteria tragen den Status VERIFIED. | Kapitel 8.6; VO-02 |
| ROO-05 | Sämtliche Einträge des konsolidierten Registers tragen zum Freigabezeitpunkt den Zustand CLOSED oder ACCEPTED. | Kapitel 11.6, 11.11; RO-06, RP-09 |
| ROO-06 | Die Rückverfolgbarkeit bleibt über die Freigabe hinweg erhalten. | PP-01, SP-02; QG-005 |
| ROO-07 | Die Freigabe ist bis zu ihrer Wirksamkeit rücknehmbar. | RPR-08; Kapitel 13.8 |
| ROO-08 | Die Freigabe erweitert weder Scope noch Autorisierung. | PP-05; Kapitel 10.10 |

---

### 13.3 Rollout Principles

| ID | Grundsatz | Normative Bedeutung |
|---|---|---|
| RPR-01 | **Approval Before Rollout** | Die Freigabe folgt der Genehmigungsentscheidung, sie ersetzt oder nimmt sie nicht vorweg. |
| RPR-02 | **No Partial Rollout** | Der Freigabegegenstand ist das Gesamtergebnis. Eine Freigabe einzelner Einheiten ist ausgeschlossen. |
| RPR-03 | **Governance First** | Kein Freigabeschritt nimmt eine ausstehende Entscheidung vorweg oder umgeht einen Prüfschritt. |
| RPR-04 | **Evidence First** | Freigabereife wird durch Nachweise belegt, nicht durch Feststellung der Beteiligten. |
| RPR-05 | **Migration Completion Required** | Ohne den Zustand MIGRATED sämtlicher Migrationseinheiten besteht kein Freigabegegenstand. |
| RPR-06 | **Risk Closure Required** | Ein Registereintrag, der nicht den Zustand CLOSED oder ACCEPTED trägt, schließt die Freigabe aus. Das gilt auch für den Zustand MITIGATED: eine wirksame Mitigation ist nach RP-09 kein Schließungsgrund. |
| RPR-07 | **Traceability Preservation** | Die Freigabe verändert keine bestehende Zuordnung und erzeugt keinen neuen Knoten in der Kette. |
| RPR-08 | **Rollback Readiness** | Vor der Freigabe ist bestimmt, wie sie zurückgenommen wird. |
| RPR-09 | **No Architecture Change** | Die Freigabe berührt die eingefrorene Architektur nicht. |
| RPR-10 | **No Scope Expansion** | Die Freigabe erweitert den Umfang des Milestones nicht. |

#### Konfliktregel

Stehen Grundsätze in Spannung, gilt die Reihenfolge
RPR-03 → RPR-09 → RPR-01 → RPR-05 → RPR-06 → RPR-04 → RPR-02 → RPR-08 →
RPR-07 → RPR-10. Governance- und Architekturschutz haben Vorrang vor
Freigabeökonomie; die Vollständigkeit des Gegenstands geht der
Nachweisführung voran, weil ein unvollständiger Gegenstand nicht
nachweisfähig ist.

---

### 13.4 Rollout Scope

#### Gegenstand der Freigabe

| # | Gegenstand | Grundlage |
|---|---|---|
| 1 | Das festgestellte Migrationsergebnis sämtlicher Migrationseinheiten | Kapitel 12.15 |
| 2 | Die Nachweislage zu sämtlichen Acceptance Criteria und Quality Gates | Kapitel 8.6, 8.7 |
| 3 | Der Stand des konsolidierten Risikoregisters | Kapitel 11.11, fortgeschrieben in 12.9 und 13.9 |
| 4 | Die Feststellung der Governance-Konformität | Kapitel 8.8 |

#### Ausdrücklich nicht Gegenstand

| # | Ausschluss | Begründung |
|---|---|---|
| 1 | Deployment und Softwareverteilung | Nicht autorisiert (Kapitel 10.10); außerhalb der Begriffsbestimmung |
| 2 | Release Management und Versionierung | Kein Charter Objective, kein Functional Requirement; Zielversionen sind ausdrücklich einem späteren Verfahren zugewiesen |
| 3 | CI/CD und Werkzeugketten | Kein Planungsgegenstand gemäß Kapitel 2.3 |
| 4 | Infrastruktur und Referenzsystembeschaffung | Ressourcenplanung; ausgeschlossen durch ST-08 |
| 5 | Produktionsbetrieb und Runtime-Verhalten | Ausgeschlossen durch RC-09 und die Abgrenzung in Kapitel 11.1 |
| 6 | Kunden-Rollout und Auslieferung an Dritte | Außerhalb des Engineering-Scope |
| 7 | Freigabe des in Kapitel 5.5.4 genannten parallelen Artefaktbaums | Nicht überführungsfähig, solange GR-001 den Status PENDING DECISION trägt (MC-11) |

---

### 13.5 Rollout Units

#### Bildungsregel

Eine Rollouteinheit entspricht genau einer Migrationseinheit und damit genau
einem Work Package. Es entstehen **keine neuen Einheiten und keine neue
Struktur**.

#### Normative Klarstellung zum Verhältnis zu RPR-02

Rollouteinheiten sind **Zuordnungs- und Nachweiseinheiten**, keine
Freigabeeinheiten. Sie ordnen die Nachweislage und die Rückverfolgbarkeit
gegliedert zu; sie begründen keine einzeln erteilbare Freigabe.

Die Freigabe erfolgt ausschließlich gesamthaft über sämtliche Einheiten
(RPR-02, ROO-02). Der Zustand einer einzelnen Einheit ist damit eine
Feststellung über ihren Nachweisstand, keine Teilautorisierung.

#### Katalog

| ID | Rollouteinheit | Migration Unit | Work Package |
|---|---|---|---|
| RU-01 | Platform Hardening | MU-01 | WP-001 |
| RU-02 | Host Service & Extensibility | MU-02 | WP-002 |
| RU-03 | Developer Experience | MU-03 | WP-003 |
| RU-04 | Observability | MU-04 | WP-004 |
| RU-05 | Reliability | MU-05 | WP-005 |
| RU-06 | SDK Contract Verification | MU-06 | WP-006 |
| RU-07 | Documentation | MU-07 | WP-007 |

---

### 13.6 Rollout States

Das Zustandsmodell beschreibt den Nachweis- und Freigabestand einer
Rollouteinheit. Es ist **kein Deploymentmodell** und enthält **keine
Runtimezustände**. Die Bezeichner sind gegenüber dem Zustandsraum der
Migrationseinheiten (Kapitel 12.6) disjunkt.

| Status | Bedeutung | Eintrittsvoraussetzung |
|---|---|---|
| **PENDING** | Die zugehörige Migrationseinheit hat den Zustand MIGRATED nicht erreicht. | Ausgangszustand |
| **ELIGIBLE** | Die Migrationseinheit ist abgeschlossen; die Nachweislage ist noch nicht vollständig geprüft. | Zustand MIGRATED der Migrationseinheit |
| **READY FOR AUTHORIZATION** | Sämtliche Readiness-Bedingungen gemäß 13.12 sind erfüllt. | RR-01 bis RR-08 |
| **AUTHORIZED** | Die Freigabeentscheidung gemäß Kapitel 10 ist getroffen. | Entscheidung außerhalb dieses Kapitels |
| **WITHDRAWN** | Die Freigabe wurde vor ihrer Wirksamkeit zurückgenommen. | Rücknahme gemäß 13.8 |

#### Zustandsregeln

| # | Regel |
|---|---|
| 1 | Der Übergang erfolgt ausschließlich in der Folge PENDING → ELIGIBLE → READY FOR AUTHORIZATION → AUTHORIZED. |
| 2 | Der Zustand AUTHORIZED wird nicht durch dieses Kapitel herbeigeführt. Er tritt ausschließlich durch die Entscheidung gemäß Kapitel 10.6 ein. |
| 3 | Der Übergang nach WITHDRAWN ist aus READY FOR AUTHORIZATION und AUTHORIZED zulässig. |
| 4 | Eine zurückgenommene Einheit tritt nach PENDING zurück und durchläuft die Prüfung vollständig erneut. |
| 5 | Der Zustand einer einzelnen Einheit begründet keine Teilfreigabe (13.5). |
| 6 | Zum Zeitpunkt dieser Fassung befinden sich sämtliche Rollouteinheiten im Zustand PENDING. |

---

### 13.7 Rollout Sequence

Die Sequenz enthält keine Termine und keine Sprintzuordnung.

#### RS-01 — Feststellung der Migrationsvollständigkeit

| Feld | Inhalt |
|---|---|
| Gegenstand | Feststellung, dass sämtliche Migrationseinheiten den Zustand MIGRATED tragen |
| Eintrittsbedingung | MS-04 abgeschlossen |
| Austrittsbedingung | Sämtliche Rollouteinheiten im Zustand ELIGIBLE |
| Abhängigkeiten | Kapitel 12.7 vollständig |
| Nachweis | EV-G04 |

#### RS-02 — Nachweis- und Gate-Verifikation

| Feld | Inhalt |
|---|---|
| Gegenstand | Prüfung der Vollständigkeit sämtlicher Nachweise und des Abschlusses sämtlicher Quality Gates |
| Eintrittsbedingung | RS-01 abgeschlossen |
| Austrittsbedingung | Acceptance Criteria sämtlich im Status VERIFIED; QG-001 bis QG-008 abgeschlossen |
| Abhängigkeiten | Kapitel 8.6, 8.7 |
| Nachweis | EV-W01 bis EV-W07, EV-I01 bis EV-I04, EV-D04 |

#### RS-03 — Risikoabschluss

| Feld | Inhalt |
|---|---|
| Gegenstand | Feststellung, dass sämtliche Einträge des konsolidierten Registers abschließend behandelt sind (RPR-06) |
| Eintrittsbedingung | RS-02 abgeschlossen |
| Austrittsbedingung | Sämtliche 16 Registereinträge im Zustand CLOSED oder ACCEPTED; kein Eintrag mehr in OPEN, MITIGATED oder PENDING DECISION |
| Abhängigkeiten | Kapitel 11.6, 11.11 |
| Nachweis | EV-D05 |

#### RS-04 — Freigabefeststellung

| Feld | Inhalt |
|---|---|
| Gegenstand | Feststellung der Freigabereife und Übergabe an Kapitel 10 |
| Eintrittsbedingung | RS-03 abgeschlossen |
| Austrittsbedingung | Sämtliche Rollouteinheiten im Zustand READY FOR AUTHORIZATION; Completion Conditions gemäß 13.13 erfüllt |
| Abhängigkeiten | RS-01 bis RS-03 |
| Nachweis | EV-D03, EV-G01, EV-G02 |

#### Sequenzregeln

| # | Regel |
|---|---|
| 1 | Die Reihenfolge RS-01 → RS-02 → RS-03 → RS-04 ist verbindlich. |
| 2 | Ein Teilabschluss eines Schrittes berechtigt nicht zum Eintritt in den folgenden. |
| 3 | Die Sequenz endet mit der Feststellung der Freigabereife. Die Freigabeentscheidung selbst ist nicht Bestandteil dieser Sequenz. |

---

### 13.8 Rollback Readiness

#### Gegenstand

Rollback bezeichnet in diesem Kapitel ausschließlich die **Rücknahme einer
Freigabefeststellung** vor deren Wirksamkeit. Er umfasst weder Infrastruktur
noch Runtime noch Produktionszustände.

#### Regeln

| # | Regel |
|---|---|
| 1 | Vor Eintritt einer Einheit in den Zustand READY FOR AUTHORIZATION ist bestimmt, wie die Feststellung zurückgenommen wird. |
| 2 | Die Rücknahme versetzt die Einheit in den Zustand PENDING; ein Zwischenzustand wird nicht hergestellt. |
| 3 | Die Rücknahme ist einschließlich ihres Anlasses zu dokumentieren. |
| 4 | Eine zurückgenommene Einheit durchläuft die Readiness-Prüfung vollständig erneut. |
| 5 | Da keine Teilfreigabe besteht, wirkt die Rücknahme einer Einheit auf die Freigabereife des Gesamtergebnisses. |
| 6 | Nach Wirksamwerden der Autorisierung ist eine Rücknahme keine Rollouthandlung mehr, sondern eine Governance-Entscheidung gemäß Kapitel 10.4. |

#### Anlässe

| Anlass | Wirkung |
|---|---|
| Nachträglich festgestellte Unvollständigkeit eines Nachweises | Rücknahme verbindlich |
| Nachträglich erkannter Registereintrag, der nicht CLOSED oder ACCEPTED trägt | Rücknahme verbindlich (RPR-06) |
| Festgestellte Baseline- oder Architekturabweichung | Rücknahme verbindlich; zusätzlich Eskalation gemäß Kapitel 7.6 |
| Rückführung einer Migrationseinheit gemäß Kapitel 12.8 | Rücknahme zwingend, da der Freigabegegenstand entfällt |

---

### 13.9 Rollout Risk Mapping

#### Übernahme

Rolloutrisiken werden ausschließlich unter der Klasse **RK-11** geführt, nach
den Regeln aus Kapitel 11.6 und 11.7 behandelt und im konsolidierten Register
aus Kapitel 11.11 geführt. Es entsteht keine neue Klassifikation. Bestehende
Bewertungen bleiben unverändert.

Neu aufgenommen werden ausschließlich Risiken, die **ausschließlich** den
Rollout betreffen.

#### ROR-001 — Freigabe auf unvollständigem Gegenstand

| Feld | Inhalt |
|---|---|
| Beschreibung | Feststellung der Freigabereife, obwohl nicht sämtliche Migrationseinheiten den Zustand MIGRATED tragen; der Freigabegegenstand wäre unvollständig. |
| Ursprung | Implementation Plan, Kapitel 13 |
| Klasse | RK-11 Rollout |
| Wahrscheinlichkeit / Auswirkung | Niedrig / Kritisch |
| Kritikalität | **Hoch** |
| Mitigation | RPR-02, RPR-05; Austrittsbedingung von RS-01; Zustandsregel 5 |
| Work Package | Querschnittlich — WP-001 bis WP-007 |
| Quality Gate | QG-008 |
| Evidence | EV-G01, EV-G04 |
| Review | Independent Review |
| Owner | Governance Architect |
| Status | **MITIGATED** |
| Completion | Ende RS-01 |

#### ROR-002 — Freigabe vor Abschluss der phasenübergreifenden Quality Gates

| Feld | Inhalt |
|---|---|
| Beschreibung | Feststellung der Freigabereife, obwohl QG-001, QG-006, QG-007 oder QG-008 nicht abgeschlossen sind; diese Gates sind nicht innerhalb eines einzelnen Work Package abschließbar (Kapitel 7.5, Feststellung) und können bei einheitenbezogener Betrachtung übersehen werden. Bei QG-001 ist die Gefahr besonders ausgeprägt, weil das Gate über RU-01 einer einzelnen Einheit zugeordnet erscheint, sein auf NFR-004 bezogener Anteil aber erst am Ende von Phase B belegbar ist (Anhang B.12). |
| Ursprung | Implementation Plan, Kapitel 13 |
| Klasse | RK-11 Rollout |
| Wahrscheinlichkeit / Auswirkung | Mittel / Hoch |
| Kritikalität | **Hoch** |
| Mitigation | RPR-04; Austrittsbedingung von RS-02; Readiness-Bedingung RR-04; Kapitel 8.7 |
| Work Package | Querschnittlich — WP-001 bis WP-007 |
| Quality Gate | QG-001, QG-006, QG-007, QG-008 |
| Evidence | EV-I01, EV-I02, EV-G01 |
| Review | Independent Review; Milestone Review |
| Owner | Governance Architect |
| Status | **MITIGATED** |
| Completion | Ende RS-02 |

#### ROR-003 — Verlust der Rücknehmbarkeit vor Wirksamkeit

| Feld | Inhalt |
|---|---|
| Beschreibung | Eintritt in den Zustand READY FOR AUTHORIZATION ohne bestimmte Rücknahme; eine nachträglich erforderliche Rücknahme wäre nicht geordnet durchführbar. |
| Ursprung | Implementation Plan, Kapitel 13 |
| Klasse | RK-11 Rollout |
| Wahrscheinlichkeit / Auswirkung | Niedrig / Hoch |
| Kritikalität | **Erhöht** |
| Mitigation | RPR-08; Rollback-Regel 1; Readiness-Bedingung RR-07 |
| Work Package | Querschnittlich — WP-001 bis WP-007 |
| Quality Gate | QG-008 |
| Evidence | EV-D05, EV-G01 |
| Review | Independent Review |
| Owner | Governance Architect |
| Status | **MITIGATED** |
| Completion | Ende RS-04 |

#### Abgrenzung zu bestehenden Risiken

| Bestehendes Risiko | Abgrenzung |
|---|---|
| MGR-001 — Teilmigrierter Zustand über eine Sequenzgrenze | Betrifft den Übergang innerhalb der Migrationssequenz. ROR-001 betrifft die Freigabefeststellung nach deren Abschluss. Keine Überschneidung. |
| MGR-002 — Ausgangszustand nicht wiederherstellbar | Betrifft die Rückführung einer Migrationseinheit. ROR-003 betrifft die Rücknahme einer Freigabefeststellung. Keine Überschneidung. |
| R-001 — Scope Creep | Betrifft die Ausweitung des Umfangs. Keine der drei Rolloutrisiken betrifft den Umfang. |
| GR-001 — Paralleler Artefaktbaum | Betrifft die Zugehörigkeit von Artefakten. ROR-002 betrifft den Abschlussstand der Gates. Berührungspunkt besteht über QG-007, ist aber in GR-001 bereits geführt und wird nicht doppelt aufgenommen. |

#### Übergabe an die Registerführung

Die drei Einträge sind in das konsolidierte Register in **Kapitel 11.11**
aufgenommen und werden dort geführt. Dieser Abschnitt leitet sie her und
begründet sie; er führt kein eigenes Register (Registerregel 5).

| ID | Klasse | Kritikalität | Owner | Status | Registerführung |
|---|---|---|---|---|---|
| ROR-001 | RK-11 | Hoch | Governance Architect | MITIGATED | Kapitel 11.11 |
| ROR-002 | RK-11 | Hoch | Governance Architect | MITIGATED | Kapitel 11.11 |
| ROR-003 | RK-11 | Erhöht | Governance Architect | MITIGATED | Kapitel 11.11 |

| Beitrag dieses Kapitels zum Register | Wert |
|---|---|
| Hergeleitete Einträge | 3 |
| Klasse RK-11 | Befüllt — 3 Einträge |
| Verbindlicher Gesamtstand | Kapitel 11.11 (16 Einträge) |

#### Registerführung

Es besteht genau **eine** Registerführung: Kapitel 11.11. Sie enthält sämtliche
16 Einträge. Kapitel 12.9 und Kapitel 13.9 leiten Einträge her und begründen
sie; sie führen keinen eigenen Registerstand. Abweichende Registerstände in
anderen Kapiteln sind ausgeschlossen.

| Kapitel | Rolle |
|---|---|
| 11.11 | Registerführung; verbindlicher Gesamtstand — 16 Einträge |
| 12.9 | Herleitung und Begründung der Klasse RK-10 (3 Einträge) |
| 13.9 | Herleitung und Begründung der Klasse RK-11 (3 Einträge) |

---

### 13.10 Rollout Constraints

| ID | Beschränkung |
|---|---|
| RCO-01 | Keine Umgehung der Migration. Ohne den Zustand MIGRATED sämtlicher Migrationseinheiten besteht kein Freigabegegenstand. |
| RCO-02 | Keine Umgehung eines Quality Gate. Ein Gate wird nicht vorzeitig geschlossen, um die Freigabereife herzustellen. |
| RCO-03 | Keine Umgehung der Governance. Die Freigabefeststellung ersetzt keine Genehmigungsentscheidung. |
| RCO-04 | Keine Teilfreigabe. Der Freigabegegenstand ist stets das Gesamtergebnis. |
| RCO-05 | Keine Architekturänderung. |
| RCO-06 | Keine neuen Requirements, Acceptance Criteria oder Quality Gates. |
| RCO-07 | Keine rolloutspezifischen Evidence-Artefakte. Nachweise stammen ausschließlich aus Kapitel 8.5. |
| RCO-08 | Keine neuen Einheiten und keine neue Struktur. Rollouteinheiten sind deckungsgleich mit Migrationseinheiten. |
| RCO-09 | Keine neue Risikoklassifikation. Rolloutrisiken werden ausschließlich unter RK-11 geführt. |
| RCO-10 | Keine Deployment-, Release-, Versionierungs-, CI/CD-, Infrastruktur-, Betriebs- oder Runtimeaussagen. |
| RCO-11 | Keine Termine, keine Sprintzuordnung, keine Ressourcenaussagen. |
| RCO-12 | Keine Absenkung einer Readiness- oder Completion-Bedingung zur Herstellung der Freigabereife. |

---

### 13.11 Rollout Traceability

#### Kette

```
Rollout Unit
     ↓
Migration Unit
     ↓
Work Package
     ↓
Acceptance Criteria
     ↓
Quality Gate
     ↓
Evidence
     ↓
Review
     ↓
Completion
```

**Keine neue Traceability-Ebene.** Rollout- und Migrationseinheit sind
deckungsgleich mit dem Work Package. Beide sind Sichten auf dieselbe Entität
und bilden keinen zusätzlichen Knoten.

#### Zuordnung

| RU | MU | WP | Acceptance Criteria | Quality Gate | Evidence | Completion |
|---|---|---|---|---|---|---|
| RU-01 | MU-01 | WP-001 | AC-001.1..AC-002.2 | QG-001 | EV-W01 | RS-02 |
| RU-02 | MU-02 | WP-002 | AC-003.1..AC-004.2 | QG-002 | EV-W02 | RS-02 |
| RU-03 | MU-03 | WP-003 | AC-005.1..AC-006.2 | QG-004, QG-006 | EV-W03, EV-I02 | RS-02 |
| RU-04 | MU-04 | WP-004 | AC-007.1..AC-008.2 | QG-006 | EV-W04, EV-I02 | RS-02 |
| RU-05 | MU-05 | WP-005 | AC-009.1..AC-010.2 | QG-007 | EV-W05, EV-I01 | RS-02 |
| RU-06 | MU-06 | WP-006 | AC-013.1..AC-014.2 | QG-003 | EV-W06, EV-I03, EV-I04 | RS-02 |
| RU-07 | MU-07 | WP-007 | AC-011.1..AC-012.2 | QG-005 | EV-W07, EV-D04 | RS-02 |

Querschnittlich geprüft und keiner einzelnen Einheit zugeordnet: QG-008 sowie
die phasenbezogenen Anteile von **QG-001** (NFR-004, Anhang B.12), QG-006 und
QG-007. Diese werden in RS-02 und RS-03 gesamthaft geführt; die Zuordnung von
QG-001 zu RU-01 in der Tabelle betrifft ausschließlich den AC-Anteil.

---

### 13.12 Rollout Readiness

Eine Rollouteinheit ist autorisierungsreif, wenn **sämtliche** folgenden
Bedingungen erfüllt sind.

| ID | Bedingung | Nachweis |
|---|---|---|
| RR-01 | Die zugehörige Migrationseinheit trägt den Zustand MIGRATED. | Kapitel 12.6 |
| RR-02 | Die zugeordneten Acceptance Criteria tragen den Status VERIFIED. | Kapitel 8.6 |
| RR-03 | Die einheitenbezogenen Quality Gates sind abgeschlossen. | Kapitel 8.7 |
| RR-04 | Die nicht innerhalb eines einzelnen Work Package abschließbaren Quality Gates QG-001, QG-006, QG-007 und QG-008 sind abgeschlossen — bei QG-001 einschließlich des auf NFR-004 bezogenen Anteils. | Kapitel 7.5, 8.7; Anhang B.12 |
| RR-05 | Sämtliche zugeordneten Nachweise liegen vollständig vor. | Kapitel 8.5 |
| RR-06 | Sämtliche Registereinträge mit Bezug zur Einheit tragen den Zustand CLOSED oder ACCEPTED (RPR-06). | Kapitel 11.11 |
| RR-07 | Die Rücknahme der Freigabefeststellung ist bestimmt. | 13.8 Regel 1 |
| RR-08 | Die Governance-Bestätigungspunkte GV-01 bis GV-08 sind erfüllt. | Kapitel 8.8 |

#### Regeln

| # | Regel |
|---|---|
| 1 | Die Readiness-Prüfung erfolgt je Einheit und wird dokumentiert. |
| 2 | Eine teilweise erfüllte Readiness begründet keine Autorisierungsreife. |
| 3 | Readiness bezeichnet die Reife zur Autorisierung, nicht die Durchführung einer Freigabe. |
| 4 | Readiness sämtlicher Einheiten ist Voraussetzung der Freigabereife des Gesamtergebnisses (RPR-02). |

---

### 13.13 Rollout Completion

**Einordnung.** Der Bezeichnerraum ROC wird verwendet, weil RCC in Kapitel
11.15 für Risk Completion Conditions belegt ist. Eine doppelte Belegung würde
die Rückverfolgbarkeit korrumpieren.

| ID | Bedingung | Soll | Ist | Evidence | Review | Owner |
|---|---|---|---|---|---|---|
| ROC-01 | Rollouteinheiten definiert und Migrationseinheiten zugeordnet | 7 | 7 | EV-D03 | Independent Review | Governance Architect |
| ROC-02 | Zustandsmodell definiert | 5 | 5 | EV-D03 | Independent Review | Governance Architect |
| ROC-03 | Rolloutsequenz mit Ein- und Austrittsbedingungen definiert | 4 | 4 | EV-D03 | Independent Review | Governance Architect |
| ROC-04 | Readiness-Bedingungen definiert | 8 | 8 | EV-D03 | Independent Review | Governance Architect |
| ROC-05 | Rollback-Regeln definiert | 6 | 6 | EV-D03 | Independent Review | Governance Architect |
| ROC-06 | Rolloutrisiken im Register geführt | 3 | 3 | EV-D05 | Independent Review | Governance Architect |
| ROC-07 | Klasse RK-11 befüllt | 1 | 1 | EV-D05 | Independent Review | Governance Architect |
| ROC-08 | Registerführung eindeutig geregelt — genau ein Abschnitt führt den Gesamtstand (Kapitel 11.11, 16 Einträge) | 1 | 1 | EV-D05 | Independent Review | Governance Architect |
| ROC-09 | Traceability je Einheit lückenlos | 7 | 7 | EV-D03 | Independent Review | Governance Architect |
| ROC-10 | Acceptance Criteria über Einheiten abgedeckt | 29 | 29 | EV-D03 | Independent Review | Governance Architect |
| ROC-11 | Quality Gates abgedeckt, einschließlich der phasenübergreifenden | 8 | 8 | EV-D03 | Independent Review | Governance Architect |
| ROC-12 | Schnittstelle zu Kapitel 10 definiert | 1 | 1 | EV-D03 | Independent Review | Governance Architect |
| ROC-13 | Neue Requirements, Kriterien, Gates, Evidence, Einheiten oder Governance-Ebenen | 0 | 0 | EV-G01 | Independent Review | Governance Architect |
| ROC-14 | Bestehende Risikobewertungen unverändert — geprüft gegen die 13 vor Kapitel 13 bestehenden Einträge | 13 | 13 | EV-D05 | Independent Review | Governance Architect |

Vierzehn von vierzehn Bedingungen erfüllt. Die Rolloutplanung ist vollständig.

---

### 13.14 Authorization Interface

#### Übergabe an Kapitel 10

| Gegenstand | Inhalt | Empfangende Stelle |
|---|---|---|
| Freigabereife | Sämtliche Rollouteinheiten im Zustand READY FOR AUTHORIZATION | Kapitel 10.5, RL-04 und RL-05 |
| Nachweislage | Vollständigkeit sämtlicher Nachweise gemäß 13.11 | Kapitel 10.7 |
| Gate-Abschluss | Abschluss von QG-001 bis QG-008 | Kapitel 10.8 |
| Risikolage | Konsolidiertes Register (Kapitel 11.11), sämtliche 16 Einträge im Zustand CLOSED oder ACCEPTED | Kapitel 10.6 (Bedingung 5); Kapitel 8.8 (GV-08) |
| Governance-Bestätigung | GV-01 bis GV-08 erfüllt | Kapitel 10.6 |

#### Regeln

| # | Regel |
|---|---|
| 1 | Dieses Kapitel stellt die Freigabereife fest. Die Freigabeentscheidung trifft ausschließlich die in Kapitel 10 bezeichnete Instanz. |
| 2 | Der Approval-Prozess aus Kapitel 10.4 wird weder vorweggenommen noch wiederholt noch verändert. |
| 3 | Die Übergabe erzeugt keine Autorisierung. Autorisierung entsteht ausschließlich gemäß Kapitel 10.10. |
| 4 | Eine Rücknahme der Freigabefeststellung nach Übergabe wirkt auf die Voraussetzungen der Kapitel 10.6 zurück. |

---

### 13.15 Final Rollout Statement

#### Normative Feststellung

Die Rolloutplanung des Milestone 1.0 gilt als **vollständig** — nicht als
durchgeführt —, wenn sämtliche folgenden Bedingungen erfüllt sind:

| # | Bedingung |
|---|---|
| 1 | Der Freigabegegenstand ist bestimmt und auf das Migrationsergebnis zurückgeführt. |
| 2 | Rollouteinheiten sind bestimmt und deckungsgleich mit Migrationseinheiten und Work Packages. |
| 3 | Der Zustandsraum jeder Einheit ist definiert und die Übergänge sind geregelt. |
| 4 | Die Reihenfolge der Freigabefeststellung ist mit Ein- und Austrittsbedingungen bestimmt. |
| 5 | Für jede Einheit ist die Rücknahme der Freigabefeststellung bestimmt. |
| 6 | Für jede Einheit sind Acceptance Criteria, Quality Gates und Nachweise zugeordnet. |
| 7 | Rolloutrisiken sind im bestehenden Framework geführt und die Registerführung ist eindeutig. |
| 8 | Die Übergabe an den Genehmigungsprozess ist bestimmt. |

#### Abgrenzung

Vollständige Rolloutplanung bedeutet weder Freigabe noch Veröffentlichung
noch Auslieferung. Dieses Kapitel erzeugt keine Freigabehandlung und keine
Autorisierung dazu.

Eine Aussage über die Veröffentlichung von Software ist innerhalb dieses
Frameworks unzulässig.

#### Feststellung zum Zeitpunkt dieser Fassung

| Gegenstand | Feststellung |
|---|---|
| Bedingungen 1 bis 8 | Erfüllt |
| Zustand sämtlicher Rollouteinheiten | PENDING |
| Rolloutrisiken | Drei Einträge, sämtlich MITIGATED |
| Registerstand | 16 Einträge, geführt in Kapitel 11.11; Klassen RK-10 und RK-11 befüllt |
| Gesamtbewertung | Die Rolloutplanung des Milestone 1.0 ist **vollständig**. Eine Freigabe ist nicht erteilt und nicht autorisiert. |

---

*Ende Kapitel 13.*

---

## Anhang A — Pending Governance Resolution GR-001

Dieser Anhang ist die **Fundstelle der normativen Pending Resolution** zu
GR-001. Er ist kein Kapitel des Plans.

**Er ist kein Register.** Die Registerführung sämtlicher Risiken des Milestones
liegt ausschließlich beim konsolidierten Register in Kapitel 11.11
(Registerregel 1). GR-001 ist dort mit Klasse, Kritikalität, Owner und Status
geführt; die Verortung ist in Kapitel 11.10 dokumentiert. Die folgende
Kopfangabe ist nachrichtlich und begründet keinen zweiten Registerstand.

| ID | Titel | Klasse | Status | Owner | Registerführung |
|---|---|---|---|---|---|
| GR-001 | Paralleler Artefaktbaum außerhalb der normativen Baseline | RK-04 Governance | **PENDING DECISION** | Governance Architect | Kapitel 11.11 |

Der Anhang wurde vor Kapitel 11 erstellt. Die dort angekündigte Überführung in
die Behandlung der umsetzungsbezogenen Risiken (PS-06) ist mit Kapitel 11.10
**vollzogen**; der Anhang verbleibt ausschließlich als Fundstelle der
Resolution PR-001.1 bis PR-001.9.

---

### GR-001 — Paralleler Artefaktbaum außerhalb der normativen Baseline

| Feld | Inhalt |
|---|---|
| **Risikoklasse** | RK-04 Governance (Kapitel 11.4) |
| **Status** | **PENDING DECISION** (Kapitel 11.6) |
| **Owner** | Governance Architect |
| **Review** | Implementation Plan Independent Review |
| **Quelle** | Module Work Breakdown, Governance-Befund GB-001 (5.5.4) |
| **Registerführung** | Kapitel 11.11 |

#### Beschreibung

Während der Module-Work-Breakdown-Analyse wurde ein paralleler Artefaktbaum
unter `src/jochen_x/**` identifiziert, der nicht Bestandteil der Bootstrap
Baseline 1.0, der Engineering Specification 1.0 oder der anderen normativen
Referenzdokumente ist.

#### Feststellung

Der Artefaktbaum wird durch die normativen Governance-Dokumente nicht
referenziert. Gleichzeitig existieren Testartefakte, die auf diesen Bereich
Bezug nehmen.

#### Mögliche Auswirkungen

- unklare Regressionsbasis
- uneindeutige Modulzuordnung
- mögliche Doppelpflege
- unklare Scope-Abdeckung
- erschwerte Traceability

#### Mitigation

Vor Beginn der Sprintplanung MUSS eindeutig entschieden werden, welcher
Artefaktbaum produktiver Bestandteil des Milestones ist.

Diese Entscheidung liegt außerhalb der Autorisierung dieses Implementation
Plans und ist gegebenenfalls als separater Governance-Entscheid zu behandeln.

#### Betroffene Planungsinhalte

| Planungsinhalt | Art der Betroffenheit |
|---|---|
| Kapitel 3.1 — Regressionsbasis (1019 Tests) | Der Testbestand umfasst Artefakte beider Bäume; die Bezugsgröße ist bis zur Entscheidung nicht eindeutig zugeordnet. |
| Kapitel 3.2 — Verifikation des Ist-Zustands | Die Baseline-Bestätigung erfolgt gegen die baseline-geführte Struktur. |
| DA-015 / MWB-015 — Testbasis | Die Zuordnung ist auf die baseline-geführte Struktur beschränkt. |
| MWB-001, MWB-003, MWB-007, MWB-009 | Die Modul- und Dateizuordnung ändert sich, falls die Entscheidung zugunsten des parallelen Baums ausfällt. |
| Kapitel 5.5.4 — Nicht zugeordnete Artefaktbereiche | `src/jochen_x/**` ist bis zur Entscheidung ausdrücklich nicht zugeordnet. |

#### Wirkung auf den Plan

Die Deltas und die Modulzuordnung dieses Plans sind ausschließlich der
baseline-geführten Struktur zugeordnet. Solange GR-001 den Status PENDING
DECISION trägt, steht diese Zuordnung unter dem Vorbehalt der ausstehenden
Governance-Entscheidung.

GR-001 begründet keine Änderung an Baseline, Architecture Book, Engineering
Specification oder Scope. Der Eintrag dokumentiert das Risiko; er löst es nicht
auf (PP-04).

---

---

### GR-001 — Pending Governance Resolution

Eine abschließende Governance Resolution zu GR-001 ist zum Zeitpunkt dieser
Fassung **nicht möglich**, da die erforderliche Entscheidung außerhalb der
Autorisierungsgrenze dieses Plans liegt (Kapitel 1.6, PP-04). An ihre Stelle
tritt die folgende normative Pending Resolution.

#### PR-001.1 — Offener Punkt

Es ist nicht entschieden, welcher Artefaktbaum produktiver Bestandteil des
Milestone 1.0 ist. Das Repository enthält neben der von Bootstrap Baseline 1.0
und Architecture Book v2.0 beschriebenen Struktur einen zweiten, in sich
geschlossenen Artefaktbaum mit eigenem Testbestand, der vom
Anwendungseinstiegspunkt nicht referenziert und in keiner normativen Eingabe
dieses Plans beschrieben ist.

#### PR-001.2 — Entscheidungsbedarf

| # | Zu entscheidende Frage |
|---|---|
| 1 | Welcher Artefaktbaum ist produktiver Bestandteil des Milestone 1.0? |
| 2 | Welchen Status hat der jeweils andere Baum — Erhaltung, Stilllegung oder Überführung? |
| 3 | Welcher Testbestand bildet die verbindliche Regressionsbasis des Milestones? |
| 4 | Ist zur Umsetzung der Entscheidung ein ADR oder ein RDR erforderlich? |

Die Fragen 1 bis 3 sind Governance-Entscheidungen. Frage 4 ergibt sich aus der
Antwort auf die Fragen 1 und 2 und richtet sich nach der Change Control der
Bootstrap Baseline.

#### PR-001.3 — Referenzstellen und Begründung des Bedarfs

| Fundstelle | Warum GR-001 dort benötigt wird |
|---|---|
| Kapitel 5.5.4 — Nicht zugeordnete Artefaktbereiche | Ohne Entscheidung kann der zweite Baum keinem Delta zugeordnet werden. Die Nichtzuordnung muss ausgewiesen werden, damit sie nicht als Auslassung des Module Work Breakdown gewertet wird. |
| Kapitel 6.5 — Governance-Auswirkungen | Feststellung, dass GR-001 die **Reihenfolge** nicht berührt, da diese ausschließlich aus dem genehmigten Abhängigkeitsgraphen abgeleitet ist. Ohne diese Feststellung bliebe offen, ob die Sequenz unter Vorbehalt steht. |
| Kapitel 7.6 — Angewandtes Beispiel | GR-001 belegt die Anwendung des Eskalationsmusters: dokumentiert, nicht eigenmächtig aufgelöst. |
| Kapitel 7.8 — Reviewfähigkeit | Nachweis, dass offene Punkte ausgewiesen statt aufgelöst wurden. |
| Kapitel 8.8 — GV-08 | „Keine offenen Governance Findings" ist ohne dokumentierte Entscheidung zu GR-001 nicht bestätigbar. |
| Kapitel 9.6 — Regression Strategy | Die Bezugsgröße des Regressionsnachweises ist ohne Entscheidung nicht eindeutig. |
| Kapitel 9.8 — Test Completion, Bedingung 5 | Die Vollständigkeit der Regressionsplanung steht unter demselben Vorbehalt. |

#### PR-001.4 — Auswirkungen auf die Regressionsbasis

| Aspekt | Feststellung |
|---|---|
| Dokumentierte Bezugsgröße | 1019 Tests, 0 Regressionen (Bootstrap Baseline 1.0, Kapitel 3.1) |
| Tatsächliche Zusammensetzung | Der Testbestand umfasst Artefakte beider in Kapitel 5.5.4 genannter Strukturen |
| Folge ohne Entscheidung | Die Zahl 1019 ist als Gesamtgröße korrekt, aber nicht eindeutig einer Struktur zugeordnet. Ein Regressionsnachweis gegen „die Baseline" ist damit mehrdeutig. |
| Folge bei Entscheidung zugunsten der baseline-geführten Struktur | Die Bezugsgröße ist auf den dieser Struktur zugeordneten Testbestand einzugrenzen; die Gesamtzahl 1019 bleibt als Repository-Kennzahl bestehen, ist aber nicht die Regressionsbezugsgröße. |
| Folge bei abweichender Entscheidung | Delta Analysis und Module Work Breakdown sind in den betroffenen Zuordnungen erneut zu führen (PR-001.5). |
| Unberührt | Die Regressionsregeln aus Kapitel 9.6 gelten in jedem Fall unverändert. Betroffen ist die Bezugsgröße, nicht das Ziel „keine Regressionen". |

#### PR-001.5 — Auswirkungen auf QG-007

| Aspekt | Feststellung |
|---|---|
| Prüfkriterium QG-007 | Baseline-Tests und hinzugekommene Tests bestanden, keine Regression |
| Abhängigkeit von GR-001 | QG-007 prüft gegen die Regressionsbasis. Ist deren Umfang nicht eindeutig, ist das Prüfkriterium nicht eindeutig. |
| Nachweis EV-I01 | Der Regressionsnachweis bleibt planerisch vollständig definiert; seine Bezugsgröße ist festzulegen. |
| Wirkung auf den Phasenübergang | QG-007 ist am Ende von Phase B abzuschließen (Kapitel 8.7). Eine bis dahin ausstehende Entscheidung verhindert den formalen Abschluss des Gates. |
| Wirkung auf andere Gates | QG-001 bis QG-006 und QG-008 sind nicht über die Regressionsbasis definiert und daher nicht betroffen. QG-008 ist über GV-08 betroffen, nicht über die Regression. |

#### PR-001.6 — Auswirkungen auf die Completion Conditions

| Bedingung | Kapitel | Wirkung |
|---|---|---|
| GV-08 — Keine offenen Governance Findings | 8.8 | **Nicht erfüllbar**, solange GR-001 den Status PENDING DECISION trägt |
| Test Completion, Bedingung 5 — Vollständige Regression geplant | 9.8 | Erfüllt als **Planung**; die Bezugsgröße bleibt vorbehaltlich |
| Verification Completion, Bedingung 6 — Baseline-Invarianten berücksichtigt | 8.9 | Erfüllt; GR-001 berührt keine Baseline-Invariante, sondern die Zuordnung von Artefakten |
| SC-01 bis SC-10 — Erfolgskriterien des Plans | 2.6 | Nicht betroffen. GR-001 verhindert die Genehmigung des Plans nicht; es verhindert den Abschluss des Milestones. |

#### PR-001.7 — Späteste notwendige Entscheidung

| Zeitpunkt | Begründung |
|---|---|
| **Vor Beginn der Sprintplanung** | Ursprüngliche Mitigation gemäß GR-001. Ohne Entscheidung ist die Modulzuordnung der Sprints nicht eindeutig. |
| **Spätestens vor Abschluss von Phase B** | Härtere Grenze: QG-007 ist am Ende von Phase B abzuschließen und setzt eine eindeutige Regressionsbezugsgröße voraus (PR-001.5). |
| **Zwingend vor Phase D** | GV-08 ist ohne dokumentierte Entscheidung nicht bestätigbar (PR-001.6). |

Die maßgebliche Frist ist der Beginn der Sprintplanung. Die beiden späteren
Zeitpunkte sind Rückfallgrenzen und keine Verlängerung.

#### PR-001.8 — Auswirkungen auf das Approval

| Gegenstand | Bewertung |
|---|---|
| Genehmigung des Implementation Plan 1.0 | **Nicht blockierend.** GR-001 ist vollständig dokumentiert, mit Auswirkungen, Owner, Entscheidungsbedarf und Frist. Der Plan weist den offenen Punkt aus, statt ihn aufzulösen — dies entspricht PP-04 und dem Eskalationsmuster aus Kapitel 7.6. |
| Independent Review des Plans | Der Review hat GR-001 zur Kenntnis zu nehmen und die Frist gemäß PR-001.7 zu bestätigen oder zu ändern. |
| Beginn der Sprintplanung | **Blockierend** ohne dokumentierte Entscheidung. |
| Abschluss des Milestones | **Blockierend** über GV-08. |
| Engineering Specification 1.0 | Nicht betroffen. GR-001 begründet keine Änderung an Requirements, Acceptance Criteria, Quality Gates oder Scope. |
| Bootstrap Baseline 1.0, Architecture Book v2.0, ADRs | Nicht betroffen, solange keine Entscheidung getroffen ist. Eine Entscheidung kann eine Baseline-Änderung auslösen und erfordert dann ADR oder RDR. |

#### PR-001.9 — Status

| Feld | Wert |
|---|---|
| Registerführung | Kapitel 11.11 (Gesamtstand), Verortung dokumentiert in Kapitel 11.10. Dieser Anhang ist ausschließlich die Fundstelle der Pending Resolution und führt kein Register. |
| Resolution-Typ | **Pending Resolution** — abschließende Resolution nicht möglich |
| Status GR-001 | **PENDING DECISION** (Kapitel 11.6) |
| Owner | Governance Architect |
| Entscheidungsinstanz | Governance Architect / Release Authority; bei Baseline-Berührung zusätzlich ADR oder RDR |
| Review | Implementation Plan Independent Review |
| Wirkung dieser Pending Resolution | Sie dokumentiert den offenen Punkt normativ. Sie entscheidet ihn nicht und ändert weder Architektur noch Requirements noch die Engineering Specification. |

---

*Ende Anhang A.*

---

## Anhang B — Performance Measurement Methodology

Dieser Anhang erfüllt Erfolgskriterium SC-06 und schließt Finding F-004 des
Independent Review der Engineering Specification. Er definiert ausschließlich
das **Nachweisverfahren**. Er enthält keine Implementierung, keine Benchmarks
und keine Werkzeugfestlegung.

### B.1 Messziel

Nachweis, dass der Milestone 1.0 **keine messbare Performance-Regression**
gegenüber Bootstrap Baseline 1.0 einführt (NFR-004).

Das Messziel ist ein Erhaltungsnachweis, kein Optimierungsziel. Eine
Verbesserung der gemessenen Werte ist zulässig und erfordert keine gesonderte
Behandlung.

Die Methodik führt **kein neues Requirement** ein. Sie macht das bereits
genehmigte NFR-004 nachweisbar.

### B.2 Baseline

| Eigenschaft | Festlegung |
|---|---|
| Bezugszustand | Bootstrap Baseline 1.0 auf Release Tag `v0.9.0` |
| Erhebungszeitpunkt | Phase A — vor Beginn jeder Umsetzung |
| Gegenstand | Baseline-Messreihe gemäß B.6 |
| Verbindlichkeit | Die Baseline-Messreihe ist nach ihrer Erhebung unveränderlich. Eine erneute Erhebung ist nur zulässig, wenn das Referenzsystem gemäß B.3 gewechselt wurde; in diesem Fall ist die vollständige Messreihe neu zu erheben. |
| Bezug zur Baseline-Bestätigung | Die Erhebung erfolgt nach der Bestätigung des Baseline-Zustands gemäß Kapitel 3.8 und ist Bestandteil des Nachweises EV-D01. |

Eine Messung gegen einen unbestätigten Baseline-Zustand ist unzulässig.

### B.3 Referenzsystem

| Anforderung | Festlegung |
|---|---|
| Einheitlichkeit | Baseline-Messreihe und Vergleichsmessreihe werden auf **demselben** Referenzsystem erhoben. |
| Unveränderlichkeit | Das Referenzsystem bleibt über den gesamten Milestone unverändert. |
| Protokollpflicht | Die identitätsbestimmenden Eigenschaften des Referenzsystems sind zu protokollieren: Rechnerklasse, Betriebssystem und Version, Python-Version, Konfigurationsstand der Anwendung, Zustand der Datenbasis. |
| Wechsel | Ein Wechsel des Referenzsystems macht alle bisherigen Messreihen ungültig und erzwingt eine vollständige Neuerhebung (B.2). |
| Nicht Gegenstand | Beschaffung, Auswahl und Bereitstellung des Referenzsystems sind Ressourcenplanung und nicht Gegenstand dieses Plans (VC-09). |

### B.4 Messbedingungen

| # | Bedingung |
|---|---|
| 1 | Baseline- und Vergleichsmessung erfolgen unter identischer Anwendungskonfiguration. |
| 2 | Während der Messung findet keine andere planmäßige Last auf dem Referenzsystem statt. |
| 3 | Die Datenbasis ist in beiden Messreihen im gleichen Zustand. |
| 4 | Die Testprinzipien der Engineering Specification gelten unverändert: deterministisches Verhalten, keine Wartezeiten, keine externen Abhängigkeiten. |
| 5 | Erst- und Folgeausführung werden getrennt erfasst und nicht miteinander verrechnet. |
| 6 | Abweichungen von den Bedingungen 1 bis 5 machen die betroffene Messung ungültig und sind zu protokollieren. |

### B.5 Wiederholbarkeit

| Regel | Festlegung |
|---|---|
| Wiederholungen | Jede Messgröße wird je Messreihe mindestens **fünf** Mal erhoben. |
| Kennwert | Maßgeblich ist der **Median** der Wiederholungen. |
| Streuungsmaß | Die Streuung wird als Spanne zwischen kleinstem und größtem Messwert der Reihe erfasst. |
| Begründung des Mindestumfangs | Ohne mehrfache Erhebung ist kein Streuungsmaß bestimmbar; ohne Streuungsmaß ist die Regressionsschwelle gemäß B.7 nicht ableitbar. Fünf Wiederholungen sind der kleinste Umfang, der einen Median mit beidseitiger Streuungsangabe liefert. |
| Verwerfungsregel | Übersteigt die Streuung der Baseline-Messreihe den Median derselben Reihe, gilt die Messgröße als nicht ausreichend stabil messbar. Sie ist zu protokollieren und aus der Regressionsbewertung auszuschließen; der Ausschluss ist zu begründen. |

Der festgelegte Wiederholungsumfang ist ein Verfahrensparameter der Methodik.
Er ist kein Acceptance Criterion und kein Quality Gate.

### B.6 Messgrößen

Die Messgrößen sind aus der Struktur der Bootstrap Baseline 1.0 abgeleitet.
Es werden keine Messgrößen außerhalb des genehmigten Baseline-Umfangs
eingeführt.

| ID | Messgröße | Bezug |
|---|---|---|
| PM-01 | Gesamtdauer der Bootstrap-Ausführung von Beginn der ersten bis Abschluss der letzten Phase | Bootstrap-Phasensequenz, BP-01 |
| PM-02 | Dauer je Startup-Phase (INITIALIZE, LOAD_PLUGINS, LOAD_RESOURCES, FINALIZE) | Bootstrap-Phasensequenz, BP-01 bis BP-03 |
| PM-03 | Dauer des vollständigen Durchlaufs der Plugin-Runtime-Pipeline von Discovery bis Activation | Plugin-Runtime-Pipeline, PL-01 bis PL-05 |

| Ausschluss | Begründung |
|---|---|
| Messgrößen außerhalb von Bootstrap und Plugin-Runtime-Pipeline | Nicht Gegenstand von NFR-004 in seiner Bezugsgröße; eine Ausweitung wäre eine Scope-Erweiterung (PP-05) |
| Ressourcenkennzahlen (Speicher, CPU-Auslastung) | Nicht Bestandteil der Baseline-Kenndaten; ihre Aufnahme erforderte eine Governance-Entscheidung |

### B.7 Zulässige Abweichungen

| Regel | Festlegung |
|---|---|
| Toleranzband | Für jede Messgröße bildet die in der **Baseline-Messreihe** ermittelte Streuung das Toleranzband. |
| Zulässige Abweichung | Eine Abweichung des Vergleichsmedians vom Baseline-Median innerhalb des Toleranzbandes gilt als **nicht messbar** und damit als zulässig. |
| Verbesserung | Ein Vergleichsmedian unterhalb des Baseline-Medians ist stets zulässig und wird nicht als Abweichung geführt. |
| Keine feste Prozentgrenze | Es wird bewusst **kein** fester Prozentwert festgelegt. Eine frei gewählte Schwelle wäre eine neue, nicht genehmigte Akzeptanzbedingung. Das Toleranzband ergibt sich ausschließlich aus der gemessenen Streuung des Bezugszustands. |
| Grenzfall | Liegt der Vergleichsmedian genau auf der Grenze des Toleranzbandes, ist die Vergleichsmessreihe einmalig vollständig zu wiederholen. Das Ergebnis der Wiederholung ist maßgeblich. |

### B.8 Regressionserkennung

#### Kriterium

Eine **Performance-Regression** liegt vor, wenn der Vergleichsmedian einer
Messgröße den Baseline-Median um mehr als das Toleranzband gemäß B.7
überschreitet und dieses Ergebnis in der Wiederholungsmessung bestätigt wird.

#### Verfahren

| Schritt | Handlung |
|---|---|
| 1 | Erhebung der Vergleichsmessreihe am Ende von Phase B unter den Bedingungen gemäß B.4 |
| 2 | Bildung von Median und Streuung je Messgröße gemäß B.5 |
| 3 | Vergleich gegen die Baseline-Messreihe gemäß B.7 |
| 4 | Bei Überschreitung: einmalige vollständige Wiederholung der Vergleichsmessreihe |
| 5 | Bei bestätigter Überschreitung: Feststellung einer Regression |

#### Wirkung einer festgestellten Regression

| Gegenstand | Wirkung |
|---|---|
| NFR-004 | Nicht erfüllt |
| QG-001 | Nicht bestehbar, solange die Regression besteht |
| Behandlung | Der Sachverhalt ist gemäß Kapitel 7.6 zu eskalieren. Eine Absenkung der Messanforderung oder eine Anpassung des Toleranzbandes zur Vermeidung des Befundes ist unzulässig. |
| Ausgeschlossene Auflösung | Die Regression wird nicht durch Änderung der Methodik, sondern ausschließlich durch Beseitigung der Ursache oder durch eine dokumentierte Governance-Entscheidung aufgelöst. |

### B.9 Dokumentationspflicht

Jede Messreihe ist zu protokollieren. Das Protokoll enthält verbindlich:

| Feld | Inhalt |
|---|---|
| Messreihe | Baseline-Messreihe oder Vergleichsmessreihe |
| Bezugszustand | Release Tag beziehungsweise Umsetzungsstand |
| Referenzsystem | Identitätsbestimmende Eigenschaften gemäß B.3 |
| Messbedingungen | Bestätigung der Bedingungen 1 bis 5 gemäß B.4; Abweichungen ausdrücklich |
| Messgrößen | PM-01, PM-02, PM-03 |
| Einzelwerte | Alle Wiederholungen je Messgröße |
| Kennwerte | Median und Streuung je Messgröße |
| Bewertung | Vergleichsergebnis je Messgröße gemäß B.7 |
| Ausschlüsse | Nicht stabil messbare Messgrößen mit Begründung gemäß B.5 |
| Ergebnis | Regression festgestellt oder nicht festgestellt |

Ein unvollständiges Protokoll ist kein Nachweis. Die Archivierung erfolgt in
den Deliverables der Engineering Specification (Sprint Reports, Milestone
Review Report); es werden keine neuen Ablageartefakte eingeführt.

### B.10 Evidence-Zuordnung

Die Methodik führt **keine neuen Evidence-Einträge** ein. Sie ordnet sich
vollständig den in Kapitel 8.5 definierten Nachweisen zu.

| Gegenstand | Evidence | Zeitpunkt | Kapitelbezug |
|---|---|---|---|
| Baseline-Messreihe | EV-D01 — Bestätigungsprotokoll der Baseline | Ende Phase A | 8.5, VL-01 |
| Vergleichsmessreihe und Regressionsbewertung | EV-I01 — Regressionsnachweis | Ende Phase B | 8.5, VL-03 |
| Gate-Nachweis | EV-W01 — AC-Nachweis WP-001 | Abschluss WP-001 und Ende Phase B | 8.5, VL-02 |

Die Zuordnung ist konsistent mit Kapitel 9.4 (NFR-004 → TC-02 → QG-001) und
Kapitel 9.7 (TC-02 → EV-I01).

### B.11 Beziehung zu NFR-004

| Aspekt | Feststellung |
|---|---|
| NFR-004 | „Der Milestone führt keine messbaren Performance-Regressionen gegenüber der Bootstrap Baseline 1.0 ein." |
| Beitrag dieser Methodik | Sie definiert, was „messbar" bedeutet: eine Abweichung, die das aus dem Bezugszustand ermittelte Toleranzband überschreitet und in der Wiederholung bestätigt wird. |
| Änderung an NFR-004 | Keine. Wortlaut, Geltung und Gate-Zuordnung bleiben unverändert. |

### B.12 Beziehung zu QG-001

| Aspekt | Feststellung |
|---|---|
| QG-001 | Prüft unter anderem NFR-004; Kriterium unter anderem „keine Performance-Regression" |
| Beitrag dieser Methodik | Sie liefert das Prüfverfahren für den performancebezogenen Anteil des Gate-Kriteriums. |
| Abschlusszeitpunkt | Der performancebezogene Anteil von QG-001 ist erst mit Vorliegen der Vergleichsmessreihe am Ende von Phase B abschließend bewertbar. Der übrige Anteil von QG-001 bleibt gemäß Kapitel 8.7 mit Abschluss von WP-001 prüfbar. |
| Änderung an QG-001 | Keine. Prüfmethode, geprüfte Acceptance Criteria und Kriterium bleiben unverändert. |

### B.13 Beziehung zu TC-02

| Aspekt | Feststellung |
|---|---|
| TC-02 | Regression Tests, Testebene TL-03, Nachweis EV-I01 |
| Beitrag dieser Methodik | Die Performance-Messung ist der performancebezogene Anteil der Regressionsprüfung und teilt deren Zeitpunkt und Nachweis. |
| Abgrenzung | TC-02 umfasst die funktionale Regression und die Performance-Regression. Beide werden getrennt bewertet und getrennt protokolliert. |
| Änderung an TC-02 | Keine. Es entsteht keine neue Testkategorie und keine neue Testart. |

### B.14 Closing Statement zu F-004

| Feld | Inhalt |
|---|---|
| Finding | F-004 — Performance-Messmethodik im Implementation Plan zu definieren |
| Schweregrad | Low |
| Herkunft | Independent Governance Review der Engineering Specification 1.0 R1 |
| Erfüllungsnachweis | Anhang B, Abschnitte B.1 bis B.13 |
| Umfang der Erfüllung | Messziel, Baseline, Referenzsystem, Messbedingungen, Wiederholbarkeit, Messgrößen, zulässige Abweichungen, Regressionserkennung, Dokumentationspflicht, Evidence-Zuordnung sowie die Beziehungen zu NFR-004, QG-001 und TC-02 sind vollständig definiert. |
| Neue Anforderungen | Keine |
| Neue Acceptance Criteria | Keine |
| Neue Quality Gates | Keine |
| Neue Evidence-Artefakte | Keine |
| Änderungen an der Engineering Specification | Keine |
| Erfolgskriterium | SC-06 erfüllt |
| **Status F-004** | **CLOSED** |

Die Schließung von F-004 ist durch den Independent Review des Implementation
Plans zu bestätigen. Bis zu dieser Bestätigung gilt der Status als vom Plan
erklärt, nicht als extern verifiziert.

---

*Ende Anhang B.*
