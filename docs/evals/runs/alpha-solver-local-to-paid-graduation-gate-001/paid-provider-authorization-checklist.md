# Paid-provider authorization checklist

A paid provider call is forbidden unless every item is complete for the exact next run.

| Authorization field | Required content | Current status |
| --- | --- | --- |
| Provider | Exact hosted provider name. | Missing for this gate. |
| Model | Exact model identifier. | Missing for this gate; missing in `local-openai-token-smoke-capture-retry-002`. |
| Project/account boundary | Redacted but explicit project/account boundary approved for this run. | Prior attestation exists, but exact retry authorization was incomplete. |
| Purpose | Must be `tiny synthetic smoke` or narrower. | Not approved by this packet. |
| Max run count | Exact maximum number of invocations. | Missing. |
| Max request count | Exact maximum HTTP/API requests. | Missing. |
| Token cap | Exact input/output/total token cap or stricter equivalent. | Missing. |
| Cost cap | Exact USD or provider-credit cap. | Missing. |
| Synthetic fixture | Exact prompt payload to send, frozen before the run. | Missing for the blocked retry. |
| Data-sharing acknowledgement | Operator confirms the fixture may be sent to the provider under provider terms. | Needs run-specific refresh. |
| Redaction review | Operator confirms fixture and logs contain no secrets/sensitive data. | Needs run-specific refresh. |
| Stop conditions | Operator accepts stop conditions before execution. | Captured here, not approved. |
| Result boundary | Operator accepts that results are smoke-only and non-value evidence. | Needs approval. |

## Authorization verdict

Current status: `BLOCKED_OPERATOR_AUTHORIZATION_REQUIRED`.

The next safe paid-provider action, if the operator still wants to proceed, is an authorization-refresh lane only. It must not call providers. It should fill the missing fields above and then select a subsequent tiny smoke lane only if all fields are complete.
