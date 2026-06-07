# Inclusion Criteria

A future task candidate may be considered within this taxonomy reference only if all applicable criteria are satisfied.

## Required criteria

- The task is documentation-review or design-review oriented unless a later authorized lane explicitly permits execution.
- The task has a clear Alpha Solver evidence boundary.
- The task can be evaluated against repository source material, packet text, or explicit future source evidence.
- The task can state what artifacts would be reviewed without requiring local model inference, provider calls, benchmarks, scoring, billing work, dashboards, or `/v1/solve` exposure.
- The task identifies relevant inclusion criteria, exclusion criteria, risk labels, and expected artifacts.
- The task can preserve selected-next and blocker fallback state without selecting a new lane unless the authorizing packet permits it.
- The task can be completed without modifying preserved source artifacts, closed Level 2 packets, closed Level 3 packets, release-readiness ladder files, runtime files, provider files, CLI files, checker scripts, tests, Makefile targets, or CI files.

## Preferred criteria

- The task has a narrow source-evidence scope.
- The task can be reviewed deterministically from text artifacts.
- The task separates claim-boundary review from execution-quality measurement.
- The task records non-actions explicitly.
