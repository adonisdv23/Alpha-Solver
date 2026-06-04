# Results Import Reviewer Checklist

Lane ID: `ALPHA-LIMITED-OPERATOR-TEST-PROMPT-CONTRACT-SIMULATION-RESULTS-IMPORT-001`

Use this checklist to review the docs-only results-import PR.

## Required checks

- [ ] The PR is docs-only.
- [ ] All changed files are under `docs/evals/runs/20260604-alpha-limited-operator-test-prompt-contract-simulation-results-import/`.
- [ ] The raw transcript is preserved in `source-evidence/Chatgpt - Operator Test Task Set.md`.
- [ ] The filled feedback packet is preserved in `source-evidence/alpha_solver_operator_feedback_filled.md`.
- [ ] Ratings match the filled feedback packet.
- [ ] Mechanical totals are computed only from Adonis-provided 0-3 ratings.
- [ ] Missing stop-condition yes/no fields remain marked `missing`.
- [ ] Missing overall 0-3 operator rating fields remain marked `missing`.
- [ ] The PR does not rescore, reinterpret, normalize, or backfill operator feedback.
- [ ] The PR does not inspect operator maps or assignment maps.
- [ ] The PR does not update Google Sheets.
- [ ] The PR does not run capture, scoring, rescoring, adjudication, or unblinding.
- [ ] The PR does not change runtime, provider, model, routing, API, or solver behavior.
- [ ] The PR does not start Batch C.
- [ ] The PR does not make product/runtime, `/v1/solve`, local LLM, provider, validation, production-readiness, Batch C-readiness, Alpha-superiority, or broad plain-provider-inferiority claims.

## Notes for unsafe text scans

The raw transcript intentionally preserves source prompts and model outputs exactly as supplied. Unsafe wording that appears inside raw source evidence is not itself a generated import claim. Generated import docs should use only evidence-bounded framing.

## Merge decision rule

Safe to merge only if the PR preserves the two supplied evidence files, imports mechanical result rows, computes arithmetic totals without altering ratings, leaves missing fields missing, and remains within the evidence boundary.
