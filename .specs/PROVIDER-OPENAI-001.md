# PROVIDER-OPENAI-001 · Real OpenAI Provider Execution

## 1. Goal

Add explicitly opt-in real OpenAI execution for Alpha Solver through a provider client abstraction, first consumed by FastAPI `/v1/solve`, while preserving local/offline defaults, deterministic fallback behavior, SAFE-OUT semantics, credential safety, and default CI without real credentials.

## 2. Non-goals

- Do not make remote provider execution the default.
- Do not modify `alpha_solver_portable.py`.
- Do not change deterministic ToT/ReAct fallback behavior except as explicitly defined by this or a future implementation spec.
- Do not add Anthropic, Gemini, or Deepseek real execution.
- Do not add UI key management.
- Do not add real API keys.
- Do not require GitHub Actions secrets in default CI.
- Do not make `scripts/check_env.py` perform live provider pings by default.
- Do not change model-set routing into a provider executor.
- Do not weaken no-secret logging guarantees.

## 3. Architecture decision

The first implementation must add a new provider/client abstraction rather than adding provider execution to existing prompt-rendering surfaces. Likely future files are:

- `alpha/providers/base.py`
- `alpha/providers/openai.py`
- optionally `alpha/providers/fake.py` for tests

Architecture rules:

- Do not overload `alpha/adapters/openai.py`; provider adapters remain prompt renderers.
- Do not put raw OpenAI logic directly into `service/app.py`.
- FastAPI `/v1/solve` is the first runtime consumer after the provider client exists.
- CLI paths, prompt writer, package/root CLI, and portable solver remain local/offline initially.

## 4. Acceptance criteria

- A new provider client contract exists and is tested with fake/mocked clients.
- Real OpenAI execution is reachable only when explicitly enabled, for example `MODEL_PROVIDER=openai` plus `OPENAI_API_KEY`.
- `.env.example` remains local/offline by default.
- Default CI passes without real API keys.
- Tests prove `OPENAI_API_KEY` is discovered from environment but never logged or returned.
- Provider errors normalize into a typed error shape and route through SAFE-OUT/fallback behavior.
- Token usage and cost accounting are recorded from provider response usage when available, or marked unknown without fabricating accuracy.
- Timeout and retry behavior are deterministic in tests and bounded by config/model-set timeout values.
- `/v1/solve` remains compatible for local/offline requests and existing tests.
- `alpha_solver_portable.py`, CLI smoke paths, and adapter prompt-writing tests remain local/offline.

## 5. Input contract

The provider abstraction should accept a request shape equivalent to:

```python
ProviderRequest(
    prompt: str,
    system: str | None,
    model: str,
    max_tokens: int,
    timeout_ms: int,
    temperature: float | None,
    seed: int | None,
    metadata: {
        "request_id": str,
        "route": str | None,
        "model_set": str | None,
        "tenant": str | None,
    },
)
```

Contract notes:

- `prompt` is the already-rendered prompt passed to the provider client.
- `system` is optional and may be omitted by local/offline-compatible call sites.
- `model` is resolved before provider execution; model-set routing must not become provider execution.
- `timeout_ms` must be bounded by selected config/model-set values.
- `metadata` is for correlation and policy decisions; it must not include credentials or raw secret-bearing headers.

## 6. Output contract

The provider abstraction should return a result shape equivalent to:

```python
ProviderResult(
    provider="openai",
    model="...",
    text="...",
    finish_reason="stop" | "length" | "content_filter" | "tool_calls" | "unknown",
    usage={
        "input_tokens": int | None,
        "output_tokens": int | None,
        "total_tokens": int | None,
    },
    cost={
        "estimated_usd": float | None,
        "source": "price_hint" | "provider" | "unknown",
    },
    latency_ms=int,
    request_id=str,
    raw_metadata={... no secrets ...},
)
```

Contract notes:

- `text` is the provider response text normalized for the existing solver response path.
- `usage` must use provider-reported token counts when available.
- `cost.estimated_usd` must be `None` when neither provider cost nor trustworthy price hints are available.
- `raw_metadata` may include safe provider identifiers and finish metadata, but never credentials, authorization headers, raw request bodies, or unredacted prompts.

## 7. Error contract

The provider abstraction should normalize failures into a typed shape equivalent to:

```python
ProviderError(
    provider="openai",
    category=(
        "missing_credentials"
        | "auth"
        | "rate_limit"
        | "timeout"
        | "network"
        | "provider_5xx"
        | "invalid_request"
        | "content_filter"
        | "unknown"
    ),
    retryable=bool,
    safe_message=str,
    status_code=int | None,
    request_id=str | None,
)
```

`safe_message` must never contain API keys, headers, raw request bodies, or full provider exception strings. Missing credential errors may identify the missing environment variable name, such as `OPENAI_API_KEY`, but must never include the variable value.

## 8. Timeout and retry behavior

- Use the selected model-set `timeout_ms` when available.
- Default to one attempt plus at most one retry for retryable categories unless a future spec expands this behavior.
- Do not retry `auth`, `missing_credentials`, `invalid_request`, or `content_filter` failures.
- Use bounded backoff with a deterministic fake clock in tests.
- Timeout behavior must not hang API tests.
- Retry decisions must be deterministic and covered by fake/mocked provider tests.

## 9. Budget and cost accounting

- Do not rely only on the duration-cost shim.
- Use provider token usage when available.
- Use model-set price hints for estimated cost when available.
- If usage is unavailable, record cost as unknown instead of guessing.
- Provider budget decisions should happen before remote calls when estimates exceed hard caps and after calls when actual usage returns.
- Budget and cost events must not include credentials, raw prompts, or provider headers.

## 10. Telemetry

Implementations must emit structured telemetry events without secrets:

- `provider.request.started`
- `provider.request.completed`
- `provider.request.failed`
- `provider.request.timeout`
- `provider.fallback.local`

Telemetry payloads should include:

- provider name
- model
- model_set
- latency_ms
- token usage
- estimated_cost_usd
- status category
- retry_count
- request_id

Prompt text is excluded by default unless a future explicit redaction policy allows sanitized prompt capture. Telemetry must not contain API keys, authorization headers, raw request bodies, full provider exception strings, or other secret-bearing fields.

## 11. SAFE-OUT and fallback

- Provider errors must flow into SAFE-OUT or deterministic local fallback, not raw provider exceptions.
- `service/app.py` already has generic SAFE-OUT wrapping; provider errors should be mapped intentionally before generic fallback.
- Do not change `alpha/core/router.py` in the first implementation.
- Do not change portable SAFE-OUT/envelope behavior.
- Local/offline behavior remains the compatibility baseline for `/v1/solve` when OpenAI execution is not explicitly enabled.

## 12. Credential rules

- Use only `OPENAI_API_KEY` for OpenAI provider execution.
- `.env.example` remains `MODEL_PROVIDER=local` by default.
- `scripts/check_env.py` validates presence only and does not ping OpenAI by default.
- No provider key may appear in logs, config dumps, telemetry, test snapshots, trace files, responses, or errors.
- Missing credential errors may name `OPENAI_API_KEY` but must not include its value.
- Optional live smoke tests require both `ALPHA_LIVE_OPENAI=1` and `OPENAI_API_KEY`; default CI must not require secrets.

## 13. Test plan

| Test area | Uses real API key? | Default CI? | Purpose | Required before merge? |
| --- | --- | --- | --- | --- |
| Provider contract unit tests with fake OpenAI transport/client | No | Yes | Prove request/result/error contracts, normalization, and fake client behavior without network calls. | Yes |
| Missing credential tests | No | Yes | Prove `MODEL_PROVIDER=openai` without `OPENAI_API_KEY` returns a typed `missing_credentials` error and safe message. | Yes |
| Config validation drift tests | No | Yes | Keep `.env.example`, config validation, and provider env expectations aligned without live pings. | Yes |
| Service `/v1/solve` local/offline regression tests | No | Yes | Prove local/offline requests remain compatible and existing API tests keep passing. | Yes |
| Service `/v1/solve` fake OpenAI tests | No | Yes | Prove explicit OpenAI mode can be exercised through fake/mocked provider execution. | Yes |
| Failure-mode tests | No | Yes | Prove auth, rate-limit, network, provider 5xx, invalid request, content filter, and unknown failures map to typed errors. | Yes |
| Timeout tests | No | Yes | Prove bounded `timeout_ms` behavior and no hanging API tests using fake clocks/transports. | Yes |
| Retry/backoff tests | No | Yes | Prove one attempt plus at most one retry for retryable failures and no retry for non-retryable failures. | Yes |
| Budget/cost tests | No | Yes | Prove token usage, price hints, unknown cost handling, and before/after remote-call budget decisions. | Yes |
| Telemetry tests | No | Yes | Prove structured provider events include required safe fields and exclude prompt text/secrets by default. | Yes |
| No-secret logging tests | No | Yes | Prove `OPENAI_API_KEY` values never appear in logs, dumps, telemetry, snapshots, traces, responses, or errors. | Yes |
| Adapter prompt-rendering regression tests | No | Yes | Prove existing prompt adapters remain renderers and are not overloaded with provider execution. | Yes |
| Prompt writer regression tests | No | Yes | Prove prompt writer paths remain local/offline and unchanged by provider execution. | Yes |
| CLI smoke/regression tests | No | Yes | Prove package/root CLI and smoke paths remain local/offline initially. | Yes |
| Optional live smoke test gated by env | Yes | No | Prove real OpenAI connectivity only when both `ALPHA_LIVE_OPENAI=1` and `OPENAI_API_KEY` are set. | No |
| Replay determinism tests | No | Yes | Prove deterministic local fallback/replay behavior is preserved and provider failures do not destabilize replay. | Yes |

## 14. Dependency decision

- Do not add dependencies in the spec-only PR.
- For implementation, prefer existing `httpx` first unless the implementation spec explicitly chooses the official OpenAI SDK.
- If the official SDK is later chosen, it must be pinned and mocked at the boundary.
- No default live calls.

## 15. Runtime readiness doc decision

- `docs/RUNTIME_READINESS.md` is useful after this provider spec.
- It should not replace the spec.
- It should summarize local/offline, env-validation-only, mocked provider, optional live smoke, and production readiness states.
- Do not create it in this PR.
