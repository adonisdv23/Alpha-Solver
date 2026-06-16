# Routing preview rules

The router in `alpha/model_router.py` is deterministic and metadata-only.

## Rules

- If the prompt length is above the smoke-runner limit, return `failed_closed`.
- If no modes are allowed, return `failed_closed`.
- If a requested model is not in the catalog, return `failed_closed`.
- If a requested hosted model is present but hosted providers are not allowed, return `failed_closed`.
- If a requested local model is present but local models are not allowed, return `failed_closed`.
- If an enabled requested model is allowed, select it.
- If no model is requested, select the first enabled OpenAI model when hosted providers are allowed, otherwise select the first enabled local model when local is allowed.
- Return fallbacks from enabled catalog entries that are allowed by the request.
- Always return reasons and preview-only evidence-boundary flags.

## Non-empirical boundary

The router does not choose the best model empirically. Task profile, cost preference, and latency preference are recorded only as reasons, without provider quality, pricing, latency, or benchmark claims.
