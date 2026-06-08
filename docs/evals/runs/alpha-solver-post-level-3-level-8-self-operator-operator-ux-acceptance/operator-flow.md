# Operator Flow

## Required MVP flow

The earliest Self Operator MVP must make the operator flow explicit and reviewable.

1. **Task intake**
   - Show the task title or identifier.
   - Show the requested outcome and any known constraints.
   - Show whether the task is inspect-only or requests changes.
   - Show the evidence boundary and the no-provider-call boundary before any approval.

2. **Preflight result**
   - Show prerequisite checks and status: `pass`, `warning`, or `blocked`.
   - Show any missing inputs, unsafe ambiguity, path issues, or policy boundary conflicts.
   - Do not advance to approval when preflight is blocked.

3. **Approval request**
   - Ask the operator to approve the specific next action, not a vague session.
   - Include the planned artifacts and stop mechanism.
   - State that approval does not authorize provider calls unless the provider boundary is explicitly included.

4. **Running status**
   - Show current lifecycle state and last operator-visible event.
   - Show whether the run is still within approved scope.
   - Show artifact paths as soon as they are reserved or created.

5. **Stop state**
   - Offer a visible stop control or stop instruction throughout running state.
   - Show `stop requested`, then either `stopped` or `stop failed` with reason.
   - Preserve partial artifacts where possible and identify incomplete outputs.

6. **Blocked action**
   - Stop progression when an approval, safety, evidence, credential, provider, path, or policy boundary blocks the action.
   - Show the block reason in operator-readable language.
   - Point unresolved blocker handling to the fallback lane.

7. **Completed state**
   - Show a concise completion message.
   - List created artifacts and review steps.
   - Identify any warnings, non-actions, and outputs that must not be treated as implementation evidence.

8. **Artifact review**
   - Provide stable artifact locations.
   - Identify the minimum files the operator must review.
   - Distinguish final artifacts from logs, partial outputs, and scratch evidence.

## State labels

The UX must use stable state labels or equivalents: `intake`, `preflight`, `awaiting_approval`, `approved`, `running`, `stopping`, `stopped`, `blocked`, `completed`, and `failed`.
