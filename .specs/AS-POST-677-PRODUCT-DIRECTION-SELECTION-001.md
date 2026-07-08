# AS-POST-677-PRODUCT-DIRECTION-SELECTION-001 - Product Direction Selection

## Status

`SPEC_OK` - docs/source-truth decision packet prepared for operator review.

## Goal

Convert the post-676 roadmap reset review state into one selected product direction for Alpha Solver's next design phase.

## Motivation

PR #677 merged `AS-POST-676-NORTH-STAR-ROADMAP-RESET-001` and selected `OPERATOR_REVIEW_REQUIRED_AFTER_POST_676_NORTH_STAR_ROADMAP_RESET_001`. The reset intentionally did not select B012, B013, a real-run cockpit, or any implementation lane. This lane records the product-direction decision needed before further design work.

## Scope

- Create a product-direction selection packet under `docs/evals/runs/as-post-677-product-direction-selection-001/`.
- Select `VALUE_READ_DISCRIMINATION_WORKBENCH` as the product direction.
- Recommend `AS-B014-VALUE-READ-DISCRIMINATION-WORKBENCH-DESIGN-001` as the first follow-up design lane.
- Update source-truth docs and indexes only enough to record this selection.

## Selected direction

`VALUE_READ_DISCRIMINATION_WORKBENCH`

Plain-language name: Value Read / discrimination workbench.

This direction is selected because it best preserves Alpha Solver as a reasoning, routing, comparison, and evidence system rather than a generic prompt-runner cockpit.

## Option review

| Option | Decision | Reason |
|--------|----------|--------|
| Bounded smoke-test cockpit | Defer | Useful support surface, but not core product proof. |
| Value Read / discrimination workbench | Select | Strongest north-star alignment for evidence, comparison, capture, route context, and operator decisions. |
| Route and expert-preview surface | Defer as component or later lane | Strongly aligned, but best treated as part of the workbench or a later focused lane. |
| CLI/artifact operator companion | Defer as support infrastructure | Safe and aligned, but not the primary product direction. |
| Full real-run Operator Cockpit | Defer | Too broad without prior product and execution boundaries. |
| Read-only status checkpoint | Do not select | Already built enough for current evidence needs. |

## Recommended first follow-up lane

`AS-B014-VALUE-READ-DISCRIMINATION-WORKBENCH-DESIGN-001`

The follow-up should design the workbench as a source-truth-grounded product surface before code. It should decide artifact inputs, operator jobs, route/expert preview role, evidence boundaries, receipt/capture relationships, and what the operator can understand in 30 seconds.

## Selected next state

`OPERATOR_REVIEW_REQUIRED_AFTER_POST_677_PRODUCT_DIRECTION_SELECTION_001`

This is a review-required state, not an implementation lane. Operator review is required before implementing B014 or any workbench lane.

## Non-actions and non-claims

This lane is a source-truth product-direction decision. It does not implement UI, authorize B012, authorize B013, change runtime behavior, run model work, change scores, reveal source identities, perform final interpretation, or make value, readiness, benchmark, production, public-readiness, security/privacy, or Alpha-superiority claims.

## Definition of done

- Product-direction selection packet exists.
- Source truth records `VALUE_READ_DISCRIMINATION_WORKBENCH` as the selected direction.
- Source truth records `AS-B014-VALUE-READ-DISCRIMINATION-WORKBENCH-DESIGN-001` as the recommended first follow-up lane.
- Source truth records `OPERATOR_REVIEW_REQUIRED_AFTER_POST_677_PRODUCT_DIRECTION_SELECTION_001` as the selected next state.
- B012/B013 remain deferred.
- No runtime, execution, UI, scoring, final interpretation, or broad claim is introduced.
