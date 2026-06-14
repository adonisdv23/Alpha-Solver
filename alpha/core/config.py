"""Configuration helpers for API and observability settings."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, List
import os

try:  # pragma: no cover - exercised in tests
    import yaml  # type: ignore
except ModuleNotFoundError:  # pragma: no cover
    yaml = None


@dataclass
class ServiceAuthConfig:
    """API-Key authentication configuration."""

    enabled: bool = os.getenv("SERVICE_AUTH_ENABLED", "true").lower() == "true"
    header: str = os.getenv("SERVICE_AUTH_HEADER", "X-API-Key")
    keys: List[str] = field(
        default_factory=lambda: os.getenv(
            "SERVICE_AUTH_KEYS", os.getenv("API_KEY", "dev-secret")
        ).split(",")
    )


@dataclass
class ServiceRateLimitConfig:
    """Per-key sliding window rate limit configuration."""

    enabled: bool = os.getenv("SERVICE_RATELIMIT_ENABLED", "true").lower() == "true"
    window_seconds: int = int(os.getenv("SERVICE_RATELIMIT_WINDOW_SECONDS", "60"))
    max_requests: int = int(
        os.getenv(
            "SERVICE_RATELIMIT_MAX_REQUESTS",
            os.getenv("RATE_LIMIT_PER_MINUTE", "120"),
        )
    )


@dataclass
class ServiceCorsConfig:
    """CORS configuration (lock down in production)."""

    origins: List[str] = field(
        default_factory=lambda: os.getenv("SERVICE_CORS_ORIGINS", "*").split(",")
    )


@dataclass
class APISettings:
    """Runtime configuration for the API service.

    Values are primarily sourced from environment variables so the service can be
    configured at deployment time without code changes.
    """

    auth: ServiceAuthConfig = field(default_factory=ServiceAuthConfig)
    ratelimit: ServiceRateLimitConfig = field(default_factory=ServiceRateLimitConfig)
    cors: ServiceCorsConfig = field(default_factory=ServiceCorsConfig)
    cost_per_token: float = float(os.getenv("COST_PER_TOKEN", "0"))
    cost_per_ms: float = float(os.getenv("COST_PER_MS", "0.0001"))
    otel_endpoint: str = os.getenv("OTEL_ENDPOINT", "http://otel-collector:4317")
    prom_port: int = int(os.getenv("PROM_PORT", "8000"))
    version: str = os.getenv("ALPHA_SOLVER_VERSION", "0.0.0")

    # Back-compat shims -------------------------------------------------
    @property
    def api_key(self) -> str:
        return self.auth.keys[0] if self.auth.keys else ""

    @api_key.setter
    def api_key(self, value: str) -> None:
        self.auth.keys = [value]

    @property
    def rate_limit_per_minute(self) -> int:
        if self.ratelimit.window_seconds == 0:
            return 0
        return int(self.ratelimit.max_requests * 60 / self.ratelimit.window_seconds)

    @rate_limit_per_minute.setter
    def rate_limit_per_minute(self, value: int) -> None:
        self.ratelimit.max_requests = value
        self.ratelimit.window_seconds = 60


@dataclass
class QualityGateConfig:
    """Configuration for quality gates and evaluation budgets."""

    min_accuracy: float = 0.85
    max_p95_ms: int = 750
    max_p99_ms: int = 1200
    max_cost_per_call: float = 0.01
    primary_metric: str = "em"


@dataclass
class ValidationConfig:
    """Configuration for Chain-of-Thought self-validation."""

    enabled: bool = True
    min_conf: float = 0.70


@dataclass
class ReactConfig:
    """Configuration for ReAct-Lite executor."""

    enabled: bool = True
    max_steps: int = 2
    min_conf: float = 0.70


@dataclass
class StrategyConfig:
    """Reasoning strategy selection and nested configs."""

    strategy: str = "cot"
    react: ReactConfig = field(default_factory=ReactConfig)


@dataclass
class TokenBudgetConfig:
    """Router token budget controls."""

    max_per_example: int = 2048


@dataclass
class VoteConfig:
    """Optional majority vote configuration."""

    enabled: bool = False
    k: int = 3


@dataclass
class RouterConfig:
    """Configuration for router v12 behaviour."""

    seed: int = 42
    token_budget: TokenBudgetConfig = field(default_factory=TokenBudgetConfig)
    vote: VoteConfig = field(default_factory=VoteConfig)


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

    Uses :mod:`yaml` when available, otherwise falls back to a tiny inline
    parser that understands ``key: value`` pairs. Any failures result in the
    default :class:`QualityGateConfig` being returned.
    """

    path = Path(path)
    defaults = QualityGateConfig()
    try:
        text = path.read_text(encoding="utf-8")
        if yaml is not None:  # pragma: no branch - exercised in tests
            loaded = yaml.safe_load(text) or {}
        else:
            loaded = _parse_simple_yaml(text)
    except Exception:
        loaded = {}
    return QualityGateConfig(
        min_accuracy=float(loaded.get("min_accuracy", defaults.min_accuracy)),
        max_p95_ms=int(loaded.get("max_p95_ms", defaults.max_p95_ms)),
        max_p99_ms=int(loaded.get("max_p99_ms", defaults.max_p99_ms)),
        max_cost_per_call=float(
            loaded.get("max_cost_per_call", defaults.max_cost_per_call)
        ),
        primary_metric=str(loaded.get("primary_metric", defaults.primary_metric)),
    )


__all__ = [
    "APISettings",
    "ServiceAuthConfig",
    "ServiceRateLimitConfig",
    "ServiceCorsConfig",
    "QualityGateConfig",
    "ValidationConfig",
    "ReactConfig",
    "StrategyConfig",
    "TokenBudgetConfig",
    "VoteConfig",
    "RouterConfig",
    "get_quality_gate",
]
