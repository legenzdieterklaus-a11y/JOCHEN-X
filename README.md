# JOCHEN X Foundation

The foundation starts a PySide6 desktop shell and composes configuration, logging, SQLite,
themes, AI provider infrastructure, plugins, security, and observability. It deliberately
contains no chat, agent, browser, memory, document, office, automation, or business features.

## Architecture Reference

**Binding architecture reference:** [`docs/architecture-book-v2.md`](docs/architecture-book-v2.md) (Architecture Book v2.0, frozen).

Future changes must stay consistent with this document, or be introduced deliberately via new book versions (e.g. v2.1 / v3.0) and documented ADRs. See also [`ARCHITECTURE.md`](ARCHITECTURE.md) for a visual overview and [`CLAUDE.md`](CLAUDE.md) for working rules.

## Run

Install Python 3.13+ and PySide6, then run `python main.py` from this directory.
