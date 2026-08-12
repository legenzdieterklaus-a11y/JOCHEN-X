# JOCHEN X — Milestone 1.0
# JX-DEV-SPR01-RL05-DEC-01-R0 — SPR-01-Abschlusswirkung / RL-05 — Decision Preparation
## Nach F-SPR01R-01 (GI-07/08/09 Baseline Deviation)

> **COMPLETED — DECISION PREPARATION · HUMAN DECISION REQUIRED**
>
> Quellenbefund: Die protokollierte §3.8-Bestätigung liegt vor (EV-D01,
> 29/32 PASS, RB-1.0 258/258), aber (1) die SPR-01-Exit-Bedingung
> „Aufhebung des §4.2-Vorbehalts" ist für GI-07/08/09 nicht erfüllt und
> (2) **IP §10.6 Ausschlussgrund Nr. 8** („Baseline-Abweichung festgestellt
> und nicht entschieden") ist durch F-SPR01R-01 **aktiv**. RL-05 ist damit
> **erst nach Governance-Klärung erreichbar (Ergebnis B)**. Für
> F-SPR01R-01 ist eine **separate Human Decision erforderlich**. PREP
> entscheidet nichts.
>
> **CODING = NOT AUTHORIZED** · **RL-05 = NOT REACHED** · **QG-006 = NOT STARTED**

---

## 0. Document Identity

| Feld | Wert |
|---|---|
| **Document ID** | **JX-DEV-SPR01-RL05-DEC-01-R0** |
| Mode / Wave | GOVERNANCE · **PREP** |
| Subject | SPR-01-Abschlusswirkung und RL-05-Eintritt nach F-SPR01R-01 |
| Date | 2026-08-12 |
| Pfad | `docs/audits/jx-dev-spr01-rl05-decision-prep-r0.md` |
| **Bezugs-Baseline** | `MILESTONE-1.0-BASELINE = 8fcf42f` (per GDR-003) |
| HEAD bei Beginn | `2255a5e0992f6937a21899fa6728e8455985d484` (SPR-01-Re-Confirmation) |
| **Status** | **COMPLETED — DECISION PREPARATION · HUMAN DECISION REQUIRED** |

## 1. Baseline

HEAD = `2255a5e` — erwarteter Stand (JX-DEV-SLICE-SPR01-BUILD-01-R0
committet). Kette bis `8fcf42f` vollständig. Working Tree: 87 vorbestehende
Einträge unangetastet; Staging leer. **PASS.**

## 2. Source Gate

Geprüft (read-only, keine externe Quelle): EV-D01
(`jx-dev-spr01-baseline-confirmation-r0.md`) · IP §3.8, §4.2 (Regel 5),
§7.6, **§10.5 (RL-04/RL-05-Definition)**, **§10.6 (Bedingungen 1–9 +
Ausschlusskatalog)** · Sprint Plan 1.0 R0 (SPR-01 Exit Criteria; Kap. 6
Coding Gate; OP-1/OP-2) · ADW-SPR-1.0-001 · GDR-002 · GDR-003 (Snapshot
`8fcf42f`) · SPR-01-Erstfeststellung (untracked, FINAL 2026-08-09) ·
ADR-005/006/007 (Welt A committed „Open" / Welt B Working Tree „APPROVED")
· ADR-012 Kap. 1.1 (Register-Divergenz-Dokumentation) · GDR-OD01-001-Bezug
(getrennte Disposition) · Dev Standard §17 Anh. B (Sprint-States
Planned→In Progress→Review→Done). Repositoryweite Suchen nach SPR-01,
RL-05, GI-07/08/09, F-SPR01R-01, BASELINE DEVIATION durchgeführt —
F-SPR01R-01 existiert ausschließlich in EV-D01 (kein separates Archiv).
**PASS.**

## 3. SPR-01-Befund (aus EV-D01, nicht neu bewertet)

29/32 PASS (sämtliche 20 technischen Positionen BI/API/BP/PL grün; GI: 9
PASS) · **3 DEVIATION (GI-07/08/09)** · RB-1.0 erstmals ausgeführt:
**258 passed / 0 failed / 0 Regressionen** · EV-D01 protokolliert ·
§4.2-Vorbehalt für GI-07/08/09 ausdrücklich **nicht** aufgehoben ·
„Übergang für den betroffenen Umfang NICHT freigegeben".

## 4. F-SPR01R-01

Committed Stand (Welt A) führt ADR-005/006/007 mit `Status: Open`; IP §3.7
erwartet „APPROVED — unverändert"; Working Tree (Welt B, vorbestehend)
führt APPROVED. **Vorbekannt und registriert**: ADR-012 Kap. 1.1
(Zusatzbefund Register-Lage), Disposition per **GDR-OD01-001 getrennt und
noch nicht erfolgt**. Kein separates F-SPR01R-01-Archiv; die Feststellung
lebt in EV-D01 Kap. 8.

## 5. GI-07/08/09

Reine **Register-/Status-Divergenz** — kein technischer Widerspruch: die
von ADR-005/006/007 beschriebenen Mechanismen (Integrity, Permission,
Dependency Resolution) sind implementiert und durch PL-02/03/04 + 258/258
grüne Tests funktional belegt. Die Abweichung betrifft ausschließlich die
dokumentarische Statusführung der drei ADRs.

## 6. IP §4.2 (Regel 5)

„Die Delta Analysis ist vorläufig, bis die Baseline-Bestätigung gemäß
Kapitel 3 protokolliert vorliegt." — Die Bestätigung liegt protokolliert
vor (EV-D01); für die drei abweichenden GI-Positionen wurde der Vorbehalt
ausdrücklich aufrechterhalten. **Teilerfüllung — SOURCE FACT.**

## 7. IP §7.6

Tatbestand „Baseline-Abweichung": Unterbrechung → Dokumentation gegen
§3.8 → Vorlage; **Entscheidungsinstanz: „Governance-Entscheidung in Form
eines ADR oder RDR (Baseline Change Control)"**; Rückkehr „nach Genehmigung
… die Baseline bleibt bis dahin maßgeblich". **Regel 4:** „Nicht betroffene
Arbeit läuft weiter. Eine Eskalation unterbricht … den betroffenen Umfang."
— Beides SOURCE FACTS; ihr Verhältnis zur SPR-01-Abschlussfrage ist nicht
explizit geregelt (Kap. 11).

## 8. IP §10.6 / Bedingung 8

**Bedingung 8:** „Die Baseline-Bestätigung gemäß Kapitel 3.8 ist
protokolliert (Phase A abgeschlossen)" — zwei Komponenten:

| Komponente | Befund |
|---|---|
| (a) Bestätigung protokolliert | **ERFÜLLT** — EV-D01 liegt vor (SOURCE FACT) |
| (b) „Phase A abgeschlossen" | **UNDETERMINED** — hängt an der noch ausstehenden Abschlussfeststellung für SPR-01 (Kap. 11); keine Quelle erklärt SPR-01 bei teilaufgehobenem Vorbehalt automatisch für abgeschlossen |

**Ausschlusskatalog:** **Ausschlussgrund Nr. 8** — „Eine Baseline- oder
Architekturabweichung ist festgestellt und nicht entschieden" — ist durch
F-SPR01R-01 **AKTIV** [SOURCE: IP §10.6 „Ausschlüsse"; „Ein einzelner
Ausschlussgrund genügt"]. **Damit ist die Umsetzung unabhängig vom Status
der Bedingung 8 blockiert, bis die Abweichung entschieden ist.**

> Gesamtergebnis Bedingung 8: **TEILWEISE ERFÜLLT** ((a) ja, (b) offen) —
> und selbst bei Vollerfüllung bliebe Ausschlussgrund 8 wirksam.

## 9. RL-05-Prerequisites (IP §10.5)

RL-05 „Authorized for Implementation": Eintritt = genehmigte Sprintplanung
**+** protokollierte §3.8-Bestätigung; Kriterien = RL-04 vollständig
**+ Abschluss der Phase A** (Kap. 7.3); Nachweise = EV-D01,
Sprintplanungsdokument, **Freigabe gemäß 10.6**.

| Prerequisite | Stand |
|---|---|
| RL-04 | erreicht (dokumentiert; OP-1-Kontext) |
| Genehmigte Sprintplanung | ADW-SPR-1.0-001 (als Planungsgrundlage) — Bedingung-7-Auslegung bzgl. Umriss-Abdeckung weiterhin UNDETERMINED (HD4-HD2-B-03), hier nicht entscheidungsrelevant |
| §3.8-Bestätigung protokolliert | **JA** (EV-D01) |
| **Phase-A-Abschluss** | **AUSSTEHEND** (Kap. 8b/11) |
| **Freigabe gemäß §10.6** | **BLOCKIERT durch Ausschlussgrund 8** bis zur Entscheidung über F-SPR01R-01 |

> ## **RL-05-Ergebnis: B — erst nach Governance-Klärung erreichbar.**
> Nicht A (jetzt erreichbar): Ausschlussgrund 8 aktiv, Phase-A-Abschluss
> offen. Nicht C (dauerhaft blockiert): ein definierter Klärungsweg
> existiert (§7.6 / GDR-OD01-001 / Abschlussfeststellung).

## 10. Authority Finding

| Feststellung | Autorität | Quelle |
|---|---|---|
| SPR-01-Abschluss (Sprint-Status „Done") | **Projekteigner / Governance** — Sprint-Abnahme; „Review Before Approval"-Prinzip; SPR-01-Freigaben liefen durchgehend über den Projekteigner | Dev Standard §4/§17 Anh. B; ADW-SPR-1.0-001 Kap. 20 |
| Entscheidung der Baseline-Abweichung F-SPR01R-01 (ADR-005/006/007-Disposition) | **Governance-Entscheidung in Form eines ADR oder RDR (Baseline Change Control)**; der Gegenstand ist zugleich per GDR-OD01-001 als getrennte Disposition registriert | IP §7.6; ADR-012 Kap. 1.1 |
| RL-05-Feststellung / Freigabe gemäß §10.6 | **Projekteigner** (OP-2: „Phase-A-Protokoll + RL-05-Feststellung") | Sprint Plan Kap. 8 OP-2 |

## 11. Fakt vs. Inference

| # | Aussage | Klasse |
|---|---|---|
| 1 | EV-D01 protokolliert; 29/32 PASS; RB-1.0 258/258; Deviation dokumentiert/eskaliert | **SOURCE FACT** |
| 2 | Ausschlussgrund Nr. 8 ist aktiv; ein einzelner Grund genügt | **SOURCE FACT** (IP §10.6) |
| 3 | SPR-01-Exit verlangt „Aufhebung des §4.2-Vorbehalts"; „Bei Abweichung … kein Übergang" | **SOURCE FACT** (Sprint Plan SPR-01) |
| 4 | §7.6 Regel 4 lässt nicht betroffene Arbeit weiterlaufen | **SOURCE FACT** |
| 5 | Ob 3 und 4 zusammen einen **Teil-Abschluss** von SPR-01 (Carve-out GI-07/08/09) erlauben, regelt keine Quelle ausdrücklich | **UNDETERMINED — HUMAN DECISION REQUIRED** |
| 6 | „258/258 PASS" ⇒ „SPR-01 APPROVED" | **UNZULÄSSIGE INFERENCE — nicht gezogen** |
| 7 | „SPR-01 abgeschlossen" ⇒ „RL-05 erreicht" | **UNZULÄSSIGE INFERENCE — nicht gezogen** (Ausschlussgrund 8 + Freigabeakt nötig) |

**Antwort auf die Kernfragen 1/2:** Ob SPR-01 trotz F-SPR01R-01 als
abgeschlossen gilt, ist **nicht quellendeterminierbar** (Punkt 5) —
**separate Human Decision erforderlich** (Frage 6: **JA**).

## 12. Options

| | **OPTION A — Teil-Abschluss mit Carve-out** | **OPTION B — Erst Disposition, dann Vollabschluss** | **OPTION C — DEFERRED** |
|---|---|---|---|
| Inhalt | Projekteigner stellt SPR-01-Abschluss für den nicht betroffenen Umfang fest (§7.6 Regel 4), GI-07/08/09 ausdrücklich ausgenommen; Disposition F-SPR01R-01 läuft separat | Zuerst Governance-Entscheidung über die ADR-005/006/007-Register-Divergenz (GDR-OD01-001-Strang; Form gemäß §7.6: Baseline Change Control); danach SPR-01 vollständig (32/32) abschließen und RL-05-Feststellung in einem Akt vorbereiten | Beide Feststellungen zurückstellen; Coding-Strang bleibt ruhend |
| Quellenstütze | §7.6 Regel 4 (Weiterlauf); Carve-out-Konstrukt selbst ist **nicht** ausdrücklich geregelt (Punkt 5) | §7.6 (definierter Entscheidungsweg); Ausschlussgrund 8 verlangt „entschieden"; GDR-OD01-001 hat die Disposition bereits als eigenen Gegenstand registriert | zulässige Entscheidungskategorie (Präzedenz HD-2/AC-16) |
| Vorteil | schnelle formale Teilwirkung | löst die **einzige wurzelhafte Blockade**; keine Sonderkonstrukte; danach glatter Vollabschluss | kein Handlungsdruck |
| Nachteil/Risiko | **bringt praktisch nichts**: Ausschlussgrund 8 blockiert die Umsetzung trotzdem; erzeugt ein quellenseitig ungeregeltes Teilabschluss-Konstrukt | Disposition erfordert einen eigenen, sauber autorisierten Schritt (Berührung der vorbestehenden Welt-B-Änderungen — bisher tabu; benötigt ausdrückliche Autorisierung) | Milestone-Fortschritt ruht vollständig |
| Nötige Human Decision | Abschlussfeststellung + Carve-out-Billigung | Dispositionsentscheidung (Welt A bestätigen **oder** Welt B autorisiert committen — via Baseline-Change-Control-Akt), danach Abschluss-/RL-05-Feststellung | ausdrückliche Vertagung |

## 13. Empfehlung — ausdrücklich nur als Empfehlung

> **RECOMMENDATION: OPTION B.**

Begründung (Architektursicht): Ausschlussgrund 8 macht jede
Umsetzungsfreigabe unmöglich, solange F-SPR01R-01 unentschieden ist — ein
Carve-out (A) erzeugte daher Governance-Aufwand ohne praktischen Gewinn.
B behebt die Blockade an der Wurzel, hält die Kette einfach
(Disposition → Vollabschluss 32/32 → RL-05-Feststellung), vermeidet
ungeregelte Teilabschluss-Konstrukte und nutzt den bereits registrierten
GDR-OD01-001-Strang. Die technische Baseline ist nachweislich intakt
(20/20 technische Positionen, 258/258 Tests) — das Risiko der Disposition
ist rein dokumentarisch.

## 14. Minimaler nächster Schritt (nicht ausgeführt)

**DEC-Welle:** Human Decision des Projekteigners über Option A/B/C.
Bei B zusätzlich als Folgeschritte (je eigene, kleine Work Items):
(1) Dispositionsentscheidung ADR-005/006/007 (Baseline Change Control /
GDR-OD01-001) mit ausdrücklicher Autorisierung der betroffenen
Working-Tree-Dateien; (2) SPR-01-Vollabschluss-Feststellung; (3)
RL-05-/§10.6-Freigabeprüfung. Nichts davon wird durch diese PREP begonnen.

## 15. Explicit Non-Decisions

```text
SPR-01-Abschluss: NICHT festgestellt. RL-05: NICHT erreicht/markiert.
F-SPR01R-01: NICHT geschlossen. GI-07/08/09: UNVERÄNDERT.
ADR-005/006/007: UNVERÄNDERT (Welt A und Welt B unangetastet).
Bedingung 8: NICHT für erfüllt erklärt. Ausschlussgrund 8: NICHT aufgehoben.
Coding: NOT AUTHORIZED. QG-001…QG-008: NOT STARTED.
HD-2 DEFERRED/OPEN · HD-3 APPROVED/O-2 · AC-16 DEFERRED — unverändert.
Keine Human Decision erfunden; keine Statusnachführung; keine neue Regel.
```

## 16. Change Surface

Genau **eine neue Datei** (dieses PREP-Archiv). Keine bestehende Datei
verändert; vorbestehende Working-Tree-Änderungen unangetastet.

## 17. Preflight

| Check | Ergebnis |
|---|---|
| Baseline verifiziert (`2255a5e`); Source Gate vollständig; keine externe Quelle | PASS |
| Keine Entscheidung getroffen; keine unzulässige Inference (Kap. 11 Punkte 6/7) | PASS |
| Kein Status nachgeführt; keine OI/UNKNOWN/Deviation geschlossen | PASS |
| Optionen quellengestützt; Empfehlung als Empfehlung gekennzeichnet | PASS |
| Genau eine neue Datei; nur diese wird gestaged; kein Push/PR/Merge | PASS |

---

**Ende JX-DEV-SPR01-RL05-DEC-01-R0 — Decision Preparation — JOCHEN X
Milestone 1.0 (2026-08-12) — Bezugs-Baseline
`MILESTONE-1.0-BASELINE = 8fcf42f1997dfcf6ff232e75fd33c37b933991c8`**
