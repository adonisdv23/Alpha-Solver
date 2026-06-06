# Artifact Integrity Check

## Required file presence and parseability

| Check | Result | Evidence |
| --- | --- | --- |
| Source artifact folder exists | PASS | `docs/evals/runs/20260606-alpha-local-llm-solver-orchestration-manual-smoke-source-artifact-qwen25-3b/` is present. |
| `manual-smoke-redacted-output.json` exists | PASS | File is present. |
| `manual-smoke-redacted-output.json` is parseable JSON | PASS | Parsed successfully with Python `json.loads`. |
| `command-provenance.txt` exists | PASS | File is present. |
| `python-script-provenance.json` exists | PASS | File is present. |
| `manual-smoke-command.sh` exists | PASS | File is present. |
| `manual-smoke-runner.py` exists | PASS | File is present. |
| `manual-smoke-runner.exit-status.txt` exists | PASS | File is present. |
| `manual-smoke-runner.stdout.txt` exists | PASS | File is present. |
| `manual-smoke-runner.stderr.txt` exists | PASS | File is present. |
| `repo-status.txt` exists | PASS | File is present. |

## Required artifact facts

| Check | Result | Recorded value |
| --- | --- | --- |
| Exit status is `0` | PASS | `0` |
| `result_count` is `5` | PASS | stdout records `"result_count": 5`; JSON contains five results. |
| Repo head is recorded | PASS | `173abd2a36aa981cac1d1b4c169f085069c158f5` |
| Script checksum is recorded | PASS | `c7d9bc8b2e6de71adb885b7e5f9f4e180db5626c7455bcb55a7608d4d465a412` |
| Command provenance is recorded | PASS | `command_provenance` object and `command-provenance.txt` are present. |
| Provider key presence booleans are all false | PASS | All five recorded provider keys are `false`. |
| No full environment dump is present | PASS | Provenance note says no full environment dump was captured; artifact contains only safe environment summaries. |
| Endpoint summary is loopback | PASS | `http://127.0.0.1:<PORT>/<PATH>` |
| Model is `qwen2.5:3b` | PASS | `qwen2.5:3b` |
| Timeout is `60` | PASS | `60` top-level, `60.0` in result metadata. |
| `behavior_evidence` is `false` | PASS | `false` |
| `no_hosted_fallback` is `true` | PASS | `true` |
| `no_provider_keys_required` is `true` | PASS | `true` |

## Integrity conclusion

The preserved artifact is complete and interpretable for the purposes of this lane. Because required artifact and provenance checks pass, the final decision is not blocked or incomplete. Prompt behavior interpretation is recorded separately and determines whether the smoke passes or fails.
