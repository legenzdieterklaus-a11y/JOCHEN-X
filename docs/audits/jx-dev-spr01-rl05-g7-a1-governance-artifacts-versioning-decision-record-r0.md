# JOCHEN X — Milestone 1.0
# JX-DEV-SPR01-RL05-G7-A1-GOV-ARTIFACTS-VERSIONING-DEC-01-R0 — Human Decision Record
## Versionierung der Governance-Artefakte AR-1 / AR-2 / AR-3

> **COMPLETED — DECISION ONLY · NO EXECUTION**
>
> Dieses Dokument zeichnet die **Human-Entscheidung des Projekteigners** zu
> **E-1**, **E-2/E-5**, **E-3** und **E-4** auf. Grundlage ist
> `GOV-ARTIFACTS-PREP-01`.
>
> **Kein `git add`. Kein Commit. Kein Push. Keine der drei Dateien
> verändert.** `7c7a572` bleibt unangetastet.
>
> **SPVERS = EXECUTED (`7c7a572`)** · **Sprint Plan = TRACKED** ·
> **A1-EXEC = VERIFIED** · **U-4′ = UNDETERMINED** · **G7-b = OPEN** ·
> **Bedingung 7 = NOT FULFILLED** · **HD-2 = DEFERRED / OPEN** ·
> **RL-05 = NOT REACHED** · **CODING = NOT AUTHORIZED** ·
> **QG-006 = NOT STARTED**

---

## 1. Baseline Gate

| Prüfung | Ergebnis |
|---|---|
| **HEAD** | `7c7a572ba3633d9666ff79d01d9d98620a3e6e0e` = `7c7a572` — „docs: version sprint plan" — **exakt wie erwartet** |
| Staging vor Beginn | **leer** |
| **SPVERS-EXEC-01** | **EXECUTED / VERIFIED**, Commit `7c7a572` |
| **Sprint Plan** | `docs/milestone-1.0-sprint-plan.md` — **tracked** · `APPROVED FOR SPRINT EXECUTION PLANNING (ADW-SPR-1.0-001)` · `1.0` / `R0` / `2026-08-09` |
| Vorbestehende Working-Tree-Modifikationen | `CLAUDE.md` · `ROADMAP.md` · `docs/architecture-book-v2.md` — **unverändert, unangetastet, nicht committet** |
| Bezugs-Baseline | `MILESTONE-1.0-BASELINE = 8fcf42f1997dfcf6ff232e75fd33c37b933991c8` (GDR-003) |

**Baseline Gate: PASS.**

---

## 2. Source Gate (readonly)

Ausschließlich die bereits geprüfte Quellenlage. **Keine neue materielle
Governance-Frage aus angrenzenden Themen abgeleitet.**

| # | Quelle | Verwendung |
|---|---|---|
| 1 | **GDR-003** — `docs/governance/milestone-1.0-baseline-identifier-decision.md` Z. 84, 88, 137 | Commit-2+-Scope, „optional", „separate Governance-Entscheidung" |
| 2 | **SPVERS-PREP-01** (= AR-3) | Optionsraum-Vorlauf |
| 3 | **SPVERS-DEC-01** (`4ac6c11`) | V2-Entscheidung, Referenz auf AR-3 |
| 4 | **SPVERS-EXEC-PREP** (= AR-1) | Ausführungsvorbereitung |
| 5 | **SPVERS-Z12-DEC-01** (= AR-2) | V2-f / R-2 (Sprint-Plan-EXEC) |
| 6 | **GOV-ARTIFACTS-PREP-01** | Dateistatus, Optionsraum O-1…O-4, Entscheidungsbedarf E-1…E-5 |
| 7 | **Repository-Konventionen** — Development Standard v1.1 §C; `CLAUDE.md` | Commit-Message-**Format** |

**Nicht behandelt und vollständig unberührt:** U-4′ · G7-b · Bedingung 7 ·
HD-2 · RL-05 · Coding · QG-006 · OD-05 · ADR-012.

**Source Gate: PASS.**

---

## 3. Status AR-1 / AR-2 / AR-3 (readonly, in dieser Welle reproduziert)

| Merkmal | **AR-1** | **AR-2** | **AR-3** |
|---|---|---|---|
| Pfad | `docs/audits/jx-dev-spr01-rl05-g7-a1-sprint-plan-versioning-exec-prep-r0.md` | `docs/audits/jx-dev-spr01-rl05-g7-a1-sprint-plan-versioning-z12-decision-record-r0.md` | `docs/audits/jx-dev-spr01-rl05-g7-a1-sprint-plan-versioning-prep-r0.md` |
| Bezeichnung | SPVERS-EXEC-PREP-01 | SPVERS-Z12-DEC-01 | SPVERS-PREP-01 |
| Git-Status | **`??` untracked** | **`??` untracked** | **`??` untracked** |
| Zeilen | **384** | **363** | **456** |
| **Blob-SHA** | **`1cbd728e25103c719d69e0059dca94e98da3555a`** | **`a7a48d8aba45587773f5fc8ac3c63a9b83d59349`** | **`0b16ed0eb1fc2c311f0885f9d43dffed35b90e91`** |
| `git log --all` | 0 Einträge | 0 Einträge | 0 Einträge |
| Inhalt abgeschlossen | **JA** (R0, COMPLETED) | **JA** (R0, COMPLETED) | **JA** (R0, COMPLETED) |

Alles **FACT**, direkt erhoben. **Keine Datei verändert.**

---

## 4. HUMAN DECISION

```text
JX-DEV-SPR01-RL05-G7-A1-GOV-ARTIFACTS-VERSIONING-DEC-01-R0

Authority:  Projekteigner / Governance
Date:       2026-08-13
Baseline:   HEAD 7c7a572

--- E-1  VERSIONIERUNG ---

    E1-B — JA

Die Versionierung der ungetrackten Governance-Artefakte wird
ausdruecklich autorisiert.

NICHT gewaehlt: E1-A.

--- E-2 / E-5  UMFANG ---

    O-4 — AR-1 + AR-2 + AR-3

Alle drei ungetrackten Artefakte der SPVERS-Kette.

NICHT gewaehlt: O-1, O-2, O-3.

Diese Wahl ist eine ausdrueckliche Festlegung. Sie wurde NICHT
abgeleitet aus:
    - der Tatsache, dass AR-3 von SPVERS-DEC-01 zitiert wird,
    - dem Umstand, dass alle uebrigen Kettenartefakte getrackt sind,
    - allgemeiner Git-Praxis.

--- E-3  COMMIT MESSAGE ---

Exakter Wortlaut:

    docs: version spvers governance artifacts

Exakt zu uebernehmen. Keine Umformulierung. Keine Ergaenzung.
Kein Scope. Kein Body.

--- E-4  BEGLEIT-RECORD ---

    E4-A — KEIN zusaetzliches Begleit-/Versionierungs-Record

Der spaetere EXEC erzeugt kein weiteres Artefakt.

Die R-2-Entscheidung aus SPVERS-Z12-DEC-01 betraf ausschliesslich
den Sprint-Plan-EXEC und wurde NICHT uebertragen; E4-A ist eine
eigenstaendige Entscheidung fuer diesen Vorgang.

NICHT gewaehlt: E4-B.
```

### 4.1 Zeichenspezifikation der Commit Message

| Merkmal | Festlegung |
|---|---|
| **Exakter Wortlaut** | `docs: version spvers governance artifacts` |
| Typ | `docs` — zulässiger Typ (Development Standard v1.1 §C) |
| Scope | **keiner** |
| Body / Trailer | **keiner** |
| Zeichensatz | reines ASCII, Kleinschreibung, ein Doppelpunkt, einfache Leerzeichen |
| Abweichung zulässig? | **NEIN** — jede Abweichung erfordert eine neue Human Decision |

---

## 5. Change Surface des späteren EXEC

**Genau drei Dateien, ein Commit:**

| # | Pfad | Soll-Blob |
|---|---|---|
| CS-1 | `docs/audits/jx-dev-spr01-rl05-g7-a1-sprint-plan-versioning-exec-prep-r0.md` | `1cbd728e25103c719d69e0059dca94e98da3555a` |
| CS-2 | `docs/audits/jx-dev-spr01-rl05-g7-a1-sprint-plan-versioning-z12-decision-record-r0.md` | `a7a48d8aba45587773f5fc8ac3c63a9b83d59349` |
| CS-3 | `docs/audits/jx-dev-spr01-rl05-g7-a1-sprint-plan-versioning-prep-r0.md` | `0b16ed0eb1fc2c311f0885f9d43dffed35b90e91` |

**Ausdrücklich ausgeschlossen:** `CLAUDE.md` · `ROADMAP.md` ·
`docs/architecture-book-v2.md` · **jede** Datei unter `docs/audits/*`
außerhalb CS-1…CS-3 · OD-05 · ADR-012 · ADRs · RDRs · Architecture Book ·
Implementation Plan · Code · Tests · Config · sonstige Governance-Dateien.

**Verboten im späteren EXEC:**

```text
git add .
git add -A
git add -u
git commit -a
```

Staging ausschließlich über die drei vollständigen, expliziten Pfade.
Vor dem Commit zwingend `git diff --cached --name-only` → **genau drei
Zeilen**, keine weitere. Staged Blobs gegen CS-1…CS-3 prüfen.

### 5.1 Inhaltsidentität

Die drei Artefakte werden **byte-/inhaltstreu als Bestand** aufgenommen.
Keine Redaktion, Formatierung, Bereinigung, Ergänzung oder Zeilenänderung.
Vorzustand = Sollzustand nach Versionierung.

---

## 6. Trennung zu SPVERS-EXEC-01

| Vorgang | Status |
|---|---|
| **SPVERS-EXEC-01** | Sprint Plan versioniert · Commit **`7c7a572`** · abgeschlossen · verifiziert · **durch diese Decision nicht verändert** |
| **Dieser Gegenstand** | Versionierung der Governance-Artefakte AR-1/AR-2/AR-3 — **eigener, separater Vorgang** |

```text
7c7a572 bleibt unangetastet.
Der bereits versionierte Sprint Plan bleibt unangetastet.
Diese Entscheidung autorisiert KEINE Aenderung am Sprint Plan.
KEIN amend. KEIN reset. KEIN rebase. KEIN force push.
```

Ein späterer EXEC wäre ein **zusätzlicher, eigener Commit**.

---

## 7. FACT / NORM / HUMAN DECISION / UNKNOWN / INFERENCE

### FACT
1. AR-1/AR-2/AR-3 sind untracked, nie versioniert (`git log --all` = 0), nicht gitignored.
2. Blob-SHAs, Zeilenzahlen und Pfade gemäß Kap. 3.
3. Alle drei Artefakte stammen aus abgeschlossenen Wellen dieser Kette (R0, COMPLETED).
4. `SPVERS-DEC-01` (`4ac6c11`) referenziert AR-3 in seinem Source Gate.
5. SPVERS-EXEC-01 ist abgeschlossen und verifiziert (`7c7a572`).

### NORM
1. **GDR-003 Z. 88 / Z. 137:** Die Versionierung des Governance-/Doku-Bestands ist ein **separater, ausdrücklich optionaler** Commit-Scope, der eine **separate Governance-Entscheidung** verlangt. Diese Decision ist genau diese Entscheidung.
2. **Development Standard v1.1 §C:** Commit-Message-**Format** `<type>(<scope>): <description>` mit den Typen `feat|fix|docs|refactor|test|chore`.

### HUMAN DECISION
1. **E-1 = E1-B** — Versionierung autorisiert.
2. **E-2/E-5 = O-4** — AR-1 + AR-2 + AR-3, ein Commit.
3. **E-3** — exakter Wortlaut `docs: version spvers governance artifacts`.
4. **E-4 = E4-A** — kein Begleit-Record.

Alle vier sind **Willensakte**, nicht Ableitungen. Die Quellen tragen jede der
Optionen gleichermaßen; **O-3 / E1-A wäre ebenso zulässig gewesen**.

### UNKNOWN
1. Kein Quellensatz **verlangt** die Versionierung — Negativbefund, unverändert.
2. Kein Quellensatz **untersagt** sie — Negativbefund, unverändert.
3. Kein Quellensatz normiert einen **Commit-Message-Wortlaut** — E-3 schließt dies durch Festlegung, nicht durch Ableitung.
4. Behandlung des weiteren GDR-003-Scopes 7.2/7.3/7.4 (53 + weitere vorbestehende untracked Dokumente) — **nicht Gegenstand, nicht entschieden**.
5. Behandlung von `GOV-ARTIFACTS-PREP-01` und **dieses Records** selbst — siehe Kap. 8.2.

### INFERENCE — **nicht als Norm verwendet**
1. „AR-3 wird von einem committeten Record zitiert ⇒ AR-3 muss versioniert werden."
2. „Alle übrigen Kettenartefakte sind getrackt ⇒ diese auch."
3. „Allgemeine Git-Praxis verlangt Versionierung."
4. „R-2 aus SPVERS-Z12-DEC-01 gilt analog für AR-1/AR-2/AR-3."

Keine dieser Aussagen trägt eine der vier Entscheidungen.

---

## 8. Auswirkungen auf den späteren EXEC

### 8.1 Bestimmtheitsgrad

| Punkt | Status nach dieser Decision |
|---|---|
| Ob versioniert wird | **DECIDED** (E1-B) |
| Welche Dateien | **DECIDED** (O-4 → CS-1…CS-3) |
| Inhaltsidentität | **DECIDED** (Kap. 5.1) |
| Commit Message | **DECIDED** (Kap. 4.1) |
| Anzahl Commits | **DECIDED** — genau **einer** |
| Begleit-Record | **DECIDED** (E4-A — keiner) |
| Staging-Verfahren / Schutzmaßnahmen | **bestimmt** (Kap. 5) |
| Nachweisführung | GOV-ARTIFACTS-PREP-01 · dieses Record · Preflight · Staging-Nachweis · Commit-Hash · Post-Commit-Verifikation im Abschlussbericht |
| **EXEC-Auftrag** | **NOT AUTHORIZED** — separate Welle |

> **Der spätere EXEC ist damit inhaltlich vollständig bestimmt.** Es fehlt
> ausschließlich der **Auftrag**.

### 8.2 Fortbestehender Befund — **nicht entschieden**

**FACT:** `GOV-ARTIFACTS-PREP-01` ist untracked. Dieses Decision Record wird
gemäß Auftrag Kap. 12 **nicht committet** und bleibt ebenfalls untracked.

**Folge:** Nach einem EXEC nach O-4 wären AR-1/AR-2/AR-3 versioniert, während
`GOV-ARTIFACTS-PREP-01` und dieses Record **unversioniert** blieben — dieselbe
Konstellation, die zu dieser Welle geführt hat, auf der nächsten Ebene.

> **Ausdrücklich nicht entschieden und nicht in die Change Surface
> aufgenommen.** Reine Registrierung, damit der Umstand nicht unbemerkt bleibt.
> Jede Behandlung bedürfte einer **eigenen** Human Decision.

---

## 9. Explicit Non-Decisions

```text
Keine der drei Dateien veraendert, geloescht oder umbenannt.
Kein git add. Kein Commit. Kein Push. Kein PR, Merge, Tag.
Kein amend / reset / rebase / force push — 7c7a572 unberuehrt.
Sprint Plan: NICHT veraendert, NICHT erneut versioniert.
SPVERS-EXEC-01: NICHT veraendert, NICHT neu bewertet.
Bestehende Governance-Artefakte: NICHT ueberschrieben, nur gelesen.
Weiterer GDR-003-Scope 7.2/7.3/7.4: NICHT entschieden.
GOV-ARTIFACTS-PREP-01 und dieses Record: NICHT entschieden (Kap. 8.2).
U-4': NICHT behandelt — UNDETERMINED.
G7-b: NICHT behandelt — OPEN. G7-a: NICHT beruehrt.
Bedingung 7: NICHT bewertet — NOT FULFILLED; ACN-09 gewahrt.
HD-2: NICHT behandelt — DEFERRED / OPEN.
OP-1 / OP-2: NICHT beruehrt.
OD-05 / ADR-012 / ADRs / RDRs / Architecture Book / Implementation Plan /
      CLAUDE.md / ROADMAP.md / Code / Tests / Config: UNVERAENDERT.
RL-05: NOT REACHED. Coding: NOT AUTHORIZED. QG-006: NOT STARTED.
EXEC: NICHT autorisiert, NICHT ausgefuehrt.
```

---

## 10. Change Surface dieser Welle

| Gegenstand | Umfang |
|---|---|
| Neue Dateien | **genau eine** — `docs/audits/jx-dev-spr01-rl05-g7-a1-governance-artifacts-versioning-decision-record-r0.md` |
| Geänderte / gelöschte Dateien | **keine** |
| AR-1 / AR-2 / AR-3 | **nur gelesen** — Blob-SHAs unverändert |
| Sprint Plan · `7c7a572` | **nicht berührt** |
| Vorbestehende Working-Tree-Änderungen | **UNANGETASTET** |
| `git add` / Commit / Push | **NICHT AUSGEFÜHRT** |

---

## 11. Governance State

| Position | Status |
|---|---|
| **Versionierung AR-1/AR-2/AR-3** | **DECIDED — E1-B / O-4 / E4-A** · **EXEC NOT AUTHORIZED** |
| **SPVERS** | **EXECUTED** · Commit `7c7a572` |
| **Sprint Plan** | **TRACKED** · `APPROVED FOR SPRINT EXECUTION PLANNING (ADW-SPR-1.0-001)` · `1.0` / `R0` / `2026-08-09` |
| **A1-EXEC** | **VERIFIED** |
| **U-4′** | **UNDETERMINED** |
| **G7-a / G7-b** | **PHYSICALLY ADDRESSED** / **OPEN** |
| **Bedingung 7** | **NOT FULFILLED** |
| **HD-2** | **DEFERRED / OPEN** |
| **OP-1 / OP-2** | **OFFEN** / **NICHT ERFÜLLT** |
| **RL-05 / CODING / QG-006** | **NOT REACHED** / **NOT AUTHORIZED** / **NOT STARTED** |
| **OD-05 / ADR-012 / ADRs / RDRs / Architecture Book / IP / `CLAUDE.md` / `ROADMAP.md` / Code / Tests / Config** | **UNVERÄNDERT** |

Keine dieser Positionen wurde durch diese Decision verändert — außer der
erstgenannten, die Gegenstand der Entscheidung ist.

---

## 12. STOP

> **Nach diesem Artefakt: STOP.**
>
> Kein automatischer EXEC · kein `git add` · kein Commit der
> Governance-Artefakte · kein Push · keine weitere Governance-Entscheidung ·
> keine Bewertung von U-4′, G7-b oder Bedingung 7.
>
> **Nächster zulässiger Schritt:** separat zu beauftragender
> `JX-DEV-SPR01-RL05-G7-A1-GOV-ARTIFACTS-EXEC-01-R0`, gebunden an Kap. 4 und 5.

---

## 13. Revision History

| Revision | Datum | Änderung | Status |
|---|---|---|---|
| **R0** | 2026-08-13 | Human Decision zur Versionierung der Governance-Artefakte: **E-1 = E1-B**, **E-2/E-5 = O-4** (AR-1 + AR-2 + AR-3), **E-3** = `docs: version spvers governance artifacts`, **E-4 = E4-A**; Baseline gegen HEAD `7c7a572`, Source Gate, Status mit reproduzierten Blob-SHAs, Change Surface CS-1…CS-3 mit Soll-Blobs, Trennung zu SPVERS-EXEC-01, FACT/NORM/HUMAN-DECISION/UNKNOWN/INFERENCE, fortbestehender Befund Kap. 8.2 | **COMPLETED — DECISION ONLY** |

---

**Ende JX-DEV-SPR01-RL05-G7-A1-GOV-ARTIFACTS-VERSIONING-DEC-01-R0 —
Human Decision Record — JOCHEN X Milestone 1.0 (2026-08-13) — HEAD `7c7a572` —
Bezugs-Baseline `MILESTONE-1.0-BASELINE = 8fcf42f1997dfcf6ff232e75fd33c37b933991c8`**
