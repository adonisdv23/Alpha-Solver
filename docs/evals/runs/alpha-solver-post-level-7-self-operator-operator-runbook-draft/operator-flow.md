# Future Operator Flow

## Boundary

This is a future-use flow only. It must not be used as a command sequence today, and it does not authorize or imply any existing Self Operator capability.

## Future flow overview

1. **Intake the task**
   - Confirm the task is specific, bounded, and assigned to the future Self Operator lane.
   - Confirm the requested work is permitted by the current repo instructions and relevant specs.
   - Stop if the task is unclear or lacks a current implementation contract.

2. **Review source evidence**
   - Read the relevant implementation spec, operator guide, recent run packets, safety notes, and current branch status.
   - Stop if evidence is missing, stale, contradictory, or not tied to the exact future Self Operator version.

3. **Run preflight checks**
   - Complete `preflight-checklist.md` before any future start command.
   - Stop if credentials, branch state, provider routing, fallback behavior, artifact destination, or rollback path is ambiguous.

4. **Obtain explicit approval**
   - Complete `approval-checklist.md` with a named approver and exact approved scope.
   - Stop if approval is absent, partial, expired, or does not match the requested task.

5. **Start the future run**
   - Use only the future approved entrypoint and exact approved parameters.
   - Capture command provenance, environment summary, git branch, commit SHA, time, operator, approver, and artifact directory.
   - Do not improvise provider, model, credential, route, or fallback settings.

6. **Monitor continuously**
   - Use `monitoring-checklist.md` while the run is active.
   - Stop immediately for missing evidence, missing approval, unclear task, provider/fallback ambiguity, credential risk, branch pollution, unexpected file changes, uncontrolled spending, or unsafe output.

7. **Stop and recover when required**
   - Follow `stop-and-recovery.md` before attempting any continuation.
   - Prefer preserving evidence and fail-closed handling over completing the task.

8. **Review artifacts**
   - Use `artifact-review.md` to confirm provenance, redaction, completeness, and non-promotion boundaries.
   - Do not promote artifacts into readiness, quality, safety, or performance evidence without a separate approved evidence-promotion lane.

9. **Archive and close out**
   - Use `archive-and-closeout.md` to freeze the future run packet, document decisions, and record follow-up or no-further-lane state.
