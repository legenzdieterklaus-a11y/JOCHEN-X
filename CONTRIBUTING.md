# Contributing zu JOCHEN X

Dieses Dokument beschreibt den Arbeitsablauf für menschliche Entwickler und KI-Assistenten. Architekturregeln stehen in [CLAUDE.md](CLAUDE.md), die Systemübersicht in [ARCHITECTURE.md](ARCHITECTURE.md).

---

## Voraussetzungen

- Python ≥ 3.13
- PySide6 ≥ 6.8
- Git

```bash
pip install -e .
python -m pytest -q          # Prüfen, ob alles läuft
```

---

## Entwicklungsworkflow

1. **Aufgabe analysieren** — betroffene Dateien identifizieren, Aufwand schätzen.
2. **Kurzplan erstellen** — bei > 5 betroffenen Dateien: Freigabe einholen.
3. **Feature-Branch erstellen** — vom aktuellen Hauptbranch abzweigen.
4. **Implementieren** — kleine logisch getrennte Schritte, ein Thema pro Commit.
5. **Tests ausführen** — nur betroffene Tests, vollständiger Lauf bei Kernmodulen.
6. **Commit erstellen** — Konventionen einhalten (siehe unten).
7. **Pull Request öffnen** — Beschreibung, Testplan, betroffene ADRs angeben.

---

## Branching

| Branch | Zweck |
|---|---|
| `main` | Stabiler Hauptbranch, nur über PR |
| `feature/<paket>-<name>` | Feature-Entwicklung |
| `fix/<name>` | Bugfixes |
| `docs/<name>` | Reine Dokumentationsänderungen |

Branches werden nach Merge gelöscht.

---

## Commit-Konventionen

Format: `<prefix>(<scope>): <kurze Beschreibung>`

### Präfixe

| Präfix | Verwendung |
|---|---|
| `feat` | Neues Feature |
| `fix` | Bugfix |
| `docs` | Dokumentation |
| `refactor` | Umbau ohne Verhaltensänderung |
| `test` | Tests hinzufügen oder ändern |
| `chore` | Build, Tooling, Konfiguration |

### Regeln

- Ein Commit = ein Thema
- Keine Feature-Vermischung
- Keine unnötigen Dateien mitstageen
- Keine Secrets committen
- Commit-Message muss ohne Kontext verständlich sein

### Beispiele

```
feat(sdk): add PluginResources path traversal guard
fix(bootstrap): resolve config stage ordering on first run
docs(adr): add ADR-011 SDK-Host-Integration
test(core): add EventBus sticky delivery edge cases
refactor(registry): extract validation into separate method
```

---

## Tests

```bash
python -m pytest tests/test_core.py      # Einzelnes Modul
python -m pytest tests/ -q               # Vollständiger Lauf
```

- Nur betroffene Tests ausführen, sofern nicht mehrere Kernmodule geändert wurden.
- Tests brauchen keinen Qt-Event-Loop (außer explizite UI-Tests).
- Neue Funktionalität erfordert Tests.
- Bestehende Tests dürfen nicht ohne Begründung entfernt werden.

---

## ADR-Prozess

Architekturentscheidungen werden als ADR in `docs/adr/` dokumentiert.

### Wann ein ADR nötig ist

- Änderungen an Core, Bootstrap, ServiceRegistry, Event-System, Plugin-System oder SDK.
- Neue Abhängigkeiten oder Schnittstellen zwischen Schichten.
- Entscheidungen, die schwer rückgängig zu machen sind.

### ADR-Format

```markdown
# ADR NNN: Titel

**Status:** Open | Accepted | Resolved by [ADR-XXX]

## Context
## Decision
## Consequences
## Cross-references
```

Nummerierung fortlaufend, aktuell ab ADR-012. Bestehende ADRs: [Verzeichnis](ARCHITECTURE.md#adr-verzeichnis).

---

## Dokumentation

| Dokument | Inhalt |
|---|---|
| `CLAUDE.md` | Arbeitsregeln, Projektstruktur, Stilregeln |
| `ARCHITECTURE.md` | Systemübersicht mit Diagrammen |
| `ROADMAP.md` | Entwicklungspakete und Status |
| `docs/*.md` | Modul-Spezifikationen |
| `docs/adr/*.md` | Architekturentscheidungen |

### Wann Dokumentation aktualisiert werden muss

- Neue Module oder öffentliche APIs → `docs/<modul>.md`
- Architekturentscheidungen → `docs/adr/`
- Geänderter Bootstrap oder Lifecycle → `docs/architecture.md` und `ARCHITECTURE.md`
- Neues Entwicklungspaket → `ROADMAP.md`

---

## Coding Style

- Type Hints auf allen öffentlichen APIs
- Frozen Dataclasses für Value Types
- Protocols für Schicht-Schnittstellen
- `__all__` in jedem Modul
- Kein globaler Zustand, keine Singletons
- Kommentare nur für das Warum, nie für das Was

Vollständige Stilregeln: [CLAUDE.md](CLAUDE.md#stilregeln-für-code)

---

## Pull Requests

### Beschreibung

```markdown
## Zusammenfassung
- Was wurde geändert und warum

## Betroffene ADRs
- ADR-NNN (falls relevant)

## Testplan
- [ ] Relevante Tests ausgeführt
- [ ] Keine bestehenden Tests gebrochen
```

### Checkliste vor dem PR

- [ ] Architektur eingehalten
- [ ] Relevante Tests grün
- [ ] Dokumentation aktualisiert (falls nötig)
- [ ] Keine unnötigen Dateien geändert
- [ ] Commits thematisch sauber
- [ ] Keine unbegründeten TODOs
