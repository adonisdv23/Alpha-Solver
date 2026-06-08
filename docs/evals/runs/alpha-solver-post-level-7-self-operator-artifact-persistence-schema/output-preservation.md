# Output Preservation

## Purpose

Future Self Operator run packets must preserve raw output exactly as emitted so reviewers can distinguish successful outputs from partial, failed, malformed, empty, interrupted, or stopped outputs.

## Required output artifacts

Preserve all applicable output materials under a raw output artifact location such as `raw/outputs/`:

- stdout;
- stderr;
- structured response bodies;
- streamed chunks;
- final answer text;
- tool output;
- CLI output;
- application output;
- error messages;
- empty-output markers;
- partial-output markers.

## Raw output preservation rule

Raw output must not be cleaned, normalized, summarized, rewrapped, translated, corrected, or reclassified in place. If the output is malformed or incomplete, preserve the malformed or incomplete artifact and record reviewer interpretation separately.

## Empty and missing outputs

When an output channel is expected but empty, preserve an explicit raw marker file or structured field with one of these values:

- `EMPTY_OUTPUT_CAPTURED`
- `OUTPUT_CHANNEL_NOT_CREATED`
- `OUTPUT_CAPTURE_FAILED`
- `OUTPUT_NOT_APPLICABLE`

Reviewer notes must explain the selected marker in a separate summary file.
