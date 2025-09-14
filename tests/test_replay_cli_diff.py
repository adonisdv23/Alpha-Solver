import json
import os
import subprocess
import sys
import time
from pathlib import Path

import pytest

from service.observability.diff import diff_lists

# Path to the project root so ``service`` is importable when running the CLI
PROJECT_ROOT = Path(__file__).resolve().parent.parent


def _write_events(path: Path, events: list[dict]) -> None:
    with open(path, "w", encoding="utf-8") as f:
        for e in events:
            f.write(json.dumps(e) + "\n")


# ---------------------------------------------------------------------------
def test_replay_10_of_10_identical_no_mismatches_exit0(tmp_path: Path) -> None:
    events = [
        {
            "id": f"evt-{i:03}",
            "name": "mcp.call",
            "decision": "allow",
            "confidence": 0.91,
            "budget_verdict": "ok",
            "tool": "t",
            "score": 0.1,
            "sandbox_decision": "allow",
        }
        for i in range(10)
    ]
    path = tmp_path / "events.jsonl"
    _write_events(path, events)

    cmd = [sys.executable, "-m", "service.observability.replay_cli", "--events", str(path)]
    env = os.environ.copy()
    env["PYTHONPATH"] = str(PROJECT_ROOT)
    res = subprocess.run(cmd, capture_output=True, text=True, cwd=PROJECT_ROOT, env=env)
    assert res.returncode == 0
    summary = json.loads(res.stdout.strip())
    assert summary["total"] == 10
    assert summary["mismatches"] == 0


# ---------------------------------------------------------------------------
def test_compare_detects_mismatches_and_exit2(tmp_path: Path) -> None:
    a = {
        "id": "evt-001",
        "name": "mcp.call",
        "decision": "allow",
        "confidence": 0.9,
        "budget_verdict": "ok",
        "tool": "t",
        "score": 0.1,
        "sandbox_decision": "allow",
    }
    b = dict(a)
    b["decision"] = "deny"
    path_a = tmp_path / "a.jsonl"
    path_b = tmp_path / "b.jsonl"
    _write_events(path_a, [a])
    _write_events(path_b, [b])
    out_path = tmp_path / "out.txt"

    cmd = [
        sys.executable,
        "-m",
        "service.observability.replay_cli",
        "--events",
        str(path_a),
        "--compare",
        str(path_b),
        "--out",
        str(out_path),
    ]
    env = os.environ.copy()
    env["PYTHONPATH"] = str(PROJECT_ROOT)
    res = subprocess.run(cmd, capture_output=True, text=True, cwd=PROJECT_ROOT, env=env)
    assert res.returncode == 2
    summary = json.loads(res.stdout.strip())
    assert summary["mismatches"] >= 1
    assert "decision" in out_path.read_text()


# ---------------------------------------------------------------------------
def test_diff_is_deterministic_and_limited_lines() -> None:
    a = [
        {"id": f"evt-{i:03}", "decision": "allow"}
        for i in range(205)
    ]
    b = [
        {"id": f"evt-{i:03}", "decision": "deny"}
        for i in range(205)
    ]
    lines1 = diff_lists(list(reversed(a)), list(reversed(b)), keys=["decision"])
    lines2 = diff_lists(list(reversed(a)), list(reversed(b)), keys=["decision"])
    assert lines1 == lines2
    assert lines1[0] == "id=evt-000 decision: allow != deny"
    assert lines1[-1] == "... (truncated)"
    assert len(lines1) == 201


# ---------------------------------------------------------------------------
def test_filters_by_event_name_and_limit(tmp_path: Path) -> None:
    events = []
    for i in range(5):
        events.append({
            "id": f"evt-a-{i}",
            "name": "mcp.call",
            "decision": "allow",
            "confidence": 0.9,
        })
    for i in range(5):
        events.append({
            "id": f"evt-b-{i}",
            "name": "other",
            "decision": "allow",
            "confidence": 0.9,
        })
    path = tmp_path / "events.jsonl"
    _write_events(path, events)

    cmd = [
        sys.executable,
        "-m",
        "service.observability.replay_cli",
        "--events",
        str(path),
        "--compare",
        str(path),
        "--filter",
        "name=mcp.call",
        "--limit",
        "3",
    ]
    env = os.environ.copy()
    env["PYTHONPATH"] = str(PROJECT_ROOT)
    res = subprocess.run(cmd, capture_output=True, text=True, cwd=PROJECT_ROOT, env=env)
    summary = json.loads(res.stdout.strip())
    assert summary["total"] == 3
    assert summary["mismatches"] == 0


# ---------------------------------------------------------------------------
def test_performance_p95_under_2s_for_200_events(tmp_path: Path) -> None:
    events = [
        {
            "id": f"evt-{i:03}",
            "name": "mcp.call",
            "decision": "allow",
            "confidence": 0.8,
        }
        for i in range(200)
    ]
    path = tmp_path / "events.jsonl"
    _write_events(path, events)

    cmd = [
        sys.executable,
        "-m",
        "service.observability.replay_cli",
        "--events",
        str(path),
        "--compare",
        str(path),
    ]
    env = os.environ.copy()
    env["PYTHONPATH"] = str(PROJECT_ROOT)
    start = time.monotonic()
    res = subprocess.run(cmd, capture_output=True, text=True, cwd=PROJECT_ROOT, env=env)
    duration = time.monotonic() - start
    summary = json.loads(res.stdout.strip())
    assert summary["total"] == 200
    assert summary["mismatches"] == 0
    assert summary["p95_ms"] < 2000
    assert duration < 10


# ---------------------------------------------------------------------------
def test_no_pii_in_outputs_or_logs(tmp_path: Path) -> None:
    a = {
        "id": "evt-001",
        "name": "mcp.call",
        "decision": "allow",
        "confidence": 0.9,
        "pii_raw": "secret stuff",
        "api_token": "token123",
        "user_secret": "very secret",
    }
    b = dict(a)
    b["decision"] = "deny"
    path_a = tmp_path / "a.jsonl"
    path_b = tmp_path / "b.jsonl"
    _write_events(path_a, [a])
    _write_events(path_b, [b])
    out_path = tmp_path / "out.txt"

    cmd = [
        sys.executable,
        "-m",
        "service.observability.replay_cli",
        "--events",
        str(path_a),
        "--compare",
        str(path_b),
        "--out",
        str(out_path),
    ]
    env = os.environ.copy()
    env["PYTHONPATH"] = str(PROJECT_ROOT)
    res = subprocess.run(cmd, capture_output=True, text=True, cwd=PROJECT_ROOT, env=env)
    output = res.stdout.lower()
    report = out_path.read_text().lower()
    assert "pii" not in output
    assert "token" not in output
    assert "secret" not in output
    assert "pii" not in report
    assert "token" not in report
    assert "secret" not in report
