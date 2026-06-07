# Artifact Preservation Guidance

## Not every local run needs preservation

Casual Level 2 local usage does not automatically create evidence. Most local operator runs should remain transient development inspection unless a lane explicitly asks for preservation.

## When to preserve an artifact

Preserve an artifact when:

- a lane explicitly requests a source artifact;
- a failure mode or stop condition requires review;
- a diagnostic regression needs bounded inspection;
- an import/final-decision lane needs a source record;
- future planning requires provenance without making readiness or quality claims.

## Source artifact contents

A preserved source artifact should include:

- command provenance with environment values redacted or summarized where appropriate;
- local endpoint summary, not unnecessary raw endpoint detail;
- model identifier;
- finite timeout;
- prompt identifier or bounded prompt summary if redaction requires it;
- normalized output JSON;
- `metadata.gate_trace` inspection;
- explicit `behavior_evidence=false`, `no_hosted_fallback=true`, and `no_provider_keys_required=true` confirmation;
- non-claims and blocked-use statement.

## Import and final-decision lanes

Create an import/final-decision lane when preserved artifacts must be reviewed, classified, and recorded as bounded docs/evidence/provenance material. Do not use import/final-decision lanes to convert local usage into production readiness, benchmark evidence, model-quality evidence, provider orchestration evidence, or evidence-model promotion.

## Avoid accidental evidence claims

Do not promote casual local usage by changing labels, omitting caveats, or summarizing outputs as proof. Preserve artifacts only inside their approved boundary and keep the non-evidence flags visible.
