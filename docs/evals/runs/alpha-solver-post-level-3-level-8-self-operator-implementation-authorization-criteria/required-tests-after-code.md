# Required Tests After Code

After any separately authorized first Self Operator runtime code change, the future lane must run focused checks that prove the implementation remains local-only, supervised, and non-promotional.

## Required post-code static checks

- `git status --short` to show the final modified file set.
- `git diff --name-only` to prove the change is limited to the separately approved scope.
- `git diff --check` to prove whitespace correctness.
- `make check-local-llm-orchestration-guardrails` to prove guardrails still pass.
- The relevant packet consistency check.
- Focused unit/static tests for any changed module, guardrail, CLI, harness, artifact writer, or dry-run planner.

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
