# Stop Conditions

A future lane must stop if any condition below applies.

## Claim stop conditions

Stop if:

- proposed copy contains a blocked claim;
- proposed copy implies a blocked claim indirectly;
- proposed copy lacks exact supporting evidence;
- proposed copy generalizes beyond the evidence boundary;
- proposed copy treats this docs-only packet as claim authorization;
- proposed copy cannot preserve non-promotion rules.

## Evidence stop conditions

Stop if:

- required evidence is missing, stale, contradictory, or unauditable;
- evidence is not tied to exact artifacts, commands, dates, environments, sample sets, and acceptance gates;
- the evidence was created by a lane that did not authorize the relevant claim;
- the future lane would need to run models, run benchmarks, call providers, perform billing work, expose dashboards, or expose `/v1/solve` without separate authorization.

## Surface stop conditions

Stop if:

- UI copy would be implemented before a separately authorized lane approves the exact surface;
- API response copy would be implemented before a separately authorized lane approves the exact route;
- dashboard copy would be exposed before dashboard exposure is separately authorized;
- `/v1/solve` would be exposed before `/v1/solve` exposure is separately authorized;
- billing, provider, or fallback behavior would be represented as ready without separate evidence and authorization.

## Governance stop condition

Stop if Level 6 has not decided whether and how this packet is used for the future surface under consideration.
