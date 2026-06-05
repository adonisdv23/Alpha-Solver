# Timeout and Fail-Closed Requirements

This is a scaffold only. Local LLM runtime integration is not implemented here.

## Finite timeout requirement

Any future local LLM runtime call must use a finite timeout. Unbounded calls are prohibited.

## Required fail-closed cases

A future implementation must fail closed for all of the following local LLM mode cases:

- non-local endpoint;
- malformed endpoint;
- connection failure;
- timeout;
- malformed response;
- empty output;
- prompt echo;
- system echo.

## Fail-closed meaning

Fail-closed means the runtime must stop the local LLM path, surface a bounded error outcome, avoid hosted-provider fallback unless separately authorized, and avoid presenting the output as successful behavior evidence.

## Evidence model preservation

`behavior_evidence=false` must remain preserved for affected local LLM outcomes until a later lane explicitly changes the evidence model.
