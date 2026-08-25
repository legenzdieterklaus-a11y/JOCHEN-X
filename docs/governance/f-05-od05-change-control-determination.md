# JOCHEN X — Milestone 1.0
# F-5 — Final Change-Control / ADR-RDR / NAW-1 Determination

| Feld | Wert |
|---|---|
| Dokumenttyp | Governance Assessment (READ-ONLY, NON-IMPLEMENTING) |
| **ID** | **F-5** |
| Status | **FINAL ASSESSMENT** |
| Gegenstand | Abschließende Change-Control-Bestimmung für **OD-05 Option B**; **B-6**; **NAW-1**-Statusfortschreibung |
| Governance Input | **GR-001/GDR-002** · **GDR-OD01-001** · **GDR-OD05-001** · **G-1 HYBRID — PRECISISED** · **NAW-A** · **NAW-B** · **F-1-A** · **F-2-B** · **F-3** · **F-4** |
| Datum | 2026-08-10 |
| Branch / HEAD | `milestone-1.0-governance` / `8fcf42f1997dfcf6ff232e75fd33c37b933991c8` |
| Normcharakter | **Nicht normativ gegenüber bereits APPROVED Governance.** Keine Implementierungsautorisierung |
| Coding | **NOT AUTHORIZED** |

---

## 1. Executive Summary

F-5 schließt die Kette **NAW-A → NAW-B → F-4** ab und bestimmt, was aus den
Quellen **determinierbar** ist und was **menschlich zu entscheiden** bleibt.

**Determiniert:**

| # | Feststellung |
|---|---|
| D-1 | Die Change Surface **CS-1 + CS-2 + CS-3** ist **final und ausreichend**; keine weitere Bestandsdatei ist technisch zwingend erforderlich (Kap. 5) |
| D-2 | **§8-1, §8-2, §8-3, §8-5 = NOT TRIGGERED**; **§8-4 = TRIGGERED**. F-4 wird **bestätigt**, nicht korrigiert (Kap. 6–10) |
| D-3 | **CHANGE CONTROL = REQUIRED** — der Auslöser steht fest (Kap. 14) |
| D-4 | **ARCHITECTURE FREEZE = UNCHANGED** — F-1-A erneut bestätigt (Kap. 11) |
| D-5 | **CODING = NOT AUTHORIZED** — quellenbelegt: **RL-05 ist nicht erreicht** (Kap. 21) |

**Nicht determinierbar — menschliche Entscheidung erforderlich:**

| # | Offene Position |
|---|---|
| H-1 | **B-6 — ADR oder RDR?** In **keiner** autorisierten Quelle existiert ein Abgrenzungskriterium. Sämtliche Fundstellen nennen „ADR **oder** RDR" alternativ, ohne Zuordnungsregel (Kap. 12, 13) |
| H-2 | **Sprint-Zuordnung** — der finalisierte Umriss ist im genehmigten Sprint Plan **nicht abgedeckt** (Kap. 17) |
| H-3 | **F4-U2** — Einordnung der neu entstehenden Policy-Diskontinuität in TD-19 (Kap. 15) |

> **NAW-1-Ergebnis: D — ADR/RDR CLASSIFICATION STILL OPEN.**
> Die **Change-Control-Pflicht** ist determiniert; die **Klasse** des Instruments
> ist es nicht. Der ursprüngliche Status D wird damit **präzisiert, nicht
> aufgelöst**: aus „unbekannt, ob überhaupt" wird „feststehend, dass — offen,
> welches Instrument".

---

## 2. Source Gate

**Alle 20 Pflichtquellen vorhanden, lesbar, keine Pfadabweichung.**

| # | Quelle | Pfad | Status |
|---|---|---|---|
| 1 | F-4 | `docs/governance/f-04-od05-td19-scope-assessment.md` | FINAL ASSESSMENT |
| 2 | NAW-A | `docs/governance/naw-a-od05-change-surface-fixation.md` | FINAL / COMPLETED |
| 3 | NAW-B | `docs/governance/naw-b-g1-observable-state-contract-fixation.md` | FINAL / COMPLETED |
| 4 | G-1 Decision Brief | `docs/audits/g-01-bootstrap-behavior-interpretation-decision-brief-r0.md` | DRAFT · NON-NORMATIVE |
| 5 | OD-05 Decision | `docs/governance/od-05-governance-decision.md` | FINAL (GDR-OD05-001) |
| 6 | F-3 | `docs/governance/f-03-od05-change-surface-assessment.md` | FINAL ASSESSMENT |
| 7 | F-2 | `docs/governance/f-02-bootstrap-baseline-scope-assessment.md` | FINAL (F-2-B) |
| 8 | F-1 | `docs/governance/f-01-od05-architecture-freeze-assessment.md` | FINAL (F-1-A) |
| 9 | Bootstrap Baseline 1.0 | `docs/baselines/bootstrap-baseline-1.0.md` | **APPROVED** |
| 10 | Development Standard v1.1 | `docs/development-standard-v1.1.md` | **APPROVED** |
| 11 | Architecture Book v2.0 | `docs/architecture-book-v2.md` | **APPROVED / FROZEN** — Welt A (Kap. 3.2) |
| 12 | RDR-001 | `docs/rdr/001-bootstrap-modularization.md` | **APPROVED** |
| 13 | Implementation Plan 1.0 | `docs/milestone-1.0-implementation-plan.md` | **APPROVED R1.2** |
| 14 | Sprint Plan 1.0 | `docs/milestone-1.0-sprint-plan.md` | **DRAFT 1.0 R0** |
| 15 | OP-1 Approval | `docs/governance/milestone-1.0-sprint-planning-approval-decision-op1.md` | vorhanden |
| 16 | Master Engineering Plan R0 | `docs/audits/jochen-x-master-engineering-plan-r0.md` | R0 |
| 17 | Decision & Execution Matrix R0 | `docs/audits/jochen-x-decision-execution-matrix-r0.md` | R0 |
| 18 | Security Design 1.0 | `docs/security-design-1.0.md` | **APPROVED** |
| 19 | Security Architecture 1.0 | `docs/security-architecture-1.0.md` | **APPROVED** |
| 20 | Baseline Commit Record | `docs/governance/milestone-1.0-baseline-commit-record.md` | **FINAL** |

**Ergänzend für B-6 herangezogen (autorisierte Governance-Quellen):**
`docs/governance/gr-001-governance-decision.md` (GDR-002, FINAL),
`docs/governance/gdr-001-waiver-closing-criteria.md`, `docs/core-principles-1.0.md`.

> **SOURCE GATE: BESTANDEN.** Kein HARD STOP.

---

## 3. Baseline Reference

| Prüfung | Ergebnis |
|---|---|
| Baseline-Identifier | `MILESTONE-1.0-BASELINE = 8fcf42f1997dfcf6ff232e75fd33c37b933991c8` [SOURCE: docs/governance/milestone-1.0-baseline-commit-record.md §6] |
| HEAD zu Beginn | identisch mit der Baseline — **reproduzierbar verifiziert** |
| Staging | **leer** |
| Getrackte Modifikationen | **6** (`git diff --stat`: 6 files, +1.415/−119) |
| `src/jochen_x/**` | **0 Statuseinträge** — vollständig unangetastet |

### 3.1 Ebenentrennung

| Ebene | Verwendung in F-5 |
|---|---|
| **BASELINE** (`8fcf42f`) | **Alleinige Grundlage** aller Code-Aussagen (`git show 8fcf42f:<pfad>`) |
| **WORKING TREE** | Nur Divergenzfeststellung: die sechs Modifikationen betreffen `CLAUDE.md`, `ROADMAP.md`, ADR-005/006/007, Architecture Book — **kein** Artefakt der Change Surface |
| **UNTRACKED DOCS** | Governance-/Audit-Dokumente; **niemals** als Baseline behandelt |

### 3.2 Fassungsregel Architecture Book

Maßgeblich ist **Welt A** (`git show 8fcf42f:docs/architecture-book-v2.md`); die
Working-Tree-Fassung ist per **GDR-OD01-001 (Option C)** getrennt und noch nicht
disponiert [SOURCE: docs/governance/f-01-od05-architecture-freeze-assessment.md Kap. 2.2].

---

## 4. Governance Chain

**Als bestehender Kontext übernommen, nicht neu erfunden:**

| Entscheidung | Inhalt | Status |
|---|---|---|
| **GR-001 / GDR-002** | `src/jochen_x/**` = **STILLLEGUNG**; produktiver Baum = baseline-geführte Struktur | **FINAL** [SOURCE: docs/governance/gr-001-governance-decision.md §8 D-1/D-2] |
| **GDR-OD01-001** | OD-01 = **OPTION C** — getrennte Behandlung der Dokumentgruppen | **FINAL** |
| **GDR-OD05-001** | OD-05 = **OPTION B** — „Policy-Konfiguration in die bestehende `PluginSecurityStage` ziehen (ohne Reihenfolgeänderung)" | **FINAL** |
| **G-1** | **OPTION HYBRID — PRECISISED** (durch NAW-B): wirkungsbezogene Auslegung von §8-4 einschließlich beobachtbarer State-Contract-Werte | **PRECISISED** |
| **NAW-A** | Change Surface fixiert: **CS-1 + CS-2 + CS-3**; `[security]` = OPTIONAL; kein neues öffentliches Symbol | **COMPLETED** |
| **NAW-B** | `run_phase()` = **CHANGED**; `begin()` / `build_context()` = UNCHANGED; **§8-4 = TRIGGERED**; **CHANGE CONTROL = REQUIRED** | **COMPLETED** |
| **F-4** | **TD-19 = PARTIALLY IMPACTED** (Dimension: Policy-Kontinuität); T-a, T-b, T-c **OPEN**; **keine** Change-Surface-Erweiterung | **COMPLETED** |

---

## 5. Final Change Surface

### 5.1 Der finalisierte Umriss

| ID | Artefakt | Zweck | Klasse |
|---|---|---|---|
| **CS-1** | `app/bootstrap/stages_plugin.py` — `PluginSecurityStage.execute` | Übergabe der konfigurierten Policies an die bestehende Security-Instanz | **REQUIRED** |
| **CS-2** | `config/settings.py` | Zugang zur `[security]`-Abbildung | **REQUIRED** |
| **CS-3** | `config/default.toml` | Optionaler `[security]`-Abschnitt | **REQUIRED** |

[SOURCE: docs/governance/naw-a-od05-change-surface-fixation.md Kap. 6;
docs/governance/f-04-od05-td19-scope-assessment.md Kap. 14]

### 5.2 Frage 1 — Sind die drei Dateien ausreichend?

> **JA.**

| # | Begründung | Beleg |
|---|---|---|
| V-1 | Die Admission vollzieht sich vollständig in `PluginSecurityStage.execute` (LOAD_PLUGINS), Schritte 1–4 | [SOURCE: BASELINE 8fcf42f:app/bootstrap/stages_plugin.py:271–333] |
| V-2 | Die maßgebliche `PluginSecurity`-Instanz wird in **derselben Stage** erzeugt (`except LookupError`) | [SOURCE: BASELINE 8fcf42f:app/bootstrap/stages_plugin.py:262–266] |
| V-3 | Es existieren genau **zwei** Registrierungsstellen für `PluginSecurity` und **keine vor LOAD_PLUGINS** — der `LookupError`-Zweig greift stets | [SOURCE: docs/governance/f-04-od05-td19-scope-assessment.md Kap. 9.1, 9.2] |
| V-4 | `PluginSecurity.__init__` nimmt `integrity_policy` und `permission_policy` **bereits** entgegen | [SOURCE: BASELINE 8fcf42f:app/security/plugin_security.py:`PluginSecurity.__init__`] |
| V-5 | Beide `from_config`-Fabriken existieren bereits und sind **total** | [SOURCE: BASELINE 8fcf42f:app/security/plugin_security.py:`IntegrityPolicy.from_config`, `PermissionPolicy.from_config`] |

**Präzisierung zu CS-1:** Die bestehende Importzeile lautet
`from app.security.plugin_security import IntegrityPolicy, PluginSecurity`
[SOURCE: BASELINE 8fcf42f:app/bootstrap/stages_plugin.py:257]. `PermissionPolicy`
ist dort **nicht** importiert. Eine Ergänzung dieses Imports läge **innerhalb von
CS-1** und ist **keine** Änderungsflächen-Erweiterung — die importierte Datei
selbst wird nicht verändert.

### 5.3 Frage 2 — Ist eine weitere Bestandsdatei technisch zwingend erforderlich?

> **NEIN.**

**Ausdrückliche Bestätigung für die fünf im Auftrag genannten Dateien:**

| Datei | Erforderlich? | Beleg |
|---|---|---|
| `app/security/plugin_security.py` | **NEIN** | V-4, V-5 — beide Erweiterungspunkte existieren |
| `app/security/security_manager.py` | **NEIN** | F-4 Frage A = JA; die FINALIZE-Instanz beeinflusst die Admission nicht und hat keinen produktiven Konsumenten [SOURCE: docs/governance/f-04-od05-td19-scope-assessment.md Kap. 9.4, 12.2] |
| `ui/navigation/navigation_service.py` | **NEIN** | Stage-Zusammensetzung unverändert; Desktop-Komposition unberührt |
| `core/registry.py` | **NEIN** | TD-06-Symptomort; nicht Gegenstand von Option B |
| `sdk/context.py` | **NEIN** | TD-04-Gebiet — **NOT AUTHORIZED durch OD-05** [SOURCE: docs/governance/od-05-governance-decision.md Kap. 12.1] |

> **CHANGE-SURFACE EXPANSION REQUIRED: NEIN.**
> Es wurde keine Erweiterung vorgenommen und keine autorisiert.
> **Frage 3 entfällt** (nur bei JA einschlägig).

---

## 6. §8-1 Assessment — Paketstruktur

| Prüfung gegen den finalen Umriss | Befund |
|---|---|
| Modul im Bootstrap-Paket hinzugefügt, entfernt, umbenannt? | **NEIN** — CS-1 ändert eine Methode in einem bestehenden Modul; CS-2 und CS-3 liegen außerhalb des Baseline-Scopes §2 (sieben `app/bootstrap/`-Module) |

> ## **§8-1 = NOT TRIGGERED**
> [SOURCE: docs/baselines/bootstrap-baseline-1.0.md §2, §8]

---

## 7. §8-2 Assessment — Runtime-Pipeline

| Prüfung | Befund |
|---|---|
| Phasenreihenfolge | **unverändert** — `StartupPhase` unberührt |
| Stage-Reihenfolge | **unverändert** — konstitutiver Bestandteil von Option B |
| Admission-Reihenfolge (Integrity → API-Version → Permission → Dependency → Activation) | **unverändert** — CS-1 betrifft die Policy-Übergabe, nicht die Schrittfolge |
| Baseline §4 Invariante 6 („sicherheitskritisch") | **gewahrt** |

> ## **§8-2 = NOT TRIGGERED**
> [SOURCE: docs/governance/od-05-governance-decision.md Kap. 8; docs/baselines/bootstrap-baseline-1.0.md §4 Inv. 6, §5.2, §8]

---

## 8. §8-3 Assessment — Public Exports

| Prüfung | Befund |
|---|---|
| `__all__` in `app/bootstrap/__init__.py` geändert? | **NEIN** — NAW-A Festlegung B; die 20 Symbole bleiben identisch |
| Ausgestaltungsvorbehalt aus F-3? | **entfallen** — durch NAW-A determinat geschlossen |

> ## **§8-3 = NOT TRIGGERED**
> [SOURCE: docs/governance/naw-a-od05-change-surface-fixation.md Kap. 5, 10.3; BASELINE 8fcf42f:app/bootstrap/__init__.py]

---

## 9. §8-4 Assessment — BootstrapManager (unter G-1 HYBRID — PRECISISED)

### 9.1 Erneute Prüfung gegen den finalen Umriss

| Methode | Ergebnis | Begründung |
|---|---|---|
| `begin()` | **UNCHANGED** | erzeugt nur einen frischen `BootstrapContext`; vom Umriss unberührt [SOURCE: BASELINE 8fcf42f:app/bootstrap/manager.py:`begin`] |
| `run_phase()` | **CHANGED** | `context.admitted_manifests` und der registrierte `PluginCatalog` sind nach **NAW-B** Bestandteil des beobachtbaren Kontrakts; der Umriss macht sie **konfigurationsabhängig** [SOURCE: docs/governance/naw-b-g1-observable-state-contract-fixation.md Kap. 6, 7, 9, 10] |
| `build_context()` | **UNCHANGED** | die 12 über `_require` geprüften Felder sind unberührt; `admitted_manifests` fließt nicht ein [SOURCE: BASELINE 8fcf42f:app/bootstrap/manager.py:`build_context`] |

**Beide in F-3 identifizierten Unbestimmtheitsgründe sind aufgelöst:**

| Grund | Auflösung |
|---|---|
| **R-3** — neuer `BootstrapError`-Pfad in INITIALIZE | **entfallen** durch NAW-A (`[security]` = OPTIONAL) |
| **F3-U2 / R-5** — Einordnung der Zustandswerte | **entschieden** durch NAW-B (Kontraktbestandteil) |

### 9.2 Bestätigung oder Korrektur von F-4?

> **F-4 wird BESTÄTIGT.** F-5 findet keinen Sachverhalt, der eine Korrektur
> erforderte. Die von F-4 festgestellte **Policy-Diskontinuität** (Kap. 15) tritt
> **zusätzlich** zur bereits festgestellten Kontraktänderung auf und ändert das
> §8-4-Ergebnis nicht.

> ## **§8-4 = TRIGGERED**

---

## 10. §8-5 Assessment — `default_stages()`

| Prüfung | Befund |
|---|---|
| Stage-**Zusammensetzung** | **unverändert** — weiterhin 13 Stages |
| Stage-**Reihenfolge** | **unverändert** — `PluginSecurityStage()` an Position 9 |
| `BootstrapManager(stages=…)`-Signatur | **unberührt** |

> ## **§8-5 = NOT TRIGGERED**
> [SOURCE: BASELINE 8fcf42f:app/bootstrap/manager.py:`default_stages`]

---

## 11. Architecture Freeze

| Prüfung | Befund |
|---|---|
| **AB §22.1** — enumerierter Freeze-Scope | `app/security/**` **nicht enthalten**; `config/**` **nicht enthalten**; für `app/bootstrap` verengt auf **BootstrapStage-Protocol** und **StartupPhase-Enum** — beide vom Umriss unberührt [SOURCE: BASELINE 8fcf42f:docs/architecture-book-v2.md §22.1] |
| **AB §22.3** — ADR-pflichtige Änderungen | **keiner der sieben Tatbestände** ausgelöst; insbesondere keine Änderung der Bootstrap-Phasenreihenfolge [SOURCE: ebd. §22.3] |
| Bootstrap-Freeze-Scope ↔ Change Surface | keine Überschneidung |
| Neuer Befund aus F-4/F-5, der F-1-A widerspricht? | **NEIN** |

> ## **ARCHITECTURE FREEZE = UNCHANGED** (F-1-A bestätigt)
>
> Kein Architecture Book geändert, **keine AB-Version erstellt**.

---

## 12. ADR/RDR Source Analysis

**Erschöpfende Prüfung aller autorisierten Quellen auf ein
Abgrenzungskriterium zwischen ADR und RDR.**

| # | Quelle | Fundstelle | Enthält ein Abgrenzungskriterium? | Klasse |
|---|---|---|---|---|
| Q-1 | Bootstrap Baseline 1.0 §8 | „erfordert eine genehmigte Governance-Entscheidung in Form von: einem neuen **ADR** …, **oder** einem neuen **RDR** …" | **NEIN** — reine Alternative | **SOURCE FACT** |
| Q-2 | Bootstrap Baseline 1.0 §1 | „sofern keine genehmigte Governance-Änderung (**ADR oder RDR**) eine Abweichung autorisiert" | **NEIN** | **SOURCE FACT** |
| Q-3 | Development Standard v1.1 §13 | Acht **ADR**-Auslöser; ADR-Format; „Architecture Freeze und ADRs" | **NEIN** — enthält **keine RDR-Regel**; Volltextsuche „RDR": **0 Treffer** im gesamten Dokument | **SOURCE FACT** |
| Q-4 | Architecture Book v2.0 §22.3 | „ADR-pflichtige Änderungen" — sieben Tatbestände | **NEIN** — RDR wird nicht erwähnt | **SOURCE FACT** |
| Q-5 | RDR-001 | Kopf: „Typ: Refactoring Decision Record"; §2.2 „Keine Architekturänderungen · Keine Verhaltensänderungen · Keine öffentlichen API-Änderungen"; §7 Nr. 7 „Keine ADR-Änderungen erforderlich" | **NEIN** — Selbstbeschreibung **eines** Falls, keine allgemeine Abgrenzungsregel | **SOURCE FACT** |
| Q-6 | **GDR-002 (GR-001)** §7 Frage 4 / §8 D-4 | „**ADR/RDR nur bei Baseline-Berührung**" · „Ein ADR oder RDR ist **nicht erforderlich**" | **NEIN für die Klassenwahl** — bestimmt den **Auslöser** (Baseline-Berührung), **nicht** das Instrument | **SOURCE FACT** |
| Q-7 | GDR-001 (Waiver Closing Criteria) | „Dieses Dokument ist **kein ADR und kein RDR**" · „wäre zusätzlich ein **ADR oder RDR** erforderlich" | **NEIN** | **SOURCE FACT** |
| Q-8 | Implementation Plan 1.0 | **GC-06**: „Änderungen an der Bootstrap Baseline 1.0 erfordern einen genehmigten **ADR oder RDR** vor der Implementierung" | **NEIN** | **SOURCE FACT** |
| Q-9 | Core Principles 1.0 | führt RDR-001 als APPROVED-Bestand; keine ADR/RDR-Abgrenzungsregel | **NEIN** | **SOURCE FACT** |
| Q-10 | Sprint Planning Summary R0 | „keine ADRs/RDRs" — Nicht-Wirkungs-Aussage | **NEIN** | **SOURCE FACT** |

### 12.1 Zusammenfassender Quellenbefund

> **In keiner autorisierten Quelle existiert ein Kriterium, das bestimmt, wann
> ein ADR und wann ein RDR zu wählen ist.** Sämtliche neun einschlägigen
> Fundstellen nennen beide Instrumente **alternativ** und **gleichrangig**.
> **Kein Quellenwiderspruch** — die Quellen sind untereinander konsistent; es
> fehlt schlicht die Regel.

### 12.2 Beobachtung zum Präzedenzfall — ausdrücklich INFERENCE

| Merkmal | RDR-001 (Präzedenz) | OD-05-Umriss |
|---|---|---|
| Charakter | **verhaltensbewahrend** — „Keine Verhaltensänderungen" [SOURCE: docs/rdr/001-bootstrap-modularization.md §2.2] | **verhaltensändernd** — `run_phase()` = **CHANGED** (Kap. 9.1) |
| Ausgelöste §8-Tatbestände | Paketstruktur (§8-1) **und** Public Exports (§8-3) | **§8-4** |
| Selbstaussage zu ADR | „Keine ADR-Änderungen erforderlich" [SOURCE: ebd. §7 Nr. 7] | — |

> **Klassifikation: INFERENCE — kein Kriterium.** Der einzige RDR-Präzedenzfall
> war ein struktureller, verhaltensbewahrender Umbau; der OD-05-Umriss ist
> strukturell unauffällig, aber verhaltensändernd. **Aus dieser Beobachtung wird
> kein allgemeines Kriterium konstruiert und keine Instrumentenwahl abgeleitet.**
> Sie wird ausschließlich als Entscheidungsmaterial für die menschliche
> Governance-Entscheidung festgehalten.

---

## 13. B-6 Determination

**Mögliche Ergebnisse laut Auftrag: (A) Kriterium existiert · (B) kein Kriterium ·
(C) Quellenwiderspruch.**

| Prüfung | Ergebnis |
|---|---|
| Existiert ein autorisiertes Kriterium? | **NEIN** (Kap. 12) |
| Widersprechen sich die Quellen? | **NEIN** — konsistente Alternativnennung |

> ## **B-6 = UNRESOLVED / HUMAN GOVERNANCE DECISION REQUIRED**
> **(Ergebnis B)**

**Es wird weder ADR noch RDR ausgewählt.** Es wird kein ADR und kein RDR
erstellt. Es wird kein Kriterium aus Präzedenzfällen konstruiert.

**Entscheidungsmaterial für die menschliche Instanz** (Feststellungen, keine
Empfehlung):

| # | Material |
|---|---|
| M-1 | Beide Instrumente sind in allen Quellen **gleichrangig alternativ** genannt |
| M-2 | Der Development Standard regelt **nur ADR** (§13: Auslöser, Format, Freeze-Bezug) und enthält **keine** RDR-Regel |
| M-3 | Der einzige RDR-Präzedenzfall (RDR-001) war **verhaltensbewahrend**; der vorliegende Umriss ist **verhaltensändernd** (Kap. 12.2, INFERENCE) |
| M-4 | Keiner der acht ADR-Auslöser des Development Standard §13 und keiner der sieben AB-§22.3-Tatbestände ist erfüllt (Kap. 11; [SOURCE: docs/governance/f-01-od05-architecture-freeze-assessment.md Kap. 7.3, 10]) |
| M-5 | Die Pflicht folgt hier **allein** aus Bootstrap Baseline §8-4 — nicht aus dem Architecture Freeze und nicht aus Development Standard §13 |

---

## 14. Change-Control Determination

**Saubere Trennung der Ebenen:**

| Ebene | Status | Beleg |
|---|---|---|
| **1 — Ist Change Control ausgelöst?** | **JA — REQUIRED** | §8-4 = TRIGGERED (Kap. 9); Bootstrap Baseline §8; IP **GC-06** |
| **2 — Welches Instrument (ADR oder RDR)?** | **OPEN — HUMAN DECISION REQUIRED** | Kap. 13 |
| **3 — Ist das Instrument erstellt?** | **NEIN** | F-5 erstellt keines |
| **4 — Ist die Umsetzung autorisiert?** | **NEIN** | Kap. 21 |

> **§8-4 = TRIGGERED bedeutet CHANGE CONTROL REQUIRED. Es bedeutet NICHT
> automatisch ADR REQUIRED und NICHT automatisch RDR REQUIRED.**

**Verfahrensfolge:** IP **GC-06** verlangt die genehmigte Governance-Entscheidung
ausdrücklich **„vor der Implementierung"**
[SOURCE: docs/milestone-1.0-implementation-plan.md GC-06]. Diese Bedingung ist
**anwendbar und nicht erfüllt**, solange B-6 offen ist.

---

## 15. TD-19 Interaction

| Prüfung | Ergebnis |
|---|---|
| **TD-19 = PARTIALLY IMPACTED** weiterhin korrekt? | **JA** — F-5 findet keinen abweichenden Sachverhalt |
| **F4-U2** (Policy-Diskontinuität) korrekt weitergeführt? | **JA** — als **UNKNOWN / OPEN DECISION** geführt |
| Ist F4-U2 durch Quellen determinierbar? | **NEIN.** Der dokumentierte TD-19-Wortlaut (R0 §10.6) benennt **Instanz-Ersetzung** und **Trust-Ledger-Diskontinuität**; eine **Policy**-Dimension ist dort nicht genannt. Ob sie vom bestehenden Wortlaut erfasst ist oder gesondert zu führen wäre, ist keiner Quelle zu entnehmen → **UNKNOWN / HUMAN REVIEW REQUIRED** |
| **T-a** (Instanz-Ersetzung) | **OPEN** |
| **T-b** (Trust-Ledger-Diskontinuität) | **OPEN** |
| **T-c** (Wirkungslosigkeit für Admission) | **OPEN** |
| **SG-E / TG-3** | **weiterhin offen / nicht erbracht** [SOURCE: docs/audits/jochen-x-master-engineering-plan-r0.md §26, §15.4] |
| **QG-006** | **NOT STARTED** [SOURCE: ebd. §24.3] |

> **F-5 löst TD-19 nicht, erfindet keine neue Technical-Debt-Position und
> schließt keine bestehende.**

---

## 16. Security Impact

| Position | Status nach F-5 |
|---|---|
| **ODD-17** | **OPEN** — nicht berührt |
| **OD-04** | **OPEN** — Permission-Modelle bleiben **beratend, nicht erzwingend** [SOURCE: docs/audits/jochen-x-master-engineering-plan-r0.md §10.4 SEC-04] |
| **TD-04** | **OPEN / NOT AUTHORIZED** |
| **TD-05** | **OPEN** — der Umriss adressiert den Konfigurationsweg, schließt ihn nicht |
| **TD-06** | **OPEN** |
| **TD-19** | **OPEN — PARTIALLY IMPACTED** |
| **TD-21** | **OPEN** |
| **SG-C / SG-D / SG-E** | **nicht erfüllt bzw. nicht nachgewiesen** |
| **TG-2 / TG-3 / TG-4** | **erforderlich, nicht erbracht** |
| **QG-006** | **NOT STARTED** |
| **RB-1.0** | **unverändert (258/14)** |

> **Keine dieser Positionen wird geschlossen.** Keine Security Design Revision,
> keine Security ADR, keine Security-Freigabe.

---

## 17. Sprint Alignment

| Prüfung | Befund | Beleg |
|---|---|---|
| Enthält der Sprint Plan eine Zuordnung für **OD-05**, „Security-Verdrahtung", **TD-19** oder **TD-05**? | **NEIN — 0 Fundstellen** | Volltextprüfung von `docs/milestone-1.0-sprint-plan.md` |
| Hat OD-05 eine eigene Sprint-/WP-Zuordnung? | **NEIN** — „Kein FR; berührt Bootstrap Baseline §8" | [SOURCE: docs/audits/jochen-x-master-engineering-plan-r0.md §24.2] |
| Welche WPs sind betroffen? | **WP-003** (SPR-04) und **WP-004** (SPR-05) — über **QG-006** | [SOURCE: ebd. §23.3 V-4, §24.3; docs/audits/jochen-x-decision-execution-matrix-r0.md §D-3] |
| Decken deren Deliverables den Umriss ab? | **NEIN** — SPR-04/WP-003 betrifft Autorenvorgaben und Ablehnungs-Feedback (FR-005, FR-006); SPR-05/WP-004 betrifft Observability. Eine Policy-Konfiguration ist in keinem der beiden Deliverable-Sätze vorgesehen | [SOURCE: docs/milestone-1.0-sprint-plan.md SPR-04, SPR-05] |
| Sprint-Plan-Status | **DRAFT 1.0 R0**, als Planungsgrundlage genehmigt | [SOURCE: docs/milestone-1.0-sprint-plan.md Kopf] |

> **Ergebnis: PROPOSED CHANGE / GOVERNANCE DECISION REQUIRED.**
> Der finalisierte Umriss ist im genehmigten Sprint Plan **nicht abgedeckt**.
> **F-5 erzeugt keinen Sprint, kein Work Package und ändert keine bestehende
> Zuordnung.** Der Sprint Plan bleibt unverändert.

---

## 18. NAW-1 Status

**Ursprüngliche Frage:** Welche ADR/RDR-/Change-Control-Konsequenz hat OD-05
Option B? — **Ursprünglicher Status: D — UNKNOWN / HUMAN REVIEW REQUIRED**
[SOURCE: docs/governance/naw-01-od05-adr-rdr-assessment.md Kap. 10].

**Prüfung der fünf möglichen Ergebnisse:**

| Option | Trägt die Quellenlage sie? |
|---|---|
| **A — DETERMINED / NO ADR-RDR REQUIRED** | **NEIN** — §8-4 = TRIGGERED (Kap. 9) |
| **B — ADR REQUIRED** | **NEIN** — kein Auslöser aus Development Standard §13 oder AB §22.3; kein Kriterium, das ADR gegenüber RDR bestimmte (Kap. 12, 13) |
| **C — RDR REQUIRED** | **NEIN** — kein autorisiertes Kriterium; der einzige Präzedenzfall ist nicht übertragbar (Kap. 12.2, INFERENCE) |
| **D — ADR/RDR CLASSIFICATION STILL OPEN** | **JA** |
| **E — CHANGE-SURFACE / GOVERNANCE BLOCKER REMAINS** | **teilweise zutreffend, aber nicht die Antwort auf die NAW-1-Frage** — die Change Surface ist final (Kap. 5); der verbleibende Blocker ist genau die Klassifikationsfrage (= D). Die Sprint-Zuordnung (Kap. 17) ist eine **separate** Governance-Position |

> ## **NAW-1 = D — ADR/RDR CLASSIFICATION STILL OPEN**

**Fortschreibung gegenüber dem ursprünglichen Status D — was sich geändert hat:**

| Aspekt | NAW-1 (ursprünglich) | nach F-5 |
|---|---|---|
| Ob überhaupt Change Control greift | **UNKNOWN** | **DETERMINED — REQUIRED** |
| §8-1, §8-2, §8-3, §8-5 | teils mit Vorbehalt | **determinat NOT TRIGGERED** |
| §8-4 | **UNKNOWN** | **TRIGGERED** |
| Change Surface | offen | **final: CS-1 + CS-2 + CS-3** |
| Architecture Freeze | offen (B-5) | **UNCHANGED** (F-1-A) |
| **Instrumentenwahl ADR ↔ RDR** | offen (B-6) | **weiterhin offen** |

> Der Status **D** bleibt, sein **Inhalt** hat sich jedoch von „unbekannt, ob
> überhaupt" zu „feststehend, dass — offen, welches Instrument" verschoben.

---

## 19. Remaining UNKNOWNs

| ID | Frage | Status | Zuständig |
|---|---|---|---|
| **B-6 / F4-U4** | Abgrenzungskriterium **ADR ↔ RDR** | **UNRESOLVED — HUMAN GOVERNANCE DECISION REQUIRED** | Projekteigner / Governance |
| **F4-U2** | Einordnung der Policy-Diskontinuität in TD-19 | **UNKNOWN / HUMAN REVIEW REQUIRED** (Kap. 15) | Security-/Architektur-Governance |
| **F4-U1 / U-3** | „teilweise"-Restumfang von TD-19 | **UNKNOWN** — F-4 hat präzisiert, dass T-a/T-b/T-c vollständig offen bleiben | — |
| **F4-U3** | Ob künftig ein Konsument der FINALIZE-Instanz entsteht | **UNKNOWN** — nicht ohne Laufzeit-/Zukunftsannahme feststellbar; **kein Test ausgeführt** | — |
| **NAW-A-U1** | Wahl zwischen den CS-2-Varianten **V-1** / **V-2** | **OFFEN** — V-1 als bevorzugt ausgewiesen, nicht festgelegt | autorisierte Umsetzung |
| **NAW-A-U2 / C-3** | Z-1 (`save_profile`), Z-2 (einstufiger `_merge`), Typprüfung an der `[security]`-Zugriffsstelle | **OFFEN** | autorisierte Umsetzung |
| **F5-U1** | Sprint-/WP-Zuordnung des Umrisses | **OPEN — GOVERNANCE DECISION REQUIRED** (Kap. 17) | Projekteigner |

> Es wurde kein Test ausgeführt, um ein UNKNOWN künstlich zu beseitigen.

---

## 20. Human Decisions Required

| # | Entscheidung | Warum menschlich | Autorität |
|---|---|---|---|
| **HD-1** | **B-6 — ADR oder RDR?** | Kein autorisiertes Kriterium existiert (Kap. 13). Eine Auswahl durch den Analysten wäre eine verdeckte Governance-Setzung | **Projekteigner + Architektur-/Security-Governance** |
| **HD-2** | **Sprint-/WP-Zuordnung** des finalisierten Umrisses | Der Umriss ist im genehmigten Sprint Plan nicht abgedeckt (Kap. 17) | **Projekteigner** |
| **HD-3** | **F4-U2** — Einordnung der Policy-Diskontinuität in TD-19 | Quellen tragen keine Determination (Kap. 15) | **Security-/Architektur-Governance** |
| **HD-4** | **Erstellung** des gewählten Instruments (ADR **oder** RDR) — nach HD-1 | F-5 erstellt keines | **Projekteigner / Governance** |

---

## 21. Implementation Boundary

**Ausdrücklich getrennt von der Change-Control-Bestimmung.**

| # | Bedingung nach IP §10.6 „Coding" | Status | Beleg |
|---|---|---|---|
| 7 | Eine **genehmigte Sprintplanung** liegt vor | Sprint Plan trägt **DRAFT 1.0 R0**; zusätzlich ist der Umriss darin **nicht abgedeckt** (Kap. 17) | [SOURCE: docs/milestone-1.0-sprint-plan.md Kopf] |
| 8 | **Baseline-Bestätigung** gemäß Kap. 3.8 protokolliert (Phase A abgeschlossen) | Baseline Commit Record §12 hält ausdrücklich fest: **„Dieser Commit bedeutet nicht: RL-05 erreicht · Coding freigegeben · SPR-02 freigegeben"** | [SOURCE: docs/governance/milestone-1.0-baseline-commit-record.md §12] |
| 9 | **Readiness Level RL-05 ist erreicht** | **RL-02 bis RL-05: Nicht erreicht** | [SOURCE: docs/milestone-1.0-implementation-plan.md §10.7 „Aktueller Stand"] |

**Zusätzlich einschlägig:** IP **GC-06** — genehmigte Governance-Entscheidung
**vor** der Implementierung; wegen HD-1 nicht erfüllt (Kap. 14).
Ferner: „Umsetzung von Produktionscode **vor** Erreichen von RL-05" ist im
Implementation Plan ausdrücklich als unzulässig geführt
[SOURCE: docs/milestone-1.0-implementation-plan.md §10, Ausschlusstabelle].

> ## **CODING = NOT AUTHORIZED**
>
> Quellenbelegt: **Bedingung 9 (RL-05) ist nicht erreicht.** Selbst wenn Change
> Surface, §8-Prüfung, Change-Control-Bestimmung und Instrumentenwahl vollständig
> vorlägen, folgte daraus **keine** Coding Authorization.
>
> **F-5 ist keine Implementierungsfreigabe.**

---

## 22. Findings

| # | Finding | Klasse |
|---|---|---|
| **F-5-01** | Change Surface **CS-1 + CS-2 + CS-3** ist final und ausreichend; keine Erweiterung erforderlich | **DETERMINED** |
| **F-5-02** | Die Ergänzung des `PermissionPolicy`-Imports läge **innerhalb** von CS-1 und ist keine Flächenerweiterung | **EXISTING** |
| **F-5-03** | §8-1, §8-2, §8-3, §8-5 = **NOT TRIGGERED**; §8-4 = **TRIGGERED** | **DETERMINED** |
| **F-5-04** | **F-4 wird bestätigt**, nicht korrigiert | **DETERMINED** |
| **F-5-05** | **Architecture Freeze = UNCHANGED** (F-1-A bestätigt) | **DETERMINED** |
| **F-5-06** | **CHANGE CONTROL = REQUIRED** | **DETERMINED** |
| **F-5-07** | **In keiner der zehn geprüften autorisierten Quellen** existiert ein ADR-↔-RDR-Abgrenzungskriterium; **kein Quellenwiderspruch**, sondern eine **Regelungslücke** | **SOURCE FACT** |
| **F-5-08** | Der einzige RDR-Präzedenzfall ist **verhaltensbewahrend**, der vorliegende Umriss **verhaltensändernd** — Beobachtung, **kein Kriterium** | **INFERENCE** |
| **F-5-09** | **B-6 = UNRESOLVED** — menschliche Governance-Entscheidung erforderlich | **HUMAN DECISION REQUIRED** |
| **F-5-10** | Der Umriss ist im genehmigten Sprint Plan **nicht abgedeckt** (0 Fundstellen; WP-003/WP-004-Deliverables decken ihn inhaltlich nicht) | **PROPOSED CHANGE** |
| **F-5-11** | **NAW-1 = D** — Change-Control-Pflicht determiniert, Instrumentenklasse offen | **DETERMINED / OPEN** |
| **F-5-12** | **CODING = NOT AUTHORIZED** — **RL-05 nicht erreicht** | **SOURCE FACT** |

---

## 23. Repository Integrity

| Prüfung | Vor F-5 | Nach F-5 |
|---|---|---|
| HEAD | `8fcf42f1997dfcf6ff232e75fd33c37b933991c8` | **unverändert** |
| Baseline-Hash | `8fcf42f1997dfcf6ff232e75fd33c37b933991c8` | **unverändert** |
| `git diff --stat` | 6 files, +1.415/−119 | **unverändert** |
| `git diff --cached --stat` | leer | **leer — kein Staging** |
| Getrackte Modifikationen | 6 | **6** |
| Untracked (`-uall`) | 81 | 82 — **+1**: dieses Dokument |
| Bestandsdateien geändert | — | **0** |
| Produktivcode / Tests / Konfiguration | — | **unverändert** |
| `src/jochen_x/**` | 0 Statuseinträge | **0 — unangetastet** |
| Commit / Tag / Push / Cleanup / Löschen / Verschieben / Umbenennen | — | **KEINE** |

**BASELINE ≠ WORKING TREE ≠ UNTRACKED DOCS** — sämtliche Code-Aussagen
ausschließlich über `git show 8fcf42f:<pfad>`.

---

## 24. Final Status

| Feld | Wert |
|---|---|
| **F-5** | **COMPLETED** |
| **CHANGE SURFACE** | **CS-1 + CS-2 + CS-3 — FINAL**, keine Erweiterung |
| **§8-1** | **NOT TRIGGERED** |
| **§8-2** | **NOT TRIGGERED** |
| **§8-3** | **NOT TRIGGERED** |
| **§8-4** | **TRIGGERED** |
| **§8-5** | **NOT TRIGGERED** |
| **ARCHITECTURE FREEZE** | **UNCHANGED** (F-1-A) |
| **CHANGE CONTROL** | **REQUIRED** |
| **ADR/RDR** | **OPEN — HUMAN DECISION REQUIRED** |
| **B-6** | **UNRESOLVED** |
| **NAW-1** | **D — ADR/RDR CLASSIFICATION STILL OPEN** |
| **TD-19** | **PARTIALLY IMPACTED — OPEN** |
| **TD-04** | **OPEN / NOT AUTHORIZED** |
| **TD-05 / TD-06 / TD-21** | **OPEN** |
| **ODD-17 / OD-04** | **OPEN** |
| **SG-C / SG-D / SG-E** | **nicht erfüllt / nicht nachgewiesen** |
| **TG-2 / TG-3 / TG-4** | **erforderlich, nicht erbracht** |
| **QG-006** | **NOT STARTED** |
| **RB-1.0** | **unverändert (258/14)** |
| **Sprint Plan** | **unverändert** — Zuordnung **PROPOSED CHANGE** |
| **RL-05** | **NICHT ERREICHT** |
| **CODING** | **NOT AUTHORIZED** |
| **TESTS** | **NOT EXECUTED** |

---

## 25. Next Authorized Governance Step

> **Keine dieser Positionen wird durch F-5 ausgeführt oder ausgelöst.**

| # | Schritt | Gegenstand | Autorität | Status |
|---|---|---|---|---|
| **1** | **HD-1 — B-6-Entscheidung** | Festlegung, ob die nach §8-4 erforderliche Change-Control-Aktion als **ADR** oder als **RDR** zu führen ist. **Alleiniger verbleibender Blocker** der NAW-1-Auflösung | **Projekteigner + Architektur-/Security-Governance** | **OPEN — HUMAN DECISION REQUIRED** |
| **2** | **HD-4 — Erstellung des Instruments** | nach HD-1; eigener, gesondert zu autorisierender Auftrag | Projekteigner / Governance | **NICHT AUTORISIERT** |
| **3** | **HD-2 — Sprint-/WP-Zuordnung** | Der Umriss ist im Sprint Plan nicht abgedeckt | Projekteigner | **OPEN** |
| **4** | **HD-3 — F4-U2** | Einordnung der Policy-Diskontinuität in TD-19 | Security-/Architektur-Governance | **OPEN** |
| **5** | **Umsetzungsautorisierung** | Erst nach 1–4 **und** Erreichen von **RL-05** gemäß IP §10.6 Bedingungen 7–9 | Projekteigner | **NICHT ERTEILT** |

**Empfohlene Reihenfolge (Feststellung, keine Autorisierung):** HD-1 zuerst — es
ist die einzige Position, die den NAW-1-Status unmittelbar fortschreibt. HD-2 und
HD-3 sind davon unabhängig und können parallel geführt werden.

---

**Ende F-5 Final Change-Control / ADR-RDR / NAW-1 Determination — JOCHEN X
Milestone 1.0 (FINAL ASSESSMENT, 2026-08-10) — Bezugs-Baseline
`MILESTONE-1.0-BASELINE = 8fcf42f1997dfcf6ff232e75fd33c37b933991c8`**
