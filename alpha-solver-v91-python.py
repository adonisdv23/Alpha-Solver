"""Alpha Solver v91 entrypoints."""

from alpha.core.observability import ObservabilityConfig
from alpha.solver.observability import AlphaSolver
from alpha.config.loader import load_config


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
    router_escalation: tuple[str, ...] = ("basic", "structured", "constrained"),
    enable_agents_v12: bool = False,
    agents_v12_order: tuple[str, ...] = (
        "decomposer",
        "checker",
        "calculator",
    ),
    replay: str | None = None,
    record: str | None = None,
    strict_accessibility: bool = False,
    log_path: str | None = None,
    telemetry_endpoint: str | None = None,
) -> dict:
    """Solve ``query`` via deterministic Tree-of-Thought reasoning."""

    cfg = ObservabilityConfig.load()
    if log_path:
        cfg.log_path = log_path
    if telemetry_endpoint:
        cfg.enable_telemetry = True
        cfg.telemetry_endpoint = telemetry_endpoint
    from alpha.core.observability import ObservabilityManager

    obs = ObservabilityManager(cfg, replay_session=replay)
    cfg_dict = load_config(
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
        router_escalation=router_escalation,
        enable_agents_v12=enable_agents_v12,
        agents_v12_order=agents_v12_order,
    )
    solver = AlphaSolver(observability=obs)
    envelope = solver.solve(
        query,
        seed=cfg_dict["seed"],
        branching_factor=cfg_dict["branching_factor"],
        score_threshold=cfg_dict["score_threshold"],
        max_depth=cfg_dict["max_depth"],
        timeout_s=cfg_dict["timeout_s"],
        dynamic_prune_margin=cfg_dict["dynamic_prune_margin"],
        low_conf_threshold=cfg_dict["low_conf_threshold"],
        enable_cot_fallback=cfg_dict["enable_cot_fallback"],
        max_cot_steps=cfg_dict["max_cot_steps"],
        multi_branch=cfg_dict["multi_branch"],
        max_width=cfg_dict["max_width"],
        max_nodes=cfg_dict["max_nodes"],
        enable_progressive_router=cfg_dict["enable_progressive_router"],
        router_min_progress=cfg_dict["router_min_progress"],
        router_escalation=tuple(cfg_dict["router_escalation"]),
        enable_agents_v12=cfg_dict["enable_agents_v12"],
        agents_v12_order=tuple(cfg_dict["agents_v12_order"]),
    )
    envelope.setdefault("diagnostics", {})["config"] = cfg_dict
    a11y = solver.observability.check_text(envelope.get("solution", ""))
    if strict_accessibility and a11y and not a11y.get("ok", True):
        raise ValueError("accessibility check failed")
    envelope["accessibility"] = a11y
    session_id = solver.observability.close(record)
    if session_id:
        envelope.setdefault("diagnostics", {})["replay_session"] = session_id
    from alpha.reasoning.logging import emit_run_summary

    emit_run_summary(
        counts={"explored_nodes": envelope.get("tot", {}).get("explored_nodes", 0)},
        final_route=envelope.get("route", ""),
        final_confidence=float(envelope.get("confidence", 0.0)),
    )
    return envelope


def main() -> None:  # pragma: no cover - simple CLI
    import argparse, json

    ap = argparse.ArgumentParser()
    ap.add_argument("query")
    ap.add_argument("--replay")
    ap.add_argument("--record")
    ap.add_argument("--strict-accessibility", action="store_true")
    ap.add_argument("--log-path")
    ap.add_argument("--telemetry-endpoint")
    args = ap.parse_args()
    result = _tree_of_thought(
        args.query,
        replay=args.replay,
        record=args.record,
        strict_accessibility=args.strict_accessibility,
        log_path=args.log_path,
        telemetry_endpoint=args.telemetry_endpoint,
    )
    print(json.dumps(result))


__all__ = ["_tree_of_thought", "AlphaSolver"]

if __name__ == "__main__":  # pragma: no cover
    main()
