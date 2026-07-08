# Alpha Solver - Current State

> Source-of-truth navigation doc. Last verified **2026-07-08** for `AS-POST-677-PRODUCT-DIRECTION-SELECTION-001`.
> This selection records `VALUE_READ_DISCRIMINATION_WORKBENCH` as the product direction after the post-676 reset and recommends `AS-B014-VALUE-READ-DISCRIMINATION-WORKBENCH-DESIGN-001` as the first follow-up design lane.

## Current verified phase

**Post-677 product-direction selection completed: Value Read / discrimination workbench selected for operator review.**

The previous selected state was `OPERATOR_REVIEW_REQUIRED_AFTER_POST_676_NORTH_STAR_ROADMAP_RESET_001`. This lane resolves that review state into one product direction. It does not implement B014, UI, runtime behavior, B012, B013, scoring, unblinding, final interpretation, or broad claims.

The selected direction is `VALUE_READ_DISCRIMINATION_WORKBENCH` because it best preserves Alpha Solver as a reasoning, routing, comparison, evidence, and operator-control system rather than a generic prompt-runner cockpit.

## At a glance

| Field | Value |
|-------|-------|
| Latest product-direction lane | **`AS-POST-677-PRODUCT-DIRECTION-SELECTION-001`** |
| Selected product direction | **`VALUE_READ_DISCRIMINATION_WORKBENCH`** |
| Current selected next state | **`OPERATOR_REVIEW_REQUIRED_AFTER_POST_677_PRODUCT_DIRECTION_SELECTION_001`** |
| Recommended first follow-up lane | **`AS-B014-VALUE-READ-DISCRIMINATION-WORKBENCH-DESIGN-001`** |
| B012/B013 posture | Deferred pending separate operator decision; not authorized by this lane |
| Prior selected next state | `OPERATOR_REVIEW_REQUIRED_AFTER_POST_676_NORTH_STAR_ROADMAP_RESET_001` is historical prior context only |
| Strategic boundary | This lane selects a product direction only; it authorizes no runtime behavior, UI implementation, model work, scoring, unblinding, final interpretation, readiness claim, value claim, or Alpha-superiority claim |

## Product direction selection

`VALUE_READ_DISCRIMINATION_WORKBENCH` is selected as the next product direction.

This direction should focus on:

- case packets
- captured outputs
- comparison state
- route/expert context
- SAFE-OUT and confidence boundaries
- evidence and receipt boundaries
- operator understanding and next safe action

## Recommended first follow-up

`AS-B014-VALUE-READ-DISCRIMINATION-WORKBENCH-DESIGN-001`

This follow-up should be design-only. It should define what the workbench is, what artifacts it reads, what workflows it supports, what the operator should understand in 30 seconds, and what implementation lane, if any, should follow.

## Deferred directions

- Bounded smoke-test cockpit: deferred as support surface.
- Route and expert-preview surface: deferred as component or later focused lane.
- CLI/artifact operator companion: deferred as support infrastructure.
- Full real-run Operator Cockpit: deferred until separate product and execution boundaries exist.
- Read-only status checkpoint: not selected as next.

## What is blocked / not authorized

- B012 implementation.
- B013 real-run provider work.
- Runtime behavior changes.
- UI implementation.
- New routes or write paths.
- Model work.
- Score changes.
- Unblinding or source identity reveal.
- Final interpretation.
- External ledger mutation.
- Broad value, readiness, benchmark, production, public-readiness, security/privacy, or Alpha-superiority claims.

## Historical context

PR #677 merged `AS-POST-676-NORTH-STAR-ROADMAP-RESET-001` and recorded the post-#663 through post-#676 Operator Console sequence as adjacent/supporting work. The reset selected `OPERATOR_REVIEW_REQUIRED_AFTER_POST_676_NORTH_STAR_ROADMAP_RESET_001`, which this lane now resolves into a product-direction selection.

Historical lanes remain preserved in `docs/EVIDENCE_INDEX.md` and `docs/LANE_REGISTRY.md`.
