# Allowed Smoke Scope

Lane ID: `ALPHA-LOCAL-LLM-SMOKE-AUTHORIZATION-REFRESH-001`

A future smoke execution lane may only:

- use the endpoint-locality-hardened local adapter path;
- target a localhost / loopback endpoint;
- use an exact operator-supplied model name;
- apply a finite timeout;
- execute the approved smoke task;
- preserve raw artifacts;
- prepare a sanitized import afterward.

It must not expand into runtime routing, `/v1/solve`, dashboard preview, hosted providers, provider keys, Batch C, benchmarks, billing, or provider orchestration.
