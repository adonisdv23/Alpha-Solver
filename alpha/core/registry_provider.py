"""Minimal RegistryProvider (stdlib only)."""
from __future__ import annotations

from pathlib import Path
from datetime import datetime, timezone
from typing import List, Dict, Any, Optional
import json

class RegistryProvider:
    """
    Loads a JSONL registry (one JSON object per line), ranks rows for a query, and logs lookups.
    Scoring:
        score = fit * sentiment_prior * adoption_prior * (1 - risk_penalty) + cost_bonus
    If 'fit' is missing, compute lexical fit from name/category/tags/capabilities/description.
    """
    def __init__(self, seed_path: str, schema_path: str, telemetry_path: Optional[str] = None):
        self.seed_path = seed_path
        self.schema_path = schema_path
        self.telemetry_path = telemetry_path or "telemetry/registry_usage.jsonl"
        self.rows: List[Dict[str, Any]] = []

    # ---- loading ----
    def load(self) -> None:
        p = Path(self.seed_path)
        self.rows = []
        if not p.exists():
            return
        with p.open("r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    obj = json.loads(line)
                    # light normalization (trim strings)
                    for k, v in list(obj.items()):
                        if isinstance(v, str):
                            obj[k] = v.strip()
                    self.rows.append(obj)
                except Exception:
                    # ignore malformed lines (keep minimal and stdlib-only)
                    pass

    # ---- scoring helpers ----
    @staticmethod
    def _lex(s: str) -> set:
        return set("".join(ch.lower() if ch.isalnum() else " " for ch in s).split())

    def score(self, query: str, row: Dict[str, Any]) -> float:
        fit = row.get("fit")
        if not isinstance(fit, (int, float)):
            bag: List[str] = []
            for k in ("name", "category", "tags", "capabilities", "description"):
                v = row.get(k)
                if isinstance(v, str):
                    bag.append(v)
                elif isinstance(v, list):
                    bag.extend(str(x) for x in v)
            qt, ct = self._lex(query), self._lex(" ".join(bag))
            overlap = len(qt & ct)
            fit = min(1.0, overlap / max(1, len(qt)))

        sentiment = float(row.get("sentiment_prior", 0.5) or 0.5)
        adoption  = float(row.get("adoption_prior", 0.5) or 0.5)
        risk_pen  = float(row.get("risk_penalty", 0.0) or 0.0)
        cost_bonus= float(row.get("cost_bonus", 0.0) or 0.0)

        try:
            s = fit * sentiment * adoption * (1 - risk_pen) + cost_bonus
        except Exception:
            s = 0.0
        return float(max(-1.0, min(1.0, s)))

    # ---- ranking & telemetry ----
    def rank(self, query: str, top_k: int, region: Optional[str] = None) -> List[Dict[str, Any]]:
        scored: List[Dict[str, Any]] = []
        for r in self.rows:
            sc = self.score(query, r)
            scored.append({
                "id": r.get("id") or r.get("vendor_id") or r.get("name"),
                "name": r.get("name"),
                "vendor_id": r.get("vendor_id"),
                "score": sc,
            })
        scored.sort(key=lambda x: (-x["score"], x.get("name") or ""))
        selected = scored[: max(0, int(top_k))]

        self.log_event({
            "query": query,
            "candidates": [{"id": c["id"], "score": c["score"]} for c in scored[:50]],
            "selected":   [{"id": s["id"], "score": s["score"]} for s in selected],
            "rationale": f"ranked {len(scored)} candidates",
        })
        return selected

    def log_event(self, event: Dict[str, Any]) -> None:
        try:
            Path(self.telemetry_path).parent.mkdir(parents=True, exist_ok=True)
            ev = {
                "ts": datetime.now(timezone.utc).isoformat().replace("+00:00","Z"),
                **event,
            }
            with Path(self.telemetry_path).open("a", encoding="utf-8") as f:
                f.write(json.dumps(ev, ensure_ascii=False) + "\n")
        except Exception:
            # never throw from telemetry
            pass
