from __future__ import annotations

"""SAFE-OUT v1.1 state machine for structured recovery."""

from dataclasses import dataclass, asdict
from typing import Any, Dict, List, Literal, Optional

from alpha.reasoning import logging as rlog

Phase = Literal["init", "assess", "fallback", "finalize"]


@dataclass(frozen=True)
class SOConfig:
    """Configuration for :class:`SafeOutStateMachine`."""

    low_conf_threshold: float = 0.60
    enable_cot_fallback: bool = True
    max_cot_steps: int = 4
    seed: int = 42


try:  # Best-effort optional CoT import
    from alpha.reasoning.cot import run_cot  # type: ignore
except Exception:  # pragma: no cover - fallback when CoT unavailable
    run_cot = None  # type: ignore


def _run_cot_shim(query: str, *, seed: int, max_steps: int) -> Dict[str, Any]:
    """Deterministic placeholder Chain-of-Thought response."""
    steps = [f"step {i + 1}: {query}" for i in range(max_steps)]
    return {"answer": f"To proceed, clarify: {query} …", "confidence": 0.50, "steps": steps}


class SafeOutStateMachine:
    """Deterministic SAFE-OUT recovery flow."""

    def __init__(self, cfg: SOConfig, logger: Any = rlog) -> None:
        self.cfg = cfg
        self.logger = logger

    def run(self, tot_result: Dict[str, Any], original_query: str) -> Dict[str, Any]:
        """Traverse SAFE-OUT phases and return a policy envelope."""
        phases: List[Phase] = ["init"]
        self.logger.log_event("safe_out_config", config=asdict(self.cfg))
        self.logger.log_safe_out_phase(
            phase="init",
            conf=float(tot_result.get("confidence", 0.0)),
            threshold=self.cfg.low_conf_threshold,
        )

        conf = float(tot_result.get("confidence", 0.0))
        tot_reason = str(tot_result.get("reason", "ok"))
        phases.append("assess")
        self.logger.log_safe_out_phase(
            phase="assess",
            conf=conf,
            threshold=self.cfg.low_conf_threshold,
        )

        if tot_reason == "timeout":
            phases.append("fallback")
            if self.cfg.enable_cot_fallback:
                cot_fn = run_cot or _run_cot_shim
                cot_result = cot_fn(
                    original_query, seed=self.cfg.seed, max_steps=self.cfg.max_cot_steps
                )
                route = "cot_fallback"
                conf = float(cot_result.get("confidence", 0.0))
            else:
                cot_result = None
                route = "best_effort"
            reason = "timeout"
            final_answer = (cot_result or tot_result).get("answer", "")
            self.logger.log_safe_out_phase(
                phase="fallback", route=route, conf=conf, threshold=self.cfg.low_conf_threshold
            )
        elif conf >= self.cfg.low_conf_threshold:
            route = "tot"
            reason = tot_reason
            final_answer = tot_result.get("answer", "")
            cot_result = None
        else:
            phases.append("fallback")
            if self.cfg.enable_cot_fallback:
                cot_fn = run_cot or _run_cot_shim
                cot_result = cot_fn(
                    original_query, seed=self.cfg.seed, max_steps=self.cfg.max_cot_steps
                )
                route = "cot_fallback"
                conf = float(cot_result.get("confidence", 0.0))
            else:
                cot_result = None
                route = "best_effort"
            reason = "low_confidence"
            final_answer = (cot_result or tot_result).get("answer", "")
            self.logger.log_safe_out_phase(
                phase="fallback", route=route, conf=conf, threshold=self.cfg.low_conf_threshold
            )

        phases.append("finalize")
        self.logger.log_safe_out_phase(
            phase="finalize", route=route, conf=conf, threshold=self.cfg.low_conf_threshold
        )
        notes = f"path={'->'.join(phases)}"
        if tot_reason != "ok":
            notes += f"; tot_reason={tot_reason}"
        return {
            "final_answer": final_answer,
            "route": route,
            "confidence": conf,
            "reason": reason,
            "notes": notes,
            "tot": tot_result,
            "cot": cot_result,
            "phases": phases,
        }
