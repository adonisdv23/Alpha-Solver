import json
from datetime import datetime, timezone
from pathlib import Path

from alpha.core.registry_provider import write_shortlist_snapshot


def test_schema_versioning(tmp_path, monkeypatch):
    monkeypatch.setenv("ALPHA_ARTIFACTS_DIR", str(tmp_path))
    items = [{"tool_id": "a", "score": 1.0, "confidence": 0.5}]
    path = write_shortlist_snapshot("query", "US", 1, items)
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    assert data["schema_version"] == "v1"
    dt = datetime.fromisoformat(data["created_at"].replace("Z", "+00:00"))
    assert dt.tzinfo == timezone.utc
