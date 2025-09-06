import subprocess
import sys

import alpha.cli as cli


def run_cli(args):
    return subprocess.run([sys.executable, "-m", "alpha.cli", *args], capture_output=True, text=True)


def test_cli_help():
    res = run_cli(["--help"])
    assert res.returncode == 0
    assert "Alpha Solver" in res.stdout
    assert "run" in res.stdout


def test_run_help():
    res = run_cli(["run", "--help"])
    assert res.returncode == 0
    assert "--queries-file" in res.stdout
    assert "--plan-only" in res.stdout


def test_examples_flag():
    res = run_cli(["--examples"])
    assert "alpha-solver run" in res.stdout


def test_quick_audit_path(monkeypatch):
    called = {}

    def fake():
        called["ok"] = True
        return 0

    monkeypatch.setattr(cli, "run_quick_audit", fake)
    assert cli.main(["quick-audit"]) == 0
    assert called["ok"]
