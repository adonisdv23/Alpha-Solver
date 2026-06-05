# Decision Options

Lane ID: `ALPHA-BATCH-C-POST-RESULTS-DECISION-001`

| Option | Selection rule | Status for this PR |
| --- | --- | --- |
| `ALPHA-BATCH-C-TRACK-CLOSEOUT-001` | Select if all tasks are `Keep` or only minor `Refine` with no blocking defects. | Selected. |
| `ALPHA-BATCH-C-PORTABLE-CONTRACT-REFINEMENT-001` | Select if material prompt-contract defects remain but raw evidence is complete. | Not selected; no material prompt-contract defect remains. |
| `ALPHA-BATCH-C-OPERATOR-EXECUTION-RETRY-001` | Select if source evidence is incomplete or raw outputs are missing. | Not selected; source evidence and raw outputs are complete. |
| `ALPHA-BATCH-C-RESULTS-IMPORT-REPAIR-001` | Select if scoring/import is blocked by redaction or artifact integrity issues. | Not selected; no redaction or artifact-integrity block was found. |

Exactly one next lane is selected.
