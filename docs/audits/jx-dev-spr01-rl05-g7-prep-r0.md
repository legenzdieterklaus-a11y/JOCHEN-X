# JOCHEN X — Milestone 1.0
# JX-DEV-SPR01-RL05-G7-PREP-01-R0 — Preparation Wave
## Herstellung der Voraussetzungen für IP §10.6 Bedingung 7 (Option A: A1 / A2)

> **COMPLETED — PREPARATION ONLY · HUMAN DECISION REQUIRED**
>
> **Kernbefund dieser Welle — drei Punkte:**
>
> **(1)** **A1 ist keine mechanische Statusnachführung.** OD-08 ist eine
> registrierte **Open Decision mit zweiwertigem Optionsraum** — (a) Kopf
> nachführen, (b) **belassen** — mit ausdrücklich vermerktem
> Entscheidungsbedarf („Entscheidung nötig? **JA** — Projekteigner /
> Governance", DEM §1.1). A1 benötigt daher **zuerst eine Human Decision**
> und **danach** einen eigenen EXEC. Zusätzlich ist der **Zielstatus** des
> Sprint Plans und das in OD-08 Option (a) genannte „vorgesehene
> kontrollierte Verfahren" **in keiner geprüften Quelle definiert**.
>
> **(2)** **A2 ist quellenseitig nicht abschließend beantwortbar.** Die
> Frage, ob der OD-05-Umriss Bestandteil einer genehmigten Sprintplanung
> sein muss, ist als **HD4-HD2-B-03 ausdrücklich als ungeregelt
> registriert**. Fünf Quellen behandeln die fehlende Abdeckung als
> **Grund** der Nichterfüllung; **keine** Quelle normiert ein
> Abdeckungskriterium. **Eine abschließende A2-Antwort wäre selbst eine
> Human Decision, keine Prüfung.**
>
> **(3)** **Die Sequenz A1/A2 ist nicht quellenbestimmbar.** Für **beide**
> Reihenfolgen existiert je eine Quellenstütze — für A2 → A1 die
> Inhaltsabhängigkeit des Statuskopfs (JX-G7-B-02), für A1 → A2 die
> **wörtliche Wiedervorlagebedingung von HD-2** („bis eine belastbare
> Planungsgrundlage … vorliegt"). **JX-G7-B-02 wird hier weder bestätigt
> noch verworfen.**
>
> **BEDINGUNG 7 = NICHT ERFÜLLT · A1 = NICHT AUSGEFÜHRT · A2 = NICHT
> AUSGEFÜHRT · HD-2 = NICHT ENTSCHIEDEN · RL-05 = NOT REACHED ·
> OP-2 = NICHT ERFÜLLT · CODING = NOT AUTHORIZED · QG-006 = NOT STARTED**

---

## 0. Document Identity

| Feld | Wert |
|---|---|
| **Document ID** | **JX-DEV-SPR01-RL05-G7-PREP-01-R0** |
| Mode / Wave | GOVERNANCE · **PREP** (READ-ONLY / PREPARATION ONLY) |
| Subject | Vorbereitung der nächsten zulässigen Sequenz zur Herstellung von IP §10.6 Bedingung 7 |
| Date | 2026-08-13 |
| Pfad | `docs/audits/jx-dev-spr01-rl05-g7-prep-r0.md` |
| **Bezugs-Baseline** | `MILESTONE-1.0-BASELINE = 8fcf42f1997dfcf6ff232e75fd33c37b933991c8` (GDR-003) |
| HEAD bei Beginn | `f97fa54` (JX-DEV-SPR01-RL05-G7-DEC-01-R0) |
| Branch | `milestone-1.0-governance` |
| **Autorisierung** | JX-DEV-SPR01-RL05-G7-DEC-01-R0 — Human Decision vom 2026-08-13, **OPTION A**: „autorisiert zunächst ausschließlich die **Vorbereitung** der notwendigen Folgeschritte" |
| **Bezug (DEC)** | `docs/audits/jx-dev-spr01-rl05-g7-decision-record-r0.md` — **nicht umgeschrieben** |
| **Bezug (PREP-02)** | `docs/audits/jx-dev-spr01-rl05-final-prep-02-r0.md` — **nicht umgeschrieben** |
| **Status** | **COMPLETED — PREPARATION · HUMAN DECISION REQUIRED** |

**Namenskonvention:** Der Pfad folgt dem im Strang etablierten Muster
(`jx-dev-spr01-rl05-final-prep-r0.md`, `…-final-prep-02-r0.md`,
`…-g7-decision-record-r0.md`) in `docs/audits/`. Keine abweichende
Konvention ist in den Quellen belegt.

---

## 1. Baseline Gate

| Prüfung | Ergebnis | Klasse |
|---|---|---|
| **HEAD** | `f97fa5470efb30c701001cca786bcc7c6cd41bde` = **`f97fa54`** — „docs: record condition 7 path decision (Option A)" — **erwarteter Stand** | FACT |
| **Vorkette bis `8fcf42f`** | `git merge-base --is-ancestor 8fcf42f HEAD` → **PASS**; 27 Commits zwischen Baseline und HEAD; Kette `f97fa54 → 7d4a603 → 351e562 → 05f4932 → 95eda8e → d540920 → 94d4dd5 → 7ee93ce → f6c441c → e5180ba → d50bd02 → 2255a5e → … → 8fcf42f` — lückenlos | FACT |
| **Produktiver Baum** | `git diff --name-only 8fcf42f..HEAD` außerhalb `docs/` = **leer** → Code, Tests, Konfiguration **baseline-identisch** | FACT |
| **Working Tree — getrackte Modifikationen** | **genau 3, unverändert vorbestehend**: `CLAUDE.md`, `ROADMAP.md`, `docs/architecture-book-v2.md` | FACT |
| **Working Tree — untracked** | 83 vorbestehende untracked Dokumente (86 Positionen gesamt in `git status --porcelain`) | FACT |
| **Staging vor Beginn** | **leer** | FACT |
| **Unerwartete Code-/Teständerungen** | **keine** | FACT |
| **Bereinigung** | **keine durchgeführt** — Working Tree unangetastet | FACT |

> **Baseline Gate: PASS.**

---

## 2. Source Gate

Ausschließlich projektinterne, autorisierte Quellen (read-only). **Keine
externe Quelle. Keine Governance-Regel aus allgemeinem Wissen ergänzt.**

### 2.1 Pflichtquellen (Auftrag)

| # | Quelle | Verwendete Fundstellen |
|---|---|---|
| 1 | **G7-DEC** `jx-dev-spr01-rl05-g7-decision-record-r0.md` | Kap. 3, **Kap. 4 (HUMAN-DECISION-Block wörtlich)**, Kap. 5, **Kap. 6 (JX-G7-B-01…B-05)**, Kap. 7, Kap. 10 |
| 2 | **PREP-02** `jx-dev-spr01-rl05-final-prep-02-r0.md` | Kap. 4.3, **Kap. 5 (5.1/5.2/5.3)**, Kap. 9 (9.1/9.2/9.3), Kap. 11, Kap. 12/13, **Kap. 14.2**, Kap. 16.1–16.4, Kap. 17, **Kap. 19** |
| 3 | **PREP-01** `jx-dev-spr01-rl05-final-prep-r0.md` | Kopf, Kap. 7 (OP-2-Prüfung), Kap. 12 (U-2 historisch) |
| 4 | **GDR-OD01-001** `od-01-governance-decision.md` | Kap. 9, Kap. 10, **Kap. 11 (Architecture Book Protection / DEV-AB)**, Kap. 12, **Kap. 13 (OD-08 bleibt OPEN)**, Kap. 14, **Kap. 15 (Folgeaktionen A/B/C/D)**, **Kap. 16 (OP-1…OP-10, insb. OP-3, OP-4, OP-9, OP-10)** |
| 5 | **IP §10.5** `milestone-1.0-implementation-plan.md` Z. 3424–3498 | Vorspann; **RL-04 (Austritt!)**; **RL-05 (Eintritt/Kriterien/Nachweise)**; „Aktueller Stand" |
| 6 | **IP §10.6** Z. 3499–3545 | Sprint Planning 1–6; **Coding 7–9**; Ausschlüsse 1–8 |
| 7 | **IP §10.9** Z. 3688–3702 | **ACN-08**, **ACN-09** (Wortlaut) |
| 8 | **IP §7.6** Z. 2480–2520 | Eskalationstatbestände, Entscheidungsinstanzen, **Regeln 1–5** |
| 9 | **ADW-SPR-1.0-001** `milestone-1.0-sprint-planning-approval-decision-op1.md` | **Kap. 16 (Decision)**, **Kap. 17 (Decision Scope)**, **Kap. 18 (Non-Effects)**, Kap. 19, Kap. 20 |
| 10 | **OD-08** — `jochen-x-master-engineering-plan-r0.md` **§20 OD-08** (Problem/Evidenz/**Optionen (a)(b)**/Empfehlung/**Autorität**); `jochen-x-decision-execution-matrix-r0.md` **§1.1 Z. 109** (P3, **„Entscheidung nötig? JA"**, Status OPEN), §366 | |
| 11 | **OD-05** `od-05-governance-decision.md`; DEM §1.1 (OD-05, P1, OPEN); GDR-OD01-001 Kap. 12 (OD-01/OD-05 **nicht vermischen**) | |
| 12 | **HD-2 — Unterlagen** `hd-4-hd2-decision-preparation-r0.md` (Kap. 9 Befunde 1–5, **Kap. 10 (HD4-HD2-B-04)**, **Kap. 11 Fragen A–G (insb. D, E, F / HD4-HD2-B-03)**, Kap. 13 Optionen O-1…O-3, Kap. 14, Kap. 15) · `hd-4-hd2-human-decision-record-r0.md` (**Kap. 5 Decision-Block wörtlich**, Kap. 8, Kap. 15, HD4-HD2-HDR-B-01) · `hd-4-a3-hd2-follow-up-r0.md` (**HD4-A3-B-04**) | |
| 13 | **Sprint Plan** `milestone-1.0-sprint-plan.md` | **Kopf (Status DRAFT / Version 1.0 / Revision R0)**, Kap. 1, **Kap. 6 (Coding Authorization Gate)**, Kap. 7, **Kap. 8 (OP-1…OP-8)** |
| 14 | **Sprint Planning Summary** `milestone-1.0-sprint-planning-summary-r0.md` | Kap. 6 (Bedingungen 7–9 PENDING), Kap. 8 |
| 15 | **Master Engineering Plan** | §20 OD-07/OD-08, §20.1, **Z. 2266 (Bedingung 7 PENDING)** |
| 16 | **HD-1** `hd-1-adr-rdr-decision.md` | Kap. 18 (Implementation Boundary), Kap. 19 (Autorität HD-2), Kap. 20 Schritte 1–5 |
| 17 | **ADR-012** `docs/adr/012-plugin-security-policy-configuration.md` | **KZ-1 (Z. 574)**, OI-1 (Z. 726), **Z. 776 (Bedingung 7 nicht erfüllt)** — nur als Sprint-/Governance-Abhängigkeit gelesen, **nicht** inhaltlich bewertet |
| 18 | **Decision Execution Matrix** | §1.1 (OD-01…OD-08), Z. 182 (BD-03 BLOCKED), Z. 199 (DEV-AB), Z. 366 |
| 19 | **F-05** `f-05-od05-change-control-determination.md` | **Kap. 21 Implementation Boundary (Bedingungen 7/8/9, GC-06)** |
| 20 | **HD-4 Approval Readiness** `hd-4-approval-readiness-r0.md` | **A3-5 (SOURCE FACT)**, **A3-6 (INFERENCE)**, A3-7 |
| 21 | **Development Standard v1.1** | §7 Lifecycle; **§17 Anh. B Approval States** |
| 22 | **Milestone 1.0 Charter** | **§8 Governance-Prozess Nr. 1–6** |

### 2.2 Durchgeführte repositoryweite Suchen

| Suchbegriff | Treffer (Dateien / Vorkommen) |
|---|---|
| `OD-05` | 31 / 459 |
| `OD-08` | 6 / 52 |
| `HD-2` | 30 / 447 |
| `Bedingung 7` | 9 / 102 |
| `§10.6` | 40 / 199 |
| `RL-05` | 48 / 438 |
| `OP-2` | 14 / 60 |
| `genehmigte Sprintplanung` | 13 / 25 |
| `Sprint Plan` | 55 / 299 |
| `DRAFT / 1.0 / R0` bzw. `DRAFT 1.0 R0` | 28 Vorkommen |
| `ACN-09` | 13 / 39 |
| `Keine Absenkung bestehender Bedingungen` | 4 / 5 |
| `approved sprint` | 0 (englische Formulierung existiert im Repository nicht) |

> **Source Gate: PASS.** Keine externe Quelle verwendet.

---

## 3. Source Reconstruction — Bedingung 7

### 3.1 Was Bedingung 7 verlangt

| Position | Wortlaut / Inhalt | Klasse |
|---|---|---|
| **IP §10.6 „Coding" Nr. 7** | „**Eine genehmigte Sprintplanung liegt vor.**" | **FACT (wörtlich)** |
| **IP §10.5 RL-04 — Austritt** | „**Genehmigte Sprintplanung liegt vor**" | **FACT (wörtlich)** |
| **IP §10.5 RL-05 — Eintritt** | „**Genehmigte Sprintplanung**; protokollierte Baseline-Bestätigung gemäß Kapitel 3.8" | **FACT (wörtlich)** |
| **IP §10.5 Vorspann** | „Die Readiness Levels … werden **ausschließlich vollständig** erreicht. Ein Teilerreichen ist nicht vorgesehen." | **FACT** |
| **Präzisierung des Begriffs** | **Keine Quelle definiert, was „genehmigt" für die Sprintplanung im Einzelnen erfordert** — weder ein Dokumentstatus noch ein Abdeckungskriterium noch ein Genehmigungsverfahren wird normiert | **UNKNOWN (Definitionslücke, quellenseitig festgestellt)** |

> **Feststellung:** Bedingung 7 steht auf **drei** Quellenpositionen
> (Coding Nr. 7, RL-04-Austritt, RL-05-Eintritt) und ist damit die
> Scharnierbedingung zwischen RL-04 und RL-05. **FACT.**

### 3.2 G7-a — Sprint-Plan-Status

| Position | Inhalt | Klasse |
|---|---|---|
| **Tatbestand** | Der Sprint Plan trägt physisch **Status DRAFT · Version 1.0 · Revision R0** (Kopf, Z. 5–8) — am HEAD `f97fa54` unverändert | **FACT** |
| **Ursache** | ADW-SPR-1.0-001 Kap. 17: „Genehmigt ist ausschließlich die Verwendung des Sprint Plans 1.0 R0 als **Planungsgrundlage**. Der **physische Status** … bleibt **DRAFT / 1.0 / R0**; eine eventuelle **Statusnachführung erfolgt in einem separat autorisierten Schritt**." | **FACT (wörtlich)** |
| **Ausdrückliche Nicht-Wirkung** | ADW-SPR-1.0-001 Kap. 18: nicht bewirkt sind u. a. „**Coding-Freigabe (OP-2 offen)**" und „**Statusänderung des Sprint Plans**" | **FACT (wörtlich)** |
| **Registrierte Position** | **OD-08 — „Statusnachführung des Sprint Plans"** | **FACT** |
| **Eigenbewertung des Plans** | Sprint Plan Kap. 6: Bedingung 7 = „**PENDING** — dieser Plan ist DRAFT; Genehmigung durch Projekteigner ausstehend" | **FACT (wörtlich)** |
| **Status** | **OPEN — unverändert seit PREP-02; durch die G7-DEC ausdrücklich nicht verändert** (G7-DEC Kap. 5) | **FACT** |

### 3.3 G7-b — OD-05-Umriss-Abdeckung

| Position | Inhalt | Klasse |
|---|---|---|
| **Tatbestand** | Der finalisierte **OD-05-Umriss** (CS-1 `app/bootstrap/stages_plugin.py` + CS-2 `config/settings.py` + CS-3 `config/default.toml`, niedergelegt in ADR-012) ist im Sprint Plan **nicht abgedeckt** | **FACT** |
| **Dokumentseitiger Nachweis** | HD-2-PREP Kap. 9 Befund 2 (**HD4-HD2-B-01**): Volltextsuche im Sprint Plan nach `OD-05`, „Umriss", `PluginSecurityStage`, `[security]` → **0 Treffer**; Befund 3: auch das OP-Register (OP-1…OP-8, OTD-1/2) führt den Umriss nicht | **FACT** |
| **Registrierte Position** | **HD-2** (= OI-1) — „Sprint-/WP-Zuordnung des finalisierten OD-05-Umrisses"; Autorität **Projekteigner** (HD-1 Kap. 19) | **FACT** |
| **Zeitliche Lage** | OP-1-Genehmigung 2026-08-09 **vor** der Umriss-Finalisierung; ADR-012 Accepted 2026-08-11; HD-1 stellt die Nichtabdeckung 2026-08-10 **danach** fest (**HD4-HD2-B-02**) | **FACT** |
| **Status** | **HD-2 = DEFERRED (Projekteigner, 2026-08-11) — bleibt OPEN / NOT DECIDED** | **FACT** |

### 3.4 Rollen der beteiligten Positionen

| Position | Rolle für Bedingung 7 | Klasse |
|---|---|---|
| **OD-08** | Registrierte Open Decision zu **G7-a**. **Optionsraum ausdrücklich zweiwertig:** „(a) Kopf im vorgesehenen kontrollierten Verfahren nachführen; (b) **belassen**, da die Genehmigungskette dokumentiert ist" [MEP §20 OD-08]. Autorität: **Projekteigner / Governance**. DEM §1.1: Prio **P3**, „Entscheidung nötig? **JA**", Status **OPEN** | **FACT (wörtlich)** |
| **OD-05** | Sachgegenstand des Umrisses (technische Security-Verdrahtung). **Nicht Gegenstand dieser PREP.** GDR-OD01-001 Kap. 12: OD-01 und OD-05 „**dürfen nicht vermischt werden**"; OD-05 „bleibt OPEN"; GDR-OD01-001 Kap. 15: OD-05 und TD-04 sind **ausdrücklich nicht Bestandteil** der Folgeaktionen A–D | **FACT** |
| **HD-2** | Registrierter **Abhilfeweg** für G7-b (PREP-02 Kap. 9.2). DEFERRED mit Wiedervorlagebedingung. **Condition: „Keine Änderung des Sprint Plans durch diese Entscheidung."** | **FACT** |
| **Sprint Plan** | Prüfgegenstand beider Gründe: Träger des Statuskopfs (G7-a) **und** des fehlenden Inhalts (G7-b) | **FACT** |
| **Physischer Status DRAFT/1.0/R0** | Von ADW-SPR-1.0-001 Kap. 17 **bewusst** unangetastet gelassen; Nachführung ausdrücklich einem separat autorisierten Schritt vorbehalten | **FACT** |

### 3.5 Welche Schritte verlangen die Quellen für die Feststellung „Bedingung 7 erfüllt"?

| # | Schritt | Quellenlage | Klasse |
|---|---|---|---|
| S-1 | G7-a beseitigen — Entscheidung über OD-08 **und**, bei Option (a), Vollzug der Statusnachführung | ADW-SPR-1.0-001 Kap. 17 („separat autorisierter Schritt"); MEP §20 OD-08; DEM §1.1 („Entscheidung nötig? JA") | **FACT** |
| S-2 | G7-b beseitigen — Klärung, **ob** die Umriss-Abdeckung erforderlich ist (A2); falls ja: **HD-2-Entscheidung** | PREP-02 Kap. 9.2 (registrierter Abhilfeweg); HD-1 Kap. 19/20 Schritt 2 | **FACT** (Abhilfeweg) / **UNKNOWN** (Erforderlichkeit — Kap. 4) |
| S-3 | Ausdrückliche Feststellung, dass Bedingung 7 erfüllt ist | **Keine Quelle** normiert Form, Instanz oder Verfahren dieser Feststellung. IP §10.4 („Die Freigabe entsteht ausschließlich durch W-6 i. V. m. W-7 und W-8") und ACN-08 („Statusaussagen … sind Feststellungen, keine Entscheidungen") schließen jedoch eine automatische Erfüllung aus | **UNKNOWN** (Form) / **FACT** (keine Automatik) |
| S-4 | Erst danach: separate RL-05-FINAL-PREP/DEC | G7-DEC Condition 12; PREP-02 Kap. 19 A3 | **FACT** |
| — | **Zielstatus des Sprint Plans** | **In keiner Quelle definiert.** Development Standard §17 Anh. B kennt Statusmodelle für **ADR** („Open → Accepted"), **Specification** („Draft → In Review → Corrections → Approved"), **Sprint** („Planned → In Progress → Review → Done") und **Release** — **kein Statusmodell für ein Sprint-Plan-Dokument**. Charter §8 führt „Sprint Planning" als Prozessschritt 6 ohne Statusmodell | **UNKNOWN** |
| — | Das in OD-08 Option (a) genannte „**vorgesehene kontrollierte Verfahren**" | **In keiner geprüften Quelle ausgestaltet** | **UNKNOWN** |

---

## 4. A2 — PREPARATION

**Untersuchte Frage (U-4′-Achse, Wortlaut der G7-DEC):** „Ist und in
welchem Umfang der OD-05-Umriss Bestandteil einer genehmigten
Sprintplanung, und welche Konsequenz hat dies für die Herstellung von
Bedingung 7?"

> **Abgrenzung:** Diese Welle **bereitet A2 vor** — sie identifiziert die
> maßgeblichen Quellen, stellt Gegenläufigkeiten dar und bestimmt, ob eine
> eindeutige Quellenlage existiert. Sie **trifft keine A2-Feststellung**
> und **entscheidet HD-2 nicht**.

### 4.1 Quellen, die die Abdeckung als erheblich behandeln

| # | Quelle | Aussage | Klasse |
|---|---|---|---|
| 1 | **ADR-012** Z. 776 | „7 — genehmigte Sprintplanung liegt vor — **nicht erfüllt** — Sprint Plan `DRAFT 1.0 R0`; **der Umriss ist darin nicht abgedeckt**" | **FACT** |
| 2 | **ADR-012 KZ-1** (Z. 574) | „**HD-2** (Sprint-/WP-Zuordnung) bleibt zu entscheiden — der Umriss ist im genehmigten Sprint Plan **nicht abgedeckt**" | **FACT** |
| 3 | **F-05 Kap. 21** | Bedingung 7: „Sprint Plan trägt **DRAFT 1.0 R0**; **zusätzlich** ist der Umriss darin **nicht abgedeckt**" | **FACT** |
| 4 | **HD-1 Kap. 18 / Kap. 20 Schritt 2** | „Der Umriss ist im genehmigten Sprint Plan **nicht abgedeckt**"; Schritt 2 = HD-2 | **FACT** |
| 5 | **HD-4 Approval Readiness A3-5** | „IP §10.6 **Bedingung 7** … ist eine Coding-Vorbedingung; **der Umriss ist im genehmigten Sprint Plan nicht abgedeckt**" — geführt als **SOURCE FACT** | **FACT** |

> **Was diese fünf Quellen belegen:** Sie führen die fehlende Abdeckung
> **faktisch als einen der beiden Gründe** der Nichterfüllung von
> Bedingung 7. **FACT.**
>
> **Was sie NICHT belegen:** Keine dieser Quellen **normiert** ein
> Abdeckungskriterium; keine leitet aus IP §10.6 Nr. 7 ab, dass eine
> Sprintplanung erst dann „genehmigt" ist, wenn der Umriss darin steht.
> Der Schritt von „wird als Grund geführt" zu „ist normativ erforderlich"
> ist **INFERENCE, nicht FACT.**

### 4.2 Gegenläufige bzw. relativierende Quellen

| # | Quelle | Aussage | Wirkung | Klasse |
|---|---|---|---|---|
| G-1 | **HD-2-PREP Kap. 11 Frage F (HD4-HD2-B-03)** | „Ist HD-2 Voraussetzung für RL-05? — **NICHT BELEGT / UNDETERMINED**. … **ob die HD-2-Zuordnung Bestandteil der Erfüllung von Nr. 7 ist, regelt keine geprüfte Quelle**" | Die A2-Frage ist **ausdrücklich als ungeregelt registriert** | **FACT** |
| G-2 | **HD-2-PREP Kap. 10 (HD4-HD2-B-04)** | Das **Verfahren** einer Fortschreibung der genehmigten Planungsgrundlage ist „in keiner geprüften Quelle geregelt → **UNDETERMINED / HUMAN REVIEW REQUIRED**" | Selbst bei bejahter Erforderlichkeit fehlt das Verfahren | **FACT** |
| G-3 | **HD-2-PREP Kap. 9 Befund 4 / OD-05 Kap. 16** | „Eigene Sprint-/WP-Zuordnung für OD-05: **keine**"; „Eigenes neues Work Package: **keines**" — ausdrücklich als „historischer Stand, **kein Verbot und keine Zuordnung**" gewertet | Kein Beleg für eine Pflichtabdeckung | **FACT** |
| G-4 | **ADW-SPR-1.0-001 Kap. 5/15/16** | Konformitätsbefund „7/7 WPs, **keine neuen WPs**"; der Plan wurde **gegen den Implementation Plan** als vollständig befunden und genehmigt | Zum Genehmigungszeitpunkt war der Plan gegen seinen eigenen Bezugstext scope-vollständig | **FACT** |
| G-5 | **HD4-HD2-B-02** | ADW-SPR-1.0-001 (2026-08-09) datiert **vor** der Umriss-Finalisierung und erwähnt den Umriss nicht | Der Umriss ist ein **nachträglicher** Gegenstand; seine planerische Behandlung ist unnormiert | **FACT** |
| G-6 | **IP §10.6 Ausschluss 7** | „Der Plan deckt seinen Planungsscope nicht vollständig ab" — bezieht sich auf den **Implementation Plan**; IP §10.8: „**AB-03 ist nicht mehr einschlägig**" | Ein Abdeckungs-Ausschlusstatbestand existiert, ist aber **nicht** auf den Sprint Plan bezogen und **nicht aktiv** (PREP-02 Kap. 8) | **FACT** (Nichtaktivität) / **INFERENCE** (Bezugsobjekt, vgl. PREP-02 I-01) |
| G-7 | **HD-2-PREP Kap. 11 Frage E** | „Ist HD-2 Voraussetzung für **Coding**? — **POSITIV BELEGT (mittelbar)**" mit Caveat „HD-2 allein erzeugt keine Coding-Readiness" | Verbindung besteht auf der **Coding**-Achse (Ebene D), nicht als normierte Bedingung-7-Anforderung | **FACT** |
| G-8 | **HD-4 A3-6** | „Die Erledigung von HD-2 ist materiell mit der Erfüllung von IP §10.6 Bedingung 7 verbunden" — ausdrücklich als **INFERENCE** geführt, nicht als SOURCE FACT | Die maßgebliche Verknüpfung ist bereits quellenseitig als Inferenz klassifiziert | **FACT** (über die Klassifikation) |

### 4.3 Existiert eine eindeutige Quellenlage?

| Frage | Antwort | Klasse |
|---|---|---|
| Ist der OD-05-Umriss **tatsächlich** in der genehmigten Sprintplanung enthalten? | **NEIN** — dokumentseitig verifiziert, 0 Treffer | **FACT** |
| Ist die Abdeckung **normativ erforderlich**, damit eine Sprintplanung als „genehmigt" i. S. v. IP §10.6 Nr. 7 gilt? | **NICHT GEREGELT** — HD4-HD2-B-03 registriert genau diese Frage als offen; fünf Quellen behandeln die Nichtabdeckung als Grund, keine normiert ein Kriterium; G-4/G-5 zeigen, dass der Plan zum Genehmigungszeitpunkt gegen seinen Bezugstext vollständig war | **UNKNOWN** |
| **In welchem Umfang** wäre die Abdeckung erforderlich (Zuordnung zu bestehendem WP / Planfortschreibung / eigenes Element)? | **NICHT BESTIMMBAR** — HD-2-PREP Kap. 13: „**SUBSTANTIVE OPTION PREFERENCE = NOT DETERMINABLE FROM CURRENT SOURCES**"; keine Quelle weist ein WP als Kandidaten aus (RELATED — NOT DERIVED, HD4-HD2-B-05) | **UNKNOWN** |
| Existiert ein **Verfahren** zur Fortschreibung der genehmigten Planungsgrundlage? | **NEIN** — HD4-HD2-B-04: UNDETERMINED / HUMAN REVIEW REQUIRED | **FACT** (über das Fehlen) |

> ## **A2-Vorbereitungsergebnis: KEINE EINDEUTIGE QUELLENLAGE.**
>
> Die Frage ist nicht durch Quellenauswertung auflösbar. Sie wird **nicht
> künstlich aufgelöst.** **UNKNOWN.**

### 4.4 Muss HD-2 für diese konkrete Frage entschieden werden?

| Prüfung | Ergebnis | Klasse |
|---|---|---|
| Ist HD-2 **Gegenstand** der A2-Frage? | **NEIN.** HD-2 ist die Entscheidung über die **Zuordnung** („ob und wie" der Umriss in die Sprint-/WP-Struktur aufgenommen wird). A2 fragt vorgelagert, **ob eine Abdeckung überhaupt erforderlich** ist | **FACT** (Gegenstandsdefinition: HD4-A3-R0 Kap. 9; HD-2-PREP Kap. 7) |
| Ist HD-2 zur **Beantwortung** von A2 zwingend? | **NEIN** — A2 ist logisch vorgelagert; HD-2 ist der **Abhilfeweg** für den Fall, dass A2 die Erforderlichkeit bejaht | **INFERENCE (quellengestützt: PREP-02 Kap. 9.2; G7-DEC Kap. 4 A2-Wortlaut „ohne HD-2 zu entscheiden")** |
| Ist HD-2 zur **Herstellung** von G7-b zwingend? | **UNKNOWN** — genau die in PREP-02 Kap. 16.3 als **U-4′** geführte Frage („Muss G7-b zwingend durch eine HD-2-Entscheidung geheilt werden?") | **UNKNOWN** |
| Wäre HD-2 durch A2 präjudiziert? | **NEIN, sofern A2 auf die Erforderlichkeitsfrage beschränkt bleibt.** Bejaht A2 die Erforderlichkeit, bleibt die **Auswahl** zwischen O-1/O-2/O-3 vollständig bei HD-2 | **INFERENCE** |

### 4.5 Ist A2 eine Prüfung oder bereits eine Human Decision?

| Teil von A2 | Charakter | Klasse |
|---|---|---|
| **Quellenerhebung und Widerspruchsdarstellung** | **Prüfung** — in dieser PREP durchgeführt (Kap. 4.1–4.3) | **FACT** |
| **Feststellung, dass keine eindeutige Quellenlage besteht** | **Prüfung** — Ergebnis oben | **FACT** |
| **Abschließende Beantwortung** („der Umriss **muss** / **muss nicht** abgedeckt sein") | **HUMAN DECISION.** Weil die Quellen die Frage nicht beantworten (HD4-HD2-B-03), wäre jede abschließende Antwort eine **Auslegung** von IP §10.6 Nr. 7. Eine verneinende Antwort stünde zudem unter dem Vorbehalt von **ACN-09** („Voraussetzungen, Kriterien und Ausschlüsse dürfen **nicht zur Herstellung der Genehmigungsfähigkeit gelockert werden**") und berührte damit denselben Normkonflikt, den die G7-DEC über Option A gerade **nicht** beschreiten wollte (JX-G7-B-04) | **INFERENCE (stark) → HUMAN DECISION REQUIRED** |

> **A2 ist damit teils Prüfung (erledigt), teils Human Decision (offen).**
> Diese PREP nimmt die Entscheidung **nicht** vorweg.

---

## 5. A1 — PREPARATION

**Untersuchte Frage:** Welche konkrete Statusnachführung des Sprint Plans
wäre erforderlich, um G7-a zu erfüllen? — **Nicht ausgeführt.**

| # | Prüfpunkt | Befund | Klasse |
|---|---|---|---|
| A1-1 | **Betroffenes Dokument** | **genau eines:** `docs/milestone-1.0-sprint-plan.md` (Kopf, Z. 5–8). Mittelbar berührt: Kap. 6 (führt Bedingung 7/8 als PENDING) und Kap. 8 (OP-1/OP-2) — deren Nachführung ist **von keiner Quelle verlangt** und **nicht Gegenstand von A1** | **FACT** / **UNKNOWN** (Umfang über den Kopf hinaus) |
| A1-2 | **Aktueller Status** | `Status | **DRAFT**` · `Version | 1.0` · `Revision | R0` · `Datum | 2026-08-09` — am HEAD unverändert | **FACT** |
| A1-3 | **Quellenbelegter Zielstatus** | **KEINER.** Development Standard §17 Anh. B definiert **kein** Statusmodell für ein Sprint-Plan-Dokument (nur ADR / Specification / Sprint / Release). Charter §8 nennt keinen Dokumentstatus. ADW-SPR-1.0-001 Kap. 17 nennt nur den Vorgang („Statusnachführung"), **nicht** das Ziel. MEP §20 OD-08 nennt „das vorgesehene kontrollierte Verfahren", ohne es zu benennen | **UNKNOWN** |
| A1-4 | **Inhaltliche Voraussetzungen** | Bei Wahl von OD-08 Option (a) müsste feststehen, **welchen Inhalt** der Plan im Zeitpunkt der Nachführung trägt — insbesondere, ob der OD-05-Umriss darin abgedeckt sein muss. Genau das ist die A2-Frage (Kap. 4) | **INFERENCE (quellengestützt: Kap. 4.1 Quellen 1–5 verknüpfen Statuskopf und Abdeckung als **zwei** Gründe **derselben** Bedingung)** |
| A1-5 | **Beeinflusst A2 das Ergebnis von A1?** | **JA, potenziell** — bejaht A2 die Erforderlichkeit, verändert sich der Inhalt, den der nachgeführte Plan tragen muss. Verneint A2 sie, bleibt der Inhalt unverändert. **Der Umfang der Beeinflussung ist nicht quellenbestimmbar** | **INFERENCE** / **UNKNOWN** (Umfang) |
| A1-6 | **Benötigt A1 einen eigenen EXEC?** | **JA** — ADW-SPR-1.0-001 Kap. 17: „**separat autorisierter Schritt**"; G7-DEC Condition 8: „Keine Änderung des Sprint Plans ohne separaten EXEC-Auftrag"; PREP-02 Kap. 14.2: „eigener PREP/DEC/EXEC-Zyklus mit Änderung einer Bestandsdatei" | **FACT** |
| A1-7 | **Zusätzlich eine Human Decision erforderlich?** | **JA** — **OD-08 ist eine offene Entscheidung mit zweiwertigem Optionsraum**: „(a) Kopf im vorgesehenen kontrollierten Verfahren nachführen; **(b) belassen**, da die Genehmigungskette dokumentiert ist" [MEP §20 OD-08]. DEM §1.1 Z. 109: „**Entscheidung nötig? JA — Projekteigner / Governance**", Status **OPEN**. Solange (a) nicht gewählt ist, existiert **kein** auszuführender Vollzug | **FACT** |
| A1-8 | **Governance-Entscheidung oder mechanischer Vollzug?** | **Beides — in dieser Reihenfolge.** Die **Auswahl** zwischen (a) und (b) ist eine Governance-Entscheidung des Projekteigners (A1-7). **Nach** getroffener Wahl (a) ist die Kopfänderung ein mechanischer Vollzug — **soweit der Zielstatus feststeht**, was derzeit **nicht** der Fall ist (A1-3) | **FACT** (Entscheidungsteil) / **UNKNOWN** (Vollzugsteil, wegen A1-3) |
| A1-9 | **Verhältnis von OD-08 Option (b) zur getroffenen G7-DEC** | Option (b) („belassen, da die Genehmigungskette dokumentiert ist") würde **G7-a nicht beseitigen**. Die G7-DEC hat aber ausdrücklich die **materielle Herstellung** gewählt und die Auslegungsoption verworfen (JX-G7-B-04); ACN-09 bleibt voll wirksam. **Ob Option (b) damit ausgeschlossen ist, entscheidet diese PREP nicht** — der Optionsraum von OD-08 ist eine eigenständige registrierte Position | **INFERENCE (stark) — HUMAN DECISION REQUIRED** |
| A1-10 | **Empfehlungslage in den Quellen** | MEP §20 OD-08 und DEM §366: „**Redaktionell, nicht dringlich; sinnvoll gemeinsam mit OD-01**". Diese Empfehlung stammt aus einem Kontext **vor** der Verknüpfung von OD-08 mit Bedingung 7 und ist eine **Empfehlung, keine Entscheidung** | **FACT** (Wortlaut) / **OBSERVATION** (Kontextlage) |

> **Kein Dateizugriff über Lesen hinaus. Keine Datei geändert.**

### 5.1 Beobachtung (Feststellung, keine Entscheidung)

| ID | Beobachtung | Klasse |
|---|---|---|
| **JX-G7P-B-01** | **A1 ist zweistufig, nicht einstufig.** PREP-02 Kap. 19 und die G7-DEC beschreiben A1 als „Statusnachführung … eigener PREP → DEC → **EXEC**". Der Befund A1-7 präzisiert: die DEC-Stufe ist **nicht** bloß eine Ausführungsfreigabe, sondern die **Auswahl innerhalb des registrierten OD-08-Optionsraums (a)/(b)**. Das ist eine Feststellung zum Charakter von A1, keine Änderung an OD-08 | **OBSERVATION** |
| **JX-G7P-B-02** | **Der Zielstatus ist quellenseitig undefiniert.** Ohne eine Bestimmung, welchen Status ein Sprint-Plan-Dokument annehmen kann, ist auch bei gewählter Option (a) kein EXEC formulierbar, der sich vollständig auf Quellen stützt. Dies ist eine **zusätzliche**, in PREP-02 noch nicht ausgewiesene Lücke | **OBSERVATION / UNKNOWN** |

---

## 6. Sequenz A2 / A1

**Zu bewerten:** Ist A2 → A1 quellenbasiert erforderlich, A1 → A2 zulässig,
sind beide unabhängig, oder ist die Reihenfolge nicht quellenbestimmbar?

### 6.1 Quellenstützen für **A2 → A1**

| # | Beleg | Aussage | Klasse |
|---|---|---|---|
| S2a | **G7-DEC Kap. 6, JX-G7-B-02** | „Das Ergebnis von A2 bestimmt mit, welchen Inhalt der Sprint Plan tragen muss, bevor sein Status nachgeführt werden kann … die Sequenzfrage ist **in der nachfolgenden PREP zu behandeln**" — ausdrücklich als **OBSERVATION**, nicht als Anordnung geführt | **FACT** (dass die Beobachtung existiert) / **INFERENCE** (ihr Inhalt) |
| S2b | **Kap. 4.1 Quellen 1–5** | ADR-012, F-05, HD-1, HD-4 A3-5 nennen Statuskopf **und** Nichtabdeckung als zwei Gründe **derselben** Bedingung — beide müssten für eine materielle Herstellung beseitigt werden | **FACT** (Nennung) / **INFERENCE** (Sequenzfolge) |
| S2c | **MEP §20 OD-08 Option (a)** | „Kopf im vorgesehenen **kontrollierten Verfahren** nachführen" — ein Verfahren, das einen Inhalt zertifiziert, setzt den Inhalt als feststehend voraus | **INFERENCE** |

### 6.2 Quellenstützen für **A1 → A2**

| # | Beleg | Aussage | Klasse |
|---|---|---|---|
| S1a | **HD-2 Human Decision Record Kap. 5 (wörtlich)** | „HD-2 bleibt offen, **bis eine belastbare Planungsgrundlage und eine konkrete Zuordnung vorliegen**." — Die Wiedervorlagebedingung von HD-2 knüpft an eine **Planungsgrundlage** an, deren Herstellung/Bestätigung Gegenstand von A1 wäre | **FACT (wörtlich)** |
| S1b | **HD-2 Condition (wörtlich)** | „**Keine Änderung des Sprint Plans durch diese Entscheidung.**" — HD-2 kann den Plan selbst nicht ändern; eine Planänderung ist ein von HD-2 getrennter Akt | **FACT (wörtlich)** |
| S1c | **HD4-HD2-HDR-B-01** | Die Wiedervorlagebedingung „definiert **keinen** Termin und **kein** Verfahren; beides bleibt einer künftigen Human-Entscheidung vorbehalten" | **FACT** |
| S1d | **Gegenläufig zu S1a** | ADW-SPR-1.0-001 Kap. 16 hat den Plan bereits als „**verbindliche Planungsgrundlage**" genehmigt. Ob „belastbare Planungsgrundlage" i. S. v. HD-2 damit **bereits vorliegt** oder erst durch A1 entsteht, ist **nicht definiert** | **UNKNOWN** |

### 6.3 Quellenstützen für **Unabhängigkeit**

| # | Beleg | Aussage | Klasse |
|---|---|---|---|
| U-a | **HD-1 Kap. 20 / HD-4 A3-1** | HD-2 ist „**unabhängig, parallel führbar**" — **Bezugspunkt ist jedoch der HD-4-/ADR-Strang**, nicht OD-08. Eine Aussage zum Verhältnis HD-2 ↔ OD-08 enthält die Quelle **nicht** | **FACT** (Wortlaut) / **UNKNOWN** (Übertragbarkeit auf OD-08) |
| U-b | **MEP §20 OD-08 / DEM §366** | OD-08 wird mit **OD-01** gebündelt empfohlen — **nicht** mit OD-05/HD-2 | **FACT** |
| U-c | **GDR-OD01-001 Kap. 13** | „**OD-08** bleibt **OPEN**; die empfohlene Bündelung wird durch diesen Record **nicht** vollzogen" — OD-08 wird dort ohne HD-2-Bezug geführt | **FACT** |
| U-d | **Change-Surface-Trennung** | A2 hat **keine** Change Surface (reine Prüfung/Entscheidung); A1 berührt eine Bestandsdatei. Die Akte kollidieren technisch nicht | **INFERENCE** |

### 6.4 Bewertung

| Aussage | Ergebnis | Klasse |
|---|---|---|
| Ist **A2 → A1** quellenbasiert **erforderlich**? | **NEIN — nicht belegt.** Die einzige Quelle, die diese Richtung nahelegt (JX-G7-B-02), führt sich selbst ausdrücklich als **OBSERVATION** und verweist die Sequenzfrage in diese PREP | **FACT** (Klassifikation) → **UNKNOWN** (Erforderlichkeit) |
| Ist **A1 → A2** **zulässig**? | **NICHT BESTIMMBAR.** S1a stützt diese Richtung wörtlich, wird aber durch S1d entkräftet: ob eine „belastbare Planungsgrundlage" bereits vorliegt, ist undefiniert | **UNKNOWN** |
| Sind **A1 und A2 unabhängig**? | **NICHT BELEGT.** U-a ist auf einen anderen Bezugspunkt gemünzt; U-b/U-c belegen nur, dass **keine** Quelle eine Kopplung anordnet — das Fehlen einer Kopplungsregel ist kein Beleg für Unabhängigkeit | **UNKNOWN** |
| **Ist die Reihenfolge selbst quellenbestimmbar?** | ## **NEIN.** | **UNKNOWN — HUMAN DECISION REQUIRED** |

> **JX-G7-B-02 wird weder bestätigt noch verworfen.** Die Beobachtung ist
> eine von **zwei** quellengestützten Lesarten; die Gegenlesart (S1a) ist
> **wörtlich** belegt und in PREP-02 wie in der G7-DEC bisher nicht
> ausgewiesen worden.

### 6.5 Zirkularitätsbefund

| Position | Inhalt | Klasse |
|---|---|---|
| **JX-G7P-B-03** | Es besteht eine **wechselseitige Wartelage**: HD-2 wartet ausweislich seiner Wiedervorlagebedingung auf eine „belastbare Planungsgrundlage" (S1a); die Frage, welchen Inhalt eine nachgeführte Planungsgrundlage tragen muss, hängt ihrerseits von der A2-Frage ab (A1-4/S2b). **Keine Quelle löst diese Lage auf.** Sie ist damit selbst ein Entscheidungsgegenstand des Projekteigners | **OBSERVATION / UNKNOWN** |

---

## 7. Condition-7-Matrix

| Element | Aktueller Status | Erforderlicher Zustand | Quelle | Offene Frage | Nächster zulässiger Akt |
|---|---|---|---|---|---|
| **G7-a — Sprint-Plan-Status** | **OFFEN** — Plan trägt physisch `DRAFT / 1.0 / R0` | Statuskopf so beschaffen, dass „genehmigte Sprintplanung" trägt — **Zielzustand quellenseitig undefiniert** | Sprint-Plan-Kopf; ADW-SPR-1.0-001 Kap. 17/18; PREP-02 Kap. 5.3 | **Welcher Zielstatus? Welches „kontrollierte Verfahren"?** (JX-G7P-B-02) | **PREP → Human Decision zu OD-08 (a)/(b) → separater EXEC** |
| **G7-b — OD-05-Abdeckung** | **OFFEN** — Umriss im Plan **nicht** enthalten (0 Treffer) | **Nicht bestimmbar**: ob überhaupt Abdeckung erforderlich, und in welchem Umfang | ADR-012 Z. 574/776; F-05 Kap. 21; HD-1 Kap. 18/20; HD-4 A3-5; HD4-HD2-B-01 | **U-4′: Ist die Abdeckung normativ erforderlich?** (HD4-HD2-B-03 = ungeregelt) | **A2-Feststellung durch Human Decision** (Kap. 4.5) |
| **HD-2** | **DEFERRED — OPEN / NOT DECIDED** (Projekteigner, 2026-08-11) | Bei bejahter A2-Erforderlichkeit: Entscheidung O-1 / O-2 / O-3 | `hd-4-hd2-human-decision-record-r0.md` Kap. 5/8; HD-1 Kap. 19 | Wiedervorlagebedingung („belastbare Planungsgrundlage") **undefiniert** | **Keiner** — HD-2 wird in dieser Welle **nicht** angerührt; Wiedervorlage nur durch eigene Human Decision |
| **OD-08** | **OPEN** — Prio P3; „Entscheidung nötig? **JA**" | Entscheidung zwischen Option (a) und (b) | MEP §20 OD-08; DEM §1.1 Z. 109, §366; GDR-OD01-001 Kap. 13/16 (OP-9) | Ob Option (b) mit der G7-DEC (materielle Herstellung) vereinbar ist (A1-9) | **Human Decision (Projekteigner / Governance)** |
| **Sprint Plan** | **UNVERÄNDERT** — `DRAFT / 1.0 / R0`, Kap. 6 führt Bed. 7/8 als PENDING | Abhängig von OD-08-Entscheidung und A2-Ergebnis | `docs/milestone-1.0-sprint-plan.md` Kopf, Kap. 6, Kap. 8 | Umfang einer etwaigen Nachführung über den Kopf hinaus (A1-1) | **Keiner ohne separaten EXEC-Auftrag** (G7-DEC Condition 8) |
| **OP-2** | **NICHT ERFÜLLT** — „Coding Authorization (Bedingungen 8–9, RL-05)"; benötigt „Phase-A-Protokoll + RL-05-Feststellung" | Erfüllung erst nach RL-05 **und** separater Coding-Autorisierung | Sprint Plan Kap. 8; PREP-01 Kap. 7; PREP-02 Kap. 3 | — | **Keiner** — Ebene D, außerhalb dieser Welle |
| **RL-05** | **NOT REACHED** | Eintritt setzt genehmigte Sprintplanung voraus (§10.5) | IP §10.5; PREP-02 Kap. 4.3/7 | Instanz namentlich nicht normiert (U-5) | **Separate RL-05-FINAL-PREP/DEC — erst nach nachgewiesener Bedingung 7** (G7-DEC Condition 12) |
| **Coding (Ebene D)** | **NOT AUTHORIZED** | Bedingungen 7 **und** 8 **und** 9, kein Ausschlussgrund | IP §10.6 (kumulativ); GDR-OD01-001 Kap. 14; F-05 Kap. 21 (zusätzlich GC-06) | — | **Keiner** |
| **QG-006** | **NOT STARTED** | Abschluss WP-003 **und** WP-004 | Sprint Plan Kap. 5; IP §8.7 („ausnahmslos"); GDR-OD01-001 Kap. 13 | — | **Keiner** |

---

## 8. Human-Decision-Bedarf

### 8.1 Welche Entscheidungen muss der Projekteigner treffen?

| # | Entscheidungsgegenstand | Autorität | Klasse der Autoritätsgrundlage |
|---|---|---|---|
| **HD-A** | **Sequenz** — in welcher Reihenfolge A1 und A2 behandelt werden (bzw. ob parallel) | **Projekteigner** | **UNKNOWN normativ** — keine Quelle regelt die Sequenz; Zuständigkeit folgt aus der durchgehenden Präzedenz (PREP-02 Kap. 12/13) → **INFERENCE (stark)** |
| **HD-B** | **A2-Feststellung** — ob und in welchem Umfang die OD-05-Umriss-Abdeckung für eine genehmigte Sprintplanung erforderlich ist (U-4′) | **Projekteigner** | **INFERENCE** — PREP-02 Kap. 13 weist die Bedingung-7-Auslegung dem Projekteigner zu; normativ nicht ausdrücklich zugewiesen |
| **HD-C** | **OD-08-Entscheidung** — Option (a) nachführen oder (b) belassen; bei (a) zusätzlich: Zielstatus und Verfahren | **Projekteigner / Governance** | **FACT** — MEP §20 OD-08 („Erforderliche Autorität: Projekteigner / Governance"); DEM §1.1 („Entscheidung nötig? JA — Projekteigner / Governance"); ADW-SPR-1.0-001 Kap. 17 („separat autorisierter Schritt") |
| **HD-D** | **HD-2** — nur falls HD-B die Erforderlichkeit bejaht | **Projekteigner** | **FACT** — HD-1 Kap. 19 |

### 8.2 Was darf in dieser PREP NICHT vorweggenommen werden?

```text
- Die A2-Feststellung selbst (HD-B) — Kap. 4.5.
- Die OD-08-Optionswahl (HD-C) — Kap. 5, A1-7/A1-9.
- Die Sequenzentscheidung (HD-A) — Kap. 6.4.
- HD-2 in jeder Ausprägung (HD-D) — auch keine Wiedervorlage, keine
  Neubewertung der Wiedervorlagebedingung.
- Jede Aussage darüber, ob Bedingung 7 nach A1/A2 erfüllt WÄRE.
- Die RL-05-Feststellung und jede Vorstufe davon.
```

### 8.3 Ist für A2 eine Human Decision erforderlich?

> **JA — für die abschließende Feststellung.** Die Prüfung ist mit Kap. 4
> durchgeführt; ihr Ergebnis ist **UNKNOWN**. Weil HD4-HD2-B-03 die Frage
> ausdrücklich als ungeregelt führt, ist jede abschließende Antwort eine
> Auslegung von IP §10.6 Nr. 7 und damit eine Human Decision (Kap. 4.5).
> **Ein EXEC ist für A2 nicht erforderlich** — A2 hat keine Change Surface.

### 8.4 Ist für A1 eine Human Decision erforderlich?

> **JA — und zusätzlich ein separat autorisierter EXEC.**
> **(1)** Human Decision zur OD-08-Optionswahl (a)/(b) — **FACT**-belegt
> (MEP §20 OD-08; DEM §1.1). **(2)** Bei Wahl (a): separater EXEC-Auftrag
> — **FACT**-belegt (ADW-SPR-1.0-001 Kap. 17; G7-DEC Condition 8;
> PREP-02 Kap. 14.2). **Ein EXEC allein genügt nicht.**

### 8.5 Reicht nach A2 ein separat autorisierter EXEC?

> **NEIN — nicht allein.** Auch nach abgeschlossener A2-Feststellung
> verbleibt für A1 die eigenständige OD-08-Entscheidung (HD-C). Zusätzlich
> ist der Zielstatus derzeit undefiniert (A1-3 / JX-G7P-B-02); ohne dessen
> Bestimmung ist ein quellengestützter EXEC nicht formulierbar.

### 8.6 Autoritätsübersicht

| Gegenstand | Autorität | Klasse |
|---|---|---|
| OD-08 / Statusnachführung (A1) | **Projekteigner / Governance** | **FACT** |
| HD-2 (bei Bedarf) | **Projekteigner** | **FACT** |
| A2-Feststellung / Bedingung-7-Auslegungsfragen | **Projekteigner** | **INFERENCE** |
| Sequenz A1/A2 | **Projekteigner** | **UNKNOWN normativ / INFERENCE (Präzedenz)** |
| Feststellung „Bedingung 7 erfüllt" | **nicht normiert** | **UNKNOWN** |
| RL-05-Feststellung | **nicht normiert**; Projekteigner nach Präzedenz | **UNKNOWN / INFERENCE (stark)** |
| Eskalationsinstanz bei Governance-Verstoß | „Governance Architect / Release Authority" (IP §7.6) — **kein Bezug zu Bedingung 7 hergestellt** | **FACT** (Wortlaut) / **UNKNOWN** (Anwendbarkeit) |

---

## 9. Optionen für den nächsten Schritt

> **Herleitung:** Die drei Optionen folgen unmittelbar aus dem
> Sequenzbefund (Kap. 6.4: nicht quellenbestimmbar) und dem
> Human-Decision-Bedarf (Kap. 8). Es wird **keine** Option erfunden; eine
> vierte Option („A1 und A2 gleichzeitig in einem Akt") wird **nicht**
> dargestellt, weil die G7-DEC die getrennte Behandlung ausdrücklich
> anordnet („die beiden … Ursachen **getrennt zu behandeln**").

| | **OPTION A — A2 zuerst** | **OPTION B — A1 zuerst** | **OPTION C — DEFERRED** |
|---|---|---|---|
| **Scope** | Vorlage der A2-Frage (U-4′) als eigener DEC-Gegenstand auf Grundlage von Kap. 4; **danach** eigener PREP → DEC (OD-08) → EXEC für A1 | Eigener PREP → DEC (OD-08) → EXEC für A1 zuerst; A2 separat und nachgelagert | Beide Achsen werden ausdrücklich vertagt; der Stand bleibt unverändert eingefroren |
| **Change Surface** | **A2: keine.** Nachgelagert bei A1: genau eine Bestandsdatei (`docs/milestone-1.0-sprint-plan.md`) | **A1: genau eine Bestandsdatei** (`docs/milestone-1.0-sprint-plan.md`) — Änderung vor geklärter Inhaltsfrage | **keine** |
| **Governance-Risiko** | Gering. Kein Eingriff in Bestandsdateien vor geklärter Inhaltsfrage. Risiko: die A2-Feststellung selbst berührt die ACN-09-Grenze, falls sie die Erforderlichkeit verneint | **Erhöht.** Eine Statusnachführung vor geklärter Abdeckungsfrage könnte einen Plan zertifizieren, dessen Genehmigungsfähigkeit genau in Frage steht — Spannung zu **ACN-09**. Zusätzlich: Zielstatus undefiniert (JX-G7P-B-02) | Keines. **ACN-09** gewahrt; keine Bedingung berührt |
| **Abhängigkeiten** | HD-B → (ggf.) HD-D → HD-C → EXEC | HD-C → EXEC; HD-B/HD-D bleiben offen; **S1a** (HD-2-Wiedervorlagebedingung) würde adressiert | keine |
| **Auswirkung auf Bedingung 7** | Bedingung 7 bleibt **NICHT ERFÜLLT**, bis **beide** Gründe beseitigt sind | dito | Bedingung 7 bleibt **NICHT ERFÜLLT** |
| **Auswirkung auf RL-05** | **keine** — RL-05 bleibt NOT REACHED | **keine** | **keine** |
| **Human Decision erforderlich?** | **JA** — HD-A (Sequenz) + HD-B, danach HD-C | **JA** — HD-A (Sequenz) + HD-C | **JA** — ausdrückliche Vertagung |
| **Quellenstütze** | S2a (JX-G7-B-02), S2b, S2c | S1a (HD-2-Wiedervorlagebedingung, **wörtlich**), S1b, U-d | Zulässige Entscheidungskategorie; Präzedenz: HD-2 = DEFERRED, AC-16 = DEFERRED |

### 9.1 RECOMMENDATION — NOT A DECISION

> ## **RECOMMENDATION: OPTION A**

**Begründung (Architektur-/Governance-Sicht):**

1. **A2 hat keine Change Surface.** Sie kann geführt werden, ohne eine
   Bestandsdatei zu berühren und ohne A1 zu präjudizieren. Das Risiko
   einer falschen Reihenfolge ist bei A2-zuerst asymmetrisch geringer.
2. **A1 ist ohne A2-Ergebnis unvollständig bestimmbar.** Der Zielstatus
   ist quellenseitig undefiniert (A1-3), und der Inhalt, den ein
   nachgeführter Plan tragen müsste, hängt von der A2-Frage ab (A1-4).
3. **ACN-09 spricht gegen einen frühen Statuseingriff.** Eine
   Statusnachführung vor Klärung der Abdeckungsfrage stünde in der Nähe
   dessen, was die G7-DEC über Option A gerade vermeiden wollte
   (JX-G7-B-04).
4. **Die Gegenlesart bleibt bestehen.** S1a (HD-2 wartet auf eine
   „belastbare Planungsgrundlage") ist wörtlich belegt. Diese Empfehlung
   **entkräftet sie nicht** und stellt **nicht** fest, dass A2 → A1
   quellenbasiert erforderlich sei — sie ist eine Risikoabwägung, keine
   Quellenableitung.

**RECOMMENDATION ≠ DECISION. Diese PREP entscheidet nichts.**

---

## 10. RL-05-Abgrenzung

> ## **RL-05 = NOT REACHED — ausdrücklich bestätigt.**

| Position | Status | Quelle |
|---|---|---|
| **RL-05** | **NOT REACHED** | IP §10.5 („Aktueller Stand": RL-02 bis RL-05 nicht erreicht); PREP-02 Kap. 7; G7-DEC Kap. 5/10 |
| **OP-2** | **NICHT ERFÜLLT** | Sprint Plan Kap. 8; G7-DEC Condition 4 |
| **Coding (Ebene D)** | **NOT AUTHORIZED** | IP §10.6 (kumulativ); GDR-OD01-001 Kap. 14; G7-DEC Condition 5 |
| **QG-006 / QG-001…QG-008** | **NOT STARTED** | Sprint Plan Kap. 5; IP §8.7; G7-DEC Condition 6 |

**Ausdrücklich nicht gezogene Ableitungen:**

```text
"PREP erstellt → Bedingung 7 näher an Erfüllung"   — NICHT GEZOGEN
"A2 geprüft → A2 festgestellt"                     — NICHT GEZOGEN (Kap. 4.5)
"OD-08 analysiert → OD-08 entschieden"             — NICHT GEZOGEN (Kap. 5)
"Sequenz empfohlen → Sequenz entschieden"          — NICHT GEZOGEN (Kap. 9.1)
"Bedingung 7 vorbereitet → RL-05 erreichbar"       — NICHT GEZOGEN
"Vorbereitung abgeschlossen → EXEC autorisiert"    — NICHT GEZOGEN
```

Diese PREP erzeugt **keine** RL-05-Feststellung, keine Vorstufe, keine
Markierung als „pending approval" oder vergleichbar.

---

## 11. Explicit Non-Decisions

```text
Bedingung 7: NICHT ERFÜLLT. NICHT abgesenkt, NICHT umgedeutet, NICHT ausgelegt.
A1: NICHT ausgeführt, NICHT vorbereitet im Sinne eines vollzogenen Schritts.
A2: NICHT ausgeführt, NICHT festgestellt — nur quellenseitig vorbereitet.
Sequenz A1/A2: NICHT entschieden. JX-G7-B-02 weder bestätigt noch verworfen.
HD-2: NICHT entschieden, NICHT wiedervorgelegt, NICHT neu bewertet — DEFERRED/OPEN.
OD-08: NICHT entschieden, NICHT geschlossen, Optionsraum NICHT verengt — OPEN.
Sprint Plan: NICHT verändert. Statuskopf NICHT nachgeführt. DRAFT / 1.0 / R0.
OD-05: NICHT verändert, NICHT bewertet, NICHT als genehmigt erklärt — OPEN.
RL-05: NICHT erreicht, NICHT festgestellt, NICHT als "pending" markiert.
OP-2: NICHT erfüllt. Coding: NOT AUTHORIZED. QG-006 / QG-001..QG-008: NOT STARTED.
ADR-012, ADR-005/006/007, HD-1, HD-3, AC-16, TD-19: UNVERÄNDERT.
Architecture Book v2.0 (FROZEN), CLAUDE.md, ROADMAP.md: UNVERÄNDERT, UNDISPONIERT.
GDR-OD01-001 Folgeaktionen A/B/C/D und Gruppen 2/3: NICHT disponiert.
U-2', U-3', U-4', U-5, U-1: NICHT geschlossen.
Keine Governance-Bedingung abgesenkt. Keine Ausnahme konstruiert. ACN-09 gewahrt.
Keine Human Decision erfunden, simuliert, erweitert oder vorweggenommen.
PREP-01, PREP-02, G7-DEC und alle historischen Archive: NICHT umgeschrieben.
Kein Produktionscode, kein Test, keine Konfiguration verändert.
Vorbestehende Working-Tree-Änderungen: UNANGETASTET, NICHT übernommen.
Kein Push, kein PR, kein Merge, kein Tag.
```

---

## 12. Change Surface

| Gegenstand | Umfang |
|---|---|
| Neue Dateien | **genau eine** — `docs/audits/jx-dev-spr01-rl05-g7-prep-r0.md` |
| Geänderte Dateien | **keine** |
| Gelöschte Dateien | **keine** |
| Produktionscode / Tests / Konfiguration | **unberührt** |
| Governance-/Status-/Archivdateien | **unberührt** |
| Sprint Plan / ADRs / Architecture Book / CLAUDE.md / ROADMAP.md | **unberührt** |
| Vorbestehende Working-Tree-Änderungen | **unangetastet** |

---

## 13. Preflight

| Check | Ergebnis |
|---|---|
| Baseline Gate: HEAD `f97fa54`, Vorkette bis `8fcf42f` lückenlos, Staging leer, keine unerwarteten Code-/Teständerungen | PASS |
| Working Tree unangetastet; nichts bereinigt | PASS |
| Source Gate: alle 22 Pflichtquellen geprüft; 13 repositoryweite Suchen durchgeführt; keine externe Quelle | PASS |
| Bedingung 7, G7-a, G7-b vollständig aus Quellen rekonstruiert (Kap. 3) | PASS |
| Jede wesentliche Aussage klassifiziert (FACT / SOURCE-DERIVED / INFERENCE / UNKNOWN / RECOMMENDATION) | PASS |
| Keine Inference als Fakt dargestellt | PASS |
| A2 vorbereitet, **nicht** ausgeführt; UNKNOWN nicht künstlich aufgelöst (Kap. 4) | PASS |
| A1 vorbereitet, **nicht** ausgeführt; keine Datei geändert (Kap. 5) | PASS |
| Sequenzfrage bewertet; JX-G7-B-02 weder bestätigt noch verworfen (Kap. 6) | PASS |
| Condition-7-Matrix vollständig (9 geforderte Elemente) (Kap. 7) | PASS |
| Human-Decision-Bedarf bestimmt; Autorität je Position klassifiziert (Kap. 8) | PASS |
| Höchstens drei Optionen; sämtlich aus Quellen und Befund abgeleitet (Kap. 9) | PASS |
| Empfehlung als **RECOMMENDATION ≠ DECISION** gekennzeichnet | PASS |
| RL-05-Abgrenzung ausdrücklich bestätigt; keine automatische Ableitung (Kap. 10) | PASS |
| Explicit Non-Decisions vollständig (Kap. 11) | PASS |
| Keine Governance-Bedingung abgesenkt; **ACN-09** gewahrt | PASS |
| Keine Statusnachführung, keine RL-05-Feststellung, keine Coding-Autorisierung, kein QG-006 | PASS |
| Genau eine neue Datei; keine bestehende Datei verändert | PASS |
| Kein Push / PR / Merge / Tag | PASS |

---

## 14. Final Governance Gate

> ## **JX-DEV-SPR01-RL05-G7-PREP-01-R0 = COMPLETED — PREPARATION ONLY**
>
> **IP §10.6 Bedingung 7 = NICHT ERFÜLLT (unverändert)**
> **A1 = NICHT AUSGEFÜHRT · A2 = NICHT AUSGEFÜHRT · HD-2 = NICHT ENTSCHIEDEN**
> **OD-08 = OPEN · Sprint Plan = DRAFT / 1.0 / R0 (unverändert)**
> **RL-05 = NOT REACHED · OP-2 = NICHT ERFÜLLT ·
> CODING = NOT AUTHORIZED · QG-006 = NOT STARTED**

**Drei Entscheidungen liegen jetzt beim Projekteigner und können durch
keine weitere Vorbereitung ersetzt werden:**

1. **HD-A — Sequenz** (A2 zuerst / A1 zuerst / vertagen) — Kap. 6.4:
   quellenseitig **nicht bestimmbar**.
2. **HD-B — A2-Feststellung** (U-4′) — Kap. 4.3: **keine eindeutige
   Quellenlage**.
3. **HD-C — OD-08-Optionswahl** (a)/(b) — Kap. 5, A1-7: registrierter
   Entscheidungsbedarf, **FACT**-belegt.

> # **STOP — HUMAN DECISION REQUIRED**

Es wird **nicht** automatisch weitergearbeitet.

---

## Revision History

| Revision | Datum | Änderung | Status |
|---|---|---|---|
| **R0** | 2026-08-13 | Vorbereitungswelle zur Herstellung von IP §10.6 Bedingung 7 nach Option A; A1/A2 quellenbasiert vorbereitet; Sequenzfrage bewertet (nicht bestimmbar); Condition-7-Matrix; Human-Decision-Bedarf (HD-A/HD-B/HD-C/HD-D) bestimmt | **COMPLETED — PREPARATION · HUMAN DECISION REQUIRED** |

---

**Ende JX-DEV-SPR01-RL05-G7-PREP-01-R0 — Preparation Wave —
JOCHEN X Milestone 1.0 (2026-08-13) — HEAD `f97fa54` — Bezugs-Baseline
`MILESTONE-1.0-BASELINE = 8fcf42f1997dfcf6ff232e75fd33c37b933991c8`**
