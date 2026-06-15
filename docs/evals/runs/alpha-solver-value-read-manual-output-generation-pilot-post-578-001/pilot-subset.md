# Pilot Subset

| Packet ID | Source case | Primary category | Secondary categories |
| --- | --- | --- | --- |
| VR-SIM-001 | `FP-HC-002` | False premise | Claim-boundary; confidence |
| VR-SIM-002 | `FP-HC-007` | Hidden constraint | No-echo derivation |
| VR-SIM-004 | `FP-HC-001` | No-echo derivation | Hidden constraint |
| VR-SIM-006 | `HVR-003` | False premise | Safety-advantage claim boundary |
| VR-SIM-009 | `HVR-013` | Needs-human | Legal-safe escalation |
| VR-SIM-010 | `HVR-014` | Needs-human | Safety regression containment |
| VR-SIM-011 | `HVR-015` | Evidence conflict | Claim-boundary |
| VR-SIM-012 | `HVR-017` | Evidence conflict | Provider-call boundary |
| VR-SIM-013 | `HVR-018` | Confidence | Future-separation non-claim |
| VR-SIM-016 | `HVR-022` | Claim-boundary | Rewrite |

## Minimum category coverage

- False premise: `VR-SIM-001`, `VR-SIM-006`.
- Hidden constraint: `VR-SIM-002`, `VR-SIM-004`.
- No-echo / derivation: `VR-SIM-002`, `VR-SIM-004`.
- Needs-human: `VR-SIM-009`, `VR-SIM-010`.
- Confidence: `VR-SIM-001`, `VR-SIM-013`.
- Claim-boundary: `VR-SIM-001`, `VR-SIM-006`, `VR-SIM-011`, `VR-SIM-016`.
- Evidence conflict: `VR-SIM-011`, `VR-SIM-012`.

Coverage is met by the selected 10 committed synthetic cases.
