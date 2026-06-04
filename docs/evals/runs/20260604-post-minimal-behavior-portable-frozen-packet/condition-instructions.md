# Condition Instructions

Lane ID: `OUTPUT-DIFF-POST-IMPROVEMENT-FROZEN-PACKET-001`

Status: condition definition only, pre-capture.

## Alpha condition

The Alpha condition must explicitly load the repository file `alpha_solver_portable.py` as the Alpha portable behavior contract.

Future capture operators must use the merged repository version of `alpha_solver_portable.py` at capture time. Do not paste or use an older local copy unless the later capture authorization explicitly pins a commit.

For each comparison, the Alpha condition must apply the portable contract to the same frozen user prompt used in the plain condition.

The Alpha condition must not use `/v1/solve` unless a later approved task proves `/v1/solve` consumes `alpha_solver_portable.py` and authorizes that measurement surface.

The Alpha condition must not add extra hidden instructions beyond:

1. the merged `alpha_solver_portable.py` portable contract; and
2. the exact frozen diagnostic prompt for that comparison.

## Plain condition

The plain condition must use the same exact frozen user prompt as the Alpha condition.

The plain condition must not include `alpha_solver_portable.py`.

The plain condition must not include Alpha Solver repository context, prior eval outcomes, scoring rubrics, identity labels, operator notes, or improvement instructions.

The plain condition must use the same provider, model, and tool policy as the Alpha condition in the later capture task.

## Shared condition rules

- No tool use unless a future capture task explicitly authorizes it.
- No browsing.
- No extra attachments.
- No retries except documented technical failure.
- Preserve raw outputs exactly.
- Use identical provider/model settings for both conditions when a future capture task is approved.
- Do not include scoring instructions in either generation condition.
- Do not reveal condition identity in the generated output request.
