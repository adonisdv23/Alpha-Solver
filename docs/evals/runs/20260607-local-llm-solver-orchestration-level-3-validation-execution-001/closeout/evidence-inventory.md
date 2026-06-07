# Evidence Inventory

## Source artifact packet

Preserved source artifact location:

`docs/evals/runs/20260607-local-llm-solver-orchestration-level-3-validation-execution-001/source-artifact/`

Expected preserved contents include:

- `README.md`
- `file_list.txt`
- `run_level3_validation.sh`
- `run_metadata.txt`
- five frozen prompt files under `prompts/`
- per-case result directories for `L3-FROZEN-TC-001` through `L3-FROZEN-TC-005`
- per-case `executed_command.txt`, `stdout.json`, `stderr.txt`, `exit_code.txt`, `metadata.txt`, `json_review.txt`, `redaction_confirmation.txt`, and `operator_environment_notes.txt`

## Import/final-decision packet

Import/final-decision location:

`docs/evals/runs/20260607-local-llm-solver-orchestration-level-3-validation-execution-001/import-final-decision/`

The import/final-decision packet records the final accepted decision, accepted artifact facts, final accepted evidence boundary, blocked claims, selected next lane, blocker fallback lane, and checks run.

## Closeout handling

This closeout packet does not modify the preserved source artifact packet and does not modify the import/final-decision packet. It records the accepted outcome from the import/final-decision packet without rerun, reinterpretation, broadening, or evidence promotion.
