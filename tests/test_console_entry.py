import subprocess
import sys
from importlib import metadata

import alpha


def _expected_version() -> str:
    try:
        return metadata.version("alpha-solver")
    except metadata.PackageNotFoundError:
        return alpha.__version__


def test_console_help_and_version():
    result = subprocess.run(
        [sys.executable, "-m", "alpha.cli", "--help"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    assert "Alpha Solver command-line interface" in result.stdout

    result = subprocess.run(
        [sys.executable, "-m", "alpha.cli", "version"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    assert f"alpha-solver {_expected_version()}" in result.stdout
