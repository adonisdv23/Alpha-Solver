"""MCP-aware routing logic for Alpha Solver."""
from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional

from .gates import CircuitBreaker, apply_budget_gate


@dataclass
class RouteDecision:
    use_mcp: bool
    mcp_reason_codes: List[str]
    mcp_score: float
    llm_score: float


def _latency_component(latency_budget_ms: int, expected_latency_ms: int) -> float:
    if latency_budget_ms <= 0:
        return 0.0
    if expected_latency_ms <= latency_budget_ms:
        return 1.0
    over_budget = expected_latency_ms - latency_budget_ms
    return max(0.0, 1.0 - (over_budget / max(latency_budget_ms, 1)))


def compute_mcp_score(
    tool_fit: float,
    estimated_cost_savings: float,
    llm_confidence: float,
    latency_budget_ms: int,
    expected_latency_ms: int,
) -> float:
    latency_score = _latency_component(latency_budget_ms, expected_latency_ms)
    return (
        max(tool_fit, 0.0) * 0.4
        + estimated_cost_savings * 0.3
        + max(0.0, 1.0 - llm_confidence) * 0.2
        + latency_score * 0.1
    )


def compute_llm_score(llm_confidence: float, estimated_cost_savings: float) -> float:
    penalty = max(0.0, -estimated_cost_savings)
    return llm_confidence * 0.8 + (1 - penalty) * 0.2


def route_request(
    tool_fit: float,
    estimated_cost_savings: float,
    llm_confidence: float,
    latency_budget_ms: int,
    expected_mcp_latency_ms: int,
    estimated_mcp_cost: float,
    tool_available: bool = True,
    epsilon: float = 0.05,
    breaker: Optional[CircuitBreaker] = None,
) -> RouteDecision:
    reasons: List[str] = []
    if tool_available:
        reasons.append("tool_available")
    else:
        return RouteDecision(False, reasons, 0.0, llm_confidence)

    budget_allowed, budget_reason = apply_budget_gate(estimated_mcp_cost)
    if not budget_allowed:
        reasons.append(budget_reason)
        return RouteDecision(False, reasons, 0.0, llm_confidence)

    breaker = breaker or CircuitBreaker()
    if breaker.is_open:
        reasons.append("circuit_open")
        return RouteDecision(False, reasons, 0.0, llm_confidence)

    if estimated_cost_savings > 0:
        reasons.append("cost_effective")
    if llm_confidence < 0.5:
        reasons.append("low_confidence_reroute")
    if expected_mcp_latency_ms <= latency_budget_ms:
        reasons.append("within_latency_budget")

    mcp_score = compute_mcp_score(
        tool_fit, estimated_cost_savings, llm_confidence, latency_budget_ms, expected_mcp_latency_ms
    )
    llm_score = compute_llm_score(llm_confidence, estimated_cost_savings)

    use_mcp = mcp_score > (llm_score + epsilon)
    if not use_mcp:
        reasons.append("llm_preferred")
    return RouteDecision(use_mcp, reasons, mcp_score, llm_score)


__all__ = [
    "RouteDecision",
    "route_request",
    "compute_mcp_score",
    "compute_llm_score",
]
