# Blocker fallback lane (repair portion)

If the repair portion of this combined lane is blocked before execution
(repair cannot be completed safely, a verification check fails, or any
unsafe executable-plan pattern remains):

`ALPHA-SOLVER-POST-LEVEL-3-LEVEL-14-SELF-OPERATOR-FIRST-SUPERVISED-USE-PACKET-REPAIR-FIX-001`

Fallback if that fix lane cannot proceed:

`ALPHA-SOLVER-POST-LEVEL-3-LEVEL-14-SELF-OPERATOR-FIRST-SUPERVISED-USE-REPAIR-AND-EXECUTION-FALLBACK-001`

Routing rule: on any blocker, stop the owning lane, preserve all evidence
as written, record the blocker in this packet, and continue only in the fix
lane. Do not weaken inputs, do not edit prior evidence, and do not recreate
earlier evidence. Execution blockers (after the repair gate) route per the
execution packet's `blocker-fallback-lane.md` instead.
