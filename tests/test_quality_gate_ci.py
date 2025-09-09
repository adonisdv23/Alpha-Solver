from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _run() -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    env["PYTHONPATH"] = str(ROOT)
    cmd = [
        sys.executable,
        "-m",
        "alpha.eval.harness",
        "--dataset",
        str(ROOT / "datasets/mvp_golden.jsonl"),
        "--seed",
        "42",
        "--compare-baseline",
    ]
    return subprocess.run(cmd, cwd=ROOT, env=env, text=True, capture_output=True)


def test_ci_quality_gate(tmp_path: Path) -> None:
    first = _run()
    assert first.returncode == 0, first.stderr
    summary_file = ROOT / "artifacts/eval/summary.json"
    router_file = ROOT / "artifacts/eval/router_compare.json"
    assert summary_file.exists()
    assert router_file.exists()
    summary = json.load(summary_file.open())
    assert summary.get("token_savings_pct", 0) >= 0.15
    h1 = hashlib.sha256(router_file.read_bytes()).hexdigest()
    second = _run()
    assert second.returncode == 0, second.stderr
    h2 = hashlib.sha256(router_file.read_bytes()).hexdigest()
    assert h1 == h2

