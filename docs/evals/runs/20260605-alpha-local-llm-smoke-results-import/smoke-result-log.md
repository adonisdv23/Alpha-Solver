# Smoke Result Log

Lane ID: `ALPHA-LOCAL-LLM-SMOKE-RESULTS-IMPORT-001`

## Import gate caveat

The pasted artifact preserves stdout-equivalent generated output, completed timestamps, sanitized request details, and the raw response artifact. It does not separately preserve the literal terminal command text or a numeric process exit code.

Because the literal command and numeric exit code are absent from the pasted artifact, this log does not mark those fields as complete and does not invent them. No numeric exit code is imported.

The artifact is still imported under this docs-only lane because the pasted source records `executed: true`, `exception: null`, completed start and end timestamps, stdout-equivalent content in the Markdown artifact, a sanitized request artifact, and a raw response artifact. This import caveat is preserved for interpretation and final decision.

## Imported result row

| source evidence file | lane ID | prerequisite PR link | literal terminal command | endpoint pattern | model disclosed | timeout seconds | start timestamp | end timestamp | numeric exit code | executed/skipped/blocked | classification | stdout-equivalent artifact | stderr artifact | raw artifact notes present | redaction notes present | evidence boundary present | non-claims present |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `source-evidence/sanitized-smoke-execution-artifact.md` | `ALPHA-LOCAL-LLM-SMOKE-TEST-EXECUTION-001` | PR #305 merged and GS updated | caveat: not separately preserved in pasted evidence; not reconstructed | `http://127.0.0.1:11434/api/chat` | `gemma3:4b` | `120.0` | `2026-06-05T16:41:02.641341+00:00` | `2026-06-05T16:41:41.668264+00:00` | caveat: not separately preserved in pasted evidence; no numeric exit code imported | executed | `non_evidence` | yes; captured in Markdown with full system message omitted while length and role order are preserved | no stderr content included in pasted evidence | yes | yes | yes | yes |

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

## Gate reconciliation

The earlier scaffold required future evidence to include a literal terminal command and numeric exit code. Those two fields are not present in the pasted artifact supplied for this lane, so this import must not be treated as a complete terminal transcript import.

The current import remains evidence-bound to the artifact that was supplied: it records execution completion, adapter result fields, stdout-equivalent generated output, sanitized request details, and raw response details without reconstructing missing terminal metadata.
