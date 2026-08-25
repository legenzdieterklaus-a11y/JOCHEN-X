# JOCHEN X — Decision & Execution Matrix

| Feld | Wert |
|---|---|
| Dokumenttyp | Entscheidungs- und Ausführungsmatrix |
| **Status** | **DRAFT** |
| **Classification** | **NON-NORMATIVE** |
| Revision | R0 |
| Datum | 2026-08-10 |
| Phase | Phase 0.1 — READ-ONLY |
| **Einzige Primärquelle** | [`docs/audits/jochen-x-master-engineering-plan-r0.md`](jochen-x-master-engineering-plan-r0.md) (DRAFT, R0, NON-NORMATIVE) |
| Wirkung | **Keine.** Analyse- und Entscheidungsvorbereitungsartefakt. Keine Genehmigung, keine Governance-Entscheidung, keine Anforderung, keine Coding-Freigabe. |
| Autoritätsgrenze | **Ich empfehle. Sie entscheiden.** |
| Baseline-Bezug | `MILESTONE-1.0-BASELINE = 8fcf42f1997dfcf6ff232e75fd33c37b933991c8` [SOURCE: docs/audits/jochen-x-master-engineering-plan-r0.md §3.1] |

---

## 0. Lesehinweise und Vorbehalte

### 0.1 Quellenbindung

Diese Matrix verdichtet **ausschließlich** den R0-Plan. Es wurde keine neue
Analyse durchgeführt, keine Datei erneut gelesen, keine Aussage ergänzt.
Positionen, die sich aus dem R0-Plan nicht eindeutig ergeben, sind mit
**UNKNOWN** gekennzeichnet.

Quellenformat: `[SOURCE: docs/audits/jochen-x-master-engineering-plan-r0.md §<Abschnitt>]`,
im Folgenden abgekürzt als **`[R0 §<Abschnitt>]`**.

### 0.2 Zählkorrektur zum R0-Plan

Der R0-Plan nennt in der Einleitung zu Kapitel 19 die Verteilung
„CRITICAL 0 · HIGH 7 · MEDIUM 12 · LOW 3 · OBSERVATION 4 (insgesamt 26)".
Die tatsächlichen Tabellenzeilen in §19.1–§19.4 enthalten jedoch:

| Stufe | Zeilen in R0 §19.1–§19.4 | IDs |
|---|---|---|
| CRITICAL | 0 | — |
| HIGH | **8** | TD-01, TD-02, TD-03, TD-04, TD-05, TD-14, TD-19, TD-23 |
| MEDIUM | 12 | TD-06, TD-07, TD-11, TD-12, TD-15, TD-16, TD-18, TD-21, TD-22, TD-24, TD-25, TD-26 |
| LOW | 3 | TD-10, TD-13, TD-27 |
| OBSERVATION | 4 | TD-08, TD-09, TD-17, TD-20 |
| **Summe** | **27** | TD-01 … TD-27, lückenlos |

> **Korrektur:** Die Zahl **27** (davon **8 HIGH**) ist zutreffend; die
> Summenzeile in R0 §19 ist eine Fehlzählung. Diese Matrix führt **alle 27**
> Positionen. Der R0-Plan wurde dafür **nicht** geändert.
> Klassifikation: redaktionelle Inkonsistenz des R0-Plans, ohne inhaltliche
> Auswirkung auf einen einzelnen Befund. [SOURCE: R0 §19, §19.1–§19.4]

### 0.3 Bedeutung des Status **READY**

**Wichtig:** `READY` bedeutet in dieser Matrix ausschließlich *„liegt innerhalb
der bestehenden genehmigten Sprint-/WP-Autorisierung und benötigt keine
zusätzliche Architektur- oder Governance-Entscheidung"*.

Es bedeutet **nicht**, dass mit der Arbeit begonnen werden darf. Über **allen**
Umsetzungspositionen steht unverändert das Coding Authorization Gate:

> Bedingungen 7–9 / RL-05 — **Nr. 7 PENDING, Nr. 8 ERFÜLLT (SPR-01),
> Nr. 9 PENDING.** **CODING = NOT AUTHORIZED.**
> [SOURCE: R0 §23.2, RM-01]

### 0.4 Priorisierungsvorbehalt

Die Prioritäten **P0–P4** und die aus R0 übernommenen Schweregrade
(HIGH/MEDIUM/LOW/OBSERVATION) sind **rein technische Priorisierungsmittel**.
Sie ersetzen und redefinieren die JOCHEN-X-Governance-Wirkungsstufen **nicht**
und sind keine Findings im Governance-Sinn. [SOURCE: R0 §19, Vorbemerkung]

### 0.5 Kategorien und Prioritäten

| Kat. | Bedeutung |
|---|---|
| **A** | MUST DECIDE BEFORE CODING — Entscheidung nötig, bevor die betroffene Umsetzung sinnvoll/governance-konform beginnen kann |
| **B** | IMPLEMENTABLE WITHIN EXISTING AUTHORIZATION — innerhalb genehmigter Sprints/WPs, ohne neue Architektur-/Governance-Entscheidung |
| **C** | SECURITY-CRITICAL DECISION / REVIEW |
| **D** | GOVERNANCE / ARCHITECTURE DECISION — außerhalb des normalen Coding-Scope |
| **E** | FUTURE / NOT CURRENTLY AUTHORIZED |
| **F** | OBSERVATION / TECHNICAL DEBT — wichtig, derzeit keine unmittelbare Blockade |

| Prio | Bedeutung |
|---|---|
| **P0** | blockiert wesentliche Umsetzung |
| **P1** | sollte vor dem betroffenen Work Package geklärt werden |
| **P2** | innerhalb des vorgesehenen Sprints bearbeitbar |
| **P3** | später / nicht kritisch |
| **P4** | Zukunft |

Statuswerte: `OPEN` · `BLOCKED` · `READY` · `READY AFTER DECISION` · `FUTURE` · `NOT AUTHORIZED`

Sprint-Alignment: `ALIGNED` · `PARTIALLY ALIGNED` · `NO CURRENT SPRINT` · `PROPOSED CHANGE`

---

## 1. Zentrale Matrix

### 1.1 Open Decisions (OD-01 … OD-08)

| ID | Kat. | Prio | Problem | Entscheidung nötig? | Quelle | Security | Sprint/WP | Empfehlung | Status |
|---|---|---|---|---|---|---|---|---|---|
| **OD-01** | **D** (sek. A, C) | **P0** | ADR-005/006/007 + Architecture Book tragen am Baseline „Open"; APPROVED-Fassung nur uncommittet | **JA** — Projekteigner / Governance Architect | [R0 §4.2, §20 OD-01] | mittelbar: ADR-005/006 sind Bezugstexte aller Plugin-Security-Befunde | NO CURRENT SPRINT (Vorarbeit V-1) | Vor SPR-02 disponieren; ohne geklärte Fassung fehlt WP-001..WP-005 der Vertragstext. **Ohne Präferenz zwischen den Optionen** | **OPEN** (Spiegel: BD-03) |
| **OD-02** | **D** (sek. A, F) | **P1** | Zweiter, gleichnamiger Composition Root `app/host.py` + `ui/`-Altbestand; von GDR-002 nicht erfasst | **JA** — Projekteigner / Governance Architect | [R0 §6.3, §20 OD-02] | latenter Pfad ohne Plugin-Pipeline (nicht aktiv) | NO CURRENT SPRINT; berührt SPR-03/WP-002 (FR-003) | Entscheiden, **bevor** WP-002 beginnt: „zentrale Registrierung" (FR-003) ist mit zwei Composition Roots nicht widerspruchsfrei erfüllbar. Option (c) berührt RB-1.0 | **OPEN** (Spiegel: BD-06) |
| **OD-03** | **D** (sek. F) | **P1** | Packaging/Tooling zeigt auf den stillgelegten Baum (`where=["src"]`, mypy, ruff, `testpaths`) | **JA** — Projekteigner | [R0 §7.6, §20 OD-03] | keine direkte | NO CURRENT SPRINT | Vor einer etwaigen CI-Einführung behandeln; höchster ökonomischer Hebel (Auslieferbarkeit) | **OPEN** |
| **OD-04** | **C** (sek. D, E) | **P4** | Plugin-Isolationsstrategie; ohne Isolation ist jedes Permission-Modell beratend | **JA** — Projekteigner + Security-Governance, ADR-pflichtig | [R0 §10.4, §20 OD-04] | **fundamental** | NO CURRENT SPRINT / nicht M1.0-Scope | **Keine Empfehlung** — Optionsbildung wäre bereits Security-Architekturarbeit. Feststellung: sollte **vor** jeder Fähigkeit fallen, die Fremd-/KI-erzeugten Code ausführt | **BLOCKED** (BD-01) |
| **OD-05** | **C** (sek. D) | **P1** | Security-Verdrahtung: `SecurityBootstrapStage` läuft nach der Pipeline; Policies nicht konfigurierbar; Trust-Ledger-Identität wechselt | **JA** — Projekteigner + Architektur-/Security-Governance | [R0 §10.6, §20 OD-05] | **hoch** — betrifft die tatsächliche Wirksamkeit der Admission-Policy | NO CURRENT SPRINT; berührt QG-006 (SPR-04 + SPR-05) | Option (b) — Policy-Konfiguration in die bestehende `PluginSecurityStage` ziehen — ist die eingriffsärmste Variante (löst TD-05 vollständig, TD-19 teilweise) und käme ohne Reihenfolgeänderung aus. **Empfehlung, keine Entscheidung**; ersetzt keine ADR-/RDR-Prüfung | **OPEN** |
| **OD-06** | **D** (sek. A) | **P1** | Auslegung von NFR-007 gegenüber der vorbestehenden, undeklarierten Abhängigkeit `ollama` | **JA** — Projekteigner | [R0 §11.3, §20 OD-06] | keine direkte | NO CURRENT SPRINT | Gemeinsam mit OD-02 behandeln — derselbe Altbestand-Cluster | **OPEN** (Spiegel: BD-04) |
| **OD-07** | **D** (sek. A, B) | **P1** | Event-Zustellsemantik bei Handler-Ausnahmen (Abbruch + Propagation) vs. FR-010; berührt ADR-002 | **JA** — Architektur-Governance | [R0 §16.3 REL-01, §20 OD-07] | mittelbar (Verfügbarkeit) | **SPR-06 / WP-005** (dort planmäßig verortet) | Im Rahmen von WP-005 prüfen. **Keine** eigenmächtige Semantikänderung | **OPEN** (Spiegel: BD-05) |
| **OD-08** | **D** | **P3** | Sprint Plan trägt im Kopf DRAFT, ist über ADW-SPR-1.0-001 als Planungsgrundlage genehmigt | **JA** — Projekteigner / Governance | [R0 §2.3 SG-02, §20 OD-08] | keine | NO CURRENT SPRINT | Redaktionell, nicht dringlich; sinnvoll gemeinsam mit OD-01 | **OPEN** |

### 1.2 Technical Debt — HIGH (8)

| ID | Kat. | Prio | Problem | Entscheidung nötig? | Quelle | Security | Sprint/WP | Empfehlung | Status |
|---|---|---|---|---|---|---|---|---|---|
| **TD-01** | **A** (sek. D, F) | **P1** | Zweiter Composition Root `app/host.py::ApplicationHost` ohne State Machine und ohne Plugin-Security-Pipeline | **JA** → OD-02 | [R0 §19.1] | latent (nicht aktiv) | NO CURRENT SPRINT; RB-1.0-Bindung über `tests/test_foundation.py` | Governance-Disposition analog GR-001; **nicht** eigenmächtig entfernen | **READY AFTER DECISION** (OD-02) |
| **TD-02** | **A** (sek. F) | **P1** | Packaging/Tooling adressiert `src/` statt der produktiven Struktur | **JA** → OD-03 | [R0 §19.1] | keine | NO CURRENT SPRINT | Konfiguration an GDR-002 D-1 angleichen — erfordert Freigabe | **READY AFTER DECISION** (OD-03) |
| **TD-03** | **A** (sek. F) | **P1** | Undeklarierte externe Abhängigkeit `ollama` in `core/ai_manager.py` | **JA** → OD-06 | [R0 §19.1] | keine direkte | NO CURRENT SPRINT | Deklarieren **oder** mit dem Altbestand-Cluster disponieren | **READY AFTER DECISION** (OD-06) |
| **TD-04** | **C** (sek. A, D) | **P1** | Runtime-Permission-Enforcement nutzt Plugin-Selbstdeklaration statt Host-Grants | **JA** → OD-01 + OD-05 | [R0 §10.5, §19.1] | **hoch** — Kontraktbruch ggü. ADR-006 D4; in Welt A als „Integration steht aus" benannt | NO CURRENT SPRINT | Host-Grants in den `PluginContext` übertragen — SDK-additive Änderung, ADR-/Freigabe-relevant. **Wirkungsdämpfer:** stellt Kontraktkonformität her, nicht Erzwingbarkeit (solange OD-04 offen) | **READY AFTER DECISION** (OD-01 + OD-05) |
| **TD-05** | **C** (sek. A) | **P1** | `IntegrityPolicy.from_config` / `PermissionPolicy.from_config` ohne produktive Aufrufstelle; kein `[security]` in der Konfiguration | **JA** → OD-05 | [R0 §10.6, §19.1] | **hoch** — Policy fest verdrahtet; Referenz-Plugin wird mit Default-Konfiguration abgelehnt | NO CURRENT SPRINT | Konfigurationspfad herstellen (OD-05 Option b) | **READY AFTER DECISION** (OD-05) |
| **TD-14** | **B** (sek. F) | **P2** | `PluginLoader.discover()` ohne Fehlerisolation je Manifest → ein defektes `plugin.toml` deaktiviert alle Plugins; `PluginFailed("")` ohne Identifier | NEIN (innerhalb FR-010/FR-006) | [R0 §9.3, §19.1] | Verfügbarkeit; keine Prüfungsabschwächung | **SPR-06 / WP-005** (FR-010); Diagnoseanteil **SPR-04 / WP-003** (FR-006) | PC-01 umsetzen: Isolation je Manifest, Identifier im Ereignis führen | **READY** |
| **TD-19** | **C** (sek. D) | **P1** | `SecurityBootstrapStage` (FINALIZE) ersetzt die `PluginSecurity`-Instanz **nach** Admission und Aktivierung | **JA** → OD-05 | [R0 §10.6 SEC-07, §19.1] | **hoch** — der aus der Registry bezogene Trust Ledger ist nicht derjenige, gegen den geprüft wurde | NO CURRENT SPRINT; berührt QG-006 | Reihenfolge/Komposition klären — Bootstrap-Baseline §8 Change Control | **READY AFTER DECISION** (OD-05) |
| **TD-23** | **A** (sek. B) | **P1** | `EventBus.publish` bricht die Zustellkette bei Handler-Ausnahme ab und propagiert zum Publisher | **JA** → OD-07 (ADR-002) | [R0 §16.3 REL-01, §19.1] | mittelbar (Verfügbarkeit); DEVIATION ggü. FR-010 | **SPR-06 / WP-005** | Zustellsemantik im Rahmen WP-005 klären; berührt ADR-002 | **READY AFTER DECISION** (OD-07) |

### 1.3 Technical Debt — MEDIUM (12)

| ID | Kat. | Prio | Problem | Entscheidung nötig? | Quelle | Security | Sprint/WP | Empfehlung | Status |
|---|---|---|---|---|---|---|---|---|---|
| **TD-06** | **A** (sek. F) | **P2** | Kapselungsbruch: `registry._lock` / `_registrations.pop()` an zwei Stellen | **JA** → OD-05 | [R0 §6.5, §19.2] | keine direkte | NO CURRENT SPRINT; Risiko RK-03 für SPR-03/WP-002 | Öffentliche `replace()`/`override()`-Fähigkeit erwägen (additiv) | **READY AFTER DECISION** (OD-05) |
| **TD-07** | **D** (sek. F) | **P2** | `ServiceRegistry._resolve` / Singleton-Caching ohne Lock | **JA** — Kernkomponente ohne FR-Deckung | [R0 §19.2, §21.4] | keine direkte | NO CURRENT SPRINT | Auflösung unter Lock; Test TG-7 ergänzen | **OPEN** |
| **TD-11** | **B** | **P2** | `sys.modules` wird bei `restart()`/`recover()` nicht bereinigt | NEIN (FR-009) | [R0 §7.4, §19.2] | keine direkte | **SPR-06 / WP-005** (FR-009) | Bereinigung analog der bereits im Testbestand vorhandenen Lösung | **READY** |
| **TD-12** | **B** | **P2** | Bootstrap Baseline §5.2 nennt 5 Pipeline-Schritte, der Code führt 6 aus (API-Version-Gate) | NEIN (FR-012) | [R0 §8.5 BS-05, §19.2] | keine — der Zusatzschritt wirkt ausschließlich verschärfend | **SPR-07 / WP-007** | Dokumentation nachführen; **kein** Codeeingriff | **READY** |
| **TD-15** | **D** (sek. C) | **P2** | Plugin-Klassenauswahl über `dir(module)`; `entry_point` unausgewertet | **JA** — Verhaltensänderung, ADR-011-Berührung möglich | [R0 §9.5 PS-04, §19.2] | mittelbar — importierte Fremdklassen wählbar | NO CURRENT SPRINT → **PROPOSED CHANGE** (PC-03) | `entry_point` auswerten, rückwärtskompatibel | **OPEN** |
| **TD-16** | **D** | **P2** | Unparsbare Versionsangabe in Abhängigkeiten wird still ignoriert (fail-open) | **JA** — ADR-007-Semantik | [R0 §9.6 PS-06, §19.2] | keine direkte | NO CURRENT SPRINT | Ablehnen statt ignorieren | **OPEN** |
| **TD-18** | **C** (sek. D) | **P2** | Keine Validierung von `manifest.identifier` vor Nutzung als Modulname und Pfadsegment | **JA** — Security-Härtung ohne FR-Deckung | [R0 §10.3 SEC-03, §19.2] | **ja** — Schutz entsteht heute nur als Nebeneffekt | NO CURRENT SPRINT → **PROPOSED CHANGE** (PC-04) | Explizite Identifier-Validierung in der Pipeline; SDK besitzt bereits `validate_identifier` | **OPEN** |
| **TD-21** | **C** (sek. E) | **P2** | Admission-Entscheidungen laufen nicht über den `AuditLogger` (existiert zu diesem Zeitpunkt nicht) | **JA** → OD-05; Katalog ist **ODD-17 (offen)** | [R0 §10.8 SEC-10, §19.2] | **ja** — kein durchgängiger Audit-Trail | NO CURRENT SPRINT | Mit TD-19 gemeinsam behandeln | **BLOCKED** (ODD-17) / teilweise READY AFTER DECISION (OD-05) |
| **TD-22** | **F** (sek. E) | **P3** | Drei konkurrierende KI-Abstraktionen, zwei Capability-Vokabulare | **JA** → OD-02 (Altbestand) | [R0 §11.4 AI-03, §19.2] | keine — Code ist von der Laufzeit entkoppelt | NO CURRENT SPRINT | Mit dem Altbestand-Cluster disponieren | **OPEN** |
| **TD-24** | **B** | **P2** | Zustandsübergangs-Listener laufen ungeschützt nach dem Zustandswechsel | NEIN (FR-010) | [R0 §16.3 REL-02, §19.2] | keine direkte | **SPR-06 / WP-005** | Isolation je Listener | **READY** |
| **TD-25** | **B** | **P2** | `EventBus` wird in `_reset()` nicht erneuert; Abonnements/Sticky/History überdauern Restarts | NEIN (FR-009) | [R0 §16.4 REL-03, §19.2] | keine direkte | **SPR-06 / WP-005** (FR-009) | Verhalten festlegen **und dokumentieren** — R0 hält fest, dass beide Varianten vertretbar sind und die fehlende Aussage der Mangel ist | **READY** |
| **TD-26** | **B** | **P2** | `_validate_for_activation`-Docstring nennt eine Permission-Prüfung, die nicht stattfindet; `permissions_valid` bleibt stets Default | NEIN (FR-006) | [R0 §18.3, §19.2] | mittelbar — `ValidationDiagnostic` suggeriert eine Prüfung | **SPR-04 / WP-003** (FR-006) | Docstring korrigieren **oder** Prüfung ergänzen | **READY** |

### 1.4 Technical Debt — LOW (3)

| ID | Kat. | Prio | Problem | Entscheidung nötig? | Quelle | Security | Sprint/WP | Empfehlung | Status |
|---|---|---|---|---|---|---|---|---|---|
| **TD-10** | **B** (sek. F) | **P2** | `Metrics` unsynchronisiert, unbegrenzte Schlüsselkardinalität mit manifestgesteuerten Namensanteilen | NEIN; **OTD-1** ist Vorbedingung des betroffenen Teils | [R0 §17.3 P-4, §19.3] | mittelbar — Schlüssel enthalten manifestgesteuerte Werte | **SPR-05 / WP-004** | Innerhalb WP-004 behandeln | **READY** (OTD-1 beachten) |
| **TD-13** | **F** (sek. B) | **P3** | `Path.glob()` liefert unsortierte Discovery-Reihenfolge | NEIN | [R0 §9.2 PS-01, §19.3] | keine | NO CURRENT SPRINT → **PROPOSED CHANGE** (PC-08) | `sorted(...)` verwenden | **OPEN** |
| **TD-27** | **F** | **P3** | `core/registry.py` und `core/events.py` ohne `__all__` (Stilregel) | NEIN | [R0 §18.2, §19.3] | keine | NO CURRENT SPRINT | Geringe Wirkung; opportunistisch | **OPEN** |

### 1.5 Technical Debt — OBSERVATION (4)

| ID | Kat. | Prio | Problem | Entscheidung nötig? | Quelle | Security | Sprint/WP | Empfehlung | Status |
|---|---|---|---|---|---|---|---|---|---|
| **TD-08** | **B** | **P2** | Bootstrap Baseline §3.1 überschreibt 22 aufgezählte Symbole mit „20 Symbole"; Code und Aufzählung stimmen überein | NEIN (FR-012) | [R0 §8.3 BS-02, §19.4] | keine | **SPR-07 / WP-007** | Redaktionell nachführen. Relevant, weil SPR-09-Nachweise gegen diesen Text zählen | **READY** |
| **TD-09** | **F** (sek. D) | **P3** | Keine CI-Konfiguration; alle Gate-Nachweise manuell | **JA** für PC-05 (neue Datei → Freigabe) | [R0 §7.7 RT-08, §19.4] | keine direkte | NO CURRENT SPRINT → **PROPOSED CHANGE** (PC-05) | Setzt OD-03 voraus, sonst prüft CI den falschen Baum | **OPEN** |
| **TD-17** | **B** (sek. C, E) | **P2** | Bezeichnung „Integrity Validation" für eine reine Schema-Prüfung | NEIN für den Dokumentationsanteil; die Substanz ist an **ODD-19** gebunden | [R0 §10.3 SEC-01/SEC-02, §19.4] | **ja** — Wirkungsgrenze; quellengedeckt zurückgestellt, aber überzeichnet benannt | **SPR-07 / WP-007** (nur Dokumentation, PC-06) | Wirkungsgrenze dokumentieren. **Kein** Codeeingriff, **keine** ODD-Auflösung | **READY** (Dokumentation) / **BLOCKED** (Substanz, BD-02) |
| **TD-20** | **C** (sek. E) | **P1** | `ReversibleEncryptionService` = Base64; stillschweigender Default für Vault **und** Backups | **JA** — Kryptografieverfahren ist **ODD-19 (offen)** | [R0 §10.7 SEC-08, §19.4] | **hoch** — Secrets und Backups effektiv im Klartext; Risiko RK-09 | NO CURRENT SPRINT → **PROPOSED CHANGE** (PC-07) | **Nur Sichtbarmachung** (Startup-Warnung, Namensklarheit). **Kein** Verfahren vorgeschlagen oder ausgewählt | **BLOCKED** (BD-02) für das Verfahren; PC-07 **OPEN** |

### 1.6 Proposed Changes (PC-01 … PC-08)

| ID | Kat. | Prio | Vorschlag | Entscheidung nötig? | Quelle | Security | Sprint/WP | Sprint-Alignment | Status |
|---|---|---|---|---|---|---|---|---|---|
| **PC-01** | **B** | **P2** | Fehlerisolation je Manifest in der Discovery; `PluginFailed` trägt den Verzeichnisnamen | NEIN | [R0 §30 PC-01] | positiv (Verfügbarkeit); keine Prüfungsabschwächung | SPR-06/WP-005 + SPR-04/WP-003 | **ALIGNED** | **READY** |
| **PC-02** | **B** | **P1** | Baseline-Messreihe (IP Anhang B / OP-8) **vor** SPR-02 erheben | NEIN — im Plan vorgesehen | [R0 §30 PC-02, §17.4] | keine | Vorbereitung SPR-08 | **ALIGNED** (Bestätigung der Planvorgabe mit Terminakzent) | **READY** |
| **PC-03** | **D** (sek. C) | **P2** | `entry_point` bei der Plugin-Klassenauswahl auswerten | **JA** — ADR-011-Berührung möglich | [R0 §30 PC-03] | mittelbar positiv | keine WP-Zuordnung | **PROPOSED CHANGE** | **OPEN** |
| **PC-04** | **C** | **P2** | Identifier-Validierung vor Pfad- und Modulnutzung | **JA** — Härtung ohne FR-Deckung | [R0 §30 PC-04] | **positiv, ausschließlich verschärfend** | keine WP-Zuordnung | **PROPOSED CHANGE** | **OPEN** |
| **PC-05** | **D** (sek. F) | **P2** | Reproduzierbarer Verifikationslauf für RB-1.0 (dokumentiertes Skript und/oder CI) | **JA** — neue Datei → Freigabe; setzt OD-03 voraus | [R0 §30 PC-05] | keine direkte | keine WP-Zuordnung | **PROPOSED CHANGE** | **OPEN** |
| **PC-06** | **B** | **P2** | Wirkungsgrenze der Integritätsprüfung dokumentieren | NEIN | [R0 §30 PC-06] | positiv (verhindert falsche Sicherheitsannahmen); schließt **keine** ODD | SPR-07/WP-007 | **ALIGNED** | **READY** |
| **PC-07** | **C** | **P1** | Platzhalter-Kryptografie sichtbar machen (Startup-Warnung, Namensklarheit) | **JA** — neue Position ohne WP | [R0 §30 PC-07] | **positiv** — adressiert RK-09. **Kein** Kryptoverfahren vorgeschlagen | keine WP-Zuordnung | **PROPOSED CHANGE** | **OPEN** |
| **PC-08** | **B** (sek. F) | **P3** | Deterministische Discovery-Reihenfolge (`sorted(glob)`) | NEIN | [R0 §30 PC-08] | keine | keine WP-Zuordnung | **PROPOSED CHANGE** (klein) | **OPEN** |

### 1.7 Blocked Decisions (BD-01 … BD-06)

> **Hinweis zur Vermeidung von Doppelzählung:** BD-03, BD-04, BD-05 und BD-06
> sind die *blockierte Spiegelung* von OD-01, OD-06, OD-07 und OD-02. Sie
> beschreiben denselben Gegenstand aus der Perspektive „was der R0-Verfasser
> ausdrücklich **nicht** getan hat". [SOURCE: R0 §33.2]

| ID | Kat. | Prio | Gegenstand | Warum blockiert | Quelle | Erforderliche Autorität | Status |
|---|---|---|---|---|---|---|---|
| **BD-01** | **C** | **P4** | Plugin-Isolationsstrategie (= OD-04) | Security-Architekturentscheidung; ADR-009 und ODD-Register offen; neue ADRs ausdrücklich nicht autorisiert | [R0 §33.2] | Projekteigner + Security-Governance, **ADR-pflichtig** | **BLOCKED** |
| **BD-02** | **C** | **P4** (Sichtbarmachung: P1) | Kryptografieverfahren für Vault/Backups (**ODD-19**) | ODD-19 offen; ODDs sind Designentscheidungen, nicht über Correction Cycles zu behandeln | [R0 §33.2] | Projekteigner + Security-Governance | **BLOCKED** |
| **BD-03** | **D** | **P0** | Statusdivergenz ADR-005/006/007 + Architecture Book zwischen Welt A und Welt B (= OD-01) | Disposition ist im Baseline Commit Record ausdrücklich dem Projekteigner vorbehalten | [R0 §33.2, §4.2] | Projekteigner / Governance Architect | **BLOCKED** |
| **BD-04** | **D** | **P1** | Auslegung von NFR-007 ggü. vorbestehenden Abhängigkeiten (= OD-06) | Auslegung einer genehmigten Anforderung | [R0 §33.2] | Projekteigner | **BLOCKED** |
| **BD-05** | **D** | **P1** | Event-Zustellsemantik bei Handler-Ausnahmen (= OD-07) | Berührt ADR-002 (genehmigt) | [R0 §33.2] | Architektur-Governance | **BLOCKED** |
| **BD-06** | **D** | **P1** | Behandlung des `app/host.py`-Clusters (= OD-02) | GDR-002 entscheidet ausdrücklich keine andere Governance-Frage | [R0 §33.2] | Projekteigner / Governance Architect | **BLOCKED** |

### 1.8 Architecture Deviations & Gap-Befunde (aus R0 §21)

| ID | Kat. | Prio | Befund | Quelle | Sprint/WP | Alignment | Status |
|---|---|---|---|---|---|---|---|
| **GAP-FR003** | **A** | **P1** | FR-003 („zentrale Registrierung") mit zwei Composition Roots nicht widerspruchsfrei erfüllbar → PARTIAL MATCH | [R0 §21.3] | SPR-03 / WP-002 | **PARTIALLY ALIGNED** | **BLOCKED** bis OD-02 |
| **GAP-FR008** | **B** | **P2** | FR-008 **MISSING** — `Metrics` ist ein geschlossener `dict`, kein Erweiterungspunkt; deckt sich mit **OTD-1** | [R0 §21.3] | SPR-05 / WP-004 | **ALIGNED** | **READY** (OTD-1 vorher festlegen) |
| **GAP-FR010** | **B/A** | **P2** | FR-010 PARTIAL MATCH: Aktivierung MATCH, Discovery/Events/Listener DEVIATION (TD-14, TD-23, TD-24) — **Lücke größer als in ES §5.5 angenommen** | [R0 §21.3, GAP-01] | SPR-06 / WP-005 | **PARTIALLY ALIGNED** (TD-23 an OD-07 gebunden) | **READY** / TD-23 READY AFTER DECISION |
| **GAP-FR001/002** | **F** | **P3** | FR-001/FR-002 sind **weitgehend MATCH** — ES §5.5 überschätzt die Lücke | [R0 §21.3, GAP-01] | SPR-02 / WP-001 | **ALIGNED** | **READY** (Feststellung, keine Arbeit) |
| **GAP-NFR004** | **B** | **P1** | NFR-004 **UNKNOWN** — keine Baseline-Messreihe vorhanden | [R0 §21.4, §17.2] | Vorbereitung SPR-08 | **ALIGNED** (OP-8) | **READY** (PC-02) |
| **GAP-NFR007** | **D** | **P1** | NFR-007 PARTIAL MATCH / strittig (`ollama` vorbestehend) | [R0 §21.4] | NO CURRENT SPRINT | **NO CURRENT SPRINT** | **OPEN** (OD-06) |
| **GAP-NFR005** | **F** | **P3** | NFR-005 nennt 1019; verbindlich ist RB-1.0 = 258 — textliche Divergenz im ES, materiell durch GDR-002 D-3 / SPR-01 aufgelöst | [R0 §21.4] | — | **ALIGNED** (nur Feststellung) | **OPEN** (kein Handlungsbedarf ausgewiesen) |
| **DEV-LAYER** | **F** | **P3** | Schichtverstoß: `core/ai_manager.py` (externer Provider) und `core/worker.py` (UI-Framework) im innersten Ring | [R0 §6.2 AM-01] | NO CURRENT SPRINT | **NO CURRENT SPRINT** | **OPEN** (OD-02/OD-06) |
| **DEV-AB** | **D** | **P0** | Architecture Book v2.0 (FROZEN) ist im Working Tree modifiziert — Dispositionsgegenstand, **nicht** als eingetretene Deviation gewertet | [R0 §4.2] | NO CURRENT SPRINT | **NO CURRENT SPRINT** | **BLOCKED** (BD-03) |

### 1.9 Risiken (aus R0 §28) — nur Steuerungsrelevanz

| ID | Prio | Risiko | Wahrsch. | Gegenmaßnahme | Bezug |
|---|---|---|---|---|---|
| **RK-04** | **P1** | FR-010 wird als „erfüllt" bewertet, weil die Aktivierungsisolation überzeugt, während Discovery/Events lückenhaft bleiben → **Gate-Scheinbestehen** | **hoch** | TG-1 und TG-6 als AC-Nachweis vorsehen | [R0 §28] |
| **RK-05** | **P1** | Regressionsnachweis versehentlich gegen 1.019 statt 258 (oder umgekehrt) | **hoch** | Explizite Pfadliste im Nachweisverfahren; `testpaths` disponieren (OD-03) | [R0 §28] |
| **RK-01** | P1 | Phase B trifft auf ungeklärte ADR-Vertragslage | mittel | OD-01 vor Phase B | [R0 §28] |
| **RK-02** | P1 | QG-005/QG-008-Nachweise gegen den Baseline-Commit nicht führbar (untracked Quellen + ADR-Divergenz) | mittel | Nachweisverfahren früh festlegen | [R0 §28] |
| **RK-03** | P2 | Registry-Änderungen brechen die zwei `_registrations.pop()`-Stellen | mittel | TD-06 vor WP-002-Arbeit sichtbar machen | [R0 §28] |
| **RK-07** | P1 | Security-Policy bleibt fest verdrahtet; Plugins produktiv nicht aktivierbar | mittel | OD-05 | [R0 §28] |
| **RK-09** | P1 | Base64-„Encryption" wird als Schutz missverstanden | mittel | TD-20 sichtbar machen (PC-07); ODD-19 disponieren | [R0 §28] |
| **RK-06** | P2 | `ollama` fehlt in sauberer Umgebung → Importfehler | mittel | OD-06 | [R0 §28] |
| **RK-08** | P3 | Registry-Nebenläufigkeitsdefekt sporadisch | niedrig | TD-07, TG-7 | [R0 §28] |
| **RK-10** | P3 | Diese Analyse wird als Autorisierung missverstanden | niedrig | Statuszeilen, Kap. 8 dieses Dokuments | [R0 §28] |

### 1.10 Matrix-Bilanz

| Kategorie | Anzahl Positionen |
|---|---|
| **A** — MUST DECIDE BEFORE CODING | 7 (TD-01, TD-02, TD-03, TD-06, TD-23, GAP-FR003, + Sekundärbezüge) |
| **B** — IMPLEMENTABLE WITHIN EXISTING AUTHORIZATION | 14 |
| **C** — SECURITY-CRITICAL DECISION / REVIEW | 10 |
| **D** — GOVERNANCE / ARCHITECTURE DECISION | 15 |
| **E** — FUTURE / NOT CURRENTLY AUTHORIZED | siehe Kap. 6 (aus R0 §31 übernommen) |
| **F** — OBSERVATION / TECHNICAL DEBT | 8 |

| Status | Anzahl |
|---|---|
| OPEN | 20 |
| BLOCKED | 9 |
| READY | 13 |
| READY AFTER DECISION | 8 |
| FUTURE / NOT AUTHORIZED | siehe Kap. 6 |

*(Positionen mit Doppelstatus — z. B. TD-17, TD-20 — sind in beiden Zeilen
gezählt; Primärkategorie bleibt eindeutig.)*

---

## 2. DECISIONS WE MUST MAKE

> **Ich empfehle. Sie entscheiden.**
> Keine der folgenden Positionen wird durch dieses Dokument entschieden.

### D-1 · OD-01 / BD-03 — Disposition der sechs uncommitteten Dokumentänderungen

| Feld | Inhalt |
|---|---|
| **ID** | OD-01 (Spiegel BD-03) — **P0** |
| **Problem** | ADR-005/006/007 und Architecture Book v2.0 tragen am Baseline-Commit den Status „Open – requires decision before implementation"; die APPROVED-Fassungen existieren nur als uncommittete Working-Tree-Modifikation (+1.415/−119 Zeilen über 6 Dateien). Auch CLAUDE.md und ROADMAP.md sind modifiziert. [R0 §4.2, BV-02] |
| **Warum Entscheidung erforderlich** | ADR-006 D4 ist die **Vertragsgrundlage** für TD-04; ADR-005 für TD-17/SEC-01. Ohne geklärte Fassung fehlt WP-001..WP-005 ein eindeutiger Bezugstext (RK-01). Zusätzlich hängen die Nachweise für QG-005/QG-008 daran (RK-02). Der Baseline Commit Record hat die Disposition ausdrücklich als „nächster Entscheidungspunkt des Projekteigners" vorgemerkt. [R0 §4.2, §20 OD-01] |
| **Betroffene Komponenten** | `docs/adr/005`, `docs/adr/006`, `docs/adr/007`, `docs/architecture-book-v2.md` (FROZEN), `CLAUDE.md`, `ROADMAP.md` — **keine** Code-Komponente |
| **Betroffene Sprints** | SPR-02 … SPR-07 (Vertragstext), SPR-09 (QG-003), SPR-10 (QG-005/QG-008) |
| **Security-Auswirkung** | mittelbar, aber breit: ADR-005/006 sind Bezugstexte **aller** Plugin-Security-Befunde dieser Matrix |
| **Produkt-Auswirkung** | keine unmittelbare |
| **Optionen** (aus R0 übernommen) | (a) Committen mit Governance-Vermerk · (b) belassen und die Divergenz in den Gate-Nachweisen dokumentieren · (c) getrennte Behandlung — ADRs vs. FROZEN Architecture Book vs. CLAUDE.md/ROADMAP.md |
| **Empfehlung** | **Vor SPR-02 disponieren.** **Ausdrücklich ohne Präferenz zwischen (a)/(b)/(c)** — die Wahl ist Governance und liegt außerhalb meiner Autorität. Option (a) berührt den Architecture Freeze; Option (b) erhöht den Nachweisaufwand in Phase D |

### D-2 · OD-02 / BD-06 — Status des `app/host.py`-Clusters

| Feld | Inhalt |
|---|---|
| **ID** | OD-02 (Spiegel BD-06) — **P1** |
| **Problem** | Zweiter, gleichnamiger Composition Root `app/host.py::ApplicationHost` neben `app/application_host.py::ApplicationHost` — ohne State Machine, ohne Plugin-Security-Pipeline, Qt-gebunden, im Produktionspfad tot, aber durch `tests/test_foundation.py` (7 Tests) in **RB-1.0** gehalten. Zugehöriger Altbestand: `ui/foundation_window.py`, `ui/*.py`-Duplikate, `core/worker.py`, `core/ai_manager.py`. [R0 §6.3 AM-02/AM-03, §6.6 AM-05] |
| **Warum Entscheidung erforderlich** | GDR-002 entscheidet ausschließlich über `src/jochen_x/**` und ausdrücklich **keine andere** Governance-Frage. Es liegt damit ein **nicht disponierter Parallelbestand innerhalb der als produktiv entschiedenen Struktur** vor. FR-003 verlangt eine *zentrale* Host-Dienst-Beschreibung — mit zwei Composition Roots nicht widerspruchsfrei erfüllbar |
| **Betroffene Komponenten** | `app/host.py`, `ui/foundation_window.py`, `ui/sidebar.py`, `ui/status_bar.py`, `ui/chat_*.py`, `ui/input_bar.py`, `ui/message_widget.py`, `ui/dashboard.py`, `core/worker.py`, `core/ai_manager.py`, `tests/test_foundation.py` |
| **Betroffene Sprints** | **SPR-03 / WP-002 (FR-003)** primär; SPR-10 (QG-002) |
| **Security-Auswirkung** | **latent, nicht aktiv:** `app/host.py` würde bei Verwendung die Plugin-Runtime-Pipeline vollständig umgehen. Da es keinen Plugin-Code importiert, besteht am Baseline **kein** Ausführungsrisiko [R0 §6.3] |
| **Produkt-Auswirkung** | keine unmittelbare; mittelbar Wartungskosten (Doppelpflege) |
| **Optionen** (aus der GDR-002-Systematik übernommen, nicht erfunden) | (a) Erhaltung (Status quo, dokumentiert) · (b) Stilllegung analog GDR-002 D-2 **ohne** physische Entfernung · (c) Überführung/Bereinigung — **berührt RB-1.0** |
| **Empfehlung** | **Entscheiden, bevor WP-002 beginnt.** Bei Option (c) ist zusätzlich eine Regressions-Disposition erforderlich, da RB-1.0 = 258 sich ändern würde. **Keine Präferenz** — dies ist Governance |

### D-3 · OD-05 — Security-Verdrahtung im Bootstrap

| Feld | Inhalt |
|---|---|
| **ID** | OD-05 — **P1** |
| **Problem** | Drei zusammenhängende Befunde: (i) `SecurityBootstrapStage` läuft in FINALIZE und ersetzt die `PluginSecurity`-Instanz **nach** Admission und Aktivierung (TD-19); (ii) `IntegrityPolicy.from_config` / `PermissionPolicy.from_config` haben **keine produktive Aufrufstelle**, es gibt keinen `[security]`-Abschnitt in der Konfiguration (TD-05); (iii) das vom Host ermittelte Grant-Set erreicht den `PluginContext` nicht (TD-04). Zusätzlich hängen TD-21 (Audit-Trail) und TD-06 (Kapselungsbrüche als Symptom) daran. [R0 §10.5, §10.6, §20 OD-05] |
| **Warum Entscheidung erforderlich** | Eine Korrektur berührt Stage-Zusammensetzung bzw. -Reihenfolge → **Bootstrap Baseline §8 Change Control** (ADR oder RDR erforderlich). Ohne Entscheidung bleibt die Admission-Policy fest verdrahtet und das Referenz-Plugin ist mit der ausgelieferten Konfiguration nicht aktivierbar (RK-07) |
| **Betroffene Komponenten** | `app/bootstrap/stages_plugin.py`, `app/security/security_manager.py`, `app/security/plugin_security.py`, `sdk/context.py`, `config/default.toml`, `core/registry.py` (mittelbar über TD-06) |
| **Betroffene Sprints** | **SPR-04 / WP-003** und **SPR-05 / WP-004** → **QG-006 (Pipeline Security Compliance)** |
| **Security-Auswirkung** | **hoch** — betrifft die tatsächliche Wirksamkeit von Default-Deny, die Identität des Trust Ledgers und die Auditierbarkeit der Admission |
| **Produkt-Auswirkung** | **hoch** — ohne Konfigurationspfad ist die Plugin-Fähigkeit produktiv faktisch abgeschaltet |
| **Optionen** (aus R0 übernommen) | (a) `PluginSecurity` bereits in INITIALIZE komponieren und konfigurieren · (b) Policy-Konfiguration in die bestehende `PluginSecurityStage` ziehen (**ohne** Reihenfolgeänderung) · (c) Status quo dokumentieren und im Milestone unverändert lassen |
| **Empfehlung** | **Option (b)** ist die eingriffsärmste Variante: sie löst TD-05 vollständig und TD-19 teilweise und käme **ohne** Änderung der Phasen- oder Stage-Reihenfolge aus, würde also Bootstrap Baseline §8 voraussichtlich nicht berühren. **Dies ist eine Empfehlung, keine Entscheidung; sie ersetzt keine ADR-/RDR-Prüfung** [R0 §20 OD-05] |

### D-4 · OD-03 — Packaging- und Werkzeugkonfiguration

| Feld | Inhalt |
|---|---|
| **ID** | OD-03 — **P1** |
| **Problem** | `pyproject.toml` konfiguriert `packages.find where=["src"]`, `mypy_path="src"`, `ruff src=["src"]` — also den gemäß GDR-002 D-2 **stillgelegten** Baum. `testpaths=["tests"]` sammelt ohne Pfadargument alle 1.019 Tests statt RB-1.0 = 258. [R0 §7.6 RT-06/RT-07] |
| **Warum Entscheidung erforderlich** | Direkte, unbereinigte Folge der GR-001-Entscheidung; GDR-002 D-2 klammert die physische/konfigurative Behandlung ausdrücklich aus. Ohne Entscheidung: (a) `pip install .` liefert die produktive Anwendung **nicht** aus, (b) mypy/ruff prüfen den falschen Baum, (c) Regressionsnachweise sind verwechslungsanfällig (**RK-05, hohe Wahrscheinlichkeit**) |
| **Betroffene Komponenten** | `pyproject.toml` |
| **Betroffene Sprints** | keiner unmittelbar; **Voraussetzung** für belastbare Nachweise in SPR-08/SPR-09/SPR-10 und für PC-05 |
| **Security-Auswirkung** | keine direkte |
| **Produkt-Auswirkung** | **höchster ökonomischer Hebel** — „ein Produkt, das sich nicht installieren lässt, hat keinen ökonomischen Wert" [R0 §27.3] |
| **Optionen** | (a) Konfiguration auf die produktive Struktur umstellen · (b) belassen und Auslieferung als out-of-scope erklären · (c) mit OD-02 bündeln |
| **Empfehlung** | Behandlung **vor** einer etwaigen CI-Einführung (PC-05); ohne korrektes Packaging misst CI den falschen Baum. Unabhängig von der Optionswahl: das Nachweisverfahren für RB-1.0 sollte eine **explizite Pfadliste** verwenden (RK-05) |

### D-5 · OD-06 / BD-04 — Auslegung von NFR-007 für `ollama`

| Feld | Inhalt |
|---|---|
| **ID** | OD-06 (Spiegel BD-04) — **P1** |
| **Problem** | `core/ai_manager.py` importiert `ollama`; die Abhängigkeit ist in `pyproject.toml` nicht deklariert und widerspricht der Projektdokumentation („einzige externe Abhängigkeit: PySide6"). Auf einer sauberen Installation ist `core/worker.py` **nicht importierbar**; lokal ist der Defekt durch eine vorhandene Installation maskiert. [R0 §11.3 AI-02] |
| **Warum Entscheidung erforderlich** | NFR-007 ist auf den **Milestone** bezogen formuliert („keine *neuen* externen Abhängigkeiten"). Ob eine **vorbestehende** undeklarierte Abhängigkeit als NFR-007-Verstoß oder als Altbestand zu werten ist, ist eine Auslegungsfrage einer genehmigten Anforderung |
| **Betroffene Komponenten** | `core/ai_manager.py`, `core/worker.py`, `pyproject.toml` |
| **Betroffene Sprints** | keiner; berührt NFR-007-Nachweis in Phase D |
| **Security-Auswirkung** | keine direkte |
| **Produkt-Auswirkung** | RK-06 — Importfehler in sauberen Umgebungen und in CI |
| **Optionen** | (a) als Altbestand einstufen und mit OD-02 disponieren · (b) deklarieren · (c) als NFR-007-Verstoß behandeln und beheben |
| **Empfehlung** | **Gemeinsam mit OD-02 behandeln** — es ist derselbe Altbestand-Cluster (C1) |

### D-6 · OD-07 / BD-05 — Event-Zustellsemantik bei Handler-Ausnahmen

| Feld | Inhalt |
|---|---|
| **ID** | OD-07 (Spiegel BD-05) — **P1** |
| **Problem** | `EventBus.publish` bricht bei einer Handler-Ausnahme die Zustellkette ab und propagiert die Ausnahme zum Publisher. Da Plugins über das SDK abonnieren können, kann ein fehlerhaftes Plugin andere Abonnenten um ihr Ereignis bringen **und** den publizierenden Host-Code zum Absturz bringen → **DEVIATION gegen FR-010**. [R0 §16.3 REL-01, TD-23] |
| **Warum Entscheidung erforderlich** | Das Verhalten ist Gegenstand von **ADR-002** (genehmigt); eine Änderung ist eine Semantikänderung eines genehmigten Kontrakts. `EventDelivery` zeichnet den Fehlertyp bereits auf — das Verhalten ist also bewusst gewählt |
| **Betroffene Komponenten** | `core/events.py`, mittelbar `sdk/events.py`, `app/state_machine.py` (verwandtes TD-24) |
| **Betroffene Sprints** | **SPR-06 / WP-005 (FR-009/FR-010)** — dort planmäßig verortet |
| **Security-Auswirkung** | mittelbar (Verfügbarkeit) |
| **Produkt-Auswirkung** | Stabilität bei fehlerhaften Plugins |
| **Optionen** | (a) Status quo · (b) Isolation je Handler mit Fehleraufzeichnung · (c) differenziert nach Abonnentenherkunft (Host vs. Plugin) |
| **Empfehlung** | Im Rahmen von WP-005 prüfen, **nicht** eigenmächtig ändern. Zusätzlich **RK-04 beachten**: ohne die Tests TG-1 und TG-6 besteht die Gefahr, FR-010 als erfüllt zu bewerten, obwohl Discovery und Event-Zustellung lückenhaft bleiben |

### D-7 · OD-04 / BD-01 — Plugin-Isolationsstrategie

| Feld | Inhalt |
|---|---|
| **ID** | OD-04 (Spiegel BD-01) — **P4** |
| **Problem** | Plugins laufen in-process ohne Sandbox mit vollen Interpreter-Rechten. Solange keine Isolation existiert, ist **jedes** Permission-Modell — Host- wie SDK-seitig — beratend, nicht erzwingend. [R0 §7.1 RT-01, §10.4 SEC-04] |
| **Warum Entscheidung erforderlich** | Security-Architekturentscheidung; ADR-009 und das ODD-Register sind offen; neue ADRs sind ausdrücklich **nicht** autorisiert und je ADR einzeln freizugeben |
| **Betroffene Komponenten** | `app/bootstrap/stages_plugin.py` (Aktivierung), `sdk/**`, Security Foundation |
| **Betroffene Sprints** | **keiner** — nicht Milestone-1.0-Scope |
| **Security-Auswirkung** | **fundamental** — jede spätere Fähigkeit, die Fremd- oder KI-erzeugten Code ausführt (Agents, Tools, Automation, Trading-Strategien), **erbt** diese Eigenschaft |
| **Produkt-Auswirkung** | Voraussetzung für belastbare Zusagen gegenüber Dritt-Plugin-Autoren |
| **Optionen** | **Werden ausdrücklich nicht aufgezählt** — die Optionsbildung wäre bereits Security-Architekturarbeit [R0 §20 OD-04] |
| **Empfehlung** | **Keine.** Reine Feststellung: Diese Entscheidung sollte **vor** jeder Fähigkeit fallen, die Fremd- oder KI-erzeugten Code ausführt. Das ist eine sachliche Konsequenzbeschreibung, **keine** von mir gesetzte Vorbedingung |

### D-8 · BD-02 — Kryptografieverfahren (ODD-19)

| Feld | Inhalt |
|---|---|
| **ID** | BD-02 / TD-20 — **P4** für das Verfahren, **P1** für die Sichtbarmachung |
| **Problem** | `ReversibleEncryptionService` leistet Base64-**Kodierung, keine Verschlüsselung**, und ist der **stillschweigende Default** für `SecretVault` **und** `BackupManager`. Secrets und Backups sind gegenüber jedem, der die Daten lesen kann, effektiv im Klartext. [R0 §10.7 SEC-08] |
| **Warum Entscheidung erforderlich** | Kryptografie ist **ODD-19** und offen. ODDs sind Designentscheidungen und ausdrücklich **nicht** über Correction Cycles zu behandeln. Es liegt **kein Verstoß gegen eine getroffene Entscheidung** vor — kritikwürdig ist die **Benennung** |
| **Betroffene Komponenten** | `app/security/encryption_service.py`, `app/security/secret_vault.py`, `app/security/backup_manager.py`, `app/security/security_manager.py` |
| **Betroffene Sprints** | keiner |
| **Security-Auswirkung** | **hoch** — RK-09: Missverständnis als Schutzmechanismus |
| **Produkt-Auswirkung** | begrenzt, solange keine echten Secrets abgelegt werden |
| **Optionen** | **Kein Verfahren wird vorgeschlagen oder ausgewählt.** Trennbar ist lediglich: Verfahrensentscheidung (ODD-19, blockiert) **vs.** Sichtbarmachung (PC-07, entscheidbar) |
| **Empfehlung** | **PC-07 als eigenständige, kleine Entscheidung behandeln:** Startup-Warnung bei aktivem Platzhalter + Namensklarheit. Das ist keine ODD-Auflösung und keine Kryptografiewahl |

### D-9 · Weitere Entscheidungen geringerer Dringlichkeit

| ID | Prio | Gegenstand | Empfehlung |
|---|---|---|---|
| **TD-07** | P2 | `ServiceRegistry`-Thread-Sicherheit — Kernkomponente ohne FR-Deckung | Entscheiden, ob im Milestone behandelt oder zurückgestellt; Test TG-7 |
| **TD-15 / PC-03** | P2 | `entry_point` auswerten — ADR-011-Berührung möglich | Vor Umsetzung ADR-Berührung prüfen |
| **TD-16** | P2 | Fail-open bei unparsbarer Versionsangabe — ADR-007-Semantik | Ablehnen statt ignorieren, nach ADR-007-Prüfung |
| **TD-18 / PC-04** | P2 | Identifier-Validierung — Security-Härtung ohne FR | Ausschließlich verschärfend; geringer Aufwand |
| **TD-09 / PC-05** | P2 | Reproduzierbarer Verifikationslauf / CI — neue Datei | Nach OD-03 |
| **OD-08** | P3 | Statuskopf des Sprint Plans | Redaktionell, mit OD-01 bündeln |

---

## 3. WORK THAT CAN PROCEED

> **Vorbehalt:** Alle folgenden Positionen liegen **innerhalb bestehender
> Sprint-/WP-Autorisierung** und benötigen **keine** zusätzliche Architektur-
> oder Governance-Entscheidung. Sie unterliegen dennoch unverändert dem
> **Coding Authorization Gate (Bedingungen 7–9 / RL-05, PENDING)**.
> [R0 §23.2 RM-01] **Es wurde keine neue Arbeit erfunden.**

### W-1 — Baseline-Messreihe erheben *(kein Coding)*

| Feld | Inhalt |
|---|---|
| **Sprint** | Vorbereitung für SPR-08 (Erhebung „zu Beginn der Umsetzung" ist Planvorgabe, OP-8) |
| **Work Package** | keines — Evidenzerhebung |
| **Ziel** | Vergleichspunkt für NFR-004 schaffen; ohne ihn ist eine Performance-Regression nicht nachweisbar |
| **Betroffene Komponenten** | vorhandene Instrumentierung: `plugin.security.validation_ms.{id}`, `plugin.dependency.resolution_ms`, `plugin.activation.duration_ms.{id}`, `startup_ms`, `EventDelivery.duration_ms` [R0 §17.1] |
| **Erforderliche Tests** | keine neuen; Messreihe gemäß IP Anhang B |
| **Security-Prüfung** | keine |
| **Erwartetes Ergebnis** | NFR-004 wird nachweisbar; GAP-NFR004 wechselt von UNKNOWN auf messbar |
| **Bezug** | PC-02, [R0 §17.4, §30 PC-02] |

### W-2 — SPR-06 / WP-005: Fehlerisolation Discovery

| Feld | Inhalt |
|---|---|
| **Sprint / WP** | SPR-06 / WP-005 (FR-010); Diagnoseanteil SPR-04 / WP-003 (FR-006) |
| **Ziel** | Ein defektes `plugin.toml` darf nicht mehr alle Plugins deaktivieren; `PluginFailed` erhält einen zuordenbaren Identifier |
| **Betroffene Komponenten** | `plugins/loader.py`, `app/bootstrap/stages_plugin.py` (`PluginDiscoveryStage`) |
| **Erforderliche Tests** | **TG-1** — defektes `plugin.toml` in Anwesenheit gültiger Plugins |
| **Security-Prüfung** | Es darf **keine** Prüfung übersprungen werden; übersprungene Manifeste müssen Warn-Log **und** Ereignis erzeugen (kein stiller Ausfall) |
| **Erwartetes Ergebnis** | FR-010 auch im Discovery-Abschnitt erfüllt; TD-14 geschlossen |
| **Bezug** | PC-01, TD-14, [R0 §9.3, §30 PC-01] |

### W-3 — SPR-06 / WP-005: Listener-Isolation

| Feld | Inhalt |
|---|---|
| **Sprint / WP** | SPR-06 / WP-005 (FR-010) |
| **Ziel** | Ein werfender Zustandsübergangs-Listener darf die Benachrichtigung der übrigen Listener nicht unterbrechen |
| **Betroffene Komponenten** | `app/state_machine.py` |
| **Erforderliche Tests** | Negativtest mit werfendem Listener (im R0 nicht als eigene TG-ID geführt → **UNKNOWN**, Zuordnung zu TG-6 sinngemäß) |
| **Security-Prüfung** | keine |
| **Erwartetes Ergebnis** | konsistente Beobachtersicht; TD-24 geschlossen |
| **Bezug** | TD-24, [R0 §16.3 REL-02] |

### W-4 — SPR-06 / WP-005: Restart-/Recover-Hygiene

| Feld | Inhalt |
|---|---|
| **Sprint / WP** | SPR-06 / WP-005 (FR-009) |
| **Ziel** | `restart()`/`recover()` verhalten sich definiert bezüglich bereits importierter Plugin-Module und bestehender Event-Abonnements |
| **Betroffene Komponenten** | `app/application_host.py` (`_reset()`), mittelbar `core/events.py` |
| **Erforderliche Tests** | **TG-5** — Restart mit bereits importierten Plugin-Modulen |
| **Security-Prüfung** | Nach Reset muss die vollständige Pipeline erneut durchlaufen werden — kein Überspringen der Security-Stage für bereits bekannte Plugins |
| **Erwartetes Ergebnis** | TD-11 und TD-25 geschlossen; das Verhalten von `_events` ist **dokumentiert** (R0 hält fest: beide Varianten vertretbar, die fehlende Aussage ist der Mangel) |
| **Bezug** | TD-11, TD-25, [R0 §7.4, §16.4] |

### W-5 — SPR-04 / WP-003: Rejection-Feedback präzisieren

| Feld | Inhalt |
|---|---|
| **Sprint / WP** | SPR-04 / WP-003 (FR-006) |
| **Ziel** | Ablehnungen weisen Pipelinestufe und verletztes Kriterium konsistent aus; Diagnose-Docstring und Implementierung stimmen überein |
| **Betroffene Komponenten** | `app/bootstrap/stages_plugin.py` (`_validate_for_activation`, `_reject_plugin`), `app/bootstrap/types.py` (`ValidationDiagnostic`, `RejectionCode`) |
| **Erforderliche Tests** | Test je `RejectionCode`; Prüfung, dass `permissions_valid` nicht irreführend belegt ist |
| **Security-Prüfung** | Ablehnungsgründe dürfen keine sensiblen Details preisgeben; `PluginRejected` muss weiterhin für jede Ablehnung ausgelöst werden |
| **Erwartetes Ergebnis** | TD-26 geschlossen; Beitrag zu QG-004 |
| **Bezug** | TD-26, [R0 §18.3, §24.1] |

### W-6 — SPR-05 / WP-004: Observability *(OTD-1 vorher festlegen)*

| Feld | Inhalt |
|---|---|
| **Sprint / WP** | SPR-05 / WP-004 (FR-007/FR-008) |
| **Ziel** | Erweiterbare Observability (FR-008 ist der einzige **MISSING**-Befund der Gap-Analyse); Metrics-Robustheit |
| **Betroffene Komponenten** | `core/observability.py` (`Metrics`, `HealthCheck`, `PluginHealthCheck`) |
| **Erforderliche Tests** | **TG-7** (Nebenläufigkeit) sinngemäß für `Metrics`; Erweiterungspunkt-Tests |
| **Security-Prüfung** | Metrik-Schlüssel enthalten manifestgesteuerte Werte → Kardinalität begrenzen |
| **Erwartetes Ergebnis** | FR-008 von MISSING auf erfüllt; TD-10 geschlossen |
| **Vorbedingung** | **OTD-1** (die „festzulegen"-Position in MWB-008) — im Sprint Plan als für den betroffenen Teil blockierend geführt |
| **Bezug** | GAP-FR008, TD-10, [R0 §21.3, §23.4] |

### W-7 — SPR-07 / WP-007: Dokumentation nachführen

| Feld | Inhalt |
|---|---|
| **Sprint / WP** | SPR-07 / WP-007 (FR-011/FR-012) |
| **Ziel** | Dokumentation gibt den implementierten Stand wieder |
| **Betroffene Komponenten** | `docs/baselines/bootstrap-baseline-1.0.md` (§3.1 „20" vs. 22 · §5.2 fünf vs. sechs Pipeline-Schritte), `docs/sdk.md`, `docs/extensions.md`, CLAUDE.md-Projektstruktur (`ai/`, `styles/` fehlen), Integritäts-Wirkungsgrenze |
| **Erforderliche Tests** | keine — Dokumentenprüfung/Vollständigkeitsabgleich (EV-W07, EV-D04) |
| **Security-Prüfung** | PC-06: die Wirkungsgrenze der Integritätsprüfung muss ausdrücklich benannt werden, damit keine falschen Sicherheitsannahmen entstehen |
| **Erwartetes Ergebnis** | TD-08, TD-12, TD-17 (Dokumentationsanteil) geschlossen; Beitrag zu QG-005 |
| **Ausdrückliche Grenze** | **Keine Änderung am FROZEN Architecture Book v2.0** — jede AB-Änderung wäre BASELINE DEVIATION |
| **Offener Punkt** | `docs/security.md` beschreibt Namen, die im produktiven Code nicht existieren — der Governance-Status der Datei ist **GF-03/GC-02, offen** → nicht eigenmächtig behandeln |
| **Bezug** | TD-08, TD-12, TD-17, PC-06, [R0 §18.3, §30 PC-06] |

### W-8 — SPR-02 / WP-001: Platform Hardening *(reduzierter Erwartungsumfang)*

| Feld | Inhalt |
|---|---|
| **Sprint / WP** | SPR-02 / WP-001 (FR-001/FR-002) |
| **Ziel** | AC-001.1..AC-002.2 verifizieren |
| **Betroffene Komponenten** | `app/state_machine.py` |
| **Erforderliche Tests** | Zustandsmaschinen-Tests für alle 10 Zustände und deren Ablehnungen (EV-W01) |
| **Security-Prüfung** | keine |
| **Erwartetes Ergebnis** | **Hinweis:** Der Ausgangszustand ist hier **besser als von ES §5.5 angenommen** — die Zustandsmaschine ist bereits tabellengetrieben, thread-safe und lehnt unzulässige Übergänge explizit ab. Der Arbeitsumfang dürfte überwiegend **Verifikation und Testabdeckung** sein, nicht Neuimplementierung |
| **Rollback** | Die Zustandsmaschine ist eine reine Tabelle → Rücknahme risikoarm |
| **Bezug** | GAP-FR001/002, [R0 §21.3 GAP-01, §25] |

### W-9 — SPR-03 / WP-002: Host Service & Extensibility *(teilweise blockiert)*

| Feld | Inhalt |
|---|---|
| **Sprint / WP** | SPR-03 / WP-002 (FR-003/FR-004) |
| **Ziel** | FR-004 (formale Erweiterungspunkte) — **umsetzbar**; FR-003 (zentrale Host-Dienst-Beschreibung) — **blockiert bis OD-02** |
| **Betroffene Komponenten** | `core/registry.py` (`descriptors()`), `core/extensions.py`, `app/bootstrap/manager.py` (`stages`-Parameter) |
| **Erforderliche Tests** | Integration Tests, ServiceRegistry-Verifikation (EV-W02) |
| **Security-Prüfung** | keine unmittelbare |
| **Erwartetes Ergebnis** | QG-002 innerhalb WP-002 abschließbar — **nur nach OD-02** |
| **Warnung** | **RK-03** — Änderungen an `ServiceRegistry` brechen die zwei `_registrations.pop()`-Aufrufstellen (TD-06). Diese Stellen **vor** Beginn sichtbar machen |
| **Bezug** | GAP-FR003, TD-06, [R0 §25, §28] |

### 3.1 Ausdrücklich **nicht** in „Work that can proceed"

Alle Positionen mit Status `READY AFTER DECISION`, `BLOCKED`, `OPEN`,
`FUTURE` oder `NOT AUTHORIZED` — insbesondere: TD-01, TD-02, TD-03, TD-04,
TD-05, TD-06, TD-07, TD-09, TD-15, TD-16, TD-18, TD-19, TD-20, TD-21, TD-22,
TD-23 (bis OD-07), TD-13, TD-27 sowie PC-03, PC-04, PC-05, PC-07, PC-08.

---

## 4. SECURITY-FIRST ITEMS

> **Keine Security-Frage wird hier gelöst.** Keine ODD wird geschlossen, kein
> Security-Finding geschlossen, kein Security-ADR erstellt oder vorgeschlagen.
> [R0 §26 SEC-GATE-01]

### 4.1 Nach Themenfeld

| Themenfeld | Position | Befund | Kennzeichnung | Bezug |
|---|---|---|---|---|
| **Security Foundation** | Komposition | `SecurityManager` wird als additive FINALIZE-Stage nachgerüstet, während die Plugin-Pipeline in LOAD_PLUGINS eigene Defaults erzeugt | **OPEN DECISION** (OD-05) | [R0 §18.4 Cluster 2] |
| **Plugin Trust** | SG-A | Pipeline-Reihenfolge (Discovery → Integrity → Permission → Dependency → Activation) unverändert | **NON-BLOCKING** — am Baseline erfüllt; Erhaltungsnachweis in SPR-09 offen | [R0 §26 SG-A] |
| **Plugin Trust** | SG-B | Kein Plugin-Code vor bestandener Prüfung (erster Import in FINALIZE) | **NON-BLOCKING** — am Baseline erfüllt; Erhaltungsnachweis offen | [R0 §26 SG-B] |
| **Plugin Trust** | TD-17 / SG-G | „Integrity Validation" = reine Manifest-Schema-Prüfung; Code wird nie gehasht oder signaturgeprüft. Quellengedeckt zurückgestellt (Spec §5.9), aber **überzeichnet benannt** | **OPEN DECISION** (Dokumentationsanteil: NON-BLOCKING, PC-06) | [R0 §10.3 SEC-01/SEC-02] |
| **Plugin Trust** | TD-18 / SG-I | Keine Identifier-Validierung vor Nutzung als Modulname/Pfadsegment | **OPEN DECISION** (PC-04) | [R0 §10.3 SEC-03] |
| **Plugin Trust** | RT-03 | `sys.path.insert(0, plugin_dir)` während der Aktivierung kann stdlib-Namen beschatten; `finally`-Behandlung korrekt | **NON-BLOCKING** — reales, aber an Dateisystemzugriff gebundenes Risiko; **kein Finding-Status**, da keine Entscheidung dies verböte | [R0 §7.3 RT-03] |
| **Permission Enforcement** | TD-04 / SG-D | Laufzeitprüfung nutzt Plugin-**Selbstdeklaration**; Host-Grants erreichen den `PluginContext` nicht | **BLOCKING** für QG-006 — **OPEN DECISION** (OD-01 + OD-05) | [R0 §10.5 SEC-05] |
| **Permission Enforcement** | TD-05 / SG-C | Default-Deny ist **nicht gegen die ausgelieferte Konfiguration nachgewiesen**; `from_config` ist toter Code | **BLOCKING** für QG-006 — **OPEN DECISION** (OD-05) | [R0 §10.6 SEC-06] |
| **Permission Enforcement** | PS-08 | Zwei Permissions-Vokabulare (Host `tuple[str]` vs. SDK `frozenset[PluginPermission]`) ohne Brücke; berührt **GC-03 (offen)** | **OPEN DECISION** | [R0 §9.8 PS-08] |
| **Isolation** | OD-04 / SG-J / BD-01 | Keine Prozess-/Thread-/Interpreter-Isolation; jedes Permission-Modell ist dadurch beratend | **BLOCKED** — ADR-009/ODD-Register offen | [R0 §10.4 SEC-04] |
| **Cryptography** | TD-20 / SG-H / BD-02 | `ReversibleEncryptionService` = Base64; stillschweigender Default für Vault **und** Backups | **BLOCKED** (ODD-19) für das Verfahren; **OPEN DECISION** für PC-07 (Sichtbarmachung) | [R0 §10.7 SEC-08] |
| **Trust Ledger** | TD-19 / SG-E | Die `PluginSecurity`-Instanz wird **nach** Admission und Aktivierung ersetzt; `IntegrityResult`/`PermissionResult` fehlen in der neuen Instanz | **BLOCKING** für QG-006 — **OPEN DECISION** (OD-05) | [R0 §10.6 SEC-07] |
| **Trust Ledger** | SEC-02 Ziff. 4/6 | Ablehnung ist innerhalb eines Laufs irreversibel; Ledger ist thread-safe | **NON-BLOCKING** — erfüllt | [R0 §10.2] |
| **Policy Wiring** | TD-05, TD-06 | Kein `[security]`-Konfigurationspfad; Kapselungsbrüche als Symptom der Reihenfolgeproblematik | **OPEN DECISION** (OD-05) | [R0 §10.6, §6.5 AM-04] |
| **AI Security** | AI-01 | KI-Bestand vollständig von der produktiven Laufzeit entkoppelt; **keine** KI-Inferenz am Baseline | **NON-BLOCKING** (heute); **FUTURE** für jede spätere Aktivierung | [R0 §11.2 AI-01] |
| **AI Security** | TD-03 | Undeklarierte externe Abhängigkeit `ollama` im innersten Ring | **OPEN DECISION** (OD-06) | [R0 §11.3 AI-02] |
| **AI Security** | AI-04 | KI-Fähigkeit für M1.0: **NOT AUTHORIZED / OUT OF SCOPE** | **FUTURE** | [R0 §11.5 AI-04] |
| **Secrets** | SEC-09 / SG-K | Secrets werden **nicht** geloggt — Vault protokolliert Namen und Metadaten, keine Werte | **NON-BLOCKING** — erfüllt | [R0 §10.7 SEC-09] |
| **Secrets** | TD-20 | Vault-Inhalte sind gegenüber Lesezugriff effektiv im Klartext | **BLOCKED** (BD-02) | [R0 §10.7 SEC-08] |
| **Auditability** | TD-21 / SG-F | Admission-Entscheidungen laufen über Logger/EventBus, **nicht** über den `AuditLogger` (existiert zu diesem Zeitpunkt nicht) | **BLOCKED** — Ereigniskatalog ist **ODD-17 (offen)** | [R0 §10.8 SEC-10] |
| **Agents / Automation** | AG-01 | Jede Agenten-/Automationsfähigkeit **erbt** SEC-04 und SEC-05 und wirft die Frage der Human Authority auf | **FUTURE** — Feststellung, **keine Vorbedingung** | [R0 §13.3 AG-01] |
| **Trading** | TR-01 | **Kein** Trading-System, **kein** Scaffolding, **keine** Trading-UI. `BrokerSecurity` ist ein Sicherheitsdienst **ohne Broker** | **FUTURE** / CONTROLLED LIVE: **NOT AUTHORIZED** | [R0 §14.1, §14.2] |

### 4.2 Security-Gates — Zusammenfassung

| Kennzeichnung | Gates |
|---|---|
| **BLOCKING** (für QG-006) | SG-C (TD-05), SG-D (TD-04), SG-E (TD-19) |
| **BLOCKED** (durch offene ODD/ADR) | SG-F (ODD-17), SG-H (ODD-19), SG-J (ADR-009) |
| **OPEN DECISION** | SG-G (TD-17), SG-I (TD-18) |
| **NON-BLOCKING / am Baseline erfüllt** | SG-A, SG-B, SG-K |

### 4.3 Security-relevante Testlücken

| ID | Lücke | Bezug |
|---|---|---|
| **TG-2** | Kein Test gegen die **produktive** Default-Policy (alle Policy-Tests injizieren eigene Policies) | TD-05, SG-C |
| **TG-3** | Kein Test der Trust-Ledger-Identität über LOAD_PLUGINS → FINALIZE | TD-19, SG-E |
| **TG-4** | Kein Test, der belegt, dass Host-Grants im `PluginContext` ankommen | TD-04, SG-D |
| **TG-9** | Kein Test für Plugin-Module mit mehreren `Plugin`-Subklassen | TD-15 |
| **TG-1 / TG-6** | Discovery- und Event-Isolation — **kritisch gegen RK-04** (FR-010-Scheinbestehen) | TD-14, TD-23 |
[SOURCE: R0 §15.4]

---

## 5. TECHNICAL DEBT CLUSTER

> Ziel: nicht 27 Einzelprobleme blind nacheinander bearbeiten, sondern die
> **gemeinsamen Ursachen** adressieren. Die Clusterbildung C1–C3 ist aus
> R0 §18.4 übernommen; **C4–C8 sind eine RECOMMENDATION dieses Dokuments**
> und im R0-Plan nicht als Cluster ausgewiesen.

### C1 — Altbestand-Cluster · **aus R0 §18.4 übernommen**

| Feld | Inhalt |
|---|---|
| **Positionen** | TD-01, TD-03, TD-22 |
| **Gemeinsame Ursache** | Nicht disponierter Vorgängerstand (`app/host.py`, `ui/*.py`, `core/worker.py`, `core/ai_manager.py`) |
| **Entlastende Entscheidung** | **OD-02** (+ OD-06 für TD-03) — **eine** Entscheidung räumt drei Schulden und den `ui/`-Altbestand |
| **Abhängigkeiten** | Option (c) von OD-02 berührt **RB-1.0** über `tests/test_foundation.py` |
| **Sekundärwirkung** | Entschärft DEV-LAYER (Schichtverstoß) und RK-06 |
| **Bezug** | [R0 §18.4 Cluster 1, §19.5] |

### C2 — Security-Verdrahtungs-Cluster · **aus R0 §18.4 übernommen**

| Feld | Inhalt |
|---|---|
| **Positionen** | TD-04, TD-05, TD-06, TD-19, TD-21 |
| **Gemeinsame Ursache** | Der `SecurityManager` wurde als *additive* FINALIZE-Stage nachgerüstet, während die Plugin-Pipeline in LOAD_PLUGINS bereits eigene Defaults erzeugt |
| **Entlastende Entscheidung** | **OD-05** (+ OD-01 für die Vertragsgrundlage von TD-04) — **eine** Entscheidung räumt bis zu fünf Schulden |
| **Abhängigkeiten** | Berührt Bootstrap Baseline §8 (Change Control); TD-21 zusätzlich an **ODD-17** gebunden |
| **Gate-Wirkung** | **QG-006** hängt vollständig an diesem Cluster |
| **Bezug** | [R0 §18.4 Cluster 2, §19.5] |

### C3 — Isolations-/Fehlerausbreitungs-Cluster · **aus R0 §18.4 übernommen**

| Feld | Inhalt |
|---|---|
| **Positionen** | TD-11, TD-14, TD-23, TD-24, TD-25 |
| **Gemeinsame Ursache** | Fehlerisolation ist an drei Stellen implementiert (Aktivierung, Disposables, Plugin-Shutdown) und an vier Stellen nicht (Discovery, Event-Zustellung, Listener, Reset) |
| **Entlastende Entscheidung** | **OD-07** für TD-23 (ADR-002); die übrigen vier sind **innerhalb SPR-06 / WP-005 umsetzbar** |
| **Abhängigkeiten** | **RK-04 (hoch)** — ohne TG-1 und TG-6 droht ein FR-010-Scheinbestehen |
| **Bezug** | [R0 §18.4 Cluster 3, §19.5] |

### C4 — Packaging & Verifikationsinfrastruktur · **RECOMMENDATION**

| Feld | Inhalt |
|---|---|
| **Positionen** | TD-02, TD-09 |
| **Gemeinsame Ursache** | Die Werkzeugkette wurde nach der GR-001-Entscheidung nicht nachgeführt; GDR-002 D-2 klammert die konfigurative Folge aus |
| **Entlastende Entscheidung** | **OD-03** — räumt TD-02 und schafft die Voraussetzung für PC-05/TD-09 |
| **Abhängigkeiten** | PC-05 setzt OD-03 voraus, sonst prüft CI den falschen Baum |
| **Sekundärwirkung** | Entschärft **RK-05 (hoch)** |
| **Kennzeichnung** | **RECOMMENDATION** — im R0-Plan nicht als Cluster geführt |

### C5 — Dokumentation & Benennung · **RECOMMENDATION**

| Feld | Inhalt |
|---|---|
| **Positionen** | TD-08, TD-12, TD-17 (Dokumentationsanteil), TD-26, TD-27 |
| **Gemeinsame Ursache** | Dokumentation und Benennung sind dem implementierten Stand nachgelaufen |
| **Entlastende Entscheidung** | **keine erforderlich** — überwiegend innerhalb SPR-07 / WP-007 und SPR-04 / WP-003 |
| **Abhängigkeiten** | Ausdrückliche Grenze: **keine Änderung am FROZEN Architecture Book**; `docs/security.md` ist an **GF-03/GC-02 (offen)** gebunden |
| **Gate-Wirkung** | **QG-005** |
| **Kennzeichnung** | **RECOMMENDATION** |

### C6 — Determinismus & Eingabehärtung · **RECOMMENDATION**

| Feld | Inhalt |
|---|---|
| **Positionen** | TD-13, TD-15, TD-16, TD-18 |
| **Gemeinsame Ursache** | An vier Stellen wird manifestgesteuerte oder dateisystemabhängige Eingabe ohne explizite Härtung bzw. ohne festgelegte Ordnung verarbeitet |
| **Entlastende Entscheidung** | **keine gemeinsame** — TD-15 (ADR-011), TD-16 (ADR-007) und TD-18 (Security-Härtung ohne FR) benötigen je eine eigene Prüfung; TD-13 ist entscheidungsfrei |
| **Abhängigkeiten** | keine untereinander |
| **Kennzeichnung** | **RECOMMENDATION** — Bündelung nur zur gemeinsamen Vorlage, **nicht** zur gemeinsamen Entscheidung |

### C7 — Kernkomponenten-Robustheit ohne FR-Deckung · **RECOMMENDATION**

| Feld | Inhalt |
|---|---|
| **Positionen** | TD-07, TD-10 |
| **Gemeinsame Ursache** | Zwei Kernkomponenten (`ServiceRegistry`, `Metrics`) sind nicht durchgängig nebenläufigkeitssicher; keine wird von einem FR adressiert |
| **Entlastende Entscheidung** | TD-10 ist über **SPR-05 / WP-004** abgedeckt; TD-07 benötigt eine eigene Entscheidung |
| **Abhängigkeiten** | RK-08 (niedrig); Test TG-7 deckt beide |
| **Kennzeichnung** | **RECOMMENDATION** |

### C8 — Kryptografie-Platzhalter · **RECOMMENDATION**

| Feld | Inhalt |
|---|---|
| **Positionen** | TD-20 |
| **Gemeinsame Ursache** | Verfahren ist an **ODD-19** gebunden und damit blockiert; die **Benennung** ist es nicht |
| **Entlastende Entscheidung** | **BD-02** für das Verfahren (blockiert); **PC-07** für die Sichtbarmachung (entscheidbar) |
| **Abhängigkeiten** | RK-09 |
| **Kennzeichnung** | **RECOMMENDATION** — die Trennung Verfahren/Sichtbarmachung ist im R0 angelegt (PC-07), aber nicht als Cluster geführt |

### 5.1 Cluster-Bilanz

| Cluster | Positionen | Entlastende Entscheidung | Entlastete Schulden |
|---|---|---|---|
| C1 | 3 | OD-02 (+ OD-06) | 3 |
| C2 | 5 | OD-05 (+ OD-01) | bis zu 5 |
| C3 | 5 | OD-07 (für 1); 4 sprintintern | 1 durch Entscheidung, 4 durch Arbeit |
| C4 | 2 | OD-03 | 2 |
| C5 | 5 | keine | 0 (reine Arbeit) |
| C6 | 4 | drei Einzelentscheidungen | 3 |
| C7 | 2 | eine Einzelentscheidung | 1 |
| C8 | 1 | BD-02 (blockiert) / PC-07 | 0 / 1 |
| **Summe** | **27** | — | — |

> **Kernaussage (aus R0 §29.4 übernommen und in dieser Matrix bestätigt):**
> **Fünf Entscheidungen — OD-01, OD-02, OD-03, OD-05, OD-07 — entlasten
> 17 der Schuldenpositionen.** [SOURCE: R0 §29.4, §19.5]

---

## 6. SPRINT ALIGNMENT

> **Der genehmigte Sprint Plan wird nicht geändert.** Wo kein Sprint existiert,
> wird **keiner erzeugt**.

### 6.1 Alignment je Sprint

| Sprint / WP | Zugeordnete Positionen | Alignment |
|---|---|---|
| **SPR-02 / WP-001** (FR-001/002) | GAP-FR001/002 (Ausgangszustand besser als angenommen) | **ALIGNED** |
| **SPR-03 / WP-002** (FR-003/004) | GAP-FR003 (blockiert bis OD-02), TD-06 (Risiko RK-03) | **PARTIALLY ALIGNED** |
| **SPR-04 / WP-003** (FR-005/006) | TD-26, TD-14 (Diagnoseanteil), PC-01 (Teil) | **ALIGNED** |
| **SPR-05 / WP-004** (FR-007/008) | GAP-FR008 (MISSING), TD-10 — **OTD-1 vorher** | **ALIGNED** (mit OTD-1-Vorbehalt) |
| **SPR-06 / WP-005** (FR-009/010) | TD-11, TD-14, TD-23 (an OD-07 gebunden), TD-24, TD-25, PC-01 | **PARTIALLY ALIGNED** |
| **SPR-07 / WP-007** (FR-011/012) | TD-08, TD-12, TD-17 (Doku), PC-06, Doku-Abweichungen | **ALIGNED** |
| **SPR-08** (Regression + Messreihe) | PC-02 / OP-8, RB-1.0-Nachweis, RK-04, RK-05 | **ALIGNED** |
| **SPR-09 / WP-006** (FR-013/014) | TD-08 (Zählgrundlage), additive Erweiterung `create_desktop_bootstrap_manager` (BS-03) | **ALIGNED** |
| **SPR-10** (Governance Closure) | OD-01..OD-08, RK-02 | **PARTIALLY ALIGNED** |

### 6.2 Positionen ohne Sprint — **NO CURRENT SPRINT**

TD-01, TD-02, TD-03, TD-04, TD-05, TD-06, TD-07, TD-09, TD-13, TD-15, TD-16,
TD-18, TD-19, TD-20, TD-21, TD-22, TD-27 · OD-01, OD-02, OD-03, OD-04, OD-05,
OD-06, OD-08 · DEV-LAYER, DEV-AB, GAP-NFR007

> **Es wird ausdrücklich kein Sprint und kein Work Package erzeugt.**
> [SOURCE: R0 §24.2]

### 6.3 Positionen als **PROPOSED CHANGE**

PC-03, PC-04, PC-05, PC-07, PC-08 — sämtlich ohne WP-Zuordnung, sämtlich
Vorschläge zur Prüfung. PC-03 hat zusätzlich eine **potenzielle
Sprint-Plan-Berührung** (ADR-011) und ist deshalb **nicht** eingeplant.
[SOURCE: R0 §30]

### 6.4 Quality-Gate-Sicht

| Gate | Berührende Positionen | Status |
|---|---|---|
| QG-001 Platform Stability | GAP-FR001/002 | **NOT STARTED** |
| QG-002 Host Service Availability | OD-02, GAP-FR003 | **NOT STARTED** |
| QG-003 Architecture Freeze Compliance | TD-08, TD-12, BS-03, OD-01 | **NOT STARTED** |
| QG-004 Developer Feedback Quality | TD-26, TD-14 (Diagnoseanteil) | **NOT STARTED** |
| QG-005 Traceability Completeness | C5-Cluster, RK-02 | **NOT STARTED** |
| QG-006 Pipeline Security Compliance | **C2-Cluster vollständig** (TD-04, TD-05, TD-19, TD-21) | **NOT STARTED** |
| QG-007 Test Coverage Maintenance | TG-1..TG-9, RB-1.0, RK-04, RK-05 | **NOT STARTED** |
| QG-008 Governance Compliance | OD-01..OD-08 | **NOT STARTED** |

> **Kein Gate wird durch dieses Dokument als PASSED markiert.**
> Alle acht bleiben **NOT STARTED**. [SOURCE: R0 §24.3 SM-01]

---

## 7. TOP 10 — WHAT WE SHOULD LOOK AT FIRST

> Sortierung nach: (1) Sicherheitsrelevanz · (2) Blockierungswirkung ·
> (3) Architekturwirkung · (4) Abhängigkeiten · (5) Produktnutzen ·
> (6) technischem Aufwand. **Nicht** nach Code-Menge.

| # | Position | Kat./Prio | Warum zuerst |
|---|---|---|---|
| **1** | **OD-05 — Security-Verdrahtung** (Cluster C2: TD-04, TD-05, TD-19, TD-21, TD-06) | C / P1 | Höchste Sicherheitsrelevanz **und** höchste Hebelwirkung: eine Entscheidung entlastet bis zu fünf Schulden und ist die **alleinige** Grundlage für QG-006. Ohne sie ist Default-Deny nicht nachgewiesen, der Trust Ledger nicht identisch über die Phasen und die Plugin-Fähigkeit produktiv abgeschaltet (RK-07) |
| **2** | **OD-01 / BD-03 — ADR-Vertragsgrundlage** | D / P0 | Einzige **P0**-Position. ADR-006 D4 ist der Vertragstext für TD-04; ohne geklärte Fassung arbeiten WP-001..WP-005 ohne eindeutige Bezugsgrundlage (RK-01) und die Phase-D-Nachweise erben die Divergenz (RK-02) |
| **3** | **TD-20 / PC-07 — Base64-„Encryption" sichtbar machen** | C / P1 | Direktes Missverständnisrisiko (RK-09): Secrets und Backups sind effektiv im Klartext, während die Benennung Schutz suggeriert. **Sehr geringer Aufwand**, keine Kryptografieentscheidung nötig — die Sichtbarmachung ist von ODD-19 sauber trennbar |
| **4** | **OD-02 / BD-06 — zweiter Composition Root** | D / P1 | Größte Architekturwirkung: berührt die Aussage „ServiceRegistry ist der einzige Kompositionsmechanismus", blockiert FR-003/QG-002 und räumt zugleich Cluster C1. **Achtung:** Option (c) berührt RB-1.0 |
| **5** | **TD-14 + TD-23 — FR-010-Isolationslücken** | B/A / P1–P2 | Zwei belegte DEVIATIONs gegen FR-010, die die ES-Gap-Analyse **unterschätzt** hat. **RK-04 (hoch):** ohne TG-1 und TG-6 droht ein Gate-Scheinbestehen, weil die überzeugende Aktivierungsisolation den Blick auf Discovery und Event-Zustellung verstellt |
| **6** | **PC-02 — Baseline-Messreihe vor Phase B** | B / P1 | Zeitkritisch und **nicht nachholbar**: ein Vergleichspunkt, der erst nach den Änderungen entsteht, kann keine Regression belegen. NFR-004 bleibt sonst dauerhaft UNKNOWN. Bereits als OP-8 im Plan vorgesehen — nur der Zeitpunkt ist die Empfehlung |
| **7** | **OD-03 — Packaging / Auslieferbarkeit** | D / P1 | Höchster **ökonomischer** Hebel bei geringem Aufwand: derzeit liefert `pip install .` die produktive Anwendung nicht aus. Zusätzlich entschärft es **RK-05 (hoch)** — die Verwechslung von 258 und 1.019 im Regressionsnachweis |
| **8** | **TD-18 / PC-04 — Identifier-Validierung** | C / P2 | Security-Härtung mit **geringem Aufwand**, ausschließlich verschärfend, und konsistent mit der bereits im SDK vorhandenen `validate_identifier`. Heute entsteht der Schutz nur als Nebeneffekt — das ist keine belastbare Grundlage |
| **9** | **OD-06 / BD-04 — `ollama` / NFR-007** | D / P1 | Maskierter Defekt (RK-06): auf sauberer Installation nicht importierbar. Kleine Entscheidung, klare Abhängigkeit zu OD-02, beseitigt zugleich den einzigen belegten Schichtverstoß |
| **10** | **OD-04 / BD-01 — Isolationsstrategie** | C / P4 | Nicht dringlich für M1.0, aber **fundamental**: jede spätere Fähigkeit (KI, Agents, Automation, Trading) erbt die fehlende Isolation. Frühzeitig auf die Governance-Agenda zu setzen ist billiger, als sie später unter Fähigkeitsdruck zu entscheiden. **Keine Empfehlung zur Lösung** — nur zur Terminierung |

### 7.1 Was bewusst **nicht** in den Top 10 steht

- **TD-01/TD-02/TD-03 einzeln** — sie sind über OD-02/OD-03/OD-06 (Plätze 4, 7, 9) bereits adressiert.
- **Der gesamte C5-Dokumentationscluster** — planmäßig in SPR-07 verortet, keine Blockade.
- **TD-07, TD-10, TD-13, TD-27** — geringe Blockierungs- und Sicherheitswirkung.
- **Alle FUTURE-Positionen** (KI, Memory, Agents, Multimodal, Trading) — nicht autorisiert, keine gegenwärtige Handlungsoption.

---

## 8. HUMAN REVIEW CHECKLIST

Für jede Position der Matrix — insbesondere für die Top 10 und die
Entscheidungen D-1 bis D-9:

```
□ Entscheidung erforderlich
□ Security prüfen
□ Architektur prüfen
□ Sprint-Zuordnung prüfen
□ Opus-Empfehlung akzeptieren
□ Opus-Empfehlung ändern
□ Punkt zurückstellen
□ Arbeitspaket freigeben
```

### 8.1 Vorschlag für die Bearbeitungsreihenfolge

| Schritt | Gegenstand | Checkliste anzuwenden auf |
|---|---|---|
| 1 | Die vier P0/P1-Governance-Entscheidungen | D-1 (OD-01), D-2 (OD-02), D-3 (OD-05), D-4 (OD-03) |
| 2 | Die security-nahen Kleinentscheidungen | D-8 (PC-07), D-9 (PC-04/TD-18) |
| 3 | Die verbleibenden P1-Auslegungen | D-5 (OD-06), D-6 (OD-07) |
| 4 | Freigabe der arbeitsfähigen Pakete | W-1 bis W-9 (Kap. 3) — **nach** dem Coding Authorization Gate |
| 5 | Terminierung der blockierten Themen | D-7 (OD-04/BD-01), BD-02 (ODD-19) |
| 6 | Redaktionelles | OD-08, Zählkorrektur R0 §19 (Kap. 0.2) |

### 8.2 Erinnerung an die harten Grenzen

> **CODING = NOT AUTHORIZED.** Bedingungen 7–9 / RL-05: Nr. 7 PENDING,
> Nr. 8 ERFÜLLT (SPR-01), Nr. 9 PENDING. Kein Punkt aus Kapitel 3 darf vor
> Bestehen dieses Gates begonnen werden. [SOURCE: R0 §23.2]

---

## 9. Final Verification

| Prüfung | Ergebnis |
|---|---|
| R0-Plan unverändert | **BESTÄTIGT** — `docs/audits/jochen-x-master-engineering-plan-r0.md` wurde nicht geöffnet zum Schreiben und nicht geändert |
| Keine bestehende Datei geändert | **BESTÄTIGT** |
| Genau **eine** neue Matrix erstellt | **BESTÄTIGT** — `docs/audits/jochen-x-decision-execution-matrix-r0.md` |
| Keine Entscheidung getroffen | **BESTÄTIGT** — alle Positionen tragen OPEN / BLOCKED / READY AFTER DECISION / FUTURE / NOT AUTHORIZED |
| Keine Implementierung | **BESTÄTIGT** — kein Code, kein Test, keine Konfiguration berührt |
| Keine Sprint-Plan-Änderung | **BESTÄTIGT** — kein Sprint erzeugt, keiner umbenannt, kein Work Package geschaffen |
| Keine Coding Authorization | **BESTÄTIGT** — CODING = NOT AUTHORIZED |
| Kein Technical-Debt-Eintrag geschlossen | **BESTÄTIGT** — alle 27 bleiben OPEN |
| Keine Open Decision geschlossen | **BESTÄTIGT** — OD-01..OD-08 bleiben offen |
| Keine ODD geschlossen | **BESTÄTIGT** — ODD-01..ODD-20, insbesondere ODD-17 und ODD-19, unberührt |
| Kein Security Finding geschlossen | **BESTÄTIGT** |
| Kein neuer ADR erstellt | **BESTÄTIGT** |
| Keine Governance-, Architektur- oder Security-Entscheidung | **BESTÄTIGT** |
| Kein Commit | **BESTÄTIGT** |
| Kein Tag | **BESTÄTIGT** |
| Kein Push | **BESTÄTIGT** |
| RB-1.0 unverändert | **BESTÄTIGT** — 258 Tests / 14 Dateien, nicht berührt |
| `src/jochen_x/**` unberührt | **BESTÄTIGT** |

### 9.1 Abweichungen gegenüber dem Auftrag — offengelegt

| # | Abweichung | Begründung |
|---|---|---|
| 1 | Der Auftrag nennt „die **26** Technical-Debt-Positionen"; diese Matrix führt **27** | Die Tabellen in R0 §19.1–§19.4 enthalten 27 lückenlos nummerierte Einträge (TD-01…TD-27, davon 8 HIGH). Die Summenzeile „26" in R0 §19 ist eine Fehlzählung. Da der Auftrag „keine Position stillschweigend entfernen" verlangt, wurden alle 27 übernommen und die Differenz in Kap. 0.2 offengelegt. **Der R0-Plan wurde dafür nicht geändert.** |
| 2 | Kapitel 5 enthält acht Cluster (C1–C8), während R0 §18.4 drei nennt | C1–C3 sind aus R0 §18.4 unverändert übernommen; C4–C8 sind als **RECOMMENDATION** gekennzeichnet, damit alle 27 Positionen genau einem Cluster zugeordnet sind |
| 3 | Für W-3 (Listener-Isolation) ist im R0 keine eigene TG-ID geführt | Als **UNKNOWN** gekennzeichnet, nicht ergänzt und nicht erraten |

---

**Ende JOCHEN X — Decision & Execution Matrix (DRAFT, R0, NON-NORMATIVE) —
Primärquelle: `docs/audits/jochen-x-master-engineering-plan-r0.md` ·
Baseline: `MILESTONE-1.0-BASELINE = 8fcf42f1997dfcf6ff232e75fd33c37b933991c8`**
