# EVAL-DIFFERENTIATION-RUN-001 - Run Plan

## Run identity

- Run ID: `20260602-eval-differentiation-run-001-alpha-vs-plain`
- Parent lane: `EVAL-DIFFERENTIATION-RUN-001`
- Phase: `OUTPUT-DIFFERENTIATION-PHASE-001`
- Status: scaffold only; not executed
- Prompt set source: `docs/evals/prompt_sets/higher_headroom_prompt_set_v1.md`
- Rubric reference: `docs/evals/RESPONSE_QUALITY_RUBRIC.md`
- Lift decision reference: `docs/evals/LIFT_DECISION_RULE.md`
- Blind scoring reference: `docs/evals/BLIND_SCORING_PROCEDURE.md`
- Artifact preservation reference: `docs/evals/ARTIFACT_PRESERVATION.md`
- Operator checklist reference: `operator-checklist.md`
- Artifact population guide reference: `artifact-population-guide.md`
- A3-1 capture packet reference: `a3-1-capture-packet.md` (capture guidance only; does not execute the run)

## Explicit execution boundary

This PR does not execute the run. It does not capture outputs, score outputs,
call live providers, unblind results, populate paired-output captures, populate
evidence packets, or record an Alpha-vs-plain result.

Before the first scored run, follow `operator-checklist.md`
(`OUTPUT-DIFF-A3-OPERATOR-CHECKLIST-DRY-RUN-001`, the A3-0 readiness step) for
pre-run setup, output-generation, blinding, scoring, defect, redaction, stop, and
non-claim rules. That checklist also is documentation only and does not execute
the run.

## Selected prompt subset

The first pilot uses these four higher-headroom prompts:

| Prompt ID | Rationale |
| --- | --- |
| `HHE-002` | Readiness claim review; tests claim-boundary discipline. |
| `HHE-003` | Repo-truth vs ledger assumptions; tests source hierarchy and implementation-evidence discipline. |
| `HHE-007` | Go/no-go memo from incomplete evidence; tests conservative rollout judgment. |
| `HHE-009` | Noisy operator notes cleanup; tests adversarial/noisy instruction handling and scope control. |

## Stage A - scaffold validation only

Stage A is the only stage performed by this PR.

1. Create the run directory and placeholder artifact paths.
2. Copy the hardened CSV headers into the run-local CSV files.
3. Document the prompt subset and expected evidence boundaries.
4. Add validation tests for the scaffold, non-claims, empty placeholders, secret
   hygiene, and physical formatting.
5. Leave paired-output captures and evidence packets empty except for `.gitkeep`.

Stage A records no outputs, no scores, no unblinding decisions, and no live
provider artifacts.

## Stage B - later operator-supervised output capture

Stage B may happen only after explicit operator approval in a later lane or run
instruction.

1. Confirm operator authorization, branch/commit, request cap, redaction rules,
   and stop conditions before any output capture.
2. Run each selected prompt against the plain surface and Alpha surface under the
   approved controlled conditions.
3. Preserve only sanitized answer text and summary-level metadata allowed by
   `docs/evals/ARTIFACT_PRESERVATION.md`.
4. Use `docs/evals/templates/paired_output_capture_template.md` for each paired
   capture.
5. Do not preserve raw provider payloads, full unredacted request/response
   traces, secrets, cookies, session values, auth headers, private user data,
   provider account identifiers, or environment dumps.
6. Stop if the operator cap, redaction boundary, provider boundary, or scope
   boundary is exceeded.

## Output capture procedure

Future output capture should create one sanitized paired-output capture per
comparison in `paired-output-captures/`. Each capture should include prompt ID,
run ID, sanitized Output A/B text or summaries, Alpha envelope fields only where
permitted for unblinded analysis, redactions performed, and non-claims. Captures
must use references to the existing template instead of introducing a new schema.

No populated paired-output captures are added by this PR.

## Blinding procedure

Future scoring should follow `docs/evals/BLIND_SCORING_PROCEDURE.md`.

1. Assign each pair to `Output A` and `Output B` before judge-facing scoring.
2. Keep Alpha/Plain identity only in `blinding-map.csv`.
3. Keep `blinding-map.csv` separate from `blinded-score-sheet.csv`.
4. Score the blinded sheet before consulting the map.
5. Acknowledge that blinding is procedural, not cryptographic, and that Alpha
   envelope structure may remain a tell in later unblinded analysis.

The current blinded score sheet is header-only and contains no Alpha/Plain labels
in judge-facing fields.

## Scoring procedure

Future scoring should use `docs/evals/RESPONSE_QUALITY_RUBRIC.md` and record all
14 dimensions in `blinded-score-sheet.csv` before unblinding. After unblinding,
`score-table.csv` should be populated using the hardened comparison-score schema
with plain and Alpha scores, totals, deltas, length fields, defects, evidence
strength, redactions, and non-claims confirmation.

This PR records no scores and no scored results.

## Lift and polish decision procedure

Future analysis should use `docs/evals/LIFT_DECISION_RULE.md` after scoring and
unblinding. The comparison score table should calculate or record:

- `total_delta`
- `lift_delta`
- `polish_delta`
- `winning_surface`
- `lift_qualified`
- `material_constraint_verified`
- `polish_only_flag`
- length fields and length ratio
- defects and follow-up fields

The decision rule is an internal review aid only. It does not by itself prove
Alpha Solver superiority or answer-quality superiority.

## Defect capture procedure

Future defects should be recorded in `defects.md` and linked from score-table
fields. Each defect should include defect ID, prompt ID, side, rubric dimension,
category, severity, evidence pointer, follow-up ticket, and whether it affects
`lift_qualified`.

Defect categories include missed requested deliverable, unsupported claim,
treating backlog as repo proof, unsafe secret/cookie/session handling, raw
payload preservation suggestion, over-interrogation, excessive caveats, invented
constraints, and plain output more direct/useful.

## Redaction and storage boundaries

Allowed committed artifacts are sanitized, summary-level, re-scorable eval
artifacts for this controlled prompt set. Do not commit secret-like strings,
private user data, provider account identifiers, cookies, session values, auth
headers, raw provider payloads, full unredacted request/response traces, or
environment dumps.

Evidence packets, when later approved, must use
`docs/evals/templates/side_by_side_evidence_packet_template.md` and reference the
source artifacts rather than replacing them.

## Strict non-claims

This scaffold makes no claim of:

- MVP validation.
- Alpha Solver superiority.
- Answer-quality superiority.
- Production readiness.
- Broad runtime readiness.
- Benchmark success.
- Exact billing accuracy.
- Provider reasoning orchestration.

## Stage C - later blinded scoring, unblinding, defects, and summary

Stage C may happen only after explicit operator approval after Stage B artifacts
exist.

1. Complete blinded scoring before consulting the blinding map.
2. Unblind and populate the comparison score table.
3. Apply the lift/polish decision rule conservatively.
4. Record defects and follow-up tickets.
5. Populate side-by-side evidence packets only if operator-approved.
6. Update `run-summary.md` with a conservative interpretation that separates
   observations from conclusions.
7. Preserve strict non-claims and avoid broad validation or superiority language.

Stage C is not performed by this PR.
