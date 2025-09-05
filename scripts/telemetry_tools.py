from __future__ import annotations
import hashlib, json, uuid, datetime as dt, os
from pathlib import Path

def sha1_query(q: str) -> str:
    qn = " ".join(q.split()).strip().lower()
    return hashlib.sha1(qn.encode("utf-8")).hexdigest()

def write_run_header(path: str, regions: list[str], queries_source: str = "", code_version: str = "") -> str:
    run_id = str(uuid.uuid4())
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    header = {
        "type": "run_header",
        "run_id": run_id,
        "started_at": dt.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
        "regions": regions,
        "queries_source": queries_source,
        "code_version": code_version or os.getenv("GIT_COMMIT_SHA","")
    }
    with p.open("a", encoding="utf-8") as f:
        f.write(json.dumps(header) + "\n")
    return run_id
