from __future__ import annotations

from pathlib import Path
from typing import Dict, Any

try:  # pragma: no cover - optional dependency
    import yaml  # type: ignore
except ModuleNotFoundError:  # pragma: no cover
    yaml = None


def _parse_simple_nested(text: str) -> Dict[str, Any]:
    data: Dict[str, Any] = {}
    stack: list[tuple[int, Dict[str, Any]]] = [(0, data)]
    for raw in text.splitlines():
        if "#" in raw:
            raw = raw.split("#", 1)[0]
        if not raw.strip():
            continue
        indent = len(raw) - len(raw.lstrip(" "))
        line = raw.strip()
        if line.endswith(":"):
            key = line[:-1]
            new: Dict[str, Any] = {}
            while stack and indent <= stack[-1][0]:
                stack.pop()
            stack[-1][1][key] = new
            stack.append((indent + 2, new))
        elif ":" in line:
            key, val = line.split(":", 1)
            val = val.strip().strip('"\'')
            try:
                parsed: Any = int(val)
            except ValueError:
                try:
                    parsed = float(val)
                except ValueError:
                    parsed = val
            stack[-1][1][key.strip()] = parsed
    return data


def load_budgets(path: Path | str = Path("config/budget_controls.yaml")) -> Dict[str, Any]:
    """Load budget configuration from YAML."""
    path = Path(path)
    try:
        text = path.read_text(encoding="utf-8")
        if yaml is not None:
            return yaml.safe_load(text) or {}
        return _parse_simple_nested(text)
    except Exception:
        return {}
