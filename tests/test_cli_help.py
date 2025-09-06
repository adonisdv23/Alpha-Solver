import subprocess
import sys


def test_cli_help():
    res = subprocess.run([sys.executable, "-m", "alpha.cli", "--help"], capture_output=True, text=True)
    assert res.returncode == 0
    assert "Alpha Solver CLI" in res.stdout
    assert "run" in res.stdout


def test_run_help():
    res = subprocess.run([sys.executable, "-m", "alpha.cli", "run", "--help"], capture_output=True, text=True)
    assert res.returncode == 0
    assert "--queries-file" in res.stdout
    assert "--plan-only" in res.stdout

