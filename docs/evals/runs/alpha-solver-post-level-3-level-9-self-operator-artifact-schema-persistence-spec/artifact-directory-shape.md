# Artifact directory shape

Future artifacts, if authorized by a later code lane, should be local-only and isolated under a dedicated unpromoted run directory. A proposed shape is:

```text
.self_operator_runs/<run_id>/
  metadata.json
  confirmation-record.json
  command-records.jsonl
  stop-state.json
  review-notes.md
```

No future lane may write this shape unless explicitly authorized. This packet only documents the shape.
