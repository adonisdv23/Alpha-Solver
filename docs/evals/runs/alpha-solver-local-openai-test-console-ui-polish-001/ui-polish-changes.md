# UI polish changes

## Layout

The page now uses a readable max-width container, a header with the product name and a local-only badge, an evidence-boundary card, a form panel, a result summary card, a sanitized JSON panel, and a setup checklist panel. Styling uses inline CSS only. No external CSS framework is used.

## Mode and model dropdowns

Mode is a dropdown with `local` and `openai`. Model is now a mode-aware dropdown.

- Local model options: `qwen2.5:3b`, `gemma3:4b`, `llama3.2:1b`, `llama3.2:latest`, `custom`.
- OpenAI model options: `gpt-4.1-mini`, `gpt-4.1`, `gpt-4o-mini`, `custom`.

Selecting `custom` shows a custom model text input. The model lists are static and embedded in the page. The page does not query remote services and does not call Ollama to populate the dropdowns.

## Prompt counter and limit

The form shows a live character counter, a max length of 500, and a warning when the prompt is over 500 characters. The browser disables submit when the prompt is over the limit. The server-side fail-closed `prompt_too_long` behavior is unchanged and still enforced.

## Friendly result display

The result summary shows readable labels for status, reason, provider, model, latency, usage tokens, estimated cost, output preview, evidence flags, and errors. A clear passed state and a clear failed-closed state are shown. A `prompt_too_long` reason renders the 500-character explanation.

## Sanitized JSON copy

The full sanitized JSON stays visible. A copy button uses inline JavaScript to copy only the sanitized JSON text content. It does not copy form state, headers, request bodies, shell history, or any secret.

## Setup checklist

The checklist lists local/Ollama steps and OpenAI steps, including the reminder to never paste API keys into the UI.

## Form state preservation

After a submit, the page preserves the submitted mode, the selected model option, the custom model value, and the prompt.

## Boundary

These are presentation and client-side interaction changes only. They do not change provider execution, do not add result persistence, and make no quality, readiness, benchmark, production, public, security/privacy, or Alpha-superiority claim.
