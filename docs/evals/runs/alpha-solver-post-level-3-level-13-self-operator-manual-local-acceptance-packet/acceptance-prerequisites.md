# Acceptance Prerequisites

Manual local acceptance must not run until all prerequisites are true:

1. Level 10 static-test scaffold merged and GS done.
2. Level 11 local artifact/preflight foundation merged and GS done.
3. Level 11 approval/stop-state/gate foundation merged and GS done.
4. Approval identity mismatch fix merged and GS done.
5. Level 12 local dry-run wrapper merged and GS done.
6. Operator has a clean local checkout at the intended commit.
7. Operator has chosen a temporary local output root.
8. Operator has reviewed evidence boundary and stop conditions.
9. Explicit operator confirmation is present.
10. No provider/API/dashboard/CLI/browser/deployment/billing/credential/Google Sheets/source-artifact/evidence-promotion scope.
