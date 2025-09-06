import json
from pathlib import Path

from alpha.adapters import runner


def test_runner_writes_trace(tmp_path, monkeypatch):
    monkeypatch.setenv("ALPHA_ARTIFACTS_DIR", str(tmp_path))
    res = runner.run("summarize", {"text": "hello"}, seed=7)
    path = Path(res["trace_path"])
    assert path.exists()
    data = json.loads(path.read_text())
    assert data["adapter"] == "summarize"
    assert data["seed"] == 7
    assert "prompt" in data


def test_runner_deterministic(tmp_path, monkeypatch):
    monkeypatch.setenv("ALPHA_ARTIFACTS_DIR", str(tmp_path))
    monkeypatch.setenv("ALPHA_DETERMINISM", "1")
    r1 = runner.run("classify", {"text": "x", "labels": ["yes", "no"]}, seed=3)
    r2 = runner.run("classify", {"text": "x", "labels": ["yes", "no"]}, seed=3)
    assert r1["prompt"] == r2["prompt"]
    assert r1["seed"] == r2["seed"]
