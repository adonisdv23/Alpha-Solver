# Stop Conditions

## Stop-condition purpose

Stop conditions define when future provider routing or selection must not proceed.

## Required stop conditions

Future routing and selection must stop when any of the following applies:

1. Level 7 has not authorized use of this packet or a downstream implementation contract.
2. The request class is outside the approved routing scope.
3. The provider set is undefined, ambiguous, or not operator-approved.
4. Required selection inputs are missing, stale, contradictory, or unverifiable.
5. Required capability matching fails or returns unknown for a mandatory capability.
6. Data sensitivity conflicts with provider locality, logging, retention, or egress policy.
7. Budget, spend, billing, retry, or quota controls are absent or exceeded.
8. Operator confirmation is required but missing.
9. A provider would be selected by implicit default, hidden fallback, configuration order, credential presence, availability alone, cost alone, or speed alone.
10. A fallback or retry would occur without explicit authorization.
11. Execution would expose `/v1/solve` or any product/API/dashboard surface without separate approval.
12. Execution would run a model, benchmark, provider call, or billing workflow outside the approved implementation scope.
13. Execution would promote evidence or change evidence status without a separate promotion decision.
14. The route decision cannot be logged or shown to the operator in an understandable form.

## Stop outcome

A stop is a valid routing outcome. Future systems should record the stop reason rather than silently choosing another provider or continuing through a hidden path.
