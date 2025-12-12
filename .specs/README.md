# Alpha-Solver Specs

## Purpose
- `.specs/` is the canonical home for every user-facing or internal implementation spec. Treat each Markdown file as the single source of truth for why a change exists and how it will be validated.
- Do **not** move or rename existing specs; link to them directly when planning or reviewing work.
- Keep specs focused on intent, constraints, and validation so Codex, VS Code, and reviewers can work from the same artifact.

## Naming Conventions
- Keep the current filenames (e.g., `AS-145.md`, `MCP-001.md`) exactly as-is for traceability.
- For new specs, follow the existing `PREFIX-###.md` pattern. Choose a short, stable prefix that communicates the area (`AS`, `MCP`, `UI`, etc.) and use a sequential or timestamp-friendly number (`PREFIX-123.md`).
- Use hyphenated uppercase words to make quick searches easy (e.g., `AREA-TOPIC-###.md`). Avoid spaces.

## Required Sections
Each spec should clearly document these sections. If a section is not relevant, explain why rather than deleting it.

1. **Goal** – What success looks like in one or two sentences.
2. **Motivation** – Why we are solving this problem now (user pain, business driver, etc.).
3. **Acceptance Criteria** – Testable statements in Given/When/Then style or bullet points.
4. **Definition of Done** – Checklist of deliverables that must be completed before merging.
5. **Code Targets** – Pointers to code areas, services, or files expected to change.
6. **Test Plan** – How functionality will be verified (unit, integration, manual, tooling).

## Creating a New Spec
1. Decide whether the work is a **feature** or **bugfix**.
2. Copy the matching template from `.specify/templates/feature.md` or `.specify/templates/bugfix.md` into `.specs/` with the chosen filename.
3. Fill out every required section above, expanding details as discovery progresses.
4. Keep the spec in sync with development—update sections as scope, code targets, or tests evolve.

## Workflow
1. **Spec first** – Author or update the relevant spec under `.specs/` before writing code.
2. **Implementation** – Build against the spec, keeping code changes traceable to its Goal and Acceptance Criteria.
3. **Tests** – Execute and document the `python -m pytest -q` run (or justified subset) noted in the spec’s Test Plan.
4. **Pull Request** – Reference the spec file (`.specs/<name>.md>`) in the PR description and verify that the spec sections remain current.

Following this loop keeps Codex, VS Code, and human reviewers aligned on requirements and validation expectations.
