# Operator decisions required

These are decisions for the human operator before changing the actual sheet or authorizing new implementation lanes.

| decision_id | decision needed | default recommendation | why |
| --- | --- | --- | --- |
| OPD-001 | Confirm whether the repo-global next lane should remain the OpenAI authorization/smoke chain or pivot to DEF-002-local closeout. | Keep repo-global lane unchanged until operator explicitly pivots. | Current source docs still treat smoke authorization as repo-global control, while many DEF-002 lanes are local/security track recommendations. |
| OPD-002 | Decide whether to mark current top-level docs stale after PRs #523-#537. | Add a follow-up docs refresh row rather than silently rewriting history. | `CURRENT_STATE.md`, `EVIDENCE_INDEX.md`, `LANE_REGISTRY.md`, and related docs mention earlier controls that were later superseded by merged packets. |
| OPD-003 | Decide whether DEF-002 remaining residuals should be fixed, accepted, or split into closeout prerequisites. | Split into remaining closure lanes plus explicit risk acceptance only where allowed. | Several RR lanes are hardened or partially hardened, but DEF-002 is not closed. |
| OPD-004 | Decide whether value work should wait for no-echo/substantive-generation and provider-smoke prerequisites or proceed with simulation-only evidence. | Do not treat simulation prep as value evidence; keep runtime/value execution blocked. | Value pilot and manual discrimination packets are prep/design only or inconclusive. |
| OPD-005 | Decide stale branch cleanup outside repo docs. | Operator-only cleanup; do not delete from this repo task. | Branch cleanup is external state and requires human confirmation. |
| OPD-006 | Decide MVP/readiness doc source-of-truth/dedup. | Keep existing docs; create a narrow docs-dedup lane if needed. | Archive index already marks overlapping MVP docs as needing operator decision. |
| OPD-007 | Decide dependency lock/hash/SBOM strategy. | Add a supply-chain decision lane. | Dependency packet captures provenance/update policy but does not close lock/hash/SBOM controls. |
