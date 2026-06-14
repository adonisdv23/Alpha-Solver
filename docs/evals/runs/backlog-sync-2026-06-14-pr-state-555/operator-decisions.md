# Operator Decisions

Before applying the paste-ready rows, the operator should decide:

1. **Active next lane:** With zero open PRs verified, choose the single next active lane. Candidate choices include an authorization-refresh/smoke-boundary lane, DEF-002 review, or another narrow docs/evidence lane.
2. **Closed-not-merged handling:** Confirm that PR #547 is superseded by PR #550, PR #544 by PR #545, and PR #533 by PR #537 in the external backlog.
3. **Value-read wording:** Keep value-read rows blocked/gated unless and until committed evidence supports substantive no-echo value execution.
4. **Archive policy:** Archive completed/superseded rows from active views only; do not delete evidence or provenance.
5. **Manual sheet application:** If rows are pasted into a Sheet, record that action outside this repo; this packet itself is not sheet synchronization.
