# Smoke Runbook Template

## Non-Execution Notice

This scaffold is blocked until a future implementation PR creates a local solver orchestration runner. It is scaffold-only and is not runtime evidence. It does not execute a local LLM, does not call hosted providers, does not import results, and does not close any track.

## Future Smoke Target

The future smoke target is a local orchestration runner that exercises a local expert two-pass path in non-production execution only.

The target must preserve these constraints:

- No `/v1/solve` exposure.
- No dashboard exposure.
- No hosted fallback.
- No provider keys.
- Local endpoint only.
- Local model only.

## Future Operator Placeholders

- Date executed: `<YYYY-MM-DD>`
- Operator: `<operator>`
- Repo root: `<REPO_ROOT>`
- Implementation PR: `<future PR number>`
- Runner command: `<future local orchestration runner command>`
- Local endpoint summary: `<scheme://local-host-placeholder:port/path summary only>`
- Model: `<local model identifier>`
- Timeout: `<timeout seconds>`

## Future Steps

1. Confirm the prerequisite gates.
2. Confirm the runner exists and is non-production only.
3. Confirm no provider keys are required.
4. Confirm hosted fallback is disabled or absent.
5. Run the future smoke prompt set only after implementation exists.
6. Capture artifacts using `artifact-capture-template.md`.
7. Record each prompt outcome in `smoke-result-log-template.md`.
8. Interpret outcomes using `interpretation-template.md`.
9. Record a final decision using `final-decision-template.md`.

## Stop Conditions

Stop without execution if any of the following are true:

- The implementation runner is missing.
- The endpoint is not local.
- A hosted fallback is present.
- Provider keys are required.
- The run would expose `/v1/solve`.
- The run would expose dashboard behavior.
