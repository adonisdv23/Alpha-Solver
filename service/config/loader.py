"""Configuration loader for Alpha Solver."""

from __future__ import annotations

import copy
import logging
import os
from pathlib import Path
from typing import Any, Dict

import yaml

SECRET_SUFFIXES = ("KEY", "TOKEN", "SECRET")
ROOT = Path(__file__).resolve().parents[2]
DEFAULT_CONFIG_PATH = ROOT / "alpha_solver.yaml"

DEFAULTS: Dict[str, Any] = {
    "server": {"host": "0.0.0.0", "port": 8000, "log_level": "info"},
    "models": {
        "provider": "openai",
        "model": "gpt-5",
        "timeout_ms": 60000,
        "max_tokens": 2048,
    },
    "gates": {
        "low_conf_threshold": 0.35,
        "clarify_conf_threshold": 0.55,
        "min_budget_tokens": 256,
        "enable_cot_fallback": True,
    },
    "finops": {
        "max_cost_usd": 0.02,
        "soft_cap_usd": 0.015,
        "alert_on_soft_cap": True,
    },
    "observability": {"tracing": True, "metrics": True, "replay": True},
    "policy": {
        "enable_input_redaction": True,
        "detectors": {"email": True, "phone": True},
        "latency_budget_ms_p95": 50,
        "fail_closed": True,
    },
    "adapters": {"playwright": {"enabled": True}, "gsheets": {"enabled": True}},
    "tenancy": {
        "rate_limits": {"rps": 5, "burst": 10},
        "quotas": {"tokens_day": 200000},
    },
}


def _deep_merge(base: Dict[str, Any], override: Dict[str, Any]) -> Dict[str, Any]:
    result = copy.deepcopy(base)
    for key, value in override.items():
        if isinstance(value, dict) and isinstance(result.get(key), dict):
            result[key] = _deep_merge(result[key], value)
        else:
            result[key] = value
    return result


def _set_in(dic: Dict[str, Any], keys: list[str], value: Any) -> None:
    for k in keys[:-1]:
        dic = dic.setdefault(k, {})
    dic[keys[-1]] = value


def _parse_value(value: str) -> Any:
    lower = value.lower()
    if lower in {"true", "false"}:
        return lower == "true"
    try:
        if "." in value:
            return float(value)
        return int(value)
    except ValueError:
        return value


_aliases = {
    "MODEL_PROVIDER": ["models", "provider"],
    "SERVER_HOST": ["server", "host"],
    "SERVER_PORT": ["server", "port"],
    "SERVER_LOG_LEVEL": ["server", "log_level"],
}


def _apply_env_overrides(cfg: Dict[str, Any], env: Dict[str, str]) -> Dict[str, Any]:
    for key, value in env.items():
        path = None
        if key in _aliases:
            path = _aliases[key]
        elif "__" in key:
            path = [p.lower() for p in key.split("__")]
        if path:
            _set_in(cfg, path, _parse_value(value))
    return cfg


def _redact(config: Dict[str, Any]) -> Dict[str, Any]:
    def walk(obj: Any, key: str | None = None):
        if isinstance(obj, dict):
            return {k: walk(v, k) for k, v in obj.items()}
        if key and key.upper().endswith(SECRET_SUFFIXES):
            return "***REDACTED***"
        return obj

    return walk(config)


def load_config(
    path: str | Path | None = None,
    env: Dict[str, str] | None = None,
    logger: logging.Logger | None = None,
) -> Dict[str, Any]:
    """Load configuration with defaults, YAML, and environment overrides."""
    cfg = copy.deepcopy(DEFAULTS)
    config_path = Path(path) if path else DEFAULT_CONFIG_PATH
    if config_path.exists():
        with open(config_path, "r", encoding="utf-8") as f:
            file_cfg = yaml.safe_load(f) or {}
        cfg = _deep_merge(cfg, file_cfg)

    env = env or os.environ
    cfg = _apply_env_overrides(cfg, env)

    log = logger or logging.getLogger(__name__)
    log.debug("Loaded config: %s", _redact(cfg))
    return cfg


__all__ = ["load_config", "DEFAULTS", "DEFAULT_CONFIG_PATH"]
