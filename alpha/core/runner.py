"""Execute plan steps with circuit breaker and audit logging"""
from __future__ import annotations
import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Any

from .plan import Plan

from .governance import CircuitBreaker, AuditLogger
from .prompt_writer import PromptWriter
from alpha.adapters import ADAPTERS


def snapshot_shortlist(region: str, query_hash: str, shortlist: List[Dict[str, Any]]) -> str:
    """Persist top-k shortlist snapshot for audits; returns file path."""
    topk = int(os.getenv("ALPHA_SNAPSHOT_TOPK", "5"))
    art_root = os.getenv("ALPHA_ARTIFACTS_DIR", "artifacts")
    path = Path(art_root) / "shortlists" / str(region) / f"{query_hash}.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    items = []
    for rank, item in enumerate(shortlist[:topk], 1):
        items.append({
            "rank": rank,
            "tool_id": str(item.get("id") or item.get("tool_id")),
            "score": float(item.get("score", 0.0)),
            "prior": float(item.get("prior", 0.0)),
        })
    rec = {
        "region": region,
        "query_hash": query_hash,
        "generated_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "items": items,
    }
    with path.open("w", encoding="utf-8") as f:
        json.dump(rec, f, ensure_ascii=False)
    return str(path)


def run(plan: Dict, *, execute: bool = False) -> List[Dict]:
    breaker_conf = plan.get("breaker", {})
    trip_count = breaker_conf.get("trip_count", 0)
    breaker = CircuitBreaker(trip_count=trip_count)
    audit = AuditLogger()
    writer = PromptWriter()
    trace: List[Dict] = []
    for idx, step in enumerate(plan.get("steps", [])):
        audit.log({"event": "step.start", "tool_id": step.get("tool_id")})
        if not breaker.allow():
            audit.log({"event": "breaker.tripped"})
            break
        adapter_name = step.get("adapter")
        if adapter_name in ADAPTERS and not execute:
            adapter = ADAPTERS[adapter_name]()
            prompt = adapter.render_prompt(step)
            path = writer.write(idx, prompt)
            trace.append({"tool_id": step.get("tool_id"), "prompt_path": str(path)})
        else:
            trace.append({"tool_id": step.get("tool_id"), "executed": True})
    plan["audit_log"] = str(audit.path)
    return trace


def run_plan(plan: Plan, local_only: bool = True) -> List[Dict]:
    """Execute a Plan dataclass; external steps skipped when local_only."""
    wrapper = {
        "steps": [s.to_dict() for s in plan.steps],
        "breaker": plan.guards.circuit_breakers,
    }
    trace = run(wrapper, execute=not local_only)
    plan.guards.audit = {"log_path": wrapper.get("audit_log")}
    return trace
