# Provider Identity Fields

## Required identity fields

A future provider registry entry should require these identity fields:

| Field | Requirement |
| --- | --- |
| `provider_id` | Stable machine-readable identifier, unique within the registry. |
| `display_name` | Human-readable provider name for operator review. |
| `provider_family` | Provider family or adapter family, such as local runtime, hosted API, or bridge adapter. |
| `integration_owner` | Responsible maintainer or owning lane; may be `unassigned` until implementation is authorized. |
| `registry_version` | Schema version used by the entry. |
| `entry_status` | One of `draft`, `review_only`, `disabled`, `eligible_for_future_review`, or another Level-7-approved state. |
| `source_packet` | Packet or spec that authorized the entry. |
| `last_reviewed_at` | Date of last docs review; must not imply runtime validation. |

## Optional identity fields

A future entry may include optional labels only if Level 7 authorizes them:

- `adapter_module` for an existing adapter path, if code already exists;
- `provider_docs_url` for external documentation reference;
- `credential_profile_name` for a future credential-policy label, not a secret value;
- `model_catalog_reference` for a docs-only model catalog pointer; and
- `deprecation_note` for retired or blocked providers.

## Identity constraints

- Identity fields must not contain secrets, API keys, tokens, account IDs, private endpoints, or billing credentials.
- Identity fields must not imply that the provider can be called.
- Identity fields must not imply readiness for provider orchestration, fallback, `/v1/solve`, dashboard exposure, benchmarks, billing, or evidence promotion.
