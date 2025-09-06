#!/usr/bin/env python3
from __future__ import annotations
import json, os
from datetime import datetime, timezone
from typing import Dict, Optional

RFC3339_FALLBACKS = ("%Y-%m-%d", "%Y-%m-%dT%H:%M:%S%z", "%Y-%m-%dT%H:%M:%SZ")

def _parse_dt(s: str) -> Optional[datetime]:
    s = str(s).strip()
    for fmt in RFC3339_FALLBACKS:
        try:
            if fmt.endswith("Z"):
                if s.endswith("Z"):
                    return datetime.strptime(s, fmt).replace(tzinfo=timezone.utc)
                continue
            dt = datetime.strptime(s, fmt)
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)
            return dt.astimezone(timezone.utc)
        except Exception:
            continue
    try:
        # last resort: fromisoformat with Z→+00:00
        return datetime.fromisoformat(s.replace("Z", "+00:00")).astimezone(timezone.utc)
    except Exception:
        return None

def load_dated_priors(path: Optional[str]) -> Dict[str, datetime]:
    """Load tool_id -> last_updated datetime map. Returns empty on None/missing/invalid."""
    if not path or not os.path.exists(path):
        return {}
    with open(path, "r", encoding="utf-8") as f:
        raw = json.load(f)
    out: Dict[str, datetime] = {}
    if isinstance(raw, dict):
        it = raw.items()
    else:
        # also allow list of {tool_id, last_updated}
        it = ((r.get("tool_id"), r.get("last_updated")) for r in raw if isinstance(r, dict))
    for tid, date_s in it:
        if not tid or not date_s:
            continue
        dt = _parse_dt(date_s)
        if dt:
            out[str(tid)] = dt
    return out

def recency_factor(last_updated: datetime, now: Optional[datetime]=None, half_life_days: float=90.0) -> float:
    """Return [0,1] where 1.0 is very recent; simple exponential decay by half-life."""
    now = now or datetime.now(timezone.utc)
    age_days = max(0.0, (now - last_updated).total_seconds() / 86400.0)
    # factor = 0.5 ** (age / half_life)
    return float(0.5 ** (age_days / max(1e-6, half_life_days)))

def blend(base_score: float, recency: float, weight: float) -> float:
    """Deterministic convex blend; weight in [0,1]."""
    w = min(1.0, max(0.0, weight))
    return (1.0 - w) * float(base_score) + w * float(recency)
