# Archive plan

Full index: [`docs/ARCHIVE_INDEX.md`](../../../ARCHIVE_INDEX.md).

**Archive = remove from active queue, NOT delete.** No evidence packet is
deleted; no historical content is mutated.

- **CURRENT_CONTROL_SOURCE**: PR #509 packet + its `selected-next-lane.md`; the
  new top-level governance docs.
- **COMPLETED_KEEP_AS_EVIDENCE**: PRs #501, #502, #503, #504, #506, #507, #508.
- **ARCHIVE_HISTORICAL**: execution-evidence 001/002/003 (#497/#499/#500); all
  pre-#509 `selected-next-lane.md` snapshots; old ROADMAP "Done" section.
- **SUPERSEDED_BY_NEWER_EVIDENCE**: `local-openai-token-smoke-capture-001` (#505);
  planning packet (#502) relative to attestation/checker packets.
- **NEEDS_OPERATOR_DECISION**: contaminated `.specs/*` (ISS-001), MVP doc overlap
  (ISS-010), stale-branch cleanup (ISS-011).
- **DO_NOT_TOUCH**: canonical `.specs/MCP-005.md`; preserved local qwen
  manual-smoke source artifacts.

No deletion of any evidence packet is recommended.
