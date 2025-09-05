import json
import os
import shutil
import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
CLI = ["python", "-m", "alpha.cli"]


def write_query(tmp_path):
    qfile = tmp_path / "q.txt"
    qfile.write_text("email automation with Gmail\n", encoding="utf-8")
    return qfile


def run_cli(args, tmp_path):
    env = dict(**os.environ, PYTHONPATH=str(REPO_ROOT))
    return subprocess.run(CLI + args, cwd=REPO_ROOT, env=env, capture_output=True, text=True)

def test_plan_only(tmp_path):
    shutil.rmtree(REPO_ROOT / "artifacts", ignore_errors=True)
    qfile = write_query(tmp_path)
    res = run_cli(["--plan-only", "--regions", "US", "--k", "1", "--queries", str(qfile)], tmp_path)
    assert res.returncode == 0
    assert (REPO_ROOT / "artifacts/last_plan.json").exists()
    assert not list((REPO_ROOT / "artifacts").glob("trace_*.json"))


def test_explain(tmp_path):
    shutil.rmtree(REPO_ROOT / "artifacts", ignore_errors=True)
    qfile = write_query(tmp_path)
    res = run_cli(["--explain", "--regions", "US", "--k", "1", "--queries", str(qfile)], tmp_path)
    assert res.returncode == 0
    assert "confidence" in res.stdout
    assert (REPO_ROOT / "artifacts/last_plan.json").exists()


def test_execute(tmp_path):
    shutil.rmtree(REPO_ROOT / "artifacts", ignore_errors=True)
    qfile = write_query(tmp_path)
    res = run_cli(["--execute", "--regions", "US", "--k", "1", "--queries", str(qfile)], tmp_path)
    assert res.returncode == 0
    trace_files = list((REPO_ROOT / "artifacts").glob("trace_*.json"))
    assert trace_files, "trace file missing"
    trace = json.loads(trace_files[0].read_text())
    assert "prompt_path" in trace[0]
    prompt_dirs = list((REPO_ROOT / "artifacts/prompts").rglob("user.txt"))
    assert prompt_dirs
