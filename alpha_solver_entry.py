from __future__ import annotations

import importlib.util
from pathlib import Path

from alpha.core.observability import ObservabilityManager
from service.gating.gates import GateConfig, evaluate_gates

ENTRY = Path(__file__).with_name("alpha-solver-v91-python.py")
if not ENTRY.exists():
    raise ImportError(f"Expected entrypoint file not found: {ENTRY}")

_spec = importlib.util.spec_from_file_location("alpha_solver_v91_impl", ENTRY)
if _spec is None or _spec.loader is None:
    raise ImportError("Could not load alpha-solver-v91-python.py via importlib")

_module = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_module)  # type: ignore[attr-defined]

AlphaSolver = _module.AlphaSolver  # type: ignore[attr-defined]


def _tree_of_thought(
    query: str,
    *,
    low_conf_threshold: float = 0.35,
    clarify_conf_threshold: float = 0.55,
    min_budget_tokens: int = 256,
    enable_cot_fallback: bool = True,
    observability: ObservabilityManager | None = None,
    **kwargs,
) -> dict:
    """Execute reasoning pipeline and run deterministic gating.

    Parameters mirror the public solver API while introducing gating knobs that
    are forwarded to :func:`evaluate_gates`.
    """

    obs = observability
    if obs:
        obs.log_event({"event": "query_start", "query": query})
    try:
        result = _module._tree_of_thought(
            query,
            low_conf_threshold=low_conf_threshold,
            enable_cot_fallback=enable_cot_fallback,
            **kwargs,
        )
    except Exception as exc:
        if obs:
            obs.log_event({"event": "query_error", "error": str(exc), "query": query})
        raise
    confidence = float(result.get("confidence", 0.0))
    usage = result.get("usage") or {}
    budget_tokens = int(usage.get("total_tokens", 0))
    policy_flags = result.get("policy_flags", {})
    cfg = GateConfig(
        low_conf_threshold=low_conf_threshold,
        clarify_conf_threshold=clarify_conf_threshold,
        min_budget_tokens=min_budget_tokens,
        enable_cot_fallback=enable_cot_fallback,
    )
    decision, explain = evaluate_gates(confidence, budget_tokens, policy_flags, cfg)
    result["route_explain"] = explain
    result["decision"] = decision
    if obs:
        obs.log_event(
            {
                "event": "query_success",
                "route_explain": explain,
                "decision": decision,
            }
        )
    return result


def get_solver() -> AlphaSolver:
    """Return a new :class:`AlphaSolver` instance.

    This helper mirrors the minimal factory expected by tests and scripts
    while deferring all heavy lifting to the lazily-loaded implementation.
    """

    return AlphaSolver()

__all__ = ["AlphaSolver", "_tree_of_thought", "get_solver"]
