# JOCHEN X — Milestone 1.0
# JX-DEV-SPR01-RL05-DISP-01-R0 — Disposition F-SPR01R-01 — Decision Preparation
## GI-07/08/09 (ADR-005/006/007, Welt A ↔ Welt B) über den GDR-OD01-001-Strang

> **COMPLETED — DECISION PREPARATION · HUMAN DECISION REQUIRED**
>
> Diese PREP-Welle bereitet **Schritt 1 der per JX-DEV-SPR01-RL05-HDR-01-R0
> genehmigten Option-B-Sequenz** vor: die Disposition der Baseline-Deviation
> **F-SPR01R-01**. Kernbefund: Welt B ist **kein Status-Flip**, sondern die
> vollständige, inhaltlich ausgearbeitete APPROVED-Fassung der drei ADRs —
> mit **auffindbarer Approval-Evidenz** (Milestone-0.9-Kette, Daten exakt
> deckungsgleich) und **implementiertem, testgrünem Code** (RB-1.0
> 258/258). Drei Optionen sind vorbereitet; **RECOMMENDATION — NOT A
> DECISION: OPTION B.** Es wurde nichts entschieden, keine Datei des
> Bestands verändert.
>
> **CODING = NOT AUTHORIZED** · **RL-05 = NOT REACHED** · **QG-006 = NOT STARTED**

---

## 1. Document Identity

| Feld | Wert |
|---|---|
| **Document ID** | **JX-DEV-SPR01-RL05-DISP-01-R0** |
| Mode / Wave | GOVERNANCE · **PREP** |
| Subject | Disposition F-SPR01R-01 (GI-07/08/09; ADR-005/006/007 Welt A ↔ Welt B) |
| Date | 2026-08-12 |
| Pfad | `docs/audits/jx-dev-spr01-rl05-disposition-prep-r0.md` |
| **Bezugs-Baseline** | `MILESTONE-1.0-BASELINE = 8fcf42f` (GDR-003) |
| HEAD bei Beginn | `e5180baff97fb2fa85223f3a55148c33656d81ac` (HDR-01, Option B) |
| **Status** | **COMPLETED — DECISION PREPARATION · HUMAN DECISION REQUIRED** |
| Sequenz-Einordnung | Schritt 1 von 3 (Disposition → SPR-01-Vollbewertung → RL-05-Prüfung) |

## 2. Baseline Gate

HEAD = `e5180ba` — erwarteter Stand; Kette bis `8fcf42f` vollständig.
Working Tree vollständig erfasst: 6 vorbestehende getrackte Modifikationen
(**ADR-005/006/007** [+1.476/−89 Zeilen über die drei Dateien],
`docs/architecture-book-v2.md`, `CLAUDE.md`, `ROADMAP.md`) + vorbestehende
untracked Dokumente — **sämtlich unangetastet**; nichts bereinigt,
überschrieben oder übernommen. Staging leer. **PASS.**

## 3. Human Decision Authority / Scope

**JX-DEV-SPR01-RL05-HDR-01-R0** (Projekteigner, 2026-08-12, OPTION B —
APPROVED) autorisiert den **Dispositionsprozess** über den bestehenden
GDR-OD01-001-Strang — ausdrücklich **nicht dessen konkreten Inhalt**
(Condition: „Disposition … muss separat und explizit autorisiert bzw.
durchgeführt werden"; Explicit Non-Decision: „Keine Entscheidung über den
konkreten Inhalt der ADR-005/006/007-Disposition"). Diese PREP bereitet
genau diese Inhaltsentscheidung vor. **GDR-OD01-001 Kap. 15 Folgeaktion A**
(„ADR-005/006/007 separat bewerten — Verhältnis Welt A zu Welt B;
Verhältnis zu den bestehenden Approval Records") ist der vorgemerkte
Rahmen; Autorität: **Projekteigner / Governance Architect**.

## 4. Source Gate

| # | Quelle | Verifikation |
|---|---|---|
| 1 | `jx-dev-spr01-rl05-human-decision-record-r0.md` (HDR-01) | Option-B-Autorisierung, Conditions — SOURCE FACT |
| 2 | `jx-dev-spr01-rl05-decision-prep-r0.md` | Ausschlussgrund-8-Analyse, Optionsraum — SOURCE FACT |
| 3 | `jx-dev-spr01-baseline-confirmation-r0.md` (EV-D01) | F-SPR01R-01-Feststellung; 20/20 technische Positionen PASS; RB-1.0 258/258 — SOURCE FACT |
| 4 | **GDR-OD01-001** (`docs/governance/od-01-governance-decision.md`, FINAL 2026-08-10) | vollständig gelesen: Kap. 4 (Welt-A/B-Verifikation), 5 (Ausgangslage inkl. Entstehung), 7 (Optionen a/b/c aus R0), 8 (OPTION C — getrennte Behandlung, kein Sammel-Commit), 9 (out of scope: Inhaltsdisposition OFFEN), 10 (Nicht-Wirkungen), 15 (Folgeaktion A/D), 16 (OP-1…OP-10, insb. **OP-3/OP-4 UNKNOWN**) |
| 5–7 | ADR-005 / ADR-006 / ADR-007 | **beide Welten gelesen** (Welt A via `git show 8fcf42f:`, Welt B via Working Tree + `git diff`) — Befunde Kap. 6–9 |
| 8 | Entstehungsquellen | GDR-003 (Baseline-Scope: 13 Include-Dateien, `docs/**` ausgeschlossen), Baseline Commit Record §15 Nr. 4, R0 §4.1/§4.2 — via GDR-OD01-001 Kap. 4/5 |
| 9 | IP §7.6 | Tatbestand „Baseline-Abweichung": Entscheidungsweg „Governance-Entscheidung in Form eines ADR oder RDR (Baseline Change Control)"; Rückkehr nach Genehmigung |
| 10 | Sprint Plan 1.0 (SPR-01 Exit, Kap. 6, OP-2) · 11: ADW-SPR-1.0-001 · 12: GDR-002/GDR-003 | Kontext verifiziert |
| 13 | Dev Standard v1.1 §5/§13/§17 Anh. B | **§5: „Alle akzeptierten ADRs in `docs/adr/` sind Teil der Baseline"**; Statuswerte `Open → Accepted`; A-1-Registrierungspräzedenz (HD4-A1-R0) |
| 14 | **Approval-Evidenz Milestone 0.9** | `docs/milestone-0.9-implementation-plan.md`: „ADR-005 APPROVED 2026-07-30 · ADR-006 APPROVED 2026-07-29 · ADR-007 APPROVED 2026-07-29" — **exakt deckungsgleich mit den Welt-B-Headern**; `docs/milestone-0.9-engineering-spec.md`: „ADR-005 Approved — Verified: docs/adr/005-…" (DISP-B-02) |

Repositoryweite Suchen (F-SPR01R-01, GI-07/08/09, GDR-OD01-001, Welt A/B,
Baseline Deviation, Disposition, SPR-01, §7.6) durchgeführt. Keine externe
Quelle. **PASS.**

## 5. F-SPR01R-01 Exact Finding

Committed Baseline-Stand (`8fcf42f`, Welt A) führt
`docs/adr/005/006/007-…md` mit `Status: Open – requires decision before
implementation`; IP §3.7 (GI-07/08/09) erwartet „APPROVED — unverändert";
der Working Tree (Welt B, vorbestehend) führt vollständige APPROVED-
Fassungen. Festgestellt in EV-D01 Kap. 8, eskaliert gemäß IP §7.6; per
HDR-01 zur Disposition über den GDR-OD01-001-Strang bestimmt.

## 6.–8. GI-07 / GI-08 / GI-09 Findings

| Position | Welt A (committed) | Welt B (Working Tree) | Diff-Umfang |
|---|---|---|---|
| **GI-07 / ADR-005** | Kurz-Stub der v0.7.0-Ära: „Open"; Kontext beschreibt fehlende Signatur-/Hash-Validierung als Zukunftsthema | „**APPROVED**, Approval Date **2026-07-30**, Supersedes: Draft v3" — vollständiger ADR (Kontext: Zwei-Phasen-Lifecycle per ADR-011; D1–D8: Purpose, Policy, Trust Determination, Signature Status, Validation Boundary, Failure Semantics, Audit, Separation) | +655 Zeilen |
| **GI-08 / ADR-006** | Stub: „Open" | „APPROVED, **2026-07-29**" — vollständig (D1–D6: Default-Deny, Three-State, Admission-Time Validation, Runtime Enforcement, Policy Source, Audit) | +308 Zeilen |
| **GI-09 / ADR-007** | Stub: „Open" | „APPROVED, **2026-07-29**" — vollständig (D1–D8 inkl. Resolution Semantics, Graph Semantics, Activation Guarantees) | +513 Zeilen |

**Zentraler Befund:** Die Divergenz ist **kein Status-Flip**, sondern
Stub ↔ vollständige, genehmigte Entscheidungsfassung.

## 9. World A vs World B

| Frage | Welt A | Welt B |
|---|---|---|
| Aussage | ADRs unentschieden (v0.7.0-Stand) | ADRs entschieden und APPROVED (2026-07-29/30) |
| Konsistenz mit implementiertem Code | **WIDERSPRICHT** — Integrity/Permission/Dependency-Mechanismen sind implementiert und per RB-1.0 (u. a. 42+33 Tests) grün; PL-02/03/04 sind laut IP §3.6 normativ „in ADR-005/006/007 verankert" | **KONSISTENT** — der Code implementiert die Welt-B-Substanz |
| Konsistenz mit nachgelagerter Governance | **WIDERSPRICHT** — Milestone-0.9-Kette, Engineering Spec 0.9/1.0, IP §3.7 (GI-07/08/09 „APPROVED"), Security Design/Architecture 1.0, ADR-012 (PL-Verankerung), CLAUDE.md | **KONSISTENT** mit sämtlichen genannten Quellen |
| Approval-Evidenz | keine (Stub) | **VORHANDEN**: Milestone-0.9-IP (Daten exakt deckungsgleich); 0.9-Engineering-Spec („Verified: docs/adr/005-…") — löst **OP-3** (GDR-OD01-001) materiell auf (DISP-B-02) |
| Autorisierte Bestätigung als maßgeblich? | **NEIN** — der Baseline-Scope (GDR-003) hat `docs/**` schlicht ausgeschlossen; keine Entscheidung bestätigt den Stub inhaltlich | **NEIN** — GDR-OD01-001 Kap. 10: Welt B ist **nicht automatisch** autorisiert/verbindlich (Frage F: **beide Welten unbestätigt** — genau das ist der Dispositionsgegenstand) |

## 10. Historical Traceability (Frage E — Entstehung)

1. 2026-07-29/30: ADR-006/007/005 im Milestone-0.9-Prozess genehmigt;
   Working-Tree-Fassungen entsprechend fortgeschrieben (Welt B).
2. Die Fortschreibungen wurden **nie committet** (vorbestehender Zustand).
3. 2026-08-09: GDR-003 definiert den Baseline-Snapshot-Scope mit **13
   Include-Dateien, alle `docs/**` ausgeschlossen** → `8fcf42f` friert die
   alten Stubs ein — laut GDR-OD01-001 Kap. 5 Nr. 5 „dokumentierte,
   **gewollte** Konsequenz … **kein Fehler**, aber mit Nachweisfolge".
4. 2026-08-10: GDR-OD01-001 (OPTION C) trennt die Disposition in drei
   Gruppen; Folgeaktion A (ADR-Gruppe) = NEXT AUTHORIZED WORK.
5. 2026-08-12: EV-D01 stellt die Divergenz als F-SPR01R-01 formal gegen
   IP §3.7 fest; HDR-01 (Option B) mandatiert die Disposition.

## 11. Authority Analysis (Frage D)

| Aussage | Autorität |
|---|---|
| Inhaltliche Disposition der ADR-Gruppe | **Projekteigner / Governance Architect** [GDR-OD01-001 Kap. 15 Folgeaktion A/D] |
| Form des Rückkehrwegs bei Baseline-Abweichung | IP §7.6: „Governance-Entscheidung in Form eines **ADR oder RDR** (Baseline Change Control)" — **Formfrage siehe Kap. 12** |
| ADR-Registrierung akzeptierter ADRs | Dev-Standard **§5** („Alle akzeptierten ADRs in `docs/adr/` sind Teil der Baseline") + §13/§17 Anh. B; Vollzugspräzedenz **HD4-A1-R0** (administrative Registrierung nach nachgewiesener Approval) |
| ADR-005/006/007-Approval selbst | **bereits erteilt** (Milestone-0.9-Kette, 2026-07-29/30) — wird durch die Disposition **nicht neu entschieden**, sondern registriert/vollzogen |

## 12. IP §7.6 / Change-Control Analysis

Zwei quellengestützte Lesarten der **Formfrage** — beide dokumentiert,
keine entschieden (Frage K: **keine Quelle verlangt zwingend eine
bestimmte Option**):

| Lesart | Inhalt | Stütze |
|---|---|---|
| **L-1 „§7.6-Wortlaut"** | Die Abweichungsauflösung erfordert eine Governance-Entscheidung **in ADR-/RDR-Form** | IP §7.6, Zeile „Baseline-Abweichung" |
| **L-2 „Registrierungsvollzug"** | Gegenstand der Abweichung sind **selbst drei bereits genehmigte ADRs**; ihre Überführung in den committeten Stand ist **administrativer Vollzug** von Dev-Standard §5 (Präzedenz: HD4-A1-R0 — Registrierung von ADR-012 per Decision Record + autorisiertem Commit, ohne neues ADR/RDR); kein neuer Architekturinhalt entsteht | Dev-Standard §5/§13; HD4-A1-R0; GDR-OD01-001 Kap. 15 D („Commit, Revision, Amendment **oder andere Governance-Aktion**") |
| Randbedingungen (beide Lesarten) | **Kein Sammel-Commit** (GDR-OD01-001 Kap. 8 Nr. 4); Architecture Book (Gruppe 2) und CLAUDE.md/ROADMAP.md (Gruppe 3) bleiben **ausgenommen**; Bootstrap Baseline §8 ist **nicht** berührt (keine Code-/Bootstrap-Änderung — die Disposition ist rein dokumentarisch) | GDR-OD01-001 Kap. 8/9 |

Die Wahl der Form ist **Entscheidungsfrage der DEC** (Kap. 17 Nr. 2).

## 13. Disposition Options

| Option | Inhalt |
|---|---|
| **OPTION A** | **Welt A bestätigen**: Der committete Stub-Stand bleibt maßgeblich; die Welt-B-Fassungen werden nicht übernommen |
| **OPTION B** | **Welt B als autorisierte Fortschreibung übernehmen**: per explizit autorisiertem Governance-Akt (Form gemäß Kap. 12 L-1 oder L-2) werden **ausschließlich die drei ADR-Dateien** committet (Gruppe-1-only; AB/CLAUDE/ROADMAP unberührt) |
| **OPTION C** | **DEFERRED** — weitere Klärung; Divergenz bleibt bestehen |

Weitere reale Optionen ergeben die Quellen nicht (die R0-Optionen a/b/c zu
OD-01 sind durch GDR-OD01-001 bereits auf die getrennte Behandlung
verengt; innerhalb der ADR-Gruppe verbleibt genau der obige Raum).

## 14. Option-by-Option Consequences (Frage H)

| Wirkung auf | **OPTION A** | **OPTION B** | **OPTION C** |
|---|---|---|---|
| GI-07/08/09 | dauerhafte DEVIATION gegen IP §3.7 — die IP-Erwartung müsste ihrerseits governance-seitig revidiert werden | nach Vollzug: **PASS** bei erneuter Prüfung (committed = APPROVED) | DEVIATION bleibt |
| F-SPR01R-01 | bleibt offen bzw. mutiert zum Dauerwiderspruch | **dispositioniert** — schließbar durch dokumentierten Vollzug | OPEN |
| §4.2-Vorbehalt | bleibt für GI-07/08/09 bestehen | nach Neubewertung aufhebbar | bleibt |
| IP §7.6 | Rückkehrweg unklar (Welt A widerspricht §3.7-Erwartung — neuer Eskalationsbedarf) | Rückkehrweg erfüllt (dokumentierte Genehmigung + Vollzug) | Eskalation bleibt offen |
| SPR-01 | Vollabschluss 32/32 **unmöglich** ohne IP-Revision | Vollabschluss nach Neubewertung **möglich** (Schritt 2 der Option-B-Sequenz) | blockiert |
| Coding-Bedingung 8 / Ausschlussgrund 8 | Ausschlussgrund 8 entfiele formal erst mit „Entscheidung" — aber neue Inkonsistenzen entstünden (Code implementiert Welt-B-Substanz ohne genehmigte ADR-Basis im committeten Stand) | Ausschlussgrund 8 nach Disposition **auflösbar**; Bedingung 8 über Schritt 2 erfüllbar | Ausschlussgrund 8 bleibt aktiv |
| RL-05 | faktisch weiter blockiert | Weg frei für Schritt 3 (separate Prüfung) | blockiert |
| Nachgelagerte Doku (SD/SA 1.0, ES 0.9/1.0, ADR-012, CLAUDE.md) | **massiver Konsistenzbruch** — alle setzen APPROVED voraus | konsistent | Zweiwertigkeit bleibt |

**Frage I (kleinste Change Surface):** OPTION B — genau **3 Dateien**,
rein dokumentarisch, Code/Tests unberührt. (OPTION A erzeugte 0 Datei-
Änderungen, aber erheblichen Folgeänderungsbedarf an IP/ES/SD/SA — die
tatsächliche Gesamt-Change-Surface wäre größer.)
**Frage J (sauberste Governance-Erhaltung):** OPTION B — erhält
Approval-Kette, Dev-Standard §5, GDR-OD01-001-Struktur und die
IP-§3.7-Erwartung zugleich.
**Frage K:** Keine Quelle **verlangt** zwingend eine Option.

## 15. Architecture Assessment

Der produktive Code ist in beiden Welten **byte-identisch** zur Baseline
(GDR-OD01-001 Kap. 5 Nr. 1); die Disposition ist eine reine
Dokumentations-/Vertragsfrage. Die technische Sicherheitsarchitektur
(Admission-Pipeline PL-01…PL-05) ist implementiert, baseline-bestätigt
und testgrün — sie **implementiert die Welt-B-Substanz**. Ein Verbleib bei
Welt A ließe den sicherheitskritischen Code ohne committeten, genehmigten
Entscheidungstext zurück — das wäre governance-seitig die riskantere Lage.

## 16. Recommendation

> ## **RECOMMENDATION — NOT A DECISION: OPTION B**
> (Welt B als autorisierte Fortschreibung übernehmen; Gruppe-1-only;
> Formfrage L-1/L-2 durch die DEC festlegen)

Bewertung: **Minimale effektive Change Surface** (3 Dokumentdateien; jede
Alternative erzeugt größeren Folgeaufwand) · **Source Authority**
(Approval-Evidenz 2026-07-29/30 vorhanden und datumsgenau deckungsgleich;
OP-3 auflösbar) · **historische Traceability** (Divergenz ist dokumentierte
Scope-Folge von GDR-003, kein inhaltlicher Dissens) · **§7.6-Konsistenz**
(dokumentierte Genehmigung + Vollzug = definierter Rückkehrweg) · **keine
Sonderlösung** (folgt dem A-1-Registrierungspräzedenz und Dev-Standard §5)
· **SPR-01/RL-05** (einziger Weg, der die Option-B-Sequenz der HDR-01
fortsetzt) · **Reversibilität** (git-revertierbar; rein dokumentarisch) ·
**Governance-Risiko gering** (kein Architekturinhalt ändert sich; AB
bleibt FROZEN und unberührt). Option A wird **nicht** wegen technischer
Einfachheit verworfen, sondern wegen des dokumentierten Widerspruchs zu
Approval-Kette, implementiertem Code und sämtlicher Folge-Governance.

## 17. Decision Questions for Project Owner

1. **Disposition:** OPTION A, B oder C?
2. Bei B — **Form** des Dispositionsakts: **L-2** (Governance Decision
   Record + explizit autorisierter Commit der drei ADR-Dateien, analog
   A-1-Registrierungsvollzug) oder **L-1** (ADR-/RDR-förmige Entscheidung
   gemäß §7.6-Wortlaut)?
3. Bei B — **Bestätigung des Umfangs:** ausschließlich
   `docs/adr/005/006/007-…md` (Gruppe 1); Architecture Book, `CLAUDE.md`,
   `ROADMAP.md` bleiben ausdrücklich unberührt (Gruppen 2/3 separat)?
4. Bei B — **Nachweisführung:** Schließung von GDR-OD01-001 **OP-3** durch
   Referenz auf die Milestone-0.9-Approval-Einträge im Dispositionsrecord?
5. Soll die erneute SPR-01-Vollbewertung (Schritt 2) unmittelbar nach dem
   Vollzug als eigenes Work Item beauftragt werden?

## 18. Explicit Non-Decisions

```text
F-SPR01R-01 bleibt bis zur Human Decision OPEN.
ADR-005/006/007 bleiben unverändert (beide Welten unangetastet).
SPR-01 bleibt NICHT vollständig abgeschlossen. §4.2-Vorbehalt besteht fort.
RL-05 bleibt NOT REACHED. Coding bleibt NOT AUTHORIZED.
QG-006 bleibt NOT STARTED. ADR-012 / HD-2 / HD-3 / AC-16 unverändert.
Keine OI-/UNKNOWN-Schließung (OP-3 nur als auflösbar dokumentiert).
Keine Sprint-/WP-Umplanung. Keine Working-Tree-Änderung.
Keine Option als Tatsache dargestellt; Empfehlung ist keine Entscheidung.
```

## 19. Follow-up DEC / EXEC Definition

| Welle | Inhalt |
|---|---|
| **DEC** | HUMAN-DECISION-Block des Projekteigners (Authority, Date, Decision [A/B/C], Scope, Decision Detail inkl. Formwahl L-1/L-2 und Umfangsbestätigung, Conditions) → Aufzeichnung als Decision Record |
| **EXEC** (nur bei B, nach DEC) | Mechanischer Vollzug gemäß Formwahl: Dispositionsrecord + autorisierter Commit **ausschließlich** der drei ADR-Dateien; Baseline-/Preflight-Gates; danach Schritt 2 (SPR-01-Vollbewertung) als eigenes Work Item |

## 20. Preflight / Change Surface

| Check | Ergebnis |
|---|---|
| Baseline verifiziert; Source Gate vollständig; keine externe Quelle | PASS |
| Nichts entschieden; keine Human Decision simuliert; keine ADR-/Working-Tree-Datei verändert | PASS |
| Beide Welten vollständig gelesen und getrennt dokumentiert (Befund ≠ Zustand ≠ Entscheidung ≠ Empfehlung) | PASS |
| Genau eine neue Datei (dieses PREP-Archiv); nur diese wird gestaged; kein Push/PR/Merge | PASS |

**Beobachtungen:** **JX-DISP-B-01** — Die Welt-B-Fassungen sind
vollständige ADR-Neufassungen (+1.476 Zeilen netto über drei Dateien),
keine Statuszeilen-Edits; jede Disposition betrifft daher den gesamten
Vertragstext, nicht nur ein Statusfeld. **JX-DISP-B-02** — Die
Approval-Evidenz (Milestone-0.9-IP: 2026-07-30/29/29; 0.9-ES „Verified")
ist datumsgenau deckungsgleich mit den Welt-B-Headern und löst
GDR-OD01-001 OP-3 materiell auf; die Evidenzquellen liegen selbst
untracked vor (Zustandsvermerk analog JX-SPR01-B-03). **JX-DISP-B-03** —
Die Formfrage (L-1 §7.6-Wortlaut vs. L-2 Registrierungsvollzug nach
Dev-Standard §5 / A-1-Präzedenz) ist quellenseitig nicht determiniert und
wurde als DEC-Frage übergeben.

## 21. Final Governance Finding

> ## **DISPOSITION PREPARED — HUMAN DECISION REQUIRED**
>
> Der Entscheidungsraum (A: Welt A bestätigen · B: Welt B autorisiert
> übernehmen · C: DEFERRED) ist vollständig quellenbasiert aufbereitet;
> Approval-Evidenz, Entstehungsgeschichte, Autoritäts- und Formfragen sowie
> sämtliche Folgen je Option liegen vor. **RECOMMENDATION — NOT A
> DECISION: OPTION B.** Bis zur Human Decision bleiben F-SPR01R-01 OPEN,
> SPR-01 unvollständig, RL-05 NOT REACHED, Coding NOT AUTHORIZED.

---

## Revision History

| Revision | Datum | Änderung | Status |
|---|---|---|---|
| **R0** | 2026-08-12 | Ersterstellung der Dispositions-Entscheidungsvorbereitung (F-SPR01R-01 / GI-07/08/09) | **COMPLETED — DECISION PREPARATION** |

---

**Ende JX-DEV-SPR01-RL05-DISP-01-R0 — Disposition Decision Preparation —
JOCHEN X Milestone 1.0 (2026-08-12) — Bezugs-Baseline
`MILESTONE-1.0-BASELINE = 8fcf42f1997dfcf6ff232e75fd33c37b933991c8`**
