# Smoke Artifact Template

Future lane: `LOCAL-OPENAI-TOKEN-SMOKE-CAPTURE-001`.

No real provider data is included in this fixture lane.

```yaml
prompt_id: ""
prompt_text: ""
redaction_status: "not_reviewed"
model_used: ""
request_timestamp: ""
response_text: ""
response_redaction_status: "not_reviewed"
token_usage_if_available: null
request_id_if_available: null
cost_metadata_if_available: null
operator_review_status: "not_reviewed"
evidence_boundary: "docs-only fixture; provider smoke evidence not captured here"
non_claims:
  - OpenAI validation
  - provider validation
  - API smoke success
  - token usage
  - eval execution
  - security/privacy completion
  - DEF-002 resolved
  - DEF-003 resolved
  - runtime readiness
  - public MVP readiness
  - production readiness
  - benchmark validation
  - benchmark superiority
  - broad-user readiness
  - autonomous readiness
  - /v1/solve readiness
  - dashboard readiness
```
