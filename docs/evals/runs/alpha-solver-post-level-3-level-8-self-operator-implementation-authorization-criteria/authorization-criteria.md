# Authorization Criteria

Before any Self Operator runtime code can be modified, all criteria below must be true and documented in the future implementation lane.

## Required conditions

1. **Local-only execution:** The implementation must run only on the operator's local machine or local test environment.
2. **Operator-supervised operation:** Every execution must be started, observed, and stopped by a human operator.
3. **No provider calls:** The implementation must not call hosted LLM providers, provider adapters, hosted APIs, paid APIs, fallback providers, or remote inference services.
4. **No browser automation:** The implementation must not drive browsers, browser extensions, web pages, DOM actions, login flows, scraping sessions, or remote UI automation.
5. **No credentials:** The implementation must not create, request, read, write, validate, persist, rotate, display, log, transmit, or require credentials, API keys, tokens, cookies, secrets, or service account material.
6. **No deployment:** The implementation must not deploy, publish, push images, change infrastructure, change Cloud Run, modify production settings, or alter release configuration.
7. **No billing:** The implementation must not create spend, enable spend, integrate billing meters, call paid services, add paid-provider fallback, or modify budget enforcement.
8. **No autonomous merges:** The implementation must not merge, squash, rebase shared branches, approve pull requests, or perform unattended repository write operations outside the operator-approved local branch.
9. **No `/v1/solve` or dashboard exposure:** The implementation must not expose Self Operator behavior through `/v1/solve`, API routes, dashboard routes, UI controls, product surfaces, public endpoints, or remote services.
10. **No evidence promotion:** The implementation must not mark generated artifacts as production evidence, benchmark evidence, acceptance evidence, behavior evidence, or promoted evaluation evidence.
11. **Static tests required:** The future lane must identify and run static guardrail checks before and after the code change.
12. **Local harness tests required:** The future lane must identify and run local harness tests that exercise only fake, fixture, dry-run, or local-only paths.
13. **Artifact capture required:** The future lane must capture local artifacts that prove command, config, stdout/stderr or structured output, exit status, and boundary compliance without storing secrets.

## Authorization rule

Implementation is authorized only if all required conditions are true at the same time. If any condition is false, ambiguous, untested, or unverifiable, Self Operator runtime code must not be modified and the blocker fallback lane must be selected instead.
