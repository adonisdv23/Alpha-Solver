# Field-to-Source Trace

Every visible field in `static-mockup.md` is listed here. Source certainty values follow B015: exact committed source file, packet family, inferred status from current source truth, unknown or missing source, future implementation requirement, or static placeholder for demonstration only.

| Mockup section | Visible field/value | Source certainty | Source |
|---|---|---|---|
| Header | Workbench: `VALUE_READ_DISCRIMINATION_WORKBENCH` | exact committed source file | `docs/CURRENT_STATE.md`; B015 packet |
| Header | Mockup packet: `AS-B016-VALUE-READ-WORKBENCH-STATIC-MOCKUP-001` | exact committed source file | `.specs/AS-B016-VALUE-READ-WORKBENCH-STATIC-MOCKUP-001.md` |
| Header | Source-map baseline: `AS-B015...` | exact committed source file | `.specs/AS-B015-VALUE-READ-WORKBENCH-SOURCE-MAP-AND-STATIC-PROTOTYPE-001.md` |
| Header | Current selected state shown in mockup | exact committed source file | `docs/CURRENT_STATE.md`; B015 packet |
| Header | Mockup status: `review_only_static_mockup` | inferred status from current source truth | B015 non-actions and B016 spec scope |
| Header | Safety banner | inferred status from current source truth | B015 static prototype plan and non-actions |
| Current packet card | Packet id placeholder | static placeholder for demonstration only | B015 first-screen wireframe requires `<packet_id>`; B016 does not select a real packet |
| Current packet card | Packet path placeholder | static placeholder for demonstration only | B015 first-screen wireframe requires `<packet_path>`; B016 does not select a real packet |
| Current packet card | Packet type | inferred status from current source truth | B015 first-screen wireframe and B016 purpose |
| Current packet card | Lifecycle state: `review_only` | inferred status from current source truth | `docs/CURRENT_STATE.md`; B015/B016 non-actions |
| Current packet card | Current operator decision | inferred status from current source truth | B015 recommended next lane and B016 completion boundary |
| Current packet card | Source certainty | inferred status from current source truth | B015 exact-source discipline and B016 spec |
| Artifact completeness card | Case packet | unknown or missing source | B015 field inventory allows unknown; B016 does not parse a selected packet |
| Artifact completeness card | Alpha/routed output | unknown or missing source | B015 field inventory allows unknown; no B016 runtime inventory |
| Artifact completeness card | Plain/baseline output | unknown or missing source | B015 field inventory allows unknown; no B016 runtime inventory |
| Artifact completeness card | Blind packet | unknown or missing source | B015 field inventory allows unknown; no B016 runtime inventory |
| Artifact completeness card | Scoring | inferred status from current source truth | B015/B016 non-actions block scoring |
| Artifact completeness card | Interpretation | inferred status from current source truth | B015/B016 non-actions block final interpretation |
| Artifact completeness card | Missing artifacts | future implementation requirement | B015 field inventory marks missing artifact inventory as future_required |
| Artifact completeness card | Completeness answer | inferred status from current source truth | B015 claim-boundary map and B016 non-claims |
| Comparison state card | Comparison setup | packet family | B015 first-screen wireframe comparison state card |
| Comparison state card | Alpha/routed side | unknown or missing source | B015 field inventory allows unknown; no B016 selected output source |
| Comparison state card | Plain/baseline side | unknown or missing source | B015 field inventory allows unknown; no B016 selected output source |
| Comparison state card | Source identity | inferred status from current source truth | B015/B016 non-actions block unblinding and source identity reveal |
| Comparison state card | Score lock | unknown or missing source | B015 field inventory allows unknown; B016 does not inspect score-lock packet |
| Comparison state card | Boundary | exact committed source file | B015 claim-boundary map |
| Route/expert context card | Route metadata | future implementation requirement | B015 field inventory and implementation-readiness gate require parser/adapter before automation |
| Route/expert context card | Expert context | future implementation requirement | B015 static prototype future implementation needs |
| Route/expert context card | SAFE-OUT | unknown or missing source | B015 field inventory allows unknown |
| Route/expert context card | Confidence | unknown or missing source | B015 field inventory allows unknown |
| Route/expert context card | Diagnostic note | exact committed source file | B015 claim-boundary map |
| Claim boundary card | Allowed bounded statement | inferred status from current source truth | B016 packet existence and B015 claim-boundary map |
| Claim boundary card | Blocked value claim | inferred status from current source truth | B015/B016 non-claims |
| Claim boundary card | Blocked readiness claim | inferred status from current source truth | B015/B016 non-claims |
| Claim boundary card | Blocked benchmark claim | inferred status from current source truth | B015/B016 non-claims |
| Claim boundary card | Blocked superiority claim | inferred status from current source truth | B015/B016 non-claims |
| Claim boundary card | Blocked provider/local-model validation claim | inferred status from current source truth | B015/B016 non-claims |
| Claim boundary card | Blocked production/public/security claim | inferred status from current source truth | B015/B016 non-claims |
| Claim boundary card | Blocked final interpretation claim | inferred status from current source truth | B015/B016 non-claims |
| One next safe action card | Next safe action | inferred status from current source truth | B016 completion boundary |
| One next safe action card | Why safe | inferred status from current source truth | B016 scope and non-actions |
| One next safe action card | Does not authorize | exact committed source file | B015/B016 non-actions |
| One next safe action card | If insufficient | inferred status from current source truth | B016 recommended next lane boundary |
| Blocked actions footer | Full blocked action list | exact committed source file | B015/B016 non-actions and user lane constraints |
