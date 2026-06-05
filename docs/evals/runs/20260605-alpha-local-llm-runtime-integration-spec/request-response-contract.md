# Request and Response Contract

Lane ID: `ALPHA-LOCAL-LLM-RUNTIME-INTEGRATION-SPEC-001`

## Request construction

A future implementation must preserve the existing adapter contract shape as the starting point for local LLM requests:

- a system message derived from the portable contract;
- a user message containing the operator/request prompt;
- local provider metadata marking the path as local LLM;
- `behavior_evidence=false`.

## Local provider payload

A future implementation may map the adapter request to a local service payload, such as a chat-style payload with:

- model identifier;
- ordered messages;
- streaming disabled unless a later lane specifies streaming behavior;
- finite timeout supplied by configuration.

## Response parsing

A future implementation must parse only the expected assistant-content field for the configured local service response. The parser must fail closed for missing, malformed, non-string, or empty assistant output.

## Echo rejection

The implementation must fail closed when local output is a prompt echo or system echo. Echo checks must compare against the request prompt and the system content sufficiently to prevent presenting echoed input as generated output.

## Output classification

Successful local adapter output remains non-evidence for this phase. It must not be promoted to behavior evidence, runtime readiness evidence, model quality evidence, MVP validation, benchmark evidence, production readiness, provider orchestration evidence, or Alpha superiority evidence.
