# Checks run

## Live verification performed

- Verified PR #591 via GitHub API: merged at `2026-06-16T07:58:16Z`.
- Verified PR #592 via GitHub API: merged at `2026-06-16T08:23:15Z`.
- Verified PR #593 via GitHub API: merged at `2026-06-16T08:55:54Z`.
- Verified no open PRs were editing `docs/CURRENT_STATE.md`, `docs/LANE_REGISTRY.md`, `docs/EVIDENCE_INDEX.md`, or this packet path.
- Verified `docs/CURRENT_STATE.md` selected next state before this lane was `OPERATOR_REVIEW_REQUIRED_AFTER_SUBSTANTIVE_DERIVATION_CHECK_001`.
- Verified `docs/EVIDENCE_INDEX.md` records PR #591 and PR #592 as merged.
- Verified `docs/EVIDENCE_INDEX.md` references the derivation criteria and test-plan files.
- Verified the derivation-check packet exists.
- Verified the derivation-check packet uses `unsupported_copying`.

## Files checked

- `docs/CURRENT_STATE.md`
- `docs/LANE_REGISTRY.md`
- `docs/EVIDENCE_INDEX.md`
- `docs/evals/runs/alpha-solver-gate-substantive-derivation-check-001/README.md`
- `docs/evals/runs/alpha-solver-gate-substantive-derivation-check-001/derivation-vs-echo-criteria.md`
- `docs/evals/runs/alpha-solver-gate-substantive-derivation-check-001/fixture-plan.md`
- `docs/evals/runs/alpha-solver-gate-substantive-derivation-check-001/heuristic-spec.md`
- `docs/evals/runs/alpha-solver-gate-substantive-derivation-check-001/test-plan.md`
- `docs/evals/runs/alpha-solver-discrimination-task-bank-asset-001/README.md`
- `docs/evals/runs/alpha-solver-discrimination-task-bank-asset-001/repeatability-plan.md`
- Existing discrimination task-bank docs found under `docs/evals/runs/alpha-solver-discrimination-task-bank-asset-001/`
- Safe static checker references in `scripts/check_narrative_claim_safety.py`, `scripts/check_local_llm_evidence_boundaries.py`, and `scripts/check_local_llm_packet_consistency.py`

## Checks run

| Check | Result | Notes |
|-------|--------|-------|
| `python scripts/check_narrative_claim_safety.py $(git diff --cached --name-only -- '*.md')` | pass | Scanned 15 changed Markdown files. This is not a completeness claim. |
| `git diff --cached --check` | pass | No whitespace errors in staged changes. |
| `python - <<'PY' ... PY` packet consistency check | pass | Confirmed all 12 required packet files exist. |
| `python - <<'PY' ... PY` source-of-truth consistency check | pass | Confirmed updated source-of-truth docs and packet selected-next file include `OPERATOR_REVIEW_REQUIRED_AFTER_DISCRIMINATION_TASK_BANK_FIRST_CHEAP_TEST_001`. |
| `python - <<'PY' ... PY` label consistency check | pass | Confirmed required copying-failure sections use `unsupported_copying` and no fixture label-set entry uses `unacceptable_output_copying`. |
| `python - <<'PY' ... PY` em dash check | pass | Confirmed changed Markdown files do not contain em dashes. |

## Checks not run and why

- Full test suite was not run because this is a docs-only packet and required checks are focused static checks.
- Provider, local-model, runtime endpoint, dashboard, public API, `/v1/solve`, external-service, and Google Sheets checks were not run because they are outside scope and explicitly blocked.
- Output-generation and scoring checks were not run because this lane does not generate or score outputs.

## Evidence boundary

Checks are limited to committed docs, static file presence, source-of-truth consistency, label consistency, and narrative claim-safety lint. No raw Alpha outputs or raw baseline outputs were inspected.

## Non-actions

No provider calls, local-model calls, runtime endpoint calls, dashboard/public API calls, `/v1/solve` exposure, Google Sheets mutation, output generation, scoring, unblinding, source-map work, raw output inspection, dependency addition, release implementation, task execution, or broad claims occurred.
