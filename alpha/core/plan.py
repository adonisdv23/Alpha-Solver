"""Plan data structures"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class PlanStep:
    tool_id: str
    prompt: str = ""
    adapter: Optional[str] = None
    reasons: Dict[str, Any] = field(default_factory=dict)
    confidence: Optional[float] = None
    estimated_cost_usd: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "tool_id": self.tool_id,
            "prompt": self.prompt,
            "adapter": self.adapter,
            "reasons": self.reasons,
            "confidence": self.confidence,
            "estimated_cost_usd": self.estimated_cost_usd,
        }


@dataclass
class Guardrails:
    budget: Dict[str, Any] = field(default_factory=dict)
    circuit_breakers: Dict[str, Any] = field(default_factory=dict)
    audit: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "budget": self.budget,
            "circuit_breakers": self.circuit_breakers,
            "audit": self.audit,
        }


@dataclass
class Fallback:
    reason: str = ""
    steps: List[PlanStep] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "reason": self.reason,
            "steps": [s.to_dict() for s in self.steps],
        }


@dataclass
class Plan:
    version: str = "1.0"
    run: Dict[str, Any] = field(default_factory=dict)
    inputs: Dict[str, Any] = field(default_factory=dict)
    steps: List[PlanStep] = field(default_factory=list)
    guards: Guardrails = field(default_factory=Guardrails)
    fallbacks: List[Fallback] = field(default_factory=list)
    artifacts: Dict[str, Any] = field(default_factory=dict)
    estimated_cost_usd: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "version": self.version,
            "run": self.run,
            "inputs": self.inputs,
            "steps": [s.to_dict() for s in self.steps],
            "guards": self.guards.to_dict(),
            "fallbacks": [f.to_dict() for f in self.fallbacks],
            "artifacts": self.artifacts,
            "estimated_cost_usd": self.estimated_cost_usd,
        }

    def human_summary(self) -> str:
        q = self.inputs.get("query", "")
        region = self.inputs.get("region", "")
        return (
            f"Plan for '{q}' in region '{region}' with {len(self.steps)} steps; "
            f"estimated cost ${self.estimated_cost_usd:.2f}"
        )
