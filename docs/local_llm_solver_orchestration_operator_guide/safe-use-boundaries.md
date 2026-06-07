# Safe Use Boundaries

## Allowed Level 2 use

The local LLM solver orchestration path is safe only for:

- local-only development;
- operator inspection;
- diagnostics;
- controlled task exploration;
- future planning.

Allowed use remains default-off, explicit opt-in, loopback-only, no hosted-provider-key, finite-timeout, and no-hosted-fallback.

## Blocked use

Do not use this path for:

- production use;
- `/v1/solve` exposure;
- dashboard exposure;
- provider fallback;
- hosted provider routing;
- benchmark claims;
- model quality claims;
- MVP readiness;
- production readiness;
- Alpha superiority;
- evidence-model promotion;
- billing readiness.

Also do not treat local output as `/v1/solve readiness`, dashboard readiness, provider orchestration evidence, local model quality evidence, broad runtime readiness, or billing evidence.
