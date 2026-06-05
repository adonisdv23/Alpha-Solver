# Smoke Result Log

Lane ID: `ALPHA-LOCAL-LLM-SMOKE-RESULTS-IMPORT-001`

## Imported result row

| source evidence file | lane ID | prerequisite PR link | command recorded | endpoint pattern | model disclosed | timeout seconds | start timestamp | end timestamp | exit code | executed/skipped/blocked | classification | stdout sanitized | stderr sanitized | raw artifact notes present | redaction notes present | evidence boundary present | non-claims present |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `source-evidence/sanitized-smoke-execution-artifact.md` | `ALPHA-LOCAL-LLM-SMOKE-TEST-EXECUTION-001` | PR #305 merged and GS updated | not separately recorded in pasted evidence | `http://127.0.0.1:11434/api/chat` | `gemma3:4b` | `120.0` | `2026-06-05T16:41:02.641341+00:00` | `2026-06-05T16:41:41.668264+00:00` | not recorded in pasted evidence | executed | `non_evidence` | yes; full system message omitted while length and role order are preserved | no stderr content included; source says preserve separately if Terminal shows errors | yes | yes | yes | yes |

## Preserved result fields

```json
{
  "backend_calls": 1,
  "backend_payloads": 1,
  "behavior_evidence": false,
  "exception": null,
  "executed": true,
  "output_text": "OK",
  "reason": "local_llm_provider_adapter_wiring_only",
  "status": "non_evidence"
}
```

## Preserved metadata fields

```json
{
  "backend_class": "stub-local-llm-provider-adapter",
  "behavior_evidence": false,
  "evidence_label": "non_evidence_local_llm_provider_adapter_wiring",
  "model": "gemma3:4b",
  "no_real_provider_call": true,
  "prompt_source_fingerprint": "98841febea17e2ea4d0155df63537bcb76f948e51395bddc1ce870b349d3c7bb",
  "prompt_source_fingerprint_algorithm": "sha256",
  "prompt_source_path": "alpha_solver_portable.py",
  "prompt_source_sha256": "98841febea17e2ea4d0155df63537bcb76f948e51395bddc1ce870b349d3c7bb",
  "provider_mode": "local_llm",
  "real_provider_call_enabled": false
}
```
