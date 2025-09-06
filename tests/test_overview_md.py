from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


def test_overview_md(tmp_path, monkeypatch):
    art = tmp_path / "artifacts"
    run_dir = art / "run"
    sl_dir = art / "shortlists" / "US"
    run_dir.mkdir(parents=True)
    sl_dir.mkdir(parents=True)

    shortlist_path = sl_dir / "q.json"
    shortlist = {
        "schema_version": "v1",
        "query": "hello",
        "region": "US",
        "k": 1,
        "created_at": "2024-01-01T00:00:00Z",
        "items": [{"tool_id": "t1", "score": 1, "confidence": 0.9, "reason": "demo"}],
    }
    shortlist_path.write_text(json.dumps(shortlist), encoding="utf-8")

    run_trace = {
        "seed": 123,
        "regions": ["US"],
        "shortlist_paths": [str(shortlist_path.relative_to(art))],
    }
    run_path = run_dir / "run_20240101T000000Z.json"
    run_path.write_text(json.dumps(run_trace), encoding="utf-8")

    monkeypatch.chdir(tmp_path)
    script = Path(__file__).resolve().parents[1] / "scripts" / "overview_md.py"
    subprocess.run([sys.executable, str(script)], check=True)

    out = art / "overview.md"
    assert out.exists()
    txt = out.read_text(encoding="utf-8")
    assert "run_id" in txt
    assert "hello" in txt
    assert "t1" in txt
