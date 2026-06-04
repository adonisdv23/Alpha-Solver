# Post-Improvement Finalization Cluster Hardening

Hardening lane ID: `OUTPUT-DIFF-POST-IMPROVEMENT-FINALIZATION-CLUSTER-HARDENING-001`

Status: optional docs-only hardening update after merged PR #270. PR #270 remains the required finalization completion PR for:

- `OUTPUT-DIFF-POST-IMPROVEMENT-INTERPRETATION-001`
- `ALPHA-MINIMAL-CONTRACT-REFINEMENT-DECISION-001`

PR #271 does not re-complete either required finalization lane. It preserves the PR #270 outcome and only hardens the lift/polish/brevity cluster-analysis basis.

## Source scored artifacts used

This hardening update uses only committed scored and preservation artifacts from the post-minimal-behavior portable capture lane:

- `docs/evals/runs/20260604-post-minimal-behavior-portable-capture/score-table.csv`
- `docs/evals/runs/20260604-post-minimal-behavior-portable-capture/scored-artifact-summary.md`
- `docs/evals/runs/20260604-post-minimal-behavior-portable-capture/score-arithmetic-check.md`
- `docs/evals/runs/20260604-post-minimal-behavior-portable-capture/unblinding-application-log.md`
- `docs/evals/runs/20260604-post-minimal-behavior-portable-capture/post-improvement-run-summary.md`
- `docs/evals/runs/20260604-post-minimal-behavior-portable-capture/scored-artifact-preservation-checklist.md`
- `docs/evals/runs/20260604-post-minimal-behavior-portable-capture/blind-scorer-result.md`
- `docs/evals/runs/20260604-post-minimal-behavior-portable-capture/blind-scoring-defects.md`
- `docs/evals/runs/20260604-post-minimal-behavior-portable-capture/blind-scoring-completeness-check.md`
- `docs/evals/RESPONSE_QUALITY_RUBRIC.md`
- `docs/evals/ARTIFACT_PRESERVATION.md`
- `docs/evals/LIFT_DECISION_RULE.md`
- `.specs/EVAL-ARTIFACT-PRESERVE-001.md`
- Prior preserved A3-1 and Batch B summary/scored artifacts under `docs/evals/runs/`

Raw output content was not inspected or used for this hardening update.

## Artifact integrity status

Artifact integrity remains preserved.

The PR #269 scored-artifact preservation checklist and unblinding application log state that the locked blind score sheet was preserved, the operator-only map was preserved, no rescoring occurred, no capture rerun occurred, no raw outputs were read for scoring or interpretation, no raw outputs were modified, the sanitized scorer-facing packet was not modified, no locked score edits occurred, no Google Sheets update occurred, no Batch C work started, no runtime/provider/model/routing behavior changed, and no `/v1/solve` measurement occurred.

This PR #271 follow-up only edits finalization documents under `docs/evals/runs/20260604-post-minimal-behavior-finalization/`.

## Locked blind result preserved

- Output A aggregate blinded total: 306
- Output B aggregate blinded total: 311
- Aggregate blinded delta, Output A minus Output B: -5
- Blinded preference counts: Output A 3 / Output B 3 / Tie 2 / Inconclusive 0

## Unblinded scored result preserved

- Alpha total: 314
- Plain total: 303
- Alpha minus plain delta: +11
- Alpha wins: 5
- Plain wins: 1
- Ties: 2

## Interpretation of delta preserved

Alpha's +11 result remains a modest positive Alpha result on a limited 8-comparison portable-surface diagnostic. The 5 / 1 / 2 win/loss/tie pattern is directionally favorable to Alpha, but the total-score margin is small relative to the approximately 300-point aggregate scale.

This should not be treated as decisive evidence or as broad Alpha-over-plain superiority. It remains a limited portable-surface signal after the PR #263 minimal portable behavior contract, bounded by the prompt set, scorer rubric, committed scored artifacts, and artifact-preservation chain.

## Outcome family preserved

Formal family: **B. Mixed improvement with brevity/control concern**.

Unified taxonomy used:

- A. Clear portable-surface improvement
- B. Mixed improvement with brevity/control concern
- C. Neutral / polish-only / near-parity
- D. Negative result
- E. Inconclusive result
- F. Compromised artifact chain

## Rationale for preserving Family B

Family B remains the conservative fit because:

- The aggregate result is positive for Alpha: +11 across 8 comparisons.
- Alpha wins 5 comparisons, Plain wins 1, and 2 are ties.
- The exact lift/polish/brevity calculation from the committed `score-table.csv` shows a lift-cluster advantage for Alpha, not a polish-only result.
- The polish cluster is flat, so the result is not explained by presentation polish.
- Brevity remains slightly negative for Alpha, and prior Batch B evidence identified brevity/control as a material Alpha weakness.
- Several comparison margins are narrow, so the evidence supports refinement rather than expansion or runtime/readiness work.

This remains stronger than neutral near-parity because Alpha has a positive aggregate, a 5-to-1 win count, and a positive lift-cluster delta. It remains below Family A because the total margin is modest, the surface is limited to portable behavior, and brevity/control remains a recurring concern.

## Lift/polish/brevity hardening review

The committed `score-table.csv` includes the per-dimension Alpha and plain scores needed to calculate the existing lift and polish clusters from `docs/evals/LIFT_DECISION_RULE.md`.

Cluster definitions used:

- Lift cluster: `d04_assumptions`, `d05_hidden_constraints`, `d06_risk_failure`, `d14_comparative_value`
- Polish cluster: `d03_structure`, `d10_next_actions`, `d12_brevity`
- Brevity dimension: `d12_brevity`

Calculated from committed scored artifacts:

| Cluster / dimension | Plain | Alpha | Alpha minus plain |
| --- | ---: | ---: | ---: |
| Lift cluster | 70 | 80 | +10 |
| Polish cluster | 69 | 69 | 0 |
| Brevity only | 24 | 23 | -1 |

Interpretation hardening:

- The +10 lift-cluster delta accounts for most of the +11 aggregate result and is directionally aligned with Alpha's intended value: assumptions, hidden constraints, risk/failure framing, and comparative value.
- The 0 polish-cluster delta argues against a polish-only explanation for the Alpha aggregate result.
- The -1 brevity delta is small in this run, but it keeps brevity/control as a live concern because Batch B previously showed a larger brevity weakness.
- This cluster analysis hardens the PR #270 interpretation without changing the lane result, decision, next lane, or evidence boundary.

## Comparison against A3-1 preserved

A3-1 result:

- Plain total: 237
- Alpha total: 228
- Alpha delta: -9
- Plain won all 4 limited comparisons

This post-improvement result moves in the opposite direction from A3-1: Alpha is ahead by +11 with 5 wins, 1 Plain win, and 2 ties. That supports the view that PR #263 likely helped the portable contract surface, but only with limited evidence. A3-1 did not establish broad plain-favored dominance, and this run does not erase the need for narrow evidence boundaries.

## Comparison against Batch B preserved

Batch B result:

- Plain total: 405
- Alpha total: 455
- Alpha delta: +50
- Alpha wins: 8
- Plain wins: 4
- Ties: 0

Batch B diagnostic pattern:

- Lift cluster: Plain 111, Alpha 132, Alpha delta +21
- Polish cluster: Plain 87, Alpha 86, Alpha delta -1
- Brevity: Plain 26, Alpha 16, Alpha delta -10

The post-improvement portable result is directionally consistent with Batch B in that Alpha again shows a positive aggregate and lift-cluster advantage while polish does not explain the result. It is weaker in magnitude than Batch B: +11 over 8 comparisons here versus +50 over 12 comparisons in Batch B. The brevity weakness is much smaller here (-1), but not eliminated as a decision concern because earlier evidence showed it can become material on brevity-sensitive prompts.

## PR #263 verdict preserved

Verdict: **helped, limited evidence**.

Rationale: the first post-PR #263 scored portable-surface run shows Alpha +11 with a 5 / 1 / 2 win/loss/tie pattern and a lift-cluster advantage of +10. The evidence is limited to this portable diagnostic and does not support broader claims.

## Evidence boundary preserved

This hardening update remains bounded to portable-surface evidence only. It does not provide evidence for:

- `/v1/solve` behavior
- Runtime API behavior
- Provider behavior
- Model routing behavior
- Production readiness
- Broad runtime readiness
- MVP validation
- Benchmark outcome success
- Exact-billing accuracy
- Provider orchestration behavior
- Automatic-recovery capability
- Adaptive-learning capability
- Self-optimization capability
- Autonomous-optimization capability
- Broad Alpha-over-plain superiority
- Broad plain-over-Alpha inferiority
- Batch C authorization

## Recommended next lane preserved

Recommended next lane remains: `ALPHA-BREVITY-CONTROL-REFINEMENT-001`.

## Blocked work preserved

The following remain blocked by the evidence boundary and should not be started from this hardening update:

- Batch C execution
- Runtime/provider/model/routing work
- `/v1/solve` measurement or claims
- Production-readiness documentation
- Google Sheets updates from this PR
- Broad validation, readiness, or superiority narratives

## Non-claims

This document makes no claim that the MVP is validated, that the system is production-ready, that Alpha is generally superior, that a benchmark has succeeded, that billing is exact, that provider orchestration is proven, that `/v1/solve` improved, that runtime behavior is ready, or that automatic-recovery, adaptive-learning, self-optimization, or autonomous-optimization capabilities are demonstrated.
