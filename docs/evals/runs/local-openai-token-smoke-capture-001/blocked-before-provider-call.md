# Blocked before provider call

| Field | Value |
| --- | --- |
| Failed precondition | Required merged OpenAI operator pre-smoke attestation packet approving `LOCAL-OPENAI-TOKEN-SMOKE-CAPTURE-001` was missing. |
| Provider call attempted | no |
| Why no token usage occurred | No OpenAI API call was attempted because the operator-attestation gate failed. |
| Required before retry | Merge a completed operator pre-smoke attestation packet selecting `LOCAL-OPENAI-TOKEN-SMOKE-CAPTURE-001` and confirming data-sharing, project/billing, synthetic prompt, redaction, cost, and output-review boundaries. |
| Selected next lane | `LOCAL-OPENAI-TOKEN-SMOKE-CAPTURE-RETRY-001` |
| Verdict | `BLOCKED_OPERATOR_ATTESTATION_PACKET_MISSING` |
