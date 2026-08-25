# JOCHEN X — Master Engineering Plan

| Feld | Wert |
|---|---|
| Dokumenttyp | Engineering Discovery & Build Plan |
| **Status** | **DRAFT** |
| **Revision** | **R0** |
| **Classification** | **NON-NORMATIVE ENGINEERING ANALYSIS** |
| Datum | 2026-08-10 |
| Rolle | Senior Principal Software Engineer / Technical Lead / Engineering Analyst |
| Phase | Phase 0 — Read-Only Engineering Discovery |
| Wirkung | **Keine.** Dieses Dokument ist keine Genehmigung, keine Governance-Entscheidung, keine Architekturentscheidung, keine Spezifikation und keine Coding-Freigabe. Es empfiehlt; es autorisiert nicht. |
| Autoritätsgrenze | Der Verfasser ist Engineering-Executor/Analyst. Projekteigner-, Governance-, Architektur-, Security- und Release-Autorität liegen ausdrücklich **nicht** beim Verfasser. |
| Baseline-Bezug | `MILESTONE-1.0-BASELINE = 8fcf42f1997dfcf6ff232e75fd33c37b933991c8` |

> **Lesehinweis zur Beweisführung.** Jede wesentliche Aussage trägt eine
> Quellenangabe in der Form `[SOURCE: <pfad> §<abschnitt>]` bzw.
> `[SOURCE: <pfad>:<zeilen>]`. Aussagen ohne Quellenangabe sind als
> **ENGINEERING INFERENCE** gekennzeichnet und ausdrücklich keine
> Quellenfakten. Es wurden keine Referenzen erfunden.

---

## 1. Executive Summary

### 1.1 Was JOCHEN X am Baseline tatsächlich ist

JOCHEN X ist am autoritativen Baseline-Commit ein **lokales PySide6-Desktop-Framework
mit einem manifestbasierten Plugin-System und einer Sicherheits-Foundation** —
rund **12.400 Zeilen produktiver Python-Code** über 15 Pakete
[SOURCE: Zeilenzählung über `core/`, `app/`, `plugins/`, `sdk/`, `services/`,
`developer/`, `ai/`, `ui/`, `database/`, `config/`, `styles/` am Baseline].
Es ist **kein KI-Assistent im Produktsinne**, **kein Agentensystem** und
**kein Trading-System**. Diese Fähigkeiten existieren am Baseline nicht,
weder implementiert noch autorisiert.

### 1.2 Governance-Zustand

Der Milestone-1.0-Strang ist bis einschließlich **SPR-01 (Baseline Confirmation)**
abgeschlossen. **RB-1.0 = 258 Tests / 14 Dateien** ist formal festgestellt
[SOURCE: docs/governance/milestone-1.0-sprint-01-baseline-confirmation.md §10]
und wurde im Rahmen dieser Analyse unabhängig reproduziert (Kap. 3.4).
**Coding ist nicht autorisiert**; die Coding-Bedingungen 7–9 des
Implementation Plans sind offen, RL-05 ist nicht erreicht
[SOURCE: docs/milestone-1.0-sprint-plan.md §6;
docs/governance/milestone-1.0-baseline-commit-record.md §12].

### 1.3 Die fünf wichtigsten technischen Befunde

| # | Befund | Klassifikation | Ref. |
|---|---|---|---|
| 1 | **Zweiter, undokumentierter Composition Root im produktiven Baum:** `app/host.py::ApplicationHost` existiert parallel zu `app/application_host.py::ApplicationHost` — gleicher Klassenname, gleiche `create_default()`-Fabrik, vollständig eigene Bootstrap-Logik ohne Security-Pipeline. GDR-002 deckt nur `src/jochen_x/**` ab, **nicht** diesen Fall. | OBSERVATION → TD-01 | Kap. 6.3 |
| 2 | **Packaging zeigt auf den stillgelegten Baum:** `pyproject.toml` konfiguriert `packages.find where = ["src"]`, `mypy_path = "src"`, `ruff src = ["src"]`. Build, Typprüfung und Linting adressieren `src/jochen_x/**`, nicht die produktive Struktur. | OBSERVATION → TD-02 | Kap. 7.6 |
| 3 | **Undeklarierte externe Abhängigkeit `ollama`** in `core/ai_manager.py`, konsumiert von `core/worker.py`. Widerspricht NFR-007 und der Charter-Out-of-Scope-Regel „Externe Abhängigkeiten". | OBSERVATION → TD-03 | Kap. 11.3 |
| 4 | **Runtime-Permission-Enforcement stützt sich auf die Selbstdeklaration des Plugins**, nicht auf das vom Host ermittelte Grant-Set. Das Ergebnis von `PluginSecurity.validate_permissions()` wird nie in den `PluginContext` übertragen. | OBSERVATION → TD-04 (Security) | Kap. 10.5 |
| 5 | **Sicherheitsrichtlinien sind nicht konfigurierbar verdrahtet:** `IntegrityPolicy.from_config()` und `PermissionPolicy.from_config()` haben **keine** produktive Aufrufstelle; `config/default.toml` enthält keinen `[security]`-Abschnitt. Die effektive Laufzeit-Policy ist damit fest verdrahtet. | OBSERVATION → TD-05 (Security) | Kap. 10.6 |

### 1.4 Plan-gegen-Realität — Kurzbild

Die Engineering Specification 1.0 beschreibt für Milestone 1.0 sieben Work
Packages und 14 Functional Requirements
[SOURCE: docs/milestone-1.0-engineering-spec.md §7.2, §7.3]. Die Gap-Analyse
des ES (§5.5) trifft in den meisten Bereichen zu, **überschätzt jedoch die
Lücke bei FR-001/FR-002 (Lifecycle-Determinismus)**: die
Zustandsmaschine ist am Baseline bereits vollständig tabellengetrieben, mit
expliziter Ablehnung unzulässiger Übergänge
[SOURCE: app/state_machine.py:41-61, :122-147]. Umgekehrt **unterschätzt die
Gap-Analyse die Lücke bei FR-010 (Failure Isolation)**: ein einziges
fehlerhaftes Manifest deaktiviert das gesamte Plugin-System (Kap. 9.3).

### 1.5 Empfehlung in einem Satz

**ENGINEERING INFERENCE / RECOMMENDATION:** Vor Beginn von Phase B (SPR-02+)
sollte der Projekteigner drei Punkte disponieren — (a) die ausstehende
Governance-Disposition der sechs uncommitteten Dokumentänderungen
(ADR-005/006/007, Architecture Book, CLAUDE.md, ROADMAP.md), (b) den Status
von `app/host.py` als zweitem Composition Root, (c) die Packaging-Konfiguration.
Alle drei sind **OPEN DECISION**, nicht vom Verfasser entscheidbar, und alle
drei berühren Nachweise, die spätere Quality Gates führen müssen.

---

## 2. Source Gate

### 2.1 Pflichtquellen — Verifikationstabelle

Methode: Existenz- und Statusprüfung am tatsächlichen Repository-Pfad; keine
Dateinamen wurden angenommen. Spalte **Ort** unterscheidet die drei
Repository-Welten aus Kap. 4.

| # | Pflichtquelle | Tatsächlicher Pfad | Dokument/Version | Status | Ort | Prüftiefe |
|---|---|---|---|---|---|---|
| 1 | Core Principles 1.0 | `docs/core-principles-1.0.md` | 1.0 R2 | APPROVED (2026-08-07) | BASELINE | Struktur + Kap. 0, 6, 7, 8, 9, 12 |
| 2 | Security Architecture 1.0 | `docs/security-architecture-1.0.md` | 1.0 R0 | APPROVED (2026-08-08) | BASELINE | Struktur + Kap. 3, 9, 11, 14, 24 |
| 3 | Security Design 1.0 | `docs/security-design-1.0.md` | 1.0 R0 | APPROVED (2026-08-09) | **UNTRACKED** | Struktur + Kap. 12, 16, 19, 22, 23 |
| 4 | Architecture Book v2.0 | `docs/architecture-book-v2.md` | v2.0 | APPROVED / FROZEN | BASELINE (+ WT-Mod.) | Struktur + Kap. 5, 10, 11, 20, 22 |
| 5 | Development Standard v1.1 | `docs/development-standard-v1.1.md` | v1.1 | APPROVED | **UNTRACKED** | Kopf, §3.3, §6.2 |
| 6 | Milestone 1.0 Charter | `docs/milestone-1.0-charter.md` | 1.0 | APPROVED (2026-08-02) | **UNTRACKED** | §4, §5, §6, §8 |
| 7 | Bootstrap Baseline 1.0 | `docs/baselines/bootstrap-baseline-1.0.md` | 1.0 | APPROVED (2026-08-01) | **UNTRACKED** | vollständig |
| 8 | Engineering Specification 1.0 | `docs/milestone-1.0-engineering-spec.md` | 1.0 R1 | APPROVED (2026-08-03) | **UNTRACKED** | §3, §5, §6, §7, §8 |
| 9 | Implementation Plan 1.0 | `docs/milestone-1.0-implementation-plan.md` | 1.0 R1.2 | APPROVED (2026-08-06) | BASELINE | selektiv (§3.1, §5.5.4, §11.10) über Sekundärquellen |
| 10 | Sprint Plan 1.0 | `docs/milestone-1.0-sprint-plan.md` | 1.0 R0 | **DRAFT**, genehmigt als Planungsgrundlage (ADW-SPR-1.0-001) | **UNTRACKED** | vollständig |
| 11 | Sprint Planning Approval Decision | `docs/governance/milestone-1.0-sprint-planning-approval-decision-op1.md` | — | FINAL | **UNTRACKED** | Kopf/Wirkung |
| 12 | Next Authorized Work Assessment | `docs/governance/jochen-x-next-authorized-work-assessment.md` | — | FINAL ASSESSMENT | **UNTRACKED** | vollständig |
| 13 | GR-001 Decision (GDR-002) | `docs/governance/gr-001-governance-decision.md` | GDR-002 | FINAL — ENTSCHIEDEN | **UNTRACKED** | vollständig |
| 14 | Baseline Identifier Decision | `docs/governance/milestone-1.0-baseline-identifier-decision.md` | GDR-003 | FINAL — OPTION A | **UNTRACKED** | über Baseline Commit Record §2 |
| 15 | Baseline Commit Record | `docs/governance/milestone-1.0-baseline-commit-record.md` | — | FINAL | **UNTRACKED** | vollständig |
| 16 | Approval-/Closing-Records | `docs/governance/*-approval-record.md`, `*-governance-closing-*.md` (16 Dateien) | — | vorhanden | teils BASELINE, teils UNTRACKED | Existenz + Statuszeilen |

**Ergänzend geprüft (nicht Pflichtquelle, aber entscheidungsrelevant):**
`docs/governance/milestone-1.0-sprint-01-baseline-confirmation.md` (FINAL),
`docs/governance/waiver-dev-001.md`, `docs/governance/waiver-amendment-001.md`,
`docs/governance/gdr-001-waiver-closing-criteria.md`, `docs/security.md`,
`docs/adr/001…011`, `docs/rdr/001-*`.

### 2.2 Source-Gate-Ergebnis

> **SOURCE GATE: BESTANDEN.** Alle 16 Pflichtquellen sind vorhanden, lesbar
> und statuskonform. Keine Pflichtquelle fehlt. Keine HARD-STOP-Bedingung
> gemäß Auftrag Kap. 26 Nr. 1 liegt vor.

### 2.3 Source-Gate-Findings (nicht blockierend)

**SG-01 — Pflichtquellen liegen überwiegend außerhalb des Baseline-Commits.**
Von den 16 Pflichtquellen sind **11 untracked**, d. h. nicht Bestandteil von
`MILESTONE-1.0-BASELINE`. Dazu zählen Charter, Engineering Specification,
Sprint Plan, Bootstrap Baseline, Security Design 1.0, GDR-002, GDR-003 und der
Baseline Commit Record selbst. Dies ist eine **dokumentierte, gewollte
Konsequenz** des GDR-003-Scopes (13 Include-Dateien, alle `docs/**`-Pfade
ausgeschlossen) [SOURCE: docs/governance/milestone-1.0-baseline-commit-record.md
§8, §10]. Es ist kein Fehler, hat aber eine Nachweisfolge (Kap. 4.4, RK-02).
Klassifikation: **OBSERVATION.**

**SG-02 — Der Sprint Plan trägt formal den Status DRAFT.**
Der Sprint Plan ist im Kopf `Status: DRAFT`
[SOURCE: docs/milestone-1.0-sprint-plan.md, Metadatentabelle], wird aber von
SPR-01 als „genehmigt durch ADW-SPR-1.0-001 (OP-1, APPROVED FOR SPRINT
EXECUTION PLANNING)" geführt
[SOURCE: docs/governance/milestone-1.0-sprint-01-baseline-confirmation.md §2].
Der Statuskopf des Plandokuments wurde nicht nachgeführt. Klassifikation:
**OBSERVATION (redaktionell)** — die Genehmigungskette ist eindeutig, es wird
kein Widerspruch konstruiert. Siehe OD-08.

**SG-03 — Pfadabweichung, bereits dokumentiert.**
Der Auftrag nennt „Approved Sprint Plan 1.0"; die tatsächliche Fundstelle ist
`docs/milestone-1.0-sprint-plan.md`, die Begleitzusammenfassung liegt unter
`docs/audits/milestone-1.0-sprint-planning-summary-r0.md`. Identisch mit dem
bereits erfassten F-SPR01-02
[SOURCE: docs/governance/milestone-1.0-sprint-01-baseline-confirmation.md §12].
Klassifikation: **NOT A BLOCKER.**

---

## 3. Baseline Verification

### 3.1 Identität

| Prüfung | Ergebnis |
|---|---|
| Commit-Objekt existiert | `git cat-file -t 8fcf42f1997dfcf6ff232e75fd33c37b933991c8` → `commit` — **PASS** |
| Commit-Subject | `chore(baseline): Milestone 1.0 Baseline Snapshot — RB-1.0 258/14, per GDR-003` — deckungsgleich mit dem Record — **PASS** [SOURCE: docs/governance/milestone-1.0-baseline-commit-record.md §1] |
| Commit-Datum | 2026-08-09 15:26:57 +0200 — **PASS** |
| Branch | `milestone-1.0-governance` — **PASS** |
| `git rev-parse HEAD` | `8fcf42f1997dfcf6ff232e75fd33c37b933991c8` — HEAD **ist** die Baseline — **PASS** |
| Vorgänger-HEAD | `63407ad…` gemäß Record §4 — konsistent mit der Commit-Historie — **PASS** |

> **BASELINE VERIFIED & REPRODUCIBLE.** Keine HARD-STOP-Bedingung gemäß
> Auftrag Kap. 26 Nr. 2.

### 3.2 Inhaltlicher Umfang

Der Baseline-Commit umfasst **262 getrackte Dateien**
[SOURCE: `git ls-tree -r --name-only 8fcf42f…`], davon:

| Menge | Umfang |
|---|---|
| Produktive Struktur (`core/`, `app/`, `plugins/`, `sdk/`, `services/`, `developer/`, `ai/`, `ui/`, `database/`, `config/`, `styles/`, `main.py`) | ~100 Dateien |
| Stillgelegter Baum `src/jochen_x/**` | 66 Dateien |
| Tests (`tests/**`) | 40 Dateien (14 RB-1.0 + 22 stillgelegt + 4 `__init__.py`) |
| Dokumentation (`docs/**`, `*.md`) | ~50 Dateien |
| Build/Meta (`pyproject.toml`, `.gitignore`) | 2 Dateien |

### 3.3 Verhältnis Working Tree ↔ Baseline — **entscheidender Befund**

```
git diff --name-only 8fcf42f… -- . ':(exclude)docs' ':(exclude)*.md'
→ (leer)

git status --porcelain -uall | grep '^??' | grep -v '^?? docs/'
→ (leer)
```

> **BV-01 (SOURCE FACT):** Der **produktive Quellcode des Working Tree ist
> byte-identisch mit dem Baseline-Commit.** Sämtliche 6 getrackten
> Modifikationen und sämtliche 67 untracked Dateien sind Markdown-/
> Dokumentationsartefakte. Es existiert **keine** uncommittete Code-, Test-
> oder Konfigurationsänderung.

Diese Feststellung ist methodisch wichtig: Für **Code-Aussagen** (Kap. 5–13,
15–21) fallen BASELINE und WORKING TREE zusammen; die Trennung nach Kap. 4
bleibt für **Dokumentaussagen** vollständig wirksam und wird dort konsequent
durchgehalten.

### 3.4 RB-1.0 Reproduktion

Methode: `pytest --collect-only -q -p no:cacheprovider` mit
`PYTHONDONTWRITEBYTECODE=1` über exakt die 14 in SPR-01 §7 gelisteten Dateien.
**Reine Kollektion, keine Testausführung, keine Dateiänderung.**

| Erwartung | Befund | Ergebnis |
|---|---|---|
| 14 Testdateien | 14 | ✓ |
| **258 Tests** | **258 tests collected in 0.29s** | **✓ REPRODUZIERT** |

> **RB-1.0 REPRODUCED** — unabhängig gegen den Baseline-Stand bestätigt
> [Vergleichsquelle: docs/governance/milestone-1.0-sprint-01-baseline-confirmation.md §8].
> Die Regressionsbezugsgröße wurde durch diese Analyse **nicht verändert**
> (Auftrag Kap. 22).

**Hinweis zur Testausführung:** Der Baseline Commit Record dokumentiert
`258 passed, 22 subtests passed`
[SOURCE: docs/governance/milestone-1.0-baseline-commit-record.md §9]. Diese
Analyse hat **keinen Testlauf durchgeführt** (Read-Only-Disziplin). Der
Pass-Zustand wird daher als **APPROVED EVIDENCE aus dem Record übernommen**,
nicht als eigene Messung ausgewiesen.

---

## 4. Repository State Separation

### 4.1 Die drei Welten

| Welt | Definition | Umfang | Beweiswert |
|---|---|---|---|
| **A — BASELINE** | `8fcf42f…` | 262 Dateien | **Autoritativ.** Einzige Grundlage für Aussagen über den Implementierungsstand. |
| **B — WORKING TREE** | 6 getrackte Modifikationen gegenüber A | `CLAUDE.md`, `ROADMAP.md`, `docs/adr/005`, `docs/adr/006`, `docs/adr/007`, `docs/architecture-book-v2.md` | **Nicht Baseline.** Governance-Disposition ausstehend. |
| **C — UNTRACKED** | 67 Dateien, ausschließlich unter `docs/**` | Governance-, Audit-, Planungs- und Spezifikationsbestand | **Dokumente, keine Implementierung.** Statuswerte gelten; Implementierungswirkung: keine. |

Diese Aufteilung entspricht exakt der im Baseline Commit Record §10
protokollierten Lage
[SOURCE: docs/governance/milestone-1.0-baseline-commit-record.md §10:
„Getrackte Änderungen: genau die 6 Excludes … Untracked: 67 Dateien,
ausschließlich unter `docs/**`"]. Die Zählung wurde unabhängig reproduziert
(6 + 67 = 73 Statuseinträge; `git status --porcelain` meldet 72 Zeilen, da
`docs/baselines/` und `docs/rdr/` als Verzeichniseinträge zusammengefasst
erscheinen — nach Auflösung mit `-uall` ergeben sich die dokumentierten 67
untracked Dateien).

### 4.2 Der Fall ADR-005/006/007 — **wesentlicher Trennungsbefund**

Dies ist der Punkt, an dem die Vermischung der Welten die größte
Fehlerwirkung hätte:

| Aspekt | Welt A (BASELINE) | Welt B (WORKING TREE) |
|---|---|---|
| `docs/adr/005-…md`, Statuszeile | `**Status:** Open – requires decision before implementation` | `**Status:** APPROVED` / `Approval Date: 2026-07-30` |
| `docs/adr/006-…md` | Open | APPROVED (2026-07-29) |
| `docs/adr/007-…md` | Open | APPROVED (2026-07-29) |
| `docs/architecture-book-v2.md` §20 | `ADR-005: **Status:** Open` … `ADR-006: Open` … `ADR-007: Open` | `Approved (2026-07-30)` … `Approved (2026-07-29)` |
| Umfang der Differenz | — | +1.415 / −119 Zeilen über 6 Dateien |

[SOURCE: `git diff 8fcf42f… -- docs/adr/005-plugin-integrity-validation.md`
Kopfzeilen; `git diff 8fcf42f… -- docs/architecture-book-v2.md` §20;
`git diff --stat 8fcf42f…`]

> **BV-02 (SOURCE FACT):** Am autoritativen Baseline-Commit tragen ADR-005,
> ADR-006 und ADR-007 den Status **„Open – requires decision before
> implementation"**. Der APPROVED-Inhalt existiert ausschließlich als
> uncommittete Working-Tree-Modifikation.

**Wirkung — nüchtern und ohne Auflösung.** Die Engineering Specification 1.0
führt in §3.2 die Evidenzen E-12/E-13/E-14 als „ADR-005/006/007 = APPROVED,
verifiziert: `docs/adr/005…md`"
[SOURCE: docs/milestone-1.0-engineering-spec.md §3.2]. Ebenso führt CLAUDE.md
(Welt B) „Genehmigte ADRs (Milestone 0.9): ADR-005/006/007 (APPROVED)". Diese
Evidenzen sind **gegen Welt B verifizierbar, gegen Welt A nicht**.

Der Baseline Commit Record hat diesen Zustand ausdrücklich erzeugt und die
Auflösung dem Projekteigner vorbehalten: „Separate Governance-Disposition für
die uncommitteten Änderungen an ADR-005, ADR-006, ADR-007 und Architecture
Book v2.0 — **nächster Entscheidungspunkt des Projekteigners**"
[SOURCE: docs/governance/milestone-1.0-baseline-commit-record.md §15 Nr. 4].

> **Dieser Analyse ist es untersagt, den Widerspruch aufzulösen.**
> Er wird als **OD-01 (Open Decision Register, Kap. 20)** geführt und in der
> Risikoliste als RK-02 gespiegelt. Es wird **nicht** behauptet, ADR-005/006/007
> seien am Baseline genehmigt; es wird **ebenso wenig** behauptet, sie seien es
> nicht — der Genehmigungsakt ist durch Approval Records belegt, die
> **Dokumentfassung** im Baseline gibt ihn nicht wieder.

**Zusatzbefund (Architecture Freeze).** Die Working-Tree-Modifikation berührt
das als FROZEN geführte Architecture Book v2.0. Der Sprint Plan qualifiziert
jede AB-Änderung als `BASELINE DEVIATION`
[SOURCE: docs/milestone-1.0-sprint-plan.md §4, SPR-07 Deliverables: „jede
AB-Änderung wäre BASELINE DEVIATION"]. Da die Änderung **nicht committet** und
ausdrücklich zur Disposition gestellt ist, wird sie hier **nicht** als
eingetretene Deviation gewertet, sondern als offener Dispositionsgegenstand
innerhalb OD-01. Klassifikation: **OPEN DECISION**, nicht `DEVIATION`.

### 4.3 Der stillgelegte Baum `src/jochen_x/**`

| Aspekt | Feststellung |
|---|---|
| Status | **STILLLEGUNG** gemäß GDR-002 D-2 [SOURCE: docs/governance/gr-001-governance-decision.md §8] |
| Umfang | 66 Python-Dateien, eigene `core/`-Struktur (`concurrency`, `di`, `events`, `plugin`, `recovery`, `registry`, `runtime`, `security`, `types`, `interfaces`, `observability`, `exceptions`) |
| Referenzierung durch `main.py` | **keine** — unabhängig verifiziert |
| Zugehöriger Testbestand | 22 Dateien / 761 Tests [SOURCE: docs/governance/milestone-1.0-sprint-01-baseline-confirmation.md §9] |
| Behandlung in dieser Analyse | **Nur inspiziert, soweit zur Verifikation von GDR-002 und zur Erklärung der Packaging-Konfiguration (Kap. 7.6) erforderlich.** Nicht reaktiviert, nicht migriert, nicht bewertet, nicht verändert. |

> Alle Aussagen über `src/jochen_x/**` in diesem Dokument sind **historisch
> bzw. konfigurationsbezogen** und begründen **keinen** produktiven
> Architektur-, Scope- oder Baseline-Bezug.

### 4.4 Nachweisfolge der Trennung

**ENGINEERING INFERENCE.** Die Quality Gates QG-005 (Traceability
Completeness) und QG-008 (Governance Compliance) sowie die Evidenzen EV-D03,
EV-G04, GV-03 und GV-05 verlangen Nachweise gegen einen eindeutig
identifizierbaren Stand [SOURCE: docs/milestone-1.0-sprint-plan.md §5, SPR-10].
Solange die normativen Eingaben (Charter, ES, Sprint Plan, Bootstrap Baseline,
Security Design) untracked sind und die ADR-Statusfassungen zwischen Welt A und
Welt B divergieren, ist ein solcher Nachweis **nur unter zusätzlicher
Bezugnahme auf die Welten B und C** führbar. Das ist keine Blockade der
Analyse; es ist ein **Nachweisrisiko für Phase D** (RK-02, Kap. 28).

---

## 5. Current State

Grundlage dieses Kapitels ist **ausschließlich Welt A**. Geplante Funktionalität
wird nirgends als vorhanden beschrieben.

### 5.1 Produktversion und Laufzeit

| Eigenschaft | Wert | Quelle |
|---|---|---|
| Anwendungsversion | `0.9.0` | [SOURCE: pyproject.toml:7] |
| SDK-Version | `0.9.0` | [SOURCE: sdk/version.py:24] |
| SDK-API-Version | `1.0.0` | [SOURCE: sdk/version.py:27] |
| Python | `>=3.13` | [SOURCE: pyproject.toml:9] |
| Deklarierte Laufzeitabhängigkeit | `PySide6>=6.8` (einzige) | [SOURCE: pyproject.toml:10-12] |
| Tatsächlich importierte, **nicht** deklarierte Abhängigkeit | `ollama` | [SOURCE: core/ai_manager.py:1] |
| Konfigurationsformat | TOML (`config/default.toml`, optional `config/profile.toml`) | [SOURCE: config/default.toml; app/host.py:43] |
| Persistenz | SQLite, `data/jochen_x.sqlite3` | [SOURCE: config/default.toml `[database] path`] |

### 5.2 Einstiegspunkt und tatsächlich gefahrener Pfad

`main.py` instanziiert `app.application_host.ApplicationHost` mit einem
**kundenspezifischen** Bootstrap-Manager aus
`ui.navigation.navigation_service.create_desktop_bootstrap_manager()` und
startet über `app.application.Application` mit `ui.navigation.main_window.MainWindow`
[SOURCE: main.py:1-27].

`create_desktop_bootstrap_manager()` **erweitert** `default_stages()` additiv:
es entfernt die `DependencyInjectionStage` aus der Standardsequenz, hängt
`SecurityBootstrapStage()` und `NavigationBootstrapStage()` an und stellt die
DI-Stage ans Ende
[SOURCE: ui/navigation/navigation_service.py:137-152].

> **CS-01 (SOURCE FACT):** Der produktive Einstiegspunkt fährt **nicht** die
> unveränderte `default_stages()`-Sequenz, sondern eine additiv erweiterte
> Komposition. Die relative Reihenfolge aller Baseline-Stages bleibt dabei
> erhalten; lediglich die DI-Stage wandert ans Ende (mit dokumentierter
> Begründung: „so its graph validation includes extension services").
> Bewertung gegen Bootstrap Baseline §4 Invariante 4 siehe Kap. 8.4.

### 5.3 Bestandsaufnahme nach Bereich

| Bereich | Ist-Zustand am Baseline | Klassifikation |
|---|---|---|
| **Bootstrap** | 7 Module, 13 Standard-Stages, 4 Phasen, Protocol-basiert, `BootstrapManager` als `frozen dataclass` | **EXISTING**, vollständig |
| **Application Host** | `app/application_host.py` — Startup/Shutdown/Restart/Recover/Health, Qt-frei | **EXISTING**, vollständig |
| **Zweiter Host** | `app/host.py` — monolithischer Composition Root, Qt-gebunden, nur von `tests/test_foundation.py` referenziert | **EXISTING (Altbestand)**, siehe TD-01 |
| **Zustandsmaschine** | 10 Zustände, explizite Adjazenztabelle, thread-safe, Event-emittierend | **EXISTING**, vollständig |
| **Event-System** | `core.events.EventBus` — Prioritäten, Filter, Sticky Events, Wildcards, History, Delivery-Diagnostik, sync + async | **EXISTING**, vollständig |
| **Service Registry** | Typisiert, 3 Lifetimes, Konstruktor-Injektion, Zyklenerkennung, `validate()`, `descriptors()` | **EXISTING**, mit Lücken (Kap. 6.5) |
| **Plugin-Discovery** | Manifest-only, kein Code-Import; v1/v2-Manifeste | **EXISTING** |
| **Plugin-Security** | Trust Ledger, Integrity (structural), Permissions (default-deny), Dependency Resolution (DAG + Zyklen + Kaskade) | **EXISTING**, mit Lücken (Kap. 10) |
| **Plugin-Activation** | Import, Instanziierung, Wiring, Start; per-Plugin-Fehlerisolation | **EXISTING** |
| **SDK** | 12 Module, 2.551 Zeilen; `Plugin`-ABC + 4 Spezialisierungen, `PluginRuntime`, `PluginContextBuilder`, Manifest-Modell, Config-Storage, Ressourcen, Events, Fehler | **EXISTING**, umfangreichste Einzelschicht |
| **Security Foundation** | 15 Module, 2.452 Zeilen; Vault, Encryption, Permissions, Identity, Audit, API-Keys, Broker, Threat Detection, Backups | **EXISTING**, teils Platzhalter (Kap. 10.7) |
| **Observability** | `Metrics` (Zähler/Dauern), `Tracer`/`Span`, `HealthCheck`-Protocol, `PluginHealthCheck`, `ActivationFailure` | **EXISTING**, minimal |
| **UI** | `ui/navigation/**` (17 Module) produktiv; `ui/*.py` (9 Module) Altbestand | **EXISTING**, dupliziert (Kap. 6.6) |
| **Developer Platform** | Optional, `Inspector`, `Diagnostics`, `DeveloperPlatform` | **EXISTING**, klein (214 Zeilen) |
| **AI** | `ai/gateway.py` (Metadaten/Routing, **keine Ausführung**), `core/ai_contracts.py` (Protocols), `core/ai_manager.py` (**ollama-Aufruf**) | **EXISTING, inkonsistent** (Kap. 11) |
| **Memory** | — | **NICHT VORHANDEN** |
| **Agents / Automation** | — | **NICHT VORHANDEN** |
| **Multimodal** | Nur Capability-Enums (`VISION`, `SPEECH`, `TRANSCRIPTION`) ohne Implementierung | **NICHT VORHANDEN** |
| **Trading** | — **keine** Trading-UI, **kein** Scaffolding, **kein** Broker-Connector. Lediglich `app/security/broker_security.py` als Security-Baustein | **NICHT VORHANDEN** (Kap. 14) |
| **Packaging** | `setuptools`, `packages.find where=["src"]` | **EXISTING, fehlgeleitet** (TD-02) |
| **CI** | **Keine** CI-Konfiguration im Repository (kein `.github/`, kein `*.yml`-Workflow) | **NICHT VORHANDEN** (TD-09) |

### 5.4 Startverhalten

```
main() → ApplicationHost(root, bootstrap_manager=desktop)
       → Application(host, window_factory).run()
       → host.start() → StartupSequence.execute(root)
            STARTING
            ├─ transition → INITIALIZING
            │    run_phase(INITIALIZE): Environment, Configuration, Logging,
            │                          Database, Registry, Theme, Scheduler
            │    publish ApplicationStarting(version), ApplicationStarted(count)
            ├─ transition → LOADING_PLUGINS
            │    run_phase(LOAD_PLUGINS): PluginDiscovery, PluginSecurity
            ├─ transition → LOADING_RESOURCES
            │    run_phase(LOAD_RESOURCES): Resource
            ├─ run_phase(FINALIZE): PluginActivation, DeveloperTools,
            │                       SecurityBootstrap, Navigation, DI
            ├─ build_context(...)  ← _require() für 12 Pflichtfelder
            └─ transition → READY ; publish ApplicationReady(startup_ms)
```
[SOURCE: app/startup.py:47-82; app/bootstrap/manager.py:43-104;
ui/navigation/navigation_service.py:137-152]

> **CS-02 (SOURCE FACT):** Die FINALIZE-Phase führt `PluginActivationStage`
> **vor** `SecurityBootstrapStage` aus. Konsequenz siehe Kap. 10.6.

### 5.5 Shutdown-Verhalten

`ApplicationHost.shutdown()` stoppt Plugin-Runtimes in **umgekehrter
Aktivierungsreihenfolge** mit Einzelfehler-Isolation und führt anschließend
`ShutdownSequence` mit Disposables und Worker-Pool aus
[SOURCE: app/application_host.py:124-152]. `DisposableRegistry.dispose_all()`
gibt in umgekehrter Registrierungsreihenfolge frei und kapselt jeden Fehler
[SOURCE: app/di.py:94-108].

### 5.6 Fehlerbehandlung

`CentralErrorHandler` klassifiziert typbasiert (nicht per String-Matching),
loggt, publiziert `ErrorRaised` und eskaliert fatale Fehler über einen
injizierten Callback [SOURCE: app/errors.py:124-155]. Fatal-Kategorien:
`FATAL`, `CONFIGURATION`, `DATABASE`, `UNEXPECTED`
[SOURCE: app/errors.py:64-69].

> **CS-03 (ENGINEERING INFERENCE):** Ein unbekannter Ausnahmetyp fällt in
> `UNEXPECTED` und ist damit **fatal**. Da Plugin-Fehler in der
> Activation-Stage lokal gefangen werden (Kap. 9.4), erreicht ein Plugin-Fehler
> diesen Pfad normalerweise nicht — die Default-Fatal-Einstufung wirkt aber für
> alle sonstigen unklassifizierten Fehler. Bewertung: konservativ und
> vertretbar (fail-secure), aber begünstigt harte Abbrüche bei
> Drittbibliotheks-Ausnahmen.

---

## 6. Architecture Map

### 6.1 Soll-Schichtung

```
Core → App → Plugins/SDK → Services → Developer → UI
```
Abhängigkeiten zeigen nach innen; keine Schicht importiert aus einer äußeren
[SOURCE: docs/architecture-book-v2.md §5; CLAUDE.md „Schichtmodell"].

### 6.2 Ist-Abhängigkeitsrichtung — Verifikation

| Prüfung | Methode | Ergebnis |
|---|---|---|
| Consumer importieren Bootstrap **nur** über die Paket-Fassade (Baseline §4 Inv. 7) | `grep "from app\.bootstrap\.\|import app\.bootstrap\."` außerhalb `app/bootstrap/` | **0 Treffer — PASS** |
| `core/` importiert nicht aus `app/`, `ui/`, `sdk/` | Import-Scan | **PASS** |
| `sdk/` importiert nicht aus `core`, `app`, `plugins` (ADR-010) | Import-Scan | **PASS** — SDK bringt eigenes `ApiVersion` [SOURCE: sdk/version.py:31-38] |
| `core/` importiert **externe** Provider | `core/ai_manager.py:1` → `import ollama` | **VERLETZUNG** (TD-03) |
| `core/worker.py` importiert `PySide6` und `core.ai_manager` | [SOURCE: core/worker.py:1-3] | **VERLETZUNG** — UI-Framework und AI-Provider im innersten Ring |

> **AM-01 (SOURCE FACT):** Die Schichtdisziplin ist über den weit überwiegenden
> Teil des Codes eingehalten. Die einzigen belegten Verstöße liegen in
> `core/ai_manager.py` und `core/worker.py` — beide gehören zu einem
> augenscheinlich älteren, nicht in die Bootstrap-Komposition eingebundenen
> Bestand (Kap. 11.3).

### 6.3 Doppelter Composition Root — **TD-01**

| Merkmal | `app/application_host.py` | `app/host.py` |
|---|---|---|
| Klassenname | `ApplicationHost` | `ApplicationHost` |
| Fabrik | `create_default()` | `create_default()` |
| Docstring-Anspruch | „the root lifecycle orchestrator" | „**the sole composition root** and lifecycle owner" |
| Bootstrap | `BootstrapManager` + Stages | monolithische `bootstrap()`-Methode, 28 direkte `services.register(...)` |
| Zustandsmaschine | ja | **nein** |
| Plugin-Security-Pipeline | ja | **nein** — registriert `PluginLoader` direkt [SOURCE: app/host.py:60] |
| Plugin-Aktivierung | ja | **nein** (kein Code-Import) |
| Qt-Kopplung | frei | `QApplication`, `FoundationWindow` [SOURCE: app/host.py:6, :24] |
| Produktive Referenz | `main.py:16` | **keine** |
| Referenz überhaupt | — | `tests/test_foundation.py:8` (RB-1.0!) |

[SOURCE: app/application_host.py:1-30; app/host.py:1-38, :40-77]

> **AM-02 (SOURCE FACT):** Es existieren zwei gleichnamige Composition Roots im
> produktiven Baum. Der zweite ist im Produktionspfad tot, wird aber durch eine
> RB-1.0-Testdatei am Leben gehalten.
>
> **AM-03 (ENGINEERING INFERENCE):** Dieser Fall ist strukturell **analog** zu
> GR-001, aber **von GDR-002 nicht erfasst** — GDR-002 entscheidet ausschließlich
> über `src/jochen_x/**` [SOURCE: docs/governance/gr-001-governance-decision.md
> §2, §12]. Es liegt damit ein **nicht disponierter Parallelbestand innerhalb
> der als produktiv entschiedenen Struktur** vor. → **OD-02.**
>
> **Sicherheitsrelevante Nebenwirkung:** `app/host.py` würde bei Verwendung die
> Plugin-Runtime-Pipeline vollständig umgehen. Da es keinen Plugin-Code
> importiert, entsteht am Baseline **kein** Ausführungsrisiko; das Risiko ist
> **latent** und würde erst bei Wiederinbetriebnahme akut. Klassifikation:
> **OBSERVATION, nicht Finding.**

### 6.4 Öffentliche Schnittstellen

| Schnittstelle | Symbolzahl | Stabilitätszusage |
|---|---|---|
| `app.bootstrap.__all__` | **22** | Bootstrap Baseline §3.1 (dort als „20 Symbole" überschrieben — siehe TD-08) |
| `sdk.__all__` | öffentliche Plugin-API | SDK API 1.0.0, additiv (NFR-003) |
| `core.registry.ServiceRegistry` | Kompositionsmechanismus | Architecture Book v2.0 §8 |
| `core.events.EventBus` | Event-Kontrakt | Architecture Book v2.0 §9, ADR-002 |

### 6.5 Interne Schnittstellen und Kapselungsbrüche

> **AM-04 (SOURCE FACT):** An **zwei** Stellen greift Code außerhalb von
> `core/registry.py` auf private Registry-Interna zu:
>
> ```python
> with registry._lock:
>     registry._registrations.pop(PluginCatalog, None)
> ```
> [SOURCE: app/bootstrap/stages_plugin.py:337-338]
>
> ```python
> with registry._lock:
>     registry._registrations.pop(PluginSecurity, None)
> ```
> [SOURCE: app/security/security_manager.py:202-203]

Ursache ist eine fehlende Fähigkeit der öffentlichen Registry-API: `register()`
wirft `ValueError` bei bereits vorhandenem Schlüssel
[SOURCE: core/registry.py:80-83]; ein `replace()`/`override()` existiert nicht.
Die Aufrufer benötigen aber genau das (Katalogverengung nach der
Security-Stage; Ersetzen der Default-`PluginSecurity` durch die vom
`SecurityManager` komponierte Instanz). → **TD-06**, Empfehlung in Kap. 30.

### 6.6 Duplikation im UI-Bestand

| Produktiv (`ui/navigation/`) | Altbestand (`ui/`) | Referenziert von |
|---|---|---|
| `main_window.py` | `foundation_window.py` | nur `app/host.py:24` |
| `sidebar.py` | `sidebar.py` | — |
| `status_bar.py` | `status_bar.py` | — |
| — | `chat_page.py`, `chat_bubble.py`, `input_bar.py`, `message_widget.py`, `dashboard.py` | teils untereinander |

[SOURCE: Dateiinventar `ui/` und `ui/navigation/` am Baseline]

> **AM-05 (ENGINEERING INFERENCE):** Der `ui/`-Altbestand (355 Zeilen über
> 9 Module) hängt am selben Faden wie `app/host.py`. Die Chat-Module deuten auf
> die frühere, direkt an `core/worker.py`/`core/ai_manager.py` gekoppelte
> KI-Oberfläche hin. → gemeinsame Disposition mit OD-02 empfohlen.

### 6.7 Zyklen, versteckte Abhängigkeiten, Kopplung

| Prüfung | Ergebnis |
|---|---|
| Import-Zyklen im Bootstrap-Paket (Baseline §4 Inv. 2) | **keine** — `types` ← `constants` ← `stages_*` ← `manager` ← `__init__` eingehalten [SOURCE: Import-Header aller 7 Module] |
| Verzögerte Imports (`import` im Funktionskörper) | **10 Stellen** in `stages_plugin.py` (`sdk.version`, `app.security.events`, `app.security.plugin_security`, `importlib`, `sys`, `core.events`, `sdk.config`, `sdk.context`, `sdk.manifest`, `sdk.plugin`) [SOURCE: app/bootstrap/stages_plugin.py:83, :254-257, :359, :419, :451-459] |
| Bewertung | **ENGINEERING INFERENCE:** Diese Verzögerung ist architektonisch **gewollt** — sie hält `app/bootstrap` frei von einer harten Kompilierzeit-Abhängigkeit auf `sdk` und `app.security` und stützt die azyklische Fassade. Preis: Import-Fehler treten erst zur Laufzeit auf und sind statisch schlechter prüfbar. **Kein Defekt.** |
| Zyklische Dienstauflösung | Wird erkannt: `CircularDependencyError` mit vollständigem Pfad [SOURCE: core/registry.py:127-130] |

### 6.8 Architektur — Stärken

1. **Manifest-only Discovery ist real durchgesetzt.** `PluginLoader` liest
   ausschließlich TOML und importiert nachweislich keinen Plugin-Code
   [SOURCE: plugins/loader.py:44-61] — ADR-001 eingehalten.
2. **Stage-Protocol statt Vererbung.** `BootstrapStage` ist ein `Protocol`;
   jede Stage ist ein `frozen dataclass` mit `execute(context)`. Sehr gut
   testbar; die 258 RB-1.0-Tests nutzen genau diese Eigenschaft.
3. **Saubere SDK-Entkopplung.** Das SDK re-exportiert keinen Framework-Typ;
   `ApiVersion` ist eigenständig [SOURCE: sdk/version.py:31-38] — ADR-010
   eingehalten, verifiziert.
4. **Immutable Value Types durchgängig.** `frozen=True, slots=True` bei
   Manifest, Katalog, Diagnostics, Verdicts, Reports, Events.
5. **Deterministische Aktivierungsreihenfolge.** Topologische Sortierung mit
   stabiler lexikografischer Tie-Breaking-Regel
   [SOURCE: app/bootstrap/stages_plugin.py:180-190] — reproduzierbar.
6. **Reverse-Order-Teardown** an beiden relevanten Stellen (Plugins,
   Disposables).

### 6.9 Architektur — Schwächen

1. Doppelter Composition Root (AM-02, TD-01).
2. Kapselungsbrüche an der Registry (AM-04, TD-06).
3. Fehlende Thread-Sicherheit in Teilen der Registry (Kap. 21.4, TD-07).
4. `ServiceRegistry` vermengt zwei Rollen: einfacher Instanz-Container
   (`register`) und reflektierender Auto-Wiring-Container (`_construct` mit
   `get_type_hints`) [SOURCE: core/registry.py:152-171]. **ENGINEERING
   INFERENCE:** Die zweite Rolle wird im produktiven Pfad kaum genutzt
   (alle Bootstrap-Registrierungen sind Instanzen), trägt aber die volle
   Komplexität und die Race-Bedingungen. Kandidat für Vereinfachung —
   jedoch `validate()`-relevant und damit **nicht ohne Prüfung** änderbar.
5. `Metrics` als globaler, unsynchronisierter `dict[str, float]` ohne
   Kardinalitätsgrenze [SOURCE: core/observability.py:20-31] (TD-10).

---

## 7. Runtime Analysis

### 7.1 Prozessmodell

Ein Prozess, ein Python-Interpreter. Plugins laufen **in-process** ohne
Sandbox: `importlib.import_module(identifier)` mit anschließender
Instanziierung im selben Adressraum
[SOURCE: app/bootstrap/stages_plugin.py:501-518].

> **RT-01 (SOURCE FACT):** Es existiert **keine** Prozess-, Thread- oder
> Interpreter-Isolation für Plugins. Ein aktiviertes Plugin besitzt volle
> Python-Rechte des Hostprozesses.

Dies ist konsistent mit dem dokumentierten Stand: ADR-009 trägt den Titel
„Plugin Isolation Strategy" und ist Teil des ADR-Bestands
[SOURCE: docs/adr/009-plugin-isolation-strategy.md]; das Security Design führt
Plugin-/Agent-Sicherheit in Kap. 12 und offene Designentscheidungen in Kap. 19
[SOURCE: docs/security-design-1.0.md §12, §19]. Bewertung und Konsequenz:
Kap. 10.4.

### 7.2 Nebenläufigkeit

| Mechanismus | Ort | Bewertung |
|---|---|---|
| `WorkerPool` | `app/concurrency.py` | Hintergrundarbeit des Hosts; von `ApplicationHost` besessen und beim Shutdown gestoppt |
| `TaskScheduler` | `core/scheduler.py` | Registriert in INITIALIZE |
| `RLock` in `EventBus`, `ApplicationStateMachine`, `PluginSecurity`, `ServiceRegistry` (teilweise) | jeweils | siehe Kap. 21.4 |
| `BackgroundPlugin` | `sdk/plugin.py:149-207` | SDK-seitiger Thread mit `stop_event` und `_run_background_safe` |
| Qt-Threads | `core/worker.py` | Altbestand, nicht in der Bootstrap-Komposition |

### 7.3 Globale Zustandsmutation während der Aktivierung

```python
parent = str(plugin_dir)
added_to_path = parent not in sys.path
if added_to_path:
    sys.path.insert(0, parent)
try:
    ... importlib.import_module(identifier) ...
finally:
    if added_to_path:
        sys.path.remove(parent)
```
[SOURCE: app/bootstrap/stages_plugin.py:471-478, :573-578]

> **RT-02 (SOURCE FACT):** Das Plugin-Verzeichnis wird während der gesamten
> Aktivierungsschleife an **Position 0** von `sys.path` eingefügt und danach
> wieder entfernt. Die `finally`-Behandlung ist korrekt und idempotent.
>
> **RT-03 (ENGINEERING INFERENCE / SECURITY OBSERVATION):** Position 0 hat
> Vorrang vor der Standardbibliothek. Ein Plugin-Verzeichnis, das ein Modul mit
> einem stdlib-Namen enthält (z. B. `logging/`, `json/`, `secrets/`), würde
> **jeden** während der Aktivierung stattfindenden Import dieses Namens
> beschatten — auch Imports des Hosts und anderer Plugins. Der Effekt endet mit
> dem `finally`, bereits geladene Module bleiben jedoch in `sys.modules`.
> Bewertung: reales, aber an Dateisystemzugriff auf `plugins/` gebundenes
> Risiko. → Kap. 10.3, **kein** Finding-Status, da keine Security-Entscheidung
> vorliegt, die dies verböte.

### 7.4 Fehlende Bereinigung von `sys.modules`

Bei Restart/Recover (`ApplicationHost._reset()` → `start()`) werden Stages neu
ausgeführt, aber bereits importierte Plugin-Module verbleiben in `sys.modules`
[SOURCE: app/application_host.py:154-174, :195-201 — kein `sys.modules`-Eingriff].

> **RT-04 (ENGINEERING INFERENCE):** Nach `restart()` liefert
> `importlib.import_module(identifier)` das **zwischengespeicherte** Modul.
> Ein neu deployter Plugin-Code würde nicht wirksam; ein zuvor entferntes
> Plugin bliebe importierbar. Für den Desktop-Anwendungsfall (Neustart des
> Prozesses) ist das folgenlos; für `restart()`/`recover()` **innerhalb**
> desselben Prozesses ist es ein Korrektheitsdefekt. → **TD-11.**
> Bemerkenswert: `tests/test_golden_reference.py:35-41` implementiert exakt
> diese Bereinigung als Testhilfe — die Notwendigkeit ist im Testbestand
> bereits erkannt, im Produktcode aber nicht adressiert.

### 7.5 Dateisystem-Seiteneffekt in der Aktivierung

```python
resources_root = plugin_dir / identifier / "resources"
resources_root.mkdir(parents=True, exist_ok=True)
```
[SOURCE: app/bootstrap/stages_plugin.py:529-530]

> **RT-05 (SOURCE FACT):** Die Aktivierung **schreibt** in das
> Plugin-Verzeichnis. Bei schreibgeschützter Installation schlägt die
> Aktivierung des betroffenen Plugins fehl (wird lokal gefangen, Kap. 9.4).
> Klassifikation: **OBSERVATION** — für ein lokales Desktop-Framework
> vertretbar, für ein späteres paketiertes Deployment relevant.

### 7.6 Packaging und Werkzeugkonfiguration — **TD-02**

```toml
[tool.setuptools.packages.find]
where = ["src"]
...
[tool.mypy]
mypy_path = "src"
[tool.ruff]
src = ["src"]
[tool.pytest.ini_options]
testpaths = ["tests"]
```
[SOURCE: pyproject.toml:14-29]

> **RT-06 (SOURCE FACT):** Build-Discovery, mypy-Pfad und ruff-Quellpfad zeigen
> auf `src/` — den gemäß GDR-002 D-2 **stillgelegten** Baum. Die produktive
> Struktur (`core/`, `app/`, `sdk/`, …) liegt im Repository-Wurzelverzeichnis
> und wird von keiner dieser Konfigurationen erfasst.
>
> **RT-07 (ENGINEERING INFERENCE):** Konsequenzen: (a) `pip install .` erzeugt
> ein Distributionspaket, das ausschließlich `jochen_x` enthält und die
> produktive Anwendung **nicht** ausliefert; (b) `mypy`/`ruff` prüfen ohne
> explizite Pfadangabe den falschen Baum; (c) `pytest` ohne Pfadargument
> sammelt alle 1.019 Tests, also RB-1.0 **plus** den stillgelegten Bestand.
>
> Dieser Zustand ist eine **direkte, unbereinigte Folge** der GR-001-Entscheidung.
> GDR-002 D-2 hat die *physische* Behandlung ausdrücklich ausgeklammert
> [SOURCE: docs/governance/gr-001-governance-decision.md §8 D-2]; die
> *Konfigurationsfolge* ist dort nicht adressiert. → **OD-03.**

### 7.7 Kein CI

Es existiert keine CI-Konfiguration im Repository (weder `.github/workflows/`
noch vergleichbare Dateien im Baseline-Inventar).

> **RT-08 (ENGINEERING INFERENCE):** Sämtliche Regressions-, Gate- und
> Evidenznachweise (EV-I01, QG-001, QG-007) müssen derzeit **manuell und
> lokal** erbracht werden. Für einen Milestone, dessen Abschluss auf
> reproduzierbaren Nachweisen beruht, ist das ein Reifegradthema. →
> **TD-09**, Empfehlung in Kap. 30 (PC-05).

---

## 8. Bootstrap Analysis

### 8.1 Struktur

7 Module, 1.153 Zeilen, deckungsgleich mit dem in Bootstrap Baseline 1.0 §2
beschriebenen Scope [SOURCE: docs/baselines/bootstrap-baseline-1.0.md §2 vs.
Dateiinventar `app/bootstrap/`]. **MATCH.**

### 8.2 Invarianten-Prüfung (Bootstrap Baseline §4)

| # | Invariante | Prüfmethode | Ergebnis |
|---|---|---|---|
| 1 | Deklarative Paket-Fassade — nur Imports und `__all__` | Sichtprüfung `__init__.py` | **PASS** — 69 Zeilen, ausschließlich Imports und `__all__` [SOURCE: app/bootstrap/__init__.py] |
| 2 | Azyklischer Import-Graph | Import-Header aller Module | **PASS** (Kap. 6.7) |
| 3 | `BootstrapManager` einziger Einstiegspunkt | Aufrufstellen von `run_phase`/`begin` | **PASS** — nur `app/startup.py:57-76` |
| 4 | `default_stages()` bewahrt Reihenfolge | Sichtprüfung | **PASS** — deterministisches Tupel, 13 Stages [SOURCE: app/bootstrap/manager.py:43-59] |
| 5 | `StartupPhase`-Reihenfolge 1→2→3→4 | Enum-Werte | **PASS** [SOURCE: app/bootstrap/types.py:45-51] |
| 6 | Plugin-Runtime-Pipeline bewahrt | Ablauf-Analyse | **PASS mit Präzisierung** (Kap. 8.5) |
| 7 | Keine internen Imports durch Consumer | `grep` | **PASS** — 0 Treffer (Kap. 6.2) |

> **BS-01 (SOURCE FACT):** Alle sieben Baseline-Invarianten sind am Baseline
> eingehalten. NFR-002 ist am Ausgangspunkt **erfüllt**.

### 8.3 Public-Export-Abgleich

| Quelle | Zahl |
|---|---|
| Bootstrap Baseline §3.1, Überschrift | „Öffentliche Exports (**20 Symbole**)" |
| Bootstrap Baseline §3.1, tatsächliche Aufzählung | 6 + 2 + 7 + 4 + 3 = **22** |
| `app/bootstrap.__all__` (Code) | **22** |

[SOURCE: docs/baselines/bootstrap-baseline-1.0.md §3.1;
app/bootstrap/__init__.py:45-68]

> **BS-02 (SOURCE FACT):** Der **Code stimmt mit der Aufzählung der Baseline
> überein (22)**. Abweichend ist allein die **Überschriftenzahl „20"** im
> Baseline-Dokument. Es liegt also **kein Code-Defekt** und **keine
> API-Verletzung** vor, sondern eine **redaktionelle Inkonsistenz im
> Baseline-Dokument**. → **TD-08**, Klassifikation **OBSERVATION
> (redaktionell)**. Relevanz: API-04/NFR-002-Nachweise in SPR-09 zählen gegen
> diesen Text; eine falsche Zahl kann dort einen Scheinbefund erzeugen.

Die zwei internen Re-Exports (`_require`, `_validate_for_activation`) sind
vorhanden und korrekt **nicht** in `__all__`
[SOURCE: app/bootstrap/__init__.py:33, :42 vs. :45-68] — deckungsgleich mit
Baseline §3.2. **MATCH.**

### 8.4 Additive Erweiterung durch den Desktop-Manager

`create_desktop_bootstrap_manager()` erzeugt eine **Instanz** von
`BootstrapManager` mit erweiterter Stage-Liste; `default_stages()` selbst
bleibt unverändert [SOURCE: ui/navigation/navigation_service.py:143-152].

> **BS-03 (ENGINEERING INFERENCE):** Bewertung gegen Baseline §4 Inv. 4:
> Die Invariante bindet **`default_stages()`**, nicht jede
> `BootstrapManager`-Instanz; `stages` ist ein öffentlich vorgesehener
> Konstruktor-Parameter [SOURCE: app/bootstrap/manager.py:66]. Architecture
> Book v2.0 §22.2 stellt „neue Stages" ausdrücklich additiv und ADR-frei
> [SOURCE: docs/milestone-1.0-engineering-spec.md §3.5, E-15].
> **Bewertung: MATCH / zulässige additive Erweiterung.** Kein Finding.
>
> **Nebenbefund:** Die Verschiebung der `DependencyInjectionStage` ans Ende ist
> eine *Umordnung innerhalb der FINALIZE-Phase*. Sie verändert weder die
> Phasenfolge (Inv. 5) noch die Plugin-Pipeline-Reihenfolge (Inv. 6). Sie ist
> begründet dokumentiert. **Kein Finding**, aber ein Punkt, den ein
> SPR-09-Nachweis explizit adressieren sollte (Kap. 25, QG-003).

### 8.5 Plugin-Runtime-Pipeline — Ist-Ablauf

| Soll (Baseline §5.2) | Ist | Ort |
|---|---|---|
| Discovery | `PluginDiscoveryStage.execute` | LOAD_PLUGINS [SOURCE: stages_plugin.py:42-68] |
| Integrity Validation (ADR-005) | `security.validate_integrity(manifest)` | LOAD_PLUGINS, Schritt 1 [SOURCE: stages_plugin.py:275] |
| *(zusätzlich)* API-Version-Gate | `host_api.is_compatible_with(plugin_api)` | LOAD_PLUGINS, Schritt 2 [SOURCE: stages_plugin.py:287-303] |
| Permission Authorization (ADR-006) | `security.validate_permissions(manifest)` | LOAD_PLUGINS, Schritt 3 [SOURCE: stages_plugin.py:306] |
| Dependency Resolution (ADR-007) | `_resolve_dependencies(...)` | LOAD_PLUGINS, Schritt 4 [SOURCE: stages_plugin.py:328] |
| Activation | `PluginActivationStage.execute` | **FINALIZE** [SOURCE: stages_plugin.py:448] |

> **BS-04 (SOURCE FACT):** Die **Reihenfolge** der fünf Pipeline-Schritte ist
> exakt eingehalten. Invariante 6 ist erfüllt. Die Aktivierung liegt
> phasenmäßig in FINALIZE, was mit Baseline §5.1 übereinstimmt.
>
> **BS-05 (SOURCE FACT):** Die Pipeline enthält einen **zusätzlichen**,
> in Baseline §5.2 nicht aufgeführten Schritt (API-Version-Gate) zwischen
> Integrity und Permission. Er ist im Docstring als „Step 2 — API Version Gate
> (WP-03)" ausgewiesen [SOURCE: stages_plugin.py:236-247] und wirkt
> ausschließlich **verschärfend** (zusätzliche Ablehnungsmöglichkeit vor
> Code-Import). Bewertung: **PARTIAL MATCH** — Reihenfolge unverletzt,
> Schrittmenge erweitert. Da restriktiv und additiv: **kein Sicherheitsdefekt**,
> aber eine **Dokumentationslücke** zwischen Code und Baseline §5.2. → **TD-12.**

### 8.6 Kontextaufbau und Pflichtfelder

`build_context()` erzwingt 12 Pflichtfelder über `_require(...)` und wirft
`BootstrapError` bei fehlender Belegung
[SOURCE: app/bootstrap/manager.py:88-104; app/bootstrap/types.py:115-119].

> **BS-06:** Sauberer Fail-Fast-Übergang von mutablem `BootstrapContext` zu
> immutablem `ApplicationContext`. **Stärke.**

### 8.7 Fehlerbehandlung im Manager

```python
except BootstrapError:
    raise
except Exception as error:
    raise BootstrapError(f"Bootstrap stage failed: {stage.name}") from error
```
[SOURCE: app/bootstrap/manager.py:81-86]

> **BS-07:** Jeder Stage-Fehler wird auf `BootstrapError` normalisiert, der
> Stage-Name bleibt erhalten, die Ursache wird verkettet. Der Fehler propagiert
> zu `ApplicationHost.start()`, wird dort als `FATAL` klassifiziert und erneut
> geworfen [SOURCE: app/application_host.py:115-119]. **Determiniertes
> Startversagen. Stärke.**

---

## 9. Plugin / SDK Analysis

### 9.1 Discovery

```python
for path in self._directory.glob("*/plugin.toml"):
    with path.open("rb") as handle:
        data = tomllib.load(handle)
    manifest = _parse_manifest(data)
    if self._versions.is_compatible(manifest.required_application_version):
        manifests.append(manifest)
```
[SOURCE: plugins/loader.py:50-61]

**Stärken:** kein Code-Import (ADR-001 belegt eingehalten); v1/v2-Manifeste
werden beide unterstützt; unbekannte Felder werden bewusst ignoriert
(Vorwärtskompatibilität) [SOURCE: plugins/loader.py:64-80].

### 9.2 Nichtdeterministische Discovery-Reihenfolge

> **PS-01 (ENGINEERING INFERENCE):** `Path.glob()` gibt keine sortierte
> Reihenfolge zu; die Reihenfolge von `context.manifests` ist damit
> dateisystemabhängig. Für die **Aktivierungsreihenfolge** ist das folgenlos
> (topologische Sortierung mit lexikografischem Tie-Break, Kap. 9.6), für
> **Diagnose, Logs, Metriken und die Reihenfolge der Ablehnungsereignisse** ist
> es eine unnötige Nichtdeterminismusquelle. → **TD-13** (LOW).

### 9.3 Discovery ist nicht fehlerisoliert — **wichtigster Zuverlässigkeitsbefund**

`PluginLoader.discover()` besitzt **keine** Fehlerbehandlung pro Manifest. Ein
`tomllib.TOMLDecodeError`, ein `KeyError` (fehlendes `id`/`version`/
`requires_application`) oder ein `ValueError` (unparsbare Version) beendet die
gesamte Schleife [SOURCE: plugins/loader.py:50-61, :72-75 Docstring nennt genau
diese Ausnahmen].

Der Aufrufer fängt die Ausnahme und fährt **ohne jedes Plugin** fort:

```python
except Exception as error:  # discovery failure is recoverable; run with no plugins
    logger.error("plugins.discovery_failed", exc_info=error)
    PluginFailed("", str(error)).publish(events)
    context.manifests = ()
    registry.register(PluginCatalog, PluginCatalog(()))
    return
```
[SOURCE: app/bootstrap/stages_plugin.py:54-59]

> **PS-02 (SOURCE FACT + ENGINEERING INFERENCE):** **Ein einziges fehlerhaftes
> `plugin.toml` deaktiviert sämtliche Plugins.** Die Anwendung startet
> weiterhin (das ist gewollt und korrekt), aber die Ausfallwirkung eines
> Plugins ist **global statt lokal**.
>
> Bewertung gegen FR-010 („Der Ausfall eines einzelnen Plugins beeinträchtigt
> weder die Plattform noch andere Plugins")
> [SOURCE: docs/milestone-1.0-engineering-spec.md §7.2 FR-010]:
> **DEVIATION im Discovery-Abschnitt**. Die Aktivierungsphase erfüllt FR-010
> dagegen (Kap. 9.4).
>
> Zusatzbefund: `PluginFailed("", …)` publiziert einen **leeren Identifier** —
> ein Abonnent kann das Ereignis keinem Plugin zuordnen. Relevant für FR-006
> (Rejection Feedback). → **TD-14 (HIGH).**

### 9.4 Aktivierung ist fehlerisoliert

Jedes Plugin wird in einem eigenen `try/except Exception` aktiviert; ein Fehler
erzeugt einen `ActivationFailure`-Datensatz, publiziert `PluginFailed` und
setzt die Schleife fort [SOURCE: app/bootstrap/stages_plugin.py:479-566].

> **PS-03:** FR-010 ist **für die Aktivierungsphase erfüllt**. **MATCH.**

### 9.5 Plugin-Klassenauswahl

```python
for attr_name in dir(module):
    attr = getattr(module, attr_name)
    if (isinstance(attr, type) and issubclass(attr, Plugin)
            and attr is not Plugin
            and not getattr(attr, "__abstractmethods__", None)):
        plugin_class = attr
        break
```
[SOURCE: app/bootstrap/stages_plugin.py:504-513]

> **PS-04 (ENGINEERING INFERENCE):** `dir()` liefert alphabetisch sortiert;
> die Auswahl ist damit **deterministisch, aber willkürlich**. Enthält ein
> Plugin-Modul mehrere konkrete `Plugin`-Subklassen — auch **importierte**
> aus anderen Plugins oder aus dem SDK — gewinnt die alphabetisch erste.
> Das Manifest-Feld `entry_point` existiert
> [SOURCE: plugins/loader.py:26 `entry_point: str = ""`] und wird
> **an dieser Stelle nicht ausgewertet**.
>
> Bewertung: **PARTIAL MATCH / Designlücke.** Ein deklarierter, im Manifest
> benannter Einstiegspunkt wäre eindeutig und würde zugleich das Risiko
> unbeabsichtigter Klassenauswahl beseitigen. → **TD-15 (MEDIUM)**,
> Empfehlung PC-03. **Achtung:** Eine Auswertung von `entry_point` wäre eine
> Verhaltensänderung an der Aktivierung → ADR-011-/Baseline-Berührung möglich →
> **nicht** eigenmächtig; **OPEN DECISION.**

### 9.6 Dependency Resolution (ADR-007)

Implementiert in `_resolve_dependencies()`
[SOURCE: app/bootstrap/stages_plugin.py:71-230]:

| Fähigkeit | Ist |
|---|---|
| Selbstabhängigkeit | erkannt und abgelehnt (:102-107) |
| Doppelte Deklaration | erkannt und abgelehnt (:109-116) |
| Versionsbedingung `>=x.y.z` | geparst und geprüft (:118-126, :150-155) |
| Fehlende Abhängigkeit | abgelehnt (:145-149) |
| Kaskadenablehnung | Fixpunkt-Schleife bis stabil (:132-159) |
| Zyklenerkennung | über Rest der topologischen Sortierung (:192-195) |
| Zyklen-Kaskade | zweite Fixpunkt-Schleife (:196-212) |
| Deterministische Ordnung | `sorted()` an drei Stellen (:180, :186, :190) |
| Ablehnungsereignisse | `PluginRejected` + Warn-Log je Plugin (:214-219) |

> **PS-05:** Vollständige, deterministische und kaskadensichere Umsetzung.
> **MATCH gegen die im Architecture Book beschriebene ADR-007-Lösung**
> [SOURCE: docs/architecture-book-v2.md §20, ADR-007-Eintrag — **Welt B**;
> in Welt A steht dort „Status: Open" (Kap. 4.2)]. **Klare Stärke des Codes.**
>
> **PS-06 (Detail):** Eine nicht parsbare Versionsangabe wird still verworfen
> (`except ValueError: pass`, :124-125) und die Bedingung damit **ignoriert**
> statt abgelehnt. **ENGINEERING INFERENCE:** fail-open in einem sonst
> fail-fast gehaltenen Resolver. Inkonsistent. → **TD-16 (MEDIUM).**

### 9.7 SDK-Oberfläche

| Baustein | Ort | Bemerkung |
|---|---|---|
| `Plugin` (ABC) + Lifecycle-Hooks | `sdk/plugin.py:53-147` | `on_initialize/start/stop/shutdown` |
| Spezialisierungen | `sdk/plugin.py:149-275` | `BackgroundPlugin`, `UIPlugin`, `ToolPlugin`, `WorkflowPlugin` |
| `PluginRuntime` | `sdk/plugin.py:277-393` | Zustandsübergänge `initialize/start/stop/shutdown` |
| `PluginContextBuilder` | `sdk/context.py:65-...` | 10 `with_*`-Methoden, Fluent Builder |
| Manifest-Modell | `sdk/manifest.py` | `PluginMetadata`, `PluginPermission`, `Capability`, `SignatureStatus`, Validierung in `__post_init__` |
| Konfiguration | `sdk/config.py` | `FilePluginConfigStorage`, Defaults, Validatoren |
| Events | `sdk/events.py` | Permission-gegatete Publish/Subscribe |
| Fehler | `sdk/errors.py` | u. a. `PluginPermissionError` |
| Version | `sdk/version.py` | eigenständiges `ApiVersion` |

> **PS-07:** Das SDK ist die reifste Schicht (2.551 Zeilen, 51 dedizierte
> Tests in `tests/test_sdk.py`). ADR-010 (SDK als einzige öffentliche API) ist
> im Code eingehalten.

### 9.8 Zwei Permissions-Vokabulare

| Vokabular | Typ | Quelle | Auswertung |
|---|---|---|---|
| Host-seitig | `tuple[str, ...]` | `plugin.toml` → `PluginManifest.permissions` [SOURCE: plugins/loader.py:28] | `PermissionPolicy.granted_for()` bei Admission |
| SDK-seitig | `frozenset[PluginPermission]` | `PluginMetadata.permissions` (Python-Code des Plugins) [SOURCE: sdk/manifest.py:225] | Laufzeit-Checks in `sdk/events.py` |

Eine Brücke existiert konzeptionell (`Capability`-Enum mit Zuordnungshinweis),
ist aber ausdrücklich unvollständig: „Capabilities without a mapping (e.g.
CLIPBOARD, CAMERA) represent contract vocabulary that does not yet have a
host-side permission equivalent" [SOURCE: sdk/manifest.py:96-100].

> **PS-08 (SOURCE FACT):** Die beiden Vokabulare sind im Code **nicht
> verbunden**. Konsequenz siehe Kap. 10.5 (TD-04). Dies berührt zugleich den
> bereits offenen Governance Conflict **GC-03** (PluginTrustLevel-/
> Terminologiefragen) [SOURCE: docs/governance/jochen-x-next-authorized-work-assessment.md
> §2, Zeile GC-03–GC-07]. Es wird hier **nichts entschieden**.

### 9.9 Referenz-Plugin

`plugins/reference/` deklariert `capabilities = ["events.publish",
"events.subscribe"]` [SOURCE: plugins/reference/plugin.toml].

> **PS-09 (ENGINEERING INFERENCE):** Mit der produktiven Default-Policy
> (`PermissionPolicy()` = leer, Kap. 10.6) ergibt
> `granted_for("reference") = ∅` ⇒ `denied = {events.publish,
> events.subscribe}` ⇒ **Ablehnung an der Admission-Grenze**. Der
> Golden-Reference-Test bestätigt diese Mechanik indirekt: er injiziert eigens
> eine permissive Policy und ruft `security.approve("reference")`
> [SOURCE: tests/test_golden_reference.py:90-98].
>
> **Folgerung:** Das mitgelieferte Referenz-Plugin würde beim regulären Start
> über `main.py` mit der ausgelieferten `config/default.toml` **nicht
> aktiviert**. Das ist **fail-secure** und damit sicherheitsseitig korrekt —
> es ist aber ein **Funktions-/Konfigurationsdefizit**, weil kein
> Konfigurationsweg existiert, dies zu ändern (TD-05). → Kap. 10.6.

---

## 10. Security Analysis

> **Vorbemerkung.** Dieses Kapitel schafft **keine** neuen Sicherheitsprinzipien,
> **keine** neue Trust-Taxonomie und **keine** neue Risikoskala. Es bewertet
> ausschließlich den Ist-Code gegen bereits genehmigte Vorgaben und weist
> Lücken aus. Keine Security-Design-ODD wird geschlossen; keine
> Security-Entscheidung wird getroffen.

### 10.1 Bezugsrahmen

| Vorgabe | Quelle |
|---|---|
| Zero Trust für Plugins | [SOURCE: docs/architecture-book-v2.md §11; docs/security.md „Plugin Security"] |
| Trust Boundaries, Identity, Human Authority, Critical Actions | [SOURCE: docs/security-architecture-1.0.md §3, §4, §5, §6] |
| Fail-Secure, Security State Model, Auditability | [SOURCE: docs/security-design-1.0.md §15, §16, §17] |
| Plugin-/Agent-Sicherheit, offene Designentscheidungen ODD-01–ODD-20 | [SOURCE: docs/security-design-1.0.md §12, §19] |
| Sicherheitskritische Pipeline-Reihenfolge | [SOURCE: docs/baselines/bootstrap-baseline-1.0.md §4 Inv. 6] |
| Plugin-Code niemals vor bestandener Prüfung ausführen | [SOURCE: CLAUDE.md „Sicherheitsregeln"] |

### 10.2 Was nachweislich funktioniert

1. **Kein Plugin-Code vor der Sicherheitsprüfung.** Discovery ist manifest-only;
   der erste `importlib.import_module` steht in FINALIZE, also nach allen vier
   LOAD_PLUGINS-Prüfschritten [SOURCE: stages_plugin.py:501 vs. :253-343].
   **Kernanforderung erfüllt.**
2. **Pipeline-Reihenfolge unverletzt** (Kap. 8.5, Invariante 6). **PASS.**
3. **Default-Deny an der Permission-Grenze.** Leere Policy ⇒ jede deklarierte
   Capability wird verweigert ⇒ Plugin abgelehnt
   [SOURCE: app/security/plugin_security.py:426-453].
4. **Ablehnung ist irreversibel innerhalb eines Laufs.** `REJECTED` wird zuerst
   geprüft und kurzschließt jede erneute Integritätsprüfung
   [SOURCE: app/security/plugin_security.py:280-299].
5. **Sicherheitsereignisse existieren und werden publiziert:**
   `PluginVerified`, `PluginRejected` mit stabilen Bus-Namen
   [SOURCE: app/security/events.py; docs/security.md „Security Events"].
6. **Trust Ledger ist thread-safe** (`RLock` um alle Zustandszugriffe)
   [SOURCE: app/security/plugin_security.py:213, :250-251, :522-534].

### 10.3 Integrity Validation — Substanz

`IntegrityEvidenceLevel` kennt `STRUCTURAL`, `CONTENT`, `SIGNATURE`
[SOURCE: app/security/plugin_security.py:38-43]. Implementiert ist **nur**
`STRUCTURAL`, und der Code sagt das offen:

> „Stronger evidence levels (content, signature) are deferred — the
> architecture supports them but the current implementation evaluates
> structural evidence only."
> [SOURCE: app/security/plugin_security.py:265-268]

`_evaluate_structural_evidence()` prüft drei Bedingungen: nichtleerer
Identifier, nichtleere Version, vorhandene
`required_application_version`
[SOURCE: app/security/plugin_security.py:512-518].

> **SEC-01 (SOURCE FACT):** „Integrity Validation" prüft am Baseline
> **ausschließlich die Wohlgeformtheit des Manifests**. Der **Code** des
> Plugins wird zu keinem Zeitpunkt gehasht, signaturgeprüft oder auf
> Unverändertheit geprüft. Jedes Plugin mit drei belegten Manifestfeldern
> erreicht `VERIFIED` und ist damit `admitted`.
>
> **SEC-02 (Einordnung, keine Entscheidung):** Dies ist **konsistent mit der
> genehmigten Vorgabe**: Die Engineering Specification stellt kryptografisches
> Enforcement ausdrücklich zurück; das Integritätsmodell muss ohne
> kryptografische Implementierung definierbar sein
> [SOURCE: docs/adr/005-plugin-integrity-validation.md (Welt B), Abschnitt
> „Existing Architectural Capabilities", Verweis auf Spec §5.9 Explicit
> Deferral]. Kryptografie ist zudem als **ODD-19** offen
> [SOURCE: docs/governance/jochen-x-next-authorized-work-assessment.md §5 D].
>
> **Bewertung: kein Verstoß, aber eine Wirkungsgrenze, die dokumentiert
> gehört.** Die Bezeichnung „Integrity Validation" ist gegenüber der
> tatsächlichen Wirkung (Schema-Validierung) **überzeichnet**. → **TD-17**,
> Klassifikation **OBSERVATION**, Empfehlung PC-06 (Dokumentation, nicht Code).

**Nicht validierter Identifier.** `manifest.identifier` wird ungeprüft als
Modulname (`importlib.import_module(identifier)`) und als Pfadsegment
(`plugin_dir / identifier`) verwendet
[SOURCE: app/bootstrap/stages_plugin.py:497-501, :528-530]. Eine
Zeichensatz-/Formatvalidierung findet weder im Loader
[SOURCE: plugins/loader.py:82] noch in der Integritätsprüfung statt. Das SDK
besitzt eine solche Prüfung (`validate_identifier`
[SOURCE: sdk/manifest.py:233]), sie greift jedoch erst **nach** dem Import auf
`PluginMetadata`.

> **SEC-03 (ENGINEERING INFERENCE / OBSERVATION):** Ein manipulierter
> Identifier (z. B. mit `..`-Anteilen) trifft zuerst auf
> `module_path.is_dir()` und danach auf `import_module`, was in der Praxis
> scheitert; ein **belastbarer** Schutz ist das jedoch nicht, weil er
> Nebeneffekt und nicht Absicht ist. Eine explizite Identifier-Validierung
> **vor** der Verwendung als Pfad- und Modulname wäre die naheliegende
> Härtung. → **TD-18 (MEDIUM).** Keine Entscheidung; Vorschlag PC-04.

### 10.4 Keine Isolation

Siehe RT-01. Plugins laufen mit vollen Interpreter-Rechten.

> **SEC-04 (ENGINEERING INFERENCE):** Solange keine Isolation existiert, ist
> **jedes** Permission-Modell — Host- wie SDK-seitig — **beratend, nicht
> erzwingend**: ein Plugin kann jede SDK-Prüfung umgehen, indem es Python-APIs
> direkt verwendet (`open`, `socket`, `subprocess`, `importlib`).
>
> Dies ist eine **Systemeigenschaft, kein Implementierungsfehler**, und es ist
> in den Quellen als offener Bereich geführt (ADR-009, Security Design §12,
> ODD-Register). Diese Analyse trifft **keine** Isolationsentscheidung und
> schlägt **keine** konkrete Isolationstechnik vor — das wäre eine
> Security-Architekturentscheidung außerhalb der Autorisierungsgrenze.
> → **OD-04 (BLOCKED DECISION-nah, siehe Kap. 33).**
>
> **Wichtig für die Roadmap:** Jede spätere Fähigkeit, die Fremdcode oder
> KI-erzeugten Code ausführt (Agents, Tools, Automation, Trading-Strategien),
> **erbt** diese Eigenschaft. Sie sollte vor solchen Fähigkeiten disponiert
> werden — als Feststellung, nicht als Forderung.

### 10.5 Runtime-Permission-Enforcement stützt sich auf Selbstdeklaration — **TD-04**

Die Beweiskette:

1. Host ermittelt das Grant-Set:
   `PermissionResult(identifier, granted, denied, admitted, reason)`
   [SOURCE: app/security/plugin_security.py:464-472].
2. Der Aufrufer in der Security-Stage wertet **nur `admitted`** aus; `granted`
   wird verworfen [SOURCE: app/bootstrap/stages_plugin.py:306-318].
3. Die Aktivierung baut den `PluginContext` **ohne** jede
   Permission-Übergabe — die Builder-Kette umfasst `with_event_bus`,
   `with_service`, `with_config_storage`, `with_resources_root`,
   `with_logger`, `with_application_version`
   [SOURCE: app/bootstrap/stages_plugin.py:532-541]. Eine
   `with_permissions(...)`-Methode existiert im Builder **nicht**
   [SOURCE: sdk/context.py:95-153, vollständige `with_*`-Liste].
4. Der Builder leitet die Laufzeitprüfung stattdessen aus den **Metadaten des
   Plugins selbst** ab:
   ```python
   permitted = self._metadata.permissions
   def permission_check(permission: PluginPermission) -> None:
       if permission in permitted: return
       raise PluginPermissionError(...)
   ```
   [SOURCE: sdk/context.py:175-182]
5. `self._metadata` stammt aus `plugin.metadata()`, also aus **Plugin-Code**
   [SOURCE: app/bootstrap/stages_plugin.py:519 `metadata = plugin.metadata()`].

> **SEC-05 (SOURCE FACT):** Das Laufzeit-Permission-Gate des SDK prüft die
> vom **Plugin selbst deklarierten** Permissions gegen sich selbst. Das vom
> Host ermittelte Grant-Set wird **nicht** übertragen. Ein Plugin, das in
> `plugin.toml` **keine** Capability deklariert (⇒ Admission ohne
> Policy-Prüfung, [SOURCE: app/security/plugin_security.py:415-424]) und in
> seinem Python-`metadata()` **alle** `PluginPermission`-Werte angibt, besteht
> jede SDK-Prüfung.
>
> **Bewertung gegen die genehmigte Vorgabe:** ADR-006 D4 lautet „Runtime
> Enforcement über bestehenden SDK-Injection-Point"
> [SOURCE: docs/architecture-book-v2.md §20, ADR-006-Eintrag — **Welt B**];
> das Architecture Book **in Welt A** hält an derselben Stelle fest: „Das SDK
> implementiert bereits 10 Permissions und Enforcement im `PluginContext`.
> **Die Integration mit dem Host steht aus.**"
> [SOURCE: docs/architecture-book-v2.md §20 — **Welt A**].
>
> **Damit ist der Befund in beiden Welten quellengedeckt:** Welt A benennt die
> ausstehende Integration ausdrücklich; Welt B fordert sie als D4. Der
> Ist-Zustand ist eine **MISSING**-Position, keine Regression.
>
> **Klassifikation: TD-04, Priorität HIGH (technisch).** Ausdrücklich **keine**
> Wirkungsstufe im Sinne der JOCHEN-X-Governance — diese Analyse vergibt keine
> Governance-Schweregrade (Auftrag Kap. 23).
>
> **Wirkungsdämpfer, der zur Ehrlichkeit gehört:** Wegen SEC-04 (keine
> Isolation) ist der praktische Sicherheitsgewinn einer Korrektur begrenzt —
> sie stellt die *Kontraktkonformität* her, nicht die *Erzwingbarkeit*.

### 10.6 Sicherheitsrichtlinien sind nicht konfigurierbar — **TD-05**

| Prüfung | Befund |
|---|---|
| `IntegrityPolicy.from_config()` — produktive Aufrufstelle | **keine** (nur `tests/test_activation_validation.py:170, :182`) |
| `PermissionPolicy.from_config()` — produktive Aufrufstelle | **keine** (nur Tests) |
| `[security]`-Abschnitt in `config/default.toml` | **nicht vorhanden** [SOURCE: config/default.toml, vollständig: `[application]`, `[database]`, `[plugins]`] |
| Policy-Übergabe in `SecurityManager.create()` | **keine** — `PluginSecurity(events, logger=resolved_logger)` ohne Policy-Argumente [SOURCE: app/security/security_manager.py:118] |
| Policy-Übergabe in `PluginSecurityStage` | **keine** — `PluginSecurity(events, logger=logger)` [SOURCE: app/bootstrap/stages_plugin.py:265] |

> **SEC-06 (SOURCE FACT):** Beide `from_config`-Fabriken sind im Produktionspfad
> **toter Code**. Die effektive Laufzeitrichtlinie ist fest verdrahtet:
> `IntegrityPolicy(STRUCTURAL, "manifest", VERIFIED)` und
> `PermissionPolicy()` (leer ⇒ deny-all-declared).

**Reihenfolgebefund.** `PluginSecurityStage` (LOAD_PLUGINS) versucht zuerst
`registry.get(PluginSecurity)` und legt bei `LookupError` eine
Default-Instanz an [SOURCE: app/bootstrap/stages_plugin.py:262-266].
`SecurityBootstrapStage` läuft jedoch in **FINALIZE**
[SOURCE: app/security/security_manager.py:236] und entfernt dort die bereits
registrierte Instanz, um die eigene zu setzen
[SOURCE: app/security/security_manager.py:202-204].

> **SEC-07 (ENGINEERING INFERENCE):** Die vom `SecurityManager` komponierte
> `PluginSecurity`-Instanz kann die **Plugin-Admission nie beeinflussen** — sie
> ersetzt die Instanz erst, nachdem die Admission (LOAD_PLUGINS) und die
> Aktivierung (FINALIZE, vor `SecurityBootstrapStage`, siehe CS-02) bereits
> stattgefunden haben. Der Trust Ledger, den nachgelagerte Konsumenten aus der
> Registry beziehen, ist damit **ein anderer** als der, gegen den die Plugins
> geprüft wurden — inklusive der aufgezeichneten `IntegrityResult`- und
> `PermissionResult`-Einträge, die in der neuen Instanz fehlen.
>
> **Klassifikation: TD-19, Priorität HIGH (technisch).** Dies erklärt zugleich
> die Kapselungsbrüche aus AM-04: die `pop()`-Hacks sind Symptome dieser
> Reihenfolgeproblematik, nicht deren Ursache.
>
> **Wichtig:** Eine Korrektur berührt die Stage-Reihenfolge bzw. die
> Stage-Zusammensetzung und damit Bootstrap Baseline §8 (Change Control).
> Sie ist **nicht** eigenmächtig zulässig. → **OD-05.**

### 10.7 Kryptografie ist ein Platzhalter

```python
class ReversibleEncryptionService(EncryptionService):
    """This implementation base64-encodes payloads so the storage layer works
    end to end..."""
    def encrypt(self, plaintext: bytes) -> bytes:
        return base64.b64encode(plaintext)
    def decrypt(self, ciphertext: bytes) -> bytes:
        return base64.b64decode(ciphertext, validate=True)
```
[SOURCE: app/security/encryption_service.py:68-91]

Dieser Dienst ist der **Default** für `SecretVault` **und** `BackupManager`
[SOURCE: app/security/security_manager.py:109-111, :119].

> **SEC-08 (SOURCE FACT):** Der als „Encryption" bezeichnete Dienst leistet
> **Kodierung, keine Verschlüsselung**. Secrets im Vault und Backups sind
> gegenüber jedem, der die Daten lesen kann, **effektiv im Klartext**.
>
> **SEC-09 (Einordnung):** Der Docstring ist ehrlich, und Kryptografie ist als
> **ODD-19 offen**
> [SOURCE: docs/governance/jochen-x-next-authorized-work-assessment.md §5 D].
> Es liegt also **kein Verstoß gegen eine getroffene Entscheidung** vor.
> Kritikwürdig ist allein die **Benennung**: `EncryptionService` /
> `ReversibleEncryptionService` suggerieren Schutz, den die Implementierung
> nicht bietet, und `SecurityManager.create()` wählt diesen Platzhalter
> **stillschweigend als Default** (`encryption or ReversibleEncryptionService()`).
>
> **Klassifikation: TD-20, Priorität HIGH (technisch).** Empfehlung PC-07
> beschränkt sich auf **Sichtbarmachung** (Startup-Warnung / Namensklarheit) —
> **keine** Kryptografieauswahl, da ODD-19 offen und nicht vom Verfasser
> entscheidbar ist. → **BLOCKED DECISION BD-02.**
>
> **Nicht geloggt werden Secrets** — die Vault-Operationen protokollieren Namen
> und Metadaten, keine Werte [SOURCE: app/security/secret_vault.py:62-128].
> CLAUDE.md „Secrets niemals loggen" ist eingehalten. **PASS.**

### 10.8 Auditierbarkeit

`AuditLogger` existiert [SOURCE: app/security/audit_logger.py] und wird vom
`SecurityManager` komponiert und registriert
[SOURCE: app/security/security_manager.py:114, :199].

> **SEC-10 (ENGINEERING INFERENCE):** Die Plugin-Pipeline schreibt ihre
> Entscheidungen über `logger` und `EventBus`, **nicht** über den
> `AuditLogger` — dieser existiert zum Zeitpunkt der Pipeline noch nicht
> (SEC-07). Ein durchgängiger, manipulationsresistenter Audit-Trail für
> Admission-Entscheidungen ist damit am Baseline **nicht** gegeben.
> Der Audit-Ereigniskatalog ist als **ODD-17** offen
> [SOURCE: docs/governance/jochen-x-next-authorized-work-assessment.md §5 D].
> **Feststellung, keine Forderung.** → **TD-21 (MEDIUM).**

### 10.9 Zusammenfassung Security-Analyse

| Bereich | Bewertung |
|---|---|
| Pipeline-Reihenfolge / kein Code vor Prüfung | **MATCH** |
| Default-Deny an der Admission-Grenze | **MATCH** |
| Trust Ledger, Ereignisse, Thread-Sicherheit | **MATCH** |
| Integrity = Schema-Prüfung | **PARTIAL MATCH** (quellengedeckt zurückgestellt) — TD-17 |
| Identifier-Validierung vor Pfad-/Modulnutzung | **MISSING** — TD-18 |
| Runtime-Enforcement gegen Host-Grants | **MISSING** — TD-04 (in Welt A ausdrücklich als „steht aus" benannt) |
| Policy-Konfigurierbarkeit | **MISSING** — TD-05 |
| Trust-Ledger-Identität über die Phasen | **DEVIATION** — TD-19 |
| Kryptografie | **PARTIAL MATCH** (ODD-19 offen) — TD-20 |
| Audit-Trail der Admission | **MISSING** — TD-21 |
| Plugin-Isolation | **OPEN / NOT AUTHORIZED** — OD-04 |

> **Keine ODD wurde geschlossen. Kein Security-ADR wurde erstellt. Keine
> Security-Entscheidung wurde getroffen.**

---

## 11. AI Analysis

> **Vorbemerkung.** KI wird hier strikt als **Fähigkeits-/Werkzeugschicht**
> behandelt. Die Trennung Modell / Provider / Capability / Tool / Agent /
> Autorität wird durchgehalten. Kein KI-Modell erhält Autorität, nur weil die
> Technik es zuließe [SOURCE: docs/core-principles-1.0.md §8;
> docs/security-architecture-1.0.md §9].

### 11.1 Was am Baseline existiert

| Artefakt | Inhalt | Bewertung |
|---|---|---|
| `ai/gateway.py` (47 Zeilen) | `Capability` (TEXT/VISION/EMBEDDING), `ModelDescriptor`, `ProviderDescriptor`, `ProviderRegistry`, `RoutingEngine.candidates(capability)` | **Reine Metadaten.** Docstring: „credentials and execution are intentionally absent" [SOURCE: ai/gateway.py:24]. `RoutingEngine` filtert Deskriptoren, ruft nichts auf [SOURCE: ai/gateway.py:42-47] |
| `core/ai_contracts.py` (53 Zeilen) | `AICapability` (7 Werte), `Model`, `Provider`, 7 Provider-`Protocol`s, `ProviderRouter` | **Reine Kontrakte.** Docstring: „no provider implementation or model loading" [SOURCE: core/ai_contracts.py:1]. Fünf der sieben Protocols sind leer (`pass`) |
| `core/ai_manager.py` (19 Zeilen) | `AIManager.ask(prompt)` → `ollama.chat(model="qwen3", …)` | **Tatsächliche Modellausführung** [SOURCE: core/ai_manager.py:1-19] |
| `core/worker.py` (53 Zeilen) | `AIWorker`/`WorkerThread` (Qt) um `AIManager` | Altbestand [SOURCE: core/worker.py:1-53] |
| `ui/chat_page.py`, `ui/chat_bubble.py`, `ui/input_bar.py`, `ui/message_widget.py` | Chat-Oberfläche | Altbestand, nicht in `ui/navigation/` |

### 11.2 Wiring-Status

| Prüfung | Ergebnis |
|---|---|
| `ai.gateway` in der produktiven Bootstrap-Sequenz registriert? | **Nein.** Einzige Registrierung in `app/host.py:58-59` — dem toten zweiten Composition Root (AM-02) |
| `core.ai_manager` von der produktiven Sequenz erreichbar? | **Nein.** Einziger Importeur ist `core/worker.py:3`; dieser wird von keinem produktiven Modul importiert |
| `core.ai_contracts` genutzt? | Nur in `tests/test_core.py:4` |

> **AI-01 (SOURCE FACT):** Der KI-Bestand ist **vollständig von der produktiven
> Laufzeit entkoppelt**. Über `main.py` wird weder ein Modell geladen noch ein
> Provider aufgerufen. JOCHEN X führt am Baseline **keine** KI-Inferenz aus.

### 11.3 Die `ollama`-Abhängigkeit — **TD-03**

```python
import ollama
class AIManager:
    def __init__(self, model="qwen3"): ...
    def ask(self, prompt: str) -> str:
        response = ollama.chat(model=self.model, messages=[...])
        return response["message"]["content"]
```
[SOURCE: core/ai_manager.py:1-19]

| Prüfung | Befund |
|---|---|
| In `pyproject.toml` deklariert? | **Nein** — `dependencies = ["PySide6>=6.8"]` [SOURCE: pyproject.toml:10-12] |
| In CLAUDE.md als Abhängigkeit geführt? | **Nein** — „einzige externe Abhängigkeit: PySide6 ≥ 6.8" |
| Lokal installiert? | **Ja** (verifiziert per `importlib.util.find_spec`) — die Lücke ist in dieser Arbeitsumgebung **maskiert** |
| Bricht RB-1.0? | **Nein** — keine der 14 RB-1.0-Dateien importiert `core.worker` oder `core.ai_manager` |

> **AI-02 (SOURCE FACT + ENGINEERING INFERENCE):** `ollama` ist eine
> **undeklarierte externe Laufzeitabhängigkeit im innersten Architekturring**.
> Sie widerspricht NFR-007 („No External Dependencies")
> [SOURCE: docs/milestone-1.0-engineering-spec.md §8.2 NFR-007], der
> Charter-Out-of-Scope-Position „Externe Abhängigkeiten (ohne explizite
> Governance-Entscheidung)"
> [SOURCE: docs/milestone-1.0-engineering-spec.md §5.2] und der
> Projektdokumentation.
>
> Auf einer sauberen Installation gemäß `pyproject.toml` ist `core/worker.py`
> **nicht importierbar**. Dass dies heute nicht auffällt, liegt an der lokal
> vorhandenen Installation — ein klassischer maskierter Defekt.
>
> **Wichtige Abgrenzung:** NFR-007 bindet den **Milestone** („keine *neuen*
> externen Abhängigkeiten"). Ob eine *vorbestehende* undeklarierte Abhängigkeit
> als NFR-007-Verstoß oder als Altbestand zu werten ist, ist eine
> **Auslegungsfrage**, die diese Analyse **nicht entscheidet**. → **OD-06.**

### 11.4 Konzeptionelle Inkonsistenz

Drei Artefakte beschreiben dieselbe Domäne mit **drei** unterschiedlichen
Modellen:

| | `ai/gateway.py` | `core/ai_contracts.py` | `core/ai_manager.py` |
|---|---|---|---|
| Capability-Enum | `Capability` (3 Werte) | `AICapability` (7 Werte) | — |
| Abstraktion | konkrete Dataclasses | Protocols | konkrete Klasse |
| Ausführung | ausdrücklich keine | ausdrücklich keine | **ja** |
| Provider | Deskriptor-Registry | Protocol | fest `ollama` |

> **AI-03 (ENGINEERING INFERENCE):** Es existieren zwei konkurrierende
> Capability-Vokabulare und drei Abstraktionsebenen ohne verbindende Schicht.
> Für einen späteren, autorisierten KI-Aufbau ist das eine
> **Konsolidierungsschuld**, kein Defekt der heutigen Laufzeit (die diesen Code
> nicht ausführt). → **TD-22 (MEDIUM).**

### 11.5 Was aus den Quellen für die Zukunft gilt (ohne Erfindung)

Die genehmigten Quellen behandeln KI-Trust, Prompt-/Instruction-Security und
KI-Klassen [SOURCE: docs/security-architecture-1.0.md §9, §10;
docs/security-design-1.0.md §11; docs/core-principles-1.0.md §8]. Diese
Analyse leitet daraus **keine** Implementierungsdetails ab, weil keine Quelle
eine konkrete KI-Implementierungsrichtung für Milestone 1.0 autorisiert:

- Der Charter-Scope umfasst Plattform-Härtung, Host-Services, Plugin-Ökosystem,
  Observability, Testabdeckung, Dokumentation — **keine KI-Fähigkeit**
  [SOURCE: docs/milestone-1.0-engineering-spec.md §5.1].
- Keiner der 14 Functional Requirements betrifft KI
  [SOURCE: docs/milestone-1.0-engineering-spec.md §7.2].

> **AI-04:** KI-Fähigkeit für Milestone 1.0: **NOT AUTHORIZED / OUT OF SCOPE.**
> KI-Fähigkeit darüber hinaus: **FUTURE / OPEN.**

### 11.6 Engineering-Anforderungen, die bei späterer Autorisierung entstehen

**RECOMMENDATION — ausdrücklich nicht REQUIRED, keine Sprint-Zuordnung, keine
Autorisierung.** Aufgeführt, weil der Auftrag (Kap. 15) danach fragt; jede
Position ist als offen markiert:

| Thema | Status |
|---|---|
| Provider-Abstraktion (Vereinheitlichung der drei Modelle aus 11.4) | OPEN |
| Lokale vs. externe Modelle, Trust-Domänen-Zuordnung | OPEN — stützt sich auf SA §7/§8, keine Entscheidung |
| Inferenz-Lebenszyklus, Asynchronität, Timeouts, Abbruch | OPEN |
| Fehlerbehandlung bei Provider-Ausfall, Degradation | OPEN |
| Prompt-Handling, Injection-Resistenz | OPEN — SA §10 vorhanden, ODDs offen |
| Tool-Calls und deren Autorisierung | OPEN — berührt Human Authority (SA §5) |
| Auditierbarkeit von Modellaufrufen | OPEN — ODD-17 |
| Menschliche Aufsicht bei kritischen Aktionen | OPEN — SA §6 |
| Kostenkontrolle / Token-Budget | OPEN — keine Quelle |

---

## 12. Memory Analysis

### 12.1 Ist-Zustand

> **MEM-01 (SOURCE FACT):** Es existiert **kein** Memory-Subsystem. Weder ein
> Paket, noch ein Modul, noch ein Kontrakt, noch ein Datenmodell. Die einzige
> Persistenz ist ein SQLite-`SettingsRepository` (Schlüssel/Wert für
> Anwendungseinstellungen) [SOURCE: database/sqlite.py:52-70] sowie
> plugin-lokale Konfigurationsdateien über `FilePluginConfigStorage`
> [SOURCE: sdk/config.py]. Beides ist **kein** Memory im Produktsinne.

### 12.2 Genehmigte Vorgaben

Memory Security ist in beiden Security-Dokumenten adressiert
[SOURCE: docs/security-architecture-1.0.md §12; docs/security-design-1.0.md §13].
Sie beschreiben Sicherheitsanforderungen an ein Memory-System, **nicht** dessen
Architektur.

### 12.3 Bewertung

| Frage | Antwort |
|---|---|
| Speichergrenzen, Segmentierung, Retrieval, Lebenszyklus, Löschung, Auditierbarkeit, Trust-Grenzen | **Sämtlich OPEN.** Keine Quelle legt eine finale Memory-Architektur fest |
| Ist Memory Teil von Milestone 1.0? | **Nein** [SOURCE: docs/milestone-1.0-engineering-spec.md §5.1, §7.2] |
| Wird hier eine Memory-Architektur vorgeschlagen? | **Nein** — ausdrücklich nicht (Auftrag Kap. 16) |

> **MEM-02:** Memory: **FUTURE / OPEN / NOT AUTHORIZED.** Es wird keine
> Memory-Architektur erfunden.

---

## 13. Agent / Automation Analysis

### 13.1 Ist-Zustand

| Bereich | Befund |
|---|---|
| Agenten | **Nicht vorhanden.** Kein Agent-Modul, kein Agent-Kontrakt, keine Agent-Laufzeit |
| Automation | **Nicht vorhanden** im Sinne autonomer Handlungsketten. Vorhanden ist `core/scheduler.py` (`TaskScheduler`) und `app/concurrency.py` (`WorkerPool`) — **Infrastruktur**, keine Automatisierungsfähigkeit |
| Multimodal | **Nicht vorhanden.** Existieren tut ausschließlich Enum-Vokabular: `Capability.VISION` [SOURCE: ai/gateway.py:11] und `AICapability.{VISION, SPEECH, TRANSCRIPTION}` [SOURCE: core/ai_contracts.py:13-15]; die zugehörigen Protocols `VisionProvider`, `SpeechProvider`, `TranscriptionProvider` sind leer (`pass`) [SOURCE: core/ai_contracts.py:32-49] |
| Werkzeugaufruf (Tool Invocation) | **Nicht vorhanden** auf Hostebene. `ToolPlugin.execute(request) -> Mapping` existiert im SDK als Plugin-Kategorie [SOURCE: sdk/plugin.py:230-247] — das ist ein **Plugin-Typ**, keine Agenten-Werkzeugschicht |

### 13.2 Vorhandene Infrastruktur, die eine spätere Fähigkeit tragen könnte

**ENGINEERING INFERENCE, ohne Implementierungsvorschlag:** `EventBus`,
`TaskScheduler`, `WorkerPool`, `ServiceRegistry`, das Plugin-Lifecycle-Modell
und `ToolPlugin` bilden zusammen eine Basis, auf der Agenten- oder
Automationsfähigkeiten **technisch** aufsetzen könnten. Ob das getan wird und
wie, ist **nicht entschieden**.

### 13.3 Sicherheitsimplikation

> **AG-01 (ENGINEERING INFERENCE):** Jede Agenten- oder Automationsfähigkeit
> würde die Eigenschaften aus SEC-04 (keine Isolation) und SEC-05
> (Selbstdeklaration) **erben** und zusätzlich die Frage der **Human
> Authority** aufwerfen [SOURCE: docs/security-architecture-1.0.md §5, §6;
> docs/security-design-1.0.md §7, §9]. Diese Feststellung ist **keine
> Forderung** und **keine Vorbedingung**, die diese Analyse setzen dürfte —
> sie ist die sachliche Konsequenzbeschreibung.

### 13.4 Klassifikation

| Bereich | Zweck (Quelle) | Ist | Genehmigte Richtung | Fehlende Infrastruktur | Offene Entscheidungen |
|---|---|---|---|---|---|
| Agents | SA §11 (Plugin & Agent Trust), SD §12 | nicht vorhanden | **keine** für M1.0 | Autorisierungsmodell, Isolation, Audit | ODD-Register, OD-04 |
| Automation | keine Milestone-Quelle | nicht vorhanden | **keine** | — | — |
| Multimodal | SA §13, SD (Identitätsverfahren ODD-03) | nur Vokabular | **keine** für M1.0 | alles | ODD-03 |

> **AG-02:** Agents / Automation / Multimodal: **FUTURE / NOT AUTHORIZED.**
> Es werden keine technischen Implementierungsdetails erfunden.

---

## 14. Trading Analysis

### 14.1 Ist-Zustand — vollständige Suche

| Gesuchtes Artefakt | Befund |
|---|---|
| Trading-UI | **nicht vorhanden** — `ui/navigation/` enthält Dashboard, Chat, Developer Center; keine Trading-Ansicht |
| Trading-Scaffolding / Domänenmodell | **nicht vorhanden** |
| Broker-Integration / Konnektor | **nicht vorhanden** |
| Wallet / Zahlungsverkehr | **nicht vorhanden** |
| Order-Ausführung | **nicht vorhanden** |
| Backtesting / Simulation / Paper Trading | **nicht vorhanden** |
| Marktdaten | **nicht vorhanden** |
| Einziger trading-benachbarter Code | `app/security/broker_security.py` — ein **Security-Baustein**, komponiert aus `PermissionManager` und `EventBus` [SOURCE: app/security/security_manager.py:117 `broker = BrokerSecurity(permissions, events, …)`] |

> **TR-01 (SOURCE FACT):** JOCHEN X besitzt am Baseline **kein Trading-System
> und kein Trading-Scaffolding**. Der Auftragshinweis, die Existenz einer
> Trading-UI nicht als Beleg für ein Trading-System zu werten, greift hier
> nicht einmal — es existiert nicht einmal eine Trading-UI.
>
> `BrokerSecurity` ist ein **Sicherheitsdienst ohne Broker**: ein
> Autorisierungspunkt, der auf eine später vorhandene Trading-Fähigkeit
> vorbereitet, aber selbst nichts handelt. Er als Beleg für Trading-Fähigkeit
> zu werten, wäre ein Fehlschluss und wird hier ausdrücklich vermieden.

### 14.2 Reifegradstufen — getrennte Betrachtung

| Stufe | Ist | Genehmigte Richtung |
|---|---|---|
| RESEARCH | nicht vorhanden | keine für M1.0 |
| SIMULATION | nicht vorhanden | keine für M1.0 |
| BACKTESTING | nicht vorhanden | keine für M1.0 |
| PAPER | nicht vorhanden | keine für M1.0 |
| CONTROLLED LIVE | nicht vorhanden | **ausdrücklich NICHT AUTORISIERT** |

Belege für die Nicht-Autorisierung:
- „Live-Trading · Echtgeld-/Wallet-Transfers · autonome kritische Aktionen"
  stehen in der Kategorie **E — AUSDRÜCKLICH NICHT AUTORISIERT**
  [SOURCE: docs/governance/jochen-x-next-authorized-work-assessment.md §5 E].
- GDR-002 §12: die Entscheidung bedeutet nicht „Trading-Live-Gang,
  Wallet-Transfers, Echtgeldzugriff"
  [SOURCE: docs/governance/gr-001-governance-decision.md §12].
- Baseline Commit Record §12: „Trading-/KI-Freigabe" ausdrücklich
  ausgeschlossen [SOURCE: docs/governance/milestone-1.0-baseline-commit-record.md §12].
- Sprint Plan §9: „keine Trading-Funktionalität"
  [SOURCE: docs/milestone-1.0-sprint-plan.md §9].
- Ein feineres Trading-Stufenmodell ist als **ODD-14 / AO-19 zurückgestellt**
  [SOURCE: docs/governance/jochen-x-next-authorized-work-assessment.md §3 E].

### 14.3 Ausdrückliche Nicht-Handlungen dieser Phase

> Es wurden **keine** Broker-Integrationen, **keine** Wallets, **keine**
> Order-Ausführung, **kein** Kapitaltransfer, **kein** autonomes Trading und
> **keine** Live-Autorisierung erstellt, entworfen oder vorbereitet.
>
> **TR-02:** Profitabilität ist ein Produktziel
> [SOURCE: docs/core-principles-1.0.md §9]. Sie ist **keine** Erlaubnis, Security,
> Governance, Tests, Simulation, Human Authority oder Kapitalschutz zu
> schwächen. Diese Analyse leitet aus dem Produktziel **keine** technische
> Freiheit ab.

### 14.4 Bewertung

**CONTROLLED LIVE TRADING wird in diesem Dokument nicht als automatisch
autorisierter Meilenstein dargestellt** (Auftrag Kap. 27). Es erscheint in
Kap. 31 ausschließlich mit dem Status **NOT AUTHORIZED**.

---

## 15. Test Architecture

### 15.1 Bestandsaufnahme

| Menge | Dateien | Tests | Status |
|---|---|---|---|
| **RB-1.0** (verbindliche Regressionsbasis) | **14** | **258** | reproduziert (Kap. 3.4) |
| Stillgelegter Bestand (`jochen_x`-Importe) | 22 | 761 | **nicht** Teil von RB-1.0 |
| Repository-Gesamtkennzahl | 36 (+4 `__init__.py`) | 1.019 | Kennzahl, **nicht** Bezugsgröße |
[SOURCE: docs/governance/milestone-1.0-sprint-01-baseline-confirmation.md §7-§9]

### 15.2 RB-1.0 nach Abdeckungsbereich

| Datei | Tests | Prüfgegenstand |
|---|---|---|
| `test_application_foundation.py` | 62 | `app/` — Host, Startup, Shutdown, Errors, DI, State Machine |
| `test_sdk.py` | 51 | `sdk/` — vollständige öffentliche API |
| `test_activation_validation.py` | 42 | Plugin-Pipeline, Integrity-/Permission-Policies |
| `test_security_foundation.py` | 33 | `app/security/` |
| `test_navigation.py` | 22 | `ui/navigation/` |
| `test_dependency_resolution.py` | 12 | ADR-007-Logik |
| `test_manifest_v2.py` | 8 | Manifest-Parsing v1/v2 |
| `test_foundation.py` | 7 | `app/host.py` (Altbestand!), `ai/gateway.py` |
| `test_core.py` | 6 | `core/` |
| `test_plugin_observability.py` | 4 | `PluginHealthCheck`, Metriken |
| `test_developer.py` | 3 | `developer/` |
| `test_golden_reference.py` | 3 | End-to-End-Plugin-Pipeline |
| `integration/test_plugin_integration.py` | 3 | Stage-Zusammenspiel, Degradation |
| `test_capability_matrix.py` | 2 | Capability-Zuordnung |
[SOURCE: docs/governance/milestone-1.0-sprint-01-baseline-confirmation.md §7]

### 15.3 Teststufen

| Stufe | Vorhanden | Bemerkung |
|---|---|---|
| Unit | ja | Großteil der 258 |
| Integration | ja | `test_golden_reference.py`, `integration/test_plugin_integration.py` |
| System / End-to-End über `main.py` | **nein** | Kein Test startet die Anwendung über den produktiven Einstiegspunkt |
| Security | teilweise | `test_security_foundation.py`, Policy-Tests in `test_activation_validation.py` |
| Failure / Negativpfade | teilweise | `TestGracefulDegradation` vorhanden; siehe Lücken 15.4 |
| Performance | **nein** | Keine Messreihe im Repository — für SPR-08/EV-I01 vorausgesetzt (OP-8) |
| Regression | ja | RB-1.0 als Bezugsgröße definiert |

### 15.4 Belegte Abdeckungslücken

Jede Lücke korrespondiert mit einem Befund dieses Dokuments:

| # | Lücke | Bezug |
|---|---|---|
| TG-1 | Kein Test für fehlerhaftes `plugin.toml` in Anwesenheit gültiger Plugins (Global-Ausfall-Szenario) | PS-02 / TD-14 |
| TG-2 | Kein Test, der die **produktive** Default-Policy prüft (alle Policy-Tests injizieren eigene Policies) | SEC-06 / TD-05, PS-09 |
| TG-3 | Kein Test für die Trust-Ledger-Identität über LOAD_PLUGINS→FINALIZE | SEC-07 / TD-19 |
| TG-4 | Kein Test, der belegt, dass Host-Grants im `PluginContext` ankommen | SEC-05 / TD-04 |
| TG-5 | Kein Test für `restart()`/`recover()` mit bereits importierten Plugin-Modulen | RT-04 / TD-11 |
| TG-6 | Kein Test für Handler-Ausnahmen in `EventBus.publish` (Abbruch der Zustellkette) | Kap. 16.3 / TD-23 |
| TG-7 | Kein Test für nebenläufige `ServiceRegistry`-Auflösung | Kap. 21.4 / TD-07 |
| TG-8 | Keine Performance-Baseline-Messreihe | OP-8 [SOURCE: docs/milestone-1.0-sprint-plan.md §8] |
| TG-9 | Kein Test für Plugin-Module mit mehreren `Plugin`-Subklassen | PS-04 / TD-15 |

### 15.5 Testarchitektur — Bewertung

**Stärken:** Stage-Isolation macht die Pipeline gut testbar; `test_golden_reference.py`
räumt `sys.modules` sauber auf [SOURCE: tests/test_golden_reference.py:35-41,
:73-77]; temporäre Verzeichnisse statt Repository-Mutation.

**Schwächen (ENGINEERING INFERENCE):**
1. `tests/test_foundation.py` hält den toten Composition Root `app/host.py`
   in der Regressionsbasis. Jede Disposition von TD-01 berührt damit RB-1.0.
   Das ist bei OD-02 mitzudenken.
2. Die Policy-Tests testen die Policy-**Mechanik**, nicht die **ausgelieferte
   Konfiguration** — deshalb fällt SEC-06 durch den Testbestand nicht auf.
3. `testpaths = ["tests"]` sammelt ohne Pfadargument alle 1.019 Tests
   [SOURCE: pyproject.toml:18]. Wer „einfach `pytest` laufen lässt", misst
   **nicht** RB-1.0. → operatives Risiko für Gate-Nachweise (RK-05).

### 15.6 Regelkonformität dieser Analyse

> Die Regressionsbezugsgröße wurde **nicht verändert** (Auftrag Kap. 22).
> Es wurden **keine** Testzahlen aufgebläht. **Kein** Test wurde als bestanden
> klassifiziert; der Pass-Zustand 258/258 wird als **übernommene Evidenz** aus
> dem Baseline Commit Record §9 geführt, nicht als eigene Messung.

---

## 16. Reliability

### 16.1 Startversagen

Determiniert: Stage-Fehler → `BootstrapError` mit Stage-Namen → `FATAL` →
Re-Raise (BS-07). Fehlende Kontextfelder → `BootstrapError` in
`build_context()` (BS-06). **Bewertung: gut.**

### 16.2 Degradation

| Szenario | Verhalten | Bewertung |
|---|---|---|
| Discovery scheitert | Start ohne Plugins, `PluginFailed("")` | **funktional korrekt, Isolation zu grob** (PS-02) |
| Einzelnes Plugin scheitert bei Aktivierung | `ActivationFailure` + `PluginFailed(id)`, Schleife läuft weiter | **gut** (PS-03) |
| Plugin von abgelehntem Plugin abhängig | Kaskadenablehnung, deterministisch | **gut** (PS-05) |
| Developer Platform nicht verfügbar | `LookupError` gefangen | **gut** [SOURCE: app/host.py:96-97] |
| Disposable wirft beim Shutdown | gefangen und geloggt | **gut** [SOURCE: app/di.py:104-108] |
| Plugin wirft beim Shutdown | gefangen und geloggt | **gut** [SOURCE: app/application_host.py:145-152] |

### 16.3 Ausnahmegrenzen — die zwei Lücken

**(a) `EventBus.publish` bricht die Zustellkette ab.**

```python
for subscription in handlers:
    result = subscription.handler(event)
    ...
except Exception as exception:
    error = type(exception).__name__
    raise
```
[SOURCE: core/events.py:82-89]

> **REL-01 (SOURCE FACT + ENGINEERING INFERENCE):** Wirft ein Handler, so
> werden **die verbleibenden Handler nicht mehr benachrichtigt**, und die
> Ausnahme propagiert **zum Publisher**. Da Plugins über
> `sdk/events.py` abonnieren können, kann ein fehlerhaftes Plugin damit
> (i) andere Abonnenten um ihr Ereignis bringen und (ii) den publizierenden
> Host-Code zum Absturz bringen.
>
> Bewertung gegen FR-010 („Der Ausfall eines einzelnen Plugins beeinträchtigt
> weder die Plattform noch andere Plugins")
> [SOURCE: docs/milestone-1.0-engineering-spec.md §7.2 FR-010]:
> **DEVIATION.** → **TD-23 (HIGH).**
>
> **Fairnesshalber:** Das Verhalten ist bewusst gewählt — `EventDelivery`
> zeichnet den Fehlertyp auf, und ADR-002 („Event Delivery") behandelt die
> Zustellsemantik [SOURCE: docs/adr/002-event-delivery.md]. Eine Änderung
> berührt damit eine genehmigte Entscheidung und ist **nicht** eigenmächtig
> zulässig. → **OD-07.**

**(b) Zustandsübergangs-Listener laufen ungeschützt.**

```python
for listener in listeners:
    listener(previous, target)
```
[SOURCE: app/state_machine.py:145-146]

> **REL-02 (ENGINEERING INFERENCE):** Ein werfender Listener unterbricht die
> Benachrichtigung der übrigen Listener und propagiert in den Aufrufer —
> **nachdem** der Zustand bereits gewechselt wurde. Ergebnis: inkonsistente
> Beobachtersicht bei gültigem Maschinenzustand. → **TD-24 (MEDIUM).**

### 16.4 Wiederherstellung

`restart()` und `recover()` bauen Zustandsmaschine, Worker-Pool und
Startup-Sequenz neu auf [SOURCE: app/application_host.py:154-201].

> **REL-03 (ENGINEERING INFERENCE):** Zwei Lücken im Reset:
> (a) `sys.modules` wird nicht bereinigt (RT-04 / TD-11);
> (b) `self._events` (`EventBus`) wird **nicht** zurückgesetzt
> [SOURCE: app/application_host.py:195-201 — `_events` fehlt in `_reset()`].
> Abonnements aus dem vorherigen Lebenszyklus, insbesondere von Plugins,
> bleiben registriert; History und Sticky Events überdauern. Bei wiederholtem
> `restart()` wachsen die Abonnentenlisten monoton. → **TD-25 (MEDIUM).**
>
> Ob `_events` bewusst lebenszyklusübergreifend ist (es ist der Publisher für
> `ApplicationStateChanged` und würde beim Reset Beobachter verlieren), ist aus
> dem Code nicht eindeutig. Der Docstring schweigt. **Beides ist vertretbar —
> die fehlende Aussage ist der Mangel.**

### 16.5 Persistenz- und Konfigurationsfehler

`ConfigurationError` und `DatabaseError` sind als **fatal** eingestuft
[SOURCE: app/errors.py:64-69]. **Bewertung: fail-secure, angemessen.**

### 16.6 Zusammenfassung

| Bereich | Bewertung |
|---|---|
| Startversagen | **stark** |
| Aktivierungsisolation | **stark** |
| Shutdown-Robustheit | **stark** |
| Discovery-Isolation | **schwach** (TD-14) |
| Event-Zustellisolation | **schwach** (TD-23) |
| Listener-Isolation | **schwach** (TD-24) |
| Restart-/Recover-Hygiene | **schwach** (TD-11, TD-25) |

---

## 17. Performance

> **Methodische Vorgabe:** Es werden **keine Benchmarks erfunden**. Jede
> Aussage trägt eine der vier Kennzeichnungen MEASURED / OBSERVED / INFERRED /
> UNKNOWN. Diese Analyse hat **keine** Messungen durchgeführt (Read-Only,
> keine Testausführung).

### 17.1 Vorhandene Instrumentierung

| Messpunkt | Ort | Art |
|---|---|---|
| `plugin.security.validation_ms.{id}` | [SOURCE: stages_plugin.py:320-324] | Dauer je Plugin |
| `plugin.dependency.resolution_ms` | [SOURCE: stages_plugin.py:329-333] | Dauer gesamt |
| `plugin.activation.duration_ms.{id}` | [SOURCE: stages_plugin.py:568-572] | Dauer je Plugin |
| `startup_ms` in `ApplicationReady` | [SOURCE: app/startup.py:79-81] | Gesamtstartzeit |
| `EventDelivery.duration_ms` | [SOURCE: core/events.py:121-122] | Zustelldauer je Ereignis |

> **PERF-01 (OBSERVED):** Die Instrumentierung für den performancekritischen
> Pfad (Start, Plugin-Pipeline, Eventzustellung) ist **vorhanden**. Das ist die
> notwendige Voraussetzung für die in Anhang B des Implementation Plans
> vorgesehene Messreihe.

### 17.2 Fehlende Grundlage

> **PERF-02 (UNKNOWN):** Es existiert **keine** Baseline-Messreihe im
> Repository. OP-8 führt sie als offenen Punkt und als Voraussetzung für SPR-08
> [SOURCE: docs/milestone-1.0-sprint-plan.md §8, OP-8]. NFR-004
> (Performance-Non-Degradation) ist ohne diese Messreihe **nicht
> nachweisbar** [SOURCE: docs/milestone-1.0-engineering-spec.md §8.2 NFR-004].
> Konkrete CPU-, RAM-, Start-, I/O- und Latenzwerte: **UNKNOWN.**

### 17.3 Strukturelle Beobachtungen (INFERRED, nicht gemessen)

| # | Beobachtung | Einordnung |
|---|---|---|
| P-1 | `_resolve_dependencies` nutzt eine Fixpunkt-Schleife über alle Plugins (`while changed`) mit innerer Iteration — bei *n* Plugins und *d* Abhängigkeiten grob O(n²·d) [SOURCE: stages_plugin.py:132-159] | **Irrelevant** bei realistischen Plugin-Zahlen (< 100). **Keine Optimierung empfohlen** — vorzeitige Optimierung |
| P-2 | `EventBus._record_and_select` führt bei **jedem** Publish `fnmatch.fnmatchcase` über **alle** Abonnements aus [SOURCE: core/events.py:129-130] | Linear in der Abonnentenzahl je Ereignis. **Bei hoher Ereignisrate der wahrscheinlichste Hotspot.** INFERRED, nicht gemessen |
| P-3 | `ServiceRegistry.descriptors()` ruft `inspect.signature()` für jede Registrierung auf [SOURCE: core/registry.py:100-122] | Wird beim Start einmal für `ApplicationStarted(service_count)` genutzt [SOURCE: app/startup.py:66]. Vernachlässigbar |
| P-4 | `Metrics._values` wächst mit **einem Eintrag je Plugin und Messpunkt**, Schlüssel enthalten den Plugin-Identifier [SOURCE: core/observability.py:22-28] | Unbegrenzte Kardinalität, an einen manifestgesteuerten Wert gebunden. Bei stabiler Plugin-Menge folgenlos; bei dynamischem Nachladen Speicherwachstum. → TD-10 |
| P-5 | `EventBus` hält `history` und `deliveries` als `deque(maxlen=256)` [SOURCE: core/events.py:50-52] | **Begrenzt — gut gelöst.** Kein unbegrenztes Wachstum |
| P-6 | `_sticky` ist ein **unbegrenztes** `dict[str, Event]` [SOURCE: core/events.py:51] | Wächst mit der Zahl **verschiedener** Sticky-Ereignisnamen. INFERRED: in der Praxis klein; strukturell unbegrenzt |
| P-7 | Startzeit wird von Plugin-Import und -Initialisierung dominiert (In-Process-Import je Plugin) | INFERRED |
| P-8 | UI-Reaktionsfähigkeit: `ApplicationHost` ist Qt-frei; Hintergrundarbeit über `WorkerPool`; `publish_async` „never executes work on a UI caller" [SOURCE: core/events.py:45] | **Strukturell günstig.** Nicht gemessen |

### 17.4 Empfehlung

> **RECOMMENDATION (nicht REQUIRED):** Die Baseline-Messreihe gemäß Anhang B
> sollte **vor** dem Beginn von Phase B erhoben werden, nicht erst zu SPR-08.
> Begründung: NFR-004 verlangt einen **Vergleich**; ein Vergleichspunkt, der
> erst nach den Änderungen entsteht, kann keine Regression nachweisen.
> Der Sprint Plan sieht die Erhebung „zu Beginn der Umsetzung" vor
> [SOURCE: docs/milestone-1.0-sprint-plan.md §8, OP-8] — diese Empfehlung
> **bestätigt** die Planvorgabe und ändert sie nicht. → PC-02.

---

## 18. Maintainability

### 18.1 Positive Merkmale

| Merkmal | Beleg |
|---|---|
| Type Hints auf öffentlichen APIs | durchgängig in `core/`, `app/`, `sdk/` |
| `__all__` in den Kernmodulen | `app/bootstrap/*`, `core/observability.py`, `plugins/loader.py`, `sdk/*`, `app/application_host.py` |
| Frozen Dataclasses für Value Types | durchgängig |
| Protocols statt ABCs zwischen Schichten | `BootstrapStage`, `HealthCheck`, `ErrorHandler`, `Disposable`, AI-Kontrakte |
| Kein globaler Zustand / keine Singletons | eingehalten — Ausnahme: `sys.path`/`sys.modules` während der Aktivierung (RT-02/RT-04) |
| Docstrings mit Args/Returns/Raises | in `app/` und `sdk/` sehr konsistent |
| Kommentardichte | niedrig, erklärt „warum" — entspricht der Stilregel |

> **MT-01:** Die Stilregeln aus CLAUDE.md sind im überwiegenden Teil des
> produktiven Codes **eingehalten**. Der Code ist überdurchschnittlich lesbar.

### 18.2 Ausreißer

| Modul | Abweichung |
|---|---|
| `core/ai_manager.py` | keine Type Hints am Konstruktor, kein `__all__`, kein Docstring, harte externe Abhängigkeit |
| `core/worker.py` | keine Rückgabetypen, ungewöhnliche Leerzeilenstruktur, deutschsprachiger Docstring (sonst englisch), `except Exception` ohne Kategorisierung |
| `app/host.py` | 28 aufeinanderfolgende `register`-Aufrufe in einer Methode; irreführender Docstring („the sole composition root") |
| `core/registry.py` | einziges Kernmodul **ohne** `__all__`; `_construct` mit `get_type_hints`-Reflexion ist die komplexeste Einzelstelle des Codes |
| `core/events.py` | kein `__all__`; sehr lange Zeilen in `_record_delivery`/`_record_and_select` |

### 18.3 Dokumentation ↔ Code

| Aussage | Zustand |
|---|---|
| CLAUDE.md-Projektstruktur listet `ai/`, `styles/` **nicht** | **Lücke** — beide existieren am Baseline |
| CLAUDE.md: „einzige externe Abhängigkeit: PySide6" | **falsch** wegen `ollama` (AI-02) |
| Bootstrap Baseline §3.1 „20 Symbole" vs. 22 | **redaktionell falsch** (BS-02 / TD-08) |
| Baseline §5.2 Pipeline (5 Schritte) vs. Code (6 Schritte) | **unvollständig** (BS-05 / TD-12) |
| `_validate_for_activation` Docstring nennt „3. Permission verification" | **Der Code prüft keine Permissions**; das Feld `permissions_valid` bleibt stets auf dem Default `True` [SOURCE: app/bootstrap/stages_plugin.py:351-357 vs. :361-409]. → **TD-26 (MEDIUM)** |
| `docs/security.md` beschreibt `SecurityContext`/`CapabilityModel` | Diese Namen existieren im produktiven Code **nicht**; die Datei ist zudem governance-seitig ungeklärt (**GF-03/GC-02**, offen) [SOURCE: docs/security.md; docs/governance/jochen-x-next-authorized-work-assessment.md §2] |

> **MT-02:** Die Dokumentationsabweichungen sind einzeln klein, in Summe aber
> relevant für **QG-005 (Traceability Completeness)** und **FR-011/FR-012**
> (SPR-07). Sie sind genau der Arbeitsgegenstand von WP-007 — insofern
> **planmäßig**, nicht überraschend.

### 18.4 Technische Schulden-Konzentration

**ENGINEERING INFERENCE:** Die Schulden verteilen sich nicht gleichmäßig. Drei
Cluster:

1. **Altbestand-Cluster** (`app/host.py`, `ui/*.py`, `core/worker.py`,
   `core/ai_manager.py`) — TD-01, TD-03, TD-22. Gemeinsame Ursache: nicht
   disponierter Vorgängerstand. **Eine** Entscheidung (OD-02) räumt mehrere
   Schulden.
2. **Security-Verdrahtungs-Cluster** (TD-04, TD-05, TD-19, TD-21, TD-06) —
   gemeinsame Ursache: Der `SecurityManager` wurde als *additive* FINALIZE-Stage
   nachgerüstet, während die Plugin-Pipeline in LOAD_PLUGINS bereits eigene
   Defaults erzeugt. **Eine** Entscheidung (OD-05) räumt mehrere Schulden.
3. **Isolations-Cluster** (TD-14, TD-23, TD-24, TD-11, TD-25) — gemeinsame
   Ursache: Fehlerisolation ist an drei Stellen implementiert (Aktivierung,
   Disposables, Plugin-Shutdown) und an vier Stellen nicht (Discovery,
   Event-Zustellung, Listener, Reset).

---

## 19. Technical Debt Register

> **Ausdrückliche Abgrenzung (Auftrag Kap. 23):** Die Prioritäten CRITICAL /
> HIGH / MEDIUM / LOW / OBSERVATION sind ein **rein technisches
> Priorisierungsmittel dieses Dokuments**. Sie ersetzen und redefinieren
> **nicht** die JOCHEN-X-Governance-Wirkungsstufen und sind **keine**
> Findings im Governance-Sinn. Status ist durchgängig **OPEN** — dieses
> Dokument schließt nichts.

**Verteilung:** CRITICAL 0 · HIGH 7 · MEDIUM 12 · LOW 3 · OBSERVATION 4
(insgesamt 26).

### 19.1 HIGH

| ID | Beschreibung | Evidenz | Auswirkung | Empfehlung | Abhängigkeiten | Prio | Status |
|---|---|---|---|---|---|---|---|
| **TD-01** | Zweiter, gleichnamiger Composition Root `app/host.py::ApplicationHost` neben `app/application_host.py::ApplicationHost`; ohne State Machine und ohne Plugin-Security-Pipeline | app/host.py:27-38, :40-77; app/application_host.py:35-72 | Verwechslungsgefahr; latenter Sicherheitspfad ohne Pipeline; Architekturaussage „sole composition root" ist falsch | Governance-Disposition analog GR-001; **nicht** eigenmächtig entfernen (RB-1.0-Bindung über `tests/test_foundation.py`) | OD-02; RB-1.0 | HIGH | OPEN |
| **TD-02** | Packaging/Tooling zeigt auf den stillgelegten Baum (`where=["src"]`, `mypy_path`, `ruff src`) | pyproject.toml:14-29 | `pip install .` liefert die produktive Anwendung nicht aus; Typ-/Lint-Prüfung adressiert den falschen Baum | Konfiguration an GDR-002 D-1 angleichen — **erfordert Freigabe**, da Folge einer Governance-Entscheidung | OD-03; GDR-002 D-2 | HIGH | OPEN |
| **TD-03** | Undeklarierte externe Abhängigkeit `ollama` in `core/ai_manager.py` | core/ai_manager.py:1; pyproject.toml:10-12 | `core/worker.py` auf sauberer Installation nicht importierbar; NFR-007/Charter-Konflikt | Deklarieren **oder** mit dem Altbestand-Cluster disponieren | OD-06; OD-02 | HIGH | OPEN |
| **TD-04** | Runtime-Permission-Enforcement nutzt Plugin-Selbstdeklaration statt Host-Grants | sdk/context.py:175-182; stages_plugin.py:306-318, :532-541 | Kontraktbruch gegen ADR-006 D4; in Welt A ausdrücklich als „Integration steht aus" benannt | Host-Grants in den `PluginContext` übertragen — **SDK-additive Änderung**, ADR-/Freigabe-relevant | OD-05; ADR-006-Disposition (OD-01) | HIGH | OPEN |
| **TD-05** | `IntegrityPolicy.from_config` / `PermissionPolicy.from_config` haben keine produktive Aufrufstelle; kein `[security]` in `config/default.toml` | app/security/plugin_security.py:61, :139; config/default.toml | Sicherheitsrichtlinie ist fest verdrahtet; Referenz-Plugin wird mit Default-Konfiguration abgelehnt | Konfigurationspfad herstellen | OD-05 | HIGH | OPEN |
| **TD-14** | `PluginLoader.discover()` ohne Fehlerisolation je Manifest → ein defektes `plugin.toml` deaktiviert alle Plugins; `PluginFailed("")` ohne Identifier | plugins/loader.py:50-61; stages_plugin.py:54-59 | DEVIATION gegen FR-010 im Discovery-Abschnitt; Diagnose ohne Zuordnung | Isolation je Manifest; Identifier im Ereignis führen | FR-010/WP-005 (SPR-06) | HIGH | OPEN |
| **TD-19** | `SecurityBootstrapStage` (FINALIZE) ersetzt die `PluginSecurity`-Instanz **nach** Admission und Aktivierung | security_manager.py:202-204, :236; stages_plugin.py:262-266 | Der aus der Registry bezogene Trust Ledger ist nicht derjenige, gegen den geprüft wurde; `IntegrityResult`/`PermissionResult` fehlen dort | Reihenfolge/Komposition klären — **Bootstrap-Baseline-Change-Control** | OD-05; Baseline §8 | HIGH | OPEN |
| **TD-23** | `EventBus.publish` bricht die Zustellkette bei Handler-Ausnahme ab und propagiert zum Publisher | core/events.py:82-89 | DEVIATION gegen FR-010: ein Plugin-Handler kann andere Abonnenten und den Host beeinträchtigen | Zustellsemantik klären — berührt **ADR-002** | OD-07; ADR-002 | HIGH | OPEN |

### 19.2 MEDIUM

| ID | Beschreibung | Evidenz | Auswirkung | Empfehlung | Prio | Status |
|---|---|---|---|---|---|---|
| **TD-06** | Kapselungsbruch: `registry._lock` / `registry._registrations.pop()` an zwei Stellen | stages_plugin.py:337-338; security_manager.py:202-203 | Umgeht die öffentliche API; bricht bei Registry-Änderungen | Öffentliche `replace()`/`override()`-Fähigkeit erwägen (additiv) | MEDIUM | OPEN |
| **TD-07** | `ServiceRegistry._resolve`/Instanz-Caching ohne Lock | core/registry.py:131-150 | Doppelkonstruktion eines „Singleton" bei Nebenläufigkeit möglich | Auflösung unter Lock; Tests ergänzen (TG-7) | MEDIUM | OPEN |
| **TD-11** | `sys.modules` wird bei `restart()`/`recover()` nicht bereinigt | app/application_host.py:195-201 | Neu deployter Plugin-Code wird nicht wirksam; entferntes Plugin bleibt importierbar | Bereinigung analog `tests/test_golden_reference.py:38-41` | MEDIUM | OPEN |
| **TD-12** | Baseline §5.2 nennt 5 Pipeline-Schritte, der Code führt 6 aus (API-Version-Gate) | baselines/bootstrap-baseline-1.0.md §5.2; stages_plugin.py:287-303 | Dokumentationslücke; SPR-09-Nachweis zählt gegen den Text | Im Rahmen WP-007 nachführen (kein Codeeingriff) | MEDIUM | OPEN |
| **TD-15** | Plugin-Klassenauswahl über `dir(module)`; `entry_point` unausgewertet | stages_plugin.py:504-513; plugins/loader.py:26 | Willkürliche Auswahl bei mehreren `Plugin`-Subklassen; importierte Fremdklassen wählbar | `entry_point` auswerten — **Verhaltensänderung, ADR-011-Berührung möglich** | MEDIUM | OPEN |
| **TD-16** | Unparsbare Versionsangabe in Abhängigkeiten wird still ignoriert (`except ValueError: pass`) | stages_plugin.py:122-126 | Fail-open in einem sonst fail-fast Resolver | Ablehnen statt ignorieren — berührt ADR-007-Semantik | MEDIUM | OPEN |
| **TD-18** | Keine Validierung von `manifest.identifier` vor Nutzung als Modulname und Pfadsegment | plugins/loader.py:82; stages_plugin.py:497-501, :528-530 | Schutz entsteht nur als Nebeneffekt; SDK-Validierung greift erst nach dem Import | Explizite Identifier-Validierung in der Pipeline | MEDIUM | OPEN |
| **TD-21** | Admission-Entscheidungen laufen nicht über den `AuditLogger` (existiert zu diesem Zeitpunkt nicht) | security_manager.py:114, :199 vs. stages_plugin.py:277-318 | Kein durchgängiger Audit-Trail der Pipeline | Mit TD-19 gemeinsam; Katalog ist **ODD-17** (offen) | MEDIUM | OPEN |
| **TD-22** | Drei konkurrierende KI-Abstraktionen, zwei Capability-Vokabulare | ai/gateway.py:7-19; core/ai_contracts.py:8-25; core/ai_manager.py | Konsolidierungsschuld für spätere, autorisierte KI-Arbeit | Mit dem Altbestand-Cluster disponieren | MEDIUM | OPEN |
| **TD-24** | Zustandsübergangs-Listener laufen ungeschützt nach dem Zustandswechsel | app/state_machine.py:145-146 | Inkonsistente Beobachtersicht bei werfendem Listener | Isolation je Listener | MEDIUM | OPEN |
| **TD-25** | `EventBus` wird in `_reset()` nicht erneuert; Abonnements/Sticky/History überdauern Restarts | app/application_host.py:195-201 | Monoton wachsende Abonnentenliste bei wiederholtem `restart()` | Verhalten festlegen und dokumentieren | MEDIUM | OPEN |
| **TD-26** | `_validate_for_activation`-Docstring nennt eine Permission-Prüfung, die nicht stattfindet; `permissions_valid` stets Default | stages_plugin.py:351-357 vs. :361-409 | Irreführende Diagnose; `ValidationDiagnostic` suggeriert eine Prüfung | Docstring korrigieren **oder** Prüfung ergänzen | MEDIUM | OPEN |

### 19.3 LOW

| ID | Beschreibung | Evidenz | Prio | Status |
|---|---|---|---|---|
| **TD-10** | `Metrics` unsynchronisiert, unbegrenzte Schlüsselkardinalität mit manifestgesteuerten Namensanteilen | core/observability.py:20-31; stages_plugin.py:322, :570 | LOW | OPEN |
| **TD-13** | `Path.glob()` liefert unsortierte Discovery-Reihenfolge | plugins/loader.py:55 | LOW | OPEN |
| **TD-27** | `core/registry.py` und `core/events.py` ohne `__all__` (Stilregel CLAUDE.md) | core/registry.py; core/events.py | LOW | OPEN |

### 19.4 OBSERVATION

| ID | Beschreibung | Evidenz | Status |
|---|---|---|---|
| **TD-08** | Bootstrap Baseline §3.1 überschreibt 22 aufgezählte Symbole mit „20 Symbole"; Code und Aufzählung stimmen überein | baselines/bootstrap-baseline-1.0.md §3.1; app/bootstrap/__init__.py:45-68 | OPEN |
| **TD-09** | Keine CI-Konfiguration im Repository; alle Gate-Nachweise manuell | Baseline-Dateiinventar | OPEN |
| **TD-17** | Bezeichnung „Integrity Validation" für eine reine Schema-Prüfung (quellengedeckt zurückgestellt, ODD-19) | app/security/plugin_security.py:265-268, :512-518 | OPEN |
| **TD-20** | `ReversibleEncryptionService` = Base64; stillschweigender Default für Vault und Backups | app/security/encryption_service.py:68-91; security_manager.py:109-111 | OPEN |

### 19.5 Abhängigkeitsgraph der Schulden

```
OD-01 (ADR-Disposition) ──► TD-04 (Vertragsgrundlage ADR-006 D4)
OD-02 (Altbestand)      ──► TD-01, TD-03, TD-22, (ui/*.py), RB-1.0-Berührung
OD-03 (Packaging)       ──► TD-02, TD-09 (CI setzt korrektes Packaging voraus)
OD-05 (Security-Wiring) ──► TD-04, TD-05, TD-19, TD-21, TD-06
OD-07 (Event-Semantik)  ──► TD-23, TD-24
(ohne Gate)             ──► TD-07, TD-10, TD-11, TD-12, TD-13, TD-16,
                            TD-18, TD-25, TD-26, TD-27, TD-08
```

---

## 20. Open Decision Register

> **Der Verfasser trifft keine dieser Entscheidungen.** Jede Position benennt
> ausdrücklich die erforderliche Autorität.

### OD-01 — Disposition der sechs uncommitteten Dokumentänderungen

| Feld | Inhalt |
|---|---|
| **Problem** | ADR-005/006/007 und Architecture Book v2.0 tragen am Baseline den Status „Open"; die APPROVED-Fassungen liegen uncommittet vor (Kap. 4.2). CLAUDE.md und ROADMAP.md sind ebenfalls modifiziert |
| **Evidenz** | `git diff 8fcf42f… --stat` (6 Dateien, +1.415/−119); docs/governance/milestone-1.0-baseline-commit-record.md §10, §15 Nr. 4 |
| **Warum offen** | GDR-003 hat `docs/**` bewusst vom Baseline-Commit ausgeschlossen; die Disposition ist ausdrücklich als „nächster Entscheidungspunkt des Projekteigners" vorgemerkt |
| **Optionen** | (a) Committen mit Governance-Vermerk; (b) belassen und die Divergenz in den Gate-Nachweisen dokumentieren; (c) getrennte Behandlung — ADRs vs. FROZEN Architecture Book vs. CLAUDE.md/ROADMAP.md |
| **Empfehlung** | **Vor SPR-02 disponieren.** Begründung: ADR-006 D4 ist die Vertragsgrundlage für TD-04; ohne geklärte Fassung fehlt WP-001..WP-005 ein eindeutiger Bezugstext. **Ohne Präferenz zwischen (a)/(b)/(c)** — das ist Governance |
| **Security-Wirkung** | Mittelbar: ADR-005/006 sind die Bezugstexte der Plugin-Security-Befunde |
| **Architektur-Wirkung** | Berührt den Architecture Freeze (Option a) |
| **Test-Wirkung** | keine |
| **Produkt-Wirkung** | keine |
| **Ökonomische Wirkung** | Verzögerungsrisiko bei Nichtbehandlung |
| **Erforderliche Autorität** | **Projekteigner / Governance Architect** |

### OD-02 — Status von `app/host.py` und des `ui/`-Altbestands

| Feld | Inhalt |
|---|---|
| **Problem** | Zweiter, gleichnamiger Composition Root plus zugehöriger UI-/AI-Altbestand innerhalb der als produktiv entschiedenen Struktur (AM-02/AM-03) |
| **Evidenz** | app/host.py:27-38; tests/test_foundation.py:8; ui/foundation_window.py; core/worker.py:3 |
| **Warum offen** | GDR-002 entscheidet ausschließlich über `src/jochen_x/**` und ausdrücklich keine andere Governance-Frage [SOURCE: gr-001-governance-decision.md §2, §12] |
| **Optionen** | (a) Erhaltung (Status quo, dokumentiert); (b) Stilllegung analog D-2 ohne physische Entfernung; (c) Überführung/Bereinigung — **berührt RB-1.0**, da `tests/test_foundation.py` (7 Tests) daran hängt |
| **Empfehlung** | **Entscheiden, bevor WP-002 (Host Service Description, FR-003) beginnt.** Begründung: FR-003 verlangt eine *zentrale* Host-Dienst-Beschreibung; zwei Composition Roots widersprechen dem Begriff „zentral" direkt |
| **Security-Wirkung** | Latenter Pfad ohne Plugin-Pipeline (nicht aktiv) |
| **Architektur-Wirkung** | Hoch — betrifft die Aussage „einziger Kompositionsmechanismus" |
| **Test-Wirkung** | Option (c) verändert RB-1.0 → Regressionsbezugsgröße betroffen |
| **Produkt-Wirkung** | keine unmittelbare |
| **Erforderliche Autorität** | **Projekteigner / Governance Architect** (bei (c) zusätzlich Regressions-Disposition) |

### OD-03 — Packaging- und Werkzeugkonfiguration

| Feld | Inhalt |
|---|---|
| **Problem** | `pyproject.toml` adressiert den stillgelegten Baum (RT-06) |
| **Evidenz** | pyproject.toml:14-29; GDR-002 D-1 |
| **Warum offen** | GDR-002 D-2 klammert die physische/konfigurative Behandlung aus |
| **Optionen** | (a) Konfiguration auf die produktive Struktur umstellen; (b) belassen und Auslieferung als out-of-scope erklären; (c) mit OD-02 bündeln |
| **Empfehlung** | Behandlung **vor** einer etwaigen CI-Einführung (PC-05); ohne korrektes Packaging misst CI den falschen Baum |
| **Security-Wirkung** | keine direkte |
| **Architektur-Wirkung** | gering |
| **Test-Wirkung** | `testpaths` betrifft, welche Tests „standardmäßig" laufen (RK-05) |
| **Ökonomische Wirkung** | Auslieferbarkeit des Produkts |
| **Erforderliche Autorität** | **Projekteigner** |

### OD-04 — Plugin-Isolationsstrategie

| Feld | Inhalt |
|---|---|
| **Problem** | Plugins laufen in-process ohne Isolation; jedes Permission-Modell ist dadurch beratend (SEC-04) |
| **Evidenz** | stages_plugin.py:501-518; ADR-009 (Titel „Plugin Isolation Strategy"); docs/security-design-1.0.md §12, §19 |
| **Warum offen** | Security-Architekturentscheidung; ODD-Register offen; ausdrücklich außerhalb der Autorisierungsgrenze dieser Analyse |
| **Optionen** | **Werden hier bewusst nicht aufgezählt** — die Optionsbildung wäre bereits Security-Architekturarbeit (Auftrag Kap. 14: keine neue Trust-Taxonomie, keine stille ODD-Auflösung) |
| **Empfehlung** | **Keine.** Feststellung: Diese Entscheidung sollte **vor** jeder Fähigkeit fallen, die Fremd- oder KI-erzeugten Code ausführt |
| **Erforderliche Autorität** | **Projekteigner + Security-Governance** (ADR-pflichtig, je ADR separat zu autorisieren [SOURCE: jochen-x-next-authorized-work-assessment.md §7]) |
| **Status** | Siehe auch **BD-01** (Kap. 33) |

### OD-05 — Security-Verdrahtung im Bootstrap

| Feld | Inhalt |
|---|---|
| **Problem** | `SecurityBootstrapStage` läuft nach der Plugin-Pipeline; Policies sind nicht konfigurierbar; Trust-Ledger-Identität wechselt (TD-04, TD-05, TD-19, TD-21, TD-06) |
| **Evidenz** | security_manager.py:202-204, :236; stages_plugin.py:262-266, :306-318; config/default.toml |
| **Warum offen** | Eine Korrektur berührt Stage-Zusammensetzung/-Reihenfolge → Bootstrap Baseline §8 Change Control (ADR oder RDR erforderlich) |
| **Optionen** | (a) `PluginSecurity` bereits in INITIALIZE komponieren und konfigurieren; (b) Policy-Konfiguration in die bestehende `PluginSecurityStage` ziehen (ohne Reihenfolgeänderung); (c) Status quo dokumentieren und im Milestone unverändert lassen |
| **Empfehlung** | Option (b) ist die **eingriffsärmste** Variante und käme ohne Änderung der Phasen- oder Stage-Reihenfolge aus — sie löst TD-05 vollständig und TD-19 teilweise. **Dies ist eine Empfehlung, keine Entscheidung**; sie ersetzt keine ADR-/RDR-Prüfung |
| **Security-Wirkung** | Hoch — betrifft die tatsächliche Wirksamkeit der Admission-Policy |
| **Architektur-Wirkung** | Option (a) berührt Baseline §8; Option (b) voraussichtlich nicht |
| **Test-Wirkung** | Neue Tests erforderlich (TG-2, TG-3, TG-4) |
| **Erforderliche Autorität** | **Projekteigner + Architektur-/Security-Governance** |

### OD-06 — Auslegung von NFR-007 für vorbestehende Abhängigkeiten

| Feld | Inhalt |
|---|---|
| **Problem** | Zählt eine **vorbestehende**, undeklarierte Abhängigkeit (`ollama`) als NFR-007-Verstoß oder als Altbestand außerhalb des Milestone-Scopes? (AI-02) |
| **Evidenz** | core/ai_manager.py:1; pyproject.toml:10-12; ES §8.2 NFR-007; ES §5.2 |
| **Warum offen** | NFR-007 ist auf den Milestone bezogen formuliert; der Fall ist vorbestehend |
| **Optionen** | (a) als Altbestand einstufen und mit OD-02 disponieren; (b) deklarieren; (c) als NFR-007-Verstoß behandeln und beheben |
| **Empfehlung** | Gemeinsam mit OD-02 behandeln — es ist derselbe Altbestand-Cluster |
| **Erforderliche Autorität** | **Projekteigner** |

### OD-07 — Event-Zustellsemantik bei Handler-Ausnahmen

| Feld | Inhalt |
|---|---|
| **Problem** | Abbruch der Zustellkette und Propagation zum Publisher (REL-01/TD-23) steht FR-010 entgegen |
| **Evidenz** | core/events.py:82-89; ES §7.2 FR-010; ADR-002 |
| **Warum offen** | Das Verhalten ist Gegenstand von ADR-002; eine Änderung ist eine Semantikänderung eines genehmigten Kontrakts |
| **Optionen** | (a) Status quo; (b) Isolation je Handler mit Fehleraufzeichnung; (c) differenziert nach Abonnentenherkunft (Host vs. Plugin) |
| **Empfehlung** | Im Rahmen von **WP-005 / SPR-06 (Reliability, FR-009/FR-010)** prüfen — dort ist es planmäßig verortet. **Keine** eigenmächtige Änderung |
| **Security-Wirkung** | Mittelbar (Verfügbarkeit) |
| **Erforderliche Autorität** | **Architektur-Governance** (ADR-002-Berührung) |

### OD-08 — Statusnachführung des Sprint Plans

| Feld | Inhalt |
|---|---|
| **Problem** | Kopf trägt DRAFT, die Genehmigung liegt über ADW-SPR-1.0-001 vor (SG-02) |
| **Evidenz** | docs/milestone-1.0-sprint-plan.md (Kopf); docs/governance/milestone-1.0-sprint-01-baseline-confirmation.md §2 |
| **Optionen** | (a) Kopf im vorgesehenen kontrollierten Verfahren nachführen; (b) belassen, da die Genehmigungskette dokumentiert ist |
| **Empfehlung** | Redaktionell, nicht dringlich; sinnvoll gemeinsam mit OD-01 |
| **Erforderliche Autorität** | **Projekteigner / Governance** |

### 20.1 Bereits bestehende offene Punkte (nicht neu, nur gespiegelt)

Diese Analyse **schließt keinen** dieser Punkte und **erweitert** sie nicht:

OP-1..OP-8, OTD-1, OTD-2 [SOURCE: docs/milestone-1.0-sprint-plan.md §8] ·
GR-001 (DECIDED durch GDR-002) · SD-W1-F-04 · SD-W1-F-06 · SA-W1-F01 ·
SA-W1-F03 · SA-W1-F04 · ODD-01–ODD-20 · GF-02/GC-01 · GF-03/GC-02 ·
GC-03–GC-07 · GQ-1 · GQ-2 · GQ-3 · WAIVER-DEV-001 §9 (3) · R2-E-01
[SOURCE: docs/governance/jochen-x-next-authorized-work-assessment.md §2, §3].

---

## 21. Current-vs-Approved Gap Analysis

Legende: **MATCH** · **PARTIAL MATCH** · **DEVIATION** · **MISSING** · **UNKNOWN**

### 21.1 Gegen Bootstrap Baseline 1.0

| Gegenstand | Soll | Ist | Ergebnis |
|---|---|---|---|
| Paketstruktur (7 Module) | §2 | 7 Module | **MATCH** |
| Invarianten 1–7 | §4 | alle geprüft | **MATCH** (Kap. 8.2) |
| Public Exports | §3.1 Aufzählung (22) / Überschrift („20") | 22 | **MATCH gegen Aufzählung**, Überschrift redaktionell falsch (TD-08) |
| Interne Re-Exports (2) | §3.2 | `_require`, `_validate_for_activation`, nicht in `__all__` | **MATCH** |
| Phasensequenz | §5.1 | identisch | **MATCH** |
| Plugin-Pipeline-Reihenfolge | §5.2 (5 Schritte) | Reihenfolge identisch, 6 Schritte | **PARTIAL MATCH** (TD-12) |
| Regressionsbasis | §7 (1019) | durch GDR-002 D-3 / SPR-01 auf RB-1.0 = 258 verengt | **MATCH nach Governance-Nachführung** |

### 21.2 Gegen Architecture Book v2.0

| Gegenstand | Ergebnis | Beleg |
|---|---|---|
| Schichtmodell Core→App→Plugins/SDK→Services→Developer→UI | **PARTIAL MATCH** | eingehalten außer `core/ai_manager.py`, `core/worker.py` (AM-01) |
| `ServiceRegistry` als einziger Kompositionsmechanismus | **PARTIAL MATCH** | zweiter Composition Root `app/host.py` (AM-02) |
| Event Bus (§9) | **MATCH** | core/events.py vollständig |
| Plugin-System (§10) | **MATCH** | manifest-only, ADR-001 belegt |
| Security (§11) | **PARTIAL MATCH** | Trust Ledger vorhanden; Runtime-Integration „steht aus" (Welt A, §20) |
| Recovery (§12) | **PARTIAL MATCH** | Host-Recovery vorhanden; Lücken RT-04/TD-25 |
| Observability (§13) | **PARTIAL MATCH** | minimal, erweiterbar erst durch WP-004 |
| Architecture Freeze (§22) | **MATCH am Baseline** | AB unverändert **in Welt A**; Welt-B-Modifikation ist Dispositionsgegenstand (OD-01) |
| ADR-Status (§20) | **DEVIATION zwischen Welt A und B** | Kap. 4.2 |

### 21.3 Gegen Engineering Specification 1.0 — Functional Requirements

Bewertung des **Ausgangszustands** (nicht der Zielerfüllung; alle 29 AC stehen
planmäßig auf NOT VERIFIED [SOURCE: docs/milestone-1.0-sprint-plan.md §5]).

| FR | Gegenstand | Ist-Zustand | Ergebnis | Anmerkung |
|---|---|---|---|---|
| FR-001 | Lifecycle-Determinismus | Tabellengetriebene Maschine, 10 Zustände, thread-safe | **weitgehend MATCH** | ES §5.5 („Übergänge nicht vollständig definiert") **überschätzt die Lücke** |
| FR-002 | Ablehnung unzulässiger Übergänge | `IllegalStateTransitionError` mit Von/Nach-Angabe | **MATCH** | ebenso |
| FR-003 | Zentrale Host-Dienst-Beschreibung | `descriptors()` liefert Metadaten; **zwei** Composition Roots | **PARTIAL MATCH** | durch OD-02 berührt |
| FR-004 | Formale Erweiterungspunkte | `stages`-Parameter, `core/extensions.py`, SDK-Kontrakte | **PARTIAL MATCH** | nicht formal beschrieben |
| FR-005 | Autorenvorgaben an einer Stelle | `docs/sdk.md`, `docs/extensions.md`, `docs/adr/*`, CLAUDE.md — verstreut | **PARTIAL MATCH** | ES §5.5 trifft zu |
| FR-006 | Rejection-Feedback mit Stufe + Kriterium | `RejectionCode` (11 Werte) + `ValidationDiagnostic` vorhanden; Integrity-/Permission-Ablehnungen der Security-Stage tragen **keinen** `RejectionCode`; `PluginFailed("")` ohne Identifier | **PARTIAL MATCH** | TD-14, TD-26 |
| FR-007 | Strukturierte Diagnostik | `ActivationFailure`, `ValidationDiagnostic`, `PluginHealthCheck` | **PARTIAL MATCH** | nicht zentral abrufbar |
| FR-008 | Erweiterbare Observability | `Metrics` ist ein geschlossener `dict`; kein Erweiterungspunkt | **MISSING** | deckt sich mit OTD-1 |
| FR-009 | Definiertes Wiederherstellungsverhalten | `recover()`, `restart()` vorhanden | **PARTIAL MATCH** | TD-11, TD-25 |
| FR-010 | Failure Isolation | Aktivierung: **MATCH**; Discovery: **DEVIATION**; Events: **DEVIATION**; Listener: **DEVIATION** | **PARTIAL MATCH** | TD-14, TD-23, TD-24 — **Lücke größer als in ES §5.5 angenommen** |
| FR-011 | SDK-Dokumentation vollständig | `docs/sdk.md` (531 Z.), `docs/extensions.md` (850 Z.) | **PARTIAL MATCH** | ES §5.5 trifft zu |
| FR-012 | Architekturdoku aktuell | mehrere Abweichungen (Kap. 18.3) | **PARTIAL MATCH** | ES §5.5 trifft zu |
| FR-013 | Additivitätsregel | am Baseline gewahrt | **MATCH** (Ausgangszustand) | Nachweis in SPR-09 |
| FR-014 | Consumer-Kompatibilität | SDK API 1.0.0 unverändert | **MATCH** (Ausgangszustand) | Nachweis in SPR-09 |

### 21.4 Gegen Non-Functional Requirements

| NFR | Gegenstand | Ergebnis | Beleg |
|---|---|---|---|
| NFR-001 | Architecture Freeze Compliance | **MATCH am Baseline** | AB in Welt A unverändert |
| NFR-002 | Bootstrap Baseline Invariants | **MATCH** | Kap. 8.2 |
| NFR-003 | SDK API 1.0.0 rückwärtskompatibel | **MATCH** | sdk/version.py:27 |
| NFR-004 | Performance-Non-Degradation | **UNKNOWN** | keine Messreihe (PERF-02) |
| NFR-005 | Test-Regressionsbasis | **MATCH nach Nachführung** | NFR-005 nennt 1019; verbindlich ist RB-1.0 = 258 (GDR-002 D-3, SPR-01 §10). **Textliche Divergenz im ES, materiell durch Governance aufgelöst** — hier nur festgestellt |
| NFR-006 | Security-Pipeline-Compliance | **MATCH** | Reihenfolge unverletzt (BS-04) |
| NFR-007 | Keine externen Abhängigkeiten | **PARTIAL MATCH / strittig** | `ollama` vorbestehend und undeklariert (AI-02) → **OD-06** |

**Nebenbefund Thread-Sicherheit** (kein NFR, aber qualitätsrelevant):

| Komponente | Zustand |
|---|---|
| `EventBus` | `RLock` um History/Sticky/Subscriptions — **gut** |
| `ApplicationStateMachine` | `RLock` um Zustand und Listener-Snapshot — **gut** |
| `PluginSecurity` | `RLock` um alle Ledger-Zugriffe — **gut** |
| `ServiceRegistry` | `register_factory` und `descriptors()` unter Lock; **`_resolve` und das Singleton-Caching nicht** [SOURCE: core/registry.py:131-150] — **Lücke (TD-07)** |
| `Metrics` | kein Lock [SOURCE: core/observability.py:20-31] — **Lücke (TD-10)** |

### 21.5 Gegen Charter

| Charter-Position | Ergebnis |
|---|---|
| Scope: Plattform-Härtung, Host-Services, Plugin-Ökosystem, Observability, Testabdeckung, Dokumentation | Ausgangszustand konsistent; Arbeit steht aus |
| Out of Scope: Architektur-Redesign, Bootstrap-Redesign, SDK Breaking Changes, experimentelle Features, UI-Redesign, externe Abhängigkeiten | **Diese Analyse schlägt nichts vor, das eine dieser Grenzen überschreitet.** Einzige Berührung: `ollama` (vorbestehend) → OD-06 |

### 21.6 Zusammenfassung

| Ergebnis | Anzahl (FR+NFR) |
|---|---|
| MATCH | 9 |
| PARTIAL MATCH | 11 |
| DEVIATION (Teilaspekte innerhalb FR-010) | 3 Teilbefunde |
| MISSING | 1 (FR-008) |
| UNKNOWN | 1 (NFR-004) |

> **GAP-01:** Der Ausgangszustand ist **besser als von ES §5.5 angenommen** bei
> FR-001/FR-002 und **schlechter** bei FR-010. Beide Abweichungen sind
> Feststellungen; sie ändern **keinen** Requirement und **keine**
> Work-Package-Zuordnung.

---

## 22. Target State

> **Regel (Auftrag Kap. 27):** Es wird **keine konkurrierende Roadmap**
> erzeugt. Der Zielzustand enthält **ausschließlich** Positionen, die durch
> genehmigte Quellen gedeckt sind. Nichts wird als automatisch autorisiert
> dargestellt.

### 22.1 Zielzustand Milestone 1.0 (quellengedeckt)

Der Zielzustand ist der in der Engineering Specification definierte: 14 FRs, 7
NFRs, 29 Acceptance Criteria, 8 Quality Gates, 7 Work Packages
[SOURCE: docs/milestone-1.0-engineering-spec.md §7, §8, §11, §12, §14].
Er wird hier **nicht neu formuliert**.

| Dimension | Zielzustand nach M1.0 | Klassifikation |
|---|---|---|
| Lifecycle-Determinismus | AC-001.1..AC-002.2 VERIFIED | **APPROVED DIRECTION** |
| Host-Dienst-Beschreibung + Erweiterungspunkte | AC-003.1..AC-004.2 VERIFIED | **APPROVED DIRECTION** |
| Autorenvorgaben + Rejection-Feedback | AC-005.1..AC-006.2 VERIFIED | **APPROVED DIRECTION** |
| Plugin-Diagnostik + erweiterbare Observability | AC-007.1..AC-008.2 VERIFIED | **APPROVED DIRECTION** |
| Recovery + Failure Isolation | AC-009.1..AC-010.2 VERIFIED | **APPROVED DIRECTION** |
| SDK-/Architekturdokumentation | AC-011.1..AC-012.2 VERIFIED | **APPROVED DIRECTION** |
| Additivität + Consumer-Kompatibilität | AC-013.1..AC-014.2 VERIFIED | **APPROVED DIRECTION** |
| Architecture Freeze, Baseline-Invarianten, SDK API 1.0.0 unverändert | erhalten | **APPROVED DIRECTION** |
| RB-1.0 grün + MWB-015-Zuwachs | keine Regression | **APPROVED DIRECTION** |

### 22.2 Was der Zielzustand von M1.0 **nicht** umfasst

KI-Fähigkeit · Memory · Agents · Automation · Multimodal · Trading (jede
Stufe) · Plugin-Isolation · Kryptografie · CI · Packaging-Korrektur ·
Auflösung von OD-01..OD-08.

> **TS-01:** Keine dieser Positionen ist Bestandteil des genehmigten
> Milestone-1.0-Zielzustands. Ihre Aufnahme wäre eine Scope-Erweiterung und
> bedürfte einer Governance-Entscheidung.

### 22.3 Zustand jenseits Milestone 1.0

| Fähigkeit | Klassifikation | Beleg |
|---|---|---|
| Security-Design-ODDs → Security-ADRs | **OPEN** — je ADR einzeln zu autorisieren | [SOURCE: jochen-x-next-authorized-work-assessment.md §5 B Nr. 2, §7] |
| Security Design R1 (Correction Cycle) | **RECOMMENDED**, bereits zugewiesen, Startfreigabe fehlt | [SOURCE: ebd. §9, §12 Nr. 2] |
| SA Correction Cycle (SA-W1-F01/F03) | **RECOMMENDED**, geringe Dringlichkeit | [SOURCE: ebd. §9] |
| Rangentscheidung Dokumentklassen (GQ-1) | **OPEN** | [SOURCE: ebd. §4] |
| Plugin-Isolation (ADR-009-Konkretisierung) | **OPEN / NOT AUTHORIZED** | OD-04, BD-01 |
| Kryptografie (ODD-19) | **OPEN / NOT AUTHORIZED** | BD-02 |
| Audit-Ereigniskatalog (ODD-17) | **OPEN** | [SOURCE: ebd. §5 D] |
| KI-Fähigkeit | **FUTURE / NOT AUTHORIZED** | Kap. 11.5 |
| Memory | **FUTURE / OPEN / NOT AUTHORIZED** | Kap. 12 |
| Agents / Automation / Multimodal | **FUTURE / NOT AUTHORIZED** | Kap. 13 |
| Trading RESEARCH/SIMULATION/BACKTESTING/PAPER | **FUTURE / OPEN** — Stufenmodell ODD-14 zurückgestellt | [SOURCE: ebd. §3 E] |
| **Trading CONTROLLED LIVE** | **NOT AUTHORIZED** | Kap. 14.2 |
| Security Engineering Specification | **NOT AUTHORIZED** | [SOURCE: ebd. §8] |

> **TS-02:** **CONTROLLED LIVE TRADING wird in diesem Dokument ausdrücklich
> nicht als autorisierter oder eingeplanter Meilenstein dargestellt.**

---

## 23. Implementation Roadmap

> **Vorrangregel (Auftrag Kap. 28):** Der genehmigte Sprint Plan ist die
> **maßgebliche Ausführungssequenz**. Diese Roadmap **erklärt** ihn, benennt
> Abhängigkeiten und Risiken und macht Vorschläge — sie **ersetzt ihn nicht**
> und erfindet weder Sprints noch Work Packages.

### 23.1 Die genehmigte Sequenz (unverändert übernommen)

```
Phase A   SPR-01  Baseline Confirmation                    ✔ ABGESCHLOSSEN
             ↓
Phase B   SPR-02  WP-001 Platform Hardening      ┐
          SPR-03  WP-002 Host Service & Extens.  │
          SPR-04  WP-003 Developer Experience    │ parallelisierbar,
          SPR-05  WP-004 Observability           │ keine verbindliche
          SPR-06  WP-005 Reliability             │ Ordnung (IP §6.3)
          SPR-07  WP-007 Documentation           ┘
             ↓  (alle sechs abgeschlossen)
          SPR-08  Phase-B-Abschluss: Regression & Messreihe (EV-I01)
             ↓
Phase C   SPR-09  WP-006 SDK Contract Verification
             ↓
Phase D   SPR-10  Governance Closure
```
[SOURCE: docs/milestone-1.0-sprint-plan.md §3]

### 23.2 Gate vor jeder Umsetzungsarbeit

| # | Bedingung | Status |
|---|---|---|
| 7 | Genehmigte Sprintplanung | **PENDING** (Plan trägt DRAFT; ADW-SPR-1.0-001 genehmigt ihn als Planungsgrundlage — OD-08) |
| 8 | Baseline-Bestätigung protokolliert (SPR-01) | **ERFÜLLT** [SOURCE: milestone-1.0-sprint-01-baseline-confirmation.md §14] |
| 9 | RL-05 erreicht | **PENDING** |
[SOURCE: docs/milestone-1.0-sprint-plan.md §6]

> **RM-01:** **CODING = NOT AUTHORIZED.** Diese Analyse ändert daran nichts
> und erzeugt keine Coding-Freigabe.

### 23.3 Empfohlene Vorarbeiten *innerhalb* des autorisierten Rahmens

Read-only-Arbeiten und Entscheidungen sind bereits autorisiert bzw. bedürfen
nur einer Projekteigner-Entscheidung
[SOURCE: docs/governance/jochen-x-next-authorized-work-assessment.md §5 A/B].

| Reihenfolge | Arbeit | Kategorie | Warum vor Phase B |
|---|---|---|---|
| V-1 | **OD-01** disponieren (ADR-/AB-/CLAUDE.md-Fassungen) | Governance-Entscheidung | ADR-006 D4 ist Bezugstext für WP-001..WP-005; ohne geklärte Fassung fehlt der Vertragstext |
| V-2 | **OD-02** entscheiden (`app/host.py`-Cluster) | Governance-Entscheidung | FR-003 („zentrale Registrierung") ist mit zwei Composition Roots nicht widerspruchsfrei erfüllbar |
| V-3 | **Baseline-Messreihe** gemäß IP Anhang B erheben (OP-8) | bereits vorgesehen | NFR-004 braucht einen **Vorher**-Punkt; nach den Änderungen erhoben ist er wertlos |
| V-4 | **OD-05** entscheiden (Security-Verdrahtung) | Governance-Entscheidung | Betrifft WP-003/WP-004 (QG-006 Pipeline Security Compliance) |
| V-5 | **OD-03** entscheiden (Packaging) | Governance-Entscheidung | Voraussetzung für belastbare, reproduzierbare Gate-Nachweise |

> **RM-02 (RECOMMENDATION, nicht REQUIRED):** V-1 bis V-5 sind **keine neuen
> Work Packages und kein neuer Sprint**. V-1, V-2, V-4, V-5 sind
> Entscheidungen; V-3 ist eine im Plan bereits vorgesehene Evidenzerhebung
> (OP-8). Sie werden hier als **empfohlene Reihenfolge** dargestellt, nicht als
> Bedingung.

### 23.4 Verfeinerung *innerhalb* der genehmigten Phase B

Die Phase-B-Sprints sind laut Plan ohne verbindliche Ordnung
[SOURCE: docs/milestone-1.0-sprint-plan.md §3, IP §6.3]. Innerhalb dieses
Spielraums:

| Vorschlag | Begründung | Charakter |
|---|---|---|
| **SPR-06 (WP-005 Reliability) früh beginnen** | Enthält FR-010; die drei belegten Isolationslücken (TD-14, TD-23, TD-24) liegen dort. Sie berühren `EventBus` und `PluginLoader` — Komponenten, auf die WP-004 (Observability) und WP-002 (Host Services) aufsetzen | Reihenfolgeempfehlung **innerhalb** des genehmigten Spielraums — **keine** Planänderung |
| **SPR-07 (WP-007 Documentation) zuletzt abschließen** | Der Plan sieht dies bereits vor: Schlussfassung setzt Endstand WP-002/WP-004 voraus [SOURCE: Sprint Plan, SPR-07 Abhängigkeiten] | **Bestätigung** der Planvorgabe |
| **OTD-1 (MWB-008) vor dem betroffenen Teil von SPR-05 festlegen** | Der Plan markiert es als blockierend „für den betroffenen Teil" [SOURCE: Sprint Plan §8, OTD-1]. FR-008 ist der einzige **MISSING**-Befund der Gap-Analyse — die offene Position dürfte genau dort liegen | **Bestätigung** |

---

## 24. Sprint Mapping

> **Regel:** Kein Sprint wird erfunden, keiner umbenannt, kein Work Package neu
> geschaffen. Positionen ohne Zuordnung erscheinen als **OPEN DECISION /
> PROPOSED CHANGE**.

### 24.1 Befunde mit vorhandener Sprint-/WP-Zuordnung

| Befund | Sprint | Work Package | Abhängigkeit | Autorisierungsstatus |
|---|---|---|---|---|
| TD-14 (Discovery-Isolation) | **SPR-06** | **WP-005** (FR-010) | [G] Coding Gate | **PENDING** (Gate 7–9) |
| TD-23 (Event-Zustellisolation) | **SPR-06** | **WP-005** (FR-010) | [G] Coding Gate; **OD-07** (ADR-002) | **PENDING + OPEN DECISION** |
| TD-24 (Listener-Isolation) | **SPR-06** | **WP-005** (FR-010) | [G] Coding Gate | **PENDING** |
| TD-11, TD-25 (Restart-/Reset-Hygiene) | **SPR-06** | **WP-005** (FR-009) | [G] Coding Gate | **PENDING** |
| TD-26 (irreführender Docstring `_validate_for_activation`) | **SPR-04** | **WP-003** (FR-006) | [G] Coding Gate | **PENDING** |
| TD-14-Teil (`PluginFailed("")` ohne Identifier) | **SPR-04** | **WP-003** (FR-006) | [G] Coding Gate | **PENDING** |
| TD-10 (Metrics-Kardinalität/Locking) | **SPR-05** | **WP-004** (FR-007/FR-008) | [G] Coding Gate; **OTD-1** | **PENDING** |
| FR-008 **MISSING** (Observability nicht erweiterbar) | **SPR-05** | **WP-004** | **OTD-1** | **PENDING + OPEN TECHNICAL DECISION** |
| TD-08 (Baseline „20 vs. 22") | **SPR-07** | **WP-007** (FR-012) | — | **PENDING** |
| TD-12 (Pipeline 5 vs. 6 Schritte) | **SPR-07** | **WP-007** (FR-012) | — | **PENDING** |
| Doku-Abweichungen Kap. 18.3 (CLAUDE.md-Struktur, `docs/security.md`) | **SPR-07** | **WP-007** (FR-011/FR-012) | `docs/security.md`: **GF-03/GC-02 offen** | **PENDING + OPEN** |
| FR-003-Spannung durch zwei Composition Roots | **SPR-03** | **WP-002** (FR-003) | **OD-02** | **BLOCKED bis OD-02** |
| Formale Erweiterungspunkte (FR-004) | **SPR-03** | **WP-002** | [G] Coding Gate | **PENDING** |
| Autorenvorgaben zentralisieren (FR-005) | **SPR-04** | **WP-003** | [G] Coding Gate | **PENDING** |
| Baseline-Messreihe (OP-8) | Vorbereitung → Nachweis in **SPR-08** | — | im Plan vorgesehen | **PENDING** |
| RB-1.0-Regressionsnachweis | **SPR-08** | — (MWB-015) | alle Phase-B-WPs | **PENDING** |
| Additivität/Consumer-Kompatibilität (TD-08-Bezug, `create_desktop_bootstrap_manager`) | **SPR-09** | **WP-006** (FR-013/FR-014) | EV-I01 | **PENDING** |

### 24.2 Befunde **ohne** Sprint-/WP-Zuordnung

Diese Positionen fallen **nicht** in den genehmigten Milestone-1.0-Scope. Es
wird ausdrücklich **kein** neues Work Package geschaffen.

| Befund | Warum keine Zuordnung | Erforderlich |
|---|---|---|
| TD-01 (`app/host.py`) | Kein FR adressiert Altbestandsbereinigung; Charter-Out-of-Scope „Architektur-Redesign" | **OD-02 — PROPOSED CHANGE** |
| TD-02 (Packaging) | Kein FR adressiert Packaging | **OD-03 — PROPOSED CHANGE** |
| TD-03 (`ollama`) | Vorbestehend; NFR-007-Auslegung offen | **OD-06** |
| TD-04 (Runtime-Enforcement) | ADR-006 D4 ist eine **Architektur**-Anforderung, kein Milestone-FR | **OD-01 + OD-05** |
| TD-05, TD-19, TD-21, TD-06 (Security-Verdrahtung) | Kein FR; berührt Bootstrap Baseline §8 | **OD-05** |
| TD-15 (`entry_point`) | Verhaltensänderung der Aktivierung; ADR-011-Berührung möglich | **OPEN DECISION** |
| TD-16 (fail-open bei unparsbarer Version) | ADR-007-Semantik | **OPEN DECISION** |
| TD-17, TD-20 (Integrity-Benennung, Base64-„Encryption") | ODD-19 offen | **BD-02** |
| TD-18 (Identifier-Validierung) | Security-Härtung ohne FR | **OPEN DECISION** |
| TD-07 (Registry-Thread-Sicherheit) | Kein FR; Kernkomponente | **OPEN DECISION** |
| TD-09 (kein CI) | Kein FR | **PROPOSED CHANGE PC-05** |
| TD-13, TD-22, TD-27 | Kein FR; geringe Wirkung | **OPEN** |
| OD-04 (Isolation) | Security-Architektur, nicht Milestone-Scope | **BD-01** |

### 24.3 Quality-Gate-Zuordnung der Befunde

| Gate | Berührende Befunde | Frühestmöglicher Abschluss | Status |
|---|---|---|---|
| QG-001 Platform Stability | FR-001/002 bereits weitgehend MATCH | Ende Phase B | **NOT STARTED** |
| QG-002 Host Service Availability | OD-02 (zwei Composition Roots) | Abschluss WP-002 | **NOT STARTED** |
| QG-003 Architecture Freeze Compliance | TD-08, TD-12, `create_desktop_bootstrap_manager` (BS-03), OD-01 | Ende Phase C | **NOT STARTED** |
| QG-004 Developer Feedback Quality | TD-26, TD-14-Teil | Abschluss WP-003 | **NOT STARTED** |
| QG-005 Traceability Completeness | Kap. 18.3, Welt-A/B-Divergenz (RK-02) | Abschluss WP-007 | **NOT STARTED** |
| QG-006 Pipeline Security Compliance | TD-04, TD-05, TD-19, TD-21 | WP-003 **und** WP-004 | **NOT STARTED** |
| QG-007 Test Coverage Maintenance | TG-1..TG-9, RB-1.0 | Ende Phase B | **NOT STARTED** |
| QG-008 Governance Compliance | OD-01..OD-08 | Phase D | **NOT STARTED** |
[Gate-Definitionen und Status: SOURCE: docs/milestone-1.0-sprint-plan.md §5]

> **SM-01:** **Kein Gate wird durch dieses Dokument als PASSED markiert.**
> Alle acht bleiben NOT STARTED.

---

## 25. Quality Gates

Für jeden Umsetzungsbereich: erforderliche Tests, Verifikation, Regressions-
und Rollback-Erwägungen. **Keines dieser Elemente ist hier erfüllt oder
bestanden.**

| Bereich | Erforderliche Tests | Verifikation | Regression | Akzeptanznachweis | Rollback |
|---|---|---|---|---|---|
| **WP-001** Platform Hardening | Zustandsmaschinen-Tests für alle 10 Zustände und deren Ablehnungen | manuelle Verifikation + Suite (EV-W01) | RB-1.0-Anteil | AC-001.1..AC-002.2 | Zustandsmaschine ist reine Tabelle → Rücknahme risikoarm |
| **WP-002** Host Service | ServiceRegistry-Verifikation, Integration Tests | EV-W02 | RB-1.0-Anteil | AC-003.1..AC-004.2 | **Achtung:** TD-06-Hacks würden bei Registry-Änderung brechen |
| **WP-003** Developer Experience | Rejection-Nachrichten je `RejectionCode`; TG-1 | EV-W03 | RB-1.0-Anteil | AC-005.1..AC-006.2 | dokumentationsnah, risikoarm |
| **WP-004** Observability | Metrik-/HealthCheck-Erweiterungstests; TG-7 | Pipeline-Verifikation, EV-W04 | RB-1.0-Anteil | AC-007.1..AC-008.2 | OTD-1 muss vorher entschieden sein |
| **WP-005** Reliability | TG-1, TG-5, TG-6 (Discovery-, Restart-, Event-Isolation) | EV-W05 | RB-1.0-Anteil | AC-009.1..AC-010.2 | **Achtung:** Event-Semantik (OD-07) ist ADR-002-gebunden |
| **WP-006** SDK Contract | API-Surface-Vergleich gegen eingefrorene Baseline | EV-W06, EV-I03, EV-I04 | vollständig | AC-013.1..AC-014.2 | Additivität muss gewahrt bleiben |
| **WP-007** Documentation | Vollständigkeitsabgleich | EV-W07, EV-D04 | — | AC-011.1..AC-012.2 | **Achtung:** keine Änderung am FROZEN Architecture Book |
| **Phase-B-Abschluss** | RB-1.0 (258) + MWB-015-Zuwachs; Vergleichsmessreihe | EV-I01, EV-I02 | vollständig | QG-001, QG-007 | Rückkehr in betroffene Provider-Sprints |
[Evidenz-IDs und Verifikationsarten: SOURCE: docs/milestone-1.0-sprint-plan.md §4]

> **QG-01:** **Kein Gate wird durch diese Analyse als bestanden markiert.
> Es wird keine Coding-Autorisierung erzeugt und keine aus dieser Analyse
> abgeleitet.**

---

## 26. Security Gates

Sicherheitsspezifische Verifikationsanforderungen. **Keine ist erfüllt; keine
wird hier geschlossen.**

| SG | Gegenstand | Erforderlicher Nachweis | Bezug | Status |
|---|---|---|---|---|
| SG-A | Pipeline-Reihenfolge unverändert (Discovery → Integrity → Permission → Dependency → Activation) | Ablaufnachweis + Test | NFR-006, Baseline §4 Inv. 6 | **erfüllt am Baseline** (BS-04); Erhaltungsnachweis in SPR-09 offen |
| SG-B | Kein Plugin-Code vor bestandener Prüfung | Nachweis, dass der erste Import in FINALIZE liegt | CLAUDE.md Sicherheitsregeln | **erfüllt am Baseline** (SEC-02 Ziff. 1); Erhaltungsnachweis offen |
| SG-C | Default-Deny an der Admission-Grenze bleibt wirksam | Test gegen die **ausgelieferte** Konfiguration (TG-2) | ADR-006 D1 | **NICHT NACHGEWIESEN** (TD-05) |
| SG-D | Host-Grants erreichen die Laufzeitprüfung | Test (TG-4) | ADR-006 D4 | **NICHT ERFÜLLT** (TD-04) |
| SG-E | Trust-Ledger-Identität über die Phasen | Test (TG-3) | — | **NICHT ERFÜLLT** (TD-19) |
| SG-F | Audit-Trail der Admission-Entscheidungen | Ereigniskatalog + Nachweis | **ODD-17 offen** | **BLOCKED** |
| SG-G | Integritätsevidenzstufe dokumentiert und nicht überzeichnet | Dokumentationsabgleich | ODD-19, ADR-005 | **OFFEN** (TD-17) |
| SG-H | Kryptografischer Schutz für Secrets/Backups | Verfahrensentscheidung + Nachweis | **ODD-19 offen** | **BLOCKED** (BD-02) |
| SG-I | Identifier-Validierung vor Pfad-/Modulnutzung | Test + Codeprüfung | — | **NICHT ERFÜLLT** (TD-18) |
| SG-J | Plugin-Isolation | Architekturentscheidung + Nachweis | **ADR-009 / ODD-Register offen** | **BLOCKED** (BD-01) |
| SG-K | Secrets werden nicht geloggt | Codeprüfung | CLAUDE.md | **erfüllt am Baseline** (SEC-09) |

> **SEC-GATE-01:** **Keine Security-Design-ODD wurde geschlossen. Kein
> Security-Finding wurde geschlossen. Kein Security-ADR wurde erstellt oder
> vorgeschlagen. Keine neue Trust-Taxonomie und keine neue Risikoskala wurden
> eingeführt.**

---

## 27. Economic / Product Value Considerations

> **Regel (Auftrag Kap. 19):** Keine Umsatzprognosen. Keine Optimierung allein
> auf Ertrag. Keine unsicheren Abkürzungen zugunsten von Profitabilität.

### 27.1 Heutiger Produktwert

**ENGINEERING INFERENCE.** JOCHEN X liefert heute eine **Plattform**, kein
Endanwenderprodukt: eine lauffähige Desktop-Shell mit Navigation, ein
manifestbasiertes Plugin-System mit Sicherheitspipeline und ein reifes SDK.
Der Nutzwert für einen Endanwender ist derzeit gering; der Wert liegt in der
**Tragfähigkeit für spätere Fähigkeiten**.

### 27.2 Wertkritische Eigenschaften

| Eigenschaft | Bewertung | Begründung |
|---|---|---|
| **Erweiterbarkeit** | **hoch** | Manifest-Discovery, Stage-Protokoll, SDK-Additivität — Fähigkeiten sind als Plugins zuführbar, ohne den Kern zu ändern |
| **Auslieferbarkeit** | **derzeit nicht gegeben** | TD-02: `pip install .` liefert die Anwendung nicht aus |
| **Betriebskosten** | **sehr niedrig** | Lokal, eine deklarierte Abhängigkeit, SQLite; keine Serverinfrastruktur |
| **Modellkosten** | **derzeit null** | Keine KI-Inferenz im produktiven Pfad (AI-01). Bei späterer Aktivierung: lokal (ollama-Muster) → Rechenkosten statt API-Kosten |
| **Wartungskosten** | **erhöht** | Drei Schuldencluster (Kap. 18.4); zwei parallele Bäume (`src/jochen_x` + `app/host.py`-Cluster) |
| **Skalierbarkeit** | für den Zweck ausreichend | Single-Process-Desktop; keine Mandantenfähigkeit gefordert |
| **Zuverlässigkeit** | **gemischt** | Start/Shutdown stark; Isolation lückenhaft (Kap. 16.6) |

### 27.3 Ökonomisch wirksame Empfehlungen

**RECOMMENDATION, nicht REQUIRED:**

1. **Auslieferbarkeit herstellen (OD-03).** Ein Produkt, das sich nicht
   installieren lässt, hat keinen ökonomischen Wert — unabhängig von seiner
   Codequalität. Höchster Hebel bei geringstem Aufwand.
2. **Altbestand disponieren (OD-02).** Doppelte Pflege ist der teuerste
   Dauerposten; GDR-002 hat diesen Grund für `src/jochen_x/**` bereits
   ausdrücklich anerkannt („Die Stilllegung … vermeidet die in Anhang A
   benannte Doppelpflege" [SOURCE: gr-001-governance-decision.md §8]).
   Dieselbe Logik ist auf den `app/host.py`-Cluster **anwendbar** — die
   Entscheidung liegt beim Projekteigner.
3. **Governance-Aufwand im Blick behalten.** **Beobachtung, keine Kritik:**
   das Verhältnis von Governance-/Audit-Dokumentation (~26.300 Zeilen unter
   `docs/`) zu produktivem Code (~12.400 Zeilen) beträgt rund 2:1. Für ein
   sicherheitskritisches, langlebiges System ist ein hoher Anteil begründbar;
   die Zahl gehört dennoch in eine ökonomische Betrachtung. **Es wird keine
   Reduktion empfohlen** — das wäre eine Governance-Entscheidung.

### 27.4 Was **nicht** empfohlen wird

Keine Abkürzung bei Security, Governance, Tests, Simulation, Human Authority
oder Kapitalschutz zugunsten schnellerer Wertschöpfung. Profitabilität ist
Produktziel, nicht Freibrief (TR-02).

---

## 28. Risks

Technische Risiken dieser Analyse. **Keine Governance-Wirkungsstufe**; die
Skala ist rein technisch.

| ID | Risiko | Eintrittspfad | Wirkung | Wahrscheinlichkeit | Gegenmaßnahme | Bezug |
|---|---|---|---|---|---|---|
| **RK-01** | Arbeit in Phase B trifft auf eine ungeklärte ADR-Vertragslage | OD-01 bleibt offen bei SPR-02-Start | Nacharbeit; Widersprüche in AC-Nachweisen | mittel | OD-01 vor Phase B disponieren | Kap. 4.2 |
| **RK-02** | QG-005/QG-008-Nachweise sind gegen den Baseline-Commit nicht führbar, weil normative Eingaben untracked sind und ADR-Fassungen divergieren | Phase D | Gate-Verzögerung | mittel | Nachweisverfahren früh festlegen (Bezug auf Welt B/C ausdrücklich regeln) | SG-01, Kap. 4.4 |
| **RK-03** | Änderungen an `ServiceRegistry` brechen die zwei `_registrations.pop()`-Aufrufstellen | WP-002 | Startfehler, schwer lokalisierbar | mittel | TD-06 vor WP-002-Arbeit sichtbar machen | AM-04 |
| **RK-04** | FR-010 wird als „erfüllt" bewertet, weil die Aktivierungsisolation überzeugt, während Discovery/Events lückenhaft bleiben | SPR-06/SPR-08 | Gate-Scheinbestehen | **hoch** | TG-1 und TG-6 als AC-Nachweis vorsehen | PS-02, REL-01 |
| **RK-05** | Regressionsnachweis wird versehentlich gegen 1.019 statt 258 geführt (oder umgekehrt) | jeder Testlauf ohne Pfadangabe | falscher Gate-Nachweis | **hoch** | Explizite Pfadliste im Nachweisverfahren; `testpaths` disponieren (OD-03) | Kap. 15.5 |
| **RK-06** | `ollama` fehlt in einer sauberen Umgebung → Importfehler in `core/worker.py` | Neuinstallation, CI | Testlauf/Start bricht ab | mittel | OD-06 | AI-02 |
| **RK-07** | Security-Policy bleibt fest verdrahtet; Plugins sind produktiv nicht aktivierbar | Auslieferung ohne OD-05 | Produktfunktion faktisch abgeschaltet | mittel | OD-05 | PS-09, SEC-06 |
| **RK-08** | Nebenläufigkeitsdefekt der Registry manifestiert sich sporadisch | Nebenläufige Auflösung | schwer reproduzierbare Fehler | niedrig | TD-07, TG-7 | Kap. 21.4 |
| **RK-09** | Base64-„Encryption" wird als Schutz missverstanden | Nutzung des Vaults für echte Secrets | Vertraulichkeitsverlust | mittel | TD-20 sichtbar machen; ODD-19 disponieren | SEC-08 |
| **RK-10** | Diese Analyse wird als Autorisierung missverstanden | Rezeption | unautorisierte Arbeit | niedrig | Statuszeile, Kap. 33/34 | — |

---

## 29. Dependencies

### 29.1 Externe Abhängigkeiten

| Abhängigkeit | Deklariert | Genutzt von | Bewertung |
|---|---|---|---|
| `PySide6 >= 6.8` | **ja** | `ui/**`, `app/application.py`, `app/main_window.py`, `core/worker.py`, `sdk/plugin.py` (UIPlugin) | konform |
| `ollama` | **nein** | `core/ai_manager.py` → `core/worker.py` | **TD-03 / OD-06** |
| Standardbibliothek (`tomllib`, `sqlite3`, `importlib`, `threading`, `asyncio`, `fnmatch`, `base64`, `inspect`, `dataclasses`, `enum`) | n. a. | durchgängig | konform |
| `setuptools>=69`, `wheel` (Build) | ja | Build | konform |

### 29.2 Interne Abhängigkeitsrichtung

```
main.py
  └─ app.application ─ app.application_host ─┬─ app.bootstrap ─┬─ core.*
                                             │                 ├─ config, database, plugins, styles
                                             │                 └─ (lazy) sdk.*, app.security.*
                                             ├─ app.startup / app.shutdown / app.errors / app.di
                                             └─ ui.navigation.* ─ (SecurityBootstrapStage, NavigationBootstrapStage)

(nicht referenziert): app.host ─ ai.gateway, ui.foundation_window
(nicht referenziert): core.worker ─ core.ai_manager ─ ollama
```

### 29.3 Governance-Abhängigkeiten der Arbeit

| Arbeit | Hängt ab von |
|---|---|
| Jede Umsetzungsarbeit | Coding Conditions 7–9, RL-05 [SOURCE: Sprint Plan §6] |
| Phase-B-Sprints | EV-D01 (durch SPR-01 erbracht) |
| SPR-08 | Abschluss **aller** sechs Phase-B-Sprints + Baseline-Messreihe (OP-8) |
| SPR-09 | Phase B vollständig inkl. EV-I01 |
| SPR-10 | GV-01..GV-08; GV-08 stützt sich auf GDR-002 |
| Security-ADRs | je ADR separate Projekteigner-Autorisierung [SOURCE: jochen-x-next-authorized-work-assessment.md §7] |

### 29.4 Abhängigkeiten dieser Befunde untereinander

Siehe Kap. 19.5 (Schuldengraph). Kernaussage: **fünf Entscheidungen (OD-01,
OD-02, OD-03, OD-05, OD-07) entlasten 17 der 26 Schuldenpositionen.**

---

## 30. Proposed Changes

> Jede Position ist **PROPOSED CHANGE** — ein Vorschlag zur Prüfung, **keine**
> Anforderung, **keine** Autorisierung, **keine** Planänderung. Vorschläge, die
> den genehmigten Sprint Plan berühren würden, sind als solche gekennzeichnet.

### PC-01 — Fehlerisolation je Manifest in der Discovery

| Feld | Inhalt |
|---|---|
| **Vorschlag** | `PluginLoader.discover()` fängt Parse-/Validierungsfehler **je Manifest** ab, überspringt das betroffene Plugin und meldet es strukturiert; `PluginFailed` trägt den Verzeichnisnamen statt eines leeren Identifiers |
| **Grund** | PS-02 / TD-14 — ein defektes Manifest deaktiviert heute alle Plugins |
| **Evidenz** | plugins/loader.py:50-61; stages_plugin.py:54-59 |
| **Nutzen** | FR-010 im Discovery-Abschnitt erfüllt; FR-006-Diagnose zuordenbar |
| **Risiken** | Verhaltensänderung der Discovery; ein bisher „lauter" Fehler wird leiser — Gegenmaßnahme: Warn-Log + Ereignis je übersprungenem Manifest |
| **Betroffene Arbeit** | **SPR-06 / WP-005** (FR-010), Diagnoseanteil **SPR-04 / WP-003** (FR-006) |
| **Security-Wirkung** | positiv (Verfügbarkeit); keine Abschwächung einer Prüfung |
| **Test-Wirkung** | neuer Test TG-1; RB-1.0 unberührt, Zuwachs über MWB-015 |
| **Governance-Wirkung** | keine — innerhalb des genehmigten FR-Scopes |
| **Sprint-Plan-Berührung** | **keine** |

### PC-02 — Baseline-Messreihe vor Phase B erheben

| Feld | Inhalt |
|---|---|
| **Vorschlag** | Die in IP Anhang B vorgesehene Messreihe **vor** SPR-02 erheben statt erst zu SPR-08 |
| **Grund** | PERF-02 — NFR-004 verlangt einen Vergleich; ein erst nachher erhobener Bezugspunkt kann keine Regression belegen |
| **Evidenz** | Sprint Plan §8 OP-8 („Erhebung zu Beginn der Umsetzung gemäß Anhang B") |
| **Nutzen** | QG-007/NFR-004 wird nachweisbar |
| **Risiken** | keine |
| **Betroffene Arbeit** | Vorbereitung SPR-08 |
| **Sprint-Plan-Berührung** | **keine** — der Plan sieht genau das vor; PC-02 ist eine **Bestätigung mit Terminakzent** |

### PC-03 — `entry_point` bei der Plugin-Klassenauswahl auswerten

| Feld | Inhalt |
|---|---|
| **Vorschlag** | Bei gesetztem `manifest.entry_point` die benannte Klasse verwenden; ohne Angabe das heutige Verhalten beibehalten (rückwärtskompatibel) |
| **Grund** | PS-04 / TD-15 — heute gewinnt die alphabetisch erste konkrete `Plugin`-Subklasse, auch eine importierte |
| **Evidenz** | stages_plugin.py:504-513; plugins/loader.py:26 |
| **Nutzen** | Eindeutigkeit; Beseitigung unbeabsichtigter Klassenauswahl |
| **Risiken** | **Verhaltensänderung der Aktivierung** — mögliche ADR-011-Berührung |
| **Betroffene Arbeit** | keine bestehende WP-Zuordnung |
| **Governance-Wirkung** | **OPEN DECISION** — vor Umsetzung zu prüfen |
| **Sprint-Plan-Berührung** | **ja, potenziell** → als PROPOSED CHANGE geführt, **nicht** eingeplant |

### PC-04 — Identifier-Validierung vor Pfad- und Modulnutzung

| Feld | Inhalt |
|---|---|
| **Vorschlag** | Explizite Zeichensatz-/Formatprüfung von `manifest.identifier` in der Pipeline **vor** `plugin_dir / identifier` und `import_module(identifier)` |
| **Grund** | SEC-03 / TD-18 — Schutz entsteht heute nur als Nebeneffekt |
| **Evidenz** | plugins/loader.py:82; stages_plugin.py:497-501; sdk/manifest.py:233 (SDK besitzt bereits `validate_identifier`) |
| **Nutzen** | Härtung; Konsistenz mit der bereits vorhandenen SDK-Validierung |
| **Risiken** | Manifeste mit ungewöhnlichen Identifiern würden abgelehnt (gewollt) |
| **Security-Wirkung** | positiv, ausschließlich verschärfend |
| **Governance-Wirkung** | **OPEN DECISION** — Security-Härtung ohne FR-Deckung |
| **Sprint-Plan-Berührung** | **keine** WP-Zuordnung vorhanden → PROPOSED CHANGE |

### PC-05 — Reproduzierbarer Verifikationslauf (CI oder dokumentiertes Skript)

| Feld | Inhalt |
|---|---|
| **Vorschlag** | Ein festgelegter, dokumentierter Ausführungspfad für RB-1.0 (exakte 14-Datei-Liste) und optional eine CI-Ausführung |
| **Grund** | RT-08 / TD-09 und RK-05 — Gate-Nachweise sind heute manuell und die Standard-`pytest`-Ausführung misst den falschen Umfang |
| **Evidenz** | pyproject.toml:18; kein CI im Baseline-Inventar |
| **Nutzen** | Reproduzierbarkeit von EV-I01, QG-001, QG-007 |
| **Risiken** | Setzt OD-03 (Packaging) voraus, sonst prüft CI den falschen Baum |
| **Governance-Wirkung** | neue Datei im Repository → Freigabe erforderlich |
| **Sprint-Plan-Berührung** | **keine** WP-Zuordnung → PROPOSED CHANGE |

### PC-06 — Wirkungsgrenze der Integritätsprüfung dokumentieren

| Feld | Inhalt |
|---|---|
| **Vorschlag** | In der SDK-/Architekturdokumentation ausdrücklich festhalten, dass „Integrity Validation" auf der Stufe STRUCTURAL eine **Manifest-Schema-Prüfung** ist und **keine** Aussage über die Unverändertheit des Plugin-Codes trifft |
| **Grund** | SEC-01/TD-17 — Bezeichnung ist gegenüber der Wirkung überzeichnet |
| **Nutzen** | Verhindert falsche Sicherheitsannahmen bei Plugin-Autoren und Betreibern |
| **Risiken** | keine — **reine Dokumentation, kein Codeeingriff** |
| **Betroffene Arbeit** | **SPR-07 / WP-007** (FR-011/FR-012) |
| **Governance-Wirkung** | keine; schließt **keine** ODD |
| **Sprint-Plan-Berührung** | **keine** |

### PC-07 — Platzhalter-Kryptografie sichtbar machen

| Feld | Inhalt |
|---|---|
| **Vorschlag** | Beim Start eine deutliche Warnung protokollieren, wenn `ReversibleEncryptionService` als Default aktiv ist; Benennung/Docstring so schärfen, dass „Encryption" keinen Schutz suggeriert |
| **Grund** | SEC-08 / TD-20 / RK-09 |
| **Evidenz** | encryption_service.py:68-91; security_manager.py:109-111 |
| **Ausdrückliche Beschränkung** | **Es wird kein Kryptoverfahren vorgeschlagen und keines ausgewählt.** ODD-19 bleibt offen und unberührt (**BD-02**) |
| **Risiken** | keine funktionale Änderung |
| **Governance-Wirkung** | keine ODD-Auflösung |
| **Sprint-Plan-Berührung** | **keine** WP-Zuordnung → PROPOSED CHANGE |

### PC-08 — Deterministische Discovery-Reihenfolge

| Feld | Inhalt |
|---|---|
| **Vorschlag** | `sorted(self._directory.glob("*/plugin.toml"))` statt unsortiertem `glob` |
| **Grund** | PS-01 / TD-13 |
| **Nutzen** | Reproduzierbare Logs, Metriken und Ereignisreihenfolgen; stabilere Tests |
| **Risiken** | minimal; die Aktivierungsreihenfolge ist ohnehin topologisch bestimmt |
| **Betroffene Arbeit** | keine WP-Zuordnung → PROPOSED CHANGE (klein) |

### 30.1 Ausdrücklich **nicht** vorgeschlagen

- Keine Architektur-Neuentwürfe aus ästhetischen Gründen (Auftrag Kap. 13).
- Keine Isolationstechnik für Plugins (OD-04/BD-01).
- Keine Kryptografieauswahl (ODD-19/BD-02).
- Keine Auflösung der ADR-Statusdivergenz (OD-01).
- Keine Entfernung, Verschiebung oder Archivierung von `src/jochen_x/**`.
- Keine Änderung von RB-1.0.
- Keine neuen Sprints, Work Packages, Requirements oder Quality Gates.
- Keine Änderung des FROZEN Architecture Book v2.0.

---

## 31. Future Capabilities

Klassifikation gemäß Auftrag Kap. 27. **Keine Position ist automatisch
autorisiert.**

| Fähigkeit | Zweck (quellengedeckt) | Ist-Stand | Klassifikation | Erforderliche Autorität |
|---|---|---|---|---|
| Security-ADRs aus ODD-01..ODD-20 | Technische Konkretisierung des Security Designs | keine | **OPEN** — je ADR einzeln | Projekteigner |
| Security Design R1 (Correction) | SD-W1-F-04, SD-W1-F-06 | zugewiesen, nicht gestartet | **RECOMMENDED** (durch ADW-SD-1.0-002 zugewiesen) | Startfreigabe Projekteigner |
| SA Correction Cycle | SA-W1-F01/F03/F04 | offen | **RECOMMENDED**, geringe Dringlichkeit | Startfreigabe |
| Rangentscheidung Dokumentklassen (GQ-1) | Governance-Hierarchie | offen | **OPEN** | Projekteigner |
| Disposition GC-02..GC-07 / GF-03 (GQ-3) | Governance Conflicts | offen | **OPEN** | Projekteigner |
| Plugin-Isolation | Trust Boundary durchsetzbar machen | keine | **OPEN / NOT AUTHORIZED** | Projekteigner + Security-Governance |
| Kryptografie (ODD-19) | Vertraulichkeit von Secrets/Backups | Platzhalter | **OPEN / NOT AUTHORIZED** | Projekteigner + Security-Governance |
| Audit-Ereigniskatalog (ODD-17) | Auditierbarkeit | teilweise | **OPEN** | Projekteigner |
| Multimodal-Identitätsverfahren (ODD-03) | Identitätsfeststellung | keine | **OPEN / FUTURE** | Projekteigner |
| **KI-Fähigkeit** (Provider, Inferenz, Tools) | CP §8, SA §9/§10, SD §11 | entkoppelter Restbestand | **FUTURE / NOT AUTHORIZED** | Projekteigner + Security-Governance |
| **Memory** | SA §12, SD §13 | nicht vorhanden | **FUTURE / OPEN / NOT AUTHORIZED** | Projekteigner + Security-Governance |
| **Agents** | SA §11, SD §12 | nicht vorhanden | **FUTURE / NOT AUTHORIZED** | Projekteigner + Security-Governance |
| **Automation** | keine Milestone-Quelle | nicht vorhanden | **FUTURE / OPEN** | Projekteigner |
| **Multimodal** | SA §13 | nur Vokabular | **FUTURE / NOT AUTHORIZED** | Projekteigner |
| Trading RESEARCH / SIMULATION / BACKTESTING / PAPER | CP §9, SA §14/§15 | nicht vorhanden | **FUTURE / OPEN** — Stufenmodell ODD-14 zurückgestellt | Projekteigner + Security-Governance |
| **Trading CONTROLLED LIVE** | — | nicht vorhanden | **NOT AUTHORIZED** | — |
| Security Engineering Specification | — | nicht vorhanden | **NOT AUTHORIZED** (Klassenfrage GQ-2 offen) | — |
[Klassifikationsbelege: SOURCE: docs/governance/jochen-x-next-authorized-work-assessment.md §5, §7, §8, §12]

> **FC-01:** Es wurden **keine** Implementierungsdetails für zukünftige
> Fähigkeiten erfunden.

---

## 32. Recommended Engineering Sequence

> **Charakter:** Empfehlung zur Prüfung. Der genehmigte Sprint Plan bleibt die
> maßgebliche Ausführungssequenz. Diese Sequenz ordnet **Entscheidungen** vor
> **Arbeit** — sie fügt keine Arbeit hinzu.

```
STUFE 0 — ENTSCHEIDUNGEN (keine Umsetzung, kein Coding)
  ├─ OD-01  Disposition ADR-005/006/007 + Architecture Book + CLAUDE.md/ROADMAP
  ├─ OD-02  Status app/host.py-Cluster (berührt RB-1.0 bei Option c)
  ├─ OD-03  Packaging-/Werkzeugkonfiguration
  ├─ OD-05  Security-Verdrahtung im Bootstrap
  └─ OD-06  Auslegung NFR-007 für ollama
        │
        ▼
STUFE 1 — EVIDENZ (im Plan vorgesehen, kein Coding)
  └─ OP-8   Baseline-Messreihe gemäß IP Anhang B          [PC-02]
        │
        ▼
STUFE 2 — CODING GATE
  └─ Bedingungen 7–9 / RL-05  ── ohne dieses Gate keine Umsetzung
        │
        ▼
STUFE 3 — PHASE B (genehmigte Sequenz, empfohlene Betonung)
  ├─ SPR-06 WP-005 Reliability   ← früh: FR-010-Lücken berühren EventBus + Loader
  ├─ SPR-02 WP-001 Platform Hardening
  ├─ SPR-03 WP-002 Host Service      ← setzt OD-02 voraus (FR-003)
  ├─ SPR-04 WP-003 Developer Experience
  ├─ SPR-05 WP-004 Observability     ← setzt OTD-1 voraus
  └─ SPR-07 WP-007 Documentation     ← zuletzt abschließen (Planvorgabe)
        │
        ▼
STUFE 4 — SPR-08  Regression + Messreihe → QG-001, QG-007
        ▼
STUFE 5 — SPR-09  WP-006 SDK Contract Verification → QG-003
        ▼
STUFE 6 — SPR-10  Governance Closure → QG-008
        │
        ▼
STUFE 7 — JENSEITS M1.0 (je einzeln zu autorisieren)
  ├─ Security Design R1 / SA Correction Cycle   [RECOMMENDED, zugewiesen]
  ├─ GQ-1, GQ-3 Governance-Entscheidungen        [OPEN]
  ├─ Security-ADRs aus dem ODD-Register          [OPEN, je ADR]
  └─ OD-04 (Isolation), ODD-19 (Kryptografie)    [BLOCKED — BD-01, BD-02]
        │
        ▼
STUFE 8 — PRODUKTFÄHIGKEITEN  [FUTURE / NOT AUTHORIZED]
  KI · Memory · Agents · Automation · Multimodal · Trading (jede Stufe)
```

### 32.1 Begründung der Reihenfolge

| Regel | Begründung |
|---|---|
| Entscheidungen **vor** Arbeit | OD-01 liefert den Vertragstext, OD-02 die Antwort auf „zentral" in FR-003, OD-05 die Wirksamkeit der Security-Policy. Arbeit ohne diese Entscheidungen erzeugt Nacharbeit (RK-01) |
| Messreihe **vor** Änderungen | Ein Vergleichspunkt nach der Änderung belegt keine Regression (PERF-02) |
| Coding Gate **vor** jeder Umsetzung | Verbindlich, nicht verhandelbar [SOURCE: Sprint Plan §6] |
| Reliability **früh** in Phase B | FR-010-Lücken liegen in `EventBus` und `PluginLoader` — Komponenten, auf denen WP-002 und WP-004 aufsetzen |
| Dokumentation **zuletzt** | Planvorgabe (SPR-07 setzt Endstand WP-002/WP-004 voraus) |
| Produktfähigkeiten **nach** Isolation | Feststellung aus SEC-04/AG-01, **keine** vom Verfasser gesetzte Bedingung |

---

## 33. STOP / BLOCKED DECISION Register

### 33.1 HARD-STOP-Prüfung

| # | Bedingung (Auftrag Kap. 26) | Eingetreten? |
|---|---|---|
| 1 | Pflichtquelle fehlt und ist nicht verifizierbar | **NEIN** — alle 16 vorhanden (Kap. 2.2) |
| 2 | Baseline-Commit nicht reproduzierbar/verifizierbar | **NEIN** — verifiziert und RB-1.0 reproduziert (Kap. 3) |
| 3 | Analyse erfordert Änderung einer bestehenden Datei | **NEIN** — keine bestehende Datei geändert |
| 4 | Analyse erfordert Implementierung | **NEIN** |
| 5 | Governance-/Architekturentscheidung wäre zur Dokumentation zwingend zu treffen | **NEIN** — alle strittigen Punkte konnten als OPEN DECISION bzw. BLOCKED DECISION dokumentiert werden, **ohne** sie zu entscheiden |

> **KEIN HARD STOP. Die Analyse wurde vollständig durchgeführt.**

### 33.2 Blocked Decisions

| ID | Gegenstand | Warum blockiert | Was **nicht** getan wurde | Erforderliche Autorität |
|---|---|---|---|---|
| **BD-01** | Plugin-Isolationsstrategie (OD-04) | Security-Architekturentscheidung; ADR-009 und das ODD-Register sind offen; neue ADRs sind ausdrücklich nicht autorisiert [SOURCE: jochen-x-next-authorized-work-assessment.md §5 E, §7] | **Keine** Isolationstechnik vorgeschlagen; **keine** Optionsliste gebildet (Optionsbildung wäre bereits Architekturarbeit); **keine** neue Trust-Taxonomie | Projekteigner + Security-Governance, ADR-pflichtig |
| **BD-02** | Kryptografieverfahren für Vault/Backups (ODD-19) | ODD-19 ist offen; ODDs sind Designentscheidungen, ausdrücklich **nicht** über Correction Cycles zu behandeln [SOURCE: ebd. §9] | **Kein** Verfahren ausgewählt oder empfohlen; PC-07 beschränkt sich auf Sichtbarmachung | Projekteigner + Security-Governance |
| **BD-03** | Statusdivergenz ADR-005/006/007 und Architecture Book zwischen Welt A und Welt B (OD-01) | Der Baseline Commit Record hat die Disposition ausdrücklich dem Projekteigner vorbehalten [SOURCE: milestone-1.0-baseline-commit-record.md §15 Nr. 4] | Die Divergenz wurde **dokumentiert, nicht aufgelöst**; **keine** Behauptung über den Genehmigungsstand am Baseline; **keine** Datei geändert | Projekteigner / Governance Architect |
| **BD-04** | Auslegung von NFR-007 gegenüber vorbestehenden Abhängigkeiten (OD-06) | Auslegung einer genehmigten Anforderung | **Keine** Auslegung vorgenommen; beide Lesarten dargestellt | Projekteigner |
| **BD-05** | Event-Zustellsemantik bei Handler-Ausnahmen (OD-07) | Berührt ADR-002 (genehmigt) | **Keine** Semantikänderung vorgeschlagen; Verortung in WP-005 benannt | Architektur-Governance |
| **BD-06** | Behandlung des `app/host.py`-Clusters (OD-02) | GDR-002 entscheidet ausdrücklich keine andere Governance-Frage | **Keine** Entscheidung; Optionen (a)/(b)/(c) aus der GDR-002-Systematik übernommen, **nicht** erfunden | Projekteigner / Governance Architect |

### 33.3 Bewusst **nicht** berührte offene Punkte

Diese Analyse hat **keinen** der folgenden Punkte geschlossen, verändert,
neu bewertet oder ausgelegt:

SD-W1-F-04 · SD-W1-F-06 · SA-W1-F01 · SA-W1-F03 · SA-W1-F04 ·
ODD-01–ODD-20 · GF-02/GC-01 · GF-03/GC-02 · GC-03–GC-07 · GQ-1 · GQ-2 ·
GQ-3 · WAIVER-DEV-001 §9 (3) · R2-E-01 · OP-1..OP-8 · OTD-1 · OTD-2 ·
GR-001 (bereits durch GDR-002 entschieden) · F-SPR01-01 (bereits CLOSED) ·
F-SPR01-02.

---

## 34. Final Assessment

### 34.1 Zustandsurteil

**JOCHEN X ist am autoritativen Baseline eine solide, sorgfältig gebaute
Plattform mit einer klaren Schichtarchitektur, einem reifen SDK und einer
funktionierenden, in der Reihenfolge korrekt implementierten
Plugin-Sicherheitspipeline — und mit drei klar abgrenzbaren Schuldenclustern,
die jeweils auf eine einzige, ausstehende Entscheidung zurückgehen.**

Die Codequalität liegt über dem, was die Dokumentation vermuten lässt: Die
Bootstrap-Invarianten sind **vollständig** eingehalten, die
Dependency-Resolution ist vorbildlich deterministisch, und die
Fehlerbehandlung in Start, Aktivierung und Shutdown ist durchdacht. Umgekehrt
liegt die tatsächliche Sicherheitswirkung **unter** dem, was die Benennungen
(„Integrity Validation", „EncryptionService", „Permission Enforcement")
suggerieren — durchweg quellengedeckt zurückgestellt, aber eben nicht durchweg
so benannt.

### 34.2 Antworten auf die Prüffragen aus Auftrag Kap. 31

| Frage | Antwort |
|---|---|
| Verbessert dieser Plan das tatsächliche Endprodukt? | **Ja** — er macht fünf entscheidungsreife Blockaden sichtbar, deren Klärung 17 von 26 Schuldenpositionen entlastet |
| Bewahrt er Security? | **Ja** — alle Vorschläge sind verschärfend oder rein dokumentarisch; keiner schwächt eine Prüfung |
| Zuverlässigkeit? | **Ja** — die drei belegten Isolationslücken sind benannt und im genehmigten WP-005 verortet |
| Wartbarkeit? | **Ja** — die Schulden sind zu Clustern mit gemeinsamer Ursache zusammengefasst |
| Architektur? | **Ja** — es wird keine neue Architektur vorgeschlagen; alle Befunde messen gegen die genehmigte |
| Governance? | **Ja** — jede strittige Position ist als OPEN oder BLOCKED DECISION geführt, keine wurde entschieden |
| Bedienbarkeit? | **Neutral** — bis auf den Hinweis, dass das Referenz-Plugin mit der Default-Konfiguration nicht aktiviert wird |
| Performance? | **Neutral** — keine Optimierung vorgeschlagen; die fehlende Messgrundlage ist als UNKNOWN benannt |
| Langfristiger ökonomischer Wert? | **Ja** — Auslieferbarkeit (OD-03) ist als höchster Hebel identifiziert |
| Führt er unnötige Komplexität ein? | **Nein** — kein Vorschlag fügt eine Abstraktion hinzu; PC-01/PC-04/PC-08 sind lokale Härtungen |
| Erzeugt er technische Schulden? | **Nein** |
| Erzeugt er Lock-in? | **Nein** |
| Erzeugt er Security-Verbindlichkeiten? | **Nein** — es wird keine Sicherheitszusage gegeben |
| Erzeugt er versehentlich eine **zweite Architektur**? | **Nein** — Kap. 22 übernimmt ausschließlich den ES-Zielzustand |
| Erzeugt er versehentlich eine **zweite Roadmap**? | **Nein** — Kap. 23/32 übernehmen die genehmigte Sequenz; Abweichungen sind als PROPOSED CHANGE markiert |
| Erzeugt er versehentlich eine **zweite Governance-Ebene**? | **Nein** — keine neue Regel, keine neue Dokumentklasse, keine neue Rangstufe, keine neue Wirkungsstufe (Kap. 19 Vorbemerkung) |

### 34.3 Verbleibende Ehrlichkeitsvorbehalte

1. **Die Analyse ist statisch.** Es wurde **kein** Testlauf und **keine**
   Laufzeitmessung durchgeführt. Die Pass-Zahl 258/258 ist übernommene Evidenz
   aus dem Baseline Commit Record, keine eigene Messung. Alle
   Performance-Aussagen sind INFERRED oder UNKNOWN.
2. **Der Implementation Plan 1.0 (5.919 Zeilen) wurde selektiv gelesen** —
   Kapitel 3.1, 5.5.4 und 11.10 überwiegend über Sekundärquellen (GDR-002,
   SPR-01, Sprint Plan). Für die getroffenen Aussagen reicht das; eine
   vollständige Durchsicht könnte weitere Bezüge ergeben.
3. **Die Security-Dokumente (SA 1.0, SD 1.0, CP 1.0 — zusammen 3.812 Zeilen)
   wurden strukturell und selektiv gelesen**, nicht vollständig. Die
   Security-Befunde in Kap. 10 stützen sich primär auf Code und auf die
   Bootstrap Baseline; sie sind **keine** vollständige Prüfung gegen SA/SD.
4. **`app/concurrency.py`, `core/scheduler.py`, `core/lifecycle.py`,
   `core/performance.py`, `developer/**`, `ui/navigation/**` (17 Module) und
   `sdk/*` wurden auf Signaturebene, nicht zeilenweise geprüft.** Dort können
   weitere Befunde liegen.
5. **Die 66 Dateien unter `src/jochen_x/**` wurden nicht analysiert** — gemäß
   GDR-002 D-2 und Auftrag Kap. 6.

### 34.4 Abschließende Feststellungen

> **Es wurde keine Implementierung durchgeführt.**
> **Es wurde keine bestehende Datei geändert** — weder Code noch Tests noch
> Dokumentation noch Governance- oder Architekturartefakte.
> **Es wurde genau eine Datei erstellt:** dieses Dokument.
> **Es wurde kein ADR und keine Spezifikation erstellt.**
> **Es wurde kein Commit, kein Tag und kein Push durchgeführt.**
> **Der Working Tree wurde nicht bereinigt.**
> **RB-1.0 wurde nicht verändert.**
> **`src/jochen_x/**` wurde nicht reaktiviert, migriert, verändert oder gelöscht.**
> **Es wurde keine Governance-Entscheidung, keine Architekturentscheidung und
> keine Security-Entscheidung getroffen.**
> **Es wurde keine Coding-Autorisierung erzeugt und keine aus diesem Dokument
> abgeleitet.**
>
> **CODING = NOT AUTHORIZED.**

### 34.5 Nächster Schritt

Der Projekteigner entscheidet über den nächsten konkreten Arbeitsschritt. Diese
Analyse empfiehlt zur Prüfung die Stufe-0-Entscheidungen aus Kap. 32
(OD-01, OD-02, OD-03, OD-05, OD-06) — **als Empfehlung, nicht als Vorbedingung
und ohne jede Autorisierungswirkung.** Es besteht kein automatischer
Folgeauftrag.

---

**Ende JOCHEN X — Master Engineering Plan (DRAFT, R0, NON-NORMATIVE) —
Baseline: `MILESTONE-1.0-BASELINE = 8fcf42f1997dfcf6ff232e75fd33c37b933991c8`**
