# UX and redaction changes

## Form state

After a form submission, the console keeps the submitted mode, selected or default-resolved model, and prompt text in the form.

## Usage token counts

Numeric `usage` token counters such as `input_tokens`, `output_tokens`, `total_tokens`, and other numeric token-count fields under `usage` remain visible.

## Secrets

API keys, authorization fields, bearer markers, secret fields, password fields, access or refresh token fields, and secret-like string values remain redacted.
