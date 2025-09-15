"""Check docstring coverage and basic style for public APIs."""

from __future__ import annotations

import argparse
import ast
import sys
from pathlib import Path
from typing import Iterable, List, Tuple


def _public_defs(tree: ast.Module) -> List[ast.AST]:
    return [
        node
        for node in tree.body
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef))
        and not node.name.startswith("_")
    ]


def scan(paths: Iterable[Path]) -> Tuple[int, int, List[Tuple[Path, int, str]]]:
    total = 0
    documented = 0
    issues: List[Tuple[Path, int, str]] = []
    for path in paths:
        files = [path] if path.is_file() else list(path.rglob("*.py"))
        for file in files:
            if "tests" in file.parts:
                continue
            tree = ast.parse(file.read_text(encoding="utf-8"), filename=str(file))
            for node in _public_defs(tree):
                total += 1
                doc = ast.get_docstring(node)
                if doc:
                    documented += 1
                    lowered = doc.lower()
                    if "todo" in lowered or "fixme" in lowered:
                        issues.append((file, node.lineno, f"{node.name} has placeholder docstring"))
                else:
                    issues.append((file, node.lineno, f"{node.name} missing docstring"))
    return total, documented, issues


def main(argv: List[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("paths", nargs="*", default=[Path("service")], type=Path)
    parser.add_argument("--fail-under", type=int, default=0)
    args = parser.parse_args(argv)

    total, documented, issues = scan(args.paths)
    coverage = 100.0 * documented / total if total else 100.0
    print(f"Docstring coverage: {coverage:.1f}% ({documented}/{total})")
    for file, lineno, msg in issues:
        print(f"{file}:{lineno}: {msg}")
    if coverage < args.fail_under or issues:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

