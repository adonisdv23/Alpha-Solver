# Blocker fallback lane

If this lane's outputs are later found defective (for example, the decision
was misrecorded or misattributed, the decision artifact misstates its scope or
schema, or the prerequisite verification in this packet misstates the #468
state), the fallback lane is:

```
ALPHA-SOLVER-POST-LEVEL-3-LEVEL-13-TO-LEVEL-14-SELF-OPERATOR-EXPECTED-SAFETY-BLOCK-OPERATOR-REVIEW-FIX-001
```

A defective decision record must be corrected by a new packet in that fix
lane, never by mutating this packet or any earlier evidence in place. If the
operator instead withdraws the acceptance, the withdrawal is likewise a new
explicit decision artifact in a new lane, and the commission-rerun branch of
#468's `operator-review-required.md` becomes available again.
