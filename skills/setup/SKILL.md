---
name: setup
description: Provider-neutral project bootstrap and OpenCode workflow configuration. Load when the user asks to set up a new project, configure providers or models via /connect, prepare an existing repo for this workflow, or writes a project-local AGENTS.md.
---

# Setup

Provider-neutral project bootstrap and OpenCode workflow configuration. It installs no provider or model settings, writes no credentials, and never mutates a project before explicit user confirmation.

## When to load

- The user asks to set up a new project, configure their OpenCode provider/model setup, or prepare an existing repo for this workflow.
- The user runs `/setup`.

## Two modes

### 1. Workflow mode

Guide the user through configuring their own provider and model:

- Run or point to OpenCode's native `/connect` command to authenticate providers. OpenCode stores credentials in its own auth store; do not read or write credential values.
- Verify the global config layout: `agents/`, `commands/`, and `skills/` directories are discoverable from the OpenCode global config directory (see opencode.ai/docs/config for the platform-specific location).
- Never write provider names, model IDs, API keys, base URLs, or environment-variable names into any config file. The kit stays provider-neutral; the user's `opencode.json` is their own.

### 2. Project mode

Bootstrap or migrate a project directory.

#### Detect

| Signal | Branch |
|---|---|
| Directory empty or only `.git`/`.gitignore` present | New project |
| `.git` exists with files, or files present without `.git` | Existing repo |

#### Interview (max 4 questions)

1. Project name and one-line purpose.
2. Delivery profile: `quick`, `standard`, `production`, or `published`.
3. Git remote URL, or "local only".
4. For Python projects: package name and whether the normalized Python route should be applied.

#### Propose and confirm

Present the exact set of files to create or merge and wait for explicit confirmation before any mutation. On an overwrite conflict with an existing file, stop and ask — never overwrite silently.

#### Compose project-local AGENTS.md

Compose from the target-file blocks below. For an existing project, merge the structural sections into any existing `AGENTS.md` — keep existing project-specific content, add the missing structural sections. For new projects, write the full file.

**Never** add planning-service references, session-state files, provider/model IDs, or personal paths.

##### Target file: `AGENTS.md`

```markdown
# <Project Name>

<Project purpose — one sentence>

## Delivery Profile

`<Delivery Profile>` — determined during setup.

- branch/commit/PR workflow → load `git-workflow` skill
- profile-specific gates → see below

## Tech Stack

- <detected or chosen stack, e.g. Python + uv, Node + pnpm>
- <key libraries and tooling>

## Structure

```
<project layout, e.g. src/<package>/ and tests/ for Python>
```

## Toolchain & Workflow

- <package manager / validation commands for this stack>
- Validation and toolchain decisions → load `python-devops-stack` skill (Python projects).
- Branch / commit / PR workflow → load `git-workflow` skill.

## Conventions

- follow existing patterns before introducing new ones
- keep it simple — build only what the project needs

## Secrets

When present, `.env.example` declares expected variable names.
Never commit secret values.

## Known Constraints

<!-- durable constraints agreed during setup are added here -->

## Project Contract

Status: not-required
Manifest: TECHNICAL_CONTRACT.md
Activation reason: none
Opt-out reason: none

<!-- Set to active only on explicit request: "set up a project contract". Never automatic. -->
```

#### Normalized Python route

Only when the user confirms it, and the repository is Python:

```bash
uv init            # creates pyproject.toml, src/<pkg>/ layout when --package is used
uv add --dev ruff pytest
uv run ruff check .
```

Profile gates:

| Profile | Gates added |
|---|---|
| `quick` | `uv` + `ruff` only |
| `standard` | `pytest`, optional `pyright`/`nox` |
| `production` | mandatory `pyright` + `nox` validation entrypoint |
| `published` | `production` gates + release ceremony via `git-workflow` (`references/release.md`) |

##### Target file: `.gitignore` (Python projects)

```gitignore
# Python
__pycache__/
*.py[cod]
.venv/
venv/
.nox/
.pytest_cache/
.ruff_cache/
.pyright/
*.egg-info/
build/
dist/
htmlcov/
.coverage

# Environment
.env
.env.*
!.env.example

# macOS
.DS_Store
```

For non-Python projects, do not fabricate a stack. Recommend only what the detected files support (e.g. `package.json` → Node/pnpm) and defer details to the user's own tooling.

#### Compact project contract (opt-in)

After setup, offer once: "Set up a project contract?" Default is no (`not-required`). On acceptance, load the `project-contract` skill and establish a compact contract. It is never activated automatically by a delivery profile.

## Rules

- Confirm before mutate. No mutation happens in workflow mode.
- No credentials, provider names, model IDs, or MCP configuration are ever written by this skill.
- Existing files are merged, never blindly replaced.
- Validation: after setup, verify the project config loads (`opencode --help` with the project config) and, for Python, `uv run nox` (or `uv run ruff check .` when nox is not part of the profile) passes.
