# Intentional missing-reference exemptions

The exemption rule is narrow:

- A missing reference is exempt when nearby line context explicitly marks it as historical, preserved, a mistake, a wrong path, an old path, a non-action, not created, were not created, absent by statement, intentionally absent, or deferred.
- A small path-level allowlist covers preserved #476 gate-path incident records where the old `...-release-closeout` path is recorded as source evidence or checker input, including the split-line cases where the context is not on the same line as the path.

Known intentional classes:

1. The #476 historical wrong-path / mistake record preserves the old `docs/evals/runs/alpha-solver-post-level-3-level-14-self-operator-release-closeout` path as part of the gate-path incident record.
2. The final-status-cli non-action record states that `docs/evals/runs/alpha-solver-post-level-3-level-14-self-operator-final-status-cli/` was not created.

These records are not evidence of missing active packets. Ordinary missing packet-directory references without explicit historical or non-action context are still reported.
