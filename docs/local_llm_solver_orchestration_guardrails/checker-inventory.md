# Checker Inventory

## Evidence-boundary checker

Command source: `scripts/check_local_llm_evidence_boundaries.py`.

### What it protects

The evidence-boundary checker protects against unsupported promotional or operational claims appearing in local LLM solver orchestration docs without nearby boundary language. It scans relevant local orchestration docs and evidence packets while excluding preserved source-artifact payloads. It also requires the final Level 3 closeout packet to retain accepted non-promotional boundary markers in authoritative packet files rather than only in logs.

### What it does not do

It does not run local models, start Ollama, call hosted providers, read secrets, exercise runtime routes, run benchmarks, bill, or promote evidence. Passing this checker means the docs preserve boundary language; it is not a runtime result.

## Docs path/link checker

Command source: `scripts/check_local_llm_doc_paths.py`.

### What it protects

The docs path/link checker protects local LLM solver orchestration operator docs and the evidence index from stale repo-relative paths, missing key packet paths, and simple conflicting selected-next statements inside a single document. It keeps links to source-of-truth docs, packet directories, scripts, and tests resolvable inside the checkout.

### What it does not do

It does not access the network, call GitHub, run models or providers, start Ollama, expose routes, run benchmarks, or promote evidence. Passing this checker means the scanned doc paths and selected-next statements are internally consistent; it is not evidence of runtime readiness.

## Packet consistency checker

Command source: `scripts/check_local_llm_packet_consistency.py`.

### What it protects

The packet consistency checker protects packet continuity after the accepted Level 2 and Level 3 tracks. It checks discovered local LLM orchestration packet directories for selected-next files, blocker fallback files, evidence-boundary or blocked-claim files, expected final decision markers, and contradictory selected-next state. It also checks the operator guide selected-next state and the index decision ledger/lane map.

### What it does not do

It does not run local models, call Ollama, call hosted providers, exercise `/v1/solve` or dashboard routes, deploy, benchmark, bill, or promote evidence. Passing this checker means packet metadata and decision markers remain coherent; it does not authorize a new implementation, validation, or release-readiness lane.
