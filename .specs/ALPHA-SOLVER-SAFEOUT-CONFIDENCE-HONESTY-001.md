# ALPHA-SOLVER-SAFEOUT-CONFIDENCE-HONESTY-001

## Objective

When the local deterministic Alpha Solver output is replaced with a bounded SAFE-OUT-style response because local synthesis is unavailable, the visible confidence must not remain inherited from the rejected prompt echo, ToT template branch, CoT fallback template, or unsupported local deterministic synthesis artifact.

## Scope

This bugfix is limited to local deterministic artifact-replacement paths. It does not add provider calls, hosted model calls, local model calls, scoring, ranking, route/persona activation, dashboard/public API changes, or `/v1/solve` exposure changes.

## Contract

- Supported deterministic fixture replacements keep existing confidence behavior.
- Unsupported SAFE-OUT replacements set visible confidence to a deterministic low value.
- Diagnostics record that confidence was adjusted because unsupported local synthesis or artifact replacement occurred.
- The rejected artifact may be retained in diagnostics for debugging, but it must not keep controlling the visible final confidence.

## Non-claims

This change is an honesty guard only. It makes no benchmark, readiness, production, provider-validation, local-model-validation, or Alpha-superiority claim.
