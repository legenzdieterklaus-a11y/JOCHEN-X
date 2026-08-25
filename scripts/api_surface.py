#!/usr/bin/env python3
"""Static extraction and comparison of public API surfaces.

A surface is derived purely from the source tree via :mod:`ast`; no module is
imported. That keeps the tool runnable without PySide6, without an installed
package and without executing plugin or application code.

Supported packages (``--package``):

``sdk``
    The plugin-facing SDK facade (``sdk/__init__.py``), carrier of the
    ``SDK_API_VERSION`` compatibility promise.

``app.bootstrap``
    The stable bootstrap facade whose export set is fixed as API-01 in the
    Milestone 1.0 Implementation Plan.

Modes:

``--write PATH``   extract and store the surface as deterministic JSON
``--check PATH``   extract and compare against a stored snapshot

Exit codes: 0 identical, 1 difference found, 2 tool failure.

Only the ``surface`` object participates in the comparison; ``meta`` carries
diagnostic values (interpreter version, extractor version) and is ignored.
"""

from __future__ import annotations

import argparse
import ast
import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

__all__ = ["extract_surface", "compare", "main"]

EXTRACTOR_VERSION = "1.1.0"
SCHEMA_VERSION = "1"

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
_SUPPORTED_PACKAGES = ("sdk", "app.bootstrap")
_VERSION_SOURCES = {"sdk": "sdk/version.py"}


@dataclass(frozen=True)
class _Module:
    name: str
    path: Path
    source: str
    tree: ast.Module


def _module_path(dotted: str) -> Path | None:
    """Map a dotted module name to a source file below the project root."""
    parts = dotted.split(".")
    package_init = _PROJECT_ROOT.joinpath(*parts) / "__init__.py"
    if package_init.exists():
        return package_init
    module_file = _PROJECT_ROOT.joinpath(*parts[:-1]) / f"{parts[-1]}.py"
    if module_file.exists():
        return module_file
    return None


def _load(dotted: str) -> _Module:
    path = _module_path(dotted)
    if path is None:
        raise FileNotFoundError(f"module not found in source tree: {dotted}")
    source = path.read_text(encoding="utf-8")
    return _Module(
        name=dotted,
        path=path,
        source=source,
        tree=ast.parse(source, filename=str(path)),
    )


def _segment(module: _Module, node: ast.AST | None) -> str | None:
    """Return the literal source text of *node*.

    Literal source text is used instead of :func:`ast.unparse` because it is
    stable across interpreter versions; unparse output is not guaranteed to be.
    """
    if node is None:
        return None
    text = ast.get_source_segment(module.source, node)
    if text is not None:
        return " ".join(text.split())
    try:
        return " ".join(ast.unparse(node).split())
    except Exception:  # pragma: no cover - defensive
        return "<unrepresentable>"


def _dunder_all(module: _Module) -> list[str]:
    for node in module.tree.body:
        if not isinstance(node, ast.Assign):
            continue
        targets = [t.id for t in node.targets if isinstance(t, ast.Name)]
        if "__all__" not in targets:
            continue
        if isinstance(node.value, (ast.List, ast.Tuple)):
            return [
                element.value
                for element in node.value.elts
                if isinstance(element, ast.Constant) and isinstance(element.value, str)
            ]
    return []


def _import_origins(module: _Module, package: str) -> dict[str, str]:
    """Map re-exported name -> absolute dotted module that defines it."""
    origins: dict[str, str] = {}
    for node in ast.walk(module.tree):
        if not isinstance(node, ast.ImportFrom):
            continue
        if node.level:  # relative import inside the package
            base = package.rsplit(".", node.level - 1)[0] if node.level > 1 else package
            origin = f"{base}.{node.module}" if node.module else base
        elif node.module:
            origin = node.module
        else:  # pragma: no cover - defensive
            continue
        for alias in node.names:
            origins[alias.asname or alias.name] = origin
    return origins


def _signature(module: _Module, node: ast.FunctionDef | ast.AsyncFunctionDef) -> str:
    args = node.args
    parts: list[str] = []

    def render(arg: ast.arg, default: ast.expr | None) -> str:
        rendered = arg.arg
        annotation = _segment(module, arg.annotation)
        if annotation:
            rendered += f": {annotation}"
        if default is not None:
            rendered += f" = {_segment(module, default)}"
        return rendered

    positional = list(args.posonlyargs) + list(args.args)
    defaults: list[ast.expr | None] = [None] * (
        len(positional) - len(args.defaults)
    ) + list(args.defaults)
    for index, arg in enumerate(positional):
        parts.append(render(arg, defaults[index]))
        if args.posonlyargs and index == len(args.posonlyargs) - 1:
            parts.append("/")

    if args.vararg is not None:
        parts.append("*" + render(args.vararg, None))
    elif args.kwonlyargs:
        parts.append("*")

    for arg, default in zip(args.kwonlyargs, args.kw_defaults):
        parts.append(render(arg, default))

    if args.kwarg is not None:
        parts.append("**" + render(args.kwarg, None))

    returns = _segment(module, node.returns)
    suffix = f" -> {returns}" if returns else ""
    prefix = "async " if isinstance(node, ast.AsyncFunctionDef) else ""
    return f"{prefix}({', '.join(parts)}){suffix}"


def _class_entry(module: _Module, node: ast.ClassDef) -> dict[str, Any]:
    members: dict[str, str] = {}
    attributes: dict[str, str] = {}
    for child in node.body:
        if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef)):
            if child.name.startswith("_") and not child.name.startswith("__"):
                continue
            decorators = sorted(
                filter(None, (_segment(module, d) for d in child.decorator_list))
            )
            entry = _signature(module, child)
            if decorators:
                entry = f"[{', '.join(decorators)}] {entry}"
            members[child.name] = entry
        elif isinstance(child, ast.AnnAssign) and isinstance(child.target, ast.Name):
            name = child.target.id
            if name.startswith("_"):
                continue
            attributes[name] = _segment(module, child.annotation) or ""
    return {
        "kind": "class",
        "module": module.name,
        "bases": [b for b in (_segment(module, base) for base in node.bases) if b],
        "decorators": sorted(
            filter(None, (_segment(module, d) for d in node.decorator_list))
        ),
        "methods": dict(sorted(members.items())),
        "attributes": dict(sorted(attributes.items())),
    }


def _module_symbols(module: _Module) -> dict[str, dict[str, Any]]:
    symbols: dict[str, dict[str, Any]] = {}
    for node in module.tree.body:
        if isinstance(node, ast.ClassDef):
            symbols[node.name] = _class_entry(module, node)
        elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            symbols[node.name] = {
                "kind": "function",
                "module": module.name,
                "signature": _signature(module, node),
                "decorators": sorted(
                    filter(None, (_segment(module, d) for d in node.decorator_list))
                ),
            }
        elif isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name):
            symbols[node.target.id] = {
                "kind": "constant",
                "module": module.name,
                "annotation": _segment(module, node.annotation),
                "value": _segment(module, node.value),
            }
        elif isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and not target.id.startswith("_"):
                    symbols[target.id] = {
                        "kind": "constant",
                        "module": module.name,
                        "annotation": None,
                        "value": _segment(module, node.value),
                    }
    return symbols


def _declared_versions(package: str) -> dict[str, str | None]:
    source = _VERSION_SOURCES.get(package)
    if source is None:
        return {}
    module = _load(source[:-3].replace("/", "."))
    values: dict[str, str | None] = {
        "SDK_NAME": None,
        "SDK_VERSION": None,
        "SDK_API_VERSION": None,
    }
    for node in module.tree.body:
        target_name: str | None = None
        value: ast.expr | None = None
        if isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name):
            target_name, value = node.target.id, node.value
        elif isinstance(node, ast.Assign) and len(node.targets) == 1:
            target = node.targets[0]
            if isinstance(target, ast.Name):
                target_name, value = target.id, node.value
        if target_name in values and isinstance(value, ast.Constant):
            values[target_name] = str(value.value)
    return values


def extract_surface(package: str = "sdk") -> dict[str, Any]:
    """Build the deterministic public-surface description of *package*."""
    entry = _load(package)
    exported = _dunder_all(entry)
    origins = _import_origins(entry, package)

    cache: dict[str, _Module] = {}
    for origin in sorted(set(origins.values())):
        try:
            cache[origin] = _load(origin)
        except (FileNotFoundError, OSError, SyntaxError):
            continue  # external or unparsable origin: symbol stays unresolved

    module_symbols = {name: _module_symbols(mod) for name, mod in cache.items()}
    own_symbols = _module_symbols(entry)

    symbols: dict[str, Any] = {}
    unresolved: list[str] = []
    for name in exported:
        origin = origins.get(name)
        found = None
        if origin and origin in module_symbols:
            found = module_symbols[origin].get(name)
        if found is None:
            found = own_symbols.get(name)
        if found is None:
            unresolved.append(name)
            symbols[name] = {"kind": "unresolved", "module": origin}
        else:
            symbols[name] = found

    return {
        "schema_version": SCHEMA_VERSION,
        "package": package,
        "entry_point": str(entry.path.relative_to(_PROJECT_ROOT)).replace("\\", "/"),
        "declared_versions": _declared_versions(package),
        "exported_count": len(exported),
        "exported": sorted(exported),
        "unresolved": sorted(unresolved),
        "symbols": dict(sorted(symbols.items())),
    }


def _payload(package: str) -> dict[str, Any]:
    return {
        "meta": {
            "extractor_version": EXTRACTOR_VERSION,
            "python": ".".join(str(p) for p in sys.version_info[:3]),
            "note": "meta is diagnostic only and excluded from --check comparison",
        },
        "surface": extract_surface(package),
    }


def _dump(payload: dict[str, Any]) -> str:
    return json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False) + "\n"


def compare(current: dict[str, Any], stored: dict[str, Any]) -> list[str]:
    """Return a list of human-readable differences (empty list = identical)."""
    differences: list[str] = []
    current_symbols = current.get("symbols", {})
    stored_symbols = stored.get("symbols", {})

    for name in sorted(set(stored_symbols) - set(current_symbols)):
        differences.append(f"REMOVED  symbol {name}")
    for name in sorted(set(current_symbols) - set(stored_symbols)):
        differences.append(f"ADDED    symbol {name}")
    for name in sorted(set(current_symbols) & set(stored_symbols)):
        if current_symbols[name] != stored_symbols[name]:
            differences.append(f"CHANGED  symbol {name}")

    for field in ("package", "declared_versions", "entry_point", "schema_version"):
        if current.get(field) != stored.get(field):
            differences.append(
                f"CHANGED  {field}: {stored.get(field)!r} -> {current.get(field)!r}"
            )
    return differences


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--write", metavar="PATH", help="write snapshot to PATH")
    group.add_argument("--check", metavar="PATH", help="compare against PATH")
    parser.add_argument(
        "--package",
        default="sdk",
        choices=_SUPPORTED_PACKAGES,
        help="package facade to extract (default: sdk)",
    )
    parser.add_argument(
        "--print", action="store_true", help="print the surface to stdout"
    )
    args = parser.parse_args(argv)

    try:
        payload = _payload(args.package)
    except (SyntaxError, FileNotFoundError, OSError) as error:
        print(f"api_surface: cannot read source: {error}", file=sys.stderr)
        return 2

    if args.print:
        sys.stdout.write(_dump(payload))

    if args.write:
        target = Path(args.write)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(_dump(payload), encoding="utf-8")
        surface = payload["surface"]
        print(
            f"api_surface[{args.package}]: wrote {target} "
            f"({surface['exported_count']} exported symbols, "
            f"{len(surface['unresolved'])} unresolved)"
        )
        return 0

    stored_path = Path(args.check)
    if not stored_path.exists():
        print(f"api_surface: snapshot missing: {stored_path}", file=sys.stderr)
        return 2
    try:
        stored = json.loads(stored_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as error:
        print(f"api_surface: snapshot unreadable: {error}", file=sys.stderr)
        return 2

    differences = compare(payload["surface"], stored.get("surface", {}))
    if differences:
        print(
            f"api_surface[{args.package}]: {len(differences)} difference(s) "
            f"against {stored_path}"
        )
        for line in differences:
            print(f"  {line}")
        return 1
    print(f"api_surface[{args.package}]: identical to {stored_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
