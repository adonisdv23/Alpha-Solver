# Raw output index

Every raw artifact below the output root
(`/tmp/alpha-solver-self-operator-first-supervised-use-execution-001`)
at the end of the run, with SHA-256 checksums. The raw root is preserved
unmodified (at minimum until this lane's PR is merged) and is never
committed; the repository carries only the redacted copies under
`imported-artifacts/`, which passed the pre-import review in
`redaction-record.md` and are byte-identical to the reviewed raws (the
review required no edits).

| Raw artifact (relative to root) | SHA-256 | Imported copy |
| --- | --- | --- |
| `checks/commands-run.txt` | `7ac27167647422093ae2c8a36d77efb4065406184ab0f7020825502766793d49` | `imported-artifacts/checks/commands-run.txt` |
| `checks/consistency-check.stdout.txt` | `4b066604d135d8b8027946fae4c9bb75d20d2620f23fd59ea384efac8cc2c961` | `imported-artifacts/checks/consistency-check.stdout.txt` |
| `checks/release-gate-check.json` | `a17e7ae2214c6839a9bf45ef1936b4abb2bf878cb3ef277b0053ffbaf56b4c5d` | `imported-artifacts/checks/release-gate-check.json` |
| `checks/release-gate-check.stdout.txt` | `73159f777592c79ce9b44e85da9ab905cbcaa292ddf7a5f9208795efadd7811a` | `imported-artifacts/checks/release-gate-check.stdout.txt` |
| `dry-run-result.json` | `5a62903ef60809b715e16660c1c09449ffb45ec110ae724d45e26fff7f8127ad` | `imported-artifacts/dry-run-result.json` |
| `execution-gate-result.json` | `7f93555c21907dc98faca54cd1be3c0ef4f29d8e9e4fe28a9a6f8c04ba366b60` | `imported-artifacts/execution-gate-result.json` |
| `inputs/approval-record.json` | `1a9bf846b1170d6f464556ad34fade24ed09a4b0c7ba4626f960a9052d8b4a29` | `imported-artifacts/inputs/approval-record.json` |
| `inputs/proposed-task.json` | `189f3ce16206c54d964a92f2c3d41f06b1116fe8f6dbb48d3bed3d91dbba1c3b` | `imported-artifacts/inputs/proposed-task.json` |
| `notes/operator-log.md` | `06a973cd4bf20ab732279e1d21d05b411c12b536df502b2e0f1ed7723266e16c` | `imported-artifacts/notes/operator-log.md` |
| `notes/run-end-utc.txt` | `5c72d734ffed1a77b4d4cff9893cf8a1394ad1e5b130b20b3bc7b5444191fbc2` | `imported-artifacts/notes/run-end-utc.txt` |
| `notes/run-start-utc.txt` | `3bea36587259d7e5c0734069cdebb2dc99770945522eb25dae064ee40b6632cf` | `imported-artifacts/notes/run-start-utc.txt` |

Pipeline artifacts (`dry-run-result.json`, `execution-gate-result.json`)
were written by the wrapper through the artifact store
(`resolve_artifact_path` + `write_artifact_json`, `overwrite` never
passed). `stop-state.json` does not exist because no stop state
occurred (`stop-state-record.md`).
