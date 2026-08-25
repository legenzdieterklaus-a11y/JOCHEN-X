# WAIVER AMENDMENT 001

## Präzisierung der Closing Criteria von WAIVER-DEV-001

---

## 1. Metadata

| Eigenschaft | Wert |
|---|---|
| **Amendment ID** | WAIVER-AMENDMENT-001 |
| **Zugehöriger Waiver** | [WAIVER-DEV-001](waiver-dev-001.md) (APPROVED, 2026-08-02) |
| **Dokumenttyp** | Waiver Amendment — normative Präzisierung |
| **Version** | 1.0 |
| **Datum** | 2026-08-05 |
| **Status** | **APPROVED** |
| **Autorität** | Governance Architect / Release Authority |
| **Auslöser** | GDR-001 — Governance Decision Record; Finding H-01 aus dem Global Consistency Audit |
| **Angenommene Option** | **Option B — Waiver Amendment** (GDR-001 §3) |
| **Geltungsbereich (Scope)** | Ausschließlich Milestone 1.0. Präzisiert werden ausschließlich die Closing Criteria §9 (1) und §9 (2) von WAIVER-DEV-001 sowie deren Inkorporation über §3.1 (4) und §3.1 (5). Kein anderer Abschnitt des Waivers wird berührt. |
| **Präzedenzwirkung** | **Keine.** Analog WAIVER-DEV-001 §3.2 gilt dieses Amendment ausschließlich für Milestone 1.0 und begründet keinen Präzedenzfall für spätere Milestones. |
| **Verhältnis zum Parent-Dokument** | WAIVER-DEV-001 bleibt **textlich unverändert**. Dieses Amendment ist ein normativer Zusatz und wird gemeinsam mit dem Waiver gelesen. Bei Auslegungsfragen zu §9 (1) und §9 (2) ist dieses Amendment maßgeblich. |

---

## 2. Referenzen

| ID | Dokument | Status | Rolle in diesem Amendment |
|---|---|---|---|
| REF-01 | [WAIVER-DEV-001](waiver-dev-001.md) | APPROVED (2026-08-02) | Parent-Dokument; Gegenstand der Präzisierung (§3.1, §9) |
| REF-02 | [Development Standard v1.1](../development-standard-v1.1.md) | APPROVED | §6.2 #4 und #5; über WAIVER-DEV-001 §3.1 inkorporiert. **Unverändert.** |
| REF-03 | [Engineering Specification 1.0](../milestone-1.0-engineering-spec.md), Revision R1 | APPROVED (2026-08-03) | Implementation Contract. **Unverändert.** |
| REF-04 | [Implementation Plan 1.0](../milestone-1.0-implementation-plan.md), Revision R1 | DRAFT | Adressat der Closing Criteria. **Unverändert.** |
| REF-05 | [GDR-001](gdr-001-waiver-closing-criteria.md) | Entschieden durch dieses Amendment | Entscheidungsvorlage mit vier bewerteten Optionen |
| REF-06 | [Global Consistency Audit R2](../audits/implementation-plan-1.0-global-consistency-audit-r2.md) | Abgeschlossen (2026-08-05) | Quelle des Findings H-01 |
| REF-07 | [Milestone 1.0 Charter](../milestone-1.0-charter.md) | APPROVED (2026-08-02) | §8 — zweistufiger Governance-Prozess. **Unverändert.** |
| REF-08 | [Correction Report R1](../audits/implementation-plan-1.0-correction-report-r1.md) | Abgeschlossen (2026-08-05) | Nachweis, dass H-01 im Correction Cycle bewusst nicht durch Textkorrektur behandelt wurde |

---

## 3. Problem Statement

Der Sachverhalt ist ausschließlich ein **Governance-Konflikt zwischen zwei
genehmigten Artefakten**. Er ist kein technisches Engineering-Finding und
betrifft keine Anforderung, kein Kriterium und kein Quality Gate.

### 3.1 Der Konflikt

WAIVER-DEV-001 weist die Pflichtabschnitte Delta Analysis und Module Work
Breakdown dem Implementation Plan zu (§3.1) und bindet den Waiver-Abschluss an
Closing Criteria (§9), die Detailmerkmale aus Development Standard v1.1 §6.2
#4 und #5 übernehmen — Merkmale, die dort für eine **Engineering
Specification** formuliert sind.

Gleichzeitig begrenzt der Milestone 1.0 Charter (§8) in Verbindung mit der
Autorisierungsgrenze des Implementation Plans dessen zulässigen Inhalt: Der
Plan ist ein Planungsartefakt; Produktionscode, Sprint Implementation und
Feature Development sind ausdrücklich nicht autorisiert.

Daraus folgt der Konflikt:

> Die Closing Criteria verlangen vom Implementation Plan Inhalte, deren
> Erzeugung dem Implementation Plan durch dieselbe Governance-Kette untersagt
> ist.

### 3.2 Ursache

Die Verschiebung der Pflichtabschnitte durch den Waiver hat den geforderten
Detailgrad unverändert mitgeführt. Der Detailgrad war jedoch auf die
Autorisierungslage einer Engineering Specification zugeschnitten, nicht auf die
eines Implementation Plans. Der Konflikt ist damit **strukturell**, nicht
redaktionell, und nicht durch Auslegung im Plan selbst auflösbar.

### 3.3 Warum der Implementation Plan den Konflikt nicht auflösen durfte

| Regel | Wirkung |
|---|---|
| Implementation Plan §1.5 | Verpflichtet bei Verletzung einer Governance Constraint zur Unterbrechung und Eskalation |
| Planungsprinzip PP-04 (Governance First) | Untersagt die Auflösung erkannter Governance-Konflikte im Plan |
| Constraint ACN-09 | Untersagt die Absenkung bestehender Bedingungen zur Herstellung der Genehmigungsfähigkeit |

Der Plan hat den Konflikt daher ausgewiesen und über GDR-001 der
Entscheidungsinstanz vorgelegt. Dieses Verhalten war korrekt und wird hiermit
bestätigt.

---

## 4. Decision

**Option B gemäß GDR-001 §3 wird angenommen.**

Die Closing Criteria §9 (1) und §9 (2) von WAIVER-DEV-001 werden für
Milestone 1.0 verbindlich präzisiert.

### 4.1 Verbindliche Auslegung des Begriffs „Dateireferenz"

Eine **Dateireferenz** im Sinne von WAIVER-DEV-001 §9 (1) und §9 (4) besteht
aus vier Bestandteilen. Alle vier sind erforderlich; weitere sind es nicht.

| # | Bestandteil | Verbindliche Bedeutung |
|---|---|---|
| 1 | **Datei** | Eindeutige Bezeichnung des betroffenen Artefakts als Pfad relativ zur Repository-Wurzel. |
| 2 | **Änderungsbereich** | Bestimmung des betroffenen Bereichs: Modul beziehungsweise Paket, Änderungsart, Änderungsstatus und Änderungsbeziehung. Ein Zeilenanker ist zu führen, **soweit** ein stabiler, verifizierter Anker vorliegt; wo der Änderungsort erst durch die autorisierte Umsetzung bestimmt wird, ist er nicht zu führen. |
| 3 | **Traceability** | Rückführung des Artefakts auf das zugeordnete Delta, das Work Package und das genehmigte Element der Engineering Specification. |
| 4 | **Nachweis** | Zuordnung des Artefakts zu dem Nachweis beziehungsweise Quality Gate, über den seine Veränderung oder Unverändertheit belegt wird. |

### 4.2 Ausdrücklich nicht erforderlich im Implementation Plan

Die folgenden Inhalte sind **kein** Bestandteil der Closing Criteria und für
deren Erfüllung **nicht** erforderlich:

| # | Nicht erforderlich | Begründung |
|---|---|---|
| 1 | Klassenimplementierungen | Umsetzungsentscheidung; nicht autorisiert vor der Implementierungsphase |
| 2 | Methodenimplementierungen | Wie vorstehend |
| 3 | **Codebeispiele** | Wie vorstehend; zudem für noch nicht bestimmte Artefakte nicht ohne Erfindung darstellbar |
| 4 | Produktionscode | Ausdrücklich nicht autorisiert (Charter §8; Implementation Plan §1.6) |
| 5 | Sprint-Artefakte | Der Sprint Planning Phase zugewiesen (Charter §8, Schritt 6) |

### 4.3 Zuweisung der ausgenommenen Inhalte

**Codebeispiele und implementierungsnahe Änderungsbeschreibungen gehören
ausschließlich in die autorisierte Implementierungsphase.** Sie entstehen dort,
wo sie autorisiert sind — nach genehmigter Sprintplanung — und werden über die
dafür vorgesehenen Deliverables der Engineering Specification geführt.

Die Anforderung entfällt damit **nicht**; sie wird an den Ort verlegt, an dem
sie erfüllbar ist. Eine Absenkung des Qualitätsanspruchs findet nicht statt.

### 4.4 Wirkung auf die einzelnen Closing Criteria

| # | Closing Criterion | Wirkung dieses Amendments | Erfüllungsstand |
|---|---|---|---|
| §9 (1) | Vollständige Delta Analysis mit Dateireferenzen | Der Begriff „Dateireferenz" ist gemäß 4.1 auszulegen. Das Merkmal „Zeile" ist als Bestandteil des Änderungsbereichs zu führen, soweit ein stabiler Anker vorliegt. | **Erfüllt** durch Implementation Plan Kapitel 4 in Verbindung mit 5.5.2 und 5.5.3 |
| §9 (2) | Vollständiges Module Work Breakdown je Work Package | Dateibasierte Änderungsbeschreibungen sind auf Ebene von Änderungsart, Änderungsstatus und Änderungsbeziehung zu führen. Codebeispiele sind gemäß 4.2 und 4.3 nicht erforderlich. | **Erfüllt** durch Implementation Plan Kapitel 5.3, 5.4 und 5.5.2 |
| §9 (3) | Bestätigung der Vollständigkeit durch den Independent Review | **Unverändert.** Dieses Amendment nimmt die Bestätigung nicht vorweg und ersetzt sie nicht. | **Ausstehend** — zu erbringen in Workflow-Schritt W-3 |
| §9 (4) | Scope Verification mit Dateireferenzen | Auslegung gemäß 4.1. | **Erfüllt** durch Implementation Plan 5.5.2 in Verbindung mit 4.6 |

### 4.5 Der Waiver bleibt aktiv

WAIVER-DEV-001 ist mit diesem Amendment **nicht geschlossen**. Closing
Criterion §9 (3) bleibt offen und ist ausschließlich durch den Independent
Review des Implementation Plans erfüllbar. Der Waiver bleibt bis dahin aktiv
und ist bei jeder Governance-Prüfung des Milestone 1.0 zu berücksichtigen
(WAIVER-DEV-001 §9, Schlusssatz).

Dieses Amendment beseitigt ausschließlich die **Auslegungsunsicherheit**, gegen
die der Independent Review prüft.

---

## 5. Auswirkungen

### 5.1 Ausdrücklich unverändert

| Artefakt | Status |
|---|---|
| Milestone 1.0 Charter | **Unverändert** |
| Engineering Specification 1.0, Revision R1 | **Unverändert** |
| Implementation Plan 1.0, Revision R1 | **Inhaltlich unverändert** (siehe 5.3) |
| Architecture Book v2.0 | **Unverändert** — FROZEN |
| Bootstrap Baseline 1.0 | **Unverändert** |
| ADR-005, ADR-006, ADR-007, ADR-011 | **Unverändert** |
| Development Standard v1.1 | **Unverändert** |
| WAIVER-DEV-001 (Text des Parent-Dokuments) | **Unverändert** |

### 5.2 Ausdrücklich nicht erzeugt

| Gegenstand | Anzahl |
|---|---|
| Neue Functional Requirements | **0** — FR-001 bis FR-014 unverändert |
| Neue Non-Functional Requirements | **0** — NFR-001 bis NFR-010 unverändert |
| Neue Acceptance Criteria | **0** — 29 unverändert |
| Neue Quality Gates | **0** — QG-001 bis QG-008 unverändert |
| Neue Work Packages | **0** — WP-001 bis WP-007 unverändert |
| Neue Deliverables | **0** — D-001 bis D-010 unverändert |
| Neue Evidence-Artefakte | **0** — 20 unverändert |
| Neue Architekturaussagen | **0** |
| Neue ADRs oder RDRs | **0** — dieses Amendment ist weder ADR noch RDR |
| Neue Security-Anforderungen | **0** |
| Neue Implementierungsdetails | **0** |
| Neue Governance-Instanzen oder Prozessschritte | **0** |
| Neue Registereinträge | **0** — das konsolidierte Register führt unverändert 16 Einträge |

### 5.3 Dokumentarische Folge für den Implementation Plan

Der Implementation Plan wurde durch dieses Amendment **nicht geändert**. Seine
Statusaussagen zu GDR-001 in den Abschnitten 5.5.1, 7.6, 7.8, 10.3 (AP-09,
AP-01), 10.5, 10.7 und 10.8 beschreiben den Entscheidungsbedarf als offen und
sind mit Wirksamkeit dieses Amendments überholt.

Die Nachführung dieser Statusaussagen ist eine **rein redaktionelle
Dokumentationsaufgabe ohne inhaltliche Wirkung**. Sie ist als
Nachführungsvermerk NV-001 im Finding Closure Addendum geführt, nicht
blockierend für W-3 und erzeugt kein Finding.

### 5.4 Wirkung auf die Risikolage

| Registereintrag | Wirkung |
|---|---|
| WR-1 — „Der Implementation Plan enthält die zugewiesenen Pflichtabschnitte nicht" | **Bewertung unverändert.** Status bleibt MITIGATED mit ausstehender Bestätigung durch den Independent Review (§9 (3)). Dieses Amendment beseitigt die Auslegungsunsicherheit, nicht die Bestätigungspflicht. |
| GR-001 — Paralleler Artefaktbaum | **Nicht betroffen.** Bleibt PENDING DECISION mit unveränderter Frist gemäß PR-001.7. |
| Alle übrigen 14 Einträge | **Nicht betroffen.** |

Keine Neubewertung, keine Umwidmung, keine Aufnahme, keine Streichung.

---

## 6. Authorization

| Feststellung | Inhalt |
|---|---|
| **Dokumentstatus des Implementation Plans** | Bleibt **DRAFT** |
| **Implementierungsautorisierung** | Es entsteht **keine**. Produktionscode bleibt nicht autorisiert. |
| **Sprint-Planungsautorisierung** | Es entsteht **keine**. Die Bedingungen aus Implementation Plan 10.6 bleiben unverändert und vollständig anwendbar, einschließlich der dokumentierten Entscheidung zu GR-001. |
| **Autorisierungsgrenze** | Unverändert gemäß Engineering Specification 1.0 Approval Record §11 und Implementation Plan Kapitel 1.6 |
| **Was dieses Amendment autorisiert** | Ausschließlich die verbindliche Auslegung der Closing Criteria §9 (1) und §9 (2) für Milestone 1.0 |
| **Was dieses Amendment nicht autorisiert** | Coding, Tests, Deployment, Release, Sprintdurchführung, Änderungen an Baseline oder Architektur, Vorwegnahme der Bestätigung nach §9 (3) |

---

## 7. Finding Closure — H-01

| Feld | Inhalt |
|---|---|
| **Finding** | H-01 — Verengte Wiedergabe der Waiver Closing Criteria ohne deklarierte Abweichung |
| **Quelle** | Global Consistency Audit R1, bestätigt in R2 |
| **Severity** | High |
| **Status** | **CLOSED** |
| **Schließungsdatum** | 2026-08-05 |
| **Schließende Instanz** | Governance Architect / Release Authority |
| **Schließungsgrundlage** | WAIVER-AMENDMENT-001, Abschnitt 4 |

### 7.1 Begründung der Schließung

Das Finding beanstandete, dass der Implementation Plan die Closing Criteria in
verkürzter Form wiedergibt und auf dieser Grundlage als adressiert führt, ohne
die Abweichung vom Wortlaut zu deklarieren oder zu eskalieren.

Der Vorwurf der **fehlenden Eskalation** ist mit der Vorlage von GDR-001 und
der vorliegenden Entscheidung gegenstandslos: Der Konflikt wurde ausgewiesen,
vorgelegt und durch die zuständige Instanz im dafür vorgesehenen Verfahren
entschieden.

Der Vorwurf der **verengten Wiedergabe** ist mit Abschnitt 4 gegenstandslos:
Die Darstellung im Implementation Plan entspricht nunmehr der verbindlichen
Auslegung der Kriterien. Es liegt keine Abweichung mehr vor, die zu deklarieren
wäre.

Eine **Absenkung** im Sinne von ACN-09 findet nicht statt:

| Prüfpunkt | Feststellung |
|---|---|
| Wurde eine Bedingung gestrichen? | Nein. Codebeispiele und implementierungsnahe Änderungsbeschreibungen sind der Implementierungsphase zugewiesen (4.3), nicht entfallen. |
| Wurde die Entscheidung durch den Plan getroffen? | Nein. Sie wurde durch die zuständige Instanz in einem eigenen Governance-Artefakt getroffen. |
| Wurde der Prüfumfang des Independent Review verkürzt? | Nein. §9 (3) bleibt unverändert und ausstehend. |
| Wurde ein Präzedenzfall geschaffen? | Nein. Geltung ausschließlich für Milestone 1.0. |

### 7.2 Wirkung auf Readiness Level RL-01

Das Kriterium für RL-01 lautet gemäß Implementation Plan 10.5:

> „AP-01 bis AP-06 und AP-09 erfüllt; Gesamtkonsistenzaudit ohne offene
> Critical- oder High-Findings"

| Bedingung | Stand nach diesem Amendment |
|---|---|
| AP-01 bis AP-06 und AP-09 erfüllt | Erfüllt |
| 0 offene Critical Findings | Erfüllt |
| 0 offene High Findings | **Erfüllt** — H-01 CLOSED |

**RL-01 ist damit materiell erreicht.** Die formale Feststellung erfolgt über
die Status Summary; die redaktionelle Nachführung der Statusaussagen im
Implementation Plan (NV-001) ist davon unabhängig und nicht blockierend.

---

## 8. Governance Chain

Die Governance-Kette des Milestone 1.0 bleibt **unverändert und vollständig**:

```
Charter
   ↓
Engineering Specification
   ↓
Implementation Plan
   ↓
Sprint Planning
   ↓
Implementation
   ↓
Verification
   ↓
Release
```

| Prüfpunkt | Bestätigung |
|---|---|
| Reihenfolge der Kette | Unverändert |
| Zusätzliche Stufen eingefügt | Keine |
| Stufen entfallen oder übersprungen | Keine |
| Rangfolge der normativen Artefakte (Implementation Plan 1.4) | Unverändert |
| Zweistufiger Governance-Prozess (Charter §8) | Unverändert |
| Lifecycle-Ordnung (Development Standard v1.1 §7) | Unverändert |
| Autorisierungsgrenzen | Unverändert |

Dieses Amendment ist ein Zusatz zu einem bestehenden Artefakt derselben Ebene.
Es tritt nicht neben die Kette und erzeugt keine neue Entscheidungsebene.

---

## 9. Independent Review Preparation

### 9.1 Findings-Stand nach Genehmigung dieses Amendments

| Kategorie | Anzahl | Einträge |
|---|---|---|
| **Offene Critical Findings** | **0** | — |
| **Offene High Findings** | **0** | — |
| Offene Medium Findings | 0 | — |
| Offene Low Findings | 0 | — |
| Offene Editorial Findings | 1 | R2-E-01 (Registerregel 3, terminologisch, nicht blockierend) |
| Offene Entscheidungsbedarfe | 1 | GR-001 — PENDING DECISION, Frist gemäß PR-001.7; nach PR-001.8 **nicht** genehmigungsblockierend für den Plan |
| Prozessbedingt offen | 1 | CC-14 / §9 (3) — Independent Review W-3 |
| Redaktionelle Nachführung | 1 | NV-001 — nicht blockierend |

**Es bestehen keine offenen Critical Findings und keine offenen High
Findings.**

### 9.2 Nächster autorisierter Schritt

| Feld | Inhalt |
|---|---|
| **Nächster Schritt** | **Independent Review — Workflow-Schritt W-3** gemäß Implementation Plan 10.4 |
| **Gegenstand** | Unabhängige Prüfung des Gesamtplans in Revision R1 |
| **Ausdrücklicher Prüfauftrag** | Bestätigung der Vollständigkeit der zugewiesenen Abschnitte nach WAIVER-DEV-001 §9 (3), **gemessen an der durch dieses Amendment festgelegten Auslegung** |
| **Weitere Prüfaufträge** | Bestätigung der Schließung von F-004 (Anhang B); Bestätigung oder Änderung der Frist gemäß PR-001.7 zu GR-001; unabhängige Verifikation der selbsterklärten Completion Conditions (CC, RCC, MCC, ROC) |
| **Nicht autorisiert** | Coding, Sprintdurchführung, Deployment, Release, Baseline- oder Architekturänderung |

---

## 10. Approval

| Feld | Wert |
|---|---|
| **Entscheidung** | Option B gemäß GDR-001 §3 — Waiver Amendment |
| **Status** | **APPROVED** |
| **Datum** | 2026-08-05 |
| **Instanz** | Governance Architect / Release Authority |
| **Geltung** | Ausschließlich Milestone 1.0; kein Präzedenzfall |
| **Wirksamkeit** | Mit Genehmigungsdatum |
| **Folgeartefakte** | Finding Closure Addendum H-01; Governance Decision Update in GDR-001 §7; Governance Status Summary |

---

*Ende WAIVER-AMENDMENT-001.*
