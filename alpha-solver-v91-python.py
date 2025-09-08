"""Alpha Solver v91 entrypoints."""

from alpha.reasoning.tot import TreeOfThoughtSolver
from alpha.policy.safe_out_sm import SOConfig, SafeOutStateMachine
from alpha.router import ProgressiveRouter, AgentsV12Config


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
    max_cot_steps: int = 4,
    multi_branch: bool = False,
    max_width: int = 3,
    max_nodes: int = 100,
    enable_progressive_router: bool = False,
    router_min_progress: float = 0.3,
    enable_agents_v12: bool = False,
    agents_v12_order: tuple[str, ...] = (
        "decomposer",
        "checker",
        "calculator",
    ),
) -> dict:
    """Solve ``query`` via deterministic Tree-of-Thought reasoning."""
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
    )
    router = (
        ProgressiveRouter(min_progress=router_min_progress)
        if enable_progressive_router
        else None
    )
    agents_cfg = AgentsV12Config(
        enable_agents_v12=enable_agents_v12, agents_v12_order=agents_v12_order
    )
    if router is None:
        tot_result = solver.solve(query)
    else:
        tot_result = solver.solve(query, router=router)
    cfg = SOConfig(
        low_conf_threshold=low_conf_threshold,
        enable_cot_fallback=enable_cot_fallback,
        seed=seed,
        max_cot_steps=max_cot_steps,
    )
    sm = SafeOutStateMachine(cfg)
    envelope = sm.run(tot_result, query)
    envelope["diagnostics"] = {
        "tot": tot_result,
        "router": {"stage": router.stage if router else "basic"},
        "agents_v12": {
            "enabled": agents_cfg.enable_agents_v12,
            "order": agents_cfg.agents_v12_order,
        },
    }
    return envelope
