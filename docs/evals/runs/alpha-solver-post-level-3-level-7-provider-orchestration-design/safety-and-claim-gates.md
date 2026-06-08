# Safety and Claim Gates

## Provider-backed safety gates

Future provider-backed behavior must pass safety gates before any provider output can be treated as a successful answer. Required gates include:

- provider eligibility gate;
- credential availability and boundary gate;
- request-shape and token-budget gate;
- prompt/content policy gate where applicable;
- provider response parsing gate;
- unsafe/empty/malformed/echo output gate;
- provenance completeness gate;
- cost/quota gate;
- fallback eligibility gate when fallback is explicitly enabled;
- claim-boundary gate before output can be referenced as evidence.

## Claim gates

Provider-backed output must not be claimed as MVP-ready, production-ready, benchmarked, superior, cost-controlled, safe for hosted fallback, or validated for `/v1/solve` until the required downstream review lanes accept evidence for those claims.

## Preserved prior evidence boundaries

Level 2 remains local operator usability evidence only. Level 3 remains artifact-complete, non-promotional local orchestration evidence only. Level 4, Level 5, and Level 6 remain requirements/design evidence only. This Level 7 packet does not promote any prior evidence and does not create provider-backed evidence.
