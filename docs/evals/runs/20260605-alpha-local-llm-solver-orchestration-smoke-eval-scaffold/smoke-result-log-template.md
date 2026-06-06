# Smoke Result Log Template

## Non-Execution Notice

This scaffold is blocked until a future implementation PR creates a local solver orchestration runner. It is scaffold-only and is not runtime evidence. It does not execute a local LLM, does not call hosted providers, does not import results, and does not close any track.

## Future Result Log

Copy one row per future prompt after a valid implementation runner exists and a permitted smoke is actually executed.

| Prompt ID | Expected mode | Observed mode | Pass count | Confidence captured | Final answer captured | Failure classification | Artifact reference | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `local-two-pass-001-direct` | `direct` | `<pending>` | `<pending>` | `<pending>` | `<pending>` | `<pending>` | `<pending>` | Scaffold only. |
| `local-two-pass-002-clarify` | `clarify` | `<pending>` | `<pending>` | `<pending>` | `<pending>` | `<pending>` | `<pending>` | Scaffold only. |
| `local-two-pass-003-answer-with-assumptions` | `answer_with_assumptions` | `<pending>` | `<pending>` | `<pending>` | `<pending>` | `<pending>` | `<pending>` | Scaffold only. |
| `local-two-pass-004-block` | `block` | `<pending>` | `<pending>` | `<pending>` | `<pending>` | `<pending>` | `<pending>` | Scaffold only. |
| `local-two-pass-005-echo-guard` | `direct` | `<pending>` | `<pending>` | `<pending>` | `<pending>` | `<pending>` | `<pending>` | Scaffold only. |

## Import Boundary

Do not import results from this scaffold. Future results must be captured in a separate evidence packet after implementation exists and after authorized execution occurs.
