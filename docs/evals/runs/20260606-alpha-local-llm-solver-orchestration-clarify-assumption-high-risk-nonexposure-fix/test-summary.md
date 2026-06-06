# Test Summary

Focused fake-transport tests were added or updated for:

- pass-one `block` plus underspecified prompt clarifies without pass two;
- pass-one `block` plus bounded assumptions proceeds to pass two;
- high-risk prompts still block without normal answer fields;
- high-risk outputs do not expose unsafe considerations or assumptions;
- serious risk flags block without pass two;
- non-allowlisted risk flags block by default;
- pass-one forbidden boundary claims fail closed without exposing fields;
- pass-two forbidden boundary claims fail closed without exposing the forbidden answer;
- existing compatibility and local-only invariants.

All tests use fake or sequenced transports only. No network calls, local model calls, hosted provider calls, smoke reruns, or source artifact imports were performed.
