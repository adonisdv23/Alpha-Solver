# Analysis Plan

STATUS: PROTOCOL ONLY - NOT EXECUTED. Contains no results and is no evidence of value.

## Primary paired comparison

Compute paired per-task composite differences between Alpha and baseline after unblinding. Report the raw paired mean or median difference and the paired win/tie/loss counts only for an executed future run.

## Length-adjusted model

Record answer length for each condition. Report raw and length-adjusted differences using the preregistered paired model:

```text
score_diff_i = beta0 + beta1 * length_diff_i + error_i
```

`beta0` is the length-adjusted Alpha effect.

## Tie handling

Composite difference within `+/-0.3` is a tie. Because Alpha has higher cost and latency prior, an overall tie is `NO-GO` for general superiority. A clear win limited to abstention/calibration can support only a narrow abstention/calibration claim.

## Confidence interval reporting

Report confidence intervals for the primary paired difference and the length-adjusted effect in any future execution. Do not report intervals in protocol-only artifacts.

## Stratum caveats

Report results by task stratum and state when strata are underpowered. Stratum wins do not imply general superiority unless the predefined overall criteria also pass.

## Human validation rule

At least `15` random tasks require human validation. Human adjudication is required for hallucination flags and ties.

## Blinding-integrity rule

Judges must guess which answer was Alpha and record confidence. If blinding is badly compromised, the run is `NO-GO` for general superiority.

## Cost/latency reporting rule

Record and report cost and latency for each condition. Cost and latency are not standalone gates, but no unqualified superiority claim is allowed if Alpha's premium is high.

## NO-GO conditions

The run is `NO-GO` if Alpha is worse overall after length adjustment, worse on correctness, worse on hallucination, blinding is badly compromised, or the echo precondition fails.
