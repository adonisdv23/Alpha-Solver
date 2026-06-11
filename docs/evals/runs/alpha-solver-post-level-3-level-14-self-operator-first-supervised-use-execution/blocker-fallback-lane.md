# Blocker fallback lane

If the execution portion of this combined lane had been blocked (any stop
state, abort condition, failed check, redaction finding, or remaining
forbidden-claim / unsafe-pattern classification):

`ALPHA-SOLVER-POST-LEVEL-3-LEVEL-14-SELF-OPERATOR-FIRST-SUPERVISED-USE-BLOCKER-FIX-001`

Fallback if that fix lane cannot proceed:

`ALPHA-SOLVER-POST-LEVEL-3-LEVEL-14-SELF-OPERATOR-FIRST-SUPERVISED-USE-REPAIR-AND-EXECUTION-FALLBACK-001`

(Repair-portion blockers before execution route instead per the repair
packet's `blocker-fallback-lane.md`.)

Routing rule: on any blocker, stop the owning lane, preserve all evidence
and stop-state artifacts exactly as written, record the blocker in this
packet, and continue only in the fix lane — with a fresh approval record
and a fresh run ID. Do not weaken inputs, do not edit prior evidence, do
not recreate earlier evidence, and never retry in place. No blocker
occurred in this run (`stop-state-record.md`).
