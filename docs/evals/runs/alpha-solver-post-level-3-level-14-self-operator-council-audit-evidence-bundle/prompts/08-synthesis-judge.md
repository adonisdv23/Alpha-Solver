# Synthesis Judge

This is evidence for a narrow local-only operator-supervised Self Operator candidate. Do not infer production readiness, hosted readiness, runtime readiness, provider readiness, benchmark superiority, broad MVP readiness, release readiness, or autonomous readiness.

Use `prompts/00-common-instructions.md`, all completed non-synthesis Council seat outputs, `defect-register-template.md`, and `synthesis-instructions.md`. Do not run commands and do not inspect live systems.

## Prohibited actions

```text
provider calls
hosted model calls
local model calls
external APIs
browser automation
deployment
billing
credential access
secret access
/v1/solve exposure
dashboard exposure
source-artifact mutation
evidence promotion
readiness claims
autonomous operation claims
benchmark superiority claims
```

## Required synthesis output format

```text
1. consolidated defect register
2. block/no-block decision for manual operator review
3. required Codex repair prompts
4. deferred items
5. final selected next lane
6. evidence-boundary caveats
```

## Decision rules

- One P0 blocks everything.
- One unresolved P1 blocks manual review.
- P2 must be fixed or explicitly deferred with rationale.
- P3 may be backlogged.
- If blocked, select `ALPHA-SOLVER-POST-LEVEL-3-LEVEL-14-SELF-OPERATOR-COUNCIL-AUDIT-EVIDENCE-BUNDLE-FIX-001`.
- If not blocked for the future manual Council run, select `ALPHA-SOLVER-POST-LEVEL-3-LEVEL-14-SELF-OPERATOR-COUNCIL-AUDIT-MANUAL-RUN-001`.
