from __future__ import annotations

"""Budget simulation engine used by the CLI tests.

The goal is not to be feature complete but to provide a deterministic and fast
estimator that mirrors the service's accounting logic closely enough for
parity tests.  Scenarios are lightweight dictionaries containing pre-counted
prompt and completion token lengths.
"""

from dataclasses import dataclass
from typing import Iterable, Dict, Any, List, Optional, Tuple

from . import pricing

SOFT_RATIO = 0.9


@dataclass
class Caps:
    """Optional budget limits used to compute verdicts."""

    max_cost_usd: Optional[float] = None
    max_tokens: Optional[int] = None
    latency_budget_ms: Optional[float] = None


def _p95(values: List[float]) -> float:
    if not values:
        return 0.0
    values = sorted(values)
    k = int(0.95 * (len(values) - 1))
    return values[k]


def _latency(tokens: int, info: Dict[str, Any]) -> float:
    return info.get("base_latency_ms", 0.0) + tokens * info.get(
        "per_token_latency_ms", 0.0
    )


def _verdict(totals: Dict[str, float], caps: Caps) -> Tuple[str, List[str]]:
    verdict = "ok"
    reasons: List[str] = []

    def check(value: float, cap: Optional[float], kind: str) -> None:
        nonlocal verdict
        if cap is None:
            return
        if value > cap:
            verdict = "block"
            reasons.append(f"{kind} cap")
        elif value > SOFT_RATIO * cap and verdict != "block":
            verdict = "warn"
            reasons.append(f"{kind} nearing cap")

    check(totals.get("cost_usd", 0.0), caps.max_cost_usd, "cost")
    check(totals.get("tokens", 0.0), caps.max_tokens, "tokens")
    check(totals.get("latency_ms", 0.0), caps.latency_budget_ms, "latency")
    return verdict, reasons


def simulate(
    scenarios: Iterable[Dict[str, Any]],
    model_set: str,
    caps: Caps | None = None,
) -> Dict[str, Any]:
    """Simulate token usage, cost and latency for a single model-set."""

    caps = caps or Caps()
    info = pricing.MODEL_SETS[model_set]
    provider, model = info["provider"], info["model"]

    rows: List[Dict[str, Any]] = []
    costs: List[float] = []
    tokens_list: List[int] = []
    latencies: List[float] = []

    for sc in scenarios:
        pt = int(sc.get("prompt_tokens", 0))
        ct = int(sc.get("completion_tokens", 0))
        tokens = pt + ct
        cost = pricing.cost_of_tokens(provider, model, pt, ct)
        latency = _latency(tokens, info)

        sc_totals = {"cost_usd": cost, "tokens": tokens, "latency_ms": latency}
        verdict, _ = _verdict(sc_totals, caps)

        rows.append(
            {
                "id": sc.get("id"),
                "intent": sc.get("intent", ""),
                "model_set": model_set,
                "route": sc.get("route", ""),
                "est_tokens": tokens,
                "est_cost_usd": cost,
                "est_latency_ms": latency,
                "verdict": verdict,
            }
        )
        costs.append(cost)
        tokens_list.append(tokens)
        latencies.append(latency)

    summary = {
        "model_set": model_set,
        "total_cost_usd": sum(costs),
        "total_tokens": sum(tokens_list),
        "p95_latency_ms": _p95(latencies),
    }
    overall = {
        "cost_usd": summary["total_cost_usd"],
        "tokens": summary["total_tokens"],
        "latency_ms": summary["p95_latency_ms"],
    }
    verdict, reasons = _verdict(overall, caps)
    summary["budget_verdict"] = verdict
    summary["reasons"] = reasons

    return {"summary": summary, "scenarios": rows}


def compare(
    before_cfg: Dict[str, Any],
    after_cfg: Dict[str, Any],
    scenarios: Iterable[Dict[str, Any]],
) -> Dict[str, Any]:
    """Run a before/after comparison returning a delta table."""

    def _cfg_to_caps(cfg: Dict[str, Any]) -> Caps:
        return Caps(
            max_cost_usd=cfg.get("max_cost_usd"),
            max_tokens=cfg.get("max_tokens"),
            latency_budget_ms=cfg.get("latency_budget_ms"),
        )

    before = simulate(
        scenarios,
        before_cfg["model_set"],
        caps=_cfg_to_caps(before_cfg),
    )
    after = simulate(
        scenarios,
        after_cfg["model_set"],
        caps=_cfg_to_caps(after_cfg),
    )
    delta = {
        "total_cost_usd": after["summary"]["total_cost_usd"]
        - before["summary"]["total_cost_usd"],
        "total_tokens": after["summary"]["total_tokens"]
        - before["summary"]["total_tokens"],
        "p95_latency_ms": after["summary"]["p95_latency_ms"]
        - before["summary"]["p95_latency_ms"],
    }
    return {"before": before, "after": after, "delta": delta}
