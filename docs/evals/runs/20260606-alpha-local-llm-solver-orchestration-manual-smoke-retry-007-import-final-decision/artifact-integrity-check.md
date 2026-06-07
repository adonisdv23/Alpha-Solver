# Artifact integrity check

| Check | Result |
|---|---|
| source artifact folder exists | confirmed |
| manual-smoke-redacted-output.json exists and is parseable JSON | confirmed |
| command-provenance.txt exists | confirmed |
| python-script-provenance.json exists | confirmed |
| manual-smoke-command.sh exists | confirmed |
| manual-smoke-runner.py exists | confirmed |
| manual-smoke-runner.exit-status.txt exists | confirmed |
| manual-smoke-runner.stdout.txt exists | confirmed |
| manual-smoke-runner.stderr.txt exists | confirmed |
| repo-status.txt exists | confirmed |
| exit status is 0 | confirmed |
| result count is 5 | confirmed |
| every prompt record has outer status completed | confirmed |
| every prompt record has error null | confirmed |
| repo head is recorded | confirmed |
| script checksum is recorded | confirmed |
| command provenance is recorded | confirmed |
| provider key presence booleans are all false | confirmed |
| no full environment dump is present | confirmed |
| endpoint summary is loopback | confirmed |
| model is qwen2.5:3b | confirmed |
| timeout is 60 | confirmed |
| behavior_evidence is false | confirmed |
| no_hosted_fallback is true | confirmed |
| no_provider_keys_required is true | confirmed |

## Integrity conclusion

Artifact integrity is complete for interpretation: the source folder and required files are present, the primary JSON is parseable, the runner exit status is `0`, five result records are present, all outer statuses are `completed`, all outer errors are `null`, provenance is recorded, provider key presence booleans are all `false`, the endpoint summary is loopback, model is `qwen2.5:3b`, timeout is `60`, and local non-evidence/no-fallback/no-provider-key boundaries are preserved.

Exit status `0` is interpreted only as evidence that the smoke runner completed and captured output. It is not interpreted as evidence that all expected prompt outcomes passed.
