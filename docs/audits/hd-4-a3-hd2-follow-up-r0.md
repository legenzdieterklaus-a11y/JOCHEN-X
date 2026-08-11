# JOCHEN X — Milestone 1.0
# HD4-A3-R0 — A-3 Follow-up: HD-2 / Sprint-/WP-Zuordnung
## Governance Follow-up — Determination Review (keine Entscheidung)

> **COMPLETED — DETERMINATION REVIEW**
>
> Dieses Dokument verifiziert quellenbasiert die bestehende Klassifikation
> **A-3 = `PARALLEL`** (HD4-AP-01-R0) nach HD-4-Approval (HD4-APP-01-R0),
> A-1-Registrierung (HD4-A1-R0) und A-2-Follow-up (HD4-A2-R0). Es trifft
> **keine** Entscheidung über HD-2, nimmt **keine** Sprint-/WP-Planung vor
> und erzeugt **keine** neue Governance-Regel. Ergebnis:
> **A-3 = PARALLEL · HD-2 = OPEN / NOT DECIDED · HUMAN DECISION REQUIRED.**
>
> **CODING = NOT AUTHORIZED** · **RL-05 = NOT REACHED** · **QG-006 = NOT STARTED**

---

## 1. Document Control

| Feld | Wert |
|---|---|
| **Document ID** | **HD4-A3-R0** |
| Subject | **A-3 — HD-2 / Sprint-/WP-Zuordnung Follow-up (Determination Review)** |
| Date | 2026-08-11 |
| Pfad | `docs/audits/hd-4-a3-hd2-follow-up-r0.md` |
| Revision | R0 |
| **Bezugs-Baseline** | `MILESTONE-1.0-BASELINE = 8fcf42f1997dfcf6ff232e75fd33c37b933991c8` (historisch, unverändert) |
| HEAD bei Beginn | `3231e5bac5d2d4d6311dbe4c99ee3bb4fbe799dd` (HD4-A2-R0) |
| Branch | `milestone-1.0-governance` |
| **Status** | **COMPLETED — DETERMINATION REVIEW** |
| Artefakt-Typ | Traceability-/Determination-Archiv (keine Governance-Entscheidung) |
| Rolle des Erstellers | Governance-/Architektur-Analyst — **nicht** entscheidungsbefugt |
| **A-3** | **PARALLEL — VERIFIED** (Klassifikation, keine Entscheidung) |
| **HD-2** | **OPEN / NOT DECIDED — HUMAN DECISION REQUIRED** |
| **ADR-012** | **UNCHANGED** |
| Coding | **NOT AUTHORIZED** · RL-05 **NOT REACHED** · QG-006 **NOT STARTED** |

## 2. Purpose

Quellenbasierte Prüfung des A-3-Gegenstands (HD-2 / Sprint-/WP-Zuordnung):
Verifikation des bestehenden Befunds `A-3 = PARALLEL` aus HD4-AP-01-R0,
Bestimmung der nach HD4-APP-01-R0 und HD4-A1-R0 geltenden Governance-Lage,
Prüfung der Approval- und Registrierungs-Abhängigkeit, strikte Erhaltung der
Achsentrennung HD-2-Entscheidung ↔ Sprint-/WP-Abdeckung ↔
Coding-Autorisierung, Archivierung des Ergebnisses.

## 3. Scope

**In Scope:** Baseline-Gate; Source Gate; Chronologie; Definition, Status und
Traceability von HD-2 (F5-U1 → HD-2 → OI-1); Verifikation der Klassifikation
`PARALLEL`; Prerequisite-Prüfungen (ADR Approval, ADR-012 Registration);
Beziehungsprüfung Sprint/WP und Coding (IP §10.6 Nr. 7); repositoryweite Suche
nach einer HD-2-Human-Entscheidung; Archivierung; Commit.

## 4. Non-Goals

Keine HD-2-Entscheidung; keine HD-3-Entscheidung; keine Sprint-/WP-Planung
oder -Festlegung; keine Änderung von ADR-012 (Status, Inhalt, ID, Pfad); keine
Schließung von OI- oder UNKNOWN-Positionen; keine neue Governance-Regel, kein
neues Gate, keine neue Approval-Reihenfolge; keine Coding-Autorisierung; kein
RL-05, kein QG-006; keine Überschreibung bestehender Governance-Dateien; keine
Umdeutung historischer Entscheidungen; kein Push, kein PR, kein Merge.

## 5. Baseline Verification

| Prüfung | Ergebnis | Klasse |
|---|---|---|
| `git rev-parse HEAD` | `3231e5bac5d2d4d6311dbe4c99ee3bb4fbe799dd` — entspricht dem erwarteten HEAD `3231e5b` | SOURCE FACT |
| Governance-Kette | `3231e5b` (HD4-A2-R0) → `70893fc` (HD4-A1-R0) → `14354b8` (HD4-APP-01-R0) → `8414384` (HD4-HDR-01-R0) → `b20858e` (HD4-GOV-DECISION-R0) → `641947c` (HD4-AP-01-R0) → `1efb61b` (HD4-FU-R0) → `8fcf42f` (MILESTONE-1.0-BASELINE) — **exakt wie erwartet** | SOURCE FACT |
| Working Tree vor Beginn | vorbestehende Modifikationen (`CLAUDE.md`, `ROADMAP.md`, ADR-005/006/007, Architecture Book) und untracked Dokumente — **unangetastet** | SOURCE FACT |
| Staging vor Beginn | leer | SOURCE FACT |

**Status: PASS** — keine neue Baseline definiert; historische Bezugs-Baseline
bleibt `8fcf42f`.

## 6. Source Gate

| # | Source | Path | Verification |
|---|---|---|---|
| 1 | HD-4 (registriert als ADR-012) | `docs/adr/012-plugin-security-policy-configuration.md` | SOURCE FACT — Kap. 1, 3, 6.0/6.2 (ND-5), 13.3 (KZ-1), 19 (OI-1), 20, 21.1 (A-3); der historische Draft-Pfad `docs/audits/hd-4-od05-adr-draft-r0.md` existiert nicht mehr — per HD4-A1-R0 Kap. 8 dorthin überführt; die geforderten Kapitel liegen dort unverändert (historischer R0-Stand) vor (HD4-A3-B-01) |
| 2 | HD4-FU-R0 | `docs/audits/hd-4-governance-follow-up-r0.md` | SOURCE FACT — Traceability F5-U1 → HD-2 → OI-1 („TRACEABLE BUT RENAMED", in HD-1 dokumentierter Bestand) |
| 3 | HD4-AP-01-R0 | `docs/audits/hd-4-approval-readiness-r0.md` | SOURCE FACT — Kap. 10 (A-3-Analyse A3-1 … A3-7), 11, 12, 15 (NF-3), 16 (U-C), 19 |
| 4 | HD4-GOV-DECISION-R0 | `docs/audits/hd-4-governance-decision-r0.md` | SOURCE FACT — Kap. 12 (A-3 Status), 13 (OI-1), 17 |
| 5 | HD4-HDR-01-R0 | `docs/audits/hd-4-human-decision-record-r0.md` | SOURCE FACT — Explicit Non-Decisions („Keine Entscheidung über HD-2"), Kap. 11.3, 12, 14 |
| 6 | HD4-APP-01-R0 | `docs/audits/hd-4-approval-decision-r0.md` | SOURCE FACT — Kap. 5 (wörtliche Human-Entscheidung inkl. „Keine automatische Entscheidung über HD-2"), 11, 12 (OI-1 OPEN, Wirkung: keine), 13, 15 |
| 7 | HD4-A1-R0 | `docs/audits/hd-4-a1-registration-r0.md` | SOURCE FACT — Kap. 7 (Autorisierungsgrundlage ohne HD-2), 10 (HD-2 OPEN, Wirkung von A-1: keine), 13 |
| 8 | HD4-A2-R0 | `docs/audits/hd-4-a2-hd3-follow-up-r0.md` | SOURCE FACT — HD-2 dort ausdrücklich „nicht Gegenstand", OPEN / NOT DECIDED |
| 9 | HD-1 | `docs/governance/hd-1-adr-rdr-decision.md` | SOURCE FACT — Kap. 17 („HD-2 bleibt OFFEN — wird separat entschieden"), 19 („F5-U1 … OPEN (= HD-2)"; HD-2 OPEN, Autorität Projekteigner), 20 (Schritt 2: „OPEN — unabhängig, parallel führbar"), SF-14 (Kap. 8 — nur ADR-Bestandsangabe, kein HD-2-Bezug) |
| 10 | F-5 | `docs/governance/f-05-od05-change-control-determination.md` | SOURCE FACT — **PRE-HD-1 / HISTORISCH**: Kap. 2 (H-2), 17, 19 (F5-U1 „GOVERNANCE DECISION REQUIRED"), 20 (HD-2-Ausweisung), 21 (Schritt 3). Fortgeltung ausschließlich über HD-1 Kap. 19 |
| 11 | F-4 | `docs/governance/f-04-od05-td19-scope-assessment.md` | GEPRÜFT — kein HD-2-Vorkommen; Sprint Plan dort „unverändert" (Final Gate); F4-U1/U2/U3 sind TD-19-/Security-Positionen ohne HD-2-Identität (Kap. 14) |
| 12 | OD-05 | `docs/governance/od-05-governance-decision.md` | SOURCE FACT — Kap. 16 (Sprint-/WP-Auswirkung: WP-003/WP-004/QG-006; „Eigene Sprint-/WP-Zuordnung für OD-05: **keine**"; kein Sprint gestartet), Kap. 17 (U-1 … U-10 ohne HD-2-Position) |
| 13 | NAW-A / NAW-B | `docs/governance/naw-a-…` / `naw-b-…` | GEPRÜFT — kein HD-2-Vorkommen; für A-3 nicht weiter einschlägig |
| 14 | Development Standard v1.1 | `docs/development-standard-v1.1.md` | SOURCE FACT — §5, §13, §17 Anh. B geprüft (kein HD-2-Bezug). **Ein §10.6 existiert im Development Standard nicht**; die Coding-Bedingungen 7–9 liegen in **IP §10.6** (HD4-A3-B-02) |
| 15 | Implementation Plan §10.6 | `docs/milestone-1.0-implementation-plan.md` (APPROVED R1.2) | SOURCE FACT — §10.6 „Authorization Criteria": Sprint Planning Bedingungen 1–6; **Coding Bedingungen 7–9** (Nr. 7: „Eine genehmigte Sprintplanung liegt vor"); Ausschlusskatalog |

**Repositoryweite Suche** nach `HD-2` unter `docs/`: genau **10
Treffer-Dateien** — sämtlich Bestandteil der obigen Quellenliste. **Kein
separates HD-2-Entscheidungsartefakt existiert** (HD4-A3-B-03).

Keine externe Quelle verwendet. **Status: PASS**

## 7. Governance Chronology

| Stufe | Ereignis | Einordnung |
|---|---|---|
| 1 | **F-5** | **HISTORISCH / PRE-HD-1** — erzeugt F5-U1 („Sprint-/WP-Zuordnung — GOVERNANCE DECISION REQUIRED", Kap. 19) und weist **HD-2** als erforderliche Human Decision aus (Kap. 20) |
| 2 | **HD-1** (2026-08-10) | Maßgeblicher Post-Decision-Stand: schreibt F5-U1 ausdrücklich als **HD-2** fort (Kap. 19); Kap. 17: „HD-2 bleibt OFFEN — wird **separat** entschieden"; Kap. 20 Schritt 2: „**OPEN — unabhängig, parallel führbar**" |
| 3 | HD4-FU-R0 | Traceability F5-U1 → HD-2 → OI-1 — keine Entscheidung |
| 4 | HD4-AP-01-R0 | Klassifikation **A-3 = `PARALLEL`** (Kap. 10.3) — Analyse, keine Entscheidung; U-C bleibt HUMAN REVIEW REQUIRED |
| 5 | HD4-GOV-DECISION-R0 / HD4-HDR-01-R0 | HD-2 durchgehend OPEN / NOT DECIDED |
| 6 | **HD4-APP-01-R0** (2026-08-11) | HD-4 = APPROVED — Explicit Non-Decision: „Keine automatische Entscheidung über HD-2"; OI-1 OPEN, Wirkung: keine |
| 7 | **HD4-A1-R0** | ADR-012 registriert — HD-2 unverändert OPEN; A-1-Wirkung auf HD-2: keine |
| 8 | **HD4-A2-R0** | A-2-Determination — HD-2 „nicht Gegenstand", unverändert OPEN |
| 9 | **HD4-A3-R0** | dieses Follow-up |

**Chronologie-Regel angewendet:** F-5-Aussagen werden als historisch
behandelt; die Position gilt ausschließlich fort, weil HD-1 Kap. 19 sie als
HD-2 fortschreibt. Kein späteres Artefakt verändert den HD-1-Stand — jedes
bestätigt ihn. **Kein Widerspruch zwischen den Quellen.**

## 8. A-3 Definition

| Frage | Befund |
|---|---|
| Was ist **HD-2**? | Die offene Human-Entscheidung „**Sprint-/WP-Zuordnung des finalisierten Umrisses**" (OD-05 Option B / CS-1+CS-2+CS-3). Autorität: **Projekteigner** [SOURCE: HD-1 Kap. 19; F-5 Kap. 20] |
| Definierende Quelle | **F-5 Kap. 17/19/20** (Erzeugung als F5-U1/H-2, Ausweisung als HD-2, historisch) und **HD-1 Kap. 19** (maßgebliche Fortschreibung: „F5-U1 … OPEN (= HD-2)") |
| Rolle in der HD-4-Kette | HD-4 Kap. 21.1 führt **A-3** als offenen Klärungspunkt „Verhältnis HD-2 / Sprint-/WP-Zuordnung zur ADR-Genehmigung"; ADR-012 hält HD-2 als ND-5/KZ-1/OI-1 ausdrücklich offen |
| Sachgrund | Der finalisierte Umriss ist im genehmigten Sprint Plan **nicht abgedeckt** [SOURCE: HD-1 Kap. 18/20 Schritt 2; F-5 Kap. 17 H-2; ADR-012 KZ-1] |

## 9. HD-2 Determination

> ## **HD-2 = OPEN / NOT DECIDED — HUMAN DECISION REQUIRED**

Durchgehend belegt in sämtlichen Artefakten bis einschließlich HEAD:
HD-1 Kap. 17/19/20 (OFFEN/OPEN) · ADR-012 ND-5/OI-1/Kap. 20 (OPEN) ·
HD4-AP-01-R0 Kap. 14/19 (NOT DECIDED) · HD4-GOV-DECISION-R0 Kap. 12/17
(OPEN) · HD4-HDR-01-R0 Kap. 12/14 (OPEN / NOT DECIDED) · HD4-APP-01-R0
Kap. 11/15 (OPEN / NOT DECIDED) · HD4-A1-R0 Kap. 10/13 (OPEN / NOT
DECIDED) · HD4-A2-R0 Kap. 20 (OPEN / NOT DECIDED, nicht Gegenstand).
Zuständige Autorität: **Projekteigner** (HD-1 Kap. 19).

## 10. HD-2 vs ADR Approval

```text
HD-2 prerequisite for ADR Approval?  →  NO
```

| # | Beleg |
|---|---|
| 1 | HD-1 Kap. 20: Die ADR-Genehmigung (Schritt 4) ist allein als „nach HD-4" sequenziert — **ohne** HD-2-Bedingung; HD-2 (Schritt 2) ist „unabhängig, parallel führbar" [SOURCE FACT] |
| 2 | HD-1 Kap. 17: „HD-2 bleibt OFFEN — wird **separat** entschieden" [SOURCE FACT] |
| 3 | HD4-AP-01-R0 NF-3: keine geprüfte Quelle legt A-3 als Approval-Voraussetzung fest (Negative Finding, dort positiv auf HD-1 Kap. 17/20 gestützt) |
| 4 | **Vollzugsbeleg:** Die HD-4-Genehmigung wurde am 2026-08-11 tatsächlich erteilt (HD4-APP-01-R0), **während HD-2 OPEN war**; die Human-Entscheidung trennt ausdrücklich: „keine automatische Entscheidung über … HD-2" und `HD-4 APPROVAL ≠ … ≠ HD-2 DECISION` |

Das NO beruht auf ausdrücklichen Quellenaussagen und dem vollzogenen
Approval-Sachverhalt — **nicht** auf bloßer Regel-Abwesenheit. Die von HD-4
Kap. 21.1 offen gehaltene Gestaltungsfrage (freiwilliges Abwarten, U-C) ist
durch den Vollzug der Genehmigung gegenstandslos geworden, wird aber nicht
rückwirkend umgedeutet.

## 11. HD-2 vs ADR-012 Registration

```text
HD-2 prerequisite for ADR registration?  →  NO
```

| # | Beleg |
|---|---|
| 1 | HD4-A1-R0 Kap. 7 führt die Autorisierungsgrundlage der Registrierung abschließend auf (Dev-Standard §5/§13/§17 Anh. B; HD-4 Kap. 1.1/21; HD-1 SF-14; HD4-APP-01-R0) — **HD-2 kommt darin nicht vor** |
| 2 | HD4-A1-R0 Kap. 10: „HD-2 — OPEN / NOT DECIDED — Wirkung von A-1: keine" [SOURCE FACT] |
| 3 | **Vollzugsbeleg:** Die Registrierung (ADR-012, Commit `70893fc`) wurde durchgeführt, **während HD-2 OPEN war** |

Die bestehende Registrierung wird **nicht** rückwirkend verändert.

## 12. HD-2 vs Sprint/WP

| Ebene | Befund |
|---|---|
| **Gegenstand der Entscheidung** | HD-2 **ist** die Entscheidung über die Sprint-/WP-**Zuordnung** des finalisierten Umrisses — nicht deren Durchführung |
| **Planung** | Ein genehmigter Sprint Plan existiert (`docs/milestone-1.0-sprint-plan.md`, DRAFT 1.0 R0, als Planungsgrundlage genehmigt [SOURCE: OD-05 Kap. 4 Nr. 10]); dieses Follow-up nimmt **keine** Planung vor |
| **Abdeckung** | Der Umriss ist im genehmigten Sprint Plan **nicht abgedeckt** [SOURCE: HD-1 Kap. 18/20]; OD-05 Kap. 16: „Eigene Sprint-/WP-Zuordnung für OD-05: **keine**"; die dort genannten WP-003/WP-004 und QG-006 betreffen das Umfeld (QG-006 abschließbar erst nach WP-003 **und** WP-004), nicht die Zuordnung des Umrisses (HD4-A3-B-04) |
| **Umsetzung** | NICHT AUTORISIERT — unverändert |
| **Coding Authorization** | separat (Kap. 13) |

Diese fünf Ebenen werden hier ausschließlich unterschieden — keine wird durch
dieses Dokument verändert oder herbeigeführt.

## 13. HD-2 vs Coding

| Prüfung | Ergebnis |
|---|---|
| Bestehende Coding-Vorbedingung | **IP §10.6 Bedingung 7**: „Eine genehmigte Sprintplanung liegt vor" — verifiziert im Wortlaut [SOURCE: `docs/milestone-1.0-implementation-plan.md` §10.6 „Coding"]; zusätzlich Bedingungen 8–9 (Baseline-Bestätigung; RL-05) und der Ausschlusskatalog |
| Beziehung HD-2 ↔ Bedingung 7 | Der HD-2-Gegenstand (Sprintplan-Abdeckung des Umrisses) ist **materiell mit Bedingung 7 verbunden** [SOURCE: HD4-AP-01-R0 A3-5/A3-6, HD4-AP-B-04] — eine **bestehende** Abhängigkeit, hier nur dokumentiert |
| Umdeutungsverbot | Diese Coding-Vorbedingung wird **nicht** in eine ADR-Approval-Voraussetzung umgedeutet; die Achsen bleiben getrennt: `ADR Approval ≠ HD-2 Decision ≠ Sprint/WP Coverage ≠ Coding Authorization` |
| Konsequenz | Eine künftige HD-2-Entscheidung allein erzeugte **keine** Coding-Readiness (zusätzlich RL-05, GC-06, IP §10.6 Nr. 8–9 erforderlich [SOURCE: HD4-AP-01-R0 A3-6/A3-7; ADR-012 Kap. 20.1]) |

## 14. F4/UNKNOWN Traceability

| Position | Verhältnis zu HD-2 | Einordnung |
|---|---|---|
| **F5-U1** | Ursprungsposition — von HD-1 Kap. 19 ausdrücklich als HD-2 fortgeschrieben („TRACEABLE BUT RENAMED", HD4-FU-R0); keine neue Umbenennung | **IDENTISCH (fortgeschrieben)** |
| **F4-U1** (TD-19-Restumfang, OI-6) | andere Sachfrage (Security/TD-19) | **RELATED — NOT IDENTICAL** (gemeinsame OD-05-Kette, getrennte Positionen) |
| **F4-U2** (Policy-Diskontinuität, HD-3/OI-2) | andere Sachfrage; per HD4-A2-R0 OPEN/UNKNOWN | **RELATED — NOT IDENTICAL** |
| **F4-U3** (FINALIZE-Konsument, OI-5) | kein HD-2-Bezug | **NOT IDENTICAL** |
| **AC-16** (ADR-012 Kap. 18) | abhängig von **HD-3/F4-U2**, nicht von HD-2 | **NOT IDENTICAL** |
| **AC-15 / OI-4** (Z-1/Z-2) | Umsetzungsdetail, kein HD-2-Bezug | **NOT IDENTICAL** |

Keine Verschmelzung; jede Position behält ihre historische Herkunft.

```text
F5-U1  →  HD-2  →  OI-1
```

## 15. OI Integrity

| OI | Gegenstand | Status | Durch HD4-A3-R0 verändert? |
|---|---|---|---|
| **OI-1** | **HD-2 — Sprint-/WP-Zuordnung** | **OPEN** | **NEIN** — Gegenstand dieses Reviews, unverändert offen |
| OI-2 | HD-3 / F4-U2 | OPEN / UNKNOWN (per HD4-A2-R0) | NEIN |
| OI-3 | NAW-A-U1 / C-3 | OFFEN | NEIN |
| OI-4 | NAW-A-U2 / Z-1, Z-2 | OFFEN | NEIN |
| OI-5 | F4-U3 | UNKNOWN | NEIN |
| OI-6 | F4-U1 / U-3 | UNKNOWN / OPEN | NEIN |
| OI-7 | ADR-ID/Registrierung | FULFILLED BY HD4-A1-R0 (historisch dokumentiert) | NEIN |
| OI-8 | ADR-Genehmigung | FULFILLED BY HUMAN DECISION (HD4-APP-01-R0) | NEIN |

Die Erfüllung von OI-8 durch die HD-4-Approval wird **nicht** auf HD-2/OI-1
übertragen. Keine OI-Position wird geschlossen, umbenannt oder erzeugt.

## 16. Human Decision Check

**Ergebnis: KEINE autorisierte Human-Entscheidung über HD-2 gefunden.**

| Prüfung | Befund |
|---|---|
| Repositoryweite Suche (`HD-2`) | 10 Dateien — sämtlich im Source Gate; keine enthält eine Entscheidung mit Authority, Datum, konkreter Entscheidung (APPROVED/ACCEPTED/REJECTED/DEFERRED) und Scope zu HD-2 |
| HD4-APP-01-R0 Kap. 5 (wörtlich) | „Explicit Non-Decisions: … **Keine automatische Entscheidung über HD-2.**" — die HD-4-Approval wird **nicht** als HD-2-Genehmigung interpretiert |
| Nicht als Entscheidung gewertet | Analysen/Determinationen (HD4-AP-01-R0, HD4-A2-R0, dieses Dokument), PASS-Befunde, Klassifikationen („PARALLEL"), Negative Findings, die HD-4-Approval, die ADR-012-Registrierung, Coding-Bedingungskataloge |
| Konsequenz | `HD-2 = OPEN / NOT DECIDED` · `HUMAN DECISION REQUIRED` — Autorität: Projekteigner |

## 17. Negative Findings

| # | Negative Finding |
|---|---|
| **NF-1** | Keine geprüfte Quelle legt HD-2 als Voraussetzung der (bereits erteilten) HD-4-ADR-Genehmigung fest |
| **NF-2** | Keine geprüfte Quelle legt HD-2 als Voraussetzung der (bereits vollzogenen) ADR-012-Registrierung fest |
| **NF-3** | Repositoryweit existiert kein Artefakt, das eine autorisierte Human-Entscheidung über HD-2 dokumentiert |
| **NF-4** | F-4, OD-05 (außer Sprint-Kontext Kap. 16), NAW-A und NAW-B enthalten keine HD-2-Fundstelle |
| **NF-5** | Der Development Standard v1.1 enthält kein §10.6 und keine HD-2-bezogene Regel; die Coding-Bedingungen 7–9 liegen ausschließlich in IP §10.6 |

> Aus keinem Negative Finding wird eine neue Regel erzeugt.

## 18. Observation Register

| ID | Beobachtung | Klasse |
|---|---|---|
| **HD4-A3-B-01** | Der im Auftrag genannte Pfad `docs/audits/hd-4-od05-adr-draft-r0.md` existiert nicht mehr — per HD4-A1-R0 Kap. 8 nach `docs/adr/012-plugin-security-policy-configuration.md` überführt; die geforderten HD-4-Kapitel (1, 3, 19, 20, 21, 21.1) liegen dort als unveränderter historischer R0-Stand vor. Historische Referenzen auf den alten Pfad bleiben als Zeitpunktdokumentation gültig | SOURCE FACT / OBSERVATION |
| **HD4-A3-B-02** | Der Development Standard v1.1 besitzt **kein** §10.6; die im Auftrag referenzierten Coding-Bedingungen („§10.6 Nr. 7") liegen im **Implementation Plan** (`docs/milestone-1.0-implementation-plan.md` §10.6 Authorization Criteria, APPROVED R1.2) und wurden dort im Wortlaut verifiziert | SOURCE FACT / OBSERVATION |
| **HD4-A3-B-03** | Die repositoryweite `HD-2`-Suche ergab genau 10 Dateien — sämtlich Bestandteil des Source Gate; ein separates HD-2-Entscheidungs- oder Planungsartefakt existiert nicht | SOURCE FACT / OBSERVATION |
| **HD4-A3-B-04** | Der genehmigte Sprint Plan enthält WP-003/WP-004 (mit QG-006 als nachgelagertem Gate), jedoch gemäß OD-05 Kap. 16 **keine** eigene Sprint-/WP-Zuordnung für den OD-05-Umriss — der HD-2-Gegenstand (Abdeckung des Umrisses) bleibt unerledigt | TRACEABILITY FINDING |
| **HD4-A3-B-05** | Für A-3 existiert — wie für A-2 — kein administrativ vollziehbarer Bestandteil: HD-2 ist eine materielle, noch ausstehende Human-Entscheidung des Projekteigners; die einzige zulässige A-3-Nachführung ist dieses Archiv | OBSERVATION |

## 19. Explicit Non-Decisions

```text
HD-2 decision: NOT DECIDED
HD-3 decision: NOT DECIDED
ADR-012: UNCHANGED
ADR approval: ALREADY APPROVED
ADR-ID: ADR-012
Coding: NOT AUTHORIZED
RL-05: NOT REACHED
QG-006: NOT STARTED
```

Ergänzend: keine Sprint-/WP-Planung vorgenommen; kein Work Package
festgelegt; keine OI- oder UNKNOWN-Position geschlossen; keine neue
Governance-Regel, kein neues Gate, keine neue Approval-Reihenfolge; keine
historische Entscheidung umgedeutet; keine bestehende Governance-Datei
überschrieben; keine generischen `B-<n>`-IDs verwendet; kein Push, kein PR,
kein Merge.

## 20. Final Governance Finding

> ## **A-3 = `PARALLEL` — VERIFIED (Fall A)**
> ## **HD-2 = OPEN / NOT DECIDED**
> ## **HUMAN DECISION REQUIRED**

```text
A-3
COMPLETED — DETERMINATION
Classification: PARALLEL
Human Decision on HD-2: REQUIRED
```

Die Klassifikation `PARALLEL` aus HD4-AP-01-R0 ist quellenbasiert
**bestätigt** — positiv gestützt auf HD-1 Kap. 17 („separat") und Kap. 20
(„unabhängig, parallel führbar") sowie auf den vollzogenen Sachverhalt, dass
Approval und Registrierung bei offenem HD-2 stattfanden — **nicht** allein
auf Regel-Abwesenheit. `PARALLEL` ist eine Klassifikation des Verhältnisses
zur ADR-Genehmigung — **keine** Genehmigung, **keine** Erledigung und
**keine** Human-Entscheidung über HD-2. Die HD-2-Entscheidung
(Sprint-/WP-Zuordnung des Umrisses) liegt beim **Projekteigner**.

## 21. Repository Integrity

| Prüfung | Ergebnis |
|---|---|
| ADR-012 | **UNCHANGED** — nicht angefasst (kein Status, Inhalt, ID, Pfad, keine HD-2-Referenz eingefügt) |
| Bestehende Governance-/Audit-Dateien | **UNVERÄNDERT** — keine überschrieben |
| Vorbestehende Working-Tree-Änderungen | **UNANGETASTET** |
| Neue Dateien | genau **eine**: dieses Archiv |
| Historische B-IDs | nur referenziert, keine umbenannt oder neu vergeben |

## 22. Final Gate

> ## **HD4-A3-R0 = COMPLETED — DETERMINATION REVIEW**

| Gate | Status |
|---|---|
| **A-3** | **PARALLEL — VERIFIED** (Determination, keine Entscheidung) |
| **HD-2** | **OPEN / NOT DECIDED — HUMAN DECISION REQUIRED** (Autorität: Projekteigner) |
| **HD-3** | **OPEN / NOT DECIDED** (unverändert, per HD4-A2-R0) |
| **OI-1** | **OPEN** (unverändert) |
| **OI-2 … OI-8** | **UNVERÄNDERT** |
| **ADR-012** | **UNCHANGED — Accepted / Registered** |
| **HD-4** | **APPROVED** (unverändert) |
| **Sprint/WP** | **keine Planung vorgenommen** — Sprint Plan unverändert |
| **CODING** | **NOT AUTHORIZED** |
| **RL-05** | **NOT REACHED** |
| **QG-006** | **NOT STARTED** |
| **Push / PR / Merge** | **NOT PERFORMED** |

---

## Revision History

| Revision | Datum | Änderung | Status |
|---|---|---|---|
| **R0** | 2026-08-11 | Ersterstellung des A-3-Follow-up-Archivs (HD-2 / Sprint-/WP-Zuordnung Determination Review) | **COMPLETED — DETERMINATION REVIEW** |

---

**Ende HD4-A3-R0 — A-3 Follow-up HD-2 / Sprint-/WP-Zuordnung — JOCHEN X
Milestone 1.0 (2026-08-11) — Bezugs-Baseline
`MILESTONE-1.0-BASELINE = 8fcf42f1997dfcf6ff232e75fd33c37b933991c8`**
