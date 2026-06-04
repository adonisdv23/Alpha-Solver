# Results Import Issues to Refine Before Merge

Lane ID: `ALPHA-LIMITED-OPERATOR-TEST-RESULTS-IMPORT-REVIEW-GATE-001`

These issues are fixable if the future results-import PR otherwise preserves evidence, artifact, and claim boundaries. If the fix would require inventing results, inferring ratings, inspecting forbidden materials, or making prohibited claims, treat the issue as a blocker instead.

## Fixable issues

- **Missing provenance field:** A row has operator evidence, but the import does not clearly identify the evidence source, operator, date, or portable-surface context required by the future schema.
- **Weak evidence snippet:** A snippet is too vague to support the rating or defect, but a small safe operator-provided snippet can be added without exposing private data, secrets, raw provider payloads, full traces, raw outputs, or operator-only maps.
- **Unclear primary defect:** Multiple observed defects are listed but the primary defect is ambiguous; the PR should mark the primary defect as unclear or use the operator-provided primary defect if available.
- **Incomplete but declared feedback:** The PR says the feedback set is complete even though ratings, notes, defects, or stop-condition fields are missing for one or more actually run tasks.
- **Non-claims too weak:** The PR avoids explicit overclaims but does not clearly state that imported material is operator feedback only and not validation, benchmarking, readiness, superiority evidence, runtime evidence, provider evidence, production evidence, or billing evidence.
- **Next lane missing or too broad:** The PR either omits a narrow next lane or proposes an overly broad next lane such as Batch C, runtime/provider testing, production readiness, public launch, or broad validation.

## Refinement rule

A refinement is acceptable only when it makes the future import more faithful to actual operator evidence. Do not refine by reconstructing missing rows, inferring ratings, adding invented defects, interpreting results, unblinding, consulting operator-only maps, treating Google Sheets as proof, or expanding claims.
