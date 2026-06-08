# Circuit-breaker policy

## Policy intent

Future provider orchestration must define circuit-breaker behavior before enabling repeated provider calls across requests. The breaker must protect users, operators, and budgets from repeated failing provider interactions.

## Required breaker states

A future implementation must define stable state labels equivalent to:

- `closed`: provider attempts are allowed subject to normal guards;
- `open`: provider attempts are blocked and fail closed;
- `half_open`: a bounded probe may be allowed only if explicitly authorized by the future implementation lane.

## Required opening conditions

A future implementation must define quantitative thresholds for opening the circuit, such as:

- consecutive retry-exhausted provider failures;
- rolling-window timeout rate;
- rolling-window provider error rate;
- rolling-window budget guard failures;
- provider safety or SAFE-OUT rejection rate when applicable;
- operator-forced open state.

## Required closing and probing conditions

A future implementation must define:

- cool-down duration before any half-open probe;
- maximum half-open probes;
- success criteria to return to closed;
- failure criteria to return to open;
- whether breaker state is process-local, persistent, tenant-scoped, provider-scoped, model-scoped, or route-scoped.

## Fail-closed requirement

When breaker state is missing, corrupted, stale beyond an accepted window, or impossible to evaluate safely, provider orchestration must fail closed. It must not silently ignore breaker state or route to another provider as fallback.

## Evidence boundary

This circuit-breaker policy is docs-only. It does not add circuit-breaker state, provider calls, retries, fallback, runtime behavior, dashboards, tests, benchmarks, billing, or evidence promotion.
