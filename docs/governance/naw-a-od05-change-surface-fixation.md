# JOCHEN X — Milestone 1.0
# NAW-A — Change-Surface Fixation for OD-05 Option B

| Feld | Wert |
|---|---|
| Dokumenttyp | Governance Assessment / Change-Surface Fixation (READ-ONLY) |
| **ID** | **NAW-A** |
| Status | **FINAL GOVERNANCE ASSESSMENT** — nicht normativ außerhalb dieses NAW-A-Auftrags |
| Gegenstand | Fixierung des minimalen Änderungsumrisses für **OD-05 Option B**; Auflösung von **F3-U1** und **F3-U4** |
| Governance Input | **Projekteigner-Entscheidung A und B** (Kap. 3) · **G-1 = OPTION HYBRID** · **GDR-OD05-001** (Option B) · **F-3** · **F-2-B** · **F-1-A** |
| Datum | 2026-08-10 |
| Branch / HEAD | `milestone-1.0-governance` / `8fcf42f1997dfcf6ff232e75fd33c37b933991c8` |
| Bezugs-Baseline | `MILESTONE-1.0-BASELINE = 8fcf42f1997dfcf6ff232e75fd33c37b933991c8` |
| Coding | **NOT AUTHORIZED** |

---

## 1. Executive Decision

**Der Projekteigner hat den minimalen Änderungsumriss für OD-05 Option B
festgelegt.** NAW-A dokumentiert diese Festlegung und leitet ihre
Governance-Wirkung ab. **NAW-A ist keine Coding-Freigabe.**

| # | Festlegung | Wirkung |
|---|---|---|
| **A** | Der `[security]`-Abschnitt ist **OPTIONAL**; sein Fehlen führt zu sicheren Defaults und **nicht** zu einem `ConfigurationError` | **F3-U1 GESCHLOSSEN** |
| **B** | **Kein neues öffentliches Symbol** in `app/bootstrap/__init__.py`; `__all__` bleibt unverändert | **F3-U4 GESCHLOSSEN** → **§8-3 = NOT TRIGGERED** (determinat) |

**Minimale Änderungsfläche: CS-1 + CS-2 + CS-3** (Kap. 6).

**Die wesentliche Governance-Wirkung dieser Fixierung.** F-3 hatte §8-4 aus
**zwei** voneinander unabhängigen Gründen als UNKNOWN eingestuft
[SOURCE: docs/governance/f-03-od05-change-surface-assessment.md Kap. 18]:

| Grund | Status nach NAW-A |
|---|---|
| **R-3** — neuer `BootstrapError`-Pfad in INITIALIZE bei verpflichtendem `[security]` | **ENTFÄLLT** durch Festlegung A (Kap. 4) |
| **F3-U2 / R-5** — ob geänderte Zulassungswerte (`admitted_manifests`) unter „Kontrakt" i. S. v. G-1 fallen | **BESTEHT FORT** — Gegenstand von **NAW-B** |

> **§8-4 bleibt UNKNOWN, ruht nach NAW-A aber nur noch auf einer einzigen
> offenen Frage.** NAW-A darf §8-4 nicht schließen (Kap. 10.4).

---

## 2. Ausgangslage F-3

**F-3-Ergebnisse, die NAW-A als Eingangsgrößen übernimmt**
[SOURCE: docs/governance/f-03-od05-change-surface-assessment.md Kap. 12, 18, 27]:

| # | Feststellung | Klassifikation |
|---|---|---|
| A-1 | Minimale erforderliche Änderungsfläche: `app/bootstrap/stages_plugin.py`, `config/settings.py`, `config/default.toml` | **REQUIRED** |
| A-2 | `app/security/plugin_security.py` — `PluginSecurity.__init__` akzeptiert bereits `integrity_policy` und `permission_policy` [SOURCE: BASELINE 8fcf42f:app/security/plugin_security.py:`PluginSecurity.__init__`] | **NOT REQUIRED** |
| A-3 | `app/bootstrap/manager.py`, `app/bootstrap/__init__.py`, `app/bootstrap/types.py` | **NOT REQUIRED** |
| A-4 | `sdk/context.py` — TD-04-Gebiet | **NOT AUTHORIZED durch OD-05** |
| A-5 | `app/security/security_manager.py` — TD-19-Anteil | **separat, F-4** |
| A-6 | Stage-Reihenfolge unverändert | **konstitutiv (Option B)** |
| A-7 | Architecture Freeze unangetastet | **F-1-A** |
| A-8 | Beide `from_config`-Fabriken sind **total** — kein neuer Ausnahmepfad [SOURCE: BASELINE 8fcf42f:app/security/plugin_security.py:`IntegrityPolicy.from_config`, `PermissionPolicy.from_config`] | **EXISTING** |
| A-9 | Aktivierungsfehler propagieren nicht [SOURCE: BASELINE 8fcf42f:app/bootstrap/stages_plugin.py:`PluginActivationStage.execute`] | **EXISTING** |
| A-10 | §8-4 = **UNKNOWN**; §8-1/§8-2/§8-5 = NOT TRIGGERED; §8-3 = NOT TRIGGERED mit Vorbehalt | **Ergebnis F-3** |

---

## 3. NAW-A Decision

**Verbindlich für diesen Auftrag festgelegt durch den Projekteigner:**

> **A — `[security]` ist OPTIONAL.** Der Abschnitt darf fehlen. Fehlt er, werden
> sichere Defaults verwendet. Es entsteht **keine** neue `ConfigurationError`-Pflicht
> allein wegen eines fehlenden `[security]`-Abschnitts und damit **kein** neuer
> `BootstrapError`-Pfad in INITIALIZE allein durch dessen Fehlen.
>
> **B — Kein neues öffentliches Symbol.** Für die minimale Umsetzung wird **kein**
> neues Symbol in `app/bootstrap/__init__.py` eingeführt; `__all__` bleibt
> unverändert. Keine neue Policy-Factory im Bootstrap-Paket.

**Autorisierungsumfang von NAW-A:** ausschließlich die **Fixierung des
Änderungsumrisses**. **Keine** Coding-Freigabe, **keine** Implementierung,
**keine** Sprint-Freigabe.

---

## 4. `[security]` = OPTIONAL

### 4.1 Ist-Zustand

| # | Befund | Fundstelle |
|---|---|---|
| O-1 | `config/default.toml` enthält `[application]`, `[database]`, `[plugins]` — **kein `[security]`** | [SOURCE: BASELINE 8fcf42f:config/default.toml] |
| O-2 | `ApplicationSettings.from_mapping` liest die drei Abschnitte über `raw["…"]`, prüft `isinstance(value, dict)` und wandelt `KeyError`/`TypeError`/`ValueError` in einen `ConfigurationError` | [SOURCE: BASELINE 8fcf42f:config/settings.py:`ApplicationSettings.from_mapping`] |
| O-3 | `ConfigurationStage.execute` (INITIALIZE) ruft `configuration.load()`; ein `ConfigurationError` propagiert und wird von `run_phase` zu `BootstrapError` gewandelt | [SOURCE: BASELINE 8fcf42f:app/bootstrap/stages_init.py:`ConfigurationStage.execute`; app/bootstrap/manager.py:`run_phase`] |

### 4.2 Wirkung der Festlegung A

Festlegung A schließt aus, dass `[security]` wie die drei bestehenden
Pflichtabschnitte behandelt wird. Damit **entfällt der in F-3 als R-3 geführte
neue Ausnahmepfad** [SOURCE: docs/governance/f-03-od05-change-surface-assessment.md Kap. 9.1 R-3].

> **F3-U1 = GESCHLOSSEN.**

### 4.3 Aus der Festlegung folgende Eigenschaften des Umrisses

Damit Festlegung A auch bei **ungültigen** Werten trägt, muss der Umriss die
folgenden Eigenschaften aufweisen. **Dies sind Eigenschaften der Fixierung, keine
Implementierungsvorgaben und kein Code.**

| # | Erforderliche Eigenschaft | Begründung |
|---|---|---|
| **C-1** | Fehlender `[security]`-Abschnitt ⇒ **sichere Defaults**, keine Ausnahme | Festlegung A |
| **C-2** | Ungültige **Werte innerhalb** des Abschnitts ⇒ sichere Defaults | Bereits durch die bestehenden Fabriken erfüllt: `IntegrityPolicy.from_config` fängt `ValueError` bei der Enum-Konversion ab und prüft `scope` gegen eine Whitelist; `PermissionPolicy.from_config` prüft `isinstance` und fällt auf leere Mengen zurück [SOURCE: BASELINE 8fcf42f:app/security/plugin_security.py:`IntegrityPolicy.from_config`, `PermissionPolicy.from_config`] |
| **C-3** | Ein `security`-Eintrag, der **keine Tabelle** ist (z. B. `security = "x"`), muss ebenfalls zu sicheren Defaults führen | **Präzisierungsbedarf:** Beide `from_config`-Fabriken rufen `config.get(...)` auf. Ein Nicht-Mapping erzeugte an dieser Stelle einen `AttributeError`, der über `run_phase` zu einem `BootstrapError` würde. Ein reines `raw.get("security", {})` genügt daher **nicht**; die Zugriffsstelle muss den Typ prüfen. Ohne diese Eigenschaft wäre Festlegung A nicht vollständig erfüllt |

> **C-3 ist ein Befund dieses Assessments.** Er beschreibt eine **Eigenschaft**,
> die der fixierte Umriss besitzen muss — nicht, wie sie herzustellen ist. Es wird
> kein Code vorgegeben und keine Implementierung vorgenommen.

---

## 5. Public Export = UNCHANGED

| # | Befund | Fundstelle |
|---|---|---|
| P-1 | `app/bootstrap/__init__.py` exportiert **20 Symbole** über `__all__` | [SOURCE: BASELINE 8fcf42f:app/bootstrap/__init__.py; docs/baselines/bootstrap-baseline-1.0.md §3.1] |
| P-2 | Festlegung B: Für die minimale Umsetzung wird **kein** Symbol hinzugefügt, entfernt oder umbenannt | Kap. 3 |
| P-3 | Die minimale Umsetzung benötigt kein neues öffentliches Symbol: `PluginSecurity.__init__` nimmt die Policy-Objekte bereits entgegen, und beide `from_config`-Fabriken existieren in `app/security/plugin_security.py` — außerhalb des Bootstrap-Pakets | [SOURCE: BASELINE 8fcf42f:app/security/plugin_security.py] |

> **F3-U4 = GESCHLOSSEN.** **§8-3 = NOT TRIGGERED** — determinat, nicht mehr
> unter Vorbehalt (Kap. 10.3).

---

## 6. Minimal Change Surface

**Die zulässige minimale Änderungsfläche besteht ausschließlich aus CS-1, CS-2
und CS-3.**

### 6.1 CS-1 — `app/bootstrap/stages_plugin.py`

| Feld | Inhalt |
|---|---|
| Symbol | `PluginSecurityStage.execute` |
| Baseline-Zustand | Im Zweig `except LookupError` wird `PluginSecurity(events, logger=logger)` **ohne Policy-Argumente** erzeugt und registriert [SOURCE: BASELINE 8fcf42f:app/bootstrap/stages_plugin.py:`PluginSecurityStage.execute`] |
| Zweck der Änderung | Die bestehende Stage soll die **konfigurierten** Policies verwenden; die Policy-Konfiguration wird an die bestehende Security-Instanz übergeben |
| **Unveränderlich** | `name = "plugin_security"` · `phase = StartupPhase.LOAD_PLUGINS` · Position 9 in `default_stages()` · die Admission-Reihenfolge **Integrity → API-Version → Permission → Dependency Resolution → Activation** [SOURCE: docs/baselines/bootstrap-baseline-1.0.md §4 Inv. 6, §5.2] |
| Klassifikation | **REQUIRED** |

### 6.2 CS-2 — `config/settings.py`

| Feld | Inhalt |
|---|---|
| Zweck | Ausschließlich: die `[security]`-Konfiguration aus der geladenen Konfiguration für die Stage verfügbar machen |
| Baseline-Zustand | `ApplicationSettings` ist ein frozen Dataclass mit **sieben** Feldern ohne Security-Feld; `ConfigurationService.load()` gibt `ApplicationSettings` zurück und **verwirft die rohe TOML-Abbildung**; `_read`/`_merge` sind privat — es existiert **kein** öffentlicher Rohzugriff [SOURCE: BASELINE 8fcf42f:config/settings.py:`ApplicationSettings`, `ConfigurationService`] |
| Grenzen (Auftrag Kap. 3) | Keine unnötige Erweiterung des `ApplicationContext` · keine neue öffentliche API über den minimal erforderlichen Konfigurationszugang hinaus · keine Änderung der bestehenden **sieben Pflichtfelder**, sofern nicht zwingend erforderlich |
| Klassifikation | **REQUIRED** |

**Mehrere technisch mögliche Wege — dokumentiert, nicht implementiert:**

| Variante | Beschreibung | Bewertung |
|---|---|---|
| **V-1** | Ein **zusätzliches, optionales** Feld auf `ApplicationSettings`, gespeist aus der rohen Abbildung mit sicherem Default und Typprüfung (C-3) | **BEVORZUGT** — rein additiv; die sieben bestehenden Felder bleiben unverändert; keine neue öffentliche Methode; kein zusätzlicher Datei-Zugriff und damit keine neue Ausnahmequelle |
| **V-2** | Ein **öffentlicher Zugang** auf `ConfigurationService` zur rohen bzw. zur `[security]`-Abbildung | **möglich, nicht bevorzugt** — erweitert die öffentliche API von `ConfigurationService`. Zusatzbefund: Da `load()` die rohe Abbildung nicht aufbewahrt, müsste ein solcher Zugang entweder erneut lesen — dann wäre `_read` mit seinem `ConfigurationError` bei `OSError`/`TOMLDecodeError` eine **zusätzliche Auslösestelle** [SOURCE: BASELINE 8fcf42f:config/settings.py:`ConfigurationService._read`] — oder die Abbildung während `load()` zwischenspeichern |
| **V-3** | Die Stage liest die TOML-Dateien selbst | **nicht mit der Fixierung vereinbar** — dupliziert das Laden der Konfiguration, umgeht den Profil-Merge und führt Datei-IO und damit eine **neue Ausnahmequelle** in die Stage ein (Widerspruch zu C-1/C-3) |

> **Es wird keine Variante implementiert.** V-1 ist als **bevorzugte
> minimalinvasive Variante** ausgewiesen. Die endgültige Wahl bleibt der
> autorisierten Umsetzung vorbehalten.

**Zwei belegte Zusatzbefunde zu CS-2 — dokumentiert, nicht entschieden:**

| # | Befund | Fundstelle |
|---|---|---|
| Z-1 | `ConfigurationService.save_profile` schreibt eine handgebaute TOML-Zeichenkette, die ausschließlich `[application]`, `[database]` und `[plugins]` umfasst. Ein `[security]`-Abschnitt würde durch `save_profile` **nicht** zurückgeschrieben | [SOURCE: BASELINE 8fcf42f:config/settings.py:`ConfigurationService.save_profile`] |
| Z-2 | `_merge` führt eine **einstufige** Zusammenführung durch: `result[key] = {**result.get(key, {}), **value}` für Tabellen der obersten Ebene. **Verschachtelte** Tabellen innerhalb eines Abschnitts werden durch die Profilfassung **vollständig ersetzt**, nicht gemischt | [SOURCE: BASELINE 8fcf42f:config/settings.py:`ConfigurationService._merge`] |

### 6.3 CS-3 — `config/default.toml`

| Feld | Inhalt |
|---|---|
| Zweck | Einführung eines `[security]`-Abschnitts |
| Erforderliche Eigenschaften | fehlender Abschnitt ⇒ sichere Defaults (C-1) · ungültige Werte ⇒ sichere Defaults bzw. bestehendes Fail-Secure-Verhalten (C-2, C-3) · **keine neue Ausnahmequelle** · Verwendung der **bestehenden** `from_config`-Fabriken |
| Schlüsselbindung | Die Schlüsselnamen müssen zu den bestehenden Fabriken passen: `evidence_level`, `scope`, `minimum_trust` (Integrity) sowie `wildcard`, `grants` (Permission) [SOURCE: BASELINE 8fcf42f:app/security/plugin_security.py:`IntegrityPolicy.from_config`, `PermissionPolicy.from_config`] |
| **Ausdrückliche Grenze** | Die genaue Policy-Konfiguration ist **keine neue Security-Entscheidung**: **keine neuen Grants erfinden**, **kein Plugin produktiv freischalten** |
| Klassifikation | **REQUIRED** |

> **Feststellung zur Wahrung von Default-Deny:** Ein `[security]`-Abschnitt ohne
> Grants ergibt über `PermissionPolicy.from_config` `wildcard = frozenset()` und
> `plugin_grants = {}` — identisch zum heutigen `PermissionPolicy()`. Das
> fail-secure-Verhalten des Baselines bleibt damit erhalten
> [SOURCE: BASELINE 8fcf42f:app/security/plugin_security.py:`PermissionPolicy`, `granted_for`].

---

## 7. Explicit Exclusions

**Die folgenden Artefakte sind NICHT Teil der erforderlichen Änderungsfläche:**

| # | Artefakt | Klassifikation | Grund |
|---|---|---|---|
| E-1 | `app/security/plugin_security.py` | **NOT REQUIRED** | Beide Policy-Argumente und beide `from_config`-Fabriken existieren bereits (A-2, A-8) |
| E-2 | `app/bootstrap/manager.py` | **NOT REQUIRED** | Weder Signatur noch `default_stages()` noch `run_phase` müssen geändert werden |
| E-3 | `app/bootstrap/__init__.py` | **NOT REQUIRED** | Festlegung B; `__all__` bleibt unverändert |
| E-4 | `app/bootstrap/types.py` | **NOT REQUIRED** | `BootstrapContext` besitzt bereits alle benötigten Felder |
| E-5 | `sdk/context.py` | **NOT AUTHORIZED** | TD-04-Gebiet; durch OD-05 nicht entschieden [SOURCE: docs/governance/od-05-governance-decision.md Kap. 12.1] |
| E-6 | `app/security/security_manager.py` | **NOT REQUIRED / separat** | TD-19-Anteil — Gegenstand von **F-4** (Kap. 8) |
| E-7 | `core/registry.py` | **NOT REQUIRED** | Die `pop()`-Kapselungsbrüche (**TD-06**) sind Symptom von TD-19, nicht Gegenstand |
| E-8 | `ui/navigation/navigation_service.py` | **NOT REQUIRED** | Desktop-Komposition unberührt; keine Änderung der Stage-Zusammensetzung |
| E-9 | Tests | **NOT REQUIRED durch NAW-A** | Nachweise **TG-2/TG-3/TG-4** bleiben erforderlich und nicht erbracht; ihre Erstellung ist nicht Gegenstand von NAW-A |
| E-10 | Packaging, CI, Deployment | **NOT REQUIRED** | außerhalb des Umrisses |
| E-11 | Trading, AI-/Agent-System, Memory-System | **NOT AUTHORIZED** | außerhalb jedes Auftragsumfangs |

---

## 8. TD-19 Boundary

> **TD-19 bleibt ausdrücklich OPEN. NAW-A löst TD-19 nicht.**

| Feld | Inhalt |
|---|---|
| Sachverhalt | `SecurityBootstrapStage` (FINALIZE) entfernt die registrierte `PluginSecurity`-Instanz und setzt die eigene [SOURCE: BASELINE 8fcf42f:app/security/security_manager.py Z. 203–204]. Im R0 als **DEVIATION** geführt [SOURCE: docs/audits/jochen-x-master-engineering-plan-r0.md §10.6, §10.9] |
| Wirkung von NAW-A | **keine.** `app/security/security_manager.py` ist ausgeschlossen (E-6). `SecurityBootstrapStage` wird durch NAW-A **nicht** geändert |
| Verbleibender TD-19-Umfang | **UNKNOWN** [SOURCE: docs/governance/od-05-governance-decision.md U-3] |
| Zuständigkeit | **F-4** |

**Konsequenz für den fixierten Umriss:** Die durch CS-1 konfigurierte Instanz
kann weiterhin in FINALIZE ersetzt werden. **Das ist eine Feststellung zum
Fortbestand von TD-19, keine Bewertung und keine Lösung.**

---

## 9. G-1 Boundary

> **G-1 = OPTION HYBRID bleibt unverändert. NAW-A interpretiert G-1 nicht neu.**

| Feld | Inhalt |
|---|---|
| Nicht entschieden durch NAW-A | „Sind geänderte `admitted_manifests` Teil des geschützten `BootstrapManager`-Kontrakts?" |
| Klassifikation | **F3-U2** — **OPEN DECISION** |
| Zuständigkeit | **NAW-B** — Präzisierung durch den **Projekteigner** |

Eine eigenständige Beantwortung durch NAW-A wäre eine Erweiterung von G-1 und
damit eine neue Governance-Regel. **Das findet nicht statt.**

---

## 10. §8 Impact

Bewertet gegen den **fixierten** Umriss CS-1 + CS-2 + CS-3.

### 10.1 §8-1 — Paketstruktur

Kein Modul im Bootstrap-Paket hinzugefügt, entfernt oder umbenannt. CS-1 ändert
eine bestehende Methode in einem bestehenden Modul; CS-2 und CS-3 liegen
**außerhalb** des Baseline-Scopes §2 (sieben `app/bootstrap/`-Module)
[SOURCE: docs/baselines/bootstrap-baseline-1.0.md §2, §8].

> **§8-1 = NOT TRIGGERED**

### 10.2 §8-2 — Runtime-Pipeline

Phasenreihenfolge unverändert; Stage-Reihenfolge unverändert (konstitutiv für
Option B); die Admission-Reihenfolge Integrity → API-Version → Permission →
Dependency → Activation bleibt unangetastet (CS-1)
[SOURCE: docs/governance/od-05-governance-decision.md Kap. 8; docs/baselines/bootstrap-baseline-1.0.md §5.2].

> **§8-2 = NOT TRIGGERED**

### 10.3 §8-3 — Public Exports

Durch Festlegung B bleibt `__all__` unverändert (Kap. 5). **Der in F-3 gehaltene
Vorbehalt für Ausgestaltungsvarianten entfällt** — die Bewertung ist jetzt
determinat.

> **§8-3 = NOT TRIGGERED** (determinat)

### 10.4 §8-4 — BootstrapManager (unter G-1 HYBRID)

| Grund aus F-3 | Status nach NAW-A |
|---|---|
| **R-3** — neuer `BootstrapError`-Pfad in INITIALIZE | **ENTFÄLLT** durch Festlegung A und die Eigenschaften C-1…C-3 (Kap. 4) |
| **R-5 / F3-U2** — Einordnung geänderter Zulassungswerte unter „Kontrakt" | **BESTEHT FORT** — NAW-B |

Kontraktbewertung gegen den fixierten Umriss:

| Methode | Ergebnis |
|---|---|
| `begin()` | **UNCHANGED** [SOURCE: docs/governance/f-03-od05-change-surface-assessment.md Kap. 8] |
| `run_phase()` | **UNKNOWN** — allein wegen F3-U2 |
| `build_context()` | **UNCHANGED** [ebd. Kap. 10] |

> **§8-4 = UNKNOWN**
>
> **NAW-A schließt §8-4 nicht** (Auftragsvorgabe Kap. 7). Die
> Unbestimmtheit ruht nach dieser Fixierung jedoch **nur noch auf einer**
> Grundlage: **F3-U2 / NAW-B**.

### 10.5 §8-5 — `default_stages()`

Stage-Zusammensetzung und -Reihenfolge unverändert; `PluginSecurityStage()`
bleibt an Position 9 [SOURCE: BASELINE 8fcf42f:app/bootstrap/manager.py:`default_stages`].

> **§8-5 = NOT TRIGGERED**

### 10.6 Architecture Freeze

Kein neuer Sachverhalt widerspricht **F-1-A**. `config/**` ist in AB §22.1 nicht
aufgeführt; der Freeze-Scope für `app/bootstrap` ist auf **BootstrapStage-Protocol**
und **StartupPhase-Enum** verengt — beide unberührt
[SOURCE: BASELINE 8fcf42f:docs/architecture-book-v2.md §22.1; docs/governance/f-01-od05-architecture-freeze-assessment.md Kap. 10].

> **F-1-A bleibt unverändert.** Kein Architecture Book geändert, keine
> AB-Version erzeugt.

---

## 11. Security Impact

**Ausdrücklich bestätigt:**

| # | Bestätigung | Beleg |
|---|---|---|
| S-1 | **Default-Deny bleibt erhalten.** Ein `[security]`-Abschnitt ohne Grants ergibt dieselbe leere Policy wie heute | [SOURCE: BASELINE 8fcf42f:app/security/plugin_security.py:`PermissionPolicy`, `granted_for`] |
| S-2 | **Keine neue Grant-Liste erfunden** — NAW-A legt keine Policy-Werte fest | Kap. 6.3 |
| S-3 | **Kein Plugin produktiv freigeschaltet** | Kap. 6.3 |
| S-4 | **TD-05 bleibt OPEN** — die Fixierung adressiert den fehlenden Konfigurationsweg, schließt ihn aber nicht | [SOURCE: docs/governance/od-05-governance-decision.md Kap. 12] |
| S-5 | **TD-19 bleibt OPEN** | Kap. 8 |
| S-6 | **TD-04 bleibt OPEN / NOT AUTHORIZED** | E-5 |
| S-7 | **TD-21 bleibt OPEN** | [SOURCE: docs/governance/od-05-governance-decision.md Kap. 12.3] |
| S-8 | **TD-06 bleibt OPEN** | E-7 |
| S-9 | **ODD-17 bleibt OPEN** | [SOURCE: docs/audits/jochen-x-master-engineering-plan-r0.md §10.8] |
| S-10 | **QG-006 bleibt NOT STARTED** | [SOURCE: docs/audits/jochen-x-master-engineering-plan-r0.md §24.3] |
| S-11 | **SG-C / SG-D / SG-E** unverändert nicht erfüllt bzw. nicht nachgewiesen; **TG-2 / TG-3 / TG-4** weiterhin erforderlich und **nicht erbracht** | [SOURCE: docs/audits/jochen-x-master-engineering-plan-r0.md §26, §15.4] |
| S-12 | **OD-04** bleibt OPEN; jedes Permission-Modell bleibt bis dahin **beratend, nicht erzwingend** | [SOURCE: docs/audits/jochen-x-master-engineering-plan-r0.md §10.4 SEC-04] |
| S-13 | **RB-1.0 (258/14) unverändert** | [SOURCE: docs/governance/milestone-1.0-baseline-commit-record.md §9] |

> **Kein Security Finding, keine ODD, kein Quality Gate und kein Technical Debt
> wird durch NAW-A geschlossen oder als bestanden markiert.**

---

## 12. ADR/RDR Status

| Prüfung | Befund |
|---|---|
| Ist ein §8-Tatbestand determinat ausgelöst? | **NEIN** — §8-1/§8-2/§8-3/§8-5 = NOT TRIGGERED; **§8-4 = UNKNOWN** |
| Steht eine Change-Control-Pflicht fest? | **NEIN** — und sie ist ebenso wenig ausgeschlossen |
| Bestimmt eine autorisierte Quelle die Wahl ADR ↔ RDR? | **NEIN** — §8 nennt beide alternativ ohne Kriterium; der Development Standard enthält keine RDR-Regeln [SOURCE: docs/baselines/bootstrap-baseline-1.0.md §8; docs/governance/f-02-bootstrap-baseline-scope-assessment.md Kap. 19] |

> ## **ADR/RDR = OPEN** · **B-6 bleibt offen**
>
> **Kein ADR erstellt. Kein RDR erstellt.**

---

## 13. Remaining UNKNOWNs

| ID | Offene Frage | Status nach NAW-A | Zuständig |
|---|---|---|---|
| ~~**F3-U1**~~ | `[security]` verpflichtend oder optional? | **GESCHLOSSEN** — OPTIONAL (Festlegung A) | — |
| ~~**F3-U4**~~ | Neues öffentliches Bootstrap-Symbol? | **GESCHLOSSEN** — NEIN (Festlegung B) | — |
| **F3-U2** | Erfasst G-1 HYBRID mit „Kontrakt" auch die von Stages erzeugten Zustandswerte (`admitted_manifests`)? | **OFFEN** — alleinige verbleibende Grundlage für §8-4 = UNKNOWN | **NAW-B** — Projekteigner |
| **F3-U3** | Verbleibender **TD-19**-Umfang | **OFFEN** | **F-4** |
| **F3-U5** | Abgrenzungskriterium **ADR ↔ RDR** (B-6) | **OFFEN** | **F-5** |
| **F3-U6** | Ob die Kontraktwirkung ohne Testlauf abschließend feststellbar ist | **OFFEN** — kein Testlauf durchgeführt | ggf. autorisierter Verifikationsschritt |
| **NAW-A-U1** | Wahl zwischen den CS-2-Varianten **V-1** und **V-2** | **OFFEN** — V-1 als bevorzugte minimalinvasive Variante ausgewiesen, **nicht** festgelegt | autorisierte Umsetzung |
| **NAW-A-U2** | Behandlung von Z-1 (`save_profile` schreibt `[security]` nicht zurück) und Z-2 (einstufiger `_merge`) | **OFFEN** — dokumentiert, nicht entschieden | autorisierte Umsetzung |

> Es wurde nicht implementiert und kein Test ausgeführt, um ein UNKNOWN
> künstlich zu beseitigen.

---

## 14. Next Authorized Work

> **Keine dieser Positionen wird durch NAW-A ausgeführt oder ausgelöst.**

| # | Position | Gegenstand | Autorität | Status |
|---|---|---|---|---|
| **NAW-B** | Präzisierung von **G-1** zu **F3-U2** | **Alleinige verbleibende Voraussetzung**, um §8-4 für den fixierten Umriss determinierbar zu machen | **Projekteigner** | **OPEN — HUMAN DECISION REQUIRED** |
| **F-4** | Bestimmung des **TD-19**-Restumfangs (F3-U3) | unverändert offen | Architektur-/Security-Governance | **OPEN** |
| **F-5** | Wiederholung der §8-Prüfung nach NAW-B und F-4; anschließend ADR-/RDR-Determination (B-6) | erst danach ist NAW-1 von Ergebnis D fortzuschreiben | Architektur-/Security-Governance | **OPEN** |
| — | **Umsetzungsautorisierung** (GDR-OD05-001 NAW-2) | erst nach F-5 und ggf. ADR/RDR | Projekteigner | **NICHT ERTEILT** |

**Reihenfolge-Feststellung (keine Autorisierung):** Nach NAW-A ist **NAW-B der
einzige verbleibende Blocker für die §8-4-Determination**. F-4 bleibt davon
unabhängig erforderlich, bevor F-5 abschließen kann.

---

## 15. Repository Integrity

| Prüfung | Vor NAW-A | Nach NAW-A |
|---|---|---|
| HEAD | `8fcf42f1997dfcf6ff232e75fd33c37b933991c8` | **unverändert** |
| Baseline-Hash | `8fcf42f1997dfcf6ff232e75fd33c37b933991c8` (`git cat-file -t` → `commit`) | **unverändert** |
| `git status` — getrackte Modifikationen | 6 | **6 — unverändert** |
| Staged changes | 0 | **0 — kein Staging** |
| Untracked (`-uall`) | 78 | 79 — **+1**: dieses Dokument |
| Bestandsdateien geändert | — | **0** |
| Tests | — | **nicht verändert, nicht ausgeführt** |
| Commit / Tag / Push / Cleanup | — | **KEINE** |

**BASELINE ≠ WORKING TREE ≠ UNTRACKED DOCS** — die drei Ebenen wurden getrennt
gehalten; sämtlicher Code ausschließlich über `git show 8fcf42f:<pfad>` gelesen.

---

## 16. Final Status

| Feld | Wert |
|---|---|
| **NAW-A** | **AUTHORIZED / COMPLETED** |
| **G-1** | **OPTION HYBRID — UNCHANGED** |
| **OD-05** | **OPTION B — UNCHANGED** |
| **`[security]`** | **OPTIONAL** |
| **NEW PUBLIC EXPORT** | **NO** |
| **MINIMAL CHANGE SURFACE** | **CS-1 + CS-2 + CS-3** |
| **§8-1** | **NOT TRIGGERED** |
| **§8-2** | **NOT TRIGGERED** |
| **§8-3** | **NOT TRIGGERED** |
| **§8-4** | **UNKNOWN** |
| **§8-5** | **NOT TRIGGERED** |
| **ARCHITECTURE FREEZE** | **F-1-A unverändert** |
| **ADR/RDR** | **OPEN** |
| **TD-04** | **OPEN / NOT AUTHORIZED** |
| **TD-05** | **OPEN** |
| **TD-06** | **OPEN** |
| **TD-19** | **OPEN** |
| **TD-21** | **OPEN** |
| **ODD-17 / OD-04** | **OPEN** |
| **QG-006** | **NOT STARTED** |
| **RB-1.0** | **unverändert (258/14)** |
| **Sprint Plan** | **unverändert** |
| **CODING** | **NOT AUTHORIZED** |

> **NAW-A ist eine Fixierung des Änderungsumrisses — keine Umsetzungsfreigabe,
> keine Coding-Autorisierung, keine Sprint-Freigabe.**

---

**Ende NAW-A Change-Surface Fixation — JOCHEN X Milestone 1.0
(FINAL GOVERNANCE ASSESSMENT, 2026-08-10) — Bezugs-Baseline
`MILESTONE-1.0-BASELINE = 8fcf42f1997dfcf6ff232e75fd33c37b933991c8`**
