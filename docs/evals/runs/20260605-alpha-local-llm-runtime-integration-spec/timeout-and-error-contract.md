# Timeout and Error Contract

Lane ID: `ALPHA-LOCAL-LLM-RUNTIME-INTEGRATION-SPEC-001`

## Finite timeout

Every future local LLM call must use a finite timeout. Unbounded requests are prohibited.

The implementation must reject missing, non-numeric, zero, negative, infinite, or otherwise invalid timeout values for local LLM mode.

## Required fail-closed cases

A future implementation must fail closed for:

1. non-local endpoint;
2. malformed endpoint;
3. connection failure;
4. timeout;
5. malformed response;
6. empty output;
7. prompt echo;
8. system echo.

## Fail-closed semantics

Fail-closed means:

- stop the local LLM path;
- return or record a bounded local LLM failure outcome;
- do not make a hosted-provider call unless separately authorized by a later lane;
- do not present failed or echoed output as successful local behavior;
- preserve `behavior_evidence=false`.

## Error labels

A future implementation must use deterministic reason labels that distinguish endpoint rejection, connection failure, timeout, malformed response, empty output, prompt echo, and system echo. Labels may be refined during implementation, but they must remain observable in tests and smoke artifacts.
