import json
import re
import sys
import tempfile
from pathlib import Path
from subprocess import run

import pytest


def _run_gate(args):
    cmd = [sys.executable, "-m", "service.replay.gate"] + args
    return run(cmd, capture_output=True, text=True)


def _write_records(records):
    fd, path = tempfile.mkstemp(suffix=".jsonl")
    with open(fd, "w") as f:
        for rec in records:
            f.write(json.dumps(rec) + "\n")
    return Path(path)


def test_gate_passes_on_stable_set():
    recs = [{"id": 1, "result": 1}]
    path = _write_records(recs)
    proc = _run_gate(["--runs", "3", "--replay-file", str(path)])
    assert proc.returncode == 0, proc.stdout
    assert "PASS (3/3 stable)" in proc.stdout


def test_gate_fails_on_intentional_noise():
    recs = [{"id": 1, "result": 1, "flap": True}]
    path = _write_records(recs)
    proc = _run_gate(["--runs", "3", "--replay-file", str(path)])
    assert proc.returncode != 0
    assert "FAIL after run" in proc.stdout
    assert "winner" in proc.stdout


def test_skip_tags_works():
    recs = [
        {"id": 1, "result": 1},
        {"id": 2, "result": 2, "tags": ["skip_reason"]},
    ]
    path = _write_records(recs)
    proc = _run_gate(
        ["--runs", "3", "--skip-tags", "skip_reason", "--replay-file", str(path)]
    )
    assert proc.returncode == 0
    assert "PASS (3/3 stable)" in proc.stdout
    assert "skipped: 1" in proc.stdout


def test_no_secrets_in_output():
    recs = [{"id": 1, "result": 1}]
    path = _write_records(recs)
    proc = _run_gate(["--runs", "3", "--replay-file", str(path)])
    output = proc.stdout + proc.stderr
    assert not re.search(r"sk-[\w-]+", output)
    assert not re.search(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+", output)
    assert not re.search(r"\d{3}[- ]?\d{3}[- ]?\d{4}", output)


def test_fast_mode():
    recs = [{"id": 1, "result": 1}]
    path = _write_records(recs)
    proc = _run_gate(["--runs", "5", "--fast", "--replay-file", str(path)])
    assert proc.returncode == 0
    assert "PASS (2/2 stable)" in proc.stdout
