# Runtime Risk Register

Lane ID: `ALPHA-LOCAL-LLM-RUNTIME-INTEGRATION-PLANNING-001`

This register identifies risks for a future specification or implementation lane. It does not claim that any risk has been mitigated.

| Risk | Why it matters | Future mitigation to specify |
| --- | --- | --- |
| Provider-selection ambiguity | Operators and runtime paths may disagree about whether hosted or local backend is active. | Define a single source of truth for provider mode and surface backend provenance. |
| Backend registry drift | Adding local providers can create duplicate names, inconsistent availability checks, or hidden defaults. | Require deterministic backend identifiers and explicit unavailable-backend behavior. |
| Local endpoint misconfiguration | A mistyped endpoint could fail, point to an unintended service, or violate locality expectations. | Require local-endpoint validation and fail-closed configuration errors. |
| Model availability variance | Local model names and installed artifacts vary by operator machine. | Require explicit model configuration and clear unavailable-model errors. |
| Hardware-dependent latency | Local inference latency can vary significantly by CPU/GPU/RAM and model size. | Require finite timeouts, latency capture, and operator-facing timeout guidance. |
| Unbounded waits | Local services can hang or stream slowly. | Define connect/read/total timeout behavior and runtime-safe cancellation boundaries. |
| Malformed response | Local endpoints may return unexpected schemas or partial output. | Require strict parsing, typed error categories, and no unsafe best-effort coercion. |
| Empty output | A local call may complete without usable assistant text. | Map empty output to a visible local-provider error or SAFE-OUT path defined by spec. |
| Prompt echo | Some local models may echo instructions, prompt text, or system content. | Specify echo detection requirements before exposing output through runtime paths. |
| Silent hosted fallback | Fallback could hide local failures and create privacy/cost confusion. | Prohibit silent fallback; require explicit opt-in, provenance labels, and artifact proof if allowed. |
| Operator configuration burden | Local runtime setup can be unclear for operators. | Provide operator configuration docs, disablement instructions, and clear failure messages. |
| Evidence-boundary drift | Planning artifacts may be cited as runtime or quality evidence. | Preserve explicit boundary language in future spec and implementation packages. |
