import re
import subprocess
import sys
from pathlib import Path


def test_gen_release_notes(tmp_path):
    changelog = tmp_path / "CHANGELOG.md"
    changelog.write_text("# Changelog\n\n## [Unreleased]\n- Added\n")
    script = Path(__file__).resolve().parent.parent / "scripts" / "gen_release_notes.py"
    subprocess.run([sys.executable, script], cwd=tmp_path, check=True)
    out = (tmp_path / "artifacts/release_notes/release_notes.md").read_text()
    assert "1.0.0" in out
    assert re.search(r"Date: .*Z", out)
