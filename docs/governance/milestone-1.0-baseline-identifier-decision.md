# JOCHEN X — Milestone 1.0
# Baseline Identifier Decision (F-SPR01-01)

## 1. Decision Metadata

| Feld | Wert |
|---|---|
| Dokumenttyp | Governance / Repository-Integrity Decision |
| Decision ID | **GDR-003** |
| Status | **FINAL** |
| Datum | 2026-08-09 |
| Rolle | Governance Architect / Release Authority / Repository-Integrity-Verantwortlicher |
| Gegenstand | F-SPR01-01 (MEDIUM, OPEN) — OPEN BASELINE IDENTIFIER |
| Wirkung | Dokumentierte Entscheidung über die Identifizierbarkeit und den Scope des Baseline-Snapshots. **Kein Commit, kein Tag, kein Push, kein Cleanup** wurde durchgeführt. Der Working Tree wurde ausschließlich gelesen (Beweismaterial). |

## 2. Authorization

Projekteigner-Auftrag zur Behandlung von F-SPR01-01 (dieser Auftrag). Grundlagen: SPR-01 Baseline Confirmation (FINAL — BASELINE CONFIRMED, RB-1.0 CONFIRMED: 258 Tests / 14 Dateien), ADW-SPR-1.0-001, GDR-002, IP 1.0 R1.2 (APPROVED). Dieser Schritt ist ausdrücklich **kein Commit-Auftrag**; die physische Herstellung erfolgt nur in einem separat autorisierten Folgeschritt.

## 3. Source Gate

Alle 12 Pflichtquellen vorhanden, gelesen, statuskonform (SPR-01-Artefakte FINAL; OP-1 FINAL; Sprint Plan DRAFT 1.0 R0 genehmigt; IP APPROVED R1.2; Charter/ES/DevStd/Bootstrap-Baseline APPROVED; AB v2.0 FROZEN; GDR-002 FINAL; W-8 CLOSED). Zusätzlich sämtliche in F-SPR01-01 genannten Dateien forensisch erfasst (Kap. 5–7). **BESTANDEN.**

## 4. Git Snapshot

| Element | Wert |
|---|---|
| Branch | `milestone-1.0-governance` |
| HEAD | `63407ad9d8538c5ea5ae5b06b2f7f461332eea14` |
| Erfassungszeitpunkt | 2026-08-09 |
| Methode | `git status --porcelain`, `git diff --stat`, `git diff --cached --stat`, `git ls-files`, Datei-/Referenzanalyse — sämtlich read-only |

## 5. HEAD State

- HEAD `63407ad` enthält den committeten Stand bis einschließlich der Governance-Commits zu Milestone 1.0 / Security-Governance.
- **HEAD-only relevanter Bestand:** `src/jochen_x/**` — 66 Dateien bei HEAD getrackt, **unmodifiziert**. Gemäß GDR-002 D-2 stillgelegt; die physische Behandlung bleibt separat zu entscheiden. Der Baseline-Commit-Scope dieser Entscheidung **berührt diesen Bestand nicht** (weder Aufnahme noch Entfernung — Cleanup ist in diesem Schritt verboten).

## 6. Working Tree State

| Kategorie | Anzahl | Befund |
|---|---|---|
| A. Modified tracked | **12** | siehe Kap. 7 |
| B. Deleted tracked | **0** | — |
| C. Untracked | **71 Einträge** (inkl. 2 Verzeichnisse `docs/baselines/`, `docs/rdr/`) | siehe Kap. 7 |
| D. Staged | **0** | Index leer (`git diff --cached` leer) |
| E. HEAD-only | `src/jochen_x/**` (66 Dateien, unmodifiziert) | Kap. 5 |
| F. Working-Tree-only | = untracked (C) | — |

## 7. File Classification

Jede betroffene Datei wurde inhaltlich (Diff-Umfang, Quellenreferenz, Testbezug) eingeordnet — keine Einordnung allein nach Dateinamen.

### 7.1 BASELINE-INCLUDE (13 Dateien) — Bestandteil des künftigen Baseline-Commits

| Datei | Zustand | Begründung (Quellen) |
|---|---|---|
| `app/bootstrap/__init__.py` | M (−972 Zeilen: Monolith → Fassade) | Bootstrap-Modularisierung gemäß **Bootstrap Baseline 1.0** (APPROVED, „Ersetzt: Bootstrap-Implementierung vor RDR-001"); IP §5.5 führt die modulare Struktur als bestehend |
| `app/bootstrap/constants.py` | untracked | dito — Bestandteil der von Bootstrap Baseline 1.0 beschriebenen modularen Struktur |
| `app/bootstrap/manager.py` | untracked | dito (BootstrapManager — CLAUDE.md/AB-Bootstrap-Reihenfolge; IP-Bestand) |
| `app/bootstrap/stages_init.py` | untracked | dito |
| `app/bootstrap/stages_late.py` | untracked | dito |
| `app/bootstrap/stages_plugin.py` | untracked | dito (PluginSecurity-/Activation-Stages, ADR-011-Struktur) |
| `app/bootstrap/types.py` | untracked | **IP §5.5 referenziert diese Datei ausdrücklich als Definitionsort von Baseline-Symbolen (Z. 54/71, API-01)** |
| `app/application_host.py` | M (22 Zeilen) | Produktivbestand des bestätigten Zustands; von RB-1.0-Tests (`test_application_foundation.py`) geprüft |
| `app/events.py` | M (+47) | Typed Application Events — Produktivbestand des bestätigten Zustands (AB/CLAUDE.md-Struktur); RB-1.0-testrelevant |
| `app/security/security_manager.py` | M (+2) | Produktivbestand; im SD-W-1 Source Gate in genau diesem Zustand gelesen |
| `sdk/_test_hooks.py` | untracked | **Wird von der RB-1.0-Testdatei `tests/test_application_foundation.py` referenziert** — ohne sie ist der bestätigte Testzustand nicht reproduzierbar |
| `tests/test_application_foundation.py` | M (+80) | **RB-1.0-Datei (62 Tests)** — die Zählung vom 2026-08-09 erfolgte gegen exakt diesen Working-Tree-Stand |
| `tests/integration/test_plugin_integration.py` | M (Umbau) | **RB-1.0-Datei (3 Tests)** — dito |

Maßgebliches Kriterium: Dies ist exakt der produktive Zustand, gegen den SPR-01 am 2026-08-09 BASELINE CONFIRMED und RB-1.0 CONFIRMED festgestellt hat — nicht „Nützlichkeit" oder „Funktionsfähigkeit". Alle 13 Dateien waren bereits **vor** SPR-01 in diesem Zustand vorhanden (identischer Working-Tree-Stand seit Sessionbeginn dokumentiert); keine wurde nach SPR-01 verändert.

### 7.2 PRE-EXISTING-EXTERNAL — getrackte Modifikationen an Governance-/Meta-Dokumenten (6 Dateien) → BASELINE-EXCLUDE

| Datei | Zustand | Einordnung |
|---|---|---|
| `docs/adr/005-plugin-integrity-validation.md` | M (+655) | APPROVED-ADR mit umfangreichen uncommitteten Erweiterungen (D1–D8-Entscheidungsstrukturen — von den Security-Reviews in diesem Zustand verifiziert). **Governance-Bestand: darf nicht mit Produktivcode „mitcommittet" werden**; Disposition über den Governance-Lebenszyklus in separatem Schritt |
| `docs/adr/006-plugin-permission-model.md` | M (+308) | dito |
| `docs/adr/007-plugin-dependency-resolution.md` | M (+513) | dito |
| `docs/architecture-book-v2.md` | M (45) | **FROZEN-Dokument mit uncommitteten Änderungen** — Governance-Disposition erforderlich (separater Schritt); nicht Teil des Produkt-Baseline-Commits |
| `CLAUDE.md` | M (8) | Projekt-Metadokument; separater Doku-Commit-Scope |
| `ROADMAP.md` | M (5) | dito |

### 7.3 SESSION-ARTEFACT (11 Dateien, diese Governance-/Sprint-Session) → BASELINE-EXCLUDE

`docs/governance/security-design-1.0-approval-decision-w2.md` · `…/security-design-1.0-approval-record.md` · `…/security-design-1.0-governance-closing-w4.md` · `…/jochen-x-next-authorized-work-assessment.md` · `…/gr-001-governance-decision.md` · `…/milestone-1.0-sprint-planning-preflight.md` · `…/milestone-1.0-sprint-planning-approval-decision-op1.md` · `…/milestone-1.0-sprint-01-baseline-confirmation.md` · `docs/audits/milestone-1.0-sprint-planning-summary-r0.md` · `docs/audits/milestone-1.0-sprint-01-verification-summary.md` · `docs/milestone-1.0-sprint-plan.md`

Governance-/Audit-/Planungsartefakte — keine genehmigte Quelle verlangt ihre Aufnahme in den Produkt-Baseline-Commit; ihre Versionierung ist ein separater Governance-Commit-Scope.

### 7.4 PRE-EXISTING-EXTERNAL — untracked Governance-/Doku-Bestand (53 Einträge) → BASELINE-EXCLUDE

Vorbestehender, nie committeter Dokumentationsbestand: `docs/audits/**` (29 vorbestehende Dateien inkl. Milestone-0.8/0.9- und IP-1.0-Audits, SD-Creation-Summary, SD-W1-Review, `.docx`-Bundle) · `docs/governance/**` (16 vorbestehende Dateien inkl. Waiver, GDR-001, IP-/ES-/Charter-Records, W-8) · `docs/baselines/` · `docs/rdr/` · `docs/development-standard-v1.md` / `-v1.1.md` · Milestone-0.8/0.9/1.0-Spezifikationen, Charter, Pläne, Roadmap · `docs/security-design-1.0.md` (inkl. autorisierter W-4-Statusnachführung). Sämtlich Governance-/Dokumentationsbestand — eigener, separat zu autorisierender Commit-Scope; **nicht** Teil des Produkt-Baseline-Commits.

### 7.5 UNRESOLVED

**Keine.** Jede der 83 betroffenen Positionen (12 modified + 71 untracked) ist eindeutig zugeordnet.

## 8. Baseline Inclusion Criteria

Aufgenommen wird eine Datei genau dann, wenn sie (a) Teil des produktiven Milestone-Baums (GDR-002 D-1) ist **und** (b) in dem Zustand vorliegt, gegen den SPR-01 die Baseline bzw. RB-1.0 bestätigt hat, **und** (c) durch genehmigte Quellen getragen ist (Bootstrap Baseline 1.0, IP §5.5, RB-1.0-Register). Nützlichkeit, Funktionieren oder Herkunft sind ausdrücklich **keine** Kriterien.

## 9. Baseline Exclusion Criteria

Ausgeschlossen: Governance-/Security-/Audit-/Planungsartefakte (eigener Lebenszyklus, Kap. 11/12), Projekt-Metadokumente, vorbestehender unversionierter Doku-Bestand, `src/jochen_x/**` (stillgelegt — verbleibt unberührt bei HEAD bis zur separaten Entscheidung).

## 10. RB-1.0 Protection

- RB-1.0 (258/14) wurde gegen den **aktuellen Working-Tree-Stand** festgestellt; die beiden modifizierten RB-1.0-Dateien und `sdk/_test_hooks.py` sind daher zwingend im Include-Scope — **nicht** der HEAD-Stand dieser Dateien.
- Die übrigen 12 RB-1.0-Testdateien sind getrackt und unmodifiziert (HEAD-Stand = bestätigter Stand).
- Weder HEAD allein noch der Gesamt-Working-Tree wird übernommen: Der Snapshot ist exakt HEAD + die 13 Include-Dateien.
- Nach Herstellung des Baseline-Commits ist RB-1.0 (258/14) gegen den Commit reproduzierbar; eine Nachzählung als Abschlussprüfung des Commit-Schritts wird empfohlen.

## 11. Security/Governance Boundary

Core Principles, Security Architecture, Security Design, ADRs, Waiver, Records: **keine** dieser Dateien ist im Baseline-Commit-Scope. Die uncommitteten Änderungen an ADR-005/006/007 und Architecture Book v2.0 (Kap. 7.2) erfordern eine **eigene Governance-Disposition** (separater Schritt; kein stillschweigendes Mitcommitten). Keine Security-Findings/ODDs werden berührt.

## 12. Session Artefact Boundary

Die 11 Session-Artefakte (Kap. 7.3) und der vorbestehende Doku-Bestand (Kap. 7.4) sind nicht Teil des Produkt-Baseline-Commits. Ihre Versionierung (z. B. als getrennter `docs(governance)`-Commit) ist sinnvoll, aber ein **separat zu autorisierender** Schritt.

## 13. Unresolved Items

Keine (Kap. 7.5).

## 14. Proposed Baseline Snapshot

> **Snapshot-Definition:** HEAD `63407ad` **plus** exakt die 13 BASELINE-INCLUDE-Dateien aus Kap. 7.1 in ihrem aktuellen Working-Tree-Zustand (2026-08-09).
> Dieser Snapshot ist der Zustand, gegen den SPR-01 BASELINE CONFIRMED und RB-1.0 CONFIRMED festgestellt hat.

**Vorgeschlagener Baseline-Identifier** (nach separat autorisiertem Commit): der entstehende Commit-Hash, referenzierbar als `MILESTONE-1.0-BASELINE` (z. B. Commit-Message `chore(baseline): Milestone 1.0 Baseline Snapshot — RB-1.0 258/14, per GDR-003`). Bis dahin gilt weiterhin: OPEN BASELINE IDENTIFIER.

## 15. Proposed Commit Scope

| Scope | Inhalt | Autorisierung |
|---|---|---|
| **Commit 1 — Baseline-Commit** (Vorschlag) | genau die 13 Dateien aus Kap. 7.1 | **separat durch Projekteigner freizugeben** |
| Commit 2+ — Governance-/Doku-Commits (optional, nachgelagert) | Kap. 7.2 (ADR/AB-Disposition zuerst klären!), 7.3, 7.4 | separate Governance-Entscheidung |
| Kein Scope | `src/jochen_x/**` (unberührt), Caches/Artefaktverzeichnisse | — |

## 16. Decision

> ## OPTION A — BASELINE SNAPSHOT IDENTIFIABLE
>
> Der bei SPR-01 bestätigte Baseline-Zustand ist eindeutig identifizierbar:
> HEAD `63407ad` + die 13 in Kap. 7.1 exakt dokumentierten Dateien.
> Ein separater Commit darf auf Grundlage dieses exakt dokumentierten
> Scopes hergestellt werden.
>
> **Dies ist noch KEINE Commit-Freigabe.** Der tatsächliche Baseline-Commit
> erfolgt ausschließlich nach separater ausdrücklicher Freigabe des
> Projekteigners.

### F-SPR01-01 Disposition

> F-SPR01-01 (MEDIUM): **PARTIALLY RESOLVED.**
> *Decision resolves the governance disposition of the Finding; physical
> baseline establishment remains a separately authorized repository
> action.* Das Finding wird nicht als CLOSED bezeichnet, solange die
> physische Baseline nicht hergestellt ist.

## 17. Non-Effects

Nicht bewirkt: Commit/Tag/Push/Merge/Rebase/Reset/Clean/Restore · Cleanup oder Verwerfen irgendeiner Änderung · Behandlung von `src/jochen_x/**` · Coding-Freigabe (**CODING = NOT AUTHORIZED**, kein RL-05) · SPR-02-Freigabe · Schließung von Security-Findings/ODDs · Änderung irgendeiner bestehenden Datei.

## 18. Verification

| Prüfung | Ergebnis |
|---|---|
| Nur dieses eine neue Dokument erstellt | PASS |
| Keine bestehende Datei verändert (Produktivcode, Tests, Governance, Security, Baseline) | PASS |
| Keine Working-Tree-Änderung verworfen/verschoben/gelöscht | PASS |
| Git-Status unverändert bis auf dieses Dokument (12 M / 0 staged / 0 deleted wie vor Beginn) | PASS |
| Include- (13) / Exclude-Listen (70) vollständig; UNRESOLVED = 0 | PASS |
| RB-1.0 explizit geschützt (Kap. 10) | PASS |
| F-SPR01-01 korrekt disponiert (PARTIALLY RESOLVED, nicht CLOSED) | PASS |
| Coding weiterhin NOT AUTHORIZED | PASS |

## 19. Next Authorized Action

> **A) Separat autorisierter Baseline-Commit** gemäß Kap. 14/15 (Scope:
> exakt die 13 Include-Dateien) — erst nach ausdrücklicher Freigabe des
> Projekteigners; empfohlen mit anschließender RB-1.0-Nachzählung gegen
> den Commit.
>
> Erst danach: Behandlung der Frage des nächsten Sprints. **Kein SPR-02,
> kein Coding** in der Zwischenzeit. Die Governance-Disposition der
> uncommitteten ADR-/AB-Änderungen (Kap. 7.2) ist als eigener Punkt zu
> entscheiden.

---

**Ende Baseline Identifier Decision GDR-003 — JOCHEN X Milestone 1.0 (FINAL, 2026-08-09)**
