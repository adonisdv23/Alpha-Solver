from __future__ import annotations
import csv
import json
from pathlib import Path
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


_WEIGHTS_CACHE: Dict[str, Dict[str, float]] | None = None
_PRIORS_CACHE: Dict[str, float] | None = None
_CANON_CACHE: Dict[str, Dict[str, Any]] | None = None


def _load_weights() -> Dict[str, Dict[str, float]]:
    global _WEIGHTS_CACHE
    if _WEIGHTS_CACHE is not None:
        return _WEIGHTS_CACHE
    path = Path("config/scoring_weights.json")
    data = {}
    if path.exists():
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            data = {}
    _WEIGHTS_CACHE = {k: {kk: float(vv) for kk, vv in v.items()} for k, v in data.items()} if isinstance(data, dict) else {}
    return _WEIGHTS_CACHE


def _load_priors() -> Dict[str, float]:
    global _PRIORS_CACHE
    if _PRIORS_CACHE is not None:
        return _PRIORS_CACHE
    path = Path("config/priors.yaml")
    data = {}
    if path.exists():
        from .loader import parse_yaml_lite
        data = parse_yaml_lite(path.read_text(encoding="utf-8"))
    boosts = data.get("boosts", {}) if isinstance(data, dict) else {}
    _PRIORS_CACHE = {k: float(v) for k, v in boosts.items()}
    return _PRIORS_CACHE


def _load_canon() -> Dict[str, Dict[str, Any]]:
    global _CANON_CACHE
    if _CANON_CACHE is not None:
        return _CANON_CACHE
    canon: Dict[str, Dict[str, Any]] = {}
    for p in [Path("registries/tools_canon.csv"), Path("artifacts/tools_canon.csv")]:
        if p.exists():
            try:
                with p.open(newline="", encoding="utf-8") as f:
                    for row in csv.DictReader(f):
                        key = row.get("key")
                        if key:
                            canon[key] = row
            except Exception:
                pass
            break
    _CANON_CACHE = canon
    return _CANON_CACHE

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

    weights = _load_weights()
    priors = _load_priors()
    w_cfg = weights.get(region, weights.get("default", {}))
    w_base = _as_float(w_cfg.get("base", 1.0))
    w_syn = _as_float(w_cfg.get("synergy", 1.0))
    w_conf = _as_float(w_cfg.get("confidence", 0.0))
    vendor_penalty = _as_float(w_cfg.get("vendor_penalty", 0.0))

    bonus = 0.1 if clusters else 0.0
    canon = _load_canon()

    enriched: List[Dict[str, Any]] = []
    for t in eligible:
        base = _as_float(t.get("router_value", 0))
        confidence = _as_float(t.get("confidence", 0))
        item = dict(t)
        item["score_base"] = base
        item["synergy_bonus"] = bonus
        score = base * w_base + bonus * w_syn + confidence * w_conf - vendor_penalty
        tags = t.get("tags") or []
        boost = 0.0
        matched = []
        for tag in tags:
            if tag in priors:
                boost += priors[tag]
                matched.append(tag)
        if boost > 0.1:
            boost = 0.1
        score += boost
        reasons = dict(item.get("reasons", {}))
        reasons["region_filter"] = "allowed"
        reasons["synergy_notes"] = "clusters bonus applied" if bonus else ""
        if matched:
            reasons["priors"] = {m: priors[m] for m in matched}
        if boost:
            reasons["prior_boost"] = boost

        key = f"{t.get('id', '')}:{t.get('vendor_id', '')}"
        canon_row = canon.get(key)
        if canon_row:
            enrichment = {
                k: canon_row.get(k)
                for k in ("category", "popularity", "sentiment")
                if canon_row.get(k) is not None
            }
            item["enrichment"] = enrichment
            pop = _as_float(canon_row.get("popularity", 0))
            pop_bonus = min(pop, 0.1)
            if pop_bonus:
                score += pop_bonus
                reasons["popularity_bonus"] = pop_bonus
        item["final_score"] = score
        item["score"] = score
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
