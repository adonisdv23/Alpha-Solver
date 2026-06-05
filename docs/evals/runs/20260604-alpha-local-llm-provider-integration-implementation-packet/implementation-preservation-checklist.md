# Implementation Preservation Checklist

A later implementation lane must preserve every item below.

## Adapter identity

- [ ] Keep `provider_mode="local_llm"`.
- [ ] Do not reinterpret `MODEL_PROVIDER=local`; it remains smoke-only unless a
  later approved implementation lane explicitly changes it.
- [ ] Do not substitute v91 deterministic fallback output for backend output.

## Portable contract

- [ ] Preserve the portable-contract path in metadata.
- [ ] Preserve the SHA-256 fingerprint in metadata.
- [ ] Preserve `prompt_source_fingerprint_algorithm="sha256"`.
- [ ] Fail closed on expected-fingerprint mismatch before backend access.
- [ ] Fail closed on missing or empty contract before backend access.

## Prompt separation

- [ ] Keep system/contract content separate from user prompt content.
- [ ] Preserve message order when mapping to the Ollama-style payload.
- [ ] Reject prompt echo of either user prompt or system/contract content.

## Provider boundary

- [ ] Keep the backend default-off.
- [ ] Keep no-provider-by-default behavior.
- [ ] Require explicit opt-in for any live local HTTP path.
- [ ] Do not call hosted providers or alternate backends on failure.
- [ ] Require finite timeout and no infinite retries.

## Evidence labels

- [ ] Keep offline fixture output labeled as offline parser or mapping evidence
  only.
- [ ] Keep `behavior_evidence=False` for adapter outputs in this lane family
  unless a later explicit evidence lane changes the label with authorization.
- [ ] Do not claim runtime readiness, quality, comparison, Batch C, benchmark,
  billing, or provider-orchestration conclusions from packet or fixture output.
