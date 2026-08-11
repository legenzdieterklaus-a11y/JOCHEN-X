# ADR 012: Policy-Konfiguration in der bestehenden PluginSecurityStage (OD-05 Option B)

**Status:** Accepted

> **ACCEPTED / REGISTERED** — genehmigt durch Human-Entscheidung des
> Projekteigners am 2026-08-11 [Approval Record: `docs/audits/hd-4-approval-decision-r0.md`
> (HD4-APP-01-R0)]; registriert als **ADR-012** per `docs/audits/hd-4-a1-registration-r0.md`
> (HD4-A1-R0). Erstellt als HD-4 ADR-Entwurf R0.
>
> **Registrierungsvermerk:** Bei der Registrierung wurden ausschließlich
> mechanische Status-/ID-Nachführungen vorgenommen (Titel, dieses Banner,
> Kap. 1, Kap. 2, Kap. 22). Alle übrigen Kapitel — einschließlich der
> Statusangaben „DRAFT"/„AUSSTEHEND"/„NICHT VERGEBEN" in Kap. 1.1, 19, 20
> und 21 — dokumentieren unverändert den historischen R0-Entwurfsstand vor
> der Genehmigung und sind durch dieses Banner sowie die Records
> HD4-APP-01-R0/HD4-A1-R0 überholt. Offene Positionen (OI-1 … OI-7, UNKNOWNs)
> bleiben davon unberührt offen.
>
> **CODING = NOT AUTHORIZED** · **RL-05 = NOT REACHED** · **QG-006 = NOT STARTED**

---

## 1. Document Identity

| Feld | Wert |
|---|---|
| Dokumenttyp | **Architecture Decision Record (registriert)** — erstellt als ADR-Entwurf im Auftrag HD-4 |
| Auftrag | **HD-4** — Erstellung des ADR-Entwurfs; Registrierung per **HD4-A1-R0** |
| Pfad | `docs/adr/012-plugin-security-policy-configuration.md` (überführt aus `docs/audits/hd-4-od05-adr-draft-r0.md`) |
| Revision | **R0** |
| **ADR-ID** | **ADR-012** — vergeben per HD4-A1-R0 (2026-08-11); zur historischen Herleitung siehe Kap. 1.1 |
| Gegenstand | **OD-05 OPTION B** — „Policy-Konfiguration in die bestehende `PluginSecurityStage` ziehen (ohne Reihenfolgeänderung)" |
| Dokumentstatus | **ACCEPTED / REGISTERED** — genehmigt per HD4-APP-01-R0 (2026-08-11) |
| ADR-Status-Feld (Dev-Standard §13) | **Accepted** |
| Datum | 2026-08-11 |
| Branch / HEAD | `milestone-1.0-governance` / `8fcf42f1997dfcf6ff232e75fd33c37b933991c8` |
| **Bezugs-Baseline** | `MILESTONE-1.0-BASELINE = 8fcf42f1997dfcf6ff232e75fd33c37b933991c8` |
| Architecture-Book-Fassung | **Welt A / Baseline-Fassung** gemäß **GDR-OD01-001** |
| Instrumentenwahl | **ADR SELECTED** [SOURCE: `docs/governance/hd-1-adr-rdr-decision.md` Kap. 6] |
| Coding | **NOT AUTHORIZED** |

### 1.1 ADR-ID — bewusst nicht vergeben

| Prüfung | Ergebnis |
|---|---|
| Definiert der Development Standard ein Dateimuster? | **JA** — `docs/adr/{NNN}-{kebab-case-title}.md` [SOURCE: `docs/development-standard-v1.1.md` §13 „ADR-Format"] |
| Definiert eine autorisierte Quelle ein **Nummernvergabe- oder Registrierungsverfahren**? | **NEIN** — geprüft per Volltextsuche in `docs/development-standard-v1.1.md`, `docs/baselines/bootstrap-baseline-1.0.md`, `docs/core-principles-1.0.md`, `docs/milestone-1.0-implementation-plan.md` und BASELINE `8fcf42f:docs/architecture-book-v2.md`. Einziger einschlägiger Treffer ist das **Dateimuster** `{NNN}` in Development Standard §13; eine **Vergabe- oder Registrierungsregel** enthält keine dieser Quellen. Der Befund ist auf die genannten fünf Quellen begrenzt |
| Hat HD-1 eine ID festgelegt? | **NEIN** — HD-1 SF-14 führt den Bestand **ADR-001 … ADR-011** und **RDR-001** ausdrücklich als **reine Bestandsangabe**: „Aus ihr wird **keine** Nummer, **keine** Reihenfolge und **keine** Zuordnung für das künftige Instrument abgeleitet; die Identifikatorvergabe gehört zu **HD-4**" [SOURCE: `docs/governance/hd-1-adr-rdr-decision.md` Kap. 8 SF-14] |
| Zusatzbefund zum ADR-Register | Die Register-Lage ist derzeit **nicht eindeutig**: ADR-005/006/007 stehen in **Welt A** auf `Open`, in **Welt B** auf `APPROVED`; die Disposition ist per **GDR-OD01-001** **getrennt** [SOURCE: `docs/governance/od-05-governance-decision.md` **Kap. 4 (Source Gate)**, Tabellenzeile 12] und **noch nicht erfolgt** [SOURCE: `docs/governance/f-01-od05-architecture-freeze-assessment.md` Kap. 2.2 i. V. m. Kap. 2.3 — ADR-005/006/007 zählen zu den dort benannten sechs uncommitteten Dokumentänderungen] |

> **Konsequenz:** Eine ADR-Nummer wird **nicht** eigenmächtig vergeben. Der Entwurf
> wird als **Draft-Artefakt** unter `docs/audits/` geführt.
> **Die endgültige ADR-ID und die Registrierung unter `docs/adr/` sind Gegenstand
> der noch ausstehenden Genehmigung — sie werden hier nicht vorweggenommen.**
> Diese Position wird als **OI-7** geführt (Kap. 19).

### 1.2 Verhältnis zum Development Standard §13

Der Development Standard hat gemäß Auftrag Vorrang vor der vorgegebenen
Gliederung. Abgleich der **Pflichtinhalte** [SOURCE: `docs/development-standard-v1.1.md` §13 „ADR-Format"]:

| Pflichtinhalt §13 | Erfüllt in |
|---|---|
| **Status:** `Open \| Accepted \| Resolved by ADR-XXX` | Kap. 2 |
| **Problem:** Was MUSS entschieden werden | Kap. 4 |
| **Alternativen:** mindestens zwei Optionen mit Vor-/Nachteilen | Kap. 12 |
| **Lösung:** gewählte Alternative mit Begründung | Kap. 6 |
| **Konsequenzen:** Auswirkungen auf bestehenden Code und zukünftige Arbeit | Kap. 13, 14 |

**Terminologie-Auflösung.** Der Auftrag erlaubt „`DRAFT — PENDING GOVERNANCE
APPROVAL` **oder** die exakt im Development Standard vorgesehene Draft-Terminologie,
falls dort eine verbindliche Form existiert". Eine verbindliche Form **existiert**:
das Status-Feld eines ADR kennt nur `Open`, `Accepted` und `Resolved by ADR-XXX`
[SOURCE: `docs/development-standard-v1.1.md` §13, §17 Anhang B „Approval States"].
Ein Status `DRAFT` ist für ADRs **nicht** vorgesehen.

> **Auflösung:** Das **ADR-Status-Feld** lautet **`Open`** (normkonform).
> Der **Dokumentstatus** dieses Artefakts lautet **DRAFT / NON-NORMATIVE /
> PENDING APPROVAL** (Auftrag Kap. 21). Beides ist widerspruchsfrei: `Open`
> bezeichnet die noch nicht genehmigte Entscheidung, `DRAFT` den Zustand des
> Dokuments. **Es wird keine neue Statusterminologie eingeführt.**

---

## 2. Status

| Feld | Wert |
|---|---|
| **Status (ADR-Feld nach Dev-Standard §13)** | **Accepted** |
| **Dokumentstatus** | **ACCEPTED / REGISTERED** (per HD4-APP-01-R0 / HD4-A1-R0) |
| **Genehmigt?** | **JA** — Human-Entscheidung des Projekteigners, 2026-08-11 [SOURCE: `docs/audits/hd-4-approval-decision-r0.md`] |
| **Implementierung autorisiert?** | **NEIN** |
| **Resolved by** | — |

---

## 3. Context

### 3.1 Governance-Kette (übernommen, nicht neu analysiert)

| Entscheidung | Inhalt | Status |
|---|---|---|
| **GDR-OD05-001** | **OD-05 = OPTION B** — „Policy-Konfiguration wird in die bestehende `PluginSecurityStage` gezogen. Die bestehende Phasen-/Stage-Reihenfolge wird durch diese Entscheidung **NICHT** geändert." | **FINAL** [SOURCE: `docs/governance/od-05-governance-decision.md` Kap. 8] |
| **G-1** | **OPTION HYBRID — präzisiert** durch NAW-B: wirkungsbezogene Auslegung von §8-4 | **PRECISISED** |
| **NAW-A** | Change Surface fixiert: **CS-1 + CS-2 + CS-3**; `[security]` = **OPTIONAL**; **kein** neues öffentliches Symbol | **AUTHORIZED / COMPLETED** |
| **NAW-B** | `run_phase()` = **CHANGED**; `begin()` / `build_context()` = UNCHANGED; **§8-4 = TRIGGERED**; **CHANGE CONTROL = REQUIRED** | **AUTHORIZED / COMPLETED** |
| **F-4** | **TD-19 = PARTIALLY IMPACTED** (Dimension: Policy-Kontinuität); T-a/T-b/T-c **OPEN**; keine Change-Surface-Erweiterung | **COMPLETED** |
| **F-5** | §8-1/§8-2/§8-3/§8-5 = **NOT TRIGGERED**; §8-4 = **TRIGGERED**; Change Surface final; **B-6 unresolved** | **COMPLETED** |
| **HD-1** | **B-6 = ADR SELECTED** — menschliche Governance-Entscheidung des Projekteigners, **ohne Präzedenzwirkung** | **COMPLETED / FINAL** |

> Diese Positionen werden von diesem Entwurf **übernommen** und **nicht erneut
> analysiert oder zur Disposition gestellt**.

### 3.2 Ebenentrennung

> **BASELINE ≠ WORKING TREE ≠ UNTRACKED DOCS.**

| Ebene | Verwendung in diesem Entwurf |
|---|---|
| **BASELINE** (`8fcf42f`) | **Alleinige** Grundlage aller Aussagen über bestehenden Code und über das Architecture Book (`git show 8fcf42f:<pfad>`) |
| **WORKING TREE** | Sechs getrackte Modifikationen (`CLAUDE.md`, `ROADMAP.md`, ADR-005/006/007, Architecture Book) — **nicht** als Baseline-Wahrheit behandelt |
| **UNTRACKED DOCS** | Governance-/Audit-Dokumente einschließlich dieses Entwurfs — **niemals** Baseline |

### 3.3 Technischer Ist-Zustand am Baseline (CURRENT STATE)

**Sämtliche Befunde read-only über `git show 8fcf42f:<pfad>` erhoben.**

| # | Befund (CURRENT STATE) | Fundstelle |
|---|---|---|
| **CU-1** | `PluginSecurityStage` ist ein frozen Dataclass mit `name = "plugin_security"` und `phase = StartupPhase.LOAD_PLUGINS` | [SOURCE: BASELINE `8fcf42f:app/bootstrap/stages_plugin.py` — `PluginSecurityStage`] |
| **CU-2** | Die Stage importiert lokal `from app.security.plugin_security import IntegrityPolicy, PluginSecurity`. **`PermissionPolicy` ist dort nicht importiert** | [SOURCE: ebd. Z. 257] |
| **CU-3** | Die Stage versucht `registry.get(PluginSecurity)`; im Zweig `except LookupError` erzeugt sie `PluginSecurity(events, logger=logger)` — **ohne Policy-Argumente** — und registriert sie | [SOURCE: ebd. Z. 262–266] |
| **CU-4** | Dieser Zweig greift **stets**, da vor LOAD_PLUGINS **keine** Registrierung von `PluginSecurity` existiert; es gibt genau zwei Registrierungsstellen, keine davor | [SOURCE: `docs/governance/f-04-od05-td19-scope-assessment.md` Kap. 9.1, 9.2] |
| **CU-5** | Die Admission vollzieht sich vollständig in dieser Stage, in vier Schritten: **Integrity → API-Version → Permission → Dependency Resolution** | [SOURCE: BASELINE `8fcf42f:app/bootstrap/stages_plugin.py:271–333`] |
| **CU-6** | Am Ende gilt `context.admitted_manifests = resolved`; anschließend wird ein gefilterter `PluginCatalog` registriert (unter Entfernung des vorherigen Eintrags) | [SOURCE: ebd. Z. 335–339] |
| **CU-7** | `PluginSecurity.__init__` nimmt **bereits** die keyword-only Parameter `integrity_policy` und `permission_policy` entgegen; fehlen sie, gelten `IntegrityPolicy()` bzw. `PermissionPolicy()` | [SOURCE: BASELINE `8fcf42f:app/security/plugin_security.py` — `PluginSecurity.__init__`] |
| **CU-8** | `IntegrityPolicy.from_config` existiert und ist **total**: unbekannte Schlüssel werden ignoriert, ungültige Werte fallen auf sichere Defaults (`STRUCTURAL`, `"manifest"`, `VERIFIED`) zurück | [SOURCE: ebd. — `IntegrityPolicy.from_config`] |
| **CU-9** | `PermissionPolicy.from_config` existiert und ist **total**: Nicht-Listen ⇒ leeres `wildcard`; Nicht-Mapping ⇒ leere `grants` — **Default-Deny** | [SOURCE: ebd. — `PermissionPolicy.from_config`, `granted_for`] |
| **CU-10** | `config/default.toml` enthält `[application]`, `[database]`, `[plugins]` — **keinen `[security]`-Abschnitt** | [SOURCE: BASELINE `8fcf42f:config/default.toml`] |
| **CU-11** | `ApplicationSettings` ist ein frozen Dataclass mit **sieben** Feldern, ohne Security-Feld; `from_mapping` liest die drei Pflichtabschnitte und wandelt `KeyError`/`TypeError`/`ValueError` in `ConfigurationError` | [SOURCE: BASELINE `8fcf42f:config/settings.py` — `ApplicationSettings`] |
| **CU-12** | `ConfigurationService.load()` liest, mergt optional das Profil und gibt `ApplicationSettings` zurück — die **rohe TOML-Abbildung wird verworfen**; `_read`/`_merge` sind privat | [SOURCE: ebd. — `ConfigurationService`] |

> **Folgerung aus CU-3/CU-7/CU-8/CU-9:** Die Policy-**Infrastruktur** existiert
> vollständig; was fehlt, ist ausschließlich der **Konfigurationsweg** zu ihr.
> [INFERENCE: aus CU-3, CU-7, CU-8, CU-9 — deckungsgleich mit
> `docs/governance/f-05-od05-change-control-determination.md` Kap. 5.2 V-4/V-5]

---

## 4. Problem Statement

### 4.1 Was MUSS entschieden werden

> **Auf welchem Weg wird die bestehende Policy-Infrastruktur der
> Plugin-Admission konfigurationsabhängig versorgt, ohne die bestehende
> Phasen- und Stage-Reihenfolge zu verändern — und welcher Änderungsumfang wird
> dafür verbindlich festgelegt?**

### 4.2 Präzise Problembeschreibung

| # | Aussage | Klasse |
|---|---|---|
| **P-1** | `PluginSecurity.__init__` akzeptiert `integrity_policy` und `permission_policy`; beide `from_config`-Fabriken existieren und sind total (CU-7 … CU-9) | **SOURCE FACT** |
| **P-2** | Die Stage erzeugt die maßgebliche Instanz jedoch **ohne Policy-Argumente** (CU-3); es greifen daher stets die Konstruktor-Defaults | **SOURCE FACT** |
| **P-3** | `config/default.toml` besitzt keinen `[security]`-Abschnitt (CU-10), und `ConfigurationService.load()` verwirft die rohe Abbildung (CU-12) — es existiert **kein Zugang** zu einer Security-Konfiguration | **SOURCE FACT** |
| **P-4** | Der bisherige Zustand hat die relevante Policy-Erzeugung und -Verwendung damit **nicht in der vorgesehenen konfigurationsabhängigen Form** | [INFERENCE: aus P-1 bis P-3] |
| **P-5** | OD-05 adressiert die **Konfiguration der Policy-Verwendung innerhalb der bestehenden Plugin-Admission** | [SOURCE: `docs/governance/od-05-governance-decision.md` Kap. 8, 9] |

### 4.3 Ausdrückliche Abgrenzung des Problems

> **Es wird NICHT behauptet, dass „Security aktuell gar nicht funktioniert".**

| Was **nicht** behauptet wird | Was **tatsächlich** gilt |
|---|---|
| „Es findet keine Sicherheitsprüfung statt" | Die vierstufige Admission läuft am Baseline vollständig (CU-5) |
| „Die Defaults sind unsicher" | Die Defaults sind **fail-secure**: `IntegrityPolicy()` = `STRUCTURAL`/`manifest`/`VERIFIED`; `PermissionPolicy()` = **Default-Deny** (CU-8, CU-9) |
| „Plugins werden ungeprüft zugelassen" | Nicht zutreffend — jede der vier Stufen kann ablehnen (CU-5) |

> **Das Problem ist ein Konfigurations-, kein Wirksamkeitsproblem.**

### 4.4 Warum eine Governance-Entscheidung erforderlich ist

| # | Schritt | Beleg |
|---|---|---|
| **W-1** | Unter **G-1 HYBRID — präzisiert (NAW-B)** sind Zustandswerte, die durch die Ausführung einer `BootstrapStage` über den bestehenden `BootstrapContext` erzeugt oder verändert werden und „für nachfolgende Bootstrap-Stufen oder den Aufrufer **beobachtbar** sind", Bestandteil des beobachtbaren Kontrakts von `run_phase()`. Rein interne Änderungen ohne beobachtbare Wirkung bleiben außerhalb von §8-4 | [SOURCE: `docs/governance/naw-b-g1-observable-state-contract-fixation.md` Kap. 5.1 „Die maßgebliche Governance-Regel"; Kap. 1 ergänzt „beobachtbar **bzw.** für das Ergebnis der Bootstrap-Ausführung bestimmend"] |
| **W-2** | `admitted_manifests` wird von `PluginActivationStage` (FINALIZE) unmittelbar gelesen; der `PluginCatalog` wird vom Aufrufer über den `ApplicationContext` gelesen | [SOURCE: ebd. Kap. 6 M-2, Kap. 7 K-3] |
| **W-3** | Der Umriss macht beide Werte **konfigurationsabhängig** ⇒ `run_phase()` = **CHANGED** | [SOURCE: `docs/governance/f-05-od05-change-control-determination.md` Kap. 9.1] |
| **W-4** | Damit ist **§8-4 = TRIGGERED**; Bootstrap Baseline §8 verlangt eine genehmigte Governance-Entscheidung (ADR **oder** RDR) | [SOURCE: `docs/baselines/bootstrap-baseline-1.0.md` §8] |
| **W-5** | Das Instrument ist durch **HD-1** festgelegt: **ADR SELECTED** — als menschliche Governance-Entscheidung, nicht als Quellenableitung | [SOURCE: `docs/governance/hd-1-adr-rdr-decision.md` Kap. 6, 9.1] |

---

## 5. Governance Basis

| # | Grundlage | Wirkung auf diesen Entwurf |
|---|---|---|
| **GB-1** | **Bootstrap Baseline 1.0 §8** — Änderungen am `BootstrapManager` (API-Signatur, **Verhalten**) erfordern eine genehmigte Governance-Entscheidung in Form eines neuen ADR **oder** RDR | Begründet die **Pflicht** |
| **GB-2** | **HD-1 / B-6 = ADR SELECTED** | Bestimmt das **Instrument** |
| **GB-3** | **Implementation Plan GC-06** — die genehmigte Governance-Entscheidung ist **vor der Implementierung** erforderlich | Bindet die Reihenfolge; **derzeit nicht erfüllt** |
| **GB-4** | **Development Standard v1.1 §13** — ADR-Format und Pflichtinhalte | Bestimmt die **Form** (Kap. 1.2) |
| **GB-5** | **GDR-OD05-001** — OD-05 = Option B | Bestimmt die **Richtung** der Security-Verdrahtung; die **Ausgestaltung** ist ausdrücklich **nicht** Gegenstand jenes Records [SOURCE: `docs/governance/od-05-governance-decision.md` Kap. 8, Zeile „Geltungsumfang"] |
| **GB-6** | **NAW-A / NAW-B / F-4 / F-5** | Bestimmen **Umfang**, **Kontraktwirkung** und **Restrisiken** |

### 5.1 Was HD-1 ausdrücklich **nicht** trägt

| Aussage | Status |
|---|---|
| „Die Quellen schreiben vor, dass es ein ADR sein muss." | **FALSCH** — wird hier nicht behauptet |
| „Die Quellen bestimmen die Change-Control-**Pflicht**, aber nicht das **Instrument**. Der Projekteigner entscheidet daher ADR." | **KORREKT** [SOURCE: `docs/governance/hd-1-adr-rdr-decision.md` Kap. 9.1] |
| Präzedenzwirkung für künftige ADR/RDR-Fälle | **KEINE** — die Regelungslücke F-5-07 bleibt bestehen [SOURCE: ebd. Kap. 7] |
| Ein AB-§22.3-Tatbestand liegt vor | **NEIN** — keiner der sieben Tatbestände ist ausgelöst [SOURCE: ebd. Kap. 15; `docs/governance/f-05-od05-change-control-determination.md` Kap. 11] |

---

## 6. Decision

> ## **Entscheidungsvorschlag (Status: `Open` — nicht genehmigt)**
>
> **Die Policy-Konfiguration wird in die bestehende `PluginSecurityStage`
> integriert — ohne Änderung der Phasen- oder Stage-Reihenfolge.**
>
> Die bestehende `PluginSecurity`-Instanz der Stage wird mit den aus der
> Anwendungskonfiguration abgeleiteten Policies (`IntegrityPolicy`,
> `PermissionPolicy`) versorgt. **Der autorisierte Zielumriss sieht einen
> optionalen `[security]`-Abschnitt innerhalb des bestehenden
> Konfigurationsmodells vor. Die konkrete Zugangsvariante innerhalb von CS-2
> bleibt OI-3 vorbehalten.** Fehlt der Abschnitt oder ist er ungültig, gilt
> unverändert das bestehende **fail-secure Default-Verhalten**.

### 6.0 Abgrenzung — entschieden ↔ nicht entschieden

| **ENTSCHIEDEN** (durch GDR-OD05-001 / NAW-A / NAW-B — hier nur dokumentiert) |
|---|
| **OD-05 = OPTION B** |
| Policy-Konfiguration **innerhalb der bestehenden `PluginSecurityStage`** |
| **Optionaler** `[security]`-Abschnitt |
| Change Surface **CS-1 + CS-2 + CS-3** |
| **Keine** Änderung der Phasen- oder Stage-Reihenfolge |

| **NICHT ENTSCHIEDEN** (offen — durch diesen Entwurf nicht aufgelöst) |
|---|
| CS-2-Zugangsvariante **V-1 vs. V-2** (**OI-3**) |
| Konkrete Zugriffsgestaltung innerhalb von CS-2 (**OI-3**) |
| Konkrete Typprüfung innerhalb der Umsetzung (C-3 / **OI-3**) |
| **Z-1** / **Z-2** (**OI-4**) |
| **TD-19**-Restumfang (**OI-6**) |
| **HD-2** — Sprint-/WP-Zuordnung |
| **HD-3** — F4-U2 / TD-19-Einordnung |

> **Aus der obigen Präzisierung folgt ausdrücklich NICHT, dass Variante V-1
> ausgewählt wurde.** V-1 ist in NAW-A als bevorzugte minimalinvasive Variante
> **ausgewiesen**, **nicht festgelegt**
> [SOURCE: `docs/governance/naw-a-od05-change-surface-fixation.md` Kap. 6.2, NAW-A-U1].

### 6.1 Begründung der gewählten Lösung

| # | Begründung | Beleg |
|---|---|---|
| **L-1** | Option (b) ist die **eingriffsärmste** der drei geprüften Optionen | [SOURCE: `docs/governance/od-05-governance-decision.md` Kap. 9 Nr. 1] |
| **L-2** | Sie kommt **ohne Änderung der Phasen- oder Stage-Reihenfolge** aus | [SOURCE: ebd. Nr. 2] |
| **L-3** | Sie adressiert **TD-05** vollständig (Adressierungsrichtung — **nicht** Schließung) | [SOURCE: ebd. Nr. 3, Kap. 12] |
| **L-4** | Sie adressiert **TD-19 nur teilweise** | [SOURCE: ebd. Nr. 4, Kap. 12.2] |
| **L-5** | Option (a) würde demgegenüber **Baseline §8 berühren** | [SOURCE: ebd. Nr. 5] |
| **L-6** | Die Policy-Infrastruktur existiert bereits vollständig; es ist **keine** Änderung an `app/security/**` erforderlich | [SOURCE: `docs/governance/f-05-od05-change-control-determination.md` Kap. 5.2 V-4/V-5, Kap. 5.3] |

> **Diese Begründung dokumentiert die bereits getroffene Entscheidung
> GDR-OD05-001. Sie trifft keine neue Entscheidung.**

### 6.2 Was dieser Entwurf ausdrücklich **nicht** entscheidet

| # | Position | Status |
|---|---|---|
| **ND-1** | Wahl zwischen den CS-2-Varianten **V-1** und **V-2** | **OFFEN** — V-1 in NAW-A als bevorzugt ausgewiesen, **nicht** festgelegt [SOURCE: `docs/governance/naw-a-od05-change-surface-fixation.md` Kap. 6.2, NAW-A-U1] |
| **ND-2** | Behandlung von **Z-1** (`save_profile` schreibt `[security]` nicht zurück) und **Z-2** (einstufiger `_merge`) | **OFFEN** [SOURCE: ebd. Z-1, Z-2, NAW-A-U2] |
| **ND-3** | Konkrete Policy-**Werte** (Evidenzstufe, Scope, Trust-Schwelle, Grants) | **NICHT GEGENSTAND** — keine neuen Grants, kein Plugin produktiv freischalten [SOURCE: ebd. Kap. 6.3] |
| **ND-4** | Einordnung der Policy-Diskontinuität in TD-19 (**F4-U2**) | **OFFEN — HD-3** |
| **ND-5** | Sprint-/WP-Zuordnung | **OFFEN — HD-2** |

---

## 7. Scope / Change Surface

### 7.1 Die finalisierte Change Surface — abschließend

| ID | Artefakt | Zweck | Klasse |
|---|---|---|---|
| **CS-1** | `app/bootstrap/stages_plugin.py` — `PluginSecurityStage.execute` | Übergabe der konfigurierten Policies an die bestehende Security-Instanz | **REQUIRED** |
| **CS-2** | `config/settings.py` | Zugang zur `[security]`-Abbildung | **REQUIRED** |
| **CS-3** | `config/default.toml` | Optionaler `[security]`-Abschnitt | **REQUIRED** |

[SOURCE: `docs/governance/naw-a-od05-change-surface-fixation.md` Kap. 6;
`docs/governance/f-05-od05-change-control-determination.md` Kap. 5.1, Finding F-5-01;
`docs/governance/hd-1-adr-rdr-decision.md` Kap. 14]

> **Die Change Surface wird durch diesen Entwurf NICHT erweitert.**

### 7.2 Präzisierung zu CS-1 — keine Flächenerweiterung

> Der fehlende **`PermissionPolicy`**-Import innerhalb von CS-1 (CU-2) ist **keine
> Change-Surface-Erweiterung**. Eine Ergänzung läge **innerhalb von CS-1**; die
> importierte Datei `app/security/plugin_security.py` selbst wird **nicht**
> verändert.
> [SOURCE: `docs/governance/f-05-od05-change-control-determination.md` Kap. 5.2, Finding **F-5-02**]

### 7.3 Ausdrücklich ausgeschlossene Artefakte

| # | Artefakt | Klassifikation | Grund |
|---|---|---|---|
| X-1 | `app/security/plugin_security.py` | **NOT REQUIRED** | Beide Policy-Parameter und beide `from_config`-Fabriken existieren bereits (CU-7 … CU-9) |
| X-2 | `app/security/security_manager.py` | **NOT REQUIRED / separat** | Die FINALIZE-Instanz beeinflusst die Admission nicht und hat keinen produktiven Konsumenten [SOURCE: `docs/governance/f-04-od05-td19-scope-assessment.md` Kap. 9.4, 12.2 B-6] |
| X-3 | `app/bootstrap/manager.py` | **NOT REQUIRED** | Weder Signatur noch `default_stages()` noch `run_phase` müssen geändert werden [SOURCE: `docs/governance/naw-a-od05-change-surface-fixation.md` E-2] |
| X-4 | `app/bootstrap/__init__.py` | **NOT REQUIRED** | NAW-A Festlegung B — `__all__` bleibt unverändert |
| X-5 | `app/bootstrap/types.py` | **NOT REQUIRED** | `BootstrapContext` besitzt bereits alle benötigten Felder |
| X-6 | `app/bootstrap/stages_core.py`, `stages_init.py`, `stages_late.py` | **NOT REQUIRED** | Vom Umriss unberührt |
| X-7 | `core/registry.py` | **NOT REQUIRED** | TD-06-Symptomort; nicht Gegenstand |
| X-8 | `ui/navigation/navigation_service.py` | **NOT REQUIRED** | Stage-Zusammensetzung unverändert |
| X-9 | `sdk/context.py` | **NOT AUTHORIZED** | TD-04-Gebiet — durch OD-05 nicht entschieden [SOURCE: `docs/governance/od-05-governance-decision.md` Kap. 12.1] |
| X-10 | Zusätzliche Konfigurationsdateien | **NOT REQUIRED** | Nicht Teil des fixierten Umrisses |
| X-11 | Zusätzliche öffentliche APIs | **NOT REQUIRED** | NAW-A Festlegung B |
| X-12 | Packaging, CI, Deployment | **NOT REQUIRED** | Außerhalb des Umrisses |
| X-13 | `src/jochen_x/**` | **STILLGELEGT** | GR-001 / GDR-002 |

---

## 8. Technical Semantics

> **Strikte Trennung: CURRENT STATE (Baseline, belegt) ↔ INTENDED STATE
> (Zielwirkung nach einer künftigen, noch nicht autorisierten Umsetzung).**
> **Der INTENDED STATE ist nicht implementiert.**

### 8.1 Gegenüberstellung

| Aspekt | **CURRENT STATE** (Baseline `8fcf42f`) | **INTENDED STATE AFTER IMPLEMENTATION** (nicht implementiert) |
|---|---|---|
| Stage-Identität | `name = "plugin_security"`, `phase = LOAD_PLUGINS` (CU-1) | **unverändert** |
| Position in `default_stages()` | Position 9 von 13 [SOURCE: `docs/governance/f-05-od05-change-control-determination.md` Kap. 10] | **unverändert** |
| Instanzerzeugung | `PluginSecurity(events, logger=logger)` ohne Policy-Argumente (CU-3) | Instanz erhält die **aus der Konfiguration abgeleiteten** Policies |
| Wirksame Policies | stets `IntegrityPolicy()` und `PermissionPolicy()` (Konstruktor-Defaults, CU-7) | **konfigurationsabhängig**; bei fehlender/ungültiger Konfiguration **identisch mit heute** |
| Admission-Schrittfolge | Integrity → API-Version → Permission → Dependency (CU-5) | **unverändert** |
| `context.admitted_manifests` | Ergebnis der Admission (CU-6) | **konfigurationsabhängig bestimmbar** |
| Registrierter `PluginCatalog` | gefilterter Katalog (CU-6) | **konfigurationsabhängig bestimmbar** |
| `config/default.toml` | kein `[security]` (CU-10) | **optionaler** `[security]`-Abschnitt |
| Konfigurationszugang | rohe Abbildung wird verworfen (CU-12) | Zugang zur `[security]`-Abbildung über CS-2 |

### 8.2 Ausdrücklich unveränderte technische Invarianten

| # | Invariante | Beleg |
|---|---|---|
| **TI-1** | `PluginSecurityStage` bleibt in **LOAD_PLUGINS** | [SOURCE: `docs/governance/naw-a-od05-change-surface-fixation.md` Kap. 6.1] |
| **TI-2** | Die **Stage-Reihenfolge** bleibt unverändert — konstitutiver Bestandteil von Option B | [SOURCE: `docs/governance/od-05-governance-decision.md` Kap. 8] |
| **TI-3** | **Keine neue Stage** wird eingeführt; die Stage-Zusammensetzung bleibt bei 13 | [SOURCE: `docs/governance/f-05-od05-change-control-determination.md` Kap. 10] |
| **TI-4** | **Kein neuer `SecurityManager`**; `app/security/security_manager.py` ist ausgeschlossen (X-2) | [SOURCE: `docs/governance/naw-a-od05-change-surface-fixation.md` E-6] |
| **TI-5** | **Keine Änderung der `BootstrapManager`-Signatur** | [SOURCE: ebd. E-2] |
| **TI-6** | **`begin()` = UNCHANGED** — erzeugt nur einen frischen `BootstrapContext` | [SOURCE: `docs/governance/f-05-od05-change-control-determination.md` Kap. 9.1] |
| **TI-7** | **`build_context()` = UNCHANGED** — die 12 über `_require` geprüften Felder sind unberührt | [SOURCE: ebd.] |
| **TI-8** | **`run_phase()`** ist die gemäß NAW-B/F-5 **betroffene beobachtbare Semantik** — nicht seine Signatur, sondern das beobachtbare Ergebnis | [SOURCE: ebd.; `docs/governance/naw-b-g1-observable-state-contract-fixation.md` Kap. 6, 7, 9] |
| **TI-9** | **Kein neues öffentliches Symbol** in `app/bootstrap/__init__.py`; die `__all__`-**Symbolmenge bleibt identisch** | [SOURCE: `docs/governance/naw-a-od05-change-surface-fixation.md` Kap. 5, Festlegung B] · **Zählwert-Divergenz — UNKNOWN / HUMAN REVIEW REQUIRED:** Der Baseline-Stand enthält **22** `__all__`-Einträge [SOURCE: BASELINE `8fcf42f:app/bootstrap/__init__.py`]. `docs/baselines/bootstrap-baseline-1.0.md` §3.1 nennt **20**; `docs/milestone-1.0-implementation-plan.md` (APPROVED R1.2) **API-01** nennt **22** und hält die Korrektur „von 20 auf 22 … **Symbolmenge unverändert**" fest. Die Divergenz wird hier **festgestellt, nicht aufgelöst**. Sie berührt TI-9 nicht, da TI-9 die **Unverändertheit der Symbolmenge** betrifft, nicht deren Anzahl |
| **TI-10** | Die **Admission-Reihenfolge** Integrity → API-Version → Permission → Dependency → Activation bleibt unangetastet (Baseline §4 Invariante 6) | [SOURCE: `docs/baselines/bootstrap-baseline-1.0.md` §4 Inv. 6, §5.2] |

### 8.3 Beobachtbare Kontraktwirkung — Einordnung

| Methode | Ergebnis | Begründung |
|---|---|---|
| `begin()` | **UNCHANGED** | vom Umriss unberührt (TI-6) |
| **`run_phase()`** | **CHANGED** | `context.admitted_manifests` und der registrierte `PluginCatalog` sind nach NAW-B Bestandteil des beobachtbaren Kontrakts; der Umriss macht sie konfigurationsabhängig |
| `build_context()` | **UNCHANGED** | `admitted_manifests` fließt nicht ein (TI-7) |

> **Klarstellung zur Reichweite von NAW-B:** Es gilt **nicht** „jede interne
> Änderung einer Stage ist §8-4-relevant". Es gilt: eine interne Änderung ist
> relevant, wenn sie eine **beobachtbare Wirkung** auf den bestehenden
> `BootstrapManager`-Kontrakt erzeugt
> [SOURCE: `docs/governance/naw-b-g1-observable-state-contract-fixation.md` Kap. 8].

---

## 9. Security Semantics

### 9.1 Fail-Secure-Verhalten — CURRENT STATE, belegt

| # | Befund | Beleg |
|---|---|---|
| **SE-1** | `PermissionPolicy()` ohne Argumente ergibt `wildcard_grants = frozenset()` und `plugin_grants = {}` — **Default-Deny** | [SOURCE: BASELINE `8fcf42f:app/security/plugin_security.py` — `PermissionPolicy`, `granted_for`] |
| **SE-2** | `IntegrityPolicy()` ohne Argumente ergibt `STRUCTURAL` / `"manifest"` / **`VERIFIED`** als Mindest-Trust | [SOURCE: ebd. — `IntegrityPolicy`] |
| **SE-3** | Ein `[security]`-Abschnitt **ohne Grants** ergibt über `PermissionPolicy.from_config` dieselbe leere Policy wie heute — **Default-Deny bleibt erhalten** | [SOURCE: `docs/governance/naw-a-od05-change-surface-fixation.md` Kap. 6.3, S-1] |

### 9.2 Konfigurationsverhalten — INTENDED STATE (nicht implementiert)

| # | Erforderliche Eigenschaft | Herkunft |
|---|---|---|
| **C-1** | Fehlender `[security]`-Abschnitt ⇒ **sichere Defaults**, **keine** Ausnahme, **kein** neuer `BootstrapError`-Pfad in INITIALIZE | NAW-A Festlegung A |
| **C-2** | Ungültige **Werte innerhalb** des Abschnitts ⇒ sichere Defaults — bereits durch die bestehenden totalen Fabriken erfüllt (CU-8, CU-9) | NAW-A Kap. 4.3 |
| **C-3** | Ein `security`-Eintrag, der **keine Tabelle** ist (z. B. `security = "x"`), muss ebenfalls zu sicheren Defaults führen. Ein reines `raw.get("security", {})` genügt **nicht**; die Zugriffsstelle muss den Typ prüfen | NAW-A Kap. 4.3 C-3 — **offener Präzisierungsbedarf**, siehe OI-3 |

> **C-1 bis C-3 sind Eigenschaften des fixierten Umrisses — keine
> Implementierungsvorgaben und kein Code.**

### 9.3 Policy-Diskontinuität — offenes Risiko, nicht gelöst

| Feld | Inhalt |
|---|---|
| Sachverhalt (CURRENT STATE) | `SecurityBootstrapStage` (FINALIZE) entfernt die registrierte `PluginSecurity`-Instanz und setzt eine eigene [SOURCE: BASELINE `8fcf42f:app/security/security_manager.py` Z. 203–204; `docs/governance/naw-a-od05-change-surface-fixation.md` Kap. 8] |
| Zusätzliche Wirkung nach Option B | Zwischen der in LOAD_PLUGINS konfigurierten und der in FINALIZE gesetzten Instanz entstünde zusätzlich eine **Policy-Diskontinuität** [SOURCE: `docs/governance/f-04-od05-td19-scope-assessment.md` Kap. 10.2, Finding F-4-05] |
| Praktische Wirkung derzeit | **Kein produktiver Konsument** der FINALIZE-Instanz [SOURCE: ebd. Kap. 9.4, 10.3, 12.2 B-6] |
| Umsetzungsblockierend? | **NEIN** [SOURCE: ebd. Kap. 12.3] |
| Einordnung in TD-19 | **UNKNOWN / OPEN DECISION** — **F4-U2**; der dokumentierte TD-19-Wortlaut benennt Instanz-Ersetzung und Trust-Ledger-Diskontinuität, **nicht** eine Policy-Dimension [SOURCE: `docs/governance/f-05-od05-change-control-determination.md` Kap. 15] |

> **Dieser Entwurf löst die Policy-Diskontinuität NICHT und ordnet sie NICHT ein.
> TD-19 wird durch dieses ADR NICHT geschlossen.**

### 9.4 Ausdrückliche Security-Grenzen

| # | Grenze | Beleg |
|---|---|---|
| **SB-1** | **Keine neuen Grants** werden erfunden | [SOURCE: `docs/governance/naw-a-od05-change-surface-fixation.md` Kap. 6.3, S-2] |
| **SB-2** | **Kein Plugin** wird produktiv freigeschaltet | [SOURCE: ebd. S-3] |
| **SB-3** | Die konkrete Policy-Konfiguration ist **keine neue Security-Entscheidung** | [SOURCE: ebd. Kap. 6.3] |
| **SB-4** | Jedes Permission-Modell bleibt bis zur Entscheidung von **OD-04** **beratend, nicht erzwingend** | [SOURCE: `docs/governance/f-05-od05-change-control-determination.md` Kap. 16] |
| **SB-5** | Die Schlüsselnamen der Konfiguration müssen an die **bestehenden** Fabriken gebunden bleiben: `evidence_level`, `scope`, `minimum_trust` (Integrity) sowie `wildcard`, `grants` (Permission) | [SOURCE: BASELINE `8fcf42f:app/security/plugin_security.py` — `IntegrityPolicy.from_config`, `PermissionPolicy.from_config`] |

---

## 10. Architecture Invariants

| # | Invariante | Status |
|---|---|---|
| **AI-1** | **§8-1 Paketstruktur** — kein Modul im Bootstrap-Paket hinzugefügt, entfernt oder umbenannt | **NOT TRIGGERED** |
| **AI-2** | **§8-2 Runtime-Pipeline** — Phasen- und Stage-Reihenfolge unverändert | **NOT TRIGGERED** |
| **AI-3** | **§8-3 Public Exports** — `__all__`-**Symbolmenge unverändert** (zum Zählwert siehe **TI-9**: Baseline **22**, Bootstrap Baseline §3.1 **20** — Divergenz festgestellt, nicht aufgelöst) | **NOT TRIGGERED** |
| **AI-4** | **§8-4 BootstrapManager (Verhalten)** — `run_phase()` beobachtbar betroffen | **TRIGGERED** |
| **AI-5** | **§8-5 `default_stages()`** — Zusammensetzung und Reihenfolge unverändert (13 Stages, Position 9) | **NOT TRIGGERED** |

[SOURCE: `docs/governance/f-05-od05-change-control-determination.md` Kap. 6–10, Finding F-5-03]

### 10.1 Architecture Freeze

> ## **ARCHITECTURE FREEZE = UNCHANGED**

| Prüfung | Befund |
|---|---|
| **AB §22.1** — enumerierter Freeze-Scope | `app/security/**` **nicht enthalten**; `config/**` **nicht enthalten**; für das Bootstrap-Gebiet verengt auf **BootstrapStage-Protocol** und **StartupPhase-Enum** — beide vom Umriss unberührt [SOURCE: BASELINE `8fcf42f:docs/architecture-book-v2.md` §22.1] |
| **AB §22.3** — ADR-pflichtige Änderungen | **Keiner der sieben Tatbestände** ausgelöst; insbesondere **keine** Änderung der Bootstrap-Phasenreihenfolge [SOURCE: ebd. §22.3] |
| **AB §22.2** — erlaubte Änderungen | „Interne Refactorings — API-Surface unverändert" und „Bugfix in Implementierung — keine API-Änderung" sind als zulässig geführt [SOURCE: ebd. §22.2] |
| **F-1-A** | **bleibt gültig** |
| Überschneidung Freeze-Scope ↔ Change Surface | **keine** |

> **Dieser ADR-Entwurf autorisiert KEIN Architecture-Book-Update.**
> **Keine Version v2.1 oder höher wird erzeugt, beantragt oder impliziert.**
> **Der Freeze-Scope wird nicht verändert.**

**Zur Regel §13 „Wenn eine ADR den Freeze-Scope betrifft, wird eine neue
Architecture Book Version (v2.1+) erforderlich"**
[SOURCE: `docs/development-standard-v1.1.md` §13]: Diese Bedingung ist **nicht
erfüllt**, da der Umriss den Freeze-Scope nach AB §22.1 nicht berührt
(F-1-A, F-5 Kap. 11). Eine Architecture-Book-Version wird daher **nicht**
ausgelöst. Sollte eine künftige, hier **nicht** vorgeschlagene Erweiterung den
Freeze-Scope berühren, wäre das ein **separates, zukünftiges
Governance-Thema** — nicht Gegenstand dieses Entwurfs.

---

## 11. Configuration Contract

> **Beschreibung des vorgesehenen Konfigurationsvertrags. Nicht implementiert,
> nicht autorisiert.**

### 11.1 Vertragseigenschaften

| # | Eigenschaft | Klasse |
|---|---|---|
| **CC-1** | Der Abschnitt `[security]` ist **OPTIONAL** | **festgelegt** (NAW-A A) |
| **CC-2** | Fehlt er ⇒ bestehendes fail-secure Default-Verhalten, **keine** Ausnahme | **festgelegt** (C-1) |
| **CC-3** | Ungültige Werte ⇒ sichere Defaults über die bestehenden totalen Fabriken | **belegt** (CU-8, CU-9) |
| **CC-4** | Nicht-Tabelle unter `security` ⇒ ebenfalls sichere Defaults; erfordert eine Typprüfung an der Zugriffsstelle | **offener Präzisierungsbedarf** (C-3 / OI-3) |
| **CC-5** | **Keine neue Ausnahmequelle** in INITIALIZE oder LOAD_PLUGINS | **festgelegt** (NAW-A Kap. 6.3) |
| **CC-6** | Verwendung **ausschließlich** der bestehenden `from_config`-Fabriken — keine neue Parser-Logik | **festgelegt** (NAW-A Kap. 6.3) |
| **CC-7** | Schlüsselbindung an die bestehenden Fabriken (SB-5) | **belegt** |

### 11.2 Bekannte Randbedingungen des bestehenden Konfigurationswegs

| # | Befund (CURRENT STATE) | Wirkung | Status |
|---|---|---|---|
| **Z-1** | `ConfigurationService.save_profile` schreibt eine handgebaute TOML-Zeichenkette, die nur `[application]`, `[database]`, `[plugins]` umfasst — ein `[security]`-Abschnitt würde **nicht** zurückgeschrieben | Profil-Persistenz erfasst `[security]` nicht | **OFFEN** (OI-4) |
| **Z-2** | `_merge` führt eine **einstufige** Zusammenführung durch; **verschachtelte** Tabellen innerhalb eines Abschnitts werden durch die Profilfassung **vollständig ersetzt**, nicht gemischt | Ein Profil mit `[security.grants]` ersetzt die Default-Grants vollständig | **OFFEN** (OI-4) |
| **Z-3** | `ConfigurationService.load()` verwirft die rohe Abbildung; `_read` ist die einzige Lesestelle und wirft `ConfigurationError` bei `OSError`/`TOMLDecodeError` | Ein erneutes Lesen wäre eine **zusätzliche Auslösestelle** — Argument gegen CS-2-Variante V-2 | **belegt** |

[SOURCE für Z-1 … Z-3: BASELINE `8fcf42f:config/settings.py` — `save_profile`, `_merge`, `_read`, `load`;
`docs/governance/naw-a-od05-change-surface-fixation.md` Kap. 6.2 Z-1/Z-2, V-2]

### 11.3 Zugangsvarianten für CS-2 — dokumentiert, **nicht entschieden**

| Variante | Beschreibung | Bewertung laut NAW-A |
|---|---|---|
| **V-1** | Ein **zusätzliches, optionales** Feld auf `ApplicationSettings`, gespeist aus der rohen Abbildung mit sicherem Default und Typprüfung | **BEVORZUGT** — rein additiv; die sieben bestehenden Felder bleiben unverändert; keine neue öffentliche Methode; keine neue Ausnahmequelle |
| **V-2** | Ein **öffentlicher Zugang** auf `ConfigurationService` zur rohen bzw. zur `[security]`-Abbildung | **möglich, nicht bevorzugt** — erweitert die öffentliche API; erfordert erneutes Lesen (Z-3) oder Zwischenspeichern |
| **V-3** | Die Stage liest die TOML-Dateien selbst | **nicht mit der Fixierung vereinbar** — dupliziert das Laden, umgeht den Profil-Merge, führt Datei-IO in die Stage ein |

> **Es wird keine Variante gewählt.** Die Wahl bleibt der autorisierten Umsetzung
> vorbehalten — **NAW-A-U1 / OI-3**.

---

## 12. Alternatives Considered

> **Die Alternativen wurden im Governance-Verfahren geprüft und durch
> GDR-OD05-001 entschieden. Sie werden hier dokumentiert, NICHT neu bewertet.
> Es werden keine neuen Alternativen erfunden.**

**Optionswortlaut aus der Primärquelle** [SOURCE: `docs/governance/od-05-governance-decision.md` **Kap. 4 „Optionsabgleich (Stop-Condition-Prüfung)"** — dort zitiert aus R0 §20 OD-05, DEM §D-3, Briefs §D; gleichlautend in **Kap. 7 „Geprüfte Optionen"**]:

### Option (a) — `PluginSecurity` bereits in INITIALIZE komponieren und konfigurieren

| | |
|---|---|
| **Vorteile** | Die Instanz wäre vor LOAD_PLUGINS verfügbar und komponierbar; der `except LookupError`-Zweig der Stage (CU-3) würde nicht mehr greifen |
| **Nachteile** | Würde **Baseline §8 berühren** [SOURCE: `docs/governance/od-05-governance-decision.md` Kap. 9 Nr. 5]; höherer Eingriff in die Runtime-Pipeline als Option (b) |
| **Status** | **CONSIDERED DURING GOVERNANCE — NOT SELECTED by GDR-OD05-001** |

### Option (b) — Policy-Konfiguration in die bestehende `PluginSecurityStage` ziehen (ohne Reihenfolgeänderung)

| | |
|---|---|
| **Vorteile** | **Eingriffsärmste** der drei Optionen; **ohne** Änderung der Phasen-/Stage-Reihenfolge; adressiert **TD-05** vollständig und **TD-19** teilweise [SOURCE: ebd. Kap. 9 Nr. 1–4] |
| **Nachteile** | Löst **TD-19 nur teilweise**; erzeugt zusätzlich eine **Policy-Diskontinuität** gegenüber der FINALIZE-Instanz (Kap. 9.3); löst **TD-04** nicht [SOURCE: ebd. Kap. 12, 12.1, 12.2; `docs/governance/f-04-od05-td19-scope-assessment.md` Finding F-4-05] |
| **Status** | ## **SELECTED by GDR-OD05-001** |

### Option (c) — Status quo dokumentieren und im Milestone unverändert lassen

| | |
|---|---|
| **Vorteile** | Kein Eingriff; keine Change-Control-Pflicht ausgelöst |
| **Nachteile** | **Keine Verbesserung**; SG-C/SG-D/SG-E blieben nicht erfüllt bzw. nicht nachgewiesen [SOURCE: `docs/governance/od-05-governance-decision.md` **Kap. 7 „Geprüfte Optionen", Zeile (c)**] |
| **Status** | **CONSIDERED DURING GOVERNANCE — NOT SELECTED by GDR-OD05-001** |

> **Damit sind die vom Development Standard §13 geforderten „mindestens zwei
> Optionen mit Vor-/Nachteilen" erfüllt.**
> **Die Entscheidung zwischen (a), (b) und (c) wird hier nicht wiedereröffnet.**

---

## 13. Consequences

### 13.1 Positiv

| # | Konsequenz | Klasse |
|---|---|---|
| **KP-1** | Die Policy-Konfiguration erfolgt über den **bestehenden** Konfigurationsweg — kein zweiter Konfigurationsmechanismus | **Entwurfseigenschaft** |
| **KP-2** | **Keine Änderung der Pipeline-Reihenfolge** — Phasen, Stages und Admission-Schritte bleiben identisch (TI-1 … TI-3, TI-10) | **belegt** (F-5 Kap. 7, 10) |
| **KP-3** | Die bestehende `PluginSecurityStage` bleibt der **einzige** Integrationspunkt der Admission | **belegt** (CU-5) |
| **KP-4** | Die Konfigurationsabhängigkeit der Admission wird **nachvollziehbar** an einer Stelle sichtbar | [INFERENCE: aus KP-3] |
| **KP-5** | Die **Change Surface bleibt klein** — drei Artefakte, keine Änderung an `app/security/**`, `app/bootstrap/manager.py` oder am SDK | **belegt** (Kap. 7) |
| **KP-6** | **Keine neue öffentliche API** im Bootstrap-Paket (TI-9) | **belegt** (NAW-A B) |

> **Es wird keine Wirkung behauptet, die erst durch Tests nachzuweisen wäre.**
> Insbesondere wird **nicht** behauptet, dass das Default-Verhalten nach einer
> Umsetzung tatsächlich unverändert bleibt — das ist als **AC-04** zu **beweisen**,
> nicht vorauszusetzen.

### 13.2 Negativ / Risiken

| # | Konsequenz | Klasse |
|---|---|---|
| **KN-1** | **TD-19 bleibt teilweise offen** — Option B adressiert TD-19 laut Quelle nur teilweise | **belegt** [SOURCE: `docs/governance/od-05-governance-decision.md` Kap. 12.2] |
| **KN-2** | Die **Policy-Diskontinuität** zwischen der LOAD_PLUGINS- und der FINALIZE-Instanz bleibt als Risiko bestehen und wird durch diesen Entwurf **nicht** eingeordnet (F4-U2) | **belegt** (Kap. 9.3) |
| **KN-3** | **Zusätzliche Konfigurationskomplexität** — ein weiterer Abschnitt mit eigenen Gültigkeits- und Merge-Eigenschaften (Z-1, Z-2) | [INFERENCE: aus CC-1 … CC-7, Z-1, Z-2] |
| **KN-4** | **Typ- und Konfigurationsfehler** müssen berücksichtigt werden; C-3 ist ein belegter offener Präzisierungsbedarf | **belegt** (NAW-A C-3) |
| **KN-5** | **Verifikation ist erforderlich** und bisher **nicht erbracht** — TG-2/TG-3/TG-4 bleiben offen | **belegt** [SOURCE: `docs/governance/f-05-od05-change-control-determination.md` Kap. 16] |
| **KN-6** | Eine fehlerhafte Konfiguration könnte Plugins **weiter** zulassen als heute, wenn Grants gesetzt werden — deshalb SB-1/SB-2/SB-3 | [INFERENCE: aus SE-1, SB-1] |
| **KN-7** | `save_profile` erfasst `[security]` nicht (Z-1); ein gespeichertes Profil verlöre den Abschnitt | **belegt** — Behandlung **OFFEN** (OI-4) |

### 13.3 Auswirkungen auf zukünftige Arbeit

| # | Auswirkung |
|---|---|
| **KZ-1** | **HD-2** (Sprint-/WP-Zuordnung) bleibt zu entscheiden — der Umriss ist im genehmigten Sprint Plan **nicht abgedeckt** |
| **KZ-2** | **HD-3** (F4-U2) bleibt zu entscheiden |
| **KZ-3** | **QG-006** bleibt **NOT STARTED**; die Nachweise sind erst nach einer Umsetzungsfreigabe zu erbringen |
| **KZ-4** | Die CS-2-Variantenwahl (V-1/V-2) und die Behandlung von Z-1/Z-2 bleiben der autorisierten Umsetzung vorbehalten |
| **KZ-5** | Eine spätere Behandlung der Policy-Diskontinuität wäre ein **separates, zukünftiges Governance-Thema** — nicht durch diesen Entwurf autorisiert |

---

## 14. Risks

| ID | Risiko | Wirkung | Status |
|---|---|---|---|
| **R-1** | Policy-Diskontinuität LOAD_PLUGINS ↔ FINALIZE | derzeit **ohne produktiven Konsumenten**; würde wirksam, falls ein Konsument entstünde (**F4-U3**, UNKNOWN) | **OFFEN — nicht gelöst** |
| **R-2** | Nicht-Tabellen-Wert unter `security` (C-3) | könnte ohne Typprüfung an der Zugriffsstelle einen `AttributeError` und damit einen `BootstrapError` erzeugen | **OFFEN — Präzisierung erforderlich** |
| **R-3** | Profil-Merge ersetzt verschachtelte Tabellen vollständig (Z-2) | Grants aus dem Default könnten unbeabsichtigt entfallen | **OFFEN** |
| **R-4** | `save_profile` schreibt `[security]` nicht zurück (Z-1) | Konfigurationsverlust beim Speichern eines Profils | **OFFEN** |
| **R-5** | Falsch gesetzte Grants weiten die Admission aus | Sicherheitsrisiko — deshalb SB-1/SB-2/SB-3 und **AC-09** | **kontrolliert durch Grenzen, nachzuweisen** |
| **R-6** | Regression gegen **RB-1.0 (258/14)** | nicht nachgewiesen; Nachweis erst nach Umsetzungsfreigabe möglich | **UNKNOWN — AC-10** |
| **R-7** | Beobachtbare Kontraktänderung an `run_phase()` | erfordert die Change Control, die dieses ADR (nach Genehmigung) leisten soll | **adressiert durch dieses ADR — noch nicht genehmigt** |
| **R-8** | ADR-ID/Registrierung noch nicht festgelegt | Der Entwurf ist noch nicht im ADR-Register verortet | **OFFEN — OI-7** |

---

## 15. Non-Goals — OUT OF SCOPE

> **Dieses ADR — auch nach Genehmigung — bewirkt ausdrücklich NICHTS davon:**

| # | Out of Scope |
|---|---|
| **NG-1** | **Keine Implementierungsfreigabe** |
| **NG-2** | **Keine Coding Authorization** |
| **NG-3** | **Keine Sprintplanänderung** |
| **NG-4** | **Kein neues Work Package** |
| **NG-5** | **Kein Architecture-Book-Update**, keine Version v2.1+ |
| **NG-6** | **Kein Security-Redesign**, kein `SecurityManager`-Redesign |
| **NG-7** | **Kein TD-19-Closure** |
| **NG-8** | **Kein ODD-Closure** (insbesondere **ODD-17** bleibt offen) |
| **NG-9** | **Kein QG-006-Approval** |
| **NG-10** | **Keine Live-/Trading-Freigabe** |
| **NG-11** | **Keine Wallet-/Broker-Funktion** |
| **NG-12** | **Keine autonome Agentenfreigabe** |

### 15.1 Ausdrücklich nicht gelöste Positionen

Die folgenden Positionen werden **als Kontext und offenes Risiko** genannt —
**nicht** als durch dieses ADR entschieden oder gelöst:

| Position | Status |
|---|---|
| Trust-Ledger-Diskontinuität | **OFFEN** |
| Instanz-Ersetzung | **OFFEN** |
| **T-a** (Instanz-Ersetzung) | **OPEN** |
| **T-b** (Trust-Ledger-Diskontinuität) | **OPEN** |
| **T-c** (Wirkungslosigkeit für die Admission) | **OPEN** |
| **ODD-17** | **OPEN** |
| **OD-04** | **OPEN** — Permission-Modelle bleiben beratend, nicht erzwingend |
| **TD-04** | **OPEN / NOT AUTHORIZED** |
| **TD-05** | **OPEN** — Adressierungsrichtung entschieden, **nicht** geschlossen |
| **TD-06** | **OPEN** |
| **TD-19** (insgesamt) | **PARTIALLY IMPACTED / OPEN** |
| **TD-21** | **OPEN** |
| Host-Grant-System | **nicht Gegenstand** |
| Vollständige Security-Enforcement-Neuarchitektur | **nicht Gegenstand** |
| Verschlüsselungsarchitektur | **nicht Gegenstand** |
| Neue Security-ODDs / neue Security-ADRs | **werden nicht erzeugt** |

[SOURCE: `docs/governance/f-05-od05-change-control-determination.md` Kap. 15, 16;
`docs/governance/hd-1-adr-rdr-decision.md` Kap. 12, 16]

---

## 16. Acceptance Criteria

> **KEIN Kriterium ist VERIFIED. Kein Kriterium wurde geprüft. Es wurde kein
> Test ausgeführt.** Alle Kriterien sind erst nach einer künftigen, noch nicht
> erteilten Umsetzungsfreigabe zu erbringen.

**Prüfklassen:** `S` = statisch prüfbar · `T` = testbar · `G` = Governance-Nachweis · `U` = UNKNOWN / benötigt spätere Verifikation

| ID | Kriterium | Klasse | Status | Bezug |
|---|---|---|---|---|
| **AC-01** | Die Phasen- und Stage-Reihenfolge ist identisch zur Baseline; `default_stages()` liefert unverändert 13 Stages mit `PluginSecurityStage()` an Position 9 | **S** + **T** | **NOT VERIFIED** | TI-2, TI-3, AI-5 |
| **AC-02** | `PluginSecurityStage` verbleibt in `StartupPhase.LOAD_PLUGINS`; `name` bleibt `"plugin_security"` | **S** | **NOT VERIFIED** | TI-1, CU-1 |
| **AC-03** | Der Abschnitt `[security]` ist **optional**; sein Fehlen erzeugt **keinen** `ConfigurationError` und **keinen** `BootstrapError` | **T** | **NOT VERIFIED** | CC-1, CC-2, C-1 |
| **AC-04** | Ohne `[security]` ist das beobachtbare Bootstrap-Ergebnis identisch zum Baseline-Verhalten (`admitted_manifests`, registrierter `PluginCatalog`) | **T** | **NOT VERIFIED** | SE-1, SE-2, KP-2 |
| **AC-05** | Konfiguration wird typkorrekt verarbeitet: ungültige Werte **und** ein Nicht-Tabellen-Wert unter `security` führen zu sicheren Defaults, nicht zu einer Ausnahme | **T** | **NOT VERIFIED** | CC-3, CC-4, C-2, C-3 |
| **AC-06** | Keine neue öffentliche API außerhalb der finalisierten Change Surface; die `__all__`-**Symbolmenge** von `app/bootstrap/__init__.py` bleibt **unverändert** (zum Zählwert siehe **TI-9** — Divergenz festgestellt, nicht aufgelöst) | **S** | **NOT VERIFIED** | TI-9, AI-3 |
| **AC-07** | Keine Änderung an `BootstrapManager.begin()`, an der `run_phase()`-**Schnittstelle** oder an der `build_context()`-Signatur | **S** | **NOT VERIFIED** | TI-5 … TI-8 |
| **AC-08** | Die Security-Policy wird von der **vorgesehenen bestehenden Instanz** verwendet — derjenigen, die die Admission in LOAD_PLUGINS durchführt | **T** | **NOT VERIFIED** | CU-3, CU-4, Kap. 6 |
| **AC-09** | Es werden **keine unautorisierten Grants** eingeführt; Default-Deny bleibt bei leerer oder fehlender Grant-Konfiguration erhalten | **S** + **T** + **G** | **NOT VERIFIED** | SB-1, SB-2, SE-3 |
| **AC-10** | Regression gegen **RB-1.0 (258/14)** ist nachgewiesen | **T** | **NOT VERIFIED** — Nachweis erst **nach** der Umsetzungsfreigabe möglich | R-6 |
| **AC-11** | **QG-006** wird erst nach den dafür vorgesehenen Nachweisen als bestanden markiert | **G** | **NOT STARTED** | KZ-3 |
| **AC-12** | Die Änderung bleibt auf **CS-1 + CS-2 + CS-3** beschränkt; kein weiteres Bestandsartefakt wird verändert | **S** | **NOT VERIFIED** | Kap. 7 |
| **AC-13** | Die Admission-Schrittfolge Integrity → API-Version → Permission → Dependency → Activation ist unverändert | **S** + **T** | **NOT VERIFIED** | TI-10 |
| **AC-14** | Die Konfigurationsschlüssel sind an die bestehenden `from_config`-Fabriken gebunden; es wird **keine** neue Parser-Logik eingeführt | **S** | **NOT VERIFIED** | SB-5, CC-6 |
| **AC-15** | Das Verhalten bei einem Profil-Merge über `[security]` (Z-2) und bei `save_profile` (Z-1) ist bewusst festgelegt und dokumentiert | **U** | **UNKNOWN** — Behandlung noch nicht entschieden (OI-4) | Z-1, Z-2 |
| **AC-16** | Die Einordnung der Policy-Diskontinuität ist governance-seitig geklärt | **U** / **G** | **UNKNOWN** — abhängig von **HD-3 / F4-U2** | Kap. 9.3 |

---

## 17. Verification Strategy

> **Beschreibung der späteren Verifikation. NICHT AUSGEFÜHRT.**
> **Es wurde kein Test geschrieben, geändert oder ausgeführt. Kein Quality Gate
> wird als bestanden markiert.**

| # | Verifikationsgegenstand | Stufe | Bezug |
|---|---|---|---|
| **VS-1** | Policy-Ableitung aus einer Konfigurationsabbildung — Defaults, gültige Werte, ungültige Werte | Unit | AC-05, AC-14 |
| **VS-2** | Konfigurationsvarianten: kein `[security]` · leeres `[security]` · gültige Werte · ungültige Werte · Nicht-Tabelle | Unit | AC-03, AC-05 |
| **VS-3** | **Default-Verhalten**: ohne `[security]` identisches beobachtbares Bootstrap-Ergebnis | Integration | AC-04 |
| **VS-4** | **Plugin-Admission**: die vier Schritte laufen in unveränderter Reihenfolge; Ablehnungen erfolgen an derselben Stufe wie am Baseline | Integration | AC-13, AC-08 |
| **VS-5** | **Invalid configuration** / **Failure semantics**: kein neuer `BootstrapError`-Pfad in INITIALIZE oder LOAD_PLUGINS allein wegen der Security-Konfiguration | Integration | AC-03, CC-5 |
| **VS-6** | **Pipeline-Invarianz**: Stage-Zusammensetzung, -Reihenfolge und Phasenzuordnung unverändert | Unit / statisch | AC-01, AC-02 |
| **VS-7** | **Public-Surface-Invarianz**: `__all__` unverändert; keine neue öffentliche API | statisch | AC-06 |
| **VS-8** | **Observability / Auditspur**: die bestehenden Log-Ereignisse der Stage bleiben erhalten; die Konfigurationsherkunft ist nachvollziehbar — **ohne** Secrets zu protokollieren | Integration | KP-4 |
| **VS-9** | **Regression gegen RB-1.0 (258/14)** | Regression | AC-10 |
| **VS-10** | **Governance-Nachweis**: TG-2 / TG-3 / TG-4 sowie SG-C / SG-D / SG-E | Governance | KN-5 |

**Statusfeststellung:**

| Feld | Wert |
|---|---|
| Tests geschrieben | **NEIN** |
| Tests geändert | **NEIN** |
| Tests ausgeführt | **NOT EXECUTED** |
| **QG-006** | **NOT STARTED** |
| **TG-2 / TG-3 / TG-4** | **erforderlich, nicht erbracht** |
| **SG-C / SG-D / SG-E** | **nicht erfüllt / nicht nachgewiesen** |
| **RB-1.0** | **unverändert (258/14)** |

---

## 18. Rollback / Failure Considerations

> **Entwurfsebene. Keine Anweisung, keine Umsetzung.**

| # | Betrachtung | Inhalt |
|---|---|---|
| **RB-1** | **Rückbaubarkeit** | Die Change Surface umfasst drei Artefakte; die Änderung ist rein additiv gegenüber dem bestehenden Konfigurationsvertrag (`[security]` optional). Ein Rückbau erforderte keine Migration von Persistenzdaten [INFERENCE: aus CC-1, Kap. 7] |
| **RB-2** | **Konfigurations-Rollback** | Entfernen des `[security]`-Abschnitts stellt — bei erfüllter AC-04 — das Baseline-Verhalten her. **Das ist nachzuweisen, nicht vorauszusetzen** |
| **RB-3** | **Fehlersemantik** | Es soll **keine** neue Ausnahmequelle entstehen (CC-5). Ein Fehlschlagen der Policy-Ableitung soll zu sicheren Defaults führen, nicht zu einem Bootstrap-Abbruch |
| **RB-4** | **Fail-secure-Richtung** | Im Zweifel gilt die restriktivere Policy: `IntegrityPolicy()` mit `minimum_trust = VERIFIED` und `PermissionPolicy()` mit Default-Deny (SE-1, SE-2) |
| **RB-5** | **Nicht abgedeckt** | Ein Rollback der **Governance**-Entscheidung (GDR-OD05-001, HD-1) ist **nicht** Gegenstand dieses Entwurfs |
| **RB-6** | **Persistenz-Randfall** | Z-1/Z-2 (Kap. 11.2) können ein Rollback-Verhalten beeinflussen; die Behandlung ist **OFFEN** (OI-4) |

---

## 19. Open Issues

| ID | Offene Position | Status | Zuständig |
|---|---|---|---|
| **OI-1** | **HD-2** — Sprint-/WP-Zuordnung des finalisierten Umrisses | **OPEN** | Projekteigner |
| **OI-2** | **HD-3 / F4-U2** — Einordnung der Policy-Diskontinuität in TD-19 | **OPEN — UNKNOWN** | Security-/Architektur-Governance |
| **OI-3** | **NAW-A-U1** — Wahl zwischen den CS-2-Varianten V-1 und V-2 sowie die Typprüfung an der `[security]`-Zugriffsstelle (C-3) | **OFFEN** | autorisierte Umsetzung |
| **OI-4** | **NAW-A-U2** — Behandlung von Z-1 (`save_profile`) und Z-2 (einstufiger `_merge`) | **OFFEN** | autorisierte Umsetzung |
| **OI-5** | **F4-U3** — ob künftig ein Konsument der FINALIZE-Instanz entsteht | **UNKNOWN** — nicht ohne Laufzeit-/Zukunftsannahme feststellbar | — |
| **OI-6** | **F4-U1 / U-3** — „teilweise"-Restumfang von TD-19 (T-a, T-b, T-c) | **UNKNOWN / OPEN** | Security-/Architektur-Governance |
| **OI-7** | **ADR-ID und Registrierung** unter `docs/adr/` | **NICHT FESTGELEGT** — bewusst nicht vorweggenommen (Kap. 1.1) | Projekteigner / Governance |
| **OI-8** | **Genehmigung dieses ADR** | **AUSSTEHEND** | Projekteigner / Governance |

**Dokumentierte Beobachtung zum Source Gate (kein Blocker).** Die Datei
`docs/baselines/bootstrap-baseline-1.0.md` ist im Repository **untracked** und
damit nicht Bestandteil des Baseline-Commits `8fcf42f`, wird in der gesamten
Governance-Kette jedoch als **APPROVED** geführt und verwendet
[SOURCE: `docs/governance/f-05-od05-change-control-determination.md` Kap. 2 Nr. 9].
Dies ist eine **bereits bekannte, dokumentierte Governance-Lage** und wird hier
nur festgehalten — **kein HARD STOP**, keine eigenmächtige Auflösung.

---

## 20. Governance Status

| Position | Status |
|---|---|
| **HD-1** | **COMPLETED — ADR SELECTED** |
| **OD-05** | **OPTION B — FINAL** |
| **§8-4** | **TRIGGERED** |
| **§8-1 / §8-2 / §8-3 / §8-5** | **NOT TRIGGERED** |
| **CHANGE CONTROL** | **REQUIRED** |
| **ADR** | **DRAFT — NOT APPROVED** |
| **ADR-ID** | **NICHT VERGEBEN** (OI-7) |
| **CHANGE SURFACE** | **CS-1 + CS-2 + CS-3 — FINAL** |
| **ARCHITECTURE FREEZE** | **UNCHANGED** |
| **Architecture Book** | **unverändert** — keine v2.1 |
| **TD-19** | **PARTIALLY IMPACTED / OPEN** |
| **TD-04** | **OPEN / NOT AUTHORIZED** |
| **TD-05 / TD-06 / TD-21** | **OPEN** |
| **ODD-17 / OD-04** | **OPEN** |
| **QG-006** | **NOT STARTED** |
| **RL-05** | **NOT REACHED** |
| **CODING** | **NOT AUTHORIZED** |
| **Sprint Plan** | **UNCHANGED** |
| **RB-1.0** | **unverändert (258/14)** |
| **TESTS** | **NOT EXECUTED** |
| **HD-2** | **OPEN** |
| **HD-3** | **OPEN** |

### 20.1 Implementation Boundary

| Bedingung (IP §10.6 „Coding") | Status |
|---|---|
| 7 — genehmigte Sprintplanung liegt vor | **nicht erfüllt** — Sprint Plan `DRAFT 1.0 R0`; der Umriss ist darin nicht abgedeckt |
| 8 — Baseline-Bestätigung protokolliert (Phase A abgeschlossen) | **nicht erfüllt** |
| 9 — **RL-05** erreicht | **nicht erfüllt** |
| **GC-06** — genehmigte Governance-Entscheidung **vor** der Implementierung | **nicht erfüllt** — dieses ADR ist **nicht genehmigt** |

[SOURCE: `docs/governance/f-05-od05-change-control-determination.md` Kap. 21;
`docs/governance/hd-1-adr-rdr-decision.md` Kap. 18]

> **Auch die Genehmigung dieses ADR erzeugte für sich genommen KEINE Coding
> Authorization, solange RL-05 nicht erreicht ist.**

---

## 21. Approval Section

> **NICHT AUSGEFÜLLT — dieser Entwurf ist nicht genehmigt.**

| Rolle | Zuständigkeit | Datum | Ergebnis |
|---|---|---|---|
| **Projekteigner** | Genehmigung der Entscheidung | — | **AUSSTEHEND** |
| **Architektur-Governance** | Prüfung §8-Bezug, Architecture Freeze, Change Surface | — | **AUSSTEHEND** |
| **Security-Governance** | Prüfung Security-Semantik, TD-19-Abgrenzung, Default-Deny | — | **AUSSTEHEND** |
| **ADR-ID-Vergabe / Registrierung** | Zuweisung `{NNN}` und Überführung nach `docs/adr/` | — | **AUSSTEHEND (OI-7)** |

### 21.1 Für die Genehmigungsprüfung noch zu klärende Punkte (keine festgelegten Approval-Gates)

> Die folgenden Punkte sind für die weitere Governance-Prüfung relevant. Aus
> ihnen wird in diesem Entwurf **KEINE Reihenfolge**, **KEIN Approval-Gate** und
> **KEINE notwendige Vorbedingung** für die ADR-Genehmigung abgeleitet.

| # | Offener Klärungspunkt | Status |
|---|---|---|
| **A-1** | **ADR-ID / Registrierung** (OI-7) | **OFFEN** |
| **A-2** | Verhältnis **HD-3 / F4-U2** zur ADR-Genehmigung | **OFFEN** |
| **A-3** | Verhältnis **HD-2** / Sprint-/WP-Zuordnung zur ADR-Genehmigung | **OFFEN** |

**Ausdrücklich nicht entschieden:**

| Frage | Status in diesem Entwurf |
|---|---|
| Ist **HD-2** vor der ADR-Genehmigung erforderlich? | **NICHT ENTSCHIEDEN** |
| Ist **HD-3** vor der ADR-Genehmigung erforderlich? | **NICHT ENTSCHIEDEN** |
| Ist die **ADR-ID-Vergabe** vor der Genehmigung zwingend erforderlich? | **NICHT ENTSCHIEDEN** |

> Die Reihenfolge dieser Punkte wird hier **nicht** festgelegt — das
> wäre eine neue Governance-Regel.

---

## 22. Revision History

| Revision | Datum | Änderung | Status |
|---|---|---|---|
| **R0** | 2026-08-11 | Ersterstellung des ADR-Entwurfs im Auftrag **HD-4**, auf Grundlage von **HD-1 (ADR SELECTED)**, **GDR-OD05-001 (Option B)**, **NAW-A**, **NAW-B**, **F-4**, **F-5**; Bezugs-Baseline `8fcf42f` | **DRAFT / NON-NORMATIVE / PENDING APPROVAL** |
| **R0 (Registrierung)** | 2026-08-11 | Genehmigung durch Human-Entscheidung des Projekteigners (**HD4-APP-01-R0**); Registrierung als **ADR-012** unter `docs/adr/` per **HD4-A1-R0** — ausschließlich mechanische Status-/ID-Nachführung (Titel, Banner, Kap. 1, Kap. 2, diese Zeile), keine inhaltliche Änderung | **ACCEPTED / REGISTERED** |

---

## 23. Repository Integrity (Erstellungsvermerk)

| Prüfung | Ergebnis |
|---|---|
| HEAD | `8fcf42f1997dfcf6ff232e75fd33c37b933991c8` — **unverändert** |
| Baseline-Hash | `8fcf42f1997dfcf6ff232e75fd33c37b933991c8` — **unverändert** |
| Staging | **leer** |
| Getrackte Modifikationen | **6 — unverändert** |
| Bestandsdateien geändert | **0** |
| Produktivcode / Tests / Konfiguration geändert | **0** |
| Sprint Plan / Architecture Book / Security Design geändert | **0** |
| `src/jochen_x/**` | **0 Statuseinträge — unangetastet** |
| Neue Dateien | **genau 1**: dieses Dokument |
| Commit / Tag / Push / Cleanup / Löschen / Verschieben / Umbenennen | **KEINE** |

**BASELINE ≠ WORKING TREE ≠ UNTRACKED DOCS** — sämtliche Code- und
Architecture-Book-Aussagen ausschließlich über `git show 8fcf42f:<pfad>`.

---

**Ende HD-4 ADR-Entwurf R0 — OD-05 Option B — JOCHEN X Milestone 1.0
(DRAFT / NON-NORMATIVE / PENDING APPROVAL, 2026-08-11) — Bezugs-Baseline
`MILESTONE-1.0-BASELINE = 8fcf42f1997dfcf6ff232e75fd33c37b933991c8`**
