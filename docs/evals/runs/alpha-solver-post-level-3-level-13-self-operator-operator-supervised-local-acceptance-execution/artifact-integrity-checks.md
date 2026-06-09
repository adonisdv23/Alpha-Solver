# Artifact integrity checks

| Check | Status | Evidence |
| --- | --- | --- |
| JSON parse status | PASS | All copied JSON artifacts parsed successfully during ledger creation. |
| Checksum status | PASS | SHA-256 checksum recorded for every copied JSON artifact. |
| Schema version presence | PASS | Schema version is present for every copied JSON artifact; no JSON artifacts were produced for MLA-006 path traversal pre-write rejection. |
| Lane ID | PASS | Copied artifacts retain wrapper lane ID `ALPHA-SOLVER-POST-LEVEL-3-LEVEL-12-SELF-OPERATOR-LOCAL-HARNESS-DRY-RUN-WRAPPER-001`; packet lane ID is `ALPHA-SOLVER-POST-LEVEL-3-LEVEL-13-SELF-OPERATOR-OPERATOR-SUPERVISED-LOCAL-ACCEPTANCE-EXECUTION-001`. |
| Run ID | PASS | Run ID is present for every copied JSON artifact. |
| Task ID | PASS | Task IDs are preserved in packet directory paths and dry-run metadata where dry-run-result.json is present. |
| Output-root containment | PASS | Copied artifacts originated under `/tmp/alpha-solver-operator-supervised-local-acceptance-execution-001` task roots or were rejected before write. |
| Redaction status | PASS | Copied artifacts report redaction status or contain redacted summaries; MLA-008 synthetic secret-like value absent. |
| Evidence boundary | PASS | Artifacts and packet docs preserve local-only evidence boundary. |
| Non-execution confirmation | PASS | dry-run-result.json artifacts contain wrapper non-execution confirmation; sentinel check passed for MLA-010. |
| No source-artifact mutation | PASS | Only this new packet directory was written in the repository. |
| No evidence promotion | PASS | No import, interpretation, acceptance promotion, or readiness claim performed. |
