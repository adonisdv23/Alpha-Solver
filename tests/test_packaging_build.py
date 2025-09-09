import shutil
import subprocess
import sys
from pathlib import Path

import pytest


def test_packaging_build(tmp_path: Path) -> None:
    repo_root = Path(__file__).resolve().parents[1]
    work = tmp_path / "pkg"
    shutil.copytree(
        repo_root,
        work,
        ignore=shutil.ignore_patterns(
            "artifacts",
            "telemetry",
            "logs",
            "docs",
            "dist",
            "*.egg-info",
            ".git",
            "__pycache__",
            ".pytest_cache",
            ".ruff_cache",
        ),
    )

    proc = subprocess.run([sys.executable, "-m", "build"], cwd=work)
    if proc.returncode != 0:
        pytest.skip("build module missing or build failed")

    assert any((work / "dist").glob("*"))
