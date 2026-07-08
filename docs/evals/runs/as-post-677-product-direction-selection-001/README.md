# AS-POST-677-PRODUCT-DIRECTION-SELECTION-001

## TLDR

Select `VALUE_READ_DISCRIMINATION_WORKBENCH` as the product direction after the post-676 roadmap reset. Recommend `AS-B014-VALUE-READ-DISCRIMINATION-WORKBENCH-DESIGN-001` as the first follow-up design lane.

## Why this decision exists

PR #677 reset the roadmap after the Operator Console sequence and left the repository in `OPERATOR_REVIEW_REQUIRED_AFTER_POST_676_NORTH_STAR_ROADMAP_RESET_001`. That state requires a product-direction selection before any next design or implementation lane.

## Source-truth baseline

- PR #677 merge commit: `57d2a450250b9b9d70c3b936fced46a1503fb939`.
- B012/B013-style cockpit work remains deferred.
- Operator Console work is adjacent/supporting context, not the selected product direction.
- No broad project claims are added by this lane.

## Selected direction

`VALUE_READ_DISCRIMINATION_WORKBENCH`

Plain-language name: Value Read / discrimination workbench.

## Why this direction

This direction best preserves Alpha Solver as a reasoning, routing, comparison, and evidence system. It keeps the next product surface focused on case packets, captured outputs, route/expert context, evidence boundaries, comparison workflow, and operator decisions.

## Deferred directions

- Bounded smoke-test cockpit: defer as support surface.
- Route and expert-preview surface: defer as component or later focused lane.
- CLI/artifact operator companion: defer as support infrastructure.
- Full real-run Operator Cockpit: defer until product and execution boundaries are separately selected.
- Read-only status checkpoint: do not select as next.

## Recommended first follow-up lane

`AS-B014-VALUE-READ-DISCRIMINATION-WORKBENCH-DESIGN-001`

This follow-up should be design-only. It should define the workbench purpose, artifact inputs, operator workflows, route/expert preview role, evidence and receipt boundaries, and implementation stop conditions.

## Selected next state

`OPERATOR_REVIEW_REQUIRED_AFTER_POST_677_PRODUCT_DIRECTION_SELECTION_001`

## Non-actions

This lane does not implement UI, change runtime behavior, select B012, select B013, run model work, change scores, reveal source identities, perform final interpretation, or mutate external ledgers.

## Non-claims

This lane does not claim value, readiness, benchmark success, production suitability, public readiness, security/privacy completion, or Alpha superiority.

## Checks

See `checks-run.md`.
