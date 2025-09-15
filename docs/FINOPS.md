# FinOps Budget Guardrails

The FinOps budget guardrails keep track of spend for each tenant/project
pair and enforce soft and hard caps. The implementation focuses on
in-memory counters so it can be embedded into offline tests while still
exporting Prometheus metrics for production observability.

## Budget manager

`alpha.finops.budget.BudgetManager` exposes a small API:

1. **`register_budget`** – define the soft and hard limits for a
   `(tenant, project)` scope.
2. **`record_tokens`** – convert token usage (per provider) into cents by
   using a static cost shim and increment the counters. When the soft cap
   is crossed the manager logs a warning, while exceeding the hard cap
   raises `BudgetExceeded`.
3. **`record_cost`** – increment the counters directly with a cents
   amount, bypassing the cost shim.
4. **`get_usage` / `snapshot`** – retrieve the current counters for
   inspection or reporting.

Budgets maintain the total spend, operation count and whether a soft-cap
warning was triggered. These counters are safe for concurrent access via
an internal lock.

## Metrics

Every successful spend update increments the Prometheus counter
`budget_spend_cents{tenant=...,project=...,provider=...}`. The metric is
available through the default registry and custom registries supplied to
`BudgetManager`.

## Performance guardrail

The tests include a 95th percentile latency check (target `< 5ms`) for
`record_tokens` to keep the guardrails light-weight and suitable for
real-time evaluation.
