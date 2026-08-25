# JOCHEN X — Milestone 1.0
# OD-05 — Security Wiring Governance Decision

## 1. Decision Identity

| Feld | Wert |
|---|---|
| Dokumenttyp | Governance Decision Record |
| **Decision ID** | **GDR-OD05-001** |
| Titel | OD-05 — Security Wiring Governance Decision |
| Gegenstand | **OD-05** — Security-Verdrahtung im Bootstrap / Plugin Security Pipeline |
| Status dieses Records | **FINAL** |
| **Entscheidung** | **OPTION B — Policy-Konfiguration in die bestehende `PluginSecurityStage` ziehen (ohne Reihenfolgeänderung)** |
| Priorität der Position | **P1** [DEM §1.1, §D-3] |
| BD-Spiegelung | **keine** — OD-05 hat keine Blocked-Decision-Spiegelung [R0 §33.2] |
| Charakter | **Governance-Entscheidung. KEINE Implementierungsanweisung.** |
| Branch | `milestone-1.0-governance` |
| Bezugs-Baseline | `MILESTONE-1.0-BASELINE = 8fcf42f1997dfcf6ff232e75fd33c37b933991c8` |

---

## 2. Decision Authority

| Feld | Wert |
|---|---|
| Erforderliche Autorität | **Projekteigner + Architektur-/Security-Governance** [R0 §20 OD-05; Briefs §L; DEM §D-3] |
| Entscheidende Instanz | **Projekteigner JOCHEN X / autorisierte Governance-Instanz** |
| Rolle dieses Dokuments | **Dokumentation einer bereits getroffenen Entscheidung.** Dieser Record trifft, erweitert und interpretiert die Entscheidung nicht. |
| Change-Control-Bezug | **Bootstrap Baseline 1.0 §8** — der Umfang einer etwaigen ADR-/RDR-Pflicht ist für Option (b) **UNKNOWN** (Kap. 11) |

---

## 3. Decision Date

| Feld | Wert |
|---|---|
| Datum der Entscheidung | **2026-08-10** |
| Datum dieses Records | **2026-08-10** |
| Vorgelagerte Entscheidung | **GDR-OD01-001** (2026-08-10, FINAL — OD-01 Option C) |

---

## 4. Source Gate

Vor Erstellung dieses Records physisch vorhanden, lesbar und geprüft (read-only):

| # | Quelle | Status | Verifikation |
|---|---|---|---|
| 1 | `docs/audits/jochen-x-master-engineering-plan-r0.md` | R0 (Analyse ohne Entscheidungsautorität) | §10.2–§10.9, §15.4, §18.4 Cluster 2, §19.5, §20 OD-05, §24.2, §24.3, §26, §28 gelesen |
| 2 | `docs/audits/jochen-x-decision-execution-matrix-r0.md` | R0 | §1.1 (OD-05 = P1), §D-3, §4.2, C2-Cluster gelesen |
| 3 | `docs/audits/jochen-x-decision-briefs-r0.md` | R0 | Decision Brief 4 (OD-05) vollständig gelesen — A.1–A.6, B, C, D, E, F, G, H, I, J, K, L, N |
| 4 | `docs/governance/od-01-governance-decision.md` | **FINAL — GDR-OD01-001, Option C** | Kap. 8, 10, 12 gelesen; Abgrenzung OD-01/OD-05 übernommen |
| 5 | `docs/security-architecture-1.0.md` | **APPROVED**, 1.0 R0 (2026-08-08) | Kopf verifiziert; auf Aussagen zur Stage-Komposition geprüft — **keine** |
| 6 | `docs/security-design-1.0.md` | **APPROVED**, 1.0 R0 | Kopf verifiziert; auf Aussagen zur Stage-Komposition geprüft — **keine** |
| 7 | `docs/development-standard-v1.1.md` | **APPROVED**, v1.1 (2026-07-27) | Kopf verifiziert |
| 8 | `docs/baselines/bootstrap-baseline-1.0.md` | **APPROVED** | **§8 Change Control** im Wortlaut gelesen (Kap. 11) |
| 9 | `docs/milestone-1.0-implementation-plan.md` | **APPROVED R1.2** (2026-08-06) | Kopf/Dokumentstatus verifiziert; §8.7 (QG-006 nach WP-003 **und** WP-004) über Sprint Plan referenziert |
| 10 | `docs/milestone-1.0-sprint-plan.md` | **DRAFT 1.0 R0** (2026-08-09), als Planungsgrundlage genehmigt | SPR-04/WP-003, SPR-05/WP-004, QG-006-Zeile gelesen |
| 11 | `docs/architecture-book-v2.md` | **APPROVED / FROZEN (v2.0)** | Kopfstatus verifiziert; **nicht verändert** |
| 12 | `docs/adr/005…md`, `006…md`, `007…md` | Welt A `Open` / Welt B `APPROVED` — Disposition per GDR-OD01-001 getrennt | **nicht verändert** |

**Optionsabgleich (Stop-Condition-Prüfung).** Der Optionswortlaut lautet in der
Primärquelle [R0 §20 OD-05], gleichlautend übernommen in [DEM §D-3] und
[Briefs §D]:

| Option | Wortlaut aus der Quelle |
|---|---|
| **(a)** | `PluginSecurity` bereits in INITIALIZE komponieren und konfigurieren |
| **(b)** | Policy-Konfiguration in die bestehende `PluginSecurityStage` ziehen (**ohne** Reihenfolgeänderung) |
| **(c)** | Status quo dokumentieren und im Milestone unverändert lassen |

Die vom Projekteigner getroffene Entscheidung — **Option B** — ist mit diesem
Wortlaut **deckungsgleich**. Die HARD-STOP-Bedingung greift **nicht**.

**Widerspruchsprüfung W-2 / OD-01 / OD-05.** `security-architecture-1.0.md` und
`security-design-1.0.md` (beide APPROVED, W-2-Genehmigungslinie) enthalten
**keine** Festlegung zur Stage-Zusammensetzung, zur Stage-Reihenfolge oder zum
Kompositionsort von `PluginSecurity` (verifiziert per Volltextsuche auf
`PluginSecurityStage`, `SecurityBootstrapStage`, `INITIALIZE`, `from_config`,
`[security]` — 0 Treffer). **Ein Widerspruch zwischen W-2, GDR-OD01-001 und
Option B ist nicht feststellbar.** Kein HARD STOP.

> **SOURCE GATE: BESTANDEN.**

---

## 5. Ausgangslage

### 5.1 Der belegte Ablauf am Baseline

```
STARTING
├─ INITIALIZING     INITIALIZE:      Environment, Configuration, Logging,
│                                    Database, Registry, Theme, Scheduler
├─ LOADING_PLUGINS  LOAD_PLUGINS:    PluginDiscoveryStage, PluginSecurityStage
├─ LOADING_RESOURCES LOAD_RESOURCES: ResourceManager
├─ FINALIZE         FINALIZE:        PluginActivationStage, DeveloperTools,
│                                    SecurityBootstrapStage, Navigation, DI
└─ READY
```
[R0 §5.4; Briefs A.1]

> **CS-02 (SOURCE FACT):** „Die FINALIZE-Phase führt `PluginActivationStage`
> **vor** `SecurityBootstrapStage` aus." [R0 §5.4]

### 5.2 Der Kern des Problems

Die Sicherheits-Foundation und die Plugin-Pipeline sind **zwei getrennt
entstandene Kompositionen, die sich in der Zeit nicht treffen** [Briefs §B]:

- Die **Plugin-Pipeline** benötigt `PluginSecurity` in **LOAD_PLUGINS** und
  erzeugt sich dort mangels registrierter Instanz eine **Default-Instanz mit
  fest verdrahteter Policy**.
- Der **`SecurityManager`** komponiert seine `PluginSecurity` erst in
  **FINALIZE** — nach Admission **und** nach Aktivierung — und **ersetzt** die
  registrierte Instanz.

Gemeinsame Ursache laut [R0 §18.4 Cluster 2]: „Der `SecurityManager` wurde als
*additive* FINALIZE-Stage **nachgerüstet**, während die Plugin-Pipeline in
LOAD_PLUGINS bereits eigene Defaults erzeugt."

### 5.3 Cluster C2 — die fünf zugeordneten Positionen

| Position | Kurzfassung | Klassifikation (R0) |
|---|---|---|
| **TD-04** | Das Laufzeit-Permission-Gate des SDK prüft die vom Plugin **selbst deklarierten** Permissions gegen sich selbst; `PermissionResult.granted` erreicht den `PluginContext` nicht | **MISSING** (§10.9); SEC-05 **SOURCE FACT**; HIGH (technisch); ausdrücklich **keine Regression** |
| **TD-05** | `IntegrityPolicy.from_config()` / `PermissionPolicy.from_config()` ohne produktive Aufrufstelle; kein `[security]`-Abschnitt in `config/default.toml`; effektive Policy **fest verdrahtet** | **MISSING** (§10.9); SEC-06 **SOURCE FACT** |
| **TD-19** | `SecurityBootstrapStage` (FINALIZE) ersetzt die in LOAD_PLUGINS angelegte Instanz; der konsumierte Trust Ledger ist **nicht** der prüfende | **DEVIATION** (§10.9); SEC-07 INFERENCE; HIGH (technisch) |
| **TD-21** | Admission-Entscheidungen laufen über `logger`/`EventBus`, **nicht** über den `AuditLogger` (existiert zu diesem Zeitpunkt nicht) | SEC-10 INFERENCE; Substanz an **ODD-17 (offen)** gebunden; „Feststellung, keine Forderung" |
| **TD-06** | Zwei Kapselungsbrüche an der Registry (`_lock`, `_registrations.pop(...)`) | AM-04 **SOURCE FACT**; im R0 als **Symptom** von TD-19 eingeordnet, nicht als Ursache |

[Briefs A.3; R0 §10.5, §10.6, §10.8, §6.5, §19.5]

### 5.4 Was ausdrücklich NICHT das Problem ist

Aus [Briefs §B] übernommen — diese Abgrenzung ist Bestandteil der Ausgangslage:

- Die **Pipeline-Reihenfolge** ist **nicht** verletzt (BS-04; NFR-006 **MATCH**).
- **Kein Plugin-Code** läuft vor bestandener Prüfung (SG-B **erfüllt am Baseline**).
- Die **Default-Deny-Mechanik** ist **im Code implementiert** — sie ist lediglich
  nicht gegen die **ausgelieferte Konfiguration** nachgewiesen.
- Der **Integritätsumfang** (nur STRUCTURAL) ist **quellengedeckt zurückgestellt**
  (TD-17 / ADR-005 / Spec §5.9) und **kein** Bestandteil von OD-05.
- Die **fehlende Isolation** (SEC-04) ist eine **Systemeigenschaft** und Gegenstand
  von **OD-04**, nicht von OD-05.

### 5.5 Produktlage

Mit der ausgelieferten `config/default.toml` ergibt `granted_for("reference") = ∅`
⇒ das mitgelieferte Referenz-Plugin würde beim regulären Start **nicht aktiviert**.
Das ist **fail-secure und sicherheitsseitig korrekt**, aber ein
**Funktions-/Konfigurationsdefizit**, weil kein Konfigurationsweg existiert
[R0 §9.9 PS-09]. → **RK-07**: „Produktfunktion faktisch abgeschaltet",
Wahrscheinlichkeit **mittel** [R0 §28].

---

## 6. Entscheidungsfrage

> **Wie wird die Sicherheits-Foundation mit der Plugin-Pipeline verdrahtet — und
> in welchem Umfang, mit welcher Change-Control-Einordnung gegenüber Bootstrap
> Baseline §8?** [Briefs §C]

Teilfragen und ihre Behandlung durch GDR-OD05-001:

| # | Teilfrage | Betroffene Position | Durch diesen Record |
|---|---|---|---|
| C-1 | Wo wird `PluginSecurity` komponiert und registriert? | TD-19, TD-05 | **beantwortet** — in der bestehenden `PluginSecurityStage`, ohne Reihenfolgeänderung |
| C-2 | Wird ein `[security]`-Konfigurationspfad hergestellt (`from_config` aktivieren)? | TD-05 | **Richtungsentscheidung getroffen**; Ausgestaltung ist Implementierung, hier **nicht** festgelegt |
| C-3 | Wird das Host-Grant-Set in den `PluginContext` übertragen? | TD-04 — **zusätzlich an OD-01 gebunden** | **NICHT entschieden** (Kap. 12) |
| C-4 | Wird die Admission auditierbar gemacht? | TD-21 — Substanz an **ODD-17** blockiert | **NICHT entschieden** (Kap. 12) |
| C-5 | Wird die Registry um `replace()`/`override()` ergänzt? | TD-06 — eigene MEDIUM-Position | **NICHT entschieden** |
| C-6 | Erfordert die gewählte Variante einen **ADR oder RDR** (Baseline §8)? | Change Control | **UNKNOWN — offen** (Kap. 11) |

---

## 7. Geprüfte Optionen

Wörtlich aus [R0 §20 OD-05] übernommen — nicht erweitert, nicht umformuliert:

| Option | Wortlaut | Security-Wirkung (Quelle) | Architektur-Wirkung (Quelle) |
|---|---|---|---|
| **(a)** | `PluginSecurity` bereits in INITIALIZE komponieren und konfigurieren | HIGH positiv ⓘ — adressiert TD-05 **und** TD-19 an der Wurzel | **berührt Baseline §8** [R0 §20 OD-05] |
| **(b)** | Policy-Konfiguration in die bestehende `PluginSecurityStage` ziehen (**ohne** Reihenfolgeänderung) | **HIGH positiv für TD-05**, **teilweise für TD-19** | **„voraussichtlich nicht"** — Vermutung, keine Feststellung |
| **(c)** | Status quo dokumentieren und im Milestone unverändert lassen | **keine Verbesserung**; SG-C/SG-D/SG-E bleiben nicht erfüllt bzw. nicht nachgewiesen | **keine** |

**R0-Empfehlung im Wortlaut:** „Option (b) ist die **eingriffsärmste** Variante
und käme ohne Änderung der Phasen- oder Stage-Reihenfolge aus — sie löst
**TD-05 vollständig und TD-19 teilweise**. **Dies ist eine Empfehlung, keine
Entscheidung**; sie ersetzt keine ADR-/RDR-Prüfung" [R0 §20 OD-05].

> **Methodische Warnung aus der Quelle [Briefs §E]:** Aus „QG-006 hängt an diesem
> Cluster" folgt **nicht**, dass eine bestimmte Option richtig ist. **QG-006 ist
> ein Gate, keine technische Lösung.** Ein Gate benennt einen Nachweisbedarf; es
> schreibt keine Bauweise vor.

---

## 8. Entscheidung

> ## **OD-05 = OPTION B**
>
> **Policy-Konfiguration wird in die bestehende `PluginSecurityStage` gezogen.**
>
> **Die bestehende Phasen-/Stage-Reihenfolge wird durch diese Entscheidung
> NICHT geändert.**

**Charakter der Entscheidung:**

| Feld | Wert |
|---|---|
| Art | **GOVERNANCE-ENTSCHEIDUNG** |
| **Keine** Implementierungsanweisung | Dieser Record beauftragt, autorisiert und beschreibt **keine** technische Umsetzung |
| Geltungsumfang | Die **Richtung** der Security-Verdrahtung ist entschieden; die **Ausgestaltung** ist nicht Gegenstand dieses Records |
| Erweiterung | Die Entscheidung wird durch diesen Record **nicht** erweitert, technisch interpretiert oder um eigene Architekturentscheidungen ergänzt |

---

## 9. Entscheidungsbegründung

Ausschließlich quellengebunden [R0 §20 OD-05; DEM §D-3; Briefs §D, §K]:

| # | Begründung | Beleg |
|---|---|---|
| 1 | Option (b) ist die **eingriffsärmste** Variante der drei geprüften Optionen | [R0 §20 OD-05] |
| 2 | Sie kommt **ohne Änderung der Phasen- oder Stage-Reihenfolge** aus | [R0 §20 OD-05] |
| 3 | Sie löst **TD-05 vollständig** | [R0 §20 OD-05] |
| 4 | Sie adressiert **TD-19 teilweise** | [R0 §20 OD-05] |
| 5 | Option (a) würde demgegenüber **Baseline §8 berühren** | [R0 §20 OD-05] |
| 6 | Option (c) brächte **keine Verbesserung**; RK-07 bliebe bestehen und die Plugin-Fähigkeit bliebe produktiv faktisch abgeschaltet | [DEM §D-3; Briefs §E] |

**Confidence der zugrunde liegenden Analyse: MEDIUM** — R0 spricht die Empfehlung
für (b) ausdrücklich aus, qualifiziert sie aber im selben Satz dreifach mit
„voraussichtlich", „teilweise" und „ersetzt keine ADR-/RDR-Prüfung" [Briefs §K].
Diese Qualifizierungen sind in Kap. 10, 11, 12 und 17 vollständig erhalten.

---

## 10. Security-Auswirkung

**Belegte Wirkung — und ausschließlich diese:**

| Aspekt | Bewertung | Beleg |
|---|---|---|
| Security-Relevanz der Entscheidung insgesamt | **HOCH** — „betrifft die tatsächliche Wirksamkeit der Admission-Policy" | [R0 §20 OD-05] |
| Wirkung auf **TD-05** | **vollständig adressiert** (durch die spätere Umsetzung; nicht durch diesen Record) | [R0 §20 OD-05] |
| Wirkung auf **TD-19** | **nur teilweise adressiert** | [R0 §20 OD-05] |
| Betroffene Security Gates | **SG-C, SG-D, SG-E** (BLOCKING für QG-006); mittelbar **SG-F** (**BLOCKED** durch ODD-17) | [R0 §26; DEM §4.2] |
| Nicht betroffene Security Gates | SG-A, SG-B, SG-K (am Baseline erfüllt) · SG-G (TD-17, Dokumentation) · SG-H (ODD-19/BD-02) · SG-I (TD-18, getrennt geführt) · SG-J (OD-04/BD-01) | [R0 §26; Briefs §H] |
| **Wirkungsgrenze** | Solange **OD-04** offen ist, bleibt **jedes** Permission-Modell **beratend, nicht erzwingend**. Eine OD-05-Korrektur stellt **Kontraktkonformität** her, **nicht Erzwingbarkeit** | [R0 §10.4 SEC-04, §10.5] |

**Ausdrückliche Wirkungsgrenzen — diese Aussagen werden NICHT getroffen:**

- **NICHT:** „Security ist jetzt vollständig korrekt."
- **NICHT:** „Plugins sind jetzt vollständig sicher."
- **NICHT:** „Permission Enforcement ist jetzt aktiv."
- **NICHT:** „Trust Ledger ist vollständig hergestellt."

Diese vier Aussagen sind durch **keine** Quelle gedeckt und werden durch Option B
**nicht** begründet. SG-C, SG-D und SG-E bleiben zum Zeitpunkt dieses Records
**nicht erfüllt bzw. nicht nachgewiesen** [R0 §26].

**Kein Security Finding, keine ODD, kein Security Gate wird durch diesen Record
geschlossen.**

---

## 11. Architektur-/Bootstrap-Auswirkung

### 11.1 Bootstrap Baseline 1.0 §8 — Wortlaut der Change Control

Änderungen an **Paketstruktur**, **Runtime-Pipeline (Phasenreihenfolge,
Stage-Reihenfolge)**, **Public Exports**, **BootstrapManager (API/Verhalten)**
oder **`default_stages()` (Stage-Zusammensetzung, Reihenfolge)** erfordern eine
genehmigte Governance-Entscheidung in Form eines neuen **ADR** oder **RDR**
[Bootstrap Baseline 1.0 §8].

### 11.2 Einordnung von Option B — qualifizierte Annahme, keine Feststellung

| Feld | Wert |
|---|---|
| Aussage der Quelle | „Option (b) **voraussichtlich** nicht [Baseline §8 berührend]" [R0 §20 OD-05] |
| Bewertung dieser Aussage im Decision Brief | „**„voraussichtlich" ist eine Vermutung, keine Feststellung** → **HUMAN REVIEW REQUIRED**" [Briefs A.4 „Nicht belegt / UNKNOWN"; §E; §K Vorbehalt 2] |
| **Status des §8-Bezugs** | **NICHT VERIFIZIERT — OFFEN** |

Daraus folgt für diesen Record ausdrücklich:

- **Keine** Behauptung eines bereits bestätigten §8-Status.
- **Keine** automatische Change-Control-Freigabe.
- **Keine** ADR-Freigabe, **keine** RDR-Freigabe.
- Die Prüfung, ob Option B Bootstrap Baseline §8 berührt, ist **verbleibende,
  ausstehende Governance-Arbeit** (Kap. 19, NAW-1).

> **Die Entscheidung für Option B ersetzt keine ADR-/RDR-Prüfung**
> [R0 §20 OD-05; Briefs §K Vorbehalt 1].

### 11.3 Weitere Architekturbezüge

| Dimension | Bewertung | Beleg |
|---|---|---|
| Phasen-/Stage-Reihenfolge | **unverändert** — das ist konstitutiver Bestandteil von Option B | [R0 §20 OD-05] |
| Betroffene Komponenten (bei späterer Umsetzung) | `app/bootstrap/stages_plugin.py`, `app/security/security_manager.py`, `app/security/plugin_security.py`, `sdk/context.py`, `config/default.toml`, mittelbar `core/registry.py` | [DEM §D-3] |
| SDK-Berührung | **ja bei TD-04** — „SDK-**additive** Änderung, ADR-/Freigabe-relevant". TD-04 ist durch diesen Record **nicht** entschieden | [R0 §19.1 TD-04] |
| NFR-003 (SDK API 1.0.0 rückwärtskompatibel) | am Baseline **MATCH**; Vereinbarkeit einer additiven Ergänzung im R0 **nicht ausdrücklich bewertet** → **UNKNOWN** | [Briefs §I] |
| Architecture Book v2.0 | **FROZEN, unberührt** — durch diesen Record nicht verändert und nicht zur Änderung freigegeben | [AB v2.0 Kopf; GDR-OD01-001 Kap. 11] |
| Regressionsumfang | **UNKNOWN** — R0 quantifiziert ihn nicht; ⓘ vermutlich geringer als bei (a), da ohne Reihenfolgeänderung | [Briefs §E, §N] |

---

## 12. TD-04 / TD-05 / TD-19 / TD-21 / TD-06

> **Grundregel dieses Kapitels: Kein Technical Debt wird durch diesen Record
> geschlossen.** Der Record dokumentiert eine Richtungsentscheidung, keine
> erfolgte Umsetzung und keinen erbrachten Nachweis.

| Position | Wirkung von Option B laut Quelle | Status **nach** GDR-OD05-001 |
|---|---|---|
| **TD-04** | Wird bei **keiner** der drei Optionen ausdrücklich als gelöst bezeichnet. Die Grant-Übertragung in den `PluginContext` ist eine **eigene, SDK-additive Änderung**; die Vertragsgrundlage hängt zusätzlich an **OD-01** | **OPEN** |
| **TD-05** | **vollständig adressiert** — Richtung entschieden; Umsetzung und Nachweis stehen aus | **OPEN** (Adressierungsrichtung entschieden, nicht geschlossen) |
| **TD-19** | **nur teilweise adressiert**; **was ungelöst bliebe, ist im R0 nicht ausgeführt** | **OPEN — teilweise adressiert; verbleibender Umfang UNKNOWN** |
| **TD-21** | **nicht gelöst** — die Substanz (Audit-Ereigniskatalog) ist an **ODD-17 (offen)** gebunden | **OPEN** |
| **TD-06** | Im R0 als **Symptom** von TD-19 geführt; von Option B nicht ausdrücklich adressiert (R0 nennt für (b) nur TD-05 und TD-19) | **OPEN** |

### 12.1 TD-04 — Schutzregel (keine Scheinschließung)

**OD-05 allein schließt TD-04 NICHT.**

- [R0 §24.2] führt TD-04 ausdrücklich als **„OD-01 + OD-05"** — **beide
  gemeinsam**.
- [Briefs §K Vorbehalt 4]: „Option (b) löst **TD-04 nicht automatisch** — dessen
  Vertragsgrundlage hängt zusätzlich an **OD-01**."
- [Briefs §F] benennt den Fehlschluss „TD-04 ist mit OD-05 erledigt" ausdrücklich
  als **Scheinschließung einer MISSING-Position**.
- [Briefs A.4]: Ob TD-04 innerhalb von Option (b) **überhaupt** lösbar ist →
  **UNKNOWN / HUMAN REVIEW REQUIRED**.

> **TD-04 bleibt OPEN.** Die zugrunde liegenden Quellen führen TD-04 weiterhin als
> offenen Punkt; dieser Record ändert daran nichts.

### 12.2 TD-19 — Unterscheidung vollständig/teilweise

Die Quelle sagt für Option (b) **nicht** „TD-19 ist gelöst", sondern
**„TD-19 teilweise"** [R0 §20 OD-05].

> **TD-19 wird durch Option B nur teilweise adressiert; der verbleibende Umfang
> ist gemäß Quelle UNKNOWN, da dort nicht weiter spezifiziert.**

Eine eigene Interpretation des verbleibenden Umfangs wird in diesem Record
**nicht** vorgenommen. TD-19 ist in [R0 §10.9] als **DEVIATION** geführt; dieser
Status wird durch GDR-OD05-001 **nicht** geändert.

### 12.3 TD-21 / ODD-17

- Die Substanz von TD-21 (Audit-Ereigniskatalog) ist an **ODD-17** gebunden;
  **ODD-17 ist offen** [R0 §10.8; §26 SG-F].
- **SG-F ist BLOCKED** — durch ODD-17, nicht durch OD-05 [R0 §26].
- **ODD-17 wird durch diesen Decision Record NICHT geschlossen.**
- Aus GDR-OD05-001 wird **keine Security-Freigabe** abgeleitet.

---

## 13. OD-01-/OD-04-Abgrenzung

### 13.1 Abgrenzung zu OD-01

| Position | Gegenstand | Status |
|---|---|---|
| **OD-01** (GDR-OD01-001, FINAL) | **Dokument-/Vertragsdisposition** — Option C, getrennte Behandlung von ADRs / FROZEN Architecture Book / `CLAUDE.md`+`ROADMAP.md` | entschieden |
| **OD-05** (dieser Record) | **Technische Security-Verdrahtung** — Option B | entschieden |

**Die beiden Entscheidungen bleiben getrennt.** GDR-OD05-001 verändert
GDR-OD01-001 **nicht**, hebt keine seiner Nicht-Wirkungen auf und nimmt keine der
dort als NEXT AUTHORIZED WORK dokumentierten Folgeaktionen (A–D) vorweg. Die dort
offenen Punkte (OP-1…OP-10) bleiben unverändert offen. **TD-04 hängt an beiden
Entscheidungen gemeinsam und bleibt OPEN** (Kap. 12.1).

### 13.2 Abgrenzung zu OD-04

**OD-04 (Plugin-Isolationsstrategie, gespiegelt als BD-01) wird durch diesen
Record NICHT entschieden.**

- [R0 §10.4 SEC-04]: Solange **keine Isolation** existiert, ist **jedes**
  Permission-Modell — Host- wie SDK-seitig — **beratend, nicht erzwingend**. Dies
  ist eine **Systemeigenschaft, kein Implementierungsfehler**.
- [R0 §10.5]: Eine Korrektur „stellt die **Kontraktkonformität** her, nicht die
  **Erzwingbarkeit**".
- **SG-J bleibt BLOCKED** (OD-04 / BD-01) [R0 §26].

> **Aus Option B darf keine automatische Behauptung tatsächlicher
> Permission-Enforcement-Wirksamkeit entstehen, solange OD-04 offen ist.**

### 13.3 Ausdrücklich nicht Teil von OD-05

| Gegenstand | Zugehörigkeit | Beleg |
|---|---|---|
| **TD-20** (Base64-„Encryption") / SG-H | **ODD-19 / BD-02** | [R0 §10.7; §26] |
| **TD-17** (Integritätsbezeichnung) / SG-G | ADR-005 / Spec §5.9 / ODD-19; Dokumentationsanteil SPR-07/WP-007 | [R0 §10.3; §26] |
| **TD-18** (Identifier-Validierung) / SG-I | getrennt geführt, ohne WP und ohne OD-Zuordnung | [R0 §24.2; §26] |
| **PS-08** (zwei Permissions-Vokabulare) | berührt **GC-03 (offen)**; Zugehörigkeit zu OD-05 **UNKNOWN** | [R0 §9.8; Briefs §G] |
| **TD-26** (Docstring `_validate_for_activation`) | SPR-04/WP-003, **nicht** OD-05 | [Briefs A.5.2] |

---

## 14. Test-/Verification-Auswirkungen

Die Quellen führen für Option (b) — wie für Option (a) — **drei erforderliche
Tests/Nachweise** [R0 §20 OD-05, §15.4]:

| Nachweis | Inhalt | Status am Baseline | Status **nach** GDR-OD05-001 |
|---|---|---|---|
| **TG-2** | Test gegen die **produktive Default-Policy** / die ausgelieferte Konfiguration | **existiert nicht** — alle Policy-Tests injizieren eigene Policies | **ERFORDERLICH — NICHT ERBRACHT / NICHT BESTANDEN** |
| **TG-3** | Test der **Trust-Ledger-Identität** über LOAD_PLUGINS → FINALIZE | **existiert nicht** | **ERFORDERLICH — NICHT ERBRACHT / NICHT BESTANDEN** |
| **TG-4** | Test, dass **Host-Grants im `PluginContext` ankommen** | **existiert nicht** | **ERFORDERLICH — NICHT ERBRACHT / NICHT BESTANDEN** |

**Kein Test wurde im Rahmen dieses Records ausgeführt, erstellt oder verändert.**

| Dimension | Wert | Beleg |
|---|---|---|
| **RB-1.0 (258/14)** | **UNVERÄNDERT** — Zuwachs liefe über **MWB-015**, wie für Phase-B-Arbeit vorgesehen | [R0 §25; Briefs §J] |
| Testarchitektur-Schwäche 2 | „Die Policy-Tests testen die Policy-**Mechanik**, nicht die **ausgelieferte Konfiguration**" — Ursache dafür, dass SEC-06 durch den Testbestand nicht auffällt | [R0 §15.5 Nr. 2] |
| Verifikationsart (später) | EV-W03 (WP-003), EV-W04 (WP-004) ⓘ | [Briefs §J] |
| Mittelbar betroffenes Gate | **QG-007** (Testabdeckung) ⓘ | [Briefs §J] |

---

## 15. QG-006-Auswirkung

| Feld | Wert | Beleg |
|---|---|---|
| Gate | **QG-006 — Pipeline Security Compliance** | [R0 §24.3] |
| Berührende Befunde | **TD-04, TD-05, TD-19, TD-21** | [R0 §24.3] |
| Blockierende Security Gates | **SG-C** (TD-05), **SG-D** (TD-04), **SG-E** (TD-19) — sämtlich **BLOCKING**; **SG-F BLOCKED** durch ODD-17 | [R0 §26; DEM §4.2] |
| Frühestmöglicher Abschluss | „**WP-003 und WP-004**" | [R0 §24.3; Sprint Plan SPR-05, IP §8.7] |
| Status vor GDR-OD05-001 | **NOT STARTED** | [R0 §24.3 SM-01] |
| **Status nach GDR-OD05-001** | **NOT STARTED — UNVERÄNDERT** | — |

**Wirkung von Option B auf QG-006 laut Quelle:** adressiert **TD-05 vollständig**
und **TD-19 teilweise**; **TD-04 und TD-21 bleiben offen** [Briefs §E].

> **QG-006 wird durch diesen Record NICHT bestanden und NICHT auf PASSED gesetzt.**
> Ebenso wenig ein anderes Quality Gate (QG-001…QG-008 bleiben in ihrem
> bestehenden Status; alle Gates sind laut [R0 §24.3 SM-01] **NOT STARTED**).

---

## 16. Sprint-/WP-Auswirkung

| Feld | Wert | Beleg |
|---|---|---|
| Zugeordnete Work Packages | **WP-003** (SPR-04, Developer Experience) und **WP-004** (SPR-05, Observability) | [R0 §23.3 V-4, §24.3; DEM §D-3; Sprint Plan SPR-04/SPR-05] |
| Zugeordnetes Gate | **QG-006** — abschließbar erst nach **WP-003 und WP-004** | [Sprint Plan SPR-05 Exit Criteria; IP §8.7] |
| Eigene Sprint-/WP-Zuordnung für OD-05 | **keine** — „Kein FR; berührt Bootstrap Baseline §8" | [R0 §24.2] |
| Eigenes neues Work Package | **keines** | [Briefs §N] |

**Ausdrücklich:**

- **Kein Sprint wird gestartet.**
- **Kein Work Package wird als abgeschlossen markiert.**
- **Kein neuer Sprint wird erzeugt.**
- **Keine Änderung am genehmigten Sprint Plan** — dieser bleibt unverändert
  (Status DRAFT 1.0 R0, als Planungsgrundlage genehmigt).
- **RK-07** bleibt bestehen, solange keine Umsetzung erfolgt ist.

---

## 17. Offene UNKNOWNs

| # | UNKNOWN | Quellenlage | Status |
|---|---|---|---|
| **U-1** | Ob Option B **Bootstrap Baseline §8** berührt | R0: „voraussichtlich nicht" — Vermutung, keine Feststellung | **UNKNOWN — HUMAN REVIEW REQUIRED** |
| **U-2** | Ob Option B einen **ADR** oder **RDR** erfordert, und in welchem Umfang | im R0 nicht festgestellt | **UNKNOWN** |
| **U-3** | Welcher Teil von **TD-19** nach Option B ungelöst bliebe | „teilweise" — im R0 **nicht ausgeführt** | **UNKNOWN** |
| **U-4** | Ob **TD-04** innerhalb von Option B überhaupt lösbar ist | TD-04 wird bei keiner Option ausdrücklich als gelöst bezeichnet | **UNKNOWN — HUMAN REVIEW REQUIRED** |
| **U-5** | **Aufwand** jeder Option | R0 macht keine Aufwandsangabe | **UNKNOWN** |
| **U-6** | **Regressionsumfang** von Option B | R0 quantifiziert ihn nicht | **UNKNOWN** |
| **U-7** | Ob eine Brücke zwischen den beiden Permissions-Vokabularen (**PS-08**) Bestandteil von OD-05 wäre | nicht ausgewiesen; berührt **GC-03 (offen)** | **UNKNOWN** |
| **U-8** | Vereinbarkeit einer additiven SDK-Ergänzung mit **NFR-003 / FR-013** | im R0 nicht ausdrücklich bewertet | **UNKNOWN** |
| **U-9** | Bewertung eines QG-006-Verlaufs **ohne** SG-C/SG-D/SG-E | R0 bewertet dies nicht | **UNKNOWN — HUMAN REVIEW REQUIRED** |
| **U-10** | Zukünftige Erweiterbarkeit je Option | keine Quellengrundlage | **UNKNOWN** |

> Diese UNKNOWNs werden dokumentiert, **nicht** aufgelöst. Eine eigene
> Interpretation findet in diesem Record nicht statt.

---

## 18. Nicht-Wirkungen

**Option B bedeutet NICHT automatisch:**

| # | Nicht-Wirkung |
|---|---|
| 1 | **NICHT**, dass **TD-04** geschlossen ist |
| 2 | **NICHT**, dass **TD-19** vollständig geschlossen ist |
| 3 | **NICHT**, dass **TD-21** geschlossen ist |
| 4 | **NICHT**, dass **TD-05** oder **TD-06** geschlossen sind |
| 5 | **NICHT**, dass **ODD-17** geschlossen ist |
| 6 | **NICHT**, dass ein **Security Finding** geschlossen ist |
| 7 | **NICHT**, dass **QG-006** bestanden ist |
| 8 | **NICHT**, dass **TG-2** bestanden ist |
| 9 | **NICHT**, dass **TG-3** bestanden ist |
| 10 | **NICHT**, dass **TG-4** bestanden ist |
| 11 | **NICHT**, dass **Permission Enforcement** gelöst ist |
| 12 | **NICHT**, dass **OD-04** entschieden ist |
| 13 | **NICHT**, dass ein **Security-ADR** erstellt ist |
| 14 | **NICHT**, dass ein **RDR** erstellt ist |
| 15 | **NICHT**, dass der **Sprint Plan** geändert ist |
| 16 | **NICHT**, dass **Coding** freigegeben ist |
| 17 | **NICHT**, dass **Deployment** freigegeben ist |
| 18 | **NICHT**, dass **Trading** freigegeben ist |
| 19 | **NICHT**, dass **SG-C, SG-D oder SG-E** erfüllt oder nachgewiesen sind |
| 20 | **NICHT**, dass **RK-07** entschärft ist |
| 21 | **NICHT**, dass **Bootstrap Baseline §8** als nicht berührt festgestellt ist |

**Insbesondere — die Unterscheidung, die nicht verwischt werden darf:**

> Die Quellen unterscheiden zwischen **KONTRAKTKONFORMITÄT** und tatsächlicher
> **ERZWINGBARKEIT** [R0 §10.5]. Solange **OD-04** offen ist, darf aus Option B
> **keine automatische Behauptung tatsächlicher
> Permission-Enforcement-Wirksamkeit** entstehen. Jedes Permission-Modell bleibt
> bis zur Klärung von OD-04 **beratend** [R0 §10.4 SEC-04].

---

## 19. Next Authorized Work

> **Keine dieser Positionen wird durch diesen Record ausgeführt.** Sie sind
> ausschließlich als **OPEN GOVERNANCE REQUIREMENT / NEXT AUTHORIZED WORK**
> dokumentiert und bedürfen jeweils einer eigenen, ausdrücklichen Autorisierung.

| # | Position | Gegenstand | Autorität | Status |
|---|---|---|---|---|
| **NAW-1** | **ADR-/RDR-Prüfung gegen Bootstrap Baseline §8** | Feststellen, ob Option B die Change-Control-Tatbestände des §8 berührt und ob ein ADR oder RDR erforderlich ist. Die R0-Aussage „voraussichtlich nicht" ist **nicht** verifiziert | Architektur-/Security-Governance | **OPEN GOVERNANCE REQUIREMENT — nicht ausgeführt** |
| **NAW-2** | **Umsetzungsautorisierung** für Option B | Getrennte, ausdrückliche Coding-Freigabe. Dieser Record erteilt sie **nicht** | Projekteigner | **NICHT ERTEILT** |
| **NAW-3** | **TD-04-Behandlung** | Nur gemeinsam mit **OD-01**; U-4 (Lösbarkeit innerhalb von Option B) ist UNKNOWN | Projekteigner + Architektur-/Security-Governance | **OPEN** |
| **NAW-4** | **TD-19 — verbleibender Umfang** | Bestimmen, was Option B an TD-19 **nicht** löst (U-3) | Architektur-/Security-Governance | **OPEN** |
| **NAW-5** | **ODD-17** (Audit-Ereigniskatalog) | Voraussetzung für die Substanz von TD-21 und für SG-F | Security-Governance | **OPEN — separat** |
| **NAW-6** | **OD-04 / BD-01** (Isolationsstrategie) | Voraussetzung für Erzwingbarkeit; SG-J BLOCKED | Projekteigner + Architektur-/Security-Governance | **OPEN — separat** |
| **NAW-7** | **TG-2, TG-3, TG-4** | Erstellung und Erbringung der drei fehlenden Nachweise; Zuwachs über **MWB-015**, RB-1.0 unverändert | nach Coding-Freigabe | **OPEN** |
| **NAW-8** | **Klärung U-7 (PS-08 / GC-03)** | Ob die Vokabularbrücke Bestandteil von OD-05 ist | Architektur-Governance | **UNKNOWN — OPEN** |

**Dieser Record erstellt weder einen Security-ADR noch einen RDR.**

---

## 20. Final Decision Statement

> **GDR-OD05-001 — FINAL**
>
> **OD-05 ist entschieden: OPTION B — Policy-Konfiguration in die bestehende
> `PluginSecurityStage` ziehen, ohne Änderung der bestehenden Phasen-/Stage-
> Reihenfolge.**
>
> Dies ist eine **Governance-Entscheidung**, **keine Implementierungsanweisung**.
> Sie legt die Richtung der Security-Verdrahtung fest und **nichts darüber
> hinaus**.
>
> Laut Quelle adressiert Option B **TD-05 vollständig** und **TD-19 teilweise**;
> der verbleibende TD-19-Umfang ist **UNKNOWN**. **TD-04 bleibt OPEN** und hängt
> an **OD-01 + OD-05 gemeinsam**. **TD-21 bleibt OPEN**, seine Substanz ist an
> **ODD-17 (offen)** gebunden. **TD-06 bleibt OPEN.**
>
> Die Einordnung „berührt Bootstrap Baseline §8 voraussichtlich nicht" ist eine
> **qualifizierte Annahme, keine verifizierte Tatsache**. Eine **ADR-/RDR-Prüfung
> steht aus** und wird durch diese Entscheidung **nicht ersetzt**.
>
> Solange **OD-04** offen ist, stellt eine Korrektur **Kontraktkonformität** her,
> **nicht Erzwingbarkeit**.
>
> **SG-C, SG-D, SG-E: nicht erfüllt bzw. nicht nachgewiesen.
> SG-F: BLOCKED (ODD-17). SG-J: BLOCKED (OD-04).
> TG-2 / TG-3 / TG-4: erforderlich, nicht erbracht.
> QG-006: NOT STARTED. RB-1.0: unverändert (258/14).
> Sprint Plan: unverändert.**
>
> **CODING = NOT AUTHORIZED.**

**Coding Authorization Statement.** Dieser Decision Record erteilt **keine**
Coding Authorization, keine Umsetzungs-, Deployment- oder Trading-Freigabe. Es
wurde **keine** technische Umsetzung durchgeführt: keine Datei des
Produktionscodes, keine Testdatei, keine Konfiguration und kein SDK-Bestandteil
wurde verändert.

---

## 21. Verification

☑ Source Gate bestanden — alle Pflichtquellen physisch vorhanden und gelesen
☑ **Option B** eindeutig dokumentiert; Wortlaut mit [R0 §20 OD-05] abgeglichen, deckungsgleich
☑ Entscheidung **nicht erweitert**, nicht technisch interpretiert, nicht um eigene Architekturentscheidungen ergänzt
☑ **genau eine** neue Datei erzeugt (`docs/governance/od-05-governance-decision.md`)
☑ **keine** bestehende Datei verändert
☑ `src/**`, `app/**`, `sdk/**`, `tests/**`, `config/**` **unverändert**
☑ `docs/security-architecture-1.0.md`, `docs/security-design-1.0.md` **unverändert**
☑ Sprint Plan, Implementation Plan, ADRs, Architecture Book, `CLAUDE.md`, `ROADMAP.md` **unverändert**
☑ **OD-01 (GDR-OD01-001) nicht verändert** und nicht überschrieben
☑ **OD-04 nicht entschieden**
☑ **TD-04 nicht geschlossen** — als OPEN dokumentiert, keine Scheinschließung
☑ **TD-19 nur als teilweise adressiert** dokumentiert; verbleibender Umfang als UNKNOWN geführt
☑ **TD-21 nicht geschlossen**; **TD-05 / TD-06 nicht geschlossen**
☑ **ODD-17 nicht geschlossen**
☑ **kein Security Finding geschlossen**; SG-C/SG-D/SG-E/SG-F unverändert
☑ **kein Quality Gate als PASSED markiert** — QG-006 bleibt NOT STARTED
☑ **keine Tests ausgeführt, erstellt oder verändert**; TG-2/TG-3/TG-4 als erforderlich und nicht erbracht dokumentiert
☑ **RB-1.0 (258/14) unverändert**
☑ **kein Sprint gestartet**, kein Work Package abgeschlossen, kein neuer Sprint erzeugt
☑ **keine technische Implementierung**
☑ **kein ADR erstellt**
☑ **kein RDR erstellt**
☑ ADR-/RDR-Prüfung ausschließlich als NEXT AUTHORIZED WORK dokumentiert (NAW-1)
☑ §8-Status **nicht** als bestätigt dargestellt
☑ Security-Wirkung **nicht** über die belegte Wirkung hinaus erweitert
☑ Unterscheidung Kontraktkonformität ↔ Erzwingbarkeit erhalten
☑ **Coding weiterhin NOT AUTHORIZED**
☑ **kein Commit**
☑ **kein Tag**
☑ **kein Push**

---

**Ende OD-05 Governance Decision Record — JOCHEN X Milestone 1.0
(GDR-OD05-001, FINAL, 2026-08-10) — Bezugs-Baseline
`MILESTONE-1.0-BASELINE = 8fcf42f1997dfcf6ff232e75fd33c37b933991c8`**
