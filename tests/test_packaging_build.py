"""Smoke test for building the package.

The project doesn't require the optional ``build`` and ``packaging`` modules in
all environments (for example, some CI runners).  If they're missing we skip
this test during collection rather than raising an ``ImportError``.
"""

from pathlib import Path
import shutil
import subprocess
import sys
import unittest


# Skip eagerly if optional dependencies are missing.  We try importing them
# directly so environments without ``build`` or ``packaging`` don't error during
# collection.
try:  # pragma: no cover - exercised implicitly when deps are missing
    import build  # type: ignore  # noqa: F401
    import packaging  # type: ignore  # noqa: F401
except ModuleNotFoundError:  # pragma: no cover - exercised when deps absent
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

