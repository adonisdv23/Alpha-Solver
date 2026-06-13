# Artifacts index

Generated artifacts under `docs/evals/runs/alpha-solver-post-level-3-level-14-self-operator-execution-evidence-002/artifacts/`:

| Artifact | SHA-256 | Schema/version | Status field |
| --- | --- | --- | --- |
| `acceptance-interpretation.json` | `c643f6be3d8cb959c91f5209c8fce792ea370ee1b334fbd5f0724e8042dd223f` | `self_operator.acceptance_interpretation.v1` | `readiness_implication=blocked` |
| `dry-run-result.json` | `484047681786b5f4babaae30cfb44a13ccabd812efa8b3e499229648ce738e2c` | `self_operator.dry_run_result.v1` | `dry_run_status=blocked_by_missing_approval` |
| `execution-gate-result.json` | `3e15f57a6c01906a894556af4535f8385ffec7f12e43305efee2dad9694aab9e` | `self_operator.execution_gate_result.v1` | `gate_status=blocked_by_missing_approval` |
| `result-import-summary.json` | `b79807faebf09bec16508494820b3eca813cb8d1dfcb67ab290e70433d174801` | `self_operator.acceptance_import_summary.v1` | `status=import_ready_with_expected_blocks` |
| `stop-state.json` | `ea09bcd9f8cd23385ad3eb0be35e8a9ce408c0ae5b9907f32681045912604c4a` | `self_operator.stop_state_record.v1` | `stop_state=blocked` |

## Artifact boundary

The artifacts are deterministic local JSON outputs. They do not contain provider responses, model responses, tokens, credentials, external API responses, browser-automation output, deployment output, dashboard exposure, `/v1/solve` exposure, or readiness approval.
