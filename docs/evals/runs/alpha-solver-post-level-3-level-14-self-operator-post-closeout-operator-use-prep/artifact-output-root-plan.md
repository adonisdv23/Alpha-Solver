# Artifact output root plan

Where output artifacts of any future supervised use must be written. This
restates the canonical runbook (section 7) and the enforced behavior of
`alpha/self_operator/artifact_store.py`.

## Output root rules

1. The operator supplies an explicit local output root for each run; nothing
   defaults into the repository tree. The root must be outside the
   repository checkout. The accepted #461 execution used
   `/tmp/alpha-solver-operator-supervised-local-acceptance-execution-001`;
   the first supervised use should follow the same pattern with its own lane
   ID and run ID in the directory name.
2. Every artifact write goes through `resolve_artifact_path`, which rejects
   absolute targets outside the root and any path containing `..`
   (`artifact path outside allowed output root`).
3. Existing artifacts are never silently replaced: `write_artifact_json`
   raises unless `overwrite` is explicitly true.
4. Artifacts a run persists below the root: `dry-run-result.json`,
   `execution-gate-result.json`, and `stop-state.json` when stopped.

## Repository-side outputs

- Raw output roots are never committed.
- The future supervised-use lane writes its repository evidence only inside
  its own packet directory under `docs/evals/runs/` (exact directory name
  fixed by that lane's charter), and imports only copied, redacted
  artifacts through its own lane review.
- No other repository location receives outputs from operator use.

## This prep lane's outputs

This lane wrote only the files inside
`docs/evals/runs/alpha-solver-post-level-3-level-14-self-operator-post-closeout-operator-use-prep/`.
Its one transient artifact (the read-only release-gate re-check JSON) was
written to `/tmp` outside the repository and was not committed.
