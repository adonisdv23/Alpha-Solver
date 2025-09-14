import json
import subprocess
import sys
from pathlib import Path

CLI = Path(__file__).resolve().parents[1] / "alpha_solver_cli.py"


def _run(tmp_path: Path, *args: str) -> list[str]:
    cmd = [sys.executable, str(CLI), *args]
    proc = subprocess.run(cmd, cwd=tmp_path, capture_output=True, text=True, check=True)
    return [line for line in proc.stdout.splitlines() if line.strip()]


def test_record_then_replay_identical(tmp_path: Path) -> None:
    lines = _run(tmp_path, "2+2", "--record", "--obs-stats")
    first = json.loads(lines[0])
    expected = {
        "solution": first["solution"],
        "decision": first["decision"],
        "route_explain": first["route_explain"],
    }
    stats = json.loads(lines[1])
    session_id = stats["sessions"][0]
    for _ in range(10):
        replay_lines = _run(tmp_path, "2+2", "--replay", session_id)
        replay_data = json.loads(replay_lines[0])
        assert {
            "solution": replay_data["solution"],
            "decision": replay_data["decision"],
            "route_explain": replay_data["route_explain"],
        } == expected


def test_obs_stats_fields(tmp_path: Path) -> None:
    lines = _run(tmp_path, "1+1", "--record", "--obs-stats")
    stats = json.loads(lines[1])
    assert "events_logged" in stats and "sessions" in stats
