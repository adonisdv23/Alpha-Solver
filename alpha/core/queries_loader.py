from __future__ import annotations

from pathlib import Path
from typing import List, Set


def _read_lines(p: Path) -> List[str]:
    return p.read_text(encoding="utf-8").splitlines()


def load_queries(path: str | None) -> List[str]:
    if not path:
        return []
    start = Path(path)
    if not start.exists():
        raise FileNotFoundError(f"queries file not found: {start}")
    out: List[str] = []
    seen: Set[Path] = set()

    def visit(fp: Path) -> None:
        if fp in seen:
            return
        seen.add(fp)
        for line in _read_lines(fp):
            s = line.strip()
            if not s or s.startswith("#"):
                continue
            if s.startswith("@file"):
                parts = s.split(maxsplit=1)
                if len(parts) != 2:
                    continue
                inc = (fp.parent / parts[1]).resolve()
                if inc.exists():
                    visit(inc)
                continue
            out.append(s)

    visit(start.resolve())
    return out

