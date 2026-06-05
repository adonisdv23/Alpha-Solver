# Smoke Preconditions

Lane ID: `ALPHA-LOCAL-LLM-SMOKE-AUTHORIZATION-REFRESH-001`

A future local smoke execution lane must require:

- endpoint-locality hardening merged and recorded in GS;
- explicit operator approval;
- localhost or loopback endpoint only;
- exact operator-supplied model name;
- finite timeout;
- no hosted provider fallback;
- no provider keys or access material;
- raw artifact preservation before any summary;
- sanitized import after execution;
- no readiness, quality, benchmark, production, runtime, `/v1/solve`, provider-orchestration, Batch C, or Alpha-superiority claims.
