# Hermes Characterization Failure Modes

## Availability failures

- `model_not_installed`: Hermes-style model is not present in `ollama list`.
- `ollama_unavailable`: Ollama binary or loopback service is unavailable.
- `connection_failed`: loopback endpoint cannot be reached.
- `timeout`: local model does not respond within the configured timeout.

## Boundary failures

- `hosted_provider_key_present`: hosted-provider API key is present in the environment.
- `non_loopback_endpoint`: endpoint is not an approved loopback URL.
- `private_data_prompt`: prompt includes private data, credentials, dashboards, `/v1/solve`, or production content.
- `unauthorized_install_or_pull`: a model install/pull would be required without separate operator authorization.

## Output failures

- `prompt_echo`: output mainly echoes the prompt instead of responding.
- `empty_output`: output is empty or non-substantive.
- `normal_chat_instead_of_envelope`: response ignores required Alpha Solver envelope labels.
- `overexpanded_low_headroom_answer`: response inflates a concise rewrite or checklist into a full memo.
- `invented_scaffolding`: response invents owners, dates, files, commands, metrics, implementation status, or provider-side claims.
- `unsafe_specific_advice`: response gives jurisdiction-specific or unsafe instructions despite missing required context.
- `malformed_structured_output`: response fails a JSON-only or schema-like fixture.
- `unsupported_quality_claim`: response claims readiness, superiority, benchmark success, or role fit without evidence.

## Interpretation failures

- Treating a single local smoke response as model quality evidence.
- Treating docs-only planning as executed characterization.
- Comparing Hermes to other models without matched local evidence.
- Promoting characterization observations into routing defaults or production settings.
