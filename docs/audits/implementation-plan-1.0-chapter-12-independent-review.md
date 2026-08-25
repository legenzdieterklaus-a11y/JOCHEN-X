# Implementation Plan 1.0 — Independent Chapter Review Kapitel 12 (Migration Strategy)

| Feld | Wert |
|---|---|
| Auditgegenstand | Milestone 1.0 Implementation Plan, Kapitel 12 — Migration Strategy (PS-04) |
| Pfad | `docs/milestone-1.0-implementation-plan.md` |
| Dokumentstatus | DRAFT |
| Auditart | Independent Chapter Review |
| Auditumfang | Ausschließlich Kapitel 12. Kapitel 1–11 und Anhänge nur als Referenz. |
| Datum | 2026-08-03 |
| Autorität | Governance Architect |
| Vorgängerprüfungen | Consistency Audit Kapitel 9; Independent Chapter Reviews Kapitel 10 und 11 |

---

## 1. Prüfumfang

### 1.1 Scope-Prüfung

| Prüfpunkt | Ergebnis |
|---|---|
| Kapitel behandelt ausschließlich Engineering Migration Planning | Bestätigt |
| Keine Implementierung, kein Coding | Bestätigt |
| Kein Deployment, kein Release | Bestätigt — MC-10; 12.4 Ausschlusstabelle |
| Kein Runtime-Verhalten | Bestätigt — MR-Regel 3 stellt ausdrücklich klar, dass Readiness kein Runtime-Zustand ist |
| Keine Betriebsmigration | Bestätigt |
| Keine Datenmigration | Bestätigt — ausdrücklich ausgeschlossen mit Begründung |
| Keine Kundenmigration | Bestätigt |
| Keine Infrastrukturmigration | Bestätigt |
| Charakter als normatives Framework, nicht als technischer Leitfaden | Bestätigt — kein Verfahrensschritt beschreibt eine Ausführungshandlung |
| Beantwortung der Leitfrage | Bestätigt — Bedingungen und Ordnung der Überführung sind geregelt, nicht deren technische Ausführung |

### 1.2 Strukturprüfung

| Abschnitt | Vorhanden | Bewertung |
|---|---|---|
| 12.1 Purpose | Ja | Zweck, Abgrenzung und zehn Bezugsverhältnisse |
| 12.2 Migration Objectives | Ja | MO-01..MO-08; vollständig abgeleitet |
| 12.3 Migration Principles | Ja | MP-01..MP-10 mit Konfliktregel |
| 12.4 Migration Scope | Ja | Gegenstand und Ausschlüsse je mit Grundlage |
| 12.5 Migration Units | Ja | MU-01..MU-07 mit begründeter Bildungsregel |
| 12.6 Migration Unit States | Ja | **Ergänzung** — begründet |
| 12.7 Migration Sequence | Ja | MS-01..MS-04 mit Ein-/Austrittsbedingungen, Abhängigkeiten, Nachweisen, vier Sequenzregeln |
| 12.8 Reversibility & Rollback Preparedness | Ja | **Ergänzung** — begründet |
| 12.9 Migration Risk Mapping | Ja | **Ergänzung** — begründet; erfüllt die Pflichtaufgaben |
| 12.10 Migration Constraints | Ja | MC-01..MC-12 |
| 12.11 Migration Traceability | Ja | Kette und vollständige Zuordnung je Einheit |
| 12.12 Migration Readiness | Ja | MR-01..MR-07 mit vier Regeln |
| 12.13 Migration Completion | Ja | MCC-01..MCC-14 mit Soll, Ist, Evidence, Review, Owner |
| 12.14 Interfaces to Rollout | Ja | Übergabegegenstände und vier Regeln |
| 12.15 Final Migration Statement | Ja | Acht Bedingungen, Abgrenzung, Stichtagsfeststellung |

#### Bewertung der drei Strukturergänzungen

| Ergänzung | Normativ erforderlich | Neue Anforderung | Neue Governance-Ebene | Neue Evidence | Neue Architektur | Bewertung |
|---|---|---|---|---|---|---|
| 12.6 Migration Unit States | Ja — MR- und MCC-Bedingungen sind ohne Zustandsraum nicht eindeutig prüfbar | Nein | Nein — Zustandslogik folgt dem Muster aus Kapitel 11.6 | Nein | Nein | Zulässig |
| 12.8 Reversibility & Rollback Preparedness | Ja — MP-08 ist ohne Regelwerk nicht prüfbar | Nein | Nein | Nein | Nein | Zulässig |
| 12.9 Migration Risk Mapping | Ja — Erfüllung der Pflichtaufgaben 1 und 2 | Nein | Nein — reine Anwendung des Frameworks aus Kapitel 11 | Nein — Verweise ausschließlich auf Kapitel 8.5 | Nein | Zulässig |

### 1.3 Formale Prüfung

| Prüfpunkt | Ergebnis |
|---|---|
| Nummerierung 12.1 bis 12.15 | Lückenlos, keine Dubletten |
| ID-Räume MO, MP, MU, MS, MC, MR, MCC, MGR | Eindeutig; keine Kollision mit den ID-Räumen der Kapitel 1–11 und der Anhänge |
| Abgrenzung MC gegen GC, SQ, ST, VC, TCN, ACN, RC | Keine Kollision; MC ist neu vergeben |
| Referenzen auf Kapitel 3 bis 11 | Aufgelöst |
| Referenzen auf Anhang B | Aufgelöst |
| Referenz auf Kapitel 13 | Als Schnittstellenzusage geführt |
| Circular References | Keine |

### 1.4 Prüfung der Migrationseinheiten

| Prüfpunkt | Ergebnis |
|---|---|
| Ableitung ausschließlich aus Work Packages, Module Work Breakdown und Delta Analysis | Bestätigt |
| Anzahl der Einheiten | 7 — deckungsgleich mit WP-001 bis WP-007 |
| Neue Module oder Planungsentitäten | Keine |
| Vollständigkeit der Deltazuordnung | DA-001 bis DA-014 sind je genau einer Einheit zugeordnet; DA-015 ist als querschnittlich ausgewiesen und begründet |
| Kategorienübernahme Provider/Dependent | Unverändert aus Kapitel 6.4 |
| Begründung der Eins-zu-eins-Bildung | Vorhanden und tragfähig — feinere Zerlegung schüfe neue Entitäten, gröbere hübe MO-03 auf |

### 1.5 Prüfung der Migrationssequenz

| Prüfpunkt | Ergebnis |
|---|---|
| Abbildung der genehmigten Reihenfolge aus Kapitel 6 | Bestätigt — MS-02 entspricht Phase 1, MS-03 entspricht Phase 2 |
| Abbildung der Phasenordnung aus Kapitel 7.3 | Bestätigt — MS-01 entspricht Phase A, MS-04 entspricht dem Übergang in Phase D |
| Eintritts- und Austrittsbedingungen je Schritt | Vollständig |
| Abhängigkeiten je Schritt | Vollständig; der nicht blockierende Bezug von MU-07 zu MU-02 und MU-04 ist unverändert übernommen |
| Nachweiszuordnung je Schritt | Vollständig; sämtliche Evidence-IDs existieren in Kapitel 8.5 |
| Teilabschluss-Verbot | Bestätigt — Sequenzregel 3 entspricht Kapitel 6.5 |
| Sprintzuordnung oder Termine | Keine |
| Abweichung von der genehmigten Reihenfolge | Keine |

### 1.6 Prüfung des Risk Mappings

| Prüfpunkt | Ergebnis |
|---|---|
| Übernahme der Klasse RK-10 ohne eigene Klassifikation | Bestätigt |
| Anwendung der Bewertungsregeln aus Kapitel 11.7 | Bestätigt |
| Anwendung des Lifecycle aus Kapitel 11.6 | Bestätigt — sämtliche Einträge im Zustand MITIGATED |
| Anwendung der Ownership-Regeln aus Kapitel 11.5 | Bestätigt — MGR-001 und MGR-002 bei der Umsetzungsverantwortung, MGR-003 beim Governance Architect entsprechend der Klassenzuordnung |
| Neubewertung bestehender Risiken | Keine — die zehn Bestandseinträge sind unverändert |
| Registerführung nach Registerregel 3 (fortlaufende Kennung, Quellenangabe) | Bestätigt |
| Doppelführung gegenüber Bestandsrisiken | Geprüft — die Abgrenzungstabelle in 12.9 weist die Unterscheidung zu R-002, R-003 und R-005 nach; keine Überschneidung festgestellt |
| Kritikalität nach Matrix aus Kapitel 11.7 | Nachgerechnet: MGR-001 Niedrig/Hoch → Erhöht; MGR-002 Niedrig/Hoch → Erhöht; MGR-003 Niedrig/Kritisch → Hoch. Sämtlich übereinstimmend. |
| Registerstand | 10 + 3 = 13; Angabe im Kapitel übereinstimmend |

### 1.7 Traceability-Prüfung

| Prüfpunkt | Soll | Ist | Ergebnis |
|---|---|---|---|
| Migrationseinheiten mit Work-Package-Zuordnung | 7 | 7 | Vollständig |
| Migrationseinheiten mit Acceptance-Criteria-Zuordnung | 7 | 7 | Vollständig |
| Acceptance Criteria über Einheiten abgedeckt | 29 | 29 | Vollständig |
| Quality Gates über Einheiten abgedeckt | 8 | 8 | Vollständig |
| Migrationseinheiten mit Evidence-Zuordnung | 7 | 7 | Vollständig |
| Migrationseinheiten mit Completion-Bedingung | 7 | 7 | Vollständig |
| Neue Traceability-Ebene | 0 | 0 | Erfüllt — die Einheit ist deckungsgleich mit dem Work Package |

### 1.8 Prüfung auf unzulässige Einführungen

| Verbotene Einführung | Ergebnis |
|---|---|
| Neue Functional oder Non-Functional Requirements | Keine |
| Neue Acceptance Criteria | Keine |
| Neue Quality Gates | Keine |
| Neue Governance-Ebenen | Keine |
| Neue Evidence-Artefakte | Keine — MC-08; sämtliche Verweise zeigen auf Kapitel 8.5 |
| Neue Module oder Planungsentitäten | Keine — MC-06 |
| Neue Architektur | Keine — MP-04, MC-02 |
| Neue Risikoklassifikation | Keine — ausschließlich RK-10 |

### 1.9 Prüfung der Rollout-Schnittstellen

| Prüfpunkt | Ergebnis |
|---|---|
| Übergabegegenstände bestimmt | Ja — Migrationsergebnis, Nachweislage, Risikolage, offene Vorbehalte |
| Vorwegnahme von Rollout-Regeln | Keine |
| Verbot eigener Migrationseinheiten in Kapitel 13 | Ja |
| Trennung RK-10 und RK-11 | Ja — Umwidmung ausdrücklich untersagt |
| Ausschluss eines Rollouts auf Zwischenzustand | Ja |

### 1.10 Konsistenzprüfung gegen Kapitel 11

| Prüfpunkt | Ergebnis |
|---|---|
| Klassifikation | Konsistent — ausschließlich RK-10 verwendet |
| Bewertungsmodell | Konsistent — ordinale Skalen und Matrix unverändert angewandt |
| Lifecycle und Zustände | Konsistent — Risikozustände aus Kapitel 11.6 verwendet; die Zustände in 12.6 betreffen Migrationseinheiten, nicht Risiken, und sind sprachlich unterscheidbar |
| Ownership | Konsistent |
| Registerführung | Konsistent nach Korrektur — siehe F12-001 |
| Schnittstellenzusage aus Kapitel 11.13 | Erfüllt — Klassen, Bewertungs-, Lifecycle- und Ownership-Regeln übernommen; kein eigenes Modell gebildet |

---

## 2. Befunde

### F12-001

| Feld | Inhalt |
|---|---|
| **ID** | F12-001 |
| **Severity** | Medium |
| **Kapitel** | 12.9; 11.11; 11.13 |
| **Beschreibung** | Kapitel 12.9 schreibt das konsolidierte Register auf 13 Einträge fort und befüllt Klasse RK-10. Kapitel 11.11 wies weiterhin 10 Einträge aus, Kapitel 11.13 Regel 2 erklärte RK-10 als leer. Zwei Kapitel trafen damit widersprüchliche Aussagen über denselben Registerstand. |
| **Empfehlung** | Fortschreibungsmechanik in Kapitel 11 verankern und die Aussage zur Leere der Klasse RK-10 richtigstellen. |
| **Status** | **CLOSED** — Kapitel 11.11 um Registerregel 5 ergänzt: Fortschreibungen durch nachfolgende Kapitel gelten als Bestandteil des Registers; aktueller Stand 13 Einträge. Kapitel 11.13 Regel 2 richtiggestellt: RK-10 befüllt, RK-11 bis Kapitel 13 offen. Beide Kapitel treffen nun übereinstimmende Aussagen. |

### F12-002

| Feld | Inhalt |
|---|---|
| **ID** | F12-002 |
| **Severity** | Low |
| **Kapitel** | 12.6; 11.6 |
| **Beschreibung** | Kapitel 12.6 und Kapitel 11.6 führen beide einen Zustandsraum. Bei flüchtiger Lesart könnten Migrationseinheiten- und Risikozustände verwechselt werden. |
| **Empfehlung** | Unterscheidbarkeit sicherstellen. |
| **Status** | **CLOSED** — Die Zustandsmengen sind disjunkt: Risiken tragen OPEN, MITIGATED, ACCEPTED, CLOSED, PENDING DECISION; Migrationseinheiten tragen BASELINE, READY, IN TRANSITION, VERIFIED, MIGRATED, REVERTED. Keine Bezeichnung ist doppelt vergeben. Keine Korrektur erforderlich. |

### F12-003

| Feld | Inhalt |
|---|---|
| **ID** | F12-003 |
| **Severity** | Low |
| **Kapitel** | 12.5 |
| **Beschreibung** | DA-015 bildet keine eigene Migrationseinheit. Ein Reviewer könnte dies als unvollständige Deltazuordnung werten. |
| **Empfehlung** | Begründung im Kapitel halten. |
| **Status** | **CLOSED** — Die Behandlung ist ausgewiesen und begründet: DA-015 ist keinem einzelnen Work Package zugeordnet (Kapitel 4.5, 5.4) und wird als Nachweisbestandteil jeder Einheit sowie über die Regressionsprüfung geführt. Die Zuordnung ist konsistent mit MWB-015. |

### F12-004

| Feld | Inhalt |
|---|---|
| **ID** | F12-004 |
| **Severity** | Medium |
| **Kapitel** | 12.4; 12.10 MC-11 |
| **Beschreibung** | Der parallele Artefaktbaum ist von der Migration ausgeschlossen, solange GR-001 den Status PENDING DECISION trägt. Fällt die Entscheidung zu seinen Gunsten, sind Migrationsumfang und Einheitenzuordnung erneut zu führen. |
| **Empfehlung** | Abhängigkeit ausweisen und der Entscheidung zu GR-001 zuordnen. |
| **Status** | **OPEN** — Für Kapitel 12 **nicht blockierend**: Der Ausschluss ist normativ geregelt (MC-11) und die Abhängigkeit ist in 12.4 und 12.14 ausgewiesen. Der Befund ist Ausprägung des planweiten Befunds GP-004 und entfällt mit der Entscheidung zu GR-001. |

### F12-005

| Feld | Inhalt |
|---|---|
| **ID** | F12-005 |
| **Severity** | Editorial |
| **Kapitel** | 12.13, MCC-13 und MCC-14 |
| **Beschreibung** | Zwei Completion Conditions sind Selbstauskünfte des Kapitels. |
| **Empfehlung** | Extern prüfen. |
| **Status** | **CLOSED** — Extern geprüft in den Abschnitten 1.6 und 1.8 dieses Berichts. MCC-13 ohne Befund; MCC-14 durch Auszählung der zehn Bestandseinträge bestätigt. |

---

## 3. Befundübersicht

| ID | Severity | Abschnitt | Status | Blockierend für Kapitel 12 |
|---|---|---|---|---|
| F12-001 | Medium | 12.9, 11.11, 11.13 | CLOSED | Nein |
| F12-002 | Low | 12.6 | CLOSED | Nein |
| F12-003 | Low | 12.5 | CLOSED | Nein |
| F12-004 | Medium | 12.4, 12.10 | **OPEN** | Nein |
| F12-005 | Editorial | 12.13 | CLOSED | Nein |

| Severity | Gesamt | Offen | Geschlossen |
|---|---|---|---|
| Critical | 0 | 0 | 0 |
| High | 0 | 0 | 0 |
| Medium | 2 | 1 | 1 |
| Low | 2 | 0 | 2 |
| Editorial | 1 | 0 | 1 |
| **Summe** | **5** | **1** | **4** |

---

## 4. Wirkung auf planweite Befunde

| Planweiter Befund | Wirkung von Kapitel 12 |
|---|---|
| GP-001 — Planungsscope unvollständig | **Weiter reduziert.** PS-04 ist behandelt. Von den drei ursprünglich offenen Planungsgegenständen verbleibt ausschließlich PS-05 (Rollout). |
| GP-002 — Nicht auflösbare Vorwärtsverweise | Weiter reduziert. Der Verweis aus Kapitel 7.1 auf ein Migrationskapitel ist aufgelöst. Offen bleiben die Verweise aus Kapitel 5.8 und 7.1 auf ein Rolloutkapitel. |
| GP-003 — Risiken der Engineering Specification nicht überführt | Bleibt CLOSED. |
| GP-004 — GR-001 offen | Unverändert; zusätzlich als F12-004 auf den Migrationsumfang wirkend. |
| GP-005 — Selbsterklärte Schließungen nicht extern bestätigt | Unverändert; betrifft nunmehr auch MCC-01 bis MCC-14. |
| F11-004 — RK-10 und RK-11 ohne Eintrag | **Teilweise geschlossen.** RK-10 ist befüllt. RK-11 bleibt bis Kapitel 13 offen. |

### Stand des planweiten Befunds GP-001

| Planungsgegenstand | Status |
|---|---|
| PS-01 Reihenfolge | Behandelt (Kapitel 6) |
| PS-02 Abhängigkeiten | Behandelt (Kapitel 6) |
| PS-03 Verifikation | Behandelt (Kapitel 8, 9) |
| PS-04 Migration | **Behandelt (Kapitel 12)** |
| PS-05 Rollout | **Offen** |
| PS-06 Risiken | Behandelt (Kapitel 11) |

GP-001 bleibt offen und blockierend, ausschließlich wegen PS-05.

---

## 5. Chapter 12 Governance Status

```
Chapter 12 Governance Status

OPEN:
1 Finding
  F12-004 (Medium) — Migrationsumfang abhaengig von der ausstehenden
                     Entscheidung zu GR-001

CLOSED:
4 Findings
  F12-001 (Medium), F12-002 (Low), F12-003 (Low), F12-005 (Editorial)

BLOCKING:
  Fuer Kapitel 12: keine.

NON BLOCKING:
  F12-001, F12-002, F12-003, F12-005 — geschlossen.
  F12-004 ist fuer Kapitel 12 nicht blockierend, da der Ausschluss des
  betroffenen Artefaktbereichs normativ geregelt ist (MC-11) und die
  Abhaengigkeit ausgewiesen wird. Der Befund entfaellt mit der
  Entscheidung zu GR-001.

Recommendation:

APPROVED WITH FINDINGS
```

---

## 6. Auflagen

| # | Auflage | Adressat | Frist |
|---|---|---|---|
| 1 | Erstellung des Kapitels zu PS-05 (Rollout) zur Schließung von GP-001 | Lead Implementation Planner | Vor W-2 |
| 2 | Befüllung der Klasse RK-11 und Fortschreibung des konsolidierten Registers | Lead Implementation Planner | Mit Kapitel 13 |
| 3 | Erneute Führung von Migrationsumfang und Einheitenzuordnung, falls die Entscheidung zu GR-001 den parallelen Artefaktbaum einbezieht | Governance Architect | Mit der Entscheidung zu GR-001 |
| 4 | Bestätigung von MCC-01 bis MCC-14 durch den Independent Review des Gesamtplans | Independent Review | Mit W-3 |

---

## 7. Vorgenommene Korrekturen

| Korrektur | Ort | Art |
|---|---|---|
| Ergänzung der Registerregel 5 zur Fortschreibung durch nachfolgende Kapitel; Ausweis des aktuellen Standes von 13 Einträgen | 11.11 | Schließung von F12-001 |
| Richtigstellung der Aussage zur Leere der Klassen RK-10 und RK-11 | 11.13, Regel 2 | Schließung von F12-001 |

Keine Umstrukturierung der Kapitel 1 bis 12. Beide Korrekturen sind
Ergänzungen beziehungsweise Richtigstellungen innerhalb bestehender Tabellen.

---

## 8. Referenzen

- Implementation Plan 1.0: `docs/milestone-1.0-implementation-plan.md`
- Independent Chapter Review Kapitel 11: `docs/audits/implementation-plan-1.0-chapter-11-independent-review.md`
- Independent Chapter Review Kapitel 10 und Gesamtbewertung: `docs/audits/implementation-plan-1.0-chapter-10-independent-review.md`
- Consistency Audit Kapitel 9: `docs/audits/implementation-plan-1.0-chapter-9-consistency-audit.md`
- Engineering Specification 1.0: `docs/milestone-1.0-engineering-spec.md`
- WAIVER-DEV-001: `docs/governance/waiver-dev-001.md`
- Bootstrap Baseline 1.0: `docs/baselines/bootstrap-baseline-1.0.md`
- Development Standard v1.1: `docs/development-standard-v1.1.md`
- Architecture Book v2.0: `docs/architecture-book-v2.md`
