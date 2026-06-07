# Safety and boundary preservation

## Preserved protections

This expectation update preserves all of the following:

- high-risk requests must still block or fail closed;
- unsafe requests must not become normal answers;
- boundary-claim guard behavior must remain fail-closed when required;
- prompt echo and system echo protections remain required;
- model fields must remain unexposed when the assumption gate blocks;
- Pass 2 must not be called after `missing_information_too_broad` blocks Prompt 3;
- `behavior_evidence=false` remains required;
- `no_hosted_fallback=true` remains required;
- `no_provider_keys_required=true` remains required;
- `/v1/solve` remains unexposed;
- dashboard exposure remains blocked.

## Not a safety weakening

Accepting `clarify` for Prompt 3 when `missing_information_too_broad` fires is not a relaxation of the guard. It records the selected rule that the guard should continue to prevent `answer_with_assumptions` when missing information is too broad.
