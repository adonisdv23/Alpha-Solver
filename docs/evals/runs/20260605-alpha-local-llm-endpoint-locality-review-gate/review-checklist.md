# Review Checklist

Lane ID: `ALPHA-LOCAL-LLM-ENDPOINT-LOCALITY-REVIEW-GATE-001`

- [x] Endpoint validation occurs before injected transport invocation.
- [x] Hosted URLs fail closed before transport invocation.
- [x] Non-loopback IP endpoints fail closed before transport invocation.
- [x] Malformed and empty endpoints fail closed before transport invocation.
- [x] 127.0.0.1 loopback endpoint can reach injected fake transport.
- [x] localhost loopback endpoint can reach injected fake transport.
- [x] IPv6 loopback endpoint can reach injected fake transport.
- [x] Stable reason code is `endpoint_not_local_non_evidence`.
- [x] `behavior_evidence` remains false.
- [x] No real network, provider, local model, `/v1/solve`, dashboard, or Batch C work was added.
- [x] Evidence boundary remains offline/non-evidence only.
