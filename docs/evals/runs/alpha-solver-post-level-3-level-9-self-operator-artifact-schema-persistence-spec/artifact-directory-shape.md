# Artifact directory shape

Future artifacts must be local-only and written only under a lane-authorized local run directory. Planning shape:

```text
self-operator-run-<timestamp>/
  metadata.json
  confirmation-record.json
  commands.jsonl
  stop-state.json
  review-notes.md
  redactions.md
  raw/
    static-test-output.txt
    diff-proof.txt
```

No artifact path may be a source-artifact directory or evidence-promotion target.
