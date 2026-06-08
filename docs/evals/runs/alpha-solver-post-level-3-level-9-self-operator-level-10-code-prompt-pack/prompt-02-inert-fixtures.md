# Prompt 02 inert fixtures

Use this prompt only after the Level 9 implementation plan is accepted and GS done. Do not run this prompt from the Level 9 packet.

## Hard stops

- stop unless Level 9 implementation plan is accepted and GS done;
- stop unless the selected Level 10 lane matches the prompt;
- stop if current branch is not current-main-based;
- stop if changed files exceed allowed scope;
- stop on provider call risk;
- stop on credential risk;
- stop on browser automation;
- stop on deployment;
- stop on billing;
- stop on `/v1/solve` or dashboard exposure;
- stop on fallback;
- stop on evidence promotion;
- stop on source-artifact mutation.

## Intended future scope

Create only inert text or JSON fixtures needed by authorized static tests. Do not include secrets, provider outputs, external API responses, browser data, deployment output, billing data, or evidence-promotion labels.

## Required return from future Codex run

Return branch name, changed files, exact checks run, artifact summary, stop-state confirmation, and evidence-boundary confirmation. Do not claim MVP behavior evidence.
