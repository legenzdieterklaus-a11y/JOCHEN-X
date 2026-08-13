# JOCHEN X — Milestone 1.0
# JX-DEV-SPR01-RL05-G7-A1-OD08-Z12-PREP-01-R0 — Decision Preparation
## Z-1 (Zielstatus) und Z-2 (kontrolliertes Verfahren) für die autorisierte OD-08-Nachführung

> **COMPLETED — PREPARATION ONLY · NO DECISION**
>
> **Warum PREP und nicht DEC:** Der Auftrag lässt ein Decision Record nur zu,
> „falls bereits vollständig durch den Projekteigner vorgegeben". Für **Z-1
> wurde kein Zielwert vorgegeben** — im Gegenteil: das Erfinden oder
> Übertragen eines Wertes ist ausdrücklich untersagt. Diese Welle bereitet
> daher die noch fehlende Entscheidung vor und stellt den ausfüllbaren
> HUMAN-DECISION-Block für **JX-DEV-SPR01-RL05-G7-A1-OD08-Z12-DEC-01-R0**
> bereit.
>
> **A1-EXEC = NOCH NICHT AUTORISIERT** · **Sprint Plan = PHYSISCH UNVERÄNDERT
> (DRAFT / 1.0 / R0)** · **IP §10.6 BEDINGUNG 7 = WEITERHIN NICHT ERFÜLLT** ·
> **RL-05 = NOT REACHED** · **CODING = NOT AUTHORIZED** · **QG-006 = NOT STARTED** ·
> **U-4′ = UNDETERMINED / HUMAN REVIEW REQUIRED** · **HD-2 = DEFERRED / OPEN / NOT DECIDED**

---

## 1. Baseline Gate

| Prüfung | Ergebnis |
|---|---|
| **HEAD** | `9ec12d8e3a51e6b23e5bf14772300af97d9ea70e` = `9ec12d8` — „docs: record OD-08 decision option a (status update authorized)" |
| **Erwartete Vorkette** | `3b76b89` → `a13a148` → `fa6e192` → `8e51c33` → `9ec12d8` — **alle fünf als Vorfahren verifiziert** |
| Staging vor Beginn | **leer** |
| Produktiver Baum vs. `8fcf42f` (`app core sdk ui config tests src`) | **0 Dateien** — baseline-identisch |
| **Sprint Plan Kopf** | Z. 6 `Status \| **DRAFT**` · Z. 7 `Version \| 1.0` · Z. 8 `Revision \| R0` · Z. 9 `Datum \| 2026-08-09` — **unverändert, direkt verifiziert** |
| Working Tree | 3 vorbestehende getrackte Modifikationen (`CLAUDE.md`, `ROADMAP.md`, `docs/architecture-book-v2.md`) + untracked Dokumente — **unangetastet** |
| Bezugs-Baseline | `MILESTONE-1.0-BASELINE = 8fcf42f1997dfcf6ff232e75fd33c37b933991c8` (GDR-003) |

**Baseline Gate: PASS.**

---

## 2. Source Gate (readonly)

| # | Quelle | Fundstelle | Ergebnis |
|---|---|---|---|
| 1 | **OD-08-DEC** (Option a) | `…-g7-a1-od08-decision-record-r0.md` (`9ec12d8`) | **gelesen** — Nachführung dem Grunde nach autorisiert, Z-1/Z-2 offen |
| 2 | **OD-08-PREP** | `…-g7-a1-od08-prep-r0.md` (`8e51c33`) Kap. 8, 9 | **gelesen** |
| 3 | **MEP §20 OD-08** | `jochen-x-master-engineering-plan-r0.md` Z. 2056–2064 | **gelesen** |
| 4 | **DEM §1.1 / §366** | `jochen-x-decision-execution-matrix-r0.md` Z. 109, 366 | **gelesen** |
| 5 | **ADW-SPR-1.0-001** | `milestone-1.0-sprint-planning-approval-decision-op1.md` Kap. 17, 18, Z. 21 | **gelesen** |
| 6 | **Development Standard v1.1 §17 Anh. A/B** | `development-standard-v1.1.md` Z. 740–800 | **vollständig gelesen** |
| 7 | **Sprint Plan** | `milestone-1.0-sprint-plan.md` Z. 6–9, 83, 276, 301–302 | **gelesen** |
| 8 | **IP §10.4 W-1…W-8 · §10.6 · §10.9 ACN-09** | `milestone-1.0-implementation-plan.md` Z. 3375–3392, 3499–3543, 3700 | **gelesen** |
| 9 | **PREP-02** | `jx-dev-spr01-rl05-final-prep-02-r0.md` Z. 444, 596 | **gelesen** |
| 10 | **G7-DEC-01** | `jx-dev-spr01-rl05-g7-decision-record-r0.md` Z. 144 (Condition 8) | **gelesen** |
| 11 | **G7-PREP-01** | `jx-dev-spr01-rl05-g7-prep-r0.md` Kap. 5 (A1-1…A1-10) | **gelesen** |
| 12 | **Charter** | `milestone-1.0-charter.md` Z. 5 | **gelesen** (Statuswert-Konvention) |

Keine externe Quelle. Keine Datei geschrieben.

**Source Gate: PASS**

---

## 3. Z-1 — Quellenbefund (Zielstatus für Sprint Plan Z. 6)

| # | Prüfpunkt | Befund | Klasse |
|---|---|---|---|
| Z1-Q1 | Statusmodell für ein **Sprint-Plan-Dokument** | **Existiert nicht.** Dev Standard v1.1 §17 Anh. B kennt States nur für **ADR** (`Open → Accepted \| Resolved by ADR-XXX`), **Specification** (`Draft → In Review → Corrections → Approved`), **Sprint** (`Planned → In Progress → Review → Done`), **Release** (`Candidate → Verified → Released`) | **FACT (Negativbefund)** |
| Z1-Q2 | Nennt eine Quelle einen **Zielwert** für Z. 6? | **NEIN** — keine der 12 geprüften Quellen | **FACT (Negativbefund)** |
| Z1-Q3 | **IP §10.4 W-7** | Normiert wörtlich einen Statuswechsel „**Überführung des Dokumentstatus DRAFT → APPROVED**". **Bezugsobjekt ist der Implementation Plan** (Kap. 10 = dessen eigener Approval Workflow, W-1…W-8) | **FACT** (Wortlaut) / **NICHT ÜBERTRAGBAR** ohne Analogie |
| Z1-Q4 | Hausübliche Statuswerte anderer Dokumente | Charter Z. 5 `APPROVED` · Implementation Plan Z. 3 `APPROVED` · Architecture Book `APPROVED / FROZEN` | **FACT** (Beobachtung) / **KEINE NORM** für den Sprint Plan |
| Z1-Q5 | Selbstaussage des Sprint Plans | Z. 276: „Genehmigte Sprintplanung liegt vor \| **PENDING** — dieser Plan ist DRAFT; **Genehmigung durch Projekteigner ausstehend**"; Z. 83: „[G] genehmigter Sprint Plan (**dieses Dokument nach Genehmigung**)" | **FACT (wörtlich)** — benennt die **Kategorie** „Genehmigung", **nicht** einen Feldwert |
| Z1-Q6 | Was ADW-SPR-1.0-001 tatsächlich genehmigt hat | Kap. 17 wörtlich: genehmigt ist „**ausschließlich die Verwendung des Sprint Plans 1.0 R0 als Planungsgrundlage**"; „Der physische Status … bleibt **DRAFT / 1.0 / R0**" | **FACT (wörtlich)** |
| Z1-Q7 | Status von OP-1 im Sprint Plan | Z. 301: „OP-1 … **Genehmigung dieses Sprint Plans (Coding-Bedingung 7)** … **OFFEN** … Projekteigner-Genehmigung" | **FACT** |

> ## **Z-1 = UNKNOWN / HUMAN DECISION REQUIRED**
>
> Kein Zielstatuswert ist quellennormiert. Jede Ableitung aus W-7, aus der
> Hauskonvention oder aus den ADR-/Specification-/Sprint-/Release-Modellen
> wäre **Analogie = Festlegung**, keine Feststellung — und ist nach der
> Human Decision `…-OD08-DEC-01-R0` ausdrücklich untersagt.

### 3.1 Entscheidungsrelevante Teilfrage **Z-1b** (nicht entschieden)

Ein Zielwert `APPROVED` (oder gleichwertig) würde **mehr** aussagen als
ADW-SPR-1.0-001 erteilt hat (Z1-Q6) und stünde neben der noch offenen
Position **OP-1** (Z1-Q7) sowie neben der Sprint-Plan-Selbstaussage
„Genehmigung ausstehend" (Z1-Q5).

| Frage Z-1b | Status |
|---|---|
| Soll der neue Statuswert **exakt** abbilden, was ADW-SPR-1.0-001 erteilt hat (Planungsgrundlage), **oder** eine darüber hinausgehende Dokumentgenehmigung ausdrücken? | **NICHT ENTSCHIEDEN — HUMAN DECISION** |
| Falls Letzteres: Wäre dafür ein **eigener Genehmigungsakt** (analog IP §10.4 W-6/W-7) erforderlich? | **NICHT QUELLENBESTIMMT** |
| Darf aus dem Statuswert eine Erfüllung von OP-1 oder von IP §10.6 Nr. 7 abgeleitet werden? | **NEIN** — das wäre eine Absenkung/Umgehung i. S. v. **ACN-09** und ist ausgeschlossen |

---

## 4. Z-2 — Quellenbefund (kontrolliertes Verfahren)

| # | Prüfpunkt | Befund | Klasse |
|---|---|---|---|
| Z2-Q1 | Wortlaut | MEP §20 OD-08 Option (a): „Kopf im **vorgesehenen kontrollierten Verfahren** nachführen" — benennt das Verfahren **nicht** | **FACT** |
| Z2-Q2 | Vorgabe zur **Form** des Vollzugs | ADW-SPR-1.0-001 Kap. 17: Statusnachführung nur in einem „**separat autorisierten Schritt**" | **FACT (wörtlich)** |
| Z2-Q3 | Konkretisierung dieses Schritts | **PREP-02 Z. 444** klassifiziert **als FACT**: „→ **eigener PREP/DEC/EXEC-Zyklus** mit Änderung einer Bestandsdatei"; **PREP-02 Z. 596**: A1 = „eigener PREP → DEC → **EXEC** (berührt eine Bestandsdatei)" | **FACT** |
| Z2-Q4 | Verbindliche Sperre | **G7-DEC-01 Condition 8** (Z. 144): „Keine Änderung des Sprint Plans **ohne separaten EXEC-Auftrag**" | **FACT (wörtlich)** |
| Z2-Q5 | Ist damit ein Verfahren bestimmbar? | **JA, im Kern** — der prozedurale Rahmen **PREP → DEC → EXEC mit separater Autorisierung** ist quellenbelegt und in dieser Kette durchgehend praktiziert (`3b76b89` → `a13a148` → `fa6e192` → `8e51c33` → `9ec12d8`) | **FACT** |
| Z2-Q6 | Was bleibt offen? | Ob **über** diesen Zyklus hinaus ein **förmlicher Genehmigungs-/Dokumentenkontrollakt** (analog IP §10.4 W-6/W-7) erforderlich ist. Dazu existiert **keine positive Norm** für den Sprint Plan | **UNKNOWN (Negativbefund)** |

> ## **Z-2 = TEILWEISE QUELLENBESTIMMT**
>
> **Bestimmt (FACT):** separat autorisierter Schritt in Form eines
> PREP → DEC → **EXEC**-Zyklus.
> **Offen (UNKNOWN):** ob zusätzlich ein förmlicher Genehmigungsakt
> erforderlich ist. **Diese Restfrage bedarf einer Human Decision** —
> ihre Beantwortung darf nicht aus dem Schweigen der Quellen abgeleitet
> werden.

---

## 5. FACT / UNKNOWN / INFERENCE

### FACT

1. Dev Standard v1.1 §17 Anh. B definiert **kein** Statusmodell für ein Sprint-Plan-Dokument.
2. Keine Quelle nennt einen **Zielwert** für Sprint Plan Z. 6.
3. IP §10.4 W-7 normiert „DRAFT → APPROVED" — **für den Implementation Plan**.
4. ADW-SPR-1.0-001 Kap. 17 genehmigt **ausschließlich die Verwendung als Planungsgrundlage**; physischer Status bleibt DRAFT.
5. Sprint Plan Z. 276 führt Bedingung 7 als **PENDING**, „Genehmigung durch Projekteigner ausstehend"; Z. 301 führt **OP-1 als OFFEN**.
6. Der Vollzug ist ein „separat autorisierter Schritt" (ADW-SPR-1.0-001 Kap. 17), konkretisiert als **eigener PREP/DEC/EXEC-Zyklus** (PREP-02 Z. 444/596) und gesperrt durch **G7-DEC-01 Condition 8**.
7. OD-08 ist mit **Option (a)** entschieden; die Nachführung ist **dem Grunde nach** autorisiert, ohne Zielwert.
8. IP §10.9 **ACN-09** verbietet jede Absenkung bestehender Bedingungen.

### UNKNOWN

1. **Z-1** — konkreter Zielstatuswert für Z. 6.
2. **Z-1b** — Bedeutungsreichweite des neuen Status (Planungsgrundlage vs. Dokumentgenehmigung) und ggf. erforderlicher eigener Genehmigungsakt.
3. **Z-4** — Behandlung von `Version` / `Revision` / `Datum` (Z. 7–9).
4. **Z-2 Restfrage** — förmlicher Genehmigungs-/Dokumentenkontrollakt zusätzlich erforderlich?
5. Form und Instanz einer späteren Feststellung „G7-a beseitigt".

### INFERENCE (nicht als Norm verwendet)

1. Die Hauskonvention `APPROVED` (Charter, IP, Architecture Book) legt einen Kandidatenwert **nahe** — sie normiert ihn **nicht** für den Sprint Plan.
2. PREP-02 Z. 596 beschreibt das Ziel als „genehmigter Stand" — eine **Beschreibung**, kein normierter Feldwert.
3. Dass der PREP/DEC/EXEC-Zyklus **allein** genügt, ist plausibel (Präzedenz der gesamten Kette), aber **nicht positiv normiert** (Z2-Q6).

---

## 6. Zulässige Entscheidungsoptionen

### 6.1 Z-1 — Zielstatus (genau eine Option zu wählen)

| Option | Inhalt | Bewertung |
|---|---|---|
| **Z1-A** | Z. 6 → `APPROVED` (Hauskonvention, analog IP §10.4 W-7) | Kandidatenwert; **sagt mehr aus als ADW-SPR-1.0-001 erteilt hat** (Z1-Q6); wirft Z-1b und das Verhältnis zu OP-1 auf |
| **Z1-B** | Z. 6 → ein Wert, der **exakt** das Erteilte abbildet, z. B. `APPROVED AS PLANNING BASIS (ADW-SPR-1.0-001)` bzw. `Als Planungsgrundlage genehmigt (ADW-SPR-1.0-001)` | Quellentreu; keine Über-Aussage; OP-1 und Bedingung 7 bleiben erkennbar offen |
| **Z1-C** | Z. 6 bleibt `DRAFT`, Nachführung erfolgt als **ergänzender Genehmigungsvermerk** im Kopf | Deckt „Kopf nachführen" wörtlich ab, ohne Statuswortwechsel; **ob das Option (a) genügt, ist Auslegung** — vom Projekteigner mitzuentscheiden |
| **Z1-D** | Zunächst **eigener förmlicher Genehmigungsakt** (analog IP §10.4 W-6/W-7), danach Statuswert aus diesem Akt | Höchste Zeremonie; klärt Z-1b vollständig; verschiebt den Vollzug um eine Welle |

**Zusatzfrage Z-4 (immer mitzuentscheiden):** `Version` / `Revision` / `Datum`
(Z. 7–9) — **unverändert lassen** oder **konkrete Werte** festlegen.

### 6.2 Z-2 — Verfahren (genau eine Option zu wählen)

| Option | Inhalt | Bewertung |
|---|---|---|
| **Z2-A** | Das „kontrollierte Verfahren" **ist** der quellenbelegte PREP → DEC → **EXEC**-Zyklus mit separater Autorisierung; ein weiterer förmlicher Akt ist **nicht** erforderlich | Deckungsgleich mit Z2-Q2/Q3/Q4; schließt die Restfrage Z2-Q6 durch **Festlegung** |
| **Z2-B** | Zusätzlich ist ein **förmlicher Genehmigungs-/Dokumentenkontrollakt** erforderlich (analog IP §10.4 W-6/W-7) | Höhere Zeremonie; koppelt Z-2 an Z1-D |
| **Z2-C** | Ausgestaltung eines **eigenen, neu zu definierenden Verfahrens** | Größter Aufwand; von keiner Quelle verlangt |

### 6.3 Bündelbarkeit von Z-1 und Z-2 (Auftragspunkt 9)

| Prüfung | Ergebnis |
|---|---|
| Verlangt eine Quelle getrennte Entscheidungen? | **NEIN** — kein Trennungsgebot in einer der 12 Quellen | **FACT (Negativbefund)** |
| Gleiche Autorität? | **JA** — Projekteigner / Governance für beide [MEP §20 OD-08; DEM §1.1 Z. 109] | **FACT** |
| Gleicher Gegenstand? | **JA** — beide sind Vollzugsvoraussetzungen **derselben** bereits getroffenen Entscheidung (OD-08 Option a) | **FACT** |
| Präzedenz für Bündelung? | **JA** — DEC-02 bündelt 10 Details + 9 Conditions in **einem** Record | **FACT** |
| Wird durch Bündelung eine Bedingung abgesenkt? | **NEIN** — Prüftiefe, Nachweispflicht und ACN-09 bleiben unverändert; nur die Zahl der Wellen sinkt | **FACT** |

> **Ergebnis: Z-1 und Z-2 können und sollen in EINER Human Decision
> entschieden werden** — weniger Zeremonie bei unveränderter
> Governance-Härte. Dies ist eine **Feststellung zur Zulässigkeit**,
> keine Entscheidung.

---

## 7. Change Surface des späteren A1-EXEC

**Diese Welle ändert nichts.** Vorabgrenzung für einen künftigen,
separat zu autorisierenden A1-EXEC:

| Ebene | Gegenstand | Zulässigkeit |
|---|---|---|
| **CS-A1-1** | `docs/milestone-1.0-sprint-plan.md` **Z. 6** | **Kerngegenstand** — zulässig **erst nach Festlegung von Z-1** |
| **CS-A1-2** | Z. 7 `Version` · Z. 8 `Revision` · Z. 9 `Datum` | **Nur** bei ausdrücklicher Festlegung (Z-4); sonst unverändert |
| **CS-A1-3** | Z. 301 `OP-1` · Z. 302 `OP-2` | **NICHT Gegenstand** — von keiner Quelle verlangt |
| **CS-A1-4** | Z. 90 · Z. 276 (Bedingungs-/PENDING-Zeilen) | **NICHT Gegenstand** — eine Nachführung von Z. 276 würde Bedingung 7 berühren und ist **ausgeschlossen** |
| **CS-A1-5** | Inhaltliche Fortschreibung (insb. OD-05-Umriss) | **AUSGESCHLOSSEN** — Gegenstand von U-4′/HD-2 |
| **CS-A1-6** | OD-05 · ADR-012 · ADRs/RDRs · Architecture Book · Implementation Plan · `CLAUDE.md` · `ROADMAP.md` · Code · Tests · Config | **AUSGESCHLOSSEN** |
| **CS-A1-7** | Bestehende Governance-/Archivdateien | **AUSGESCHLOSSEN** (kein Umschreiben) |

**Maximaler Umfang eines künftigen A1-EXEC:** **eine** geänderte Datei,
Kopfzeile Z. 6 (zwingend) und Z. 7–9 (nur bei ausdrücklicher Festlegung).

---

## 8. Explicit Non-Decisions

```text
Z-1: NICHT festgelegt, NICHT erfunden, NICHT aus ADR-/Specification-/Sprint-/
     Release-Statusmodellen uebertragen, NICHT aus IP §10.4 W-7 analogisiert,
     NICHT aus der Hauskonvention abgeleitet — UNKNOWN / HUMAN DECISION REQUIRED.
Z-1b: Bedeutungsreichweite des Zielstatus NICHT entschieden.
Z-4: Version / Revision / Datum NICHT disponiert.
Z-2: Restfrage (zusaetzlicher foermlicher Genehmigungsakt) NICHT entschieden;
     der prozedurale Rahmen ist quellenbelegt, NICHT neu erfunden.
Optionen Z1-A..D / Z2-A..C: dargestellt, KEINE davon gewaehlt.
Empfehlung: unverbindlich, KEINE Entscheidung, KEINE Vorwegnahme.
A1-EXEC: NICHT autorisiert, NICHT erteilt, NICHT ausgefuehrt.
Sprint Plan: NICHT geaendert — physisch DRAFT / 1.0 / R0.
OD-08 Option (a): NICHT erneut entschieden, NICHT erweitert, NICHT eingeschraenkt.
G7-a: NICHT beseitigt. G7-b: NICHT beruehrt.
U-4': NICHT materiell beantwortet — UNDETERMINED / HUMAN REVIEW REQUIRED.
HD-2: NICHT entschieden, NICHT wiedervorgelegt — DEFERRED / OPEN / NOT DECIDED.
IP §10.6 Bedingung 7: NICHT erfuellt, NICHT abgesenkt, NICHT umgedeutet; ACN-09 gewahrt.
OP-1 / OP-2: NICHT geschlossen.
RL-05: NICHT vorbereitet, NICHT entschieden — NOT REACHED.
Coding: NOT AUTHORIZED. QG-006 / QG-001..QG-008: NOT STARTED.
OD-05 / ADR-012 / ADRs / RDRs / Architecture Book / Implementation Plan /
     CLAUDE.md / ROADMAP.md / Code / Tests / Config: UNVERAENDERT.
Alle bestehenden Governance-Artefakte: NICHT ueberschrieben.
Vorbestehende Working-Tree-Aenderungen unangetastet. Kein Push, PR, Merge, Tag.
```

---

## 9. Empfehlung — **unverbindlich, KEINE Entscheidung**

| Position | Empfehlung | Begründung |
|---|---|---|
| **Bündelung** | **Z-1 und Z-2 in EINER Human Decision** | Kap. 6.3: kein Trennungsgebot, gleiche Autorität, gleicher Gegenstand, Präzedenz DEC-02, keine Absenkung |
| **Z-2** | **Z2-A** — der quellenbelegte PREP → DEC → EXEC-Zyklus **ist** das kontrollierte Verfahren | Z2-Q2/Q3/Q4 sind **FACT**; ein zusätzlicher Akt ist von **keiner** Quelle verlangt. Z2-A **legt** die Restfrage fest, statt sie aus Schweigen abzuleiten |
| **Z-1** | **Z1-B** — Zielwert, der exakt das Erteilte abbildet (`Als Planungsgrundlage genehmigt (ADW-SPR-1.0-001)` o. ä.) | Einziger Wert, der **nichts** behauptet, was die Quellen nicht tragen: ADW-SPR-1.0-001 Kap. 17 erteilt genau dies. **Z1-A** stünde in Spannung zu Z1-Q5/Q6/Q7 und würde die Frage aufwerfen, ob OP-1 oder Bedingung 7 mit-erfüllt seien — ein **ACN-09-Risiko**. **Z1-D** ist governance-seitig zulässig, aber aufwendiger, ohne dass eine Quelle den zusätzlichen Akt verlangt |
| **Z-4** | `Version` / `Revision` / `Datum` **unverändert lassen** | Keine Quelle verlangt eine Änderung; minimaler Eingriff |

> **Diese Empfehlung ist ausdrücklich keine Entscheidung.** Der Zielwert
> ist auch bei Z1-B eine **Festlegung des Projekteigners**, keine
> Ableitung aus den Quellen — Z-1 bleibt bis zur Unterzeichnung
> **UNKNOWN / HUMAN DECISION REQUIRED**.

---

## 10. HUMAN-DECISION-Block (auszufüllen)

```text
JX-DEV-SPR01-RL05-G7-A1-OD08-Z12-DEC-01-R0

Authority:  Projekteigner / Governance
Date:       <YYYY-MM-DD>

Bezug:      OD-08 = OPTION (a), entschieden am 2026-08-13
            (JX-DEV-SPR01-RL05-G7-A1-OD08-DEC-01-R0, Commit 9ec12d8)

--- Z-1  ZIELSTATUS (Sprint Plan Z. 6) ---
Gewaehlte Option:   Z1-A  |  Z1-B  |  Z1-C  |  Z1-D
Konkreter Zielwert fuer Z. 6:
    <exakter Zeichenlaut, z. B.: Als Planungsgrundlage genehmigt (ADW-SPR-1.0-001)>

Z-1b Reichweite:    Der Zielwert bildet ab:
    ( ) ausschliesslich die Genehmigung als Planungsgrundlage (ADW-SPR-1.0-001)
    ( ) eine darueber hinausgehende Dokumentgenehmigung
        -> falls angekreuzt: erforderlicher eigener Genehmigungsakt: <ja/nein + Form>

--- Z-4  KOPFFELDER Z. 7-9 ---
Version  (Z. 7):    ( ) unveraendert 1.0        ( ) neuer Wert: <...>
Revision (Z. 8):    ( ) unveraendert R0         ( ) neuer Wert: <...>
Datum    (Z. 9):    ( ) unveraendert 2026-08-09 ( ) neuer Wert: <YYYY-MM-DD>

--- Z-2  KONTROLLIERTES VERFAHREN ---
Gewaehlte Option:   Z2-A  |  Z2-B  |  Z2-C
Festlegung:         <z. B.: Das kontrollierte Verfahren ist der separat
                    autorisierte PREP -> DEC -> EXEC-Zyklus; ein zusaetzlicher
                    foermlicher Genehmigungsakt ist nicht erforderlich.>

--- CONDITIONS ---
- Diese Entscheidung ist DEC, kein EXEC. Kein physischer Vollzug in ihrer Welle.
- Der A1-EXEC bedarf eines eigenen, separaten Auftrags.
- Change Surface des EXEC: hoechstens Sprint Plan Z. 6 (zwingend) und Z. 7-9
  (nur soweit oben ausdruecklich festgelegt). Nichts anderes.
- Aus dem neuen Statuswert wird KEINE Erfuellung von OP-1 und KEINE Erfuellung
  von IP §10.6 Nr. 7 abgeleitet.
- Bedingung 7 bleibt NICHT ERFUELLT; ACN-09 gewahrt, keine Absenkung.
- U-4' bleibt UNDETERMINED; HD-2 bleibt DEFERRED / OPEN.
- Keine inhaltliche Aenderung des Sprint Plans (kein OD-05-Umriss).
- Kein RL-05, kein Coding, kein QG-006.
- Keine Aenderung an OD-05, ADR-012, ADRs/RDRs, Architecture Book,
  Implementation Plan, CLAUDE.md, ROADMAP.md, Code, Tests, Config.
- Vorbestehende Working-Tree-Aenderungen unangetastet. Kein Push.
```

---

## 11. Governance-State — ausdrückliche Feststellung

| Position | Status nach dieser PREP |
|---|---|
| **A1-EXEC** | **NOCH NICHT AUTORISIERT** |
| **Sprint Plan** | **PHYSISCH UNVERÄNDERT — DRAFT / 1.0 / R0** |
| **IP §10.6 Bedingung 7** | **WEITERHIN NICHT ERFÜLLT** |
| **RL-05** | **NOT REACHED** |
| **CODING** | **NOT AUTHORIZED** |
| **QG-006 / QG-001…QG-008** | **NOT STARTED** |
| **Z-1** | **UNKNOWN / HUMAN DECISION REQUIRED** |
| **Z-1b / Z-4** | **OFFEN** |
| **Z-2** | **TEILWEISE QUELLENBESTIMMT — Restfrage HUMAN DECISION REQUIRED** |
| **OD-08** | **DECIDED (Option a) — Vollzug ausstehend** |
| **G7-a** | **adressiert, NICHT beseitigt** |
| **G7-b** | **UNVERÄNDERT OFFEN** |
| **U-4′** | **UNDETERMINED / HUMAN REVIEW REQUIRED** |
| **HD-2** | **DEFERRED / OPEN / NOT DECIDED** |
| **OP-1 / OP-2** | **OFFEN** |
| **OD-05 / ADR-012 / ADRs / RDRs / Architecture Book / IP / CLAUDE.md / ROADMAP.md / Code / Tests / Config** | **UNVERÄNDERT** |

---

## 12. Change Surface dieser Welle · Preflight · Commit

| Gegenstand | Umfang |
|---|---|
| Neue Dateien | **genau eine** — `docs/audits/jx-dev-spr01-rl05-g7-a1-od08-z12-prep-r0.md` |
| Geänderte / gelöschte Dateien | **keine** |
| Bestehende Governance-Artefakte | **UNBERÜHRT** — ausschließlich gelesen |
| Code / Tests / Config | **UNBERÜHRT** — baseline-identisch |
| Vorbestehende Working-Tree-Änderungen | **UNANGETASTET** |

| # | Preflight | Ergebnis |
|---|---|---|
| 1 | Baseline gegen `9ec12d8` und vollständige Vorkette verifiziert | **PASS** |
| 2 | Source Gate readonly, 12 Quellen | **PASS** |
| 3 | Z-1 nicht erfunden, nicht analogisiert; ausdrücklich UNKNOWN | **PASS** |
| 4 | Z-2 aus Quellen bestimmt, soweit sie tragen; Restfrage ausgewiesen | **PASS** |
| 5 | FACT / UNKNOWN / INFERENCE getrennt | **PASS** |
| 6 | Bündelbarkeit geprüft (Auftragspunkt 9) | **PASS** |
| 7 | U-4′ nicht beantwortet · HD-2 nicht entschieden | **PASS** |
| 8 | Kein Sprint-Plan-Edit · kein A1-EXEC · **DEC ≠ EXEC** | **PASS** |
| 9 | ACN-09 gewahrt, keine Bedingung abgesenkt oder umgangen | **PASS** |
| 10 | Keine Änderung an OD-05/ADR-012/ADRs/RDRs/AB/IP/CLAUDE/ROADMAP/Code/Tests/Config | **PASS** |
| 11 | Genau ein neues Artefakt, genau ein Commit | **PASS** |
| 12 | Kein Push / PR / Merge / Tag | **PASS** |

| Position | Status |
|---|---|
| Commit | **genau EIN Commit**, ausschließlich diese Datei |
| Commit-Message | `docs: prepare Z-1/Z-2 human decision for OD-08 execution` |
| Push / PR / Merge / Tag | **NICHT DURCHGEFÜHRT** |

---

## 13. Next Step

> **Genau eine Human Decision:** `JX-DEV-SPR01-RL05-G7-A1-OD08-Z12-DEC-01-R0`
> — **Z-1 (inkl. Z-1b und Z-4) und Z-2 gemeinsam**, Block Kap. 10.
>
> **Erst danach** ist ein separater **A1-EXEC** zulässig, begrenzt auf
> CS-A1-1 (ggf. CS-A1-2).

**STOP NACH DIESEM ARTEFAKT. Keine automatische Ausführung von A1.**

---

## 14. Revision History

| Revision | Datum | Änderung | Status |
|---|---|---|---|
| **R0** | 2026-08-13 | Entscheidungsvorbereitung Z-1/Z-2: Quellenbefund gegen HEAD `9ec12d8`, Z-1 als UNKNOWN/HUMAN DECISION REQUIRED festgestellt, Z-2 als teilweise quellenbestimmt mit ausgewiesener Restfrage, Optionsräume Z1-A…D / Z2-A…C, Bündelbarkeit bejaht, unverbindliche Empfehlung, ausfüllbarer Human-Decision-Block | **COMPLETED — PREPARATION ONLY** |

---

**Ende JX-DEV-SPR01-RL05-G7-A1-OD08-Z12-PREP-01-R0 — Decision Preparation —
JOCHEN X Milestone 1.0 (2026-08-13) — HEAD `9ec12d8` — Bezugs-Baseline
`MILESTONE-1.0-BASELINE = 8fcf42f1997dfcf6ff232e75fd33c37b933991c8`**
