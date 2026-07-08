# AS-B015-VALUE-READ-WORKBENCH-SOURCE-MAP-AND-STATIC-PROTOTYPE-001

## Status

Completed for operator review.

## Goal

Convert the B014 `VALUE_READ_DISCRIMINATION_WORKBENCH` design into a precise source map and static prototype plan.

## Motivation

Before any mockup or implementation, the workbench needs exact boundaries for which committed files, packet families, inferred states, unknowns, and future-required adapters can support each display field.

## Source context

This lane follows `AS-B014-VALUE-READ-DISCRIMINATION-WORKBENCH-DESIGN-001`, merged by PR #679. B014 selected a source-truth-grounded Value Read / discrimination workbench and recommended this B015 source-map/static-prototype planning lane.

## Scope

- Create the B015 packet under `docs/evals/runs/as-b015-value-read-workbench-source-map-and-static-prototype-001/`.
- Create source-map, field-inventory, status-taxonomy, data-readiness, claim-boundary, static-prototype, and implementation-gate planning docs.
- Update source-truth docs narrowly for the B015 review state.

## Non-goals

This lane is a docs/source-truth source-map and static prototype planning lane. It does not implement UI, execute providers, authorize B012, authorize B013, expose `/v1/solve`, run models, score outputs, unblind results, perform final interpretation, or make value/readiness/superiority claims.

## Allowed files

Only docs/spec/source-truth and static prototype planning files are allowed: this spec, the B015 packet docs, `.specs/INDEX.md`, `docs/CURRENT_STATE.md`, `docs/ROADMAP.md`, `docs/EVIDENCE_INDEX.md`, and `docs/LANE_REGISTRY.md`.

## Source-truth preservation rule

Detailed registry, history, completed, superseded, blocked, do-not-run-again, and DAG sections must be preserved. Updates must be narrow current-state additions only.

## Exact-source discipline

The source map must distinguish exact committed files, packet families, inferred statuses, unknown/missing sources, and `future_required` implementation needs. It must not invent source files, source fields, statuses, or evidence.

## Source-map requirements

`source-map-table.md` must map current packet, artifact completeness, comparison state, route/expert context, claim/safety boundary, and operator next action to source files or packet families with certainty and fallback text.

## Field inventory requirements

`field-inventory.md` must define all static prototype fields, including packet identity, lifecycle, output status, blind/scoring/lock/source-identity/interpretation state, route/SAFE-OUT/confidence state, claims, missing artifacts, blocked actions, and check results.

## Status taxonomy requirements

`status-taxonomy.md` must define controlled conservative values including `present`, `missing`, `unknown`, `not_applicable`, `blocked`, `authorized`, `not_authorized`, `blank`, `locked`, `reviewed`, `hidden`, `out_of_scope`, `historical_only`, `support_context_only`, and `future_required`.

## Static prototype plan requirements

`static-prototype-plan.md` must describe a static, non-interactive prototype plan only. It must not create a functioning static mockup asset.

## First-screen wireframe requirements

`first-screen-wireframe.md` must be text-only and answer what the operator is reviewing, whether it is complete, what can safely happen next, and what cannot be claimed.

## Data-readiness rules

`data-readiness-rules.md` must define rules for output collection, scoring, scoring lock, interpretation, source identity, review-only, and stop/defer states.

## Claim-boundary map

`claim-boundary-map.md` must map display areas to allowed bounded statements, blocked claims, why blocked, and safe wording.

## Implementation-readiness gate

`implementation-readiness-gate.md` must state that no runtime implementation is authorized and recommend exactly one next lane or stop/defer.

## Recommended next lane

`AS-B016-VALUE-READ-WORKBENCH-STATIC-MOCKUP-001`

Purpose: create a static, non-runtime workbench mockup from the B015 source map and wireframe. B016 remains static only unless separately authorized.

## Selected next state

`OPERATOR_REVIEW_REQUIRED_AFTER_B015_VALUE_READ_WORKBENCH_SOURCE_MAP_STATIC_PROTOTYPE_001`

The B015 source map and static prototype plan are complete for operator review. Implementation is not authorized. B016 static mockup is recommended. B012/B013 remain deferred. No provider calls, `/v1/solve` exposure, scoring, unblinding, final interpretation, or value/readiness/superiority claim is authorized.

## Non-actions

No provider calls, hosted model calls, local model calls, `/v1/solve`, browser automation, UI shell execution, queue/runner/scheduler/worker/background job, web route, POST route, write path, runtime behavior change, live UI, functional static mockup asset, B012/B013 implementation, scoring, unblinding, source identity reveal, final interpretation, Google Sheets mutation, validation claims, broad claims, generic LLM playground behavior, or Roadmap HP repo module.

## Non-claims

No readiness, value, benchmark, provider-validation, local-model-validation, production, public-readiness, security/privacy, Alpha-superiority, output-quality, model-quality, operator-usability, or final-interpretation claim.

## Test/check plan

- Run `git diff --check`.
- Run `python scripts/check_narrative_claim_safety.py` over the B015 packet, this spec, and changed source-truth docs.
- Run the closest applicable packet consistency check if available.

## Definition of done

- B015 packet and spec exist.
- Required source map, field inventory, status taxonomy, static prototype plan, wireframe, data-readiness, claim-boundary, implementation gate, non-actions, non-claims, and checks files exist.
- Source-truth docs are narrowly updated.
- B012/B013 remain deferred.
- No runtime, provider, UI, scoring, unblinding, final interpretation, or broad claims are authorized.
