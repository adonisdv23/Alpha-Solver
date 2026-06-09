# MLA-007 raw artifacts

- Task ID: `MLA-007`
- Expected artifact list: `dry-run-result.json, execution-gate-result.json, stop-state.json` unless the wrapper rejected before write.
- Produced artifact list: `dry-run-result.json, execution-gate-result.json`
- Status: `PASS`
- Notes: initial dry_run_status=ready_for_operator_supervised_local_dry_run; second invocation blocked with ArtifactStoreError: artifact already exists and overwrite is false: execution-gate-result.json No readiness interpretation is made.

## Checksum list

- `dry-run-result.json`: `6681ee4cd065c458f756b32e4056e0a939592c9be4673a32ce0d0e4815baf151`
- `execution-gate-result.json`: `ea1399695a88465b8b542cc3dcb44eaa7235f594774af1f9c7a9a224c754550e`
## Packet-consistency marker

This raw-artifact subdirectory is closed for packet-consistency discovery only. No follow-on lane is started from this raw-artifact subdirectory.
