#!/usr/bin/env python3
"""Validate the OpenCode workflow kit's runtime configuration.

Checks:
- opencode.json parses and uses only agent wiring (no provider/model/mcp keys)
- prompt file references ({file:./prompts/X.md}) resolve
- every agent referenced by a prompt exists under agents/
- every agents/*.md and commands/*.md has well-formed frontmatter and no model: assignment
- every skills/*/SKILL.md has a valid name and description; name matches the directory
- skill references from prompts, agents, and commands resolve to shipped skills
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

SKILL_NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
SKILL_REF_RE = re.compile(r"`([a-z0-9]+(?:-[a-z0-9]+)*)`\s+skill")

# Exclusions from the privacy scan. LICENSE carries the copyright holder's
# name (the identity is public as the repository owner); the validator embeds
# the patterns it enforces and would self-flag.
PRIVACY_SCAN_EXCLUDE = {"LICENSE"}
VALIDATOR_PATH = Path(__file__).resolve()

# Exact public-source locators containing the GitHub owner name; only these
# specific URLs in the files listed beside them are permitted.  Any other
# personal-name occurrence remains fail-closed.
CANONICAL_SOURCE_URLS = {
    "README.md": re.compile(
        r"https://raw\.githubusercontent\.com/spignotti/opencode-workflow-kit/v1\.0\.0/install\.sh"
    ),
    "install.sh": re.compile(
        r"https://codeload\.github\.com/spignotti/opencode-workflow-kit/tar\.gz/refs/tags/v1\.0\.0"
    ),
}

SKIP_DIRS = {".git", "__pycache__", ".nox", ".venv", "node_modules"}


def fail(message):
    sys.stderr.write(f"validate-public-config: {message}\n")
    raise SystemExit(1)


def parse_frontmatter(text):
    """Return (fields dict, well_formed bool). Parses simple scalar lines only."""
    if not text.startswith("---\n"):
        return {}, False
    parts = text.split("\n---\n", 1)
    if len(parts) != 2:
        return {}, False
    fields = {}
    for line in parts[0].splitlines()[1:]:
        m = re.match(r"^\s*([A-Za-z0-9_-]+):\s*(.*)$", line)
        if m:
            fields[m.group(1)] = m.group(2).strip()
    return fields, True


def check_opencode_config(config_path):
    try:
        config = json.loads(config_path.read_text())
    except (OSError, json.JSONDecodeError) as exc:
        fail(f"opencode.json: {exc}")

    for key in ("provider", "model", "small_model", "mcp", "enabled_providers", "disabled_providers", "whitelist"):
        if key in config:
            fail(f"opencode.json: forbidden top-level key {key!r}")

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


def check_prompt_agent_refs():
    prompt_texts = "".join(p.read_text(errors="replace") for p in (REPO / "prompts").glob("*.md"))
    for agent_name in AGENT_NAMES:
        if f"`{agent_name}`" in prompt_texts and not (REPO / "agents" / f"{agent_name}.md").is_file():
            fail(f"prompts: agent {agent_name!r} referenced but agents/{agent_name}.md is missing")


def check_agent_files():
    for agent_file in sorted((REPO / "agents").glob("*.md")):
        text = agent_file.read_text(errors="replace")
        if not text.startswith("---\n") or "\n---\n" not in text:
            fail(f"{agent_file.name}: frontmatter must start with --- and close with a second --- line")
        frontmatter = text.split("\n---\n", 1)[0]
        if re.search(r"^\s*model\s*:", frontmatter, re.MULTILINE):
            fail(f"{agent_file.name}: model: assignment not allowed in public agents")


def check_command_files():
    # Configured agents: opencode.json agent keys, agents/*.md files, built-ins.
    config = json.loads((REPO / "opencode.json").read_text())
    configured = set(config.get("agent", {}))
    configured.update(p.stem for p in (REPO / "agents").glob("*.md"))
    configured.update({"build", "plan", "general", "explore", "scout"})

    for command_file in sorted((REPO / "commands").glob("*.md")):
        text = command_file.read_text(errors="replace")
        fields, ok = parse_frontmatter(text)
        if not ok:
            fail(f"{command_file.name}: frontmatter must start with --- and close with a second --- line")
        if not fields.get("description"):
            fail(f"{command_file.name}: command requires a description in frontmatter")
        if "model" in fields:
            fail(f"{command_file.name}: model: assignment not allowed in public commands")
        agent = fields.get("agent")
        if agent and agent not in configured:
            fail(f"{command_file.name}: agent {agent!r} is not a configured or built-in agent")


def check_skill_files():
    skills_dir = REPO / "skills"
    if not skills_dir.is_dir():
        return
    for skill_dir in sorted(skills_dir.iterdir()):
        if not skill_dir.is_dir():
            continue
        skill_md = skill_dir / "SKILL.md"
        if not skill_md.is_file():
            fail(f"skills/{skill_dir.name}: missing SKILL.md")
        text = skill_md.read_text(errors="replace")
        fields, ok = parse_frontmatter(text)
        if not ok:
            fail(f"skills/{skill_dir.name}/SKILL.md: frontmatter must start with --- and close with a second --- line")
        name = fields.get("name")
        description = fields.get("description")
        if not name:
            fail(f"skills/{skill_dir.name}/SKILL.md: missing required frontmatter name")
        if not description:
            fail(f"skills/{skill_dir.name}/SKILL.md: missing required frontmatter description")
        if not SKILL_NAME_RE.match(name):
            fail(f"skills/{skill_dir.name}/SKILL.md: invalid skill name {name!r}")
        if name != skill_dir.name:
            fail(f"skills/{skill_dir.name}/SKILL.md: frontmatter name {name!r} must match directory name")


def check_skill_refs():
    if not (REPO / "skills").is_dir():
        return
    skills_dir = REPO / "skills"
    scan = list((REPO / "prompts").glob("*.md")) + list((REPO / "agents").glob("*.md")) \
        + list((REPO / "commands").glob("*.md")) + list(skills_dir.glob("**/*.md"))
    for path in scan:
        text = path.read_text(errors="replace")
        for name in SKILL_REF_RE.findall(text):
            if not (skills_dir / name / "SKILL.md").is_file():
                fail(f"{path.relative_to(REPO)}: references skill {name!r} but skills/{name}/SKILL.md is missing")


def check_privacy():
    """Scan every shipped file, excluding only LICENSE and this validator."""
    scan_targets = [p for p in REPO.rglob("*")
                    if p.is_file()
                    and not any(part in SKIP_DIRS for part in p.relative_to(REPO).parts)
                    and p.name not in PRIVACY_SCAN_EXCLUDE
                    and p.resolve() != VALIDATOR_PATH]

    for path in scan_targets:
        text = path.read_text(errors="replace")
        rel = str(path.relative_to(REPO))
        for label, pattern in PRIVACY_PATTERNS:
            for lineno, line in enumerate(text.splitlines(), 1):
                if pattern.search(line):
                    # Allow exact canonical public-source locator URLs on
                    # lines that contain them; any other match fails.
                    if label == "personal name" and rel in CANONICAL_SOURCE_URLS:
                        if CANONICAL_SOURCE_URLS[rel].search(line):
                            continue
                    fail(f"{path.relative_to(REPO)}:{lineno}: {label}")


def main():
    check_opencode_config(REPO / "opencode.json")
    check_prompt_agent_refs()
    check_agent_files()
    check_command_files()
    check_skill_files()
    check_skill_refs()
    check_privacy()

    print("validate-public-config: OK")


if __name__ == "__main__":
    main()