# JOCHEN X — Milestone 1.0
# HD-1 — Governance-Entscheidungsrecord: ADR oder RDR? (B-6)

---

## 1. Document Identity

| Feld | Wert |
|---|---|
| Dokumenttyp | **Governance Decision Record (HUMAN DECISION)** — nicht implementierend |
| Pfad | `docs/governance/hd-1-adr-rdr-decision.md` |
| **ID** | **HD-1** |
| Gegenstand | **B-6** — Wahl des Change-Control-Instruments für **OD-05 OPTION B** |
| Status | **FINAL** |
| Datum | 2026-08-10 |
| Branch / HEAD | `milestone-1.0-governance` / `8fcf42f1997dfcf6ff232e75fd33c37b933991c8` |
| Primärquelle | `docs/governance/f-05-od05-change-control-determination.md` (F-5, FINAL ASSESSMENT) |
| Normcharakter | Menschliche Governance-Entscheidung. **Keine** Implementierungsautorisierung |
| Coding | **CODING NOT AUTHORIZED** |

---

## 2. Decision ID / HD-1

| Feld | Wert |
|---|---|
| **Decision ID** | **HD-1** |
| Zugrunde liegende offene Position | **B-6** — „ADR oder RDR?" |
| Herkunft der Position | F-5 Kap. 13, Kap. 20 (HD-1), Kap. 25 Schritt 1 |
| Status der Position **vor** dieser Entscheidung | **UNRESOLVED — HUMAN GOVERNANCE DECISION REQUIRED** |
| Status der Position **nach** dieser Entscheidung | **RESOLVED — ADR SELECTED** |

---

## 3. Date / Baseline

| Prüfung | Ergebnis |
|---|---|
| Datum | 2026-08-10 |
| **MILESTONE-1.0-BASELINE** | `8fcf42f1997dfcf6ff232e75fd33c37b933991c8` |
| HEAD zum Zeitpunkt der Aufzeichnung | `8fcf42f1997dfcf6ff232e75fd33c37b933991c8` — **identisch mit der Baseline** |
| Architecture-Book-Fassung | **Welt A / Baseline-Fassung** gemäß **GDR-OD01-001** (`git show 8fcf42f:docs/architecture-book-v2.md`) |
| Staging | **leer** |

### 3.1 Ebenentrennung

> **BASELINE ≠ WORKING TREE ≠ UNTRACKED DOCS.**

| Ebene | Verwendung in HD-1 |
|---|---|
| **BASELINE** (`8fcf42f`) | Alleinige Grundlage aller Code- und Architecture-Book-Bezüge |
| **WORKING TREE** | Sechs getrackte Modifikationen (`CLAUDE.md`, `ROADMAP.md`, ADR-005/006/007, Architecture Book) — **kein** Artefakt der Change Surface, **nicht** als Baseline behandelt |
| **UNTRACKED DOCS** | Governance-/Audit-Dokumente einschließlich dieses Records — **niemals** Baseline |

---

## 4. Decision Authority

| Feld | Wert |
|---|---|
| Entscheidende Instanz | **Projekteigner** |
| Grundlage der Zuständigkeit | F-5 Kap. 20, HD-1: „Autorität = Projekteigner + Architektur-/Security-Governance" |
| Art der Entscheidung | **HUMAN GOVERNANCE DECISION** |
| Entscheidungsgrundlage | Vollständiges F-5-Assessment (FINAL) einschließlich des Entscheidungsmaterials M-1 bis M-5 |
| Rolle des Verfassers dieses Records | **Governance Recorder** — dokumentierend, **nicht** entscheidend, **nicht** empfehlend |

> Dieser Record **trifft** die Entscheidung nicht und **bewertet** sie nicht neu.
> Er **protokolliert** eine bereits getroffene menschliche Entscheidung.

---

## 5. Source Gate

**Alle Pflichtquellen vorhanden, lesbar, keine Pfadabweichung.**

| # | Quelle | Pfad | Status |
|---|---|---|---|
| 1 | **F-5 (Primärquelle)** | `docs/governance/f-05-od05-change-control-determination.md` | **FINAL ASSESSMENT** |
| 2 | OD-05 Decision | `docs/governance/od-05-governance-decision.md` | **FINAL (GDR-OD05-001)** |
| 3 | F-4 | `docs/governance/f-04-od05-td19-scope-assessment.md` | FINAL ASSESSMENT |
| 4 | NAW-A | `docs/governance/naw-a-od05-change-surface-fixation.md` | FINAL / COMPLETED |
| 5 | NAW-B | `docs/governance/naw-b-g1-observable-state-contract-fixation.md` | FINAL / COMPLETED |
| 6 | F-3 | `docs/governance/f-03-od05-change-surface-assessment.md` | FINAL ASSESSMENT |
| 7 | F-2 | `docs/governance/f-02-bootstrap-baseline-scope-assessment.md` | FINAL (F-2-B) |
| 8 | F-1 | `docs/governance/f-01-od05-architecture-freeze-assessment.md` | FINAL (F-1-A) |
| 9 | G-1 Decision Brief | `docs/audits/g-01-bootstrap-behavior-interpretation-decision-brief-r0.md` | DRAFT · NON-NORMATIVE |
| 10 | Bootstrap Baseline 1.0 | `docs/baselines/bootstrap-baseline-1.0.md` | **APPROVED** |
| 11 | Development Standard v1.1 | `docs/development-standard-v1.1.md` | **APPROVED** |
| 12 | Architecture Book v2.0 | `docs/architecture-book-v2.md` | **APPROVED / FROZEN** — Welt A |
| 13 | RDR-001 | `docs/rdr/001-bootstrap-modularization.md` | **APPROVED** |
| 14 | Implementation Plan 1.0 | `docs/milestone-1.0-implementation-plan.md` | **APPROVED R1.2** |
| 15 | Sprint Plan 1.0 | `docs/milestone-1.0-sprint-plan.md` | **DRAFT 1.0 R0** |
| 16 | Baseline Commit Record | `docs/governance/milestone-1.0-baseline-commit-record.md` | **FINAL** |

| Prüfschritt laut Auftrag | Ergebnis |
|---|---|
| F-5 vollständig gelesen | **JA** (Kap. 1–25) |
| Entscheidung und Kontext gegen die autorisierten Quellen verifiziert | **JA** (Kap. 8) |
| Baseline-Identifier geprüft | **JA** — `8fcf42f…` = HEAD |
| Git-Status read-only geprüft | **JA** — 6 getrackte Modifikationen, Staging leer, `src/jochen_x/**` = 0 Einträge |
| Bestandsdatei verändert? | **NEIN** |
| Fehlende Pflichtquelle? | **NEIN** — kein HARD STOP |
| Pfadabweichung? | **NEIN** |

> **SOURCE GATE: BESTANDEN.**

---

## 6. Decision Statement

> ## **HD-1 / B-6 = ADR SELECTED**

Für die nach **Bootstrap Baseline §8-4** erforderliche Change-Control-Aktion zu

> **OD-05 — OPTION B**
> „Policy-Konfiguration in die bestehende `PluginSecurityStage` ziehen
> (ohne Reihenfolgeänderung)"
> [SOURCE: `docs/governance/od-05-governance-decision.md` — GDR-OD05-001]

wird als Change-Control-Instrument das **Architecture Decision Record (ADR)**
gewählt.

**RDR wird für diesen Vorgang nicht gewählt.**

Damit ist die Instrumentenklasse festgelegt — und **ausschließlich** die
Instrumentenklasse (siehe Kap. 11 und Kap. 12).

---

## 7. Decision Classification

| Merkmal | Wert |
|---|---|
| Klasse | **HUMAN GOVERNANCE DECISION** |
| **Nicht** | Assessment · Feststellung · Empfehlung · Ableitung aus Quellen |
| Begründung der Klasse | F-5 hat ausdrücklich festgestellt, dass **kein autorisiertes allgemeines ADR/RDR-Abgrenzungskriterium existiert** (F-5 Kap. 12.1, Finding **F-5-07**). Eine Auswahl ist daher nur durch die menschliche Governance-Instanz möglich |
| Verhältnis zu F-5 | F-5 bleibt **unverändert und gültig**. HD-1 **löst** die von F-5 als offen ausgewiesene Position B-6 auf; F-5 wird dadurch **nicht** korrigiert |
| Präzedenzwirkung | **KEINE.** Aus HD-1 wird **kein allgemeines ADR/RDR-Abgrenzungskriterium** und **keine** Regel für künftige Fälle abgeleitet. Die Regelungslücke aus **F-5-07** bleibt bestehen |

---

## 8. Source Facts

**Feststellungen aus den autorisierten Quellen — nicht Bestandteil der
menschlichen Entscheidung.**

| # | SOURCE FACT | Beleg |
|---|---|---|
| SF-1 | **OD-05 = OPTION B**, FINAL | `docs/governance/od-05-governance-decision.md` — GDR-OD05-001 |
| SF-2 | **§8-1, §8-2, §8-3, §8-5 = NOT TRIGGERED**; **§8-4 = TRIGGERED** | F-5 Kap. 6–10, Finding F-5-03 |
| SF-3 | **`run_phase()` = CHANGED**; `begin()` und `build_context()` = UNCHANGED | F-5 Kap. 9.1; NAW-B |
| SF-4 | **CHANGE CONTROL = REQUIRED** — der Auslöser steht fest | F-5 Kap. 14 Ebene 1, Finding F-5-06 |
| SF-5 | **§8-4 = TRIGGERED bedeutet CHANGE CONTROL REQUIRED — nicht automatisch ADR REQUIRED und nicht automatisch RDR REQUIRED** | F-5 Kap. 14 |
| SF-6 | **In keiner der zehn geprüften autorisierten Quellen existiert ein ADR-↔-RDR-Abgrenzungskriterium.** Kein Quellenwiderspruch, sondern eine **Regelungslücke** | F-5 Kap. 12, 12.1, Finding F-5-07 |
| SF-7 | Der Development Standard v1.1 §13 regelt **nur ADR** (acht Auslöser, Format, Freeze-Bezug) und enthält **keine RDR-Regel** — Volltextsuche „RDR": 0 Treffer | F-5 Kap. 12 Q-3, M-2 |
| SF-8 | Keiner der **acht ADR-Auslöser** des Development Standard §13 und keiner der **sieben AB-§22.3-Tatbestände** ist erfüllt | F-5 Kap. 11, M-4 |
| SF-9 | Die Change-Control-Pflicht folgt hier **allein** aus **Bootstrap Baseline §8-4** — nicht aus dem Architecture Freeze und nicht aus Development Standard §13 | F-5 M-5 |
| SF-10 | Der einzige RDR-Präzedenzfall **RDR-001** war ausdrücklich **verhaltensbewahrend / strukturell**: „Keine Architekturänderungen · Keine Verhaltensänderungen · Keine öffentlichen API-Änderungen"; §7 Nr. 7: „Keine ADR-Änderungen erforderlich" | `docs/rdr/001-bootstrap-modularization.md` §2.2, §7; F-5 Kap. 12 Q-5, Kap. 12.2 |
| SF-11 | Die Gegenüberstellung RDR-001 ↔ OD-05-Umriss ist in F-5 ausdrücklich als **INFERENCE — kein Kriterium** klassifiziert | F-5 Kap. 12.2, Finding F-5-08 |
| SF-12 | **B-6 = UNRESOLVED / HUMAN GOVERNANCE DECISION REQUIRED (Ergebnis B)** | F-5 Kap. 13, Finding F-5-09 |
| SF-13 | **CODING = NOT AUTHORIZED**, quellenbelegt: **RL-05 nicht erreicht** | F-5 Kap. 21, Finding F-5-12 |
| SF-14 | Bestand an Entscheidungsdokumenten zur Baseline: **ADR-001 bis ADR-011**, **RDR-001** | `docs/adr/`, `docs/rdr/` |

> **SF-14 ist eine reine Bestandsangabe.** Aus ihr wird **keine** Nummer, **keine**
> Reihenfolge und **keine** Zuordnung für das künftige Instrument abgeleitet;
> die Identifikatorvergabe gehört zu **HD-4**.

---

## 9. Human Decision Rationale

**Die folgende Begründung ist die des Projekteigners. Sie ist keine
Quellenableitung.**

| # | Erwägung | Klasse |
|---|---|---|
| R-1 | **OD-05 Option B verändert beobachtbares Verhalten** — `run_phase()` = **CHANGED** (SF-3) | gestützt auf SOURCE FACT |
| R-2 | Die Änderung betrifft **Security-Policy-Konfiguration** und deren **Einbindung in die Plugin-Admission** (CS-1 in `PluginSecurityStage.execute`) | gestützt auf SOURCE FACT |
| R-3 | Der einzige bestehende RDR-Präzedenzfall **RDR-001** war ausdrücklich **verhaltensbewahrend / strukturell** (SF-10) | gestützt auf SOURCE FACT |
| R-4 | **F-5 hat kein formales Kriterium erfunden**, das aus R-1 bis R-3 automatisch „ADR" ableitet (SF-6, SF-11) | gestützt auf SOURCE FACT |
| R-5 | Die konkrete Auswahl **ADR** erfolgt daher **ausdrücklich als menschliche Governance-Entscheidung des Projekteigners** | **HUMAN DECISION** |
| R-6 | **ADR** wird gewählt, weil die Änderung eine nachvollziehbare **architektonische und sicherheitsbezogene Entscheidung mit beobachtbarer Laufzeitwirkung** dokumentieren soll | **HUMAN DECISION** |

### 9.1 Ausdrückliche Abgrenzung

| Aussage | Zulässig? |
|---|---|
| „Die Quellen schreiben vor, dass es ein ADR sein muss." | **FALSCH — wird hier nicht behauptet** |
| „Die Quellen bestimmen die Change-Control-**Pflicht**, aber nicht das **Instrument**. Der Projekteigner entscheidet daher ADR." | **KORREKT — dies ist die Aussage dieses Records** |

> R-1 bis R-4 sind **Entscheidungsmaterial**. Die **Auswahl** liegt in R-5/R-6 und
> ist menschlich. Zwischen Material und Auswahl besteht **keine** zwingende
> Ableitung.

---

## 10. Why ADR / Why not RDR

| Frage | Antwort |
|---|---|
| **Warum ADR?** | Weil der Projekteigner die Änderung als architektonische und sicherheitsbezogene Entscheidung **mit beobachtbarer Laufzeitwirkung** dokumentiert sehen will (R-6). Das ADR-Format ist im **Development Standard v1.1 §13** als einziges der beiden Instrumente **formal beschrieben** (SF-7) |
| **Warum nicht RDR?** | Weil der einzige RDR-Präzedenzfall ausdrücklich **verhaltensbewahrend** war (SF-10), der vorliegende Umriss dagegen **verhaltensändernd** ist (SF-3). Dies ist eine **Erwägung** des Projekteigners, **kein** aus den Quellen abgeleitetes Ausschlusskriterium (SF-11) |
| **Existiert ein Kriterium, das RDR verbietet?** | **NEIN.** RDR wäre nach Quellenlage nicht ausgeschlossen gewesen. Beide Instrumente sind in allen Quellen **gleichrangig alternativ** genannt (F-5 M-1). Die Wahl ist eine **Setzung**, keine Notwendigkeit |
| **Wird aus RDR-001 ein Kriterium konstruiert?** | **NEIN** — ausdrücklich nicht. Die Präzedenzbeobachtung bleibt **INFERENCE** (SF-11) und wird nicht in eine Regel überführt |
| **Wird die Regelungslücke F-5-07 geschlossen?** | **NEIN.** Sie bleibt bestehen. HD-1 entscheidet **diesen einen Fall**, nicht die allgemeine Abgrenzung |

---

## 11. What the Decision Does

**HD-1 bewirkt genau und ausschließlich Folgendes:**

| # | Wirkung |
|---|---|
| W-1 | **Das Change-Control-Instrument für OD-05 Option B ist festgelegt: ADR** |
| W-2 | **B-6** wechselt von **UNRESOLVED** zu **RESOLVED — ADR SELECTED** |
| W-3 | **HD-1** wechselt von **OPEN** zu **COMPLETED** |
| W-4 | **NAW-1** wird fortgeschrieben: die ADR/RDR-Klassifikation ist damit **nicht mehr offen**; der Status der übrigen NAW-1-Positionen bleibt, wie in F-5 Kap. 18 festgehalten |
| W-5 | Der nächste, **gesondert zu autorisierende** Governance-Schritt ist damit identifiziert: **HD-4 — Erstellung des ADR-ENTWURFS** |

---

## 12. What the Decision Does NOT Do

**HD-1 bedeutet ausdrücklich NICHT:**

| # | Nicht bewirkt | Status bleibt |
|---|---|---|
| N-1 | ADR bereits **erstellt** | **NICHT ERSTELLT** — HD-4 offen |
| N-2 | ADR bereits **genehmigt** | **NICHT GENEHMIGT** |
| N-3 | Implementierung autorisiert | **NICHT AUTORISIERT** |
| N-4 | Coding autorisiert | **CODING NOT AUTHORIZED** |
| N-5 | RL-05 erreicht | **RL-05 NOT REACHED** |
| N-6 | Sprint-Plan geändert | **UNVERÄNDERT** |
| N-7 | Work Package erzeugt | **KEINES ERZEUGT** |
| N-8 | QG-006 bestanden | **QG-006 NOT STARTED** |
| N-9 | TD-19 geschlossen | **TD-19 PARTIALLY IMPACTED / OPEN** |
| N-10 | Security Finding geschlossen | **KEINES GESCHLOSSEN** |
| N-11 | ODD geschlossen | **KEINE geschlossen** |
| N-12 | Architecture Book geändert | **UNVERÄNDERT** |
| N-13 | Architecture Freeze aufgehoben | **ARCHITECTURE FREEZE UNCHANGED** |
| N-14 | OD-05 implementiert | **NICHT IMPLEMENTIERT** |

> **Keine dieser Positionen wird durch HD-1 berührt.** Alle bleiben unverändert.

### 12.1 Ausdrückliche Klarstellung zum ADR

Die Wahl des Instruments **ADR** autorisiert **nicht**:

- eine Änderung am **Architecture Book v2.0**,
- die Erstellung einer **Architecture-Book-Version v2.1** oder höher,
- eine Aufhebung oder Verengung des **Architecture Freeze**,
- eine Abweichung von **Bootstrap Baseline 1.0** vor Genehmigung des ADR.

Das ADR ist ein **Change-Control-Instrument**, kein Änderungsvollzug.

---

## 13. OD-05 Context

| Feld | Wert |
|---|---|
| Entscheidung | **GDR-OD05-001 — OD-05 = OPTION B** (FINAL) |
| Wortlaut | „Policy-Konfiguration in die bestehende `PluginSecurityStage` ziehen (ohne Reihenfolgeänderung)" |
| Reihenfolge | **unverändert** — konstitutiver Bestandteil von Option B |
| Beobachtbare Wirkung | `context.admitted_manifests` und der registrierte `PluginCatalog` werden **konfigurationsabhängig** → `run_phase()` = **CHANGED** (NAW-B, F-5 Kap. 9.1) |
| Ausgelöster §8-Tatbestand | **§8-4 TRIGGERED** |
| Change-Control-Pflicht | **CHANGE CONTROL REQUIRED** |
| Gewähltes Instrument | **ADR SELECTED** (dieser Record) |

> Der Inhalt von OD-05 Option B wird durch HD-1 **nicht** verändert, **nicht**
> erweitert und **nicht** ausgelegt.

---

## 14. Change Surface

**Die bereits finalisierte Change Surface bleibt unverändert. HD-1 erweitert sie
nicht und erfindet keine zusätzliche Datei.**

| ID | Artefakt | Zweck | Klasse |
|---|---|---|---|
| **CS-1** | `app/bootstrap/stages_plugin.py` — `PluginSecurityStage.execute` | Übergabe der konfigurierten Policies an die bestehende Security-Instanz | **REQUIRED** |
| **CS-2** | `config/settings.py` | Zugang zur `[security]`-Abbildung | **REQUIRED** |
| **CS-3** | `config/default.toml` | Optionaler `[security]`-Abschnitt | **REQUIRED** |

[SOURCE: `docs/governance/naw-a-od05-change-surface-fixation.md` Kap. 6;
`docs/governance/f-04-od05-td19-scope-assessment.md` Kap. 14;
F-5 Kap. 5.1, Finding F-5-01]

### 14.1 Bestehende Präzisierung — unverändert übernommen

> Der fehlende **`PermissionPolicy`**-Import innerhalb von **CS-1** ist **keine
> Change-Surface-Erweiterung**. Die Ergänzung läge **innerhalb von CS-1**; die
> importierte Datei selbst wird nicht verändert.
> [SOURCE: F-5 Kap. 5.2 „Präzisierung zu CS-1", Finding **F-5-02**]

| Prüfung | Ergebnis |
|---|---|
| **CHANGE-SURFACE EXPANSION** durch HD-1? | **NEIN** |
| Zusätzliche Datei als Teil der technischen Change Surface? | **KEINE** |
| Änderung an CS-1 / CS-2 / CS-3? | **KEINE** |

> **CHANGE SURFACE = CS-1 + CS-2 + CS-3 — FINAL.**

---

## 15. Architecture Freeze

| Prüfung | Ergebnis |
|---|---|
| Architecture Freeze | **ARCHITECTURE FREEZE UNCHANGED** |
| **F-1-A** | **bleibt gültig** — durch HD-1 weder bestätigt noch berührt in seinem Bestand |
| Architecture Book v2.0 | **nicht verändert** |
| Architecture Book v2.1 (oder höher) | **nicht erzeugt, nicht autorisiert, nicht impliziert** |
| Autorisiert das ADR automatisch eine Architecture-Book-Änderung? | **NEIN** — ausdrücklich nicht (Kap. 12.1) |
| AB §22.1 Freeze-Scope ↔ Change Surface | **keine Überschneidung** (F-5 Kap. 11) |
| AB §22.3 — ADR-pflichtige Änderungen | **keiner der sieben Tatbestände ausgelöst** (SF-8) |

> Die Wahl des Instruments **ADR** erfolgt **nicht** wegen eines
> AB-§22.3-Tatbestands — ein solcher liegt nach SF-8 **nicht** vor —, sondern als
> menschliche Governance-Entscheidung zur Ausfüllung der **§8-4**-Pflicht (SF-9).

---

## 16. TD-19 / Security Status

| Position | Status nach HD-1 |
|---|---|
| **TD-19** | **TD-19 PARTIALLY IMPACTED / OPEN** — unverändert |
| **F4-U2** (Einordnung der Policy-Diskontinuität) | **OFFEN** — unverändert |
| **T-a** (Instanz-Ersetzung) | **OPEN** |
| **T-b** (Trust-Ledger-Diskontinuität) | **OPEN** |
| **T-c** (Wirkungslosigkeit für Admission) | **OPEN** |
| **QG-006** | **QG-006 NOT STARTED** |
| **ODD-17 / OD-04** | **OPEN** |
| **TD-04** | **OPEN / NOT AUTHORIZED** |
| **TD-05 / TD-06 / TD-21** | **OPEN** |
| **SG-C / SG-D / SG-E** | **nicht erfüllt / nicht nachgewiesen** |
| **TG-2 / TG-3 / TG-4** | **erforderlich, nicht erbracht** |
| **RB-1.0** | **unverändert (258/14)** |

### 16.1 Ausdrückliche Nichtwirkung

Die ADR-Auswahl entscheidet **NICHT**:

- ob die Policy-Diskontinuität Bestandteil von **TD-19** ist,
- **T-a**,
- **T-b**,
- **T-c**,
- **QG-006**.

> Diese Punkte bleiben für **HD-3** bzw. spätere Governance-Arbeit **offen**.
> **Kein Security Finding wird geschlossen.** Keine Security-Freigabe wird erteilt.

---

## 17. Sprint Status

| Prüfung | Ergebnis |
|---|---|
| Sprint Plan 1.0 | **UNVERÄNDERT** (`DRAFT 1.0 R0`) |
| Ist der finalisierte OD-05-Umriss im genehmigten Sprint Plan abgedeckt? | **NEIN** — 0 Fundstellen; WP-003/WP-004-Deliverables decken ihn inhaltlich nicht [SOURCE: F-5 Kap. 17, Finding F-5-10] |
| Sprint hinzugefügt? | **NEIN** |
| Work Package hinzugefügt? | **NEIN** |
| Bestehende Zuordnung geändert? | **NEIN** |
| **HD-2** | **bleibt OFFEN** — wird **separat** entschieden |

---

## 18. Implementation Boundary

| Feld | Wert |
|---|---|
| **CODING** | **CODING NOT AUTHORIZED** |
| **RL-05** | **RL-05 NOT REACHED** |
| **QG-006** | **QG-006 NOT STARTED** |
| IP **GC-06** — genehmigte Governance-Entscheidung **vor** der Implementierung | **nicht erfüllt** — das ADR ist weder erstellt noch genehmigt (N-1, N-2) |
| IP §10.6 Bedingung 7 (genehmigte Sprintplanung) | **nicht erfüllt** |
| IP §10.6 Bedingung 8 (Baseline-Bestätigung / Phase A) | **nicht erfüllt** |
| IP §10.6 Bedingung 9 (**RL-05**) | **nicht erfüllt** |
| Tests | **NOT EXECUTED** |

> **HD-1 ist keine Implementierungsfreigabe.**
> Auch nach vollständiger Erstellung und Genehmigung des ADR folgte daraus
> **keine** Coding Authorization, solange **RL-05** nicht erreicht ist
> [SOURCE: F-5 Kap. 21, Finding F-5-12].

---

## 19. Remaining Open Decisions

| ID | Gegenstand | Status | Autorität |
|---|---|---|---|
| **HD-1** | **B-6 — ADR oder RDR?** | **COMPLETED — ADR SELECTED** | Projekteigner |
| **HD-2** | **Sprint-/WP-Zuordnung** des finalisierten Umrisses | **OPEN** | Projekteigner |
| **HD-3** | **F4-U2** — Einordnung der Policy-Diskontinuität in TD-19 | **OPEN** | Security-/Architektur-Governance |
| **HD-4** | **Erstellung des ADR-ENTWURFS** | **OPEN — NICHT AUTORISIERT** | Projekteigner / Governance |

**Weiterhin offene UNKNOWNs aus F-5 Kap. 19 — durch HD-1 unberührt:**

| ID | Gegenstand | Status |
|---|---|---|
| **F4-U1 / U-3** | „teilweise"-Restumfang von TD-19 | **UNKNOWN** |
| **F4-U2** | Policy-Diskontinuität ↔ TD-19 | **UNKNOWN / HUMAN REVIEW REQUIRED** |
| **F4-U3** | künftiger Konsument der FINALIZE-Instanz | **UNKNOWN** |
| **NAW-A-U1** | CS-2-Varianten **V-1** / **V-2** | **OFFEN** |
| **NAW-A-U2 / C-3** | Z-1 (`save_profile`), Z-2 (einstufiger `_merge`), Typprüfung an der `[security]`-Zugriffsstelle | **OFFEN** |
| **F5-U1** | Sprint-/WP-Zuordnung | **OPEN** (= HD-2) |

> **B-6 / F4-U4** ist die **einzige** Position, die durch HD-1 aufgelöst wird.

---

## 20. Next Authorized Step

| # | Schritt | Gegenstand | Status |
|---|---|---|---|
| **1** | **HD-4 — Erstellung des ADR-ENTWURFS** | Ausarbeitung des mit HD-1 gewählten Instruments für OD-05 Option B | **NÄCHSTER SCHRITT — gesondert zu autorisieren; NICHT Bestandteil von HD-1** |
| **2** | **HD-2 — Sprint-/WP-Zuordnung** | Der Umriss ist im Sprint Plan nicht abgedeckt | **OPEN** — unabhängig, parallel führbar |
| **3** | **HD-3 — F4-U2 / TD-19-Einordnung** | Einordnung der Policy-Diskontinuität | **OPEN** — unabhängig, parallel führbar |
| **4** | **Genehmigung des ADR** | nach HD-4 | **NICHT ERTEILT** |
| **5** | **Umsetzungsautorisierung** | erst nach 1–4 **und** Erreichen von **RL-05** (IP §10.6 Bedingungen 7–9) | **NICHT ERTEILT** |

> **HD-4 ist nicht Bestandteil dieses Auftrags. Mit HD-1 wurde kein ADR erstellt.**
> Dieser Record dokumentiert **ausschließlich**, dass ein **ADR** das gewählte
> Instrument sein soll.

---

## 21. Repository Integrity

| Prüfung | Vor HD-1 | Nach HD-1 |
|---|---|---|
| HEAD | `8fcf42f1997dfcf6ff232e75fd33c37b933991c8` | **unverändert** |
| Baseline-Hash | `8fcf42f1997dfcf6ff232e75fd33c37b933991c8` | **unverändert** |
| `git diff --stat` | 6 files, +1.415/−119 | **unverändert** |
| `git diff --cached --stat` | leer | **leer — kein Staging** |
| Getrackte Modifikationen | 6 | **6** |
| Untracked | *n* | ***n* + 1** — **ausschließlich** dieses Dokument |
| Bestandsdateien geändert | — | **0** |
| Neue Dateien | — | **genau 1**: `docs/governance/hd-1-adr-rdr-decision.md` |
| ADR erstellt | — | **NEIN** |
| RDR erstellt | — | **NEIN** |
| Produktivcode / Tests / Konfiguration | — | **unverändert** |
| Sprint Plan / Architecture Book / TD-Einträge / ODDs / Findings / Quality Gates | — | **unverändert, keines geschlossen** |
| `src/jochen_x/**` | 0 Statuseinträge | **0 — vollständig unangetastet** |
| Commit / Tag / Push / Cleanup / Löschen / Verschieben / Umbenennen | — | **KEINE** |

---

## 22. Final Status

| Feld | Wert |
|---|---|
| **HD-1** | **COMPLETED** |
| **B-6** | **RESOLVED — ADR SELECTED** |
| **ADR/RDR classification** | **ADR SELECTED** |
| **Entscheidungsklasse** | **HUMAN GOVERNANCE DECISION** (Projekteigner) |
| **OD-05** | **OD-05 OPTION B** — unverändert |
| **CHANGE SURFACE** | **CS-1 + CS-2 + CS-3** — FINAL, keine Erweiterung |
| **§8-4** | **§8-4 TRIGGERED** |
| **§8-1 / §8-2 / §8-3 / §8-5** | **NOT TRIGGERED** |
| **CHANGE CONTROL** | **CHANGE CONTROL REQUIRED** |
| **ADR erstellt** | **NEIN** (HD-4 offen) |
| **ADR genehmigt** | **NEIN** |
| **ARCHITECTURE FREEZE** | **ARCHITECTURE FREEZE UNCHANGED** |
| **Architecture Book** | **unverändert** — keine v2.1 |
| **TD-19** | **TD-19 PARTIALLY IMPACTED / OPEN** |
| **F4-U2** | **OFFEN** (HD-3) |
| **QG-006** | **QG-006 NOT STARTED** |
| **RL-05** | **RL-05 NOT REACHED** |
| **CODING** | **CODING NOT AUTHORIZED** |
| **Sprint Plan** | **unverändert** — HD-2 offen |
| **RB-1.0** | **unverändert (258/14)** |
| **TESTS** | **NOT EXECUTED** |
| **HD-2 / HD-3 / HD-4** | **OFFEN** |
| **Nächster autorisierter Schritt** | **HD-4 — Erstellung des ADR-ENTWURFS** (gesondert zu autorisieren) |

---

**Ende HD-1 — Governance-Entscheidungsrecord ADR/RDR (B-6) — JOCHEN X
Milestone 1.0 (FINAL, 2026-08-10) — Bezugs-Baseline
`MILESTONE-1.0-BASELINE = 8fcf42f1997dfcf6ff232e75fd33c37b933991c8`**
