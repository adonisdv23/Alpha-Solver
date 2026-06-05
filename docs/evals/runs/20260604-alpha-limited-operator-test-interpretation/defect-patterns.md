# Defect Patterns

Lane ID: `ALPHA-LIMITED-OPERATOR-TEST-INTERPRETATION-001`

## Primary recurring defect: output-format contamination

The strongest recurring operator-feedback defect is output-format contamination. The imported notes identify visible process-style text, extra labels, wrappers, and `standard:` artifacts across several tasks.

Affected tasks from operator feedback:

| task_id | operator-noted pattern | severity | disposition |
| --- | --- | --- | --- |
| LT-002 | visible process text and `standard:` artifact before reviewer comment | Minor to moderate | Refine |
| LT-003 | visible process text before answer | Minor | Keep |
| LT-004 | `standard:` artifact and “Replacement:” label | Minor | Refine |
| LT-005 | visible process text before final answer | Minor | Keep |
| LT-006 | visible process text before final answer | Minor | Keep |
| LT-007 | visible process text, `standard:` artifact, and extra wrapper | Minor to moderate | Refine |
| LT-010 | visible process text and `standard:` artifact before checklist | Minor | Refine |

Interpretation: the pattern is not primarily about unsafe claims. It is a formatting and answer-shape defect that makes otherwise usable outputs less directly usable, especially for concise rewrite, comment, template, and checklist requests.

## Secondary defect: answer-shape mismatch on concise requests

LT-002 shows the clearest task-level mismatch. The operator noted that the output violated the “no memo / concise” expectation and returned the comment back as-is. This aligns with lower ratings for direct usefulness, over-framing, stop-condition handling, and usability with minor edits.

LT-007 and LT-010 show a lighter version of the same pattern: substantive content was usable, but wrapper text and artifacts reduced fit for compact output requests.

## Lower-scoring dimensions

The lowest preserved dimension total is no-overframe at 22 / 30. Answer-first totals are 25 / 30, while brevity and usable-with-minor-edits are each 26 / 30. These totals support focusing refinement on output shape, first-token usefulness, and artifact suppression rather than changing the underlying boundary policy.

## Non-defects in imported feedback

The operator feedback did not report serious evidence-boundary failures, fabricated results, fabricated repo state, runtime claims, provider claims, or Batch C-readiness claims. This statement is limited to the imported operator feedback and does not establish behavior outside the manual prompt-contract simulation.
