from __future__ import annotations
import csv, json, sys, os
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REG_DIR = ROOT / "registries"
ART_DIR = ROOT / "artifacts"

sys.path.insert(0, str(ROOT))

from alpha.core.ids import slugify_tool_id, validate_tool_id
from scripts.validate_registry import validate_all as validate_registries
from alpha.core import freshness

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
    ids_set = {slugify_tool_id(x) for x in ids_reg}
    priors_path = os.getenv("ALPHA_RECENCY_PRIORS_PATH")
    if priors_path:
        loaded = freshness.load_dated_priors(priors_path)
        try:
            raw_obj = json.loads(Path(priors_path).read_text(encoding="utf-8"))
        except Exception:
            raise SystemExit(f"[preflight] cannot read recency priors: {priors_path}")
        if isinstance(raw_obj, dict):
            raw_ids = {k for k in raw_obj.keys() if isinstance(k, str) and not k.startswith("_")}
        else:
            raw_ids = {r.get("tool_id") for r in raw_obj if isinstance(r, dict) and r.get("tool_id")}
        bad_dates = sorted(raw_ids - set(loaded.keys()))
        missing = sorted(t for t in loaded.keys() if slugify_tool_id(t) not in ids_set)
        if bad_dates or missing:
            parts = []
            if bad_dates:
                parts.append("bad dates for: " + ", ".join(bad_dates))
            if missing:
                parts.append("unknown tool_ids: " + ", ".join(missing))
            raise SystemExit("[preflight] recency priors invalid: " + "; ".join(parts))
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

import json
from pathlib import Path
from typing import Any, Dict
try:
    import jsonschema  # optional
except Exception:
    jsonschema = None

def _basic_registry_checks(tools: list[Dict[str,Any]]) -> None:
    seen = set()
    required = ("tool_id","name","description")
    for t in tools:
        for k in required:
            if not t.get(k):
                raise SystemExit(f"[preflight] Missing required field '{k}' in {t}")
        tid = t["tool_id"]
        if tid in seen:
            raise SystemExit(f"[preflight] Duplicate tool_id: {tid}")
        seen.add(tid)
        for k in ("sentiment","adoption","risk","cost"):
            v = t.get("priors",{}).get(k)
            if v is not None and not (0.0 <= float(v) <= 1.0):
                raise SystemExit(f"[preflight] Prior {k} out of range [0,1]: {v} in {tid}")

def validate_registry(path: str) -> None:
    data = [json.loads(line) for line in Path(path).read_text(encoding="utf-8").splitlines()]
    _basic_registry_checks(data)
    schema_path = Path("schemas/registry_tool.schema.json")
    if jsonschema and schema_path.exists():
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
        for obj in data:
            jsonschema.validate(obj, schema)
    print(f"[preflight] OK. tools={len(data)}")

if __name__ == "__main__":
    validate_registry("registries/registry_seed_v0_7_0.jsonl")
