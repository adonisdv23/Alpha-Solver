# Claim-Boundary Display Rules

## Evidence display rule

A future dashboard may display only claims supported by the cited source artifact. If the claim is not directly supported, the dashboard must either omit it or display it as blocked.

## Required boundary labels

Dashboard displays must label evidence as one of:

- Documentation-only design.
- Static guardrail check evidence.
- Local operator usability evidence.
- Artifact-complete non-promotional local orchestration evidence.
- Draft or unaccepted evidence.
- Blocked or unsupported claim.

## Required nearby boundary language

Any future display using terms such as dashboard, product surface, readiness, quality evidence, benchmark, provider, billing, `/v1/solve`, production, MVP, Alpha superiority, or promotion must show nearby boundary language explaining what the source does and does not establish.

Required phrases for this packet's descendants include:

- This docs-only dashboard design does not create dashboard routes.
- This docs-only dashboard design does not expose dashboards.
- This docs-only dashboard design does not expose `/v1/solve`.
- This docs-only dashboard design does not call providers, run models, run benchmarks, perform billing work, or promote evidence.
- Level 6 controls whether this design is used.

## Prohibited display claims

A future dashboard must not claim or imply:

- Dashboard readiness.
- Product-surface readiness.
- MVP readiness.
- Production readiness.
- `/v1/solve` readiness.
- Provider readiness.
- Billing readiness.
- Benchmark success.
- Local model quality.
- Alpha superiority.
- Evidence-model promotion.

## Release gate before display

Before any dashboard display is implemented, a later authorized lane must prove that the display can preserve these claim-boundary rules without changing checker scripts, tests, Makefile targets, CI, runtime code, provider behavior, API exposure, or evidence artifacts.
