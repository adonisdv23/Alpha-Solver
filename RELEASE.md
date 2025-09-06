# Release Checklist

- [ ] Update CHANGELOG.md Unreleased section
- [ ] Run `make release-notes`
- [ ] Bump version via scripts/bump_version.py
- [ ] Commit & tag: `make tag-release V=X.Y.Z`
- [ ] Push tag to trigger release workflow
- [ ] Verify artifacts attached to GitHub Release
