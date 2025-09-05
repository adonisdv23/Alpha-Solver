from __future__ import annotations
import json, sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
SCHEMA_PATH = ROOT / "schemas/registry.schema.json"

from alpha.core.loader import parse_yaml_lite


def _load(p: Path) -> Any:
    text = p.read_text(encoding="utf-8")
    if p.suffix in (".yaml", ".yml"):
        return parse_yaml_lite(text)
    return json.loads(text)

def _valid_entry(obj: Any) -> bool:
    return isinstance(obj, dict) and isinstance(obj.get("id"), str)

def validate_obj(obj: Any) -> bool:
    if _valid_entry(obj):
        return True
    if isinstance(obj, list):
        return all(_valid_entry(i) for i in obj)
    if isinstance(obj, dict):
        for v in obj.values():
            if validate_obj(v):
                return True
    return False

def validate_all(path: Path = ROOT / "registries", quiet: bool = False) -> int:
    errors = []
    for p in path.glob("*.*"):
        if p.suffix not in (".json", ".yaml", ".yml"):
            continue
        try:
            data = _load(p)
        except Exception:
            errors.append(str(p))
            continue
        if not validate_obj(data):
            errors.append(str(p))
    if errors:
        if not quiet:
            print(json.dumps({"ok": False, "errors": errors}, ensure_ascii=False))
        return 1
    if not quiet:
        print(json.dumps({"ok": True}, ensure_ascii=False))
    return 0

if __name__ == "__main__":
    sys.exit(validate_all())
