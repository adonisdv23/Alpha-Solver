# Deferred Work

The following downstream work remains deferred because this packet only defines Level 4 pre-product-surface requirements:

- Level 5 quality evaluation design, except for selecting it as the next lane.
- Product surface design.
- Provider orchestration design.
- Dashboard planning.
- `/v1/solve` planning.
- Billing planning.
- MVP readiness review.
- Runtime behavior changes.
- Local LLM provider adapter changes.
- Operator CLI changes.
- Tests, checker scripts, Makefile, and CI workflow changes.

## Why quality evaluation design is selected next

Quality evaluation design is selected next because downstream surfaces require a bounded quality framework before they can safely define user-facing claims, API behavior, dashboard displays, provider orchestration expectations, billing assumptions, or MVP review criteria.

## Why other downstream lanes remain deferred

Product surface design, provider orchestration design, and MVP readiness remain deferred because they depend on a quality evaluation design that has not yet been created or accepted. Starting those lanes before Level 5 design would risk unsupported claims, premature route or dashboard assumptions, and evidence promotion beyond the accepted Level 2 and Level 3 boundaries.
