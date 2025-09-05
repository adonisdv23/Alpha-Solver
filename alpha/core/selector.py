from __future__ import annotations
from typing import Any, Dict, List

# REGISTRY_CACHE is populated elsewhere; we only read from it here.
try:
    from .loader import REGISTRY_CACHE
except Exception:
    REGISTRY_CACHE = {}

def _ensure_list(obj):
    return obj if isinstance(obj, list) else []

def _get_tools_list() -> List[Dict[str, Any]]:
    raw = REGISTRY_CACHE.get("tools", {})
    if isinstance(raw, dict):
        items = raw.get("tools", [])
    elif isinstance(raw, list):
        items = raw
    else:
        items = []
    return _ensure_list(items)

def _as_float(x) -> float:
    try:
        return float(x)
    except Exception:
        return 0.0

def rank_from(rows: List[Dict[str, Any]], top_k: int = 5) -> List[Dict[str, Any]]:
    """
    Rank a list of tool dicts by router_value (desc), tie-break by id.
    Used by tools-canon flow.
    """
    rows = _ensure_list(rows)
    return sorted(
        rows,
        key=lambda t: (-_as_float(t.get("router_value", 0)), str(t.get("id", "")))
    )[:top_k]

def rank_region(
    tools: List[Dict[str, Any]],
    region: str = "",
    top_k: int = 5,
    clusters: Dict[str, Any] | None = None,
) -> List[Dict[str, Any]]:
    """
    Region-aware ranking with simple explanations:
      • In EU, exclude vendor_id 'cn_state_cloud'.
      • Add a small positive synergy_bonus when a clusters map is provided.
      • Return detailed scoring fields and reason annotations.
    """
    region = (region or "").upper()
    banned_vendors_in_eu = {"cn_state_cloud"}

    def allowed(t: Dict[str, Any]) -> bool:
        vid = (t.get("vendor_id") or "").lower()
        if region == "EU" and vid in banned_vendors_in_eu:
            return False
        return True

    eligible = [t for t in _ensure_list(tools) if allowed(t)]

    # Minimal synergy signal the test expects.
    bonus = 0.1 if clusters else 0.0

    enriched: List[Dict[str, Any]] = []
    for t in eligible:
        base = _as_float(t.get("router_value", 0))
        item = dict(t)  # shallow copy
        item["score_base"] = base
        item["synergy_bonus"] = bonus
        final = base + bonus
        item["final_score"] = final
        item["score"] = final  # backwards compatible
        reasons = dict(item.get("reasons", {}))
        reasons["region_filter"] = "allowed"
        reasons["synergy_notes"] = "clusters bonus applied" if bonus else ""
        item["reasons"] = reasons
        enriched.append(item)

    ranked = sorted(
        enriched,
        key=lambda t: (-_as_float(t.get("final_score", 0)), str(t.get("id", "")))
    )
    top = ranked[:top_k]

    # Annotate ties among returned items
    score_groups: Dict[float, List[Dict[str, Any]]] = {}
    for item in top:
        score_groups.setdefault(item["final_score"], []).append(item)
    for group in score_groups.values():
        ids = sorted(t.get("id", "") for t in group)
        for item in group:
            item.setdefault("reasons", {})
            item["reasons"]["ties"] = [i for i in ids if i != item.get("id", "")]

    # Confidence scaled to top score
    max_score = max((t["final_score"] for t in top), default=0.0)
    for item in top:
        conf = (item["final_score"] / max_score) if max_score > 0 else 0.0
        item["confidence"] = max(0.0, min(1.0, conf))

    return top

def rank(top_k: int = 5) -> List[Dict[str, Any]]:
    """
    Fallback ranking from the in-memory REGISTRY_CACHE.
    Deterministic: sort lexicographically by id/name/slug.
    """
    tools = _get_tools_list()

    def to_key(t: Any) -> str:
        if isinstance(t, dict):
            return str(t.get("id") or t.get("name") or t.get("slug") or t)
        return str(t)

    return sorted(tools, key=to_key)[:top_k]
