import subprocess
import sys
from pathlib import Path


def test_cli_eval_and_gate(tmp_path):
    root = Path(__file__).resolve().parents[1]
    dataset = root / "datasets" / "mvp_golden.jsonl"
    cmd = [
        sys.executable,
        "-m",
        "alpha.cli.main",
        "eval",
        "run",
        "--dataset",
        str(dataset),
        "--scorers",
        "em",
        "--seed",
        "1337",
        "--limit",
        "2",
    ]
    subprocess.run(cmd, check=True, cwd=root)
    report = root / "artifacts/eval/latest_report.json"
    assert report.exists()
    result = subprocess.run(
        [sys.executable, "-m", "alpha.cli.main", "gate", "check", "--report", str(report)],
        cwd=root,
    )
    assert result.returncode == 0
