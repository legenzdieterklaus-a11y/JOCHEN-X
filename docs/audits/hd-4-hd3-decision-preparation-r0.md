# JOCHEN X — Milestone 1.0
# HD4-HD3-DECISION-01-R0 — HD-3 Human Decision Preparation
## Einordnung der Policy-Diskontinuität F-4-05 in TD-19 / Behandlung von F4-U2

> **COMPLETED — HUMAN DECISION REQUIRED**
>
> Dieses Dokument bereitet die offene **HD-3**-Entscheidung (Einordnung der
> Policy-Diskontinuität F-4-05 in TD-19; Behandlung der UNKNOWN-Position
> F4-U2) quellenbasiert für die zuständige **Security-/Architektur-
> Governance** vor. Es trifft **keine** Entscheidung, schließt **keine**
> UNKNOWN-Position und erzeugt **keine** neue Governance-Regel. Ergebnis:
> **HD-3 = OPEN / NOT DECIDED — HUMAN DECISION REQUIRED.**
>
> **CODING = NOT AUTHORIZED** · **RL-05 = NOT REACHED** · **QG-006 = NOT STARTED**

---

## 1. Document Identity

| Feld | Wert |
|---|---|
| **Document ID** | **HD4-HD3-DECISION-01-R0** |
| Subject | HD-3 Decision Preparation — F4-U2 / Policy-Diskontinuität F-4-05 |
| Date | 2026-08-11 |
| Pfad | `docs/audits/hd-4-hd3-decision-preparation-r0.md` |
| Revision | R0 |
| **Bezugs-Baseline** | `MILESTONE-1.0-BASELINE = 8fcf42f1997dfcf6ff232e75fd33c37b933991c8` (historisch, unverändert) |
| HEAD bei Beginn | `5ffb8cfe567bb53504026b74b8b5b21b58092010` (HD4-HD2-HDR-01-R0) |
| Branch | `milestone-1.0-governance` |
| **Status** | **COMPLETED — HUMAN DECISION REQUIRED** |
| Artefakt-Typ | Decision Preparation (keine Entscheidung, kein Decision Record) |
| Rolle des Erstellers | Governance-/Architektur-Analyst — **nicht** entscheidungsbefugt |
| **AUTHORITY (HD-3)** | **Security-/Architektur-Governance** [SOURCE: HD-1 Kap. 19; F-4 Kap. 18; F-5 Kap. 20] |

## 2. Purpose

Erstellung einer belastbaren, quellenbasierten Entscheidungsgrundlage für die
zuständige Governance-Instanz zu HD-3. Strikte Trennung von Fakten, Regeln,
Abhängigkeiten, offenen Entscheidungsfragen und quellenbasiert ableitbarem
Optionsraum. **DECISION PREPARATION ≠ HUMAN DECISION.**

## 3. Scope

**In Scope:** Baseline-Gate; Source Gate (18 Quellgruppen); exakte
HD-3-Abgrenzung; Authority-Bestimmung; Ist-Zustand; Traceability
(F4-U2 → HD-3 → OI-2); Chronologie; Determination; Prerequisite-/Gate- und
Abhängigkeitsanalyse; Optionsraum; Entscheidungsfragen; Human-Decision-Suche;
Archivierung; Commit.

**Non-Goals (§17 des Auftrags, vollständig übernommen):** keine
HD-3-Entscheidung; keine Schließung von F4-U2/OI-2/anderen UNKNOWNs; keine
Änderung/Neugenehmigung von ADR-012, keine ADR-ID-Änderung; keine
HD-2-Entscheidung; keine Sprint-Plan-Änderung, keine WP-Zuordnung; keine
Coding-Autorisierung, kein RL-05, kein QG-006; keine neuen Regeln, Gates
oder Approval-Reihenfolgen; keine Umschreibung historischer Dokumente.

## 4. Baseline

| Prüfung | Ergebnis | Klasse |
|---|---|---|
| `git rev-parse HEAD` | `5ffb8cfe567bb53504026b74b8b5b21b58092010` — erwarteter Stand `5ffb8cf` (HD4-HD2-HDR-01-R0) | SOURCE FACT |
| Governance-Kette | `5ffb8cf` → `10de589` → `bc4ec44` → `3231e5b` → `70893fc` → `14354b8` → `8414384` → `b20858e` → `641947c` → `1efb61b` → `8fcf42f` — **exakt wie erwartet**; keine unerwarteten Commits seit HD4-A2-R0/HD4-HD2-HDR-01-R0 | SOURCE FACT |
| Historische Baseline | `8fcf42f1997dfcf6ff232e75fd33c37b933991c8` — unverändert; keine neue Baseline definiert | SOURCE FACT |
| Working Tree | vorbestehende Modifikationen (`CLAUDE.md`, `ROADMAP.md`, ADR-005/006/007, Architecture Book) und untracked Dokumente — **nur beobachtet, unangetastet** | SOURCE FACT |
| Staging vor Beginn | leer | SOURCE FACT |

**Status: PASS**

## 5. Source Gate

| # | Source | Verification |
|---|---|---|
| 1 | `docs/adr/012-plugin-security-policy-configuration.md` | SOURCE FACT — Kap. 9.3 (Policy-Diskontinuität), 13.2 KN-2, 13.3 KZ-2/KZ-5, 18 AC-16, 19 OI-2; **nicht verändert** |
| 2 | `docs/audits/hd-4-a2-hd3-follow-up-r0.md` (HD4-A2-R0) | SOURCE FACT — vollständige A-2-Determination; HD-3/F4-U2/OI-2 OPEN |
| 3 | `docs/audits/hd-4-approval-readiness-r0.md` (HD4-AP-01-R0) | SOURCE FACT — Kap. 9 (A-2 = PARALLEL, A2-1 … A2-6), 15 NF-2, 16 U-B |
| 4 | `docs/audits/hd-4-governance-decision-r0.md` | SOURCE FACT — Kap. 11 (A-2 Status), 13/14 |
| 5 | `docs/audits/hd-4-approval-decision-r0.md` (HD4-APP-01-R0) | SOURCE FACT — Explicit Non-Decision „Keine automatische Entscheidung über HD-3" |
| 6 | `docs/audits/hd-4-human-decision-record-r0.md` (HD4-HDR-01-R0) | SOURCE FACT — HD-3 OPEN durchgehend |
| 7 | `docs/audits/hd-4-a1-registration-r0.md` (HD4-A1-R0) | SOURCE FACT — Registrierung ohne HD-3-Bedingung; HD-3 unberührt |
| 8 | `docs/audits/hd-4-a3-hd2-follow-up-r0.md` (HD4-A3-R0) | SOURCE FACT — HD-3 „nicht Gegenstand", OPEN |
| 9 | `docs/audits/hd-4-hd2-decision-preparation-r0.md` | SOURCE FACT — Abgrenzung HD-2 ↔ HD-3 (RELATED — NOT IDENTICAL) |
| 10 | `docs/audits/hd-4-hd2-human-decision-record-r0.md` (HD4-HD2-HDR-01-R0) | SOURCE FACT — HD-2 = DEFERRED **ohne** HD-3-Aussage (Kap. 13 dort: HD-3 Boundary) |
| 11 | `docs/governance/hd-1-adr-rdr-decision.md` (HD-1) | SOURCE FACT — Kap. 16 (TD-19-Status, T-a/T-b/T-c), 16.x („bleiben für HD-3 … offen"), 19 (HD-3: F4-U2, **Security-/Architektur-Governance**), 20 (Schritt 3 parallel; Schritt 5 Sequenz) |
| 12 | `docs/governance/f-04-od05-td19-scope-assessment.md` (F-4) | SOURCE FACT — Kap. 10.2 (**F-4-05**), 10.3, 12.3, 15 S-9, 18 (F4-U2) |
| 13 | `docs/governance/f-05-od05-change-control-determination.md` (F-5) | SOURCE FACT — **PRE-HD-1/HISTORISCH**: Kap. 2 H-3, 15 (Nicht-Determinierbarkeit), 19, 20 (HD-3-Ausweisung) — RETAINED FOR TRACEABILITY |
| 14 | `docs/governance/od-05-governance-decision.md` | SOURCE FACT — Kap. 12.2 (TD-19 teilweise), 15 (QG-006: SG-C/SG-D/**SG-E** BLOCKING) |
| 15 | `docs/governance/naw-a-od05-change-surface-fixation.md` | SOURCE FACT — Kap. 8 (Instanz-Ersetzung als Kontext); kein HD-3-Vorkommen |
| 16 | `docs/governance/naw-b-g1-observable-state-contract-fixation.md` | GEPRÜFT — kein HD-3-/F4-U2-Vorkommen |
| 17 | Development Standard v1.1 | GEPRÜFT — §5/§13/§17 Anh. B; kein HD-3-Bezug |
| 18 | `docs/audits/jochen-x-master-engineering-plan-r0.md` §10.6 (**SEC-07**) | SOURCE FACT — dokumentierter **TD-19-Ursprungswortlaut** (von F-4/F-5 ausdrücklich referenziert): Instanz-Ersetzung + Trust-Ledger-Diskontinuität, Priorität HIGH (technisch), Korrektur berührt Baseline §8 → OD-05. **Eine Policy-Dimension ist dort nicht enthalten** (HD4-HD3-B-01) |

Keine externe Quelle. Keine Quelle NOT FOUND. **Status: PASS**

## 6. HD-3 Definition

**Quellenbelegte Definition (verifiziert gegen F-4, HD-1, HD4-A2-R0, F-5):**

| Element | Befund | Klasse |
|---|---|---|
| Gegenstand | **HD-3 = Entscheidungsposition „F4-U2 — Einordnung der Policy-Diskontinuität in TD-19"** [SOURCE: HD-1 Kap. 19] | SOURCE FACT |
| **F-4-05** (Sachverhalt) | Nach OD-05 Option B entstünde zwischen der in **LOAD_PLUGINS** konfigurierten und der in **FINALIZE** gesetzten `PluginSecurity`-Instanz zusätzlich eine **Policy-Diskontinuität** — eine Dimension, die am Baseline **nicht** existiert; klassifiziert als „Folge derselben Ursache, **kein neuer Technical Debt**" [SOURCE: F-4 Kap. 10.2] | SOURCE FACT |
| **F4-U2** (Frage) | „Ist die festgestellte Policy-Diskontinuität vom dokumentierten TD-19-Wortlaut erfasst, oder wäre sie als eigener Bestandteil zu führen?" [SOURCE: F-4 Kap. 18] | SOURCE FACT |
| TD-19 (Bezugsrahmen) | Dokumentierter Ursprungswortlaut SEC-07: **Instanz-Ersetzung** (SecurityBootstrapStage/FINALIZE ersetzt die registrierte Instanz) und **Trust-Ledger-Diskontinuität** (nachgelagerte Konsumenten erhalten einen anderen Ledger ohne die aufgezeichneten `IntegrityResult`-/`PermissionResult`-Einträge); Priorität HIGH; Korrektur berührt Baseline §8 → OD-05 [SOURCE: Master Engineering Plan R0 §10.6; deckungsgleich F-5 Kap. 15] | SOURCE FACT |
| Teilaspekte | **T-a** Instanz-Ersetzung · **T-b** Trust-Ledger-Diskontinuität · **T-c** Wirkungslosigkeit für Admission — sämtlich **OPEN** [SOURCE: HD-1 Kap. 16] | SOURCE FACT |

Die Arbeitsdefinition des Auftrags ist mit den Quellen **deckungsgleich**;
keine neue Definition wird erfunden.

## 7. Authority

```text
AUTHORITY = Security-/Architektur-Governance
```

| Prüfung | Befund |
|---|---|
| HD-1 Kap. 19 | HD-3-Autorität: „**Security-/Architektur-Governance**" | 
| F-4 Kap. 18 | F4-U2 zuständig: „Security-/Architektur-Governance" |
| F-5 Kap. 20 | HD-3: „Quellen tragen keine Determination" — Autorität: „**Security-/Architektur-Governance**" |
| Projekteigner? | Der Projekteigner ist quellenseitig die Autorität für HD-2 und die HD-4-Approval — für HD-3 benennen die Quellen die Governance-**Rolle**, nicht den Projekteigner |
| Personelle Ausgestaltung | In keiner geprüften Quelle geregelt, wer diese Rolle personell ausübt → **Detail: UNDETERMINED — HUMAN GOVERNANCE CLARIFICATION möglich** (HD4-HD3-B-02); die Rolle selbst ist eindeutig belegt |

## 8. Current Governance State

| Position | Status | Unverändert durch dieses Work Item |
|---|---|---|
| **HD-3** | **OPEN / NOT DECIDED** | ✓ |
| **F4-U2** | **OPEN / UNKNOWN** | ✓ |
| **OI-2** | **OPEN / UNKNOWN** | ✓ |
| **ADR-012** | **Accepted / Registered — UNCHANGED** | ✓ |
| **HD-2** | **DEFERRED / OPEN / NOT DECIDED** (HD4-HD2-HDR-01-R0) | ✓ |
| **HD-4** | **APPROVED** (HD4-APP-01-R0) | ✓ |
| **Coding** | **NOT AUTHORIZED** | ✓ |
| **RL-05** | **NOT REACHED** | ✓ |
| **QG-006** | **NOT STARTED** | ✓ |
| TD-19 | PARTIALLY IMPACTED / OPEN; T-a/T-b/T-c OPEN | ✓ |

## 9. F4-U2 Traceability

```text
F4-U2  →  HD-3  →  OI-2
```

| Element | Inhalt |
|---|---|
| Ursprung F4-U2 | **F-4 Kap. 18** — erzeugt als UNKNOWN / OPEN DECISION aus dem Befund F-4-05 (Kap. 10.2); F-4 „erfindet keine neue Position und verschmilzt keine bestehende" |
| Konkrete Fragestellung | Erfasst der dokumentierte TD-19-Wortlaut (SEC-07: Instanz-Ersetzung, Trust-Ledger) die **Policy**-Dimension — oder ist sie eigenständig zu führen? |
| Beziehung zu F-4-05 | F4-U2 ist die **Einordnungsfrage** zum Sachbefund F-4-05 |
| Rolle von HD-3 | HD-3 ist die von F-5 (Kap. 20, historisch) ausgewiesene und von HD-1 (Kap. 19, maßgeblich) fortgeführte **Entscheidungsposition** zu F4-U2 |
| Beziehung zu OI-2 | OI-2 ist die **Registerposition** im ADR-012-OI-Register (Kap. 19: „HD-3 / F4-U2 … OPEN — UNKNOWN"), fortgeführt in HD4-FU-R0 (F4-U2 → OI-2: TRACEABLE; HD-3 → OI-2: TRACEABLE / OPEN / UNKNOWN) |
| **Abgrenzung** | **F4-U2 (Sachfrage) ≠ HD-3 (Entscheidungsposition) ≠ OI-2 (Registerposition)** — verbunden, aber nicht identisch; keine Verschmelzung. Getrennt bleiben ferner: F4-U1 (OI-6, „teilweise"-Restumfang), F4-U3 (OI-5, FINALIZE-Konsument), NAW-A-U1/U2 (OI-3/OI-4) |

## 10. Historical Chronology

| Stufe | Ereignis | Einordnung |
|---|---|---|
| 1 | **SEC-07 / TD-19** (Master Engineering Plan R0 §10.6) | Ursprung des TD-19-Wortlauts (Instanz-Ersetzung, Trust-Ledger; HIGH; → OD-05) | 
| 2 | OD-05 = OPTION B (GDR-OD05-001) | FINAL; TD-19 „teilweise" adressiert (Kap. 12.2); QG-006-Kontext: SG-E (TD-19) BLOCKING (Kap. 15) |
| 3 | NAW-A / NAW-B | Umriss-/Kontraktfixierung; NAW-A Kap. 8 dokumentiert die Instanz-Ersetzung als Kontext |
| 4 | **F-4** | **HISTORISCH** — stellt **F-4-05** fest (Kap. 10.2), erzeugt **F4-U2** (Kap. 18); nicht umsetzungsblockierend (Kap. 12.3); kein produktiver Konsument (Kap. 9.4/10.3) |
| 5 | **F-5** | **HISTORISCH / PRE-HD-1 — RETAINED FOR TRACEABILITY**: F4-U2 nicht determinierbar (Kap. 15); weist **HD-3** als Human Decision aus (Kap. 20) — fortgeschrieben durch HD-1 |
| 6 | **HD-1** (2026-08-10) | **MASSGEBLICH**: HD-3 = F4-U2, OPEN, Security-/Architektur-Governance (Kap. 19); „unabhängig, parallel führbar" (Kap. 20 Schritt 3); T-a/T-b/T-c und die Einordnungsfrage „bleiben für HD-3 … offen" (Kap. 16.x) |
| 7 | HD-4 Draft → **ADR-012** | Kap. 9.3: „Dieser Entwurf löst die Policy-Diskontinuität NICHT und ordnet sie NICHT ein"; KN-2; AC-16 (UNKNOWN, abhängig von HD-3/F4-U2); OI-2 |
| 8 | HD4-AP-01-R0 | **A-2 = PARALLEL** (Klassifikation, keine Entscheidung); U-B HUMAN REVIEW |
| 9 | HD4-APP-01-R0 / HD4-A1-R0 | HD-4 APPROVED / ADR-012 registriert — je mit ausdrücklicher HD-3-Non-Decision |
| 10 | **HD4-A2-R0** | Determination: HD-3 OPEN, F4-U2 OPEN/UNKNOWN, HUMAN DECISION REQUIRED |
| 11 | HD4-A3-R0 / HD4-HD2-DECISION-01-R0 / **HD4-HD2-HDR-01-R0** | HD-2-Strang inkl. **HD-2 = DEFERRED** — ohne HD-3-Aussage |
| 12 | **HD4-HD3-DECISION-01-R0** | dieses Work Item |

## 11. Determination Findings

| # | Aussage | Klasse |
|---|---|---|
| D-1 | Gegenstand, Ursprung und Traceability von HD-3/F4-U2 sind vollständig quellenbelegt (Kap. 6/9) | **SOURCE FACT / DETERMINED** |
| D-2 | Autorität = Security-/Architektur-Governance (Rolle) | **SOURCE FACT / DETERMINED** |
| D-3 | Der dokumentierte TD-19-Wortlaut enthält **keine** Policy-Dimension | **SOURCE FACT** (SEC-07; F-5 Kap. 15) |
| D-4 | Ob die Policy-Diskontinuität vom TD-19-Wortlaut **erfasst** ist oder eigenständig zu führen wäre, ist aus den Quellen **nicht determinierbar** | **UNKNOWN — HUMAN DECISION REQUIRED** (F-5 Kap. 15; F-4 Kap. 10.2) |
| D-5 | HD-3 ist „unabhängig, parallel führbar" | **DETERMINED** (HD-1 Kap. 20 — Klassifikation, keine Entscheidung) |
| D-6 | Die Policy-Diskontinuität ist **nicht umsetzungsblockierend** und hat **derzeit keinen produktiven Konsumenten** | **SOURCE FACT** (F-4 Kap. 12.3, 9.4/10.3) |
| D-7 | AC-16 („Einordnung governance-seitig geklärt") ist als Verifikationskriterium **UNKNOWN — abhängig von HD-3/F4-U2** | **SOURCE FACT** (ADR-012 Kap. 18) |
| D-8 | Die materielle Einordnungsentscheidung selbst | **HUMAN DECISION REQUIRED** |

## 12. Prerequisite / Gate Analysis

| Frage | Ergebnis | Evidenz |
|---|---|---|
| **A** — HD-3 Voraussetzung für ADR-Approval? | **NEIN — negativ belegt** | HD-1 Kap. 20 (Genehmigung nur „nach HD-4"); HD4-A2-R0 NF-1; **Vollzugsbeleg**: Approval erteilt bei offenem HD-3, mit expliziter Trennung (HD4-APP-01-R0) |
| **B** — HD-3 Voraussetzung für ADR-Registrierung? | **NEIN — negativ belegt** | HD4-A1-R0 Kap. 7/10; HD4-A2-R0 NF-2; Registrierung vollzogen bei offenem HD-3 |
| **C** — HD-3 Voraussetzung für HD-2? | **UNDETERMINED / NICHT BELEGT** | keine Quelle verbindet HD-3 als HD-2-Voraussetzung; **Vollzugsbeleg**: die HD-2-Entscheidung (DEFERRED, HD4-HD2-HDR-01-R0) erging ohne HD-3-Bezug |
| **D** — HD-3 Voraussetzung für Coding? | **DIFFERENZIERT — beide Befunde dokumentiert** | *Positive Evidenz (Sequenzebene):* HD-1 Kap. 20 Schritt 5 — Umsetzungsautorisierung „erst nach 1–4 **und** RL-05"; Schritt 3 = HD-3. *Negative Evidenz (Bedingungskatalog):* IP §10.6 Nr. 7–9 und GC-06 nennen HD-3 **nicht** [HD4-AP-01-R0 Kap. 9.2 Achse 3]. *Technisch:* nicht umsetzungsblockierend (F-4 Kap. 12.3). Das Verhältnis dieser Aussagen ist quellenseitig nicht aufgelöst → Bestandteil der Entscheidungsfragen (Kap. 14 Nr. 5; HD4-HD3-B-03). **Keine neue Regel wird erzeugt** |
| **E** — HD-3 Voraussetzung für RL-05? | **UNDETERMINED / NICHT BELEGT** | RL-05 (IP §10.6 Nr. 9) setzt Nr. 7/8 voraus; kein HD-3-Bezug in den Quellen |
| **F** — HD-3 Voraussetzung für QG-006? | **NICHT BELEGT — aber RELATED** | keine ausdrückliche HD-3-Regel für QG-006; jedoch ist **SG-E (TD-19)** als **BLOCKING** Security Gate für QG-006 dokumentiert [OD-05 Kap. 15; F-5 „SG-E/TG-3 weiterhin offen"] — der HD-3-Gegenstand (TD-19-Einordnung) ist damit sachlich benachbart: **RELATED — NOT A DERIVED GATE** |

Aus dem Fehlen einer Regel wird keine positive Aussage konstruiert.

## 13. Dependency Analysis

| Abhängigkeit | Befund |
|---|---|
| **AC-16** (ADR-012 Kap. 18) | Verifikationskriterium der späteren Umsetzung; Status UNKNOWN, **abhängig von HD-3/F4-U2** — die HD-3-Entscheidung ist Voraussetzung der AC-16-**Verifizierbarkeit** (SOURCE FACT), nicht eines Approval- oder Coding-Gates |
| **TD-19-Fortschreibung** | F-4 Kap. 15 S-9 / Kap. 19 I-6: F4-U2 ist „bei der TD-19-Fortschreibung zu berücksichtigen" |
| **T-a / T-b / T-c** | bleiben unabhängig von HD-3 OPEN (HD-1 Kap. 16) — HD-3 entscheidet die **Einordnung** der Policy-Dimension, nicht die Behebung der Teilaspekte |
| **F4-U3** (OI-5) | verwandt (künftiger FINALIZE-Konsument würde die Diskontinuität wirksam machen), aber eigenständig — keine Verschmelzung |
| **HD-2 / OI-1** | getrennte Achse (DEFERRED); keine wechselseitige Bedingung belegt |

## 14. Decision Questions (für die Security-/Architektur-Governance)

1. **Einordnung:** Ist die Policy-Diskontinuität F-4-05 vom dokumentierten
   TD-19-Wortlaut (SEC-07: Instanz-Ersetzung, Trust-Ledger-Diskontinuität)
   **erfasst**, oder wird sie als **eigener Bestandteil / Präzisierung** des
   „teilweise"-Restumfangs von TD-19 geführt?
2. **F4-U2-Folge:** Wird F4-U2 durch diese Einordnung **geschlossen**, oder
   bleibt sie (ggf. präzisiert) **offen**?
3. **Artefakt-Folge:** Welche konkrete Governance-/Architektur-Folge soll
   entstehen (z. B. dokumentierte Einordnungsentscheidung; Auswirkung auf die
   spätere TD-19-Fortschreibung)? — Es wird keine Form vorgegeben.
4. **Bedingungen:** Gelten Bedingungen (z. B. Wiedervorlage bei Entstehen
   eines FINALIZE-Konsumenten, vgl. F4-U3)?
5. **Folgepositionen:** Welche Wirkung hat die Entscheidung auf **OI-2** und
   auf die Verifizierbarkeit von **AC-16** — und soll das Verhältnis der
   Sequenzaussage HD-1 Kap. 20 Schritt 5 zur IP-§10.6-Bedingungslage
   (Kap. 12 Frage D) geklärt werden?

Keine Antwort wird vorgegeben.

## 15. Option Space

**Quellenbasierter Entscheidungsraum — keine Empfehlungen:**

| Option | Gehalt | Quellenstütze |
|---|---|---|
| **O-1** | F-4-05 wird als vom bestehenden TD-19-Wortlaut **erfasst** eingeordnet (Subsumtion unter die dokumentierte Behandlung) | **SOURCE-SUPPORTED** — F-4 Kap. 10.2 benennt genau diese Möglichkeit („ob sie vom dokumentierten TD-19-Wortlaut … bereits erfasst ist") |
| **O-2** | F-4-05 wird als **eigener Bestandteil / Präzisierung** des „teilweise"-Restumfangs innerhalb TD-19 geführt | **SOURCE-SUPPORTED** — F-4 Kap. 10.2 („oder als Präzisierung des ‚teilweise‘-Restumfangs zu führen wäre"); F4-U1-Abgrenzung beachten (keine Verschmelzung) |
| **O-3** | HD-3 wird **vertagt** (DEFERRED), bis eine zusätzliche fachliche oder Governance-Grundlage vorliegt | **SOURCE-SUPPORTED** als zulässige Entscheidungskategorie (Decision-Gate-Kategorien; Präzedenz: HD-2 = DEFERRED, HD4-HD2-HDR-01-R0) |
| **O-4** | Andere Behandlung (z. B. Neuklassifikation außerhalb TD-19 als neuer Technical Debt) | **NOT SOURCE-SUPPORTED** — F-4 Kap. 10.2 klassifiziert F-4-05 ausdrücklich als „Folge derselben Ursache; **kein neuer Technical Debt**"; eine abweichende Behandlung wäre eine neue, hier nicht vorbereitete Governance-Setzung |

Der Raum wird nicht künstlich vervollständigt; O-1/O-2 sind die beiden von
F-4 selbst formulierten Alternativen der Einordnungsfrage.

## 16. Negative Findings

| # | Negative Finding |
|---|---|
| NF-1 | Keine automatische HD-3-Entscheidung existiert oder wird erzeugt |
| NF-2 | Keine Quelle autorisiert eine OI-2-Schließung |
| NF-3 | Keine Quelle autorisiert eine F4-U2-Schließung |
| NF-4 | Keine Coding-Freigabe ist mit HD-3 verbunden oder wird abgeleitet |
| NF-5 | Keine ADR-Änderung ist autorisiert (ADR-012 UNCHANGED) |
| NF-6 | Keine neue Approval-Reihenfolge, kein neues Gate, keine neue Governance-Regel |
| NF-7 | Repositoryweit existiert kein HD-3-Decision-Record und keine als Human Decision verifizierbare HD-3-Aussage |

## 17. Human Decision Search

Repositoryweite Suche (`docs/`, read-only) nach `HD-3`, `F4-U2`, `F-4-05`
sowie Entscheidungsbegriffen (HUMAN DECISION / APPROVED / ACCEPTED /
REJECTED / DEFERRED / Decision Record / Governance Decision / Approval):

| Befund | Ergebnis |
|---|---|
| `HD-3` | 13 Dateien — sämtlich bekannte Governance-Kette; durchgehend OPEN / NOT DECIDED |
| `F4-U2` | bekannte Kette (10 Dateien der A-2-Prüfung + Folgearchive); durchgehend OPEN / UNKNOWN |
| `F-4-05` | 3 Dateien (F-4; ADR-012; HD4-A2-R0) — kein Entscheidungsartefakt |
| Entscheidungsartefakte | Die einzigen Human-Decision-Records betreffen **HD-4** (HD4-APP-01-R0 — mit expliziter HD-3-Non-Decision) und **HD-2** (HD4-HD2-HDR-01-R0 — ohne HD-3-Aussage) |

```text
HUMAN DECISION = NOT FOUND
```

HD-3 wird daher **nicht** entschieden.

## 18. Explicit Non-Decisions

```text
HD-3 nicht entschieden. F4-U2 nicht geschlossen. OI-2 nicht geschlossen.
Keine UNKNOWN-Position geschlossen (F4-U1, F4-U3, NAW-A-U1/U2, OD-05 U-*).
ADR-012 nicht verändert, nicht erneut genehmigt; ADR-ID unverändert.
HD-2 nicht entschieden (bleibt DEFERRED per HD4-HD2-HDR-01-R0).
Sprint Plan unverändert; keine WP-Zuordnung.
Coding nicht autorisiert. RL-05 nicht erreicht. QG-006 nicht gestartet.
Keine neue Governance-Regel, kein neues Gate, keine Approval-Reihenfolge.
Keine historische Quelle als aktuelle Entscheidung dargestellt.
Kein Push, kein PR, kein Merge.
```

## 19. Repository Integrity

| Prüfung | Ergebnis |
|---|---|
| Bestehende Governance-/Audit-/ADR-Dateien | **UNVERÄNDERT** |
| Vorbestehende Working-Tree-Änderungen | **UNANGETASTET** (kein reset/checkout/restore/stash) |
| Neue Dateien | genau **eine**: dieses Archiv |
| Historische B-IDs | nur referenziert |

## 20. Observations

| ID | Beobachtung | Klasse |
|---|---|---|
| **HD4-HD3-B-01** | Der TD-19-Ursprungswortlaut wurde erstmals in der HD-3-Kette direkt an der Primärstelle verifiziert (Master Engineering Plan R0 §10.6, SEC-07): Instanz-Ersetzung + Trust-Ledger-Diskontinuität, Priorität HIGH, Korrektur → OD-05. Eine Policy-Dimension ist dort **nicht** enthalten — deckungsgleich mit der F-5-Kap.-15-Feststellung; die Einordnungsfrage bleibt dadurch unverändert offen | SOURCE FACT / OBSERVATION |
| **HD4-HD3-B-02** | Die HD-3-Autorität ist als **Rolle** („Security-/Architektur-Governance") dreifach belegt (HD-1 Kap. 19; F-4 Kap. 18; F-5 Kap. 20); ihre **personelle Ausgestaltung** ist in keiner geprüften Quelle geregelt — ggf. vorab durch die Human Governance zu klären | OBSERVATION |
| **HD4-HD3-B-03** | Auf der Coding-Achse bestehen drei nebeneinanderstehende Quellenaussagen (HD-1 Kap. 20 Schritt 5 Sequenz „nach 1–4"; IP §10.6 ohne HD-3-Nennung; F-4 Kap. 12.3 „nicht umsetzungsblockierend"), deren Verhältnis quellenseitig nicht aufgelöst ist — dokumentiert als offene Klärungsfrage (Kap. 14 Nr. 5), **nicht** aufgelöst und **nicht** in eine Regel überführt | TRACEABILITY FINDING |
| **HD4-HD3-B-04** | SG-E (TD-19) ist als BLOCKING Security Gate für QG-006 dokumentiert (OD-05 Kap. 15); der HD-3-Gegenstand ist damit sachlich benachbart, ohne dass eine Quelle HD-3 als QG-006-Voraussetzung bestimmt (RELATED — NOT A DERIVED GATE) | TRACEABILITY FINDING |

## 21. Final Governance Finding

> ## **HD-3 = OPEN / NOT DECIDED — HUMAN DECISION REQUIRED**

**Die Entscheidungsgrundlage ist vorbereitet; die HD-3-Entscheidung selbst
wurde nicht getroffen.** Gegenstand, Ursprung, Autorität (Rolle),
Traceability, Abhängigkeiten und der quellenbasierte Optionsraum
(O-1/O-2/O-3; O-4 NOT SOURCE-SUPPORTED) liegen vor. Die Entscheidung —
APPROVED / ACCEPTED / REJECTED / DEFERRED, mit Authority, Datum, Scope und
ggf. Conditions — obliegt ausschließlich der **Security-/Architektur-
Governance**. Bis dahin bleiben HD-3, F4-U2 und OI-2 offen.

## 22. Governance Gate

| Gate | Status |
|---|---|
| **HD-3** | **OPEN / NOT DECIDED — HUMAN DECISION REQUIRED** |
| **F4-U2** | **OPEN / UNKNOWN** |
| **OI-2** | **OPEN / UNKNOWN** |
| **HD-2** | **DEFERRED / OPEN / NOT DECIDED** (unverändert) |
| **ADR-012** | **UNCHANGED — Accepted / Registered** |
| **HD-4** | **APPROVED** (unverändert) |
| **CODING** | **NOT AUTHORIZED** |
| **RL-05** | **NOT REACHED** |
| **QG-006** | **NOT STARTED** |
| **Push / PR / Merge** | **NOT PERFORMED** |

## 23. Revision History

| Revision | Datum | Änderung | Status |
|---|---|---|---|
| **R0** | 2026-08-11 | Ersterstellung der HD-3-Entscheidungsvorbereitung (F4-U2 / F-4-05) | **COMPLETED — HUMAN DECISION REQUIRED** |

---

**Ende HD4-HD3-DECISION-01-R0 — HD-3 Human Decision Preparation — JOCHEN X
Milestone 1.0 (2026-08-11) — Bezugs-Baseline
`MILESTONE-1.0-BASELINE = 8fcf42f1997dfcf6ff232e75fd33c37b933991c8`**
