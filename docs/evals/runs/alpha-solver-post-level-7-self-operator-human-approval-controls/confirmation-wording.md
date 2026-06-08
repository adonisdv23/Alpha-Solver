# Confirmation Wording

## Required confirmation pattern

For gated actions, Self Operator should require confirmation that follows this pattern:

```text
I approve Self Operator to perform [ACTION CATEGORY] on [EXACT TARGET] for [SPECIFIC PURPOSE] within [TIME WINDOW], limited to [SCOPE LIMITS]. I understand Self Operator must stop if approval state becomes missing, ambiguous, stale, contradictory, or out of scope.
```

## Category examples

- PR creation: `I approve Self Operator to create a PR for branch [BRANCH] targeting [BASE] for [PACKET OR CHANGE SUMMARY] within [TIME WINDOW], limited to [SCOPE LIMITS].`
- Merge instructions: `I approve Self Operator to provide merge instructions for PR [PR IDENTIFIER] within [TIME WINDOW], limited to [SCOPE LIMITS].`
- External provider calls: `I approve Self Operator to call [PROVIDER] for [PURPOSE] using [DATA BOUNDARY] within [TIME WINDOW], limited to [SCOPE LIMITS].`
- File deletion: `I approve Self Operator to delete [EXACT FILE PATHS] for [PURPOSE] within [TIME WINDOW], limited to [SCOPE LIMITS].`
- Deployment: `I approve Self Operator to deploy [ARTIFACT OR SERVICE] to [ENVIRONMENT] for [PURPOSE] within [TIME WINDOW], limited to [SCOPE LIMITS].`
- Billing: `I approve Self Operator to perform [BILLING ACTION] on [BILLING TARGET] for [PURPOSE] within [TIME WINDOW], limited to [SCOPE LIMITS].`
- Credential use: `I approve Self Operator to use [CREDENTIAL NAME OR SOURCE] for [PURPOSE] within [TIME WINDOW], limited to [SCOPE LIMITS].`
- Browser automation: `I approve Self Operator to automate browser actions on [EXACT SITE OR SESSION TARGET] for [PURPOSE] within [TIME WINDOW], limited to [SCOPE LIMITS].`
- Evidence promotion: `I approve Self Operator to promote [EVIDENCE ARTIFACT] to [CLAIM OR RELEASE STATUS] for [PURPOSE] within [TIME WINDOW], limited to [SCOPE LIMITS].`

## Denial and stop wording

When approval is absent or unclear, Self Operator should use wording equivalent to:

```text
Approval is missing or ambiguous for this gated action. Self Operator will stop and will not proceed unless a valid approval record is provided.
```
