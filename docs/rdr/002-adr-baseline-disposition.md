# RDR-002: Disposition F-SPR01R-01 — Übernahme des World-B-Stands für ADR-005/006/007

| Feld | Wert |
|---|---|
| Status | **APPROVED** |
| Typ | Repository Decision Record — Disposition / Baseline Change Control (IP §7.6) |
| Erstellt | 2026-08-13 |
| Genehmigt | 2026-08-13 (Human Decision des Projekteigners, wörtlich in §3) |
| Betrifft | `docs/adr/005-plugin-integrity-validation.md` · `docs/adr/006-plugin-permission-model.md` · `docs/adr/007-plugin-dependency-resolution.md` |
| Governance | PREP (JX-DEV-SPR01-RL05-DISP-01-R0) → DEC (JX-DEV-SPR01-RL05-DISP-HDR-01-R0 + Instrumentenwahl) → **dieser RDR (EXEC)** → separater VERIFY |
| Bezugs-Baseline | `MILESTONE-1.0-BASELINE = 8fcf42f` (GDR-003) |
| Coding | **NOT AUTHORIZED** · RL-05 **NOT REACHED** · QG-006 **NOT STARTED** |

---

## 1. Zweck

Dieser RDR dokumentiert **ausschließlich** die Disposition der
Baseline-Deviation **F-SPR01R-01** (GI-07/GI-08/GI-09) und die
Autorisierung der Übernahme des quellenbelegten **WORLD-B-Stands** von
ADR-005, ADR-006 und ADR-007 in den committeten Stand. Er **ersetzt keine
der drei ADRs** und trifft **keine neue technische
Architekturentscheidung**. Er ist der per Human Decision gewählte
L-1-Vollzugsweg gemäß IP §7.6 (Baseline Change Control).

## 2. Kontext

Am Baseline-Snapshot `8fcf42f` (GDR-003; `docs/**` bewusst außerhalb des
Snapshot-Scopes) verblieben ADR-005/006/007 als historische v0.7.0-Stubs
(`Status: Open`), während die im Milestone-0.9-Prozess **genehmigten**
Vollfassungen (World B) ausschließlich als vorbestehende, uncommittete
Working-Tree-Modifikationen existierten. GDR-OD01-001 (OPTION C, FINAL
2026-08-10) ordnete die getrennte Disposition an (Folgeaktion A);
EV-D01 (JX-DEV-SLICE-SPR01-BUILD-01-R0) stellte die Divergenz als
**F-SPR01R-01** formal gegen IP §3.7 fest; JX-DEV-SPR01-RL05-HDR-01-R0
(OPTION B) mandatierte die Disposition; die Dispositions-PREP
(JX-DEV-SPR01-RL05-DISP-01-R0) bereitete den Entscheidungsraum vor.

## 3. Human Decision — wörtlich, unverändert

```text
HUMAN-DECISION

Authority: Project Owner / Projekteigner
Date: 2026-08-13

Decision: OPTION B — WORLD B AUTHORISED

Scope:
F-SPR01R-01 / Disposition der Baseline-Divergenz ADR-005, ADR-006 und
ADR-007.

Decision Detail:
Die quellenbelegte WORLD-B-Fassung von ADR-005, ADR-006 und ADR-007 wird
als autorisierter Stand übernommen.

Form:
L-1 — Governance-Entscheidung gemäß IP §7.6 als RDR (Repository Decision
Record).

RDR-Zweck:
Der RDR dokumentiert ausschließlich die Disposition von F-SPR01R-01 und
die Autorisierung der Übernahme des WORLD-B-Stands. Er ersetzt keine der
drei ADRs und trifft keine neue technische Architekturentscheidung.

Authorized Change Surface:
Ausschließlich:
1. der neue RDR / Dispositions-Record,
2. ADR-005,
3. ADR-006,
4. ADR-007.

Die WORLD-B-Fassungen der drei ADRs dürfen auf den im PREP verifizierten,
quellenbelegten Stand übernommen werden.

Conditions:
1. Vor Ausführung müssen die drei WORLD-B-Dateien nochmals gegen die im
   PREP identifizierte Approval-Evidenz verifiziert werden.
2. Kein Sammel-Commit mit anderen Dateien.
3. Keine Änderung an Architecture Book, IP, Sprint Plan, ADR-012 oder
   anderen Governance-Artefakten.
4. Keine technische Codeänderung.
5. Keine Änderung an Tests.
6. Keine Änderung an Working-Tree-Dateien außerhalb der ausdrücklich
   autorisierten drei ADRs.
7. F-SPR01R-01 darf erst nach erfolgreichem EXEC + anschließendem VERIFY
   als aufgelöst betrachtet werden.
8. GI-07/08/09 dürfen nicht automatisch als PASS markiert werden; dies
   erfolgt erst durch die separate SPR-01-Vollbewertung.
9. SPR-01 wird durch diese Entscheidung noch nicht als abgeschlossen
   erklärt.
10. RL-05 bleibt NOT REACHED.
11. QG-006 bleibt NOT STARTED.
12. HD-2, HD-3, AC-16, ADR-012, OI-2 und TD-19 bleiben unverändert.
13. Kein Push, kein PR, kein Merge.

Explicit Non-Decisions:
Diese Entscheidung:
- autorisiert kein Coding,
- autorisiert keinen RL-05-Eintritt,
- schließt SPR-01 nicht ab,
- entscheidet keine weiteren ADRs,
- ändert keine anderen Governance-Status,
- löst keine weiteren UNKNOWNs,
- autorisiert keine Sprint-/WP-Änderung.

EXEC-Auftrag:
Nach Verifikation dieses HUMAN-DECISION-Blocks darf die EXEC-Welle
ausschließlich den oben definierten mechanischen Vollzug durchführen.

Danach ist ein separater VERIFY-Schritt erforderlich.
Erst nach erfolgreichem VERIFY darf Schritt 2 der bereits genehmigten
OPTION-B-Sequenz vorbereitet werden:
SPR-01-Vollbewertung gegen alle 32 Positionen.

END HUMAN-DECISION
```

## 4. Approval-Evidenz (Condition 1 — vor Ausführung erneut verifiziert)

| ADR | World-B-Header (Working Tree, 2026-08-13) | Approval-Evidenz | Ergebnis |
|---|---|---|---|
| ADR-005 Plugin Integrity Validation | `Status: APPROVED · Approval Date: 2026-07-30` | `docs/milestone-0.9-implementation-plan.md`: „ADR-005 (Integrity Validation) — APPROVED — 2026-07-30" | **MATCH** |
| ADR-006 Plugin Permission Model | `Status: APPROVED · Approval Date: 2026-07-29` | ebd.: „ADR-006 (Permission Model) — APPROVED — 2026-07-29" | **MATCH** |
| ADR-007 Plugin Dependency Resolution | `Status: APPROVED · Approval Date: 2026-07-29` | ebd.: „ADR-007 (Dependency Resolution) — APPROVED — 2026-07-29" | **MATCH** |

Ergänzend: `docs/milestone-0.9-engineering-spec.md` führt die drei ADRs als
„Approved — Verified" gegen die ADR-Dateien; der implementierte
Admission-Code (Integrity → Permission → Dependency) ist per RB-1.0
(258/258, EV-D01) funktional grün und implementiert die World-B-Substanz.
Damit ist **GDR-OD01-001 OP-3** („Inhalt der Approval Records — UNKNOWN")
durch dieses Record und die referenzierte Evidenz **aufgelöst**.

**CONDITION 1: PASS — datumsgenaue Übereinstimmung aller drei Fassungen.**

## 5. Autorisierter Vollzug (EXEC)

| # | Aktion | Status |
|---|---|---|
| 1 | Erstellung dieses RDR (`docs/rdr/002-adr-baseline-disposition.md`) | **AUSGEFÜHRT** |
| 2 | Übernahme der drei ADR-Dateien auf den quellenbelegten World-B-Stand: die vorbestehenden Working-Tree-Fassungen werden **unverändert** (kein Zusatz, keine Neuinterpretation, keine technische Änderung) in den committeten Stand überführt | **AUSGEFÜHRT** (per Commit dieses Vollzugs) |
| 3 | Commit ausschließlich der vier autorisierten Dateien (RDR-002 + ADR-005/006/007) — kein Sammel-Commit mit anderen Dateien; `CLAUDE.md`, `ROADMAP.md`, `docs/architecture-book-v2.md` und alle übrigen Working-Tree-Bestände bleiben unangetastet | **AUSGEFÜHRT** |

Der Vollzug ist rein dokumentarisch: keine Code-, Test- oder
Konfigurationsdatei ist betroffen; der produktive Baum bleibt
byte-identisch zur Baseline.

## 6. Wirkung und Grenzen

| Position | Stand nach diesem RDR |
|---|---|
| ADR-005/006/007 (committed) | **APPROVED-Vollfassungen (World B)** — Welt-A/Welt-B-Divergenz für die ADR-Gruppe beendet |
| **F-SPR01R-01** | **EXEC VOLLZOGEN — Auflösung erst nach separatem VERIFY** (Condition 7); bis dahin formal OPEN |
| **GI-07/08/09** | **NICHT als PASS markiert** — Feststellung obliegt der separaten SPR-01-Vollbewertung (Condition 8) |
| GDR-OD01-001 | Folgeaktion A (ADR-Gruppe) vollzogen; Gruppen 2 (Architecture Book) und 3 (`CLAUDE.md`/`ROADMAP.md`) **unverändert offen und unberührt** |
| SPR-01 | **NICHT abgeschlossen** (Condition 9) — Vollbewertung ist Schritt 2 der Option-B-Sequenz, nach VERIFY |
| RL-05 / Coding / QG-006 | **NOT REACHED / NOT AUTHORIZED / NOT STARTED** (Conditions 10/11) |
| HD-2, HD-3, AC-16, ADR-012, OI-2, TD-19 | **UNVERÄNDERT** (Condition 12) |
| Architecture Book v2.0 | **FROZEN, unberührt** — dieser RDR ändert es nicht und löst keine AB-Version aus |
| Push / PR / Merge | **NOT PERFORMED** (Condition 13) |

## 7. Nächste Schritte (nicht Bestandteil dieses RDR)

1. **VERIFY** — separater Schritt: Prüfung des Vollzugs (Commit-Inhalt =
   exakt die vier autorisierten Dateien; committeter ADR-Stand =
   World-B-Stand; keine Fremdänderung). Erst danach gilt F-SPR01R-01 als
   aufgelöst.
2. **Schritt 2 der Option-B-Sequenz** — SPR-01-Vollbewertung gegen alle
   32 Positionen (erst nach erfolgreichem VERIFY vorzubereiten).
3. **Schritt 3** — RL-05-/§10.6-Freigabeprüfung (separat).

---

**Ende RDR-002 — Disposition F-SPR01R-01 — JOCHEN X Milestone 1.0
(2026-08-13) — Bezugs-Baseline
`MILESTONE-1.0-BASELINE = 8fcf42f1997dfcf6ff232e75fd33c37b933991c8`**
