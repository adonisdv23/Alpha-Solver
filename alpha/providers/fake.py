"""Test helper provider implementations."""

from __future__ import annotations

from collections.abc import Iterable

from .base import ProviderError, ProviderRequest, ProviderResult


class FakeProviderClient:
    """Deterministic provider client useful for narrow unit tests."""

    def __init__(self, outcomes: Iterable[ProviderResult | ProviderError]):
        self._outcomes = list(outcomes)
        self.requests: list[ProviderRequest] = []

    def execute(self, request: ProviderRequest) -> ProviderResult:
        self.requests.append(request)
        if not self._outcomes:
            raise AssertionError("FakeProviderClient has no configured outcomes")
        outcome = self._outcomes.pop(0)
        if isinstance(outcome, ProviderError):
            raise outcome
        return outcome
