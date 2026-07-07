# OPERATOR-RUN-CAPTURE-CASE-PACKET-ANCHOR-PREFLIGHT-CLI-001 · Case-Packet Anchor Preflight CLI

Status: Implemented

## Goal

Give the operator run capture harness an authoring-time, local, read-only
anchor preflight over a case packet's prompts, so the operator learns which
prompts are anchor-bearing (the Substantive Lift anchoring checks will apply)
and which are anchor-free (those checks would be vacuous) before spending an
expensive manual ghost-chat run — without turning the harness into an
evaluator.

## Motivation

The `lift-preflight` subcommand
(`OPERATOR-RUN-CAPTURE-SUBSTANTIVE-LIFT-PREFLIGHT-CLI-001`) runs on routed
outputs, so it can only surface `anchor_checks_vacuous` after the operator has
already done the manual capture work. Nothing in the harness reports anchor
coverage at case-packet authoring time. `validate_case_packet` checks
structure only (task IDs, non-empty prompts, unknown keys); it does not look at
anchors. This lane closes that gap by running the existing deterministic
`_extract_case_anchors` extractor over each prompt at authoring time, moving
the anchor-coverage feedback from post-capture (expensive) to pre-run (free).

## Scope

- `alpha/eval/operator_run_capture.py`: read-only anchor preflight helpers.
  `anchor_preflight_case_packet(case_packet, require_anchors=False)` classifies
  each case into one of `ANCHOR_PREFLIGHT_STATES` (`invalid_case`,
  `anchor_free`, `anchor_bearing`) using `_extract_case_anchors` from
  `alpha_solver_portable.py`; `render_anchor_preflight_text(report)` renders
  operator console output. Every report embeds `ANCHOR_PREFLIGHT_BOUNDARY`.
- `anchor_free` is informational, not a defect: some prompts are legitimately
  low-headroom. Only `invalid_case` needs attention by default. `require_anchors`
  is an opt-in stricter authoring gate that additionally lists `anchor_free`
  cases as needing attention.
- `scripts/operator_run_capture.py`: new `anchor-preflight` subcommand with
  `--case-packet`, optional `--report-out` (local JSON report, overwrite-guarded
  behind `--force`), and `--require-anchors`. Exit code 0 when nothing needs
  attention, 1 otherwise. `init` / `validate` / `export` / `lift-preflight`
  are untouched.
- `docs/OPERATOR_RUN_CAPTURE.md`: CLI usage, state meanings, exit codes, and
  boundary language under the existing preflight section.
- Tests in `tests/test_operator_run_capture.py`.

## Non-goals and boundaries

- No provider, hosted-model, or local-model calls; no network access.
- No `/v1/solve` wiring, dashboard/API changes, or route/persona activation.
- No scoring, ranking, winner fields, blind labels, source maps, identity
  maps, or A/B identity keys; the report structure carries none of these.
- No change to the capture schema, the export packet schema, or the existing
  `init` / `validate` / `export` / `lift-preflight` semantics; the anchor
  preflight report is a separate local file with its own
  `operator_anchor_preflight_report/v1` schema version and is not an input to
  `export`.
- The preflight never mutates the case packet.
- No change to SAFE-OUT semantics, SolverEnvelope shape, or low-headroom
  precedence; the portable extractor is consumed, not modified.
- No benchmark, readiness, production, provider-validation,
  local-model-validation, model-superiority, or Alpha-superiority claims.
- No claim that PR #646, #652, #654, #655, or this lane improves answer
  quality. Reporting a prompt as `anchor_bearing` means only that the prompt
  contains the concrete objects the lift anchoring checks look for; it is not
  a quality judgment, and comparative interpretation stays out of scope.

## Code Targets

- `alpha/eval/operator_run_capture.py`
- `scripts/operator_run_capture.py`
- `docs/OPERATOR_RUN_CAPTURE.md`
- `tests/test_operator_run_capture.py`

## Test Plan

`tests/test_operator_run_capture.py` (`TestAnchorPreflight`,
`TestAnchorPreflightCli`): an anchor-bearing prompt reaches `anchor_bearing`
with a non-empty anchor list; an anchor-free prompt reaches `anchor_free` and
is not flagged for attention by default; `--require-anchors` flags anchor-free
cases; malformed and empty-prompt cases are `invalid_case`; the committed
PR646 case packet is fully anchor-bearing; the report and console output carry
the boundary language and no score/rank/winner/blind/source-map/identity-map
keys; the preflight never mutates the packet (in-memory and on-disk byte
checks); invalid top-level shapes raise; `--report-out` refuses to overwrite
without `--force`; and the existing subcommands still work.

## Validation

- `python -m pytest tests/test_operator_run_capture.py -q`
- `python -m pytest tests/test_pr646_substantive_lift_eval_prep.py -q`
- `python -m pytest tests/test_alpha_substantive_lift_contract.py -q`
- `python -m pytest tests/test_alpha_local_runtime_honesty.py -q`
- `python -m pytest -q`
- `python scripts/check_narrative_claim_safety.py docs/OPERATOR_RUN_CAPTURE.md`
- `python scripts/check_narrative_claim_safety.py .specs/OPERATOR-RUN-CAPTURE-CASE-PACKET-ANCHOR-PREFLIGHT-CLI-001.md`
- `ruff check alpha/eval/operator_run_capture.py scripts/operator_run_capture.py tests/test_operator_run_capture.py`

## Definition of Done

Anchor preflight helpers, CLI subcommand, docs, tests, and this spec merged;
all validation commands pass; existing capture/export/lift-preflight behavior
and all schemas unchanged; all boundaries above hold. A passing anchor
preflight run means only that the configured structural anchor-presence rules
held for the checked prompts; it is not a quality, benchmark, readiness, or
superiority judgment.
