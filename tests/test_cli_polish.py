import pytest
from alpha.cli import main
from alpha import __version__


def test_version_output(capsys):
    rc = main(["--version"])
    out = capsys.readouterr().out
    assert __version__ in out
    assert rc == 0


def test_dry_run_alias(tmp_path, monkeypatch):
    # ensure queries file exists
    qfile = tmp_path / "q.txt"
    qfile.write_text("hello", encoding="utf-8")
    rc1 = main(["--plan-only", "--queries", str(qfile)])
    rc2 = main(["--dry-run", "--queries", str(qfile)])
    assert rc1 == rc2 == 0


def test_missing_queries_file():
    rc = main(["--plan-only", "--queries", "nope.txt"])
    assert rc == 2
