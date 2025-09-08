import subprocess
import sys
from pathlib import Path


def test_cli_eval_and_gate(tmp_path):
    cmd = [
        sys.executable,
        "-m",
        "alpha.cli.main",
        "eval",
        "run",
        "--dataset",
        "datasets/mvp_golden.jsonl",
        "--scorers",
        "em",
        "--seed",
        "1337",
        "--limit",
        "2",
    ]
    subprocess.run(cmd, check=True)
    report = Path("artifacts/eval/latest_report.json")
    assert report.exists()
    result = subprocess.run(
        [sys.executable, "-m", "alpha.cli.main", "gate", "check", "--report", str(report)]
    )
    assert result.returncode == 0
