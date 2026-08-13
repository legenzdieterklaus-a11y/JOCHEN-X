# JOCHEN X — Milestone 1.0
# JX-DEV-SPR01-RL05-G7-A1-SPVERS-Z12-DEC-01-R0 — Human Decision Record
## V2-f (Commit Message) und R-2 (Begleit-Record) für den SPVERS-V2-EXEC

> **COMPLETED — DECISION ONLY · NO EXECUTION**
>
> Dieses Dokument entscheidet **ausschließlich** die beiden nach
> `SPVERS-EXEC-PREP-01` und `SPVERS-EXEC-REVIEW-01` verbliebenen offenen
> Punkte **V2-f** und **R-2**. Die Entscheidung **V2 — ERSTMALIG
> VERSIONIEREN** (`SPVERS-DEC-01`, Commit `4ac6c11`) wird **nicht erneut
> entschieden**.
>
> **Kein `git add` des Sprint Plans. Kein Commit des Sprint Plans. Kein
> Push. Keine Bestandsdatei verändert.**
>
> **SPVERS: V2 DECIDED · EXEC NOCH NICHT AUSGEFÜHRT** ·
> **A1-EXEC = VERIFIED** · **U-4′ = UNDETERMINED** · **G7-b = OPEN** ·
> **Bedingung 7 = NOT FULFILLED** · **HD-2 = DEFERRED / OPEN** ·
> **RL-05 = NOT REACHED** · **CODING = NOT AUTHORIZED** ·
> **QG-006 = NOT STARTED**

---

## 1. Baseline Gate

| Prüfung | Ergebnis |
|---|---|
| **HEAD** | `4ac6c11cbb93570338478e6371a551c7a34e6590` = `4ac6c11` — „docs: record sprint plan versioning decision" — **exakt wie erwartet** |
| Staging vor Beginn | **leer** |
| Vorgelagerte Entscheidung | **SPVERS-DEC-01** (`4ac6c11`) — **V2 — ERSTMALIG VERSIONIEREN** |
| A1-EXEC / A1-VERIFY | **VERIFIED** / **READ-ONLY VERIFIED** |
| SPVERS-EXEC-PREP | vorhanden (`docs/audits/jx-dev-spr01-rl05-g7-a1-sprint-plan-versioning-exec-prep-r0.md`), reviewed |
| **Sprint Plan — Status** | `APPROVED FOR SPRINT EXECUTION PLANNING (ADW-SPR-1.0-001)` · Version `1.0` · Revision `R0` · Datum `2026-08-09` |
| **Sprint Plan — Git** | **ungetrackt** (`?? docs/milestone-1.0-sprint-plan.md`) · **324 Zeilen** · **Blob-SHA `18ffa1770ae87df45ba447bc47ef920864ddb2cd`** — direkt reproduziert |
| Vorbestehende Working-Tree-Modifikationen | `CLAUDE.md` · `ROADMAP.md` · `docs/architecture-book-v2.md` — **unverändert, unangetastet** |
| Bezugs-Baseline | `MILESTONE-1.0-BASELINE = 8fcf42f1997dfcf6ff232e75fd33c37b933991c8` (GDR-003) |

**Baseline Gate: PASS.**

---

## 2. Bereits entschieden — nicht Gegenstand dieser Welle

| Position | Status |
|---|---|
| **V2 — ERSTMALIG VERSIONIEREN** | **DECIDED** (`SPVERS-DEC-01`) — **nicht erneut entschieden** |
| Inhalt des Sprint Plans | **nicht erneut entschieden** |
| A1-EXEC | **nicht erneut ausgeführt** |
| U-4′ | **nicht ausgelegt** — UNDETERMINED |
| G7-b | **nicht entschieden** — OPEN |
| HD-2 | **nicht wiedervorgelegt** — DEFERRED / OPEN |
| Bedingung 7 | **nicht bewertet** — NOT FULFILLED |
| CODING / RL-05 | **NOT AUTHORIZED** / **NOT REACHED** |

---

## 3. Quellenlage zu V2-f

| # | Prüfpunkt | Befund | Klasse |
|---|---|---|---|
| F-1 | Existiert eine Commit-Message-Konvention? | **JA** — `<type>(<scope>): <description>` mit `feat`, `fix`, `docs`, `refactor`, `test`, `chore` (Development Standard v1.1 §C; identisch `CLAUDE.md`) | **NORM** |
| F-2 | Normiert eine Quelle einen **exakten Wortlaut** für die Erstversionierung des Sprint Plans? | **NEIN** | **UNKNOWN (Negativbefund)** |
| F-3 | Ist die DEC-01-Message ein normativer Wert? | **NEIN** — lediglich **Stilreferenz** | **FACT** |
| F-4 | Gelebte Repo-Praxis zum Scope-Bestandteil | Die letzten 20 `docs`-Commits verwenden **ausnahmslos** `docs:` **ohne** Scope (20/20; 0× `docs(...)`) | **FACT (Beobachtung)** |

> **Folge:** Der exakte Wortlaut ist **nicht quellenbestimmt** und daher durch
> **Human Decision** festzulegen (Kap. 5). Die Festlegung erzeugt **keine
> zusätzliche normative Bedeutung**.

---

## 4. Quellenlage zu R-2

| # | Prüfpunkt | Befund | Klasse |
|---|---|---|---|
| R-a | Gegenstand von R-2 | Ob im SPVERS-EXEC ein zusätzliches Begleit-/Versionierungs-Record unter `docs/audits/*` erzeugt werden darf bzw. soll | **FACT (Fragestellung)** |
| R-b | Verlangt die V2-Entscheidung ein solches Record? | **NEIN** — `SPVERS-DEC-01` verlangt ausschließlich die erstmalige Versionierung des Sprint Plans | **FACT** |
| R-c | Verlangt eine Quelle ein solches Record? | **NEIN** — GDR-003 verlangt lediglich eine „separate Governance-Entscheidung", kein bestimmtes Artefakt | **UNKNOWN (Negativbefund)** |
| R-d | Vorbefund | `SPVERS-PREP-01` **CS-V-3** führte ein Begleit-Record als zulässig **falls bejaht**; die Frage blieb in DEC-01 **offen**. Das Review meldete den pauschalen Ausschluss in EXEC-PREP Kap. 4 als **Vorgriff (R-2)** | **FACT** |
| R-e | Versionierungsgegenstand | bleibt `docs/milestone-1.0-sprint-plan.md` | **FACT** |

> **Folge:** Auch R-2 ist **nicht quellenbestimmt** und durch **Human
> Decision** zu schließen (Kap. 5). Damit wird der im Review gemeldete
> Vorgriff **nachträglich durch eine ausdrückliche Entscheidung geheilt** —
> die Frage ist nun entschieden statt stillschweigend geschlossen.

---

## 5. HUMAN DECISION

```text
JX-DEV-SPR01-RL05-G7-A1-SPVERS-Z12-DEC-01-R0

Authority:  Projekteigner / Governance
Date:       2026-08-13
Baseline:   HEAD 4ac6c11

--- V2-f  COMMIT MESSAGE ---

Commit Message fuer den spaeteren SPVERS-EXEC, exakt:

    docs: version sprint plan

Dieser Wortlaut ist als HUMAN DECISION festgehalten.
Nicht weiter abzuleiten. Nicht umzuformulieren.
Nicht automatisch zu verbessern.

Status: DECIDED

--- R-2  BEGLEIT-/VERSIONIERUNGS-RECORD ---

KEIN zusaetzliches Begleit-/Versionierungs-Record im SPVERS-EXEC.

Begruendung (Willensakt, keine Ableitung):
Der SPVERS-EXEC soll ausschliesslich den bereits entschiedenen
Versionierungsvorgang vollziehen.

Change Surface des EXEC:
    docs/milestone-1.0-sprint-plan.md
Keine zusaetzliche Governance-Datei.

Die Audit-/Nachweisfuehrung erfolgt ausschliesslich ueber:
    - SPVERS-DEC-01
    - SPVERS-EXEC-PREP
    - den EXEC-Abschlussbericht
    - Git-Preflight
    - Staging-Nachweis
    - Commit-Hash
    - Post-Commit-Verifikation

Diese Entscheidung erweitert den materiellen Change Surface nicht.

Status: DECIDED
```

### 5.1 Zeichenspezifikation der Commit Message

| Merkmal | Festlegung |
|---|---|
| **Exakter Wortlaut** | `docs: version sprint plan` |
| Typ | `docs` — zulässiger Typ nach Development Standard v1.1 §C |
| Scope | **keiner** — entspricht der gelebten Repo-Praxis (F-4) |
| Zeichensatz | reines ASCII, Kleinschreibung, ein Doppelpunkt, einfache Leerzeichen |
| Zusätze | **keine** — kein Trailer, keine Klammerergänzung, keine Referenz |
| Abweichung zulässig? | **NEIN** — jede Abweichung erfordert eine neue Human Decision |

---

## 6. EXEC-Auftrag — Inhalt der späteren Welle

> Der EXEC ist **noch nicht erteilt**. Diese Kapitel binden ihn inhaltlich,
> autorisieren ihn aber **nicht**.

Der spätere `JX-DEV-SPR01-RL05-G7-A1-SPVERS-EXEC-01-R0` darf ausschließlich:

1. den aktuellen Sprint Plan **readonly** prüfen,
2. dessen **SHA und Zeilenzahl** erfassen,
3. sicherstellen, dass er **ungetrackt** ist,
4. ausschließlich `docs/milestone-1.0-sprint-plan.md` **stagen**,
5. den staged Inhalt **byte-/inhaltstreu** gegen den Vorzustand verifizieren,
6. **genau einen** Commit mit exakt der Message `docs: version sprint plan` erstellen,
7. den Commit **nachprüfen**,
8. den Sprint Plan als **tracked** bestätigen,
9. den Dateiinhalt gegen den **Vorzustand** vergleichen,
10. die drei vorbestehenden Working-Tree-Modifikationen als **weiterhin unverändert** bestätigen.

**Nichts darüber hinaus.**

---

## 7. Technische Sicherheit — verbindlich für den EXEC

**Ausdrücklich zu verhindern:**

```text
git add -A
git add .
git add -u
git commit -a
```

| # | Pflicht | Zweck |
|---|---|---|
| T-1 | Staging **ausschließlich** über den exakten Pfad `docs/milestone-1.0-sprint-plan.md` | genau ein Pfad im Index |
| T-2 | Vor dem Commit **zwingend**: `git diff --cached --name-only` | erwartet: **`docs/milestone-1.0-sprint-plan.md`** und **genau keine weitere Datei** |
| T-3 | Der **staged Blob** ist gegen den vor dem Staging ermittelten Inhalt zu prüfen | Sollwert: **`18ffa1770ae87df45ba447bc47ef920864ddb2cd`** |
| T-4 | Commit ohne `-a` und ohne Pfadargumente, ausschließlich aus dem Index | verhindert unbeabsichtigte Erweiterung |

> **Kritischster Fehlerpfad:** `git commit -a` oder `git add -A` — beide zögen
> `CLAUDE.md`, `ROADMAP.md` und `docs/architecture-book-v2.md` in den Commit
> und verletzten die Change Surface.

---

## 8. Wichtige Trennung — verbindlich im EXEC-Abschlussbericht

| Akt | Merkmale |
|---|---|
| **A1-EXEC** | **1 Datei / 1 materielle Zeile** · bereits vollzogen · bereits verifiziert |
| **SPVERS-EXEC** | **Erstaufnahme eines bislang ungetrackten Bestandsdokuments** · Git zeigt technisch **324 hinzugekommene Zeilen** · diese 324 Zeilen stellen **NICHT** 324 materielle Änderungen dar |

```text
Der spaetere Commit darf NICHT als A1-EXEC bezeichnet werden.
Die 324 Zeilen bemessen den BESTAND, nicht den AENDERUNGSUMFANG.
```

**Der EXEC-Abschlussbericht muss diese Unterscheidung ausdrücklich festhalten.**

---

## 9. Post-Commit-Verifikation — verbindlich

| # | Prüfung | Sollwert |
|---|---|---|
| Q-1 | Commit existiert | Hash zu protokollieren |
| Q-2 | Sprint Plan ist **tracked** | `git ls-files` → Treffer |
| Q-3 | Inhalt **byte-identisch** zum Vorzustand | committeter Blob = `18ffa177…` |
| Q-4 | Zeilenzahl | **324** |
| Q-5 | Z. 6 unverändert | `**APPROVED FOR SPRINT EXECUTION PLANNING (ADW-SPR-1.0-001)**` |
| Q-6 | Z. 7–9 unverändert | `1.0` · `R0` · `2026-08-09` |
| Q-7 | Keine sonstige Datei im Commit | `git show --name-status` → **eine** Zeile, `A` |
| Q-8 | `CLAUDE.md` unverändert | weiterhin `M`, Inhalt unberührt |
| Q-9 | `ROADMAP.md` unverändert | weiterhin `M`, Inhalt unberührt |
| Q-10 | `docs/architecture-book-v2.md` unverändert | weiterhin `M`, Inhalt unberührt |
| Q-11 | Kein Push · kein PR · kein Merge · kein Tag | **NOT PERFORMED** |

---

## 10. Governance-Abgrenzung — verbindlich für den EXEC

Der EXEC darf **NICHT**: U-4′ verändern · G7-b bewerten · HD-2 behandeln ·
Bedingung 7 bewerten · OP-1/OP-2 verändern · OD-05 ändern · ADR-012 ändern ·
andere Governance-Dokumente verändern · Coding freigeben · RL-05 starten ·
QG-006 starten.

---

## 11. Entscheidungsergebnis

| Punkt | Ergebnis |
|---|---|
| **V2-f** | **DECIDED** — exakter Commit-Message-Wortlaut: `docs: version sprint plan` |
| **R-2** | **DECIDED** — **kein** zusätzliches Begleit-/Versionierungs-Record im EXEC |
| **SPVERS** | **V2 DECIDED** · **EXEC noch nicht ausgeführt** |

### 11.1 Wirkung auf die EXEC-Readiness

| Punkt | Status vor dieser Decision | Status danach |
|---|---|---|
| V2-a … V2-e | bestimmt / EXEC-fähig | **unverändert bestimmt** |
| **V2-f** | **UNKNOWN — HUMAN DECISION REQUIRED** | **DECIDED** |
| **R-2** | **offen / im Review als Vorgriff gemeldet** | **DECIDED — ausdrücklich geschlossen** |
| **EXEC-Auftrag** | **NOT AUTHORIZED** | **weiterhin NOT AUTHORIZED** — separate Welle |

> **Damit sind alle inhaltlichen Voraussetzungen des EXEC bestimmt.** Es fehlt
> ausschließlich noch der **EXEC-Auftrag selbst**.

---

## 12. Negative Checks

| # | Prüfung | Ergebnis |
|---|---|---|
| N-1 | V2 erneut entschieden? | **NEIN** |
| N-2 | Sprint Plan verändert? | **NEIN** — nur gelesen, weiterhin `??`, SHA `18ffa177…` |
| N-3 | `git add` des Sprint Plans? | **NEIN** |
| N-4 | Commit des Sprint Plans? | **NEIN** |
| N-5 | Push / PR / Merge / Tag? | **NEIN** |
| N-6 | Bestandsdatei verändert? | **NEIN** |
| N-7 | EXEC ausgeführt oder autorisiert? | **NEIN** — DEC ≠ EXEC |
| N-8 | Commit-Message abgeleitet, umformuliert oder „verbessert"? | **NEIN** — wortgleich übernommen |
| N-9 | Change Surface materiell erweitert? | **NEIN** — R-2 verengt, erweitert nicht |
| N-10 | A1-EXEC wiederholt oder umgedeutet? | **NEIN** |
| N-11 | U-4′ ausgelegt? | **NEIN** — **UNDETERMINED** |
| N-12 | G7-b entschieden? | **NEIN** — **OPEN** |
| N-13 | HD-2 wiedervorgelegt? | **NEIN** — **DEFERRED / OPEN** |
| N-14 | Bedingung 7 bewertet? | **NEIN** — **NOT FULFILLED**; ACN-09 gewahrt |
| N-15 | OP-1 / OP-2 verändert? | **NEIN** |
| N-16 | OD-05 / ADR-012 / ADRs / RDRs / AB / IP verändert? | **NEIN** |
| N-17 | Coding / RL-05 / QG-006? | **NEIN** — NOT AUTHORIZED / NOT REACHED / NOT STARTED |
| N-18 | Vorbestehende Working-Tree-Änderungen berührt? | **NEIN** |
| N-19 | Empfehlung als Entscheidung ausgegeben? | **NEIN** — beide Werte sind Vorgaben des Projekteigners |

**Negative Checks: alle PASS.**

---

## 13. Explicit Non-Decisions

```text
V2: NICHT erneut entschieden. Sprint-Plan-Inhalt: NICHT erneut entschieden.
EXEC: NICHT autorisiert, NICHT vorbereitet ueber diese Bindung hinaus,
      NICHT ausgefuehrt.
Sprint Plan: NICHT geaendert, NICHT gestaged, NICHT committet.
A1-EXEC / A1-VERIFY: NICHT wiederholt, NICHT umgedeutet.
U-4': NICHT ausgelegt — UNDETERMINED.
G7-b: NICHT entschieden — OPEN. G7-a: NICHT beruehrt.
HD-2: NICHT wiedervorgelegt — DEFERRED / OPEN / NOT DECIDED.
Bedingung 7: NICHT bewertet, NICHT abgesenkt — NOT FULFILLED.
OP-1 / OP-2: NICHT veraendert.
Aufnahme weiterer Dateien des GDR-003-Scopes 7.3/7.4: NICHT entschieden.
OD-05 / ADR-012 / ADRs / RDRs / Architecture Book / Implementation Plan /
      CLAUDE.md / ROADMAP.md / Code / Tests / Config: UNVERAENDERT.
Alle bestehenden Governance-Artefakte: NICHT ueberschrieben.
RL-05: NOT REACHED. Coding: NOT AUTHORIZED. QG-006: NOT STARTED.
Kein Push, PR, Merge, Tag.
```

---

## 14. Change Surface dieser Welle

| Gegenstand | Umfang |
|---|---|
| Neue Dateien | **genau eine** — `docs/audits/jx-dev-spr01-rl05-g7-a1-sprint-plan-versioning-z12-decision-record-r0.md` |
| Geänderte / gelöschte Dateien | **keine** |
| Sprint Plan | **nur gelesen** — unverändert, ungetrackt |
| Bestehende Governance-Artefakte | **UNBERÜHRT** |
| Code / Tests / Config | **UNBERÜHRT** |
| Vorbestehende Working-Tree-Änderungen | **UNANGETASTET** |

---

## 15. Governance State

| Position | Status |
|---|---|
| **SPVERS** | **V2 DECIDED** · **V2-f DECIDED** · **R-2 DECIDED** · **EXEC NOCH NICHT AUSGEFÜHRT / NICHT AUTORISIERT** |
| **A1-EXEC** | **VERIFIED** |
| **Sprint Plan** | `APPROVED FOR SPRINT EXECUTION PLANNING (ADW-SPR-1.0-001)` · `1.0` / `R0` / `2026-08-09` · **ungetrackt** · 324 Zeilen · Blob `18ffa177…` |
| **U-4′** | **UNDETERMINED** |
| **G7-a / G7-b** | physisch adressiert / **OPEN** |
| **Bedingung 7** | **NOT FULFILLED** |
| **HD-2** | **DEFERRED / OPEN / NOT DECIDED** |
| **OP-1 / OP-2** | **OFFEN** / **NICHT ERFÜLLT** |
| **RL-05 / CODING / QG-006** | **NOT REACHED** / **NOT AUTHORIZED** / **NOT STARTED** |
| **OD-05 / ADR-012 / ADRs / RDRs / Architecture Book / IP / `CLAUDE.md` / `ROADMAP.md` / Code / Tests / Config** | **UNVERÄNDERT** |

---

## 16. Next Step

> **Separat zu beauftragende EXEC-Welle:**
> `JX-DEV-SPR01-RL05-G7-A1-SPVERS-EXEC-01-R0`
>
> Inhaltlich vollständig gebunden durch Kap. 6–10 dieses Records.
> Es fehlt ausschließlich der **Auftrag**.

**STOP NACH DIESEM ARTEFAKT. Kein automatischer SPVERS-EXEC.**

---

## 17. Revision History

| Revision | Datum | Änderung | Status |
|---|---|---|---|
| **R0** | 2026-08-13 | Human Decision zu **V2-f** (Commit Message `docs: version sprint plan`) und **R-2** (kein Begleit-Record im EXEC); Baseline Gate gegen HEAD `4ac6c11` mit Reproduktion des Blob-SHA `18ffa177…`; Quellenlage F-1…F-4 und R-a…R-e; EXEC-Bindung (10 Schritte), technische Sicherheit T-1…T-4, Trennung A1-EXEC/SPVERS-EXEC, Post-Commit-Verifikation Q-1…Q-11, Governance-Abgrenzung; Negative Checks N-1…N-19 | **COMPLETED — DECISION ONLY** |

---

**Ende JX-DEV-SPR01-RL05-G7-A1-SPVERS-Z12-DEC-01-R0 — Human Decision Record —
JOCHEN X Milestone 1.0 (2026-08-13) — HEAD `4ac6c11` — Bezugs-Baseline
`MILESTONE-1.0-BASELINE = 8fcf42f1997dfcf6ff232e75fd33c37b933991c8`**
