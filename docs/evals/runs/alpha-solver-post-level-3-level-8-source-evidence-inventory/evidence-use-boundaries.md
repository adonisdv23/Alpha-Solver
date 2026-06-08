# Evidence Use Boundaries

## Authorized uses

This packet may be used only to:

- identify source packets Level 8 should review;
- separate accepted evidence from supporting references;
- identify guardrails and checker scripts Level 8 should run or inspect;
- identify missing, stale, contradictory, pending, or non-usable evidence;
- preserve docs-only boundaries before any later authorized lane.

## Unauthorized uses

This packet does not authorize implementation. It must not be used to:

- implement Self Operator;
- claim Self Operator exists or is ready;
- run Self Operator;
- run models or benchmarks;
- call hosted or local providers;
- configure credentials;
- expose or exercise `/v1/solve`;
- expose or exercise dashboard routes;
- deploy services;
- promote source artifacts or docs-only design packets into accepted runtime evidence;
- modify runtime, tests, scripts, CI, API routes, dashboard routes, provider code, or specs outside this packet.

## Claim boundaries

Accepted evidence may support only the status explicitly recorded in the accepted source packets, such as Level 3 artifact-complete non-promotional local orchestration evidence and docs-only downstream design boundaries. Supporting references may support inventory traceability only. Missing or pending evidence must be named as missing or pending and must not be filled by inference.
