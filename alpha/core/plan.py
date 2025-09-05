"""Simple plan structures"""
from dataclasses import dataclass, field
from typing import List, Dict, Optional

@dataclass
class PlanStep:
    tool_id: str
    prompt: str = ""
    adapter: Optional[str] = None
    estimated_cost_usd: float = 0.0

@dataclass
class Plan:
    steps: List[PlanStep] = field(default_factory=list)
    estimated_cost_usd: float = 0.0
    breaker: Dict[str, int] = field(default_factory=dict)
    audit_log: Optional[str] = None
    instructions_only: bool = False
