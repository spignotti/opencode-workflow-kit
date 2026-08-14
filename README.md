# OpenCode Workflow Kit

A curated, generic OpenCode workflow: agent behavior rules, subagent contracts, and domain skills. It is a downstream product of a larger private configuration, intentionally smaller, and not kept in sync automatically.

## Status

Pre-release. The repository currently ships a runtime `AGENTS.md`, provider-neutral primary agents (`build`, `plan`), review/research subagents, and their prompts. Commands and domain skills are intentionally deferred until their required skills are selected.

You must configure your own provider and model before use. The agent definitions in this repository carry no model or provider settings; set your default model in your own `opencode.json`.

## Layout

The repository mirrors the OpenCode global configuration layout:

```
opencode-workflow-kit/
├── AGENTS.md       # runtime agent rules
├── opencode.json   # provider-neutral agent wiring (no models, no providers)
├── prompts/        # build.md, plan.md
├── agents/         # review and research subagents
├── commands/       # planned: slash commands
└── skills/         # planned: domain skills
```

Only OpenCode is supported. Claude Code, Codex, and other agents are out of scope; translating the content for them is left to the user.
