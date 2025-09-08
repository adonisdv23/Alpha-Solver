from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _run_cli(args: list[str]) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    env["PYTHONPATH"] = str(ROOT)
    return subprocess.run(
        [sys.executable, "-m", "alpha.cli.main", *args],
        cwd=ROOT,
        env=env,
        text=True,
        capture_output=True,
    )


def test_eval_and_gate_cli() -> None:
    dataset = ROOT / "datasets/mvp_golden.jsonl"
    proc = _run_cli([
        "eval",
        "run",
        "--dataset",
        str(dataset),
        "--scorers",
        "em,f1",
        "--limit",
        "2",
    ])
    assert proc.returncode == 0, proc.stderr
    report = ROOT / "artifacts/eval/latest_report.json"
    assert report.exists()
    gate = _run_cli(["gate", "check", "--report", str(report)])
    assert gate.returncode == 0, gate.stderr
    budgets = _run_cli(["budgets", "show"])
    assert budgets.returncode == 0
