# Checks run

- `git diff --name-only`
- `git diff --name-only --cached`
- `git diff --check --cached`
- Manual changed-file scope review: staged changed files are limited to docs expectation surfaces.
- Manual runtime/source/provider/dashboard/API review: no runtime, source, provider, dashboard, or API files changed.
- Manual tests/fixture review: no tests or deterministic fixture files changed.
- Deterministic tests: not run because no tests or fixtures changed.
- Smoke: not run, per lane instructions.
- Local / hosted model invocation: not run, per lane instructions.
- Selected next lane count: exactly one selected next lane value recorded in `selected-next-lane.md`.
- Evidence boundary review: narrow boundary language preserved.
