# Model Smoke Result Template

Use one record per model name.

```json
{
  "model": "<local-ollama-model-name>",
  "status": "not_installed | connection_failed | timeout | empty_output | prompt_echo | substantive_looking_output | blocked",
  "reason": "<non_evidence_reason_code>",
  "behavior_evidence": false,
  "evidence_label": "local_multi_model_smoke_only_no_behavior_evidence",
  "output_preview": "<short redacted preview if safe>",
  "metadata": {
    "no_hosted_fallback": true,
    "no_provider_keys_accepted": true,
    "strict_no_behavior_evidence_labeling": true
  }
}
```

`substantive_looking_output` means only that the adapter received non-empty text that was not exact prompt/system echo. It is not a claim of correctness, quality, utility, benchmark performance, routing success, production readiness, value evidence, or Alpha superiority.
