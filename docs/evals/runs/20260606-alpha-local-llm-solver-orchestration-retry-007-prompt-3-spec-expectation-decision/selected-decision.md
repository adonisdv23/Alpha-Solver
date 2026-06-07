# Selected decision

## Decision path

`KEEP_CURRENT_RULE`

## Contract statement

`missing_information_too_broad` blocks `answer_with_assumptions` for Prompt 3 and for the bounded local Python CLI startup-plan shape.

When `missing_information_too_broad` is present, Prompt 3 should not still require `answer_with_assumptions`. A `clarify` outcome is acceptable for that condition.

## Implementation status

No runtime implementation change is authorized by this decision packet.

No test expectation change is made in this packet. The selected next lane may update the smoke expectation documentation or fixture surface narrowly to accept `clarify` when `missing_information_too_broad` is present.
