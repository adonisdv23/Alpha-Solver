# Contributing

## Workflow

1. Spec Kit → 2. Codex → 3. PR → 4. CI → 5. Squash & Merge

## Specs

- Specs live under `.specs/` (see `.specs/README.md` for structure, sections, and workflow).
- Start each feature or bugfix by copying the appropriate template from `.specify/templates/`.
- Every pull request must link to its spec and satisfy the checklist in `.github/pull_request_template.md`.

## Branch naming

- `mvp/*` for baseline work
- `next/*` for future iterations

## Local development

```bash
pip install -r requirements.txt
pytest -q
```

## Style

- Type hints and docstrings
- Deterministic tests

## Pull requests

- Keep branches up to date
- Squash merge after CI passes

## Issue templates

Templates live under `.github/ISSUE_TEMPLATE/`.
