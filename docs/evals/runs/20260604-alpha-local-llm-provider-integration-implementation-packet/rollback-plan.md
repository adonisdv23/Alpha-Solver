# Rollback Plan

This rollback plan applies to a later implementation lane. The current packet
adds docs only.

## If future implementation code is added

1. Disable the opt-in flag so the backend cannot initiate local HTTP traffic.
2. Revert or remove the Ollama-style backend class or helper functions from
   `alpha/local_llm/provider_adapter.py`.
3. Remove any public exports added in `alpha/local_llm/__init__.py`.
4. Remove or quarantine offline fixtures and tests introduced solely for the
   backend implementation if they no longer apply.
5. Confirm `provider_mode="local_llm"` remains the adapter mode for existing
   inert seams.
6. Confirm `MODEL_PROVIDER=local` remains smoke-only unless an approved lane has
   explicitly changed that meaning.
7. Confirm portable-contract path, SHA-256 fingerprint metadata, fingerprint
   algorithm, and system/user separation are preserved.
8. Run focused local LLM adapter tests and relevant docs checks.
9. Record rollback evidence in a lane-specific docs directory without modifying
   unrelated operator evidence.

## If future smoke execution is authorized and then must be rolled back

1. Remove or unset the smoke opt-in environment flag.
2. Stop any local model process outside the repository workflow.
3. Delete any temporary local endpoint configuration from the test environment.
4. Re-run offline tests to confirm the default-off path.
5. Keep smoke evidence labeled separately and do not use it for runtime,
   readiness, comparison, billing, benchmark, or provider-orchestration
   conclusions.

## Current packet impact

Rollback for this packet is limited to deleting this docs directory before merge
or reverting the docs-only commit after merge.
