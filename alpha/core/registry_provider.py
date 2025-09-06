from __future__ import annotations
import os
from .semantic import hybrid_score


"""RegistryProvider with lexical scoring + priors + telemetry (stdlib only)."""

from pathlib import Path
from datetime import datetime, timezone
from typing import Any, Dict, Iterable, List, Optional, Tuple
import json

try:
    from . import freshness
except Exception:  # pragma: no cover - safety
    freshness = None

class RegistryProvider:
    def __init__(self, seed_path: str, schema_path: str, telemetry_path: Optional[str] = None):
        self.seed_path = seed_path
        self.schema_path = schema_path
        self.telemetry_path = telemetry_path or "telemetry/registry_usage.jsonl"
        self.rows: List[Dict[str, Any]] = []
        # optional recency priors
        path = os.getenv("ALPHA_RECENCY_PRIORS_PATH")
        if freshness and path:
            self._dated = freshness.load_dated_priors(path)
        else:
            self._dated = {}
        try:
            self._recency_weight = float(os.getenv("ALPHA_RECENCY_WEIGHT", "0.15"))
        except Exception:
            self._recency_weight = 0.15
        try:
            self._recency_halflife = float(os.getenv("ALPHA_RECENCY_HALFLIFE_DAYS", "90"))
        except Exception:
            self._recency_halflife = 90.0

    # ------------ load ------------
    def load(self) -> None:
        p = Path(self.seed_path)
        self.rows = []
        if not p.exists():
            return
        with p.open("r", encoding="utf-8") as f:
            for raw in f:
                line = (raw or "").strip()
                if not line:
                    continue
                try:
                    obj = json.loads(line)
                    # normalize strings
                    for k, v in list(obj.items()):
                        if isinstance(v, str):
                            obj[k] = v.strip()
                    # normalize list-like fields
                    for field in (
                        "tags","keywords","capabilities","core_capabilities",
                        "best_integration_scenarios","limitations","risk_flags",
                        "compliance_scope","regions"
                    ):
                        v = obj.get(field)
                        if isinstance(v, str):
                            toks = [t.strip() for t in v.replace("|",",").replace(";",",").split(",") if t.strip()]
                            obj[field] = toks
                    # precompute lexical bag
                    obj["_lex_bag"] = self._tokens(" ".join(self._iter_texts(obj) or []))
                    self.rows.append(obj)
                except Exception:
                    pass

    # ------------ helpers ------------
    @staticmethod
    def _tokens(text: str) -> set:
        return set("".join(ch.lower() if ch.isalnum() else " " for ch in text).split())

    @staticmethod
    def _iter_texts(obj: Any) -> Iterable[str]:
        if obj is None:
            return
        if isinstance(obj, str):
            yield obj
        elif isinstance(obj, (list, tuple, set)):
            for x in obj:
                for y in RegistryProvider._iter_texts(x):
                    yield y
        elif isinstance(obj, dict):
            for v in obj.values():
                for y in RegistryProvider._iter_texts(v):
                    yield y

    def _bag_from_row(self, row: Dict[str, Any]) -> set:
        bag = row.get("_lex_bag")
        if isinstance(bag, set):
            return bag
        return self._tokens(" ".join(self._iter_texts(row) or []))

    def _derive_priors(self, row: Dict[str, Any]) -> Tuple[float, float, float, float]:
        # sentiment_prior
        sp = row.get("sentiment_prior")
        if isinstance(sp, (int, float)):
            sentiment = float(sp)
        else:
            s10 = row.get("sentiment_score_0_10")
            try:
                sentiment = max(0.0, min(1.0, float(s10) / 10.0))
            except Exception:
                sentiment = 0.5

        # adoption_prior
        ap = row.get("adoption_prior")
        if isinstance(ap, (int, float)):
            adoption = float(ap)
        else:
            level = str(row.get("adoption_level") or "").strip().lower()
            adoption = {"dominant": 0.9, "established": 0.75, "growing": 0.6, "early": 0.5}.get(level, 0.5)

        # risk penalty (lower is better)
        rp = row.get("risk_penalty")
        if isinstance(rp, (int, float)):
            risk = max(0.0, min(1.0, float(rp)))
        else:
            flags = row.get("risk_flags") or []
            risk = min(0.4, 0.05 * (len(flags) if isinstance(flags, list) else 0))

        # cost bonus (adds directly)
        cb = row.get("cost_bonus")
        cost = float(cb) if isinstance(cb, (int, float)) else 0.0

        return (sentiment, adoption, risk, cost)

    # ------------ scoring / ranking ------------
    def score(self, query: str, row: Dict[str, Any]) -> float:
        qt = self._tokens(query or "")
        bag = self._bag_from_row(row)
        fit = (len(qt & bag) / max(1, len(qt))) if (qt and bag) else 0.0
        fit = max(0.0, min(1.0, fit))
        sentiment, adoption, risk, cost = self._derive_priors(row)
        return float(max(-1.0, min(1.0, fit * sentiment * adoption * (1.0 - risk) + cost)))

    def rank(self, query: str, top_k: int, region: Optional[str] = None) -> List[Dict[str, Any]]:
        candidates: List[Dict[str, Any]] = []
        utc_now = datetime.now(timezone.utc)
        for r in self.rows:
            sc = self.score(query, r)
            if region:
                regions = r.get("regions")
                if isinstance(regions, list) and regions:
                    norm = {str(x).strip().upper() for x in regions}
                    if region.upper() not in norm and "GLOBAL" not in norm:
                        sc *= 0.8
            tid = r.get("id") or r.get("vendor_id") or r.get("name")
            if tid and self._dated:
                rdt = self._dated.get(str(tid))
                if rdt and freshness:
                    rfac = freshness.recency_factor(
                        rdt, now=utc_now, half_life_days=self._recency_halflife
                    )
                    sc = freshness.blend(sc, rfac, self._recency_weight)
            candidates.append({
                "id": tid,
                "name": r.get("name"),
                "score": sc,
            })

        candidates.sort(key=lambda x: x["score"], reverse=True)
        out = candidates[: max(1, int(top_k))]

        try:
            self._log(query, candidates[:20], out)
        except Exception:
            pass

        return out

    # ------------ telemetry ------------
    def _log(self, query: str, candidates: List[Dict[str, Any]], selected: List[Dict[str, Any]]) -> None:
        rec = {
            "ts": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
            "query": query,
            "candidates": [{"id": c["id"], "score": round(float(c["score"]), 6)} for c in candidates],
            "selected": [{"id": s["id"], "score": round(float(s["score"]), 6)} for s in selected],
            "rationale": "lexical_match * sentiment * adoption * (1-risk) + cost_bonus",
        }
        tp = Path(self.telemetry_path or "telemetry/registry_usage.jsonl")
        tp.parent.mkdir(parents=True, exist_ok=True)
        with tp.open("a", encoding="utf-8") as f:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
