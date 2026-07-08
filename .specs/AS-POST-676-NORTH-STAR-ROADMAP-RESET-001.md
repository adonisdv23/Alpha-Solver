# AS-POST-676-NORTH-STAR-ROADMAP-RESET-001 · Post-#676 North-Star Roadmap Reset

## Status

`SPEC_OK` — source-truth reset packet completed for operator review.

## Goal

Create a repo-grounded source-truth reset packet after the PR #663 through PR #676 Operator Console sequence. The lane records that recent Operator Console work improved local-first visibility and operator-facing status, while human operator feedback exposed a product-direction question that must be resolved before more UI or real-run cockpit work.

## Motivation

Human validation after PR #676 still raised basic product-use questions: how the page should be used, whether it is only an FAQ/status page, whether the work is moving in the right direction, and whether it remains aligned with Alpha Solver's original purpose. This reset preserves the evidence boundary before the repository drifts from reasoning/routing plus discrimination evidence into generic cockpit or playground behavior.

## Source context

- Known main baseline after PR #676: `bef685c43676019c0de97157935b4f3b60f177d0`.
- PR #663 through PR #676 added case-packet preflight, local-first Operator Console shell work, artifact status, freshness checks, provider/model/cost gate panel, dry-run preview, local receipt store, copy/paste capture guidance, no-provider-call/write-boundary hardening, manual next-step guidance, first-use and daily-use docs, progressive disclosure, and flow-first orientation.
- Existing source-truth docs identify Alpha Solver as a reasoning/routing layer with gates, scoring, observability, replay, determinism, and budget guard rather than a generic LLM playground.

## Scope

- Add the reset packet under `docs/evals/runs/as-post-676-north-star-roadmap-reset-001/`.
- Add this spec.
- Update source-truth indexes only enough to point to the reset and selected next state.
- Preserve claim boundaries and implementation deferrals.

## Non-goals

This lane is a source-truth reset. It does not implement UI, execute providers, authorize B012, authorize B013, expose /v1/solve, run models, score outputs, unblind results, or make value/readiness/superiority claims.

## Allowed files

- `.specs/AS-POST-676-NORTH-STAR-ROADMAP-RESET-001.md`
- `.specs/INDEX.md`
- `docs/CURRENT_STATE.md`
- `docs/ROADMAP.md`
- `docs/EVIDENCE_INDEX.md`
- `docs/LANE_REGISTRY.md`
- `docs/evals/runs/as-post-676-north-star-roadmap-reset-001/*.md`

## Required source-truth updates

- Record the reset lane and packet location.
- Record selected next state: `OPERATOR_REVIEW_REQUIRED_AFTER_POST_676_NORTH_STAR_ROADMAP_RESET_001`.
- Reclassify B012/B013-style cockpit work as deferred pending operator direction.
- State that no implementation lane, provider execution lane, `/v1/solve` exposure, scoring, unblinding, final interpretation, or broad claim is selected by this reset.

## Product direction options

| Option | Product direction | Classification |
|--------|-------------------|----------------|
| A | Bounded smoke-test cockpit | Useful support surface, not core product proof. |
| B | Value Read / discrimination workbench | Strongest north-star alignment. |
| C | Route and expert-preview control surface | Strong alignment with reasoning/routing layer. |
| D | CLI/artifact operator companion | Safe and aligned support surface. |
| E | Full real-run Operator Cockpit | Potentially useful later, but too broad without prior decisions. |
| F | Read-only status checkpoint | Already built enough for current evidence needs and not next. |

## Selected next state

`OPERATOR_REVIEW_REQUIRED_AFTER_POST_676_NORTH_STAR_ROADMAP_RESET_001`

This is a review/decision state, not an implementation lane. It authorizes no B012 implementation, no B013 real-run provider work, no provider calls, no `/v1/solve` exposure, no scoring, no unblinding, no final interpretation, no value/readiness/superiority claim, and no next product direction without an operator decision.

## Non-actions

The lane does not add routes, POST routes, UI behavior, shell execution from the web UI, provider calls, hosted model calls, local model calls, browser automation, queue/runner/scheduler/worker/background jobs, new write paths, score changes, source identity reveal, Google Sheets mutation, or a generic LLM playground.

## Non-claims

The lane does not claim value, readiness, benchmark success, provider validation, local-model validation, production suitability, public suitability, security/privacy completion, or Alpha superiority.

## Test/check plan

- Verify live main SHA and PR #676 merge state.
- Verify no open PRs exist that conflict with source-truth docs.
- Search for an existing post-#676 north-star reset packet before creating this one.
- Inspect required source-truth docs and recent Operator Console specs.
- Run `git diff --check`.
- Run the narrative claim-safety checker over the reset packet, this spec, and updated source-truth docs.

## Definition of done

- Reset packet exists with README, source-truth delta, Operator Console sequence review, north-star diagnosis, product-direction options, recommended next state, non-actions, non-claims, and checks-run files.
- Source-truth docs point to the review-required selected next state.
- `.specs/INDEX.md` includes this spec.
- Required checks are recorded in the packet.
