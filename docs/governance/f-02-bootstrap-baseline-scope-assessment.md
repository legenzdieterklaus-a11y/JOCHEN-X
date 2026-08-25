# JOCHEN X — Milestone 1.0
# F-2 — Bootstrap Baseline §8-4 — Autoritative Auslegung des Änderungsumfangs

## 1. Assessment Identity

| Feld | Wert |
|---|---|
| Dokumenttyp | Governance / Architecture Assessment (READ-ONLY) |
| **Assessment ID** | **F-2** |
| Titel | Bootstrap Baseline §8-4 — Autoritative Auslegung des Änderungsumfangs |
| Status | **FINAL ASSESSMENT** |
| Untersuchter Gegenstand | Reichweite des Schutzbegriffs „**BootstrapManager (API-Signatur, Verhalten)**" [SOURCE: docs/baselines/bootstrap-baseline-1.0.md §8, Zeile 209] |
| Referenz | **NAW-1** B-2 · **F-1** (F-1-A) · **GDR-OD05-001** (Option B) |
| Datum | 2026-08-10 |
| Branch / HEAD | `milestone-1.0-governance` / `8fcf42f1997dfcf6ff232e75fd33c37b933991c8` |
| **Ergebnis** | **F-2-B — §8-4 PARTIALLY DEFINED** (Kap. 16) |
| Normcharakter | Dieses Dokument ist ein **Assessment**, **keine neue Governance-Norm**. Es definiert nichts, es stellt fest |

> **Dieses Assessment trifft keine Entscheidung.** Es entscheidet weder OD-05 noch
> B-1, B-3, B-4, B-6, B-7, noch erzeugt es eine Auslegungsregel. Wo die Quellen
> keine Antwort tragen, bleibt **UNKNOWN / HUMAN REVIEW REQUIRED** stehen.

---

## 2. Executive Result

> ## **F-2-B — §8-4 PARTIALLY DEFINED**

| Ebene | Befund | Sicherheit |
|---|---|---|
| **„API-Signatur"** (erste Hälfte von §8-4) | Erfasst die öffentliche Signatur des `BootstrapManager`: das Dataclass-Feld `stages` und die drei Methoden `begin()`, `run_phase()`, `build_context()`. Durch Implementation Plan **API-04** ausdrücklich bestätigt | **DETERMINATE** |
| **„Verhalten"** — öffentlich beobachtbares Verhalten von `begin()` / `run_phase()` / `build_context()` | **erfasst** — gestützt durch den Wortlaut und die einzige Konkretisierung in einer autoritativen Quelle (RDR-001 Invariante 5) | **PARTIALLY DETERMINATE** |
| **„Verhalten"** — Stage-Zusammensetzung / Stage-Reihenfolge | §8 enthält **eigene** Tatbestände hierfür (§8-2, §8-5). Ob §8-4 sie **zusätzlich** erfasst, ist nicht geregelt — **praktisch folgenlos**, da ohnehin unter Change Control | **NOT COVERED durch §8-4** (Schutz besteht über §8-2/§8-5) |
| **„Verhalten"** — **Stage-interne Logik** | **Keine Quelle regelt dies.** Zwei autoritative Quellen weisen in **entgegengesetzte Richtungen** (Kap. 15.3) | **UNKNOWN / HUMAN REVIEW REQUIRED** |
| **„Verhalten"** — interne Orchestrierungslogik des Managers | nicht adressiert | **UNKNOWN** |
| **„Verhalten"** — indirekte Wirkungen (Lifecycle, Error, Events, Shutdown) | nicht adressiert; für Option B potenziell einschlägig (Kap. 13) | **UNKNOWN** |

**Kernbefund:** Der Begriff „Verhalten" kommt in der Bootstrap Baseline 1.0
**genau einmal** vor — in §8-4 selbst. Es existiert dort **keine Definition,
kein Beispiel, keine Positiv- und keine Negativliste**
[SOURCE: docs/baselines/bootstrap-baseline-1.0.md, Volltextprüfung „Verhalten": 1 Treffer, Zeile 209].
Im Development Standard v1.1 kommt der Begriff **überhaupt nicht** vor
[SOURCE: docs/development-standard-v1.1.md, Volltextprüfung: 0 Treffer].

**Die für OD-05 Option B entscheidende Teilfrage — ob Stage-interne Logik von
§8-4 erfasst ist — bleibt offen.** Die Regelungslücke aus NAW-1 B-2 ist damit
**bestätigt, präzisiert und eingegrenzt, aber nicht geschlossen.**

---

## 3. Source Gate

### 3.1 Pflichtquellen (18)

| # | Quelle | Pfad | Status/Version | Verifikation |
|---|---|---|---|---|
| 1 | Bootstrap Baseline 1.0 | `docs/baselines/bootstrap-baseline-1.0.md` | **APPROVED**, BOOTSTRAP-BASELINE-1.0, 2026-08-01 | **vollständig gelesen** (227 Z.); §1–§9; §8 im Wortlaut |
| 2 | Development Standard v1.1 | `docs/development-standard-v1.1.md` | **APPROVED** v1.1, 2026-07-27 | §13 im Wortlaut; Volltextsuche „Verhalten" |
| 3 | Architecture Book v2.0 | `docs/architecture-book-v2.md` | **APPROVED / FROZEN** v2.0 | **Welt A** verwendet (Kap. 3.3); §22.1–§22.3, §9, Glossar |
| 4 | NAW-1 | `docs/governance/naw-01-od05-adr-rdr-assessment.md` | **FINAL ASSESSMENT** | Kap. 6, 12 (B-1…B-7), 13 |
| 5 | F-1 | `docs/governance/f-01-od05-architecture-freeze-assessment.md` | **FINAL ASSESSMENT** (F-1-A) | Kap. 10, 11.3 |
| 6 | OD-05 Decision | `docs/governance/od-05-governance-decision.md` | **FINAL** (GDR-OD05-001) | Kap. 4, 6, 8, 11, 17 |
| 7 | Decision Briefs R0 | `docs/audits/jochen-x-decision-briefs-r0.md` | R0 | Brief 4 (OD-05) |
| 8 | Master Engineering Plan R0 | `docs/audits/jochen-x-master-engineering-plan-r0.md` | R0 | §10.6, §19.1, §20 OD-05, §24.2 |
| 9 | Decision Execution Matrix R0 | `docs/audits/jochen-x-decision-execution-matrix-r0.md` | R0 | §D-3 |
| 10 | OD-01 Decision | `docs/governance/od-01-governance-decision.md` | **FINAL** (GDR-OD01-001) | Kap. 8 (Fassungsregel) |
| 11 | GR-001 / GDR-002 | `docs/governance/gr-001-governance-decision.md` | **FINAL — ENTSCHIEDEN** | §2, §12 (Scope-Begrenzung) |
| 12 | Baseline Commit Record | `docs/governance/milestone-1.0-baseline-commit-record.md` | **FINAL** | §5, §6, §10 |
| 13 | Baseline Identifier Decision | `docs/governance/milestone-1.0-baseline-identifier-decision.md` | **FINAL** (GDR-003) | §2, §6 |
| 14 | Implementation Plan 1.0 | `docs/milestone-1.0-implementation-plan.md` | **APPROVED R1.2**, 2026-08-06 | §3.4 **API-04**, §3.5 BP-01…BP-04, BI-03, GC-06 |
| 15 | Sprint Plan 1.0 | `docs/milestone-1.0-sprint-plan.md` | **DRAFT 1.0 R0**, als Planungsgrundlage genehmigt | Volltextprüfung auf §8-Regeln |
| 16 | Engineering Specification 1.0 | `docs/milestone-1.0-engineering-spec.md` | **APPROVED**, ES-1.0 R1 | §393-Passage, §132, §224 |
| 17 | Sprint Planning Summary R0 | `docs/audits/milestone-1.0-sprint-planning-summary-r0.md` | Creation/Planning Summary, 2026-08-09 | Kopf verifiziert |
| 18 | Next Authorized Work Assessment | **`docs/governance/`**`jochen-x-next-authorized-work-assessment.md` | **FINAL ASSESSMENT**, 2026-08-09 | **Pfadabweichung, siehe 3.2** |

**Zusatzquelle (nicht in der Pflichtliste, für die Auslegung wesentlich):**
`docs/rdr/001-bootstrap-modularization.md` — **APPROVED** (2026-08-01). Aufgenommen,
weil Bootstrap Baseline §1 die Baseline ausdrücklich als Ergebnis von RDR-001
ausweist und §6 RDR-001 als Governance-Referenz führt
[SOURCE: docs/baselines/bootstrap-baseline-1.0.md §1, §6].

### 3.2 Pfadabweichung

| Auftrag nennt | Tatsächlicher Pfad | Verifikation |
|---|---|---|
| `docs/audits/jochen-x-next-authorized-work-assessment.md` | **`docs/governance/jochen-x-next-authorized-work-assessment.md`** | Inhaltlich verifiziert: „JOCHEN X — Governance Status & Next Authorized Work Assessment", Status **FINAL ASSESSMENT**, 2026-08-09. **Eindeutig identifizierbar** |

Der Pfad unter `docs/audits/` existiert nicht. Es handelt sich um eine
Pfadabweichung, **nicht** um eine fehlende Pflichtquelle. **Kein HARD STOP.**

### 3.3 Fassungsentscheidung Architecture Book

`docs/architecture-book-v2.md` ist im Working Tree modifiziert (Welt B) und
Gegenstand der per **GDR-OD01-001 (Option C)** getrennt zu führenden, **noch
nicht erfolgten** Disposition. Es wird daher — wie bereits in F-1 — **keine
eigenständige Fassungsentscheidung getroffen**, sondern die bestehende Regel
angewandt: maßgeblich ist die autoritative Fassung **Welt A**
(`git show 8fcf42f:docs/architecture-book-v2.md`, read-only entnommen)
[SOURCE: docs/governance/od-01-governance-decision.md Kap. 8; docs/governance/f-01-od05-architecture-freeze-assessment.md Kap. 2.2].

> **SOURCE GATE: BESTANDEN.** 18/18 Pflichtquellen vorhanden, eine Pfadabweichung
> dokumentiert und aufgelöst.

---

## 4. Baseline Verification

| Prüfung | Ergebnis |
|---|---|
| Baseline-Identifier | `MILESTONE-1.0-BASELINE = 8fcf42f1997dfcf6ff232e75fd33c37b933991c8` [SOURCE: docs/governance/milestone-1.0-baseline-commit-record.md §6] |
| Reproduzierbarkeit | `git cat-file -t 8fcf42f…` → `commit`; HEAD identisch. **PASS** |
| HEAD vor Beginn | `8fcf42f1997dfcf6ff232e75fd33c37b933991c8` |
| Staging vor Beginn | **leer** (`git diff --cached --stat` ohne Ausgabe) |

**Drei-Ebenen-Trennung** [SOURCE: docs/audits/jochen-x-master-engineering-plan-r0.md §4.1]:

| Ebene | Umfang | Verwendung in F-2 |
|---|---|---|
| **BASELINE (Welt A)** | `8fcf42f…` | **Alleinige Grundlage** aller Code- und AB-Aussagen |
| **WORKING TREE (Welt B)** | 6 getrackte Modifikationen, +1.415/−119 (unabhängig reproduziert per `git diff --stat`) | **Nur als Zusatzbefund**; verändert die Baseline nicht |
| **UNTRACKED (Welt C)** | Governance-/Audit-/Planungsdokumente unter `docs/**` | Statuswerte gelten; keine Implementierungswirkung |

**Zusatzbefund Welt B (verändert nichts):** Die sechs Modifikationen betreffen
`CLAUDE.md`, `ROADMAP.md`, ADR-005/006/007, `docs/architecture-book-v2.md`.
**Kein Bootstrap-Artefakt** ist darunter — der in F-2 untersuchte Code ist im
Working Tree **baseline-identisch**
[SOURCE: docs/audits/jochen-x-master-engineering-plan-r0.md §3.3 BV-01].

---

## 5. F-2 Question / Scope

**Untersuchte Frage — ausschließlich diese:**

> Was schützt Bootstrap Baseline 1.0 §8-4 mit dem Begriff
> „**BootstrapManager (API-Signatur, Verhalten)**" konkret?

**Untersuchungsgegenstand: ausschließlich NAW-1 B-2.**

**Ausdrücklich nicht untersucht und nicht entschieden:** B-1 (neues öffentliches
Symbol), B-3 (`default_stages()`-Zusammensetzung), B-4 (TD-19 /
`SecurityBootstrapStage`), B-6 (ADR-↔-RDR-Kriterium), B-7 (AB §9 ↔ Stage-Anzahl)
[SOURCE: docs/governance/naw-01-od05-adr-rdr-assessment.md Kap. 12].

**Verhältnis zu F-1:** F-1 ist abgeschlossen mit **F-1-A — ARCHITECTURE FREEZE
NOT TOUCHED**. Architecture Freeze und Bootstrap Baseline sind **verschiedene
Governance-Instrumente mit verschiedenen Schutzbereichen**
[SOURCE: docs/governance/f-01-od05-architecture-freeze-assessment.md Kap. 11.3].
**F-1 wird in F-2 nicht zur Erweiterung oder Verengung von §8-4 herangezogen.**

**Verhältnis zu OD-05:** Option B bleibt unverändert: „Policy-Konfiguration in die
bestehende `PluginSecurityStage` ziehen (ohne Reihenfolgeänderung)"
[SOURCE: docs/governance/od-05-governance-decision.md Kap. 8]. F-2 vergleicht
keine Optionen, erzeugt keine Option und definiert keine Implementierung. F-2
stellt ausschließlich fest, **welche Teile einer späteren Ausgestaltung nach §8-4
überhaupt unter Change Control fielen**.

---

## 6. Bootstrap Baseline §8 — vollständige Analyse

### 6.1 Wortlaut

> „Jede zukünftige Änderung am Bootstrap-Paket, die eines der folgenden betrifft:
> — **Paketstruktur** (Module hinzufügen, entfernen, umbenennen)
> — **Runtime-Pipeline** (Phasenreihenfolge, Stage-Reihenfolge)
> — **Public Exports** (`__all__`-Einträge ändern)
> — **BootstrapManager** (API-Signatur, Verhalten)
> — **default_stages()** (Stage-Zusammensetzung, Reihenfolge)
> erfordert eine genehmigte Governance-Entscheidung in Form von:
> — einem neuen **ADR** (Architecture Decision Record), oder
> — einem neuen **RDR** (Refactoring Decision Record)"
> [SOURCE: docs/baselines/bootstrap-baseline-1.0.md §8]

### 6.2 Strukturbefund der Enumeration

| Tatbestand | Klammerzusatz (Präzisierung durch die Quelle selbst) | Präzisionsgrad |
|---|---|---|
| §8-1 Paketstruktur | „Module hinzufügen, entfernen, umbenennen" | **operativ präzise** |
| §8-2 Runtime-Pipeline | „Phasenreihenfolge, Stage-Reihenfolge" | **operativ präzise** |
| §8-3 Public Exports | „`__all__`-Einträge ändern" | **operativ präzise** |
| **§8-4 BootstrapManager** | **„API-Signatur, Verhalten"** | **API-Signatur präzise; „Verhalten" undefiniert** |
| §8-5 `default_stages()` | „Stage-Zusammensetzung, Reihenfolge" | **operativ präzise** |

**Feststellung (Quellenfakt):** Vier der fünf Tatbestände tragen einen
operativ prüfbaren Klammerzusatz. **§8-4 ist der einzige Tatbestand, der einen
nicht weiter bestimmten Begriff enthält.** Dies ist genau die in NAW-1 B-2
benannte Lücke.

### 6.3 Suche nach Definitionen, Beispielen, Positiv-/Negativlisten

Vollständige Prüfung der Bootstrap Baseline 1.0 auf die vom Auftrag genannten
Regelungsarten:

| Gesuchte Regelungsart | Fundstelle in Bootstrap Baseline 1.0 |
|---|---|
| Explizite Definition von „Verhalten" | **KEINE** — Begriff erscheint genau einmal, in §8-4 selbst (Z. 209) |
| Beispiele zu §8-4 | **KEINE** |
| Positivliste | **KEINE** |
| Negativliste / Ausnahmen | **KEINE** |
| API-Schutz | §3.1 (20 Exporte), §3.2 (2 interne Re-Exports, **ausdrücklich nicht stabile API**), §3.3 (Consumer-Import-Kompatibilität) |
| Verhaltensschutz (allgemein) | **KEINER außerhalb §8-4** |
| Stage-Schutz (Existenz einzelner Stages) | §5.1 (Phasensequenz), §3.1 (Stages als Exporte) |
| Reihenfolgeschutz | §4 Inv. 4, 5, 6; §5.1; §5.2; §8-2; §8-5 |
| Lifecycle-Schutz | §4 Inv. 5 (StartupPhase-Reihenfolge) — **kein** Objekt-Lebenszyklusschutz |
| Event-Semantik | **KEINE Regel** |
| Error-Semantik | **KEINE Regel** |
| Shutdown-Semantik | **KEINE Regel** |
| Composition-Root-Regeln | §4 Inv. 3 (`BootstrapManager` als einziger Einstiegspunkt); §4 Inv. 4 (`default_stages()`) |
| Default-Stages-Regeln | §4 Inv. 4; §5.1; §8-5 |
| Trennung intern ↔ extern | §3.2 (interne Re-Exports nicht stabil); §3.3; §4 Inv. 7 |
| ADR-/RDR-Auslöser | §8 Schlussteil — **beide alternativ, ohne Abgrenzungskriterium** |

> **Negativbefund von zentraler Bedeutung:** Die Bootstrap Baseline 1.0 enthält
> **keinerlei** Regelung zu Event-, Error- oder Shutdown-Semantik und **keine**
> Definition von „Verhalten".

### 6.4 Chapeau-Bedingung

Der Einleitungssatz von §8 verlangt eine „Änderung **am Bootstrap-Paket**", die
„eines der folgenden **betrifft**". Die Lage im Paket `app/bootstrap/` ist damit
**notwendige, aber nicht hinreichende** Bedingung — dies war bereits Befund von
NAW-1 Kap. 6 und wird hier bestätigt
[SOURCE: docs/baselines/bootstrap-baseline-1.0.md §8; docs/governance/naw-01-od05-adr-rdr-assessment.md Kap. 6].

---

## 7. §8-4 Wortlaut / Kontext

**Wortlaut:** „**BootstrapManager** (API-Signatur, Verhalten)"
[SOURCE: docs/baselines/bootstrap-baseline-1.0.md §8, Zeile 209]

**Textinterner Kontext:**

| Kontextelement | Aussage | Fundstelle |
|---|---|---|
| Bezugsobjekt | Der `BootstrapManager` — nicht „das Bootstrap-Paket", nicht „die Stages" | §8-4 |
| Zweigliedrigkeit | Der Tatbestand nennt **zwei** Schutzgegenstände: „API-Signatur" **und** „Verhalten" | §8-4 |
| Nachbartatbestände | §8-2 und §8-5 adressieren Reihenfolge und Zusammensetzung **eigenständig** | §8-2, §8-5 |
| Invariante 3 | „**BootstrapManager als Orchestrator** — Der `BootstrapManager` ist der einzige Einstiegspunkt für die Bootstrap-Ausführung. Stages werden **nicht direkt aufgerufen**." | §4 Inv. 3 |
| Baseline-Purpose | „Alle zukünftigen Bootstrap-Arbeiten müssen diese Baseline **bewahren**, sofern keine genehmigte Governance-Änderung (ADR oder RDR) eine **Abweichung** autorisiert." | §1 |

**Strukturelle Beobachtung (Quellenfakt, keine Schlussfolgerung):** Die
Enumeration in §8 enthält für Stage-Reihenfolge (§8-2) und Stage-Zusammensetzung
(§8-5) **eigene, ausdrücklich benannte Tatbestände**.

> **Ausdrücklich keine verdeckte Entscheidung:** Ob aus dieser Struktur folgt,
> dass §8-4 diese Gegenstände **nicht zusätzlich** erfasst, ist eine **Auslegung**
> und **wird hier nicht als Tatsache ausgegeben**. Festgestellt wird
> ausschließlich, dass die Quelle **eigene** Tatbestände dafür vorsieht.

---

## 8. Definition „Verhalten"

### 8.1 Befundlage in allen autoritativen Quellen

| # | Quelle | Verwendung von „Verhalten" | Definitorischer Gehalt |
|---|---|---|---|
| V-1 | Bootstrap Baseline 1.0 | **1 Treffer**: §8-4 selbst | **KEINER** — der zu definierende Begriff selbst |
| V-2 | Development Standard v1.1 | **0 Treffer** | **KEINER** [SOURCE: docs/development-standard-v1.1.md, Volltextprüfung] |
| V-3 | Architecture Book v2.0 §22.2 | „Performance-Optimierung \| Ja \| **Verhalten unverändert**" | **KEINER** — ebenfalls undefiniert [SOURCE: BASELINE 8fcf42f:docs/architecture-book-v2.md §22.2] |
| V-4 | Engineering Specification 1.0 | „Änderungen an Paketstruktur, Runtime-Pipeline, Public Exports, **BootstrapManager** oder `default_stages()` erfordern eine genehmigte Governance-Entscheidung gemäß Baseline §8" | **KEINER** — nennt „BootstrapManager" **ohne** Klammerzusatz [SOURCE: docs/milestone-1.0-engineering-spec.md §393-Passage] |
| V-5 | Implementation Plan 1.0 **API-04** | „Jede Änderung an der öffentlichen Exportmenge, an der Paketstruktur, an der **`BootstrapManager`-Signatur** oder an der Zusammensetzung von `default_stages()` erfordert eine genehmigte Governance-Entscheidung vor der Umsetzung (Bootstrap Baseline 1.0, Change Control)." | **Verengend** — nennt ausschließlich die **Signatur**; „Verhalten" **fehlt** [SOURCE: docs/milestone-1.0-implementation-plan.md §3.4 API-04] |
| V-6 | RDR-001 **Invariante 5** | „**`BootstrapManager`-Verhalten bleibt identisch.** `begin()`, `run_phase()` und `build_context()` verhalten sich exakt wie vorher." | **Konkretisierend, eng** — bindet „BootstrapManager-Verhalten" an die **drei öffentlichen Methoden** [SOURCE: docs/rdr/001-bootstrap-modularization.md §3 Inv. 5] |
| V-7 | RDR-001 **§2.2** | „**Keine Verhaltensänderungen.** Die Laufzeitpipeline, Phase-Reihenfolge und **Stage-Ausführungslogik** bleiben identisch." | **Weit** — subsumiert **Stage-Ausführungslogik** unter „Verhalten"; jedoch **nicht** BootstrapManager-spezifisch [SOURCE: docs/rdr/001-bootstrap-modularization.md §2.2] |
| V-8 | Sprint Plan 1.0 | keine §8-Reichweitenregel | **KEINER** |

### 8.2 Bewertung der Befundlage

**Antwort auf Prüffrage G („Gibt es eine explizite Regel?"): NEIN.**
Keine der 18 Pflichtquellen enthält eine **Definition** von „Verhalten" i. S. v.
§8-4. Es existieren lediglich **Verwendungen** (V-3 bis V-7), von denen zwei
(V-6, V-7) aus derselben Quelle stammen und **unterschiedlich weit** reichen.

**Antwort auf Prüffrage H: JA** — die Regelungslücke ist mit diesem Assessment
dokumentiert und bleibt als **OPEN / HUMAN REVIEW REQUIRED** bestehen (Kap. 18).

---

## 9. API vs. Observable Behaviour

| Bereich | §8-4 erfasst? | Quelle | Sicherheit | Begründung |
|---|---|---|---|---|
| Öffentliche **Signatur** des `BootstrapManager` (Feld `stages`; Methoden `begin`, `run_phase`, `build_context`) | **JA** | §8-4 („API-Signatur"); IP **API-04** | **DETERMINATE** | Wortlaut ausdrücklich; durch eine zweite APPROVED-Quelle (V-5) bestätigt |
| **Öffentlich beobachtbares Verhalten** dieser drei Methoden | **JA** | §8-4 („Verhalten"); RDR-001 Inv. 5 (V-6) | **PARTIALLY DETERMINATE** | V-6 ist die **einzige** Konkretisierung von „BootstrapManager-Verhalten" in einer autoritativen Quelle und bindet ihn an exakt diese drei Methoden. V-6 ist jedoch eine Selbstaussage eines Refactoring-Records, **keine ausgewiesene Definition** von §8-4 |
| Rückgabetyp/-inhalt von `build_context()` (`ApplicationContext`-Zusammensetzung) | **wahrscheinlich JA** | §8-4; V-6 | **PARTIALLY DETERMINATE** | Teil des beobachtbaren Verhaltens von `build_context()`; nicht ausdrücklich geregelt |
| Fehlerkontrakt von `run_phase()` (Wrapping in `BootstrapError`) | **wahrscheinlich JA**, soweit der Wrapping-**Mechanismus** selbst geändert würde | §8-4; V-6; Code V-C3 | **PARTIALLY DETERMINATE** | Die Docstring-Zusage „Raises: BootstrapError" ist Teil des Methodenkontrakts. **Abzugrenzen** von Kap. 13 (indirekte Auslösung durch Stages) |

---

## 10. Internal Manager Behaviour

**Prüffrage B: Umfasst „Verhalten" auch die interne Orchestrierungslogik des
`BootstrapManager`?**

| Bereich | §8-4 erfasst? | Quelle | Sicherheit | Begründung |
|---|---|---|---|---|
| Interne Implementierung von `run_phase()` (Schleife, Phasenfilter `stage.phase is not phase`) bei **unverändertem** beobachtbarem Verhalten | **UNKNOWN** | keine | **UNKNOWN** | §8-4 unterscheidet nicht zwischen interner Implementierung und beobachtbarem Verhalten. AB §22.2 erlaubt „Interne Refactorings — API-Surface unverändert", trifft aber keine Aussage zur **Baseline** §8-4 (verschiedene Instrumente, F-1 Kap. 11.3) |
| Interne Hilfsfunktion `_require` (in §3.2 ausdrücklich als **nicht stabile API** geführt) | **UNKNOWN** | §3.2 | **UNKNOWN** | §3.2 verneint den **API**-Status, trifft aber keine Aussage zum **Verhaltens**-Tatbestand |

> Es wird ausdrücklich **nicht** gefolgert, interne Manager-Logik sei erlaubt oder
> geschützt. Beide Schlüsse wären ungedeckt.

---

## 11. Stage Composition / Ordering

**Prüffrage C: Umfasst „Verhalten" die Zusammensetzung bzw. Reihenfolge der
Stages?**

| Bereich | §8-4 erfasst? | Quelle | Sicherheit | Begründung |
|---|---|---|---|---|
| Stage-**Reihenfolge** | **NOT COVERED durch §8-4** — abschließend durch **§8-2** erfasst | §8-2; §4 Inv. 4, 5, 6; §5.1; §5.2; IP BP-01…BP-03 | **DETERMINATE**, dass Change Control greift; **PARTIALLY DETERMINATE**, dass §8-4 sie nicht zusätzlich erfasst | §8-2 nennt „Phasenreihenfolge, Stage-Reihenfolge" ausdrücklich; RDR-001 führt sie als **eigene** Invarianten 1/2 **neben** der BootstrapManager-Invariante 5 |
| Stage-**Zusammensetzung** in `default_stages()` | **NOT COVERED durch §8-4** — abschließend durch **§8-5** erfasst | §8-5; §4 Inv. 4; IP API-04 | dito | §8-5 nennt „Stage-Zusammensetzung, Reihenfolge" ausdrücklich; IP API-04 nennt sie eigenständig neben der Signatur |
| Stage-Zusammensetzung über das **Konstruktorfeld** `BootstrapManager(stages=…)` | **JA, soweit die Signatur betroffen wäre** | §8-4 („API-Signatur"); Code V-C1 | **PARTIALLY DETERMINATE** | `stages` ist ein öffentliches Dataclass-Feld und damit Teil der Signatur. **Die Übergabe anderer Stages an ein unverändertes Feld ändert die Signatur nicht** — dies ist der in AB §9 und R0 §8.4 BS-03 beschriebene, zulässige additive Erweiterungsweg |

> **Praktische Folge (Feststellung, keine Entscheidung):** Für Stage-Reihenfolge
> und -Zusammensetzung ist die Frage nach §8-4 **ohne Auswirkung auf das
> Ergebnis** — beide fallen über §8-2 bzw. §8-5 ohnehin unter Change Control.
> **B-3 wird hier nicht entschieden**; F-2 stellt nur fest, unter welchem
> Tatbestand die Frage zu prüfen wäre.

---

## 12. Stage-Internal Logic

**Prüffragen D und E: Umfasst „Verhalten" die konkrete Implementierung einzelner
Stages bzw. Stage-interne Logik?**

**Dies ist die für OD-05 Option B entscheidende Teilfrage.**

| Bereich | §8-4 erfasst? | Quelle | Sicherheit | Begründung |
|---|---|---|---|---|
| Implementierung einer einzelnen Stage (z. B. `PluginSecurityStage.execute`) bei unveränderter Phase, Position und Signatur | **UNKNOWN** | Quellenkonflikt V-6 ↔ V-7 | **UNKNOWN / HUMAN REVIEW REQUIRED** | siehe 12.1 |
| Stage-interne Logik allgemein | **UNKNOWN** | dito | **UNKNOWN / HUMAN REVIEW REQUIRED** | dito |

### 12.1 Der Quellenkonflikt

| Richtung | Beleg | Wortlaut |
|---|---|---|
| **Eng** (Stage-Interna **nicht** von §8-4 erfasst) | **V-6** — RDR-001 §3 Inv. 5 | „`BootstrapManager`-Verhalten bleibt identisch. **`begin()`, `run_phase()` und `build_context()`** verhalten sich exakt wie vorher." — bindet den Begriff an drei Methoden |
| **Eng** (stützend) | **V-5** — IP API-04 (APPROVED R1.2) | Nennt für den `BootstrapManager` **ausschließlich die Signatur**; der Verhaltensbegriff fehlt in dieser Wiedergabe der Change Control vollständig |
| **Weit** (Stage-Interna **von „Verhalten" erfasst**) | **V-7** — RDR-001 §2.2 | „Keine **Verhaltens**änderungen. Die Laufzeitpipeline, Phase-Reihenfolge und **Stage-Ausführungslogik** bleiben identisch." — subsumiert Stage-Ausführungslogik ausdrücklich unter den Verhaltensbegriff |

**Bewertung des Konflikts — ohne Auflösung:**

- V-6 und V-7 stammen aus **derselben APPROVED-Quelle** und verwenden den Begriff
  „Verhalten" in **unterschiedlicher Weite**. V-6 ist **BootstrapManager-spezifisch**
  (und damit dem Wortlaut von §8-4 näher), V-7 ist **allgemein** gefasst.
- V-5 lässt „Verhalten" bei der Wiedergabe der Change Control weg. Ob dies eine
  **bewusste Verengung** oder eine **verkürzte Wiedergabe** ist, ist den Quellen
  **nicht entnehmbar** — V-5 lässt ebenfalls den Tatbestand „Runtime-Pipeline"
  weg, deckt ihn jedoch über IP BP-01…BP-03 gesondert ab. → **UNKNOWN.**
- Keine Quelle ordnet diesen Verwendungen einen **Vorrang** zu.

> **Ausdrücklich keine verdeckte Entscheidung** (Auftrag Kap. 13): Aus „Stage-interne
> Logik ist in §8-4 nicht ausdrücklich genannt" wird **nicht** gefolgert, sie sei
> erlaubt. Aus „Stage-Ausführungslogik ist in V-7 Verhalten" wird **nicht**
> gefolgert, sie sei nach §8-4 automatisch geschützt.
> **Ergebnis: UNKNOWN / INTERPRETATION REQUIRED.**

---

## 13. Lifecycle / Events / Errors / Shutdown

**Prüffrage F: Umfasst „Verhalten" indirekte Auswirkungen auf Lifecycle, Error
Handling, Event-Semantik oder Shutdown?**

| Bereich | §8-4 erfasst? | Quelle | Sicherheit | Begründung |
|---|---|---|---|---|
| **Indirekte** Änderung des `run_phase()`-Ergebnisses durch geändertes Stage-Verhalten (z. B. eine Stage wirft neu → `BootstrapError`) | **UNKNOWN** | Code V-C3; keine Regel | **UNKNOWN / HUMAN REVIEW REQUIRED** | Der Manager-Code bliebe unverändert, das **beobachtbare Ergebnis** von `run_phase()` änderte sich. Ob dies „BootstrapManager-Verhalten" ist, regelt keine Quelle. **Für Option B potenziell einschlägig** (Kap. 14.2, V-C6) |
| **Indirekte** Änderung von `build_context()` (`_require`-Guards schlagen fehl, wenn eine Stage ihr Kontextfeld nicht setzt) | **UNKNOWN** | Code V-C4 | **UNKNOWN** | dito |
| **Event-Semantik** (`PluginVerified` / `PluginRejected` u. a.) | **NOT COVERED** | — | **NOT COVERED** | Die Bootstrap Baseline enthält **keine** Regel zur Event-Semantik (Kap. 6.3). Ein Schutz über §8-4 ist nicht erkennbar; ein Schutz über andere Instrumente ist **nicht Gegenstand von F-2** |
| **Shutdown-Semantik** | **NOT COVERED** | — | **NOT COVERED** | Die Bootstrap Baseline enthält **keine** Shutdown-Regel (Kap. 6.3). AB §6.5 nennt `ShutdownSequence`, liegt aber außerhalb des §8-Regelungsbereichs |
| **Lifecycle** i. S. d. Phasenreihenfolge | **NOT COVERED durch §8-4** — durch §8-2 und §4 Inv. 5 erfasst | §8-2; §4 Inv. 5 | **DETERMINATE**, dass Change Control greift | eigene Tatbestände vorhanden |

---

## 14. Code Verification

**Ausschließlich READ-ONLY** über `git show 8fcf42f:<pfad>`. Keine Änderung, keine
Testausführung, keine Simulation.

### 14.1 Verifizierte Befunde

| # | Gegenstand | Befund | Fundstelle |
|---|---|---|---|
| **V-C1** | `BootstrapManager` | `@dataclass(frozen=True, slots=True)` mit **einem** öffentlichen Feld: `stages: tuple[BootstrapStage, ...] = field(default_factory=default_stages)` | [SOURCE: BASELINE 8fcf42f:app/bootstrap/manager.py, `class BootstrapManager`] |
| **V-C2** | Öffentliche Methoden | genau drei: `begin(root)`, `run_phase(context, phase)`, `build_context(context, state_machine)` — deckungsgleich mit der Aufzählung in RDR-001 Inv. 5 (V-6) | [SOURCE: BASELINE 8fcf42f:app/bootstrap/manager.py] |
| **V-C3** | Orchestrierungslogik | `run_phase` iteriert `self.stages`, filtert `stage.phase is not phase`, ruft `stage.execute(context)`; `BootstrapError` wird durchgereicht, jede andere Exception wird zu `BootstrapError(f"Bootstrap stage failed: {stage.name}") from error` gewandelt | [SOURCE: BASELINE 8fcf42f:app/bootstrap/manager.py, `run_phase`] |
| **V-C4** | `build_context` | Setzt `ApplicationContext` aus 12 über `_require(...)` geprüften Kontextfeldern zusammen (u. a. `plugins`) | [SOURCE: BASELINE 8fcf42f:app/bootstrap/manager.py, `build_context`] |
| **V-C5** | `manager.py` `__all__` | genau `["BootstrapManager", "default_stages"]` | [SOURCE: BASELINE 8fcf42f:app/bootstrap/manager.py] |
| **V-C6** | `PluginSecurityStage` | `name = "plugin_security"`, `phase = StartupPhase.LOAD_PLUGINS`; `execute()` bezieht `PluginSecurity` aus der Registry und legt bei `LookupError` selbst eine Default-Instanz an und registriert sie | [SOURCE: BASELINE 8fcf42f:app/bootstrap/stages_plugin.py, `class PluginSecurityStage`, Z. 262–266] |
| **V-C7** | `default_stages()` | 13 Stages in fester Ordnung; `PluginSecurityStage()` an Position 9 | [SOURCE: BASELINE 8fcf42f:app/bootstrap/manager.py, `default_stages`] |
| **V-C8** | `app/bootstrap/__init__.py` | `__all__` mit **20** Symbolen (inkl. `PluginSecurityStage`); zusätzlich zwei interne Re-Exports außerhalb `__all__` | [SOURCE: BASELINE 8fcf42f:app/bootstrap/__init__.py; docs/baselines/bootstrap-baseline-1.0.md §3.1/§3.2] |
| **V-C9** | `SecurityBootstrapStage` | definiert in **`app/security/security_manager.py`**, `phase = StartupPhase.FINALIZE` — **außerhalb** des Baseline-Scopes §2 (sieben `app/bootstrap/`-Module) | [SOURCE: BASELINE 8fcf42f:app/security/security_manager.py; docs/baselines/bootstrap-baseline-1.0.md §2] |
| **V-C10** | `create_desktop_bootstrap_manager()` | in **`ui/navigation/navigation_service.py`**; filtert eine **Kopie** von `default_stages()` und übergibt die erweiterte Sequenz an das Feld `BootstrapManager(stages=…)`. `default_stages()` selbst bleibt unangetastet | [SOURCE: BASELINE 8fcf42f:ui/navigation/navigation_service.py] |

### 14.2 Die sieben vom Auftrag geforderten Unterscheidungsebenen

| # | Ebene | Konkretisierung am Baseline | §8-4-Zuordnung |
|---|---|---|---|
| 1 | BootstrapManager **API** | Feld `stages`; drei Methoden (V-C1, V-C2) | **erfasst** — DETERMINATE |
| 2 | BootstrapManager **öffentlich beobachtbares Verhalten** | Rückgabe von `begin`/`build_context`; Ausführungs- und Fehlerkontrakt von `run_phase` (V-C3, V-C4) | **erfasst** — PARTIALLY DETERMINATE |
| 3 | **interne** Manager-Implementierung | Schleife und Phasenfilter in `run_phase` (V-C3) | **UNKNOWN** |
| 4 | **Stage-Komposition** | `default_stages()` (V-C7); Feld `stages` (V-C1); Desktop-Erweiterung (V-C10) | **NOT COVERED durch §8-4** — §8-5 bzw. §8-4-„API-Signatur" |
| 5 | **Stage-Reihenfolge** | V-C7 | **NOT COVERED durch §8-4** — §8-2 |
| 6 | **Stage-interne Logik** | `PluginSecurityStage.execute` (V-C6) — **Ort der OD-05-Option-B-Ausgestaltung** | **UNKNOWN / HUMAN REVIEW REQUIRED** |
| 7 | **externe Auswirkungen** der Stage-Ausführung | Registry-Registrierungen; `BootstrapError`-Auslösung über `run_phase` (V-C3, V-C6) | **UNKNOWN** |

> **Feststellung zur Tragweite (keine Entscheidung):** Die Ausgestaltung von OD-05
> Option B läge nach ihrem eigenen Wortlaut in **Ebene 6** — genau der Ebene, die
> §8-4 nicht bestimmt. Ebene 4 und 5 sind durch Option B ausdrücklich
> ausgeschlossen bzw. über §8-2/§8-5 ohnehin erfasst.

---

## 15. Cross-Source Comparison

**Zweck ausschließlich:** Feststellen, ob eine **bestehende** Regel die Reichweite
von §8-4 eindeutig bestimmt. **Keine neue Hierarchie, keine neue Taxonomie.**

### 15.1 Vergleichstabelle

| Quelle | Bestimmt sie §8-4? | Befund |
|---|---|---|
| **Development Standard v1.1 §13** | **NEIN** | Enthält acht ADR-Auslöser; **keiner** adressiert Stage-interne Logik oder den Verhaltensbegriff. Begriff „Verhalten" kommt im Dokument **nicht vor** [SOURCE: docs/development-standard-v1.1.md §13] |
| **Architecture Book v2.0 §22** | **NEIN** | Definiert den **Architecture Freeze**, ein **anderes Instrument** (F-1 Kap. 11.3). §22.2 verwendet „Verhalten unverändert" ebenfalls undefiniert [SOURCE: BASELINE 8fcf42f:docs/architecture-book-v2.md §22] |
| **Bootstrap Baseline §4** | **NEIN, aber eingrenzend** | Sieben Invarianten; Inv. 3 („BootstrapManager als Orchestrator"), Inv. 4 (`default_stages()` bewahrt Reihenfolge), Inv. 5 (StartupPhase-Reihenfolge), Inv. 6 (Plugin-Runtime-Pipeline). **Keine** Invariante adressiert Stage-interne Logik [SOURCE: docs/baselines/bootstrap-baseline-1.0.md §4] |
| **RDR-001** | **NEIN, aber am nächsten** | Einzige Quelle mit Konkretisierung des Begriffs — jedoch **in zwei unterschiedlichen Weiten** (V-6 eng, V-7 weit). Siehe 15.3 |
| **ADR-011** | **NEIN** | Keine Fundstelle zu „Verhalten", `BootstrapManager` oder `default_stages()` [SOURCE: docs/adr/011-sdk-host-integration.md, Volltextprüfung] |
| **Implementation Plan 1.0** | **NEIN, aber verengend wiedergebend** | **API-04** nennt für den `BootstrapManager` ausschließlich die **Signatur** (V-5). **GC-06**: „Keine Bootstrap-Änderung. Änderungen an der Bootstrap Baseline 1.0 erfordern einen genehmigten ADR oder RDR vor der Implementierung." **BI-03/BP-04**: Orchestrator-Invariante [SOURCE: docs/milestone-1.0-implementation-plan.md §3.4 API-04, GC-06, BI-03, BP-04] |
| **Engineering Specification 1.0** | **NEIN** | Nennt „BootstrapManager" ohne Klammerzusatz (V-4) [SOURCE: docs/milestone-1.0-engineering-spec.md §393-Passage] |
| **Sprint Plan 1.0** | **NEIN** | Keine §8-Reichweitenregel |

### 15.2 Ausdrücklich gezeigter Widerspruch (Auftrag Kap. 22)

> **Divergenz D-1 — Implementation Plan API-04 gegenüber Bootstrap Baseline §8-4:**
> Die Baseline schützt „BootstrapManager (**API-Signatur, Verhalten**)". Der
> APPROVED Implementation Plan gibt denselben Change-Control-Tatbestand als
> „Änderung an der **`BootstrapManager`-Signatur**" wieder — **ohne** den
> Verhaltensbegriff. Ob dies eine bewusste Verengung oder eine verkürzte
> Wiedergabe darstellt, ist den Quellen **nicht entnehmbar**. **Der Konflikt wird
> hier gezeigt, nicht aufgelöst.**

> **Divergenz D-2 — RDR-001 §2.2 gegenüber RDR-001 §3 Invariante 5:**
> Dieselbe APPROVED-Quelle verwendet „Verhalten" einmal weit (§2.2: einschließlich
> **Stage-Ausführungslogik**) und einmal eng und BootstrapManager-spezifisch
> (Inv. 5: **`begin()`, `run_phase()`, `build_context()`**). **Der Konflikt wird
> hier gezeigt, nicht aufgelöst.**

### 15.3 Strukturelle Parallele RDR-001 §3 ↔ Bootstrap Baseline §8

**Quellenfakt:** RDR-001 §3 führt **getrennte** Invarianten für Runtime-Pipeline
(Inv. 1), Phase-Reihenfolge (Inv. 2), `__all__`-Exporte (Inv. 4),
**BootstrapManager-Verhalten** (Inv. 5), Plugin-Lebenszyklus (Inv. 6) und
Sicherheitsvalidierungs-Reihenfolge (Inv. 7)
[SOURCE: docs/rdr/001-bootstrap-modularization.md §3]. Bootstrap Baseline §8 führt
ebenfalls getrennte Tatbestände für Paketstruktur, Runtime-Pipeline, Public
Exports, BootstrapManager und `default_stages()`. Die Baseline weist RDR-001 als
ihre unmittelbare Entstehungsgrundlage aus
[SOURCE: docs/baselines/bootstrap-baseline-1.0.md §1: „nach vollständiger Umsetzung
von RDR-001"; §6 Governance References; Kopf: „Ersetzt: Bootstrap-Implementierung
vor RDR-001"].

> **Keine Schlussfolgerung.** Ob aus dieser strukturellen Parallele folgt, dass
> §8-4 im Sinne von RDR-001 Inv. 5 (drei Methoden) zu lesen ist, ist eine
> **Auslegungsentscheidung** und wird hier **nicht getroffen**. Sie ist der
> wesentliche Anknüpfungspunkt für die in Kap. 19 benannte menschliche
> Governance-Entscheidung.

---

## 16. F-2 Determination

> # **F-2-B — §8-4 PARTIALLY DEFINED**

**Entscheidungsrelevante Kernfrage:** *Ist §8-4 bereits hinreichend bestimmt, um
F-3 ohne weitere Governance-Auslegung durchzuführen?*

> **NEIN — nicht vollständig.** §8-4 ist in seinem **Signatur**-Teil bestimmt und
> in seinem **Verhaltens**-Teil nur insoweit, als der beobachtbare Kontrakt der
> drei öffentlichen Methoden erfasst ist. **Für die entscheidende Teilfrage —
> Stage-interne Logik — bleibt §8-4 unbestimmt.**

**Zusammenfassende Zuordnung nach dem vorgegebenen Analysemodell:**

| Bereich | §8-4 erfasst? | Sicherheit |
|---|---|---|
| BootstrapManager-API-Signatur | JA | **DETERMINATE** |
| Beobachtbares Verhalten von `begin`/`run_phase`/`build_context` | JA | **PARTIALLY DETERMINATE** |
| Interne Orchestrierungslogik des Managers | offen | **UNKNOWN** |
| Stage-Zusammensetzung | über §8-5 | **NOT COVERED durch §8-4** |
| Stage-Reihenfolge | über §8-2 | **NOT COVERED durch §8-4** |
| **Stage-interne Logik** | **offen** | **UNKNOWN / HUMAN REVIEW REQUIRED** |
| Indirekte Wirkungen (Error/Lifecycle) | offen | **UNKNOWN** |
| Event-Semantik | keine Regel in der Baseline | **NOT COVERED** |
| Shutdown-Semantik | keine Regel in der Baseline | **NOT COVERED** |

**Weshalb nicht F-2-A:** Eine Feststellung „hinreichend bestimmt" wäre nur
haltbar, wenn eine Quelle den Verhaltensbegriff **definierte**. Keine der 18
Pflichtquellen tut dies (Kap. 8.1); zwei belegte Divergenzen (D-1, D-2) stehen
einer eindeutigen Lesart entgegen.

**Weshalb nicht F-2-D:** Ein Befund „vollständige Regelungslücke" würde
verkennen, dass der Signatur-Teil determiniert ist (§8-4 Wortlaut + IP API-04),
dass der Methodenkontrakt durch RDR-001 Inv. 5 konkretisiert ist, und dass
Reihenfolge und Zusammensetzung über §8-2/§8-5 **unabhängig von §8-4** unter
Change Control fallen. Die Lücke ist real, aber **eingegrenzt**.

---

## 17. F-3 Handoff

### 17.1 Übergabetabelle

| F-3 Frage | Durch F-2 geklärt? | Ergebnis |
|---|---|---|
| **Neues `__all__`-Symbol** (NAW-1 B-1) | **NEIN** (nicht Gegenstand von F-2) — **aber Zuordnung geklärt** | Fällt unter **§8-3** („Public Exports — `__all__`-Einträge ändern"), **nicht** unter §8-4. Die §8-4-Auslegung ist hierfür **nicht** erforderlich. **F-3 darf dies prüfen; F-2 entscheidet es nicht** |
| **`default_stages()`** (NAW-1 B-3) | **NEIN** (nicht Gegenstand) — **aber Zuordnung geklärt** | Fällt unter **§8-5** („Stage-Zusammensetzung, Reihenfolge"), **nicht** unter §8-4. **F-3 darf dies prüfen; F-2 entscheidet es nicht** |
| **Konkrete Änderungsfläche** der Ausgestaltung | **NEIN** | Die Ausgestaltung von Option B ist durch GDR-OD05-001 Kap. 6 ausdrücklich offen gelassen. **F-3-Kernaufgabe** |
| **Stage-interne Logik** | **NEIN — bleibt offen** | **UNKNOWN / HUMAN REVIEW REQUIRED** (Kap. 12). **F-3 darf dies NICHT entscheiden** — es bedarf einer menschlichen Auslegungsentscheidung (Kap. 19, G-1) |
| **BootstrapManager-Verhalten** | **TEILWEISE** | Signatur: **DETERMINATE erfasst**. Beobachtbares Verhalten der drei Methoden: **PARTIALLY DETERMINATE erfasst**. Interne Logik und indirekte Wirkungen: **UNKNOWN** |

### 17.2 Was F-3 prüfen darf

| # | Zulässiger F-3-Prüfgegenstand | Grundlage |
|---|---|---|
| 1 | Ob die Ausgestaltung ein neues Symbol in `app/bootstrap/__init__.py` `__all__` erzeugte → **§8-3** | Zuordnung in 17.1 |
| 2 | Ob die Ausgestaltung die von `default_stages()` gelieferte Zusammensetzung oder Ordnung veränderte → **§8-5** | Zuordnung in 17.1 |
| 3 | Ob die Ausgestaltung die **Signatur** des `BootstrapManager` veränderte → **§8-4, Signatur-Teil (DETERMINATE)** | Kap. 9 |
| 4 | Ob die Ausgestaltung den beobachtbaren Kontrakt von `begin`/`run_phase`/`build_context` **unmittelbar** veränderte → **§8-4, Verhaltens-Teil (PARTIALLY DETERMINATE)** | Kap. 9 |
| 5 | Ob die Ausgestaltung ein Modul hinzufügte, entfernte oder umbenennte → **§8-1** | §8-1 (operativ präzise) |
| 6 | Ob die Ausgestaltung Phasen- oder Stage-Reihenfolge veränderte → **§8-2** | §8-2; durch Option B ausdrücklich ausgeschlossen |

### 17.3 Was F-3 NICHT entscheiden darf

| # | Verbotener F-3-Gegenstand | Grund |
|---|---|---|
| 1 | Ob **Stage-interne Logik** unter §8-4 fällt | **UNKNOWN**; erfordert eine menschliche Auslegungsentscheidung (Kap. 19, G-1) |
| 2 | Ob **indirekte** Wirkungen auf `run_phase`/`build_context` §8-4 auslösen | **UNKNOWN** (Kap. 13) |
| 3 | Ob **interne Manager-Logik** von §8-4 erfasst ist | **UNKNOWN** (Kap. 10) |
| 4 | Die Auflösung von **D-1** oder **D-2** | Quellenkonflikte; keine Vorrangregel vorhanden |
| 5 | **B-4**, **B-6**, **B-7** | ausdrücklich außerhalb F-2 und F-3 |
| 6 | Eine ADR-/RDR-Pflicht abschließend festzustellen | erst **F-5**, nach G-1 |

> **Wesentliche Einschränkung:** Solange G-1 offen ist, kann F-3 die
> §8-Betroffenheit **nur für die Ebenen 1–5 und 7 der Enumeration** abschließend
> klären, **nicht** für Ebene 6 (Stage-interne Logik) — und genau dort läge die
> Ausgestaltung von Option B nach ihrem eigenen Wortlaut (Kap. 14.2).

---

## 18. Remaining UNKNOWNs

| ID | Offene Frage | Verursachende Quelle | Erforderliche Zusatzprüfung |
|---|---|---|---|
| **F2-U1** | Erfasst §8-4 „Verhalten" die **Stage-interne Logik**? | Bootstrap Baseline §8-4 (keine Definition); Divergenz **D-2** | **Autoritative Auslegungsentscheidung** durch die Baseline-Autorität (Kap. 19, G-1) |
| **F2-U2** | Erfasst §8-4 die **interne Orchestrierungslogik** des Managers bei unverändertem beobachtbarem Verhalten? | keine Quelle | dito |
| **F2-U3** | Erfassen §8-4 **indirekte** Wirkungen (eine Stage löst neu `BootstrapError` über `run_phase` aus)? | keine Quelle; Code V-C3 | dito |
| **F2-U4** | Ist die Weglassung des Verhaltensbegriffs in IP **API-04** bewusste Verengung oder Verkürzung? (**D-1**) | IP API-04 ↔ Baseline §8-4 | Klarstellung durch die Autorität des Implementation Plan |
| **F2-U5** | Welche der beiden RDR-001-Verwendungen (§2.2 weit / Inv. 5 eng) ist für §8-4 maßgeblich? (**D-2**) | RDR-001 | dito |
| **F2-U6** | Nach welchem Kriterium bestimmt sich bei bejahter §8-Pflicht **ADR** oder **RDR**? | §8 nennt beide alternativ ohne Kriterium; Development Standard enthält keine RDR-Regeln | **NAW-1 B-6** — bleibt offen, **nicht Gegenstand von F-2** |
| **F2-U7** | Sind Event-, Error- und Shutdown-Semantik durch ein **anderes** Instrument geschützt? | Bootstrap Baseline enthält dazu keine Regel (Kap. 6.3) | außerhalb F-2 |

---

## 19. Governance Consequences

> **Keine der folgenden Positionen wird durch dieses Assessment ausgeführt oder
> ausgelöst.** Jede bedarf einer eigenen, ausdrücklichen Autorisierung.

| # | Folge | Gegenstand | Autorität | Status |
|---|---|---|---|---|
| **G-1** | **Auslegungsentscheidung zu §8-4 „Verhalten"** — insbesondere zur Stage-internen Logik (F2-U1), einschließlich Stellungnahme zu D-1 und D-2 | Menschliche Governance-Entscheidung; **Voraussetzung** dafür, dass F-3/F-5 die §8-Betroffenheit der Ausgestaltung abschließend feststellen können | Baseline-Autorität („Bootstrap Modularization Final Audit") / Architektur-Governance **+ Projekteigner** | **OPEN — HUMAN REVIEW REQUIRED** |
| **G-2** | **F-3** — Fixierung der Änderungsfläche, beschränkt auf die in 17.2 zulässigen Prüfgegenstände | vorbereitend | Architektur-/Security-Governance | **OPEN — nicht gestartet** |
| **G-3** | **F-4** — Bestimmung des TD-19-Restumfangs | unverändert offen | Architektur-/Security-Governance | **OPEN** |
| **G-4** | **F-5** — Wiederholung der §8-Prüfung | erst nach G-1, G-2, G-3 abschließend führbar | Architektur-/Security-Governance | **OPEN** |

**ADR-/RDR-Feststellung:**

> **ADR/RDR determination remains open.** §8 nennt ADR und RDR alternativ und
> enthält **kein Abgrenzungskriterium**; der Development Standard enthält keine
> RDR-Regeln. **F-2 löst dies nicht** (F2-U6 / NAW-1 B-6).

**Wirkung auf NAW-1:** Das NAW-1-Gesamtergebnis bleibt **D — UNKNOWN / HUMAN
REVIEW REQUIRED**. F-2 **präzisiert** B-2, **schließt es aber nicht**.

---

## 20. Explicit Non-Decisions

Dieses Assessment hat **nicht**:

| # | Nicht getan |
|---|---|
| 1 | §8-4 ausgelegt oder eine Auslegungsregel geschaffen |
| 2 | aus „nicht ausdrücklich genannt" auf „erlaubt" geschlossen |
| 3 | aus „ist Verhalten" auf „automatisch geschützt" geschlossen |
| 4 | **B-1**, **B-3**, **B-4**, **B-6** oder **B-7** entschieden |
| 5 | **OD-05** neu entschieden; Option A/B/C verglichen; eine neue Option erzeugt; Option B geändert |
| 6 | eine Implementierung definiert, empfohlen oder autorisiert |
| 7 | die Divergenzen **D-1** oder **D-2** aufgelöst |
| 8 | ein ADR oder RDR erstellt |
| 9 | eine neue Taxonomie, Schutzklasse oder Risikoskala eingeführt |
| 10 | ein Quality Gate geschlossen, ein Finding, eine ODD oder Technical Debt geschlossen |
| 11 | Sprint Plan, Work Packages, Architecture Book oder Security Design berührt |
| 12 | **RL-05** erreicht oder behauptet |
| 13 | eine Coding Authorization erteilt |
| 14 | F-1 zur Erweiterung oder Verengung von §8-4 herangezogen |

**Unveränderte Status:** TD-04 OPEN · TD-05 OPEN · TD-19 OPEN · TD-21 OPEN ·
TD-06 OPEN · ODD-17 OPEN · OD-04 OPEN · SG-C/SG-D/SG-E nicht erfüllt bzw. nicht
nachgewiesen · TG-2/TG-3/TG-4 erforderlich, nicht erbracht · **QG-006 NOT
STARTED** · **RB-1.0 = 258/14 unverändert** · Sprint Plan unverändert ·
Architecture Book v2.0 unverändert und weiterhin FROZEN.

> ## **CODING = NOT AUTHORIZED.**
>
> F-2 erzeugt keinerlei Coding Authorization.

---

## 21. Repository Integrity

| Prüfung | Vor F-2 | Nach F-2 |
|---|---|---|
| HEAD | `8fcf42f1997dfcf6ff232e75fd33c37b933991c8` | **unverändert** |
| `git status` (getrackt) | 6 bekannte Excludes | **unverändert** |
| `git diff --stat` | 6 files changed, 1.415 insertions(+), 119 deletions(−) | **unverändert** |
| `git diff --cached --stat` | leer | **leer** — kein Staging |
| Neue Dateien | — | **genau eine**: `docs/governance/f-02-bootstrap-baseline-scope-assessment.md` |
| Bestandsdateien verändert | — | **keine** |
| `src/**`, `app/**`, `sdk/**`, `tests/**`, `config/**` | — | **unverändert**; ausschließlich lesend über `git show 8fcf42f:<pfad>` |
| Tests | — | **nicht verändert, nicht ausgeführt** |
| Commit / Tag / Push / Cleanup | — | **KEINE** |

---

## 22. Final Assessment Statement

> **F-2 — FINAL ASSESSMENT**
>
> **Ergebnis: F-2-B — §8-4 PARTIALLY DEFINED.**
>
> **Was geklärt ist:** Der Begriff „**API-Signatur**" in §8-4 ist bestimmt und
> erfasst das öffentliche Feld `stages` sowie die drei Methoden `begin()`,
> `run_phase()` und `build_context()` — bestätigt durch Implementation Plan
> **API-04**. Der Begriff „**Verhalten**" erfasst jedenfalls den **beobachtbaren
> Kontrakt dieser drei Methoden** — gestützt auf **RDR-001 Invariante 5**, die
> einzige Konkretisierung in einer autoritativen Quelle. **Stage-Reihenfolge und
> Stage-Zusammensetzung** fallen über die **eigenen** Tatbestände **§8-2** und
> **§8-5** unter Change Control — unabhängig davon, wie §8-4 gelesen wird.
>
> **Was offen bleibt:** Ob „Verhalten" auch die **Stage-interne Logik**, die
> **interne Orchestrierungslogik** des Managers oder **indirekte Wirkungen** auf
> `run_phase()`/`build_context()` erfasst, ist durch **keine** der 18
> Pflichtquellen geregelt. Der Begriff erscheint in der Bootstrap Baseline
> **genau einmal** — in §8-4 selbst — und im Development Standard **überhaupt
> nicht**. Zwei Divergenzen stehen einer eindeutigen Lesart entgegen: **D-1**
> (Implementation Plan API-04 nennt nur die Signatur) und **D-2** (RDR-001 §2.2
> subsumiert Stage-Ausführungslogik unter „Verhalten", Invariante 5 beschränkt
> BootstrapManager-Verhalten auf drei Methoden). **Beide Konflikte werden gezeigt,
> nicht aufgelöst.**
>
> **Was F-3 prüfen darf:** die sechs in Kap. 17.2 aufgeführten Gegenstände —
> insbesondere §8-1, §8-2, §8-3, §8-5 und den Signatur-Teil von §8-4.
>
> **Was F-3 NICHT entscheiden darf:** ob Stage-interne Logik unter §8-4 fällt
> (**F2-U1**), sowie **F2-U2** bis **F2-U5**, **B-4**, **B-6** und **B-7**.
> Da die Ausgestaltung von OD-05 Option B nach ihrem eigenen Wortlaut genau in
> dieser unbestimmten Ebene läge, ist **G-1 — die menschliche Auslegungsentscheidung
> zu §8-4 — die vorrangige offene Governance-Position.**
>
> **ADR/RDR determination remains open.** Das NAW-1-Gesamtergebnis bleibt **D**.
>
> **CODING = NOT AUTHORIZED.**
> **Repository unverändert; genau eine neue Datei; kein Commit, kein Tag, kein Push.**

---

**Ende F-2 Bootstrap Baseline Scope Assessment — JOCHEN X Milestone 1.0
(FINAL ASSESSMENT, 2026-08-10, Referenz NAW-1 B-2 / GDR-OD05-001) —
Bezugs-Baseline `MILESTONE-1.0-BASELINE = 8fcf42f1997dfcf6ff232e75fd33c37b933991c8`**
