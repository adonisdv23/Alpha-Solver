# Implementation scope rules for future lanes

## Required before behavior changes

1. Start from an approved Self Operator MVP spec or update an existing relevant spec before changing behavior.
2. Define whether the lane is inspect-only, docs-only, test-only, guardrail-only, or runtime implementation.
3. State the exact entrypoint and runtime surfaces in scope.
4. State which sensitive surfaces are explicitly out of scope.
5. Add or update focused tests before broad regression claims.
6. Preserve default-off, local-only, no-silent-hosted-fallback, fail-closed, and non-evidence boundaries unless a later approved spec explicitly changes them.

## May inspect vs. may modify later

- `may inspect` means a future lane can read the file to understand contracts, dependencies, and risks.
- `may modify later` means modification is possible only after a separate approved implementation scope names that file or surface.
- This packet grants no current permission to modify runtime, tests, scripts, CI, API, provider, dashboard, credentials, source artifacts, or generated artifacts.

## Narrow implementation preference

- Prefer local LLM operator CLI and local orchestration surfaces first if future Self Operator MVP behavior is local/operator-only.
- Prefer focused tests for the exact changed behavior.
- Avoid broad refactors, opportunistic cleanup, or cross-surface consolidation.
- Keep historical evidence packets immutable unless the future lane is an explicitly authorized packet repair lane.

## Required future validation pattern

A future implementation lane should run the most focused relevant tests first, then the local LLM guardrail suite, then broader `python -m pytest -q` when practical. Any skipped live, hosted-provider, local-model, dashboard, or deployment check must be reported with the reason.
