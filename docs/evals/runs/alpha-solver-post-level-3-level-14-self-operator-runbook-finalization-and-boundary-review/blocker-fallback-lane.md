# Blocker fallback lane

If this lane's outputs are later found defective — for example, the runbook
is shown to contradict accepted evidence, the boundary review is shown to
have missed a present surface, or a scope violation is found in the
changed-file set — the fallback lane is:

```text
ALPHA-SOLVER-POST-LEVEL-3-LEVEL-14-SELF-OPERATOR-RUNBOOK-FINALIZATION-AND-BOUNDARY-REVIEW-FIX-001
```

That lane would correct the runbook and redo the boundary review, without
mutating this packet in place. For a defect that is specifically a boundary
finding (a blocked surface present in evidence), the boundary fix lane
`ALPHA-SOLVER-POST-LEVEL-3-LEVEL-14-SELF-OPERATOR-EVIDENCE-BOUNDARY-REVIEW-FIX-001`
is the route instead.
