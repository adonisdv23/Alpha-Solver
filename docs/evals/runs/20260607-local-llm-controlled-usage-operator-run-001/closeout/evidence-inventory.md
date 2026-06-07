# Evidence Inventory

## Source artifact packet

Preserved source artifact location:

`docs/evals/runs/20260607-local-llm-controlled-usage-operator-run-001/source-artifact/`

Expected preserved files:

- `README.md`
- `cli_stderr.txt`
- `cli_stdout.json`
- `controlled_usage_prompt.txt`
- `executed_command.txt`
- `exit_code.txt`
- `run_controlled_usage.sh`
- `run_metadata.txt`

## Import/final-decision packet

Import/final-decision location:

`docs/evals/runs/20260607-local-llm-controlled-usage-operator-run-001/import-final-decision/`

The import/final-decision packet records the final accepted decision, accepted facts, field review, artifact summary, evidence boundary, blocked claims, selected next lane, blocker fallback lane, and checks run.

## Closeout handling

This closeout packet does not modify the source artifact packet and does not modify the import/final-decision packet. It records the accepted outcome from the import/final-decision packet without rerun or reinterpretation.
