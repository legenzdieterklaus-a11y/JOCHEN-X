# JOCHEN X — Milestone 1.0
# JX-DEV-SPR01-RL05-G7-A1-SPVERS-DEC-01-R0 — Human Decision Record
## Erstversionierung des bislang unversionierten Sprint Plans

> **COMPLETED — DECISION ONLY · NO EXECUTION**
>
> Dieses Dokument zeichnet die **Human-Entscheidung des Projekteigners** zur
> Erstversionierung von `docs/milestone-1.0-sprint-plan.md` auf. Grundlage ist
> `JX-DEV-SPR01-RL05-G7-A1-SPVERS-PREP-01-R0`.
>
> **Gewählt: V2 — ERSTMALIG VERSIONIEREN.**
>
> **Diese Entscheidung autorisiert NICHT den tatsächlichen `git add` / Commit
> der Sprint-Plan-Datei.** Der Vollzug bedarf eines separaten Auftrags.
>
> **Sprint Plan = PHYSISCH UNVERÄNDERT und weiterhin UNGETRACKT** ·
> **A1-EXEC = verifiziert korrekt vollzogen** · **U-4′ = UNDETERMINED** ·
> **G7-b = OFFEN** · **IP §10.6 BEDINGUNG 7 = NICHT ERFÜLLT** ·
> **HD-2 = DEFERRED / OPEN** · **RL-05 = NOT REACHED** ·
> **CODING = NOT AUTHORIZED** · **QG-006 = NOT STARTED**

---

## 1. Baseline Gate

| Prüfung | Ergebnis |
|---|---|
| **HEAD** | `35beef98c4163e197243cc546fa4a273196611f6` = `35beef9` — „docs: record u-4-prime human decision (option c, no material interpretation)" — **exakt wie erwartet** |
| Staging vor Beginn | **leer** |
| Vorkette | `3b76b89 → a13a148 → fa6e192 → 8e51c33 → 9ec12d8 → 92b67e2 → 73988c5 → 5fd7919 → 35beef9` — **unverändert, im PREP readonly verifiziert** |
| **Sprint Plan — Git-Status** | `?? docs/milestone-1.0-sprint-plan.md` — **weiterhin ungetrackt** |
| **Sprint Plan — Kopf** | Z. 6 `APPROVED FOR SPRINT EXECUTION PLANNING (ADW-SPR-1.0-001)` · Z. 7 `1.0` · Z. 8 `R0` · Z. 9 `2026-08-09` — **unverändert, direkt gelesen** |
| Vorbestehende Working-Tree-Änderungen | `CLAUDE.md`, `ROADMAP.md`, `docs/architecture-book-v2.md` sowie sämtliche vorhandenen untracked Dateien — **unangetastet** |
| Ausgeführte Git-Schreiboperationen | **keine** — kein `git add`, kein `commit`, kein `restore`, kein `checkout` |
| Bezugs-Baseline | `MILESTONE-1.0-BASELINE = 8fcf42f1997dfcf6ff232e75fd33c37b933991c8` (GDR-003) |

**Baseline Gate: PASS.**

---

## 2. Source Gate (readonly)

Ausschließlich die bereits im PREP erhobenen Quellen; die entscheidungstragenden
Stellen wurden **erneut direkt gelesen**. Keine externe Quelle, keine Datei geschrieben.

| # | Quelle | Fundstelle | Erneut verifiziert |
|---|---|---|---|
| 1 | **GDR-003 — Baseline Identifier Decision** | `docs/governance/milestone-1.0-baseline-identifier-decision.md` Z. 84, 88, 137 | **JA — wörtlich** |
| 2 | **SPVERS-PREP-01** | `docs/audits/jx-dev-spr01-rl05-g7-a1-sprint-plan-versioning-prep-r0.md` | **gelesen, nicht verändert** |
| 3 | **Sprint Plan** | `docs/milestone-1.0-sprint-plan.md` Z. 6–9 | **gelesen, nicht verändert** |
| 4 | **A1-EXEC / A1-VERIFY** | Vollzugs- und Verifikationsberichte dieser Session | **als gegeben übernommen** |
| 5 | **Z-1c Decision Record** | `docs/audits/jx-dev-spr01-rl05-g7-a1-od08-z1c-decision-record-r0.md` Kap. 4.1 | **gelesen** |
| 6 | **U-4′ Decision Record** | `docs/audits/jx-dev-spr01-rl05-g7-b-u4-prime-decision-record-r0.md` (`35beef9`) | **gelesen** |
| 7 | **Repository-Zustand** | `git rev-parse` · `git diff --cached` · `git status` | **direkt erhoben** |

**Source Gate: PASS.**

---

## 3. GDR-003-Klassifikation — maßgeblicher Befund

| # | Fundstelle | Wortlaut / Inhalt | Klasse |
|---|---|---|---|
| G-1 | Z. 84 | Kapitel **7.3 SESSION-ARTEFACT (11 Dateien, diese Governance-/Sprint-Session) → BASELINE-EXCLUDE** | **FACT** |
| G-2 | Z. 86 | `docs/milestone-1.0-sprint-plan.md` ist in dieser Liste **namentlich enthalten** | **FACT** |
| G-3 | Z. 88 | „Governance-/Audit-/Planungsartefakte — **keine genehmigte Quelle verlangt ihre Aufnahme** in den Produkt-Baseline-Commit; **ihre Versionierung ist ein separater Governance-Commit-Scope**." | **FACT (wörtlich)** |
| G-4 | Z. 137 | „Commit 2+ — Governance-/Doku-Commits (**optional**, nachgelagert) \| Kap. 7.2, **7.3**, 7.4 \| **separate Governance-Entscheidung**" | **FACT (wörtlich)** |

**Ableitungen und Nicht-Ableitungen:**

| Prüfung | Ergebnis |
|---|---|
| Normieren die Quellen eine **Pflicht** zur Versionierung? | **NEIN** (G-3) — die Versionierung ist **optional** (G-4) |
| Ist der bisherige untracked-Zustand ein Mangel, Fehler oder Verstoß? | **NEIN** — er ist eine **dokumentierte, bewusste Klassifikation** (G-1, G-2) |
| Ist die hier getroffene Entscheidung verfahrensmäßig vorgesehen? | **JA** — sie ist genau die von G-4 vorgesehene „separate Governance-Entscheidung" über den Commit-2+-Scope |
| Folgt V2 aus den Quellen? | **NEIN** — die Quellen lassen V1 und V2 gleichermaßen zu. **V2 ist ein Willensakt des Projekteigners** |

---

## 4. Registrierter Optionsraum

| Option | Inhalt | Gewählt? |
|---|---|---|
| **V1 — NICHT VERSIONIEREN** | Der Sprint Plan bleibt außerhalb der Git-Historie | **NEIN** |
| **V2 — ERSTMALIG VERSIONIEREN** | Der bestehende Sprint Plan wird als **bestehendes Dokument** erstmalig in Git aufgenommen | **JA** |

Der Optionsraum ist **deckungsgleich** mit SPVERS-PREP-01 Kap. 6.1. **Nicht erweitert, nicht verändert.**

---

## 5. Human Authority

| Position | Angabe |
|---|---|
| **Entscheidende Instanz** | **Projekteigner / Governance** |
| Zuständigkeitsbeleg | GDR-003 Z. 137 („separate Governance-Entscheidung") |
| Datum | 2026-08-13 |
| Charakter | **DEC** — Governance-Entscheidung über Dokumentenkontrolle, **ohne** physischen Vollzug |
| Empfehlung als Entscheidung behandelt? | **NEIN** — SPVERS-PREP-01 Kap. 12 war ausdrücklich **NON-BINDING**; die Wahl ist ein eigenständiger Willensakt. Die inhaltliche Übereinstimmung ist Ergebnis, nicht Ursache |

---

## 6. HUMAN DECISION

```text
JX-DEV-SPR01-RL05-G7-A1-SPVERS-DEC-01-R0

Authority:  Projekteigner / Governance
Date:       2026-08-13
Baseline:   HEAD 35beef9

Frage:
Soll der bislang unversionierte Sprint Plan
(docs/milestone-1.0-sprint-plan.md) erstmalig unter Versionskontrolle
aufgenommen werden?

--- ENTSCHEIDUNG ---

    V2 — ERSTMALIG VERSIONIEREN

Der bestehende Sprint Plan wird als bestehendes Dokument erstmalig in
Git aufgenommen.

NICHT gewaehlt: V1.

--- CHARAKTER ---

Ausschliesslich eine Governance-Entscheidung ueber die Versionskontrolle
des BESTEHENDEN Sprint Plans. Keine inhaltliche Entscheidung.

--- DIESE ENTSCHEIDUNG BEDEUTET NICHT ---

    keine Aenderung des Inhalts
    keine erneute Aenderung von Z. 6
    keine Aenderung von Z. 7-9
    keine Aenderung von Z. 90
    keine Aenderung von Z. 276
    keine Aenderung von Z. 301-302
    keine Aenderung von Bedingung 7
    keine Entscheidung zu U-4'
    keine Entscheidung zu G7-b
    keine Entscheidung zu HD-2
    keine Coding-Freigabe
    keine RL-05-Freigabe
    keine QG-006-Freigabe

Der bereits physisch vollzogene A1-EXEC bleibt inhaltlich unveraendert.

--- VOLLZUG ---

Diese Entscheidung autorisiert NICHT den tatsaechlichen git add / Commit
der Sprint-Plan-Datei. Der Versionierungs-EXEC bedarf eines separaten
Auftrags.
```

---

## 7. Begründung der Entscheidung

| # | Begründung | Charakter |
|---|---|---|
| B-1 | Die Entscheidung ist die von **GDR-003 Z. 137** ausdrücklich vorgesehene **separate Governance-Entscheidung** über den Commit-2+-Scope. Sie wird damit im vorgesehenen Verfahren getroffen, nicht neben ihm | **verfahrensbezogen** |
| B-2 | Die Versionierung ist nach **GDR-003 Z. 88 / Z. 137 optional** und **nicht normativ erzwungen**. V1 wäre governance-seitig ebenso zulässig gewesen | **Quellenlage — trägt beide Optionen** |
| B-3 | **Bewusste Wahl für Nachvollziehbarkeit und Verlustschutz:** Der verifizierte A1-EXEC-Vollzug existiert derzeit ausschließlich im Working Tree und ist durch gewöhnliche Git-Operationen spurlos verlierbar. Die Aufnahme sichert den Nachweis dauerhaft | **Willensakt des Projekteigners** |
| B-4 | **Keine materielle Inhaltsänderung:** Aufgenommen wird der Bestand in exakt dem Zustand, den A1-VERIFY bestätigt hat | **Abgrenzung** |

> **B-3 ist der tragende Grund und ausdrücklich ein Willensakt** — er wird
> **nicht** als Ableitung aus den Quellen dargestellt. Die Quellen verlangen
> die Versionierung nicht (B-2).

---

## 8. Abgrenzung: Erstversionierung ≠ A1-EXEC

Die Erstversionierung ist ein **neuer Git-/Dokumentenkontrollakt**. Sie ist
**keine** Fortsetzung und **keine** nachträgliche Ausweitung des A1-EXEC.

| Merkmal | **A1-EXEC (materiell)** | **Erstversionierung (Dokumentenkontrolle)** |
|---|---|---|
| Change Surface | **eine Datei, eine Statuszeile** (Z. 6) | **eine bestehende Datei** wird erstmals als Repository-Datei aufgenommen |
| Physischer Vollzug | **bereits erfolgt** | **ausstehend** — nicht durch diese Decision autorisiert |
| VERIFY | **bereits erfolgt** (byte-exakter Abgleich) | steht aus |
| Autorisierung | Kette `3b76b89 … 5fd7919` | **dieser Record** (Entscheidung) + **separater EXEC-Auftrag** (Vollzug) |
| Inhaltliche Wirkung | Statuswert Z. 6 geändert | **keine** |

```text
MATERIELLER A1-EXEC:  1 Datei / 1 Zeile
VERSIONIERUNG:        1 bestehende Datei wird erstmals als
                      Repository-Datei aufgenommen
```

---

## 9. Nachweisproblem — technische Erstaufnahme vs. materieller Umfang

**FACT:** Da der Sprint Plan **nie** getrackt war, existiert kein Vorzustand in
Git, gegen den ein Ein-Zeilen-Diff gebildet werden könnte. Eine spätere
Erstaufnahme erscheint technisch als:

```text
new file:   docs/milestone-1.0-sprint-plan.md
324 lines added
```

**Verbindliche Lesart:**

```text
FALSCH: "A1-EXEC hat 324 Zeilen geaendert."
FALSCH: "Der Erstaufnahme-Commit ist der A1-EXEC-Commit."
FALSCH: "Der Umfang des Git-Adds bemisst den Umfang des materiellen Vollzugs."

RICHTIG: A1-EXEC = 1 Datei / 1 Zeile (Z. 6), verifiziert.
RICHTIG: Erstaufnahme = separater technischer Akt ueber die gesamte
         bestehende Datei — unabhaengig vom materiellen Aenderungsumfang.
RICHTIG: Die 324 Zeilen bemessen den BESTAND der Datei, nicht den
         UMFANG der Aenderung.
```

Beide Tatsachen bleiben in den Records **getrennt nachvollziehbar** (A1-VERIFY
für den materiellen Vollzug, ein künftiger Versionierungs-EXEC für die Aufnahme).

---

## 10. Offene Teilfragen — **NICHT entschieden**

> Der Auftrag beschränkt diese Welle ausdrücklich auf die Hauptfrage V1/V2.
> Die im PREP Kap. 6.2 registrierten Teilfragen bleiben daher **offen** und
> sind **vor oder mit** dem Versionierungs-EXEC zu klären.

| # | Teilfrage | Status |
|---|---|---|
| **V2-a** | Nachweisform, dass materiell nur Z. 6 geändert wurde | **OFFEN — HUMAN DECISION REQUIRED** |
| **V2-b** | Dokumentationsform, dass die 324 Zeilen aus der Erstaufnahme stammen | **OFFEN** |
| **V2-c** | Eigener Versionierungs-Record erforderlich? | **OFFEN** |
| **V2-d** | Minimale Change Surface des EXEC | **OFFEN** — PREP Kap. 9 (CS-V-1…7) liegt als **Vorschlag** vor, **nicht bestätigt** |
| **V2-e** | Nur der Sprint Plan oder weitere Dateien des GDR-003-Scopes 7.3/7.4 | **OFFEN** |
| **V2-f** | Commit-Präfix und Wortlaut der Commit-Message | **OFFEN** |

**Kein Wert erfunden, keine Teilfrage stillschweigend beantwortet.**

---

## 11. Negative Checks

| # | Prüfung (vor **und** nach Erstellung) | Ergebnis |
|---|---|---|
| N-1 | Sprint Plan verändert? | **NEIN** — Z. 6–9 vor und nach Erstellung gelesen, identisch |
| N-2 | Sprint Plan gestaged oder committet? | **NEIN** — weiterhin `??` |
| N-3 | `git add` ausgeführt? | **NEIN** |
| N-4 | `git restore` / `git checkout` / sonstige Git-Schreiboperation am Sprint Plan? | **NEIN** |
| N-5 | Andere Datei als der Decision Record verändert? | **NEIN** |
| N-6 | Push / PR / Merge / Tag? | **NEIN** |
| N-7 | A1-EXEC erneut ausgeführt? | **NEIN** |
| N-8 | VERIFY erneut ausgeführt? | **NEIN** |
| N-9 | Coding gestartet? | **NEIN** — **NOT AUTHORIZED** |
| N-10 | Statusänderung bei Bedingung 7? | **NEIN** — **NICHT ERFÜLLT**, unberührt; ACN-09 gewahrt |
| N-11 | U-4′ ausgelegt? | **NEIN** — **UNDETERMINED** |
| N-12 | HD-2 entschieden oder wiedervorgelegt? | **NEIN** — **DEFERRED / OPEN** |
| N-13 | OD-05 geändert? | **NEIN** |
| N-14 | ADR-012 geändert? | **NEIN** |
| N-15 | PREP-Artefakt verändert? | **NEIN** — nur gelesen |
| N-16 | GDR-003 verändert oder umgedeutet? | **NEIN** — nur zitiert |
| N-17 | Vorbestehende Working-Tree-Änderungen berührt? | **NEIN** — unangetastet, nicht im Commit |
| N-18 | Optionsraum erweitert? | **NEIN** — exakt V1/V2 |
| N-19 | Teilfrage V2-a…f stillschweigend entschieden? | **NEIN** — sämtlich als OFFEN geführt |
| N-20 | Entscheidung als quellennormiert dargestellt? | **NEIN** — B-2/B-3: Willensakt bei quellenseitig offener Lage |
| N-21 | Vollzug (`git add` des Sprint Plans) autorisiert? | **NEIN** — ausdrücklich nicht (Kap. 12) |

**Negative Checks: alle PASS.**

---

## 12. Ausdrückliche Feststellung zum Vollzug

> **Diese Entscheidung autorisiert noch NICHT den tatsächlichen `git add` /
> Commit der Sprint-Plan-Datei.**
>
> Entschieden ist ausschließlich das **Ob** (V2). Der **Vollzug** bedarf eines
> eigenen, separat zu beauftragenden Versionierungs-EXEC — und setzt die
> Klärung der in Kap. 10 offenen Teilfragen voraus.

---

## 13. Explicit Non-Decisions

```text
Vollzug: NICHT autorisiert. Kein git add, kein Commit des Sprint Plans.
V2-a bis V2-f: NICHT entschieden — OFFEN.
Change Surface des EXEC: NICHT bestaetigt (PREP Kap. 9 bleibt Vorschlag).
Sprint Plan: NICHT geaendert, NICHT versioniert, NICHT gestaged.
A1-EXEC / A1-VERIFY: NICHT neu bewertet, NICHT umgedeutet, NICHT ausgeweitet.
Z-1 / Z-1b / Z-1c / Z-2 / Z-4: NICHT beruehrt.
U-4': NICHT ausgelegt — UNDETERMINED / HUMAN REVIEW REQUIRED.
G7-a: NICHT beruehrt. G7-b: NICHT beantwortet — OFFEN.
Bedingung 7: NICHT bewertet, NICHT abgesenkt — NICHT ERFUELLT; ACN-09 gewahrt.
HD-2: NICHT entschieden, NICHT wiedervorgelegt — DEFERRED / OPEN.
OP-1 / OP-2: NICHT beruehrt.
OD-05 / ADR-012 / ADRs / RDRs / Architecture Book / Implementation Plan /
      CLAUDE.md / ROADMAP.md / Code / Tests / Config / Archive: UNVERAENDERT.
GDR-003 / SPVERS-PREP-01: NICHT geaendert — nur gelesen und zitiert.
RL-05: NOT REACHED. Coding: NOT AUTHORIZED. QG-006 / QG-001..QG-008: NOT STARTED.
Vorbestehende Working-Tree-Aenderungen unangetastet. Kein Push, PR, Merge, Tag.
```

---

## 14. Governance State nach dieser Decision

| Position | Status |
|---|---|
| **Sprint Plan** | `APPROVED FOR SPRINT EXECUTION PLANNING (ADW-SPR-1.0-001)` · Version `1.0` · Revision `R0` · Datum `2026-08-09` |
| **Versionierung** | **DECIDED — V2** · **EXEC AUSSTEHEND** · Teilfragen V2-a…f **OFFEN** |
| **A1-EXEC** | **VERIFIZIERT — korrekt vollzogen** |
| **U-4′** | **UNDETERMINED** |
| **G7-a** | **physisch adressiert** |
| **G7-b** | **OFFEN** |
| **IP §10.6 Bedingung 7** | **NICHT ERFÜLLT** |
| **HD-2** | **DEFERRED / OPEN / NOT DECIDED** |
| **OP-1** | **OFFEN** |
| **OP-2** | **NICHT ERFÜLLT** |
| **RL-05** | **NOT REACHED** |
| **CODING** | **NOT AUTHORIZED** |
| **QG-006** | **NOT STARTED** |
| **OD-05 / ADR-012 / ADRs / RDRs / Architecture Book / IP / `CLAUDE.md` / `ROADMAP.md` / Code / Tests / Config** | **UNVERÄNDERT** |

---

## 15. Change Surface dieser Welle

| Gegenstand | Umfang |
|---|---|
| Neue Dateien | **genau eine** — `docs/audits/jx-dev-spr01-rl05-g7-a1-sprint-plan-versioning-decision-record-r0.md` |
| Geänderte / gelöschte Dateien | **keine** |
| Sprint Plan | **nur gelesen** — unverändert, ungetrackt |
| PREP-Artefakt | **nur gelesen** |
| Bestehende Governance-Artefakte | **UNBERÜHRT** |
| Code / Tests / Config | **UNBERÜHRT** |
| Vorbestehende Working-Tree-Änderungen | **UNANGETASTET** |

---

## 16. Next Step

> **Separat zu beauftragender Versionierungs-EXEC:**
> `JX-DEV-SPR01-RL05-G7-A1-SPVERS-EXEC-01-R0`
>
> Voraussetzung: Klärung der in Kap. 10 offenen Teilfragen **V2-a bis V2-f**,
> insbesondere der Change Surface (V2-d) und der Commit-Message (V2-f).

**STOP NACH DIESEM ARTEFAKT. Nicht automatisch mit der Erstversionierung beginnen.**

---

## 17. Revision History

| Revision | Datum | Änderung | Status |
|---|---|---|---|
| **R0** | 2026-08-13 | Human Decision zur Sprint-Plan-Versionierung: **V2 — ERSTMALIG VERSIONIEREN**; Baseline Gate gegen HEAD `35beef9`, Source Gate mit erneuter GDR-003-Verifikation (Z. 84/88/137), Optionsraum V1/V2, Begründung B-1…B-4, Abgrenzung Erstversionierung ≠ A1-EXEC, Nachweisproblem, Teilfragen V2-a…f als OFFEN geführt, Negative Checks N-1…N-21, ausdrückliche Feststellung: Vollzug nicht autorisiert | **COMPLETED — DECISION ONLY** |

---

**Ende JX-DEV-SPR01-RL05-G7-A1-SPVERS-DEC-01-R0 — Human Decision Record —
JOCHEN X Milestone 1.0 (2026-08-13) — HEAD `35beef9` — Bezugs-Baseline
`MILESTONE-1.0-BASELINE = 8fcf42f1997dfcf6ff232e75fd33c37b933991c8`**
