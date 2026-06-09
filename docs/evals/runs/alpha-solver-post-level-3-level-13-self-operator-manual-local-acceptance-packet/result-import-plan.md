# Result Import Plan

This is a future import plan only. Do not import results in this lane.

Import remains blocked until raw artifacts exist.

Future import requirements:

- Required files: raw artifact records, scored result records, operator notes, and checks evidence for each MLA task.
- Record artifact paths and checksums before import.
- Verify redaction before import.
- Verify lane ID match.
- Verify run ID match across artifacts.
- Verify commit SHA match with the operator checkout.
- Verify no source-artifact mutation.
- Verify no evidence-promotion occurred before review.
- Keep failed, blocked, and missing artifacts explicit; do not infer pass status.
