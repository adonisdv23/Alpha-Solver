# Blind Scorer Result

Lane ID: `OUTPUT-DIFF-POST-IMPROVEMENT-BLIND-SCORING-001`

Status: blind scoring complete, still blinded, no unblinding.

Source sanitized packet: `docs/evals/runs/20260604-post-minimal-behavior-portable-capture/sanitized-scorer-facing-packet.md`

## Blinding and scope confirmations

- Raw outputs were not inspected.
- The operator-only map was not inspected or requested.
- No source identity was inferred from tone, structure, length, formatting, prompt wording, scorer-facing order, or any other cue.
- No provider/model/runtime metadata was used.
- No Google Sheets update occurred.
- Batch C was not started.
- No runtime/provider/model/routing changes occurred.
- No validation, readiness, superiority, benchmark, exact-billing, self-healing, adaptive-learning, self-optimization, autonomous-optimization, or provider-orchestration claims are made.
- No provider calls, capture reruns, or `/v1/solve` measurements occurred.

## Per-comparison scoring summary

| Comparison | Output A total | Output B total | Blinded delta A-B | Blinded preference | Rationale |
| --- | ---: | ---: | ---: | --- | --- |
| comparison-001 / PMB-PF-001 | 34 | 42 | -8 | Output B | Output B is more complete on evidence still needed and claim boundaries; Output A is usable but less specific about repeatability and locked scoring. |
| comparison-002 / PMB-PF-002 | 39 | 37 | 2 | Output A | Output A gives a firm, blame-free hold request and a clear fix path; Output B is also strong but slightly less explicit about the remediation sequence. |
| comparison-003 / PMB-PF-003 | 40 | 37 | 3 | Output A | Output A follows the requested yes-or-no-first format more cleanly while still giving safe next actions; Output B is safer-toned but the leading stop label weakens requested format discipline. |
| comparison-004 / PMB-PF-004 | 35 | 35 | 0 | Tie | Outputs are textually identical and fully satisfy the active-voice rewrite request. |
| comparison-005 / PMB-PF-005 | 40 | 40 | 0 | Tie | Both outputs identify the central process risks and provide a safer sequence within the requested length. |
| comparison-006 / PMB-PF-006 | 38 | 40 | -2 | Output B | Output B more clearly separates instruction-test evidence from live endpoint evidence and gives a stronger final boundary sentence; Output A is accurate but slightly less explicit. |
| comparison-007 / PMB-PF-007 | 41 | 40 | 1 | Output A | Output A gives a slightly stronger safe sequence by preserving prompt freezing and separate authorization before later actions; Output B is also strong and comparable. |
| comparison-008 / PMB-PF-008 | 39 | 40 | -1 | Output B | Output B provides a crisper controlling-evidence sentence and more complete endpoint-specific follow-up checks; Output A is accurate and usable. |

## Aggregate blinded totals

- Output A aggregate blinded total: 306
- Output B aggregate blinded total: 311
- Aggregate blinded delta, Output A minus Output B: -5

## Aggregate blinded preference counts

- Output A: 3
- Output B: 3
- Tie: 2
- Inconclusive: 0

## Recurring defects and caveats

- Some outputs were materially comparable, so d14 was scored conservatively when visible user-facing value was only marginally different.
- Several low-complexity prompts did not require extensive assumption or risk handling; acceptable scores on those dimensions should not be read as defects by themselves.
- Output A recurring caveats: occasional lower specificity on evidence requirements or endpoint-proof examples.
- Output B recurring caveats: occasional extra leading label or slightly weaker authorization/frozen-prompt specificity.
- No comparisons were stopped as unscoreable.
- Alpha/plain interpretation requires a later authorized unblinding/scored-artifact lane.
