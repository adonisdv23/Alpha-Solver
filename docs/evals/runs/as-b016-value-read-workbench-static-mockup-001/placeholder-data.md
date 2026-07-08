# Placeholder Data

B016 uses conservative placeholders only. No placeholder is a fake output, fake score, fake source identity, fake benchmark number, fake readiness verdict, or Alpha-vs-baseline result.

| Placeholder | Where shown | Why safe | Future replacement requirement |
|---|---|---|---|
| `[static placeholder: packet id]` | Current packet card | Clearly labels demonstration-only identity slot and does not name a real evaluation packet. | Future authorized lane must select an exact committed packet id. |
| `[static placeholder: packet path]` | Current packet card | Clearly labels demonstration-only path slot and does not imply parser access. | Future authorized lane must map to an exact committed packet path. |
| `[unknown: selected packet source not mapped in static mockup]` | Artifact completeness | Reports unknown rather than inventing packet completeness. | Future parser/inventory must inspect exact committed sources. |
| `[unknown: output source not mapped in static mockup]` | Artifact and comparison cards | Avoids fake model/provider outputs and avoids output-quality claims. | Future authorized inventory must map real committed output artifacts, if any. |
| `[unknown: blind packet source not mapped in static mockup]` | Artifact completeness | Avoids inventing blinding/custody evidence. | Future authorized inventory must map exact blind packet source. |
| `[blocked: scoring not authorized]` | Artifact completeness | Blocks score creation and avoids fake scores. | Separate scoring authorization and packet prerequisites would be required. |
| `[blocked: final interpretation not authorized]` | Artifact completeness | Prevents final interpretation claim. | Separate interpretation authorization and prerequisites would be required. |
| `[future_required: parser/inventory needed before automated completeness]` | Artifact completeness | States missing capability as future work, not current automation. | Future implementation planning must define parser/inventory contract. |
| `[not_authorized: unblinding]` | Comparison state | Preserves source identity boundary. | Separate unblinding/source identity review authorization would be required. |
| `[unknown: score-lock source not mapped in static mockup]` | Comparison state | Avoids fake lock status. | Future authorized inventory must map score-lock source. |
| `[future_required: route metadata parser/source adapter needed]` | Route/expert context | Does not imply live route metadata extraction. | Future authorized parser/adapter would be required. |
| `[future_required: expert context source adapter needed]` | Route/expert context | Does not imply live expert-context extraction. | Future authorized source adapter would be required. |
| `[unknown: SAFE-OUT source not mapped in static mockup]` | Route/expert context | Avoids inventing diagnostic metadata. | Future authorized inventory must map exact SAFE-OUT source. |
| `[unknown: confidence source not mapped in static mockup]` | Route/expert context | Avoids inventing confidence metadata. | Future authorized inventory must map exact confidence source. |
| `[not_authorized: value claim]` | Claim boundary | Prevents value assertion. | Separate evidence and authorization would be required. |
| `[not_authorized: readiness claim]` | Claim boundary | Prevents readiness assertion. | Separate readiness review would be required. |
| `[not_authorized: benchmark claim]` | Claim boundary | Prevents benchmark assertion. | Separate benchmark design/evidence would be required. |
| `[not_authorized: Alpha superiority claim]` | Claim boundary | Prevents superiority assertion. | Separate bounded evidence and authorization would be required. |
| `[not_authorized: provider or local-model validation claim]` | Claim boundary | Prevents provider/local-model validation assertion. | Separate provider/local-model validation lane would be required. |
| `[not_authorized: production, public-readiness, or security/privacy claim]` | Claim boundary | Prevents deployment/security claim. | Separate production/public/security/privacy reviews would be required. |
| `[not_authorized: final interpretation]` | Claim boundary | Prevents final interpretation assertion. | Separate final interpretation authorization would be required. |
