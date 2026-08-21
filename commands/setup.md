---
description: Set up the OpenCode workflow or bootstrap a project — configure providers via /connect, prepare a new or existing repo, write project-local AGENTS.md, optional Python bootstrap, opt-in project contract.
agent: build
---

Load the `setup` skill and execute its workflow.

**Arguments:** Pass the requested mode or a project description as `$ARGUMENTS`. If empty, start in guided mode.

**Behavior:**
- **Workflow mode:** guide provider/model configuration through OpenCode's native `/connect`. Never read, write, or recommend credential values, provider names, or model IDs.
- **Project mode:** detect empty directory vs. existing repo. Gather purpose, delivery profile, and git remote. Preview all changes and require explicit confirmation before mutating anything.
- Write or merge a project-local `AGENTS.md` from the setup assets.
- For Python projects, offer the normalized bootstrap: `uv`, Ruff, pytest, profile-gated Pyright/Nox, `src/` layout, and a `.gitignore`.
- Optionally establish a compact, opt-in Project Contract via the `project-contract` skill.