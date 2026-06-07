# Artifact Integrity Review

## Source artifact directory

`docs/evals/runs/20260607-local-llm-controlled-usage-operator-run-001/source-artifact/`

## Preserved files reviewed

- `README.md`
- `controlled_usage_prompt.txt`
- `executed_command.txt`
- `run_metadata.txt`
- `exit_code.txt`
- `cli_stdout.json`
- `cli_stderr.txt`
- `run_controlled_usage.sh`

## Integrity findings

- The source artifact directory exists.
- `exit_code.txt` records `0`.
- `cli_stdout.json` is parseable JSON.
- `cli_stdout.json` records `status=ok`.
- `cli_stdout.json` records `behavior_evidence=false`.
- `cli_stdout.json` records `no_hosted_fallback=true`.
- `cli_stdout.json` records `no_provider_keys_required=true`.
- `cli_stdout.json` metadata includes loopback/local endpoint handling, including `endpoint_host_label=loopback` and `endpoint_is_loopback=true`.
- `cli_stderr.txt` is preserved as a source artifact.
- `executed_command.txt` preserves the operator CLI command.
- `run_metadata.txt` preserves repo head, repo status boundaries, command identity, and artifact directory.
- The artifact is bounded as Level 2 local operator usability output only.

## Completeness determination

The artifact is complete enough for interpretation in this import/final-decision lane.
