"""Alpha Solver v91 entrypoints."""

from alpha.reasoning.tot import TreeOfThoughtSolver
from alpha.policy.safe_out_sm import SOConfig, SafeOutStateMachine


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
) -> dict:
    """Solve ``query`` via deterministic Tree-of-Thought reasoning."""
    solver = TreeOfThoughtSolver(
        seed=seed,
        branching_factor=branching_factor,
        score_threshold=score_threshold,
        max_depth=max_depth,
        timeout_s=timeout_s,
        dynamic_prune_margin=dynamic_prune_margin,
    )
    tot_result = solver.solve(query)
    cfg = SOConfig(
        low_conf_threshold=low_conf_threshold,
        enable_cot_fallback=enable_cot_fallback,
        seed=seed,
        max_cot_steps=max_cot_steps,
    )
    sm = SafeOutStateMachine(cfg)
    return sm.run(tot_result, query)
