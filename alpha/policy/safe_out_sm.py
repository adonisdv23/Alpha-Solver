from __future__ import annotations

"""SAFE-OUT v1.2 state machine and configuration."""

from dataclasses import asdict, dataclass
from typing import Any, Dict, List, Optional

from alpha.reasoning.logging import log_event, log_safe_out_decision, log_safe_out_phase

try:  # Optional deterministic CoT import
    from alpha.reasoning.cot import run_cot  # type: ignore
except Exception:  # pragma: no cover - fallback when CoT unavailable

    def run_cot(query: str, seed: int, max_steps: int) -> Dict[str, Any]:  # type: ignore
        return {
            "answer": f"To proceed, clarify: {query} …",
            "confidence": 0.50,
            "steps": [],
        }


@dataclass(frozen=True)
class SOConfig:
    """Configuration for the SAFE-OUT state machine."""

    low_conf_threshold: float = 0.60
    enable_cot_fallback: bool = True
    seed: int = 42
    max_cot_steps: int = 4


class SafeOutStateMachine:
    """Deterministic SAFE-OUT policy state machine."""

    def __init__(self, config: SOConfig) -> None:
        self.config = config

    def run(self, tot_result: Dict[str, Any], original_query: str) -> Dict[str, Any]:
        """Execute the SAFE-OUT state machine for ``tot_result``."""

        phases: List[str] = ["init"]
        confidence = float(tot_result.get("confidence", 0.0))
        evidence: List[str] = list(tot_result.get("evidence", []))
        recovery_notes = ""
        log_event("safe_out_config", layer="safe_out", config=asdict(self.config))
        log_safe_out_phase(
            phase="init",
            route="pending",
            conf=confidence,
            threshold=self.config.low_conf_threshold,
        )

        phases.append("assess")
        if confidence >= self.config.low_conf_threshold:
            route = "tot"
            notes = "confidence above threshold"
            cot_result: Optional[Dict[str, Any]] = None
            log_safe_out_phase(
                phase="assess",
                route=route,
                conf=confidence,
                threshold=self.config.low_conf_threshold,
            )
        else:
            log_safe_out_phase(
                phase="assess",
                route="below_threshold",
                conf=confidence,
                threshold=self.config.low_conf_threshold,
            )
            phases.append("fallback")
            if self.config.enable_cot_fallback:
                cot_result = run_cot(
                    original_query,
                    seed=self.config.seed,
                    max_steps=self.config.max_cot_steps,
                )
                confidence = float(cot_result.get("confidence", 0.0))
                route = "cot_fallback"
                notes = (
                    f"Confidence below {self.config.low_conf_threshold:.2f}; used chain-of-thought fallback."
                )
                recovery_notes = "used chain-of-thought fallback"
                log_safe_out_phase(
                    phase="fallback",
                    route=route,
                    conf=confidence,
                    threshold=self.config.low_conf_threshold,
                )
            else:
                cot_result = None
                route = "best_effort"
                notes = (
                    f"Confidence below {self.config.low_conf_threshold:.2f}; recommending clarification or narrower query."
                )
                recovery_notes = "escalated to constrained profile"
                log_safe_out_phase(
                    phase="fallback",
                    route=route,
                    conf=confidence,
                    threshold=self.config.low_conf_threshold,
                )

        phases.append("finalize")
        log_safe_out_phase(
            phase="finalize",
            route=route,
            conf=confidence,
            threshold=self.config.low_conf_threshold,
        )
        if route == "tot":
            reason = tot_result.get("reason", "ok")
        else:
            reason = tot_result.get("reason")
            if not reason or reason == "ok":
                reason = "low_confidence"
        notes = f"{notes} | phases: {'->'.join(phases)}"
        envelope = {
            "final_answer": (cot_result or tot_result).get("answer", ""),
            "route": route,
            "confidence": confidence,
            "reason": reason,
            "notes": notes,
            "tot": tot_result,
            "cot": cot_result,
            "phases": phases,
            "evidence": evidence,
            "recovery_notes": recovery_notes if route != "tot" else "",
        }
        log_safe_out_decision(
            route=route, conf=confidence, threshold=self.config.low_conf_threshold, reason=reason
        )
        return envelope


__all__ = ["SOConfig", "SafeOutStateMachine"]
