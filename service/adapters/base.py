from __future__ import annotations

"""Minimal adapter interface and error class."""

from dataclasses import dataclass
from typing import Protocol, Dict, Any


@dataclass
class AdapterError(Exception):
    """Deterministic error raised by tool adapters.

    Attributes:
        code: Stable error code string.
        retryable: Whether the operation can be retried safely.
    """

    code: str
    retryable: bool
    message: str | None = None

    def __post_init__(self) -> None:  # pragma: no cover - simple delegator
        super().__init__(self.message or self.code)


class IToolAdapter(Protocol):
    """Minimal protocol for tool adapters."""

    def run(
        self,
        payload: Dict[str, Any],
        *,
        idempotency_key: str | None = None,
        timeout_s: float = 5.0,
    ) -> Dict[str, Any]:
        """Execute the adapter against the given payload."""

    def name(self) -> str:
        """Return adapter name."""

    def to_route_explain(self, meta: Dict[str, Any]) -> Dict[str, Any]:
        """Return compact explanation data for routing."""
