# Field Inventory

| Field name | Display label | Meaning | Source | Source certainty | Allowed values | Unknown value | Can be inferred | Above the fold |
|---|---|---|---|---|---|---|---|---|
| packet_id | Packet id | Identifier of packet under review | Packet README, folder name, source-truth docs | exact | committed lane id or folder id | `unknown` | Yes | Yes |
| packet_path | Packet path | Committed source path | `docs/evals/runs/<packet>/` | exact | committed path | `unknown` | No | Yes |
| packet_type | Packet type | Case, output, blind packet, scoring, interpretation, design, or source-map packet | Packet README/spec | inferred | `case`, `output`, `blind_packet`, `scoring`, `interpretation`, `design`, `source_map`, `unknown` | `unknown` | Yes | Yes |
| lifecycle_state | Lifecycle state | Current lifecycle posture | `docs/CURRENT_STATE.md`, `docs/LANE_REGISTRY.md`, packet selected state files | inferred | `review_required`, `completed`, `blocked`, `historical_only`, `support_context_only`, `unknown` | `unknown` | Yes | Yes |
| current_operator_decision | Current operator decision | Decision the operator must make | selected state/gate docs | inferred | `review_b015`, `approve_static_mockup_lane`, `stop_defer`, `unknown` | `unknown` | Yes | Yes |
| next_safe_action | Next safe action | One bounded next action | `data-readiness-rules.md`, selected next state/action files | inferred | `review_only`, `ready_for_output_collection`, `ready_for_scoring`, `ready_for_interpretation`, `stop_defer` | `stop_defer` | Yes | Yes |
| case_packet_status | Case packet | Whether case/task source exists | prompt sets and task-bank packet families | packet_family | `present`, `missing`, `unknown`, `out_of_scope` | `unknown` | Yes | Yes |
| raw_alpha_routed_output_status | Alpha/routed output | Whether Alpha/routed output artifact exists | Value Read raw alpha and routed-vs-plain routed packet families | packet_family | `present`, `missing`, `unknown`, `out_of_scope`, `historical_only` | `unknown` | Yes | Yes |
| raw_plain_baseline_output_status | Plain/baseline output | Whether comparison output exists | Value Read raw baseline and routed-vs-plain plain packet families | packet_family | `present`, `missing`, `unknown`, `out_of_scope`, `historical_only` | `unknown` | Yes | Yes |
| blind_packet_status | Blind packet | Whether scorer-facing blind materials exist | blind packet construction families | packet_family | `present`, `missing`, `blank`, `unknown`, `historical_only` | `unknown` | Yes | Yes |
| scoring_status | Scoring | Whether scoring is blank, blocked, reviewed, or historical | scoring pass and authorization packet families | packet_family | `blank`, `blocked`, `reviewed`, `missing`, `unknown`, `historical_only` | `unknown` | Yes | Yes |
| score_lock_status | Score lock | Whether score mutation is locked | score-lock confirmation packets | packet_family | `locked`, `missing`, `unknown`, `not_applicable` | `unknown` | Yes | Yes |
| source_identity_state | Source identity | Whether A/B identities are hidden or reviewed | blinding, custody, unblinding packet families | packet_family | `hidden`, `reviewed`, `unknown`, `out_of_scope`, `blocked` | `hidden` | Yes | Yes |
| final_interpretation_state | Final interpretation | Whether bounded final interpretation exists | final interpretation packet family | packet_family | `reviewed`, `blocked`, `missing`, `unknown`, `historical_only` | `unknown` | Yes | Yes |
| route_metadata_state | Route metadata | Whether route metadata exists | routed metadata and Operator Console route-preview docs | packet_family | `present`, `missing`, `unknown`, `out_of_scope`, `support_context_only` | `unknown` | Yes | Yes |
| safe_out_state | SAFE-OUT | SAFE-OUT diagnostic status | route metadata packet family | packet_family | `present`, `missing`, `not_applicable`, `unknown`, `out_of_scope` | `unknown` | Yes | No |
| confidence_state | Confidence | Confidence diagnostic status | confidence contract and route metadata packet family | packet_family | `present`, `missing`, `unknown`, `out_of_scope` | `unknown` | Yes | No |
| claim_boundary | Claim boundary | Allowed and blocked wording | B014/B015 claim-boundary docs and packet non-claims | exact | bounded text | `unknown_stop_defer` | Yes | Yes |
| missing_artifacts | Missing artifacts | List of absent required inputs | future inventory over source map | future_required | list, `none_known`, `unknown` | `unknown` | No | Yes |
| blocked_actions | Blocked actions | Actions not authorized | non-actions and source-truth docs | exact | list | `blocked_by_default` | Yes | Yes |
| check_results | Check results | Validation commands and outcomes | packet `checks-run.md` | exact | `pass`, `fail`, `warning`, `not_run`, `unknown` | `unknown` | No | No |
