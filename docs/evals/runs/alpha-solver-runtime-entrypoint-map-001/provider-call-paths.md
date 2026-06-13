# Provider Call Paths

## Live-capable provider path

1. `POST /v1/solve` receives query and context.
2. `sanitize_query` rejects length/control/import-like patterns.
3. `_is_openai_provider_enabled()` returns true only when `MODEL_PROVIDER` is `openai`.
4. The service builds a `ProviderRequest` with prompt, model set, request ID, route, and tenant/provider metadata where available.
5. `_get_provider_client()` returns an `OpenAIProviderClient`.
6. `_execute_provider_call()` emits provider started/completed/failed/timeout telemetry and accounting.
7. `OpenAIProviderClient.execute()` reads `OPENAI_API_KEY` unless injected, then posts to `/responses` on the configured base URL.

## Dashboard preview path

The bundled dashboard mounts only auth plus expert preview. When provider is OpenAI, `alpha/webapp/routes/expert_preview.py` requires `ALPHA_LIVE_PREVIEW_ENABLED` and a positive request cap before allowing live preview flow. This is still unsafe to expose as a public product surface.

## Non-call paths

- Default `MODEL_PROVIDER=local` path uses local `_tree_of_thought` behavior and must not be treated as provider validation.
- `alpha/local_llm/provider_adapter.py` is local-LLM adapter plumbing and does not prove provider readiness.
- `alpha/webapp/routes/requests.py` simulates provider latency; it is not a live provider integration.
- Tests can inject fake transports/clients and do not imply external network calls.

## Provider boundary confirmation

This packet made no provider calls, used no tokens, did not inspect credentials, and did not print environment secrets.
