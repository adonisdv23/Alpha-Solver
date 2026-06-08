# Stop Conditions

Self Operator must stop before taking a gated action when any condition in this file is present.

## Approval-state stop conditions

Self Operator must stop when approval state is:

- Missing.
- Ambiguous.
- Contradictory.
- Stale or outside the approved time window.
- Partial or missing required approval-record fields.
- Attached to a different action, target, branch, provider, environment, credential, browser target, billing target, deployment target, or evidence artifact.
- Broader than allowed by repo instructions, specs, safety rules, or the current lane.
- Not auditable.

## Action-boundary stop conditions

Self Operator must stop when the next action may involve:

- PR creation without approval.
- Merge instructions without approval.
- External provider calls without approval.
- File deletion without approval.
- Deployment without approval.
- Billing without approval.
- Credential use without approval.
- Browser automation without approval.
- Evidence promotion without approval.

## Evidence-boundary stop condition

Self Operator must stop if a proposed action would imply that docs-only approval-control design has implemented controls, executed actions, called providers, modified runtime, deployed, merged, or promoted evidence.
