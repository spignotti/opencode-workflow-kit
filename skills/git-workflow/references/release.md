---
name: git-release
description: Prepare and publish a release for a published project. Load when preparing a version bump, changelog, tag, or push for projects with Delivery Profile: published.
---

# Git Release

Use this reference to release a published project. Only for projects with `Delivery Profile: published` in their `AGENTS.md`.

Run after a feature PR has been merged to `main`.

## Prerequisites

Before running a release:
- you are on `main` with a clean working tree
- the PR for the feature has been merged
- `nox` passes cleanly
- `git-cliff` is installed (`brew install git-cliff`)
- for Python: the GitHub Actions release workflow is configured (`.github/workflows/release.yml`) and PyPI Trusted Publisher is set up
- for Astro: deployment workflow is configured if applicable

## Release Flow

```
1. state guards
2. tooling guards
3. run nox — full validation gate
3b. run security audit (pip-audit for Python, pnpm audit for Astro)
4. inspect version and commit history
5. suggest bump type and new version
6. wait for user confirmation
7. bump version in pyproject.toml (Python) or package.json (Astro)
8. generate CHANGELOG.md with git-cliff
9. commit release artifacts
10. tag vX.Y.Z
11. push commit + tag
12. report to user
```

## Detailed Steps

### 1. State Guards

```bash
git branch --show-current   # must be main
git status --short           # must be clean
```

If either fails: stop and explain why.

### 2. Tooling Guards

```bash
git-cliff --version   # must be available
```

If not available: stop with install instruction: `brew install git-cliff`

### 3. Full Validation

```bash
uv run nox   # Python
# or
pnpm run build   # Astro
```

Must be green. Stop if any session fails.

### 3b. Security Audit

**Python:**
```bash
pip-audit --skip-editable
```

**Astro:**
```bash
pnpm audit
```

If vulnerabilities found:
- **Critical/High**: Stop release, fix vulnerabilities first
- **Medium/Low**: Warn user, ask for confirmation to proceed

### 4. Inspect Version and History

Read current version from `pyproject.toml` (Python) or `package.json` (Astro):
```bash
rg '^version = ' pyproject.toml   # Python
# or
rg '"version"' package.json       # Astro
```

Find the latest tag:
```bash
git tag --sort=-version:refname | head -1
```

**No prior tag (first release):**
- state: "No prior release found. This will be your first release."
- show the current version as the suggested version
- ask the user to confirm

**Prior tag exists:**
- review commits since the latest tag:
  ```bash
  git log <latest-tag>..HEAD --oneline
  ```
- suggest bump type based on Conventional Commit history:
  - any `!` or `BREAKING CHANGE` → major
  - any `feat` → minor
  - only `fix`, `refactor`, `docs`, `chore`, `ci`, `test` → patch
- show the reasoning and the resulting version
- ask the user to confirm

### 5. Wait for Confirmation

Do not modify any files until the user confirms the version. Show:
- current version
- suggested new version
- bump type reasoning
- preview of commits that will be in this release

### 6. Bump Version

**Python** — Update `pyproject.toml`:
- find `version = "X.Y.Z"` under `[project]`
- replace with the confirmed new version
- do not edit anything else in the file

**Astro** — Update `package.json`:
- find `"version": "X.Y.Z"`
- replace with the confirmed new version

### 7. Generate Changelog

```bash
git-cliff --tag vX.Y.Z -o CHANGELOG.md
```

If `CHANGELOG.md` does not exist, `git-cliff` will create it. If it exists, it will be overwritten with the full history. This is correct — `git-cliff` regenerates from all tags every time.

### 8. Commit Release Artifacts

```bash
# Python
git add pyproject.toml CHANGELOG.md
git commit -m "chore: release vX.Y.Z"

# Astro
git add package.json CHANGELOG.md
git commit -m "chore: release vX.Y.Z"
```

Only stage version file and CHANGELOG.md. Nothing else.

### 9. Tag

```bash
git tag vX.Y.Z
```

Always use the `v` prefix. Never tag before the release commit is in place.

### 10. Push Commit + Tag

```bash
git push origin main
git push origin vX.Y.Z
```

Push the commit first, then the tag. The tag push triggers the GitHub Actions release workflow.

### 11. Report

Tell the user:
- release `vX.Y.Z` is tagged and pushed
- GitHub Actions release workflow is now running (if configured)
- PyPI publish will follow if CI passes (Python)

## Rules

- release only from `main` with a clean working tree
- release only after `nox` (Python) or `pnpm run build` (Astro) passes
- run security audit before every release
- never tag before bumping and committing
- never push the tag before pushing the commit
- never hand-write changelog entries — always use `git-cliff`
- tag format is always `vX.Y.Z`
- only touch version file and CHANGELOG.md in the release commit
- never create a release PR — push directly to main
