from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple

from .semantic import hybrid_score

"""RegistryProvider with lexical scoring + priors + telemetry (stdlib only)."""

try:
    from alpha.core import freshness
except Exception:  # pragma: no cover - safety
    freshness = None

class RegistryProvider:
    def __init__(
        self,
        seed_path: str | None = None,
        schema_path: str | None = None,
        telemetry_path: Optional[str] = None,
    ) -> None:
        self.seed_path = seed_path or "registries/registry_seed_v0_7_0.jsonl"
        self.schema_path = schema_path
        self.telemetry_path = telemetry_path or "telemetry/registry_usage.jsonl"
        self.rows: List[Dict[str, Any]] = []
        path = os.getenv("ALPHA_RECENCY_PRIORS_PATH")
        if freshness and path:
            self._dated = freshness.load_dated_priors(path)
        else:
            self._dated = {}
        self._now_utc = getattr(self, "_now_utc", datetime.now(timezone.utc))
        self._recency_weight = float(os.getenv("ALPHA_RECENCY_WEIGHT", "0.15"))
        self._recency_halflife_days = float(
            os.getenv("ALPHA_RECENCY_HALFLIFE_DAYS", "90")
        )

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
    def _apply_region_weight(self, score: float, region: str) -> float:
        import json
        import os

        path = os.getenv("ALPHA_REGION_WEIGHTS_PATH")
        if not path:
            return score
        try:
            cache = getattr(self, "_region_weights_cache", None)
            if cache is None:
                with open(path, "r", encoding="utf-8") as f:
                    cache = json.load(f)
                setattr(self, "_region_weights_cache", cache)
            w = float(cache.get(region, 1.0))
            return score * w
        except Exception:
            return score

    def shortlist(self, query: str, region: Optional[str] = None, k: int = 5) -> List[Dict[str, Any]]:
        if not self.rows:
            self.load()
        qt = self._tokens(query or "")
        candidates: List[Dict[str, Any]] = []
        for r in self.rows:
            bag = self._bag_from_row(r)
            lexical_score = (len(qt & bag) / max(1, len(qt))) if (qt and bag) else 0.0
            candidate_text = " ".join(self._iter_texts(r) or [])
            semantic_score = hybrid_score(query or "", candidate_text, lexical_score)
            sentiment, adoption, risk, cost = self._derive_priors(r)
            prior = sentiment * adoption * (1.0 - risk) + cost
            hybrid = semantic_score * prior
            parts = {
                "lexical": float(lexical_score),
                "semantic": float(semantic_score),
                "priors": float(prior or 0.0),
                "recency": 0.0,
            }
            final_score = hybrid
            tool_id = r.get("id") or r.get("vendor_id") or r.get("name")
            rdt = (
                getattr(self, "_dated", None).get(tool_id)
                if (getattr(self, "_dated", None) and freshness)
                else None
            )
            if rdt:
                rf = freshness.recency_factor(
                    rdt, now=self._now_utc, half_life_days=self._recency_halflife_days
                )
                parts["recency"] = float(rf)
                final_score = freshness.blend(hybrid, rf, self._recency_weight)
            if region:
                regions = r.get("regions")
                if isinstance(regions, list) and regions:
                    norm = {str(x).strip().upper() for x in regions}
                    if region.upper() not in norm and "GLOBAL" not in norm:
                        final_score *= 0.8
            final_score = self._apply_region_weight(final_score, region or "")
            row = {
                "tool_id": tool_id,
                "name": r.get("name"),
                "score": final_score,
                "_parts": parts,
            }
            candidates.append(row)

        candidates.sort(key=lambda x: (-x["score"], str(x["tool_id"])) )
        ranked = candidates[: max(1, int(k))]

        try:
            self._log(query, candidates[:20], ranked)
        except Exception:
            pass

        if ranked:
            scores = [r["score"] for r in ranked]
            lo, hi = min(scores), max(scores)
            span = (hi - lo) or 1.0
            for r in ranked:
                r["confidence"] = (r["score"] - lo) / span
                p = r.get("_parts")
                if p:
                    r["explain"] = {
                        "lexical": round(p["lexical"], 6),
                        "semantic": round(p["semantic"], 6),
                        "priors": round(p["priors"], 6),
                        "recency": round(p["recency"], 6),
                        "total": round(r["score"], 6),
                    }
                    r["reason"] = (
                        f"lex {p['lexical']:.2f} + sem {p['semantic']:.2f} + "
                        f"pri {p['priors']:.2f} + rec {p['recency']:.2f}"
                    )
        return ranked

    def rank(self, query: str, top_k: int, region: Optional[str] = None) -> List[Dict[str, Any]]:
        res = self.shortlist(query=query, region=region, k=top_k)
        out: List[Dict[str, Any]] = []
        for r in res:
            out.append({"id": r.get("tool_id"), "name": r.get("name"), "score": r.get("score")})
        return out

    # ------------ telemetry ------------
    def _log(self, query: str, candidates: List[Dict[str, Any]], selected: List[Dict[str, Any]]) -> None:
        rec = {
            "ts": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
            "query": query,
            "candidates": [
                {"id": c.get("tool_id") or c.get("id"), "score": round(float(c["score"]), 6)}
                for c in candidates
            ],
            "selected": [
                {"id": s.get("tool_id") or s.get("id"), "score": round(float(s["score"]), 6)}
                for s in selected
            ],
            "rationale": "lex + sem + priors + recency",
        }
        tp = Path(self.telemetry_path or "telemetry/registry_usage.jsonl")
        tp.parent.mkdir(parents=True, exist_ok=True)
        with tp.open("a", encoding="utf-8") as f:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
