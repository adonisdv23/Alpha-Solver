# Source Artifact Preservation Plan

The exact Mac command writes retry 007 source artifacts to:

`docs/evals/runs/20260606-alpha-local-llm-solver-orchestration-manual-smoke-retry-007-source-artifact-qwen25-3b-after-diagnostic-router-reset/`

## Expected future artifact files

The generated command should preserve, at minimum:

- `manual-smoke-command.sh`;
- `manual-smoke-runner.py`;
- `manual-smoke-runner.stdout.txt`;
- `manual-smoke-runner.stderr.txt`;
- `manual-smoke-runner.exit-status.txt`;
- `manual-smoke-redacted-output.json`;
- command provenance, Python script provenance/checksum, and repo status artifacts produced by the inherited runner script.

## Preservation rule

This operator packet does not create or commit the source artifact directory. After Adonis runs the command locally, a later source artifact preservation step should preserve the generated directory exactly as produced, subject only to the established redaction boundary.

## Interpretation rule

Do not import, interpret, repair, or make a final decision from retry 007 in this packet. The future artifact should be interpreted only by a later authorized import/final-decision lane.
