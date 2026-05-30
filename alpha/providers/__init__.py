"""Provider client abstractions for real execution lanes."""

from .base import (
    ProviderCost,
    ProviderError,
    ProviderErrorCategory,
    ProviderRequest,
    ProviderResult,
    ProviderUsage,
)
from .accounting import (
    PROVIDER_COST_RECORDED,
    build_provider_accounting_record,
    emit_provider_accounting,
)
from .fake import FakeProviderClient
from .openai import OpenAIProviderClient
from .telemetry import (
    PROVIDER_REQUEST_COMPLETED,
    PROVIDER_REQUEST_FAILED,
    PROVIDER_REQUEST_STARTED,
    PROVIDER_REQUEST_TIMEOUT,
    build_provider_event,
    emit_provider_event,
)

__all__ = [
    "FakeProviderClient",
    "OpenAIProviderClient",
    "ProviderCost",
    "ProviderError",
    "ProviderErrorCategory",
    "ProviderRequest",
    "ProviderResult",
    "ProviderUsage",
    "PROVIDER_COST_RECORDED",
    "PROVIDER_REQUEST_COMPLETED",
    "PROVIDER_REQUEST_FAILED",
    "PROVIDER_REQUEST_STARTED",
    "PROVIDER_REQUEST_TIMEOUT",
    "build_provider_accounting_record",
    "build_provider_event",
    "emit_provider_accounting",
    "emit_provider_event",
]
