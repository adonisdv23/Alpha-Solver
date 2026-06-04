# Blocked Review Template

Lane ID: `ALPHA-LIMITED-OPERATOR-TEST-RESULTS-IMPORT-REVIEW-GATE-001`

Copy/paste this template when the future `ALPHA-LIMITED-OPERATOR-TEST-RESULTS-IMPORT-001` PR fails the review gate.

```markdown
Blocked: do not merge yet.

Gate reviewed: `ALPHA-LIMITED-OPERATOR-TEST-RESULTS-IMPORT-REVIEW-GATE-001`

Blocking issue(s):
- [ ] No actual operator evidence was provided.
- [ ] One or more task rows appear fabricated from templates, memory, planning ledgers, or expectations.
- [ ] One or more imported tasks were not actually run.
- [ ] One or more missing ratings were inferred, averaged, normalized, backfilled, translated, or converted.
- [ ] One or more ratings are outside the allowed `0`-`3` scale.
- [ ] Stop-condition status is missing for one or more imported task rows.
- [ ] Defects were imported without operator-observed evidence.
- [ ] Snippets expose or depend on private data, secrets, raw provider payloads, full unredacted traces, raw outputs, or operator-only maps.
- [ ] The PR makes unsupported benchmark, validation, readiness, superiority, runtime, `/v1/solve`, provider, Batch C, production, or billing claims.
- [ ] The PR changes protected runtime/provider/model/routing surfaces, scored artifacts, raw outputs, operator maps, Google Sheets integrations, Batch C materials, or production-readiness docs.
- [ ] Google Sheets or a planning ledger is treated as proof instead of actual operator evidence.

Required fix before approval:
- Replace this line with the smallest evidence-preserving fix needed. Do not invent rows, infer ratings, inspect forbidden materials, score/rescore outputs, unblind, use `/v1/solve`, call providers, start Batch C, or expand claims.

Non-claims:
- This blocked review does not interpret operator feedback or establish pass/fail benchmark results.
- This blocked review does not prove production readiness, MVP readiness, Alpha superiority, `/v1/solve` behavior, provider behavior, runtime behavior, Batch C readiness, or billing accuracy.
```
