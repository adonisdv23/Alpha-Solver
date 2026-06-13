# Smoke-capture preconditions

Before `LOCAL-OPENAI-TOKEN-SMOKE-CAPTURE-001` can run, all minimum preconditions must be satisfied:

- PR #502 merged.
- DEF-002 / DEF-003 evidence-boundary packet merged, or explicit caveat accepted.
- This operator-verification packet merged.
- Operator has completed go/no-go checklist.
- Synthetic smoke prompt selected.
- Cost cap selected.
- Redaction check passed.

Current status: operator-account-specific verification remains `pending_operator_verification`, so token smoke is not selected by this packet.
