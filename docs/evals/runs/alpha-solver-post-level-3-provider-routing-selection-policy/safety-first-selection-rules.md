# Safety-First Selection Rules

## Principle

Future provider selection must prefer a safe stop over an unsafe, unclear, unaudited, or unauthorized provider call.

## Safety-first rules

Future selection must stop when:

- operator authorization is absent or ambiguous;
- data sensitivity is unknown or incompatible with provider/data-egress policy;
- required capability matching is absent, stale, unknown, or failed;
- budget/spend limits are absent, exceeded, or unverifiable;
- provider logging/retention behavior conflicts with the task;
- the request requires local-only processing but only hosted providers are eligible;
- the request could promote evidence without a separate promotion decision;
- the provider route would expose a product/API/dashboard surface without approval;
- fallback/retry would occur without explicit authorization;
- safety classification is missing, contradictory, or outside policy;
- the route decision cannot be explained to an operator.

## Safety cannot be outweighed by convenience

Cost, speed, provider availability, cached success, operator convenience, or implementation simplicity must not override missing safety gates. Safety gate failure results in stop, not degraded implicit routing.

## Evidence safety

Routing output is not promoted evidence by default. Any future evidence promotion must be decided by the appropriate downstream authority and must not be inferred from successful provider execution.
