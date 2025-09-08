import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _run(cmd, cwd=ROOT):
    env = os.environ.copy()
    env["PYTHONPATH"] = str(ROOT)
    return subprocess.run(cmd, cwd=cwd, env=env, check=True, text=True, capture_output=True)


def test_eval_and_gate_and_budgets() -> None:
    report = ROOT / "artifacts" / "eval" / "latest_report.json"
    if report.exists():
        report.unlink()
    _run([
        sys.executable,
        "-m",
        "alpha.cli.main",
        "eval",
        "run",
        "--dataset",
        "datasets/mvp_golden.jsonl",
        "--scorers",
        "em,f1",
        "--seed",
        "1337",
        "--limit",
        "2",
    ])
    assert report.exists()
    _run([
        sys.executable,
        "-m",
        "alpha.cli.main",
        "gate",
        "check",
        "--report",
        str(report),
    ])
    out = _run([
        sys.executable,
        "-m",
        "alpha.cli.main",
        "budgets",
        "show",
    ])
    assert "default" in out.stdout
