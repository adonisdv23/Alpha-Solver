# Adapter Safe Next Options

This review gate recommends one preferred next lane and lists bounded safe
alternatives only if the preferred lane is deferred.

## Preferred recommendation

Recommended next lane:
`ALPHA-LOCAL-LLM-PROVIDER-INTEGRATION-PLAN-001`

Purpose: create a plan/review-only lane that defines requirements for a future
local-provider integration without executing a real provider.

The preferred lane must remain non-executing. It may draft integration plans,
required specs, safety checks, offline fixtures, and authorization criteria. It
must not call a local model, Ollama, hosted providers, `/v1/solve`, or dashboard
preview paths.

## Bounded safe alternatives

If the preferred lane is deferred, acceptable alternatives are:

1. A docs-only evidence-boundary refresh for the local LLM seam.
2. A docs-only spec-drafting lane for provider-call authorization requirements.
3. A tests-only offline fixture review lane that continues to use injected
   stubs and does not add real provider calls.

## Unsafe next work

The next lane must not be a real-provider execution lane. It must not perform
runtime integration, provider-key setup, Ollama smoke execution, local model
execution, hosted-provider execution, `/v1/solve` calls, dashboard preview work,
operator-test interpretation, PR #288 or PR #289 evidence changes, Batch C work,
or readiness/superiority assertions.
