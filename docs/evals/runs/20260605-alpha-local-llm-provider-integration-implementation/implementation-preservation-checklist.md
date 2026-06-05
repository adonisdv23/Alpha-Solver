# Implementation Preservation Checklist

- [x] Existing adapter seam remains injected-backend based.
- [x] Backend remains default-off without an injected transport.
- [x] Default tests use fake transports or static dictionaries only.
- [x] `provider_mode` remains `local_llm`.
- [x] `MODEL_PROVIDER=local` remains separate from this adapter mode.
- [x] Portable contract path metadata remains present.
- [x] Portable contract SHA-256 fingerprint metadata remains present.
- [x] Fingerprint mismatch fails before backend invocation.
- [x] System contract and user prompt are separate request messages.
- [x] `behavior_evidence` remains `False`.
- [x] Documentation selects exactly one next lane.
