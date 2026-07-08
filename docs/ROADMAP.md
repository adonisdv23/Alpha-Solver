# Roadmap

> Refreshed **2026-07-08** for `AS-POST-677-PRODUCT-DIRECTION-SELECTION-001`.
> Source of truth for current state: [`CURRENT_STATE.md`](CURRENT_STATE.md).
> This roadmap makes no readiness, provider-validation, benchmark, production, or Alpha-superiority claims.

## Current phase

**Post-677 product-direction selection.** The selected product direction is `VALUE_READ_DISCRIMINATION_WORKBENCH`.

The post-676 reset review state has been resolved into a product-direction decision. The next recommended lane is design-only: `AS-B014-VALUE-READ-DISCRIMINATION-WORKBENCH-DESIGN-001`.

B012/B013-style cockpit work remains deferred. This roadmap selection authorizes no implementation, runtime behavior change, `/v1/solve` exposure, scoring, unblinding, final interpretation, or broad project claims.

## Current next state

**`OPERATOR_REVIEW_REQUIRED_AFTER_POST_677_PRODUCT_DIRECTION_SELECTION_001`** - operator review is required before implementing the first workbench lane.

## Recommended next lane

`AS-B014-VALUE-READ-DISCRIMINATION-WORKBENCH-DESIGN-001`

Purpose: design the Value Read / discrimination workbench as a source-truth-grounded product surface before code.

## Near-term roadmap after product-direction selection

1. Operator reviews the product-direction selection.
2. If accepted, create or dispatch B014 as a design-only lane.
3. B014 defines the workbench job, artifact inputs, workflow boundaries, route/expert preview role, evidence and receipt relationship, and operator 30-second understanding target.
4. No implementation lane follows until B014 names it and the operator approves it.
5. B012/B013 remain deferred until separately selected.

## Active deferrals

See [`DEFERRAL_REGISTER.md`](DEFERRAL_REGISTER.md).

- **DEF-001** - Self Operator execution evidence: advanced within local-only scope; not broad runtime proof.
- **DEF-002** - Security/privacy review: open.
- **DEF-003** - Fable delta-audit custody/replacement: open.
- **DEF-004** - Audit custody/provenance: open.

## Historical roadmap context

`AS-POST-676-NORTH-STAR-ROADMAP-RESET-001` selected `OPERATOR_REVIEW_REQUIRED_AFTER_POST_676_NORTH_STAR_ROADMAP_RESET_001`. `AS-POST-677-PRODUCT-DIRECTION-SELECTION-001` resolves that state by selecting `VALUE_READ_DISCRIMINATION_WORKBENCH`.

The earlier `ALPHA-SOLVER-VALUE-READ-EXECUTION-PACKET-AUTHORIZATION-001` item remains historical pre-reset context only. It is not the current selected next lane.

The pre-#100 roadmap is preserved as historical context only.
