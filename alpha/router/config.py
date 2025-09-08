from __future__ import annotations

"""Configuration flags for router components."""

from dataclasses import dataclass
from typing import Tuple


@dataclass(frozen=True)
class AgentsV12Config:
    """Flags controlling experimental v12 agents."""

    enable_agents_v12: bool = False
    agents_v12_order: Tuple[str, ...] = ("decomposer", "checker", "calculator")


@dataclass(frozen=True)
class ProgressiveRouterConfig:
    """Flags controlling the progressive complexity router."""

    enable_progressive_router: bool = False
    router_escalation: Tuple[str, ...] = ("basic", "structured", "constrained")
    router_min_progress: float = 0.3

