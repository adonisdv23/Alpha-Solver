# Required Artifacts

Any future implementation run derived from this plan must capture raw artifacts and reviewer notes. This packet does not create artifacts and does not run anything.

## Required raw artifacts

For each future implementation run, the lane must capture:

- The exact command lines run.
- Raw stdout and stderr captures for each command.
- Exit statuses for each command.
- The staged and unstaged diff state (`git status --short`, `git diff --name-only`, `git diff --name-only --cached`, `git diff --check`, `git diff --cached --check`).
- The changed-file baseline and the final changed-file set.
- A local-only boundary statement confirming no provider calls, no hosted model calls, no external API calls, no credentials, no browser automation, no deployment, no billing, no route exposure, no fallback, and no evidence promotion.

## Required reviewer notes

Each future implementation run must include reviewer notes that record:

- The operator who approved and supervised the run.
- The exact lane approved and its allowed scope.
- Confirmation that the run stayed within the approved scope.
- Any stop conditions encountered and how they were handled.
- A statement that no secrets or credential values were captured in any artifact.

## Artifact boundary

Artifacts must remain local and inspectable. Artifacts must not be promoted into product, readiness, benchmark, or score evidence. Capturing raw artifacts and reviewer notes is not evidence promotion and does not authorize any further lane.
