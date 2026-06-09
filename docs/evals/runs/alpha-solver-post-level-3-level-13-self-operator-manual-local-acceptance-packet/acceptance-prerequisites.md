# Acceptance Prerequisites

Manual local acceptance must not run until all prerequisites are true:

1. Level 10 static-test scaffold merged and GS done.
2. Level 11 local artifact/preflight foundation merged and GS done.
3. Level 11 approval/stop-state/gate foundation merged and GS done.
4. Approval identity mismatch fix merged and GS done.
5. Level 12 local dry-run wrapper merged and GS done.
6. Final MVP/Self Operator runbook reviewed, including the accepted operator flow, stop states, artifact storage, redaction, and blocked-claim constraints.
7. Operator has a clean local checkout at the intended commit.
8. Operator has chosen a temporary local output root.
9. Operator has reviewed evidence boundary and stop conditions.
10. Explicit operator confirmation is present.
11. No provider/API/dashboard/CLI/browser/deployment/billing/credential/Google Sheets/source-artifact/evidence-promotion scope.

Acceptance remains blocked until the Level 12 local dry-run wrapper is merged and GS done, the final runbook reviewed, the operator has a clean local checkout and temporary local output root, evidence boundary and stop conditions are reviewed, explicit operator confirmation is present, and no forbidden external/provider/runtime/source-artifact/evidence-promotion scope exists.
