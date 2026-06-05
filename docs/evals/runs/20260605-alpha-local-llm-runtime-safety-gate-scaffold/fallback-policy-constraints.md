# Fallback Policy Constraints

Lane: `ALPHA-LOCAL-LLM-RUNTIME-SAFETY-GATE-SCAFFOLD-001`

This is a scaffold only. Local LLM runtime integration is not implemented here.

## No hosted provider fallback by default

Future local LLM runtime integration must not silently switch to a hosted provider when local LLM mode fails, times out, returns malformed output, returns empty output, echoes the prompt, echoes system content, or has an invalid endpoint.

Hosted provider fallback is blocked unless separately authorized by a later lane with explicit routing, evidence, observability, and operator-consent requirements.

## Fail-closed over fallback

For this safety gate, fail-closed behavior is required instead of fallback for:

- non-local endpoint
- malformed endpoint
- connection failure
- timeout
- malformed response
- empty output
- prompt echo
- system echo
