# Provider Options

All options in this document are planning only. This lane does not implement,
configure, start, contact, or verify any provider.

## Option A: Ollama-style local HTTP backend

A future backend could translate `LocalLLMAdapterRequest` into an HTTP request
for a locally managed service with an Ollama-style API.

Planning constraints:

- endpoint must be localhost or an explicitly approved local address;
- no default network access;
- timeout must be mandatory;
- request body must keep system/contract and user content logically separated;
- response parser must fail closed on missing text, unexpected JSON, empty text,
  prompt echo, and backend error status;
- no automatic model pull, installation, or background service start;
- evidence must distinguish local HTTP smoke output from offline stub output.

## Option B: OpenAI-compatible local endpoint

A future backend could target a local server that implements an OpenAI-compatible
chat/completions-style interface.

Planning constraints:

- endpoint must be local and approved for the lane;
- hosted-provider base URLs are not allowed;
- provider credentials are not allowed for this lane family unless a later spec says
  otherwise;
- model name must be an explicit local label, not a hosted model shortcut;
- messages must preserve system/contract and user roles;
- response parser must reject missing choices/content, malformed payloads,
  empty content, prompt echo, timeout, and transport failures.

## Option C: Direct subprocess-based local server wrapper

A subprocess wrapper should remain a future option only and requires extra
restrictions because it can start processes and consume local compute.

Additional restrictions before this option can be considered:

- explicit operator approval for the command and arguments;
- no shell interpolation of prompts or paths;
- fixed allowlist of executable path and arguments;
- working directory, environment variables, and resource limits documented;
- startup timeout, generation timeout, and teardown behavior documented;
- captured logs scrubbed for prompts, credential material, and nonpublic paths before storage;
- no automatic downloads, model pulls, package installs, or daemon persistence.

## Recommendation for the next spec

The next spec should select exactly one provider shape for implementation
planning. It should prefer the smallest local endpoint option that can be tested
with offline fixtures before any opt-in local smoke command is considered.
