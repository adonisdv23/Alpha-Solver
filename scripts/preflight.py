from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Any, Dict, List

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from alpha.core.ids import slugify_tool_id, validate_tool_id
REG_DIR = ROOT / "registries"
ART_DIR = ROOT / "artifacts"


def _load_tools() -> List[Dict[str, Any]]:
    try:
        raw = json.loads((REG_DIR / "tools.json").read_text(encoding="utf-8"))
    except Exception:
        return []
    if isinstance(raw, dict) and isinstance(raw.get("tools"), list):
        return list(raw["tools"])
    if isinstance(raw, list):
        return list(raw)
    return []


def _norm_id(t: Dict[str, Any]) -> str:
    tid = str(t.get("tool_id") or t.get("id") or "")
    norm = slugify_tool_id(tid)
    validate_tool_id(norm)
    return norm


def _validate(tools: List[Dict[str, Any]]) -> List[str]:
    errors: List[str] = []
    seen: set[str] = set()
    for idx, tool in enumerate(tools, 1):
        tid_raw = tool.get("tool_id") or tool.get("id")
        if not tid_raw:
            errors.append(f"tool {idx} missing tool_id")
            continue
        try:
            norm = _norm_id(tool)
        except Exception:
            errors.append(f"tool {idx} invalid id: {tid_raw}")
            continue
        if norm in seen:
            errors.append(f"duplicate id: {norm}")
        seen.add(norm)
        if "name" not in tool:
            errors.append(f"{norm} missing field: name")
        priors = tool.get("priors", {})
        if not priors:
            priors = {
                "sentiment": tool.get("sentiment_prior"),
                "adoption": tool.get("adoption_prior"),
                "risk": tool.get("risk_penalty"),
                "cost": tool.get("cost_bonus"),
            }
        for name in ("sentiment", "adoption", "risk", "cost"):
            v = priors.get(name)
            if v is None:
                continue
            try:
                f = float(v)
            except Exception:
                errors.append(f"{norm} prior {name} not numeric: {v}")
                continue
            if not (0.0 <= f <= 1.0):
                errors.append(f"{norm} prior {name} out of range: {v}")
    min_tools = int(os.getenv("ALPHA_MIN_TOOLS", "50"))
    if len(tools) < min_tools:
        errors.append(f"requires at least {min_tools} tools, found {len(tools)}")
    return errors


def _basic_registry_checks(tools: List[Dict[str, Any]]) -> None:
    seen: set[str] = set()
    required = ("tool_id", "name", "description")
    for t in tools:
        for k in required:
            if not t.get(k):
                raise SystemExit(f"Missing required field '{k}' in {t}")
        tid = str(t.get("tool_id"))
        if tid in seen:
            raise SystemExit(f"Duplicate tool_id: {tid}")
        seen.add(tid)
        priors = t.get("priors", {})
        for k in ("sentiment", "adoption", "risk", "cost"):
            v = priors.get(k)
            if v is not None:
                f = float(v)
                if not (0.0 <= f <= 1.0):
                    raise SystemExit(f"Prior {k} out of range [0,1]: {v} in {tid}")


def main(argv: List[str] | None = None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--fix-ids", action="store_true", help="rewrite non-normalized ids")
    args = ap.parse_args(argv or [])

    tools = _load_tools()
    errors = _validate(tools)
    if args.fix_ids:
          for tool in tools:
              tid_key = "tool_id" if "tool_id" in tool else "id"
              tool[tid_key] = _norm_id(tool)
          (REG_DIR / "tools.json").write_text(json.dumps({"tools": tools}, ensure_ascii=False, indent=2), encoding="utf-8")
          errors = _validate(tools)

    summary = {"ok": not errors, "count": len(tools), "errors": errors[:20]}
    print(json.dumps(summary, ensure_ascii=False))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
