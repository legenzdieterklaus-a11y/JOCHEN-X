# JOCHEN X — Milestone 1.0
# JX-DEV-SPR01-RL05-G7-A1-GOV-ARTIFACTS-PREP-01-R0 — Decision Preparation
## Versionierung der uncommitteten Governance-Artefakte der SPVERS-Kette

> **COMPLETED — PREPARATION ONLY · NO DECISION · NO EXECUTION**
>
> **Keine Option gewählt. Keine Datei verändert. Kein `git add`, kein
> Commit, kein Push.**
>
> **BEFUND MIT SOFORTIGER RELEVANZ:** Der Auftrag benennt **zwei**
> uncommittete Artefakte. Tatsächlich sind es **drei** — siehe Kap. 3.1.
> Das dritte (`…-sprint-plan-versioning-prep-r0.md`) wird vom **bereits
> committeten** `SPVERS-DEC-01` als Quelle referenziert.
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
| **HEAD** | `7c7a572ba3633d9666ff79d01d9d98620a3e6e0e` = `7c7a572` — „docs: version sprint plan" — **wie erwartet** |
| Staging | **leer** |
| Working Tree — getrackte Modifikationen | `CLAUDE.md` · `ROADMAP.md` · `docs/architecture-book-v2.md` — **unangetastet** |
| SPVERS-EXEC-01 | **EXECUTED**, Commit `7c7a572`, Sprint Plan **tracked**, Blob vor/nach identisch, genau eine Datei im Commit, Push NOT PERFORMED |
| A1-EXEC | **VERIFIED**, unverändert |
| Namenskonvention für diese PREP-Art | **nicht belegt** — 0 Treffer im Repository; der im Auftrag vorgegebene Name wird verwendet |
| Bezugs-Baseline | `MILESTONE-1.0-BASELINE = 8fcf42f1997dfcf6ff232e75fd33c37b933991c8` (GDR-003) |

Der aktuelle Governance-Zustand wird **übernommen, nicht neu bewertet**.

**Baseline Gate: PASS.**

---

## 2. Gegenstand

| # | Artefakt (Auftragsgegenstand) | Kurzbezeichnung |
|---|---|---|
| **AR-1** | `docs/audits/jx-dev-spr01-rl05-g7-a1-sprint-plan-versioning-exec-prep-r0.md` | **SPVERS-EXEC-PREP-01** |
| **AR-2** | `docs/audits/jx-dev-spr01-rl05-g7-a1-sprint-plan-versioning-z12-decision-record-r0.md` | **SPVERS-Z12-DEC-01** |

---

## 3. Dateistatus (readonly erhoben)

| Merkmal | **AR-1** | **AR-2** |
|---|---|---|
| Existiert | **JA** | **JA** |
| Git-Status | **`??` untracked** | **`??` untracked** |
| Zeilen | **384** | **363** |
| Bytes | **21 348** | **15 818** |
| **Blob-SHA** | **`1cbd728e25103c719d69e0059dca94e98da3555a`** | **`a7a48d8aba45587773f5fc8ac3c63a9b83d59349`** |
| `git log --all -- <pfad>` | **0 Einträge** — nie versioniert | **0 Einträge** — nie versioniert |
| Bestandteil eines bestehenden Commits | **NEIN** | **NEIN** |
| Durch `.gitignore` ausgeschlossen | **NEIN** | **NEIN** |

Alles **FACT**, direkt erhoben.

### 3.1 Vollständigkeitsbefund — **ein drittes Artefakt**

Eine Vollständigkeitsprüfung über **alle** `docs/audits/jx-dev-spr01*`-Artefakte
(25 Dateien) ergibt: **22 sind getrackt, 3 sind untracked** — nicht zwei.

| # | Artefakt | Status |
|---|---|---|
| AR-1 | `…-sprint-plan-versioning-exec-prep-r0.md` | **untracked** (Auftragsgegenstand) |
| AR-2 | `…-sprint-plan-versioning-z12-decision-record-r0.md` | **untracked** (Auftragsgegenstand) |
| **AR-3** | **`…-sprint-plan-versioning-prep-r0.md`** (**SPVERS-PREP-01**) | **untracked** — **nicht im Auftrag benannt** |

| Merkmal | **AR-3** |
|---|---|
| Zeilen · Bytes | **456** · **27 009** |
| **Blob-SHA** | **`0b16ed0eb1fc2c311f0885f9d43dffed35b90e91`** |
| `git log --all` | **0 Einträge** |
| Herkunft | `SPVERS-PREP-01`-Welle; deren Auftrag lautete ausdrücklich **„COMMIT: NEIN"** |

> **Relevanz (FACT, keine Wertung):** Der **committete** `SPVERS-DEC-01`
> (`4ac6c11`) führt AR-3 in seinem Source Gate als Quelle und stützt
> Optionsraum (Kap. 4) und Empfehlungsabgrenzung (Kap. 5) ausdrücklich darauf.
> Ein versioniertes Decision Record referenziert damit ein **unversioniertes**
> PREP. Dieselbe Konstellation besteht zwischen AR-2 und AR-1.
>
> **Nicht entschieden.** AR-3 ist **nicht** Auftragsgegenstand; der Befund wird
> lediglich registriert, damit eine spätere Entscheidung nicht unbemerkt eine
> Lücke hinterlässt.

### 3.2 Entstehungskontext

Alle drei Artefakte stammen **ausschließlich** aus den bereits abgeschlossenen
Governance-Wellen dieser Kette. Beleg: `git log --all` = 0 Einträge (nie in
irgendeinem Ref), Inhalt jeweils mit `Revision History R0 — COMPLETED`
abgeschlossen. **Keine neue inhaltliche Bewertung vorgenommen.** — **FACT**

---

## 4. Herkunft und Funktion je Artefakt

| Frage | **AR-1 — SPVERS-EXEC-PREP-01** | **AR-2 — SPVERS-Z12-DEC-01** |
|---|---|---|
| **A) Erzeugende Welle** | `JX-DEV-SPR01-RL05-G7-A1-SPVERS-EXEC-PREP-01-R0` — **FACT** | `JX-DEV-SPR01-RL05-G7-A1-SPVERS-Z12-DEC-01-R0` — **FACT** |
| **B) Dokumentierter Inhalt** | Ausführungsvorbereitung des V2-EXEC: Objektprüfung, Nachweiskonzept, Change Surface, Evidence-Checkliste, offene Punkte — **FACT** | Human Decision zu **V2-f** (Commit Message `docs: version sprint plan`) und **R-2** (kein Begleit-Record) — **FACT** |
| **C) Inhalt abgeschlossen?** | **JA** — R0, „COMPLETED — PREPARATION ONLY" — **FACT** | **JA** — R0, „COMPLETED — DECISION ONLY" — **FACT** |
| **D) In einem Commit enthalten?** | **NEIN** — **FACT** | **NEIN** — **FACT** |
| **E) Quelle, die Versionierung verlangt?** | **NEIN** — **UNKNOWN (Negativbefund)** | **NEIN** — **UNKNOWN (Negativbefund)** |
| **F) Quelle, die sie als optional/separat behandelt?** | **JA** — GDR-003 Z. 88 („ihre Versionierung ist ein separater Governance-Commit-Scope") und Z. 137 („Commit 2+ … **optional**, nachgelagert … separate Governance-Entscheidung"); Kap. 7.3/7.4 erfassen den Governance-/Doku-Bestand als eigenen Scope — **NORM** | **JA** — dieselben Fundstellen — **NORM** |
| **G) Quelle, die Nichtversionierung verlangt?** | **NEIN** — **UNKNOWN (Negativbefund)** | **NEIN** — **UNKNOWN (Negativbefund)** |

### 4.1 Nicht als Norm verwendet

| Aussage | Klasse |
|---|---|
| „Alle übrigen Artefakte der Kette sind getrackt, also müssen es auch diese sein" | **INFERENCE — nicht als Norm verwendet** |
| „Ein committetes Decision Record verlangt versionierte Quellen" | **INFERENCE — nicht als Norm verwendet.** Keine geprüfte Quelle normiert das |
| „Die Wellen sagten ‚Commit: NEIN', also ist Nichtversionierung entschieden" | **INFERENCE — nicht als Norm verwendet.** Die Aufträge schwiegen bzw. untersagten den Commit **in ihrer Welle**; eine Aussage über eine **spätere** Versionierung liegt darin nicht |

---

## 5. Change Surface eines möglichen späteren EXEC — Optionsraum

**Keine Option gewählt.**

| Option | Inhalt | Change Surface | Quellenlage |
|---|---|---|---|
| **O-1** | **Beide gemeinsam** versionieren | AR-1 + AR-2 — **2 Dateien, 1 Commit** | zulässig nach GDR-003 Z. 137 (Commit-2+-Scope); keine Quelle verlangt Trennung |
| **O-2** | **Jedes separat** versionieren | AR-1 und AR-2 — **je 1 Datei, 2 Commits** | ebenso zulässig; keine Quelle verlangt Bündelung |
| **O-3** | **Nicht versionieren** | **keine** | zulässig — GDR-003 bezeichnet den Scope ausdrücklich als **„optional"** |
| **O-4** | **Alle drei** gemeinsam (AR-1 + AR-2 + **AR-3**) | **3 Dateien, 1 Commit** | **quellengetragen**: GDR-003 Kap. 7.3/7.4 + Z. 137 behandeln den Governance-/Doku-Bestand als **einen** Commit-2+-Scope. **Nicht erfunden** — folgt aus dem Vollständigkeitsbefund Kap. 3.1 |

> **O-4 ist keine Erweiterung des Auftrags**, sondern die Abbildung des
> tatsächlichen Repository-Zustands auf den bereits bestehenden
> GDR-003-Scope. Die Wahl bleibt vollständig offen.
>
> **Weitere Optionen** (z. B. Aufnahme des gesamten GDR-003-Scopes 7.2/7.3/7.4
> mit den 53 vorbestehenden untracked Dokumenten) wären quellenseitig ebenfalls
> denkbar, sind aber **erheblich weiter** als der Gegenstand dieser PREP und
> werden hier **nur benannt, nicht ausgearbeitet**.

---

## 6. Wichtige Trennung

| Vorgang | Status |
|---|---|
| **SPVERS-EXEC-01** | Sprint Plan versioniert · Commit **`7c7a572`** · **abgeschlossen** · **verifiziert** |
| **Jetziger Gegenstand** | Versionierung der **Governance-Artefakte** — **eigener, noch nicht entschiedener Vorgang** |

```text
Das jetzige Thema ist NICHT Teil des abgeschlossenen SPVERS-EXEC.
Commit 7c7a572 wird NICHT nachtraeglich umgeschrieben.
KEIN amend. KEIN reset. KEIN rebase. KEIN force push.
```

Ein etwaiger späterer EXEC wäre ein **zusätzlicher, eigener Commit** — niemals
eine Änderung an `7c7a572`.

---

## 7. Governance-Entscheidung erforderlich?

| # | Frage | Bereits entschieden? | Status |
|---|---|---|---|
| E-1 | Werden AR-1 und AR-2 versioniert? | **NEIN** | **HUMAN DECISION REQUIRED** |
| E-2 | Gemeinsam oder getrennt (O-1/O-2/O-3/O-4)? | **NEIN** | **HUMAN DECISION REQUIRED** |
| E-3 | Welche Commit Message? | **NEIN** | **HUMAN DECISION REQUIRED** (Kap. 8) |
| E-4 | Begleitender Record erforderlich? | **NEIN** für diesen Vorgang. *(R-2 in `SPVERS-Z12-DEC-01` betraf ausschließlich den **Sprint-Plan**-EXEC und ist auf diesen Vorgang **nicht** übertragbar — eine Übertragung wäre **INFERENCE**.)* | **HUMAN DECISION REQUIRED** |
| E-5 | Behandlung von **AR-3** (Kap. 3.1)? | **NEIN** | **HUMAN DECISION REQUIRED** |

**Keine dieser Fragen wird hier entschieden.**

---

## 8. Commit Message

| # | Prüfung | Befund | Klasse |
|---|---|---|---|
| M-1 | Existiert eine Commit-Message-Konvention? | **JA** — `<type>(<scope>): <description>`, Typen `feat`, `fix`, `docs`, `refactor`, `test`, `chore` (Development Standard v1.1 §C; identisch `CLAUDE.md`) | **NORM** |
| M-2 | Normiert eine Quelle einen **exakten Wortlaut** für diesen Vorgang? | **NEIN** | **UNKNOWN (Negativbefund)** |
| M-3 | Gelebte Praxis | Die letzten 20 `docs`-Commits verwenden ausnahmslos `docs:` **ohne** Scope | **FACT (Beobachtung)** |
| M-4 | Taugt `docs: version sprint plan` als Vorlage? | Nur als **Stilreferenz**; sie bezeichnet den Sprint-Plan-Vorgang, nicht diesen | **FACT / INFERENCE getrennt** |

> ## **COMMIT MESSAGE = HUMAN DECISION REQUIRED**
>
> Nur das **Format** ist NORM (M-1). Der **Wortlaut** ist es nicht (M-2) und
> wird hier **nicht** als normativer Wert ausgegeben.

### 8.1 NON-BINDING Vorschlag — **keine Festlegung**

```text
docs: version spvers governance artifacts
```

Nur Vorschlag; nicht gewählt.

---

## 9. Technische Risiken und Schutzmaßnahmen

> **Prüfkonzept. Kein `git add`.**

| # | Prüfung | Ergebnis |
|---|---|---|
| TR-1 | Können beide Dateien gemeinsam gestaged werden? | **JA** — beide untracked, nicht ignoriert, gleiches Verzeichnis; ein Aufruf mit **zwei expliziten Pfaden** genügt |
| TR-2 | Andere Working-Tree-Modifikationen vorhanden? | **JA** — `CLAUDE.md`, `ROADMAP.md`, `docs/architecture-book-v2.md` (getrackt, `M`) |
| TR-3 | Gefahr des versehentlichen Mitcommittens? | **JA, real** — jede pauschale Staging-Option würde sie erfassen |
| TR-4 | Weitere Risikoquelle | **29+ vorbestehende untracked Dokumente** unter `docs/` — `git add .` würde auch diese aufnehmen |

**Erforderliche Schutzmaßnahmen bei einem späteren EXEC** — sämtlich
**VERFAHRENSVORSCHLAG**, keine Governance-Norm:

| # | Maßnahme |
|---|---|
| S-1 | Staging **ausschließlich** mit vollständigen, expliziten Pfaden |
| S-2 | **Verboten:** `git add -A` · `git add .` · `git add -u` · `git commit -a` |
| S-3 | Vor dem Commit: `git diff --cached --name-only` → **exakt** die vorgesehenen Pfade, **kein** weiterer |
| S-4 | Staged Blobs gegen die in Kap. 3 erfassten SHAs prüfen (`1cbd728e…`, `a7a48d8a…`, ggf. `0b16ed0e…`) |
| S-5 | Commit ohne `-a` und ohne Pfadargumente, ausschließlich aus dem Index |
| S-6 | Nach dem Commit: die drei getrackten Modifikationen müssen **weiterhin `M`** sein und ihre Blob-SHAs unverändert |
| S-7 | **Kein** `amend`, `reset`, `rebase`, `force push` — `7c7a572` bleibt unberührt |

---

## 10. NON-BINDING EMPFEHLUNG

> **Ausdrücklich getrennt von FACT, NORM und HUMAN DECISION. Keine Entscheidung.**

> **Sauberster nächster einzelner Schritt:** **eine** Human Decision, die
> **E-1, E-2 (einschließlich E-5) und E-3** in **einem** Record schließt —
> also: ob versioniert wird, welcher Umfang (O-1 / O-2 / O-3 / **O-4**), und
> mit welchem Wortlaut.

**Begründung (unverbindlich):** Die drei Fragen sind nicht unabhängig — der
Umfang bestimmt den sinnvollen Wortlaut, und ohne beide ist kein EXEC
ausführbar. Sie getrennt zu entscheiden erzeugte zwei Wellen ohne
Erkenntnisgewinn. **E-4** (Begleit-Record) ist von der Umfangswahl abhängig
und sollte im selben Record mitentschieden werden, sobald der Umfang feststeht.

**Ausdrücklich nicht empfohlen:** eine Option vorwegzunehmen. Auch **O-3
(nicht versionieren)** ist governance-seitig vollständig zulässig — GDR-003
bezeichnet den Scope als **„optional"**.

---

## 11. Ausdrücklich NICHT ausgeführt

```text
Keine der beiden Dateien veraendert. AR-3 nicht veraendert.
Kein git add. Kein Commit. Kein Push. Kein PR, Merge, Tag.
Kein amend / reset / rebase / force push — 7c7a572 unberuehrt.
Sprint-Plan-Versionierung NICHT erneut ausgefuehrt.
Keine Option gewaehlt (O-1 bis O-4 offen).
Commit Message NICHT festgelegt.
AR-3 NICHT entschieden — nur als Befund registriert.
U-4': NICHT ausgelegt. G7-b: NICHT entschieden.
Bedingung 7: NICHT bewertet. HD-2: NICHT wiedervorgelegt.
OP-1 / OP-2 / OD-05 / ADR-012 / ADRs / RDRs / Architecture Book /
      Implementation Plan / CLAUDE.md / ROADMAP.md / Code / Tests /
      Config: UNVERAENDERT.
Coding: NICHT freigegeben. RL-05: NICHT gestartet. QG-006: NICHT gestartet.
Keine bestehende Governance-Datei ueberschrieben.
```

---

## 12. Change Surface dieser Welle

| Gegenstand | Umfang |
|---|---|
| Neue Dateien | **genau eine** — `docs/audits/jx-dev-spr01-rl05-g7-a1-governance-artifacts-versioning-prep-r0.md` |
| Geänderte / gelöschte Dateien | **keine** |
| AR-1 / AR-2 / AR-3 | **nur gelesen** |
| Sprint Plan | **nicht berührt** |
| Vorbestehende Working-Tree-Änderungen | **UNANGETASTET** |

---

## 13. Governance State — unverändert

| Position | Status |
|---|---|
| **SPVERS** | **EXECUTED** · Commit **`7c7a572`** |
| **Sprint Plan** | **TRACKED** · `APPROVED FOR SPRINT EXECUTION PLANNING (ADW-SPR-1.0-001)` · `1.0` / `R0` / `2026-08-09` |
| **A1-EXEC** | **VERIFIED** |
| **U-4′** | **UNDETERMINED** |
| **G7-a** | **PHYSICALLY ADDRESSED** |
| **G7-b** | **OPEN** |
| **Bedingung 7** | **NOT FULFILLED** |
| **HD-2** | **DEFERRED / OPEN** |
| **RL-05 / CODING / QG-006** | **NOT REACHED** / **NOT AUTHORIZED** / **NOT STARTED** |
| **Versionierung AR-1 / AR-2 / AR-3** | **OPEN — HUMAN DECISION REQUIRED** |

Keine dieser Positionen wurde durch diese PREP verändert.

---

## 14. STOP

> Kein automatischer EXEC · kein `git add` · kein Commit · kein Push · keine
> weitere Governance-Entscheidung.
>
> **Nächster zulässiger Schritt:** genau eine Human Decision zu E-1, E-2/E-5
> und E-3.

---

## 15. Revision History

| Revision | Datum | Änderung | Status |
|---|---|---|---|
| **R0** | 2026-08-13 | Entscheidungsvorbereitung zur Versionierung der uncommitteten SPVERS-Governance-Artefakte: Baseline gegen HEAD `7c7a572`; Dateistatus AR-1/AR-2 mit Blob-SHAs; **Vollständigkeitsbefund: drittes untracked Artefakt AR-3**; Herkunft/Funktion A–G je Artefakt; Optionsraum O-1…O-4; Trennung vom abgeschlossenen SPVERS-EXEC; Entscheidungsbedarf E-1…E-5; Commit Message als HUMAN DECISION REQUIRED mit NON-BINDING-Vorschlag; technische Risiken TR-1…TR-4 und Schutzmaßnahmen S-1…S-7; NON-BINDING Empfehlung für genau einen nächsten Schritt | **COMPLETED — PREPARATION ONLY** |

---

**Ende JX-DEV-SPR01-RL05-G7-A1-GOV-ARTIFACTS-PREP-01-R0 — Decision Preparation —
JOCHEN X Milestone 1.0 (2026-08-13) — HEAD `7c7a572` — Bezugs-Baseline
`MILESTONE-1.0-BASELINE = 8fcf42f1997dfcf6ff232e75fd33c37b933991c8`**
