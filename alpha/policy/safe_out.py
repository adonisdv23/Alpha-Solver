from __future__ import annotations

"""Facade for SAFE-OUT state machine."""

from typing import Any, Dict

from alpha.reasoning import logging as rlog

from .safe_out_sm import SOConfig, SafeOutStateMachine


class SafeOutPolicy:
    """Backward-compatible wrapper around :class:`SafeOutStateMachine`."""

    def __init__(
        self,
        *,
        low_conf_threshold: float = 0.60,
        enable_cot_fallback: bool = True,
        max_cot_steps: int = 4,
        seed: int = 42,
    ) -> None:
        self.cfg = SOConfig(
            low_conf_threshold=low_conf_threshold,
            enable_cot_fallback=enable_cot_fallback,
            max_cot_steps=max_cot_steps,
            seed=seed,
        )

    def apply(self, tot_result: Dict[str, Any], original_query: str) -> Dict[str, Any]:
        """Apply SAFE-OUT policy to ``tot_result``."""
        sm = SafeOutStateMachine(self.cfg, rlog)
        return sm.run(tot_result, original_query)
