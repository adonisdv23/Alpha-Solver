"""Tool selection"""
from typing import List, Dict
from .loader import REGISTRY_CACHE

def rank(top_k: int = 5) -> List[Dict]:
    tools = REGISTRY_CACHE.get("tools", {}).get("tools", [])
    sorted_tools = sorted(
        tools,
        key=lambda t: (-t.get("router_value", 0), -t.get("tier", 0), t.get("name", ""))
    )
    return sorted_tools[:top_k]


def rank_from(tools: List[Dict], top_k: int = 5) -> List[Dict]:
    scored: List[Dict] = []
    for t in tools:
        score = float(t.get("router_value", 0) or 0) * 100
        if str(t.get("tier")) == "1" or t.get("tier") == 1:
            score += 2
        item = dict(t)
        item["score"] = score
        scored.append(item)
    sorted_tools = sorted(scored, key=lambda x: (-x["score"], x.get("name", "")))
    return sorted_tools[:top_k]
