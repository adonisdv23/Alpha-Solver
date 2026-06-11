# Synthesis instructions

Use only completed seat responses and the evidence manifest. Do not inspect live systems or execute commands. Do not convert any narrow evidence into broad readiness claims.

This is evidence for a narrow local-only operator-supervised Self Operator candidate. Do not infer production readiness, hosted readiness, runtime readiness, provider readiness, benchmark superiority, broad MVP readiness, release readiness, or autonomous readiness.

## Required synthesis output

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
- If clean enough for the future manual run lane, select `ALPHA-SOLVER-POST-LEVEL-3-LEVEL-14-SELF-OPERATOR-COUNCIL-AUDIT-MANUAL-RUN-001`.
