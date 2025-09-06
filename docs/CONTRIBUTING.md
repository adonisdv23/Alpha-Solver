# Contributing

## Branch & PR Flow
1. Create a feature branch.
2. Push commits and open a pull request.
3. CI runs tests and linters.
4. Squash merge after review.

## Code Quality
- **Format**: `black` and `isort`
- **Lint**: `ruff`
- **Tests**: `pytest`
- **Preflight**: `make preflight` before large changes

## Commit & PR Titles
Reference roadmap tags like `T2`, `T3`, or `T5` in commit and PR titles to
indicate the relevant task.
