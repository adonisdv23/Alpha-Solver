"""Provider client contracts for real LLM execution lanes.

These contracts are intentionally separate from ``alpha.adapters`` prompt
renderers. Provider implementations may perform network I/O, while adapters only
render prompts for local/offline workflows.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Literal, Mapping

ProviderErrorCategory = Literal[
    "missing_credentials",
    "auth",
    "rate_limit",
    "timeout",
    "network",
    "provider_5xx",
    "invalid_request",
    "content_filter",
    "unknown",
]

ProviderCostSource = Literal["price_hint", "provider", "unknown"]


@dataclass(frozen=True)
class ProviderUsage:
    input_tokens: int | None = None
    output_tokens: int | None = None
    total_tokens: int | None = None


@dataclass(frozen=True)
class ProviderCost:
    estimated_usd: float | None = None
    source: ProviderCostSource = "unknown"


@dataclass(frozen=True)
class ProviderRequest:
    prompt: str
    model: str
    max_tokens: int
    timeout_ms: int
    system: str | None = None
    temperature: float | None = None
    seed: int | None = None
    metadata: Mapping[str, Any] = field(default_factory=dict)

    @property
    def request_id(self) -> str | None:
        value = self.metadata.get("request_id")
        return str(value) if value is not None else None


@dataclass(frozen=True)
class ProviderResult:
    provider: str
    model: str
    text: str
    finish_reason: str
    usage: ProviderUsage
    cost: ProviderCost
    latency_ms: int
    request_id: str | None = None
    raw_metadata: Mapping[str, Any] = field(default_factory=dict)
    retry_count: int = 0


@dataclass(frozen=True)
class ProviderError(Exception):
    provider: str
    category: ProviderErrorCategory
    retryable: bool
    safe_message: str
    status_code: int | None = None
    request_id: str | None = None
    retry_count: int = 0

    def __post_init__(self) -> None:
        Exception.__init__(self, self.safe_message)


RETRYABLE_CATEGORIES: frozenset[ProviderErrorCategory] = frozenset(
    {"rate_limit", "timeout", "network", "provider_5xx"}
)
