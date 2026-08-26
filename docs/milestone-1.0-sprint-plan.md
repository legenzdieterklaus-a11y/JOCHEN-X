# JOCHEN X — Milestone 1.0 Sprint Plan

| Feld | Wert |
|---|---|
| Document | JOCHEN X — Milestone 1.0 Sprint Plan |
| Status | **APPROVED AS PLANNING BASIS (ADW-SPR-1.0-001)** |
| Version | 1.0 |
| Revision | R0 |
| Datum | 2026-08-09 |
| Rolle | Senior Software Architect / Technical Program Planner / Governance-konformer Sprint Planner |
| Planungsgrundlage | Implementation Plan 1.0 **R1.2 (APPROVED)** — maßgebliche Grundlage; Engineering Specification 1.0 R1 (APPROVED); Architecture Book v2.0 (FROZEN); Bootstrap Baseline 1.0 (APPROVED); GDR-002 (GR-001 DECIDED); Preflight 2026-08-09 (SPRINT PLANNING AUTHORIZED) |
| Begleitartefakt | `docs/audits/milestone-1.0-sprint-planning-summary-r0.md` |
| Geltung | Dieser Plan operationalisiert den genehmigten Implementation Plan. Er definiert **keine** neuen Requirements, keine Architektur-, Security- oder Governance-Entscheidungen und ist **keine Implementierung**. |

---

## 1. Leitprinzip und Grenzen

> **Wir planen jetzt die Umsetzung. Wir führen sie noch nicht aus.**

- Sprint Planning ≠ Coding. Kein Code wurde geschrieben oder geändert; keine Anwendungsdatei wurde verändert.
- Coding-Bedingungen 7–9 des Implementation Plans (IP §10.6) sind offen; **RL-05 ist nicht erreicht** (IP §10.5).
- Jeder Sprint unterscheidet zwischen **Planning Deliverable** (dieses Dokument) und späterem **Implementation Deliverable** (entsteht erst nach Coding-Freigabe).
- `src/jochen_x/**` ist gemäß GDR-002 D-2 stillgelegt, bleibt physisch unangetastet und wird durch diesen Plan **nicht** reaktiviert.

---

## 2. Regressionsbezugsgröße (erster Planungsschritt — festgestellt)

Traceability: `SP-001 → GDR-002 D-3 → IP §11.10 (Completion), §3.1, §9.6; PR-001.4`

**Methode:** Read-only-Testkollektion (`pytest --collect-only`, kein Testlauf, keine Dateiänderung). Abgrenzung der Testbestände über Import-Analyse: Testdateien, die aus dem stillgelegten Paket `jochen_x` importieren, gehören zum stillgelegten Bestand; String-Vorkommen (Logger-Name, Datenbankpfad) sind keine Zugehörigkeit.

| Größe | Wert |
|---|---|
| Repository-Gesamtbestand (Kennzahl, nicht Bezugsgröße) | 1019 Tests (deckungsgleich mit IP §3.1) |
| Testbestand des stillgelegten Baums (`tests/unit/**`, `tests/recovery/**`, `tests/security/test_security_policies.py`, `tests/integration/test_concurrency_integration.py`, `tests/integration/test_event_bus_integration.py`, `tests/integration/test_runtime_integration.py` — 22 Dateien mit `jochen_x`-Imports) | 761 Tests |
| **Regressionsbezugsgröße Milestone 1.0 (baseline-geführte Struktur, 14 Testdateien)** | **258 Tests** |
| Konsistenzprüfung | 258 + 761 = 1019 ✓ |

**Verbindliche Regressionsbasis (RB-1.0):** die 258 Tests der folgenden 14 Dateien:
`tests/test_activation_validation.py`, `tests/test_application_foundation.py`, `tests/test_capability_matrix.py`, `tests/test_core.py`, `tests/test_dependency_resolution.py`, `tests/test_developer.py`, `tests/test_foundation.py`, `tests/test_golden_reference.py`, `tests/test_manifest_v2.py`, `tests/test_navigation.py`, `tests/test_plugin_observability.py`, `tests/test_sdk.py`, `tests/test_security_foundation.py`, `tests/integration/test_plugin_integration.py`.

Die Regressionsregeln aus IP §9.6 gelten unverändert; Ziel bleibt „keine Regressionen" gegen RB-1.0 zuzüglich der in MWB-015 hinzukommenden Tests. Der stillgelegte Testbestand (761) ist **nicht** Bestandteil der Regressionsbasis; seine physische Behandlung folgt der separaten Entscheidung zu `src/jochen_x/**` (GDR-002 D-2) und wird hier nicht vorweggenommen.

---

## 3. Sprintstruktur — Übersicht

Die Sprints folgen exakt der genehmigten Phasenfolge (IP §7.3) und dem genehmigten Abhängigkeitsgraphen (IP §6.3/§6.4). Traceability: `SP-002 → IP §6.3, §7.3`.

```
Phase A          SPR-01  Baseline Confirmation
                    ↓
Phase B          SPR-02  WP-001 Platform Hardening        ┐
(parallelisierbar)SPR-03  WP-002 Host Service & Extens.    │
                 SPR-04  WP-003 Developer Experience      │ keine verbindliche
                 SPR-05  WP-004 Observability             │ Ordnung innerhalb
                 SPR-06  WP-005 Reliability               │ der Phase (IP §6.3)
                 SPR-07  WP-007 Documentation             ┘
                    ↓  (alle sechs abgeschlossen)
                 SPR-08  Phase-B-Abschluss: Regression & Messreihe (EV-I01)
                    ↓
Phase C          SPR-09  WP-006 SDK Contract Verification
                    ↓
Phase D          SPR-10  Governance Closure
```

Abhängigkeitsarten: **[T]** harte technische, **[G]** Governance-, **[D]** Daten-, **[V]** Verification-, **[E]** Evidence-Abhängigkeit.

---

## 4. Sprint-Katalog

### SPR-01 — Baseline Confirmation (Phase A)

| Feld | Inhalt |
|---|---|
| Zweck | Protokollierte Bestätigung, dass der dokumentierte Baseline-Zustand dem Ist-Zustand entspricht (`SP-010 → IP §3, §7.3 Phase A`) |
| Ausgangslage | IP R1.2 APPROVED; GDR-002 vorliegend; Preflight OPTION A; Bootstrap Baseline 1.0 APPROVED |
| Work Packages | keines — Governance-Phase ohne Umsetzungsinhalt (IP §7.3) |
| MWBs | keine |
| Abhängigkeiten | [G] Startfreigabe der Sprintplanung erteilt; [G] genehmigter Sprint Plan (dieses Dokument nach Genehmigung) |
| Deliverables (Planning) | Bestätigungsprotokoll gemäß IP §3.8: BI-01..BI-07, API-01..API-04, BP-01..BP-04, PL-01..PL-05, GI-01..GI-12 |
| Verification | Dokumentenprüfung, Vollständigkeitsabgleich (IP §8.5 EV-D01) |
| Evidence | **EV-D01** |
| Exit Criteria | Vollständige, protokollierte Bestätigung; Aufhebung des Vorbehalts aus IP §4.2. Bei Abweichung: Eskalation gemäß IP §7.6, **kein** Übergang |
| Blocker | Festgestellte Baseline-Abweichung (→ `BASELINE DEVIATION — GOVERNANCE REQUIRED`); fehlende Startfreigabe |

**Hinweis:** SPR-01 enthält kein Coding. Sein Abschluss ist Coding-Bedingung 8 (IP §10.6 Nr. 8) und Eintritt für RL-05.

---

### SPR-02 — WP-001 Platform Hardening (Phase B, Pos. 1a)

| Feld | Inhalt |
|---|---|
| Zweck | Bestimmtheit und Ablehnungsverhalten der Plattform-Zustandsübergänge (FR-001, FR-002) planmäßig herstellen (`SP-020 → IP §6.3 Pos. 1a; ES FR-001/FR-002`) |
| Ausgangslage | EV-D01 liegt vor; BI-03/BI-05 als Erhaltungsvorgaben verstanden |
| Work Packages | WP-001 |
| MWBs | MWB-001, MWB-002; MWB-015 (Testbasis-Anteil WP-001) |
| Abhängigkeiten | [G] Coding Authorization Gate (Kap. 6) bestanden; [T] keine (Provider ohne Vorgänger, IP §6.4); [E] EV-D01 |
| Deliverables (Planning) | Vorsehen: Implementierung der Lifecycle-Zustandsmaschinen-Bestimmtheit gemäß ES; Erweiterung der Testbasis gemäß MWB-015 |
| Verification | Automatisierte Testsuite, manuelle Verifikation der Zustandsmaschine (IP §8.5 EV-W01) |
| Evidence | **EV-W01**; Beitrag zu EV-I01 |
| Exit Criteria | AC-001.1..AC-002.2 = VERIFIED; keine Regression gegen RB-1.0-Anteil; QG-001-AC-Anteil prüfbar (Gate-Abschluss erst Ende Phase B, IP §8.7) |
| Blocker | AC im Status FAILED (→ IP §7.6); Baseline-Konflikt |

---

### SPR-03 — WP-002 Host Service & Extensibility (Phase B, Pos. 1b)

| Feld | Inhalt |
|---|---|
| Zweck | Host-Dienste vollständig beschreiben und abrufbar machen; Erweiterungspunkte formal definieren (FR-003, FR-004) (`SP-030 → IP §6.3 Pos. 1b`) |
| Ausgangslage | EV-D01; API-04-Änderungsschutz als Erhaltungsvorgabe |
| Work Packages | WP-002 |
| MWBs | MWB-003, MWB-004; MWB-015-Anteil |
| Abhängigkeiten | [G] Coding Gate; [T] keine; [E] EV-D01; [D] liefert Endstand für SPR-07 (optional, nicht blockierend, IP §6.4) |
| Deliverables (Planning) | Vorsehen: zentrale Host-Dienst-Beschreibung/Abrufbarkeit, formale Erweiterungspunkte gemäß ES |
| Verification | Integration Tests, ServiceRegistry-Verifikation (EV-W02) |
| Evidence | **EV-W02** |
| Exit Criteria | AC-003.1..AC-004.2 = VERIFIED; **QG-002 innerhalb WP-002 abschließbar** (IP §8.7) |
| Blocker | AC FAILED; API-Surface-Verletzung (→ BASELINE DEVIATION) |

---

### SPR-04 — WP-003 Developer Experience (Phase B, Pos. 1c)

| Feld | Inhalt |
|---|---|
| Zweck | Vorgaben für Plugin-Autoren konsolidieren; Ablehnungs-Feedback der Pipeline strukturieren (FR-005, FR-006) (`SP-040 → IP §6.3 Pos. 1c`) |
| Ausgangslage | EV-D01; PL-01..PL-05 als unveränderliche Pipeline-Reihenfolge |
| Work Packages | WP-003 |
| MWBs | MWB-005, MWB-006; MWB-015-Anteil |
| Abhängigkeiten | [G] Coding Gate; [T] keine; [V] QG-006 erst nach WP-003 **und** WP-004 (IP §8.7) |
| Deliverables (Planning) | Vorsehen: Autorenvorgaben an definierter Stelle; Ablehnungen mit Stufe und verletztem Kriterium |
| Verification | Verifikation der Rejection-Nachrichten, Dokumentationsprüfung (EV-W03) |
| Evidence | **EV-W03**; Beitrag zu EV-I02 |
| Exit Criteria | AC-005.1..AC-006.2 = VERIFIED; **QG-004 abschließbar**; QG-006-Beitrag erbracht |
| Blocker | AC FAILED; Änderung der Pipeline-Reihenfolge (verboten — Security-/Baseline-Konflikt) |

---

### SPR-05 — WP-004 Observability (Phase B, Pos. 1d)

| Feld | Inhalt |
|---|---|
| Zweck | Plugin-spezifische Diagnoseinformationen; erweiterbare Observability (FR-007, FR-008) (`SP-050 → IP §6.3 Pos. 1d`) |
| Ausgangslage | EV-D01; BI-06 als Erhaltungsvorgabe |
| Work Packages | WP-004 |
| MWBs | MWB-007, MWB-008; MWB-015-Anteil. **Hinweis:** MWB-008 enthält eine als „festzulegen" ausgewiesene Position (IP §5.3/§5.6) → OPEN TECHNICAL DECISION OTD-1 (Kap. 8) |
| Abhängigkeiten | [G] Coding Gate; [T] keine; [V] QG-006 gemeinsam mit WP-003; [D] liefert Endstand für SPR-07 (nicht blockierend) |
| Deliverables (Planning) | Vorsehen: strukturierte Diagnoseinformationen mit Pipelinestufe; Observability-Erweiterbarkeit |
| Verification | Pipeline-Verifikation, Tests (EV-W04) |
| Evidence | **EV-W04**; Beitrag zu EV-I02 |
| Exit Criteria | AC-007.1..AC-008.2 = VERIFIED; QG-006 nach WP-003+WP-004 abschließbar; EV-I02 nach Abschluss beider führbar |
| Blocker | AC FAILED; OTD-1 unentschieden, soweit die betroffene Position erreicht wird |

---

### SPR-06 — WP-005 Reliability (Phase B, Pos. 1e)

| Feld | Inhalt |
|---|---|
| Zweck | Definiertes Wiederherstellungsverhalten; Isolation von Plugin-Ausfällen (FR-009, FR-010) (`SP-060 → IP §6.3 Pos. 1e`) |
| Ausgangslage | EV-D01; BI-03, BI-04, BI-06, PL-05 als Erhaltungsvorgaben |
| Work Packages | WP-005 |
| MWBs | MWB-009, MWB-010; MWB-015-Anteil |
| Abhängigkeiten | [G] Coding Gate; [T] keine |
| Deliverables (Planning) | Vorsehen: definiertes Wiederherstellungsverhalten; isolierte Plugin-Ausfälle |
| Verification | Automatisierte Testsuite (EV-W05) |
| Evidence | **EV-W05**; Beitrag zu EV-I01 (QG-007) |
| Exit Criteria | AC-009.1..AC-010.2 = VERIFIED; QG-007-Beitrag erbracht (Gate-Abschluss erst Ende Phase B) |
| Blocker | AC FAILED |

---

### SPR-07 — WP-007 Documentation (Phase B, Pos. 1f)

| Feld | Inhalt |
|---|---|
| Zweck | SDK-Dokumentation vervollständigen; Architekturdokumentation nachführen (FR-011, FR-012) (`SP-070 → IP §6.3 Pos. 1f`) |
| Ausgangslage | EV-D01; Architecture Freeze GI-01 als unverrückbare Grenze |
| Work Packages | WP-007 |
| MWBs | MWB-011, MWB-012; MWB-015-Anteil |
| Abhängigkeiten | [G] Coding Gate (soweit Repository-Dateien betroffen); [T] keine blockierenden; [D] abschließende Fassung setzt Endstand WP-002/WP-004 voraus (optional, IP §6.4) |
| Deliverables (Planning) | Vorsehen: vollständige SDK-Dokumentation; nachgeführte Architekturdokumentation — ohne Änderung des FROZEN Architecture Book v2.0 (Nachführung nur in den dafür vorgesehenen Dokumenten; jede AB-Änderung wäre BASELINE DEVIATION) |
| Verification | Dokumentenprüfung, Vollständigkeitsabgleich (EV-W07, EV-D04) |
| Evidence | **EV-W07**, **EV-D04** |
| Exit Criteria | AC-011.1..AC-012.2 = VERIFIED; **QG-005 abschließbar**; keine Widersprüche zum implementierten Stand |
| Blocker | Endstand WP-002/WP-004 fehlt für die Schlussfassung; AC FAILED |

---

### SPR-08 — Phase-B-Abschluss: Regression & Messreihe

| Feld | Inhalt |
|---|---|
| Zweck | Vollständiger Regressionsnachweis (funktional und performancebezogen) gegen RB-1.0 zzgl. hinzugekommener Tests; Abschluss von QG-001 und QG-007 (`SP-080 → IP §8.5 EV-I01, §8.7; Anhang B.8/B.12`) |
| Ausgangslage | SPR-02 bis SPR-07 abgeschlossen (alle sechs Provider-Pakete — Teilabschluss berechtigt nicht zum Übergang, IP §7.3) |
| Work Packages | keines — Verifikationsabschluss der Phase B |
| MWBs | MWB-015 (Gesamtstand der Testbasis) |
| Abhängigkeiten | [T] alle Phase-1-WPs; [V] EV-W01..EV-W05, EV-W07 geführt; [E] Baseline-Messreihe gemäß Anhang B.2; [D] RB-1.0 (Kap. 2) |
| Deliverables (Planning) | Vorsehen: Regressionsnachweis EV-I01; Vergleichsmessreihe und Regressionsbewertung gemäß Anhang B.8 |
| Verification | Automatisierte Testsuite gegen RB-1.0 + neue Tests; Vergleichsmessreihe (IP §8.5) |
| Evidence | **EV-I01**; **EV-I02** (falls noch offen) |
| Exit Criteria | Baseline- und neue Tests bestanden; keine funktionale, keine Performance-Regression; **QG-001 und QG-007 abschließbar** (frühestmöglicher Abschluss: Ende Phase B, IP §8.7) |
| Blocker | Regression festgestellt (→ Rückkehr in betroffene Provider-Sprints); Messreihe unvollständig |

---

### SPR-09 — WP-006 SDK Contract Verification (Phase C)

| Feld | Inhalt |
|---|---|
| Zweck | Nachweis der Additivität aller Erweiterungen und der Consumer-Kompatibilität (FR-013, FR-014) (`SP-090 → IP §6.3 Pos. 2, §7.3 Phase C`) |
| Ausgangslage | Phase B vollständig abgeschlossen inkl. EV-I01; API-01..API-04 und SDK API 1.0.0 unverändert |
| Work Packages | WP-006 |
| MWBs | MWB-013, MWB-014; MWB-015-Anteil |
| Abhängigkeiten | [T] WP-001..WP-005, WP-007 (blockierend, IP §6.4); [V] EV-I01; [E] eingefrorene API-Baseline |
| Deliverables (Planning) | Vorsehen: API-Surface-Vergleich; Kompatibilitätsnachweis gegen Referenzplugin/Konsumenten |
| Verification | API-Surface-Vergleich, Kompatibilitätsprüfung, Review (EV-W06, EV-I03, EV-I04) |
| Evidence | **EV-W06**, **EV-I03**, **EV-I04** |
| Exit Criteria | AC-013.1..AC-014.2 = VERIFIED; **QG-003 abschließbar** (Ende Phase C); keine Verletzung API-01..API-04 / SDK API 1.0.0 |
| Blocker | Negativer Nachweis → Rückkehr in Phase B für betroffene Inhalte (IP §7.3), keine Fortsetzung |

---

### SPR-10 — Governance Closure (Phase D)

| Feld | Inhalt |
|---|---|
| Zweck | Formaler Milestone-Abschluss: alle Quality Gates geprüft, Definition of Done erfüllt, Milestone Review durchgeführt (`SP-100 → IP §7.3 Phase D, §8.8, §10.8`) |
| Ausgangslage | Phasen A–C abgeschlossen; QG-001..QG-007 in prüfbarem Endzustand |
| Work Packages | keines — Governance-Phase |
| MWBs | keine |
| Abhängigkeiten | [G] GV-01..GV-08 bestätigbar; [V] EV-D03 (Traceability-Audit), EV-D05; [E] EV-G01..EV-G04 |
| Deliverables (Planning) | Vorsehen: Governance-Audit, DoD-Abschlussnachweis, Milestone Review, Unverändertheitsnachweis GI-01..GI-12 |
| Verification | Governance-Audit, Dokumentenprüfung, Review (IP §8.5 VL-04) |
| Evidence | **EV-G01, EV-G02, EV-G03, EV-G04, EV-D03, EV-D05** |
| Exit Criteria | **QG-008 abschließbar**; GV-01..GV-08 bestätigt — GV-08 stützt sich auf die dokumentierte GR-001-Entscheidung (GDR-002) |
| Blocker | Offener GV-Punkt; offenes Finding ohne dokumentierte Entscheidung |

---

## 5. Quality-Gate-Zuordnung und Status

Statuswerte: NOT STARTED · IN PROGRESS · READY FOR VERIFICATION · PASSED · BLOCKED. Kein Gate wird durch Planung als PASSED markiert (`SP-110 → IP §8.7`).

| Gate | Zugeordnete Sprints | Frühestmöglicher Abschluss (IP §8.7) | Status |
|---|---|---|---|
| QG-001 Platform Stability | SPR-02, SPR-08 | Ende Phase B | **NOT STARTED** |
| QG-002 Host Service Availability | SPR-03 | Abschluss WP-002 | **NOT STARTED** |
| QG-003 Architecture Freeze Compliance | SPR-09 | Ende Phase C | **NOT STARTED** |
| QG-004 Developer Feedback Quality | SPR-04 | Abschluss WP-003 | **NOT STARTED** |
| QG-005 Traceability Completeness | SPR-07 | Abschluss WP-007 | **NOT STARTED** |
| QG-006 Pipeline Security Compliance | SPR-04 + SPR-05 | Abschluss WP-003 und WP-004 | **NOT STARTED** |
| QG-007 Test Coverage Maintenance | SPR-06, SPR-08 | Ende Phase B | **NOT STARTED** |
| QG-008 Governance Compliance | SPR-10 | Phase D | **NOT STARTED** |

Grundregel (IP §8.7, ausnahmslos): Kein Gate wird geschlossen, solange abhängige Work Packages offen sind.

Alle 29 Acceptance Criteria: Ausgangsstatus **NOT VERIFIED** (IP §8.6 — planmäßiger Zustand, kein Defizit).

---

## 6. Coding Authorization Gate

> **Sprint Planning abgeschlossen ≠ Coding freigegeben.**

Coding darf erst beginnen, wenn sämtliche Bedingungen des Implementation Plans erfüllt sind (`SP-120 → IP §10.6 Nr. 7–9, §10.5 RL-05`):

| # | Bedingung | Status |
|---|---|---|
| 7 | Genehmigte Sprintplanung liegt vor | **PENDING** — dieser Plan ist DRAFT; Genehmigung durch Projekteigner ausstehend |
| 8 | Baseline-Bestätigung gemäß IP §3.8 protokolliert (Phase A / SPR-01 abgeschlossen) | **PENDING** |
| 9 | RL-05 erreicht | **PENDING** — setzt Nr. 7 und Nr. 8 voraus |

Zusätzlich wirken die acht Ausschlussgründe aus IP §10.6 unabhängig voneinander. Der Preflight (2026-08-09) bestätigt ausdrücklich, dass diese Bedingungen aktuell **nicht** erfüllt sind. Kein Sprint dieses Plans beginnt mit Umsetzungsarbeit vor Bestehen dieses Gates.

---

## 7. Completion Conditions (übernommen, nicht neu definiert)

`SP-130 → IP §8.9, §9.8, §10.8`

| Bedingung | Quelle | Status |
|---|---|---|
| Verification Completion (u. a. Baseline-Invarianten berücksichtigt) | IP §8.9 | PENDING — phasengebunden |
| Test Completion Bedingung 5 (vollständige Regression geplant) | IP §9.8 | Planung erfüllt; Bezugsgröße festgestellt (Kap. 2); Nachweis folgt in SPR-08 |
| GV-01..GV-08 | IP §8.8 | PENDING — Phase D (GR-001-Anteil von GV-08 durch GDR-002 erledigt) |
| Completion Conditions Kap. 10.8 | IP §10.8 | PENDING — Milestone-Abschluss |

---

## 8. Offene Punkte (Register)

| ID | Kat. | Beschreibung | Quelle | Status | Blockiert Sprint? | Benötigte Entscheidung |
|---|---|---|---|---|---|---|
| OP-1 | GOVERNANCE | Genehmigung dieses Sprint Plans (Coding-Bedingung 7) | IP §10.6 | OFFEN | JA — Start SPR-01-Folgearbeit/Coding | Projekteigner-Genehmigung |
| OP-2 | GOVERNANCE | Coding Authorization (Bedingungen 8–9, RL-05) | IP §10.5/§10.6; Preflight | OFFEN | JA — Umsetzungsbeginn SPR-02+ | Phase-A-Protokoll + RL-05-Feststellung |
| OP-3 | BASELINE | Physische Behandlung `src/jochen_x/**` (stillgelegt) | GDR-002 D-2 | OFFEN | NEIN | Separater Projekteigner-Auftrag |
| OTD-1 | TECHNICAL | „Neu — festzulegen"-Position in MWB-008 (Observability) | IP §5.3, §5.6 | OPEN TECHNICAL DECISION | NEIN für Planung; JA für betroffenen Teil von SPR-05 | Festlegung im vorgesehenen Rahmen der Umsetzung, quellenkonform |
| OTD-2 | TECHNICAL | „Neu — festzulegen"-Position in MWB-015 (Testbasis-Erweiterung) | IP §5.3, §5.6 | OPEN TECHNICAL DECISION | NEIN | Festlegung mit MWB-015-Umsetzung |
| OP-4 | VERIFICATION | R2-E-01 (Editorial Finding des Plans) | IP §10.7 | OFFEN | NEIN | Späterer redaktioneller Schritt |
| OP-5 | GOVERNANCE | Formaler Schließungsakt WAIVER-DEV-001 | W-5 §6 | OFFEN | NEIN | Vorgesehener Governance-Schritt |
| OP-6 | SECURITY | SD-W1-F-04, SD-W1-F-06 (Security Design R1) | ADW-SD-1.0-002 | OFFEN | NEIN | Freigabe Correction Cycle |
| OP-7 | SECURITY | SA-W1-F01/F03/F04; ODD-01–ODD-20; GF-02/GF-03; GC-02–GC-07; GQ-1–GQ-3 | Assessment 2026-08-09 | OFFEN | NEIN | Separate Governance-Schritte |
| OP-8 | EVIDENCE | Baseline-Messreihe (Anhang B.2) als Voraussetzung der Performance-Regressionsbewertung | IP Anhang B | OFFEN | NEIN für Planung; Voraussetzung für SPR-08 | Erhebung zu Beginn der Umsetzung gemäß Anhang B |

Kein offener Punkt wird durch diesen Plan geschlossen. Keine `PLANNING-FINDING`s aus dem Source Gate (alle Primärquellen vorhanden und widerspruchsfrei).

---

## 9. Sicherheits- und Bestandsgarantien dieses Plans

- Security-Randbedingungen werden ausschließlich als genehmigte Vorgaben übernommen (CP 1.0, SA 1.0, SD 1.0 — APPROVED/CLOSED); keine Security-Entscheidung wurde getroffen, kein Security-Artefakt verändert, kein Finding/ODD geschlossen.
- Scope, Requirements, Architektur, Engineering Specification, Governance Rules: unverändert übernommen aus IP R1.2; keine neuen Features, keine neuen Datenflüsse, keine neuen Agentenfähigkeiten, keine Trading-Funktionalität.
- Bootstrap Baseline respektiert; keine stillgelegte Struktur reaktiviert; jede erforderlich erscheinende Abweichung wäre `BASELINE DEVIATION — GOVERNANCE REQUIRED` mit STOP.

---

**Ende JOCHEN X — Milestone 1.0 Sprint Plan (DRAFT, 1.0 R0)**
