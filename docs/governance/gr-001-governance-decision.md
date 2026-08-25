# GDR-002 — GR-001 Governance Decision
## Paralleler Artefaktbaum außerhalb der normativen Baseline

## 1. Document Metadata

| Feld | Wert |
|---|---|
| Dokumenttyp | Governance Decision Record |
| **Decision ID** | **GDR-002** |
| Gegenstand | **GR-001** — Paralleler Artefaktbaum außerhalb der normativen Baseline |
| Status dieses Records | **FINAL — ENTSCHIEDEN** |
| Datum | 2026-08-09 |
| Entscheidungsinstanz | Governance Architect / Release Authority (gemäß Implementation Plan 1.0, Kap. 11.10 und PR-001.9); beauftragt durch den Projekteigner JOCHEN X |
| Wirkung | Dokumentierte Governance-Entscheidung zu GR-001 gemäß PR-001.7. **Keine** technische Umsetzung, **keine** Änderung bestehender Dateien, **keine** weitere Governance-Frage wird entschieden. |

---

## 2. Decision Subject

Ausschließlich **GR-001**: die im genehmigten Implementation Plan 1.0 R1.2
(Kap. 5.5.4 / GB-001, Kap. 11.10, Kap. 11.11, Anhang A / PR-001.1–PR-001.9)
dokumentierte, ausstehende Entscheidung über den parallelen Artefaktbaum
`src/jochen_x/**`. Keine andere Governance-Frage ist Gegenstand dieses
Records (siehe Kap. 13, 18, 19).

---

## 3. Source Gate

| # | Quelle | Status | Verifikation |
|---|---|---|---|
| 1 | `docs/milestone-1.0-implementation-plan.md` | APPROVED R1.2 (2026-08-06) | Kap. 5.5.4, 11.10, 11.11, Anhang A (PR-001.1–PR-001.9) vollständig gelesen |
| 2 | `docs/governance/milestone-1.0-governance-closing-report-w8.md` | GOVERNANCE CLOSED | §7 (GR-001-Vorbedingung), §8 gelesen |
| 3 | `docs/governance/implementation-plan-1.0-approval-record.md` | vorhanden | Existenz und Genehmigungskette (W-6/W-7) verifiziert |
| 4 | `docs/development-standard-v1.1.md` | APPROVED | Kopf verifiziert |
| 5 | `docs/milestone-1.0-charter.md` | APPROVED (2026-08-02, per Status Summary) | Existenz verifiziert |
| 6 | `docs/governance/waiver-dev-001.md` | APPROVED, aktiv | Kopf gelesen |
| 7 | `docs/governance/waiver-amendment-001.md` | APPROVED | Kopf gelesen |
| 8 | `docs/governance/gdr-001-waiver-closing-criteria.md` | ENTSCHIEDEN — Option B | Kopf gelesen |
| 9 | `docs/governance/jochen-x-next-authorized-work-assessment.md` | FINAL ASSESSMENT | GR-001 = PENDING DECISION bestätigt |

**Unabhängige Sachverhaltsverifikation (read-only, 2026-08-09):**
`src/jochen_x/**` existiert als in sich geschlossener zweiter Baum
(66 Python-Dateien; eigene Kernstruktur `core/` mit u. a. `concurrency`,
`di`, `events`, `plugin`, `recovery`, `registry`, `runtime`, `security`).
`main.py` (Anwendungseinstiegspunkt) enthält **keine** Referenz auf
`src/jochen_x`. Der Befund GB-001 des Plans ist damit unabhängig bestätigt.

**Source Gate: BESTANDEN.**

---

## 4. Background

Während der Module-Work-Breakdown-Analyse des Implementation Plan 1.0 wurde
festgestellt (GB-001, Kap. 5.5.4): Das Repository enthält neben der von
Bootstrap Baseline 1.0 und Architecture Book v2.0 beschriebenen
Paketstruktur (baseline-geführte Struktur: `core/`, `app/`, `plugins/`,
`sdk/`, `services/`, `developer/`, `ui/`, `config/`, `database/` …) einen
zweiten, in sich geschlossenen Artefaktbaum unter `src/jochen_x/**` mit
eigenem Testbestand. Dieser Baum wird vom Anwendungseinstiegspunkt nicht
referenziert und ist in keiner normativen Eingabe des Plans beschrieben.

Der Befund wurde als Risiko **GR-001** (Klasse RK-04 Governance,
Kritikalität Hoch, Status PENDING DECISION) in das konsolidierte
Risikoregister (Kap. 11.11) überführt; die normative Pending Resolution
PR-001.1–PR-001.9 steht in Anhang A. Die Entscheidung lag ausdrücklich
außerhalb der Autorisierungsgrenze des Plans (Kap. 1.6, PP-04) und war als
separater Governance-Entscheid zu treffen — dieser liegt hiermit vor.

---

## 5. GR-001 Problem Statement (aus den Quellen)

Nicht entschieden war (PR-001.1/PR-001.2):

1. Welcher Artefaktbaum ist produktiver Bestandteil des Milestone 1.0?
2. Welchen Status hat der jeweils andere Baum — Erhaltung, Stilllegung
   oder Überführung?
3. Welcher Testbestand bildet die verbindliche Regressionsbasis?
4. Ist zur Umsetzung ein ADR oder RDR erforderlich?

Mögliche Auswirkungen ohne Entscheidung (Anhang A): unklare
Regressionsbasis, uneindeutige Modulzuordnung, mögliche Doppelpflege,
unklare Scope-Abdeckung, erschwerte Traceability. Betroffen: Regressions-
bezugsgröße (1019 Tests umfassen Artefakte beider Bäume), QG-007 (Ende
Phase B), GV-08 (Phase D), Beginn der Sprintplanung (blockierend,
PR-001.8).

---

## 6. Verified Source Position

- Sämtliche Deltas und die gesamte Modulzuordnung des genehmigten Plans
  sind ausschließlich der **baseline-geführten Struktur** zugeordnet
  (Kap. 5.5.4; PR-001.4).
- `src/jochen_x/**` ist nicht Bestandteil von Bootstrap Baseline 1.0,
  Engineering Specification 1.0 oder Architecture Book v2.0 und wird von
  keiner normativen Eingabe referenziert (PR-001.1).
- Die Baseline-Bestätigung (Kap. 3.2) erfolgt gegen die baseline-geführte
  Struktur.
- PR-001.4 beschreibt beide Entscheidungsfolgen: Bei Entscheidung
  zugunsten der baseline-geführten Struktur ist die Regressionsbezugsgröße
  auf deren Testbestand einzugrenzen; bei abweichender Entscheidung wären
  Delta Analysis und Module Work Breakdown neu zu führen.
- PR-001.8: Eine Entscheidung, die die Baseline **berührt**, erfordert
  ADR oder RDR; solange keine Baseline-Berührung vorliegt, sind Baseline,
  Architecture Book und ADRs nicht betroffen.
- Frist (PR-001.7): maßgeblich **vor Beginn der Sprintplanung**;
  Rückfallgrenzen Ende Phase B und vor Phase D. Die Frist ist gewahrt —
  die Sprintplanung hat nicht begonnen.

---

## 7. Available Decision Options (aus den Quellen übernommen)

Die Optionsstruktur stammt vollständig aus PR-001.2; es wurden keine
künstlichen Optionen erfunden:

- **Frage 1:** baseline-geführte Struktur **oder** `src/jochen_x/**` als
  produktiver Baum.
- **Frage 2:** für den jeweils anderen Baum — **Erhaltung, Stilllegung
  oder Überführung** (wörtlich PR-001.2).
- **Frage 3:** Regressionsbasis folgt der Entscheidung zu Frage 1
  (PR-001.4).
- **Frage 4:** ADR/RDR nur bei Baseline-Berührung (PR-001.2, PR-001.8;
  Change Control der Bootstrap Baseline).

---

## 8. Decision

Die Entscheidungsinstanz entscheidet GR-001 wie folgt:

> **D-1 (Frage 1):** Produktiver Artefaktbaum des Milestone 1.0 ist
> ausschließlich die **baseline-geführte Struktur** gemäß Bootstrap
> Baseline 1.0 und Architecture Book v2.0 — die Struktur, der sämtliche
> Deltas und die vollständige Modulzuordnung des genehmigten
> Implementation Plan 1.0 R1.2 bereits zugeordnet sind.
>
> **D-2 (Frage 2):** Der parallele Artefaktbaum `src/jochen_x/**` erhält
> den Status **STILLLEGUNG**: Er ist **kein** produktiver Bestandteil des
> Milestone 1.0, wird nicht weitergepflegt, ist keinem Delta und keinem
> Work Package zugeordnet und begründet keine Scope-, Baseline- oder
> Spezifikationswirkung. Die **physische Behandlung** (Entfernung,
> Verschiebung oder Archivierung der Dateien) ist **nicht** Teil dieser
> Entscheidung; sie ist separat zu autorisierende Arbeit.
>
> **D-3 (Frage 3):** Die verbindliche Regressionsbasis des Milestone 1.0
> ist der der **baseline-geführten Struktur zugeordnete Testbestand**.
> Die Repository-Gesamtzahl von 1019 Tests bleibt als Kennzahl bestehen,
> ist aber nicht die Regressionsbezugsgröße (PR-001.4). Die zahlenmäßige
> **Festlegung der Bezugsgröße** erfolgt gemäß Kap. 11.10 (Completion) als
> nachgelagerter Schritt zu Beginn der Sprintplanung; die Regressionsregeln
> aus Kap. 9.6 gelten unverändert.
>
> **D-4 (Frage 4):** Ein ADR oder RDR ist **nicht erforderlich.** Die
> Entscheidung bestätigt die bestehende, genehmigte Baseline-Struktur und
> berührt weder Bootstrap Baseline 1.0 noch Architecture Book v2.0 noch
> Engineering Specification 1.0 (PR-001.8). Es wird nichts an der Baseline
> geändert.

**Begründung:** Die baseline-geführte Struktur ist die einzige von allen
normativen Quellen (Baseline, Architecture Book, Engineering Specification,
Implementation Plan) beschriebene und vom Anwendungseinstiegspunkt
referenzierte Struktur; `src/jochen_x/**` ist unreferenziert und normativ
unbeschrieben (unabhängig verifiziert, Kap. 3). Jede abweichende
Entscheidung würde Delta Analysis und Module Work Breakdown des soeben
genehmigten Plans neu aufreißen (PR-001.4) und eine Baseline-Änderung mit
ADR/RDR-Pflicht auslösen — ohne dass eine Quelle dafür einen Bedarf
ausweist. Die Stilllegung (statt Erhaltung) vermeidet die in Anhang A
benannte Doppelpflege; die Überführung wäre Implementierungsarbeit ohne
Autorisierung.

---

## 9. Decision Authority · 10. Decision Date

| Feld | Wert |
|---|---|
| Approval Authority | **Governance Architect / Release Authority** — die in Implementation Plan 1.0 Kap. 11.10 und PR-001.9 ausdrücklich benannte Entscheidungsinstanz für GR-001; tätig auf Auftrag des Projekteigners JOCHEN X. ADR/RDR-Mitwirkung nicht erforderlich, da keine Baseline-Berührung (D-4). |
| Entscheidungsdatum | **2026-08-09** |
| Status vorher | **PENDING DECISION** (verifiziert: Kap. 11.10/11.11, Anhang A, W-8 §7, Assessment) |
| Status nachher | **DECIDED** — dokumentierte Entscheidung gemäß PR-001.7 liegt vor (dieses Dokument) |

---

## 11. Governance Effect

1. Die gemäß PR-001.7 maßgebliche Frist („vor Beginn der Sprintplanung")
   ist gewahrt; die geforderte **dokumentierte Entscheidung zu GR-001
   liegt vor.**
2. Die Vorbedingung aus W-8 §7 für den tatsächlichen Beginn der
   Sprint-Planning-Phase (RL-04, Kriterium „dokumentierte Entscheidung zu
   GR-001 gemäß PR-001.7") ist **erfüllt.**
3. Die GV-08-Blockade über GR-001 (PR-001.6: „nicht erfüllbar, solange
   PENDING DECISION") ist **aufgehoben**; die Bestätigung von GV-08 selbst
   erfolgt unverändert erst zum vorgesehenen Zeitpunkt (Phase D).
4. QG-007 erhält eine eindeutige Grundlage: Die Regressionsbezugsgröße ist
   dem Grunde nach bestimmt (D-3); ihre zahlenmäßige Festlegung ist der
   nächste vorgesehene Schritt (Kap. 11.10 Completion).
5. Das Risikoregister des Implementation Plans (Kap. 11.11) wird durch
   diesen Record **nicht physisch verändert** — der Plan ist APPROVED und
   bleibt unangetastet. Die Statusnachführung des Registereintrags kann
   nur über den dafür vorgesehenen kontrollierten Prozess erfolgen; bis
   dahin gilt: Registereintrag PENDING DECISION + dieser Record = Status
   DECIDED (dieser Record ist die von PR-001.7/RL-04/GV-08 geforderte
   dokumentierte Entscheidung).

---

## 12. Explicit Non-Effects

Diese Entscheidung bedeutet **nicht**:

- Sprint wurde gestartet oder geplant
- Coding-Freigabe (W-8 §7: Coding bleibt bis zur separaten Freigabe nicht autorisiert)
- Runtime-Änderung, Deployment-, Release-Freigabe
- Trading-Live-Gang, Wallet-Transfers, Echtgeldzugriff
- Genehmigung von Security-ADRs oder einer Engineering Specification
- physische Entfernung, Verschiebung oder Archivierung von `src/jochen_x/**`
- Änderung von Baseline, Architecture Book, Engineering Specification, Scope, Requirements, Quality Gates oder Deliverables
- Schließung anderer Findings, ODDs oder Governance-Fragen

---

## 13. Impact on Sprint Planning · RL-04 / GV-08

| Gegenstand | Wirkung |
|---|---|
| Sprint Planning | Die GR-001-Blockade (PR-001.8 „blockierend ohne dokumentierte Entscheidung") ist beseitigt. Der **Start** der Sprintplanung erfolgt dennoch **nicht automatisch** — er bedarf der ausdrücklichen Entscheidung des Projekteigners. |
| RL-04 | GR-001-Kriterium erfüllt (dokumentierte Entscheidung gemäß PR-001.7 liegt vor). Übrige RL-04-Kriterien unberührt. |
| GV-08 | Über GR-001 nicht mehr blockiert; Bestätigung erfolgt regulär in Phase D. |
| QG-007 | Bezugsgröße dem Grunde nach eindeutig; zahlenmäßige Festlegung als Folgeschritt bei Sprintplanungsbeginn. |

---

## 14. Relationship to Waivers

| Waiver / Record | Zusammenhang | Wirkung dieser Entscheidung |
|---|---|---|
| WAIVER-DEV-001 (APPROVED, aktiv) | Betrifft die Zuweisung von Delta Analysis / Module Work Breakdown an den Implementation Plan — nicht den parallelen Artefaktbaum | **Keine.** Keine Neuinterpretation, keine Änderung |
| WAIVER-AMENDMENT-001 (APPROVED) | Präzisierung der Closing Criteria von WAIVER-DEV-001 | **Keine** |
| GDR-001 (ENTSCHIEDEN, Option B) | Auslegung der Closing Criteria §9 (1)/(2) von WAIVER-DEV-001 | **Keine.** GDR-002 steht neben GDR-001, ändert es nicht |

GR-001 hat nach den Quellen keine Bedingung, die einen Waiver verändert;
es besteht keine Wechselwirkung, die hier zu entscheiden wäre.

---

## 15. Relationship to Milestone 1.0

Die Genehmigung des Implementation Plan 1.0 R1.2 war durch GR-001 nicht
blockiert (PR-001.8) und wird durch diese Entscheidung rückwirkend weder
in Frage gestellt noch verändert. Betroffen war ausschließlich der
Milestone-**Fortschritt** (Sprintplanung, QG-007, GV-08) — diese Blockade
ist mit diesem Record beseitigt. Es entsteht keine neue Milestone-Phase
und keine neue Reifegraddefinition.

---

## 16. Security-Stream Non-Impact

Die geschlossenen Security-Governance-Zyklen bleiben unangetastet:
Core Principles 1.0 (APPROVED/CLOSED), Security Architecture 1.0
(APPROVED/CLOSED), Security Design 1.0 (APPROVED/CLOSED). Aus GR-001
werden keine Security-Entscheidungen abgeleitet; insbesondere werden
keine Security-ADRs autorisiert, keine Security-Design-ODDs geschlossen
und keine Security Corrections durchgeführt.

---

## 17. Remaining Open Items (unverändert offen)

SD-W1-F-04 · SD-W1-F-06 · SA-W1-F01 · SA-W1-F03 · SA-W1-F04 ·
ODD-01–ODD-20 · GF-02 · GF-03 · GC-02–GC-07 · GQ-1 · GQ-2 · GQ-3 ·
WAIVER-DEV-001 §9 (3) (an Sprint-Realität gebunden) · zahlenmäßige
Festlegung der Regressionsbezugsgröße (Folgeschritt gemäß Kap. 11.10).

Keiner dieser Punkte wird durch GDR-002 geschlossen.

---

## 18. Verification

| Prüfung | Ergebnis |
|---|---|
| GR-001 war vorher PENDING DECISION | PASS (Kap. 11.10/11.11, Anhang A, W-8, Assessment) |
| Entscheidung entspricht den Primärquellen (Optionsraum PR-001.2, Folgen PR-001.4/.8) | PASS |
| Keine andere Governance-Frage entschieden | PASS |
| Keine bestehende Datei verändert (einzige neue Datei: dieses Dokument) | PASS |
| Keine neue Governance-Regel, keine neue Dokumentklasse, keine neue Rangstufe | PASS |
| Keine Security-ODD geschlossen, kein Security-ADR erstellt | PASS |
| Keine Engineering Specification erstellt | PASS |
| Keine Implementierung gestartet, keine Coding-Freigabe erzeugt | PASS |
| Kein Trading-/Wallet-/Echtgeldzugriff freigegeben | PASS |
| Kein Commit, kein Tag, kein Push, kein Merge, kein Rebase | PASS |

---

## 19. Final Decision Status

> **GR-001: DECIDED (GDR-002, 2026-08-09).**
>
> Produktiver Baum: baseline-geführte Struktur · `src/jochen_x/**`:
> Stilllegung (physische Behandlung separat zu autorisieren) ·
> Regressionsbasis: Testbestand der baseline-geführten Struktur
> (zahlenmäßige Festlegung als Folgeschritt) · Kein ADR/RDR erforderlich.

Nächster Schritt: **ausschließlich nach ausdrücklicher Entscheidung des
Projekteigners** (insbesondere Start der Sprint-Planning-Phase). Kein
automatischer Folgeauftrag.

---

**Ende GDR-002 — GR-001 Governance Decision (FINAL, 2026-08-09)**
