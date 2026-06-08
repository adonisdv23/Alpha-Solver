# Future Preflight Checklist

## Use boundary

This checklist is a draft for a future implementation. Passing this checklist today would not prove that Self Operator exists, is implemented, is ready, or is safe to run.

## Required preflight gates

Before a future Self Operator run starts, the operator must verify:

- [ ] The future Self Operator implementation exists on the current branch or approved release.
- [ ] The relevant spec or implementation contract is identified and matches the requested task.
- [ ] The task is clear, bounded, and has an allowed stop point.
- [ ] The branch is clean except for explicitly approved worktree changes.
- [ ] The current branch name and commit SHA are recorded.
- [ ] The future run artifact directory is empty or intentionally created for this run.
- [ ] The provider, model, local/runtime mode, hosted mode, fallback behavior, and budget mode are explicit.
- [ ] Provider and fallback settings cannot silently change during the run.
- [ ] No credential values will be printed, committed, uploaded, or stored in artifacts.
- [ ] Required secrets are present only through approved secret handling.
- [ ] Network, provider, and deployment permissions match the approved scope.
- [ ] The operator can stop the run immediately using the documented future stop mechanism.
- [ ] Recovery, rollback, and artifact preservation steps are known before start.

## Mandatory pre-start stops

Do not start the future run if any item is unchecked or uncertain, especially:

- missing evidence;
- missing approval;
- unclear task;
- provider or fallback ambiguity;
- credential risk;
- branch pollution.
