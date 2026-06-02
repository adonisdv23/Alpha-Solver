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

Follow this order so blinding is preserved:

1. Confirm every Section A pre-run item in `operator-checklist.md` is recorded.
2. Generate the two outputs per prompt under the approved cap.
3. Write one sanitized paired-output capture per prompt.
4. Assign Output A / Output B and record `blinding-map.csv`.
5. Score the blinded sheet (`blinded-score-sheet.csv`) on all 14 dimensions.
6. Unblind via the map, then fill `score-table.csv`.
7. Compute the decision fields and apply the polish-only guard.
8. Record any defects in `defects.md`.
9. Write evidence packets only if operator-approved.
10. Update `run-summary.md` with a conservative interpretation.

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

- prompt ID and run ID;
- sanitized plain answer text or summary;
- sanitized Alpha answer text or summary;
- word counts for each side;
- sanitized Alpha expert-envelope fields only if available and allowed;
- allowed summary-level metadata only;
- redactions performed;
- non-claims.

Do not place Alpha/plain identity in any judge-facing field. Save sanitized
answer text only. Never paste raw provider payloads, response IDs, headers,
account identifiers, cookies, CSRF or session values, environment dumps, or
private user data into a capture.

## Blinding map

`blinding-map.csv` records the de-anonymizing mapping and stays separate from the
judge-facing score sheet. Populate it only at step 4 above, using a recorded
random method or seed. The scorer must not consult it until blinded scoring is
complete. Blinding is procedural, not cryptographic.

## Blinded score sheet

`blinded-score-sheet.csv` is the judge-facing sheet. It uses neutral
`Output A` / `Output B` columns and must contain no Alpha or plain labels. Score
all 14 rubric dimensions per `docs/evals/RESPONSE_QUALITY_RUBRIC.md` before
unblinding.

## Score table

After unblinding, transfer scores into `score-table.csv` using the hardened
comparison schema. Compute the decision fields:

- `plain_total` and `alpha_total`;
- `total_delta`, `lift_delta`, and `polish_delta`;
- `lift_qualified` and `material_constraint_verified`;
- `polish_only_flag`.

Apply the polish-only guard from `docs/evals/LIFT_DECISION_RULE.md`. Do not count
polish-only wins as expert-interrogation lift. Record plain wins and ties
honestly.

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
