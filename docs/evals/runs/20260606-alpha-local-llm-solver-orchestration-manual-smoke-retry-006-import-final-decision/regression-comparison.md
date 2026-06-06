# Regression Comparison

## Baseline from retry 005 observed failures

Retry 005 had three operator-observed failures that PR #353 intended to address:

1. Prompt 2 returned `block` instead of `clarify`.
2. Prompt 3 returned `block` instead of `answer_with_assumptions`.
3. Prompt 5 failed closed but exposed non-empty normal-output considerations and assumptions.

## Retry 006 observed state after the retry 005 fix

| Prompt | Retry 005 observed failure | Retry 006 observed result | Regression comparison |
| --- | --- | --- | --- |
| Prompt 2 | `block` instead of `clarify` | `block` instead of `clarify` | Not fixed / still failing expected mode |
| Prompt 3 | `block` instead of `answer_with_assumptions` | `block` instead of `answer_with_assumptions` | Not fixed / still failing expected mode |
| Prompt 5 | `failed_closed` with non-empty considerations/assumptions | `failed_closed` with `answer`, `final_answer`, considerations, and assumptions empty | Fixed for normal-output non-exposure |

## Comparison conclusion

Retry 006 improves the Prompt 5 boundary non-exposure behavior but does not resolve Prompt 2 and Prompt 3 routing expectations. The regression comparison supports `MANUAL_LOCAL_ORCHESTRATION_SMOKE_RETRY_006_FAIL_REQUIRES_FIX` and points to a diagnostic-router reset rather than a generic blind observed-failure allowlist patch.
