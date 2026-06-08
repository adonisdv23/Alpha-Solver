# Prompt Preservation

## Purpose

Future Self Operator run packets must preserve prompts exactly enough for reviewer inspection of what was asked, what constraints were supplied, and what operator instructions governed the run.

## Required prompt artifacts

Preserve all applicable prompt materials under a raw prompt artifact location such as `raw/prompts/`:

- initial user/operator prompt;
- system or agent instructions available to the operator;
- task packet instructions;
- prompt templates;
- prompt variables and substitutions;
- follow-up prompts;
- clarifying questions and answers;
- explicit stop, continue, confirmation, or refusal prompts.

## Exact preservation rule

Prompt text must be preserved verbatim unless redaction is required. Formatting, ordering, whitespace, variable values, and delimiters should remain as captured.

If redaction is required, replace only the sensitive span with an explicit marker documented in `redaction-rules.md`; do not paraphrase the surrounding prompt.

## Separation rule

Reviewer prompt analysis belongs in `review/` or a reviewer-authored notes file. It must not be mixed into raw prompt files.
