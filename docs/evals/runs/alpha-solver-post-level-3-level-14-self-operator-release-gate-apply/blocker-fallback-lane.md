# Blocker fallback lane

If this lane's outputs are later found defective — for example, the checker
fix is shown to mask a genuine defect marker, the recorded gate result is
shown to be non-deterministic, or a scope violation is found — the fallback
lane is:

```text
ALPHA-SOLVER-POST-LEVEL-3-LEVEL-14-SELF-OPERATOR-RELEASE-GATE-APPLY-FIX-001
```

That lane would re-run the release gate after correcting the defect, without
mutating this packet in place.
