#!/usr/bin/env python
"""Environment sanity checks for Alpha Solver.

This script validates that required environment variables are present and that
basic invariants hold. No secret values are ever printed.
"""
from __future__ import annotations

import os
import sys
from typing import List

SECRET_KEYS = ("KEY", "TOKEN", "SECRET")
_NO_KEY_PROVIDERS = {"local", "none"}


def _is_truthy(value: str | None) -> bool:
    return str(value).lower() in {"1", "true", "yes", "on"}


def _print(msg: str) -> None:
    sys.stdout.write(msg + "\n")


def _required_keys_for_provider(provider: str) -> List[str]:
    """Return the API keys required for the given provider."""
    if provider == "openai":
        return ["OPENAI_API_KEY"]
    if provider == "anthropic":
        return ["ANTHROPIC_API_KEY"]
    if provider in {"gemini", "google"}:
        return ["GOOGLE_API_KEY"]
    return []


def _missing(var: str) -> bool:
    value = os.getenv(var)
    return value is None or not value.strip()


def main() -> int:
    missing: List[str] = []
    provider_raw = os.getenv("MODEL_PROVIDER", "")
    if provider_raw is None or not provider_raw.strip():
        missing.append("MODEL_PROVIDER")
        provider = ""
    else:
        provider = provider_raw.strip().lower()

    if provider and provider not in _NO_KEY_PROVIDERS:
        for var in _required_keys_for_provider(provider):
            if _missing(var):
                missing.append(var)

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
