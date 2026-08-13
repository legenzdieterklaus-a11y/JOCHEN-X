# JOCHEN X — Milestone 1.0
# JX-DEV-SPR01-RL05-G7-A1-OD08-PREP-01-R0 — Decision Preparation
## OD-08 — Optionsraum (a)/(b): Statusnachführung des Sprint Plans

> **COMPLETED — PREPARATION ONLY · NO DECISION**
>
> Diese PREP bereitet **eine** Human Decision vor: die Wahl im registrierten
> **zweiwertigen OD-08-Optionsraum** — **(a)** Sprint-Plan-Kopf/Status
> nachführen oder **(b)** unverändert belassen.
>
> **PREP ≠ DEC ≠ EXEC.** Diese Welle **entscheidet nichts**, führt **A1
> nicht aus** und ändert den Sprint Plan **nicht**.
>
> **OD-08 = OPEN** · **A1 = NICHT AUSGEFÜHRT** · **U-4′ = UNDETERMINED /
> HUMAN REVIEW REQUIRED** · **BEDINGUNG 7 = NICHT ERFÜLLT** ·
> **HD-2 = DEFERRED / OPEN / NOT DECIDED** · **RL-05 = NOT REACHED** ·
> **CODING = NOT AUTHORIZED** · **QG-006 = NOT STARTED**

---

## 1. Document Identity

| Feld | Wert |
|---|---|
| **Document ID** | **JX-DEV-SPR01-RL05-G7-A1-OD08-PREP-01-R0** |
| Mode / Wave | GOVERNANCE · **PREP** |
| Subject | Entscheidungsvorbereitung OD-08 — Optionsraum (a)/(b) |
| Date | 2026-08-13 |
| Pfad | `docs/audits/jx-dev-spr01-rl05-g7-a1-od08-prep-r0.md` |
| **Bezugs-Baseline** | `MILESTONE-1.0-BASELINE = 8fcf42f1997dfcf6ff232e75fd33c37b933991c8` (GDR-003) |
| HEAD bei Beginn | `fa6e192` — A2-VERIFY-Record |
| Branch | `milestone-1.0-governance` |
| Vorkette | `3b76b89` (DEC-02) → `a13a148` (A2-EXEC) → `fa6e192` (A2-VERIFY) |
| Autorisierende Grundlage | DEC-02 **Detail 5** / **Condition 5** („Erst danach darf A1 vorbereitet … werden"); A2-VR Kap. 17 Welle 1 |
| **Status** | **COMPLETED — PREPARATION ONLY** |

---

## 2. Baseline

| Prüfung | Ergebnis |
|---|---|
| HEAD | `fa6e192` — „docs: record separate verify of A2 execution (U-4-prime)" |
| A2-EXEC / A2-VERIFY | `a13a148` / `fa6e192` — beide in der Kette, beide **COMPLETED** |
| DEC-02 | `3b76b89` — Vorfahr von HEAD |
| Condition 5 erfüllt (Vorbereitung von A1 jetzt zulässig) | **JA** — A2 abgeschlossen **und** separat verifiziert |
| Produktiver Baum vs. `8fcf42f` (`app core sdk ui config tests src`) | **0 Dateien** — baseline-identisch |
| Staging vor Beginn | **leer** |
| Working Tree | 3 vorbestehende getrackte Modifikationen (`CLAUDE.md`, `ROADMAP.md`, `docs/architecture-book-v2.md`) + vorbestehende untracked Dokumente — **unangetastet** |

**Baseline-Gate: PASS.** Keine neue Baseline definiert.

---

## 3. Source Gate (readonly)

| # | Quelle | Fundstelle | Prüfhandlung | Ergebnis |
|---|---|---|---|---|
| 1 | **MEP §20 OD-08** | `docs/audits/jochen-x-master-engineering-plan-r0.md` Z. 2056–2064 | Problem / Evidenz / **Optionen (a)(b)** / Empfehlung / Autorität wörtlich gelesen | **SOURCE FACT** |
| 2 | **DEM §1.1 / §366** | `docs/audits/jochen-x-decision-execution-matrix-r0.md` Z. 109, 366 | Priorität, „Entscheidung nötig?", Status, Empfehlung gelesen | **SOURCE FACT** |
| 3 | **ADW-SPR-1.0-001** | `docs/governance/milestone-1.0-sprint-planning-approval-decision-op1.md` Kap. 17, 18, Z. 21 | Decision Scope / Non-Effects gelesen | **SOURCE FACT** |
| 4 | **Sprint Plan** | `docs/milestone-1.0-sprint-plan.md` Z. 1–12, 90, 301–302 | Kopf, OP-1/OP-2, Bedingungsverweis direkt gelesen | **SOURCE FACT** |
| 5 | **Development Standard v1.1 §17 Anh. B** | `docs/development-standard-v1.1.md` Z. 795–800 | Approval-States-Tabelle vollständig gelesen | **SOURCE FACT** |
| 6 | **GDR-OD01-001** | `docs/governance/od-01-governance-decision.md` Kap. 13 (Z. 306) | OD-08-Bezug gelesen | **SOURCE FACT** |
| 7 | **G7-PREP-01** | `docs/audits/jx-dev-spr01-rl05-g7-prep-r0.md` Kap. 5 (A1-1…A1-10), 5.1 | A1-Befundlage gelesen | **SOURCE FACT** |
| 8 | **DEC-02** | `docs/audits/jx-dev-spr01-rl05-g7-decision-record-02-r0.md` Kap. 4 | Details 4–6, Conditions 5, 7 gelesen | **SOURCE FACT** |
| 9 | **A2-EXEC / A2-VR** | `…-g7-a2-verify-r0.md`; `…-g7-a2-verification-record-r0.md` | Ergebnisstand U-4′ übernommen | **SOURCE FACT** |

Keine externe Quelle. Keine Datei geschrieben. Keine Working-Tree-Modifikation als Baseline-Wahrheit verwendet.

**Source Gate: PASS**

---

## 4. Gegenstand und Abgrenzung

| Feld | Wert |
|---|---|
| **Registrierte Position** | **OD-08 — „Statusnachführung des Sprint Plans"** [MEP §20 OD-08] |
| **Problem (wörtlich)** | „Kopf trägt DRAFT, die Genehmigung liegt über ADW-SPR-1.0-001 vor (SG-02)" |
| **Optionsraum (wörtlich, zweiwertig)** | „(a) Kopf im vorgesehenen kontrollierten Verfahren nachführen; (b) belassen, da die Genehmigungskette dokumentiert ist" |
| **Erforderliche Autorität** | **Projekteigner / Governance** [MEP §20 OD-08; DEM §1.1 Z. 109] |
| **Priorität / Status** | **P3** · **OPEN** · „Entscheidung nötig? **JA**" [DEM §1.1 Z. 109] |
| **Blocker laut DEM** | „**keine**" · Sprintbezug: „NO CURRENT SPRINT" |

**Nicht Gegenstand dieser PREP:** U-4′ materiell · HD-2 · Bedingung 7
feststellen · RL-05 · Coding · QG-006 · ADR-012 / OD-05 · Inhaltliche
Fortschreibung des Sprint Plans über den Statuskopf hinaus · Ausgestaltung
des „kontrollierten Verfahrens" · Auswahl innerhalb (a)/(b).

---

## 5. Quellenprüfung gegen den aktuellen Stand

| # | Prüfpunkt | Befund am HEAD `fa6e192` | Klasse |
|---|---|---|---|
| Q-1 | Ist OD-08 noch offen? | **JA** — DEM §1.1 Z. 109 Status **OPEN**; GDR-OD01-001 Kap. 13 Z. 306: „OD-08 bleibt **OPEN**; die empfohlene Bündelung wird durch diesen Record **nicht** vollzogen" | **FACT** |
| Q-2 | Ist der Optionsraum unverändert zweiwertig? | **JA** — keine Quelle erweitert, verengt oder ersetzt (a)/(b); DEC-01/DEC-02 und A2/A2-VR lassen ihn ausdrücklich unverengt | **FACT** |
| Q-3 | Trägt der Sprint Plan noch DRAFT? | **JA** — `docs/milestone-1.0-sprint-plan.md` Z. 6 `Status \| **DRAFT**`, Z. 7 `Version \| 1.0`, Z. 8 `Revision \| R0`, Z. 9 `Datum \| 2026-08-09` — unverändert | **FACT** |
| Q-4 | Ist die Genehmigungskette dokumentiert? | **JA** — ADW-SPR-1.0-001 Kap. 17: genehmigt ist „**ausschließlich die Verwendung des Sprint Plans 1.0 R0 als Planungsgrundlage**"; „Der physische Status … bleibt **DRAFT / 1.0 / R0**; eine eventuelle Statusnachführung erfolgt in einem **separat autorisierten Schritt**" | **FACT (wörtlich)** |
| Q-5 | Verlangt eine Quelle die Nachführung? | **NEIN** — keine geprüfte Quelle normiert eine Pflicht. MEP/DEM führen sie als **Empfehlung**: „Redaktionell, nicht dringlich; sinnvoll gemeinsam mit OD-01" | **FACT (Negativbefund)** |
| Q-6 | Ist ein Zielstatus quellenbestimmt? | **NEIN** — siehe Kap. 8. Development Standard v1.1 §17 Anh. B kennt Statusmodelle nur für **ADR**, **Specification**, **Sprint**, **Release** — **kein** Modell für ein Sprint-Plan-**Dokument** (unabhängig verifiziert, Z. 795–800) | **FACT (Negativbefund)** / **UNKNOWN** (Ziel) |
| Q-7 | Ist das „vorgesehene kontrollierte Verfahren" ausgestaltet? | **NEIN** — MEP §20 OD-08 nennt es, benennt es aber nicht; in keiner geprüften Quelle ausgestaltet [G7-PREP A1-3; MEP §20] | **UNKNOWN** |
| Q-8 | Hat die A2/A2-VERIFY-Welle die OD-08-Lage verändert? | **NEIN** — U-4′ bleibt UNDETERMINED; A2-VR Kap. 9 führt OD-08 als **OPEN, Optionsraum unverengt** | **FACT** |
| Q-9 | Bleibt die Empfehlung „gemeinsam mit OD-01" vollziehbar? | **Teilweise gegenstandslos** — GDR-OD01-001 ist **FINAL** entschieden (Option C), die Bündelung wurde ausdrücklich **nicht** vollzogen. Die Empfehlung stammt zudem aus einem Kontext **vor** der Verknüpfung von OD-08 mit Bedingung 7 [G7-PREP A1-10] | **FACT** (Wortlaut) / **OBSERVATION** (Kontextlage) |
| Q-10 | Steht ein Blocker der Entscheidung entgegen? | **NEIN** laut DEM („Blocker: keine"); praktisch begrenzend wirkt allein die Zielstatus-/Verfahrenslücke Q-6/Q-7 **auf den Vollzug**, nicht auf die Entscheidung | **FACT** / **OBSERVATION** |

---

## 6. Option (a) — exakte Bedeutung

| Feld | Feststellung | Klasse |
|---|---|---|
| **Wortlaut** | „Kopf im vorgesehenen kontrollierten Verfahren nachführen" | **FACT** |
| **Was gewählt wird** | Die **grundsätzliche Entscheidung**, den Statuskopf des Sprint Plans nachzuführen | **FACT** |
| **Was damit noch nicht feststeht** | **Zielstatus** (Q-6) und **Verfahren** (Q-7) | **UNKNOWN** |
| **Unmittelbare Wirkung der DEC** | **keine physische** — die Nachführung selbst ist ein **separat autorisierter Schritt** [ADW-SPR-1.0-001 Kap. 17] und benötigt einen eigenen **A1-EXEC** [G7-PREP A1-6; DEC-01 Condition 8] | **FACT** |
| **Charakter des Vollzugs** | Nach getroffener Wahl (a) mechanisch — **nur soweit der Zielstatus feststeht**, was derzeit nicht der Fall ist [G7-PREP A1-8] | **FACT** (Entscheidungsteil) / **UNKNOWN** (Vollzugsteil) |
| **Beziehung zu Bedingung 7** | (a) adressiert **G7-a** (Statuskopf). **G7-b** (Nichtabdeckung OD-05-Umriss) bleibt davon **unberührt**; ob und wieweit G7-b für Nr. 7 relevant ist, ist **U-4′ = UNDETERMINED** und wird hier **nicht** beantwortet | **FACT** / **UNDETERMINED** |
| **Was (a) NICHT bewirkt** | Keine Erfüllung von Bedingung 7 · kein RL-05 · keine Coding-Freigabe · keine HD-2-Erledigung · keine inhaltliche Planänderung | **FACT** |

---

## 7. Option (b) — exakte Bedeutung

| Feld | Feststellung | Klasse |
|---|---|---|
| **Wortlaut** | „belassen, da die Genehmigungskette dokumentiert ist" | **FACT** |
| **Was gewählt wird** | Der Statuskopf bleibt dauerhaft **DRAFT / 1.0 / R0**; die Genehmigung wirkt allein über die dokumentierte Kette (ADW-SPR-1.0-001) | **FACT** |
| **Unmittelbare Wirkung** | **keine Dateiänderung**; OD-08 würde als Position **geschlossen** (Entscheidung getroffen), ohne physischen Vollzug | **FACT** |
| **Kein A1-EXEC erforderlich** | **JA** — bei (b) existiert kein auszuführender Vollzug [G7-PREP A1-7] | **FACT** |
| **Beziehung zu G7-a** | Option (b) **beseitigt G7-a nicht**. DEC-01 hat die **materielle Herstellung** von Bedingung 7 gewählt und die Auslegungsoption verworfen; ACN-09 bleibt voll wirksam | **INFERENCE (stark)** |
| **Ist (b) dadurch ausgeschlossen?** | **NICHT ENTSCHIEDEN.** OD-08 ist eine eigenständige registrierte Position mit unverengtem Optionsraum; ob DEC-01 (b) faktisch ausschließt, ist eine **Human Decision** [G7-PREP A1-9] | **HUMAN DECISION REQUIRED** |
| **Was (b) NICHT bewirkt** | Keine Erfüllung von Bedingung 7 · keine Absenkung von Bedingung 7 (ACN-09) · keine HD-2-Erledigung · keine Coding-Freigabe | **FACT** |

---

## 8. Zielstatus und Verfahren — ausdrückliche Nichtbestimmtheit

| # | Position | Quellenlage | Klasse |
|---|---|---|---|
| Z-1 | **Zielstatus des Sprint-Plan-Dokuments** | **KEINER quellenbestimmt.** Development Standard v1.1 §17 Anh. B definiert States nur für ADR (`Open → Accepted \| Resolved by ADR-XXX`), Specification (`Draft → In Review → Corrections → Approved`), Sprint (`Planned → In Progress → Review → Done`), Release (`Candidate → Verified → Released`) — **kein Sprint-Plan-Dokumentmodell**. ADW-SPR-1.0-001 Kap. 17 nennt nur den **Vorgang**, nicht das **Ziel** | **UNKNOWN — NICHT QUELLENBESTIMMT** |
| Z-2 | **„Vorgesehenes kontrolliertes Verfahren"** | In keiner geprüften Quelle **ausgestaltet** (weder Schritte, noch Instanz, noch Nachweisform) | **UNKNOWN — NICHT QUELLENBESTIMMT** |
| Z-3 | **Analogiebildung** (z. B. Specification-States auf den Sprint Plan anwenden) | **Nicht quellennormiert.** Eine Analogie wäre eine **Festlegung**, keine Feststellung — und damit Gegenstand der Human Decision, nicht dieser PREP | **NICHT QUELLENNORMIERT** |
| Z-4 | **Mit-Änderung von Version / Revision / Datum** | Von **keiner** Quelle verlangt oder ausgeschlossen | **UNKNOWN** |
| Z-5 | **Feststellungsinstanz für den Vollzug** | Nicht ausgestaltet; Autorität für die **Entscheidung** ist belegt (Projekteigner / Governance), für die **Form des Vollzugs** nicht | **UNKNOWN** |

> **Folge (Feststellung, keine Entscheidung):** Eine Wahl von Option (a)
> ist **entscheidbar**, aber ohne zusätzliche Festlegung des Zielstatus
> **nicht vollständig quellengestützt vollziehbar**. Ein A1-EXEC, der sich
> ausschließlich auf Quellen stützt, ist bei ungelöstem Z-1 **nicht
> formulierbar** [G7-PREP **JX-G7P-B-02**].

---

## 9. Zulässiger Change Surface (bei späterem A1-EXEC)

**Diese PREP ändert nichts.** Die folgende Bestimmung gilt für einen
etwaigen späteren, separat zu autorisierenden **A1-EXEC** nach Wahl von (a).

| Ebene | Gegenstand | Zulässigkeit | Beleg |
|---|---|---|---|
| **CS-A1-1** | `docs/milestone-1.0-sprint-plan.md` **Z. 6** (`Status \| **DRAFT**`) | **Kern der Option (a)** — genau diese Zeile ist Gegenstand der Nachführung | G7-PREP A1-1/A1-2; eigene Prüfung Z. 6 |
| **CS-A1-2** | Z. 7 `Version`, Z. 8 `Revision`, Z. 9 `Datum` | **Nicht quellenbestimmt** (Z-4) — nur zulässig, wenn die Human Decision es ausdrücklich festlegt | Q-6/Z-4 |
| **CS-A1-3** | Sprint Plan Z. 301 `OP-1 … (Coding-Bedingung 7) … OFFEN` und Z. 302 `OP-2` | **Mittelbar berührt, aber von keiner Quelle verlangt** und **nicht Gegenstand von A1** | G7-PREP A1-1 |
| **CS-A1-4** | Sprint Plan Z. 90 (Verweis Coding-Bedingung 8 / RL-05) | wie CS-A1-3 — **nicht Gegenstand** | G7-PREP A1-1 |
| **CS-A1-5** | Inhaltliche Fortschreibung (z. B. Aufnahme des OD-05-Umrisses) | **AUSGESCHLOSSEN** in A1 — das ist der Gegenstand von U-4′/HD-2, nicht von OD-08 | A2-VR Kap. 9; DEC-02 Detail 3 |
| **CS-A1-6** | ADRs · RDRs · Architecture Book · `CLAUDE.md` · `ROADMAP.md` · Implementation Plan · Code · Tests · Konfiguration | **AUSGESCHLOSSEN** | DEC-02 Details 9/10 |
| **CS-A1-7** | Bestehende Governance-/Archivdateien | **AUSGESCHLOSSEN** (kein Umschreiben) | durchgehende Vorkette |

**Bei Option (b): Change Surface = LEER.** Kein Dateivollzug; ausschließlich
ein Decision Record dokumentiert die Wahl.

---

## 10. Entscheidungsrelevante offene Punkte

| # | Offener Punkt | Wirkung auf die Entscheidung |
|---|---|---|
| OP-A | **Z-1 Zielstatus nicht quellenbestimmt** | Bei Wahl (a) muss die Human Decision den Zielstatus **selbst festlegen**, sonst bleibt A1-EXEC blockiert |
| OP-B | **Z-2 Verfahren nicht ausgestaltet** | Bei Wahl (a) muss die Human Decision entweder ein Verfahren benennen oder den Vollzug als einfache Kopfänderung mit eigenem EXEC-Auftrag freigeben |
| OP-C | **A1-9 — Verhältnis (b) ↔ DEC-01** | Nur der Projekteigner kann feststellen, ob (b) angesichts der gewählten materiellen Herstellung noch offensteht |
| OP-D | **U-4′ UNDETERMINED** | Betrifft **G7-b**, nicht (a)/(b). Die OD-08-Wahl ist davon **unabhängig entscheidbar**; die **Erfüllung von Bedingung 7** ist es nicht |
| OP-E | **HD-2 DEFERRED** | Unberührt; keine Vorbedingung der OD-08-Wahl (kein Quellenbeleg für eine solche Kopplung) |

---

## 11. Empfehlung — **ausdrücklich KEINE Entscheidung**

> **Diese Empfehlung ist unverbindlich. Sie bevorzugt eine Option, trifft
> aber keine Wahl und verengt den Optionsraum (a)/(b) nicht.**

**Empfohlen: Option (a) — mit gleichzeitiger Festlegung des Zielstatus.**

Begründung, jeweils quellengestützt:

| # | Grund | Beleg | Klasse |
|---|---|---|---|
| E-1 | Die Quellen führen (a) bereits als Empfehlungsrichtung: „Redaktionell, nicht dringlich" — also als **vorgesehen**, nur nicht **dringlich** | MEP §20 OD-08; DEM §366 | **FACT** (Wortlaut) |
| E-2 | ADW-SPR-1.0-001 Kap. 17 sieht eine Nachführung als **antizipierten, separat autorisierten Schritt** vor — (a) ist damit der von der Genehmigungsentscheidung selbst mitgedachte Weg | ADW-SPR-1.0-001 Kap. 17 | **FACT** |
| E-3 | (b) beseitigt **G7-a nicht**; DEC-01 hat die **materielle Herstellung** gewählt | G7-PREP A1-9; DEC-01 | **INFERENCE (stark)** |
| E-4 | Der einzige praktische Einwand gegen (a) ist die **Zielstatus-Lücke** (Z-1) — sie ist durch die Human Decision selbst schließbar, ohne Absenkung irgendeiner Bedingung | Z-1; ACN-09 unberührt | **OBSERVATION** |

**Ausdrücklich mitzuentscheiden, falls (a) gewählt wird:** der **Zielstatus**
(Z-1) und, soweit gewünscht, die Behandlung von Version/Revision/Datum
(Z-4). Ohne diese Festlegung ist ein quellengestützter A1-EXEC nicht
formulierbar.

**Gegen die Empfehlung sprechende, ebenfalls belegte Lage:** DEM stuft
OD-08 als **P3, nicht dringlich, ohne Blocker, „NO CURRENT SPRINT"** ein —
eine Wahl von (b) oder eine erneute Vertagung wäre governance-seitig
**nicht ausgeschlossen** und bleibt allein der Autorität des Projekteigners
vorbehalten.

---

## 12. Beobachtungen (Feststellungen, keine Entscheidungen)

| ID | Beobachtung | Klasse |
|---|---|---|
| **JX-A1-OD08-P-B-01** | **Die OD-08-Wahl erfüllt Bedingung 7 auch bei (a) nicht.** (a) adressiert ausschließlich **G7-a**; **G7-b** bleibt offen und hängt an U-4′ (UNDETERMINED) und ggf. HD-2. Eine Feststellung „Bedingung 7 erfüllt" wäre ein **eigener, späterer Akt** | TRACEABILITY |
| **JX-A1-OD08-P-B-02** | **Die Bündelungsempfehlung „gemeinsam mit OD-01" ist überholt.** GDR-OD01-001 ist FINAL (Option C) und hat die Bündelung ausdrücklich **nicht** vollzogen (Kap. 13 Z. 306). Die Empfehlung bleibt als Wortlaut bestehen, ist aber praktisch nicht mehr ausführbar | OBSERVATION |
| **JX-A1-OD08-P-B-03** | **Entscheidbarkeit ≠ Vollziehbarkeit.** OD-08 ist trotz Z-1/Z-2 **entscheidbar** (DEM: „Blocker: keine"). Die Lücken betreffen den **Vollzug** bei (a), nicht die Wahl | OBSERVATION |
| **JX-A1-OD08-P-B-04** | **Sprint Plan Z. 301 führt OP-1 („Genehmigung dieses Sprint Plans (Coding-Bedingung 7)") weiterhin als OFFEN** — unabhängig verifiziert. Ob diese Zeile bei (a) mit nachzuführen wäre, ist **von keiner Quelle verlangt** und hier **nicht entschieden** (CS-A1-3) | OBSERVATION / **NICHT ENTSCHIEDEN** |

---

## 13. Explicit Non-Decisions (dieser PREP-Welle)

```text
OD-08: NICHT entschieden. Optionsraum (a)/(b) NICHT verengt, NICHT erweitert — OPEN.
Empfehlung: unverbindlich, KEINE Entscheidung, KEINE Vorwegnahme.
Zielstatus / Verfahren: NICHT festgelegt, NICHT analogisiert — NICHT QUELLENBESTIMMT.
A1: NICHT ausgefuehrt, kein EXEC erteilt, kein Vollzug vorbereitet ueber diese PREP hinaus.
Sprint Plan: NICHT geaendert, Statuskopf NICHT nachgefuehrt — DRAFT / 1.0 / R0.
U-4': NICHT materiell beantwortet — UNDETERMINED / HUMAN REVIEW REQUIRED.
Bedingung 7: NICHT erfuellt, NICHT abgesenkt, NICHT umgedeutet (ACN-09 gewahrt).
HD-2: NICHT entschieden, NICHT wiedervorgelegt — DEFERRED / OPEN / NOT DECIDED.
RL-05: NICHT vorbereitet, NICHT entschieden — NOT REACHED. OP-2: NICHT erfuellt.
Coding: NOT AUTHORIZED. QG-006 / QG-001..QG-008: NOT STARTED — vollstaendig unberuehrt.
OD-05 / ADR-012 / ADRs / RDRs / Architecture Book / Implementation Plan: UNVERAENDERT.
CLAUDE.md / ROADMAP.md / Code / Tests / Konfiguration: UNVERAENDERT.
DEC-01, DEC-02, G7-PREP, A2-EXEC, A2-VERIFY und alle Archive: NICHT umgeschrieben.
Keine Human Decision simuliert, erweitert oder vorweggenommen.
Vorbestehende Working-Tree-Aenderungen unangetastet. Kein Push, PR, Merge, Tag.
```

---

## 14. Change Surface dieser Welle

| Gegenstand | Umfang |
|---|---|
| Neue Dateien | **genau eine** — `docs/audits/jx-dev-spr01-rl05-g7-a1-od08-prep-r0.md` |
| Geänderte / gelöschte Dateien | **keine** |
| Sprint Plan / ADRs / RDRs / Architecture Book / `CLAUDE.md` / `ROADMAP.md` | **UNBERÜHRT** |
| Code / Tests / Konfiguration | **UNBERÜHRT** — baseline-identisch |
| Bestehende Governance-/Archivdateien | **UNBERÜHRT** |
| Vorbestehende Working-Tree-Änderungen | **UNANGETASTET** |

---

## 15. Preflight

| # | Prüfung | Ergebnis |
|---|---|---|
| 1 | DEC-02 Condition 5 erlaubt A1-Vorbereitung (A2 + VERIFY abgeschlossen) | **PASS** |
| 2 | Baseline `fa6e192`, Staging leer, produktiver Baum baseline-identisch | **PASS** |
| 3 | Quellen gegen aktuellen Stand geprüft (Kap. 5, Q-1…Q-10) | **PASS** |
| 4 | Option (a) und (b) exakt bestimmt (Kap. 6/7) | **PASS** |
| 5 | Change Surface bestimmt (Kap. 9) | **PASS** |
| 6 | Zielstatus/Verfahren nur soweit beschrieben, wie Quellen tragen; Nichtbestimmtheit ausdrücklich festgestellt (Kap. 8) | **PASS** |
| 7 | Keine eigene Governance-Entscheidung; Empfehlung als unverbindlich gekennzeichnet | **PASS** |
| 8 | U-4′ nicht beantwortet · HD-2 nicht entschieden · A1 nicht ausgeführt | **PASS** |
| 9 | Bedingung 7 nicht als erfüllt festgestellt · RL-05 nicht vorbereitet | **PASS** |
| 10 | Coding / QG-006 unberührt | **PASS** |
| 11 | Genau eine neue Datei; keine bestehende Datei verändert | **PASS** |
| 12 | Kein Push / PR / Merge / Tag | **PASS** |

**Preflight: PASS**

---

## 16. Final Gate

> ## **JX-DEV-SPR01-RL05-G7-A1-OD08-PREP-01-R0 = COMPLETED — PREPARATION ONLY**
>
> **OD-08 = OPEN · Optionsraum (a)/(b) unverengt · KEINE Entscheidung getroffen**
> **Zielstatus (Z-1) und Verfahren (Z-2) = NICHT QUELLENBESTIMMT**
> **Bedingung 7 = NICHT ERFÜLLT · U-4′ = UNDETERMINED · HD-2 = DEFERRED/OPEN**
> **A1 = NICHT AUSGEFÜHRT · RL-05 = NOT REACHED · CODING = NOT AUTHORIZED ·
> QG-006 = NOT STARTED**

---

## 17. Commit / Push Status

| Position | Status |
|---|---|
| Commit | **genau EIN Commit**, ausschließlich diese PREP-Datei |
| Commit-Message | `docs: prepare OD-08 option space human decision (A1 PREP)` |
| Push / PR / Merge / Tag | **NICHT DURCHGEFÜHRT** |

---

## 18. Benötigte Human Decision — genau eine

**Autorität:** Projekteigner / Governance [MEP §20 OD-08; DEM §1.1 Z. 109]

**Frage:** Welche Option des registrierten OD-08-Optionsraums wird gewählt?

| Option | Wahl |
|---|---|
| **(a)** | Sprint-Plan-Kopf/Status im vorgesehenen kontrollierten Verfahren **nachführen** — **zusätzlich festzulegen: Zielstatus (Z-1)**, optional Behandlung von Version/Revision/Datum (Z-4) |
| **(b)** | Sprint-Plan-Status **unverändert belassen** (DRAFT / 1.0 / R0), da die Genehmigungskette dokumentiert ist |

**Vorlageformat (auszufüllen durch den Projekteigner):**

```text
JX-DEV-SPR01-RL05-G7-A1-OD08-DEC-01-R0

Authority:  Projekteigner
Date:       <YYYY-MM-DD>
Decision:   OPTION (a)  |  OPTION (b)

Falls (a):
  Zielstatus des Sprint-Plan-Kopfes: <Wert>
  Version / Revision / Datum:        <unveraendert | Wert>
  Verfahren:                         <Benennung | einfache Kopfaenderung per separatem A1-EXEC>

Conditions:
- Kein Coding, kein RL-05, kein QG-006.
- Bedingung 7 wird durch diese Entscheidung NICHT als erfuellt festgestellt.
- U-4' wird NICHT beantwortet; HD-2 bleibt DEFERRED/OPEN.
- Keine inhaltliche Aenderung des Sprint Plans (kein OD-05-Umriss).
- Vollzug nur ueber separaten A1-EXEC-Auftrag.
- ACN-09 gewahrt; keine Bedingung abgesenkt.
- Vorbestehende Working-Tree-Aenderungen unangetastet. Kein Push.
```

**Danach — und nur danach — zulässig:**
bei **(a)** ein separater **A1-EXEC** (Change Surface CS-A1-1, ggf. CS-A1-2);
bei **(b)** ausschließlich ein **Decision Record**, kein Vollzug.

**Es wird nicht automatisch weitergearbeitet. STOP nach dieser PREP.**

---

## 19. Revision History

| Revision | Datum | Änderung | Status |
|---|---|---|---|
| **R0** | 2026-08-13 | Entscheidungsvorbereitung OD-08: Quellenprüfung gegen HEAD `fa6e192`, exakte Bestimmung der Optionen (a)/(b), zulässiger Change Surface, ausdrückliche Feststellung der Nichtbestimmtheit von Zielstatus und Verfahren, unverbindliche Empfehlung | **COMPLETED — PREPARATION ONLY** |

---

**Ende JX-DEV-SPR01-RL05-G7-A1-OD08-PREP-01-R0 — Decision Preparation —
JOCHEN X Milestone 1.0 (2026-08-13) — HEAD `fa6e192` — Bezugs-Baseline
`MILESTONE-1.0-BASELINE = 8fcf42f1997dfcf6ff232e75fd33c37b933991c8`**
