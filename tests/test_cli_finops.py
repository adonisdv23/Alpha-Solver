import subprocess
import sys

CLI = [sys.executable, 'cli/alpha_solver_cli.py']


def run_cmd(args):
    return subprocess.run(CLI + args, text=True, capture_output=True)


def test_finops_within():
    res = run_cmd(['finops', '--prompt', 'tiny', '--min-budget-tokens', '10'])
    assert res.returncode == 0
    assert 'budget=within' in res.stdout


def test_finops_over():
    res = run_cmd(['finops', '--tokens', '30', '--min-budget-tokens', '10'])
    assert res.returncode == 3
    assert 'budget=over' in res.stdout
