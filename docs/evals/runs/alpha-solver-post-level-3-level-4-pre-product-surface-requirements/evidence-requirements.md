# Evidence Requirements

## Required evidence categories before downstream work

Before downstream lanes can proceed, they must define evidence requirements for:

1. Quality evaluation: fixtures or datasets, scoring rules, review workflow, failure categories, reproducibility, and non-promotion boundaries.
2. API and `/v1/solve`: request and response contract design, safety boundaries, authentication assumptions, route exposure limits, error behavior, and non-execution boundaries.
3. Dashboard: display scope, operator-only versus user-facing assumptions, exposure limits, data provenance, and blocked readiness displays.
4. Provider orchestration: provider boundaries, credential assumptions, privacy requirements, timeout requirements, fallback requirements, and fail-closed behavior, without implementing fallback in a design packet.
5. Billing: metering assumptions, non-billing defaults, privacy and audit requirements, and explicit prohibition on billing execution until separately authorized.
6. MVP readiness: dependency list, prerequisite gate completion, accepted evidence references, unresolved blockers, rollback planning, and non-readiness boundary until a later review lane is authorized.

## Evidence quality requirements

Evidence must be:

- attributable to a specific artifact path;
- reproducible or reviewable by a later operator;
- fresh enough for the claim being considered;
- scoped to a specific lane;
- accompanied by pass/fail criteria;
- accompanied by contradiction handling;
- preserved without rewriting closed source artifacts.

## Insufficient evidence handling

If evidence is missing, stale, contradictory, incomplete, unsafe, or broader than the lane's claim boundary, the lane must stop and use its blocker fallback instead of inferring readiness.
