# Adapter Design

## Design target

The adapter seam is a narrow request-construction and injected-backend handoff
layer. It is intentionally separate from the existing fake-client
contract-consumption proof while reusing the same portable contract loader.

## Request shape

The adapter request contains:

- `system`: the full text loaded from `alpha_solver_portable.py`.
- `user_prompt`: the caller-supplied user prompt.
- `messages`: a two-entry tuple with a `system` message for the portable
  contract and a `user` message for the user prompt.
- `metadata`: prompt-source path, SHA-256 fingerprint, fingerprint algorithm,
  adapter mode, backend class, model label, and non-evidence flags.

## Mode label

The adapter accepts only `provider_mode="local_llm"`. Passing
`provider_mode="local"` fails closed so existing `MODEL_PROVIDER=local` remains
smoke-only until a separate approved lane changes it.

## Backend behavior

The adapter accepts an injected backend implementing `generate(request) -> str`.
The included stub backend records calls and returns configured text without
network, local model, Ollama, OpenAI, Anthropic, or hosted-provider access.

## Failure behavior

The adapter reports `failed_closed` non-evidence results for:

- missing, unreadable, empty, or fingerprint-mismatched portable contracts;
- empty model output;
- prompt echo;
- injected-backend errors.

Successful stub output remains wiring-only non-evidence.
