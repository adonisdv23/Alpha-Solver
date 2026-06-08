# Required Tests Before Code

Before any Self Operator runtime code is modified in a future lane, the operator-supervised implementation lane must run and record the checks below.

## Required static checks

- `git status --short` to prove the starting worktree state.
- `git diff --name-only` to prove no unexpected tracked files are already modified.
- `git diff --check` to detect whitespace errors in any prepared changes.
- `make check-local-llm-orchestration-guardrails` to confirm existing local orchestration guardrails before editing.
- A packet consistency check for the implementation packet or authorization packet that will govern the change.

## Required local harness checks

The future lane must identify the exact local harness command before code changes. The command must use only dry-run, fake transport, fixtures, local temporary directories, or local-only disabled-by-default execution.

The local harness plan must prove:

- no provider calls are possible;
- no browser automation is possible;
- no credentials are required or read;
- no deployment is possible;
- no billing is possible;
- no autonomous merge is possible;
- no `/v1/solve` or dashboard exposure is possible;
- no evidence promotion is possible.

## Required pre-code artifact capture

Before code changes, the future lane must capture:

- command lines run;
- exit statuses;
- relevant stdout/stderr summaries;
- changed-file baseline;
- local-only boundary statement;
- operator approval statement.
