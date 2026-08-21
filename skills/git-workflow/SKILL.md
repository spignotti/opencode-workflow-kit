---
name: git-workflow
description: Git workflow for commits, branches, pushes, pull requests, and local merges — adapted to delivery profile (quick, standard, production, published). Load this skill whenever making a commit, creating a branch, opening a PR, pushing, or deciding how to handle git at a checkpoint. Also load it when the user runs /git or asks how to finish a feature, ship work, or handle git hygiene.
---
## Purpose

Load this skill whenever work involves a git decision or action — commits, branches, pushes, PRs, merges, bootstrap, or release.

The workflow adapts to the delivery profile (quick, standard, production, published), so reading the profile from `AGENTS.md` is the first step. The same quality standards apply everywhere; what changes is how much ceremony is appropriate.

## Lifecycle Routing

- **Project bootstrap** (git init, first commit, remote push) → `references/bootstrap.md`
- **Published release** (version bump, changelog, tag, push) → `references/release.md`
- **Daily work** (commit, push, branch, PR, ship) → use the workflows below

---

## Core principles

Conventional Commits matter because they make history readable, enable automated changelog generation with git-cliff, and make PR titles meaningful at a glance. They're worth the small discipline cost.

Stage intentionally rather than `git add .` because committing unrelated changes together makes history noisy and harder to revert cleanly if something goes wrong.

Scan for secrets before committing because it's cheap to catch them here and expensive to remove them from history later.

Validate before pushing because pushing broken code wastes CI minutes and creates noise for anyone watching the branch.

Avoid destructive git commands (force-push, hard reset, checkout --) unless explicitly requested — they rewrite history and can cause data loss that's hard to recover from.

---

## Conventional Commits

Types:
- `feat` — new functionality
- `fix` — bug fix
- `refactor` — restructuring without behavior change
- `docs` — documentation only
- `test` — tests only
- `chore` — deps, config, tooling, build
- `ci` — CI/CD changes

Message rules:
- imperative mood: "add" not "added"
- lowercase after the prefix
- no trailing period
- optional scope when it adds clarity: `feat(auth): ...`
- breaking changes: use `!` and a `BREAKING CHANGE:` footer

Examples:
- `feat(auth): add token refresh flow`
- `fix(api): handle null response payloads`
- `docs: clarify installation steps`
- `feat(api)!: change response envelope`

---

## Secrets Scan

Run before every commit on staged files:

```bash
git diff --cached --name-only | xargs rg -il "(api_key|secret_key|password|token|private_key|AWS_|sk-|ghp_|-----BEGIN)" 2>/dev/null
```

If matches found: review each one. Variable names and docs referencing these words are false positives and are fine. Actual secrets → stop, remove them, use env vars, add file to `.gitignore`.

---

## Delivery Profiles

Read the delivery profile from the project `AGENTS.md` `## Delivery Profile` section before choosing a workflow. The profile changes which steps are required, not the underlying quality standards.

### quick

Optimize for speed. Minimal ceremony.

- direct work on `main` is acceptable when low-risk
- branch when the change is large, risky, or benefits from isolation
- conventional commits always
- validate before committing (lint only)
- no PR required, no release process
- push when ready

### standard

Balanced. Feature branches for meaningful work.

- feature branches preferred for meaningful work
- direct commits to `main` acceptable for small cosmetic changes
- conventional commits always
- validate before committing (lint + typecheck/test if configured)
- PR flow preferred but not required for trivial solo changes
- no release process

### production

High-care. Green CI required before merge.

- always work on a feature branch for meaningful changes
- conventional commits always
- validate before every commit and before every push
- open a PR for all meaningful work — never merge in the terminal
- squash merge in GitHub UI to keep history clean
- CI must pass before merge
- deployment is separate and manual

### published

Highest-care. Release-ready work.

- always work on a feature branch, never directly on `main`
- conventional commits always
- validate before every commit and before every push
- open a PR for all meaningful work — never merge in the terminal
- squash merge in GitHub UI to keep history clean
- CI must pass before merge
- release via `references/release.md`

---

## Workflow: Feature Branch Creation

Use when starting meaningful work on production/published repos, or when a quick/standard repo change is large enough to warrant isolation.

```
1. check for uncommitted changes — if any, stop: commit or stash first
2. git checkout main && git pull origin main
3. derive branch name from the task description:
   - format: type/kebab-case-description
   - types: feat/, fix/, docs/, refactor/, test/, chore/
   - max 50 chars, lowercase, hyphens only
4. git checkout -b <branch-name>
5. git push -u origin <branch-name>
```

Branch name examples:
- `feat/add-oauth2-support`
- `fix/login-redirect-loop`
- `docs/update-api-reference`
- `refactor/simplify-auth-logic`

Branch from `main` only — branching from another feature branch creates dependency chains that make merging painful. Use lowercase with hyphens for portability across filesystems and tools.

---

## Workflow: Commit

Steps for all profiles:

```
1. branch guard (production/published only): if on main → stop, tell user to create a branch first
2. git status --short + git diff --stat — understand what changed
3. run validation at the appropriate level for the change
4. git add <files> — stage only the intended files, review before staging
5. secrets scan on staged files
6. determine commit type from the nature of the changes
7. derive scope from affected file paths when it adds clarity
8. write the commit message: type(scope): description
9. show the commit preview — wait for confirmation before executing
10. git commit -m "<message>"
```

Validation level by change type:
- docs, config, comments only → `nox -s lint` or skip if no linter
- structural changes (new modules, imports, type signatures) → `nox -s lint typecheck`
- logic or behavior changes → `nox -s lint typecheck test`
- checkpoint or release gate → full `nox`

For non-Python repos, use the project's equivalent validation profile.

One logical change per commit. If staged files span multiple unrelated concerns, suggest splitting.

---

## Workflow: Push

```
1. branch guard (production/published): if on main → stop
2. confirm commits exist to push: git log origin/<branch>..HEAD
   if none → say so and stop
3. run validation at push level (branch-ready quality)
4. git push origin <current-branch>
```

For quick/standard repos where direct main commits are acceptable, push to main is fine after validation.

---

## Workflow: Pull Request (production/published)

```
1. branch guard: must not be on main
2. git status --short — no uncommitted changes
3. run full validation
4. git push -u origin <branch> (if not already pushed)
5. derive PR title: Conventional Commit style — type(scope): description
6. write PR body:
   - what changed
   - why it changed
   - validation performed
7. gh pr create --title "<title>" --body "<body>"
8. gh pr view --web  (open in browser)
9. tell the user: PR is open, CI is running, review and squash merge in GitHub UI
```

Don't auto-merge — the whole point of a PR is a human review gate before history is finalized. Don't create PRs from `main` or with failing validation — both undermine the PR's value as a quality checkpoint.

---

## Workflow: Ship (quick/standard local merge)

Use when a PR is not needed and you want to merge a feature branch into main locally.

```
1. confirm not on main and no uncommitted changes
2. git fetch origin main
3. git rebase main — stop and explain if conflicts
4. run full validation after rebase
5. git checkout main
6. git merge --no-ff <branch> -m "Merge branch '<branch>'"
7. git push origin main
8. git branch -d <branch>
9. git push origin --delete <branch>
```

Rebase before merge so the branch tip is current and conflicts are resolved cleanly before touching `main`. Use `--no-ff` to preserve the branch topology in history — it makes it easy to see what was part of a feature and revert it if needed. Clean up branches after merge to keep the remote tidy; stale branches cause confusion about what's still in flight.

---

## Manual Workflow Guidance

For manual sessions, use the `/git` command with the task as the argument:
- `/git commit`
- `/git push`
- `/git pr`
- `/git feature <description>`
- `/git ship`
- `/git status`

The command loads this skill and routes through the appropriate workflow for the delivery profile.

For published releases, use `/git release` — this routes to `references/release.md`.

---

## What Does Not Belong Here

- language-specific validation commands → project `AGENTS.md` or stack skills
