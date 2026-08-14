# OpenCode Workflow Kit

A curated, generic OpenCode workflow: agent behavior rules, subagent contracts, and prompts. It is a downstream product of a larger private configuration, intentionally smaller, and not kept in sync automatically.

Only OpenCode is supported. Claude Code, Codex, and other agents are out of scope; translating the content for them is left to the user.

## Status

Pre-release. The repository ships a runtime `AGENTS.md`, provider-neutral primary agents (`build`, `plan`), review and research subagents, and their prompts. Commands and domain skills are intentionally deferred.

## What's Included

```
opencode-workflow-kit/
├── AGENTS.md               # runtime agent rules
├── opencode.json           # provider-neutral agent wiring (no models, no providers)
├── prompts/
│   ├── build.md            # manual implementation agent prompt
│   └── plan.md             # manual planning agent prompt
├── agents/                 # review and research subagents
│   ├── auto-research.md
│   ├── auto-research-external.md
│   ├── auto-review.md
│   ├── auto-review-integration.md
│   ├── auto-plan-checker.md
│   ├── auto-web-research-free.md
│   └── plan-deep.md
├── scripts/
│   └── validate_public_config.py   # config and reference validation
└── .github/workflows/validate.yml  # CI: config validation + secret scan
```

## Prerequisites

You must configure your own provider and model before use. The agent definitions in this repository carry no model or provider settings; set your default model in your own `opencode.json`.

## Installation

No installer yet. Until one exists, copy the files into your OpenCode global config directory (for example `$HOME/.config/opencode/` on macOS and Linux) and adapt them to your setup. The repository mirrors that directory's layout.

## Feedback

Issues are welcome for bug reports and suggestions. This is a personal project maintained in my own workflow; external pull requests are not actively maintained. The repository is MIT licensed, so you are free to fork and adapt it for your own use.

## License

MIT. See [LICENSE](LICENSE).
