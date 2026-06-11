# Severity rubric

```text
P0: Safety, evidence-boundary, source-artifact mutation, secret, or false readiness issue. Blocks Council completion and manual review.
P1: Breaks repeatability, lineage, required artifact review, command integrity, or evidence integrity. Blocks manual review.
P2: Should be fixed before broader repeated use, but may be explicitly deferred if the narrow Council audit can still proceed safely.
P3: Documentation clarity, UX polish, or future hardening.
```

One P0 blocks everything.

One unresolved P1 blocks manual review.

P2 must be fixed or explicitly deferred with rationale.

P3 may be backlogged.
