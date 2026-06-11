# Manual Council runbook

This runbook is for the future operator. This lane did not run the Council.

## Setup

1. Open a fresh GPT chat for each auditor seat.
2. Provide `prompts/00-common-instructions.md` and exactly one seat prompt to that chat.
3. Provide repo evidence by pasting or attaching only the packet files listed in `evidence-manifest.md`, subject to redaction rules.
4. Do not authorize any prohibited action.
5. Capture each response in the format from `council-response-capture-template.md`.
6. After all non-synthesis seats are captured, open a separate synthesis chat using `prompts/08-synthesis-judge.md` plus the captured seat outputs.

## Hard stops

Stop the manual Council run if any chat asks for provider calls outside the GPT chat itself, hosted model calls beyond the operator's manual chat session, local model calls, external APIs, browser automation, deployment, billing, credential access, secret access, `/v1/solve` exposure, dashboard exposure, source-artifact mutation, evidence promotion, or readiness claims.

## Expected state before starting

- Council has run: no.
- Manual review has happened: no.
- Final status CLI implemented: no.
- Readiness claimed: no.
