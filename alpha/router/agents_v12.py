"""Groundwork for pluggable multi-agent router v12."""

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Protocol


class Decomposer(Protocol):
    """Interface for breaking down complex queries."""

    def run(self, query: str) -> List[str]:
        """Return subqueries for ``query``."""
        ...


class Checker(Protocol):
    """Interface for verifying statements."""

    def run(self, statements: List[str]) -> bool:
        """Return validation result for ``statements``."""
        ...


class Calculator(Protocol):
    """Interface for deterministic calculations."""

    def run(self, expr: str) -> float:
        """Evaluate ``expr`` deterministically."""
        ...


@dataclass
class NoOpDecomposer:
    """Deterministic no-op decomposer."""

    def run(self, query: str) -> List[str]:
        return [query]


@dataclass
class NoOpChecker:
    """Deterministic no-op checker."""

    def run(self, statements: List[str]) -> bool:
        return True


@dataclass
class NoOpCalculator:
    """Deterministic no-op calculator."""

    def run(self, expr: str) -> float:
        return 0.0

