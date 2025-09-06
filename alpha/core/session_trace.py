from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Any


def write_session_trace(trace: Dict[str, Any]) -> Path:
    art_root = Path(os.environ.get("ALPHA_ARTIFACTS_DIR", "artifacts"))
    art_root.mkdir(parents=True, exist_ok=True)
    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    path = art_root / "run" / f"run_{ts}.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    rec: Dict[str, Any] = {
        "schema_version": "v1",
        "queries_source": trace.get("queries_source"),
        "regions": trace.get("regions", []),
        "seed": trace.get("seed"),
        "shortlist_paths": trace.get("shortlist_paths", []),
        "env_snapshot_path": trace.get("env_snapshot_path"),
        "started_at": trace.get("started_at"),
        "ended_at": trace.get("ended_at"),
    }
    code_version = os.getenv("GIT_COMMIT_SHA")
    if code_version:
        rec["code_version"] = code_version
    with path.open("w", encoding="utf-8") as f:
        json.dump(rec, f, ensure_ascii=False, sort_keys=True)
    return path
