#!/usr/bin/env python
"""Environment sanity checks for Alpha Solver.

This script validates that required environment variables are present and that
basic invariants hold. No secret values are ever printed.
"""
from __future__ import annotations

import os
from pathlib import Path
import sys
from typing import List

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

SECRET_KEYS = ("KEY", "TOKEN", "SECRET")
ALLOWED_PROVIDERS = {"local", "local_llm", "none", "openai", "anthropic", "gemini", "google"}
_NO_KEY_PROVIDERS = {"local", "none"}
_LOCAL_LLM_PROVIDER_KEYS = (
    "OPENAI_API_KEY",
    "ANTHROPIC_API_KEY",
    "GOOGLE_API_KEY",
    "GEMINI_API_KEY",
    "DEEPSEEK_API_KEY",
)


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


def _validate_local_llm_env() -> List[str]:
    errors: List[str] = []
    if not _is_truthy(os.getenv("ALPHA_LOCAL_LLM_ENABLED")):
        errors.append("ALPHA_LOCAL_LLM_ENABLED must be true for MODEL_PROVIDER=local_llm")
    for var in (
        "ALPHA_LOCAL_LLM_ENDPOINT",
        "ALPHA_LOCAL_LLM_MODEL",
        "ALPHA_LOCAL_LLM_TIMEOUT_SECONDS",
    ):
        if _missing(var):
            errors.append(var)
    for var in _LOCAL_LLM_PROVIDER_KEYS:
        if not _missing(var):
            errors.append(f"{var} must be unset for MODEL_PROVIDER=local_llm")
    if not errors:
        try:
            from alpha.local_llm.provider_adapter import LocalLLMRuntimeConfig

            LocalLLMRuntimeConfig.from_env()
        except Exception as exc:
            reason = getattr(exc, "reason_code", exc.__class__.__name__)
            errors.append(f"local_llm configuration failed closed: {reason}")
    return errors


def main() -> int:
    missing: List[str] = []
    provider_raw = os.getenv("MODEL_PROVIDER", "")
    if provider_raw is None or not provider_raw.strip():
        missing.append("MODEL_PROVIDER")
        provider = ""
    else:
        provider = provider_raw.strip().lower()

    if provider and provider not in ALLOWED_PROVIDERS:
        _print(
            "Unknown MODEL_PROVIDER "
            f"{provider!r}. Allowed values: {', '.join(sorted(ALLOWED_PROVIDERS))}."
        )
        _print(
            "This check validates environment variable configuration only; "
            "it does not perform remote provider API calls."
        )
        return 1

    if provider == "local_llm":
        missing.extend(_validate_local_llm_env())
    elif provider and provider not in _NO_KEY_PROVIDERS:
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

    _print(
        "Environment looks good. This validates configuration only; "
        "no remote provider API calls were made."
    )
    return 0


if __name__ == "__main__":  # pragma: no cover - manual invocation
    raise SystemExit(main())
