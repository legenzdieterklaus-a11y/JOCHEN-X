# JOCHEN X — Milestone 1.0
# OD-01 / BD-03 — Getrennte Behandlung der Dokumentänderungen

## 1. Decision Identity

| Feld | Wert |
|---|---|
| Dokumenttyp | Governance Decision Record |
| **Decision ID** | **GDR-OD01-001** |
| Titel | OD-01 / BD-03 — Getrennte Behandlung der Dokumentänderungen |
| Gegenstand | **OD-01** (Spiegel: **BD-03**) — Disposition der sechs uncommitteten Dokumentänderungen gegenüber `MILESTONE-1.0-BASELINE` |
| Status dieses Records | **FINAL** |
| Entscheidung | **OPTION C — GETRENNTE BEHANDLUNG** |
| Priorität der Position | **P0** (einzige P0-Position des Decision Registers) [DEM §1.1, §1.7] |
| Wirkung | Reine Governance-/Dispositionsentscheidung. **Keine** inhaltliche Änderung an einem Vertragstext, **keine** technische Entscheidung, **keine** physische Repository-Aktion. |
| Branch | `milestone-1.0-governance` |
| Bezugs-Baseline | `MILESTONE-1.0-BASELINE = 8fcf42f1997dfcf6ff232e75fd33c37b933991c8` |

---

## 2. Decision Authority

| Feld | Wert |
|---|---|
| Erforderliche Autorität | **Projekteigner / Governance Architect** [R0 §20 OD-01, §33.2 BD-03; DEM §1.1, §1.7] |
| Entscheidende Instanz | **Projekteigner JOCHEN X** |
| Rolle dieses Dokuments | **Dokumentation einer bereits getroffenen Entscheidung.** Dieser Record trifft keine Entscheidung, er hält sie fest. |
| Autoritätsdeckung | Der Baseline Commit Record §15 Nr. 4 hat die Disposition ausdrücklich als „nächster Entscheidungspunkt des Projekteigners" vorgemerkt — die Entscheidung erfolgt damit durch die vorgesehene Instanz |

---

## 3. Decision Date

| Feld | Wert |
|---|---|
| Datum der Entscheidung | **2026-08-10** |
| Datum dieses Records | **2026-08-10** |
| Vorgelagerte Entscheidung | GDR-003 (2026-08-09, FINAL) → Baseline Commit Record (2026-08-09, FINAL) |

---

## 4. Source Gate

Vor Erstellung dieses Records geprüft (read-only):

| # | Quelle | Status | Verifikation |
|---|---|---|---|
| 1 | `docs/audits/jochen-x-master-engineering-plan-r0.md` | R0, Analyse ohne Entscheidungsautorität | §4.1 (Drei Welten), §4.2 (Trennungsbefund ADR-005/006/007), §20 OD-01 (Optionen a/b/c), §20 OD-05, §24.2, §24.3, §33.2 gelesen |
| 2 | `docs/audits/jochen-x-decision-execution-matrix-r0.md` | R0 | §1.1 (OD-01 = P0), §1.7 (BD-03 BLOCKED), §1.8 (DEV-AB), §D-1, §W-7 gelesen |
| 3 | `docs/audits/jochen-x-decision-briefs-r0.md` | R0 | Brief 1 (OD-01/BD-03) vollständig gelesen — Abschnitte A–N |
| 4 | `docs/governance/milestone-1.0-baseline-commit-record.md` | **FINAL** | §8, §10, §12, §13, §15 Nr. 4 gelesen |
| 5 | `docs/governance/milestone-1.0-baseline-identifier-decision.md` (GDR-003) | **FINAL — OPTION A** | §2, §3, §5, §6 gelesen |
| 6 | `docs/governance/gr-001-governance-decision.md` (GDR-002) | **FINAL — ENTSCHIEDEN** | §1, §2, §3 gelesen — bestätigt: GDR-002 entscheidet ausschließlich `src/jochen_x/**` |
| 7 | `docs/architecture-book-v2.md` | **APPROVED / FROZEN (v2.0) — 2026-07-26** | Statuskopf und Änderungsregel gelesen; **nicht verändert** |
| 8 | `docs/adr/005-plugin-integrity-validation.md` | Welt A: `Open` · Welt B: `APPROVED (2026-07-30)` | Kopfzeilen beider Fassungen gelesen; **nicht verändert** |
| 9 | `docs/adr/006-plugin-permission-model.md` | Welt A: `Open` · Welt B: `APPROVED (2026-07-29)` | dito |
| 10 | `docs/adr/007-plugin-dependency-resolution.md` | Welt A: `Open` · Welt B: `APPROVED (2026-07-29)` | dito |
| 11 | `CLAUDE.md`, `ROADMAP.md` | getrackt modifiziert (uncommittet) | Statuseintrag verifiziert; **nicht verändert** |

**Unabhängige Sachverhaltsverifikation (read-only, 2026-08-10):**

- `git status --porcelain` weist **genau die sechs getrackten Modifikationen** aus: `CLAUDE.md`, `ROADMAP.md`, `docs/adr/005-…md`, `docs/adr/006-…md`, `docs/adr/007-…md`, `docs/architecture-book-v2.md`. Keine weitere getrackte Änderung, kein Staging.
- `git show 8fcf42f:docs/adr/00{5,6,7}-…md` bestätigt in Welt A durchgängig `**Status:** Open – requires decision before implementation`.
- Die Working-Tree-Fassungen tragen `**Status:** APPROVED` mit Approval Date 2026-07-30 / 2026-07-29 / 2026-07-29.
- `docs/architecture-book-v2.md` trägt in **beiden** Welten den Kopfstatus `APPROVED / FROZEN (v2.0)`; die Divergenz betrifft §20 (ADR-Statusspiegel), nicht den Freeze-Status selbst.

> **SOURCE GATE: BESTANDEN.** Keine Pflichtquelle fehlt, keine Quelle ist mehrdeutig identifizierbar.

**Optionsabgleich (Stop-Condition-Prüfung):** Der Wortlaut von Option (c) lautet in
der Quelle „**getrennte Behandlung — ADRs vs. FROZEN Architecture Book vs.
CLAUDE.md/ROADMAP.md**" [R0 §20 OD-01; DEM §D-1; Briefs §D]. Die vom
Projekteigner getroffene Entscheidung ist mit diesem Wortlaut **deckungsgleich**.
Die absolute Stop Condition aus dem Auftrag greift daher **nicht**.

---

## 5. Ausgangslage

| # | Feststellung | Beleg |
|---|---|---|
| 1 | Der produktive Quellcode des Working Tree ist **byte-identisch** mit dem Baseline-Commit. Alle sechs getrackten Modifikationen sind Markdown-/Dokumentationsartefakte. Es existiert **keine** uncommittete Code-, Test- oder Konfigurationsänderung | [R0 §3.3 BV-01; Briefs A-1] |
| 2 | Die sechs Modifikationen umfassen **+1.415 / −119 Zeilen** über sechs Dateien | [R0 §4.2; Briefs A-2] |
| 3 | Am autoritativen Baseline-Commit (Welt A) tragen ADR-005/006/007 den Status „Open – requires decision before implementation". Der APPROVED-Inhalt existiert **ausschließlich** als uncommittete Working-Tree-Modifikation (Welt B) | [R0 §4.2 BV-02; Briefs A-3] |
| 4 | Architecture Book v2.0 §20 führt in Welt A „ADR-005: Open … ADR-006: Open … ADR-007: Open", in Welt B „Approved" | [R0 §4.2; Briefs A-4] |
| 5 | Die Divergenz ist eine **dokumentierte, gewollte Konsequenz** des GDR-003-Scopes (13 Include-Dateien, alle `docs/**`-Pfade ausgeschlossen) — **kein Fehler**, aber mit Nachweisfolge | [R0 §2.3 SG-01, §4.1; Briefs A-7] |
| 6 | Der Baseline Commit Record §15 Nr. 4 hat die Disposition ausdrücklich als „nächster Entscheidungspunkt des Projekteigners" vorgemerkt | [Baseline Commit Record §15; Briefs A-8] |
| 7 | Die Working-Tree-Modifikation berührt das als **FROZEN** geführte Architecture Book v2.0. R0 wertet dies **nicht** als eingetretene Deviation, sondern als offenen Dispositionsgegenstand innerhalb OD-01 | [R0 §4.2 Zusatzbefund; Briefs A-9; DEM §1.8 DEV-AB] |
| 8 | R0 ist es ausdrücklich untersagt, den Widerspruch aufzulösen; die Position ist als OD-01 geführt, als RK-02 gespiegelt und als BD-03 blockiert | [R0 §4.2, §33.2; Briefs A-13] |

**Kern des Problems.** ADR-005/006/007, Architecture Book v2.0 sowie `CLAUDE.md`
und `ROADMAP.md` befinden sich in **unterschiedlichen Governance-/Dokumentklassen**
und können deshalb **nicht als ein einziger homogener Änderungsblock** behandelt
werden:

| Dokumentgruppe | Klasse | Governance-Eigenschaft |
|---|---|---|
| **Gruppe 1** — ADR-005, ADR-006, ADR-007 | Architekturentscheidungen | Eigene Governance-Funktion; eigener Genehmigungs-/Statuslebenszyklus; Bezugstext für TD-04 (ADR-006 D4) und TD-17/SEC-01 (ADR-005) |
| **Gruppe 2** — `docs/architecture-book-v2.md` | Verbindliche Architekturreferenz | **FROZEN (v2.0)**; Änderungsregel: keine inhaltlichen Änderungen an v2.0, nur neue Dokumentversionen + ADR; jede AB-Änderung ist laut Sprint Plan `BASELINE DEVIATION` |
| **Gruppe 3** — `CLAUDE.md`, `ROADMAP.md` | Projekt-/Meta-Dokumente | Arbeits-/Roadmap-Dokumente, **keine** Vertragstexte [Briefs C-3] |

OD-01 ist zudem **keine technische Implementierungsentscheidung**: Es ist keine
Code-Komponente betroffen [DEM §D-1], der produktive Code ist baseline-identisch
[R0 §3.3 BV-01]. OD-01 ist **vollständig** eine Dokumentations- und Vertragsfrage
[Briefs M-2].

---

## 6. Entscheidungsfrage

> **Wie werden die sechs uncommitteten Dokumentänderungen governance-seitig
> disponiert?**

Teilfragen gemäß Decision Brief §C:

| # | Teilfrage | Charakter |
|---|---|---|
| C-1 | Werden ADR-005/006/007 in den Baseline-Stand überführt, oder bleibt die Divergenz bestehen? | Governance |
| C-2 | Wird das **FROZEN** Architecture Book v2.0 gleich behandelt wie die ADRs oder getrennt? | Governance + Architektur-Freeze |
| C-3 | Werden `CLAUDE.md` und `ROADMAP.md` mit den ADRs gebündelt oder getrennt? | Governance |
| C-4 | Wie wird in Phase D nachgewiesen, gegen **welchen** Stand QG-005 und QG-008 geprüft wurden? | Nachweisverfahren |

**Durch GDR-OD01-001 beantwortet:** C-2 und C-3 (Trennung der Dokumentklassen).
**Nicht abschließend beantwortet:** C-1 (die inhaltliche Disposition je Gruppe)
und C-4 (Weltangabe im Nachweisverfahren) — siehe Kap. 16.

---

## 7. Geprüfte Optionen

Wörtlich aus [R0 §20 OD-01] übernommen — nicht erweitert, nicht umformuliert:

| Option | Wortlaut | Wesentliche Konsequenz |
|---|---|---|
| **(a)** | **Committen mit Governance-Vermerk** | Vertragstext eindeutig ab Commit-Zeitpunkt; **berührt den Architecture Freeze** — R0 nennt dies ausdrücklich als Architektur-Wirkung von (a) |
| **(b)** | **Belassen und die Divergenz in den Gate-Nachweisen dokumentieren** | Freeze nicht berührt; Vertragstext bleibt zweiwertig; **Nachweisaufwand in Phase D steigt** [DEM §D-1] |
| **(c)** | **Getrennte Behandlung** — ADRs vs. FROZEN Architecture Book vs. `CLAUDE.md`/`ROADMAP.md` | Freeze-Berührung **steuerbar** (das AB kann ausgenommen werden); Wirkung gemischt; **drei Teilentscheidungen** erforderlich |

> R0 spricht ausdrücklich **keine Präferenz** zwischen (a), (b) und (c) aus:
> „Ohne Präferenz zwischen (a)/(b)/(c) — das ist Governance" [R0 §20 OD-01].
> DEM §D-1 und Decision Brief §K bestätigen dies wörtlich.

Gemeinsam für **alle drei** Optionen belegt: Code-Wirkung **keine**,
Test-Wirkung **keine**, Produkt-Wirkung **keine**, RB-1.0 (258/14) **unberührt**
[R0 §20 OD-01; DEM §D-1; Briefs §E, §J].

---

## 8. Getroffene Entscheidung

> ## **OPTION C — GETRENNTE BEHANDLUNG**

Der Projekteigner entscheidet:

1. **ADR-005, ADR-006 und ADR-007** werden als eigene ADR-Gruppe **separat**
   behandelt.
2. **Architecture Book v2.0** wird **separat** behandelt. Es darf **nicht**
   automatisch zusammen mit den ADRs committet, verändert oder in einen neuen
   Status überführt werden.
3. **`CLAUDE.md` und `ROADMAP.md`** werden **separat** als Projekt-/Meta-Dokumente
   behandelt.
4. Es erfolgt **KEIN Sammel-Commit** dieser sechs Dokumentänderungen.
5. Der bestehende **Architecture Freeze** des Architecture Book wird durch diese
   Entscheidung **NICHT** aufgehoben und **NICHT** verändert.
6. Die Entscheidung selbst verändert **keine fachlichen Inhalte**.
7. **TD-04 bleibt OPEN.** Die technische Behandlung von TD-04 ist Gegenstand der
   späteren Security-/**OD-05**-Entscheidung und wird durch OD-01 **nicht**
   vorweggenommen.
8. **QG-003, QG-005 und QG-008** werden durch diese Entscheidung **NICHT** als
   bestanden markiert.
9. **Coding bleibt: NOT AUTHORIZED.**

**Begründung.** Die drei Dokumentgruppen tragen unterschiedliche
Governance-Eigenschaften (Kap. 5). Option (c) ist die einzige Option, die diesen
Klassenunterschied abbildet: Sie erlaubt, das FROZEN Architecture Book von einer
etwaigen Nachführung der ADRs auszunehmen, und trennt die Projekt-/Meta-Dokumente
von den Vertragstexten. Die Freeze-Berührung wird damit **steuerbar** statt
zwangsläufig [Briefs §E, Zeile „Architecture Freeze"].

---

## 9. Genaue Reichweite der Entscheidung

**In scope — durch GDR-OD01-001 entschieden:**

| # | Gegenstand |
|---|---|
| 1 | Die **Disposition ist getrennt zu führen** — drei Dokumentgruppen, drei eigenständige Governance-Vorgänge |
| 2 | Ein **Sammel-Commit ist ausgeschlossen** |
| 3 | Das **Architecture Book ist von einer gemeinsamen Behandlung ausgenommen** und wird eigenständig bewertet |
| 4 | `CLAUDE.md` / `ROADMAP.md` sind **nicht** an die ADR-Gruppe gebunden |
| 5 | Teilfrage **C-2** und **C-3** des Decision Briefs sind beantwortet |
| 6 | **BD-03** ist als Spiegelposition insoweit adressiert, als die Dispositionsform entschieden ist |

**Out of scope — durch GDR-OD01-001 ausdrücklich NICHT entschieden:**

| # | Gegenstand | Verbleibender Status |
|---|---|---|
| 1 | Welche konkrete Governance-Aktion je Gruppe erfolgt (Commit, Revision, Amendment, Belassen) | **OFFEN** — je Gruppe separat festzustellen (Kap. 15) |
| 2 | Ob die Working-Tree-Fassungen der ADRs verbindlich werden | **OFFEN** |
| 3 | Ob und wie das Architecture Book angepasst wird | **OFFEN** — nur über eigenen, autorisierten Governance-Schritt |
| 4 | Teilfrage **C-4** — Weltangabe im QG-005/QG-008-Nachweisverfahren | **OPEN INTERPRETATION** [Briefs M-1] |
| 5 | **OD-08** (Statuskopf Sprint Plan) — Bündelung war nur *empfohlen* | **OPEN** |
| 6 | Jede technische Frage (TD-04, TD-05, TD-06, TD-19, TD-21) | **OPEN** — Gegenstand von OD-05 |

**Physische Wirkung dieses Records: keine.** Es wurde keine Bestandsdatei
verändert, kein Commit, kein Tag, kein Push erzeugt. Die physische Behandlung der
einzelnen Dokumentgruppen ist ein **separater, später zu autorisierender
Arbeitsschritt**.

---

## 10. Explizite Nicht-Wirkungen

**OPTION C bedeutet NICHT:**

| # | Nicht-Wirkung |
|---|---|
| 1 | **NICHT**, dass ADR-005, ADR-006 oder ADR-007 automatisch APPROVED sind |
| 2 | **NICHT**, dass die Working-Tree-Fassungen automatisch autorisiert oder verbindlich sind |
| 3 | **NICHT**, dass das Architecture Book verändert werden darf |
| 4 | **NICHT**, dass der Architecture Freeze aufgehoben ist |
| 5 | **NICHT**, dass TD-04 gelöst, behoben oder geschlossen ist |
| 6 | **NICHT**, dass Security-Wiring freigegeben ist |
| 7 | **NICHT**, dass irgendein Sprint automatisch startet |
| 8 | **NICHT**, dass ein Quality Gate bestanden ist |
| 9 | **NICHT**, dass ein Security Finding, eine ODD oder ein Security Gate geschlossen ist |
| 10 | **NICHT**, dass RK-01 oder RK-02 aufgelöst sind |
| 11 | **NICHT**, dass Coding autorisiert ist |

> **Status und Verbindlichkeit jeder einzelnen Dokumentgruppe bleiben
> unverändert entsprechend ihrem bestehenden Governance-Status bestehen.**

**Ergänzender Ehrlichkeitsvorbehalt (aus der Quelle übernommen).** RK-02 speist
sich aus **zwei** Quellen: (i) der ADR-Fassungsdivergenz **und** (ii) dem Umstand,
dass 11 von 16 normativen Pflichtquellen untracked sind. **Keine** der drei
Optionen adressiert (ii) — „Wer OD-01 entscheidet, entscheidet RK-02 nicht mit"
[Briefs §E].

---

## 11. Architecture Book Protection

| Feld | Wert |
|---|---|
| Dokument | `docs/architecture-book-v2.md` |
| Status | **APPROVED / FROZEN (v2.0) — 2026-07-26** |
| Änderungsregel (Originalwortlaut Kopf) | „Keine inhaltlichen Änderungen an v2.0. Anpassungen erfolgen ausschließlich über neue Dokumentversionen (z. B. v2.1 oder v3.0) und dokumentierte ADRs." |
| Git-Tags | `architecture-book-v2.0`, `core-runtime-v1.0.0` |
| Wirkung von GDR-OD01-001 auf den Freeze | **KEINE** |

Deshalb gilt aus dieser Entscheidung heraus:

- **Keine Änderung** am Architecture Book.
- **Kein Statuswechsel** des Architecture Book.
- **Keine automatische Übernahme** der Working-Tree-Fassung.
- **Kein implizites Amendment.**
- **Keine Aufhebung** des Freeze.

Der zugehörige Deviation-Kandidat **DEV-AB** („FROZEN AB im Working Tree
modifiziert") bleibt gemäß [DEM §1.8] an BD-03 gebunden und wird — der R0-Wertung
folgend — weiterhin **nicht** als eingetretene Deviation, sondern als offener
Dispositionsgegenstand geführt.

> Falls die spätere getrennte Behandlung eine Änderung am Architecture Book
> erfordern sollte, muss dafür ein **eigener Governance-Schritt identifiziert und
> ausdrücklich autorisiert** werden. **Nicht Gegenstand dieses Records.**

---

## 12. TD-04 / OD-05 — Abgrenzung

| Position | Gegenstand | Wirkung von OD-01 |
|---|---|---|
| **OD-01** | **Dokument-/Vertragsdisposition** — gegen welchen Text gemessen wird | entschieden (Form der Disposition, Kap. 8) |
| **OD-05** | **Technische Security-Verdrahtung** im Bootstrap | **NICHT entschieden — bleibt OPEN** |
| **TD-04** | Runtime-Permission-Enforcement nutzt Plugin-Selbstdeklaration statt Host-Grants | **BLEIBT OPEN** |

**Diese beiden Fragen dürfen nicht vermischt werden.**

- TD-04 hängt gemäß [R0 §24.2] an **OD-01 + OD-05 gemeinsam**. OD-01 liefert den
  **Vertragstext** (ADR-006 D4), **nicht die Lösung**; die technische Behebung
  hängt an OD-05.
- „Eine Entscheidung über OD-01 macht TD-04 **nicht** behoben — sie macht nur
  eindeutig, gegen welchen Text TD-04 gemessen wird" [Briefs §H].
- Der Fehlschluss „TD-04 ist mit OD-05 erledigt" ist in [Briefs, OD-05 Brief]
  ausdrücklich als **Scheinschließung einer MISSING-Position** benannt.
- **Aus GDR-OD01-001 wird keine technische Lösung für TD-04 abgeleitet.**
- **Keine Option von OD-05** (a/b/c) wird durch diesen Record vorweggenommen,
  bewertet oder präferiert.

Ebenfalls unberührt und weiterhin OPEN: **TD-05, TD-06, TD-17, TD-19, TD-21**,
**SEC-01**, **SEC-05**, sämtliche Security Gates **SG-A…SG-K** und alle **ODDs**.

---

## 13. Sprint-/QG-Auswirkungen

**Sprint-Wirkung:**

| Gegenstand | Wirkung |
|---|---|
| Sprint Plan | **UNVERÄNDERT** — keine Planänderung; OD-01 löst laut [R0 §20 OD-01; Briefs §N] keine Planänderung aus |
| SPR-02 und Folgesprints | **NICHT freigegeben.** Kein automatischer Start |
| WP-001 … WP-005 | Vertragstext weiterhin **nicht abschließend** eindeutig — die inhaltliche Disposition je Gruppe steht aus (Kap. 9, out of scope Nr. 1) |
| RB-1.0 (258/14) | **UNBERÜHRT** — Test-Wirkung: keine [R0 §20 OD-01] |
| OD-08 | bleibt **OPEN**; die empfohlene Bündelung wird durch diesen Record **nicht** vollzogen |

**Quality-Gate-Wirkung:**

| Gate | Bezug | Status vor GDR-OD01-001 | Status nach GDR-OD01-001 |
|---|---|---|---|
| QG-003 Architecture Freeze Compliance | TD-08, TD-12, BS-03, OD-01 | NOT STARTED | **NOT STARTED** |
| QG-005 Traceability Completeness | OD-01 (Weltangabe) | NOT STARTED | **NOT STARTED** |
| QG-006 Pipeline Security Compliance | OD-05 / C2-Cluster | NOT STARTED | **NOT STARTED** (nicht an OD-01 gebunden) |
| QG-008 Governance Compliance | OD-01..OD-08 | NOT STARTED | **NOT STARTED** |

> **Kein Quality Gate wird durch diesen Record als PASSED markiert.**

**Risiken:**

| Risiko | Status |
|---|---|
| **RK-01** — Phase B trifft auf ungeklärte ADR-Vertragslage | **BESTEHT FORT** — nur teilweise entschärft; die inhaltliche Disposition je Gruppe steht aus |
| **RK-02** — QG-005/QG-008-Nachweise gegen den Baseline nicht führbar | **BESTEHT FORT** — Ursache (ii), untracked Pflichtquellen, ist durch keine OD-01-Option adressiert |

---

## 14. Coding Authorization Statement

> ## **CODING = NOT AUTHORIZED.**

Dieser Record erteilt **keine** Coding-Autorisierung, **keine**
Implementierungsfreigabe, **keine** Sprint-Freigabe und **keine**
Security-Implementierungsfreigabe. Die Coding-Sperre bleibt in dem durch
[Baseline Commit Record §12] und die vorgelagerten Governance-Entscheidungen
festgelegten Umfang unverändert bestehen.

---

## 15. Folgeaktionen (PLAN / NEXT AUTHORIZED WORK)

> **Keine dieser Aktionen wird durch diesen Record ausgeführt.** Sie sind
> ausschließlich als Plan dokumentiert und bedürfen jeweils einer eigenen,
> ausdrücklichen Autorisierung durch den Projekteigner.

| # | Folgeaktion | Gegenstand | Autorität | Status |
|---|---|---|---|---|
| **A** | ADR-005/006/007 **separat bewerten** | Verhältnis Welt A (`Open`) zu Welt B (`APPROVED`); Verhältnis zu den bestehenden Approval Records | Projekteigner / Governance Architect | **NEXT AUTHORIZED WORK — nicht gestartet** |
| **B** | Architecture Book v2.0 **separat bewerten** | Behandlung unter Wahrung des FROZEN-Status; ob überhaupt ein Governance-Schritt erforderlich ist | Projekteigner / Governance Architect | **NEXT AUTHORIZED WORK — nicht gestartet** |
| **C** | `CLAUDE.md` / `ROADMAP.md` **separat bewerten** | Projekt-/Meta-Dokumente; geringere Tragweite [Briefs M-1] | Projekteigner | **NEXT AUTHORIZED WORK — nicht gestartet** |
| **D** | Je Gruppe **separat feststellen**, ob ein Commit, eine Revision, ein Amendment oder eine andere Governance-Aktion erforderlich ist — oder keine | alle drei Gruppen | Projekteigner / Governance Architect | **NEXT AUTHORIZED WORK — nicht gestartet** |

**Ausdrücklich nicht Bestandteil dieser Folgeaktionen:** OD-05, TD-04 und jede
technische Security-Entscheidung. Diese werden **separat** geführt.

---

## 16. Offene Punkte

| # | Offener Punkt | Herkunft | Status |
|---|---|---|---|
| **OP-1** | Inhaltliche Disposition je Dokumentgruppe (Teilfrage C-1) | Kap. 9, out of scope Nr. 1 | **OPEN** — Folgeaktionen A–D |
| **OP-2** | Nachweisverfahren für QG-005/QG-008: wie die **Weltangabe** geführt wird (Teilfrage C-4) | R0 definiert es **nicht** als Teil von OD-01, benennt den Bedarf aber über RK-02 [Briefs M-1, OI-4] | **OPEN INTERPRETATION** |
| **OP-3** | Inhalt der Approval Records für ADR-005/006/007 — in R0 nicht geprüft | [Briefs §A „Nicht belegt / UNKNOWN"; U-2] | **UNKNOWN** |
| **OP-4** | Governance-technische Wertung eines etwaigen Commits der Welt-B-Fassung (AB-Änderung / Nachführung / beides) | [Briefs §A „Nicht belegt / UNKNOWN"] | **UNKNOWN** |
| **OP-5** | Detailinhalt der Modifikationen an `CLAUDE.md` / `ROADMAP.md` | [Briefs §A; U-3] | **UNKNOWN** |
| **OP-6** | 11 von 16 Pflichtquellen sind untracked — Grundursache (ii) von RK-02 | [R0 §2.3 SG-01, §4.4] | **OPEN** — durch keine OD-01-Option adressiert |
| **OP-7** | **OD-05** — technische Security-Verdrahtung | [R0 §20 OD-05] | **OPEN** |
| **OP-8** | **TD-04** — Permission-Enforcement | [R0 §10.5 SEC-05, §24.2] | **OPEN** |
| **OP-9** | **OD-08** — Statuskopf Sprint Plan | [R0 §20 OD-08] | **OPEN** |
| **OP-10** | **BD-03** — vollständige Aufhebung der Blockade | [R0 §33.2] | **teilweise adressiert** (Dispositionsform entschieden); vollständige Auflösung erst nach Folgeaktionen A–D |

---

## 17. Verification

☑ OD-01-Entscheidung dokumentiert
☑ **Option C** dokumentiert — Wortlaut mit [R0 §20 OD-01] abgeglichen, deckungsgleich
☑ Source Gate bestanden — alle Pflichtquellen vorhanden und gelesen
☑ **keine** fachliche Security-Entscheidung getroffen
☑ **TD-04 nicht geschlossen** — bleibt OPEN
☑ **OD-05 nicht entschieden** — bleibt OPEN; keine Option vorweggenommen
☑ `docs/architecture-book-v2.md` **nicht verändert**
☑ `docs/adr/005-…md`, `docs/adr/006-…md`, `docs/adr/007-…md` **nicht verändert**
☑ `CLAUDE.md` **nicht verändert**
☑ `ROADMAP.md` **nicht verändert**
☑ Sprint Plan **nicht verändert**
☑ **kein** Quality Gate als PASSED markiert (QG-003/QG-005/QG-006/QG-008 bleiben NOT STARTED)
☑ **kein** Technical Debt geschlossen
☑ **keine** ODD geschlossen
☑ **kein** Security Finding und **kein** Security Gate geschlossen
☑ Architecture Freeze **nicht aufgehoben, nicht verändert**
☑ **Coding weiterhin NOT AUTHORIZED**
☑ **genau eine** neue Datei erzeugt (`docs/governance/od-01-governance-decision.md`)
☑ **keine** Datei gelöscht, verschoben oder archiviert
☑ **kein Commit**
☑ **kein Tag**
☑ **kein Push**
☑ Folgeaktionen ausschließlich als PLAN / NEXT AUTHORIZED WORK dokumentiert

---

## 18. Final Decision Statement

> **GDR-OD01-001 — FINAL**
>
> **OD-01 / BD-03 ist entschieden: OPTION C — GETRENNTE BEHANDLUNG.**
>
> ADR-005/006/007, das FROZEN Architecture Book v2.0 sowie `CLAUDE.md` und
> `ROADMAP.md` werden als **drei getrennte Dokumentgruppen** disponiert. Ein
> Sammel-Commit der sechs Dokumentänderungen findet **nicht** statt.
>
> Diese Entscheidung ist **ausschließlich** eine Governance- und
> Dispositionsentscheidung. Sie verändert **keinen** fachlichen Inhalt, hebt den
> **Architecture Freeze nicht auf**, überführt **keine** Working-Tree-Fassung in
> einen verbindlichen Status, schließt **weder TD-04 noch eine ODD, noch ein
> Security Finding, noch ein Quality Gate**, und nimmt **OD-05 nicht vorweg**.
>
> **TD-04: OPEN. OD-05: OPEN. QG-003 / QG-005 / QG-008: NOT STARTED.**
>
> **CODING = NOT AUTHORIZED.**
>
> Die physische Behandlung der drei Dokumentgruppen ist ein separater, später
> ausdrücklich zu autorisierender Arbeitsschritt (Kap. 15, Folgeaktionen A–D).

---

**Ende OD-01 Governance Decision Record — JOCHEN X Milestone 1.0
(GDR-OD01-001, FINAL, 2026-08-10) — Bezugs-Baseline
`MILESTONE-1.0-BASELINE = 8fcf42f1997dfcf6ff232e75fd33c37b933991c8`**
