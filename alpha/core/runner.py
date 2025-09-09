"""Execute plan steps with governance checks"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

from .plan import Plan, PlanStep, bounded_retry
from .governance import (
    AuditLogger,
    BudgetCapGate,
    CircuitBreaker,
    GovernanceError,
    PolicyDryRun,
)
from .prompt_writer import PromptWriter
from alpha.adapters import ADAPTERS
from .session_trace import write_session_trace
from .determinism import apply_seed
from alpha.policy.governance import GovernanceEngine
from alpha.reasoning.cot_self_validate import validate_answer
from alpha.core.config import ValidationConfig

# simple in-memory telemetry log used in tests
TELEMETRY_EVENTS: List[Dict[str, Any]] = []


def run_reasoning(
    query: str,
    *,
    strategy: str = "CoT",
    seed: int = 0,
    config: ValidationConfig | None = None,
    cot_steps: List[str] | None = None,
    answer: str | None = None,
    confidence: float = 0.0,
) -> Dict[str, Any]:
    """Run a reasoning strategy optionally applying self-validation."""

    from alpha.reasoning.cot import run_cot

    if cot_steps is None or answer is None:
        result = run_cot(query, seed=seed, max_steps=3)
    else:
        result = {"steps": cot_steps, "answer": answer, "confidence": confidence}
    cfg = config or ValidationConfig()
    if strategy == "CoT" and cfg.enabled:
        ok, reasons = validate_answer(result.get("steps", []), result.get("answer", ""))
        result["validation"] = {"ok": ok, "reasons": reasons}
        result["post_validate_confidence"] = result.get("confidence", 0.0)
        if not ok and result.get("confidence", 0.0) < cfg.min_conf:
            from alpha.reasoning.cot_self_validate import _eval_simple_arithmetic

            expected = _eval_simple_arithmetic("\n".join(result.get("steps", [])))
            if expected is not None:
                corrected = str(int(expected)) if float(expected).is_integer() else str(expected)
                if corrected != result.get("answer"):
                    result["answer"] = corrected
                    result["post_validate_confidence"] = cfg.min_conf
                    result["validation"] = {"ok": True, "reasons": reasons}
                    TELEMETRY_EVENTS.append({"event": "cot_validate_correction"})
    return result


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


class Runner:
    def __init__(self) -> None:
        self.budget_gate = BudgetCapGate(
            max_steps=int(os.getenv("ALPHA_BUDGET_STEPS", "100"))
        )
        self.circuit_breaker = CircuitBreaker(
            max_errors=int(os.getenv("ALPHA_MAX_ERRORS", "5"))
        )
        self.audit_logger = AuditLogger("logs/governance_audit.jsonl")
        self.dryrun = PolicyDryRun(
            enabled=os.getenv("ALPHA_POLICY_DRYRUN", "0") == "1"
        )
        self.writer = PromptWriter()

    def solve(self, plan: Dict, *, execute: bool = False) -> List[Dict]:
        trace: List[Dict] = []
        self.audit_logger.log_event("query", {"steps": len(plan.get("steps", []))})
        for idx, step in enumerate(plan.get("steps", []), 1):
            try:
                self.budget_gate.check(idx)
            except GovernanceError as err:
                self.audit_logger.log_event("budget.exceeded", {"step": idx})
                self.dryrun.handle(err)
                if not self.dryrun.enabled:
                    break
            self.audit_logger.log_event("step.start", {"tool_id": step.get("tool_id")})
            try:
                adapter_name = step.get("adapter")
                if adapter_name in ADAPTERS and not execute:
                    adapter = ADAPTERS[adapter_name]()
                    prompt = adapter.render_prompt(step)
                    path = self.writer.write(idx - 1, prompt)
                    trace.append({"tool_id": step.get("tool_id"), "prompt_path": str(path)})
                else:
                    trace.append({"tool_id": step.get("tool_id"), "executed": True})
            except Exception as e:
                try:
                    self.circuit_breaker.record_error()
                except GovernanceError as err:
                    self.audit_logger.log_event("breaker.tripped", {})
                    self.dryrun.handle(err)
                    if not self.dryrun.enabled:
                        break
                if not self.dryrun.enabled:
                    raise e
        return trace


def run(plan: Dict, *, execute: bool = False) -> List[Dict]:
    runner = Runner()
    trace = runner.solve(plan, execute=execute)
    plan["audit_log"] = str(runner.audit_logger.path)
    return trace


def run_plan(plan: Plan, local_only: bool = True) -> List[Dict]:
    """Execute a Plan dataclass; external steps skipped when local_only."""
    wrapper = {
        "steps": [s.to_dict() for s in plan.steps],
        "breaker": plan.guards.circuit_breakers,
    }
    shortlist_paths: List[str] = []
    sl = plan.artifacts.get("shortlist_snapshot")
    if isinstance(sl, str):
        shortlist_paths.append(sl)
    env_path = ""
    try:
        env_path = subprocess.check_output(
            [sys.executable, "-m", "scripts.env_snapshot"], text=True
        ).strip()
    except Exception:
        env_path = ""
    deterministic = os.getenv("ALPHA_DETERMINISM") == "1"
    if deterministic:
        seed = plan.run.get("seed", 0)
        plan.run["seed"] = apply_seed(int(seed))
        now = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
        started = now
    else:
        started = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    try:
        trace = run(wrapper, execute=not local_only)
        return trace
    finally:
        ended = now if deterministic else datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
        write_session_trace(
            {
                "queries_source": plan.run.get("queries_source"),
                "regions": [plan.run.get("region")] if plan.run.get("region") else [],
                "seed": plan.run.get("seed"),
                "shortlist_paths": shortlist_paths,
                "env_snapshot_path": env_path,
                "started_at": started,
                "ended_at": ended,
            }
        )
        plan.guards.audit = {"log_path": wrapper.get("audit_log")}


# ---------------------------------------------------------------------------
# Plan spine / CLI helpers


def _build_plan(query: str, region: str) -> Plan:
    """Construct a minimal Plan instance for the given query/region."""
    step = PlanStep(
        tool_id="noop",
        step_id="step-1",
        description=f"demo step for {query}",
        contract={"ok": True},
    )
    return Plan(
        run_id=uuid.uuid4().hex,
        query=query,
        region=region,
        steps=[step],
        retries=1,
    )


def _execute_step(step: PlanStep) -> Dict[str, Any]:
    """Demo executor used for CLI runs."""
    # If description hints failure, return failing result for retry tests.
    if "fail" in (step.description or "").lower():
        return {"ok": False}
    return {"ok": True}


def execute_plan(plan: Plan, policy: GovernanceEngine | None = None) -> None:
    """Execute steps with bounded retry and populate results."""
    for s in plan.steps:
        if policy:
            dec = policy.decide(
                query=plan.query,
                region=plan.region,
                tool_id=s.tool_id,
                family=s.enrichment.get("family", ""),
                tags=s.enrichment.get("tags", []),
            )
            if dec.decision == "block" and not policy.dry_run:
                raise RuntimeError(f"policy blocked: {dec.reason}")
        bounded_retry(s, lambda: _execute_step(s), max_retries=plan.retries)
        if policy:
            policy.record_step_result(s.status == "ok")


def _write_last_plan(plan: Plan) -> Path:
    art_root = Path(os.getenv("ALPHA_ARTIFACTS_DIR", "artifacts"))
    art_root.mkdir(parents=True, exist_ok=True)
    path = art_root / "last_plan.json"
    with path.open("w", encoding="utf-8") as f:
        json.dump(plan.to_json(), f, ensure_ascii=False, sort_keys=True)
    return path


def run_cli(
    *,
    queries: List[str],
    regions: List[str],
    seed: int = 0,
    topk: int = 5,
    mode: str = "execute",
    policy_dry_run: bool = False,
    budget_max_steps: int = 0,
    budget_max_seconds: float = 0.0,
    breaker_max_fails: int = 0,
    data_policy: str | None = None,
) -> int:
    """Minimal CLI helper used by tests and the alpha CLI."""
    _ = seed, topk, data_policy  # presently unused, kept for API completeness
    policy = GovernanceEngine(
        max_steps=budget_max_steps,
        max_seconds=budget_max_seconds,
        breaker_max_fails=breaker_max_fails,
        dry_run=policy_dry_run,
    )
    for region in regions:
        for query in queries:
            plan = _build_plan(query, region)
            if mode != "plan-only":
                if mode in ("execute", "explain"):
                    execute_plan(plan, policy)
                if mode == "explain":
                    print(plan.human_summary())
                    for s in plan.steps:
                        print(f"{s.step_id}: {s.description}")
            _write_last_plan(plan)
    return 0


def main(argv: List[str] | None = None) -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--query", default="")
    parser.add_argument("--region", default="US")
    parser.add_argument("--plan-only", action="store_true")
    parser.add_argument("--explain", action="store_true")
    parser.add_argument("--execute", action="store_true")
    args = parser.parse_args(argv)

    # default behaviour is execute unless plan-only or explain is set
    do_execute = args.execute or (not args.plan_only and not args.explain)

    plan = _build_plan(args.query, args.region)

    if args.plan_only:
        _write_last_plan(plan)
        return

    if args.explain:
        _write_last_plan(plan)
        print(plan.human_summary())
        for s in plan.steps:
            print(f"{s.step_id}: {s.description}")
        if not do_execute:
            return

    if do_execute:
        execute_plan(plan)
        _write_last_plan(plan)


if __name__ == "__main__":  # pragma: no cover - CLI entry
    main()
