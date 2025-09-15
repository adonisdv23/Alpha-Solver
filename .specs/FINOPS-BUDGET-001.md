# FINOPS-BUDGET-001 · Budget Guardrails

## Goal
Implement FinOps budget guardrails that enforce soft/hard caps while
exporting spend metrics.

## Acceptance Criteria
- Budget counters maintained for each tenant/project scope.
- Soft cap emits a warning; hard cap blocks with `BudgetExceeded`.
- Prometheus counter `budget_spend_cents` records spend in cents.
- `record_tokens` remains fast (p95 latency under 5ms in tests).
- All new tests pass.

## Notes
- Uses an in-memory cost shim with static per-provider token pricing.
- Metrics should work with the default registry and custom registries.
