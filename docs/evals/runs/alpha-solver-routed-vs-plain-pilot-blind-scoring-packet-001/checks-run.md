# Checks run

- `git diff --check` — PASS: no whitespace errors.
- `python scripts/check_narrative_claim_safety.py $(cat /tmp/changed_md.txt)` — PASS: `ALPHA-SOLVER-NARRATIVE-CLAIM-SAFETY-LINTER-001 passed (16 files scanned). This is not a completeness claim.`
- Source artifact completeness check for all 12 plain/routed/metadata files — PASS: all 12 plain files, all 12 routed files, and all 12 metadata files are present under `docs/evals/runs/alpha-solver-routed-vs-plain-pilot-outputs-001/`.
- Blinded comparison completeness check for all `RVP-001` through `RVP-012` — PASS: 12 comparisons are present and each includes Answer A and Answer B.
- Scorer-facing no-identity-leak check — PASS: `blind-scorer-packet.md` contains no prohibited plain/routed/source identity labels, route metadata field labels, source paths beside answers, or PR numbers.
- Private map exclusion warning check — PASS: `PRIVATE - DO NOT INCLUDE IN SCORER PACKET - DO NOT USE DURING BLIND SCORING` is present.
- No scores/no winners/no totals check — PASS: no completed scores, winner selections, or totals are recorded in changed Markdown.
- Selected-next-state consistency check — PASS: `OPERATOR_REVIEW_REQUIRED_AFTER_ROUTED_VS_PLAIN_PILOT_BLIND_SCORING_PACKET_CONSTRUCTION_001` is present in the packet and source-of-truth docs.
- Changed-line secret-safety check — PASS: no obvious secret patterns such as API-key prefixes, password assignments, secret access keys, or private-key blocks are present in changed Markdown.
- Packet completeness check — PASS: all 13 required packet files are present.
