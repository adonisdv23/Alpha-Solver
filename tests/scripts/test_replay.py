import json
import subprocess
import sys
from pathlib import Path


def _env(path: Path) -> Path:
    data = {
        "route": "tot",
        "confidence": 0.8,
        "diagnostics": {"tot": {"path": ["q", "a"]}},
        "phases": ["init", "assess", "finalize"],
    }
    path.write_text(json.dumps(data), encoding="utf-8")
    return path


def test_replay(tmp_path: Path):
    src = _env(tmp_path / "env.json")
    out = subprocess.check_output([sys.executable, "scripts/replay.py", str(src)])
    text = out.decode("utf-8").strip().splitlines()
    assert text == [
        "route: tot",
        "confidence: 0.800",
        "path: q -> a",
        "phases: init->assess->finalize",
    ]
