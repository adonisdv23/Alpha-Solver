# Safety-Gate Summary

Lane: `ALPHA-LOCAL-LLM-RUNTIME-SAFETY-GATE-SCAFFOLD-001`

This is a scaffold only. Local LLM runtime integration is not implemented here.

## Gates future implementation must satisfy

Any future local LLM runtime integration must require all of the following before runtime-readiness claims are allowed:

1. **Default-off local LLM runtime mode** unless explicitly configured by an authorized operator.
2. **Explicit opt-in configuration** for local LLM runtime use.
3. **Localhost / loopback endpoint only** for local LLM runtime endpoints.
4. **No hosted provider fallback** unless a separate lane explicitly authorizes and specifies that behavior.
5. **No provider keys** required, loaded, or used for local LLM mode.
6. **Finite timeout** for all local LLM runtime calls.
7. **Fail-closed behavior** for unsafe or ambiguous local runtime outcomes.
8. **Runtime smoke before runtime-readiness claims**.
9. **`behavior_evidence=false` remains preserved** until a later lane explicitly changes the evidence model.
10. **Raw artifact preservation** for future runtime smoke review.

## Mandatory fail-closed cases

Future implementation must fail closed for:

- non-local endpoint
- malformed endpoint
- connection failure
- timeout
- malformed response
- empty output
- prompt echo
- system echo

## Surfaces blocked until later authorization

Future review must confirm that `/v1/solve` and dashboard preview are not exposed to local LLM mode until explicitly authorized by a later lane.
