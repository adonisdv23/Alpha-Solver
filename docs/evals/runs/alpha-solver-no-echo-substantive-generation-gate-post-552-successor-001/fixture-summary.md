# Fixture Summary

Source fixture file: `tests/fixtures/no_echo_substantive_gate_cases.json`

## Categories and known outcomes

| Fixture ID | Group | Expected category |
| --- | --- | --- |
| `exact-echo-photosynthesis` | exact echo cases | `exact_prompt_echo` |
| `exact-echo-normalized-case` | exact echo cases | `exact_prompt_echo` |
| `near-echo-preface` | near-echo cases | `near_echo` |
| `near-echo-long-span` | near-echo cases | `near_echo` |
| `placeholder-todo` | placeholder/stub cases | `placeholder_stub_canned_output` |
| `placeholder-canned` | placeholder/stub cases | `placeholder_stub_canned_output` |
| `safeout-unsupported` | bounded SAFE-OUT cases | `safe_out_refusal_or_clarification` |
| `clarification-missing-context` | bounded SAFE-OUT cases | `safe_out_refusal_or_clarification` |
| `derived-photosynthesis` | known derived-output cases | `substantive_derived_output` |
| `derived-work-trip` | known derived-output cases | `substantive_derived_output` |

## Pass/fail counts

- Total fixtures: 10
- Expected category matches: 10
- Expected category mismatches: 0

## Heuristic coverage

- Exact echo: normalized full-output equality.
- Near echo: normalized token overlap ratio and longest copied-span ratio.
- Placeholder/stub/canned: deterministic phrase patterns, too-short outputs, and missing required fields.
- SAFE-OUT/refusal/clarification: deterministic SAFE-OUT and bounded clarification/refusal phrase patterns.
- Substantive-derived: minimum length, novelty, answer-field presence, and no echo/near-echo/placeholder classification.
