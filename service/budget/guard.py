from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class BudgetGuard:
    """Simple budget guard for enforcing cost and token budgets."""

    max_cost_usd: float
    max_tokens: Optional[int] | None = None

    def check(self, sim_result: Dict[str, Any]) -> Dict[str, Any]:
        """Check simulation totals against thresholds.

        Parameters
        ----------
        sim_result:
            The result from :func:`service.budget.simulator.simulate`.

        Returns
        -------
        dict
            A dictionary with keys ``ok``, ``budget_verdict``, ``totals`` and
            ``route_explain``.
        """

        totals = sim_result.get("totals", {})
        cost = float(totals.get("cost_usd", 0.0))
        tokens = int(totals.get("tokens", 0))

        over_cost = cost > self.max_cost_usd
        over_tokens = self.max_tokens is not None and tokens > self.max_tokens

        if over_cost:
            verdict = "over_cost"
        elif over_tokens:
            verdict = "over_tokens"
        else:
            verdict = "ok"

        ok = verdict == "ok"
        decision = "allow" if ok else "block"

        return {
            "ok": ok,
            "budget_verdict": verdict,
            "totals": totals,
            "route_explain": {"decision": decision, "budget_verdict": verdict},
        }
