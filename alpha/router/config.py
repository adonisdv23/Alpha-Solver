from __future__ import annotations

"""Router configuration dataclasses."""

from dataclasses import dataclass, field
from typing import List


@dataclass
class RouterConfig:
    """Configuration flags for router components."""

    enable_progressive_router: bool = True
    router_escalation: List[str] = field(
        default_factory=lambda: ["basic", "structured", "constrained"]
    )
    enable_agents_v12: bool = False
    agents_v12_order: List[str] = field(
        default_factory=lambda: ["decomposer", "checker", "calculator"]
    )

