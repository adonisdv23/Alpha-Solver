# First-Screen Wireframe

```text
HEADER
VALUE_READ_DISCRIMINATION_WORKBENCH / static source-map review
Selected next state: OPERATOR_REVIEW_REQUIRED_AFTER_B015_VALUE_READ_WORKBENCH_SOURCE_MAP_STATIC_PROTOTYPE_001
Banner: docs/source-truth planning only; no runtime/provider/scoring/unblinding/final interpretation.

[Current packet card] - What am I reviewing?
Packet id: <packet_id>
Packet path: <packet_path>
Packet type: <packet_type>
Lifecycle state: <lifecycle_state>
Current operator decision: <current_operator_decision>

[Artifact completeness card] - Is it complete?
Case packet: <case_packet_status>
Alpha/routed output: <raw_alpha_routed_output_status>
Plain/baseline output: <raw_plain_baseline_output_status>
Blind packet: <blind_packet_status>
Scoring: <scoring_status>
Interpretation: <final_interpretation_state>
Missing artifacts: <missing_artifacts>

[Comparison state card]
Comparison state: Alpha/routed side <status> vs plain/baseline side <status>
Source identity: <source_identity_state>
Score lock: <score_lock_status>
Boundary: comparison setup/status is not a benchmark, value, readiness, or superiority claim.

[Route/expert context card]
Route metadata: <route_metadata_state>
SAFE-OUT: <safe_out_state>
Confidence: <confidence_state>
Note: route context is diagnostic only and does not prove output quality.

[Claim boundary card] - What can I not claim?
Allowed: <bounded statement from claim-boundary map>
Blocked: value/readiness/superiority/provider-validation/local-model-validation/benchmark/production/public-readiness/security-privacy/final-interpretation claims.

[One next safe action card] - What can I safely do next?
Next safe action: <next_safe_action>
Why safe: reads or reviews committed source truth only.
Does not authorize: implementation, provider/model/runtime/live UI, scoring, unblinding, source identity reveal, or final interpretation.

BLOCKED ACTIONS FOOTER
No provider calls. No local or hosted model calls. No /v1/solve exposure. No routes or POST routes. No scoring. No unblinding. No source identity reveal. No final interpretation. No Google Sheets mutation. No broad claims.
```
