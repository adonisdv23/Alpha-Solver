# Rationale

## Why `KEEP_CURRENT_RULE` is selected

The current implementation already distinguishes a bounded startup-plan prompt that can answer with assumptions from one that cannot. The gate permits `answer_with_assumptions` only when confidence, considerations, assumptions, missing information, risk terms, and boundary terms satisfy the assumption gate.

`missing_information_too_broad` is a deterministic indication that the parsed missing-information set is broader than the current assumption gate permits. Preserving that rule is safer than converting the result into a successful answer because Prompt 3's Pass 1 output asked for more missing context than the current contract treats as bounded enough for an assumptions answer.

The selected rule is also more consistent with the orchestration spec's requirement that the gate use bounded local confidence and missing-information checks. It follows the spec preference for `clarify` or `block` over unsupported successful behavior when the runner cannot establish enough bounded support for an answer.

## Why the alternatives are less consistent now

`AMEND_CONTRACT_NARROWLY` would require a new secondary classification inside broad missing information. That could be useful later, but it is not supported by this lane's source evidence and would risk broadening behavior before the allowed surface is fully specified.

`REDEFINE_SMOKE_EXPECTATION` describes the likely next work, but it is not the contract decision itself. The contract decision is to keep the current rule; a later lane can update the smoke expectation to reflect it.

`STOP_CURRENT_TRACK` is too broad. The evidence identifies a Prompt 3 expectation mismatch, not a reason to stop the entire current local solver orchestration track.

## Safety result

The selected rule preserves the safer non-answering outcome when missing information is too broad, preserves field non-exposure for the failed assumption gate path, and preserves the prohibition on Pass 2 when the assumption gate fails.
