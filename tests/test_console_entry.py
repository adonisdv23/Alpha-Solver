import subprocess
import sys


def test_console_help_and_version():
    result = subprocess.run([sys.executable, "-m", "alpha.cli", "--help"], capture_output=True, text=True)
    assert result.returncode == 0
    assert "Alpha Solver command-line interface" in result.stdout

    result = subprocess.run([sys.executable, "-m", "alpha.cli", "version"], capture_output=True, text=True)
    assert result.returncode == 0
    assert "alpha-solver 1.0.0b1" in result.stdout

