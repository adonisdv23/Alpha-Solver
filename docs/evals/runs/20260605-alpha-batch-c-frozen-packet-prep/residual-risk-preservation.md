# Residual Risk Preservation

Lane ID: `ALPHA-BATCH-C-FROZEN-PACKET-PREP-001`

## Preserved residual risks from the prior decision packet

| residual risk | preservation requirement for Batch C |
| --- | --- |
| LT2-001 process-style lead-in | Score future BC tasks for visible lead-in text before the requested artifact. Do not hide or normalize this issue during capture or sanitization. |
| LT2-005 process-style lead-in | Preserve prompt/template tasks that can reveal process-style prefatory text before the requested template. |
| LT2-009 minor wording drift | Keep claim-boundary scoring sensitive to wording that sounds stronger than packet-scoped observations. |
| Evidence type limit | Keep Batch C framed as manual prompt-contract simulation preparation/execution only, not product/runtime, endpoint, provider, local-model, benchmark, MVP, production, or comparative proof. |

## Positive patterns to preserve

| positive pattern | preservation requirement for Batch C |
| --- | --- |
| Reduced accidental literal-label artifacts | Include prompts that reveal whether unwanted literal labels appear before concise artifacts. |
| Reduced unnecessary replacement labels | Include replacement-only prompts that should not add wrapper labels. |
| Correct LT2-006 stop-condition handling | Include at least one missing-raw-artifact prompt where reconstruction and scoring must stop. |

## Preservation rule

Future Batch C scoring must report both improvements and regressions. It must not smooth over residual risks because the final artifact is otherwise usable.
