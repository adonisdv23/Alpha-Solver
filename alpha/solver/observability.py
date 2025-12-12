from __future__ import annotations

"""Observability-enabled solver wrapper."""

from dataclasses import dataclass, field
from typing import Any, Dict, Tuple

from alpha.core.observability import ObservabilityManager
from alpha.reasoning.tot import TreeOfThoughtSolver
from alpha.router import ProgressiveRouter
from alpha.router.config import AgentsV12Config
from alpha.policy.safe_out_sm import SOConfig, SafeOutStateMachine


__all__ = ["AlphaSolver"]


@dataclass
class AlphaSolver:
    """Minimal Alpha Solver v2.2.6 with P3 observability.

    This lightweight implementation focuses on determinism and logging while
    delegating reasoning to :class:`TreeOfThoughtSolver`.
    """

    tools_canon_path: str | None = None
    k: int = 1
    observability: ObservabilityManager = field(default_factory=ObservabilityManager)

    def solve(
        self,
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
        router_escalation: Tuple[str, ...] = ("basic", "structured", "constrained"),
        enable_agents_v12: bool = False,
        agents_v12_order: Tuple[str, ...] = (
            "decomposer",
            "checker",
            "calculator",
        ),
        scorer: str = "composite",
        scorer_weights: Dict[str, float] | None = None,
        cache: Dict[str, Any] | None = None,
    ) -> Dict[str, Any]:
        """Solve ``query`` and return an envelope with diagnostics."""

        self.observability.log_event({"event": "solve_start", "query": query})

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
            scorer=scorer,
            scorer_weights=scorer_weights,
        )
        router = (
            ProgressiveRouter(
                min_progress=router_min_progress, escalation=router_escalation
            )
            if enable_progressive_router
            else None
        )
        agents_cfg = AgentsV12Config(
            enable_agents_v12=enable_agents_v12, agents_v12_order=agents_v12_order
        )

        solve_kwargs: Dict[str, Any] = {"cache": cache}
        if router is not None:
            solve_kwargs["router"] = router
        try:
            tot_result = solver.solve(query, **solve_kwargs)
        except TypeError:
            solve_kwargs.pop("cache", None)
            tot_result = solver.solve(query, **solve_kwargs)

        cfg = SOConfig(
            low_conf_threshold=low_conf_threshold,
            enable_cot_fallback=enable_cot_fallback,
            seed=seed,
            max_cot_steps=max_cot_steps,
        )
        sm = SafeOutStateMachine(cfg)
        envelope = sm.run(tot_result, query)

        router_stage = router.stage if router else "basic"
        if (
            router
            and multi_branch
            and router_stage
            == (router.escalation[0] if router.escalation else "basic")
        ):
            # Surface that we are in a ToT routing path even if cache hits skipped escalation.
            router_stage = "tot"

        envelope["diagnostics"] = {
            "tot": tot_result,
            "router": {"stage": router_stage},
            "agents_v12": {
                "enabled": agents_cfg.enable_agents_v12,
                "order": agents_cfg.agents_v12_order,
            },
            "safe_out": {
                "low_conf_threshold": low_conf_threshold,
                "enable_cot_fallback": enable_cot_fallback,
            },
            "scorer": {"name": solver.scorer_name, "weights": solver.scorer_weights},
        }

        # Basic fields for legacy smoke tests
        shortlist = [
            {"answer": tot_result["answer"], "confidence": tot_result["confidence"]}
        ]
        envelope.setdefault("pending_questions", [])
        envelope.setdefault("shortlist", shortlist)
        envelope.setdefault("orchestration_plan", [])
        envelope.setdefault("solution", tot_result["answer"])
        envelope.setdefault("confidence", tot_result["confidence"])
        envelope.setdefault("response_time_ms", 0)
        envelope.setdefault("telemetry_contract", {})
        envelope.setdefault("expert_team", [])
        envelope.setdefault("eligibility_analysis", {})
        envelope.setdefault("requirements_analysis", {})
        envelope.setdefault("safe_out_state", envelope.get("route", ""))
        envelope.setdefault("steps", tot_result.get("steps", []))
        envelope.setdefault("best_path_hash", tot_result.get("best_path_hash"))
        envelope.setdefault("cache_hit", tot_result.get("cache_hit", False))
        if "best_path" in tot_result:
            envelope.setdefault("best_path", tot_result["best_path"])

        envelope.setdefault("run_summary", {})["accounting"] = solver.accounting.summary()
        self.observability.log_event(
            {"event": "solve_end", "diagnostics": envelope["diagnostics"]}
        )
        return envelope


__all__ = ["AlphaSolver"]
