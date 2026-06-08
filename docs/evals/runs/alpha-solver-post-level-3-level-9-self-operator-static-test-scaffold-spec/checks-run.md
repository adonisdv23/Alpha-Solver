# Checks run

## Required preflight verification

Confirmed the required existing packet directories and files are present before creating this docs-only packet.

## Required checks for the combined PR

The combined PR must record these commands after all six packets are created:

- `git status --short`
- `git diff --name-only`
- `git diff --cached --name-only`
- `git diff --check`
- `git diff --cached --check`
- `make check-local-llm-orchestration-guardrails`
- `python scripts/check_local_llm_packet_consistency.py docs/evals/runs/alpha-solver-post-level-3-level-9-self-operator-code-file-map-ownership`
- `python scripts/check_local_llm_packet_consistency.py docs/evals/runs/alpha-solver-post-level-3-level-9-self-operator-static-test-scaffold-spec`
- `python scripts/check_local_llm_packet_consistency.py docs/evals/runs/alpha-solver-post-level-3-level-9-self-operator-artifact-schema-persistence-spec`
- `python scripts/check_local_llm_packet_consistency.py docs/evals/runs/alpha-solver-post-level-3-level-9-self-operator-local-preflight-runner-spec`
- `python scripts/check_local_llm_packet_consistency.py docs/evals/runs/alpha-solver-post-level-3-level-9-self-operator-approval-stopstate-spec`
- `python scripts/check_local_llm_packet_consistency.py docs/evals/runs/alpha-solver-post-level-3-level-9-self-operator-level-10-code-prompt-pack`

## Scope confirmation

Before PR creation, run `git diff --name-only` and confirm every changed file is under one of the six allowed new Level 9 Self Operator support/spec packet directories.
