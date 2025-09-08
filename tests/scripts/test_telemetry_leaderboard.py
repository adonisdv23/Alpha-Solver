import json
import subprocess
import sys
from pathlib import Path


def _log_file(path: Path) -> Path:
    events = [
        {"event": "run_summary", "run_id": "r1", "task": "a", "final_confidence": 0.8, "final_route": "tot"},
        {"event": "run_summary", "run_id": "r2", "task": "b", "final_confidence": 0.6, "final_route": "cot"},
        {"event": "run_summary", "run_id": "r3", "task": "a", "final_confidence": 0.9, "final_route": "tot"},
    ]
    path.write_text("\n".join(json.dumps(e) for e in events) + "\n", encoding="utf-8")
    return path


def test_markdown(tmp_path: Path):
    src = _log_file(tmp_path / "events.jsonl")
    out = tmp_path / "out.md"
    subprocess.check_call([
        sys.executable,
        "scripts/telemetry_leaderboard.py",
        "--paths",
        str(src),
        "--format",
        "md",
        "--out",
        str(out),
    ])
    expected = Path("tests/golden/telemetry_leaderboard.md").read_text(encoding="utf-8")
    assert out.read_text(encoding="utf-8") == expected


def test_csv(tmp_path: Path):
    src = _log_file(tmp_path / "events.jsonl")
    out = tmp_path / "out.csv"
    subprocess.check_call([
        sys.executable,
        "scripts/telemetry_leaderboard.py",
        "--paths",
        str(src),
        "--format",
        "csv",
        "--out",
        str(out),
    ])
    expected = Path("tests/golden/telemetry_leaderboard.csv").read_text(encoding="utf-8")
    assert out.read_text(encoding="utf-8") == expected
