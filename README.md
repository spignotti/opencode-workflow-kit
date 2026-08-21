# OpenCode Workflow Kit

A curated, provider-neutral OpenCode workflow: plan → build → review, with research and review subagents, project setup, git discipline, and data/geo/frontend guidance. It is a standalone snapshot of a larger private configuration — intentionally smaller, self-contained, and not kept in sync automatically.

Only OpenCode is supported. Claude Code, Codex, and other agents are out of scope.

## What It Is

- **Plan + Build primary agents** with a strict plan-lock and stop-authority execution model.
- **Seven subagents**: deep planning, research, external research, plan checking, contract review, integration review, and public-web research — each with a read-only evidence-probe permission contract.
- **Core controls**: evidence-first research protocol, review protocol with a severity model, behavioral test-quality checks.
- **Project delivery**: `/git` (conventional commits, profiles, secrets scan) and `/setup` (workflow configuration, project bootstrap, optional compact project contract).
- **Domain packs**: `data-work` (source/purpose/grain, schema invariants, reproducible transforms, independent validation) and `geospatial` (CRS, units, geometry/raster validity, Nodata, alignment, provenance).
- **Frontend guidance**: a reduced `frontend-design` skill with anti-pattern constraints, accessibility, and visual QA.

## What It Is Not

- **Not a provider or model bundle.** No provider names, model IDs, credentials, or API configuration ship in this repository. You configure your own provider once via OpenCode's `/connect`.
- **Not a personal setup.** No planning-service bindings, session databases, personal paths, or private workflow references.
- **Not continuously updated.** This is an independent snapshot. It does not auto-sync and no upstream feeds it.

## Included Layout

```
opencode-workflow-kit/
├── AGENTS.md               # runtime agent rules
├── opencode.json           # provider-neutral agent wiring (no models, no providers)
├── prompts/
│   ├── build.md            # manual implementation agent prompt
│   └── plan.md             # manual planning agent prompt
├── agents/                 # 7 review and research subagents
├── commands/
│   ├── git.md              # /git — repo-aware git workflow
│   └── setup.md            # /setup — workflow config and project bootstrap
├── skills/
│   ├── research-protocol/  # evidence-first research behavior
│   ├── review-protocol/    # shared review standard (with security/simplify/thermo refs)
│   ├── test-quality/       # behavioral test review
│   ├── git-workflow/       # commit/branch/PR/release workflows (with bootstrap/release refs)
│   ├── python-devops-stack/# uv/ruff/pyright/pytest/nox toolchain reference
│   ├── setup/              # provider-neutral setup skill with embedded project file recipes
│   ├── project-contract/   # compact opt-in technical contract + structural checker
│   ├── data-work/          # data methodology contract + tool catalogs
│   ├── geospatial/         # spatial guardrails + specialized references
│   └── frontend-design/    # reduced design guidance + anti-patterns + QA checklist
├── scripts/
│   └── validate_public_config.py   # config, reference, and privacy validation
├── tests/                  # stdlib unit tests for validator and contract checker
├── .github/                # issue templates + validation CI
├── LICENSE                 # MIT
├── SECURITY.md             # vulnerability reporting policy
└── install.sh              # safe release installer
```

## Prerequisites

OpenCode with your own provider configured. This repository contains no provider or model settings; set your default model in your own `opencode.json`.

## Installation

### Quick install

Download and inspect the installer, then run it:

```bash
curl -fsSL https://raw.githubusercontent.com/spignotti/opencode-workflow-kit/v1.0.0/install.sh > install.sh
less install.sh   # review before executing
bash install.sh
```

The default target is `./opencode-workflow-kit/`. To install elsewhere:

```bash
bash install.sh /path/to/target
```

Requirements: `curl` and `tar`. The installer never overwrites an existing directory.

### Manual install

Copy the files into your OpenCode config directories and adapt them to your setup.

#### Global install (all projects)

1. Find your OpenCode global config directory (see opencode.ai/docs/config for the platform-specific location, e.g. `$HOME/.config/opencode/` on macOS and Linux). Set it in the commands below:

```bash
export OPENCODE_CONFIG_DIR="$HOME/.config/opencode"   # adjust to your platform
mkdir -p "$OPENCODE_CONFIG_DIR"
```

2. Copy the kit trees without overwriting any existing file:

```bash
cp -Rn agents commands skills prompts "$OPENCODE_CONFIG_DIR/"
```

3. Merge `opencode.json` and `AGENTS.md` by hand. Do **not** copy them over your existing files — OpenCode deep-merges config from multiple sources, so:

   - Open your existing `$OPENCODE_CONFIG_DIR/opencode.json`, add any kit sections you want (agents, permissions), and keep your own keys. `{file:./prompts/...}` references only resolve if the prompts live in the same directory as the config, so either copy `prompts/` next to it or inline the prompt text.
   - Open your existing `$OPENCODE_CONFIG_DIR/AGENTS.md`, add the kit's rules that are missing, and keep your own sections.

#### Project-local install (single project)

```bash
export PROJECT="/path/to/your/project"     # adjust to your project
mkdir -p "$PROJECT/.opencode/commands" "$PROJECT/.opencode/skills"
cp -Rn agents prompts "$PROJECT/.opencode/"
cp commands/git.md commands/setup.md "$PROJECT/.opencode/commands/"
cp -Rn skills/* "$PROJECT/.opencode/skills/"
```

Then merge `AGENTS.md` and `opencode.json` into the project root as above: keep existing content, add the kit's missing sections by hand.

## Setup

1. **Connect a provider:** run `/connect` in OpenCode and authenticate your provider of choice. Credentials are stored by OpenCode; nothing here reads or writes them.
2. **Run `/setup`** to configure the workflow or bootstrap a project:
   - **Workflow mode:** verifies your config layout and points you at `/connect`. It never writes provider or model settings.
   - **Project mode:** detects new vs. existing repos, gathers purpose and delivery profile, previews all changes, and requires confirmation before writing a project-local `AGENTS.md`.
   - **Python route (optional):** normalized bootstrap with `uv`, Ruff, pytest, and profile-gated Pyright/Nox.
   - **Project contract (opt-in):** a compact, Git-versioned technical contract with a structural checker. Never automatic.

## Daily Use

- **Plan:** switch to the `plan` agent for scoping, research, and executable plans.
- **Build:** switch to `build` to execute approved plans with stop authority and review gates.
- **Review:** planned work is reviewed by the review subagents; integration boundaries get an adversarial integration review.
- **Git:** `/git commit`, `/git feature <desc>`, `/git pr`, `/git ship` route through the `git-workflow` skill using the project's delivery profile.

## Included Domain Packs

- **data-work** — process contract for every data task: source/purpose/grain, schema invariants, reproducible transforms, independent validation, uncertainty disclosure. Includes curated tool catalogs for engineering, science, and synthetic test data.
- **geospatial** — base guardrails (CRS, units, geometry/raster validity, Nodata, alignment, provenance) plus specialized references: remote sensing, spatial statistics, spatial features, spatial validation, DL on EO, spatial databases, geocoding, urban morphology, data sources, MCP servers.
- **frontend-design** — surface-type thinking, aesthetic direction, accessibility, anti-pattern constraints against generic UI output, and a visual QA checklist.

## Validation

From the repository root:

```bash
python3 scripts/validate_public_config.py   # config, reference, privacy checks
python3 -m unittest discover -s tests       # unit tests
```

CI (`.github/workflows/validate.yml`) runs the validator, the unit tests, and a secret scan on every push.

## Lifecycle

This repository is an independent snapshot. It is updated deliberately, not continuously:

- Content is curated from a private source configuration; there is no automated sync between the two.
- Additions follow the same review standards as any other change: validation, unit tests, and review before merge.
- MIT licensed — fork and adapt freely.

## License

MIT. See [LICENSE](LICENSE).