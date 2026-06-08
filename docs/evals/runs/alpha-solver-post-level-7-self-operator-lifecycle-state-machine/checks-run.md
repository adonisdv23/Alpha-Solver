# Checks Run

This file records the required checks for the docs-only Self Operator lifecycle state-machine packet.

## Required checks

- `git status --short`
- `git diff --name-only`
- `git diff --check`
- `make check-local-llm-orchestration-guardrails`
- `python scripts/check_local_llm_packet_consistency.py docs/evals/runs/alpha-solver-post-level-7-self-operator-lifecycle-state-machine`
- Confirm changed files are only under the new packet directory.

## Checks executed for this PR

Recorded after final local verification.

- PASS: `git status --short` showed only the new docs-only packet directory before staging.
- PASS: `git diff --name-only` produced no tracked-file modifications before staging because all changes were new untracked docs files.
- PASS: `git diff --check` reported no whitespace errors for tracked unstaged changes.
- PASS: `make check-local-llm-orchestration-guardrails` passed.
- PASS: `python scripts/check_local_llm_packet_consistency.py docs/evals/runs/alpha-solver-post-level-7-self-operator-lifecycle-state-machine` passed.
- PASS: changed-file confirmation listed only files under `docs/evals/runs/alpha-solver-post-level-7-self-operator-lifecycle-state-machine/`.
