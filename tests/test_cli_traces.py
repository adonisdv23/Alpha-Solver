import json
import subprocess
import sys

CLI = [sys.executable, 'cli/alpha_solver_cli.py']


def run_cmd(args):
    return subprocess.run(CLI + args, text=True, capture_output=True)


def test_traces_id():
    res = run_cmd(['traces', '--prompt', 'hi'])
    assert res.returncode == 0
    assert res.stdout.strip().startswith('trace-')


def test_traces_json():
    res = run_cmd(['traces', '--prompt', 'hi', '--out', 'json'])
    data = json.loads(res.stdout)
    assert 'trace_id' in data
