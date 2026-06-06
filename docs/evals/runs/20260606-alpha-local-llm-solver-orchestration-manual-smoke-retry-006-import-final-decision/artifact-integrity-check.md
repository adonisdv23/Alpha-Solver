# Artifact Integrity Check

## File presence

| Check | Result |
| --- | --- |
| Source artifact folder exists | Pass |
| `manual-smoke-redacted-output.json` exists | Pass |
| `manual-smoke-redacted-output.json` is parseable JSON | Pass |
| `command-provenance.txt` exists | Pass |
| `python-script-provenance.json` exists | Pass |
| `manual-smoke-command.sh` exists | Pass |
| `manual-smoke-runner.py` exists | Pass |
| `manual-smoke-runner.exit-status.txt` exists | Pass |
| `manual-smoke-runner.stdout.txt` exists | Pass |
| `manual-smoke-runner.stderr.txt` exists | Pass |
| `repo-status.txt` exists | Pass |

## Execution and record integrity

| Check | Observed value | Result |
| --- | --- | --- |
| Exit status | `0` | Pass |
| Result count | `5` | Pass |
| Every prompt record outer status | `completed` | Pass |
| Every prompt record error | `null` | Pass |
| Repo head recorded | `7ecb1e8ed60a87c22d3ef3bcb4ca3ed61caa5cd5` | Pass |
| Script checksum recorded | `51b26c6a29431794f86abb47377f1417d9f95cbc2d059b0e8c645b86261b5c9a` | Pass |
| Command provenance recorded | present | Pass |
| Provider key presence booleans | all `false` | Pass |
| Full environment dump | absent; safe summary only | Pass |
| Endpoint summary | `http://127.0.0.1:<PORT>/<PATH>` / loopback | Pass |
| Model | `qwen2.5:3b` | Pass |
| Timeout | `60` | Pass |
| `behavior_evidence` | `false` | Pass |
| `no_hosted_fallback` | `true` | Pass |
| `no_provider_keys_required` | `true` | Pass |

## Integrity conclusion

The artifact is complete enough to support prompt interpretation and final decision selection. Integrity does not imply smoke success; it only means the preserved evidence can be interpreted.
