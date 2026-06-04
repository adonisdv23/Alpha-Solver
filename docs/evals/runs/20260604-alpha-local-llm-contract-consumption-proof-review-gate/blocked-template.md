# Blocked Reviewer Comment Template

Use this template when the future
`ALPHA-LOCAL-LLM-CONTRACT-CONSUMPTION-PROOF-001` PR does not satisfy the review
gate.

```markdown
Blocked for `ALPHA-LOCAL-LLM-CONTRACT-CONSUMPTION-PROOF-001`.

Reviewed against
`ALPHA-LOCAL-LLM-CONTRACT-CONSUMPTION-PROOF-REVIEW-GATE-001`.

Blocking findings:

- [ ] Real model, Ollama, hosted provider, or provider-adapter calls are present.
- [ ] Full Ollama adapter implementation is included.
- [ ] `MODEL_PROVIDER=local` is overloaded beyond smoke-only behavior.
- [ ] The proof silently falls back to `alpha-solver-v91-python.py` or
      `_tree_of_thought`.
- [ ] Prompt source path or fingerprint metadata is missing.
- [ ] The proof lacks tests for portable contract consumption.
- [ ] Fail-closed coverage is missing for contract load, fingerprint mismatch,
      empty output, prompt echo, or fake-client error.
- [ ] Fake-client evidence is described as behavior, quality, validation,
      readiness, superiority, MVP, production, `/v1/solve`, or
      provider-orchestration evidence.
- [ ] Operator tests were executed or imported.
- [ ] Batch C files or materials changed.

Required before reconsideration:

1. Remove all blocked execution paths, claims, or out-of-scope artifacts.
2. Restore the proof to fake-client-only portable contract consumption.
3. Add or repair focused fail-closed tests.
4. Update docs so the evidence boundary is explicit and non-behavioral.

This block does not reject future local LLM work. It only prevents merging a
proof PR that exceeds or fails the required contract-consumption proof boundary.
```
