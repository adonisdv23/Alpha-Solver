# Artifact output root

## Exact root used

```
/tmp/alpha-solver-self-operator-first-supervised-use-execution-001
```

Exactly the root defined in the first-use packet's `output-root.md`; no
substitution was needed. Before the run it did not exist; it was created
empty, confirmed writable (probe file created and removed), and confirmed
outside the repository checkout.

## Root rules honored (per `output-root.md`)

1. Created before the run, empty and writable — confirmed and recorded in
   `commands-run.md`.
2. Every pipeline artifact write went through
   `alpha.self_operator.artifact_store.resolve_artifact_path` (the wrapper's
   only write path), which rejects absolute targets outside the root and
   any path containing `..`.
3. `overwrite=true` was never passed; no artifact was replaced.
4. Checker stdout captures, the release-gate JSON, the drafted operator
   inputs, the command record, and the operator log were all kept below
   this root (see `raw-output-index.md`).
5. The raw root was not committed. Only copied, redacted artifacts were
   imported into this packet directory (`imported-artifacts/`), after the
   review in `redaction-record.md`.
6. The raw root is preserved unmodified for the retention period: at
   minimum until this lane's PR is merged. It is never retroactively
   edited.
