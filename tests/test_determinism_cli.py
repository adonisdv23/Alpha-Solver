import json
import subprocess
import sys
import time
import re

CLI = [sys.executable, "-m", "cli.determinism"]


def run_cli(args, **kwargs):
    cmd = CLI + args
    return subprocess.run(cmd, capture_output=True, text=True, **kwargs)


def test_stable_set(tmp_path):
    json_path = tmp_path / "out.json"
    txt_path = tmp_path / "out.txt"
    res = run_cli([
        "--replay-file",
        "data/datasets/replay/replay_small.jsonl",
        "--runs",
        "5",
        "--seed",
        "123",
        "--out-json",
        str(json_path),
        "--out",
        str(txt_path),
    ])
    assert res.returncode == 0
    data = json.loads(json_path.read_text())
    assert data["stable"] is True
    assert data["pass_pct"] == 100.0
    assert txt_path.exists()


def test_mismatch_exit_code_and_reports(tmp_path):
    ds = tmp_path / "flap.jsonl"
    ds.write_text(json.dumps({"id": 1, "result": 1, "flap": True}) + "\n")
    json_path = tmp_path / "out.json"
    txt_path = tmp_path / "out.txt"
    res = run_cli([
        "--replay-file",
        str(ds),
        "--runs",
        "4",
        "--seed",
        "7",
        "--out-json",
        str(json_path),
        "--out",
        str(txt_path),
    ])
    assert res.returncode == 4
    data = json.loads(json_path.read_text())
    assert data["mismatches"]
    txt_content = txt_path.read_text()
    assert "first_mismatch_id" in txt_content


def test_skip_tags(tmp_path):
    ds = tmp_path / "skip.jsonl"
    records = [
        {"id": 1, "result": 1},
        {"id": 2, "result": 2, "flap": True, "skip_reason": "known_flaky"},
    ]
    with ds.open("w") as f:
        for r in records:
            f.write(json.dumps(r) + "\n")
    res = run_cli([
        "--replay-file",
        str(ds),
        "--runs",
        "4",
        "--skip-tags",
        "known_flaky",
    ])
    assert res.returncode == 0


def test_runtime_under_limit():
    start = time.time()
    res = run_cli([
        "--replay-file",
        "data/datasets/replay/replay_small.jsonl",
        "--runs",
        "10",
    ])
    duration = time.time() - start
    assert res.returncode == 0
    assert duration < 60


def test_output_redaction(tmp_path):
    ds = tmp_path / "secret.jsonl"
    ds.write_text(json.dumps({"id": 1, "result": 1, "flap": True}) + "\n")
    res = run_cli([
        "--replay-file",
        str(ds),
        "--runs",
        "3",
        "--seed",
        "5",
    ])
    # digits in winner should be redacted (no 'model' followed by digits)
    assert not re.search(r"model\d", res.stdout)
