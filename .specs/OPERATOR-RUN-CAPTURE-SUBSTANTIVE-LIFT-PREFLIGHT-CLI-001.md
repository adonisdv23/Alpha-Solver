# OPERATOR-RUN-CAPTURE-SUBSTANTIVE-LIFT-PREFLIGHT-CLI-001 · Substantive Lift Preflight CLI

Status: Implemented

## Goal

Turn the post-#654 Substantive Lift capture-preflight guidance in
`docs/OPERATOR_RUN_CAPTURE.md` into an optional, local, read-only CLI path so
the operator can catch structural lift/case-anchoring wording problems in a
filled capture before qualitative review, without converting the capture
harness into an evaluator.

## Motivation

PR #654 documented that `check_substantive_lift(solution, prompt=prompt)` may
be used as a non-scoring structural preflight, but the operator had to wire
that call up by hand for every case in a capture. This lane gives the existing
operator run capture CLI a `lift-preflight` subcommand that performs exactly
that documented, bounded use over an existing capture file. It automates
already-approved guidance; it adds no new evaluation semantics.

## Scope

- `alpha/eval/operator_run_capture.py`: read-only preflight helpers —
  `lift_preflight_capture(capture)` classifies each case into one of
  `LIFT_PREFLIGHT_STATES` (`invalid_case`, `excluded_case`, `missing_prompt`,
  `missing_routed_output`, `safe_out_not_applicable`, `structural_pass`,
  `structural_fail`), calling
  `check_substantive_lift(solution_text, prompt=prompt)` from
  `alpha_solver_portable.py` only for cases that carry both texts. If a
  pasted routed output starts with a full-response `SOLUTION:` label, the
  preflight strips that narrow leading envelope label before checking;
  `render_lift_preflight_text(report)` renders operator-readable console
  output. Every report embeds `LIFT_PREFLIGHT_BOUNDARY`, the structural-only
  boundary statement.
- Bounded `SAFE-OUT:`-prefixed routed outputs are reported as
  `safe_out_not_applicable`: the lift wording contract does not apply to
  honest non-answers, mirroring the POST652 honesty boundary.
- Anchor-free prompts are reported as vacuous for anchor-specific checks
  (`anchor_checks_vacuous`), never as failures.
- `scripts/operator_run_capture.py`: new `lift-preflight` subcommand with
  `--capture`, optional `--report-out` (local JSON report, overwrite-guarded
  behind `--force`), exit code 0 when no case needs attention and 1 when any
  case is a structural fail, has missing text, or is malformed.
- `docs/OPERATOR_RUN_CAPTURE.md`: CLI usage, state meanings, exit codes, and
  boundary language under the existing Substantive Lift capture preflight
  section.
- Tests in `tests/test_operator_run_capture.py` covering pass, fail,
  vacuous-anchor, excluded, missing-text, SAFE-OUT, non-mutation,
  prohibited-field absence, report/overwrite behavior, and that the existing
  init/validate/export flow is untouched.

## Non-goals and boundaries

- No provider, hosted-model, or local-model calls; no network access.
- No `/v1/solve` wiring, dashboard/API changes, or route/persona activation.
- No scoring, ranking, winner fields, blind labels, source maps, identity
  maps, or A/B identity keys; the report structure carries none of these.
- No change to the capture schema, the export packet schema, or the existing
  `init` / `validate` / `export` semantics; the preflight report is a separate
  local file with its own `operator_lift_preflight_report/v1` schema version
  and is not an input to `export`.
- The preflight never mutates the capture file.
- No change to SAFE-OUT semantics, SolverEnvelope shape, or low-headroom
  precedence; the portable checker itself is consumed, not modified.
- No benchmark, readiness, production, provider-validation,
  local-model-validation, model-superiority, or Alpha-superiority claims.
- No claim that PR #646, #652, #654, or this lane improves answer quality.
  A `structural_pass` means only that the configured local structural wording
  checks held for the supplied routed output text and prompt; it is not an
  answer-quality judgment, and comparative interpretation of baseline versus
  routed outputs stays out of scope.

## Code Targets

- `alpha/eval/operator_run_capture.py`
- `scripts/operator_run_capture.py`
- `docs/OPERATOR_RUN_CAPTURE.md`
- `tests/test_operator_run_capture.py`

## Test Plan

`tests/test_operator_run_capture.py` (`TestLiftPreflight`,
`TestLiftPreflightCli`): anchored compliant routed output reaches
`structural_pass`; a generic six-move block under an anchored prompt reaches
`structural_fail` with `unanchored_lift` named; an anchor-free prompt yields a
vacuous pass, not a false failure; excluded cases are skipped and never
checked; missing prompt and missing routed output map to their own states;
bounded `SAFE-OUT:` routed output maps to `safe_out_not_applicable`; the
preflight never mutates the capture (in-memory and on-disk byte checks); the
report and console output carry the structural-only boundary language and no
score/rank/winner/blind/source-map/identity-map keys; `--report-out` refuses
to overwrite without `--force`; invalid top-level shapes raise; non-dict cases
are flagged, not crashed; the existing init/validate/export flow still passes
unchanged.

## Validation

- `python -m pytest tests/test_operator_run_capture.py -q`
- `python -m pytest tests/test_pr646_substantive_lift_eval_prep.py -q`
- `python -m pytest tests/test_alpha_substantive_lift_contract.py -q`
- `python -m pytest tests/test_alpha_local_runtime_honesty.py -q`
- `python -m pytest -q`
- `python scripts/check_narrative_claim_safety.py docs/OPERATOR_RUN_CAPTURE.md`
- `python scripts/check_narrative_claim_safety.py .specs/OPERATOR-RUN-CAPTURE-SUBSTANTIVE-LIFT-PREFLIGHT-CLI-001.md`
- `ruff check alpha/eval/operator_run_capture.py scripts/operator_run_capture.py tests/test_operator_run_capture.py`

## Definition of Done

Preflight helpers, CLI subcommand, docs, tests, and this spec merged; all
validation commands pass; existing init/validate/export behavior and both
capture/export schemas unchanged; all boundaries above hold. A passing
preflight run means only that the configured structural rules held for the
checked capture text; it is not a quality, benchmark, readiness, or
superiority judgment.
