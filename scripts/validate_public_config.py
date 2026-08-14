#!/usr/bin/env python3
"""Validate the OpenCode workflow kit's runtime configuration.

Checks:
- opencode.json parses and uses only agent wiring (no provider/model/mcp keys)
- prompt file references ({file:./prompts/X.md}) resolve
- every agent referenced by a prompt exists under agents/
- every agents/*.md has well-formed frontmatter and no model: assignment
- no private or personal content (rtk, private skills, Notion, paths, emails, provider IDs)

Exit code 0 on success, 1 on any failure. Stdlib only.
"""

import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
AGENT_NAMES = (
    "plan-deep", "auto-research", "auto-research-external", "auto-review",
    "auto-review-integration", "auto-web-research-free", "auto-plan-checker",
)

PRIVACY_PATTERNS = [
    ("private tool wrapper", re.compile(r"(?i)\brtk\b")),
    ("private skill reference", re.compile(r"(?i)research-protocol|review-protocol|test-quality|project-contract")),
    ("Notion reference", re.compile(r"(?i)\bnotion\b")),
    ("personal home path", re.compile(r"~/(?:Documents|code|\.config|\.ssh|Downloads|Desktop)")),
    ("absolute user path", re.compile(r"/Users/[^/\s]+")),
    ("personal name", re.compile(r"(?i)\bpignotti\b|\bsilas\b")),
    ("email address", re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")),
    ("private repo reference", re.compile(r"context-engineering")),
    ("private workflow file", re.compile(r"(?i)project_state|notion-bridge|template-manager|session_maintenance")),
    ("provider or model id", re.compile(
        r"(?i)opencode-go|openrouter|deepseek|gpt-5\.6|gpt-4[o0-9.]*|claude-[a-z]|"
        r"qwen3?\.?7|gemini-|kimi-|glm-|mimo-|nemotron|longcat|laguna|ling-3|big-pickle|whitelist"
    )),
]


def fail(message):
    sys.stderr.write(f"validate-public-config: {message}\n")
    raise SystemExit(1)


def main():
    config_path = REPO / "opencode.json"
    try:
        config = json.loads(config_path.read_text())
    except (OSError, json.JSONDecodeError) as exc:
        fail(f"opencode.json: {exc}")

    for key in ("provider", "model", "small_model", "mcp", "enabled_providers", "disabled_providers", "whitelist"):
        if key in config:
            fail(f"opencode.json: forbidden top-level key {key!r}")

    # Reject provider/model keys at any depth (e.g. agent.<name>.model).
    def find_forbidden(node, path):
        if isinstance(node, dict):
            for key, value in node.items():
                if key in ("model", "provider", "small_model"):
                    fail(f"opencode.json: forbidden key {key!r} at {path or '<root>'}")
                find_forbidden(value, f"{path}/{key}")
        elif isinstance(node, list):
            for index, value in enumerate(node):
                find_forbidden(value, f"{path}[{index}]")

    find_forbidden(config, "")

    agents = config.get("agent", {})
    if not isinstance(agents, dict):
        fail("opencode.json: agent must be an object")

    for name in ("build", "plan"):
        agent = agents.get(name)
        if not agent or agent.get("mode") != "primary":
            fail(f"opencode.json: missing primary agent {name!r}")
        match = re.fullmatch(r"\{file:\./prompts/([a-z-]+)\.md\}", agent.get("prompt", ""))
        if not match:
            fail(f"opencode.json: agent {name!r} has no valid {{file:./prompts/...}} prompt reference")
        prompt_file = REPO / "prompts" / f"{match.group(1)}.md"
        if not prompt_file.is_file():
            fail(f"opencode.json: agent {name!r} prompt file missing: prompts/{match.group(1)}.md")

    prompt_texts = "".join(p.read_text(errors="replace") for p in (REPO / "prompts").glob("*.md"))
    for agent_name in AGENT_NAMES:
        if f"`{agent_name}`" in prompt_texts and not (REPO / "agents" / f"{agent_name}.md").is_file():
            fail(f"prompts: agent {agent_name!r} referenced but agents/{agent_name}.md is missing")

    for agent_file in sorted((REPO / "agents").glob("*.md")):
        text = agent_file.read_text(errors="replace")
        if not text.startswith("---\n") or "\n---\n" not in text:
            fail(f"{agent_file.name}: frontmatter must start with --- and close with a second --- line")
        frontmatter = text.split("\n---\n", 1)[0]
        if re.search(r"^\s*model\s*:", frontmatter, re.MULTILINE):
            fail(f"{agent_file.name}: model: assignment not allowed in public agents")

    scan_targets = list((REPO / "prompts").glob("*.md")) + list((REPO / "agents").glob("*.md"))
    scan_targets.append(config_path)
    for path in scan_targets:
        text = path.read_text(errors="replace")
        for label, pattern in PRIVACY_PATTERNS:
            match = pattern.search(text)
            if match:
                lineno = text.count("\n", 0, match.start()) + 1
                fail(f"{path.relative_to(REPO)}:{lineno}: {label}")

    print("validate-public-config: OK")


if __name__ == "__main__":
    main()
