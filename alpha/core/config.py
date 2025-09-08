"""Configuration helpers for API and observability settings."""

from __future__ import annotations

from dataclasses import dataclass
import os
from pathlib import Path
from typing import Any, Dict

try:  # optional dependency
    import yaml  # type: ignore
except ModuleNotFoundError:  # pragma: no cover - exercised in tests via monkeypatch
    yaml = None  # type: ignore


@dataclass
class APISettings:
    """Runtime configuration for the API service.

    Values are primarily sourced from environment variables so the service can be
    configured at deployment time without code changes.
    """

    api_key: str = os.getenv("API_KEY", "")
    rate_limit_per_minute: int = int(os.getenv("RATE_LIMIT_PER_MINUTE", "60"))
    cost_per_token: float = float(os.getenv("COST_PER_TOKEN", "0"))
    cost_per_ms: float = float(os.getenv("COST_PER_MS", "0.0001"))
    otel_endpoint: str = os.getenv("OTEL_ENDPOINT", "http://otel-collector:4317")
    prom_port: int = int(os.getenv("PROM_PORT", "8000"))
    version: str = os.getenv("ALPHA_SOLVER_VERSION", "0.0.0")


__all__ = ["APISettings"]


@dataclass
class QualityGateConfig:
    min_accuracy: float = 0.85
    max_p95_ms: float = 750
    max_p99_ms: float = 1200
    max_cost_per_call: float = 0.01
    primary_metric: str = "em"


def get_quality_gate(overrides: Dict[str, Any] | None = None) -> QualityGateConfig:
    cfg = QualityGateConfig()
    path = Path("config/quality_gate.yaml")

    def _fallback_parse(p: Path) -> Dict[str, Dict[str, Any]]:
        """Very small YAML subset parser for `key: value` pairs.

        Only handles the structure used in ``config/quality_gate.yaml`` and is
        sufficient when PyYAML isn't available."""
        result: Dict[str, Dict[str, Any]] = {}
        current: str | None = None
        for raw in p.read_text().splitlines():
            line = raw.strip()
            if not line or line.startswith("#"):
                continue
            if not raw.startswith(" ") and line.endswith(":"):
                current = line[:-1]
                result[current] = {}
            elif ":" in line and current:
                k, v = line.split(":", 1)
                v = v.strip()
                try:
                    val: Any = float(v)
                except ValueError:
                    val = v
                result[current][k.strip()] = val
        return result

    if path.exists():
        if yaml is not None:
            data = yaml.safe_load(path.read_text()) or {}
        else:
            data = _fallback_parse(path)
        section = data.get("quality_gate", data)
        for k, v in section.items():
            if hasattr(cfg, k):
                setattr(cfg, k, v)
    env_map = {
        "min_accuracy": "QUALITY_GATE_MIN_ACCURACY",
        "max_p95_ms": "QUALITY_GATE_MAX_P95_MS",
        "max_p99_ms": "QUALITY_GATE_MAX_P99_MS",
        "max_cost_per_call": "QUALITY_GATE_MAX_COST_PER_CALL",
        "primary_metric": "QUALITY_GATE_PRIMARY_METRIC",
    }
    for field, env_name in env_map.items():
        val = os.getenv(env_name)
        if val is not None:
            if field == "primary_metric":
                setattr(cfg, field, val)
            else:
                setattr(cfg, field, float(val))
    if overrides:
        for k, v in overrides.items():
            if hasattr(cfg, k):
                setattr(cfg, k, v)
    return cfg


__all__ += ["QualityGateConfig", "get_quality_gate"]
