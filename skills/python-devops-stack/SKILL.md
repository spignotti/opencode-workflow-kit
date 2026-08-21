---
name: python-devops-stack
description: Python toolchain reference for working in existing Python repositories — which nox sessions to run for which change type, how to migrate old tooling to uv/ruff/pyright/nox, and daily workflow commands. Load this skill when running validation in a Python project, deciding which nox sessions apply to a change, migrating a Python repo's toolchain, or needing the daily uv/nox workflow commands.
---
## Purpose

Use this skill when working in an existing Python repository.

This is the shared Python knowledge layer for `plan` and `build`. It covers how to operate, validate, and migrate Python projects — not how to scaffold new ones from scratch. New project bootstrapping is handled by a project setup workflow, not this skill.

## Python Stack

The standard Python toolchain for all projects:

- `uv` — package and environment management
- `ruff` — linting and formatting
- `pyright` — type checking
- `pytest` — tests
- `nox` — validation entrypoint

## Core Principles

- Keep Python setup simple, modern, and consistent
- One clear tool per concern — no overlapping responsibilities
- Use the lightest setup that still supports the project's scope
- Always leave the repository with a working validation path
- Make validation explicit and easy to run

## Validation Profiles

Use validation intensity that matches the change type. Always use the repository's actual `nox` session names when they differ from defaults.

| Change type | Validation |
|---|---|
| Docs, config, comments only | `nox -s lint` or skip |
| Structural (new modules, imports, type signatures) | `nox -s lint typecheck` |
| Logic or behavior changes | `nox -s lint typecheck test` |
| Checkpoint or release gate | `nox` (full default sessions) |

Do not default to full `nox` for every change — it defeats the purpose of having targeted sessions.

## Migration Guidance

When standardizing an existing Python repo, preserve existing functionality and migrate incrementally.

Migration direction:
- package management → `uv`
- lint/format → `ruff`
- type checking → `pyright`
- task runner → `nox`

Migration order:
1. audit the current toolchain and structure
2. create or update project `AGENTS.md`
3. migrate package management to `uv`
4. migrate lint/format to `ruff`
5. migrate type checking to `pyright`
6. migrate task runner to `nox`
7. verify end state: `uv run nox` must pass

Rules:
- migrate one tool at a time, verify after each step
- do not force a new layout unless the current one is broken
- do not remove working tests or restructure for style reasons alone
- keep working patterns that are already fine

## Daily Workflow

```bash
uv sync                    # sync dependencies
uv run nox -s fix          # lint and format (auto-fix)
uv run nox -s test         # run tests
uv run nox                 # full validation
```

Always use `uv add` to add dependencies — never hand-edit `pyproject.toml` dependency entries directly.

## Git Interaction

Validation before commit, push, PR, or release should go through `nox`. Use the validation profile that matches the action:
- commit → match the change type
- push/PR → at minimum `nox -s lint typecheck test`
- release → full `nox`

## Working Without a Configured Project

When Python work is needed outside a configured UV project:

### One-off Scripts
Use `uv run --with` to inject dependencies ad-hoc:
```bash
uv run --with pandas --with matplotlib python analyze_data.py
```

### Temporary Analysis Environment
For interactive work:
```bash
uv venv
source .venv/bin/activate  # `.venv\Scripts\activate` on Windows
uv pip install pandas matplotlib seaborn
# work...
deactivate
rm -rf .venv  # cleanup when done
```

### Scratch Project Pattern
For ad-hoc data work that needs persistence:
```bash
mkdir -p "${TMPDIR%/}/scratch/analysis-$(date +%Y%m%d)"
cd "${TMPDIR%/}/scratch/analysis-$(date +%Y%m%d)"
uv init --bare
uv add pandas matplotlib seaborn
# proper UV project ready for work
```

### Global CLI Tools
Installed via `uv tool install`:
- `ruff` — linting and formatting
- `pyright` — type checking
- `jupytext` — notebook synchronization
- `nox` — task runner

**Never:**
- Use `pip install` directly
- Install into system Python
- Install into user site-packages

## Tool Selection

When the task asks which Python utility, CLI helper, HTTP client, or developer aid to use, check `references/tools.md` first. Keep the canonical stack (`uv`, `ruff`, `pyright`, `pytest`, `nox`) unchanged; the catalog covers adjacent developer tooling.

## What Does Not Belong Here

- new project scaffolding, project structures, starter files → the project setup workflow
- release preparation, version bumping, changelog generation, tagging → `git-workflow` skill (`references/release.md`)
- git workflow decisions → `git-workflow` skill
- UI/data-app libraries (Streamlit/Shiny/Mercury), publishing tools (Quarto), browser testing (Playwright), monitoring stacks (Sentry/Grafana), cloud/container selection, and general data libraries → their owning domain skills, not this catalog

## Common Pitfalls

Pitfalls and edge cases that are easy to overlook when working with the Python toolchain.

**uv sync can update lockfile unexpectedly:**
`uv sync` after non-dependency metadata edits in `pyproject.toml` may still resolve newer package versions and rewrite `uv.lock` → for polish/docs/config-only work where dependency versions must stay unchanged, use `uv sync --frozen` (or skip sync) and avoid committing lock churn.

**nox + uv run:**
nox creates its own session virtualenvs, but `uv run` resolves tools from the project .venv. Use `session.run("uv", "run", "ruff", ...)` instead of `session.install("ruff")` to get dependencies available at tool runtime. Alternatively, add dev tools to project .venv with `uv add --dev` and use `uv run` in nox sessions — this is cleaner and avoids double-installs.

**uv run --active fails in nox contexts:**
Supposed to target the active virtualenv instead of project .venv, but causes "Failed to spawn" errors in nox session context. Not reliable — prefer explicit `uv run` pointing at project .venv.

**uv pip install in nox sessions:**
`session.install("uv", "pip", "install", "ruff")` does not work because nox runs Python from its own venv where pip's `__main__` module is not available. Use `session.run("uv", "pip", "install", ...)` instead with `external=True`.

**pyproject.toml readme field with hatchling:**
hatchling fails with "README.md does not exist" if `readme = "README.md"` is set and the file does not exist. Remove the field or create the file — the field is optional.

**hatchling + src layout:**
`[tool.hatch.build.targets.wheel]` with `packages = ["src"]` is needed for src-layout packages. Without it, hatchling cannot find the package.

**uv tool vs uv run:**
For CI/nox, use `uv run` with `--with` or project-installed tools. For local dev, `uv add --dev` to project .venv is simpler — `uv run ruff` etc. just works without `--with`.
