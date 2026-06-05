# Fixture Plan

## Purpose

Fixtures for the next implementation lane should exercise parser and mapping
logic only. They must be static, offline, and free of private URLs, credentials,
provider keys, localhost tokens, nonpublic endpoints, and model outputs from a
live run.

## Proposed fixture groups

1. Valid assistant-text fixture
   - JSON object shaped like an Ollama-style response.
   - Contains one assistant text value.
   - Expected result is normalized adapter output with `behavior_evidence=False`.
2. Missing text fixture
   - Omits the selected assistant text field.
   - Expected result is `failed_closed`.
3. Malformed JSON fixture
   - Uses invalid JSON or an unexpected top-level type.
   - Expected result is `failed_closed`.
4. Non-string text fixture
   - Provides object, array, number, boolean, or null where text is expected.
   - Expected result is `failed_closed`.
5. Empty text fixture
   - Provides empty or whitespace-only text.
   - Expected result is `failed_closed`.
6. Prompt echo fixtures
   - Provides output equal to the user prompt.
   - Provides output equal to the system/contract text or normalized contract
     content.
   - Expected result is `failed_closed`.
7. Backend-error fixture
   - Represents an HTTP error or local backend exception as static test input.
   - Expected result is `failed_closed` with no fallback.

## Fixture labels

All fixture results must be labeled as offline parser or mapping evidence only.
Fixtures must not be labeled as local execution evidence, runtime readiness
proof, quality evidence, comparison evidence, benchmark evidence, billing
evidence, or provider-orchestration evidence.

## Storage boundary

The future lane may place fixtures under the local LLM adapter test area or a
lane-specific fixture directory if approved. This packet does not create fixture
files because it does not implement parser code.
