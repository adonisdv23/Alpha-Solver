# Branch Pollution Risks

## Risks

- Polluted PR branches can mix authorized docs with unrelated runtime changes, generated files, source artifacts, dependency lock changes, workbook changes, or prior failed attempts.
- Stale PR updates can reuse old checks after the base branch, selected-next state, risk boundary, or reviewer instructions changed.
- Force pushes can erase reviewer context or hide unsafe changes.
- Broad refactors can accidentally alter sensitive systems such as MCP, routing, SAFE-OUT, budget guard, determinism, observability, replay, or SolverEnvelope behavior.
- Automated conflict resolution can choose convenience over preserving reviewer intent.

## Mitigations required before implementation

- Require lane-scoped write allowlists and explicit changed-file confirmation.
- Require `git status --short`, `git diff --name-only`, and diff review before commit.
- Require fresh base-branch checks before significant PR updates.
- Require a rule that Self Operator cannot merge, enable auto-merge, change branch protections, or force-push without explicit human authorization.
- Require source-artifact and backlog-workbook protections.

## Stop conditions

- Stop if changed files are outside the authorized lane.
- Stop if a PR branch contains unrelated prior work.
- Stop if selected-next state or source-of-truth instructions changed during the task.
- Stop if a force-push, auto-merge, branch-protection edit, or direct protected-branch push is requested.

## Boundary

This packet does not clean branches, change branch protections, merge PRs, or implement branch-pollution controls.
