import subprocess
import sys
from pathlib import Path


def test_tag_release(tmp_path):
    repo = tmp_path
    pkg = repo / "alpha"
    pkg.mkdir()
    init = pkg / "__init__.py"
    init.write_text('__version__ = "0.0.1"\n')
    subprocess.run(["git", "init"], cwd=repo, check=True)
    subprocess.run(["git", "config", "user.email", "a@b.com"], cwd=repo, check=True)
    subprocess.run(["git", "config", "user.name", "a"], cwd=repo, check=True)
    subprocess.run(["git", "add", "alpha/__init__.py"], cwd=repo, check=True)
    subprocess.run(["git", "commit", "-m", "init"], cwd=repo, check=True)
    script = Path(__file__).resolve().parent.parent / "scripts" / "tag_release.py"
    subprocess.run([sys.executable, script, "--version", "2.3.4"], cwd=repo, check=True)
    assert '__version__ = "2.3.4"' in init.read_text()
