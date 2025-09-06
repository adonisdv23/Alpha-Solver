"""Plan data structures"""
from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Callable, Dict, List, Optional, Tuple


@dataclass
class PlanStep:
    tool_id: str
    prompt: str = ""
    adapter: Optional[str] = None
    reasons: Dict[str, Any] = field(default_factory=dict)
    confidence: Optional[float] = None
    estimated_cost_usd: float = 0.0
    mode: str = "execute"
    enrichment: Dict[str, Any] = field(default_factory=dict)
    # --- plan spine fields ---
    step_id: str = ""
    description: str = ""
    contract: Dict[str, Any] = field(default_factory=dict)
    result: Dict[str, Any] = field(default_factory=dict)
    status: str = "pending"

    def to_dict(self) -> Dict[str, Any]:
        data = {
            "tool_id": self.tool_id,
            "prompt": self.prompt,
            "adapter": self.adapter,
            "reasons": self.reasons,
            "confidence": self.confidence,
            "estimated_cost_usd": self.estimated_cost_usd,
            "mode": self.mode,
            "enrichment": self.enrichment,
        }
        if self.step_id:
            data["step_id"] = self.step_id
        if self.description:
            data["description"] = self.description
        if self.contract:
            data["contract"] = self.contract
        if self.result:
            data["result"] = self.result
        if self.status != "pending":
            data["status"] = self.status
        return data


@dataclass
class Guardrails:
    budget: Dict[str, Any] = field(default_factory=dict)
    circuit_breakers: Dict[str, Any] = field(default_factory=dict)
    audit: Dict[str, Any] = field(default_factory=dict)
    policy_dryrun: bool = False
    policy_notes: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "budget": self.budget,
            "circuit_breakers": self.circuit_breakers,
            "audit": self.audit,
            "policy_dryrun": self.policy_dryrun,
            "policy_notes": self.policy_notes,
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
    # --- plan spine fields ---
    run_id: str = ""
    query: str = ""
    region: str = ""
    retries: int = 0
    created_at: str = field(
        default_factory=lambda: datetime.now(timezone.utc)
        .isoformat()
        .replace("+00:00", "Z")
    )

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

    def to_json(self) -> Dict[str, Any]:
        """Emit minimal JSON representation with schema_version."""
        return {
            "schema_version": "v1",
            "run_id": self.run_id,
            "query": self.query or self.inputs.get("query"),
            "region": self.region or self.inputs.get("region"),
            "retries": self.retries,
            "created_at": self.created_at,
            "steps": [s.to_dict() for s in self.steps],
        }

    def human_summary(self) -> str:
        q = self.inputs.get("query", self.query)
        region = self.inputs.get("region", self.region)
        return (
            f"Plan for '{q}' in region '{region}' with {len(self.steps)} steps; "
            f"estimated cost ${self.estimated_cost_usd:.2f}"
        )


def validate_contract(step: PlanStep, result: Dict[str, Any]) -> Tuple[bool, str]:
    """Validate result against the step contract."""
    contract = step.contract or {}
    for key, expected in contract.items():
        actual = result.get(key)
        if actual != expected:
            critique = (
                f"contract mismatch for '{key}': expected {expected!r} got {actual!r}"
            )
            return False, critique
    return True, ""


def bounded_retry(
    step: PlanStep,
    func: Callable[[], Dict[str, Any]],
    max_retries: int = 0,
    logger: Optional[Callable[[str], None]] = None,
) -> None:
    """Execute func until contract passes or retries exhausted."""
    attempts = 0
    while True:
        result = func()
        ok, critique = validate_contract(step, result)
        step.result = result
        if ok:
            step.status = "ok"
            return
        step.status = "failed"
        if critique:
            step.result.setdefault("critique", critique)
            if logger:
                logger(critique)
        attempts += 1
        if attempts > max_retries:
            return
