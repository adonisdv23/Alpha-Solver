"""Replay a saved _tree_of_thought envelope deterministically."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Iterable


def _load(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as fh:
        return json.load(fh)


def _render(env: dict) -> str:
    lines: list[str] = []
    lines.append(f"route: {env.get('route', '')}")
    lines.append(f"confidence: {float(env.get('confidence', 0.0)):.3f}")
    path = env.get("diagnostics", {}).get("tot", {}).get("path") or []
    if path:
        lines.append("path: " + " -> ".join(path))
    phases = env.get("phases")
    if isinstance(phases, Iterable):
        lines.append("phases: " + "->".join(str(p) for p in phases))
    return "\n".join(lines)


def main() -> None:  # pragma: no cover - thin CLI
    ap = argparse.ArgumentParser(description="Replay a _tree_of_thought envelope")
    ap.add_argument("envelope", help="Path to envelope JSON")
    args = ap.parse_args()
    env = _load(Path(args.envelope))
    print(_render(env))


if __name__ == "__main__":  # pragma: no cover
    main()
