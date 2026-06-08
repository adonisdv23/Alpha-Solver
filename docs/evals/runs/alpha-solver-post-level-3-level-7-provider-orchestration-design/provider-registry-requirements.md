# Provider Registry Requirements

## Registry requirement

Future provider orchestration must use an explicit provider registry before selecting or calling any provider. The registry must be allowlist-based, deterministic for a given configuration, auditable, and safe to inspect without exposing secrets.

## Required provider fields

A provider registry entry must define, at minimum:

- stable provider identifier;
- human-readable display name;
- supported model identifiers or model-set identifiers;
- capability flags such as chat, structured output, streaming support, tool use, embeddings, or local-only operation where applicable;
- endpoint class such as local loopback, hosted provider, or disabled;
- credential requirement class without storing credential values;
- maximum allowed input/output token limits or equivalent request bounds;
- default timeout and maximum timeout;
- retry eligibility;
- fallback eligibility;
- cost-accounting support and cost-source class;
- quota-accounting support;
- provenance metadata fields returned or unavailable;
- safety-gate compatibility;
- environment constraints and deployment constraints;
- disabled-by-default status unless a future accepted lane explicitly authorizes enablement.

## Registry safety requirements

The registry must not contain API keys, bearer tokens, authorization headers, raw credential values, raw prompts, raw provider payloads, raw exception dumps, billing account identifiers, or environment dumps. Registry output must be allowlist-built rather than redacted after broad capture.

## Capability requirements

Provider selection must only use declared capabilities. A provider must be ineligible when required capabilities are missing, unknown, contradictory, disabled, out of policy, over quota, over budget, or unable to satisfy safety and provenance requirements.
