# Budget and cost guards

## Policy intent

Future timeout, retry, and circuit-breaker behavior must be constrained by budget and cost guardrails before provider orchestration can run. Cost controls must be defined before any retry expansion increases provider spend.

## Required future guardrails

A future implementation must define:

- per-request maximum provider attempts;
- per-request estimated maximum token budget;
- per-request estimated maximum provider cost;
- per-tenant or per-operator spend controls, if the future lane supports tenancy;
- behavior when estimated cost is unknown;
- accounting fields for attempts, retry count, timeout status, breaker state, and final status;
- stop behavior when a cost or budget guard is exceeded.

## Unknown-cost behavior

Unknown cost must not be fabricated. If a future request cannot estimate or record the required budget fields safely, the implementation must either omit unknown values in explicit allowlisted records or fail closed when the missing value is required for a pre-call guard.

## Retry cost interaction

Retry policy must count all attempts against budget. A later implementation must not treat retries as free, invisible, or outside budget accounting.

## Billing boundary

This packet does not perform billing work, does not query billing APIs, does not create spend dashboards, does not persist budget ledgers, and does not promote any cost evidence.
