#!/usr/bin/env python
"""Environment sanity checks for Alpha Solver.

This script validates that required environment variables are present and that
basic invariants hold. No secret values are ever printed.
"""
from __future__ import annotations

import os
import sys
from typing import List

REQUIRED_VARS = ["MODEL_PROVIDER"]
SECRET_KEYS = ("KEY", "TOKEN", "SECRET")


def _is_truthy(value: str | None) -> bool:
    return str(value).lower() in {"1", "true", "yes", "on"}


def _print(msg: str) -> None:
    sys.stdout.write(msg + "\n")


def main() -> int:
    missing: List[str] = []
    for var in REQUIRED_VARS:
        if not os.getenv(var):
            missing.append(var)

    provider = os.getenv("MODEL_PROVIDER", "").lower()
    if provider == "openai" and not os.getenv("OPENAI_API_KEY"):
        missing.append("OPENAI_API_KEY")

    if missing:
        _print("Missing required environment variables:")
        for var in missing:
            _print(f"  - {var}")
        _print("Refer to .env.example for sample values.")
        return 1

    if _is_truthy(os.getenv("PROD")) and _is_truthy(os.getenv("DEBUG")):
        _print("Cannot run with PROD=true and DEBUG=true.")
        return 1

    _print("Environment looks good.")
    return 0


if __name__ == "__main__":  # pragma: no cover - manual invocation
    raise SystemExit(main())
