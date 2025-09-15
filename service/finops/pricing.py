from __future__ import annotations

"""Simple in-repo pricing tables and helpers.

This module mirrors a tiny portion of the service side cost model so tests can
assert parity between the CLI simulator and the service estimator.  Pricing data
is intentionally small and completely static; no network calls are performed.
"""

from functools import lru_cache
from typing import Dict, Any
import yaml

PRICING_PATH = "config/cost_models.yaml"


@lru_cache()
def load_pricing(path: str = PRICING_PATH) -> Dict[str, Any]:
    """Load pricing information from the repo's YAML table.

    Parameters
    ----------
    path:
        Optional override path to the YAML file.

    Returns
    -------
    dict
        Parsed YAML structure.  The result is cached so repeated calls are
        cheap.
    """

    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def price_for(provider: str, model: str) -> Dict[str, float]:
    """Return pricing dict for a given provider/model pair."""

    models = load_pricing()
    return models["providers"][provider][model]


def cost_of_tokens(
    provider: str,
    model: str,
    prompt_tokens: int,
    completion_tokens: int,
) -> float:
    """Compute USD cost for token usage.

    The formula intentionally matches the service implementation so that tests
    can verify ~parity (within 1%).
    """

    pricing = price_for(provider, model)
    cost = (
        prompt_tokens * pricing.get("input_price_per_1k", 0.0) / 1000.0
        + completion_tokens * pricing.get("output_price_per_1k", 0.0) / 1000.0
    )
    min_charge = pricing.get("min_charge_usd", 0.0)
    if cost < min_charge:
        cost = min_charge
    return cost


# Model-set lookup table.  A model-set is simply a short name that maps to a
# provider/model combination along with a couple of latency heuristics.  The
# numbers are deliberately small and easy to reason about.
MODEL_SETS: Dict[str, Dict[str, Any]] = {
    "default": {
        "provider": "openai",
        "model": "gpt-4o",
        "base_latency_ms": 100.0,
        "per_token_latency_ms": 0.5,
    },
    "cheap": {
        "provider": "openai",
        "model": "gpt-4o-mini",
        "base_latency_ms": 80.0,
        "per_token_latency_ms": 0.3,
    },
}
