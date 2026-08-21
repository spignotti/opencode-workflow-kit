---
description: Run a repo-aware git workflow task — commit, push, pr, feature, ship, init, release, or status
agent: build
---

Load the `git-workflow` skill. Execute the requested task (`$ARGUMENTS`) using the delivery profile from `AGENTS.md`.

Supported intents: `commit`, `push`, `pr`, `feature <desc>`, `ship`, `init`, `release`, `status`. Use `init` with the `git-workflow` bootstrap reference. Use `release` with the release reference (published profile only).
