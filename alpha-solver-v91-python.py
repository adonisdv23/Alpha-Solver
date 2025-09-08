"""Alpha Solver v91 entrypoints."""

from alpha.solver.observability import AlphaSolver


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

    solver = AlphaSolver()
    return solver.solve(
        query,
        seed=seed,
        branching_factor=branching_factor,
        score_threshold=score_threshold,
        max_depth=max_depth,
        timeout_s=timeout_s,
        dynamic_prune_margin=dynamic_prune_margin,
        low_conf_threshold=low_conf_threshold,
        enable_cot_fallback=enable_cot_fallback,
        max_cot_steps=max_cot_steps,
        multi_branch=multi_branch,
        max_width=max_width,
        max_nodes=max_nodes,
        enable_progressive_router=enable_progressive_router,
        router_min_progress=router_min_progress,
        enable_agents_v12=enable_agents_v12,
        agents_v12_order=agents_v12_order,
    )


__all__ = ["_tree_of_thought", "AlphaSolver"]
