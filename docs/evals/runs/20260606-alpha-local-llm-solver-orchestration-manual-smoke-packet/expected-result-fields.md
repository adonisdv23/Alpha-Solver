# Expected Result Fields

Future manual smoke output must capture the fields below for each prompt or at packet level where noted. The canonical solver orchestration spec requires `answer`; the current smoke/eval scaffold also preserves `final_answer`.

## Required normalized result fields

- `provider_mode`: expected `local_llm`.
- `orchestration_mode`: expected `non_production_local_solver_orchestration`.
- `strategy`: expected `local_expert_two_pass`.
- `pass_count`: expected `1` or `2` depending on gate path.
- `mode`: one of `direct`, `clarify`, `answer_with_assumptions`, or `block`.
- `considerations`: list or empty list.
- `assumptions`: list or empty list.
- `confidence`: number or null.
- `answer`: string required by the canonical solver orchestration spec; may be empty for fail-closed or blocked outcomes.
- `final_answer`: string preserved for the current smoke/eval scaffold shape; may be empty for fail-closed or blocked outcomes.
- `metadata`: object preserving runtime provenance and reason labels.
- `evidence_boundary`: narrow non-production local smoke boundary.
- `behavior_evidence`: must be `false`.
- `no_hosted_fallback`: must be `true`.
- `no_provider_keys_required`: must be `true`.
- `local endpoint summary`: redacted loopback summary only.
- `model`: local model identifier.
- `timeout`: finite timeout used.
- `status`: status label.
- `failure reason if any`: deterministic failure or block reason where available.

## Required packet-level provenance fields

- command provenance;
- Python script provenance;
- stdout capture;
- stderr capture;
- repo status;
- repo HEAD;
- diff name-only output;
- prompt ID and expected mode/outcome;
- started and finished UTC timestamps.
