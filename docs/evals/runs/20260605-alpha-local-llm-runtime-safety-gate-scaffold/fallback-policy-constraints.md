# Fallback Policy Constraints

This is a scaffold only. Local LLM runtime integration is not implemented here.

## No hosted fallback without authorization

A future local LLM runtime implementation must not fall back to a hosted provider unless a later lane separately authorizes that behavior. Local LLM failures must not be masked by hosted-provider output.

## Required fallback review questions

Future implementation review must confirm that:

- routing does not silently switch to a hosted provider;
- hosted provider keys are not required for local LLM mode;
- local LLM mode does not use hosted-provider billing, telemetry, or orchestration paths;
- failure outcomes are visible as local LLM failures rather than transformed into hosted-provider successes.

## Fail-closed fallback handling

For local LLM mode, connection failures, timeouts, malformed responses, empty outputs, prompt echoes, and system echoes must fail closed rather than triggering hosted fallback.
