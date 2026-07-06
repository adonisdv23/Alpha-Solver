# PR646-SUBSTANTIVE-LIFT-MANUAL-EVAL-PREP-001 · Substantive Lift Manual Eval Prep

Status: Implemented

## Goal

Create a local-only manual evaluation prep packet and runbook for checking
whether PR #646's Substantive Lift Answer Contract creates a noticeable
operator-visible answer-quality difference between plain and Alpha answers.

## Source Truth

- PR #646 introduced `ALPHA-SOLVER-SUBSTANTIVE-LIFT-ANSWER-CONTRACT-001` on the
  portable surface.
- PR #647 bounded non-substantive local template outputs.
- PR #648 capped unsupported SAFE-OUT confidence.
- `ALPHA-SOLVER-OPERATOR-RUN-CAPTURE-HARNESS-MVP-001` remains the existing local
  capture/export harness.

## Scope

- Add one PR #646-specific case packet under
  `tests/fixtures/operator_run_capture/`.
- Add a runbook under `docs/evals/runbooks/` that uses only the existing
  operator run capture CLI flow.
- Add tests that validate packet shape, non-scoring boundaries, runbook
  boundary statements, and spec indexing.
- Update `.specs/INDEX.md` for this spec.

## Case Packet Shape

The packet contains six concrete, repo-grounded high-headroom prompts covering:

1. The next answer-quality bottleneck after PR #646, PR #647, and PR #648.
2. Runtime lift wiring versus manual portable testing.
3. Route/persona causality versus bloat.
4. Local ToT honesty and unsupported synthesis boundaries.
5. Manual evaluation design without scoring claims.
6. One constrained implementation-lane selection.

Each prompt asks for intent diagnosis, hidden assumption, dominant tradeoff,
committed recommendation, failure condition, and same-day next action.

## Non-goals and Boundaries

- No provider calls, hosted model calls, local model calls, or network calls.
- No scoring, ranking, winner fields, blinding, unblinding, `blind_label`,
  `source_map`, `identity_map`, or A/B identity keys.
- No `/v1/solve`, dashboard, API, route/persona activation, provider routing,
  local-model routing, or runtime behavior changes.
- No benchmark, readiness, production, provider-validation,
  local-model-validation, or Alpha-superiority claims.
- No manual evaluation is started by this lane; it prepares local capture
  materials only.

## Acceptance Criteria

- The PR #646 case packet validates under the existing operator capture harness.
- The packet has at least five high-headroom cases with unique stable task IDs.
- Prompts are non-empty and grounded in Alpha Solver repo files or PR context.
- Packet fields exclude scoring, ranking, blinding, source-map, identity-map,
  readiness, benchmark, and superiority fields.
- The runbook documents the existing `init`, `validate`, and `export` CLI flow
  and the required boundaries.
- This spec is indexed in `.specs/INDEX.md`.

## Validation

- `python -m pytest tests/test_pr646_substantive_lift_eval_prep.py -q`
- `python -m pytest tests/test_operator_run_capture.py -q`
- `python scripts/check_narrative_claim_safety.py .specs/PR646-SUBSTANTIVE-LIFT-MANUAL-EVAL-PREP-001.md`
- `python scripts/check_narrative_claim_safety.py docs/evals/runbooks/PR646_SUBSTANTIVE_LIFT_MANUAL_EVAL.md`
