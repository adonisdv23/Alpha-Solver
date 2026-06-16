# Operator Smoke Results

## Summary

- Local mode passed using `qwen2.5:3b` with provider `ollama`.
- OpenAI mode passed using `gpt-4.1-mini-2025-04-14` with provider `openai`.
- Both results are smoke-only evidence.
- No behavior evidence, quality evidence, readiness evidence, benchmark evidence, production/public evidence, or Alpha-superiority evidence is created.

## Local/Ollama smoke JSON

```json
{
  "behavior_evidence": false,
  "errors": [],
  "estimated_cost_usd": null,
  "finish_reason": null,
  "latency_ms": 25137,
  "mode": "local",
  "model": "qwen2.5:3b",
  "model_set": null,
  "output_preview": "Portable Alpha Solver will process user queries through a modular engine for deterministic and non-deterministic solving methods.",
  "provider": "ollama",
  "quality_evidence": false,
  "readiness_evidence": false,
  "reason": "local_llm_provider_adapter_wiring_only",
  "redaction_status": "sanitized_no_secrets_printed",
  "smoke_evidence_only": true,
  "status": "passed",
  "usage": null
}
```

## OpenAI smoke JSON

```json
{
  "behavior_evidence": false,
  "errors": [],
  "estimated_cost_usd": null,
  "finish_reason": "stop",
  "latency_ms": 2318,
  "mode": "openai",
  "model": "gpt-4.1-mini-2025-04-14",
  "model_set": "operator_smoke",
  "output_preview": "Understood, I will provide concise replies without repeating the prompt.",
  "provider": "openai",
  "quality_evidence": false,
  "readiness_evidence": false,
  "reason": "openai_smoke_completed",
  "redaction_status": "sanitized_no_secrets_printed",
  "smoke_evidence_only": true,
  "status": "passed",
  "usage": {
    "input_tokens": 36,
    "output_tokens": 14,
    "total_tokens": 50
  }
}
```
