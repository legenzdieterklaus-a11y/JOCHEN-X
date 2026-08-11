# JOCHEN X — Milestone 1.0
# HD4-HD2-DECISION-01-R0 — HD-2 Human Decision Preparation
## Entscheidungsvorbereitung Sprint-/WP-Zuordnung des finalisierten OD-05-Umrisses

> **COMPLETED — HUMAN DECISION REQUIRED**
>
> Dieses Dokument bereitet die offene **HD-2**-Entscheidung (Sprint-/WP-
> Zuordnung des finalisierten OD-05-Umrisses) quellenbasiert für den
> **Projekteigner** vor. Es trifft **keine** Entscheidung, nimmt **keine**
> Zuordnung vor, erfindet **keine** WP-Nummern und erzeugt **keine** neue
> Governance-Regel. Ergebnis: **HD-2 DECISION READY — HUMAN DECISION
> REQUIRED · HD-2 = OPEN / NOT DECIDED.**
>
> **CODING = NOT AUTHORIZED** · **RL-05 = NOT REACHED** · **QG-006 = NOT STARTED**

---

## 0. Document Identity

| Feld | Wert |
|---|---|
| **Document ID** | **HD4-HD2-DECISION-01-R0** |
| Subject | HD-2 Human Decision Preparation / Decision Gate |
| Date | 2026-08-11 |
| Pfad | `docs/audits/hd-4-hd2-decision-preparation-r0.md` |
| Revision | R0 |
| **Bezugs-Baseline** | `MILESTONE-1.0-BASELINE = 8fcf42f1997dfcf6ff232e75fd33c37b933991c8` (historisch, unverändert) |
| HEAD bei Beginn | `bc4ec44b92b3d580617c5de647c52cb1c56e22f4` (HD4-A3-R0) |
| Branch | `milestone-1.0-governance` |
| **Status** | **COMPLETED — HUMAN DECISION REQUIRED** |
| Rolle des Erstellers | Governance-/Architektur-Analyst — **nicht** entscheidungsbefugt |
| Entscheidungsautorität HD-2 | **Projekteigner** [SOURCE: HD-1 Kap. 19] |

## 1. Purpose

Vorbereitung der offenen HD-2-Entscheidung, sodass der Projekteigner eine
informierte Human-Entscheidung treffen kann. Das Dokument trennt durchgehend:
(1) bestehende Fakten, (2) bestehende Governance-Regeln, (3) bestehende
Abhängigkeiten, (4) offene Entscheidungsfragen, (5) quellenbasiert
ableitbaren Entscheidungsraum, (6) Human Decision Required.

## 2. Scope

**In Scope:** Baseline-Gate; Source Gate inkl. repositoryweiter Suchen
(HD-2, F5-U1, Sprint, WP, OD-05-Umriss, WP-003, WP-004, QG-006, OI-1,
AC-16); Chronologie; exakte Bestimmung des HD-2-Gegenstands; Sprint-/WP-
Inventar; Abhängigkeits- und Voraussetzungsanalyse (§7-Fragen A–G);
Optionsraum-Analyse; Human-Decision-Gate; OI-1-/UNKNOWN-Traceability;
Archivierung; Commit.

## 3. Non-Goals

Keine HD-2-Entscheidung; keine eigenmächtige Sprint-/WP-Zuweisung; keine
neuen Sprint-/WP-Nummern; keine Änderung der bestehenden Sprintplanung;
keine Änderung oder erneute Genehmigung von ADR-012; keine HD-3-Entscheidung;
keine Schließung von F4-U2, OI-1 oder anderen UNKNOWNs; keine
Coding-Autorisierung; kein RL-05; kein QG-006; keine neue Governance-Regel
oder Approval-Reihenfolge; keine Ableitung von „APPROVED"/„COMPLETED" aus
„PARALLEL"; keine Umdeutung historischer Befunde; keine Rekonstruktion nicht
auffindbarer Inhalte; kein Push/PR/Merge.

## 4. Baseline

| Prüfung | Ergebnis | Klasse |
|---|---|---|
| `git rev-parse HEAD` | `bc4ec44b92b3d580617c5de647c52cb1c56e22f4` — entspricht dem erwarteten HEAD `bc4ec44` | SOURCE FACT |
| Parent-Kette | `bc4ec44` (HD4-A3-R0) → `3231e5b` (HD4-A2-R0) → `70893fc` (HD4-A1-R0) → `14354b8` (HD4-APP-01-R0) → `8414384` (HD4-HDR-01-R0) → `b20858e` (HD4-GOV-DECISION-R0) → `641947c` (HD4-AP-01-R0) → `1efb61b` (HD4-FU-R0) → `8fcf42f` (MILESTONE-1.0-BASELINE) — **exakt wie erwartet** | SOURCE FACT |
| HD4-Archive vorhanden | alle acht (`hd-4-a1` … `hd-4-a3`, `-approval-*`, `-governance-*`, `-human-decision-*`) | SOURCE FACT |
| Unerwarteter Governance-Commit seit HD4-A3-R0 | **keiner** | SOURCE FACT |
| Working Tree | vorbestehende Modifikationen und untracked Dokumente — **unangetastet** | SOURCE FACT |
| Staging vor Beginn | leer | SOURCE FACT |

**Status: PASS** — historische Bezugs-Baseline bleibt `8fcf42f`.

## 5. Source Gate

| # | Source | Verification |
|---|---|---|
| 1 | `docs/adr/012-plugin-security-policy-configuration.md` | SOURCE FACT — ND-5, KZ-1, OI-1 (Kap. 19), Kap. 20/21.1; **nicht verändert** |
| 2 | `docs/audits/hd-4-a3-hd2-follow-up-r0.md` (HD4-A3-R0) | SOURCE FACT — A-3 = PARALLEL VERIFIED; HD-2 OPEN; Prerequisite-Prüfungen NO/NO |
| 3 | `docs/audits/hd-4-human-decision-record-r0.md` | SOURCE FACT — „Keine Entscheidung über HD-2" |
| 4 | `docs/audits/hd-4-approval-decision-r0.md` | SOURCE FACT — Human-Entscheidung HD-4 mit Explicit Non-Decision HD-2 |
| 5 | `docs/audits/hd-4-approval-readiness-r0.md` | SOURCE FACT — A-3-Analyse (A3-1 … A3-7), NF-3, U-C |
| 6 | `docs/audits/hd-4-governance-decision-r0.md` | SOURCE FACT — HD-2 OPEN durchgehend |
| 7 | `docs/audits/hd-4-governance-follow-up-r0.md` | SOURCE FACT — Traceability F5-U1 → HD-2 → OI-1 |
| 8 | HD-1 `docs/governance/hd-1-adr-rdr-decision.md` | SOURCE FACT — Kap. 17 („separat"), 18, 19 (HD-2, Projekteigner), 20 (Schritt 2 parallel; Schritt 5 „erst nach 1–4 und RL-05") |
| 9 | F-5 `docs/governance/f-05-od05-change-control-determination.md` | SOURCE FACT — **PRE-HD-1/HISTORISCH**: H-2, F5-U1 (Kap. 17/19), HD-2-Ausweisung (Kap. 20) |
| 10 | F-4 `docs/governance/f-04-od05-td19-scope-assessment.md` | GEPRÜFT — kein HD-2-Vorkommen; F4-U1/U2/U3 abgegrenzt |
| 11 | OD-05 `docs/governance/od-05-governance-decision.md` | SOURCE FACT — Kap. 15 (QG-006, SG-C/D/E), **Kap. 16** (WP-003/WP-004; „Eigene Sprint-/WP-Zuordnung für OD-05: **keine**"; „Eigenes neues Work Package: **keines**"; kein Sprint gestartet) |
| 12 | Implementation Plan `docs/milestone-1.0-implementation-plan.md` (APPROVED R1.2) | SOURCE FACT — §10.6 Authorization Criteria: Sprint Planning 1–6, **Coding 7–9**, Ausschlusskatalog |
| 13 | Development Standard v1.1 | GEPRÜFT — §5/§13/§17 Anh. B; kein HD-2-Bezug; kein §10.6 im Dev-Standard (per HD4-A3-B-02) |
| 14 | Sprint-/WP-Planungsartefakte | SOURCE FACT — `docs/milestone-1.0-sprint-plan.md` (DRAFT 1.0 R0); `docs/governance/milestone-1.0-sprint-planning-approval-decision-op1.md` (**ADW-SPR-1.0-001**, FINAL, 2026-08-09); `docs/audits/milestone-1.0-sprint-planning-summary-r0.md`; `docs/governance/milestone-1.0-sprint-planning-preflight.md` |

**Repositoryweite Suchen** (`docs/`, read-only): `HD-2` → 11 Dateien (10 aus
der HD-4-/HD-1-/F-5-Kette + HD4-A3-R0) · `F5-U1` → 8 Dateien (sämtlich
bekannte Kette) · `AC-16` → 5 Dateien (HD-4-Kette; HD-3-Bezug) · `OI-1` →
10 Dateien · `WP-003`/`WP-004`/`QG-006` → Planungs-/Governance-Bestand inkl.
Sprint Plan, OP-1-Approval, IP · `OD-05-Umriss`-Begriffe im Sprint Plan →
**0 Treffer** (Kap. 9, HD4-HD2-B-01). Keine externe Quelle. **Status: PASS**

## 6. Governance Chronology

| Stufe | Ereignis | Einordnung |
|---|---|---|
| 1 | **ADW-SPR-1.0-001** (2026-08-09) | Sprint Plan 1.0 R0 als **verbindliche Planungsgrundlage** genehmigt (OP-1 behandelt); Konformitätsbefund „7/7 WPs, keine neuen WPs"; **vor** der OD-05-Umriss-Finalisierung; enthält keinen HD-2-Bezug | **HISTORISCH / WEITERHIN GÜLTIG** (als Plan-Approval) |
| 2 | F-5 (PRE-HD-1) | erzeugt **F5-U1** („Sprint-/WP-Zuordnung — GOVERNANCE DECISION REQUIRED") und weist **HD-2** aus | **HISTORISCH** — fortgeschrieben durch HD-1 |
| 3 | **HD-1** (2026-08-10) | schreibt F5-U1 als **HD-2** fort (Kap. 19); „Der Umriss ist im genehmigten Sprint Plan nicht abgedeckt" (Kap. 18/20); HD-2 „OPEN — unabhängig, parallel führbar"; Umsetzungsautorisierung „erst nach 1–4 **und** RL-05" (Schritt 5) | **AKTUELL MASSGEBLICH** |
| 4 | HD-4 Draft → ADR-012 | ND-5/KZ-1/OI-1: HD-2 offen gehalten | AKTUELL (Registerstand) |
| 5 | HD4-AP-01-R0 | **A-3 = PARALLEL** (Klassifikation) | AKTUELL (Klassifikation, keine Entscheidung) |
| 6 | HD4-APP-01-R0 (2026-08-11) | HD-4 = APPROVED; Explicit Non-Decision: „Keine automatische Entscheidung über HD-2" | AKTUELL |
| 7 | HD4-A1-R0 / HD4-A2-R0 | HD-2 unverändert OPEN | AKTUELL |
| 8 | **HD4-A3-R0** | A-3 = PARALLEL **verifiziert**; HD-2 = OPEN / NOT DECIDED; Prerequisite-Prüfungen NO/NO | **AKTUELLSTER STAND** |

Überholte Aussage: Die F-5-Formulierung F5-U1 gilt nur als HD-2 fort (HD-1
Kap. 19). Weiterhin gültig: sämtliche HD-2-OPEN-Feststellungen bis HEAD.

## 7. HD-2 Definition

| Frage | Befund |
|---|---|
| Gegenstand | **Sprint-/WP-Zuordnung des finalisierten OD-05-Umrisses** [SOURCE: HD-1 Kap. 19/20; F-5 Kap. 17/20] |
| „Finalisierter OD-05-Umriss" | Die per GDR-OD05-001 (Option B) entschiedene und per NAW-A/NAW-B/F-5 fixierte Änderung: Policy-Konfiguration in der bestehenden `PluginSecurityStage`, Change Surface **CS-1** (`app/bootstrap/stages_plugin.py`) + **CS-2** (`config/settings.py`) + **CS-3** (`config/default.toml`), optionaler `[security]`-Abschnitt, keine Reihenfolgeänderung — inhaltlich niedergelegt in **ADR-012** (Accepted/Registered) |
| Was ist zuzuordnen? | Die **Umsetzung** dieses Umrisses ist bisher keinem Sprint und keinem Work Package zugeordnet; zu entscheiden ist, **ob und wie** sie in die Sprint-/WP-Struktur aufgenommen wird |
| Entscheidungsautorität | **Projekteigner** [SOURCE: HD-1 Kap. 19] |

## 8. Current State

| Position | Status | Quelle |
|---|---|---|
| HD-2 | **OPEN / NOT DECIDED** | durchgehend, zuletzt HD4-A3-R0 |
| A-3-Klassifikation | **PARALLEL — VERIFIED** (keine Entscheidung) | HD4-AP-01-R0; HD4-A3-R0 |
| HD-4 / ADR-012 | APPROVED / Accepted+Registered — **keine HD-2-Wirkung** | HD4-APP-01-R0; HD4-A1-R0 |
| Sprint Plan | 1.0 R0 (physischer Status DRAFT), per **ADW-SPR-1.0-001** als **verbindliche Planungsgrundlage genehmigt** | OP-1-Decision Kap. 16/17 |
| Umriss-Abdeckung im Plan | **NICHT ABGEDECKT** | HD-1 Kap. 18/20; dokumentseitig verifiziert (Kap. 9) |
| Coding | NOT AUTHORIZED (OP-2 offen; Bedingungen 8–9/RL-05 offen) | Sprint Plan Kap. 6; OP-1-Decision Kap. 12/18 |

## 9. Sprint/WP Inventory

**Bestand (SOURCE FACTS aus `docs/milestone-1.0-sprint-plan.md`):**

| Sprint | Work Package | Inhalt |
|---|---|---|
| SPR-01 | — | Baseline Confirmation (Phase A) |
| SPR-02 | **WP-001** | Platform Hardening |
| SPR-03 | **WP-002** | Host Service & Extensibility (QG-002) |
| SPR-04 | **WP-003** | Developer Experience (QG-004; QG-006-Anteil) |
| SPR-05 | **WP-004** | Observability (QG-006-Anteil) |
| SPR-06 | **WP-005** | Reliability |
| SPR-07 | **WP-007** | Documentation (QG-005) |
| SPR-08 | — | Phase-B-Abschluss: Regression & Messreihe |
| SPR-09 | **WP-006** | SDK Contract Verification (Phase C) |
| SPR-10 | — | Governance Closure (Phase D) |

**Befunde:**

| # | Befund | Klasse |
|---|---|---|
| 1 | WP-003 und WP-004 **existieren** (SPR-04/SPR-05); **QG-006** (Pipeline Security Compliance) ist erst nach Abschluss **WP-003 und WP-004** abschließbar [Sprint Plan Kap. 4/5; IP §8.7] | SOURCE FACT |
| 2 | Der Sprint Plan enthält **keine** Fundstelle zu `OD-05`, „Umriss", `PluginSecurityStage` oder `[security]` (Volltextsuche, 0 Treffer) — der OD-05-Umriss ist **nicht enthalten** | SOURCE FACT (HD4-HD2-B-01) |
| 3 | Auch das Offene-Punkte-Register des Plans (OP-1 … OP-8, OTD-1/OTD-2) führt den Umriss **nicht** | SOURCE FACT |
| 4 | OD-05 Kap. 16: „Eigene Sprint-/WP-Zuordnung für OD-05: **keine**"; „Eigenes neues Work Package: **keines**" — historischer Stand, kein Verbot und keine Zuordnung | SOURCE FACT |
| 5 | **Was konkret fehlt:** eine Entscheidung des Projekteigners, ob die Umsetzung des Umrisses (CS-1+CS-2+CS-3) einem bestehenden WP zugeordnet, als Planfortschreibung aufgenommen oder vertagt wird — und in welchem Verfahren die genehmigte Planungsgrundlage dafür fortgeschrieben würde | Feststellung (keine Entscheidung) |

## 10. Dependency Analysis

| Beziehung | Befund |
|---|---|
| HD-2 ↔ Sprint Plan | Der Plan ist die genehmigte Planungsgrundlage (ADW-SPR-1.0-001); der HD-2-Gegenstand beträfe deren Fortschreibung. Das **Verfahren** einer solchen Fortschreibung ist in keiner geprüften Quelle geregelt → **UNDETERMINED / HUMAN REVIEW REQUIRED** (HD4-HD2-B-04) |
| HD-2 ↔ QG-006 | thematisch benachbart (QG-006 = Pipeline Security Compliance; SG-C/SG-D/SG-E blockierend, TD-05/TD-19-bezogen [OD-05 Kap. 15]); **keine Quelle** leitet daraus eine Zuordnung des Umrisses zu WP-003/WP-004 ab → **RELATED — NOT DERIVED** (HD4-HD2-B-05) |
| HD-2 ↔ IP §10.6 Nr. 7 | materieller Zusammenhang belegt [HD4-AP-01-R0 A3-5/A3-6]: Coding setzt genehmigte Sprintplanung voraus; der Umriss ist darin nicht abgedeckt |
| HD-2 ↔ HD-3 / F4-U2 / AC-16 | getrennte Positionen — **RELATED — NOT IDENTICAL** (Kap. 16) |

## 11. Prerequisite Analysis (§7 A–G)

| # | Frage | Ergebnis | Beleg |
|---|---|---|---|
| **A** | Ist ADR-012 Voraussetzung für HD-2? | **NEGATIV BELEGT** | HD-1 Kap. 20 führt HD-2 „unabhängig, parallel führbar" neben dem gesamten HD-4-/ADR-Strang; keine Quelle nennt das ADR als HD-2-Voraussetzung |
| **B** | Ist HD-4 Approval Voraussetzung für HD-2? | **NEGATIV BELEGT** | ebd.; HD4-APP-01-R0 trennt ausdrücklich (`HD-4 APPROVAL ≠ HD-2 DECISION`) |
| **C** | Ist HD-3 Voraussetzung für HD-2? | **NICHT BELEGT** | keine Quelle verbindet HD-3 als Voraussetzung mit HD-2; getrennte Autoritäten (Security-/Architektur-Governance vs. Projekteigner); beide je „unabhängig, parallel führbar" (HD-1 Kap. 20) |
| **D** | Ist eine bestehende Sprintplanung Voraussetzung für HD-2? | **NICHT BELEGT / UNDETERMINED** (als Regel) | sachlogisch ist der genehmigte Sprint Plan der Bezugsgegenstand der Zuordnung (SOURCE FACT: er existiert, ADW-SPR-1.0-001); eine normative Voraussetzungsregel existiert in keiner geprüften Quelle |
| **E** | Ist HD-2 Voraussetzung für Coding? | **POSITIV BELEGT (mittelbar)** | HD-1 Kap. 20 Schritt 5: Umsetzungsautorisierung „erst nach 1–4 **und** RL-05" — Schritt 2 = HD-2; IP §10.6 Nr. 7 (genehmigte Sprintplanung) i. V. m. fehlender Umriss-Abdeckung [HD4-AP-01-R0 A3-5/A3-6]. **Caveat:** HD-2 allein erzeugt keine Coding-Readiness (zusätzlich Nr. 8–9, RL-05, GC-06) |
| **F** | Ist HD-2 Voraussetzung für RL-05? | **NICHT BELEGT / UNDETERMINED** | Sprint Plan Kap. 6: RL-05 (Nr. 9) „setzt Nr. 7 und Nr. 8 voraus"; ob die HD-2-Zuordnung Bestandteil der Erfüllung von Nr. 7 ist, regelt keine geprüfte Quelle (HD4-HD2-B-03) |
| **G** | Ist HD-2 Voraussetzung für QG-006? | **NICHT BELEGT** | QG-006 hängt am Abschluss von WP-003+WP-004 [IP §8.7; Sprint Plan Kap. 5]; kein HD-2-Bezug in den Quellen; thematische Nähe ist RELATED — NOT IDENTICAL |

Keine dieser Feststellungen erzeugt eine neue Regel.

## 12. Coding Separation

```text
HD-4 APPROVAL ≠ ADR-012 REGISTRATION ≠ HD-2 DECISION ≠ HD-3 DECISION
≠ SPRINT/WP EXECUTION ≠ CODING AUTHORIZATION
```

Eine künftige HD-2-Entscheidung autorisiert **kein** Coding. Es gelten
unverändert: **Coding = NOT AUTHORIZED** (OP-2 offen; IP §10.6 Nr. 7–9;
Ausschlusskatalog) · **RL-05 = NOT REACHED** · **QG-006 = NOT STARTED**.
Keine geprüfte Quelle belegt einen anderen bereits autorisierten Zustand.

## 13. Option Analysis

**Quellenbasiert ableitbarer Entscheidungsraum (strukturell — keine
Empfehlung, keine Vorauswahl):**

| Option | Struktureller Gehalt | Quellenlage |
|---|---|---|
| **O-1** | Zuordnung der Umriss-Umsetzung zu einem **bestehenden** WP (Inventar WP-001 … WP-007, Kap. 9) | Das Inventar ist SOURCE FACT. **Keine Quelle weist ein bestimmtes WP als Kandidaten aus.** Die thematische Nähe von QG-006/WP-003+WP-004 ist belegt, aber nicht als Zuordnung ableitbar (RELATED — NOT DERIVED) |
| **O-2** | **Fortschreibung** der genehmigten Planungsgrundlage (z. B. eigenes Planungselement für den Umriss) | Als Möglichkeit nur strukturell benennbar; keine Quelle definiert Verfahren oder Inhalt; die OP-1-Approval prüfte Konformität „keine neuen WPs" gegen den IP — jede Fortschreibung wäre eine neue Planungs-/Genehmigungshandlung des Projekteigners |
| **O-3** | **DEFERRED** — ausdrückliche Vertagung von HD-2 | zulässige Entscheidungskategorie des Decision Gate (APPROVED/ACCEPTED/REJECTED/DEFERRED) |

> **Eine inhaltliche Präferenz oder Empfehlung zwischen O-1/O-2/O-3 ist aus
> den vorhandenen Quellen NICHT ableitbar:**
> **SUBSTANTIVE OPTION PREFERENCE = NOT DETERMINABLE FROM CURRENT SOURCES.**
> Es wird keine WP-Nummer erfunden, keine Sprintstruktur erzeugt und keine
> Option empfohlen.

**Offene Entscheidungsfragen für den Projekteigner:**

1. Soll die Umsetzung des OD-05-Umrisses einem bestehenden WP zugeordnet
   werden — und welchem?
2. Soll stattdessen die Planungsgrundlage um ein eigenes Element
   fortgeschrieben werden?
3. Soll HD-2 ausdrücklich vertagt werden (DEFERRED)?
4. In welchem Verfahren wird die genehmigte Planungsgrundlage
   (ADW-SPR-1.0-001) im Fall einer Zuordnung fortgeschrieben?

## 14. Human Decision Gate

**Ergebnis: HUMAN DECISION NOT FOUND.**

| Prüfung | Befund |
|---|---|
| Repositoryweite Suche | keine Fundstelle mit Decision Authority + Datum + Entscheidung (APPROVED/ACCEPTED/REJECTED/DEFERRED) + Scope zu HD-2 |
| HD4-APP-01-R0 | Explicit Non-Decision: „Keine automatische Entscheidung über HD-2" |
| **ADW-SPR-1.0-001** | ist die **OP-1-Genehmigung des Sprint Plans** (2026-08-09) — **keine HD-2-Entscheidung**: sie datiert vor der Umriss-Finalisierung, erwähnt den Umriss nicht und HD-1 (2026-08-10) stellt die Nichtabdeckung **danach** fest (HD4-HD2-B-02) |
| Nicht gewertet | Analysen, Determinationen, Klassifikationen („PARALLEL"), PASS-Befunde, Empfehlungen, bestehende Planung |

```text
HD-2 = OPEN / NOT DECIDED
```

## 15. OI-1 Traceability

```text
F5-U1  →  HD-2  →  OI-1
```

| Prüfung | Ergebnis |
|---|---|
| OI-1 | **HD-2 — Sprint-/WP-Zuordnung** · **OPEN** · Zuständig: Projekteigner — **unverändert durch dieses Dokument** |
| Kette | F-5 Kap. 19 (F5-U1) → HD-1 Kap. 19 („F5-U1 … OPEN (= HD-2)") → ADR-012 Kap. 19 (OI-1) → HD4-FU-R0 (TRACEABLE BUT RENAMED — bestehender Sachverhalt) → HD4-APP-01-R0/HD4-A1-R0/HD4-A3-R0 (OPEN, Wirkung: keine) — **verifiziert, keine Scheinschließung** |

## 16. UNKNOWN Traceability

| Position | Verhältnis zu HD-2 | Einordnung |
|---|---|---|
| **F4-U1** (TD-19-Restumfang, OI-6) | andere Sachfrage | **RELATED — NOT IDENTICAL** |
| **F4-U2** (Policy-Diskontinuität, HD-3/OI-2) | andere Sachfrage, andere Autorität | **RELATED — NOT IDENTICAL** |
| **F4-U3** (FINALIZE-Konsument, OI-5) | kein HD-2-Bezug | **NOT IDENTICAL** |
| **AC-16** (ADR-012 Kap. 18) | abhängig von HD-3/F4-U2, nicht von HD-2 | **NOT IDENTICAL** |

Keine Verschmelzung; keine Position wird geschlossen.

## 17. Negative Findings

| # | Negative Finding |
|---|---|
| **NF-1** | Keine Quelle dokumentiert eine autorisierte Human-Entscheidung über HD-2 |
| **NF-2** | Keine Quelle weist ein bestimmtes bestehendes WP als Zuordnungskandidaten für den OD-05-Umriss aus |
| **NF-3** | Keine Quelle definiert das Verfahren einer Fortschreibung der genehmigten Planungsgrundlage um den Umriss |
| **NF-4** | Der Sprint Plan und sein Offene-Punkte-Register enthalten keine OD-05-/Umriss-Position |
| **NF-5** | Keine Quelle regelt, ob die HD-2-Zuordnung Bestandteil der Erfüllung von IP §10.6 Nr. 7 ist (UNDETERMINED, Kap. 11 F) |

Aus keinem Negative Finding wird eine Regel abgeleitet.

## 18. Observations

| ID | Beobachtung | Klasse |
|---|---|---|
| **HD4-HD2-B-01** | Volltextsuche im Sprint Plan nach `OD-05`, „Umriss", `PluginSecurityStage`, `[security]`: **0 Treffer** — die von HD-1 festgestellte Nichtabdeckung ist damit dokumentseitig unmittelbar verifiziert | SOURCE FACT |
| **HD4-HD2-B-02** | **ADW-SPR-1.0-001** (FINAL, 2026-08-09) genehmigte den Sprint Plan als verbindliche Planungsgrundlage (OP-1 behandelt) — **vor** HD-1 (2026-08-10) und ohne Umriss-Bezug; sie ist **keine** HD-2-Entscheidung und wird nicht als solche gewertet | SOURCE FACT / OBSERVATION |
| **HD4-HD2-B-03** | Sprint Plan Kap. 6 führt Coding-Bedingung 7 als PENDING (Planstatus bei Erstellung); ob die spätere OP-1-Genehmigung Bedingung 7 erfüllt — und ob dafür die Umriss-Abdeckung erforderlich wäre — ist in keiner geprüften Quelle geregelt: **UNDETERMINED / HUMAN REVIEW REQUIRED**; hier nicht entschieden | OBSERVATION |
| **HD4-HD2-B-04** | Die OP-1-Approval prüfte die Plan-Konformität ausdrücklich mit „7/7 WPs … Keine neuen WPs" gegen den IP; eine HD-2-Zuordnung, die den Plan erweitert, wäre eine neue Planungs-/Genehmigungshandlung — deren Verfahren ist ungeregelt (NF-3); es wird **keine** Verfahrensregel erzeugt | TRACEABILITY FINDING |
| **HD4-HD2-B-05** | Die thematische Nähe des Umrisses zu QG-006/WP-003+WP-004 (TD-05/TD-19, SG-C/D/E [OD-05 Kap. 15/16]) ist belegt, trägt aber **keine** Zuordnungsableitung: **RELATED — NOT DERIVED** | TRACEABILITY FINDING |

## 19. Explicit Non-Decisions

```text
HD-2: NOT DECIDED — dieses Dokument bereitet vor, es entscheidet nicht.
Keine Sprint-/WP-Zuordnung vorgenommen oder empfohlen.
Keine neue WP-Nummer, kein neuer Sprint, keine Planänderung.
HD-3: NOT DECIDED. F4-U2: NICHT GESCHLOSSEN.
OI-1: NICHT GESCHLOSSEN. Andere OI/UNKNOWNs: UNVERÄNDERT.
ADR-012: UNCHANGED — nicht verändert, nicht erneut genehmigt.
Keine neue Governance-Regel, kein neues Gate, keine Approval-Reihenfolge.
PARALLEL nicht in APPROVED/COMPLETED umgedeutet.
Coding: NOT AUTHORIZED. RL-05: NOT REACHED. QG-006: NOT STARTED.
Kein Push, kein PR, kein Merge.
```

## 20. Final Governance Finding

> ## **A) HD-2 DECISION READY — HUMAN DECISION REQUIRED**
>
> ## **HD-2 = OPEN / NOT DECIDED**

Die Entscheidungsgrundlage ist vollständig vorbereitet: Gegenstand exakt
bestimmt (Kap. 7), Ist-Zustand und Inventar erhoben (Kap. 8/9),
Abhängigkeiten und Voraussetzungen quellenbasiert geprüft (Kap. 10/11),
struktureller Entscheidungsraum dokumentiert (Kap. 13 — ohne Präferenz, da
NOT DETERMINABLE FROM CURRENT SOURCES), Traceability erhalten (Kap. 15/16).
Die Entscheidung selbst — APPROVED / ACCEPTED / REJECTED / DEFERRED, mit
Authority, Datum, Scope und ggf. Conditions — liegt ausschließlich beim
**Projekteigner**. Ohne diese Entscheidung bleibt HD-2 OPEN / NOT DECIDED.

---

## Revision History

| Revision | Datum | Änderung | Status |
|---|---|---|---|
| **R0** | 2026-08-11 | Ersterstellung der HD-2-Entscheidungsvorbereitung | **COMPLETED — HUMAN DECISION REQUIRED** |

---

**Ende HD4-HD2-DECISION-01-R0 — HD-2 Human Decision Preparation — JOCHEN X
Milestone 1.0 (2026-08-11) — Bezugs-Baseline
`MILESTONE-1.0-BASELINE = 8fcf42f1997dfcf6ff232e75fd33c37b933991c8`**
