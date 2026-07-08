# Status Taxonomy

| Status | Meaning | When to use | When not to use | Claim boundary | Operator-facing text |
|---|---|---|---|---|---|
| `present` | Committed source exists. | A named file/folder or packet-family artifact is available. | Do not use as quality proof. | Presence is artifact existence only. | Source present. |
| `missing` | Expected source is absent. | Required source cannot be found for the selected packet. | Do not use when out of scope. | Missing source blocks claims, not necessarily the packet. | Required source not found. |
| `unknown` | This lane did not identify a source. | Source cannot be confirmed. | Do not infer presence. | Unknown status requires conservative wording. | Status unknown. |
| `not_applicable` | Field does not apply. | Packet type does not require the field. | Do not use to hide missing required inputs. | Does not support claims. | Not applicable for this packet. |
| `blocked` | Action or state is not allowed. | Authorization is absent or stop condition applies. | Do not use for completed historical states unless current action is blocked. | Blocks execution or claims. | Blocked; stop or defer. |
| `authorized` | Source truth explicitly allows a bounded action. | A committed authorization packet exists for that action. | Do not infer from artifact presence. | Authorization is action-specific only. | Authorized for this bounded step. |
| `not_authorized` | No source truth authorizes the action. | Runtime/scoring/unblinding/final interpretation lacks explicit approval. | Do not use as a quality judgment. | Prevents action and claims. | Not authorized. |
| `blank` | A template or slot exists without completed content. | Scoring sheet/template exists but scoring not filled. | Do not use for missing files. | Blank is not evidence. | Blank template only. |
| `locked` | A score or artifact is recorded as immutable for review. | A lock confirmation source exists. | Do not infer from scoring pass alone. | Locking is not interpretation. | Locked for review. |
| `reviewed` | A human/operator review artifact exists. | Committed review or interpretation packet exists. | Do not use for automatic parsing. | Reviewed remains packet-bounded. | Reviewed in source truth. |
| `hidden` | Source identity is not revealed. | Blind packet/custody posture applies. | Do not reveal identity. | Preserves blinding. | Source identity hidden. |
| `out_of_scope` | Field is deliberately outside packet scope. | Packet does not cover route metadata, scoring, etc. | Do not use for required but missing fields. | No claim can depend on it. | Out of scope for this packet. |
| `historical_only` | Artifact exists as prior context only. | Historical packet informs context but not current authorization. | Do not treat as current selected state. | Historical evidence does not authorize new work. | Historical context only. |
| `support_context_only` | Artifact supports understanding but is not primary source. | Operator Console or support docs inform context. | Do not treat as workbench proof. | Support context is not runtime proof. | Support context only. |
| `future_required` | Future implementation work is needed. | Parser/inventory/adapter/static fixture does not yet exist. | Do not claim current automation. | Future requirement is not present capability. | Future source adapter required. |
