# Artifact Integrity Check

## Mechanical checks

| Check | Result | Evidence |
| --- | --- | --- |
| Source artifact folder exists | Pass | Directory is present in repo |
| `manual-smoke-redacted-output.json` exists | Pass | File is present |
| `manual-smoke-redacted-output.json` is parseable JSON | Pass | `jq .` completed successfully |
| `command-provenance.txt` exists | Pass | File is present |
| `python-script-provenance.json` exists | Pass | File is present and parseable |
| `manual-smoke-command.sh` exists | Pass | File is present |
| `manual-smoke-runner.py` exists | Pass | File is present |
| `manual-smoke-runner.exit-status.txt` exists | Pass | File is present |
| `manual-smoke-runner.stdout.txt` exists | Pass | File is present |
| `manual-smoke-runner.stderr.txt` exists | Pass | File is present |
| `repo-status.txt` exists | Pass | File is present |
| Exit status is `0` | Pass | Exit status file contains `0` |
| Result count is `5` | Pass | JSON `results` length is `5` |
| Every prompt record has outer status `completed` | Pass | All five result wrappers have `status: completed` |
| Every prompt record has `error: null` | Pass | All five result wrappers have `error: null` |
| Repo head is recorded | Pass | `repo_head.stdout` records `e8b6b5aba3d1338b15893319702781e4d4070a8a` |
| Script checksum is recorded | Pass | `python_script_provenance.sha256` is present |
| Command provenance is recorded | Pass | `command_provenance` object and `command-provenance.txt` are present |
| Provider key presence booleans are all `false` | Pass | All five recorded key-presence values are `false` |
| No full environment dump is present | Pass | Provenance states no full environment dump was captured and includes only safe env summary |
| Endpoint summary is loopback | Pass | `local_endpoint_summary` and safe env endpoint summary are `http://127.0.0.1:<PORT>/<PATH>` |
| Model is `qwen2.5:3b` | Pass | JSON `model` is `qwen2.5:3b` |
| Timeout is `60` | Pass | JSON `timeout` is `60`; per-result metadata records `60.0` |
| `behavior_evidence` is `false` | Pass | Top-level and per-result fields preserve `false` |
| `no_hosted_fallback` is `true` | Pass | Top-level and per-result fields preserve `true` |
| `no_provider_keys_required` is `true` | Pass | Top-level and per-result fields preserve `true` |

## Integrity conclusion

The preserved artifact is complete enough to support interpretation. The final decision is therefore not blocked or incomplete. Exit status `0` is interpreted only as evidence that the smoke runner completed and captured outputs; it is not interpreted as a pass of expected smoke behavior.
