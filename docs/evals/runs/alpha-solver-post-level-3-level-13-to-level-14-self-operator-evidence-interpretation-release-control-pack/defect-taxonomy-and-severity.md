# Defect Taxonomy and Severity

| Severity | Definition | Examples | Blocks acceptance? | Blocks MVP readiness? | Required next action |
| --- | --- | --- | --- | --- | --- |
| P0 | Evidence boundary or source mutation violation. | Source artifacts mutated, evidence promoted, credentials exposed, provider or deployment activity observed. | Yes | Yes | Stop, preserve evidence, operator review, create fix or incident lane. |
| P1 | Approval, identity, stop-state, or non-execution safety failure. | `approval_identity_mismatch` not blocked, `SELF_OPERATOR_APPROVAL_IDENTITY_MISMATCH` missing, stop-state omitted, proposed command executed. | Yes | Yes | File blocking defect, fix safety gate, rerun only after approval. |
| P2 | Artifact schema, import, or determinism failure. | Missing schema version, checksum absent, JSON malformed, nondeterministic artifact content. | Usually yes until resolved | Yes until resolved | Repair import or artifact contract, rerun integrity checks. |
| P3 | Docs, clarity, or operator UX issue. | Ambiguous operator note, unclear runbook step, typo in ledger label. | No unless it prevents reliable execution/review | No unless unresolved ambiguity blocks review | Patch docs or request operator clarification. |

P0 and P1 defects always block acceptance and MVP readiness until resolved and reviewed.
