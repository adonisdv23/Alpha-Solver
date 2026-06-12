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


## Post-#490 verification annex amendment

A post-#490 verification annex has been added at `docs/evals/runs/alpha-solver-post-level-3-level-14-self-operator-council-audit-evidence-bundle/verification-annex/` and mirrored by the lane packet at `docs/evals/runs/alpha-solver-post-level-3-level-14-self-operator-council-bundle-verification-annex/`. It records the verified #480 through #490 PR chain, #488 AUDIT-005 routing/wording fix, #489 checker-scope extension, #490 directory reference gap fix, current checker coverage, D-1 through D-5 caveats, CI evidence, and self-attestation/review-independence notes.

Council has not run. Manual operator review has not happened. Targeted Fable delta re-audit has not run in this lane. No readiness claim is made by this amendment.
