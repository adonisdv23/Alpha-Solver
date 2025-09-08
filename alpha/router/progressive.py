from __future__ import annotations

"""Deterministic progressive complexity router."""

from dataclasses import dataclass
from typing import Tuple, Optional

from alpha.reasoning.logging import log_event
from .config import ProgressiveRouterConfig


@dataclass
class ProgressiveRouter:
    """Escalate prompt complexity only when needed."""

    escalation: Tuple[str, ...] = ("basic", "structured", "constrained")
    min_progress: float = 0.3
    stage_index: int = 0

    @classmethod
    def from_config(
        cls, config: ProgressiveRouterConfig
    ) -> Optional["ProgressiveRouter"]:
        """Construct a router from ``ProgressiveRouterConfig``.

        Returns ``None`` when ``enable_progressive_router`` is ``False`` to allow
        callers to gate creation behind a single configuration object.
        """
        if not config.enable_progressive_router:
            return None
        return cls(
            escalation=config.router_escalation,
            min_progress=config.router_min_progress,
        )

    @property
    def stage(self) -> str:
        return self.escalation[self.stage_index]

    def route(self, progress: float) -> str:
        """Return current stage and escalate if ``progress`` is low."""
        if progress < self.min_progress and self.stage_index < len(self.escalation) - 1:
            prev = self.stage
            self.stage_index += 1
            log_event("router_escalate", previous=prev, new=self.stage, progress=progress)
        return self.stage
