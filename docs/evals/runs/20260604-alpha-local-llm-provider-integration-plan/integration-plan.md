# Integration Plan

## Current seam to preserve

The current adapter seam builds a request from the portable contract and an
explicit user prompt, then hands that request to an injected backend. A future
implementation must keep that seam shape rather than bypassing it.

Preserved request properties:

- portable contract text is system/contract content;
- user prompt remains a separate user field/message;
- prompt-source path is retained;
- SHA-256 fingerprint is retained;
- fingerprint algorithm is retained;
- `provider_mode="local_llm"` remains the adapter label;
- `MODEL_PROVIDER=local` remains smoke-only unless a later approved lane
  explicitly changes it.

## Future implementation sequence

1. Create or update a `.specs/` implementation contract before code changes.
2. Add an explicit authorization gate covering provider class, endpoint shape,
   local environment, allowed commands, and evidence labeling.
3. Implement an adapter backend behind the existing injected-backend protocol.
4. Keep default behavior inert unless explicit configuration and authorization
   are present.
5. Add offline stub/fixture tests first.
6. Add serialization and response-normalization tests without live provider
   execution.
7. Only after a separate authorization decision, add a narrow local-provider
   smoke test that is opt-in, skipped by default, and labeled separately from
   offline evidence.
8. Keep runtime entrypoints, dashboard preview, hosted providers, and `/v1/solve`
   out of scope unless a later lane explicitly authorizes them.

## Data flow for a future backend

1. Caller supplies a user prompt and optional expected portable-contract
   fingerprint.
2. Existing loader reads `alpha_solver_portable.py` and computes SHA-256.
3. Adapter builds the request with separate system/contract and user content.
4. Future backend converts the adapter request into the chosen local-provider
   wire shape.
5. Backend applies a timeout and parses the response into plain output text.
6. Adapter failure checks reject empty output, prompt echo, malformed response,
   backend errors, and contract errors.
7. Result metadata preserves source path, fingerprint, algorithm, provider mode,
   backend class, and evidence labels.

## Review gates before code

A future implementation must document:

- exact files to change;
- exact provider option selected;
- exact offline tests to add;
- exact opt-in smoke command, if any;
- default-disabled behavior;
- credential policy;
- rollback plan;
- evidence label and non-claim wording.
