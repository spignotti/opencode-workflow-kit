---
name: git-bootstrap
description: Initialize a fresh git repository during project bootstrap. Load when a setup skill needs to handle git init, first commit, or remote push.
---

# Git Bootstrap

Initialize a git repository during project bootstrap. Idempotent — safe to run if `.git` already exists.

## Variables (passed by caller)

- **commit_message** — full commit message, e.g. `chore: initial project setup`
- **git_remote** — remote URL or `"local only"` (no remote)

## Steps

### 1. Guard

```bash
git rev-parse --is-inside-work-tree 2>/dev/null
```

### 2. Fresh init or skip

**If `.git` does not exist:**
```bash
git init
git add <setup files>   # stage the generated files explicitly, e.g. AGENTS.md opencode.json .gitignore
git commit -m "{commit_message}"
```

**If `.git` exists** (cloned from GitHub):
- skip `git init`
- check `git remote -v`
- if no remote and `git_remote` is set, add it: `git remote add origin {git_remote}`
- stage and commit: `git add <setup files> && git commit -m "{commit_message}"`
- push: `git push -u origin main`

### 3. Optional remote push

If `git_remote` is set and not `"local only"`:
```bash
git remote add origin {git_remote}
git push -u origin main
```

If push fails: stop and report init is incomplete — likely causes: remote repo does not exist, wrong URL, auth issue.

## Rules

- Conventional Commits `chore:` prefix for initial commit
- Don't push before the commit is in place
- Don't auto-merge or force-push during init
- For OSS repos, push is mandatory — fail loudly if it doesn't work
