# Smoke expectation impact

## Impact

The retry 007 Prompt 3 smoke expectation should no longer require `answer_with_assumptions` when the preserved gate trace contains `missing_information_too_broad`.

For that condition, `clarify` is acceptable because the selected contract keeps the current assumption-gate breadth rule.

## Required follow-up

A later narrow smoke expectation update lane should update the relevant smoke expectation documentation or fixture surface so Prompt 3 accepts `clarify` when `missing_information_too_broad` is present.

## Not changed in this packet

This packet does not rerun smoke, alter smoke results, change tests, call a local model, call a hosted provider, or update Google Sheets.
