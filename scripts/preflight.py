from __future__ import annotations
import json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REG_DIR = ROOT / "registries"

def _safe_load_json(p: Path):
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except Exception:
        return None

def _safe_load_yaml(p: Path):
    # Try PyYAML; otherwise just return raw text in a dict so counting works.
    try:
        import yaml  # type: ignore
        return yaml.safe_load(p.read_text(encoding="utf-8"))
    except Exception:
        return {"_raw": p.read_text(encoding="utf-8")}

def _count(obj) -> int:
    if obj is None: return 0
    if isinstance(obj, list): return len(obj)
    if isinstance(obj, dict): return len(obj)
    return 1

def _count_tools_blob(obj) -> int:
    # Accept either {"tools":[...]} or a bare list [...]
    if isinstance(obj, list): return len(obj)
    if isinstance(obj, dict):
        val = obj.get("tools", [])
        return len(val) if isinstance(val, list) else 0
    return 0

FILES = [
    ("sections.yaml", _safe_load_yaml),
    ("questions.json", _safe_load_json),
    ("risks.json", _safe_load_json),
    ("templates.playbooks.yaml", _safe_load_yaml),
    ("policy.routes.yaml", _safe_load_yaml),
    ("tools.json", _safe_load_json),
    ("secrets_vault.json", _safe_load_json),
    ("budget_controls.yaml", _safe_load_yaml),
    ("audit_trail.json", _safe_load_json),
    ("sla_contracts.yaml", _safe_load_yaml),
    ("circuit_breakers.json", _safe_load_json),
    ("data_classification.yaml", _safe_load_yaml),
    ("clusters.yaml", _safe_load_yaml),
    ("regions.yaml", _safe_load_yaml),
]

def main() -> int:
    counts = {}
    for name, loader in FILES:
        p = REG_DIR / name
        if not p.exists():
            counts[name] = 0
            continue
        obj = loader(p)
        if name == "tools.json":
            counts[name] = _count_tools_blob(obj)
        else:
            counts[name] = _count(obj)
    print(json.dumps({"ok": True, "registries": counts}, ensure_ascii=False))
    return 0

if __name__ == "__main__":
    sys.exit(main())
