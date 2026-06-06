# Target Integration Surface

## First target

The first implementation target is a non-production local orchestration runner, not `/v1/solve`.

## Allowed capabilities

The runner can:

- call the local LLM runtime backend;
- wrap outputs in an Alpha-style envelope;
- preserve local runtime metadata;
- run bounded expert-style passes;
- run local confidence, clarify, or block decisions where possible;
- fail closed on runtime errors;
- preserve evidence boundaries.

## Blocked surfaces

The runner must not be exposed through production `/v1/solve` or dashboard preview. Those surfaces require separate approval after this non-production runner contract is implemented and reviewed.
