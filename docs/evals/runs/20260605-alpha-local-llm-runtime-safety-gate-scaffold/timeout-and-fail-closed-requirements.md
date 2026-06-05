# Timeout and Fail-Closed Requirements

Lane: `ALPHA-LOCAL-LLM-RUNTIME-SAFETY-GATE-SCAFFOLD-001`

This is a scaffold only. Local LLM runtime integration is not implemented here.

## Finite timeout

Future local LLM runtime calls must have a finite timeout. Unbounded waits are not allowed.

## Required fail-closed outcomes

Future implementation must fail closed for each of the following conditions:

| Condition | Required outcome |
| --- | --- |
| non-local endpoint | reject before local runtime call |
| malformed endpoint | reject before local runtime call |
| connection failure | fail closed without hosted fallback |
| timeout | fail closed without hosted fallback |
| malformed response | fail closed without hosted fallback |
| empty output | fail closed without hosted fallback |
| prompt echo | fail closed without hosted fallback |
| system echo | fail closed without hosted fallback |

## Evidence expectation

A later implementation lane must preserve evidence that these paths were reviewed or tested before making any runtime-readiness claim.
