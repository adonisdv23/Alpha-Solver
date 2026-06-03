# EVAL-DIFFERENTIATION-RUN-001 · Artifact Population Guide (A3-0)

This companion to `operator-checklist.md` describes how the A3-1 step should
populate the run artifacts once it is separately approved. It is documentation
only. A3-0 does not populate any artifact described here.

- Lane: `OUTPUT-DIFF-A3-OPERATOR-CHECKLIST-DRY-RUN-001`
- Step: A3-0 (readiness only)
- Run directory: `docs/evals/runs/20260602-eval-differentiation-run-001-alpha-vs-plain/`
- Operator checklist: `operator-checklist.md`

## Scope of this guide

This guide explains the mechanics of filling each artifact so an operator can
execute A3-1 consistently and safely. It does not authorize execution. Read the
stop conditions, redaction rules, and non-claims in `operator-checklist.md`
first; they govern everything below.

A3-0 adds no outputs, no scores, no provider calls, no populated paired-output
captures, and no populated evidence packets.

## Population order for A3-1

Follow this order so blinding is preserved and the captures stay aligned to the
`Output A` / `Output B` framing that scoring uses:

1. Confirm every Section A pre-run item in `operator-checklist.md` is recorded.
2. Generate the two outputs per prompt under the approved cap.
3. Assign plain and Alpha to `Output A` / `Output B` using a recorded random
   method or seed.
4. Record the mapping in `blinding-map.csv`, kept separate from judge-facing
   scoring.
5. Write one sanitized paired-output capture per prompt using the `Output A` /
   `Output B` labels, not judge-facing plain/Alpha labels.
6. Score `blinded-score-sheet.csv` on all 14 dimensions using `Output A` and
   `Output B` only.
7. Unblind via `blinding-map.csv` only after blinded scoring is complete.
8. Fill `score-table.csv` from the unblinded scores.
9. Compute the decision fields and apply the polish-only guard from
   `docs/evals/LIFT_DECISION_RULE.md`.
10. Record any defects in `defects.md`.
11. Write evidence packets only if operator-approved.
12. Update `run-summary.md` with a conservative interpretation.

This order matches `docs/evals/BLIND_SCORING_PROCEDURE.md`: outputs are assigned
to `Output A` / `Output B` and recorded in the blinding map before any capture or
scoring, so the captures and the blinded score sheet share the same neutral
labels and no rewrite is needed after unblinding.

## Paired-output captures

Planned files (one per prompt):

```text
paired-output-captures/cmp-HHE-002-paired-output-capture.md
paired-output-captures/cmp-HHE-003-paired-output-capture.md
paired-output-captures/cmp-HHE-007-paired-output-capture.md
paired-output-captures/cmp-HHE-009-paired-output-capture.md
```

Each capture must reuse
`docs/evals/templates/paired_output_capture_template.md` and should record:

- comparison ID, prompt ID, and run ID;
- sanitized `Output A` answer text or summary, with word count;
- sanitized `Output B` answer text or summary, with word count;
- sanitized Alpha expert-envelope fields, only if available and allowed, in the
  template's unblinded-analysis section;
- allowed summary-level metadata only;
- redactions performed;
- non-claims.

Write captures only after `Output A` / `Output B` are assigned and recorded in
`blinding-map.csv` (steps 3 and 4 above). Use the `Output A` / `Output B` labels
in all judge-facing sections and keep plain/Alpha identity out of them. A capture
may carry the plain/Alpha mapping only if it is not used as a judge-facing scoring
artifact; otherwise it must preserve the `Output A` / `Output B` framing. The
Alpha expert-envelope fields are for unblinded material-lift analysis only and
must not be used to bias blinded scoring. Save sanitized answer text only. Never
paste raw provider payloads, response IDs, headers, account identifiers, cookies,
CSRF or session values, environment dumps, or private user data into a capture.

## Blinding map

`blinding-map.csv` records the de-anonymizing mapping and stays separate from the
judge-facing score sheet. Populate it at steps 3 and 4 above — immediately after
assigning `Output A` / `Output B` and before writing any capture or scoring —
using a recorded random method or seed. The scorer must not consult it until
blinded scoring is complete. Blinding is procedural, not cryptographic.

## Blinded score sheet

`blinded-score-sheet.csv` is the judge-facing sheet. It uses neutral
`Output A` / `Output B` columns and must contain no Alpha or plain labels. Score
all 14 rubric dimensions per `docs/evals/RESPONSE_QUALITY_RUBRIC.md` before
unblinding.

## Score table

After unblinding, transfer scores into `score-table.csv` using the hardened
comparison schema. For future runs, preserve enough machine-readable fields to
make the score arithmetic, capture provenance, and blinding sequence auditable.
Compute the decision fields:

- `plain_total` and `alpha_total`;
- `total_delta`, `lift_delta`, and `polish_delta`;
- `lift_subscore_plain`, `lift_subscore_alpha`, `polish_subscore_plain`, and
  `polish_subscore_alpha`;
- `lift_qualified` and `material_constraint_verified`;
- `polish_only_flag`;
- `winning_surface` and `winning_surface_resolved`;
- `length_ratio`, `length_confound_flag`, and optional `output_a_tokens` /
  `output_b_tokens` values (`not-captured` or blank is acceptable when token
  counts were unavailable).

Recompute `plain_total` and `alpha_total` from the 14 rubric dimension fields
rather than trusting a copied scorer total. If a scorer-provided total and the
recomputed total differ, preserve the recomputed total in the table and record
the scorer-total mismatch in `defects.md` or a run-summary caveat. Lock the
blinded scores before unblinding and record `scores_locked_before_unblinding`,
`blinded_scoring_completed_at`, `unblinding_approved_by`, and
`unblinding_applied_at`. Preserve capture provenance when available, including
`form_capture_level`, `capture_commit_sha`, `capture_started_at`,
`capture_completed_at`, `capture_model_set`, `capture_surface_count`, and safe
summary-level `capture_provider_execution_count`.

Apply the polish-only guard from `docs/evals/LIFT_DECISION_RULE.md`. Do not count
polish-only wins as expert-interrogation lift. Record plain wins and ties
honestly. If the guard prevents an Alpha win from being treated as material lift,
cap `winning_surface_resolved` at `Tie` or `Inconclusive` and explain the reason
in the run summary.

## Defects

Record defects in `defects.md` with defect ID, prompt ID, side, rubric dimension,
category, severity, evidence pointer, follow-up ticket, and whether the defect
affects `lift_qualified`. Use the defect categories listed in
`operator-checklist.md`.

## Evidence packets

Planned files (one per prompt), created only if operator-approved:

```text
evidence-packets/cmp-HHE-002-evidence-packet.md
evidence-packets/cmp-HHE-003-evidence-packet.md
evidence-packets/cmp-HHE-007-evidence-packet.md
evidence-packets/cmp-HHE-009-evidence-packet.md
```

Each evidence packet must reuse
`docs/evals/templates/side_by_side_evidence_packet_template.md` and should
reference the paired-output capture and score-table row rather than duplicating
raw content. Packets must preserve the same redaction and non-claim boundaries.

## Redaction reminder

Never commit API keys, bearer-token credentials, dashboard passwords, cookies,
CSRF tokens, session values, auth headers, raw provider payloads, provider
account identifiers, full unredacted request/response traces, environment dumps,
private user data, or any secret-like string. Only sanitized, summary-level,
re-scorable artifacts may be committed.

## Non-claims

Artifacts produced by following this guide do not claim MVP validation, Alpha
Solver superiority, answer-quality superiority, production readiness, broad
runtime readiness, benchmark success, exact billing accuracy, or provider
reasoning orchestration.
