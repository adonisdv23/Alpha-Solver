# Checks Run

This file records checks for the docs-only future Self Operator operator runbook draft packet.

## Required checks

- `git status --short`
- `git diff --name-only`
- `git diff --check`
- `make check-local-llm-orchestration-guardrails`
- `python scripts/check_local_llm_packet_consistency.py docs/evals/runs/alpha-solver-post-level-7-self-operator-operator-runbook-draft`
- Confirm changed files are only under the new packet directory.

## Evidence boundary

These checks are static repository checks. They do not implement Self Operator, run Self Operator, run models, call providers, deploy, expose routes, or promote evidence.

## Results

Results are recorded after command execution in the PR summary and final response.

## Checks executed for this PR

- PASS: `git status --short` showed only the new docs-only packet directory as untracked before staging.
- PASS: `git diff --name-only` produced no tracked-file output before staging; changed-file scope was confirmed with `git status --short` because the packet files were newly untracked.
- PASS: `git diff --check` produced no whitespace errors.
- PASS: `make check-local-llm-orchestration-guardrails` passed static local LLM evidence-boundary, doc path/link, and packet consistency checks.
- PASS: `python scripts/check_local_llm_packet_consistency.py docs/evals/runs/alpha-solver-post-level-7-self-operator-operator-runbook-draft` passed for this packet directory.
- PASS: changed files were confirmed to be only under `docs/evals/runs/alpha-solver-post-level-7-self-operator-operator-runbook-draft/`.
