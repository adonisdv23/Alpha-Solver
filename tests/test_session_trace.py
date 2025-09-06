import json
from datetime import datetime, timezone
from pathlib import Path

from alpha.core.session_trace import write_session_trace


def test_session_trace(tmp_path, monkeypatch):
    monkeypatch.setenv("ALPHA_ARTIFACTS_DIR", str(tmp_path))
    start = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    end = start
    path = write_session_trace(
        {
            "queries_source": "tests",
            "regions": ["US"],
            "seed": 1,
            "shortlist_paths": [],
            "env_snapshot_path": "env.json",
            "started_at": start,
            "ended_at": end,
        }
    )
    p = Path(path)
    assert p.is_file()
    data = json.loads(p.read_text(encoding="utf-8"))
    assert data["schema_version"] == "v1"
    assert datetime.fromisoformat(data["started_at"].replace("Z", "+00:00"))
