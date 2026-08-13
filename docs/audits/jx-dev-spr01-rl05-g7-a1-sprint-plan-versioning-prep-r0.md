# JOCHEN X — Milestone 1.0
# JX-DEV-SPR01-RL05-G7-A1-SPVERS-PREP-01-R0 — Decision Preparation
## Erstversionierung des bislang ungetrackten Sprint Plans

> **COMPLETED — PREPARATION ONLY · NO DECISION · NO EXECUTION**
>
> Dieses Dokument bereitet **ausschließlich** eine spätere Human Decision
> vor: ob `docs/milestone-1.0-sprint-plan.md` erstmals unter
> Versionskontrolle genommen werden soll und — falls ja — wie der dadurch
> entstehende Git-Nachweis behandelt und dokumentiert wird.
>
> **Keine Option gewählt.** **Keine Datei verändert.** **Kein `git add`,
> kein Commit, kein Push.**
>
> **A1-EXEC / OD-08 = verifiziert korrekt vollzogen** · **U-4′ =
> UNDETERMINED** · **G7-b = OFFEN** · **IP §10.6 BEDINGUNG 7 = NICHT
> ERFÜLLT** · **HD-2 = DEFERRED / OPEN** · **RL-05 = NOT REACHED** ·
> **CODING = NOT AUTHORIZED** · **QG-006 = NOT STARTED**

---

## 1. Baseline Gate

| Prüfung | Ergebnis |
|---|---|
| **HEAD** | `35beef98c4163e197243cc546fa4a273196611f6` = `35beef9` — „docs: record u-4-prime human decision (option c, no material interpretation)" |
| Staging vor Beginn | **leer** (`git diff --cached` leer) |
| Bezugs-Baseline | `MILESTONE-1.0-BASELINE = 8fcf42f1997dfcf6ff232e75fd33c37b933991c8` (GDR-003) |

### 1.1 Autorisierungskette — readonly verifiziert

Alle neun Commits **existieren** und sind **Vorfahren von HEAD**. Kein Hash erfunden.

| Commit | Betreff | Existenz | Vorfahre |
|---|---|---|---|
| `3b76b89` | docs: record condition 7 sequence decision (A2 first) | **JA** | **JA** |
| `a13a148` | docs: verify A2 U-4-prime condition 7 coverage question | **JA** | **JA** |
| `fa6e192` | docs: record separate verify of A2 execution (U-4-prime) | **JA** | **JA** |
| `8e51c33` | docs: prepare OD-08 option space human decision (A1 PREP) | **JA** | **JA** |
| `9ec12d8` | docs: record OD-08 decision option a (status update authorized) | **JA** | **JA** |
| `92b67e2` | docs: prepare Z-1/Z-2 human decision for OD-08 execution | **JA** | **JA** |
| `73988c5` | docs: record Z-1/Z-2 human decision for OD-08 execution | **JA** | **JA** |
| `5fd7919` | docs: record Z-1c exact status wording for sprint plan header | **JA** | **JA** |
| `35beef9` | docs: record u-4-prime human decision (option c…) | **JA** | **JA (= HEAD)** |

### 1.2 Übernommener Governance-Zustand (als gegeben behandelt, **nicht** neu bewertet)

OD-08 Option (a) physisch vollzogen · Z-1 = Z1-B · Z-1c = `APPROVED FOR SPRINT EXECUTION PLANNING (ADW-SPR-1.0-001)` · Z-2 = Z2-A · A1-EXEC verifiziert korrekt vollzogen · A1-VERIFY read-only verifiziert · Sprint Plan physisch Status/1.0/R0/2026-08-09 · U-4′ UNDETERMINED · G7-b OFFEN · Bedingung 7 NICHT ERFÜLLT · HD-2 DEFERRED/OPEN · RL-05 NOT REACHED · CODING NOT AUTHORIZED · QG-006 NOT STARTED.

**Baseline Gate: PASS.**

---

## 2. Source Gate (readonly)

**Keine externe Quelle.** Keine Datei geschrieben. Keine allgemeine Git-Praxis als Norm herangezogen.

| # | Quelle | Fundstelle | Ergebnis |
|---|---|---|---|
| 1 | **GDR-003 — Baseline Identifier Decision** | `docs/governance/milestone-1.0-baseline-identifier-decision.md` Z. 9–14, 84, 86, 88, 137 | **gelesen — einschlägig, siehe Kap. 2.1** |
| 2 | **A1-EXEC / OD-08** | Vollzugsbericht dieser Session; Z-1c-Record `5fd7919` Kap. 4.1, 10 | **gelesen** |
| 3 | **A1-VERIFY / OD-08** | read-only VERIFY dieser Session (HEAD `5fd7919`) | **gelesen** |
| 4 | **Z-1c Decision Record** | `docs/audits/jx-dev-spr01-rl05-g7-a1-od08-z1c-decision-record-r0.md` | **gelesen** |
| 5 | **Z-1/Z-2 Decision Record** | `docs/audits/jx-dev-spr01-rl05-g7-a1-od08-z12-decision-record-r0.md` | **gelesen** |
| 6 | **OD-08 PREP / DEC** | `…-od08-prep-r0.md` (`8e51c33`) · `…-od08-decision-record-r0.md` (`9ec12d8`) · `…-z12-prep-r0.md` (`92b67e2`) | **gelesen** |
| 7 | **U-4′ Decision Record** | `docs/audits/jx-dev-spr01-rl05-g7-b-u4-prime-decision-record-r0.md` (`35beef9`) | **gelesen** |
| 8 | **G7-DEC-01** | `…-g7-decision-record-r0.md` Z. 144 (Condition 8) | **gelesen** |
| 9 | **ADW-SPR-1.0-001** | `docs/governance/milestone-1.0-sprint-planning-approval-decision-op1.md` Z. 13, 14, 153, 155 | **gelesen** |
| 10 | **Development Standard v1.1** | `docs/development-standard-v1.1.md` §C „Git Conventions" (Z. 803 ff.), §17 Anh. B | **gelesen — kein Gebot zur Versionierung von Planungsdokumenten gefunden** |
| 11 | **Repository-Zustand** | `git ls-files` · `git log --all` · `git check-ignore` · `git status` · `wc -l` | **direkt erhoben, Kap. 3** |

**Source Gate: PASS.**

### 2.1 Maßgeblicher Quellenfund — GDR-003

GDR-003 (Decision ID `GDR-003`, Status **FINAL**, 2026-08-09) behandelt den
untracked-Zustand des Sprint Plans **bereits ausdrücklich**:

| # | Fundstelle | Wortlaut / Inhalt | Klasse |
|---|---|---|---|
| G-1 | Z. 84 | Kapitel **7.3 SESSION-ARTEFACT (11 Dateien) → BASELINE-EXCLUDE** | **FACT** |
| G-2 | Z. 86 | `docs/milestone-1.0-sprint-plan.md` ist in dieser Liste **namentlich enthalten** | **FACT** |
| G-3 | Z. 88 | „Governance-/Audit-/Planungsartefakte — **keine genehmigte Quelle verlangt ihre Aufnahme** in den Produkt-Baseline-Commit; **ihre Versionierung ist ein separater Governance-Commit-Scope**." | **FACT (wörtlich)** |
| G-4 | Z. 137 | Kap. 15 Proposed Commit Scope: „Commit 2+ — Governance-/Doku-Commits (**optional**, nachgelagert) \| Kap. 7.2, **7.3**, 7.4 \| **separate Governance-Entscheidung**" | **FACT (wörtlich)** |

> **Bedeutung für diesen PREP — zwei Feststellungen, keine Wertung:**
>
> 1. Der untracked-Zustand des Sprint Plans ist **keine Nachlässigkeit**,
>    sondern eine **dokumentierte, bewusste Klassifikation** (BASELINE-EXCLUDE).
> 2. Die hier vorbereitete Entscheidung ist **genau die von GDR-003 Z. 137
>    vorgesehene „separate Governance-Entscheidung"** über den Commit-2+-Scope.
>    Sie ist damit **verfahrensmäßig vorgesehen** — GDR-003 bezeichnet diesen
>    Scope zugleich ausdrücklich als **„optional"**.
>
> **Nicht abgeleitet:** dass versioniert werden **muss**, oder dass
> Nichtversionierung ein Mangel sei. G-3/G-4 tragen beides **nicht**.

---

## 3. Repository- / Versionierungsbefund (direkt erhoben)

| # | Auftragsprüfung | Befehl | Ergebnis | Klasse |
|---|---|---|---|---|
| R-1 | Datei von Git getrackt? | `git ls-files -- <pfad>` | **kein Treffer** → **NICHT getrackt** | **FACT** |
| R-2 | Historie in irgendeinem Ref? | `git log --all -- <pfad>` | **0 Einträge** → **nie versioniert** | **FACT** |
| R-3 | Durch `.gitignore` ausgeschlossen? | `git check-ignore -v <pfad>` | **exit 1, keine Regel** → **NICHT ignoriert** | **FACT** |
| R-4 | Physisch im Working Tree vorhanden? | `test -f` | **JA** | **FACT** |
| R-5 | Git-Status | `git status --porcelain` | `?? docs/milestone-1.0-sprint-plan.md` | **FACT** |
| R-6 | Lage des A1-EXEC-Vollzugs | — | **ausschließlich im Working Tree** | **FACT** |
| R-7 | Umfang der Datei | `wc -l` | **324 Zeilen** | **FACT** |
| R-8 | Autorisierte materielle Änderung | Z-1c-Record Kap. 4.1; A1-VERIFY | **ausschließlich Z. 6** | **FACT** |
| R-9 | Z. 7–9 und ausgeschlossene Stellen | A1-VERIFY Kap. 4 | **unverändert** (`1.0` / `R0` / `2026-08-09`; Z. 90, 276, 301–302) | **FACT** |

**Ergänzend (Beobachtung, keine Wertung):** Der untracked-Zustand ist repo-weit
kein Einzelfall — GDR-003 Kap. 7.3/7.4 klassifiziert insgesamt 53 + 11 Einträge
des Governance-/Doku-Bestands ebenso. Der Sprint Plan teilt diesen Zustand mit
u. a. `ADW-SPR-1.0-001` selbst.

---

## 4. Trennung: A1-EXEC-Vollzug vs. Erstversionierung

| Merkmal | **(A) A1-EXEC — materieller Vollzug** | **(B) Erstversionierung — technischer Akt** |
|---|---|---|
| Gegenstand | Inhaltliche Änderung Z. 6 `DRAFT` → autorisierter Wortlaut | Erstmalige Aufnahme der **bestehenden** Datei in Git |
| Autorisierung | Kette `3b76b89 … 5fd7919`, abgeschlossen | **nicht erteilt** — Gegenstand der vorbereiteten Human Decision |
| Umfang | **1 Datei, 1 Zeile** | **1 Datei, 324 Zeilen als `A` (new file)** |
| Zeitpunkt | bereits erfolgt, verifiziert | ausstehend, ggf. nie |
| Nachweis | A1-VERIFY (byte-exakter Abgleich Z. 6, direkte Lektüre Z. 7–9/90/276/301–302) | ein künftiger Versionierungs-Record + Commit |
| Governance-Charakter | Vollzug einer Statusnachführung (OD-08 Option a) | Dokumentenkontrolle / Repository-Integrität (GDR-003 Commit-2+-Scope) |

> **(A) und (B) sind verschiedene Akte.** (B) ist **kein** Bestandteil von (A)
> und war in keiner Welle der Kette autorisiert.

---

## 5. FACT / UNKNOWN / NOT SOURCE-DETERMINED

### FACT
1. Der Sprint Plan war **nie versioniert** (R-1, R-2).
2. Er ist **nicht** durch `.gitignore` ausgeschlossen (R-3); er existiert physisch (R-4).
3. Der **A1-EXEC wurde physisch korrekt vollzogen** und ist verifiziert (R-8, R-9).
4. Eine erstmalige Aufnahme in Git wäre technisch ein **`A` über die gesamte 324-zeilige Datei** (R-7).
5. GDR-003 klassifiziert den Sprint Plan als **SESSION-ARTEFACT → BASELINE-EXCLUDE** (G-1, G-2).
6. GDR-003 Z. 88: **keine genehmigte Quelle verlangt** die Aufnahme; die Versionierung ist ein **separater Governance-Commit-Scope** (G-3).
7. GDR-003 Z. 137 sieht diesen Scope als **optional, nachgelagert, durch separate Governance-Entscheidung** vor (G-4).
8. Der Development Standard v1.1 enthält **kein** Gebot, Planungsdokumente zu versionieren (Source Gate #10, Negativbefund).

### UNKNOWN / NOT SOURCE-DETERMINED
1. **V-Kern** — ob versioniert werden soll. GDR-003 sagt „optional" → **quellenseitig offen**.
2. **V2-a** — Form des Nachweises, dass materiell nur Z. 6 geändert wurde.
3. **V2-b** — Form der Dokumentation, dass die 324 Zeilen aus der Erstaufnahme stammen.
4. **V2-c** — ob ein eigener Versionierungs-Record erforderlich ist.
5. **V2-d** — zulässige minimale Change Surface eines späteren EXEC.
6. **Commit-Message-Konvention** für eine Erstaufnahme: der Development Standard §C normiert Präfixe (`feat`/`fix`/`docs`/`refactor`/`test`/`chore`), **nicht** aber eine Kennzeichnung „Erstversionierung/Bestandsaufnahme".
7. Ob mit dem Sprint Plan **weitere** Dateien des GDR-003-Scopes 7.3/7.4 gemeinsam aufzunehmen wären, oder isoliert nur dieser eine Pfad.

> **Zu 2.–7.:** Keine geprüfte Quelle bestimmt diese Punkte.
> **UNKNOWN / HUMAN DECISION REQUIRED.** Keine Analogie erfunden; keine
> allgemeine Git-Praxis als Norm dargestellt.

### AUSDRÜCKLICH NICHT ABGELEITET
```text
NICHT: Versionierung sei fuer eine "genehmigte Sprintplanung" materiell erforderlich.
NICHT: Versionierung erfuelle IP §10.6 Bedingung 7.
NICHT: Versionierung beantworte G7-b.
NICHT: Versionierung erledige HD-2.
NICHT: Versionierung stelle normativ eine "belastbare Planungsgrundlage" her.
NICHT: der untracked-Zustand sei ein Mangel, Fehler oder Verstoss.
NICHT: aus "optional" (GDR-003 Z. 137) folge eine Empfehlung in eine Richtung.
```

---

## 6. Optionsraum für die spätere Human Decision

Eng gehalten, aus GDR-003 Kap. 15 (Commit-2+-Scope) und dem Repository-Zustand
abgeleitet — **nicht künstlich erweitert**.

### 6.1 Hauptoptionen

| Option | Inhalt | Konsequenzen (FACT-nah, keine Wertung) |
|---|---|---|
| **V1 — NICHT VERSIONIEREN** | Der Sprint Plan bleibt untracked. Der vollzogene Zustand bleibt ausschließlich im Working Tree. | **Deckungsgleich mit dem Status quo nach GDR-003 Kap. 7.3** (BASELINE-EXCLUDE). Kein Commit, kein Nachweisproblem aus Kap. 7. **Risiko:** Der A1-EXEC-Vollzug existiert in keinem versionierten Zustand; `git clean -fd`, ein Checkout oder ein frischer Clone entfernen ihn ohne Spur, ohne dass dies in der Historie sichtbar würde. Wiederherstellung wäre nur über einen erneuten, erneut zu autorisierenden EXEC möglich. Der Nachweis des Vollzugs ruht allein auf A1-VERIFY (selbst ebenfalls nicht versioniert). |
| **V2 — ERSTMALIG VERSIONIEREN** | Der aktuell physisch vorliegende Sprint Plan wird erstmals in Git aufgenommen. Der Add ist ausdrücklich als **ERSTVERSIONIERUNG / BESTANDSAUFNAHME** zu bezeichnen, **nicht** als 324-zeilige materielle Änderung. | Entspricht dem in GDR-003 Z. 137 vorgesehenen **Commit-2+-Scope** („optional, nachgelagert, separate Governance-Entscheidung"). Vollzug wird verlustsicher. **Erfordert** die Klärung von V2-a…V2-d (Kap. 6.2). |

> **Vollständigkeit des Optionsraums:** Es wurde geprüft, ob eine dritte Option
> quellengetragen ist (z. B. Teilaufnahme, Aufnahme in einem anderen Zweig,
> Aufnahme des gesamten GDR-003-Scopes 7.3). **Ergebnis:** Keine Quelle trägt
> eine solche Option positiv; sie wird daher **nicht** künstlich hinzugefügt.
> Punkt 7 der UNKNOWN-Liste (Bündelung mit weiteren Dateien) ist als
> **Teilfrage von V2** geführt, nicht als eigene Hauptoption.

### 6.2 Teilfragen bei V2 — **sämtlich NICHT ENTSCHIEDEN**

| # | Frage | Status | Quellenlage |
|---|---|---|---|
| **V2-a** | Wie wird der Nachweis geführt, dass materiell **nur Z. 6** durch A1-EXEC geändert wurde? | **UNKNOWN / HUMAN DECISION REQUIRED** | Keine Quelle normiert eine Nachweisform. Verfügbares Material (nicht als Entscheidung, nur als Bestand benannt): A1-VERIFY mit byte-exaktem Abgleich; Z-1c-Record Kap. 4.1 mit der Sollzeile; dieser PREP Kap. 3 (R-8/R-9) |
| **V2-b** | Wie wird dokumentiert, dass die 324 Zeilen aus der **Erstaufnahme** und **nicht** aus dem A1-EXEC stammen? | **UNKNOWN / HUMAN DECISION REQUIRED** | Keine Quelle normiert dies. Denkbare Träger (nicht gewählt): Commit-Message, eigener Record, oder beides |
| **V2-c** | Soll ein **separater Governance-/Versionierungs-Record** Ausgangszustand, A1-VERIFY-Nachweis und Erstaufnahme-Commit verknüpfen? | **UNKNOWN / HUMAN DECISION REQUIRED** | Keine Quelle verlangt einen solchen Record. GDR-003 verlangt lediglich eine „separate Governance-Entscheidung", nicht ein bestimmtes Artefakt |
| **V2-d** | Welche **minimale Change Surface** ist für einen späteren EXEC zulässig? | **UNKNOWN / HUMAN DECISION REQUIRED** | Nicht quellenbestimmt. Kap. 9 stellt den **engstmöglichen** darstellbaren Rahmen dar — als Vorschlag zur Bestätigung, **nicht** als Festlegung |
| **V2-e** | Nur `docs/milestone-1.0-sprint-plan.md` oder gemeinsam mit weiteren Dateien des GDR-003-Scopes 7.3/7.4? | **UNKNOWN / HUMAN DECISION REQUIRED** | GDR-003 Z. 137 nennt 7.2/7.3/7.4 gemeinsam als Commit-2+-Scope, **ohne** eine Bündelung vorzuschreiben |
| **V2-f** | Commit-Präfix und Wortlaut der Commit-Message | **UNKNOWN / HUMAN DECISION REQUIRED** | Dev Standard §C normiert die Präfixmenge, **nicht** eine Kennzeichnung als Erstversionierung |

---

## 7. Das Nachweisproblem — „1 Zeile materiell vs. 324 Zeilen Erstaufnahme"

**Sachverhalt (FACT):**

- Materiell hat der A1-EXEC **genau eine Zeile** geändert: Z. 6, `DRAFT` → `APPROVED FOR SPRINT EXECUTION PLANNING (ADW-SPR-1.0-001)`.
- Da der Sprint Plan **nie** getrackt war, existiert **kein Vorzustand in Git**, gegen den ein Ein-Zeilen-Diff gebildet werden könnte.
- Eine spätere Erstaufnahme erschiene technisch als:

```text
new file:   docs/milestone-1.0-sprint-plan.md
324 lines added
```

**Fehlinterpretationsrisiko (ausdrücklich zu vermeiden):**

```text
FALSCH: "A1-EXEC hat 324 Zeilen geaendert."
FALSCH: "Der Erstaufnahme-Commit ist der A1-EXEC-Commit."
FALSCH: "Der Umfang des Git-Adds bemisst den Umfang des materiellen Vollzugs."

RICHTIG: A1-EXEC = 1 Datei / 1 Zeile (Z. 6), verifiziert.
RICHTIG: Erstaufnahme = separater technischer Akt ueber die gesamte
         bestehende Datei, unabhaengig vom materiellen Aenderungsumfang.
```

Die 324 Zeilen bemessen den **Bestand** der Datei, nicht den **Umfang der
Änderung**. Beide Tatsachen müssen in den Records getrennt nachvollziehbar
bleiben.

---

## 8. Mögliche Nachweisarchitektur für V2 — **Vorschlag, nicht Festlegung**

> Diese Kapitel-8-Darstellung ist ein **Vorschlag zur Bestätigung durch die
> Human Decision**. Sie ist **nicht** entschieden und **nicht** quellennormiert.

| # | Baustein | Inhalt |
|---|---|---|
| **NA-1** | **A1-VERIFY bleibt der Nachweis des materiellen Vollzugs** | genau eine Datei / genau eine Statuszeile / autorisierter Wortlaut, byte-exakt abgeglichen |
| **NA-2** | **Der Versionierungs-EXEC ist ein separater Akt** | erstmalige Aufnahme des **bereits bestehenden** Sprint Plans in Git |
| **NA-3** | **Keine rückwirkende Umdeutung** | Der spätere Commit darf **nicht** als A1-EXEC-Commit bezeichnet werden |
| **NA-4** | **Erkennbarkeit** | Der Commit muss ausdrücklich als **Erstversionierung / Bestandsaufnahme** erkennbar sein (Form: V2-b/V2-f — offen) |
| **NA-5** | **Umfangstrennung** | Der Commit kann technisch 324 neue Zeilen enthalten, obwohl der materielle A1-EXEC nur Z. 6 geändert hat |
| **NA-6** | **Getrennte Nachvollziehbarkeit** | Beide Tatsachen (NA-1, NA-5) müssen in den Records getrennt lesbar bleiben |
| **NA-7** | **Kein Sprint-Plan-Edit während PREP** | eingehalten — Kap. 10 N-2 |

**Offen innerhalb der Nachweisarchitektur:** ob NA-1…NA-6 durch einen eigenen
Record (V2-c), durch die Commit-Message (V2-b/V2-f) oder durch beides getragen
werden. **Nicht entschieden.**

---

## 9. Change Surface eines späteren Versionierungs-EXEC — **Vorschlag zur Bestätigung**

| Ebene | Gegenstand | Vorgeschlagene Zulässigkeit |
|---|---|---|
| **CS-V-1** | `git add docs/milestone-1.0-sprint-plan.md` — **unveränderter** aktueller Inhalt | **Kerngegenstand** — nur bei V2 |
| **CS-V-2** | Inhaltliche Änderung der Datei im Zuge der Aufnahme (auch „Kleinigkeiten", Formatierung, Zeilenenden) | **AUSGESCHLOSSEN** — die Aufnahme erfasst den **verifizierten** Zustand unverändert |
| **CS-V-3** | Ein begleitender Versionierungs-Record | **nur** falls V2-c ausdrücklich bejaht |
| **CS-V-4** | Weitere Dateien des GDR-003-Scopes 7.3/7.4 | **nur** falls V2-e ausdrücklich bejaht |
| **CS-V-5** | `CLAUDE.md` · `ROADMAP.md` · `docs/architecture-book-v2.md` · sonstige vorbestehende Working-Tree-Änderungen | **AUSGESCHLOSSEN** — dürfen nicht in den Commit gelangen |
| **CS-V-6** | ADRs · RDRs · Architecture Book · Implementation Plan · OD-05 · ADR-012 · Code · Tests · Config · Archive | **AUSGESCHLOSSEN** |
| **CS-V-7** | Push / PR / Merge / Tag | **AUSGESCHLOSSEN**, sofern nicht gesondert autorisiert |

**Engstmöglicher Umfang bei V2:** **eine** Datei im Commit (CS-V-1), Inhalt
**unverändert** gegenüber dem A1-VERIFY-Zustand.

---

## 10. Negative Checks (dieser PREP)

| # | Prüfung | Ergebnis |
|---|---|---|
| N-1 | Human Decision getroffen? | **NEIN** |
| N-2 | Sprint Plan verändert? | **NEIN** — ausschließlich gelesen |
| N-3 | Option gewählt? | **NEIN** — V1/V2 und V2-a…f offen |
| N-4 | `git add` / Commit / Push / PR / Merge / Tag? | **NEIN** |
| N-5 | Statusänderung? | **NEIN** |
| N-6 | Bedingung 7 bewertet? | **NEIN** — bleibt **NICHT ERFÜLLT**, unberührt |
| N-7 | U-4′ ausgelegt? | **NEIN** — bleibt **UNDETERMINED** |
| N-8 | HD-2 wiedervorgelegt oder entschieden? | **NEIN** — bleibt **DEFERRED / OPEN** |
| N-9 | G7-a / G7-b berührt? | **NEIN** |
| N-10 | OD-08 / A1-EXEC / A1-VERIFY neu bewertet? | **NEIN** — als gegeben übernommen |
| N-11 | Bestehende Governance-Datei verändert? | **NEIN** |
| N-12 | ADRs / RDRs / Architecture Book / Implementation Plan / `CLAUDE.md` / `ROADMAP.md` / Archive? | **NEIN** |
| N-13 | Code / Tests / Config? | **NEIN** |
| N-14 | Vorbestehende Working-Tree-Änderungen berührt? | **NEIN** — unangetastet |
| N-15 | Allgemeine Git-Praxis als Quellen-Norm dargestellt? | **NEIN** — Kap. 5 führt sie als NOT SOURCE-DETERMINED |
| N-16 | Analogie erfunden? | **NEIN** |
| N-17 | Optionsraum künstlich erweitert? | **NEIN** — Kap. 6.1 dokumentiert die Prüfung |
| N-18 | Nicht vorhandener Commit-Hash verwendet? | **NEIN** — alle neun readonly verifiziert (Kap. 1.1) |
| N-19 | Empfehlung als Entscheidung ausgegeben? | **NEIN** — Kap. 12 ist als **NON-BINDING** gekennzeichnet und vom Decision-Block getrennt |
| N-20 | RL-05 / Coding / QG-006 berührt? | **NEIN** |

**Negative Checks: alle PASS.**

---

## 11. Explicit Non-Decisions

```text
V1 / V2: KEINE Option gewaehlt.
V2-a / V2-b / V2-c / V2-d / V2-e / V2-f: NICHT entschieden — UNKNOWN.
Nachweisarchitektur Kap. 8: VORSCHLAG, NICHT festgelegt, NICHT quellennormiert.
Change Surface Kap. 9: VORSCHLAG zur Bestaetigung, NICHT festgelegt.
Sprint Plan: NICHT geaendert, NICHT versioniert, NICHT gestaged.
A1-EXEC / A1-VERIFY / OD-08: NICHT neu bewertet, NICHT umgedeutet.
Z-1 / Z-1b / Z-1c / Z-2 / Z-4: NICHT beruehrt.
U-4': NICHT ausgelegt — UNDETERMINED / HUMAN REVIEW REQUIRED.
G7-a: NICHT beruehrt. G7-b: NICHT beantwortet — OFFEN.
Bedingung 7: NICHT bewertet, NICHT abgesenkt — NICHT ERFUELLT; ACN-09 gewahrt.
HD-2: NICHT wiedervorgelegt, NICHT entschieden — DEFERRED / OPEN.
GDR-003: NICHT geaendert, NICHT umgedeutet — nur zitiert.
OP-1 / OP-2: NICHT beruehrt.
RL-05: NOT REACHED. Coding: NOT AUTHORIZED. QG-006 / QG-001..QG-008: NOT STARTED.
OD-05 / ADR-012 / ADRs / RDRs / Architecture Book / Implementation Plan /
      CLAUDE.md / ROADMAP.md / Code / Tests / Config / Archive: UNVERAENDERT.
Alle bestehenden Governance-Artefakte: NICHT ueberschrieben.
Vorbestehende Working-Tree-Aenderungen unangetastet. Kein Push, PR, Merge, Tag.
```

---

## 12. RECOMMENDATION — **NON-BINDING**

> **Ausdrücklich unverbindlich. Keine Entscheidung. Von Kapitel 13 strikt getrennt.**

| Position | Unverbindliche Empfehlung | Begründung |
|---|---|---|
| Hauptfrage | **V2** | Einziges konkretes, datiertes Risiko im aktuellen Zustand: Der verifizierte Vollzug einer neungliedrigen Autorisierungskette existiert in keinem versionierten Zustand und ist durch alltägliche Git-Operationen spurlos verlierbar (Kap. 6.1, V1-Risiko). GDR-003 Z. 137 sieht diesen Commit-Scope verfahrensmäßig ausdrücklich vor. |
| V2-c | **JA** — eigener Versionierungs-Record | Er ist der einzige Träger, der NA-1…NA-6 dauerhaft trennt; die Commit-Message allein trägt das Nachweisproblem aus Kap. 7 nicht. |
| V2-e | **isoliert**, nur `docs/milestone-1.0-sprint-plan.md` | Kleinste Change Surface; eine Bündelung mit dem übrigen GDR-003-Scope 7.3/7.4 wird von keiner Quelle verlangt und wäre eine eigene, größere Entscheidung. |

> **Diese Empfehlung ist keine Entscheidung.** Auch V1 ist governance-seitig
> vollständig zulässig — GDR-003 bezeichnet den Commit-2+-Scope ausdrücklich
> als **„optional"**.

---

## 13. HUMAN-DECISION-BLOCK (auszufüllen)

```text
JX-DEV-SPR01-RL05-G7-A1-SPVERS-DEC-01-R0

Authority:  Projekteigner / Governance
Date:       <YYYY-MM-DD>
Baseline:   HEAD 35beef9

ENTSCHEIDUNG ERFORDERLICH — PROJEKTEIGNER / GOVERNANCE

Frage:
Soll docs/milestone-1.0-sprint-plan.md, die bislang nie versioniert wurde,
erstmals unter Versionskontrolle genommen werden?

--- HAUPTOPTION (genau eine waehlen) ---

( ) V1 — NEIN, unversioniert belassen.
        Der vollzogene Zustand bleibt ausschliesslich im Working Tree.
        Das in Kap. 6.1 beschriebene Verlustrisiko wird bewusst getragen.

( ) V2 — JA, erstmals versionieren / Bestandsaufnahme des aktuell
        vollzogenen Zustands.

--- NUR FALLS V2: TEILENTSCHEIDUNGEN ---

V2-a  Nachweis, dass materiell nur Z. 6 geaendert wurde:
      ( ) A1-VERIFY genuegt
      ( ) zusaetzlich: <...>

V2-b  Dokumentation, dass die 324 Zeilen aus der Erstaufnahme stammen:
      ( ) in der Commit-Message
      ( ) in einem eigenen Record
      ( ) in beidem

V2-c  Separater Governance-/Versionierungs-Record, der Ausgangszustand,
      A1-VERIFY-Nachweis und Erstaufnahme-Commit verknuepft?
      ( ) JA        ( ) NEIN

V2-d  Change Surface des spaeteren EXEC:
      ( ) wie Kap. 9 vorgeschlagen (CS-V-1, Inhalt unveraendert)
      ( ) abweichend: <...>

V2-e  Umfang der Aufnahme:
      ( ) nur docs/milestone-1.0-sprint-plan.md
      ( ) zusaetzlich weitere Dateien des GDR-003-Scopes 7.3/7.4: <...>

V2-f  Commit-Message (Praefix + Wortlaut):
      <...>

--- BESTAETIGUNG DES NACHWEISRAHMENS (nur falls V2) ---

( ) Der Nachweisrahmen NA-1 bis NA-6 (Kap. 8) wird bestaetigt:
    materieller A1-EXEC (1 Zeile) und technische Erstaufnahme (324 Zeilen)
    bleiben getrennt nachvollziehbar; der Erstaufnahme-Commit wird NICHT
    rueckwirkend als A1-EXEC-Commit bezeichnet.

--- CONDITIONS ---

- Diese Entscheidung ist DEC, kein EXEC. Kein Vollzug in ihrer Welle.
- Ein Versionierungs-EXEC bedarf eines eigenen, separaten Auftrags.
- Der Sprint-Plan-INHALT wird bei der Aufnahme NICHT veraendert.
- Keine Bewertung von Bedingung 7, keine Auslegung von U-4', keine
  HD-2-Wiedervorlage, keine RL-05-/Coding-Freigabe.
- Vorbestehende Working-Tree-Aenderungen bleiben unangetastet und duerfen
  nicht in den Commit gelangen. Kein Push, PR, Merge, Tag.
```

---

## 14. Governance-State — unverändert

| Position | Status |
|---|---|
| **Sprint-Plan-Versionierung** | **OPEN — HUMAN DECISION REQUIRED** (V1/V2 und V2-a…f) |
| **A1-EXEC / OD-08** | **verifiziert korrekt vollzogen** (physisch, ungetrackt) |
| Sprint Plan physisch | `APPROVED FOR SPRINT EXECUTION PLANNING (ADW-SPR-1.0-001)` · `1.0` / `R0` / `2026-08-09` |
| **U-4′** | **UNDETERMINED / HUMAN REVIEW REQUIRED** |
| **G7-a / G7-b** | physisch adressiert / **OFFEN** |
| **IP §10.6 Bedingung 7** | **NICHT ERFÜLLT** |
| **HD-2** | **DEFERRED / OPEN / NOT DECIDED** |
| **OP-1 / OP-2** | **OFFEN** / **NICHT ERFÜLLT** |
| **RL-05 / CODING / QG-006** | **NOT REACHED** / **NOT AUTHORIZED** / **NOT STARTED** |
| **OD-05 / ADR-012 / ADRs / RDRs / Architecture Book / IP / `CLAUDE.md` / `ROADMAP.md` / Code / Tests / Config** | **UNVERÄNDERT** |

---

## 15. STOP

> **Nach Erstellung dieses PREP-Records: STOP.**
>
> Nicht automatisch: entscheiden · versionieren · `git add` · committen ·
> pushen · Sprint Plan ändern · Bedingung 7 bewerten · U-4′ auslegen ·
> HD-2 wiedervorlegen · RL-05 vorbereiten · Coding starten · QG-006 starten.
>
> **Nächster zulässiger Schritt:** genau eine Human Decision
> `JX-DEV-SPR01-RL05-G7-A1-SPVERS-DEC-01-R0` gemäß Block Kap. 13.

---

## 16. Revision History

| Revision | Datum | Änderung | Status |
|---|---|---|---|
| **R0** | 2026-08-13 | Entscheidungsvorbereitung zur Erstversionierung des Sprint Plans: Baseline Gate gegen HEAD `35beef9` mit readonly-Verifikation aller neun Kettencommits, Source Gate (11 Quellen, maßgeblicher GDR-003-Fund Z. 84/86/88/137), Repository-Befund R-1…R-9, Trennung A1-EXEC vs. Erstversionierung, FACT/UNKNOWN/NOT SOURCE-DETERMINED, Optionsraum V1/V2 mit Teilfragen V2-a…f, Nachweisproblem „1 vs. 324 Zeilen", Nachweisarchitektur NA-1…NA-7, Change Surface CS-V-1…7, Negative Checks N-1…N-20, unverbindliche Empfehlung, ausfüllbarer Human-Decision-Block | **COMPLETED — PREPARATION ONLY** |

---

**Ende JX-DEV-SPR01-RL05-G7-A1-SPVERS-PREP-01-R0 — Decision Preparation —
JOCHEN X Milestone 1.0 (2026-08-13) — HEAD `35beef9` — Bezugs-Baseline
`MILESTONE-1.0-BASELINE = 8fcf42f1997dfcf6ff232e75fd33c37b933991c8`**
