# JOCHEN X — Milestone 1.0 Sprint Planning Summary (R0)

| Feld | Wert |
|---|---|
| Dokumenttyp | Creation / Planning Summary |
| Gegenstand | `docs/milestone-1.0-sprint-plan.md` (DRAFT, 1.0 R0) |
| Datum | 2026-08-09 |
| Rolle | Senior Software Architect / Technical Program Planner / Governance-konformer Sprint Planner |
| Autorisierung | Preflight 2026-08-09 (OPTION A — SPRINT PLANNING AUTHORIZED); ausdrückliche Startfreigabe des Projekteigners |

---

## 1. Source Gate — gelesene Quellen und Status

| Quelle | Status | Verwendung |
|---|---|---|
| `docs/milestone-1.0-implementation-plan.md` | APPROVED R1.2 (2026-08-06) | Maßgebliche Planungsgrundlage — §3 (Baseline), §5.3/§5.6 (MWB), §6.3–§6.5 (Sequenz/Abhängigkeiten), §7.3 (Phasen A–D), §8.5–§8.8 (Evidence/AC/QG/GV), §9.6/§9.8, §10.5/§10.6, §11.10, Anhang A/B |
| `docs/milestone-1.0-charter.md` | APPROVED (2026-08-02) | Scope-Randbedingung |
| `docs/milestone-1.0-engineering-spec.md` | APPROVED R1 (ES-1.0) | FR/AC/QG-Referenzrahmen (unverändert übernommen) |
| `docs/architecture-book-v2.md` | APPROVED / FROZEN | Architektur-Randbedingung (GI-01) |
| `docs/development-standard-v1.1.md` | APPROVED | Lifecycle-/Governance-Randbedingung |
| `docs/baselines/bootstrap-baseline-1.0.md` | APPROVED (2026-08-01) | Baseline-Randbedingung; SPR-01-Gegenstand |
| `docs/governance/milestone-1.0-governance-closing-report-w8.md` | GOVERNANCE CLOSED | Autorisierungskette |
| `docs/governance/gr-001-governance-decision.md` (GDR-002) | FINAL — ENTSCHEIDEN (2026-08-09) | D-1..D-4 verbindlich übernommen |
| `docs/governance/implementation-plan-1.0-approval-record.md` | vorhanden (W-7) | Genehmigungsnachweis |
| `docs/governance/waiver-dev-001.md` / `waiver-amendment-001.md` / `gdr-001-…` | APPROVED / APPROVED / ENTSCHEIDEN | Randbedingungen; W-5 §6 bestätigt §9 vollständig |
| `docs/governance/milestone-1.0-sprint-planning-preflight.md` | FINAL (2026-08-09) | Startautorisierung, Blocker-Freiheit |
| `docs/core-principles-1.0.md` / `docs/security-architecture-1.0.md` / `docs/security-design-1.0.md` | APPROVED / CLOSED | Nur als genehmigte Randbedingungen; keine Security-Entscheidung getroffen |

**Ergebnis:** Alle Primärquellen vorhanden, lesbar, widerspruchsfrei. **Keine PLANNING-FINDINGs.** Kein STOP.

---

## 2. Regressionsbezugsgröße (erster Planungsschritt)

**Methode (read-only, kein Testlauf, keine Dateiänderung):**

1. Import-Analyse: 22 von 36 Testdateien importieren aus dem stillgelegten Paket `jochen_x` (`tests/unit/**` [18], `tests/recovery/**` [1], `tests/security/test_security_policies.py` [1], `tests/integration/` [3: concurrency, event_bus, runtime]). 5 weitere Dateien erwähnen `jochen_x` nur als String (Logger-Name/Pfad) — keine Zugehörigkeit zum stillgelegten Baum. `src/**` enthält keine eigenen `test_*.py`-Dateien; der „eigene Testbestand" des parallelen Baums liegt vollständig in den 22 identifizierten Dateien.
2. Testkollektion (`pytest --collect-only -q -p no:cacheprovider`):

| Menge | Tests |
|---|---|
| Repository gesamt | 1019 (deckungsgleich IP §3.1 — Konsistenznachweis) |
| Stillgelegter Baum (22 Dateien) | 761 |
| **Baseline-geführte Struktur (14 Dateien) = Regressionsbezugsgröße RB-1.0** | **258** |
| Kontrolle | 258 + 761 = 1019 ✓ |

Damit ist GDR-002 D-3 („zahlenmäßige Festlegung als erster Schritt der Sprintplanung") erfüllt. Die Repository-Gesamtzahl wurde **nicht** übernommen; keine Zahl wurde erfunden; `src/jochen_x/**` wurde **nicht** als Milestone-Bestand reaktiviert und physisch nicht angefasst.

---

## 3. Sprintstruktur

10 Sprints, exakt entlang der genehmigten Phasen (IP §7.3) und des genehmigten Abhängigkeitsgraphen (IP §6.3/§6.4):

| Sprint | Phase | Inhalt | WPs / MWBs |
|---|---|---|---|
| SPR-01 | A | Baseline Confirmation (EV-D01) | — |
| SPR-02 | B | WP-001 Platform Hardening | MWB-001/-002/-015 |
| SPR-03 | B | WP-002 Host Service & Extensibility | MWB-003/-004/-015 |
| SPR-04 | B | WP-003 Developer Experience | MWB-005/-006/-015 |
| SPR-05 | B | WP-004 Observability | MWB-007/-008/-015 |
| SPR-06 | B | WP-005 Reliability | MWB-009/-010/-015 |
| SPR-07 | B | WP-007 Documentation | MWB-011/-012/-015 |
| SPR-08 | B-Abschluss | Regression & Messreihe (EV-I01) | MWB-015 |
| SPR-09 | C | WP-006 SDK Contract Verification | MWB-013/-014/-015 |
| SPR-10 | D | Governance Closure (QG-008, GV-01..GV-08) | — |

Abdeckung: **7/7 Work Packages, 15/15 MWBs** — vollständig gegen IP §5.3/§5.6 abgeglichen, keine neuen Work Packages, keine neuen Deliverables.

## 4. Abhängigkeiten

- Normativer Graph unverändert übernommen: WP-001..WP-005, WP-007 = Provider ohne Vorgänger, parallelisierbar; WP-006 = Dependent nach Abschluss aller sechs (IP §6.4).
- Optionale, nicht blockierende Bezüge WP-002/WP-004 → WP-007 als Ausführungshinweis übernommen.
- Kein Sprint konsumiert eine laut Plan erst später entstehende Voraussetzung (SPR-08 nach allen Providern; SPR-09 nach SPR-08; SPR-10 nach SPR-09).
- Abhängigkeitsarten je Sprint gekennzeichnet: [T] technisch, [G] Governance, [D] Daten, [V] Verification, [E] Evidence.

## 5. Quality Gates

QG-001..QG-008 den Sprints zugeordnet (Sprint Plan Kap. 5) mit frühestmöglichem Abschluss gemäß IP §8.7. **Alle Gates: NOT STARTED.** Kein Gate wurde durch Planung als PASSED markiert; alle 29 AC im Ausgangsstatus NOT VERIFIED (IP §8.6).

## 6. Coding-Grenze

Explizites **Coding Authorization Gate** (Sprint Plan Kap. 6): Sprint Planning abgeschlossen ≠ Coding freigegeben. Bedingungen 7–9 (genehmigte Sprintplanung, protokollierte Baseline-Bestätigung, RL-05) sämtlich **PENDING**. Es wurde kein Code geschrieben oder geändert, keine Anwendungsdatei verändert, kein Modul/keine API/keine Datenbank implementiert, kein Deployment/Release/Trading/Wallet-Zugriff.

## 7. Verification

Verifikations- und Evidence-Anforderungen (EV-D01..D05, EV-W01..W07, EV-I01..I04, EV-G01..G04) unverändert aus IP §8.5 übernommen und den Sprints zugeordnet. Completion Conditions aus IP §8.9/§9.8/§10.8 referenziert, nicht neu definiert; nicht erfüllbare Bedingungen als PENDING mit Quelle geführt.

## 8. Offene Punkte

Register im Sprint Plan Kap. 8: OP-1 (Plan-Genehmigung), OP-2 (Coding Authorization), OP-3 (physische Behandlung `src/jochen_x/**`), OTD-1/OTD-2 (die zwei im IP als „festzulegen" ausgewiesenen Positionen in MWB-008/MWB-015 — als OPEN TECHNICAL DECISION markiert, nicht entschieden), OP-4 (R2-E-01), OP-5 (Waiver-Schließungsakt), OP-6/OP-7 (Security-Items — unverändert offen), OP-8 (Baseline-Messreihe). Kein bekanntes Non-Blocking Item wurde künstlich geschlossen.

## 9. Negativbestätigungen

- **Keine Implementierung:** kein Code geschrieben/geändert; `git status` nach Abschluss unverändert bis auf die zwei neuen Planungsdokumente.
- **Keine Governance-Änderung:** kein APPROVED-Dokument verändert; keine ADRs/RDRs; keine neuen Requirements; keine Architektur-/Security-/Baseline-Entscheidung; keine Findings/ODDs geschlossen; keine neue Planungshierarchie.
- **Kein Commit, kein Tag, kein Push.**

## 10. Erstellte Dateien

1. `docs/milestone-1.0-sprint-plan.md` — DRAFT, 1.0, R0
2. `docs/audits/milestone-1.0-sprint-planning-summary-r0.md` — dieses Dokument

---

**Ende Sprint Planning Summary R0 — JOCHEN X Milestone 1.0**
