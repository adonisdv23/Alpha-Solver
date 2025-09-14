from __future__ import annotations

"""Tool suggestion rule for MCP registries."""

from typing import Any, Dict, List, Tuple

Registry = Dict[str, Any]

_INTENT_TYPE_MAP: Dict[str, str] = {
    "browse": "http",
    "sheet": "script",
}

# penalty weights
_INTENT_MISMATCH_PENALTY = 0.4
_NETWORK_PENALTY = 0.2
_LATENCY_PENALTY = 0.2
_SANDBOX_PENALTY = 0.5


def _estimate_latency(tool: Dict[str, Any]) -> int:
    """Return the tool's estimated latency in ms (default 200)."""
    return int(tool.get("estimated_latency_ms", 200))


def _score_tool(
    tool: Dict[str, Any],
    request: Dict[str, Any],
    policy_flags: Dict[str, bool],
) -> Tuple[float, List[str]]:
    """Return score in [0,1] and reasons for a tool."""
    score = 1.0
    reasons: List[str] = []

    expected_type = _INTENT_TYPE_MAP.get(request.get("intent", ""))
    tool_type = tool.get("type")
    if expected_type and tool_type == expected_type:
        reasons.append("intent_match")
    else:
        score -= _INTENT_MISMATCH_PENALTY
        reasons.append("intent_mismatch")

    if request.get("needs_network") and tool_type != "http":
        score -= _NETWORK_PENALTY
        reasons.append("network_penalty")

    if request.get("latency_sla_ms", 0) < _estimate_latency(tool):
        score -= _LATENCY_PENALTY
        reasons.append("latency_penalty")

    if policy_flags.get("sandbox_strict") and tool_type == "script":
        score -= _SANDBOX_PENALTY
        reasons.append("sandbox_penalty")

    # clamp
    if score < 0:
        score = 0.0
    elif score > 1:
        score = 1.0

    return score, reasons


def suggest_tool(
    registry: Registry,
    request: Dict[str, Any],
    policy_flags: Dict[str, bool],
) -> Dict[str, Any]:
    """Suggest a tool based on the request and policy flags."""
    if policy_flags.get("block"):
        return {
            "decision": "block",
            "tool": None,
            "confidence": 0.0,
            "reasons": ["policy_block"],
            "gate_rules": ["policy_block"],
        }

    tools = [t for t in registry.get("tool", []) if t.get("enabled", True)]
    if not tools:
        return {
            "decision": "clarify",
            "tool": None,
            "confidence": 0.0,
            "reasons": ["no_tool"],
            "gate_rules": [],
        }

    scored: List[Tuple[float, int, str, List[str]]] = []
    for tool in tools:
        score, reasons = _score_tool(tool, request, policy_flags)
        scored.append((score, _estimate_latency(tool), tool["name"], reasons))

    scored.sort(key=lambda x: (-x[0], x[1], x[2]))
    best_score, _, best_name, reasons = scored[0]

    decision = "allow" if best_score > 0 else "clarify"
    return {
        "decision": decision,
        "tool": best_name if decision == "allow" else None,
        "confidence": best_score,
        "reasons": reasons,
        "gate_rules": [],
    }


def to_route_explain(result: Dict[str, Any]) -> Dict[str, Any]:
    """Pass-through helper for router decisions."""
    return dict(result)
