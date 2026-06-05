# Reviewer Checklist

Lane ID: `ALPHA-LIMITED-OPERATOR-TEST-SECOND-PASS-001`

Status: packet prepared, second-pass test not yet executed

## Packet completeness

- [ ] `README.md` is present.
- [ ] `operator-test-task-set.md` is present.
- [ ] `operator-instructions.md` is present.
- [ ] `operator-feedback-form-template.md` is present.
- [ ] `operator-result-log-template.md` is present.
- [ ] `second-pass-comparison-guide.md` is present.
- [ ] `reviewer-checklist.md` is present.
- [ ] `evidence-boundary.md` is present.
- [ ] `preservation-checklist.md` is present.
- [ ] `recommended-next-lane.md` is present.

## Scope checks

- [ ] Changes are docs-only.
- [ ] Changes are limited to `docs/evals/runs/20260604-alpha-limited-operator-test-second-pass/`.
- [ ] No source code changed.
- [ ] No test code changed.
- [ ] No runtime, routing, provider, model, or API behavior changed.
- [ ] No `/v1/solve` use is claimed.
- [ ] No provider or local-model call is claimed.
- [ ] No Google Sheets update is claimed.
- [ ] No Batch C work is claimed.
- [ ] No prior evidence packet was modified.

## Task-set checks

- [ ] Task set includes roughly 8 to 12 tasks.
- [ ] Task set focuses on concise reviewer comments, replacement wording, checklists, two-sentence status updates, compact prompt/template tasks, missing-results refusal, Batch C blocking under limited evidence, and boundary discipline.
- [ ] Tasks directly retest visible process-style lead-ins.
- [ ] Tasks directly retest wrapper labels.
- [ ] Tasks directly retest `standard:` artifacts.
- [ ] Tasks directly retest unnecessary `Replacement:` labels.
- [ ] Tasks directly retest memo framing when concise output is requested.
- [ ] Every task includes `stop_condition_reached_yes_no`.
- [ ] Every task includes `stop_condition_id_or_summary`.

## Template checks

- [ ] Feedback form is blank.
- [ ] Result log is blank.
- [ ] Feedback form uses the fixed higher-is-better 0-3 scale carried over for first-pass comparability.
- [ ] Feedback form does not allow the operator to define a new scale during execution.
- [ ] Feedback form includes explicit scoring guidance for `no_overframe`, `no_invention`, `stop_condition_handling`, `claim_boundary`, and `evidence_boundary`.
- [ ] Feedback form preserves direct usefulness, brevity, answer-first, no over-frame, claim boundary, evidence boundary, no invention, stop-condition handling, usable next action, and usable with minor edits.
- [ ] Result log includes raw artifact preservation fields.
- [ ] Result log includes explicit stop-condition fields for every task.

## Boundary checks

- [ ] Packet says `packet prepared, second-pass test not yet executed`.
- [ ] Packet does not report results.
- [ ] Packet does not import results.
- [ ] Packet does not include scoring outcomes.
- [ ] Packet does not make readiness claims.
- [ ] Packet does not make validation claims.
- [ ] Packet does not make superiority claims.
- [ ] Packet does not make benchmark claims.
- [ ] Packet does not make production claims.
