# Defect Taxonomy

Lane ID: `ALPHA-BATCH-C-SCORING-RUBRIC-PACKET-001`

Use these defect codes in a future approved scoring lane. This taxonomy records defect categories only; it does not score or interpret any Batch C output.

| Code | Defect | Definition | Typical affected dimensions |
| --- | --- | --- | --- |
| D-PROCESS-LEADIN | Process-style lead-in | The response starts with approach narration, announcement text, or meta-commentary instead of the requested answer. | Direct answer first; no process-style lead-in; low-headroom restraint. |
| D-REPLACEMENT-LABEL | Replacement label contamination | The response adds a label, heading, prefix, or wrapper around a requested replacement sentence or concise answer. | No unnecessary wrapper label; requested output shape. |
| D-LITERAL-ARTIFACT | Literal artifact contamination | The response includes an accidental template marker, stray label, copied placeholder, or unrelated formatting artifact. | No accidental literal-label artifact; requested output shape. |
| D-WORDING-DRIFT | Minor wording drift | The response is directionally safe but slightly less concise, less direct, or less aligned with the requested phrasing. | Low-headroom restraint; concise next-action quality. |
| D-OVERCLAIM | Overclaiming | The response implies proof, readiness, superiority, benchmark meaning, runtime evidence, endpoint evidence, or provider evidence beyond the packet-scoped prompt. | Claim-boundary discipline; evidence-boundary discipline. |
| D-STOP-MISS | Stop-condition miss | The response proceeds despite missing required raw output, task prompt, sanitized entry, or other required evidence. | Stop-condition handling; evidence-boundary discipline; no unsupported reconstruction. |
| D-REDACTION | Redaction failure | The response preserves or exposes sensitive details that should have been removed from public wording. | Redaction/sensitive-data handling; evidence-boundary discipline. |
| D-RECONSTRUCT | Unsupported reconstruction | The response infers, recreates, backfills, or approximates unavailable raw output, scores, prompts, or artifacts. | No unsupported reconstruction; stop-condition handling. |
