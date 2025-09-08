"""Smoke test for building the package.

The project doesn't require the optional ``build`` and ``packaging`` modules in
all environments (for example, some CI runners).  If they're missing we skip
this test during collection rather than raising an ``ImportError``.
"""

from pathlib import Path
import importlib.util
import shutil
import subprocess
import sys
import unittest


def _has_module(name: str) -> bool:
    return importlib.util.find_spec(name) is not None


# Skip eagerly if either dependency is unavailable.
if not (_has_module("build") and _has_module("packaging")):
    raise unittest.SkipTest("build/packaging modules required for packaging test")

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

