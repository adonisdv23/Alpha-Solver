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
        enable_agents_v12: bool = False,
        agents_v12_order: Tuple[str, ...] = (
            "decomposer",
            "checker",
            "calculator",
        ),
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
        )
        router = (
            ProgressiveRouter(min_progress=router_min_progress)
            if enable_progressive_router
            else None
        )
        agents_cfg = AgentsV12Config(
            enable_agents_v12=enable_agents_v12, agents_v12_order=agents_v12_order
        )

        tot_result = (
            solver.solve(query, router=router)
            if router is not None
            else solver.solve(query)
        )

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

        self.observability.log_event(
            {"event": "solve_end", "diagnostics": envelope["diagnostics"]}
        )
        return envelope


__all__ = ["AlphaSolver"]
