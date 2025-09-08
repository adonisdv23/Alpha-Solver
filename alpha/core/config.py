"""Configuration helpers for API and observability settings."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any
import os

try:  # pragma: no cover - exercised in tests
    import yaml  # type: ignore
except ModuleNotFoundError:  # pragma: no cover
    yaml = None


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


@dataclass
class QualityGateConfig:
    """Simple configuration used for quality gating."""

    min_score: float = 0.0
    max_latency_ms: int = 1000


def _parse_simple_yaml(text: str) -> dict[str, Any]:
    """Parse a minimal subset of YAML (``key: value`` pairs)."""

    data: dict[str, Any] = {}
    for raw in text.splitlines():
        line = raw.split("#", 1)[0].strip()
        if not line or ":" not in line:
            continue
        key, value = line.split(":", 1)
        value = value.strip().strip('"\'')
        if value.lower() in {"true", "false"}:
            parsed: Any = value.lower() == "true"
        else:
            try:
                parsed = int(value)
            except ValueError:
                try:
                    parsed = float(value)
                except ValueError:
                    parsed = value
        data[key.strip()] = parsed
    return data


def get_quality_gate(path: Path | str = Path("config/quality_gate.yaml")) -> QualityGateConfig:
    """Load the quality gate configuration.

    Falls back to a minimal parser if :mod:`yaml` is unavailable. Missing files
    or parsing errors simply return the default configuration.
    """

    path = Path(path)
    defaults = QualityGateConfig()
    try:
        text = path.read_text(encoding="utf-8")
        if yaml is not None:
            loaded = yaml.safe_load(text) or {}
        else:
            loaded = _parse_simple_yaml(text)
    except Exception:
        loaded = {}
    return QualityGateConfig(
        min_score=float(loaded.get("min_score", defaults.min_score)),
        max_latency_ms=int(loaded.get("max_latency_ms", defaults.max_latency_ms)),
    )


__all__ = ["APISettings", "QualityGateConfig", "get_quality_gate"]
