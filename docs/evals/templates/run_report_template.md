# <Run ID> · Eval Run Report

## Run metadata

- Run ID:
- Date:
- Operator:
- Branch/commit:
- Provider/mode:
- Prompt set:
- Prompt count:
- Live mode used: yes/no
- Request cap used:
- Rollback confirmed: yes/no/not applicable
- Blinding performed: yes/no (see docs/evals/BLIND_SCORING_PROCEDURE.md)
- Output A/B mapping file: docs/evals/templates/blinding_map_template.csv

## Plain output summary

Summarize plain provider output. Do not paste raw provider payloads or full
unredacted request/response traces.

## Alpha output summary

Summarize Alpha output. Do not paste raw provider payloads or full unredacted
request/response traces.

## Rubric used

- Rubric reference:
- Rubric version or commit:
- Scoring dimensions:

## Score table

Use `docs/evals/templates/comparison_score_table_template.csv` for the full
14-dimension per-output scores. Summarize per prompt here:

| Prompt ID | Plain total | Alpha total | total_delta | lift_delta | polish_delta | winning_surface | lift_qualified | polish_only_flag | length_ratio |
| --- | ---: | ---: | ---: | ---: | ---: | --- | --- | --- | ---: |
|  |  |  |  |  |  |  |  |  |  |

Lift/polish subscores and the `lift_qualified` decision aid are defined in
`docs/evals/LIFT_DECISION_RULE.md` (internal review aid only).

## Alpha advantages observed

- TBD.

## Plain advantages observed

- TBD.

## Defects or regressions

| ID | Side | Prompt ID | Defect/regression | Severity | Follow-up |
| --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  |

## Metrics summary

- Latency summary:
- Token/cost summary, if safely available:
- Request cap usage:
- Error/rollback summary:

## Evidence strength

Choose one or more:

- `operator-reported-summary`
- `screenshot-backed-summary`
- `repo-preserved-summarized-artifact`
- `automated-test-backed-artifact`
- `live-provider-artifact-with-sanitized-metrics`

Explanation:

## Redactions performed

- Secrets removed:
- Tokens/cookies/session values removed:
- Provider account identifiers removed:
- Private user data sanitized or not present:
- Raw provider payloads omitted:
- Full unredacted request/response traces omitted:
- Screenshots sanitized or not applicable:

## Conservative interpretation

State the narrowest interpretation supported by the preserved evidence. Separate
observations from conclusions and note uncertainty.

## Follow-up tickets

- TBD.

## Non-claims

This artifact does not prove:

- MVP validation.
- Alpha Solver superiority.
- Production readiness.
- Broad runtime readiness.
- Benchmark success.
- Exact billing accuracy.
- Provider reasoning orchestration.
