# Required Tests After Code

After any separately authorized first Self Operator runtime code change, the future lane must run focused checks that prove the implementation remains local-only, supervised, and non-promotional.

## Required post-code static checks

- `git status --short` to show the final modified file set.
- `git diff --name-only` to prove the unstaged changed-file scope is limited to the separately approved scope.
- `git diff --cached --name-only` to prove the staged changed-file scope is limited to the separately approved scope.
- `git diff --check` to prove unstaged whitespace correctness.
- `git diff --cached --check` to prove staged whitespace correctness.
- `make check-local-llm-orchestration-guardrails` to prove guardrails still pass.
- The relevant packet consistency check.
- Focused unit/static tests for any changed module, guardrail, CLI, harness, artifact writer, or dry-run planner.

## Required final scope proof

Before commit and before PR creation, the future implementation lane must prove the final changed-file scope using both unstaged and staged diff forms:

- `git diff --name-only`
- `git diff --cached --name-only`
- `git diff --check`
- `git diff --cached --check`

Bare `git diff` checks unstaged changes only. `git diff --cached` checks staged changes only. Both forms are required because staged out-of-scope files could otherwise bypass final scope proof when only bare `git diff` commands are reviewed.

If either the unstaged or staged diff form shows files outside the separately approved scope, the lane must stop before commit and PR creation.

## Required post-code local harness tests

The future lane must run local harness tests that exercise:

- default-disabled behavior;
- explicit operator-supervised enablement;
- fake-transport or dry-run execution;
- artifact capture;
- fail-closed behavior when forbidden capability flags or configuration are requested;
- absence of provider calls;
- absence of browser automation;
- absence of credential access;
- absence of deployment, billing, autonomous merge, `/v1/solve`, dashboard exposure, and evidence promotion.

## Required post-code artifact capture

The future lane must preserve artifacts that include:

- exact commands;
- exit statuses;
- stdout/stderr or structured local output;
- generated artifact paths;
- boundary compliance summary;
- operator review notes;
- proof that no secrets are captured.
