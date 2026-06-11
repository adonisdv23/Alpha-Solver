# Operator confirmation required

A future repeatability execution lane must not run unless the operator provides
both labels below exactly and the confirmation content matches the selected
repeatability target.

## Exact required confirmation text

```text
OPERATOR_APPROVED_REPEATABILITY_TARGET:
Repeat the same existing evidence packet consistency review pattern used by the first supervised use, using a fresh run ID and fresh output root.

OPERATOR_CONFIRMATION:
I confirm this repeatability execution is local-only and operator-supervised. It must use no providers, no hosted models, no local models, no external APIs, no browser automation, no deployment, no billing, no credentials or secrets, no /v1/solve exposure, no dashboard exposure, no source-artifact mutation, no evidence promotion, no readiness claim, no final status CLI implementation, and a fresh run ID is required.
```

## Validation rule

If either label is missing, if the target text differs materially from the
selected target, or if any required prohibition is omitted, the future execution
lane must stop before running commands and record `operator_confirmation_invalid`.
