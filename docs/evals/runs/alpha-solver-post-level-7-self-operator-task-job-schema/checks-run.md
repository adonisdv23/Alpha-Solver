# Checks Run

## Required checks

The following checks are required for this docs-only schema packet:

- `git status --short`
- `git diff --name-only`
- `git diff --check`
- `make check-local-llm-orchestration-guardrails`
- `python scripts/check_local_llm_packet_consistency.py docs/evals/runs/alpha-solver-post-level-7-self-operator-task-job-schema`

## Changed-file scope confirmation

Changed files must be only under `docs/evals/runs/alpha-solver-post-level-7-self-operator-task-job-schema/`.

## Evidence-boundary confirmation

Evidence boundary: Docs-only schema design. This does not create database tables, queues, jobs, API routes, dashboard routes, runtime execution, provider calls, or evidence promotion.

## Results

Results are recorded after command execution in the PR summary and final response.

## Execution results

- Pass: `git status --short` showed only the new packet directory as untracked before staging.
- Pass: `git diff --name-only` produced no tracked unstaged file output before staging.
- Pass: `git diff --check` reported no whitespace errors before staging.
- Pass: `make check-local-llm-orchestration-guardrails` completed the evidence-boundary, doc-path, and packet-consistency checks successfully.
- Pass: `python scripts/check_local_llm_packet_consistency.py docs/evals/runs/alpha-solver-post-level-7-self-operator-task-job-schema` passed with one packet directory scanned.
- Pass: changed-file scope was confirmed as limited to `docs/evals/runs/alpha-solver-post-level-7-self-operator-task-job-schema/`.
