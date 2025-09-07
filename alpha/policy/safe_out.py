from __future__ import annotations

"""SAFE-OUT policy for low-confidence Tree-of-Thought results."""

from typing import Any, Dict

try:  # Best-effort optional CoT import
    from alpha.reasoning.cot import run_cot  # type: ignore
except Exception:  # pragma: no cover - fallback when CoT unavailable
    run_cot = None  # type: ignore


def _run_cot_fallback(query: str) -> Dict[str, Any]:
    """Deterministic placeholder Chain-of-Thought response."""
    return {"answer": f"To proceed, clarify: {query} …", "confidence": 0.50, "steps": []}


class SafeOutPolicy:
    """Policy that handles low-confidence ToT results."""

    def __init__(self, *, low_conf_threshold: float = 0.60, enable_cot_fallback: bool = True) -> None:
        self.low_conf_threshold = low_conf_threshold
        self.enable_cot_fallback = enable_cot_fallback

    def apply(self, tot_result: Dict[str, Any], original_query: str) -> Dict[str, Any]:
        """Apply SAFE-OUT logic to ``tot_result``.

        Parameters
        ----------
        tot_result:
            Output from Tree-of-Thought solving.
        original_query:
            User query used for potential CoT fallback.
        """

        confidence = float(tot_result.get("confidence", 0.0))
        if confidence >= self.low_conf_threshold:
            return {
                "final_answer": tot_result.get("answer", ""),
                "route": "tot",
                "confidence": confidence,
                "reason": "ok",
                "notes": "confidence above threshold",
                "tot": tot_result,
                "cot": None,
            }

        if self.enable_cot_fallback:
            cot_fn = run_cot or _run_cot_fallback
            cot_result: Dict[str, Any] = cot_fn(original_query)
            return {
                "final_answer": cot_result.get("answer", ""),
                "route": "cot_fallback",
                "confidence": float(cot_result.get("confidence", 0.0)),
                "reason": "low_confidence",
                "notes": f"Confidence below {self.low_conf_threshold:.2f}; used chain-of-thought fallback.",
                "tot": tot_result,
                "cot": cot_result,
            }

        return {
            "final_answer": tot_result.get("answer", ""),
            "route": "best_effort",
            "confidence": confidence,
            "reason": "low_confidence",
            "notes": f"Confidence below {self.low_conf_threshold:.2f}; recommending clarification or narrower query.",
            "tot": tot_result,
            "cot": None,
        }
