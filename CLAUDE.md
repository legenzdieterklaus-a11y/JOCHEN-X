# JOCHEN X

Modularer lokaler KI-Assistent (JARVIS-Prinzip). PySide6 Desktop-Framework.

## Quickstart

```bash
python -m pytest                    # Tests ausführen
python main.py                      # Anwendung starten (benötigt PySide6)
```

- Python ≥ 3.13, einzige externe Abhängigkeit: PySide6 ≥ 6.8
- Konfiguration: `config/default.toml`, optional `config/profile.toml`
- Datenbank: SQLite unter `data/jochen_x.sqlite3`

## Projektstruktur

```
core/           Stabile Verträge: Events, Registry, Version, Extensions
app/            Bootstrap, Lifecycle, Security, DI, ApplicationHost
  security/     SecurityManager, PluginSecurity, SecretVault
plugins/        Manifest-only Discovery (PluginLoader, PluginCatalog)
sdk/            Plugin SDK – einzige öffentliche API für Plugin-Autoren
services/       Observability, Security-Services
developer/      Optionale Developer Platform (Inspector, Diagnostics)
ui/             PySide6 UI-Schicht (Navigation, Chat, Dashboard)
  navigation/   Sidebar, Toolbar, StatusBar, ThemeManager
config/         TOML-Konfiguration
database/       SQLite ConnectionManager, Migrations
docs/           Spezifikationen und ADRs
  adr/          Architekturentscheidungen (ADR-001 bis ADR-011)
tests/          Pytest-basierte Tests
```

## Architektur

### Verbindliche Architekturreferenz

**[`docs/architecture-book-v2.md`](docs/architecture-book-v2.md)** (Architecture Book v2.0) ist die verbindliche Architekturreferenz für JOCHEN X.

- Status: **APPROVED / FROZEN** (Tags: `architecture-book-v2.0`, `core-runtime-v1.0.0`)
- Keine inhaltlichen Änderungen an v2.0
- Zukünftige Anpassungen nur über neue Dokumentversionen (z. B. v2.1 oder v3.0) und dokumentierte ADRs in `docs/adr/`
- Alle Implementierungen und Spezifikationen müssen mit diesem Dokument konsistent sein oder bewusst über ADR + Versionsupdate abweichen

Visuelle Kurzübersicht: [`ARCHITECTURE.md`](ARCHITECTURE.md)

### Schichtmodell

```
Core → App → Plugins/SDK → Services → Developer → UI
```

Abhängigkeiten zeigen immer nach innen. Keine Schicht importiert aus einer äußeren.

### Bootstrap-Reihenfolge

`ApplicationHost` startet über `BootstrapManager` in deterministischer Phasenfolge:

1. **INITIALIZE** — Environment, Config, Logging, Database, Registry, Theme, Scheduler
2. **LOAD_PLUGINS** — PluginDiscoveryStage, PluginSecurityStage (ADR-011)
3. **LOAD_RESOURCES** — ResourceManager
4. **FINALIZE** — PluginActivationStage (ADR-011), DeveloperTools, DI-Validation

### Kernprinzipien

- `ServiceRegistry` ist der einzige Kompositionsmechanismus
- Plugin-Discovery ist manifest-only: kein Plugin-Code-Import durch die Foundation (ADR-001)
- Plugin-Autoren nutzen ausschließlich `sdk/` — nie `core`, `app` oder `plugins` (ADR-010)
- Events über `core.events.EventBus` mit typed Application Events
- Alle Architekturentscheidungen stehen in `docs/adr/`

### Genehmigte ADRs (Milestone 0.9)

- ADR-005: Plugin-Integrity-Validation (APPROVED)
- ADR-006: Plugin-Permission-Model (APPROVED)
- ADR-007: Plugin-Dependency-Resolution (APPROVED)

## Arbeitsregeln

### Vor jeder Implementierung

1. Aufgabe analysieren, betroffene Dateien nennen
2. Aufwand schätzen, Risiken benennen
3. Kurzplan erstellen
4. **Bei > 5 betroffenen Dateien: Freigabe einholen**

### Implementierung

- Kleine logisch getrennte Schritte
- Ein Commit pro Aufgabe, keine Feature-Vermischung
- Keine Änderungen außerhalb des Auftrags
- Keine unnötigen Refactorings oder Bibliotheken
- Bestehende Architektur hat Vorrang vor Neuentwicklung

### Nachweisführung

**Ohne Beleg gilt „unklar", nicht „gewollt".** Eine plausible Ableitung ist
kein Beleg. Wird eine Quelle zitiert, muss sie die Aussage tatsächlich
tragen — im Zweifel gegen die Primärquelle prüfen, nicht gegen ein Dokument,
das sie zitiert.

**Fakt, Ableitung und Empfehlung sind zu trennen.** Eine Ableitung wird als
solche gekennzeichnet, auch wenn sie überzeugend ist.

**Bei Abweichung gilt STOPP, nicht Interpretation.** Weicht ein Ist-Wert von
der Erwartung ab, wird gemeldet und angehalten — nicht angepasst, bis es
passt.

### Erwartungswerte

**Keine festen Zahlen für volatile Größen.** HEAD-SHA, Anzahl untracked
Dateien und Befundzahlen ändern sich zwischen Planung und Ausführung.
Erwartungen werden relativ formuliert („unverändert gegenüber der
Vorprüfung") oder als Erhebung, nicht als Vorgabe.

**Ausnahme:** Werte, deren Abweichung ein echter Stopp-Grund wäre. Dort ist
der feste Wert die Absicherung.

### Bereinigungsarbeit

**Befunde werden behoben, nicht wegkonfiguriert.** Eine Ausnahme ist nur
zulässig, wenn ihre Befolgung eine höherrangige Vorgabe verletzen würde oder
technisch unmöglich ist — mit Beleg. Nie aus Bequemlichkeit.

**Kein `noqa`, kein `type: ignore`, keine Lockerung der Prüfkonfiguration**
ohne ausdrückliche Entscheidung. Ausnahmen gehören in `pyproject.toml` mit
Begründungskommentar, nicht verstreut in den Quelltext.

**Zuordnungspflicht:** Jeder beseitigte Befund muss einer konkreten
Ausgangsmeldung zugeordnet werden. Nicht zugeordnete Befunde bleiben
unangetastet.

**Ein Test gewinnt gegen eine Umstellung.** Widerspricht ein Test einer
Änderung, wird die Änderung zurückgenommen — nicht der Test angepasst.

### Vor jedem Schreibakt

1. Freigabe muss ausdrücklich vorliegen
2. Verifikation **vor** dem Commit, nicht danach
3. Ein Commit pro Thema
4. Nach Änderungen an `app/`, `core/`, `sdk/`: **beide API-Snapshots prüfen**
   — eine Abweichung ist eine Vertragsänderung, kein Bereinigungsschritt
5. Nach Änderungen an der Paketstruktur oder an `app/bootstrap/`:
   **Startnachweis wiederholen** (`python main.py` bis `READY`)

### Analyse

**Ein Import aus einem Paket mit `__init__.py` zieht dessen vollständigen
Importbaum nach.** Zirkularitätsprüfungen, die nur Zielmodule lesen, sind
unvollständig. Namespace-Pakete ohne `__init__.py` sind davon nicht betroffen.

**„Statisch nicht erreichbar" bedeutet nicht „toter Code".** Dynamisch
geladene Plugins, Testinfrastruktur und Gerüste für künftige Arbeit stehen
nicht im Importgraph.

**Ruff vereinigt alle passenden `per-file-ignores`-Muster** — Datei- und
Verzeichniseinträge ergänzen einander, das spezifischste verdrängt nicht die
übrigen.

### Trennschärfe

| Unterscheidung | Bedeutung |
|---|---|
| offen ≠ unbehandelt ≠ blockierend | ein registrierter offener Punkt blockiert nichts |
| nicht im Scope ≠ erledigt | Zurückstellung schließt nichts |
| entschieden ≠ vollzogen | ein Beschluss ohne Ausführung bleibt offen |
| Inhalt ≠ Prozess | die Sachfrage und ihr Verfahren werden getrennt geführt |

### Meilensteinbericht

**Nach jedem abgeschlossenen Meilenstein wird ein Bericht erstellt** — vor
dem nächsten Arbeitsschritt, nicht nachträglich. Der Bericht wird einmal
vollständig durchgegangen und geprüft, bevor er als abgeschlossen gilt.

Er enthält:

| Abschnitt | Inhalt |
|---|---|
| **Was ausgeführt wurde** | Commits mit Hash, Umfang in Dateien und Zeilen |
| **Belegter Stand** | Messwerte mit Quelle: Tests, Lint, Typprüfung, Gate, Snapshots, Startnachweis |
| **Was entschieden wurde** | Human Decisions mit Record-Verweis |
| **Was offen bleibt** | benannt, nicht implizit — mit Kennung, wo eine existiert |
| **Zurückgenommene Aussagen** | Behauptungen, die sich nicht gehalten haben, mit Belegstelle |
| **Nicht behandelt** | ausdrücklich zurückgestelltes, damit es nicht als erledigt gilt |

**Zahlen im Bericht sind zu belegen, nicht zu erinnern.** Jede Kennzahl wird
zum Berichtszeitpunkt erhoben.

**Der Bericht ist keine Erfolgsmeldung.** Fehlgeschlagene Versuche, korrigierte
Annahmen und Stopps gehören hinein — sie sind der Teil, der später gebraucht
wird.

### Git-Konventionen

Commit-Präfixe: `feat`, `fix`, `docs`, `refactor`, `test`, `chore`

Format: `<prefix>(<scope>): <kurze Beschreibung>`

Vor jedem Commit prüfen:
- Gehört alles zum gleichen Thema?
- Kann der Commit einzeln verstanden werden?
- Sind keine Secrets oder unnötigen Dateien enthalten?

### Tests

```bash
python -m pytest tests/test_core.py      # Einzelner Testfile
python -m pytest -q                      # Kompletter Lauf
```

- Nur relevante Tests ausführen
- Kompletter Testlauf nur bei mehreren betroffenen Kernmodulen
- Tests brauchen keinen Qt-Event-Loop (außer UI-Tests)

### Dokumentation

- Architekturentscheidungen als ADR in `docs/adr/`
- Alternativen nennen, Empfehlung begründen, Auswirkungen dokumentieren
- Spezifikationen in `docs/*.md` (pro Modul eine Datei)

### Kosteneffizienz

- Nur aufgabenrelevante Dateien lesen
- Vorhandene ADRs und Doku nutzen statt neu zu analysieren
- Keine wiederholten Analysen bei unveränderten Dateien
- Bei teuren Aufgaben: günstigere Alternative vorschlagen

## Stilregeln für Code

- Type Hints auf allen öffentlichen APIs
- Frozen Dataclasses für Value Types
- Protocols statt ABCs für Schnittstellen zwischen Schichten
- Kein globaler Zustand, keine Singletons
- `__all__` in jedem Modul
- Minimale Kommentare: nur das Warum, nie das Was

## Definition of Done

Eine Aufgabe gilt als abgeschlossen, wenn:

- die Architektur eingehalten wurde
- relevante Tests erfolgreich sind
- Dokumentation aktualisiert wurde (falls erforderlich)
- keine unnötigen Dateien geändert wurden
- der Commit thematisch sauber ist
- keine unbegründeten TODOs hinterlassen wurden

## Architekturänderungen

Bei Änderungen an Core, Bootstrap, ServiceRegistry, Plugin-System, SDK oder Event-System vor der Implementierung: Auswirkungen analysieren, betroffene ADRs identifizieren, Alternativen vergleichen, Risiken dokumentieren, Empfehlung begründen.

## Sicherheitsregeln

- Plugin-Code niemals vor erfolgreicher Sicherheitsprüfung ausführen
- PluginSecurityStage darf nicht umgangen werden
- Secrets niemals loggen
- Sichere Standardwerte bevorzugen
- Sicherheitsprüfungen niemals deaktivieren, um Implementierungen zu vereinfachen

## Performance-Regeln

- Verständlicher Code vor Mikrooptimierungen
- Optimierungen nur mit nachvollziehbarer Begründung
- Keine unnötigen Abhängigkeiten
- Bestehende Infrastruktur wiederverwenden
- Speicher-/CPU-intensive Lösungen vermeiden, wenn einfachere existieren

## Architekturverantwortung

Wenn eine Anweisung der bestehenden Architektur widerspricht, technische Schulden erzeugt, ADRs verletzt oder unnötige Komplexität einführt:

- Ausdrücklich darauf hinweisen
- Auswirkungen erklären
- Mindestens eine bessere Alternative vorschlagen

## Versionierung

- Anwendungsversion: `pyproject.toml` → `project.version`
- SDK-Version: `sdk/version.py` → `SDK_VERSION`
- SDK-API-Version: `sdk/version.py` → `SDK_API_VERSION` (unabhängig)
- Semantic Versioning: Major = Breaking, Minor = Additiv, Patch = Bugfix
