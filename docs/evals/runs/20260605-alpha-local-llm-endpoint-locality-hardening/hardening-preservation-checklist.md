# Hardening Preservation Checklist

Lane ID: `ALPHA-LOCAL-LLM-ENDPOINT-LOCALITY-HARDENING-001`

- [x] Added endpoint-locality validation before transport invocation.
- [x] Rejected non-loopback / non-local endpoints with `endpoint_not_local_non_evidence`.
- [x] Added tests proving hosted endpoints fail closed without transport invocation.
- [x] Preserved loopback endpoint support for injected fake transports.
- [x] Preserved backend default-off behavior.
- [x] Preserved no-provider-by-default behavior.
- [x] Preserved `provider_mode="local_llm"`.
- [x] Preserved `MODEL_PROVIDER=local` as separate smoke-only semantics.
- [x] Preserved portable-contract path, SHA-256 fingerprint, fingerprint algorithm, and system/user separation.
- [x] Preserved `behavior_evidence=False`.
- [x] Preserved offline/non-evidence labels.
- [x] Did not run smoke.
- [x] Did not call Ollama, a local model, a hosted provider, `/v1/solve`, dashboard preview, or Batch C.
