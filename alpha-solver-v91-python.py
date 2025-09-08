"""Alpha Solver v91 entrypoints."""

from alpha.reasoning.tot import TreeOfThoughtSolver
from alpha.policy.safe_out import SafeOutPolicy
from alpha.router import ProgressiveRouter, AGENTS_V12
import logging


def _tree_of_thought(
    query: str,
    *,
    seed: int = 42,
    branching_factor: int = 3,
    score_threshold: float = 0.70,
    max_depth: int = 5,
    timeout_s: int = 10,
    dynamic_prune_margin: float = 0.15,
    low_conf_threshold: float = 0.60,
    enable_cot_fallback: bool = True,
    multi_branch: bool = True,
    max_width: int = 3,
    max_nodes: int = 200,
    enable_progressive_router: bool = True,
    router_escalation: list[str] | None = None,
    enable_agents_v12: bool = False,
    agents_v12_order: list[str] | None = None,
    logger: logging.Logger | None = None,
) -> dict:
    """Solve ``query`` via deterministic Tree-of-Thought reasoning."""
    router = None
    if enable_progressive_router:
        escalation = router_escalation or ["basic", "structured", "constrained"]
        router = ProgressiveRouter(escalation)
    agents = None
    if enable_agents_v12:
        order = agents_v12_order or ["decomposer", "checker", "calculator"]
        agents = [AGENTS_V12[name] for name in order if name in AGENTS_V12]
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
        logger=logger,
    )
    tot_result = solver.solve(query)
    policy = SafeOutPolicy(
        low_conf_threshold=low_conf_threshold,
        enable_cot_fallback=enable_cot_fallback,
    )
    decision = policy.apply(tot_result, query, logger=logger)
    decision["diagnostics"] = {
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
    return decision
