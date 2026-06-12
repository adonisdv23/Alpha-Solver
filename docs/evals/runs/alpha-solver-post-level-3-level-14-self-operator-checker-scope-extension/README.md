# Checker scope extension packet

Lane ID: `ALPHA-SOLVER-POST-LEVEL-3-LEVEL-14-SELF-OPERATOR-CHECKER-SCOPE-EXTENSION-001`

Purpose: extend static evidence-boundary and doc-path checker coverage to the `alpha-solver-post-*` Self Operator packet family, including the Council audit evidence bundle.

## Dependency preflight

The dependency lane `ALPHA-SOLVER-POST-LEVEL-3-LEVEL-14-SELF-OPERATOR-PRE-COUNCIL-AUDIT-005-DECISION-AND-BUNDLE-ROUTING-FIX-001` is present in the local checkout history as commit `3401b8e docs(self-operator): record pre-Council decision and routing fix (#488)`, and its packet is present at `docs/evals/runs/alpha-solver-post-level-3-level-14-self-operator-pre-council-audit-005-decision-and-bundle-routing-fix`.

## Scope

This packet documents the F-1 High/P1 checker-scope fix. It covers checker tooling, focused tests, and this lane packet only.

## Outcome

The evidence-boundary checker and doc-path checker now include current and future `docs/evals/runs/alpha-solver-post-*` text packet paths by default while preserving legacy local-LLM packet coverage.
