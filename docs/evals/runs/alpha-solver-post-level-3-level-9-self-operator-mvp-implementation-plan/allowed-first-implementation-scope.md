# Allowed First Implementation Scope

This file defines the only scope the first actual code lane may consider, after the Level 10 lane is separately approved by an operator. This packet does not authorize that implementation and does not implement Self Operator.

## First code lane is static tests only

The first actual code lane is static test scaffold implementation, not runtime behavior. The first code lane may add only:

- A dedicated static-test location for Self Operator guardrails (for example `tests/static/self_operator/` or an equivalent repo-approved test directory).
- Deterministic, offline static tests that inspect source text, AST nodes, configuration text, and fixtures.
- Static-test fixtures representing allowed (safe) and blocked (unsafe) code patterns.
- Shared static-scan and finding-schema helpers used only by those static tests.
- Documentation that explains the static-test scaffold boundary.

## Scope constraints

The first implementation scope must remain:

- local-only;
- operator-supervised;
- static-analysis-only (text/AST inspection, with no import of target runtime modules that could trigger side effects);
- deterministic and offline;
- with no provider calls, no hosted model calls, no external API calls, no credentials, no browser automation, no deployment, no billing, no route exposure, no fallback, and no evidence promotion.

## Ordering rule

Static tests are required before any runtime wrapper or CLI behavior. No runtime scaffold, runner entrypoint, CLI flag, or Self Operator behavior may be implemented in the first code lane. Those remain blocked until a later, separately approved lane after the static test scaffold exists and passes.
