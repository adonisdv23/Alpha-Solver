# Risk Register

This register lists risks a future lane must address if smoke evidence later supports runtime integration planning. It is not a claim that any risk has been mitigated.

| Risk | Why it matters | Future mitigation needed |
| --- | --- | --- |
| Machine-specific behavior | Local model performance and behavior may vary by hardware, OS, and local runtime setup. | Capture machine context in future raw artifacts and avoid broad generalization. |
| Model availability | Operator-selected local models may not be installed or may differ across machines. | Record exact operator-approved model name and installation assumptions in future evidence. |
| Latency on low-RAM machines | Local inference may be slow or fail on constrained machines. | Require finite timeouts and record latency/error outcomes without readiness claims. |
| Timeout handling | Long-running calls can block runtime paths or produce inconsistent failures. | Prove bounded timeout behavior and SAFE-OUT mapping before runtime use. |
| Prompt echo | Some local models may echo prompts or system content. | Add future parser and response-quality checks before exposing runtime output. |
| Malformed response | Local endpoints may return invalid JSON, missing assistant text, or unexpected schemas. | Require fail-closed parsing and structured error handling evidence. |
| Endpoint misconfiguration | Incorrect endpoint URLs can route to nonlocal or unintended services. | Keep endpoint-locality hardening and no-hosted-fallback proof as prerequisites. |
| Evidence-boundary drift | Planning notes may be misread as readiness or quality evidence. | Preserve blocked-claims and evidence-boundary language in future lanes. |
| Accidental provider fallback | Runtime fallback could mask local-provider failures with hosted-provider output. | Require explicit no-hosted-fallback proof before runtime integration. |
