# EVAL-DIFFERENTIATION-RUN-001 · Controlled Alpha-vs-Plain Run Scaffold

## Status

Documentation/spec/run-scaffold/tests lane for `OUTPUT-DIFFERENTIATION-PHASE-001`.

This lane prepares the first controlled Alpha-vs-plain differentiation run
scaffold. It does not execute the run, capture outputs, score outputs, call live
providers, or add populated evidence packets.

## Purpose

Create a narrow, auditable run directory for the first pilot comparison using the
hardened measurement artifacts from `OUTPUT-DIFF-MEASUREMENT-HARDENING-001` and
the side-by-side evidence packet contract from
`ALPHA-SIDE-BY-SIDE-EVIDENCE-PACKET-001`.

The scaffold defines where future operator-approved artifacts will live, which
prompt subset will be used, and which validation checks protect the boundary
between prepared infrastructure and a scored differentiation result.

## Scope

In scope:

- Add a run directory under `docs/evals/runs/` for the first pilot scaffold.
- Add a run plan with staged execution gates and strict non-claims.
- Add a prompt manifest for `HHE-002`, `HHE-003`, `HHE-007`, and `HHE-009`.
- Add header-only hardened CSV artifacts for blinded scoring, the separate
  blinding map, and comparison scores.
- Add blank placeholder directories for paired-output captures and evidence
  packets.
- Add docs-integrity tests that confirm the scaffold is unexecuted and contains
  no scored outputs or live-provider artifacts.

Out of scope:

- Executing the first scored differentiation run.
- Live provider calls.
- Scoring actual Alpha-vs-plain outputs.
- Populated evidence packets or paired-output captures.
- Provider expert-pass behavior changes.
- Clarify behavior changes.
- `/v1/solve` behavior changes.
- Preview UI rendering changes.
- Dashboard auth changes.
- Changes to `scripts/run_answer_quality_eval.py`.
- MCQ answer-quality eval behavior changes.
- Provider reasoning orchestration.
- Tool routing, effort toggle, or persistent quota implementation.
- Google Sheets or backlog workbook updates.

## Run scaffold

Run directory:

`docs/evals/runs/20260602-eval-differentiation-run-001-alpha-vs-plain/`

Required scaffold files:

- `run-plan.md`
- `prompt-manifest.md`
- `run-summary.md`
- `blinded-score-sheet.csv`
- `blinding-map.csv`
- `score-table.csv`
- `defects.md`
- `paired-output-captures/.gitkeep`
- `evidence-packets/.gitkeep`

## Selected first-pilot prompts

The pilot uses four prompts from the existing higher-headroom prompt set:

- `HHE-002` — readiness claim review.
- `HHE-003` — repo-truth vs ledger assumptions.
- `HHE-007` — go/no-go memo from incomplete evidence.
- `HHE-009` — noisy operator notes cleanup.

These prompts stress claim-boundary discipline, source hierarchy, conservative
rollout judgment, unsafe/noisy instruction filtering, and scope control without
requiring runtime changes in this lane.

## Required source artifacts

The scaffold must use and reference the existing hardened artifacts rather than
inventing a new schema:

- `docs/evals/templates/comparison_score_table_template.csv`
- `docs/evals/templates/blinded_score_sheet_template.csv`
- `docs/evals/templates/blinding_map_template.csv`
- `docs/evals/templates/paired_output_capture_template.md`
- `docs/evals/templates/run_report_template.md`
- `docs/evals/templates/side_by_side_evidence_packet_template.md`
- `docs/evals/RESPONSE_QUALITY_RUBRIC.md`
- `docs/evals/LIFT_DECISION_RULE.md`
- `docs/evals/BLIND_SCORING_PROCEDURE.md`
- `docs/evals/ARTIFACT_PRESERVATION.md`

## Stage gates

### Stage A — scaffold validation only

This PR performs Stage A only. Stage A validates the files, headers, prompt
manifest, non-claims, and empty artifact placeholders. It records no outputs and
no scores.

### Stage B — future operator-supervised output capture

Stage B may begin only after explicit operator approval in a later PR or run
instruction. It will capture sanitized paired outputs using the paired-output
capture template and preservation rules.

### Stage C — future blinded scoring and conservative reporting

Stage C may begin only after explicit operator approval after Stage B. It will
perform blinded scoring, maintain the separate blinding map, calculate comparison
score-table fields, apply the lift/polish decision rule, capture defects, and
write a conservative summary.

## Validation requirements

The docs-integrity tests for this lane must confirm:

- The spec and run scaffold exist.
- The spec index references this spec.
- The prompt manifest contains exactly the four selected prompts.
- CSV headers include hardened scoring, blinding, lift, polish, length, defect,
  and follow-up fields.
- Blinded judge-facing headers use Output A / Output B without Alpha or Plain
  labels.
- The blinding map remains separate from the blinded score sheet.
- Run plan and summary clearly state the run is not executed yet.
- The scaffold contains no populated outputs, no scored results, and no
  live-provider artifacts.
- Committed run artifacts contain no secret-like strings.
- Markdown and Python files have reviewable physical formatting.

## Strict non-claims

This lane does not claim:

- MVP validation.
- Alpha Solver superiority.
- Answer-quality superiority.
- Production readiness.
- Broad runtime readiness.
- Benchmark success.
- Exact billing accuracy.
- Provider reasoning orchestration.

## Backlog impact

`EVAL-DIFFERENTIATION-RUN-001` should be marked Done only after this PR merges as
a run-scaffold lane. It prepares the first controlled Alpha-vs-plain
differentiation run scaffold using the hardened measurement artifacts from PR
#232 and the evidence packet template from PR #233. It does not execute or score
the first differentiation run.
