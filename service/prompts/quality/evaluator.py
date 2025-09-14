import hashlib
import re
from typing import Dict, List, Optional

import yaml


def rubrics_sha(yaml_text: str) -> str:
    """Return SHA256 hex digest of rubrics YAML."""
    return hashlib.sha256(yaml_text.encode("utf-8")).hexdigest()


def estimate_tokens(text: str) -> int:
    """Very rough token estimate using whitespace splitting."""
    return len(text.strip().split()) if text.strip() else 0


class QualityEvaluator:
    """Heuristic evaluator for prompt responses."""

    def __init__(self, rubrics: Dict, yaml_text: Optional[str] = None):
        self.rubrics = rubrics
        if yaml_text is None:
            yaml_text = yaml.safe_dump(rubrics, sort_keys=True)
        self.rubrics_sha = rubrics_sha(yaml_text)

    # --- helpers -----------------------------------------------------------------
    def _score_correctness(self, response: str, context: Dict) -> int:
        required: List[str] = context.get("must_include", [])
        if not required:
            return 2
        present = sum(1 for k in required if re.search(re.escape(k), response, re.IGNORECASE))
        if present == len(required):
            return 2
        if present > 0:
            return 1
        return 0

    def _score_brevity(self, response: str, context: Dict) -> int:
        threshold = context.get("max_tokens", 120)
        tokens = estimate_tokens(response)
        if tokens <= threshold:
            return 2
        if tokens <= threshold * 1.5:
            return 1
        return 0

    def _score_structure(self, response: str, context: Dict) -> int:
        checks = []
        if context.get("require_headings"):
            checks.append(bool(re.search(r"^#.+", response, re.MULTILINE)))
        if context.get("require_bullets"):
            checks.append(bool(re.search(r"^[\-\*] ", response, re.MULTILINE)))
        fields: List[str] = context.get("required_fields", [])
        for f in fields:
            pattern = rf"{re.escape(f)}:"  # field followed by colon
            checks.append(bool(re.search(pattern, response)))
        if not checks:
            return 2
        passed = sum(checks)
        if passed == len(checks):
            return 2
        if passed > 0:
            return 1
        return 0

    def _score_safety(self, response: str, context: Dict) -> int:
        if context.get("pii_raw"):
            return 0
        email_re = r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"
        phone_re = r"\b\d{3}[- ]?\d{3}[- ]?\d{4}\b"
        if re.search(email_re, response) or re.search(phone_re, response):
            return 0
        return 2

    # --- public API ---------------------------------------------------------------
    def score(self, response: str, *, context: Optional[Dict] = None) -> Dict:
        ctx = context or {}
        scores = {
            "correctness": self._score_correctness(response, ctx),
            "brevity": self._score_brevity(response, ctx),
            "structure": self._score_structure(response, ctx),
            "safety": self._score_safety(response, ctx),
        }
        total = sum(scores.values())
        return {"scores": scores, "total": total, "max": 8}

    def compare(self, baseline: str, variant: str, *, context: Optional[Dict] = None) -> Dict:
        ctx = context or {}
        baseline_score = self.score(baseline, context=ctx)
        variant_score = self.score(variant, context=ctx)
        if baseline_score["total"] > variant_score["total"]:
            winner = "baseline"
        elif baseline_score["total"] < variant_score["total"]:
            winner = "variant"
        else:
            winner = "tie"
        route_explain = {
            "prompt_deck_sha": ctx.get("prompt_deck_sha"),
            "rubrics_sha": self.rubrics_sha,
        }
        return {
            "baseline": baseline_score,
            "variant": variant_score,
            "winner": winner,
            "route_explain": route_explain,
        }
