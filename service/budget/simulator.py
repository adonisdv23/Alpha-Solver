"""Budget simulation utilities."""
from __future__ import annotations

from typing import Dict, List, Any
import yaml


# Type aliases
CostModels = Dict[str, Any]
Item = Dict[str, Any]


def load_cost_models(path: str = "config/cost_models.yaml") -> CostModels:
    """Load pricing models from a YAML file.

    Parameters
    ----------
    path:
        Path to the YAML file containing model pricing information.

    Returns
    -------
    dict
        Parsed cost model data.
    """
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def _compute_cost(item: Item, pricing: Dict[str, float]) -> float:
    """Compute cost for a single item given pricing information."""
    pt = item.get("prompt_tokens", 0)
    ct = item.get("completion_tokens", 0)
    cost = (
        pt * pricing.get("input_price_per_1k", 0.0) / 1000.0
        + ct * pricing.get("output_price_per_1k", 0.0) / 1000.0
    )
    min_charge = pricing.get("min_charge_usd", 0.0)
    if cost < min_charge:
        cost = min_charge
    return cost


def simulate(
    items: List[Item],
    cost_models: CostModels,
    *,
    provider: str,
    model: str,
) -> Dict[str, Any]:
    """Simulate token usage costs.

    Parameters
    ----------
    items:
        List of items representing token usage.
    cost_models:
        Loaded cost model data.
    provider:
        Provider name.
    model:
        Model name.

    Returns
    -------
    dict
        Simulation result containing per-item details and totals.
    """

    pricing = cost_models["providers"][provider][model]

    result_items: List[Item] = []
    totals = {"cost_usd": 0.0, "tokens": 0, "latency_ms": 0.0}

    for item in items:
        tokens = int(item.get("prompt_tokens", 0) + item.get("completion_tokens", 0))
        cost = _compute_cost(item, pricing)
        latency = float(item.get("latency_ms", 0.0))
        route_explain = {
            "decision": "simulate",
            "cost_usd": cost,
            "tokens": tokens,
            "latency_ms": latency,
        }
        enriched = {
            **item,
            "cost_usd": cost,
            "tokens": tokens,
            "route_explain": route_explain,
        }
        result_items.append(enriched)
        totals["cost_usd"] += cost
        totals["tokens"] += tokens
        totals["latency_ms"] += latency

    return {
        "provider": provider,
        "model": model,
        "items": result_items,
        "totals": totals,
    }
