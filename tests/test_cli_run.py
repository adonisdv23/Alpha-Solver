import json
import subprocess
import sys
from pathlib import Path

CLI = [sys.executable, 'cli/alpha_solver_cli.py']


def run_cmd(args, input=None):
    return subprocess.run(CLI + args, input=input, text=True, capture_output=True)


def test_help_includes_subcommands():
    res = run_cmd(['--help'])
    assert res.returncode == 0
    for word in ['run', 'replay', 'gates', 'finops', 'traces']:
        assert word in res.stdout
    sub = run_cmd(['run', '--help'])
    assert '--model' in sub.stdout


def test_run_from_stdin_card():
    res = run_cmd(['run'], input='hello world')
    assert res.returncode == 0
    assert 'plan=' in res.stdout


def test_run_from_file_json(tmp_path: Path):
    p = tmp_path / 'prompt.txt'
    p.write_text('file input')
    res = run_cmd(['run', '--file', str(p), '--out', 'json'])
    data = json.loads(res.stdout)
    assert data['plan'] == 'direct'
    assert res.returncode == 0

def test_run_budget_block():
    res = run_cmd(['run', '--min-budget-tokens', '1'], input='many tokens here')
    assert res.returncode == 3
    assert 'budget=over' in res.stdout
