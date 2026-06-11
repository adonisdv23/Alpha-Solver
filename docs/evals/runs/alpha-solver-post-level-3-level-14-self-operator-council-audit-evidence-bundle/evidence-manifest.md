# Evidence manifest

The Council should inspect the following exact repository paths. These paths are evidence references, not copied raw private artifacts.

## Primary evidence packets

- PR #480 first supervised-use execution / repair:
  - `docs/evals/runs/alpha-solver-post-level-3-level-14-self-operator-first-supervised-use-packet-repair/`
  - `docs/evals/runs/alpha-solver-post-level-3-level-14-self-operator-first-supervised-use-execution/`
- PR #481 first supervised-use review:
  - `docs/evals/runs/alpha-solver-post-level-3-level-14-self-operator-first-supervised-use-review/`
- PR #482 first-use review step-label correction:
  - `docs/evals/runs/alpha-solver-post-level-3-level-14-self-operator-first-supervised-use-review/`
- PR #483 auditor backlog triage:
  - `docs/evals/runs/alpha-solver-post-level-3-level-14-self-operator-auditor-backlog-triage/`
- PR #484 limited repeatability packet:
  - `docs/evals/runs/alpha-solver-post-level-3-level-14-self-operator-limited-repeatability-packet/`
- PR #485 limited repeatability execution:
  - `docs/evals/runs/alpha-solver-post-level-3-level-14-self-operator-limited-repeatability-execution/`
- PR #486 limited repeatability review:
  - `docs/evals/runs/alpha-solver-post-level-3-level-14-self-operator-limited-repeatability-review/`

## Specific dependency decision files

- `docs/evals/runs/alpha-solver-post-level-3-level-14-self-operator-limited-repeatability-review/review-decision.md`
- `docs/evals/runs/alpha-solver-post-level-3-level-14-self-operator-limited-repeatability-review/selected-next-lane.md`
- `docs/evals/runs/alpha-solver-post-level-3-level-14-self-operator-limited-repeatability-review/checks-run.md`

## Local-path handling

- Repo-relative paths are reviewed-safe provenance references.
- Prior evidence may preserve local artifact roots or command logs. Council seats must treat them as provenance evidence and must not request or expose private machine details beyond the repository evidence.
- Any raw artifact that appears unredacted, secret-bearing, billing-related, credential-bearing, or unrelated must be recorded as a defect rather than copied into a response.
