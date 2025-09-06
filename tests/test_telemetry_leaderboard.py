import json
import subprocess
import sys
from pathlib import Path


def _write_sample(path: Path) -> Path:
    rows = [
        {"solver": "a", "status": "success"},
        {"solver": "b", "status": "success"},
        {"solver": "b", "status": "fail"},
        {"solver": "a", "status": "success"},
    ]
    path.write_text("\n".join(json.dumps(r) for r in rows) + "\n", encoding="utf-8")
    return path


def test_markdown_output(tmp_path: Path):
    src = _write_sample(tmp_path / "telemetry.jsonl")
    out = tmp_path / "out.md"
    subprocess.check_call([
        sys.executable,
        "scripts/telemetry_leaderboard.py",
        "--paths",
        str(src),
        "--topk",
        "5",
        "--format",
        "md",
        "--out",
        str(out),
    ])
    text = out.read_text(encoding="utf-8")
    assert "| a | 2 |" in text
    assert "| b | 1 |" in text


def test_csv_output(tmp_path: Path):
    src = _write_sample(tmp_path / "telemetry.jsonl")
    out = tmp_path / "out.csv"
    subprocess.check_call([
        sys.executable,
        "scripts/telemetry_leaderboard.py",
        "--paths",
        str(src),
        "--topk",
        "5",
        "--format",
        "csv",
        "--out",
        str(out),
    ])
    text = out.read_text(encoding="utf-8")
    lines = [x.strip() for x in text.splitlines() if x.strip()]
    assert "solver,success" == lines[0]
    assert "a,2" in lines[1:]
    assert "b,1" in lines[1:]
