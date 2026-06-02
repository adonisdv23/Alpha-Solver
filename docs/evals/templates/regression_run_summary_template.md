# <Regression Run ID> · Prompt Quality Regression Summary

## Run metadata

- Regression run ID:
- Date:
- Operator/reviewer:
- Branch/commit:
- Prior baseline run artifact:
- Current run artifact:
- Prompt set ID/version:
- Related behavior/spec change:
- Rubric reference: `docs/evals/RESPONSE_QUALITY_RUBRIC.md`
- Artifact preservation reference: `docs/evals/ARTIFACT_PRESERVATION.md`

## Regression comparison table

| Prompt ID | Prompt family | Prior Alpha total | Current Alpha total | Delta | Prior lift_delta | Current lift_delta | Prior lift_qualified | Current lift_qualified | Regression status | Expected change rationale | Notes |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- | --- | --- | --- | --- |
|  |  |  |  |  |  |  |  |  | Regression flagged/No regression/Expected change/Inconclusive |  |  |

Track regressions on lift (`lift_delta`, `lift_qualified`), not only on polish or
total score, so that a structure-only change is not recorded as an improvement.

## Dimensions reviewed

Flag material degradation in:

- Direct answer usefulness:
- Format preservation:
- Assumptions:
- Hidden constraints:
- Risk/failure modes:
- Claim boundaries:
- Next actions:
- Comparative added value:

## Defects or follow-up tickets

| ID | Prompt ID | Dimension | Defect/regression | Severity | Follow-up ticket |
| --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  |

## Expected changes versus regressions

Summarize which score changes were expected because of a documented behavior,
spec, or implementation change, and which changes are regressions requiring
follow-up.

## Redactions performed

- Raw provider payloads omitted:
- Secrets/tokens/cookies/session values removed:
- Provider account identifiers removed:
- Private user data sanitized or not present:
- Full unredacted request/response traces omitted:

## Conservative interpretation

State the narrowest regression conclusion supported by the preserved artifacts.
Do not claim broad superiority or readiness from this run.

## Non-claims

This regression summary does not prove:

- MVP validation.
- Alpha Solver superiority.
- Production readiness.
- Broad runtime readiness.
- Benchmark success.
- Exact billing accuracy.
- Provider reasoning orchestration.
