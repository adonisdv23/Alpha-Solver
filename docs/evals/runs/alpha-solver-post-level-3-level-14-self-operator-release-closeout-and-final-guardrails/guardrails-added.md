# Guardrails added by this lane

## New test module: `tests/test_self_operator_closeout_guardrails.py`

Focused, deterministic tests that fail on:

- premature readiness wording: blocked claim phrases appearing in this
  closeout packet outside forbidden-claim documentation files;
- external runtime surface references (the charter-enumerated terms)
  appearing in closeout outputs outside boundary/claim-documentation files;
- missing non-execution proof linkage in the evidence chain;
- missing accepted import evidence before interpretation evidence;
- missing accepted interpretation evidence before the release-gate apply
  evidence;
- missing canonical runbook before closeout;
- missing evidence-boundary review before closeout;
- approval-identity enforcement overstatement returning to the canonical
  runbook (the runbook must keep the comparable-fields wording, and the
  implementation's proposed-task identity helpers must keep the behavior the
  runbook describes);
- closeout packet path mismatch with the release gate (`CLOSEOUT_PACKET`
  must point at this packet's directory, and the directory must exist);
- a closeout packet claiming eligibility while the full-root release gate
  does not report `release_closeout_review_complete: pass` and
  `eligible_for_release_closeout_review` (checked both live against the
  repo root and against the recorded
  `post-closeout-release-gate-report.json`);
- required closeout packet files going missing;
- final-status vocabulary drifting outside
  `eligible_for_operator_supervised_review` / `blocked` / `inconclusive`;
- the deferred final status CLI being introduced or becoming required for
  closeout (its file paths must remain absent while closeout eligibility
  holds).

## New test in `tests/test_self_operator_release_gate.py`

- `test_closeout_packet_path_matches_closeout_and_final_guardrails_lane` —
  pins `CLOSEOUT_PACKET` to this packet's path so the #473/#474 mismatch
  cannot recur silently.

## Existing guardrails relied on (unchanged)

- The deterministic release gate's ordered eleven-gate evaluation and
  unresolved-defect-marker scan.
- The packet-consistency checker's selected-next-lane, blocker-fallback, and
  boundary-file requirements.
