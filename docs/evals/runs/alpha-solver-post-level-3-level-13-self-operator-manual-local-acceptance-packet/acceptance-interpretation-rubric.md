# Acceptance Interpretation Rubric

This rubric prepares future interpretation only. No interpretation is performed here.

- Passed means the task produced expected artifacts, stayed within the evidence boundary, preserved redaction, and matched the expected result.
- Failed means artifacts or observed behavior contradict the expected result.
- Blocked means the task could not be run or reviewed due to prerequisite, artifact, environment, or boundary limitations.
- The run proves only the reviewed local dry-run acceptance behavior at the recorded commit, inputs, and environment.
- The run does not prove production readiness, hosted behavior, provider behavior, benchmark superiority, autonomous operation, deployment readiness, billing readiness, or MVP readiness.
- Defect classes: approval gate defect, identity mismatch defect, unsafe-command gate defect, artifact path defect, overwrite defect, redaction defect, evidence-boundary defect, non-execution defect, reproducibility defect, documentation defect.
- Retry criteria: retry only after the defect or blocked condition is understood, scope remains local-only, artifacts are not overwritten, and the operator explicitly confirms rerun intent.
- Readiness-blocking conditions: unexpected execution, unsafe command not blocked, identity mismatch not blocked, source mutation, evidence-boundary violation, failed redaction, missing required artifacts, or non-reproducible acceptance task.
- No broad superiority claims are allowed.
- No MVP readiness claim is allowed until evidence exists and is interpreted in a later lane.
