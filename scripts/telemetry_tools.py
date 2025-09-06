
from __future__ import annotations

import json
import hashlib
import os
from pathlib import Path
import datetime as dt
from typing import Iterable, Dict, Any


# ---------- time helpers ----------
def now_rfc3339_z() -> str:
    """UTC timestamp like 2025-09-05T12:34:56Z."""
    return dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


# ---------- small utils ----------
def sha1_query(q: str) -> str:
    try:
        return hashlib.sha1((q or "").encode("utf-8")).hexdigest()
    except Exception:
        return ""


def _scrub_record(d: dict) -> dict:
    import os as _os
    if not d or _os.getenv("ALPHA_TELEMETRY_SCRUB", "0") != "1":
        return d
    fields = _os.getenv("ALPHA_TELEMETRY_SCRUB_FIELDS", "")
    deny = [s.strip() for s in fields.split(",") if s.strip()] or [
        "query_text",
        "raw_prompt",
        "user_input",
        "notes",
    ]
    out = dict(d)
    for k in deny:
        if k in out:
            v = out[k]
            out[k] = "***SCRUBBED***" if isinstance(v, str) else None
    return out


def _append_jsonl(path: str, obj: Dict[str, Any]) -> None:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("a", encoding="utf-8") as f:
        f.write(json.dumps(_scrub_record(obj), ensure_ascii=False) + "\n")


def rotate_if_too_big(path: str, max_mb: int = 5) -> None:
    """Rotate JSONL if it grows beyond max_mb. Creates <name>.<ts>.jsonl"""
    p = Path(path)
    if not p.exists():
        return
    if p.stat().st_size <= max_mb * 1024 * 1024:
        return
    ts = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%d-%H%M%S")
    p.rename(p.with_name(f"{p.stem}.{ts}{p.suffix}"))


# ---------- header + enrichment ----------
def write_run_header(path: str,
                     regions: Iterable[str] | None = None,
                     queries_source: str = "args",
                     code_version: str = "") -> str:
    """Write a run_header line and return a short run_id."""
    rotate_if_too_big(path)
    regions = list(regions or [])
    run_id = __import__("uuid").uuid4().hex
    header = {
        "type": "run_header",
        "run_id": run_id,
        "ts": now_rfc3339_z(),
        "regions": regions,
        "queries_source": queries_source,
        "code_version": code_version or os.getenv("GIT_COMMIT_SHA", ""),
    }
    _append_jsonl(path, header)
    return run_id


def ensure_run_header(path: str,
                      run_id: str,
                      regions: Iterable[str] | None = None,
                      queries_source: str = "args",
                      code_version: str = "") -> None:
    """If file missing/empty/first-line isn't a header, prepend one."""
    p = Path(path)
    if not p.exists():
        write_run_header(path, regions=regions or [], queries_source=queries_source, code_version=code_version)
        return

    lines = [x for x in p.read_text(encoding="utf-8").splitlines() if x.strip()]
    if not lines:
        write_run_header(path, regions=regions or [], queries_source=queries_source, code_version=code_version)
        return

    try:
        first = json.loads(lines[0])
    except Exception:
        first = {}

    if first.get("type") == "run_header" and first.get("run_id"):
        return  # already good

    # Prepend a header
    hdr = {
        "type": "run_header",
        "run_id": run_id or __import__("uuid").uuid4().hex,
        "ts": now_rfc3339_z(),
        "regions": list(regions or []),
        "queries_source": queries_source,
        "code_version": code_version or os.getenv("GIT_COMMIT_SHA", ""),
    }
    p.write_text(
        json.dumps(_scrub_record(hdr), ensure_ascii=False) + "\n" + "\n".join(lines) + "\n",
        encoding="utf-8",
    )


def enrich_telemetry_file(path: str, run_id: str) -> None:
    """
    Read JSONL and ensure each non-header row has:
      - run_id
      - query_hash (from 'query' field if present)
      - ts (fallback to now)
    Rewrite file in-place.
    """
    p = Path(path)
    if not p.exists():
        return

    rows: list[dict] = []
    for raw in p.read_text(encoding="utf-8").splitlines():
        if not raw.strip():
            continue
        try:
            obj = json.loads(raw)
        except Exception:
            continue

        if obj.get("type") != "run_header":
            obj.setdefault("run_id", run_id)
            if "query" in obj and "query_hash" not in obj:
                obj["query_hash"] = sha1_query(obj.get("query", ""))
            obj.setdefault("ts", now_rfc3339_z())

        rows.append(_scrub_record(obj))

    p.write_text(
        "\n".join(json.dumps(_scrub_record(r), ensure_ascii=False) for r in rows)
        + "\n",
        encoding="utf-8",
    )
