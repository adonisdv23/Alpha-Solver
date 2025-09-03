"""Tool selection"""
from typing import List, Dict
from .loader import REGISTRY_CACHE
from .regions import RegionPolicy

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


def rank_region(tools: List[Dict], region: str, top_k: int = 5, clusters: Dict = None) -> List[Dict]:
    rp = RegionPolicy(REGISTRY_CACHE)
    cluster_list = clusters.get("clusters", []) if clusters else []
    scored: List[Dict] = []
    for t in tools:
        vendor = t.get("vendor_id")
        if vendor and not rp.allowed(vendor, region):
            continue
        rv = float(t.get("router_value", 0) or 0)
        score = rv * 100
        tier = t.get("tier")
        if str(tier) == "1" or tier == 1:
            score += 2
        synergy_bonus = 0.0
        tid = t.get("id")
        for cl in cluster_list:
            if tid in cl.get("members", []):
                synergy_bonus = cl.get("router_value_bonus", 0)
                score += synergy_bonus
                break
        reasons = {
            "router_value": rv,
            "tier": tier,
            "synergy_bonus": synergy_bonus,
            "region_fit": True,
        }
        item = dict(t)
        item["score"] = score
        item["reasons"] = reasons
        scored.append(item)
    sorted_tools = sorted(scored, key=lambda x: (-x["score"], x.get("name", "")))
    return sorted_tools[:top_k]
