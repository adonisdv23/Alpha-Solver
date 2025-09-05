import json
import os
import shutil
import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
CLI = ["python", "-m", "alpha.cli"]


def run_cli(args):
    env = dict(**os.environ, PYTHONPATH=str(REPO_ROOT))
    return subprocess.run(CLI + args, cwd=REPO_ROOT, env=env, capture_output=True, text=True)


def write_query(tmp_path):
    qfile = tmp_path / "q.txt"
    qfile.write_text("email automation with Gmail\n", encoding="utf-8")
    return qfile


def normalize_plan(data):
    data = json.loads(json.dumps(data))
    data["run"]["timestamp"] = "TS"
    data["artifacts"]["plan_path"] = "PATH"
    data["artifacts"]["shortlist_snapshot"] = "PATH"
    return data


def normalize_trace(data):
    data = json.loads(json.dumps(data))
    for step in data:
        if "prompt_path" in step:
            step["prompt_path"] = "PATH"
    return data


def test_plan_only_scenario(tmp_path):
    shutil.rmtree(REPO_ROOT / "artifacts", ignore_errors=True)
    qfile = write_query(tmp_path)
    run_cli(["--plan-only", "--regions", "US", "--k", "1", "--queries", str(qfile), "--seed", "1234"])
    plan = json.loads((REPO_ROOT / "artifacts/last_plan.json").read_text())
    norm = normalize_plan(plan)
    snap = json.loads((REPO_ROOT / "tests/golden/plan_only.json").read_text())
    assert norm == snap


def test_explain_scenario(tmp_path):
    shutil.rmtree(REPO_ROOT / "artifacts", ignore_errors=True)
    qfile = write_query(tmp_path)
    out = run_cli(["--explain", "--regions", "US", "--k", "1", "--queries", str(qfile), "--seed", "1234"])
    assert "confidence" in out.stdout
    plan = json.loads((REPO_ROOT / "artifacts/last_plan.json").read_text())
    norm = normalize_plan(plan)
    snap = json.loads((REPO_ROOT / "tests/golden/explain.json").read_text())
    assert norm == snap
    assert "reasons" in norm["steps"][0]


def test_execute_scenario(tmp_path):
    shutil.rmtree(REPO_ROOT / "artifacts", ignore_errors=True)
    qfile = write_query(tmp_path)
    run_cli(["--execute", "--regions", "US", "--k", "1", "--queries", str(qfile), "--seed", "1234"])
    trace_file = next((REPO_ROOT / "artifacts").glob("trace_*.json"))
    trace = json.loads(trace_file.read_text())
    norm_trace = normalize_trace(trace)
    snap = json.loads((REPO_ROOT / "tests/golden/execute.json").read_text())
    assert norm_trace == snap
    assert list((REPO_ROOT / "artifacts/prompts").rglob("user.txt"))
