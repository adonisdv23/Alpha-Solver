# Required Tests

A future operator-only MVP release claim requires recorded passing results for all planned tests in this file.

## Required passing test categories

- Static documentation and configuration checks proving that the release packet, runbook, approvals, artifact locations, and blocked claims are internally consistent.
- Local-only smoke checks proving that the operator workflow can be exercised without provider calls, browser automation, deployment, production exposure, or autonomous execution.
- Blocked-action checks proving that provider calls, browser automation, deployments, production claims, and autonomous-operation claims remain prohibited by the release boundary.
- Approval-gate checks proving that human operator approval is required and recorded before any closeout claim is made.
- Artifact-preservation checks proving that raw artifacts are retained, named, and linked without destructive transformation.
- Stop-condition checks proving that release closeout stops when a planned test fails, an artifact is missing, an approval is missing, or a blocked action is requested.
- Release-notes checks proving that the notes state operator-only scope and do not claim production, deployment, browser automation, provider access, or autonomous operation.

## Pass condition

Every planned test must pass. A partial pass, skipped release-blocking test, missing test record, missing command output, missing approval check, or unresolved failure blocks release closeout.
