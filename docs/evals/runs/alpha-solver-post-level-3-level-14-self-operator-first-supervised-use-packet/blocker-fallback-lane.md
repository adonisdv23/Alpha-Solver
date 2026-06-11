# Blocker fallback lane

If this packet lane is blocked (out-of-scope change, packet defect, failed
check, no safe target selectable, or any remaining forbidden-claim
classification):

`ALPHA-SOLVER-POST-LEVEL-3-LEVEL-14-SELF-OPERATOR-FIRST-SUPERVISED-USE-PACKET-FIX-001`

Fallback if the fix lane cannot proceed:

`ALPHA-SOLVER-POST-LEVEL-3-LEVEL-14-SELF-OPERATOR-FIRST-SUPERVISED-USE-PACKET-FALLBACK-001`

The future execution lane routes its own blockers (including every stop
state and abort in `stop-state-rules.md` and `abort-conditions.md`) to the
same fix lane, with a fresh approval record and a fresh run ID.

Routing rule: on any blocker, stop the owning lane, preserve all evidence
as written, record the blocker in that lane's packet, and continue only in
the fix lane. Do not weaken inputs, do not edit prior evidence, and do not
recreate earlier evidence.
