# Operator Review Template

Allowed post-response review statuses:

- `accepted_as_smoke_evidence`
- `accepted_with_caveats`
- `rejected_sensitive_output`
- `rejected_boundary_drift`
- `rejected_unexpected_cost_or_usage`
- `not_reviewed`

Default future review fields:

```yaml
operator_review_status: "not_reviewed"
prompt_redaction_review_status: "not_reviewed"
response_redaction_review_status: "not_reviewed"
boundary_review_status: "not_reviewed"
cost_or_usage_review_status: "not_reviewed"
reviewer_notes: ""
```
