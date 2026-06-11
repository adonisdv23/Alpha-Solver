# Output root

## Exact output root

The first supervised use writes all run outputs below exactly one local
directory, outside the repository checkout:

```
/tmp/alpha-solver-self-operator-first-supervised-use-execution-001
```

If the execution host requires a different base path, the operator may
substitute another local path outside the repository tree, keeping the
trailing directory name; the substitution must be recorded in the execution
lane's packet before the run.

## Rules

1. The operator creates the root before the run and confirms it is empty
   and writable.
2. Every artifact write goes through
   `alpha.self_operator.artifact_store.resolve_artifact_path`, which rejects
   absolute targets outside the root and any path containing `..`.
3. Existing artifacts are never silently replaced: `write_artifact_json`
   raises unless `overwrite` is explicitly true, and this run never passes
   `overwrite=true`.
4. Checker stdout captures and operator-drafted JSON inputs are also kept
   below this root (see `expected-artifacts.md`).
5. The raw root is never committed. The execution lane imports only copied,
   redacted artifacts into its own packet directory under
   `docs/evals/runs/`, through lane review.
6. After import, the operator preserves the raw root unmodified for the
   retention period the execution lane records (at minimum until that
   lane's PR is merged), then may delete it; it is never retroactively
   edited.

## This packet lane

This lane created no output root and wrote nothing outside
`docs/evals/runs/alpha-solver-post-level-3-level-14-self-operator-first-supervised-use-packet/`.
