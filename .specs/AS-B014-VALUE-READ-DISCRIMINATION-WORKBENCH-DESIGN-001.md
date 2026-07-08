# AS-B014-VALUE-READ-DISCRIMINATION-WORKBENCH-DESIGN-001 - Value Read / Discrimination Workbench Design

## Status

`SPEC_OK` - docs/source-truth workbench design prepared for operator review.

## Goal

Define `VALUE_READ_DISCRIMINATION_WORKBENCH` as a source-truth-grounded operator workbench for understanding whether Alpha Solver is producing differentiated, evidence-bounded, route-aware work compared with plain or baseline outputs.

## Motivation

`AS-POST-677-PRODUCT-DIRECTION-SELECTION-001` selected `VALUE_READ_DISCRIMINATION_WORKBENCH` because it best preserves Alpha Solver as a reasoning, routing, comparison, evidence, and operator-control system rather than a generic prompt-runner cockpit. This lane turns that selection into a first design packet without implementing UI or runtime behavior.

## Source context

This lane follows the post-677 selected state `OPERATOR_REVIEW_REQUIRED_AFTER_POST_677_PRODUCT_DIRECTION_SELECTION_001` and uses the merged post-677 packet as its source-truth baseline. Historical Value Read, routed-vs-plain, discrimination task-bank, derivation/no-echo, capture/preflight, and Operator Console route-preview artifacts are design inputs only.

## Scope

- Create a design packet under `docs/evals/runs/as-b014-value-read-discrimination-workbench-design-001/`.
- Define the workbench, operator job-to-be-done, artifact inputs, workflow map, information architecture, route/expert preview role, evidence boundaries, first-screen operator test, and next-lane recommendation.
- Update source-truth indexes narrowly to record B014 completion and the review-required next state.

## Non-goals

This lane is a docs/source-truth workbench design. It does not implement UI, execute providers, authorize B012, authorize B013, expose `/v1/solve`, run models, score outputs, unblind results, perform final interpretation, or make value/readiness/superiority claims.

## Allowed files

- `.specs/AS-B014-VALUE-READ-DISCRIMINATION-WORKBENCH-DESIGN-001.md`
- `.specs/INDEX.md`
- `docs/evals/runs/as-b014-value-read-discrimination-workbench-design-001/*.md`
- Narrow source-truth updates to `docs/CURRENT_STATE.md`, `docs/ROADMAP.md`, `docs/EVIDENCE_INDEX.md`, and `docs/LANE_REGISTRY.md`.

## Source-truth preservation rule

Detailed completed, superseded, blocked, historical, do-not-run-again, DAG, and registry sections must be preserved. This lane may add narrow current-state entries, but must not collapse concrete registry history into summary bullets or remove forward-path context.

## Workbench definition

`VALUE_READ_DISCRIMINATION_WORKBENCH` is a source-truth-grounded operator workbench for understanding whether Alpha Solver is producing differentiated, evidence-bounded, route-aware work compared with plain or baseline outputs. It is not a generic prompt runner, status dashboard, live execution cockpit, provider console, scoring surface, unblinding tool, or final-interpretation engine.

## Required sections

1. Current packet.
2. Artifact completeness.
3. Comparison state.
4. Route and expert context.
5. Claim and safety boundary.
6. Operator next action.

## Artifact input map requirement

The design packet must map Value Read case packets, raw Alpha/routed outputs, raw plain/baseline outputs, blind scorer packets, scoring outputs, score-lock state, unblinding/source identity map state, final interpretation packets, route metadata records, capture/preflight reports, local receipt records, Operator Console artifact status, and narrative claim-safety outputs.

## Workflow map requirement

The design packet must describe readiness review, Alpha/routed vs plain/baseline comparison, route/expert context inspection, next safe action selection, and stop/defer workflows.

## Route/expert preview role

Route/expert preview is a diagnostic component of the workbench, not the whole product. It may explain task interpretation, route/expert/persona, SAFE-OUT, confidence, shortlist, fallback, and missing metadata status, but it does not prove output quality or authorize live execution.

## First-screen operator test

The first screen must let the operator answer within 30 seconds: what packet is under review, whether it is complete enough to review, what the comparison state is, what the next safe action is, and what claims are blocked.

## Recommended next lane

`AS-B015-VALUE-READ-WORKBENCH-SOURCE-MAP-AND-STATIC-PROTOTYPE-001`

Purpose: build a source map and static prototype plan for the workbench before runtime/UI implementation. B015 should remain docs/design or static prototype planning only unless separately authorized.

## Selected next state

`OPERATOR_REVIEW_REQUIRED_AFTER_B014_VALUE_READ_WORKBENCH_DESIGN_001`

The B014 design is complete for operator review. Implementation is not authorized. B015 source-map/static-prototype planning is recommended. B012/B013 remain deferred. No provider calls, `/v1/solve` exposure, scoring, unblinding, final interpretation, or value/readiness/superiority claim is authorized.

## Non-actions

No provider calls, hosted model calls, local model calls, `/v1/solve`, browser automation, CLI/subprocess execution from the web UI, shell execution from UI, queue/runner/scheduler/worker/background job, web route, POST route, write path, runtime behavior change, UI implementation, B012 implementation, B013 real-run provider work, score change, scoring, unblinding, source identity reveal, final interpretation, Google Sheets mutation, or Roadmap HP module implementation.

## Non-claims

No provider validation, local-model validation, benchmark claim, readiness claim, value claim, production claim, public-readiness claim, security/privacy claim, Alpha-superiority claim, generic LLM playground claim, product proof, operator-usability proof, or final interpretation claim.

## Test/check plan

- `git diff --check`
- `python scripts/check_narrative_claim_safety.py` over the B014 packet, B014 spec, and changed source-truth docs.
- Closest applicable packet consistency/static documentation check if present.

## Definition of done

- B014 packet files exist and define the required workbench design.
- Source-truth docs record B014 as completed design, the B014 review-required next state, and B015 as the recommended next lane.
- B012/B013 remain deferred.
- Detailed registries are preserved.
- Required checks are recorded.
- No code, UI, runtime, provider, scoring, unblinding, final interpretation, external ledger, or broad claim change is introduced.
