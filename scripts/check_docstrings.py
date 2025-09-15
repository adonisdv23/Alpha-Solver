#!/usr/bin/env python3
"""Check docstring coverage for public API modules.

Modules are taken from ``[tool.docs]`` in ``pyproject.toml``. Only symbols
exported via ``__all__`` are considered public. Modules without ``__all__`` are
ignored.  The script reports the overall coverage and fails if below the
specified threshold.
"""
from __future__ import annotations

import argparse
import ast
import sys
from pathlib import Path

try:  # Python 3.11+
    import tomllib
except Exception:  # pragma: no cover
    import tomli as tomllib  # type: ignore


def load_modules(pyproject: Path) -> list[str]:
    data = tomllib.loads(pyproject.read_text())
    return data.get("tool", {}).get("docs", {}).get("modules", [])


def iter_public_defs(path: Path):
    tree = ast.parse(path.read_text())
    module_all = None
    for node in tree.body:
        if isinstance(node, ast.Assign):
            for tgt in node.targets:
                if isinstance(tgt, ast.Name) and tgt.id == "__all__":
                    try:
                        module_all = {elt.s for elt in node.value.elts}
                    except Exception:  # pragma: no cover - malformed __all__
                        module_all = None
    if module_all is None:
        return
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            name = node.name
            if name.startswith("_"):
                continue
            if module_all is not None and name not in module_all:
                continue
            yield name, ast.get_docstring(node)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--fail-under", type=float, default=90.0)
    args = ap.parse_args(argv)

    modules = load_modules(Path("pyproject.toml"))
    total = covered = 0
    for mod in modules:
        path = Path(mod.replace(".", "/") + ".py")
        if not path.exists():
            continue
        for name, doc in iter_public_defs(path) or []:
            total += 1
            if doc:
                covered += 1
    percent = (covered / total * 100.0) if total else 100.0
    print(f"docstring coverage: {percent:.1f}% ({covered}/{total})")
    if percent < args.fail_under:
        print(f"coverage below threshold {args.fail_under}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
