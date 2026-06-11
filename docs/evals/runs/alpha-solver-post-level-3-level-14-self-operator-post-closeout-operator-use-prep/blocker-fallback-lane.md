# Blocker fallback lane

If this prep lane is blocked (out-of-scope change, packet defect, failed
check, or any remaining forbidden-claim classification):

`ALPHA-SOLVER-POST-LEVEL-3-LEVEL-14-SELF-OPERATOR-POST-CLOSEOUT-OPERATOR-USE-PREP-FIX-001`

Fallback if the fix lane cannot proceed:

`ALPHA-SOLVER-POST-LEVEL-3-LEVEL-14-SELF-OPERATOR-POST-CLOSEOUT-OPERATOR-USE-PREP-FALLBACK-001`

Routing rule: on any blocker, stop this lane, preserve all evidence as
written, record the blocker in this packet, and continue only in the fix
lane. Do not weaken inputs, do not edit prior evidence, and do not recreate
earlier evidence (`stop-state-response-plan.md` defines the same rule for
future supervised use).
