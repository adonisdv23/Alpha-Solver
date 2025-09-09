from __future__ import annotations

"""Thin façade for SAFE-OUT state machine."""

from typing import Any, Dict

from .safe_out_sm import SOConfig, SafeOutStateMachine


class SafeOutPolicy:
    """Policy wrapper constructing and executing the state machine."""

    def __init__(
        self,
        *,
        low_conf_threshold: float = 0.60,
        enable_cot_fallback: bool = True,
        seed: int = 42,
        max_cot_steps: int = 4,
    ) -> None:
        self.config = SOConfig(
            low_conf_threshold=low_conf_threshold,
            enable_cot_fallback=enable_cot_fallback,
            seed=seed,
            max_cot_steps=max_cot_steps,
        )

    def apply(self, tot_result: Dict[str, Any], original_query: str) -> Dict[str, Any]:
        """Apply SAFE-OUT policy to ``tot_result``."""

        sm = SafeOutStateMachine(self.config)
        return sm.run(tot_result, original_query)


__all__ = ["SafeOutPolicy"]
