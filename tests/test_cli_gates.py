import subprocess
import sys

CLI = [sys.executable, 'cli/alpha_solver_cli.py']


def run_cmd(args):
    return subprocess.run(CLI + args, text=True, capture_output=True)


def test_gates_clarify():
    res = run_cmd(['gates', '--confidence', '0.3', '--tokens', '10'])
    assert res.returncode == 0
    assert 'clarify' in res.stdout
    assert 'thresholds' in res.stdout


def test_gates_deny():
    res = run_cmd(['gates', '--confidence', '0.1', '--tokens', '25'])
    assert res.returncode == 3
    assert 'deny' in res.stdout
