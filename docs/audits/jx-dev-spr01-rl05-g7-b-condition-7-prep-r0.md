# JOCHEN X — Milestone 1.0
# JX-DEV-SPR01-RL05-G7B-C7-PREP-01-R0 — Decision Preparation
## G7-b — Verhältnis zu IP §10.6 Bedingung 7

> **COMPLETED — PREPARATION ONLY · READONLY · NO DECISION**
>
> **Keine Sachentscheidung. Keine Option ausgewählt. Keine Empfehlung, keine
> Priorisierung. Kein EXEC. Keine bestehende Datei verändert. Kein `git add`,
> kein Commit, kein Push.**
>
> **Kernbefunde dieser Welle:**
> 1. Der **Tatbestand** von G7-b ist quellenseitig **vollständig bestimmt** (Kap. 3).
> 2. Ob G7-b **Bestandteil, Voraussetzung oder sonstiger notwendiger Bezugspunkt**
>    von Bedingung 7 ist, ist quellenseitig **UNKNOWN** (Kap. 6).
> 3. **Kein** quellenregistrierter Optionsraum für die weitere Behandlung von
>    **G7-b** existiert (Kap. 10).
> 4. Aus **F1-K2** folgt **keine** automatische Änderung des Governance State
>    (Kap. 8).
>
> **G7-b = OPEN · Bedingung 7 = NOT FULFILLED · HD-2 = DEFERRED / OPEN ·
> F1 = DECIDED (F1-K2, nur M1-C) · U-4′ (= F3) = DECIDED, Option C ·
> RL-05 = NOT REACHED · CODING = NOT AUTHORIZED · QG-006 = NOT STARTED ·
> Push = NOT AUTHORIZED**

---

## 1. Baseline

| Prüfung | Ergebnis |
|---|---|
| **HEAD** | `6e11d9bdd1a83c4acc81927de57ec7fc796d173c` = `6e11d9b` |
| Staging | **leer** |
| Working Tree | vorbestehende Modifikationen (`CLAUDE.md`, `ROADMAP.md`, `docs/architecture-book-v2.md`) — **unangetastet** |
| Sprint Plan | **tracked, unverändert** |
| Vorgelagert | `HD-P-01` · `F1-PREP-01` · `F1-OPTIONS-PREP-01` · **HD-F1-O (DECIDED)** · **F1-DEC-01 (F1-K2)** |
| Bezugs-Baseline | `MILESTONE-1.0-BASELINE = 8fcf42f1997dfcf6ff232e75fd33c37b933991c8` (GDR-003) |

**Baseline Gate: PASS.**

---

## 2. Quellengate (readonly, ausschließlich lokal)

| # | Quelle | Fundstelle | Für diese Welle einschlägig |
|---|---|---|---|
| S-1 | **IP §10.6** | `docs/milestone-1.0-implementation-plan.md` Z. 3499–3543 | **JA** — Nr. 7/8/9 im Wortlaut; Ausschlusskatalog 1–8 |
| S-2 | **IP §10.5** | ebd. (RL-04-Austritt / RL-05-Eintritt) | **JA** — via G7-PREP Kap. 3.1 |
| S-3 | **IP §10.9 ACN-09** | ebd. | **JA** — Absenkungsverbot |
| S-4 | **Sprint Plan Kap. 6** | `docs/milestone-1.0-sprint-plan.md` Z. 268–280 | **JA** — Coding Authorization Gate, Nr. 7/8/9 = PENDING |
| S-5 | **ADR-012 Kap. 7.1** | `docs/adr/012-plugin-security-policy-configuration.md` Z. 285–293 | **JA** — CS-1/CS-2/CS-3 im Wortlaut |
| S-6 | **ADR-012** weitere | ebd. Z. 105, 237, 273, 728, 756 | **JA** — Change Surface FINAL; OI-1; offene Varianten |
| S-7 | **OD-05 Kap. 16** | `docs/governance/od-05-governance-decision.md` Z. 446–462 | **JA** — Sprint-/WP-Auswirkung |
| S-8 | **OD-05 Kap. 17** | ebd. Z. 466–482 | **mittelbar** — U-1…U-10 |
| S-9 | **G7-PREP-01 Kap. 3.1/3.3** | `docs/audits/jx-dev-spr01-rl05-g7-prep-r0.md` Z. 134–170, 361–362 | **JA** — Tatbestand G7-a/G7-b; Bedingung-7-Rekonstruktion |
| S-10 | **A2-VERIFY Kap. 5–7** | `docs/audits/jx-dev-spr01-rl05-g7-a2-verify-r0.md` Z. 95–174 | **JA** — Normbefund zu Nr. 7 |
| S-11 | **HD-2-PREP** Kap. 11 F · Kap. 13 · NF-5 | `docs/audits/hd-4-hd2-decision-preparation-r0.md` Z. 161, 182, 206–210, 271 | **JA** — HD-2-Gegenstand, HD-2-Optionsraum, Negativbefunde |
| S-12 | **HD-2-DEC** | `docs/audits/hd-4-hd2-human-decision-record-r0.md` | **JA** — DEFERRED / OPEN |
| S-13 | **HD-1 (FINAL)** Kap. 19/20 | `docs/governance/hd-1-adr-rdr-decision.md` Z. 409, 419–423 | **JA** |
| S-14 | **PREP-02** Kap. 9.1/9.2 | `docs/audits/jx-dev-spr01-rl05-final-prep-02-r0.md` Z. 280–303 | **JA** — G7-a/G7-b, Bedingung-7-Ist-Befund |
| S-15 | **U-4′-DEC (F3)** | `docs/audits/jx-dev-spr01-rl05-g7-b-u4-prime-decision-record-r0.md` | **JA** — Option C |
| S-16 | **F1-DEC-01** | `docs/audits/jx-dev-spr01-rl05-next-decision-f1-decision-record-r0.md` | **JA** — F1-K2, Reichweite M1-C/M5-B |
| S-17 | **F1-PREP-01 · F1-OPTIONS-PREP-01** | `…-f1-prep-r0.md` · `…-f1-options-prep-r0.md` | **JA** — Quellenbefund, Negativbefunde |

**Keine externe Recherche. Keine Datei verändert. Quellengate: PASS.**

---

## 3. Prüfpunkt 1 — Der exakte Tatbestand von G7-b

| Position | Inhalt | Klasse |
|---|---|---|
| **Tatbestand (wörtlich)** | Der finalisierte **OD-05-Umriss** (CS-1 + CS-2 + CS-3, niedergelegt in **ADR-012**) ist im **Sprint Plan nicht abgedeckt** | **FACT** |
| **Dokumentseitiger Nachweis** | Volltextsuche im Sprint Plan nach `OD-05`, „Umriss", `PluginSecurityStage`, `[security]` → **0 Treffer** (HD4-HD2-B-01); auch das OP-Register (OP-1…OP-8, OTD-1/2) führt den Umriss nicht | **FACT** |
| **Registrierte Position** | **HD-2** (= **OI-1**) — „Sprint-/WP-Zuordnung des finalisierten OD-05-Umrisses"; Autorität **Projekteigner** | **FACT** |
| **Zeitliche Lage** | OP-1-Genehmigung 2026-08-09 **vor** der Umriss-Finalisierung; ADR-012 Accepted 2026-08-11; HD-1 stellt die Nichtabdeckung 2026-08-10 danach fest (HD4-HD2-B-02) | **FACT** |
| **Status** | **G7-b = OPEN**; HD-2 = **DEFERRED / OPEN / NOT DECIDED** | **FACT** |
| **Abgrenzung zu G7-a** | G7-a = physischer Sprint-Plan-Status (`DRAFT / 1.0 / R0`), registriert als **OD-08**. **Getrennter Gegenstand**, hier nicht behandelt | **FACT** |

**Beleg:** G7-PREP Kap. 3.3 (Z. 161–169); PREP-02 Kap. 9.2 (Z. 285–290).

---

## 4. Prüfpunkt 2 — Welche konkrete Abdeckung fehlt

| Frage | Befund | Klasse |
|---|---|---|
| **Was** fehlt gegenständlich? | Jede Erwähnung/Zuordnung des OD-05-Umrisses (CS-1 + CS-2 + CS-3) im Sprint Plan — weder als Work Package, noch als Planungselement, noch als Deliverable, noch textlich | **FACT (Negativbefund am Dokument)** |
| **Wo** fehlt sie? | Im **Sprint Plan** (`docs/milestone-1.0-sprint-plan.md`) sowie im **OP-Register** | **FACT** |
| **Welcher Umfang** wäre erforderlich? | **Nicht bestimmbar** — keine Quelle gibt einen Umfang vor | **UNKNOWN** |
| **Welcher Vollzugsweg** wäre zulässig? | **Nicht bestimmbar** — keine Quelle gibt ein Verfahren vor | **UNKNOWN** |
| Gegenläufiger Bestandsbefund | **OD-05 Kap. 16** (Z. 452–453): „Eigene Sprint-/WP-Zuordnung für OD-05: **keine**"; „Eigenes neues Work Package: **keines**". HD-2-PREP Befund 4 ordnet dies ausdrücklich als **historischen Stand** ein — „**kein Verbot und keine Zuordnung**" | **FACT** |
| Thematische Nähe | WP-003 (SPR-04) / WP-004 (SPR-05), Gate **QG-006** sind OD-05 thematisch zugeordnet (OD-05 Kap. 16 Z. 450–451) — jedoch ausdrücklich **RELATED — NOT DERIVED** (HD4-HD2-B-05) | **FACT** · Ableitung **nicht** zulässig |

---

## 5. Prüfpunkt 3 — Quellen, die OD-05-Umriss, CS-1/CS-2/CS-3 und ADR-012 definieren

| Gegenstand | Definierende Quelle | Wortlaut / Inhalt | Klasse |
|---|---|---|---|
| **CS-1** | ADR-012 Kap. 7.1 Z. 287 | `app/bootstrap/stages_plugin.py` — `PluginSecurityStage.execute`; „Übergabe der konfigurierten Policies an die bestehende Security-Instanz"; **REQUIRED** | **FACT (wörtlich)** |
| **CS-2** | ADR-012 Kap. 7.1 Z. 288 | `config/settings.py`; „Zugang zur `[security]`-Abbildung"; **REQUIRED** | **FACT (wörtlich)** |
| **CS-3** | ADR-012 Kap. 7.1 Z. 289 | `config/default.toml`; „Optionaler `[security]`-Abschnitt"; **REQUIRED** | **FACT (wörtlich)** |
| **Herkunft der Fixierung** | ADR-012 Z. 291–293 | `naw-a-od05-change-surface-fixation.md` Kap. 6; `f-05-od05-change-control-determination.md` Kap. 5.1 (F-5-01); HD-1 Kap. 14 | **FACT** |
| **Abschließender Charakter** | ADR-012 Z. 295, 756 | „Die Change Surface wird durch diesen Entwurf **NICHT erweitert**"; „**CHANGE SURFACE: CS-1 + CS-2 + CS-3 — FINAL**" | **NORM (innerhalb ADR-012)** |
| **OD-05 selbst** | `docs/governance/od-05-governance-decision.md` | Security Wiring Governance Decision; Kap. 16 = Sprint-/WP-Auswirkung. Der Begriff „Umriss" kommt in OD-05 **nicht** vor — die Umriss-Fixierung erfolgt über NAW-A / F-05 / ADR-012 | **FACT** |
| **Offen innerhalb der Fläche** | ADR-012 Z. 242–243, 273, 728 | CS-2-Zugangsvariante **V-1 vs. V-2** (**OI-3 / NAW-A-U1**) — **OFFEN**, der autorisierten Umsetzung vorbehalten | **FACT** |

> **Feststellung:** Der Gegenstand von G7-b ist quellenseitig **präzise und
> abschließend definiert** (CS-1 + CS-2 + CS-3). Die **Abdeckungsfrage** ist
> davon zu trennen und **nicht** definiert.

---

## 6. Prüfpunkt 4 — Sieht eine Quelle einen zulässigen alternativen Weg neben HD-2 vor?

| # | Prüfung | Befund | Klasse |
|---|---|---|---|
| A-1 | Nennt eine Quelle **ausdrücklich** einen alternativen Weg zur Behandlung von G7-b neben HD-2? | **NEIN** | **UNKNOWN (Negativbefund)** |
| A-2 | Nennt eine Quelle einen alternativen Weg **implizit** als zulässig? | **NEIN.** Auffindbar ist ausschließlich die Registrierung von HD-2 als „Abhilfeweg laut Quellen" (PREP-02 Kap. 9.2) | **FACT (Registrierung)** |
| A-3 | Existiert eine strukturelle Parallele? | **JA — für G7-a**, nicht für G7-b: **OD-08** führt für G7-a einen ausdrücklich **zweiwertigen** Optionsraum („(a) Kopf nachführen; (b) belassen") [MEP §20 OD-08]. Für **G7-b** existiert **kein** vergleichbarer registrierter Optionsraum | **FACT** — jede Übertragung auf G7-b wäre **INFERENCE** |
| A-4 | Was registriert HD-2-PREP Kap. 13? | **O-1** Zuordnung zu bestehendem WP · **O-2** Fortschreibung der genehmigten Planungsgrundlage · **O-3** DEFERRED. Dies ist der Optionsraum der **HD-2-Sachfrage** (Sprint-/WP-Zuordnung), **nicht** ein Optionsraum für „Behandlung von G7-b **ohne** HD-2" | **FACT** · Übertragung **nicht** zulässig |
| A-5 | Untersagt eine Quelle einen alternativen Weg? | **NEIN** — auch das ist nicht normiert | **UNKNOWN (Negativbefund)** |

> **Ergebnis:** Ein alternativer Weg ist **weder ausdrücklich vorgesehen noch
> ausdrücklich ausgeschlossen**. Beide Richtungen sind **UNKNOWN**.

---

## 7. Prüfpunkt 5 — Bedeutung von F1-K2 für G7-b

| Position | Befund | Klasse |
|---|---|---|
| **Was F1-K2 sagt** | Innerhalb des Gegenstandsbereichs **M1-C** („ob HD-2 als Weg für die F1-Verfahrensfrage zwingend ist") ist festgelegt: **HD-2 ist als Weg nicht zwingend.** Verbindlich und zitierfähig nach **M5-B** ausschließlich für die weitere Behandlung der Verfahrensfrage HD-2 | **DECISION (Willensakt)** — F1-DEC-01 |
| **Charakter** | Beide Pole waren quellenkundig **UNKNOWN**; F1-K2 ist **keine** aus den Quellen abgeleitete Tatsache | **FACT** (so im Record festgestellt) |
| **Was F1-K2 für G7-b *nicht* bedeutet** | G7-b ist **nicht** geheilt, **nicht** erfüllt, **nicht** bewertet. F1-K2 trifft nach M1-C **keine** materielle Aussage über die Heilung von G7-b | **NORM (Reichweitenbegrenzung aus HD-F1-O / M1-C)** |
| **Alternativer Weg** | **Nicht** autorisiert, **nicht** bestimmt, **nicht** als existent festgestellt. Aus „HD-2 nicht zwingend" folgt **nicht**, dass ein anderer Weg existiert, zulässig ist oder beschritten werden darf | **INFERENCE-Sperre — ausdrücklich nicht gezogen** |
| **HD-2** | **DEFERRED / OPEN** — durch F1-K2 **nicht** entschieden, **nicht** erledigt, **nicht** gegenstandslos. Die Nichtzwingendheit eines Weges beseitigt den Weg nicht | **FACT** |
| **Tatsächliche Wirkung auf G7-b** | **KEINE.** F1-K2 wirkt ausschließlich innerhalb M1-C; G7-b liegt außerhalb dieses Gegenstandsbereichs | **NORM + FACT** |

> **Ausdrücklich nicht gezogen:** „HD-2 nicht zwingend ⇒ G7-b heilbar" ·
> „⇒ G7-b erfüllt" · „⇒ G7-b unbeachtlich" · „⇒ Abdeckung entbehrlich" ·
> „⇒ ein anderer Weg ist zulässig".

---

## 8. Prüfpunkt 10 — Folgt aus F1-K2 eine automatische Änderung des Governance State?

| Position | Vor F1-K2 | Nach F1-K2 | Änderung |
|---|---|---|---|
| G7-b | OPEN | OPEN | **keine** |
| Bedingung 7 | NOT FULFILLED | NOT FULFILLED | **keine** |
| HD-2 | DEFERRED / OPEN | DEFERRED / OPEN | **keine** |
| U-4′ (= F3) | DECIDED, Option C | DECIDED, Option C | **keine** |
| G7-a / OD-08 | PHYSICALLY ADDRESSED / OPEN | unverändert | **keine** |
| RL-05 | NOT REACHED | NOT REACHED | **keine** |
| CODING | NOT AUTHORIZED | NOT AUTHORIZED | **keine** |
| QG-006 | NOT STARTED | NOT STARTED | **keine** |
| Push | NOT AUTHORIZED | NOT AUTHORIZED | **keine** |
| **F1** | OPEN / UNKNOWN | **DECIDED — F1-K2** (nur M1-C) | **einzige Änderung** |

> ## **Ausdrückliche Feststellung: NEIN.**
> Aus F1-K2 folgt **keine** automatische Änderung des Governance State
> **außerhalb** der Position F1 selbst. Alle übrigen Positionen bleiben
> unverändert. **FACT.**

---

## 9. Prüfpunkte 6–9 — G7-b, Bedingung 7, Nr. 8 und Nr. 9

### 9.1 Prüfpunkt 7 — Exakter Wortlaut von IP §10.6 Nr. 7 und unmittelbar relevante Quellen

| # | Quelle | Wortlaut | Klasse |
|---|---|---|---|
| W-1 | **IP §10.6 „Coding" Nr. 7** (Z. 3522) | „**Eine genehmigte Sprintplanung liegt vor**" | **NORM (wörtlich)** |
| W-2 | **IP §10.6 Vorspann Coding** (Z. 3517–3518) | „Die Umsetzung von Produktionscode darf beginnen, wenn **zusätzlich sämtliche** folgenden Bedingungen erfüllt sind" | **NORM (wörtlich)** |
| W-3 | **IP §10.5 RL-04-Austritt** | „**Genehmigte Sprintplanung liegt vor**" | **NORM (wörtlich)** — via G7-PREP Kap. 3.1 |
| W-4 | **IP §10.5 RL-05-Eintritt** | „**Genehmigte Sprintplanung**; protokollierte Baseline-Bestätigung gemäß Kapitel 3.8" | **NORM (wörtlich)** — via G7-PREP Kap. 3.1 |
| W-5 | **IP §10.5 Vorspann** | Readiness Levels werden „**ausschließlich vollständig** erreicht. Ein Teilerreichen ist nicht vorgesehen." | **NORM (wörtlich)** |
| W-6 | **Sprint Plan Kap. 6** (Z. 276) | Bedingung 7 = „**PENDING** — dieser Plan ist DRAFT; Genehmigung durch Projekteigner ausstehend" | **FACT (wörtlich, Eigenbewertung)** |
| W-7 | **IP §10.9 ACN-09** | „Keine Absenkung bestehender Bedingungen. Voraussetzungen, Kriterien und Ausschlüsse dürfen nicht zur Herstellung der Genehmigungsfähigkeit gelockert werden." | **NORM** |
| W-8 | **IP §10.6 Ausschlüsse** (Z. 3531–3543) | 8 Ausschlussgründe, u. a. Nr. 1 „Der Plan trägt den Status **DRAFT**" und Nr. 7 „Der Plan **deckt seinen Planungsscope nicht vollständig ab**"; „Ein **einzelner** Ausschlussgrund genügt. Die Ausschlüsse wirken **unabhängig** voneinander." | **NORM (wörtlich)** |

> **Hinweis zu W-8:** Ausschlussgrund 7 spricht vom **Plan** (Implementation
> Plan) und seinem **Planungsscope**. Ob er auf den **Sprint Plan** und auf
> die OD-05-Abdeckung anwendbar ist, ist **in keiner Quelle festgestellt** —
> **UNKNOWN**. Eine Gleichsetzung mit G7-b wäre **INFERENCE** und wird
> **nicht** vorgenommen. Der Ausschlusskatalog wird hier **nicht geprüft**
> (nicht Auftragsgegenstand).

### 9.2 Prüfpunkt 8 — Genügt die Genehmigung der Sprintplanung allein?

| Frage | Befund | Klasse |
|---|---|---|
| Was normiert Nr. 7 positiv? | Ausschließlich: „Eine genehmigte Sprintplanung liegt vor" | **NORM** |
| Definiert eine Quelle, **was „genehmigt"** im Einzelnen erfordert? | **NEIN** — weder Dokumentstatus noch Abdeckungskriterium noch Genehmigungsverfahren normiert (**Definitionslücke, quellenseitig festgestellt**) | **UNKNOWN** |
| Definiert eine Quelle ein **Abdeckungskriterium**? | **NEIN** — kein OD-05-, WP-, Deliverable- oder Inhaltskatalog | **FACT (Negativbefund am Wortlaut)** |
| Verlangt eine Quelle ausdrücklich, dass OD-05 im Sprint Plan enthalten sein **muss**, damit Nr. 7 erfüllt ist? | **NEIN — nicht gefunden** (A2-VERIFY Kap. 7) | **FACT (Negativbefund)** |
| Ist-Lage der Genehmigung | ADW-SPR-1.0-001 genehmigt den Plan **als Planungsgrundlage**; physischer Status bleibt **DRAFT**; Kap. 18 schließt „Coding-Freigabe (OP-2 offen)" und „Statusänderung des Sprint Plans" ausdrücklich aus | **FACT (wörtlich)** |
| Hat OP-1 damit Bedingung 7 erfüllt? | **NEIN** — sieben nachgelagerte Quellen führen Bedingung 7 unverändert als nicht erfüllt; **keine** Quelle bezeichnet sie als erfüllt | **FACT** |
| Gibt es **weitere quellengetragene Voraussetzungen** für Nr. 7 über die Genehmigung hinaus? | **UNKNOWN** — der Wortlaut nennt keine; die Definitionslücke ist nicht geschlossen. Aus dem Fehlen weiterer Kriterien folgt **weder**, dass die Genehmigung allein genügt, **noch** das Gegenteil | **UNKNOWN** |

### 9.3 Prüfpunkt 6 — Ist G7-b Bestandteil, Voraussetzung oder notwendiger Bezugspunkt von Bedingung 7?

| # | Prüfung | Befund | Klasse |
|---|---|---|---|
| B-1 | Ist G7-b **Bestandteil** von Bedingung 7? | **Keine Quelle stellt dies fest** | **UNKNOWN (Negativbefund)** |
| B-2 | Ist G7-b **Voraussetzung** von Bedingung 7? | **Keine Quelle stellt dies fest** | **UNKNOWN (Negativbefund)** |
| B-3 | Ist G7-b **sonstiger notwendiger Bezugspunkt**? | **Keine Quelle stellt dies fest** | **UNKNOWN (Negativbefund)** |
| B-4 | Wörtlicher Negativbefund | HD-2-PREP **NF-5** (Z. 271): „**Keine Quelle regelt**, ob die HD-2-Zuordnung Bestandteil der Erfüllung von IP §10.6 Nr. 7 ist (UNDETERMINED)". HD4-HD2-B-03 führt es als **HUMAN REVIEW REQUIRED** | **FACT (Negativbefund, wörtlich)** |
| B-5 | Wie führen die Quellen G7-b tatsächlich? | Als **offenen Governance-Befund** — fünf Quellen behandeln die Nichtabdeckung als Grund/Befund (F-05 Kap. 17/21; HD-1; HD-4-A3; G7-PREP Kap. 4.1) | **FACT (Befundführung)** |
| B-6 | Folgt daraus eine normative Pflicht? | **Nicht belegt** (A2-VERIFY Z. 122–123): „Belegt: fehlende Abdeckung wird als offener Governance-Befund geführt. Nicht belegt: daraus folgt eine normative Pflicht" | **FACT (Negativbefund)** |
| B-7 | Entschiedener Stand zur Erforderlichkeit | **U-4′ (= F3) = Option C** — es wurde **bewusst nicht** entschieden, ob und in welchem Umfang der Umriss für Nr. 7 erforderlich ist. Weder bejaht noch verneint | **DECISION / FACT** |
| B-8 | Gleichsetzung G7-b = Bedingung 7 | **Unzulässig** — G7-b ist **einer von zwei** registrierten Gründen (neben G7-a) dafür, dass Bedingung 7 als nicht erfüllt geführt wird; die Bedingung selbst ist umfassender (W-1…W-6) | **FACT** — Gleichsetzung **nicht** vorgenommen |

> **Ergebnis Prüfpunkt 6: UNKNOWN.** Die Rolle von G7-b für Bedingung 7 ist
> quellenseitig **nicht bestimmt** — weder positiv noch negativ.

### 9.4 Prüfpunkt 9 — Zusammenhang zu Nr. 8 und Nr. 9

| Position | Wortlaut / Status | Klasse |
|---|---|---|
| **Nr. 8** | „Die **Baseline-Bestätigung** gemäß Kapitel 3.8 ist protokolliert (Phase A abgeschlossen)" (IP Z. 3523). Sprint Plan Kap. 6: **PENDING**. Sprint Plan Z. 90: „SPR-01 enthält kein Coding. Sein Abschluss ist Coding-Bedingung 8 … und Eintritt für RL-05" | **NORM / FACT** |
| **Nr. 9** | „**Readiness Level RL-05 ist erreicht**" (IP Z. 3524). Sprint Plan Kap. 6: „**PENDING** — **setzt Nr. 7 und Nr. 8 voraus**" | **NORM / FACT (wörtlich)** |
| **Verhältnis** | Nr. 9 ist von Nr. 7 **und** Nr. 8 abhängig (Sprint Plan Z. 278); RL-05-Eintritt verlangt zusätzlich die protokollierte Baseline-Bestätigung (IP §10.5) | **NORM** |
| **Verhältnis zu G7-b** | **Keine Quelle verknüpft G7-b mit Nr. 8 oder Nr. 9.** G7-b betrifft ausschließlich den Befundkreis um Nr. 7 | **FACT (Negativbefund)** |
| **Ausdrückliche Abgrenzung** | Nr. 8 und Nr. 9 werden hier **nicht geprüft, nicht bewertet und nicht mit G7-b gleichgesetzt**. Ihre Nennung dient allein der Einordnung, dass Bedingung 7 nicht isoliert steht | **PROCEDURAL FACT** |
| **HD-2 ↔ RL-05** | „Ist HD-2 Voraussetzung für RL-05? — **NICHT BELEGT / UNDETERMINED**" (HD-2-PREP Kap. 11 F, Z. 182) | **FACT (Negativbefund, wörtlich)** |

---

## 10. Prüfpunkte 11/12 — OPTIONS-GATE für die weitere Behandlung von G7-b

Gesucht wurde ein **bereits quellenregistrierter** Optionsraum für die weitere
Behandlung von **G7-b**.

| # | Prüfung | Ergebnis |
|---|---|---|
| O-1 | Registriert **PREP-02** Optionen zur Behandlung von G7-b? | **NEIN** — nur die Zuordnung „Abhilfeweg = HD-2" (Kap. 9.2) |
| O-2 | Registriert **G7-PREP-01** Optionen? | **NEIN** — Kap. 8 nennt für G7-b als Weg „A2-Feststellung durch Human Decision"; A2/F3 ist mit **Option C** beantwortet |
| O-3 | Registriert **G7-DEC-01 / G7-DEC-02** Optionen? | **NEIN** — Verfahrensfestlegungen (A1/A2-Trennung, Sequenz A2 → A1) |
| O-4 | Registriert **A2-VERIFY** Optionen? | **NEIN** — führt den Punkt als UNKNOWN |
| O-5 | Registrieren die **HD-2-Unterlagen** Optionen? | **NEIN für G7-b.** Der dort registrierte Optionsraum **O-1 / O-2 / O-3** (HD-2-PREP Kap. 13) gehört zur **HD-2-Sachfrage** (Sprint-/WP-Zuordnung) und ist **nicht** auf „Behandlung von G7-b" übertragbar |
| O-6 | Registriert **OD-08 / MEP §20** Optionen für G7-b? | **NEIN** — der zweiwertige Optionsraum (a)/(b) gehört zu **G7-a** |
| O-7 | Registriert **HD-1 / IP §10.6 / §10.9 / OD-05 / ADR-012** Optionen? | **NEIN** |
| O-8 | Erzeugt **F1-K2** einen Optionsraum für G7-b? | **NEIN** — F1-K2 wirkt nur innerhalb M1-C (Kap. 7, 8) |

> ## **Optionsraum für die weitere Behandlung von G7-b = UNKNOWN / nicht quellenregistriert**

**Es wurden keine Optionen gebildet.** Keine Übertragung aus dem
HD-2-Optionsraum (O-1/O-2/O-3), keine Übertragung aus dem OD-08-Optionsraum
((a)/(b)), keine Übertragung aus dem F3-Optionsraum (A/B/C), keine
Konstruktion „logisch möglicher" Antworten als Optionsraum. **Keine
Empfehlung, keine Priorisierung.**

---

## 11. Klassifikation — Gesamtübersicht

### FACT
1. Tatbestand G7-b: OD-05-Umriss (CS-1 + CS-2 + CS-3, ADR-012) im Sprint Plan nicht abgedeckt; 0 Volltexttreffer (Kap. 3).
2. CS-1/CS-2/CS-3 sind in ADR-012 Kap. 7.1 abschließend definiert; Change Surface **FINAL** (Kap. 5).
3. OD-05 Kap. 16: „Eigene Sprint-/WP-Zuordnung: keine"; „Eigenes neues WP: keines" — historischer Stand, **kein Verbot, keine Zuordnung**.
4. HD-2 ist der **registrierte** Abhilfeweg für G7-b; DEFERRED / OPEN.
5. Kein alternativer Weg ist ausdrücklich vorgesehen; keiner ist ausdrücklich untersagt (Kap. 6).
6. Bedingung 7 wird von **keiner** Quelle als erfüllt bezeichnet; Sprint Plan Kap. 6 führt sie als **PENDING**.
7. F1-K2 ändert den Governance State außerhalb von F1 **nicht** (Kap. 8).
8. Nr. 9 setzt nach Sprint Plan Kap. 6 **Nr. 7 und Nr. 8** voraus.

### NORM
1. **IP §10.6 Nr. 7** — „Eine genehmigte Sprintplanung liegt vor" (ohne Instrument-, Verfahrens- oder Abdeckungskriterium).
2. **IP §10.6 Vorspann Coding** — „zusätzlich sämtliche" Bedingungen 7–9.
3. **IP §10.5** — RL-04-Austritt / RL-05-Eintritt; Readiness Levels nur **vollständig**.
4. **IP §10.6 Ausschlüsse** — acht Gründe, unabhängig wirkend; hier **nicht geprüft**.
5. **IP §10.9 ACN-09** — Absenkungsverbot; gilt unabhängig vom Ausgang jeder G7-b-Entscheidung.
6. **ADR-012** — Change Surface CS-1 + CS-2 + CS-3, FINAL, nicht erweitert.
7. **HD-F1-O / M1-C, M5-B** — Reichweitenbegrenzung von F1-K2.
8. **HD-4-A3 Umdeutungsverbot** — „ADR Approval ≠ HD-2 Decision ≠ Sprint/WP Coverage ≠ Coding Authorization".

### PROCEDURAL FACT
1. G7-a (OD-08) und G7-b sind **getrennte** Gegenstände; G7-a ist hier nicht behandelt.
2. Für G7-a existiert ein registrierter zweiwertiger Optionsraum, für G7-b **nicht** (Kap. 6, A-3).
3. HD-2 besitzt eine Wiedervorlagebedingung ohne Termin und ohne Verfahren.
4. Die Kette PREP → DEC → EXEC ist als kontrolliertes Verfahren etabliert.
5. U-4′ (= F3) ist mit **Option C** beantwortet — die Erforderlichkeitsfrage ist bewusst offen.

### UNKNOWN
1. Ob G7-b Bestandteil / Voraussetzung / notwendiger Bezugspunkt von Bedingung 7 ist (Kap. 9.3).
2. Was „genehmigt" i. S. v. Nr. 7 im Einzelnen erfordert (Definitionslücke).
3. Ob die Genehmigung der Sprintplanung allein für Nr. 7 genügt (Kap. 9.2).
4. Erforderlicher **Umfang** einer etwaigen Abdeckung.
5. Zulässiger **Vollzugsweg** einer etwaigen Abdeckung.
6. Ob ein alternativer Weg neben HD-2 existiert oder zulässig wäre.
7. **Optionsraum** für die weitere Behandlung von G7-b (Kap. 10).
8. Ob HD-2 Voraussetzung für RL-05 ist.
9. Ob Ausschlussgrund 7 (IP §10.6) auf den Sprint Plan / G7-b anwendbar ist.
10. Verfahren zur Fortschreibung der genehmigten Planungsgrundlage (HD4-HD2-B-04).

### INFERENCE — **nicht als Norm verwendet**
1. „F1-K2 ⇒ G7-b heilbar / geheilt / unbeachtlich."
2. „F1-K2 ⇒ alternativer Weg zulässig oder autorisiert."
3. „F1-K2 ⇒ HD-2 erledigt oder gegenstandslos."
4. „G7-b offen ⇒ Bedingung 7 unerfüllbar" **und** „G7-b unbeachtlich ⇒ Bedingung 7 erfüllt."
5. „Nichtabdeckung als Befund geführt ⇒ normative Abdeckungspflicht."
6. „OD-05 Kap. 16 ‚keine Zuordnung' ⇒ Zuordnung verboten oder entbehrlich."
7. „WP-003/WP-004 thematisch nah ⇒ Zuordnung ableitbar" (RELATED — NOT DERIVED).
8. „OD-08-Optionsraum (a)/(b) ⇒ analog für G7-b."
9. „HD-2-Optionsraum O-1/O-2/O-3 ⇒ Optionsraum für G7-b."
10. Gleichsetzung **G7-b = Bedingung 7**.
11. Gleichsetzung G7-b mit Nr. 8 oder Nr. 9.

---

## 12. HUMAN-DECISION-GATE

| # | Erforderliche Human Decision | Charakter | Status |
|---|---|---|---|
| **HD-G7B-O** | **Bestimmung/Bildung des Optionsraums für die weitere Behandlung von G7-b** | **vorgelagert** — ohne registrierten Optionsraum gibt es nichts zu wählen (Kap. 10) | **ERFORDERLICH** |
| **HD-G7B-S** | **Sachentscheidung zur weiteren Behandlung von G7-b** im so bestimmten Optionsraum | nachgelagert | **ERFORDERLICH, nachgelagert** |

**Bedingt, je nach Ausgang:**

| # | Folgeentscheidung | Auslöser |
|---|---|---|
| HD-G7B-S1 | Erforderlicher **Umfang** einer Abdeckung | nur falls eine Abdeckung hergestellt werden soll |
| HD-G7B-S2 | Zulässiger **Vollzugsweg** | dito |
| HD-G7B-S3 | Behandlung des **HD-2-Wiedervorlageverfahrens** (nicht normiert) | nur falls HD-2 als Weg gewählt wird |

**Ausdrücklich NICHT Gegenstand und NICHT erforderlich für diese Welle:**
eine erneute Entscheidung zu **F1** oder **F3** · eine Sachentscheidung zu
**HD-2** · eine Entscheidung zu **OD-08 / G7-a** · eine Bewertung von
**Bedingung 7** · Bedingungen 8/9 · der Ausschlusskatalog · RL-05 · Coding ·
QG-006 · Push.

**Keine Entscheidung wurde getroffen.**

---

## 13. Explicit Non-Decisions

```text
G7-b: NICHT bewertet, NICHT geheilt, NICHT geschlossen — OPEN.
G7-b-Optionsraum: NICHT gebildet, NICHT uebertragen, NICHT konstruiert — UNKNOWN.
Verhaeltnis G7-b <-> Bedingung 7: NICHT bestimmt — UNKNOWN.
Gleichsetzung G7-b = Bedingung 7: NICHT vorgenommen.
Bedingung 7: NICHT bewertet, NICHT erfuellt, NICHT teilerfuellt, NICHT
      abgesenkt, NICHT umgedeutet — NOT FULFILLED; ACN-09 gewahrt.
Bedingungen 8 / 9: NICHT geprueft, NICHT bewertet, NICHT mit G7-b gleichgesetzt.
Ausschlusskatalog IP §10.6: NICHT geprueft.
F1-K2: NICHT ausgelegt, NICHT ueber M1-C hinaus angewendet; erzeugt KEINE
      automatische Aenderung des Governance State (Kap. 8).
Alternativer Weg: NICHT bestimmt, NICHT autorisiert, NICHT als existent
      festgestellt — UNKNOWN.
HD-2: NICHT entschieden, NICHT wiedervorgelegt, NICHT aufgehoben, NICHT
      erledigt — DEFERRED / OPEN. Wiedervorlageverfahren NICHT definiert.
F3 / U-4': NICHT erneut aufgeworfen — bleibt Option C.
G7-a / OD-08: NICHT beruehrt, NICHT entschieden, Optionsraum NICHT verengt.
Umfang / Vollzugsweg: NICHT bestimmt.
OD-05 / ADR-012: NICHT geaendert, NICHT ausgelegt, NICHT freigegeben.
Sprint Plan: NICHT veraendert. Erstversionierung: NICHT entschieden — OPEN.
Bestehende Governance-Dokumente: NICHT veraendert — ausschliesslich gelesen.
RL-05: NOT REACHED. Coding: NOT AUTHORIZED. QG-006: NOT STARTED.
EXEC: NICHT autorisiert, NICHT erstellt.
Push: NICHT ausgefuehrt, NICHT autorisiert. Kein PR, Merge, Tag.
Kein git add, kein Commit, kein Reset, kein Amend, kein Rebase.
Keine Empfehlung, keine Priorisierung, keine Option ausgewaehlt.
```

---

## 14. Change Surface

| Gegenstand | Umfang |
|---|---|
| Neue Dateien | **genau eine** — `docs/audits/jx-dev-spr01-rl05-g7-b-condition-7-prep-r0.md` |
| Geänderte / gelöschte Dateien | **keine** |
| Sprint Plan · OD-05 · ADR-012 · IP · HD-1 · G7-DEC · U-4′-DEC · F1-DEC · HD-2-Unterlagen · `CLAUDE.md` · `ROADMAP.md` · Code · Tests · Config · sonstige Governance-Dateien | **UNBERÜHRT** — ausschließlich gelesen |
| `git add` / Commit / Push / PR / Merge / Tag / Reset / Amend / Rebase | **NICHT AUSGEFÜHRT** |
| Vorbestehende Working-Tree-Änderungen | **UNANGETASTET** |

---

## 15. Governance State — unverändert

| Position | Status |
|---|---|
| **G7-b** | **OPEN** · Optionsraum **nicht registriert** |
| **Verhältnis G7-b ↔ Bedingung 7** | **UNKNOWN** |
| **G7-a / OD-08** | **PHYSICALLY ADDRESSED** / **OPEN** |
| **IP §10.6 Bedingung 7** | **NOT FULFILLED** |
| **Bedingungen 8 / 9** | **PENDING** — nicht geprüft |
| **F1 / HD-F1-S** | **DECIDED — F1-K2**, ausschließlich im Gegenstandsbereich M1-C |
| **HD-F1-O** | **DECIDED** |
| **U-4′ (= F3)** | **DECIDED — Option C** |
| **HD-2** | **DEFERRED / OPEN** |
| **RL-05** | **NOT REACHED** |
| **CODING** | **NOT AUTHORIZED** |
| **QG-006 / QG-001…QG-008** | **NOT STARTED** |
| **Push** | **NOT AUTHORIZED** |
| Sprint Plan · SPVERS (`7c7a572`) · GOV-ARTIFACTS (`6e11d9b`) · A1-EXEC | **unverändert** |

---

## 16. STOP

> Keine Sachentscheidung · kein Optionsraum gebildet · keine Empfehlung ·
> keine Priorisierung · kein EXEC · kein Coding · kein Push.
>
> **Nächster zulässiger Schritt:** **HD-G7B-O** — Human Decision zur Bildung
> bzw. Bestimmung des Optionsraums für die weitere Behandlung von G7-b.

---

## 17. Revision History

| Revision | Datum | Änderung | Status |
|---|---|---|---|
| **R0** | 2026-08-14 | Vorbereitung der weiteren Behandlung von **G7-b** im Verhältnis zu **IP §10.6 Bedingung 7**: Quellengate (17 Quellen, Primärwortlaut); exakter G7-b-Tatbestand; fehlender Abdeckungsgegenstand; Definition von CS-1/CS-2/CS-3 und ADR-012; Prüfung auf ausdrücklich zugelassene alternative Wege (**Negativbefund in beide Richtungen**); Bedeutung und Reichweitenbegrenzung von **F1-K2**; ausdrückliche Feststellung, dass aus F1-K2 **keine** automatische Änderung des Governance State folgt; Wortlaut IP §10.6 Nr. 7 nebst §10.5, Sprint Plan Kap. 6, ACN-09 und Ausschlusskatalog; Verhältnis zu Nr. 8/Nr. 9 ohne Gleichsetzung; **OPTIONS-GATE: G7-b-Optionsraum = UNKNOWN / nicht quellenregistriert**; Klassifikation FACT / NORM / PROCEDURAL FACT / UNKNOWN / INFERENCE; erforderliche Human Decisions **HD-G7B-O** und **HD-G7B-S** sowie bedingt HD-G7B-S1…S3 | **COMPLETED — PREPARATION ONLY** |

---

**Ende JX-DEV-SPR01-RL05-G7B-C7-PREP-01-R0 — Decision Preparation —
JOCHEN X Milestone 1.0 (2026-08-14) — HEAD `6e11d9b` — Bezugs-Baseline
`MILESTONE-1.0-BASELINE = 8fcf42f1997dfcf6ff232e75fd33c37b933991c8`**
