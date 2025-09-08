"""Tiny placeholder evaluation script.

This script serves as a minimal placeholder to allow the CI command
`python scripts/eval_small.py` to execute without error. It deliberately
avoids any heavy dependencies or external network calls.
"""

from __future__ import annotations


def main() -> None:
    """Run the placeholder evaluation and print a deterministic message."""
    print("eval_small: placeholder")


if __name__ == "__main__":
    main()
