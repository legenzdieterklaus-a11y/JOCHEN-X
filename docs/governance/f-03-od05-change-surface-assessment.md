# JOCHEN X — Milestone 1.0
# F-3 — OD-05 Option B — Change-Surface Assessment

| Feld | Wert |
|---|---|
| Dokumenttyp | Governance / Change-Surface Assessment (READ-ONLY) |
| **Assessment ID** | **F-3** |
| Status | **FINAL ASSESSMENT** — nicht normativ |
| Gegenstand | Technische Änderungsfläche von **OD-05 Option B** und ihre §8-Wirkung unter **G-1 = OPTION HYBRID** |
| Governance Input | **G-1 = OPTION HYBRID** (Projekteigner-Entscheidung) · **GDR-OD05-001** (Option B) · **F-1-A** · **F-2-B** |
| Datum | 2026-08-10 |
| Branch / HEAD | `milestone-1.0-governance` / `8fcf42f1997dfcf6ff232e75fd33c37b933991c8` |
| **§8-4 Ergebnis** | **UNKNOWN** (Kap. 18, 20) |
| Entscheidung in diesem Dokument | **KEINE** |

---

## 1. Executive Summary

**Was F-3 feststellt.** Die minimal erforderliche Änderungsfläche für OD-05
Option B umfasst **drei** Artefakte, von denen **nur eines** im Bootstrap-Paket
liegt:

| Artefakt | Im Baseline-Scope §2? | Klassifikation |
|---|---|---|
| `app/bootstrap/stages_plugin.py` — `PluginSecurityStage.execute` | **JA** | **REQUIRED** |
| `config/settings.py` — `ApplicationSettings` bzw. `ConfigurationService` | **NEIN** | **REQUIRED** |
| `config/default.toml` — `[security]`-Abschnitt | **NEIN** | **REQUIRED** |

**Der wesentliche neue Befund.** `ApplicationSettings` ist ein frozen Dataclass
mit **sieben festen Feldern und ohne Security-Feld**; `ConfigurationService.load()`
verwirft die rohe TOML-Abbildung nach der Validierung und bietet **keinen
öffentlichen Zugriff** darauf
[SOURCE: BASELINE 8fcf42f:config/settings.py:`ApplicationSettings`, `ConfigurationService.load`].
**Option B ist daher nicht allein innerhalb von `app/bootstrap/` umsetzbar** —
eine Änderung an `config/settings.py` ist strukturell erforderlich. Dieser Punkt
ist in der bisherigen Komponentenliste **nicht** enthalten
[SOURCE: docs/audits/jochen-x-decision-execution-matrix-r0.md §D-3].

**Zwei Befunde, die die Änderungsfläche verkleinern:**

1. `PluginSecurity.__init__` akzeptiert **bereits am Baseline** die Keyword-Argumente
   `integrity_policy` und `permission_policy`. Eine Änderung an
   `app/security/plugin_security.py` ist **NOT REQUIRED**
   [SOURCE: BASELINE 8fcf42f:app/security/plugin_security.py:`PluginSecurity.__init__`].
2. **Beide `from_config`-Fabriken sind total** — sie verwenden `get()` mit
   Defaults, fangen `ValueError` ab, prüfen Wertebereiche und `isinstance` und
   fallen jeweils auf sichere Defaults zurück. **Sie erzeugen keinen neuen
   Ausnahmepfad**
   [SOURCE: BASELINE 8fcf42f:app/security/plugin_security.py:`IntegrityPolicy.from_config`, `PermissionPolicy.from_config`].

**Ergebnis der Kontraktprüfung unter G-1 HYBRID:**

| Methode | Ergebnis |
|---|---|
| `begin()` | **UNCHANGED** |
| `run_phase()` | **UNKNOWN** |
| `build_context()` | **UNCHANGED** (bedingt auf die minimale Ausgestaltung) |

**§8-4 = UNKNOWN.** Zwei voneinander unabhängige Gründe (Kap. 18): (i) ob die
Ausgestaltung den `[security]`-Abschnitt **verpflichtend** oder **optional**
behandelt, entscheidet über einen **neuen `BootstrapError`-Pfad in INITIALIZE**
— und das ist durch GDR-OD05-001 ausdrücklich offen gelassen; (ii) ob geänderte
**Zulassungsergebnisse** (andere `admitted_manifests`) als Kontraktänderung von
`run_phase()` zählen, ist aus dem G-1-Wortlaut nicht determinierbar.

> **UNKNOWN wurde nicht zu NOT TRIGGERED umgedeutet** (Auftrag Kap. 11).

**§8-1, §8-2, §8-3, §8-5:** sämtlich **NOT TRIGGERED** für die erforderliche
Fläche (Kap. 15–17, 19). **F-1-A bleibt unverändert** — F-3 hat keinen
widersprechenden Sachverhalt gefunden (Kap. 20).

**ADR/RDR DETERMINATION = OPEN.** **CODING = NOT AUTHORIZED.**

---

## 2. Source Gate

| # | Pflichtquelle | Pfad | Status | Verifikation |
|---|---|---|---|---|
| 1 | Bootstrap Baseline 1.0 | `docs/baselines/bootstrap-baseline-1.0.md` | **APPROVED** | §2, §3, §4, §5, §8 |
| 2 | RDR-001 | `docs/rdr/001-bootstrap-modularization.md` | **APPROVED** | §2.2, §3 |
| 3 | Implementation Plan 1.0 | `docs/milestone-1.0-implementation-plan.md` | **APPROVED R1.2** | API-04, GC-06, BI-03, BP-01…BP-04 |
| 4 | Engineering Specification 1.0 | `docs/milestone-1.0-engineering-spec.md` | **APPROVED** ES-1.0 R1 | §132, §224, §393-Passage |
| 5 | Architecture Book v2.0 | `docs/architecture-book-v2.md` | **APPROVED / FROZEN** | **Welt A** (Kap. 3.2); §6.5, §9, §22 |
| 6 | OD-05 Decision | `docs/governance/od-05-governance-decision.md` | **FINAL** (GDR-OD05-001) | Kap. 4, 6, 8, 12, 17 |
| 7 | F-1 Assessment | `docs/governance/f-01-od05-architecture-freeze-assessment.md` | FINAL (F-1-A) | Kap. 10, 11 |
| 8 | F-2 Assessment | `docs/governance/f-02-bootstrap-baseline-scope-assessment.md` | FINAL (F-2-B) | Kap. 9–14, 17 |
| 9 | G-1 Decision Brief | `docs/audits/g-01-bootstrap-behavior-interpretation-decision-brief-r0.md` | DRAFT · NON-NORMATIVE | Kap. 8, 18–20 |
| 10 | Decision Execution Matrix | `docs/audits/jochen-x-decision-execution-matrix-r0.md` | R0 | §D-3 |
| 11 | Master Engineering Plan | `docs/audits/jochen-x-master-engineering-plan-r0.md` | R0 | §9.9, §10.5, §10.6, §10.9, §20 OD-05 |
| 12 | Security Design 1.0 | `docs/security-design-1.0.md` | **APPROVED** | geprüft — keine Aussage zur Stage-Komposition |
| 12b | Security Architecture 1.0 | `docs/security-architecture-1.0.md` | **APPROVED** | dito |
| 13 | Development Standard v1.1 | `docs/development-standard-v1.1.md` | **APPROVED** | §13 |
| 14 | Baseline Commit Record | `docs/governance/milestone-1.0-baseline-commit-record.md` | **FINAL** | §5, §6, §10 |

**Pfadabweichungen:** keine.

**Zusätzlich read-only gelesener Baseline-Code (T1/T2):**
`app/bootstrap/manager.py`, `app/bootstrap/types.py`, `app/bootstrap/__init__.py`,
`app/bootstrap/stages_init.py`, `app/bootstrap/stages_plugin.py`,
`app/bootstrap/stages_late.py`, `app/security/plugin_security.py`,
`app/security/security_manager.py`, `config/settings.py`, `config/default.toml`,
`ui/navigation/navigation_service.py`.

> **SOURCE GATE: BESTANDEN.**

---

## 3. Baseline Reference

| Prüfung | Ergebnis |
|---|---|
| Baseline-Identifier | `MILESTONE-1.0-BASELINE = 8fcf42f1997dfcf6ff232e75fd33c37b933991c8` [SOURCE: docs/governance/milestone-1.0-baseline-commit-record.md §6] |
| HEAD zu Beginn | identisch mit der Baseline |
| Reproduzierbarkeit | **PASS** — sämtlicher Code über `git show 8fcf42f:<pfad>` entnommen |

### 3.1 Ebenentrennung

| Ebene | Verwendung in F-3 |
|---|---|
| **BASELINE** (`8fcf42f`) | **Alleinige Grundlage** aller Code- und AB-Aussagen |
| **WORKING TREE** | Nur zur Divergenzfeststellung: die sechs getrackten Modifikationen betreffen `CLAUDE.md`, `ROADMAP.md`, ADR-005/006/007 und das Architecture Book — **kein** Bootstrap-, Security- oder Config-Artefakt. Der in F-3 analysierte Code ist im Working Tree **baseline-identisch** |
| **UNTRACKED DOCS** | Governance-/Audit-Dokumente; **keine Baseline** |

### 3.2 Fassungsregel Architecture Book

Angewandt wie bereits festgelegt: maßgeblich ist **Welt A**; die Working-Tree-Fassung
ist per GDR-OD01-001 (Option C) getrennt und nicht disponiert
[SOURCE: docs/governance/f-01-od05-architecture-freeze-assessment.md Kap. 2.2].

---

## 4. G-1 Input — HYBRID

**Als GOVERNANCE INPUT übernommen, nicht erneut diskutiert:**

> „Verhalten" des `BootstrapManager` umfasst (1) die API-Signatur und (2) den
> beobachtbaren Verhaltenskontrakt von `begin()`, `run_phase()` und
> `build_context()`. Eine Änderung ist unter §8-4 relevant **unabhängig davon, in
> welchem Modul die technische Ursache liegt**, wenn sie diesen Kontrakt
> **verändert**. Eine rein interne Änderung **ohne** beobachtbare Wirkung auf
> diesen Kontrakt fällt nicht allein aufgrund ihrer internen Natur unter §8-4.
> §8-1, §8-2, §8-3 und §8-5 bleiben vollständig und unabhängig in Kraft.

**Prüfregel für F-3:** Ändert die erforderliche Ausgestaltung von Option B den
beobachtbaren Kontrakt einer der drei Methoden — gleich wo die Ursache liegt?

**Nicht Gegenstand:** eine erneute Wahl zwischen NARROW/HYBRID/BROAD; eine
alternative Auslegung; eine neue Governance-Regel. G-1 genehmigt weder OD-05
Option B noch Coding noch eine konkrete Implementierung.

---

## 5. OD-05 Option B — Scope

**Unverändert** [SOURCE: docs/governance/od-05-governance-decision.md Kap. 8]:

> „Policy-Konfiguration in die bestehende `PluginSecurityStage` ziehen
> (**ohne** Reihenfolgeänderung)."

| # | Konstitutiv entschieden | Kategorie |
|---|---|---|
| 1 | Ort: die **bestehende** `PluginSecurityStage` | **APPROVED** |
| 2 | Gegenstand: **Policy-Konfiguration** | **APPROVED** |
| 3 | **Keine** Änderung der Phasen-/Stage-Reihenfolge | **APPROVED** |

| # | Ausdrücklich **offen** gelassen | Kategorie |
|---|---|---|
| 1 | Der Weg, auf dem die Policy-Konfiguration die Stage erreicht | **OPEN DECISION** [GDR-OD05-001 Kap. 6, C-2] |
| 2 | Ob ein neues öffentliches Symbol entsteht | **OPEN** [NAW-1 B-1] |
| 3 | Verbleibender **TD-19**-Umfang | **UNKNOWN** [GDR-OD05-001 U-3] |
| 4 | **TD-04** — Grant-Übertragung in den `PluginContext` | **NOT AUTHORIZED durch OD-05** [GDR-OD05-001 Kap. 12.1] |

F-3 entscheidet OD-05 nicht neu, bewertet Option A/C nicht und ändert Option B nicht.

---

## 6. Baseline IST-Zustand

| # | Feststellung | Kategorie | Fundstelle |
|---|---|---|---|
| B-1 | `default_stages()` liefert 13 Stages; `PluginSecurityStage()` an Position 9 | **EXISTING** | BASELINE 8fcf42f:app/bootstrap/manager.py:`default_stages` |
| B-2 | `PluginSecurityStage.name = "plugin_security"`, `phase = StartupPhase.LOAD_PLUGINS` | **EXISTING** | BASELINE 8fcf42f:app/bootstrap/stages_plugin.py:`PluginSecurityStage` |
| B-3 | Die Stage bezieht `PluginSecurity` aus der Registry; bei `LookupError` erzeugt sie **selbst** `PluginSecurity(events, logger=logger)` — **ohne Policy-Argumente** — und registriert sie | **EXISTING** | ebd., Z. 262–266 |
| B-4 | `PluginSecurity.__init__` akzeptiert **bereits** `integrity_policy` und `permission_policy` als optionale Keyword-Argumente; Defaults: `IntegrityPolicy()` bzw. `PermissionPolicy()` | **EXISTING** | BASELINE 8fcf42f:app/security/plugin_security.py:`PluginSecurity.__init__` |
| B-5 | `PermissionPolicy()` ohne Argumente ist **default-deny**: `wildcard_grants = frozenset()`, `plugin_grants = {}` ⇒ `granted_for(x) = ∅` | **EXISTING** | ebd.:`PermissionPolicy`, `granted_for` |
| B-6 | `IntegrityPolicy.from_config` und `PermissionPolicy.from_config` existieren, haben aber **keine produktive Aufrufstelle** (TD-05 / SEC-06) | **EXISTING** | [SOURCE: docs/audits/jochen-x-master-engineering-plan-r0.md §10.6 SEC-06] |
| B-7 | `config/default.toml` enthält die Abschnitte `[application]`, `[database]`, `[plugins]` — **kein `[security]`** | **EXISTING** | BASELINE 8fcf42f:config/default.toml |
| B-8 | `ApplicationSettings` ist ein frozen Dataclass mit **sieben** Feldern: `name`, `version`, `log_level`, `theme_mode`, `database_path`, `plugin_directory`, `developer_enabled`. **Kein Security-Feld** | **EXISTING** | BASELINE 8fcf42f:config/settings.py:`ApplicationSettings` |
| B-9 | `ApplicationSettings.from_mapping` verlangt die Abschnitte `application`, `database`, `plugins` und wirft bei `KeyError`/`TypeError`/`ValueError` einen `ConfigurationError` | **EXISTING** | ebd.:`from_mapping` |
| B-10 | `ConfigurationService.load()` liest die TOML-Dateien, merged ein optionales Profil und gibt **`ApplicationSettings`** zurück. **Die rohe Abbildung `raw` wird nicht aufbewahrt und ist über keine öffentliche Methode zugänglich** (`_read`/`_merge` sind privat) | **EXISTING** | ebd.:`ConfigurationService.load`, `_read`, `_merge` |
| B-11 | `ConfigurationStage` (INITIALIZE) setzt `context.configuration` und `context.settings = configuration.load()` | **EXISTING** | BASELINE 8fcf42f:app/bootstrap/stages_init.py:`ConfigurationStage.execute` |
| B-12 | `SecurityBootstrapStage` (FINALIZE, in `app/security/security_manager.py`) entfernt die registrierte `PluginSecurity`-Instanz und setzt die eigene — Grundlage von **TD-19** | **EXISTING** | BASELINE 8fcf42f:app/security/security_manager.py Z. 203–204 |
| B-13 | `PluginActivationStage.execute` kapselt die Aktivierung **je Plugin** in `try/except Exception` und sammelt Fehler in `context.activation_failures`; **Aktivierungsfehler propagieren nicht** | **EXISTING** | BASELINE 8fcf42f:app/bootstrap/stages_plugin.py:`PluginActivationStage.execute` |
| B-14 | Mit der ausgelieferten Konfiguration wird das Referenz-Plugin **nicht** aktiviert (`granted_for("reference") = ∅`) — fail-secure, aber ohne Konfigurationsweg (**PS-09**, **RK-07**) | **APPROVED-Befund** | [SOURCE: docs/audits/jochen-x-master-engineering-plan-r0.md §9.9 PS-09, §28 RK-07] |

---

## 7. BootstrapManager Contract

**Ist-Kontrakt aus der Baseline** [SOURCE: BASELINE 8fcf42f:app/bootstrap/manager.py].

| Element | Ist-Zustand |
|---|---|
| Typ | `@dataclass(frozen=True, slots=True)` |
| Öffentliches Feld | `stages: tuple[BootstrapStage, ...] = field(default_factory=default_stages)` |
| Öffentliche Methoden | `begin`, `run_phase`, `build_context` |
| `manager.py` `__all__` | `["BootstrapManager", "default_stages"]` |

*(Kap. 8–10 dokumentieren je Methode Inputs, Outputs, Exceptions, Operationsreihenfolge,
State-Änderungen und Seiteneffekte — jeweils nur das aus Code oder Quelle Belegbare.)*

---

## 8. `begin()`

**Ist-Kontrakt:**

| Aspekt | Belegter Zustand |
|---|---|
| Signatur | `begin(self, root: Path) -> BootstrapContext` |
| Verhalten | `return BootstrapContext(root=root)` — nichts weiter |
| Exceptions | **keine** dokumentierten; keine im Code erzeugten |
| State-Änderung | erzeugt einen frischen, mutablen `BootstrapContext`; alle übrigen Felder auf ihren Defaults |
| Seiteneffekte | **keine** |
| Security-Wirkung | **keine** |

**Prüfung gegen Option B:**

| Frage | Ergebnis | Begründung |
|---|---|---|
| Rückgabeverhalten geändert? | **nein** | Option B berührt weder `begin` noch `BootstrapContext`s Felderdefinition |
| Exceptions geändert? | **nein** | keine Ausnahmequelle in `begin` |
| Initialisierungszustand geändert? | **nein** | `BootstrapContext` besitzt bereits die Felder `admitted_manifests`, `activation_failures`, `metrics` |
| Stage-Setup geändert? | **nein** | `stages` wird in `begin` nicht berührt |
| Beobachtbare Seiteneffekte? | **nein** | keine vorhanden |

> ## **begin() = UNCHANGED**
>
> [SOURCE: BASELINE 8fcf42f:app/bootstrap/manager.py:`BootstrapManager.begin`;
> BASELINE 8fcf42f:app/bootstrap/types.py:`BootstrapContext`]

---

## 9. `run_phase()`

**Ist-Kontrakt:**

| Aspekt | Belegter Zustand |
|---|---|
| Signatur | `run_phase(self, context: BootstrapContext, phase: StartupPhase) -> None` |
| Dokumentierter Kontrakt | „Execute every stage belonging to `phase` in registration order. **Raises:** `BootstrapError`: If a stage fails; the original error is chained." |
| Operationsreihenfolge | Iteration über `self.stages` in Registrierungsreihenfolge; `stage.phase is not phase` → `continue`; sonst `stage.execute(context)` |
| Error-Wrapping | `except BootstrapError: raise` (durchgereicht) · `except Exception as error: raise BootstrapError(f"Bootstrap stage failed: {stage.name}") from error` |
| Abbruchverhalten | **erste** fehlschlagende Stage bricht die Phase ab |
| Context-Weitergabe | derselbe mutable `BootstrapContext` an alle Stages |
| State-Änderungen | ausschließlich diejenigen, die die Stages selbst vornehmen |
| Security-Wirkung | Über `PluginSecurityStage` in LOAD_PLUGINS: setzt `context.admitted_manifests` und registriert einen gefilterten `PluginCatalog` |

### 9.1 Prüfung gegen die erforderliche Änderungsfläche

| # | Prüfpunkt | Befund |
|---|---|---|
| R-1 | **Stage-Ausführung** (welche Stages, in welcher Reihenfolge) | **unverändert** — Option B ändert weder `stages` noch `phase` noch die Position (Kap. 16, 19) |
| R-2 | **Neuer Ausnahmepfad aus `PluginSecurityStage`?** | **NEIN bei der minimalen Ausgestaltung.** Beide `from_config`-Fabriken sind **total**: `IntegrityPolicy.from_config` fängt `ValueError` bei der Enum-Konversion ab und fällt auf `STRUCTURAL`/`VERIFIED` zurück, prüft `scope` gegen eine Whitelist; `PermissionPolicy.from_config` prüft `isinstance` und fällt auf leere Mengen zurück. Beide dokumentieren: „Unknown keys are ignored. Missing keys use safe defaults." [SOURCE: BASELINE 8fcf42f:app/security/plugin_security.py:`IntegrityPolicy.from_config`, `PermissionPolicy.from_config`] |
| R-3 | **Neuer Ausnahmepfad aus `ConfigurationStage` (INITIALIZE)?** | **ABHÄNGIG VON DER AUSGESTALTUNG.** `ApplicationSettings.from_mapping` wirft `ConfigurationError` bei fehlenden/fehlerhaften **Pflichtabschnitten**. Würde `[security]` als **Pflichtabschnitt** eingeführt, entstünde ein **neuer** Fehlerpfad: `ConfigurationError` → `run_phase(INITIALIZE)` → `BootstrapError`. Würde `[security]` **optional** behandelt (`raw.get("security", {})`), entstünde **kein** neuer Pfad. **GDR-OD05-001 legt dies nicht fest** → **UNKNOWN** |
| R-4 | **Neuer Ausnahmepfad aus `PluginActivationStage` (FINALIZE)?** | **NEIN.** Aktivierungsfehler werden je Plugin abgefangen und in `context.activation_failures` gesammelt; sie propagieren nicht [SOURCE: BASELINE 8fcf42f:app/bootstrap/stages_plugin.py:`PluginActivationStage.execute`]. Das gilt auch dann, wenn durch eine Policy **mehr** Plugins zugelassen und damit erstmals importiert würden |
| R-5 | **Geänderte Ergebniswerte** (`context.admitted_manifests`, registrierter `PluginCatalog`) | **JA — bei wirksamer Policy-Konfiguration.** Mit `[security]`-Grants können Plugins zugelassen werden, die am Baseline abgelehnt würden (B-5, B-14). **Ob eine Änderung der von `run_phase` erzeugten Zustandswerte eine Änderung des „beobachtbaren Kontrakts" i. S. v. G-1 darstellt, ist dem G-1-Wortlaut nicht eindeutig entnehmbar** (Kap. 14.2) → **UNKNOWN** |
| R-6 | **Abbruchverhalten** | unverändert, soweit R-3 optional ausgestaltet wird; andernfalls bricht INITIALIZE früher ab |

### 9.2 Ergebnis

> ## **run_phase() = UNKNOWN**
>
> **Warum nicht UNCHANGED:** Zwei offene Punkte können den Kontrakt verändern —
> **R-3** (neuer `BootstrapError`-Pfad in INITIALIZE, falls `[security]`
> verpflichtend ausgestaltet wird) und **R-5** (geänderte Zulassungswerte).
>
> **Warum nicht CHANGED:** Bei der minimalen Ausgestaltung (optionaler
> `[security]`-Abschnitt, Nutzung der bereits totalen `from_config`-Fabriken)
> entsteht **kein** neuer Ausnahmepfad; die Stage-Ausführung und das
> Error-Wrapping bleiben identisch.
>
> **Die Ausgestaltung ist durch GDR-OD05-001 Kap. 6 (C-2) ausdrücklich offen
> gelassen. UNKNOWN wird nicht zu UNCHANGED umgedeutet.**

---

## 10. `build_context()`

**Ist-Kontrakt:**

| Aspekt | Belegter Zustand |
|---|---|
| Signatur | `build_context(self, context: BootstrapContext, state_machine: ApplicationStateMachine) -> ApplicationContext` |
| Verhalten | Erzeugt `ApplicationContext` aus **12** über `_require(...)` geprüften Feldern: `settings`, `configuration`, `environment`, `versions`, `logger`, `service_provider`, `registry`, `events`, `scheduler`, `plugins`, `theme`, `resources`, zzgl. `RuntimeState(state_machine)` |
| Exceptions | `BootstrapError(f"Bootstrap stage dependency missing: {name}")`, wenn eines der Felder `None` ist [SOURCE: BASELINE 8fcf42f:app/bootstrap/types.py:`_require`] |
| Seiteneffekte | **keine** |

**Prüfung gegen Option B:**

| Frage | Befund |
|---|---|
| Context-**Struktur** geändert? | **nein** — Option B fügt dem `ApplicationContext` kein Feld hinzu |
| Enthaltene Werte geändert? | **nein** in den 12 geprüften Feldern. `context.plugins` ist der **`PluginLoader`**, gesetzt von `PluginDiscoveryStage` — von der Policy unberührt. `admitted_manifests` und `plugin_runtimes` fließen **nicht** in `build_context` ein [SOURCE: BASELINE 8fcf42f:app/bootstrap/manager.py:`build_context`; app/bootstrap/types.py:`BootstrapContext`] |
| Security-/Policy-Werte im Context? | **nein** — der `ApplicationContext` trägt keine Policy-Felder |
| Registry-Zustand? | Verändert sich (anderer `PluginCatalog`-Inhalt), **aber die Registry-Instanz selbst wird unverändert übergeben**; `build_context` liest keine Registry-Einträge |
| Exceptions geändert? | **nein** — keines der 12 Pflichtfelder wird von Option B beeinflusst |
| Beobachtbare Seiteneffekte? | **nein** |

> ## **build_context() = UNCHANGED**
>
> **Bedingung:** Gilt für die erforderliche Änderungsfläche (Kap. 12). Würde eine
> Ausgestaltungsvariante ein Policy-Feld in den `ApplicationContext` aufnehmen,
> wäre dies neu zu prüfen — eine solche Variante ist **POSSIBLE**, **nicht
> REQUIRED** (Kap. 13).

---

## 11. `PluginSecurityStage` — Current Flow

**Vier Schritte der Runtime-Pipeline, wie am Baseline ausgeführt**
[SOURCE: BASELINE 8fcf42f:app/bootstrap/stages_plugin.py:`PluginSecurityStage.execute`]:

```
_require(events) · _require(registry) · _require(logger)
  ↓
registry.get(PluginSecurity)
  └─ LookupError → PluginSecurity(events, logger=logger)   ← ohne Policy-Argumente
                   registry.register(PluginSecurity, security)
  ↓
für jedes manifest in context.manifests:
    1. security.validate_integrity(manifest)      → nicht admitted ⇒ continue
    2. API-Version-Gate (host_api.is_compatible_with)  → inkompatibel ⇒ PluginRejected + continue
    3. security.validate_permissions(manifest)    → nicht admitted ⇒ continue
       (finally: context.metrics.record_duration(...))
    → admitted.append(manifest)
  ↓
    4. _resolve_dependencies(tuple(admitted), logger, events) → resolved
  ↓
context.admitted_manifests = resolved
registry._lock / registry._registrations.pop(PluginCatalog, None)   ← TD-06
registry.register(PluginCatalog, PluginCatalog(ids der resolved))
logger.info("plugins.security.completed", ...)
```

### 11.1 Antworten auf die zehn Fragen des Auftrags (Kap. 9)

| # | Frage | Befund |
|---|---|---|
| 1 | **Wo wird Policy heute erzeugt?** | Implizit in `PluginSecurity.__init__` über die Defaults `IntegrityPolicy()` und `PermissionPolicy()` — **fest verdrahtet** (B-4, B-5) |
| 2 | **Wo wird Policy heute gelesen?** | In `PluginSecurity.validate_integrity` / `validate_permissions`; die Fabriken `from_config` haben **keine** produktive Aufrufstelle (B-6) |
| 3 | **Wo wird Admission entschieden?** | In `PluginSecurityStage.execute`, Schritte 1–3, ergänzt um die Abhängigkeitsauflösung in Schritt 4 |
| 4 | **Wo wird `PluginSecurity` erzeugt?** | **Zwei Orte**: `PluginSecurityStage` (LOAD_PLUGINS, bei `LookupError`) und `SecurityManager`/`SecurityBootstrapStage` (FINALIZE) — Grundlage von **TD-19** (B-3, B-12) |
| 5 | **Wo wird Policy konfiguriert?** | **Nirgends produktiv.** `config/default.toml` hat keinen `[security]`-Abschnitt (B-7); `ApplicationSettings` kein Security-Feld (B-8) |
| 6 | **Welche Daten fließen in die Entscheidung?** | Manifestdaten (Identifier, Version, `api_version`, deklarierte Permissions, Dependencies), `SDK_API_VERSION`, die Policy-Objekte |
| 7 | **Welche Defaults existieren?** | `IntegrityPolicy(evidence_level=STRUCTURAL, scope="manifest", minimum_trust=VERIFIED)`; `PermissionPolicy()` = default-deny |
| 8 | **Welche Fehler bei ungültiger Konfiguration?** | **Heute keine policy-bezogenen** — es gibt keinen Konfigurationspfad. `ApplicationSettings.from_mapping` wirft `ConfigurationError` nur für die drei bestehenden Pflichtabschnitte (B-9) |
| 9 | **Welche Wirkung hätte Option B?** | Die Policy würde aus der Konfiguration gespeist statt fest verdrahtet; damit könnten andere Plugins zugelassen werden (adressiert TD-05; RK-07 wäre entschärfbar) |
| 10 | **Würde diese Wirkung den `BootstrapManager`-Kontrakt verändern?** | **UNKNOWN** — siehe Kap. 9.2 (R-3, R-5). **Es wird ausdrücklich nicht behauptet, eine Security-Änderung löse automatisch §8-4 aus** |

---

## 12. Option B — Required Change Surface

| # | Datei / Symbol | Baseline-Zustand | Notwendige Änderung | Optionale Variante | Wirkung | Klasse |
|---|---|---|---|---|---|---|
| **CS-1** | `app/bootstrap/stages_plugin.py` → `PluginSecurityStage.execute`, Zweig `except LookupError` | `PluginSecurity(events, logger=logger)` ohne Policy-Argumente | Policy-Objekte aus der Konfiguration bilden und als `integrity_policy=` / `permission_policy=` übergeben | Ort der Policy-Bildung (in der Stage oder in einer Hilfsfunktion) | Policy nicht mehr fest verdrahtet | **REQUIRED** |
| **CS-2** | `config/settings.py` → `ApplicationSettings` **oder** `ConfigurationService` | `ApplicationSettings` hat sieben Felder ohne Security; `load()` verwirft die rohe TOML-Abbildung; **kein** öffentlicher Rohzugriff | **Ein** Zugang zur `[security]`-Abbildung schaffen — entweder ein Feld auf `ApplicationSettings` **oder** ein öffentlicher Rohzugriff auf `ConfigurationService` | Wahl zwischen beiden Wegen | Ohne dies erreicht die Konfiguration die Stage **nicht** | **REQUIRED** |
| **CS-3** | `config/default.toml` | `[application]`, `[database]`, `[plugins]` | `[security]`-Abschnitt mit Integrity-/Permission-Schlüsseln, passend zu den `from_config`-Schlüsselnamen | Umfang und Defaultwerte des Abschnitts | Konfigurationsweg entsteht (adressiert **TD-05**) | **REQUIRED** |

### 12.1 Begründung der Notwendigkeit von CS-2

Am Baseline besteht **kein Weg**, die `[security]`-Abbildung in die Stage zu
bringen:

- `context.settings` ist eine `ApplicationSettings` mit **sieben** festen Feldern,
  keines davon security-bezogen [SOURCE: BASELINE 8fcf42f:config/settings.py:`ApplicationSettings`].
- `context.configuration` ist ein `ConfigurationService`, dessen öffentliche
  Methoden `load()` und `save_profile()` sind. `load()` gibt `ApplicationSettings`
  zurück; die rohe Abbildung `raw` bleibt lokal. `_read` und `_merge` sind privat
  [SOURCE: BASELINE 8fcf42f:config/settings.py:`ConfigurationService`].

> **Neuer Befund gegenüber den Vorquellen:** Die Komponentenliste in
> [SOURCE: docs/audits/jochen-x-decision-execution-matrix-r0.md §D-3] nennt
> `config/default.toml`, **nicht** aber `config/settings.py`. F-3 stellt fest,
> dass `config/settings.py` **strukturell erforderlich** ist. **Dies ist eine
> Feststellung zur Änderungsfläche, keine Implementierungsvorgabe.**

### 12.2 Ausdrücklich NICHT erforderlich

| # | Artefakt | Warum NOT REQUIRED |
|---|---|---|
| N-1 | `app/security/plugin_security.py` | `PluginSecurity.__init__` akzeptiert beide Policy-Argumente bereits; `from_config` existiert bereits (B-4, B-6) |
| N-2 | `app/bootstrap/manager.py` | weder Signatur noch `default_stages()` noch `run_phase`-Logik müssen geändert werden |
| N-3 | `app/bootstrap/__init__.py` | kein neues Symbol für die erforderliche Fläche |
| N-4 | `app/bootstrap/types.py` | `BootstrapContext` besitzt bereits alle benötigten Felder |
| N-5 | `sdk/context.py` | betrifft **TD-04**, das durch OD-05 **nicht** entschieden ist (NOT AUTHORIZED) |
| N-6 | `app/security/security_manager.py` / `SecurityBootstrapStage` | betrifft den **TD-19**-Restumfang — **UNKNOWN**, siehe Kap. 13 |
| N-7 | `ui/navigation/navigation_service.py` | Desktop-Komposition unberührt; Option B ändert keine Stage-Zusammensetzung |
| N-8 | `core/registry.py` | die `pop()`-Kapselungsbrüche (**TD-06**) sind Symptom von TD-19 und nicht Gegenstand von Option B |

---

## 13. Required vs Possible Changes

> **Kategorientrennung strikt eingehalten: RECOMMENDED ≠ REQUIRED; UNKNOWN ≠ NOT REQUIRED.**

| Klasse | Position | Anmerkung |
|---|---|---|
| **REQUIRED** | CS-1, CS-2, CS-3 | ohne diese drei ist Option B nicht umsetzbar |
| **POSSIBLE** | Behandlung von `[security]` als **Pflichtabschnitt** statt optional | wirkt unmittelbar auf R-3 und damit auf §8-4 |
| **POSSIBLE** | Einführung eines neuen öffentlichen Symbols (z. B. einer Policy-Factory) in `app/bootstrap/__init__.py` | löste **§8-3** aus (Kap. 17) |
| **POSSIBLE** | Aufnahme von Policy-Werten in den `ApplicationContext` | wirkte auf `build_context()` (Kap. 10) |
| **POSSIBLE** | Berührung von `SecurityBootstrapStage` zur Adressierung des TD-19-Anteils | Umfang **UNKNOWN** [GDR-OD05-001 U-3]; liegt außerhalb `app/bootstrap/` |
| **RECOMMENDED** | — | **F-3 spricht keine Implementierungsempfehlung aus** |
| **NOT AUTHORIZED** | TD-04-bezogene Änderungen an `sdk/context.py`; jede Reihenfolgeänderung | [GDR-OD05-001 Kap. 12.1, Kap. 8] |

---

## 14. Indirect Effects

Unter G-1 HYBRID sind **indirekte** Wirkungen ausdrücklich erfasst. Geprüft wurden
alle vom Baseline-Code her möglichen Wirkungspfade von CS-1…CS-3 auf die drei
Methoden.

### 14.1 Geprüfte Wirkungspfade

| # | Pfad | Befund |
|---|---|---|
| I-1 | Policy-Bildung wirft → propagiert aus `PluginSecurityStage.execute` → `run_phase` wrappt zu `BootstrapError` | **kein neuer Pfad** bei Nutzung der totalen `from_config`-Fabriken (R-2) |
| I-2 | Konfigurationsvalidierung wirft in **INITIALIZE** → `ConfigurationError` → `BootstrapError` | **abhängig von der Ausgestaltung** (R-3) → **UNKNOWN** |
| I-3 | Andere Zulassungsmenge → mehr Plugins in `admitted_manifests` → `PluginActivationStage` importiert erstmals Plugin-Code | **kein neuer Ausnahmepfad** — Aktivierungsfehler werden abgefangen (B-13, R-4) |
| I-4 | Andere Zulassungsmenge → anderer `PluginCatalog` in der Registry | Registry-Instanz unverändert; `build_context` liest keine Einträge (Kap. 10) |
| I-5 | Andere Zulassungsmenge → andere Werte in `context.admitted_manifests` | **Wertänderung**; Einordnung **UNKNOWN** (14.2) |
| I-6 | `context.activation_failures` kann Einträge erhalten, wo bisher keine entstanden | **kein Kontraktbruch** — Feld existiert bereits und wird nicht von `build_context` geprüft |
| I-7 | Metriken (`context.metrics.record_duration`) | bereits am Baseline vorhanden; keine Kontraktwirkung |

### 14.2 Der verbleibende Auslegungspunkt

Die G-1-Entscheidung schützt den „**beobachtbaren Verhaltenskontrakt**" der drei
Methoden. Der dokumentierte Kontrakt von `run_phase` lautet: „Execute every stage
belonging to `phase` in registration order. Raises: `BootstrapError` if a stage
fails" [SOURCE: BASELINE 8fcf42f:app/bootstrap/manager.py:`run_phase`].

- **Unverändert** bleiben unter der minimalen Ausgestaltung: welche Stages laufen,
  in welcher Reihenfolge, und das Fehlerverhalten.
- **Verändert** würden die **Werte**, die eine Stage in den mutablen Context
  schreibt (I-5).

> **Ob G-1 HYBRID mit „Kontrakt" auch die von den Stages erzeugten Zustandswerte
> erfasst oder nur Ausführungsordnung, Rückgabe und Fehlerverhalten, ist dem
> Wortlaut der Entscheidung nicht eindeutig zu entnehmen.**
> **F-3 entscheidet dies nicht** — eine eigenständige Beantwortung wäre eine
> Erweiterung von G-1 und damit eine neue Governance-Regel.
> **Klassifikation: UNKNOWN / OPEN DECISION.**

---

## 15. §8-1 Assessment — Paketstruktur

| Prüfung | Befund |
|---|---|
| Modul im Bootstrap-Paket hinzugefügt, entfernt oder umbenannt? | **NEIN** — CS-1 ändert eine bestehende Methode in einem bestehenden Modul; CS-2 und CS-3 liegen **außerhalb** des Baseline-Scopes §2 (sieben `app/bootstrap/`-Module) |

> ## **§8-1 = NOT TRIGGERED**
> [SOURCE: docs/baselines/bootstrap-baseline-1.0.md §2, §8]

---

## 16. §8-2 Assessment — Runtime-Pipeline

| Prüfung | Befund |
|---|---|
| Phasenreihenfolge geändert? | **NEIN** — `StartupPhase`-Reihenfolge unberührt |
| Stage-Reihenfolge geändert? | **NEIN** — konstitutiver Bestandteil von Option B: „ohne Reihenfolgeänderung" |
| Pipeline Discovery → Integrity → Permission → Dependency → Activation? | **unverändert** — CS-1 berührt die Konstruktion der `PluginSecurity`-Instanz, nicht die vier Schritte oder ihre Folge |

> ## **§8-2 = NOT TRIGGERED**
> [SOURCE: docs/governance/od-05-governance-decision.md Kap. 8;
> docs/baselines/bootstrap-baseline-1.0.md §5.2, §8]

---

## 17. §8-3 Assessment — Public Exports

| Prüfung | Befund |
|---|---|
| `__all__`-Einträge in `app/bootstrap/__init__.py` geändert? | **NEIN für die erforderliche Fläche** — CS-1 ändert Methodeninhalt, kein Exportsymbol; die 20 Symbole bleiben identisch |
| Ausgestaltungsvarianten | Ein neues öffentliches Symbol wäre **POSSIBLE**, nicht REQUIRED (Kap. 13) → dann **TRIGGERED** |

> ## **§8-3 = NOT TRIGGERED** (für die erforderliche Änderungsfläche)
> **Vorbehalt:** **UNKNOWN**, falls eine Ausgestaltungsvariante ein neues
> `__all__`-Symbol einführte. [SOURCE: BASELINE 8fcf42f:app/bootstrap/__init__.py;
> docs/baselines/bootstrap-baseline-1.0.md §3.1, §8]

---

## 18. §8-4 Assessment under HYBRID

**Prüfregel (G-1):** ausgelöst, wenn der beobachtbare Kontrakt von `begin()`,
`run_phase()` oder `build_context()` verändert wird — unabhängig vom Ort der
Ursache.

| Methode | Ergebnis | Tragender Grund |
|---|---|---|
| `begin()` | **UNCHANGED** | keine Berührung (Kap. 8) |
| `run_phase()` | **UNKNOWN** | **R-3** (neuer `BootstrapError`-Pfad in INITIALIZE bei verpflichtendem `[security]`) **und** **R-5/I-5** (geänderte Zulassungswerte; Einordnung unter „Kontrakt" nicht determinierbar) |
| `build_context()` | **UNCHANGED** | 12 Pflichtfelder unberührt (Kap. 10) |

> ## **§8-4 = UNKNOWN**

**WHY — konkrete technische Begründung:**

1. **Ausgestaltungsabhängigkeit (R-3).** `ApplicationSettings.from_mapping` wirft
   `ConfigurationError` für fehlende oder fehlerhafte **Pflichtabschnitte**
   [SOURCE: BASELINE 8fcf42f:config/settings.py:`ApplicationSettings.from_mapping`].
   `ConfigurationStage.execute` ruft `configuration.load()` in **INITIALIZE**
   [SOURCE: BASELINE 8fcf42f:app/bootstrap/stages_init.py:`ConfigurationStage.execute`].
   Würde CS-2/CS-3 den `[security]`-Abschnitt **verpflichtend** ausgestalten,
   entstünde ein **neuer** `BootstrapError`-Pfad aus `run_phase(INITIALIZE)` —
   eine Änderung des dokumentierten Fehlerkontrakts. Würde er **optional**
   ausgestaltet, entstünde dieser Pfad nicht. **GDR-OD05-001 Kap. 6 (C-2) lässt
   dies ausdrücklich offen.**
2. **Auslegungsoffenheit (R-5 / I-5).** Selbst bei minimaler Ausgestaltung ändern
   sich die von `run_phase` erzeugten **Zustandswerte** (`admitted_manifests`,
   `PluginCatalog`-Inhalt). Ob G-1 HYBRID solche Wertänderungen als
   Kontraktänderung erfasst, ist dem Entscheidungswortlaut nicht zu entnehmen
   (Kap. 14.2).

> **UNKNOWN wurde nicht zu NOT TRIGGERED umgedeutet.** Bereits **einer** der
> beiden Punkte genügt, um das Ergebnis offenzuhalten.
>
> **Ausdrücklich nicht behauptet:** dass eine Security-Änderung automatisch §8-4
> auslöst.

---

## 19. §8-5 Assessment — `default_stages()`

| Prüfung | Befund |
|---|---|
| Stage-**Zusammensetzung** geändert? | **NEIN** — weiterhin dieselben 13 Stages |
| Stage-**Reihenfolge** geändert? | **NEIN** — `PluginSecurityStage()` bleibt an Position 9 |
| Signaturseitige Berührung von `BootstrapManager(stages=…)`? | **NEIN** |

> ## **§8-5 = NOT TRIGGERED**
> [SOURCE: BASELINE 8fcf42f:app/bootstrap/manager.py:`default_stages`;
> docs/baselines/bootstrap-baseline-1.0.md §8]

---

## 20. Architecture Freeze

**F-1 hat festgestellt: F-1-A — ARCHITECTURE FREEZE NOT TOUCHED.** F-3 prüft
ausschließlich, ob ein **neuer Sachverhalt** diesem Befund widerspricht.

| Neuer Sachverhalt aus F-3 | Widerspruch zu F-1-A? |
|---|---|
| CS-2 berührt `config/settings.py` | **NEIN** — `config/**` ist in AB §22.1 nicht aufgeführt [SOURCE: BASELINE 8fcf42f:docs/architecture-book-v2.md §22.1] |
| CS-3 berührt `config/default.toml` | **NEIN** — dito |
| CS-1 berührt `app/bootstrap/stages_plugin.py` | **NEIN** — der Freeze-Scope für `app/bootstrap` ist auf **BootstrapStage-Protocol** und **StartupPhase-Enum** verengt; beide unberührt |
| Möglicher neuer `BootstrapError`-Pfad (R-3) | **NEIN** — `BootstrapError` ist kein Element des Freeze-Scopes §22.1 |
| Kein §22.3-Tatbestand ausgelöst | **NEIN** — insbesondere keine Änderung der Bootstrap-Phasenreihenfolge |

> ## **F-1-A bleibt unverändert.**
> Keine AB-Version erzeugt, kein Freeze geändert, das Architecture Book nicht
> berührt.

---

## 21. Security Impact

**Ausschließlich belegte Wirkung; keine Erweiterung.**

| Aspekt | Befund | Kategorie |
|---|---|---|
| **TD-05** (Policy-Konfigurierbarkeit) | CS-1…CS-3 adressieren den fehlenden Konfigurationsweg. **Nicht geschlossen** — Umsetzung und Nachweis stehen aus | **OPEN** |
| **TD-19** (Trust-Ledger-Identität) | `SecurityBootstrapStage` ersetzt die Instanz weiterhin (B-12). Die erforderliche Fläche adressiert dies **nicht**; der Restumfang bleibt **UNKNOWN** [GDR-OD05-001 U-3] | **OPEN / UNKNOWN** |
| **TD-04** (Host-Grants im `PluginContext`) | Durch OD-05 **nicht** entschieden; `sdk/context.py` ist NOT REQUIRED (N-5) | **OPEN / NOT AUTHORIZED** |
| **TD-21** (Audit-Trail) | unberührt; Substanz an **ODD-17** gebunden | **OPEN** |
| **TD-06** (Registry-Kapselung) | die `pop()`-Stellen bestehen fort; nicht Gegenstand | **OPEN** |
| **RK-07** (Plugin-Fähigkeit produktiv abgeschaltet) | wäre durch einen wirksamen Konfigurationsweg **entschärfbar** — nicht durch dieses Assessment entschärft | **OPEN** |
| **Default-Deny** | Die Mechanik bleibt erhalten; ein `[security]`-Abschnitt kann Grants **hinzufügen**. Der fail-secure-Ausgangszustand (B-5, B-14) bliebe bei leerer Konfiguration bestehen | **EXISTING** |
| SG-C / SG-D / SG-E | unverändert nicht erfüllt bzw. nicht nachgewiesen; **TG-2/TG-3/TG-4** weiterhin erforderlich und nicht erbracht | **OPEN** |
| **QG-006** | **NOT STARTED** — unverändert | **OPEN** |

> **Kein Security Finding, keine ODD, kein Quality Gate und kein Technical Debt
> wird durch F-3 geschlossen oder als bestanden markiert.**

---

## 22. ADR/RDR Determination

| Prüfung | Befund |
|---|---|
| Ist ein §8-Tatbestand **determinat** ausgelöst? | **NEIN** — §8-1, §8-2, §8-3, §8-5 = NOT TRIGGERED; **§8-4 = UNKNOWN** |
| Steht damit eine Change-Control-Pflicht fest? | **NEIN** — solange §8-4 UNKNOWN ist, ist die Pflicht **nicht determiniert**. Sie ist ebenso wenig ausgeschlossen |
| Bestimmt eine autorisierte Quelle die Wahl zwischen ADR und RDR? | **NEIN** — Baseline §8 nennt beide alternativ **ohne Abgrenzungskriterium**; der Development Standard enthält keine RDR-Regeln [SOURCE: docs/baselines/bootstrap-baseline-1.0.md §8; docs/governance/f-02-bootstrap-baseline-scope-assessment.md Kap. 19] |

> ## **ADR/RDR DETERMINATION = OPEN**
>
> **B-6 bleibt offen.** F-3 erfindet kein Kriterium und erstellt weder ADR noch
> RDR.

**Hinweis zur Verfahrensfolge:** Implementation Plan **GC-06** verlangt die
genehmigte Governance-Entscheidung **„vor der Implementierung"**
[SOURCE: docs/milestone-1.0-implementation-plan.md GC-06]. Solange §8-4 UNKNOWN
ist, ist diese Voraussetzung **nicht geklärt**.

---

## 23. UNKNOWNs

| ID | Offene Frage | Warum offen | Auflösbar durch |
|---|---|---|---|
| **F3-U1** | Wird `[security]` als **Pflicht-** oder als **optionaler** Abschnitt ausgestaltet? | GDR-OD05-001 Kap. 6 (C-2) lässt die Ausgestaltung offen | Festlegung des Änderungsumrisses durch die Architektur-/Security-Governance (Kap. 25, NAW-A) |
| **F3-U2** | Erfasst G-1 HYBRID mit „Kontrakt" auch die von Stages erzeugten **Zustandswerte**? | Dem G-1-Wortlaut nicht entnehmbar (Kap. 14.2) | **Präzisierung durch den Projekteigner** — F-3 darf dies nicht selbst beantworten |
| **F3-U3** | Verbleibender **TD-19**-Umfang und ob dafür `SecurityBootstrapStage` berührt werden müsste | GDR-OD05-001 U-3; R0 führt es nicht aus | **F-4** |
| **F3-U4** | Führt eine Ausgestaltungsvariante ein neues `__all__`-Symbol ein (§8-3)? | POSSIBLE, nicht REQUIRED | NAW-A |
| **F3-U5** | Abgrenzungskriterium **ADR ↔ RDR** | keine Quelle | **B-6 / F-5**, außerhalb F-3 |
| **F3-U6** | Ob die Wirkung auf `run_phase` ohne Testlauf abschließend feststellbar ist | Ein Testlauf wurde **nicht** durchgeführt (Auftrag Kap. 16) | statische Festlegung des Umrisses (NAW-A) oder autorisierter Verifikationsschritt |

> **Es wurde nicht implementiert, um ein UNKNOWN künstlich zu beseitigen.**

---

## 24. Findings

| # | Finding | Kategorie | Fundstelle |
|---|---|---|---|
| **F-3-01** | Die erforderliche Änderungsfläche umfasst **drei** Artefakte; **nur eines** (`stages_plugin.py`) liegt im Bootstrap-Paket | **REQUIRED** | Kap. 12 |
| **F-3-02** | `config/settings.py` ist **strukturell erforderlich** und in der bisherigen Komponentenliste [DEM §D-3] **nicht** enthalten | **REQUIRED** — neuer Befund | Kap. 12.1 |
| **F-3-03** | `app/security/plugin_security.py` ist **NOT REQUIRED** — beide Policy-Argumente existieren bereits | **NOT REQUIRED** | Kap. 12.2, N-1 |
| **F-3-04** | Beide `from_config`-Fabriken sind **total** und erzeugen keinen neuen Ausnahmepfad | **EXISTING** | Kap. 9.1, R-2 |
| **F-3-05** | Aktivierungsfehler propagieren **nicht**; auch mehr zugelassene Plugins erzeugen keinen neuen `BootstrapError`-Pfad in FINALIZE | **EXISTING** | Kap. 9.1, R-4 |
| **F-3-06** | Ein **neuer** `BootstrapError`-Pfad in **INITIALIZE** entsteht **genau dann**, wenn `[security]` verpflichtend ausgestaltet wird | **UNKNOWN** | Kap. 18, R-3 |
| **F-3-07** | `build_context()` ist von der erforderlichen Fläche nicht betroffen — `admitted_manifests` fließt nicht ein | **EXISTING** | Kap. 10 |
| **F-3-08** | §8-1, §8-2, §8-3, §8-5 = **NOT TRIGGERED**; §8-4 = **UNKNOWN** | **Ergebnis** | Kap. 15–19 |
| **F-3-09** | **F-1-A** wird durch keinen neuen Sachverhalt widerlegt | **bestätigt** | Kap. 20 |
| **F-3-10** | Die Anwendung von G-1 HYBRID auf Wertänderungen ist nicht determiniert | **OPEN DECISION** | Kap. 14.2, F3-U2 |

---

## 25. Recommendation / Next Authorized Work

> **Keine dieser Positionen wird durch F-3 ausgeführt oder ausgelöst.** Jede
> bedarf einer eigenen, ausdrücklichen Autorisierung. **F-3 spricht keine
> Implementierungsempfehlung aus.**

| # | Position | Gegenstand | Autorität | Status |
|---|---|---|---|---|
| **NAW-A** | **Fixierung des Änderungsumrisses** — insbesondere, ob `[security]` verpflichtend oder optional ist (**F3-U1**) und ob ein neues öffentliches Symbol entsteht (**F3-U4**). **Keine Implementierung — nur Festlegung** | löst **F3-U1** und **F3-U4** auf | Architektur-/Security-Governance | **OPEN — nicht gestartet** |
| **NAW-B** | **Präzisierung von G-1** zur Frage, ob „Kontrakt" die von Stages erzeugten Zustandswerte erfasst (**F3-U2**) | erforderlich, damit §8-4 auch bei minimaler Ausgestaltung determinierbar wird | **Projekteigner** | **OPEN — HUMAN DECISION REQUIRED** |
| **NAW-C** | **F-4** — Bestimmung des TD-19-Restumfangs (**F3-U3**) | unverändert offen | Architektur-/Security-Governance | **OPEN** |
| **NAW-D** | **F-5** — Wiederholung der §8-Prüfung nach NAW-A, NAW-B und F-4; anschließend ADR-/RDR-Determination (**B-6**) | erst danach ist NAW-1 von Ergebnis D fortzuschreiben | Architektur-/Security-Governance | **OPEN** |

**Reihenfolge-Feststellung (keine Autorisierung):** **NAW-A und NAW-B sind
voneinander unabhängig, aber beide vor F-5 erforderlich.** NAW-B ist auch dann
erforderlich, wenn NAW-A den minimalen Umriss wählt — denn F3-U2 bleibt in beiden
Fällen bestehen.

---

## 26. Repository Integrity

| Prüfung | Vor F-3 | Nach F-3 |
|---|---|---|
| HEAD | `8fcf42f1997dfcf6ff232e75fd33c37b933991c8` | **unverändert** |
| Baseline-Hash | `8fcf42f1997dfcf6ff232e75fd33c37b933991c8` | **unverändert** |
| `git status` — getrackte Modifikationen | 6 | **6 — unverändert** |
| Staged changes | 0 | **0 — kein Staging** |
| Untracked (`-uall`) | 77 | 78 — **+1**: dieses Dokument |
| Bestandsdateien geändert | — | **0** |
| Tests | — | **nicht verändert, nicht ausgeführt** |
| Commit / Tag / Push / Cleanup | — | **KEINE** |

**BASELINE ≠ WORKING TREE ≠ UNTRACKED DOCS** — die Ebenen wurden getrennt
gehalten (Kap. 3.1).

---

## 27. Final Decision Status

| Feld | Wert |
|---|---|
| **F-3 STATUS** | **FINAL ASSESSMENT** |
| **G-1** | **OPTION HYBRID — GOVERNANCE INPUT** (nicht neu diskutiert) |
| **OD-05** | **OPTION B — UNCHANGED** |
| **§8-1 / §8-2 / §8-3 / §8-5** | **NOT TRIGGERED** (§8-3 mit Vorbehalt für Ausgestaltungsvarianten) |
| **§8-4** | **UNKNOWN** |
| **BEGIN** | **UNCHANGED** |
| **RUN_PHASE** | **UNKNOWN** |
| **BUILD_CONTEXT** | **UNCHANGED** |
| **ARCHITECTURE FREEZE** | **F-1-A unverändert** |
| **ADR/RDR** | **OPEN** |
| **TD-04 / TD-05 / TD-06 / TD-19 / TD-21** | **OPEN** |
| **ODD-17 / OD-04** | **OPEN** |
| **QG-006** | **NOT STARTED** |
| **RB-1.0** | **unverändert (258/14)** |
| **Sprint Plan** | **unverändert** |
| **CODING** | **NOT AUTHORIZED** |

> **F-3 entscheidet nicht:** ob OD-05 umgesetzt wird · ob Coding beginnt · ob ein
> Sprint startet · ob ein ADR oder RDR erstellt wird · ob Security Findings, ODDs
> oder Technical Debt geschlossen werden · ob QG-006 bestanden ist.

---

**Ende F-3 Change-Surface Assessment — JOCHEN X Milestone 1.0
(FINAL ASSESSMENT, 2026-08-10, Governance Input G-1 = OPTION HYBRID) —
Bezugs-Baseline `MILESTONE-1.0-BASELINE = 8fcf42f1997dfcf6ff232e75fd33c37b933991c8`**
