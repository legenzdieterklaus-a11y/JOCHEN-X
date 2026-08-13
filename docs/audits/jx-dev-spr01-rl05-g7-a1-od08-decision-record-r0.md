# JOCHEN X — Milestone 1.0
# JX-DEV-SPR01-RL05-G7-A1-OD08-DEC-01-R0 — Human Decision Record
## OD-08 — OPTION (a): Sprint-Plan-Kopf/Status nachführen

> **COMPLETED — HUMAN DECISION RECORDED**
>
> Dieses Dokument zeichnet die Human-Entscheidung des **Projekteigners**
> vom **2026-08-13** zum registrierten OD-08-Optionsraum auf:
> **OPTION (a) — Sprint-Plan-Kopf/Status nachführen.**
>
> **DEC ≠ EXEC.** Diese Welle **führt nichts aus**. Der Sprint Plan wird
> **nicht** verändert; sein Kopf trägt unverändert **DRAFT / 1.0 / R0**.
>
> **Die Entscheidung legt KEINEN konkreten Zielstatus fest.** Sie
> autorisiert die Nachführung **dem Grunde nach**. **Z-1 (Zielstatus) und
> Z-2 (kontrolliertes Verfahren) bleiben OFFEN und nicht quellenbestimmt.**
> Solange sie offen sind, ist **kein A1-EXEC** formulierbar oder zulässig.
>
> **OD-08 = DECIDED (Option a) · VOLLZUG AUSSTEHEND** ·
> **A1-EXEC = NICHT ERTEILT** · **U-4′ = UNDETERMINED / HUMAN REVIEW REQUIRED** ·
> **BEDINGUNG 7 = NICHT ERFÜLLT** · **HD-2 = DEFERRED / OPEN / NOT DECIDED** ·
> **RL-05 = NOT REACHED** · **CODING = NOT AUTHORIZED** · **QG-006 = NOT STARTED**

---

## 1. Document Identity

| Feld | Wert |
|---|---|
| **Document ID** | **JX-DEV-SPR01-RL05-G7-A1-OD08-DEC-01-R0** |
| Mode / Wave | GOVERNANCE · **DEC** (Human Decision Record) |
| Subject | OD-08 — Wahl im registrierten Optionsraum (a)/(b) |
| Date | 2026-08-13 |
| Pfad | `docs/audits/jx-dev-spr01-rl05-g7-a1-od08-decision-record-r0.md` |
| **Bezugs-PREP** | `docs/audits/jx-dev-spr01-rl05-g7-a1-od08-prep-r0.md` (`8e51c33`) — **nicht umgeschrieben** |
| **Bezugs-Baseline** | `MILESTONE-1.0-BASELINE = 8fcf42f1997dfcf6ff232e75fd33c37b933991c8` (GDR-003) |
| HEAD bei Beginn | `8e51c333fc767d5f78b9156ac93269b47510445b` = `8e51c33` |
| Branch | `milestone-1.0-governance` |
| Vorkette | `3b76b89` (DEC-02) → `a13a148` (A2-EXEC) → `fa6e192` (A2-VERIFY) → `8e51c33` (A1-OD08-PREP) |
| **Status** | **COMPLETED — HUMAN DECISION RECORDED** |

---

## 2. Baseline Gate

| Prüfung | Ergebnis |
|---|---|
| **HEAD** | `8e51c333fc767d5f78b9156ac93269b47510445b` — „docs: prepare OD-08 option space human decision (A1 PREP)" — **erwarteter Stand** |
| PREP-Commit `8e51c33` Inhalt | **genau 1 Datei**, `docs/audits/jx-dev-spr01-rl05-g7-a1-od08-prep-r0.md`, 359 Zeilen, reine Neuanlage |
| `3b76b89` (DEC-02) Vorfahr von HEAD | **JA** |
| `a13a148` (A2-EXEC) Vorfahr von HEAD | **JA** |
| `fa6e192` (A2-VERIFY) Vorfahr von HEAD | **JA** |
| `8e51c33` (PREP) Vorfahr von HEAD | **JA** (HEAD == `8e51c33`) |
| Staging vor Beginn | **leer** |
| Produktiver Baum vs. `8fcf42f` (`app core sdk ui config tests src`) | **0 Dateien** — baseline-identisch |
| **Sprint Plan am HEAD** | Z. 6 `Status \| **DRAFT**` · Z. 7 `Version \| 1.0` · Z. 8 `Revision \| R0` · Z. 9 `Datum \| 2026-08-09` — **unverändert, direkt verifiziert** |
| **Working Tree** | 3 vorbestehende getrackte Modifikationen (`CLAUDE.md`, `ROADMAP.md`, `docs/architecture-book-v2.md`) + vorbestehende untracked Dokumente — **unangetastet, nicht bereinigt, nicht committet** |

**Baseline Gate: PASS.** Keine neue Baseline definiert.

---

## 3. Decision Verification (gegen die PREP)

| Prüfung | Ergebnis |
|---|---|
| **PREP vorhanden und einschlägig** | **JA** — `JX-DEV-SPR01-RL05-G7-A1-OD08-PREP-01-R0`, Status COMPLETED — PREPARATION ONLY |
| **Optionsraum deckungsgleich** | **JA** — PREP Kap. 4/6/7 und MEP §20 OD-08: „(a) Kopf im vorgesehenen kontrollierten Verfahren nachführen; (b) belassen, da die Genehmigungskette dokumentiert ist". Die Entscheidung wählt **(a)** — eine der beiden registrierten Optionen. **Kein Scope-Mismatch**, keine Erweiterung des Optionsraums |
| **Authority** | **Projekteigner / Governance** — genau die in MEP §20 OD-08 und DEM §1.1 Z. 109 („Entscheidung nötig? **JA** — Projekteigner / Governance") ausgewiesene Instanz. **VERIFIZIERT** |
| **Date** | **2026-08-13** — chronologisch konsistent (nach Erstellung und Commit der PREP, `8e51c33`) |
| **Begründungslage** | Die Entscheidung folgt der PREP-Empfehlung (Kap. 11: E-1 bis E-4), **behandelt sie aber ausdrücklich nicht als automatische Entscheidung**. Die Empfehlung war unverbindlich; die Wahl ist ein eigenständiger Willensakt des Projekteigners |
| **Zielstatus mitentschieden?** | **NEIN** — die Entscheidung legt **keinen** konkreten Zielwert fest und untersagt ausdrücklich jede Erfindung oder Übertragung aus fremden Statusmodellen. Siehe Kap. 6 |
| **Konsistenz mit PREP Z-1/Z-2** | **JA** — PREP Kap. 8 hatte Zielstatus und Verfahren als **NICHT QUELLENBESTIMMT** ausgewiesen; die Entscheidung bestätigt diese Lage, statt sie zu überspielen |
| **Konsistenz mit PREP JX-A1-OD08-P-B-03** | **JA** — „Entscheidbarkeit ≠ Vollziehbarkeit": OD-08 wird entschieden, der Vollzug bleibt gesperrt |
| **Verbotene Inferenzen** | **keine gezogen** — insbesondere nicht „Option (a) gewählt ⇒ Statuskopf geändert", nicht „Option (a) gewählt ⇒ G7-a beseitigt", nicht „Option (a) gewählt ⇒ Bedingung 7 näher an Erfüllung", nicht „Empfehlung vorhanden ⇒ Entscheidung getroffen" |
| **Widersprüche** | **keine** |
| **Fehlende Voraussetzung** | **keine für die Entscheidung**; für den **Vollzug** fehlen Z-1 und Z-2 (Kap. 6/7) — ausdrücklich als solche geführt |

> **HUMAN DECISION VERIFIED — kein Scope-Mismatch, kein Widerspruch,
> kein STOP-Tatbestand.**

---

## 4. Human Decision — wörtlich, unverändert

```text
JX-DEV-SPR01-RL05-G7-A1-OD08-DEC-01-R0

Authority:
Projekteigner

Date:
2026-08-13

Decision:
OPTION (a) — Sprint-Plan-Kopf/Status nachfuehren.

Begruendung:
Die PREP empfiehlt Option (a), weil sie den G7-a-Befund adressiert.
Option (b) beseitigt G7-a nicht.
Die Empfehlung ist jedoch nicht als automatische Entscheidung zu behandeln.

Wichtige Bedingung:
Der Zielstatus des Sprint-Plan-Dokuments ist laut PREP nicht quellenbestimmt.
Er darf NICHT erfunden oder aus ADR-/Specification-/Sprint-/Release-
Statusmodellen uebertragen werden.

Decision Detail:

1. Keine EXEC-Ausfuehrung in dieser Welle.
2. Keine Aenderung am Sprint Plan.
3. Kein HD-2-Entscheid.
4. Keine materielle Entscheidung zu U-4'.
5. Keine Feststellung, dass Bedingung 7 bereits erfuellt ist.
6. Kein RL-05.
7. Kein Coding.
8. Kein QG-006.
9. Keine Aenderung an ADRs, RDRs, Architecture Book, CLAUDE.md oder ROADMAP.md.
10. Keine bestehenden Governance-Artefakte ueberschreiben.
11. Nur das neue Decision Record darf entstehen.
12. Commit: JA. Push: NEIN.
13. Working Tree: alle vorbestehenden Aenderungen unangetastet lassen.

Next Step:
Separater A1-EXEC nur nach vollstaendiger Festlegung der ausfuehrbaren
Zielwerte.

STOP nach dem Decision Record.
Nicht automatisch mit A1-EXEC weiterarbeiten.
```

Die Entscheidung wird **nicht ergänzt, nicht interpretiert und nicht
umgedeutet**.

---

## 5. Scope der Entscheidung

| Feld | Wert |
|---|---|
| **Gegenstand** | Ausschließlich die Wahl im registrierten OD-08-Optionsraum (a)/(b) |
| **Gewählt** | **(a)** — Sprint-Plan-Kopf/Status nachführen |
| **Reichweite** | **Grundsatzentscheidung („ob")** — nicht „womit", nicht „wie", nicht „wann" |
| **Autorität** | Projekteigner / Governance [MEP §20 OD-08; DEM §1.1 Z. 109] |
| **Charakter** | **DEC** — Governance-Entscheidung ohne physischen Vollzug |
| **Ausdrücklich außerhalb des Scopes** | Zielstatuswert · Ausgestaltung des kontrollierten Verfahrens · Version/Revision/Datum · inhaltliche Fortschreibung des Sprint Plans · U-4′ · HD-2 · Bedingung 7 · RL-05 · Coding · QG-006 · OD-05 / ADR-012 |

---

## 6. Option (a) — Inhalt der getroffenen Wahl

| # | Feststellung | Klasse |
|---|---|---|
| A-1 | Gewählt ist der **wörtliche** Optionstext: „Kopf im vorgesehenen kontrollierten Verfahren nachführen" [MEP §20 OD-08] | **FACT** |
| A-2 | Entschieden ist damit das **Ob** der Nachführung — verbindlich und abschließend für die Grundsatzfrage | **DECIDED** |
| A-3 | **Nicht** entschieden ist der **Zielwert**, auf den der Kopf gesetzt wird (Z-1) | **OFFEN** |
| A-4 | **Nicht** entschieden ist das **Verfahren**, in dem die Nachführung erfolgt (Z-2) | **OFFEN** |
| A-5 | **Nicht** entschieden ist die Behandlung von `Version` / `Revision` / `Datum` (PREP Z-4 / CS-A1-2) | **OFFEN** |
| A-6 | Die Wahl bewirkt **keine** Dateiänderung. Der Vollzug ist ein **separat autorisierter Schritt** [ADW-SPR-1.0-001 Kap. 17] und benötigt einen eigenen **A1-EXEC** [G7-PREP A1-6; DEC-01 Condition 8] | **FACT** |
| A-7 | Option (a) adressiert **G7-a** (Statuskopf). **G7-b** (Nichtabdeckung des OD-05-Umrisses) bleibt unberührt und hängt an U-4′ (UNDETERMINED) und ggf. HD-2 | **FACT** |
| A-8 | Option (b) ist durch diese Wahl **nicht mehr einschlägig**; OD-08 ist als Position **entschieden**, der Optionsraum damit **ausgeübt** — nicht abgesenkt, nicht erweitert | **FACT** |

> **Kernabgrenzung:** Diese Entscheidung ist eine **Autorisierung dem
> Grunde nach**, **keine** Festlegung ausführbarer Zielwerte.

---

## 7. Zielstatus-Unsicherheit **Z-1** — separat dokumentiert

| # | Position | Feststellung |
|---|---|---|
| Z-1.1 | **Ist ein Zielstatus quellenbestimmt?** | **NEIN.** Development Standard v1.1 §17 Anhang B definiert Approval States ausschließlich für **ADR** (`Open → Accepted \| Resolved by ADR-XXX`), **Specification** (`Draft → In Review → Corrections → Approved`), **Sprint** (`Planned → In Progress → Review → Done`) und **Release** (`Candidate → Verified → Released`). Ein Statusmodell für ein **Sprint-Plan-Dokument** existiert dort **nicht** |
| Z-1.2 | **Nennt eine andere Quelle einen Zielwert?** | **NEIN.** ADW-SPR-1.0-001 Kap. 17 nennt ausschließlich den **Vorgang** („eine eventuelle Statusnachführung erfolgt in einem separat autorisierten Schritt"), **nicht** das Ziel. MEP §20 OD-08 nennt „das vorgesehene kontrollierte Verfahren", ohne einen Zielwert zu benennen |
| Z-1.3 | **Darf ein Zielwert hergeleitet werden?** | **NEIN** — ausdrücklich untersagt durch die Human Decision („darf NICHT erfunden oder aus ADR-/Specification-/Sprint-/Release-Statusmodellen übertragen werden"). Eine Analogie wäre eine **Festlegung**, keine Feststellung [PREP Z-3] |
| Z-1.4 | **Legt diese Entscheidung einen Zielstatus fest?** | **NEIN — ausdrücklich nicht.** Sie **autorisiert ausschließlich die Nachführung dem Grunde nach** |
| Z-1.5 | **Wer muss Z-1 klären?** | **Projekteigner / Governance** — dieselbe Autorität, die OD-08 entschieden hat. Die Klärung ist eine **eigene, separat vorzulegende Human Decision** und keine Ableitungsleistung eines Ausführungsschritts |
| Z-1.6 | **Wirkung auf den Vollzug** | **Blockierend.** Ohne festgelegten Zielwert ist ein quellengestützter A1-EXEC **nicht formulierbar** [PREP Kap. 8; G7-PREP **JX-G7P-B-02**] |

> **Z-1 = OFFEN — NICHT QUELLENBESTIMMT — HUMAN DECISION REQUIRED.**

---

## 8. Kontrolliertes Verfahren **Z-2** — separat dokumentiert

| # | Position | Feststellung |
|---|---|---|
| Z-2.1 | **Ist das „vorgesehene kontrollierte Verfahren" ausgestaltet?** | **NEIN** — in keiner geprüften Quelle sind Schritte, Instanz oder Nachweisform benannt [MEP §20 OD-08; G7-PREP A1-3; PREP Q-7] |
| Z-2.2 | **Legt diese Entscheidung ein Verfahren fest?** | **NEIN** |
| Z-2.3 | **Zulässige Klärungswege (nicht gewählt, nur benannt)** | (i) Benennung/Ausgestaltung eines Verfahrens durch Governance-Entscheidung, **oder** (ii) ausdrückliche Feststellung, dass der Vollzug als einfache Kopfänderung über einen separaten A1-EXEC-Auftrag erfolgt. **Beides bedarf einer eigenen Human Decision** |
| Z-2.4 | **Wirkung auf den Vollzug** | **Blockierend, solange weder (i) noch (ii) festgelegt ist** |

> **Z-2 = OFFEN — NICHT QUELLENBESTIMMT — HUMAN DECISION REQUIRED.**

---

## 9. Change Surface für den **späteren** A1-EXEC

**Diese DEC-Welle ändert nichts.** Die folgende Bestimmung ist eine
**Vorabgrenzung** für einen künftigen, separat zu autorisierenden A1-EXEC —
**kein** Auftrag, **keine** Freigabe.

| Ebene | Gegenstand | Zulässigkeit im späteren EXEC |
|---|---|---|
| **CS-A1-1** | `docs/milestone-1.0-sprint-plan.md` **Z. 6** (`Status \| **DRAFT**`) | **Kerngegenstand** — zulässig **erst nach Festlegung von Z-1** |
| **CS-A1-2** | Z. 7 `Version` · Z. 8 `Revision` · Z. 9 `Datum` | **Nur** bei ausdrücklicher Festlegung in der Z-1-Entscheidung (A-5); sonst **unverändert lassen** |
| **CS-A1-3** | Z. 301 `OP-1 … (Coding-Bedingung 7) … OFFEN` · Z. 302 `OP-2` | **NICHT Gegenstand** — von keiner Quelle verlangt [G7-PREP A1-1] |
| **CS-A1-4** | Z. 90 (Verweis Coding-Bedingung 8 / RL-05) | **NICHT Gegenstand** |
| **CS-A1-5** | Inhaltliche Fortschreibung (insb. Aufnahme des OD-05-Umrisses) | **AUSGESCHLOSSEN** — Gegenstand von U-4′/HD-2, nicht von OD-08 |
| **CS-A1-6** | ADRs · RDRs · Architecture Book · `CLAUDE.md` · `ROADMAP.md` · Implementation Plan · Code · Tests · Konfiguration | **AUSGESCHLOSSEN** |
| **CS-A1-7** | Bestehende Governance-/Archivdateien | **AUSGESCHLOSSEN** (kein Umschreiben) |
| **CS-A1-8** | Technische Change Surface CS-1 / CS-2 / CS-3 | **NICHT BERÜHRT** |

**Umfang eines künftigen A1-EXEC: höchstens eine geänderte Datei**
(`docs/milestone-1.0-sprint-plan.md`), höchstens die Kopfzeilen Z. 6
(zwingend) und Z. 7–9 (nur bei ausdrücklicher Festlegung).

---

## 10. DEC ≠ EXEC — ausdrückliche Trennung

| Akt | Status nach dieser Welle |
|---|---|
| **DEC** (Wahl im OD-08-Optionsraum) | **VOLLZOGEN** — Option (a) entschieden und aufgezeichnet |
| **Zielwertfestlegung** (Z-1, ggf. Z-2) | **AUSSTEHEND** — eigene Human Decision erforderlich |
| **EXEC** (physische Kopfänderung) | **NICHT ERTEILT, NICHT AUSGEFÜHRT, NICHT VORBEREITET** |
| Sprint Plan physisch | **UNVERÄNDERT — DRAFT / 1.0 / R0** |
| Folgt aus „Option (a) entschieden" ein Ausführungsrecht? | **NEIN** — der Vollzug ist ein separat autorisierter Schritt [ADW-SPR-1.0-001 Kap. 17] |
| Folgt aus dieser DEC eine automatische Fortsetzung? | **NEIN — STOP nach dem Decision Record** |

---

## 11. Governance-State nach dieser DEC

| Position | Status |
|---|---|
| **OD-08** | **DECIDED — OPTION (a)** (Projekteigner, 2026-08-13). Position entschieden; **Vollzug ausstehend**; nicht geschlossen im Sinne eines vollzogenen Ergebnisses |
| **Z-1 Zielstatus** | **OFFEN — NICHT QUELLENBESTIMMT — HUMAN DECISION REQUIRED** |
| **Z-2 Kontrolliertes Verfahren** | **OFFEN — NICHT QUELLENBESTIMMT — HUMAN DECISION REQUIRED** |
| **A1 (Statusnachführung)** | **AUTORISIERT DEM GRUNDE NACH — NICHT AUSGEFÜHRT**; A1-EXEC **nicht erteilt** |
| **Sprint Plan** | **UNVERÄNDERT — DRAFT / 1.0 / R0** |
| **G7-a** (Statuskopf) | **entschieden adressiert, aber NICHT beseitigt** — Beseitigung setzt den Vollzug voraus |
| **G7-b** (OD-05-Umriss nicht abgedeckt) | **UNVERÄNDERT OFFEN** |
| **U-4′** | **UNDETERMINED / HUMAN REVIEW REQUIRED — unverändert** |
| **IP §10.6 Bedingung 7** | **NICHT ERFÜLLT — unverändert** |
| **IP §10.6 Bedingung 8** | **ERFÜLLT — unverändert** |
| **IP §10.6 Bedingung 9 / RL-05** | **NICHT ERFÜLLT / NOT REACHED** |
| **HD-2** | **DEFERRED / OPEN / NOT DECIDED — unverändert** |
| **HD-1 / HD-3 / HD-4 / AC-16 / TD-19** | **UNVERÄNDERT** |
| **OI-1** | **OPEN** (an HD-2 gebunden) |
| **OD-05 / ADR-012 / ADR-005-007** | **UNVERÄNDERT** |
| **OD-01 (GDR-OD01-001)** | **UNVERÄNDERT FINAL** — Bündelung weiterhin nicht vollzogen |
| **OP-1 / OP-2** | **UNVERÄNDERT OFFEN** |
| **Ausschlussgründe 1–8 (IP §10.6)** | **keiner aktiv — unverändert** |
| **Coding (Ebene D)** | **NOT AUTHORIZED** |
| **QG-006 / QG-001…QG-008 (Ebene E)** | **NOT STARTED** |
| **Produktionscode / Tests / Konfiguration** | **UNVERÄNDERT — baseline-identisch** |

---

## 12. Explicit Non-Decisions

```text
EXEC: NICHT ausgefuehrt, NICHT erteilt, NICHT vorbereitet.
Zielstatus (Z-1): NICHT festgelegt, NICHT erfunden, NICHT aus ADR-/Specification-/
    Sprint-/Release-Statusmodellen uebertragen, NICHT analogisiert — OFFEN.
Kontrolliertes Verfahren (Z-2): NICHT ausgestaltet, NICHT benannt — OFFEN.
Version / Revision / Datum: NICHT disponiert.
Sprint Plan: NICHT geaendert, Kopf NICHT nachgefuehrt — DRAFT / 1.0 / R0.
G7-a: NICHT beseitigt (Beseitigung setzt Vollzug voraus).
G7-b: NICHT beruehrt.
U-4': NICHT materiell beantwortet — UNDETERMINED / HUMAN REVIEW REQUIRED.
Bedingung 7: NICHT als erfuellt festgestellt, NICHT abgesenkt, NICHT umgedeutet;
    ACN-09 gewahrt.
HD-2: NICHT entschieden, NICHT wiedervorgelegt, NICHT neu bewertet — DEFERRED/OPEN.
HD-1 / HD-3 / HD-4 / AC-16 / TD-19: UNVERAENDERT.
OD-05 / ADR-012 / ADR-005/006/007: NICHT bewertet, NICHT geaendert.
RL-05: NICHT festgestellt, NICHT vorbereitet — NOT REACHED. OP-2: NICHT erfuellt.
Coding: NOT AUTHORIZED. QG-006 / QG-001..QG-008: NOT STARTED — unberuehrt.
ADRs / RDRs / Architecture Book / Implementation Plan / CLAUDE.md / ROADMAP.md:
    UNVERAENDERT.
Code / Tests / Konfiguration: UNVERAENDERT.
PREP, DEC-01, DEC-02, G7-PREP, A2-EXEC, A2-VERIFY und alle Archive:
    NICHT umgeschrieben.
Keine weitere Human Decision simuliert, erweitert oder vorweggenommen.
Kein Optionsraum erweitert oder abgesenkt. Keine Ausnahme konstruiert.
Vorbestehende Working-Tree-Aenderungen unangetastet.
Kein Push, kein PR, kein Merge, kein Tag.
```

---

## 13. Change Surface dieser Welle

| Gegenstand | Umfang |
|---|---|
| Neue Dateien | **genau eine** — `docs/audits/jx-dev-spr01-rl05-g7-a1-od08-decision-record-r0.md` |
| Geänderte / gelöschte Dateien | **keine** |
| PREP-Artefakt | **UNVERÄNDERT** — ausschließlich gelesen |
| Sprint Plan / ADRs / RDRs / Architecture Book / `CLAUDE.md` / `ROADMAP.md` | **UNBERÜHRT** |
| Bestehende Governance-/Archivdateien | **UNBERÜHRT** |
| Code / Tests / Konfiguration | **UNBERÜHRT** — baseline-identisch |
| Vorbestehende Working-Tree-Änderungen | **UNANGETASTET** |

---

## 14. Beobachtungen (Feststellungen, keine Entscheidungen)

| ID | Beobachtung | Klasse |
|---|---|---|
| **JX-A1-OD08-D-B-01** | **Entschieden ≠ vollzogen.** OD-08 ist als Position entschieden; der Befund G7-a besteht physisch fort, bis der Kopf tatsächlich nachgeführt ist. Eine Statusaussage „G7-a beseitigt" wäre derzeit unzutreffend | TRACEABILITY |
| **JX-A1-OD08-D-B-02** | **Die Entscheidung schließt eine Lücke nicht, sondern schreibt sie fort.** Z-1 und Z-2 waren in der PREP als nicht quellenbestimmt ausgewiesen und bleiben es. Die Wahl von (a) macht ihre Klärung nunmehr **vollzugskritisch** — sie ist die einzige verbleibende Hürde vor einem A1-EXEC | OBSERVATION |
| **JX-A1-OD08-D-B-03** | **Bedingung 7 bleibt zweigliedrig blockiert.** Selbst nach vollzogener Nachführung (G7-a) bliebe **G7-b** offen, dessen normative Relevanz mit **U-4′ = UNDETERMINED** ungeklärt ist. Aus dem Vollzug von (a) folgt daher **nicht** die Erfüllung von Bedingung 7 | TRACEABILITY |
| **JX-A1-OD08-D-B-04** | **Kein Automatismus zu HD-2.** Die OD-08-Entscheidung berührt die Sprint-/WP-Zuordnungsfrage nicht; HD-2 bleibt ein eigenständiger, vertagter Strang | OBSERVATION |

---

## 15. Preflight

| # | Prüfung | Ergebnis |
|---|---|---|
| 1 | Baseline gegen HEAD `8e51c33` verifiziert; Vorkette vollständig; Staging leer | **PASS** |
| 2 | PREP-Inhalt und Optionsraum verifiziert; kein Scope-Mismatch | **PASS** |
| 3 | Human Decision wörtlich und unverändert archiviert (Kap. 4) | **PASS** |
| 4 | Option (a) ausdrücklich aufgezeichnet | **PASS** |
| 5 | Z-1 separat dokumentiert; kein Zielwert erfunden oder übertragen | **PASS** |
| 6 | Z-2 separat dokumentiert | **PASS** |
| 7 | Ausdrücklich festgehalten, dass **kein** konkreter Zielstatus festgelegt wird (Z-1.4 / A-3) | **PASS** |
| 8 | **DEC ≠ EXEC** — kein Vollzug, kein EXEC-Auftrag | **PASS** |
| 9 | Sprint Plan unverändert (direkt verifiziert, Z. 6–9) | **PASS** |
| 10 | HD-2 nicht entschieden · U-4′ nicht beantwortet · Bedingung 7 nicht erfüllt | **PASS** |
| 11 | Kein RL-05 · kein Coding · kein QG-006 | **PASS** |
| 12 | Keine Änderung an ADRs, RDRs, Architecture Book, `CLAUDE.md`, `ROADMAP.md` | **PASS** |
| 13 | Kein bestehendes Governance-Artefakt überschrieben | **PASS** |
| 14 | Genau eine neue Datei; genau ein Commit | **PASS** |
| 15 | Vorbestehende Working-Tree-Änderungen unangetastet | **PASS** |
| 16 | Kein Push / PR / Merge / Tag | **PASS** |

**Preflight: PASS**

---

## 16. Final Governance Gate

> ## **JX-DEV-SPR01-RL05-G7-A1-OD08-DEC-01-R0 = COMPLETED — HUMAN DECISION RECORDED**
> ## **OD-08 = OPTION (a) — SPRINT-PLAN-KOPF/STATUS NACHFÜHREN** (Projekteigner, 2026-08-13)
>
> **Autorisiert ist die Nachführung DEM GRUNDE NACH — kein Zielstatus festgelegt.**
> **Z-1 (Zielstatus) = OFFEN · Z-2 (Verfahren) = OFFEN — beide NICHT QUELLENBESTIMMT**
> **A1-EXEC = NICHT ERTEILT · Sprint Plan = UNVERÄNDERT DRAFT / 1.0 / R0**
> **G7-a = adressiert, NICHT beseitigt · G7-b = UNVERÄNDERT OFFEN**
> **U-4′ = UNDETERMINED · Bedingung 7 = NICHT ERFÜLLT · HD-2 = DEFERRED/OPEN**
> **RL-05 = NOT REACHED · OP-2 = NICHT ERFÜLLT · CODING = NOT AUTHORIZED ·
> QG-006 = NOT STARTED**

---

## 17. Commit / Push Status

| Position | Status |
|---|---|
| Commit | **genau EIN Commit**, ausschließlich `docs/audits/jx-dev-spr01-rl05-g7-a1-od08-decision-record-r0.md` |
| Andere Dateien im Commit | **keine** |
| Commit-Message | `docs: record OD-08 decision option a (status update authorized)` |
| Push / PR / Merge / Tag | **NICHT DURCHGEFÜHRT** |

---

## 18. Next Step

> **Ein separater A1-EXEC ist zulässig — aber ausschließlich nach
> vollständiger Festlegung der ausführbaren Zielwerte.**

| # | Erforderlicher nächster Akt | Charakter | Voraussetzung |
|---|---|---|---|
| 1 | **Human Decision zu Z-1** — konkreter Zielwert des Sprint-Plan-Statuskopfes (Z. 6), optional Behandlung von `Version` / `Revision` / `Datum` (Z. 7–9) | **DEC** — Festlegung, nicht Ableitung | Autorität: Projekteigner / Governance |
| 2 | **Human Decision zu Z-2** — Benennung des kontrollierten Verfahrens **oder** ausdrückliche Feststellung, dass der Vollzug als einfache Kopfänderung per separatem EXEC erfolgt | **DEC** | wie 1; kann mit 1 in einer Welle erfolgen |
| 3 | **A1-EXEC** — physischer Vollzug im Rahmen CS-A1-1 (ggf. CS-A1-2) | **EXEC** | **erst nach 1 und 2**; eigener Auftrag |

**Nicht zulässig ohne die Akte 1–3:** Änderung des Sprint Plans · Feststellung
„G7-a beseitigt" · Feststellung „Bedingung 7 erfüllt" · RL-05-DEC · Coding ·
QG-006.

**Weiterhin unberührt und separat zu führen:** U-4′ (materielle Human
Decision, falls gewünscht) · HD-2 (Wiedervorlage) · G7-b.

**STOP NACH DIESEM DECISION RECORD. Es wird nicht automatisch mit dem
A1-EXEC weitergearbeitet.**

---

## 19. Revision History

| Revision | Datum | Änderung | Status |
|---|---|---|---|
| **R0** | 2026-08-13 | Aufzeichnung der Human-Entscheidung OD-08 = **OPTION (a)** (Nachführung dem Grunde nach autorisiert); Z-1 und Z-2 ausdrücklich als offen und nicht quellenbestimmt dokumentiert; kein Zielstatus festgelegt; kein EXEC erteilt | **COMPLETED — HUMAN DECISION RECORDED** |

---

**Ende JX-DEV-SPR01-RL05-G7-A1-OD08-DEC-01-R0 — Human Decision Record —
JOCHEN X Milestone 1.0 (2026-08-13) — HEAD `8e51c33` — Bezugs-Baseline
`MILESTONE-1.0-BASELINE = 8fcf42f1997dfcf6ff232e75fd33c37b933991c8`**
