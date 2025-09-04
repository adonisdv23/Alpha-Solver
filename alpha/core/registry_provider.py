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
PY          passver throw from telemetrynsure_ascii=False) + "\n")-8") as f:","Z"),]],
@adonisdv23 ➜ /workspaces/Alpha-Solver (main) $ python - <<'PY'
from pathlib import Path, re
p = Path("Alpha Solver.py")
s = p.read_text(encoding="utf-8")

# Ensure "from pathlib import Path" and timezone import exist
if "from pathlib import Path" not in s:
    s = s.replace("from dataclasses import dataclass, field, asdict",
                  "from dataclasses import dataclass, field, asdict\nfrom pathlib import Path")
if "from datetime import datetime, timezone" not in s and "from datetime import datetime" in s:
    s = s.replace("from datetime import datetime", "from datetime import datetime, timezone")

# Add argparse flags if missing
if "--registry-seed" not in s and 'parser.add_argument("--domain", default="")' in s:
    s = s.replace(
        'parser.add_argument("--domain", default="")',
        'parser.add_argument("--domain", default="")\n'
        '    parser.add_argument("--registry-seed", default="")\n'
        '    parser.add_argument("--registry-schema", default="schemas/registry_schema_v1.json")\n'
        '    parser.add_argument("--registry-telemetry", default="telemetry/registry_usage.jsonl")'
    )

# Add ctor params if missing
if "registry_seed: str" not in s:
    s = re.sub(
        r"def __init__\(([^)]*)\):",
        r"def __init__(\1, registry_seed: str = \"\", registry_schema: str = \"schemas/registry_schema_v1.json\", registry_telemetry: str = \"telemetry/registry_usage.jsonl\"):",
        s, count=1)

# Add assignments + provider init if missing
if "self.registry_provider = None" not in s and "self.domain = domain" in s:
    s = s.replace(
        "self.domain = domain",
        ("self.domain = domain\n"
         "        self.registry_seed = registry_seed\n"
         "        self.registry_schema = registry_schema\n"
         "        self.registry_telemetry = registry_telemetry\n"
         "        self.registry_provider = None\n"
         "        try:\n"
         "            if self.registry_seed and Path(self.registry_seed).exists():\n"
         "                from alpha.core.registry_provider import RegistryProvider\n"
         "                self.registry_provider = RegistryProvider(self.registry_seed, self.registry_schema, self.registry_telemetry)\n"
         "                self.registry_provider.load()\n"
         "        except Exception as e:  # pragma: no cover\n"
         "            logger.warning(f\"registry provider init failed: {e}\")")
    )

# Prefer provider before tools_canon
if "elif self.registry_provider:" not in s and "elif self.tools_canon_path:" in s:
    s = s.replace(
        "elif self.tools_canon_path:",
        ("elif self.registry_provider:\n"
         "                shortlist = self.registry_provider.rank(query, self.k, region=self.region or None)\n"
         "                source = \"registry\"\n"
         "            elif self.tools_canon_path:")
    )

# Pass new args into AlphaSolver(...) construction
if "registry_seed=args.registry_seed" not in s:
    s = s.replace(
        "solver = AlphaSolver(",
        "solver = AlphaSolver(")
    s = s.replace(
        "domain=args.domain)",
        "domain=args.domain,\n"
        "                         registry_seed=args.registry_seed,\n"
        "                         registry_schema=args.registry_schema,\n"
        "                         registry_telemetry=args.registry_telemetry)"
    )

p.write_text(s, encoding="utf-8")
print("patched Alpha Solver.py")
