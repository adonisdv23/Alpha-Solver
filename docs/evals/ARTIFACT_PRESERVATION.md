# Eval Artifact Preservation

## Purpose

This guide defines the durable artifact lane for future Alpha-vs-plain
evaluation runs. The goal is to preserve sanitized, citable, repo-inspectable
summaries for decision-making without storing raw provider payloads, secrets,
private runtime material, or temporary operator notes.

This guide supports `OUTPUT-DIFFERENTIATION-PHASE-001`, whose goal is to move
from "the preview works" to "we can measure whether Alpha produces visibly
better outputs than plain provider output on higher-headroom prompts."

## Scope boundaries

This is a documentation/spec preservation lane only. It does not:

- Validate the MVP.
- Prove Alpha Solver superiority.
- Prove production readiness.
- Prove broad runtime readiness.
- Prove benchmark success.
- Prove exact billing accuracy.
- Prove provider reasoning orchestration.
- Change runtime behavior.
- Change provider behavior.
- Change dashboard behavior.
- Change Cloud Run configuration.
- Enable OpenAI.
- Deploy anything.
- Update Google Sheets.

## Source hierarchy

When interpreting eval evidence, use this hierarchy:

1. Repo code and tests.
2. Repo specs and docs.
3. External planning/status ledgers, including Google Sheets.
4. AI outputs and chat summaries, which are advisory unless recorded with
   evidence.

Artifact preservation improves the evidence level of future evals, but it does
not override the code, tests, or implementation contracts.

## Where artifacts live

Committed future eval artifacts should live under:

```text
docs/evals/runs/
```

Templates should live under:

```text
docs/evals/templates/
```

Use `docs/evals/templates/run_report_template.md` as the copyable starting point
for future run reports. Keep artifacts sanitized and summary-level before
committing them.

## Naming conventions

Use lowercase, hyphenated names with an ISO-like date and lane ID:

```text
docs/evals/runs/<YYYYMMDD>-<lane-id>-<short-scope>/run-summary.md
docs/evals/runs/<YYYYMMDD>-<lane-id>-<short-scope>/score-table.csv
docs/evals/runs/<YYYYMMDD>-<lane-id>-<short-scope>/defects.md
```

For a single summarized artifact, use:

```text
docs/evals/runs/<YYYYMMDD>-<lane-id>-<short-scope>-summary.md
```

Examples:

```text
docs/evals/runs/20260602-higher-headroom-eval-001-smoke/run-summary.md
docs/evals/runs/20260602-eval-differentiation-run-001-alpha-vs-plain-summary.md
```

Do not include secrets, provider account names, private customer names, or raw
prompt text in artifact paths.

## Required run summary fields

Every future eval run summary must include:

- Run ID.
- Date.
- Operator.
- Branch/commit.
- Provider/mode.
- Prompt set.
- Prompt count.
- Live mode used: yes/no.
- Request cap used.
- Rollback confirmed: yes/no/not applicable.
- Plain output summary.
- Alpha output summary.
- Rubric used.
- Score table.
- Alpha advantages observed.
- Plain advantages observed.
- Defects or regressions.
- Metrics summary.
- Evidence strength.
- Redactions performed.
- Conservative interpretation.
- Follow-up tickets.
- Non-claims.

## Required side-by-side comparison fields

Every side-by-side Alpha-vs-plain artifact must include:

- Comparison ID.
- Parent Run ID.
- Prompt ID or sanitized prompt label.
- Prompt category or capability tested.
- Plain provider/mode and configuration summary.
- Alpha provider/mode and configuration summary.
- Plain output summary.
- Alpha output summary.
- Rubric dimensions.
- Plain per-dimension scores.
- Alpha per-dimension scores.
- Winner, tie, or no-decision field when the rubric permits it.
- Evidence-limited explanation.
- Defects or regressions for each side.
- Redactions performed.
- Evidence strength.
- Non-claims.

Summaries may cite sanitized excerpts only when safe and necessary. They must not
store raw provider payloads or full unredacted request/response traces.

## Measurement hardening: blinding, lift qualification, and length

`OUTPUT-DIFF-MEASUREMENT-HARDENING-001` extends the side-by-side artifact with:

- per-dimension plain and alpha scores for all 14 rubric dimensions, plus
  `total_delta`, `lift_delta`, `polish_delta`, `lift_qualified`,
  `material_constraint_verified`, and `polish_only_flag`
  (`docs/evals/templates/comparison_score_table_template.csv`);
- a structured Alpha expert-envelope capture and sanitized paired-output text
  (`docs/evals/templates/paired_output_capture_template.md`);
- label-stripped Output A / Output B scoring
  (`docs/evals/templates/blinded_score_sheet_template.csv`) with a separate
  mapping file (`docs/evals/templates/blinding_map_template.csv`);
- length metrics (`output_a_len_words`, `output_b_len_words`, `length_ratio`).

`OUTPUT-DIFF-B1-LIFT-REPORTING-HARDENING-001` further hardens future-run
reporting. Future score tables should preserve the lift and polish subscores
(`lift_subscore_plain`, `lift_subscore_alpha`, `polish_subscore_plain`,
`polish_subscore_alpha`) alongside the existing deltas, and should preserve
length context (`length_confound_flag`, optional `output_a_tokens`, optional
`output_b_tokens`) without requiring token counts when they were not captured.
Future runs should also record the resolved decision surface
(`winning_surface_resolved`), capture provenance (`form_capture_level`,
`capture_commit_sha`, `capture_started_at`, `capture_completed_at`,
`capture_model_set`, `capture_surface_count`, and summary-level
`capture_provider_execution_count` when safe), and blinding-integrity fields
(`scores_locked_before_unblinding`, `blinded_scoring_completed_at`,
`unblinding_approved_by`, and `unblinding_applied_at`).

See `docs/evals/LIFT_DECISION_RULE.md` and `docs/evals/BLIND_SCORING_PROCEDURE.md`.
These are internal review aids and do not change the claim boundaries below.

## Redaction rules

Before committing artifacts:

- Remove secrets, credentials, bearer tokens, cookies, CSRF tokens, session
  values, and dashboard passwords.
- Remove provider account identifiers and private tenant/user identifiers.
- Summarize outputs instead of committing raw provider payloads.
- Summarize or sanitize prompt text if it contains private, sensitive, or
  proprietary material.
- Sanitize screenshots before referencing them.
- Record the redactions performed in the run summary.

If a safe summary cannot be produced without sensitive material, do not commit
that artifact.

## Never store

Never commit or intentionally preserve these items in this eval artifact lane:

- API keys.
- Bearer tokens.
- Dashboard passwords.
- Cookies.
- CSRF tokens.
- Session values.
- Raw provider payloads.
- Provider account identifiers.
- Full unredacted request/response traces.
- Private user data unless explicitly sanitized and needed.

## Acceptable artifact types

Acceptable committed artifacts are sanitized and summary-level:

- Summarized run report.
- Prompt set manifest.
- Scoring rubric reference.
- Summarized plain output.
- Summarized Alpha output.
- Score table.
- Defect list.
- Conservative interpretation.
- Screenshot reference if sanitized.

## Evidence strength levels

Use the strongest applicable label and explain it in the run summary:

| Level | Label | Meaning |
| --- | --- | --- |
| 1 | `operator-reported-summary` | Operator-reported result without preserved repo artifacts. |
| 2 | `screenshot-backed-summary` | Summary backed by sanitized screenshots or screenshot references. |
| 3 | `repo-preserved-summarized-artifact` | Sanitized summary artifacts preserved in the repo. |
| 4 | `automated-test-backed-artifact` | Artifact generation or validation backed by automated tests. |
| 5 | `live-provider-artifact-with-sanitized-metrics` | Live provider run metrics preserved in sanitized form without raw payloads. |

Evidence strength improves reviewability. It does not by itself prove MVP
validation, Alpha superiority, production readiness, benchmark success, billing
accuracy, or provider reasoning orchestration.

## Claim boundaries for every future report

Every future report must include a `Non-claims` section stating that artifact
preservation does not prove:

- MVP validation.
- Alpha Solver superiority.
- Production readiness.
- Broad runtime readiness.
- Benchmark success.
- Exact billing accuracy.
- Provider reasoning orchestration.

## Supported future lanes

This preservation guide supports:

- `HIGHER-HEADROOM-EVAL-001` by defining where and how to preserve sanitized run
  evidence before more live eval spend.
- `DISC-MRG-069` and `DISC-MRG-068` by providing citable repo artifacts for
  decisions that should not rely on chat memory or screenshots alone.
- `ALPHA-SIDE-BY-SIDE-EVIDENCE-PACKET-001` by defining required fields for
  Alpha-vs-plain comparison packets.
- Future `EVAL-DIFFERENTIATION-RUN-001` by defining the run report, score table,
  defects, redactions, evidence strength, and conservative interpretation needed
  for decision-making.

## Side-by-side evidence packets

Future Alpha-vs-plain comparison runs may add blank-template-derived
side-by-side evidence packets under `docs/evals/runs/` using
`docs/evals/templates/side_by_side_evidence_packet_template.md`. These packets
are review/index/interpretation artifacts only and must reference, not replace,
the score table, paired-output capture, blinded score sheet, blinding map, and
run report.
