# Checks run

- PASS `git diff --check`
- PASS narrative claim-safety lint on changed Markdown files: no changed Markdown claims completed pilot outputs for this prep lane.
- PASS template completeness check: blank capture fields are present for `RVP-001` through `RVP-012`.
- PASS route metadata template check: each task includes a blank `route reasons` field.
- PASS high-stakes handling text check: `high-stakes-card-handling.md` exists and requires stop/capture-only handling.
- PASS source-of-truth consistency check: `OPERATOR_REVIEW_REQUIRED_AFTER_ROUTED_VS_PLAIN_PILOT_OUTPUT_COLLECTION_PREP_001` appears in source-of-truth docs and packet state files.
- PASS changed-line secret-safety check: changed lines contain no credentials or secrets.
- PASS packet completeness check: all required top-level prep files are present.
