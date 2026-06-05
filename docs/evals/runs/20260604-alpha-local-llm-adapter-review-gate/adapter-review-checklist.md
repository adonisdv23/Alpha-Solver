# Adapter Review Checklist

This checklist records the review items required before using the PR #290 seam
as the basis for a future local-provider planning lane.

## Contract consumption

- [x] The adapter consumes `alpha_solver_portable.py` through
  `load_portable_contract`.
- [x] The adapter request stores the loaded portable contract as the system
  content.
- [x] The request also contains a two-message shape with separate `system` and
  `user` entries.
- [x] The user prompt remains separate from system/contract content.

## Prompt-source preservation

- [x] Metadata preserves `prompt_source_path`.
- [x] Metadata preserves `prompt_source_fingerprint`.
- [x] Metadata preserves `prompt_source_sha256`.
- [x] Metadata preserves the SHA-256 fingerprint algorithm label.
- [x] Fingerprint mismatch fails closed before handoff.

## Mode separation

- [x] `provider_mode="local_llm"` is the adapter mode label.
- [x] `provider_mode="local"` is rejected by the adapter path.
- [x] `MODEL_PROVIDER=local` remains a separate smoke-only runtime setting.
- [x] This gate does not authorize any runtime routing change.

## Backend seam

- [x] The adapter requires an injected backend with a `generate(request)` seam.
- [x] The included stub backend records requests and performs no I/O.
- [x] Tests use stub/fake backends and run offline.
- [x] No Ollama, local model, hosted provider, provider key, or network call is
  part of the reviewed seam.

## Non-evidence labeling

- [x] Adapter output uses `behavior_evidence=False`.
- [x] Adapter metadata sets `no_real_provider_call=True`.
- [x] Adapter metadata sets `real_provider_call_enabled=False`.
- [x] Adapter output is labeled as non-evidence local LLM provider-adapter
  wiring.

## Fail-closed behavior

- [x] Empty output fails closed.
- [x] Prompt echo fails closed.
- [x] Backend error fails closed.
- [x] Missing contract fails closed.
- [x] Empty contract fails closed.
- [x] Fingerprint mismatch fails closed.
- [x] Empty user prompt fails before request construction.

## Fallback exclusion

- [x] The seam does not import or call v91 `_tree_of_thought` fallback.
- [x] The seam does not route through `alpha_solver_entry.py`.
- [x] The seam remains outside `/v1/solve` and dashboard preview paths.
