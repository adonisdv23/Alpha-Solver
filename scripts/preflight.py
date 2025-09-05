from __future__ import annotations
import csv, json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REG_DIR = ROOT / "registries"
ART_DIR = ROOT / "artifacts"

sys.path.insert(0, str(ROOT))

from alpha.core.ids import slugify_tool_id, validate_tool_id
from scripts.validate_registry import validate_all as validate_registries

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
    ids_reg = []
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
        ids_reg.extend(_extract_ids(obj))
    # Collect ids from any other registries
    for p in REG_DIR.glob("*.*"):
        if p.name in {n for n, _ in FILES}:
            continue
        if p.suffix in (".json", ".yaml", ".yml"):
            try:
                obj = _safe_load_yaml(p) if p.suffix in (".yaml", ".yml") else _safe_load_json(p)
                ids_reg.extend(_extract_ids(obj))
            except Exception:
                pass
    ids_canon = []
    canon = ART_DIR / "tools_canon.csv"
    if canon.exists():
        with canon.open("r", encoding="utf-8") as fh:
            reader = csv.DictReader(fh)
            for row in reader:
                if row.get("id"):
                    ids_canon.append(row["id"])
    def _check(ids_list):
        seen = set()
        for raw in ids_list:
            norm = slugify_tool_id(raw)
            if not (norm.startswith("tool.") or norm.startswith("model.")):
                continue
            validate_tool_id(norm)
            if norm in seen:
                print(json.dumps({"ok": False, "error": f"duplicate id: {norm}"}, ensure_ascii=False))
                return False
            seen.add(norm)
        return True
    if not _check(ids_reg):
        return 1
    if not _check(ids_canon):
        return 1
    validate_registries(REG_DIR, quiet=True)
    print(json.dumps({"ok": True, "registries": counts}, ensure_ascii=False))
    return 0


def _extract_ids(obj) -> list:
    results = []
    if obj is None:
        return results
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k == "id" and isinstance(v, str):
                results.append(v)
            else:
                results.extend(_extract_ids(v))
    elif isinstance(obj, list):
        for item in obj:
            results.extend(_extract_ids(item))
    return results

if __name__ == "__main__":
    sys.exit(main())
