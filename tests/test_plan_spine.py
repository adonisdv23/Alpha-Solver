import json
import os
import subprocess
import sys
from pathlib import Path

from alpha.core.plan import PlanStep, bounded_retry


def test_plan_only_creates_last_plan(tmp_path):
    env = os.environ.copy()
    env["ALPHA_ARTIFACTS_DIR"] = str(tmp_path)
    cmd = [sys.executable, "-m", "alpha.core.runner", "--plan-only", "--query", "Demo"]
    subprocess.check_call(cmd, env=env)
    path = tmp_path / "last_plan.json"
    assert path.is_file()
    data = json.loads(path.read_text())
    assert data.get("schema_version") == "v1"


def test_bounded_retry_logs(capsys):
    step = PlanStep(tool_id="noop", step_id="s1", contract={"ok": True})
    attempts = {"n": 0}

    def fn():
        attempts["n"] += 1
        return {"ok": False}

    bounded_retry(step, fn, max_retries=2, logger=lambda m: print(m))
    captured = capsys.readouterr()
    assert attempts["n"] == 3  # initial try + 2 retries
    assert step.status == "failed"
    assert "critique" in step.result
    assert "contract mismatch" in captured.out
