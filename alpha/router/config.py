from __future__ import annotations

"""Configuration flags for router v12."""

from dataclasses import dataclass
from typing import Tuple


@dataclass(frozen=True)
class AgentsV12Config:
    """Flags controlling experimental v12 agents."""

    enable_agents_v12: bool = False
    agents_v12_order: Tuple[str, ...] = ("decomposer", "checker", "calculator")
