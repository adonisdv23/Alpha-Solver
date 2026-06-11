# Output root

A future repeatability execution lane must use a fresh output root outside the
repository.

Required output root pattern:

```text
/tmp/alpha-solver-self-operator-limited-repeatability/<fresh-run-id>/
```

Required fresh run ID pattern:

```text
self-operator-limited-repeatability-001-run-YYYYMMDDTHHMMSSZ
```

The output root must be empty or newly created at the start of execution. The
future lane must record the absolute output root in its execution evidence. No
run artifact may be written inside the repository during execution.
