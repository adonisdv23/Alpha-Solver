from __future__ import annotations

"""Simple scenario runner with record/replay support."""

from dataclasses import dataclass
from pathlib import Path
from time import perf_counter
from typing import Any, Dict, Iterable, List, Mapping

import yaml

from .rubric import Rubric


# ---------------------------------------------------------------------------
# Loading
# ---------------------------------------------------------------------------

def load_pack(path: str = "scenarios/pack.yaml") -> List[Dict[str, Any]]:
    """Load a scenario pack from ``path``.

    Parameters
    ----------
    path:
        Path to the YAML file containing a top-level ``scenarios`` list.
    """
    data: Dict[str, Any] = yaml.safe_load(Path(path).read_text()) or {}
    scenarios = data.get("scenarios", [])
    return list(scenarios)


# ---------------------------------------------------------------------------
# Step / Scenario execution
# ---------------------------------------------------------------------------

def _build_payload(step: Mapping[str, Any]) -> Dict[str, Any]:
    """Create adapter payload from step data."""
    payload = dict(step.get("input", {}))
    action = step.get("action")
    tool = step.get("tool")
    if tool == "gsheets":
        payload["op"] = action
    else:
        payload["action"] = action
    return payload


def run_step(
    step: Mapping[str, Any],
    *,
    adapters: Mapping[str, Any],
    rubric: Rubric,
) -> Dict[str, Any]:
    """Execute a single step via an adapter and judge the result."""
    tool = step.get("tool")
    adapter = adapters[tool]
    payload = _build_payload(step)
    start = perf_counter()
    res = adapter.run(payload)
    latency_ms = float(res.get("meta", {}).get("latency_ms", (perf_counter() - start) * 1000))
    value = res.get("value")
    verdict, reason = rubric.judge(step.get("expect", {}), value)
    route_explain = {
        "decision": "run",
        "adapter": tool,
        "latency_ms": latency_ms,
    }
    route_explain.update(rubric.to_route_explain(verdict, reason))
    return {"ok": verdict, "value": value, "route_explain": route_explain}


def run_scenario(
    scn: Mapping[str, Any],
    *,
    adapters: Mapping[str, Any],
    rubric: Rubric,
) -> Dict[str, Any]:
    """Execute all steps of a scenario."""
    details: List[Dict[str, Any]] = []
    for step in scn.get("steps", []):
        res = run_step(step, adapters=adapters, rubric=rubric)
        details.append({**step, **res})
    passed_steps = sum(1 for d in details if d["ok"])
    total_steps = len(details)
    route_explain = {"steps": [d["route_explain"] for d in details]}
    return {
        "id": scn.get("id"),
        "passed": passed_steps == total_steps,
        "passed_steps": passed_steps,
        "total_steps": total_steps,
        "route_explain": route_explain,
        "details": details,
    }


def run_all(
    scenarios: Iterable[Mapping[str, Any]],
    *,
    adapters: Mapping[str, Any],
    rubric: Rubric,
) -> Dict[str, Any]:
    """Run all scenarios in the iterable."""
    results = [run_scenario(s, adapters=adapters, rubric=rubric) for s in scenarios]
    total = len(results)
    passed = sum(1 for r in results if r["passed"])
    pass_rate = passed / total if total else 0.0
    return {"summary": {"total": total, "passed": passed, "pass_rate": pass_rate}, "results": results}


# ---------------------------------------------------------------------------
# Replay
# ---------------------------------------------------------------------------

def replay(log_events: List[Mapping[str, Any]], *, rubric: Rubric) -> Dict[str, Any]:
    """Re-judge previously recorded events.

    Parameters
    ----------
    log_events:
        Each event must contain at least ``expect`` and ``value`` fields.
    """
    events: List[Dict[str, Any]] = []
    for ev in log_events:
        verdict, reason = rubric.judge(ev.get("expect", {}), ev.get("value"))
        event = {**ev, "ok": verdict}
        event["route_explain"] = rubric.to_route_explain(verdict, reason)
        events.append(event)
    passed = sum(1 for e in events if e["ok"])
    return {"summary": {"total": len(events), "passed": passed}, "events": events}

