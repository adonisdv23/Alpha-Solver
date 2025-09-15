"""Budget guardrails for FinOps workloads.

This module implements in-memory budget tracking with soft and hard
thresholds. Budgets are scoped by tenant and project identifiers and the
module exposes helpers to register budgets, record usage and emit
Prometheus metrics that can be scraped by external systems.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
import logging
import threading
from typing import Dict, Iterable, Mapping, MutableMapping, Tuple

from prometheus_client import Counter

__all__ = ["BudgetExceeded", "BudgetManager", "COST_PER_TOKEN_CENTS"]


logger = logging.getLogger(__name__)


def _normalize_rate(value: Fraction | float | int | str | Tuple[int, int]) -> Fraction:
    """Normalize a rate specification into a :class:`Fraction`.

    Parameters
    ----------
    value:
        A value accepted by :class:`Fraction` plus ``(numerator, denominator)``
        tuples. The result represents the cost in cents per token.
    """

    if isinstance(value, Fraction):
        return value
    if isinstance(value, tuple) and len(value) == 2:
        return Fraction(value[0], value[1])
    if isinstance(value, float):
        # ``Fraction`` from a string avoids floating point artefacts.
        return Fraction(str(value))
    return Fraction(value)


COST_PER_TOKEN_CENTS: Mapping[str, Fraction] = {
    # The values intentionally favour round numbers to keep the shim simple
    # for tests. They represent the price in cents per token.
    "openai:gpt-4": Fraction(6, 10),  # 0.6¢ per token
    "openai:gpt-4o": Fraction(5, 10),
    "openai:gpt-3.5": Fraction(2, 10),
    "anthropic:claude-3-opus": Fraction(8, 10),
    "anthropic:claude-3-sonnet": Fraction(4, 10),
}


_BUDGET_SPEND_CENTS = Counter(
    "budget_spend_cents",
    "Cumulative budget spend in cents per tenant/project/provider.",
    ("tenant", "project", "provider"),
)


class BudgetExceeded(RuntimeError):
    """Raised when an operation would push the budget past the hard limit."""

    def __init__(self, tenant: str, project: str, attempted: int, hard_limit: int) -> None:
        message = (
            f"Budget exceeded for {tenant}/{project}: "
            f"attempted {attempted}¢ > hard limit {hard_limit}¢"
        )
        super().__init__(message)
        self.tenant = tenant
        self.project = project
        self.attempted_spend_cents = attempted
        self.hard_limit_cents = hard_limit


@dataclass
class _BudgetRecord:
    soft_limit_cents: int
    hard_limit_cents: int
    spend_cents: int = 0
    events: int = 0
    soft_warning_emitted: bool = False

    def snapshot(self) -> Dict[str, int | bool]:
        return {
            "soft_limit_cents": self.soft_limit_cents,
            "hard_limit_cents": self.hard_limit_cents,
            "spend_cents": self.spend_cents,
            "events": self.events,
            "soft_alert_triggered": self.soft_warning_emitted,
        }


class BudgetManager:
    """Manage in-memory budgets with soft and hard enforcement."""

    def __init__(
        self,
        *,
        cost_table: Mapping[str, Fraction | float | int | str | Tuple[int, int]] | None = None,
        registry=None,
        metric: Counter | None = None,
    ) -> None:
        if metric is not None and registry is not None:
            raise ValueError("Provide either a metric or a registry, not both.")

        table = cost_table or COST_PER_TOKEN_CENTS
        self._cost_table: Dict[str, Fraction] = {
            provider: _normalize_rate(rate)
            for provider, rate in table.items()
        }
        self._budgets: MutableMapping[Tuple[str, str], _BudgetRecord] = {}
        self._lock = threading.Lock()

        if metric is not None:
            self._metric = metric
        elif registry is not None:
            self._metric = Counter(
                "budget_spend_cents",
                "Cumulative budget spend in cents per tenant/project/provider.",
                ("tenant", "project", "provider"),
                registry=registry,
            )
        else:
            self._metric = _BUDGET_SPEND_CENTS

    # ---------------- Budget registration helpers -----------------
    def register_budget(self, tenant: str, project: str, *, soft_limit_cents: int, hard_limit_cents: int) -> None:
        """Register or reset a budget for the provided scope."""

        soft = int(soft_limit_cents)
        hard = int(hard_limit_cents)
        if soft < 0 or hard < 0:
            raise ValueError("Budget limits must be non-negative")
        if soft > hard:
            raise ValueError("Soft limit cannot exceed hard limit")

        with self._lock:
            self._budgets[(tenant, project)] = _BudgetRecord(soft_limit_cents=soft, hard_limit_cents=hard)

    # ---------------- Recording helpers -----------------
    def record_tokens(
        self,
        tenant: str,
        project: str,
        *,
        provider: str,
        tokens: int,
    ) -> Dict[str, int | bool | str | None]:
        """Record token usage and convert it into spend."""

        if tokens < 0:
            raise ValueError("Token count must be non-negative")
        cost_cents = self.calculate_cost_cents(provider, tokens)
        return self.record_cost(
            tenant,
            project,
            cost_cents,
            provider=provider,
            tokens=tokens,
        )

    def record_cost(
        self,
        tenant: str,
        project: str,
        cost_cents: int,
        *,
        provider: str = "direct",
        tokens: int | None = None,
    ) -> Dict[str, int | bool | str | None]:
        """Record a direct spend amount and enforce the guardrails."""

        if cost_cents < 0:
            raise ValueError("Cost must be non-negative")

        key = (tenant, project)
        with self._lock:
            record = self._budgets.get(key)
            if record is None:
                raise KeyError(f"No budget registered for {tenant}/{project}")

            proposed_total = record.spend_cents + cost_cents
            if proposed_total > record.hard_limit_cents:
                raise BudgetExceeded(tenant, project, proposed_total, record.hard_limit_cents)

            record.spend_cents = proposed_total
            record.events += 1
            emit_warning = False
            if (
                not record.soft_warning_emitted
                and record.soft_limit_cents > 0
                and proposed_total >= record.soft_limit_cents
            ):
                record.soft_warning_emitted = True
                emit_warning = True

            snapshot = record.snapshot()

        if cost_cents and self._metric is not None:
            self._metric.labels(tenant=tenant, project=project, provider=provider).inc(cost_cents)

        if emit_warning:
            logger.warning(
                "Budget soft cap reached for %s/%s (provider=%s, spend=%s¢, soft_cap=%s¢)",
                tenant,
                project,
                provider,
                snapshot["spend_cents"],
                snapshot["soft_limit_cents"],
            )

        return {
            "tenant": tenant,
            "project": project,
            "provider": provider,
            "tokens": tokens,
            "cost_cents": cost_cents,
            "total_spend_cents": snapshot["spend_cents"],
            "soft_limit_cents": snapshot["soft_limit_cents"],
            "hard_limit_cents": snapshot["hard_limit_cents"],
            "events": snapshot["events"],
            "soft_alert_triggered": snapshot["soft_alert_triggered"],
        }

    # ---------------- Query helpers -----------------
    def calculate_cost_cents(self, provider: str, tokens: int) -> int:
        """Calculate the spend (in cents) for a provider/token pair."""

        try:
            rate = self._cost_table[provider]
        except KeyError as exc:
            raise KeyError(f"Unknown provider '{provider}'") from exc

        cost = rate * tokens
        numerator, denominator = cost.numerator, cost.denominator
        quotient, remainder = divmod(numerator, denominator)
        if remainder:
            quotient += 1
        return int(quotient)

    def get_usage(self, tenant: str, project: str) -> Dict[str, int | bool]:
        """Return the current counters for a budget scope."""

        key = (tenant, project)
        with self._lock:
            record = self._budgets.get(key)
            if record is None:
                raise KeyError(f"No budget registered for {tenant}/{project}")
            snapshot = record.snapshot()
        return {
            "tenant": tenant,
            "project": project,
            **snapshot,
        }

    def snapshot(self) -> Dict[Tuple[str, str], Dict[str, int | bool]]:
        """Return a snapshot of all tracked budgets."""

        with self._lock:
            return {
                key: record.snapshot().copy()
                for key, record in self._budgets.items()
            }

    def registered_budgets(self) -> Iterable[Tuple[str, str]]:
        """Return an iterable with all registered budget scopes."""

        with self._lock:
            return list(self._budgets.keys())
