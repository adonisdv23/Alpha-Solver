# 20260602-eval-differentiation-run-001-alpha-vs-plain · Eval Run Report

## Run metadata

- Run ID: `20260602-eval-differentiation-run-001-alpha-vs-plain`
- Date: 2026-06-02 scaffold date
- Operator: not assigned
- Branch/commit: to be recorded only in a later approved run
- Provider/mode: not executed
- Prompt set: higher-headroom prompt set pilot subset
- Prompt count: 4 planned prompts
- Live mode used: no
- Request cap used: not applicable; no requests made
- Rollback confirmed: not applicable; no run executed
- Blinding performed: no; no outputs exist to score
- Output A/B mapping file: `blinding-map.csv` is header-only and unpopulated

## Execution status

This run is not executed. No outputs are captured, no scores are recorded, no
blinded judging has occurred, no unblinding has occurred, and there is no
Alpha-vs-plain result yet.

## Plain output summary

Not executed. No plain output has been captured.

## Alpha output summary

Not executed. No Alpha output has been captured.

## Rubric used

- Rubric reference: `docs/evals/RESPONSE_QUALITY_RUBRIC.md`
- Rubric version or commit: to be recorded in a later approved run
- Scoring dimensions: all 14 dimensions are planned in `score-table.csv`, but no
  scores are recorded in this scaffold

## Score table

Use `score-table.csv` for the full 14-dimension comparison schema in a later
operator-approved scoring stage.

| Prompt ID | Plain total | Alpha total | total_delta | lift_delta | polish_delta | winning_surface | lift_qualified | polish_only_flag | length_ratio |
| --- | ---: | ---: | ---: | ---: | ---: | --- | --- | --- | ---: |
| Not executed |  |  |  |  |  |  |  |  |  |

## Alpha advantages observed

None recorded. The run has not been executed, so this scaffold records no Alpha
advantages.

## Plain advantages observed

None recorded. The run has not been executed, so this scaffold records no plain
advantages.

## Defects or regressions

No defects or regressions are recorded because no outputs have been captured or
scored. Use `defects.md` only after a later operator-approved run stage.

| ID | Side | Prompt ID | Defect/regression | Severity | Follow-up |
| --- | --- | --- | --- | --- | --- |
| Not executed |  |  |  |  |  |

## Metrics summary

- Latency summary: not applicable; no run executed.
- Token/cost summary, if safely available: not applicable; no provider calls.
- Request cap usage: zero requests made in this scaffold.
- Error/rollback summary: not applicable; no runtime activity.

## Evidence strength

Current scaffold evidence strength: `automated-test-backed-artifact` for file
presence, schema headers, non-claims, empty placeholders, and formatting only.

This is not evidence of answer quality, Alpha Solver superiority, benchmark
success, production readiness, broad runtime readiness, MVP validation, exact
billing accuracy, or provider reasoning orchestration.

## Redactions performed

- Secrets removed: no secrets were present.
- Tokens/cookies/session values removed: no tokens, cookies, or session values
  were present.
- Provider account identifiers removed: no provider account identifiers were
  present.
- Private user data sanitized or not present: not present.
- Raw provider payloads omitted: no provider payloads exist.
- Full unredacted request/response traces omitted: no request/response traces
  exist.
- Screenshots sanitized or not applicable: not applicable.

## Conservative interpretation

This artifact only shows that a controlled run scaffold exists for a future
operator-approved Alpha-vs-plain pilot. It does not validate the run, does not
show an Alpha-vs-plain result, and does not support validation or superiority
claims.

## Follow-up tickets

- Later operator-approved Stage B: capture sanitized paired outputs.
- Later operator-approved Stage C: complete blinded scoring, unblind, apply the
  lift decision rule, record defects, and write a conservative result summary.

## Non-claims

This artifact does not prove:

- MVP validation.
- Alpha Solver superiority.
- Answer-quality superiority.
- Production readiness.
- Broad runtime readiness.
- Benchmark success.
- Exact billing accuracy.
- Provider reasoning orchestration.
