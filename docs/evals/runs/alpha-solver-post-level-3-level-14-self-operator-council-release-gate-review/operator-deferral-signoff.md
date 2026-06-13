# Operator deferral sign-off traceability review

This file handles the release-gate traceability issue identified after PR #493 review: `release-gate-acceptance-criteria.md` requires the deferral register to include operator sign-off for each open deferral, but `deferral-register.md` does not define a per-deferral sign-off table or recording mechanism.

## Sign-off evidence rule

This review does not fabricate operator acceptance. A deferral is treated as operator-signed only if the repository evidence records explicit operator sign-off for that deferral or if an operator-provided artifact is supplied to this gate and cited.

## Per-deferral status

| Deferral | Subject | Open? | Operator sign-off evidence in repository | Gate status |
|---|---|---|---|---|
| DEF-001 | Self Operator execution evidence | Yes | Missing. The deferral is recorded, but no per-deferral operator sign-off is present. | Required before gate can pass. |
| DEF-002 | Product-level security/privacy review | Yes | Missing. The deferral is recorded, but no per-deferral operator sign-off is present. | Required before gate can pass. |
| DEF-003 | Prior targeted Fable delta audit full text | Yes | Missing. The deferral is recorded, but no per-deferral operator sign-off is present. | Required before gate can pass. |
| DEF-004 | Custody note: Council raw capture and synthesis report | Custody note | Missing in repository. The custody note is recorded, but the operator-held documents are not in repo and are not marked produced for this gate. | Not blocking for this gate if the operator can produce the documents on request; remains a custody traceability note. |

## Finding

The P2 deferral register says that operator acceptance of the packet constitutes acceptance of the deferrals as recorded. That statement is not a per-deferral sign-off record. The repository does not currently include a signed or otherwise explicit operator acceptance table for DEF-001, DEF-002, or DEF-003. DEF-004 is different: the source deferral register records it as a custody note that is not required for the release-gate review lane if the operator can produce the documents on request.

## Gate effect

Because open-deferral operator sign-off is required by the release-gate acceptance criteria for DEF-001, DEF-002, and DEF-003, and that sign-off is not recorded in repository evidence, the gate outcome is:

`BLOCKED_PENDING_OPERATOR_SIGNOFF`

This block does not assert a P0/P1 product defect. It only records that the release-gate evidence cannot be passed until operator sign-off for the hard deferrals is explicitly recorded or the operator directs a different bounded evidence treatment.
