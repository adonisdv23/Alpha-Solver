# Exclusion Criteria

A future task candidate is excluded from this taxonomy reference if it requires or implies any forbidden action below.

## Excluded task types

- Tasks that run models, run Ollama, call providers, run benchmarks, score outputs, or claim quality.
- Tasks that expose, call, or validate `/v1/solve`.
- Tasks that expose, call, or validate dashboard routes.
- Tasks that add provider fallback, hosted fallback, billing behavior, production behavior, or product-surface behavior.
- Tasks that modify runtime, provider, CLI, checker scripts, tests, Makefile, CI, source artifacts, Level 2 packets, Level 3 packets, or release-readiness ladder files.
- Tasks that create a frozen task set, fixed benchmark suite, pass/fail threshold, leaderboard, model ranking, or accepted quality score.
- Tasks that promote Level 2 or Level 3 evidence into quality, product, benchmark, readiness, provider, dashboard, API, billing, MVP, or production claims.

## Excluded claim patterns

- Claims that Alpha Solver has demonstrated quality beyond accepted evidence.
- Claims that local orchestration evidence proves product readiness.
- Claims that a docs-only taxonomy starts Level 5 execution.
- Claims that this taxonomy selects future tasks for execution.
