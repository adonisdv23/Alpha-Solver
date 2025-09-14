from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Tuple


@dataclass
class GateConfig:
    """Configuration for gating thresholds.

    Attributes:
        low_conf_threshold: Clarify if confidence below this value.
        clarify_conf_threshold: Clarify if confidence below this value but above
            ``low_conf_threshold``.
        min_budget_tokens: Minimum budget tokens required for automatic allow.
        enable_cot_fallback: Whether to enable chain-of-thought fallback on low
            confidence.
    """

    low_conf_threshold: float = 0.35
    clarify_conf_threshold: float = 0.55
    min_budget_tokens: int = 256
    enable_cot_fallback: bool = True


def evaluate_gates(
    confidence: float,
    budget_tokens: int,
    policy_flags: Dict[str, bool],
    config: GateConfig | None = None,
) -> Tuple[str, Dict[str, Any]]:
    """Evaluate gating rules and return decision with route explain metadata.

    The decision is deterministic and one of ``{"allow", "clarify", "block"}``.
    The accompanying route explanation provides structured metadata used by
    callers to understand the gating verdict.
    """

    cfg = config or GateConfig()
    rules_hit: List[str] = []
    budget_verdict = "ok"

    if policy_flags.get("block", False):
        rules_hit.append("policy_block")
        decision = "block"
    elif budget_tokens < cfg.min_budget_tokens:
        rules_hit.append("budget_low")
        budget_verdict = "low"
        decision = "clarify"
    elif confidence < cfg.low_conf_threshold:
        rules_hit.append("low_confidence")
        budget_verdict = "clarify"
        decision = "clarify"
        if cfg.enable_cot_fallback:
            rules_hit.append("cot_fallback")
    elif confidence < cfg.clarify_conf_threshold:
        rules_hit.append("clarify_band")
        decision = "clarify"
    else:
        rules_hit.append("allow")
        decision = "allow"

    route_explain = {
        "decision": decision,
        "confidence": confidence,
        "budget_verdict": budget_verdict,
        "gate_rules": rules_hit,
    }
    return decision, route_explain


__all__ = ["GateConfig", "evaluate_gates"]
