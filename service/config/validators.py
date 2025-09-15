"""Validation helpers for Alpha Solver configuration."""

from __future__ import annotations

from typing import Any, Mapping

ALLOWED_PROVIDERS = {"openai", "dummy"}
SECRET_SUFFIXES = ("KEY", "TOKEN", "SECRET")


def _check(cond: bool, msg: str) -> None:
    if not cond:
        raise ValueError(msg)


def validate(config: Mapping[str, Any]) -> None:
    server = config.get("server", {})
    _check(
        isinstance(server.get("port"), int) and server["port"] > 0,
        "server.port must be a positive integer",
    )

    models = config.get("models", {})
    provider = models.get("provider")
    _check(
        provider in ALLOWED_PROVIDERS,
        "models.provider must be one of: " + ", ".join(sorted(ALLOWED_PROVIDERS)),
    )
    _check(models.get("timeout_ms", 0) > 0, "models.timeout_ms must be positive")
    _check(models.get("max_tokens", 0) > 0, "models.max_tokens must be positive")

    gates = config.get("gates", {})
    for key in ("low_conf_threshold", "clarify_conf_threshold"):
        val = gates.get(key)
        _check(0 <= float(val) <= 1, f"gates.{key} must be between 0 and 1")
    _check(gates.get("min_budget_tokens", 0) >= 0, "gates.min_budget_tokens must be non-negative")

    finops = config.get("finops", {})
    _check(finops.get("max_cost_usd", 0) >= 0, "finops.max_cost_usd must be non-negative")
    _check(finops.get("soft_cap_usd", 0) >= 0, "finops.soft_cap_usd must be non-negative")
    _check(
        finops.get("soft_cap_usd", 0) <= finops.get("max_cost_usd", 0),
        "finops.soft_cap_usd must not exceed max_cost_usd",
    )

    policy = config.get("policy", {})
    _check(
        policy.get("latency_budget_ms_p95", 0) >= 0,
        "policy.latency_budget_ms_p95 must be non-negative",
    )

    # No secret values should be exposed - ensure keys exist but redacted elsewhere
    for section in config.values():
        if isinstance(section, Mapping):
            for key in section.keys():
                if key.upper().endswith(SECRET_SUFFIXES):
                    raise ValueError("Secret keys should not appear in configuration output")


__all__ = ["validate"]
