# Evidence boundary

This packet is based on committed repository files and offline static checks. It
reviewed registry contents, existing DEF-002 and public-exposure evidence
packets, and local code paths for policy loading, telemetry, replay, logging,
registry snapshots, and redaction. During validation, a broad `python -m pytest
-q` run was attempted in an environment that exercised an OpenAI provider path;
that incident is recorded as a boundary violation and is not used as provider
safety evidence.

## Included evidence

- Registry and config files under `registries/` and `config/`.
- Existing DEF-002 security/privacy review packet and public-exposure readiness
  gate packet.
- Local source modules for registry loading, policy classification, governance
  classification, provider telemetry, JSONL logging, replay, registry snapshots,
  and Self Operator redaction.
- Targeted local-only tests and static docs checks run from the repository checkout with `MODEL_PROVIDER=local` controls.

## Excluded evidence

- Live provider behavior, except for the recorded broad-suite validation incident,
  which is treated only as a boundary violation and failed validation signal.
- Provider-readiness evidence, provider-safety validation, token billing, or model
  usage evidence.
- Public API or dashboard exposure.
- External vendor policy review.
- Runtime proof that every prompt, trace, replay event, evidence packet, log, and
  dashboard datum is classification-enforced.
