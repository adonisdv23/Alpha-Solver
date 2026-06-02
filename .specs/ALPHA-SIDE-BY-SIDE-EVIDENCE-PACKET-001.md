# ALPHA-SIDE-BY-SIDE-EVIDENCE-PACKET-001 · Side-by-Side Evidence Packet Contract

## Status

Documentation/spec-first lane for `OUTPUT-DIFFERENTIATION-PHASE-001`.

`ALPHA-SIDE-BY-SIDE-EVIDENCE-PACKET-001` creates the reusable side-by-side evidence
packet contract and blank packet template that future Alpha-vs-plain
`EVAL-DIFFERENTIATION-RUN-001` artifacts can populate. This lane is
**docs/templates/tests only**. It does not execute a run, score outputs, create
live provider calls, or add populated evidence packets.

## Purpose

The output-differentiation measurement layer now has hardened capture and scoring
artifacts for all 14 rubric dimensions, blinded Output A / Output B scoring,
separate unblinding maps, paired-output capture, lift/polish/length decision aids,
Alpha expert-envelope evidence, and strict non-claims. This spec adds a thin
review/index/interpretation packet on top of those artifacts so future reviewers
can summarize one comparison without replacing the underlying source artifacts.

## Scope

In scope:

- Add `docs/evals/templates/side_by_side_evidence_packet_template.md` as a
  blank, placeholder-only packet template.
- Require packet references to the existing hardened artifacts:
  - `docs/evals/templates/paired_output_capture_template.md`;
  - `docs/evals/templates/blinded_score_sheet_template.csv`;
  - `docs/evals/templates/blinding_map_template.csv`;
  - `docs/evals/templates/comparison_score_table_template.csv`;
  - `docs/evals/templates/run_report_template.md`;
  - `docs/evals/RESPONSE_QUALITY_RUBRIC.md`;
  - `docs/evals/LIFT_DECISION_RULE.md`;
  - `docs/evals/BLIND_SCORING_PROCEDURE.md`;
  - `docs/evals/ARTIFACT_PRESERVATION.md`.
- Add docs-integrity tests that verify the packet contract, section coverage,
  field coverage, artifact references, redaction boundaries, and non-claims.
- Update eval docs to identify the packet as an optional future per-comparison
  review/index/interpretation artifact stored beside sanitized run artifacts.

Out of scope:

- The first scored differentiation run or any populated evidence packet.
- Live provider calls, scoring actual Alpha-vs-plain outputs, or changing scoring
  behavior.
- Provider expert-pass behavior, clarify behavior, `/v1/solve`, preview UI
  rendering, dashboard auth, tool routing, effort toggle, persistent quota, or
  provider reasoning orchestration.
- `scripts/run_answer_quality_eval.py` or the multiple-choice answer-quality eval.
- Google Sheets, backlog workbooks, or external planning ledgers.

## Packet contract

The side-by-side evidence packet is a **review/index/interpretation artifact**.
It must link to source artifacts and preserve conservative interpretation, but it
must not replace the comparison score table, paired-output capture, blinded score
sheet, blinding map, or run report.

A future populated packet must include the following sections:

1. Packet identity
2. Source artifact references
3. Prompt under review
4. Output capture summary
5. Blinded scoring record
6. Unblinding record
7. Fourteen-dimension scores
8. Lift / polish / total decision aid
9. Expert-envelope evidence
10. Material constraints, assumptions, and risks
11. Defects, regressions, and over-interrogation
12. Evidence-limited explanation
13. Conservative interpretation
14. Redactions performed
15. Follow-up tickets
16. Non-claims

The template must remain blank/placeholder-only and must not include actual scored
examples or populated evidence.

## Required packet fields

A future packet must carry placeholders for:

- `packet_id`
- `comparison_id`
- `parent_run_id`
- `run_directory`
- `prompt_id`
- `prompt_family`
- `difficulty_headroom`
- `evidence_strength`
- `non_claims_confirmed`
- `blinded_score_sheet path`
- `blinding_map path`
- `paired_output_capture path`
- `comparison_score_table path`
- `run_report path`
- `plain_total`
- `alpha_total`
- `total_delta`
- `lift_delta`
- `polish_delta`
- `winning_surface`
- `lift_qualified`
- `material_constraint_verified`
- `polish_only_flag`
- `length_ratio`
- `considerations`
- `assumptions`
- `material/correct tags`
- `confidence`
- `mode`
- `clarifying questions`
- `sanitized metadata`
- `over-interrogation defect category`
- `redactions performed`

## Fourteen-dimension coverage

The packet must list all 14 dimension keys from
`docs/evals/RESPONSE_QUALITY_RUBRIC.md`:

- `d01_intent`
- `d02_direct`
- `d03_structure`
- `d04_assumptions`
- `d05_hidden_constraints`
- `d06_risk_failure`
- `d07_claim_boundary`
- `d08_evidence_uncertainty`
- `d09_decision`
- `d10_next_actions`
- `d11_specificity`
- `d12_brevity`
- `d13_safety`
- `d14_comparative_value`

## Redaction and storage boundaries

Packets may include sanitized summaries and references to committed source
artifacts. They must not commit secrets, credentials, raw provider payloads,
provider account identifiers, private user data, full unredacted request/response
traces, environment dumps, dashboard credentials, cookies, CSRF tokens, session
values, or authorization tokens. If a safe summary cannot be produced, omit the
unsafe material and record the omission in `redactions performed`.

## Non-claims

This packet contract does not claim MVP validation, Alpha Solver superiority,
answer-quality superiority, production readiness, broad runtime readiness,
benchmark success, exact billing accuracy, or provider reasoning orchestration.
Each future packet must carry these non-claims and should interpret only the
narrow evidence preserved in its referenced artifacts.
