"""Adapter dispatcher using local prompt templates."""
from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict

from alpha.core.determinism import apply_seed
from . import prompts


def _timestamp() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def run(adapter: str, payload: Dict[str, Any], seed: int | None = None) -> Dict[str, Any]:
    builder = prompts.TEMPLATES.get(adapter)
    if builder is None:
        raise ValueError("unknown adapter")
    if seed is None:
        seed = int(os.getenv("ALPHA_SEED", "0"))
    if os.getenv("ALPHA_DETERMINISM") == "1":
        seed = apply_seed(seed)
    prompt = builder(**payload)
    ts = _timestamp()
    art_root = Path(os.getenv("ALPHA_ARTIFACTS_DIR", "artifacts"))
    trace_dir = art_root / "exec"
    trace_dir.mkdir(parents=True, exist_ok=True)
    ts_safe = ts.replace(":", "").replace("-", "")
    trace_path = trace_dir / f"{adapter}_{ts_safe}.json"
    record = {"adapter": adapter, "seed": seed, "prompt": prompt, "ts": ts}
    trace_path.write_text(json.dumps(record, ensure_ascii=False, sort_keys=True), encoding="utf-8")
    return {"prompt": prompt, "seed": seed, "trace_path": str(trace_path)}
