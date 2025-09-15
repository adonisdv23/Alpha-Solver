import json
import subprocess
import sys
from pathlib import Path

CLI = [sys.executable, 'cli/alpha_solver_cli.py']


def run_cmd(args, input=None):
    return subprocess.run(CLI + args, input=input, text=True, capture_output=True)


def make_record(path: Path, prompt: str, expected: str):
    path.write_text(json.dumps({'prompt': prompt, 'expected': expected}) + '\n')


def test_replay_success(tmp_path: Path):
    p = tmp_path / 'ok.jsonl'
    expected = 'plan=direct | tokens=1 | cost=0.01 | budget=within'
    make_record(p, 'hi', expected)
    res = run_cmd(['replay', str(p)])
    assert res.returncode == 0
    assert 'replay ok' in res.stdout


def test_replay_mismatch(tmp_path: Path):
    p = tmp_path / 'bad.jsonl'
    expected = 'different'
    make_record(p, 'hi', expected)
    res = run_cmd(['replay', str(p)])
    assert res.returncode == 4
    assert 'expected' in res.stdout
