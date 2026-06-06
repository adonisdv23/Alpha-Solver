# Expert Two-Pass Check

## Result

`PASS_FOR_MANUAL_SMOKE_PACKET_AUTHORIZATION`

## Pass 1 confirmations

- Pass 1 asks for structured gate inputs: mode, considerations, assumptions, confidence, missing information, and risk flags.
- Pass 1 prefers JSON output.
- Pass 1 parses JSON first when valid JSON is available.
- Pass 1 uses conservative bounded section parsing only when the section shape is safe.
- Unsafe, empty, echoed, malformed, ambiguous, or unparseable Pass 1 output fails closed or avoids unsupported successful answering.

## Pass 2 confirmations

- Pass 2 is only attempted after a gate mode that permits answering: `direct` or allowed `answer_with_assumptions`.
- Pass 2 receives bounded considerations and assumptions from Pass 1.
- Pass 2 preserves the local-only runtime boundary: default-off, loopback-only, no provider keys, finite timeout, no hosted fallback, and `behavior_evidence=false`.
- Pass 2 failure does not expose a successful final answer.

## Boundary statement

This check is about orchestration mechanics only. It is not local model quality evidence, benchmark evidence, Alpha superiority evidence, or MVP validation.
