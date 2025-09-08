"""Alpha Solver v91 entrypoints."""

from __future__ import annotations

from typing import Any, Dict, List, Optional

# Core ToT solver
from alpha.reasoning.tot import TreeOfThoughtSolver

# SAFE-OUT v1.1 (state machine)
from alpha.policy.safe_out_sm import SOConfig, SafeOutStateMachine

# Progressive router & agents (v12 groundwork, behind flags)
# __init__.py should re-export ProgressiveRouter and AGENTS_V12 mapping;
# if not, import directly from their modules.
try:
    from alpha.router import ProgressiveRouter, AGENTS_V12  # type: ignore
except Exception:  # fallback if __init__ doesn't export
    from alpha.router.progressive import ProgressiveRouter  # type: ignore
    from alpha.router.agents_v12 import AGENTS_V12  # type: ignore

# Lightweight structured logging helper
from alpha.reasoning.logging import log_safe_out_decision


def _tree_of_thought(
    query: str,
    *,
    # ToT core
    seed: int = 42,
    branching_factor: int = 3,
    score_threshold: float = 0.70,
    max_depth: int = 5,
    timeout_s: int = 10,
    dynamic_prune_margin: float = 0.15,
    # ToT multi-branch (beam-style)
    multi_branch: bool = True,
    max_width: int = 3,
    max_nodes: int = 200,
    # Progressive Router
    enable_progressive_router: bool = True,
    router_escalation: Optional[List[str]] = None,  # ["basic","structured","constrained"] if None
    # Agents v12 groundwork (no-op stubs behind flag)
    enable_agents_v12: bool = False,
    agents_v12_order: Optional[List[str]] = None,  # ["decomposer","checker","calculator"] if None
    # SAFE-OUT policy (low-confidence handling)
    low_conf_threshold: float = 0.60,
    enable_cot_fallback: bool = True,
    max_cot_steps: int = 4,
) -> Dict[str, Any]:
    """
    Solve `query` via deterministic Tree-of-Thought reasoning with optional
    progressive routing and SAFE-OUT low-confidence recovery.

    Returns a policy envelope:
    {
      "final_answer": str,
      "route": "tot"|"cot_fallback"|"best_effort",
      "confidence": float,
      "reason": "ok"|"low_confidence"|"timeout"|"below_threshold",
      "notes": str,
      "tot": {...},                  # ToT result (answer, confidence, path, explored_nodes, etc.)
      "cot": {...} | None,           # present when fallback executed
      "phases": [...],               # SAFE-OUT v1.1 state machine phases
      "diagnostics": {               # enriched, additive
        "tot": {"mode": "multi"|"greedy", "max_width": int, "max_nodes": int},
        "router": {"progressive": bool, "agents_v12": bool}
      }
    }
    """

    # -------- Router setup (all deterministic) --------
    router = None
    if enable_progressive_router:
        escalation = router_escalation or ["basic", "structured", "constrained"]
        router = ProgressiveRouter(escalation)

    agents = None
    if enable_agents_v12:
        order = agents_v12_order or ["decomposer", "checker", "calculator"]
        # Map names → deterministic stub callables (no external calls)
        agents = [AGENTS_V12[name] for name in order if name in AGENTS_V12]

    # -------- ToT solver invocation --------
    solver = TreeOfThoughtSolver(
        seed=seed,
        branching_factor=branching_factor,
        score_threshold=score_threshold,
        max_depth=max_depth,
        timeout_s=timeout_s,
        dynamic_prune_margin=dynamic_prune_margin,
        multi_branch=multi_branch,
        max_width=max_width,
        max_nodes=max_nodes,
        router=router,
        agents_v12=agents,
    )
    tot_result: Dict[str, Any] = solver.solve(query)

    # -------- SAFE-OUT policy (state machine) --------
    cfg = SOConfig(
        low_conf_threshold=low_conf_threshold,
        enable_cot_fallback=enable_cot_fallback,
        max_cot_steps=max_cot_steps,
        seed=seed,
    )
    sm = SafeOutStateMachine(cfg, logger=None)  # logger optional in our impl
    decision: Dict[str, Any] = sm.run(tot_result, query)

    # Structured decision log (for audits) – additive, non-breaking
    log_safe_out_decision(
        route=decision.get("route", "tot"),
        conf=float(tot_result.get("confidence", 0.0)),
        threshold=low_conf_threshold,
        reason=decision.get("reason", "ok"),
    )

    # -------- Diagnostics (additive) --------
    diagnostics: Dict[str, Any] = {
        "tot": {
            "mode": "multi" if multi_branch else "greedy",
            "max_width": max_width,
            "max_nodes": max_nodes,
        },
        "router": {
            "progressive": bool(enable_progressive_router),
            "agents_v12": bool(enable_agents_v12),
        },
    }
    # Ensure we never break existing consumers
    if "diagnostics" not in decision or not isinstance(decision["diagnostics"], dict):
        decision["diagnostics"] = diagnostics
    else:
        decision["diagnostics"].update(diagnostics)

    return decision


__all__ = ["_tree_of_thought"]
