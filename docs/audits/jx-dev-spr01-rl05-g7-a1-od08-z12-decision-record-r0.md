# JOCHEN X — Milestone 1.0
# JX-DEV-SPR01-RL05-G7-A1-OD08-Z12-DEC-01-R0 — Human Decision Record
## Z-1 (Zielstatus) und Z-2 (kontrolliertes Verfahren) für die autorisierte OD-08-Nachführung

> **COMPLETED — DECISION ONLY · NO EXECUTION**
>
> Dieses Dokument zeichnet die **Human-Entscheidung des Projekteigners** zu
> **Z-1** (inkl. **Z-1b** und **Z-4**) und **Z-2** auf. Grundlage ist
> `JX-DEV-SPR01-RL05-G7-A1-OD08-Z12-PREP-01-R0` (Commit `92b67e2`).
> Die Entscheidung ist **DEC, kein EXEC**.
>
> **A1-EXEC = NICHT AUTORISIERT / NICHT AUSGEFÜHRT** · **Sprint Plan =
> PHYSISCH UNVERÄNDERT (DRAFT / 1.0 / R0)** · **IP §10.6 BEDINGUNG 7 =
> NICHT ERFÜLLT** · **RL-05 = NOT REACHED** · **OP-2 = NICHT ERFÜLLT** ·
> **CODING = NOT AUTHORIZED** · **QG-006 = NOT STARTED** ·
> **U-4′ = UNDETERMINED / HUMAN REVIEW REQUIRED** ·
> **HD-2 = DEFERRED / OPEN / NOT DECIDED**

---

## 1. Baseline Gate

| Prüfung | Ergebnis |
|---|---|
| **HEAD** | `92b67e2813b6dbc68f6db956585d849334cb5931` = `92b67e2` — „docs: prepare Z-1/Z-2 human decision for OD-08 execution" |
| **Erwartete Vorkette** | `3b76b89` → `a13a148` → `fa6e192` → `8e51c33` → `9ec12d8` → `92b67e2` — **verifiziert** |
| Staging vor Beginn | **leer** |
| PREP-01-Artefakt in HEAD | `docs/audits/jx-dev-spr01-rl05-g7-a1-od08-z12-prep-r0.md` — **einzige Datei in `92b67e2` (A)** |
| **Sprint Plan Kopf** | Z. 6 `Status \| **DRAFT**` · Z. 7 `Version \| 1.0` · Z. 8 `Revision \| R0` · Z. 9 `Datum \| 2026-08-09` — **unverändert, direkt verifiziert** |
| Sprint Plan Z. 276 | Bedingung 7 = **PENDING**, „Genehmigung durch Projekteigner ausstehend" — **unverändert** |
| Sprint Plan Z. 301 / 302 | **OP-1 = OFFEN** · **OP-2 = OFFEN** — **unverändert** |
| Working Tree | 3 vorbestehende getrackte Modifikationen (`CLAUDE.md`, `ROADMAP.md`, `docs/architecture-book-v2.md`) + untracked Dokumente — **unangetastet** |
| Bezugs-Baseline | `MILESTONE-1.0-BASELINE = 8fcf42f1997dfcf6ff232e75fd33c37b933991c8` (GDR-003) |

**Baseline Gate: PASS.**

---

## 2. PREP-Gate — Prüfung von PREP-01 gegen die getroffene Entscheidung

| # | Prüfung | Ergebnis |
|---|---|---|
| P-1 | PREP-01 vollständig gelesen (Kap. 1–14) | **JA** |
| P-2 | Ist **Z1-B** ein in PREP-01 Kap. 6.1 **registrierter** Optionswert? | **JA** — Zeile „Z1-B" |
| P-3 | Ist **Z2-A** ein in PREP-01 Kap. 6.2 **registrierter** Optionswert? | **JA** — Zeile „Z2-A" |
| P-4 | Optionsraum-Deckung / Scope-Mismatch? | **KEIN Mismatch** — beide Wahlen liegen innerhalb der von PREP-01 dargestellten Optionsräume; **keine Erweiterung, keine Erfindung** |
| P-5 | Ist die Bündelung von Z-1 und Z-2 in **einer** Decision zulässig? | **JA** — PREP-01 Kap. 6.3: kein Trennungsgebot in 12 Quellen, gleiche Autorität, gleicher Gegenstand, Präzedenz DEC-02, keine Absenkung |
| P-6 | Deckt sich **Z-4** (unverändert) mit dem in PREP-01 Kap. 6.1 vorgesehenen Zusatzfeld? | **JA** — Zusatzfrage Z-4, Variante „unverändert lassen" |
| P-7 | Deckt sich **Z-1b** (kein zusätzlicher Statusanspruch) mit dem HUMAN-DECISION-Block Kap. 10? | **JA** — Ankreuzoption „ausschließlich die Genehmigung als Planungsgrundlage (ADW-SPR-1.0-001)" |
| P-8 | Wurde die PREP-Empfehlung (Kap. 9) **als Entscheidung** behandelt? | **NEIN** — die Empfehlung war und bleibt unverbindlich. Die hier verzeichnete Wahl ist ein **eigenständiger Willensakt des Projekteigners**; die inhaltliche Übereinstimmung mit der Empfehlung ist Ergebnis, nicht Ursache |
| P-9 | Wurde ein Zielwert **erfunden, analogisiert oder aus fremden Statusmodellen übertragen**? | **NEIN** — siehe Kap. 4.3 (Z-1c bleibt ausdrücklich offen) |
| P-10 | Verlangt die Entscheidung eine physische Änderung in dieser Welle? | **NEIN** — DEC ≠ EXEC |

**PREP-Gate: PASS.**

---

## 3. Source Gate (readonly) — Quellenlage für Z-1 / Z-2

Bewertet wurde **ausschließlich** aus den in PREP-01 Kap. 2 bereits
definierten Governance-Quellen. **Keine neue Quelle, keine externe Quelle,
keine Datei geschrieben.**

| # | Quelle | Fundstelle | Direkt gegen HEAD verifiziert |
|---|---|---|---|
| 1 | **OD-08-DEC** (Option a) | `…-g7-a1-od08-decision-record-r0.md` Z. 9, 14, 72 | **JA** — „Die Entscheidung legt KEINEN konkreten Zielstatus fest"; „Zielstatus mitentschieden? **NEIN**" |
| 2 | **ADW-SPR-1.0-001** | `milestone-1.0-sprint-planning-approval-decision-op1.md` Z. 14, 21, 153 | **JA** — Wortlaut Z. 153 geprüft |
| 3 | **PREP-02** | `jx-dev-spr01-rl05-final-prep-02-r0.md` Z. 444, 596 | **JA** — „eigener PREP/DEC/EXEC-Zyklus"; „eigener PREP → DEC → EXEC" |
| 4 | **G7-DEC-01** | `jx-dev-spr01-rl05-g7-decision-record-r0.md` Z. 144 | **JA** — Condition 8 wörtlich |
| 5 | **Sprint Plan** | `milestone-1.0-sprint-plan.md` Z. 6–9, 276, 301–302 | **JA** |
| 6 | **MEP §20 OD-08** · **DEM §1.1 Z. 109** · **Dev Standard v1.1 §17 Anh. B** · **IP §10.4/§10.6/§10.9** · **Charter** · **OD-08-PREP** · **G7-PREP-01** | wie PREP-01 Kap. 2 | **übernommen aus PREP-01** (Quellenbefund unverändert; kein Widerspruch festgestellt) |

**Source Gate: PASS.**

### 3.1 Quellenlage — maßgebliche Feststellungen

| # | Feststellung | Klasse |
|---|---|---|
| S-1 | ADW-SPR-1.0-001 Z. 153: „Genehmigt ist **ausschließlich die Verwendung des Sprint Plans 1.0 R0 als Planungsgrundlage**. Der physische Status … bleibt **DRAFT / 1.0 / R0**; eine eventuelle Statusnachführung erfolgt in einem **separat autorisierten Schritt**." | **FACT (wörtlich)** |
| S-2 | Keine der Quellen nennt einen **Zielwert** für Sprint Plan Z. 6. | **FACT (Negativbefund)** |
| S-3 | Dev Standard v1.1 §17 Anh. B definiert **kein** Statusmodell für ein Sprint-Plan-Dokument. | **FACT (Negativbefund)** |
| S-4 | IP §10.4 W-7 („DRAFT → APPROVED") bezieht sich auf den **Implementation Plan**, nicht auf den Sprint Plan. | **FACT** |
| S-5 | Sprint Plan Z. 276 (Bedingung 7 = PENDING) und Z. 301 (OP-1 = OFFEN) sind unverändert offen. | **FACT** |
| S-6 | Der prozedurale Rahmen **PREP → DEC → EXEC mit separater Autorisierung** ist quellenbelegt (S-1; PREP-02 Z. 444/596; G7-DEC-01 Cond. 8). | **FACT** |
| S-7 | Ob **darüber hinaus** ein förmlicher Genehmigungs-/Dokumentenkontrollakt erforderlich ist, ist **nicht positiv normiert**. Die Quellen **schweigen**. | **UNKNOWN (Negativbefund)** |

---

## 4. HUMAN DECISION

> Die nachfolgenden Festlegungen sind die **vom Projekteigner getroffenen
> Entscheidungen**. Sie sind **keine Empfehlung**, **keine Ableitung** und
> **keine Feststellung** aus den Quellen. Sie sind **Willensakte**.

```text
JX-DEV-SPR01-RL05-G7-A1-OD08-Z12-DEC-01-R0

Authority:  Projekteigner / Governance
Date:       2026-08-13

Bezug:      OD-08 = OPTION (a), entschieden am 2026-08-13
            (JX-DEV-SPR01-RL05-G7-A1-OD08-DEC-01-R0, Commit 9ec12d8)
            PREP: JX-DEV-SPR01-RL05-G7-A1-OD08-Z12-PREP-01-R0, Commit 92b67e2

--- Z-1  ZIELSTATUS (Sprint Plan Z. 6) ---
Gewaehlte Option:   Z1-B

Normative Festlegung:
    Der Zielwert muss ausschliesslich den tatsaechlich erteilten
    Governance-Zustand abbilden und darf keine zusaetzliche Genehmigung
    behaupten, die die Quellen nicht tragen.

Ausdruecklich NICHT gewaehlt: Z1-A (APPROVED).
Keine Analogie zu Implementation-Plan-States (IP §10.4 W-7).
Keine Ableitung aus der Hauskonvention (Charter / IP / Architecture Book).
Keine Uebertragung aus ADR-/Specification-/Sprint-/Release-Statusmodellen.

Z-1b Reichweite:    Der Zielwert bildet ab:
    (X) ausschliesslich die Genehmigung als Planungsgrundlage (ADW-SPR-1.0-001)
    ( ) eine darueber hinausgehende Dokumentgenehmigung
    -> Kein zusaetzlicher Statusanspruch. Kein eigener Genehmigungsakt
       erforderlich (siehe Z-2 / Z2-A).

--- Z-4  KOPFFELDER Z. 7-9 ---
Version  (X) unveraendert 1.0
Revision (X) unveraendert R0
Datum    (X) unveraendert 2026-08-09
    -> unveraendert, sofern die Quellen keine andere Aenderung zwingend
       verlangen. Eine solche zwingende Quellenanforderung wurde geprueft
       und NICHT festgestellt (S-2).

--- Z-2  KONTROLLIERTES VERFAHREN ---
Gewaehlte Option:   Z2-A

Festlegung:
    PREP -> DEC -> separater EXEC genuegt als kontrolliertes Verfahren
    fuer die autorisierte Nachfuehrung des Sprint-Plan-Kopfes.
    Ein zusaetzlicher foermlicher Genehmigungsakt wird NICHT erfunden.
    Das Schweigen der Quellen (S-7) wird NICHT als positive Norm
    interpretiert.

Ausdruecklich NICHT gewaehlt: Z2-B, Z2-C.
```

### 4.1 Z-1 — Entscheidung und ihre Wirkung

| Position | Festlegung |
|---|---|
| **Gewählte Option** | **Z1-B** — **DECIDED** |
| **Nicht gewählt** | **Z1-A** (`APPROVED`) — **ausdrücklich abgelehnt**; ferner Z1-C, Z1-D |
| **Kriterium** | Der Zielwert bildet **ausschließlich** den tatsächlich erteilten Governance-Zustand ab (ADW-SPR-1.0-001 Z. 153: Genehmigung als **Planungsgrundlage**) |
| **Verboten** | Jede Formulierung, die eine **darüber hinausgehende** Dokumentgenehmigung behauptet |
| **Verhältnis zu OP-1** | **KEINE** Erfüllung von OP-1 wird abgeleitet — OP-1 bleibt **OFFEN** |
| **Verhältnis zu IP §10.6 Nr. 7** | **KEINE** Erfüllung wird abgeleitet — Bedingung 7 bleibt **NICHT ERFÜLLT**; **ACN-09 gewahrt** |
| **Verhältnis zu G7-a** | Der spätere Vollzug **adressiert** G7-a. Diese Decision **beseitigt G7-a nicht** |

### 4.2 Z-1b / Z-4 — Auflösung

| Frage | Auflösung |
|---|---|
| **Z-1b** — Bedeutungsreichweite | **Ausschließlich Genehmigung als Planungsgrundlage.** Kein zusätzlicher Statusanspruch — **DECIDED** |
| **Z-1b** — eigener Genehmigungsakt erforderlich? | **NEIN** — folgt aus Z2-A; kein zusätzlicher förmlicher Akt — **DECIDED** |
| **Z-4** — Version (Z. 7) | **unverändert `1.0`** — **DECIDED** |
| **Z-4** — Revision (Z. 8) | **unverändert `R0`** — **DECIDED** |
| **Z-4** — Datum (Z. 9) | **unverändert `2026-08-09`** — **DECIDED** |
| Zwingende Quellenanforderung für eine abweichende Änderung? | **Geprüft — NICHT festgestellt** (S-2, S-3) |

### 4.3 Z-1c — verbleibende Ausgestaltung (ausdrücklich NICHT entschieden)

> **Wichtig für die spätere EXEC-Welle.**

| Position | Status |
|---|---|
| **Z-1 als Options-/Kriteriumsentscheidung** | **DECIDED (Z1-B)** — normativ vollständig |
| **Z-1c — exakter Zeichenlaut des Zielwerts für Z. 6** | **NICHT FESTGELEGT** in dieser Decision |

Der Projekteigner hat **Z1-B als Norm** entschieden, **nicht** einen
konkreten Zeichenlaut. Ein Zeichenlaut wird hier **nicht erfunden und nicht
als entschieden ausgegeben**. PREP-01 Kap. 6.1 nennt für Z1-B lediglich
**Beispiele** („z. B."): `APPROVED AS PLANNING BASIS (ADW-SPR-1.0-001)`
bzw. `Als Planungsgrundlage genehmigt (ADW-SPR-1.0-001)` — diese sind
**Kandidaten**, **keine gewählten Werte**.

**Folge für den EXEC:** Der A1-EXEC darf Z. 6 **erst** schreiben, wenn der
Zeichenlaut vom Projekteigner bestätigt ist. Er ist an **Z1-B** gebunden:
Jeder Wert, der mehr behauptet als die Genehmigung als Planungsgrundlage,
ist **unzulässig**.

### 4.4 Z-2 — Entscheidung und ihre Wirkung

| Position | Festlegung |
|---|---|
| **Gewählte Option** | **Z2-A** — **DECIDED** |
| **Nicht gewählt** | **Z2-B**, **Z2-C** |
| **Inhalt** | Das „kontrollierte Verfahren" i. S. v. MEP §20 OD-08 Option (a) **ist** der separat autorisierte **PREP → DEC → EXEC**-Zyklus |
| **Restfrage Z2-Q6** | **Durch Festlegung geschlossen** — ein zusätzlicher förmlicher Genehmigungsakt ist **nicht** erforderlich |
| **Methodische Absicherung** | Die Schließung erfolgt als **Willensakt**, **nicht** als Ableitung aus dem Schweigen der Quellen (S-7). Das Schweigen wird **nicht** zur positiven Norm erhoben |
| **Fortbestehende Sperre** | **G7-DEC-01 Condition 8** bleibt in Kraft: keine Änderung des Sprint Plans **ohne separaten EXEC-Auftrag** |

---

## 5. FACT / DECISION / UNKNOWN

### FACT (unverändert aus der Quellenlage)

1. ADW-SPR-1.0-001 genehmigt **ausschließlich die Verwendung als Planungsgrundlage**; physischer Status bleibt DRAFT / 1.0 / R0.
2. Keine Quelle nennt einen Zielwert für Sprint Plan Z. 6.
3. Dev Standard v1.1 §17 Anh. B kennt **kein** Sprint-Plan-Dokumentstatusmodell.
4. IP §10.4 W-7 („DRAFT → APPROVED") betrifft den **Implementation Plan**.
5. Sprint Plan Z. 276 = Bedingung 7 **PENDING**; Z. 301 = OP-1 **OFFEN**; Z. 302 = OP-2 **OFFEN**.
6. Der Vollzug ist ein „separat autorisierter Schritt", konkretisiert als eigener PREP/DEC/EXEC-Zyklus, gesperrt durch G7-DEC-01 Condition 8.
7. OD-08 ist mit Option (a) entschieden — **ohne** Zielwert.
8. IP §10.9 **ACN-09** verbietet jede Absenkung bestehender Bedingungen.

### DECISION (dieser Record — Willensakte, keine Ableitungen)

1. **Z-1 = Z1-B** — Zielwert bildet ausschließlich den erteilten Governance-Zustand ab. **Z1-A ausdrücklich nicht gewählt.**
2. **Z-1b** — ausschließlich Genehmigung als Planungsgrundlage; kein zusätzlicher Statusanspruch; kein eigener Genehmigungsakt.
3. **Z-4** — Version / Revision / Datum **unverändert**.
4. **Z-2 = Z2-A** — PREP → DEC → separater EXEC genügt; kein zusätzlicher förmlicher Genehmigungsakt.

### UNKNOWN (bleibt offen)

1. **Z-1c** — exakter Zeichenlaut des Zielwerts für Z. 6 (Kap. 4.3).
2. **U-4′** — **UNDETERMINED / HUMAN REVIEW REQUIRED**.
3. **HD-2** — **DEFERRED / OPEN / NOT DECIDED**.
4. **G7-b** — Nichtabdeckung des OD-05-Umrisses; hängt an U-4′ / HD-2.
5. Form und Instanz einer späteren Feststellung „G7-a beseitigt".

### INFERENCE — **keine gezogen**

Insbesondere **nicht**: „Z-1 entschieden ⇒ Sprint Plan geändert" ·
„Z-2 entschieden ⇒ EXEC autorisiert" · „Z1-B gewählt ⇒ OP-1 erfüllt" ·
„Z1-B gewählt ⇒ Bedingung 7 erfüllt oder näher an Erfüllung" ·
„Z2-A gewählt ⇒ Sprint Plan genehmigt" · „Schweigen der Quellen ⇒ Norm".

---

## 6. Negative Checks

| # | Prüfung | Ergebnis |
|---|---|---|
| N-1 | Sprint Plan physisch geändert? | **NEIN** — Z. 6–9 verifiziert unverändert (`DRAFT / 1.0 / R0 / 2026-08-09`) |
| N-2 | A1-EXEC vorbereitet oder ausgeführt? | **NEIN** — nicht autorisiert, nicht erteilt, nicht ausgeführt |
| N-3 | DEC als EXEC behandelt? | **NEIN** — **DEC ≠ EXEC** durchgehend gewahrt |
| N-4 | Zielwert erfunden / analogisiert / übertragen? | **NEIN** — Z-1c ausdrücklich offen (Kap. 4.3) |
| N-5 | Zusätzlicher Genehmigungsakt erfunden? | **NEIN** — Z2-A schließt ihn aus |
| N-6 | Schweigen der Quellen als positive Norm verwendet? | **NEIN** — S-7 als UNKNOWN geführt; Schließung erfolgt als Willensakt |
| N-7 | Empfehlung als Entscheidung ausgegeben? | **NEIN** — PREP-01 Kap. 9 bleibt unverbindlich (P-8) |
| N-8 | Bedingung 7 erfüllt, abgesenkt oder umgedeutet? | **NEIN** — **NICHT ERFÜLLT**; **ACN-09 gewahrt** |
| N-9 | OP-1 / OP-2 geschlossen? | **NEIN** — beide **OFFEN**; **OP-2 NICHT ERFÜLLT** |
| N-10 | U-4′ materiell beantwortet? | **NEIN** — **UNDETERMINED / HUMAN REVIEW REQUIRED** |
| N-11 | HD-2 entschieden oder wiedervorgelegt? | **NEIN** — **DEFERRED / OPEN / NOT DECIDED** |
| N-12 | RL-05 vorbereitet oder erreicht? | **NEIN** — **NOT REACHED** |
| N-13 | Coding autorisiert? | **NEIN** — **NOT AUTHORIZED** |
| N-14 | QG-006 (oder QG-001…QG-008) gestartet? | **NEIN** — **NOT STARTED** |
| N-15 | OD-05- oder ADR-012-Inhalt geändert? | **NEIN** |
| N-16 | ADRs / RDRs / Architecture Book / Implementation Plan geändert? | **NEIN** |
| N-17 | `CLAUDE.md` / `ROADMAP.md` geändert? | **NEIN** — vorbestehende Working-Tree-Modifikationen **unangetastet** |
| N-18 | Code / Tests / Konfiguration geändert? | **NEIN** — baseline-identisch |
| N-19 | Bestehende Governance-Datei überschrieben? | **NEIN** — ausschließlich gelesen |
| N-20 | OD-08 Option (a) erneut entschieden, erweitert oder eingeschränkt? | **NEIN** |
| N-21 | G7-a beseitigt? | **NEIN** — adressiert, nicht beseitigt. **G7-b unberührt** |
| N-22 | Push / PR / Merge / Tag? | **NEIN** |

**Negative Checks: alle PASS.**

---

## 7. Change Surface dieser Welle

| Gegenstand | Umfang |
|---|---|
| Neue Dateien | **genau eine** — `docs/audits/jx-dev-spr01-rl05-g7-a1-od08-z12-decision-record-r0.md` |
| Geänderte / gelöschte Dateien | **keine** |
| Bestehende Governance-Artefakte | **UNBERÜHRT** — ausschließlich gelesen |
| Sprint Plan | **PHYSISCH UNVERÄNDERT** |
| Code / Tests / Config | **UNBERÜHRT** — baseline-identisch |
| Vorbestehende Working-Tree-Änderungen | **UNANGETASTET** |

---

## 8. Preflight

| # | Preflight | Ergebnis |
|---|---|---|
| 1 | Baseline gegen `92b67e2` und vollständige Vorkette verifiziert | **PASS** |
| 2 | PREP-01 vollständig gegen die beabsichtigte Entscheidung geprüft (Kap. 2) | **PASS** |
| 3 | Quellenlage ausschließlich aus den definierten Governance-Quellen bewertet | **PASS** |
| 4 | Human Decision exakt dokumentiert (Kap. 4) | **PASS** |
| 5 | Keine Empfehlung als Entscheidung ausgegeben | **PASS** |
| 6 | Z-1c nicht erfunden, ausdrücklich offen geführt | **PASS** |
| 7 | FACT / DECISION / UNKNOWN getrennt | **PASS** |
| 8 | Negative Checks N-1…N-22 durchgeführt | **PASS** |
| 9 | **DEC ≠ EXEC** · kein Sprint-Plan-Edit · kein A1-EXEC | **PASS** |
| 10 | ACN-09 gewahrt, keine Bedingung abgesenkt oder umgangen | **PASS** |
| 11 | Genau ein neues Artefakt, genau ein Commit | **PASS** |
| 12 | Kein Push / PR / Merge / Tag | **PASS** |

---

## 9. Governance-State — ausdrückliche Feststellung nach dieser Decision

| Position | Status |
|---|---|
| **Z-1** | **DECIDED — Z1-B** (Z1-A ausdrücklich nicht gewählt) |
| **Z-1b** | **DECIDED** — ausschließlich Planungsgrundlage, kein zusätzlicher Statusanspruch |
| **Z-1c** (Zeichenlaut) | **OFFEN** — vor A1-EXEC vom Projekteigner zu bestätigen |
| **Z-2** | **DECIDED — Z2-A** |
| **Z-4** | **DECIDED** — Version / Revision / Datum **unverändert** (`1.0` / `R0` / `2026-08-09`) |
| **OD-08** | **OPTION (a) entschieden — Vollzug weiterhin ausstehend** |
| **A1-EXEC** | **NICHT AUTORISIERT / NICHT AUSGEFÜHRT** |
| **Sprint Plan** | **PHYSISCH UNVERÄNDERT — DRAFT / 1.0 / R0** |
| **IP §10.6 Bedingung 7** | **NICHT ERFÜLLT** — bleibt es bis zum tatsächlichen A1-EXEC |
| **OP-1** | **OFFEN** |
| **OP-2** | **NICHT ERFÜLLT** |
| **RL-05** | **NOT REACHED** |
| **CODING** | **NOT AUTHORIZED** |
| **QG-006 / QG-001…QG-008** | **NOT STARTED** |
| **U-4′** | **UNDETERMINED / HUMAN REVIEW REQUIRED** |
| **HD-2** | **DEFERRED / OPEN / NOT DECIDED** |
| **G7-a** | **adressiert, NICHT beseitigt** |
| **G7-b** | **UNVERÄNDERT OFFEN** |
| **OD-05 / ADR-012 / ADRs / RDRs / Architecture Book / IP / `CLAUDE.md` / `ROADMAP.md` / Code / Tests / Config** | **UNVERÄNDERT** |

---

## 10. Conditions für den späteren A1-EXEC

1. Der A1-EXEC bedarf eines **eigenen, separaten Auftrags** (G7-DEC-01 Condition 8).
2. **Vor** dem Schreiben von Z. 6 ist der **Zeichenlaut (Z-1c)** vom Projekteigner zu bestätigen.
3. Der Zielwert ist an **Z1-B** gebunden: keine Aussage über die Genehmigung als Planungsgrundlage hinaus.
4. Change Surface: **höchstens** Sprint Plan **Z. 6**. **Z. 7–9 bleiben unverändert** (Z-4).
5. **Z. 90 · Z. 276 · Z. 301 · Z. 302 sind NICHT Gegenstand.**
6. Keine inhaltliche Fortschreibung des Sprint Plans (kein OD-05-Umriss) — Gegenstand von U-4′ / HD-2.
7. Aus dem neuen Statuswert wird **keine** Erfüllung von OP-1 und **keine** Erfüllung von IP §10.6 Nr. 7 abgeleitet.
8. Bedingung 7 bleibt **NICHT ERFÜLLT**; **ACN-09** gewahrt.
9. Keine Änderung an OD-05, ADR-012, ADRs/RDRs, Architecture Book, Implementation Plan, `CLAUDE.md`, `ROADMAP.md`, Code, Tests, Config.
10. Bestehende Governance-Artefakte werden **nicht überschrieben**. Vorbestehende Working-Tree-Änderungen bleiben unangetastet. Kein Push.

---

## 11. Explicit Non-Decisions

```text
Z-1c: exakter Zeichenlaut fuer Z. 6 NICHT festgelegt, NICHT erfunden,
      NICHT aus Beispielen der PREP als gewaehlt ausgegeben.
Z1-A: ausdruecklich NICHT gewaehlt. Z1-C / Z1-D: NICHT gewaehlt.
Z2-B / Z2-C: NICHT gewaehlt. Kein zusaetzlicher Genehmigungsakt erfunden.
Schweigen der Quellen: NICHT als positive Norm interpretiert.
A1-EXEC: NICHT autorisiert, NICHT vorbereitet, NICHT ausgefuehrt.
Sprint Plan: NICHT geaendert — physisch DRAFT / 1.0 / R0.
OD-08 Option (a): NICHT erneut entschieden, NICHT erweitert, NICHT eingeschraenkt.
G7-a: NICHT beseitigt. G7-b: NICHT beruehrt.
U-4': NICHT materiell beantwortet — UNDETERMINED / HUMAN REVIEW REQUIRED.
HD-2: NICHT entschieden, NICHT wiedervorgelegt — DEFERRED / OPEN / NOT DECIDED.
IP §10.6 Bedingung 7: NICHT erfuellt, NICHT abgesenkt, NICHT umgedeutet; ACN-09 gewahrt.
OP-1: NICHT geschlossen. OP-2: NICHT erfuellt.
RL-05: NICHT vorbereitet, NICHT erreicht — NOT REACHED.
Coding: NOT AUTHORIZED. QG-006 / QG-001..QG-008: NOT STARTED.
OD-05 / ADR-012 / ADRs / RDRs / Architecture Book / Implementation Plan /
      CLAUDE.md / ROADMAP.md / Code / Tests / Config: UNVERAENDERT.
Alle bestehenden Governance-Artefakte: NICHT ueberschrieben.
Vorbestehende Working-Tree-Aenderungen unangetastet. Kein Push, PR, Merge, Tag.
```

---

## 12. Next Step

> Der nächste Schritt ist eine **separate EXEC-Welle**
> (`…-OD08-Z12-EXEC-01-R0` o. ä.), die **gesondert zu beauftragen** ist und
> zuvor die Bestätigung von **Z-1c** benötigt.

**STOP NACH DEC-01. Keine automatische Vorbereitung oder Ausführung von A1-EXEC.**

---

## 13. Revision History

| Revision | Datum | Änderung | Status |
|---|---|---|---|
| **R0** | 2026-08-13 | Human Decision Record zu Z-1 (Z1-B), Z-1b (nur Planungsgrundlage), Z-4 (Version/Revision/Datum unverändert) und Z-2 (Z2-A) auf Basis von PREP-01 (`92b67e2`); Baseline Gate, PREP-Gate, Source Gate, Negative Checks N-1…N-22, Preflight; Z-1c ausdrücklich offen | **COMPLETED — DECISION ONLY** |

---

**Ende JX-DEV-SPR01-RL05-G7-A1-OD08-Z12-DEC-01-R0 — Human Decision Record —
JOCHEN X Milestone 1.0 (2026-08-13) — HEAD `92b67e2` — Bezugs-Baseline
`MILESTONE-1.0-BASELINE = 8fcf42f1997dfcf6ff232e75fd33c37b933991c8`**
