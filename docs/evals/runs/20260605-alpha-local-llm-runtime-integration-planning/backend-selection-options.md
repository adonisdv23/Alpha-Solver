# Backend Selection Options

Lane ID: `ALPHA-LOCAL-LLM-RUNTIME-INTEGRATION-PLANNING-001`

This file compares possible backend strategies for a future specification. It does not select a winner.

## Option A: Hosted provider only

### Description

Alpha runtime continues to use only hosted provider paths for LLM-backed behavior. Local LLM support remains outside runtime integration.

### Potential advantages

- Simpler runtime configuration surface.
- Fewer machine-specific setup variables.
- Existing hosted-provider observability and operational patterns may remain the primary focus.
- Less risk of local endpoint misconfiguration affecting operator runs.

### Potential tradeoffs

- No optional machine-local backend path for operators who want one.
- Continued dependency on hosted-provider availability, credentials, policy, and cost model.
- Does not exercise or preserve a local-provider adapter path in runtime.
- May not address operator environments where hosted-provider calls are unavailable or undesirable.

### Spec questions

- Should local LLM work remain limited to adapter-level experiments outside runtime?
- What operator documentation is needed to prevent confusion about unsupported local runtime modes?
- What evidence would be required before reconsidering local runtime integration later?

## Option B: Local LLM only

### Description

Alpha runtime uses only a local LLM backend for the affected LLM-backed path, with no hosted-provider fallback in that mode.

### Potential advantages

- Clear locality boundary if endpoint guardrails are strict.
- No hosted-provider key requirement for that mode.
- Failures can be made visible without ambiguity about fallback source.
- Useful for isolating local-provider behavior in future controlled evaluation lanes.

### Potential tradeoffs

- Strong dependence on operator machine setup, installed model, local service availability, and hardware capacity.
- Higher risk of variable latency, malformed responses, empty outputs, or model-specific behavior.
- Requires careful timeout, parsing, and error mapping to prevent runtime disruption.
- May be harder to support consistently across operator environments.

### Spec questions

- What exact configuration proves the endpoint is local and operator-approved?
- What response schema and parser behavior must be enforced?
- How should unavailable model, unavailable endpoint, timeout, malformed response, and empty output errors surface?

## Option C: Hybrid provider strategy

### Description

Alpha runtime supports both hosted and local backends, with explicit provider selection rules and possibly explicit fallback rules.

### Potential advantages

- Gives operators a configurable choice between hosted and local backends.
- Could support local-only runs where desired and hosted-only runs where local setup is absent.
- Allows future comparison lanes to examine operational differences under controlled boundaries.
- Can preserve hosted paths while adding a separately labeled local path.

### Potential tradeoffs

- More complex provider selection, configuration, observability, and documentation.
- Fallback behavior can obscure which backend produced output unless labels and audit fields are explicit.
- Cost/privacy expectations can become confusing if fallback is implicit or poorly surfaced.
- More test and smoke coverage would be required before any implementation lane could be accepted.

### Spec questions

- Is fallback prohibited, opt-in, or request-scoped?
- How is backend provenance surfaced to operators and logs?
- What behavior occurs when local provider selection is configured but unavailable?
- How are hosted credentials handled when an operator intends local-only operation?

## Non-selection statement

This planning package does not choose among Option A, Option B, or Option C. A later spec lane must preserve this tradeoff analysis and make any selection only within its approved scope.
