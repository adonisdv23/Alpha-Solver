# Backend Contract

## Scope

This contract describes a future Ollama-style local HTTP backend without
implementing it and without making a live call.

## Input

The backend must accept the existing `LocalLLMAdapterRequest` object from
`alpha/local_llm/provider_adapter.py`. The request boundary must preserve:

- `provider_mode="local_llm"`.
- `model` as an adapter request field, defaulting to the disabled/unconfigured
  label until a later implementation lane approves a concrete opt-in value.
- `system` containing the portable contract.
- `user_prompt` containing only the caller prompt.
- `messages` containing separate system and user records.
- Metadata containing `prompt_source_path`, `prompt_source_fingerprint`,
  `prompt_source_sha256`, `prompt_source_fingerprint_algorithm`,
  `provider_mode`, `backend_class`, `no_real_provider_call`,
  `real_provider_call_enabled`, `behavior_evidence`, and `evidence_label`.

## Proposed request mapping

For an Ollama-style local HTTP backend, a later implementation may map
`LocalLLMAdapterRequest` to a local HTTP JSON payload with these logical fields:

- `model`: from `request.model`, after explicit opt-in validation.
- `messages`: an array preserving `request.messages` order and role/content
  separation.
- `stream`: false, so offline parser fixtures can be deterministic.
- Optional request options: bounded timeout-related metadata or deterministic
  decode settings only if approved by the implementation lane.

The mapping must not merge the portable contract and user prompt into one field.
It must not replace the request with v91 deterministic fallback output. It must
not route to hosted providers or alternate backends on failure.

## Output

The backend must return normalized adapter output compatible with
`LocalLLMAdapterResult` semantics:

- `output_text`: parsed text from the local response.
- `status`: `non_evidence` only for successful offline/unit handling or a
  separately authorized smoke label; `failed_closed` for unsafe outcomes.
- `reason`: a specific normalized reason.
- `behavior_evidence`: false.
- `metadata`: preserving request metadata and adding parser/failure labels as
  needed without adding secrets or endpoint details.

## Response parser expectations using offline fixtures only

Offline fixtures should cover an Ollama-style JSON response that contains text
in a single assistant message or equivalent response field. The parser must:

- Accept only expected JSON object shapes.
- Extract exactly the assistant text field selected by the implementation lane.
- Reject non-string text, missing text fields, unexpected arrays, invalid JSON,
  and mixed streaming fragments unless streaming support is separately approved.
- Trim only for validation; preserve returned text according to the future test
  contract.
- Label parsed output as fixture-only evidence.

## Required fail-closed cases

A future backend or parser must fail closed for:

- Timeout.
- Connection failure.
- Malformed response.
- Empty output.
- Prompt echo matching the user prompt or system/contract content after
  normalization.
- Missing portable contract.
- Empty portable contract.
- Expected SHA-256 fingerprint mismatch.
- Backend error, including HTTP error status, local process refusal, invalid
  model selection, or parser exception.

## Default-off and no-provider-by-default rules

The future implementation must not call a provider unless later authorization
names the lane, endpoint, timeout, opt-in command, skip behavior, evidence label,
and rollback steps. If authorization is absent, the path remains unavailable,
skipped, or failed closed according to the test contract.
