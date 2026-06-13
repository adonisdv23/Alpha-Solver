# Provider / API data-sharing boundary review

Covers: what user data crosses the provider boundary, under what gating, and what
telemetry the provider integration emits.

## When data crosses the provider boundary

- By default, **no** prompt content is shared externally. The default provider is
  `local` (`.env.example`), and the provider branch in `/v1/solve` runs only when
  `_is_openai_provider_enabled()` is true (`service/app.py:950`).
- When the OpenAI provider is explicitly enabled, the user `query` is forwarded
  as the provider prompt. The handler builds a provider request with
  `prompt=query` (`service/app.py:266`) and, for the expert route, sends derived
  prompts (`_expert_step_one_prompt(query)` at `service/app.py:987`,
  `_expert_step_two_prompt(query, preview)` at `service/app.py:1002`).

**Data-sharing fact:** With the provider enabled, the user's query/prompt text is
transmitted to the external provider. This is intrinsic to provider-backed
inference and is the central data-sharing boundary for DEF-002. It is gated
behind explicit operator opt-in, not on by default.

## What the integration emits about provider calls

- Provider lifecycle telemetry is **content-free** by construction (see
  `logging-redaction-review.md`): `alpha/providers/telemetry.py` `_ALLOWED_FIELDS`
  contains no prompt/response field, and `emit_provider_event` re-filters through
  the allowlist before logging.
- Provider failures degrade through `alpha/providers/safeout.py`, which builds the
  client-facing body from safe `ProviderError` fields only and never echoes raw
  provider payloads, metadata, or environment/config dumps.

## Accounting / cost

- `alpha/providers/accounting.py` participates in cost/usage accounting; the app
  exposes a `provider_accounting_sink` on app state (`service/app.py`, around the
  startup block). Cost fields surfaced via telemetry are numeric metadata
  (`estimated_cost_usd`, token counts), not content.

## Boundary assessment

| Aspect | Disposition |
| --- | --- |
| Default behavior | Offline; no external data sharing (strong) |
| Provider-enabled prompt transmission | Inherent; gated behind explicit opt-in |
| Telemetry content leakage | Prevented by allowlist (strong) |
| Failure-path payload leakage | Prevented by SAFE-OUT allowlist (strong) |

**Finding (PROV-1):** When a provider is enabled, prompt content leaves the host
to a third-party provider. This is expected for provider-backed inference but
must be governed by an explicit data-processing/disclosure note to operators and
end users (e.g., which provider, what is sent, retention). No such committed
end-user-facing data-sharing disclosure was identified in scope. Tracked in
`risk-register.md` as RR-04 and considered for operator acceptance in
`accepted-residual-risks.md`.

## Summary

The provider boundary is conservative by default and the surrounding telemetry /
failure paths are content-free. The open item is a governance/disclosure gap
around the inherent prompt transmission when a provider is enabled, not a code
leakage defect.
