"""Canonical default configuration for Alpha Solver."""

from __future__ import annotations

from typing import Any, Dict

# Default values mirror `_tree_of_thought` keyword arguments.  They are kept in a
# single location so tests and loaders can import them consistently.
DEFAULT_CONFIG: Dict[str, Any] = {
    "seed": 42,
    "branching_factor": 3,
    "score_threshold": 0.70,
    "max_depth": 5,
    "timeout_s": 10,
    "dynamic_prune_margin": 0.15,
    "low_conf_threshold": 0.60,
    "enable_cot_fallback": True,
    "max_cot_steps": 4,
    "multi_branch": False,
    "max_width": 3,
    "max_nodes": 100,
    "enable_progressive_router": False,
    "router_min_progress": 0.3,
    "router_escalation": ("basic", "structured", "constrained"),
    "enable_agents_v12": False,
    "agents_v12_order": ("decomposer", "checker", "calculator"),
    "scorer": "composite",
    "scorer_weights": {"lexical": 0.6, "constraint": 0.4},
    "enable_cache": True,
    "cache_path": "artifacts/cache/tot_cache.json",
}
