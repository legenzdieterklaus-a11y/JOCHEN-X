# JOCHEN X — Milestone 1.0
# HD4-FU-C-DEC-01-R0 — AC-16 Verification Authorization — Decision Preparation
## Formale Verifikationsautorität und zulässiger späterer Vollzug (Q6/Q8)

> **COMPLETED — AUTHORIZATION DECISION PREPARATION**
>
> Diese PREP-Welle bereitet die Human Decision für den späteren **FU-C-EXEC**
> (formaler AC-16-Verifikationsakt) vor. Sie entscheidet nichts, autorisiert
> nichts und führt keinen Statuswechsel aus. Ergebnis: Die materielle
> Erfüllung ist belegt; die **Verifikationsrolle und der
> Statusübergang UNKNOWN → VERIFIED sind quellenseitig ungeregelt**
> (Governance-Lücke) — drei zulässige Optionen (A/B/C) sind vorbereitet,
> mit Architektur-Empfehlung **OPTION C**.
>
> **CODING = NOT AUTHORIZED** · **RL-05 = NOT REACHED** · **QG-006 = NOT STARTED**

---

## 1. Metadata

| Feld | Wert |
|---|---|
| **Document ID** | **HD4-FU-C-DEC-01-R0** |
| Mode / Wave | GOVERNANCE · **PREP** |
| Subject | AC-16 — formale Verifikationsautorität und zulässiger späterer Vollzug |
| Date | 2026-08-11 |
| Pfad | `docs/audits/hd-4-fu-c-dec-01-r0.md` |
| Revision | R0 |
| **Bezugs-Baseline** | `MILESTONE-1.0-BASELINE = 8fcf42f1997dfcf6ff232e75fd33c37b933991c8` |
| HEAD bei Beginn | `c8979def54c1d671aa9810a82fcbbab0494346ef` (HD4-FU-C-01-R0) |
| Branch | `milestone-1.0-governance` |
| **Status** | **COMPLETED — AUTHORIZATION DECISION PREPARATION** |
| Grundsatz | **PREP ≠ DEC ≠ EXEC** — diese Welle trifft keine Entscheidung |

## 2. Baseline

| Prüfung | Ergebnis |
|---|---|
| `git rev-parse HEAD` | `c8979de` — erwarteter Stand (HD4-FU-C-01-R0 durchgeführt und archiviert) |
| Governance-Kette | `c8979de → 3ea4d8f → f9ca01f → 5ffb8cf → 10de589 → bc4ec44 → 3231e5b → 70893fc → 14354b8 → 8414384 → b20858e → 641947c → 1efb61b → 8fcf42f` — vollständig, keine Abweichung |
| Working Tree / Staging | 87 vorbestehende Einträge unangetastet; Staging leer |
| Historische Kette | nicht neu definiert |

**Status: PASS**

## 3. Source Gate

| # | Quelle | Relevante Stelle | Aussage | Bedeutung für AC-16 |
|---|---|---|---|---|
| 1 | `docs/adr/012-plugin-security-policy-configuration.md` | Kap. 18 (AC-16: U/G, „UNKNOWN — abhängig von HD-3/F4-U2"); Kap. 9.3; Kap. 19 (OI-2); Banner | Definition, formaler Ist-Status, Registerbezüge | Prüfgegenstand |
| 2 | `docs/audits/hd-4-hd3-human-decision-record-r0.md` (HDR-01) | Kap. 5–11; Conditions | HD-3 = APPROVED / O-2; Nachführung separat zu autorisieren | **Evidenzquelle** der materiellen Erfüllung |
| 3 | `docs/audits/hd4-fu-c-ac16-verification-r0.md` (FU-C-01-R0) | Q1–Q10; Kap. 10/11 | MATERIALLY VERIFIED — FORMALLY UNKNOWN; Rolle/Prozess ungeregelt (HD4-FU-C-B-02) | unmittelbarer Vorbefund — nicht überschrieben |
| 4 | `docs/governance/hd-1-adr-rdr-decision.md` | Kap. 19/20 | HD-3-Autorität = Security-/Architektur-Governance; HD-2/HD-4-Autorität = Projekteigner | Kandidatenrollen (Kap. 8) |
| 5 | F-4 / F-5 | Kap. 10.2/12.3/18 bzw. 15/20 | F-4-05/F4-U2-Ursprung; historische Nicht-Determinierbarkeit | Traceability |
| 6 | Development Standard v1.1 | §5, §13, **§17 Anh. B** | Approval States nur für ADR/Spec/Sprint/Release — **keine AC-Statusregel**, keine Verifikationsrollenregel | Negative Evidenz (Q3/Q5) |
| 7 | Repositoryweite Suchen | `AC-16` → 7 Dateien · `F4-U2`/`HD-3` → bekannte Kette · `OI-2` → 12 · `TD-19` → 24 · „VERIFIED/UNKNOWN/Verifikation" | keine Regel zur Verifikationsrolle oder Statusnachführung gefunden | bestätigt die Lücke |

Keine externe Quelle. Keine Aussage aus fehlender Evidenz konstruiert. **PASS**

## 4. AC-16 Ausgangslage

| Position | Stand |
|---|---|
| HD-3 | **APPROVED / O-2** (HDR-01, 2026-08-11) |
| F4-U2 | Sachfrage DECIDED; Register nicht automatisch nachgeführt |
| OI-2 | zugrunde liegende Frage entschieden; historischer Registereintrag unverändert |
| **AC-16** | **MATERIALLY VERIFIED — FORMALLY UNKNOWN** (FU-C-01-R0) |
| ADR-012 | Accepted / Registered — UNCHANGED |

## 5. Evidenz

Für den formalen Verifikationsakt ausreichende, bereits vorhandene Evidenz:

1. **HD4-HD3-HDR-01-R0** — die autorisierte Human Decision (Authority, Datum,
   Scope, wörtlicher Decision Detail O-2) = **Primärevidenz**.
2. **HD4-FU-C-01-R0** — unabhängige Verifikationsprüfung (Q1–Q4: materiell
   erfüllt; Scope-Deckung verifiziert) = Prüfevidenz.
3. Traceability-Kette F-4-05 → F4-U2 → HD-3 → OI-2 → AC-16 — lückenlos.

Weitere Evidenz ist **nicht** erforderlich (Q2).

## 6. Q1–Q10

| Frage | Antwort |
|---|---|
| **Q1** — Erfüllte materielle Voraussetzung? | Die governance-seitige Klärung der Einordnung der Policy-Diskontinuität: HD-3 = APPROVED / O-2 beantwortet exakt die AC-16-Bedingung („abhängig von HD-3/F4-U2") |
| **Q2** — Ausreichende Evidenz? | **HDR-01** (Primärevidenz) + FU-C-01-R0 (Prüfevidenz) — vollständig (Kap. 5) |
| **Q3** — Explizite Regel zur Verifikationsrolle? | **NEIN** — weder Dev-Standard v1.1 (§17 Anh. B kennt nur ADR/Spec/Sprint/Release-States) noch ADR-012 noch eine Governance-Quelle benennt eine Rolle für formale AC-Verifikation (Negative Finding; deckungsgleich HD4-FU-C-B-02) |
| **Q4** — Rolle eindeutig bestimmbar? | **NEIN — UNKNOWN / HUMAN REVIEW REQUIRED.** Zwei quellengestützte Kandidaten existieren, ohne dass eine Quelle sie bestimmt: (a) **Projekteigner** (Approval-Autorität des ADR und des Milestones), (b) **Security-/Architektur-Governance** (Autorität der zugrunde liegenden HD-3-Entscheidung). Die Zuweisung ist Gegenstand der DEC |
| **Q5** — Regel für UNKNOWN → VERIFIED? | **NEIN** |
| **Q6** — Governance-Lücke | **EXAKT DOKUMENTIERT:** Es existiert weder eine Statusübergangsregel für Acceptance Criteria noch ein Verfahren für eine vorgezogene Einzelverifikation; die AC-Systematik des ADR ordnet Verifikation der späteren Verifikations-/Umsetzungsarbeit zu. Die Lücke wird hier festgestellt — **nicht durch eine erfundene Regel gefüllt** |
| **Q7** — Minimal zu ändernde Datei(en) bei EXEC? | Variantenabhängig: **minimal genau eine Datei** — entweder ein **neues Verifikations-Record** unter `docs/audits/` (ADR-012 unberührt) **oder** die AC-16-Statuszeile in `docs/adr/012-…md` Kap. 18 (dann ADR-Berührung). Keine weitere Datei ist erforderlich |
| **Q8** — Betroffene Status-/Registereinträge? | ausschließlich: AC-16-Statusfeld (ADR-012 Kap. 18) bzw. dessen dokumentierte Überholung per Record; **optional** in derselben Autorisierung: Banner-Vermerk (FU-A-Gegenstand — separat) |
| **Q9** — Ausdrücklich NICHT erforderlich? | Änderungen an Kap. 9.3, Kap. 19 (OI-2), F4-U2-Registerstellen, TD-19, den übrigen AC-01 … AC-15, dem normativen ADR-Inhalt, HD-2, Sprint Plan, IP, historischen Archiven |
| **Q10** — Automatische Wirkung des formalen Vollzugs? | **HD-2:** KEINE (bleibt DEFERRED/OPEN) · **HD-3:** KEINE (unverändert APPROVED) · **ADR-012:** nur die ggf. autorisierte AC-16-Zeile — keine normative Wirkung · **OI-2:** KEINE (getrennte Registerposition) · **TD-19:** KEINE (bleibt PARTIALLY IMPACTED/OPEN; T-a/b/c offen) · **Sprint/WP:** KEINE · **Coding:** KEINE (IP §10.6 nennt AC-16 nicht) · **RL-05:** KEINE · **QG-006:** KEINE (SG-E bleibt BLOCKING) |

## 7. Autorisierungslücke

```text
FEHLEND (Governance-Lücke, quellenbelegt):
1. Regel/Rolle für den formalen AC-Verifikationsakt        → Q3/Q4
2. Statusübergangsregel UNKNOWN → VERIFIED für ACs          → Q5/Q6
3. Autorisierung einer ADR-012-Berührung (HDR-01-Conditions) → Q7/Q8
```

Alle drei Lücken sind ausschließlich durch eine **Human Decision (DEC)**
schließbar — nicht durch PREP, nicht durch Interpretation.

## 8. Rollenbestimmung

| Kandidat | Quellenstütze | Gegenargument |
|---|---|---|
| **Projekteigner** | Approval-Autorität für ADR-012 (HD4-APP-01-R0) und den Milestone; Autorität für Registerdispositionen im bisherigen Verfahren | AC-16 prüft eine Security-/Architektur-Governance-Entscheidung |
| **Security-/Architektur-Governance** | Autorität der zugrunde liegenden HD-3-Entscheidung (HD-1 Kap. 19) | Verifikation ≠ Entscheidung; die Entscheidung ist bereits getroffen |
| **Reguläre Verifikationsphase** (kein vorgezogener Akt) | AC-Systematik des ADR-012 Kap. 18: alle ACs werden in der späteren Verifikationsarbeit geprüft (HD4-FU-C-B-03) | formale UNKNOWN-Markierung bleibt bis dahin bestehen |

**AUTHORITY = UNDETERMINED — HUMAN DECISION REQUIRED** (Bestandteil der DEC).

## 9. Minimale spätere Change Surface (EXEC)

| Variante | Dateien | Umfang |
|---|---|---|
| Record-Variante | genau 1 neue Datei `docs/audits/` (Verifikations-Record) | ADR-012 unberührt |
| ADR-Variante | genau 1 Datei: `docs/adr/012-…md`, ausschließlich AC-16-Statuszeile Kap. 18 (+ ggf. minimaler Vermerk) | mechanische Nachführung, kein normativer Inhalt |
| Phasen-Variante | **0 Dateien jetzt** — Verifikation erfolgt in der regulären Verifikationsphase gegen HDR-01 | keine vorgezogene Änderung |

## 10. Optionen A/B/C

| | **OPTION A** | **OPTION B** | **OPTION C** |
|---|---|---|---|
| Was würde entschieden? | Benennung der Verifikationsrolle **+** Autorisierung des formalen Verifikationsakts **+** minimale AC-16-Statusnachführung in ADR-012 Kap. 18 | Benennung der Rolle **+** formaler Verifikationsakt als **separates Record** (Evidenz HDR-01); ADR-Statusnachführung bleibt weiterer separater Schritt | **DEFERRED**: kein vorgezogener Einzelakt; AC-16 wird in der **regulären Verifikationsphase** zusammen mit AC-01 … AC-15 verifiziert; HDR-01 wird als designierte Evidenz festgehalten |
| Später betroffene Dateien | `docs/adr/012-…md` (Kap. 18) + Verifikationsnachweis | 1 neues Audit-Record; ADR-012 unverändert | keine jetzt; Verifikationsartefakte der späteren Phase |
| Was würde NICHT verändert? | Kap. 9.3/19, OI-2, F4-U2, TD-19, HD-2, Coding-Gates | zusätzlich: ADR-012 vollständig | alles — kein Artefakt jetzt |
| Vorteil | vollständige formale Schließung in einem Schritt; Register und Realität deckungsgleich | minimale Change Surface am ADR; folgt dem etablierten Record-Präzedenz (OI-8/HDR) | **Null Change Surface jetzt**; konsistent mit der AC-Systematik (keine Prozess-Asymmetrie durch Einzelverifikation); keine zusätzliche Prozessschleife |
| Risiko / Nachteil | ADR-Datei wird berührt (größte Change Surface); erfordert zusätzlich Klärung der Übergangsregel (Q5) | formaler ADR-Eintrag bleibt historisch UNKNOWN; zwei Artefaktebenen | formale UNKNOWN-Markierung bleibt bis zur Verifikationsphase bestehen (dokumentiert, evidenzbelegt — keine Scheinlücke) |
| Notwendige Human Decision | Rolle + Akt + ADR-Nachführung (3 Elemente) | Rolle + Akt (2 Elemente) | Festlegung „Verifikation in regulärer Phase, Evidenz = HDR-01" (1 Element) |

Alle drei Optionen sind durch die bestehende Governance-Struktur zulässig
(A/B folgen dem Record-/Vermerks-Präzedenz; C folgt der dokumentierten
AC-Systematik). Keine erfundene Regel.

## 11. Architektur-Empfehlung

> ## **RECOMMENDATION: OPTION C**

Begründung (Architektursicht JOCHEN X — ausdrücklich **EMPFEHLUNG, keine
Entscheidung**):

1. **Minimale Change Surface:** null Dateien jetzt; keine ADR-Berührung.
2. **Governance-Konsistenz:** AC-16 wird wie alle übrigen ACs in der
   regulären Verifikationsphase geprüft — keine Sonderprozess-Asymmetrie
   (HD4-FU-C-B-03); die in Q3–Q6 festgestellten Lücken (Rolle,
   Übergangsregel) müssen für die Verifikationsphase ohnehin gelöst werden
   und werden dann **einmal** statt zweimal gelöst.
3. **Traceability:** bereits heute lückenlos (HDR-01 + FU-C-01-R0); die
   DEC-Festlegung „Evidenz = HDR-01" macht den späteren Vollzug rein
   **mechanisch**.
4. **Keine Scheinschließung:** der formale Status bleibt ehrlich UNKNOWN,
   bis der reguläre Verifikationsakt ihn belegt.
5. **Keine unnötige Prozessschleife:** A und B erzeugen je einen
   vorgezogenen Governance-Zyklus für ein Kriterium, das keinerlei
   blockierende Wirkung hat (Q10: keine Achse betroffen; IP §10.6 nennt
   AC-16 nicht).
6. **Keine automatische Downstream-Wirkung:** C verändert nichts und kann
   nichts implizit autorisieren.

Zweitpräferenz, falls der Projekteigner eine frühere formale Schließung
wünscht: **OPTION B** (Record-Variante, ADR unberührt).

## 12. Explicit Non-Decisions

```text
Kein AC-16-Statuswechsel (UNKNOWN → VERIFIED NICHT durchgeführt).
Keine Verifikationsrolle festgelegt (AUTHORITY = UNDETERMINED — DEC).
OI-2 / F4-U2 / TD-19 / ADR-012: unverändert.
HD-2 nicht entschieden. HD-3 nicht verändert.
Kein Sprint/WP. Kein Coding. Kein RL-05. Kein QG-006.
Keine neue Governance-Regel, kein neues Gate.
Keine Human Decision simuliert oder aus der Empfehlung abgeleitet.
Keine historischen Archive überschrieben.
```

## 13. Downstream Impact Boundary

```text
PREP ≠ DEC ≠ EXEC
APPROVAL ≠ STATUSNACHFÜHRUNG ≠ CODING AUTHORIZATION
```

Der spätere formale AC-16-Vollzug hat — gleich welcher Option — **keine**
automatische Wirkung auf HD-2, HD-3, ADR-012 (über die ggf. autorisierte
Statuszeile hinaus), OI-2, TD-19, Sprint/WP, Coding, RL-05 oder QG-006
(Q10). Coding bleibt NOT AUTHORIZED, RL-05 NOT REACHED, QG-006 NOT STARTED.

## 14. Follow-up für DEC

Die DEC (Human Decision des Projekteigners, ggf. unter Einbindung der
Security-/Architektur-Governance) muss beantworten:

1. **Option A, B oder C?**
2. Bei A/B: **Wer** ist die Verifikationsrolle (Kap. 8)?
3. Bei A: Autorisierung der ADR-012-Kap.-18-Nachführung (Form des Vermerks)?
4. Bei C: Bestätigung „AC-16-Verifikation in der regulären
   Verifikationsphase; designierte Evidenz = HD4-HD3-HDR-01-R0".
5. Optional: Verhältnis zu FU-A/FU-B (Traceability-Vermerk) — getrennt
   halten oder bündeln? (Empfehlung: getrennt — Vertical Slice.)

Format: expliziter HUMAN-DECISION-Block (Authority, Date, Decision, Scope,
Decision Detail, Conditions) — analog HD-2-/HD-3-Verfahren.

## 15. Follow-up für EXEC

Nach der DEC ist der EXEC rein mechanisch:

| DEC-Ergebnis | EXEC-Inhalt |
|---|---|
| Option A | AC-16-Zeile in ADR-012 Kap. 18 nachführen + Verifikationsnachweis; genau die autorisierten Dateien committen |
| Option B | ein Verifikations-Record unter `docs/audits/` erstellen; ADR-012 unberührt |
| Option C | **kein EXEC jetzt** — Aufnahme in die reguläre Verifikationsphase; dort AC-16 gegen HDR-01 verifizieren |

Jeder EXEC benötigt eigenes Baseline-/Source-/Preflight-Gate.

## 16. Preflight

| Check | Ergebnis |
|---|---|
| Baseline verifiziert (`c8979de`) | PASS |
| Source Gate vollständig, keine externe Quelle | PASS |
| Keine Entscheidung getroffen, keine Autorisierung erzeugt | PASS |
| Kein Statuswechsel (AC-16 unverändert FORMALLY UNKNOWN) | PASS |
| OI-2/F4-U2/TD-19/ADR-012/HD-2/HD-3 unverändert | PASS |
| Keine UNKNOWN geschlossen; keine neue Regel; kein Gate | PASS |
| Coding/RL-05/QG-006 unberührt | PASS |
| Beobachtungs-Namensraum eingehalten (keine neuen Beobachtungen erforderlich; Referenzen auf HD4-FU-C-B-02/B-03) | PASS |
| Genau eine neue Datei (dieses PREP-Archiv); keine bestehende Datei verändert | PASS |
| Nur dieses Archiv wird gestaged; kein Push/PR/Merge | PASS |

---

**Ende HD4-FU-C-DEC-01-R0 — AC-16 Verification Authorization — Decision
Preparation — JOCHEN X Milestone 1.0 (2026-08-11) — Bezugs-Baseline
`MILESTONE-1.0-BASELINE = 8fcf42f1997dfcf6ff232e75fd33c37b933991c8`**
