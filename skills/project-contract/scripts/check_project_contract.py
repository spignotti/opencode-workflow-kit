#!/usr/bin/env python3
"""Structural validator for a project's compact Project Contract.

Reads the `## Project Contract` marker in AGENTS.md and the single contract
manifest (TECHNICAL_CONTRACT.md). Proves shape and references only. It never
claims semantic validity.

Exit codes:
  0 - valid not-required, valid active, or explicit opted-out with reason
  2 - missing required active artifacts, draft, structurally invalid, or unsafe path

Read-only. No writes, no external dependencies.

Usage:
    check_project_contract.py --root <project_dir> [--json]
"""

import argparse
import json
import re
import sys
from pathlib import Path, PurePath


MANIFEST_NAME = "TECHNICAL_CONTRACT.md"
MANIFEST_HEADINGS = ["## Authority", "## Decisions", "## Risk controls", "## Open items"]
VALID_STATUSES = {"draft", "active", "opted-out", "not-required"}
MANIFEST_REQUIRED_KEYS = ("status", "activation_reason")


def read_text(path: Path) -> str | None:
    try:
        return path.read_text(encoding="utf-8")
    except OSError:
        return None


def parse_marker(content: str) -> dict:
    """Extract the Project Contract marker from AGENTS.md."""
    field_re = re.compile(r"^\s*([A-Za-z_ -]+?):\s*(.*)$")
    in_section = False
    marker = {}
    for line in content.splitlines():
        if line.strip().lower().startswith("## project contract"):
            in_section = True
            continue
        if in_section and line.startswith("## "):
            break
        if in_section:
            m = field_re.match(line)
            if m:
                key = m.group(1).strip().lower().replace(" ", "_").replace("-", "_")
                marker[key] = m.group(2).strip()
    return marker


def manifest_key(content: str, key: str) -> str | None:
    m = re.search(rf"^\s*`{re.escape(key)}`:\s*(.*)$", content, re.M)
    return m.group(1).strip() if m else None


def resolve_manifest(root: Path, name: str) -> Path | None:
    """Return a safe manifest path under root, or None if the name is unsafe.

    Rejects absolute paths and any traversal that escapes the project boundary.
    """
    p = PurePath(name)
    if p.is_absolute() or ".." in p.parts:
        return None
    candidate = root / name
    try:
        resolved = candidate.resolve()
        if not resolved.is_relative_to(root.resolve()):
            return None
    except (OSError, ValueError):
        return None
    return candidate


def check(root: Path) -> tuple[int, dict]:
    issues: list[str] = []
    agents = root / "AGENTS.md"
    if not root.is_dir():
        return 2, {
            "status": "invalid", "issues": [f"root directory does not exist: {root}"],
            "marker": {}, "manifest": {"present": False},
        }
    if not agents.exists():
        return 2, {
            "status": "invalid", "issues": ["AGENTS.md is missing; cannot determine contract requirement"],
            "marker": {}, "manifest": {"present": False},
        }
    agents_content = read_text(agents)
    if agents_content is None:
        return 2, {
            "status": "invalid", "issues": [f"cannot read {agents}"],
            "marker": {}, "manifest": {"present": False},
        }

    marker = parse_marker(agents_content)
    status = marker.get("status", "missing")

    # A Project Contract section that exists but carries no status must not be
    # silently treated as not-required.
    has_section = "## project contract" in agents_content.lower()
    if status == "missing" and has_section:
        return 2, {
            "status": "invalid",
            "issues": ["Project Contract section present but status field missing"],
            "marker": marker, "manifest": {"present": False},
        }

    # A project with no marker has no contract requirement (opt-in only).
    if status == "missing":
        return 0, {
            "status": "not-required",
            "issues": [],
            "marker": {},
            "manifest": {"present": False},
        }

    if status not in VALID_STATUSES:
        issues.append(f"invalid contract status in marker: {status!r}")

    if status == "not-required":
        return (2 if issues else 0, {
            "status": status, "issues": issues, "marker": marker,
            "manifest": {"present": False},
        })

    if status == "opted-out":
        reason = marker.get("opt_out_reason")
        if not reason or reason.lower() in {"none", "n/a", "-"}:
            issues.append("opted-out contract requires an explicit opt-out reason")
        return (2 if issues else 0, {
            "status": status, "issues": issues, "marker": marker,
            "manifest": {"present": False},
        })

    # draft / active require a manifest path in the marker.
    manifest_name = marker.get("manifest")
    if not manifest_name or manifest_name == "none":
        return 2, {
            "status": status, "issues": ["active/draft contract requires a manifest path in the marker"],
            "marker": marker, "manifest": {"present": False},
        }
    manifest_path = resolve_manifest(root, manifest_name)
    if manifest_path is None:
        return 2, {
            "status": status,
            "issues": [f"manifest path is unsafe (absolute or outside project): {manifest_name}"],
            "marker": marker, "manifest": {"present": False},
        }
    if not manifest_path.exists():
        return 2, {
            "status": status, "issues": [f"{manifest_name} is missing (status={status})"],
            "marker": marker, "manifest": {"present": False},
        }

    if status == "active" and not marker.get("activation_reason"):
        issues.append("active contract missing activation reason in marker")

    content = read_text(manifest_path) or ""
    for heading in MANIFEST_HEADINGS:
        if heading not in content:
            issues.append(f"manifest missing required heading {heading}")
    for key in MANIFEST_REQUIRED_KEYS:
        if manifest_key(content, key) is None:
            issues.append(f"manifest missing required key `{key}`")

    manifest_status = manifest_key(content, "status")
    manifest_reason = manifest_key(content, "activation_reason")
    if status == "active":
        if manifest_status != "active":
            issues.append(f"manifest status is {manifest_status!r}, expected 'active' for active contract")
        if not manifest_reason:
            issues.append("active contract missing activation_reason")
    elif status == "draft":
        issues.append("draft contract is not actionable")

    verified = {
        "status": status,
        "manifest_status": manifest_status,
        "activation_reason": manifest_reason,
        "manifest_path": manifest_path.as_posix(),
        "issues": issues,
        "marker": marker,
        "manifest": {"present": True},
    }
    return (0 if not issues else 2, verified)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=".", help="project root directory")
    parser.add_argument("--json", action="store_true", help="emit JSON")
    args = parser.parse_args(argv)

    code, result = check(Path(args.root))
    result["root"] = str(Path(args.root).resolve())
    result["exit_code"] = code

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(f"Project Contract status: {result['status']} (exit {code})")
        for issue in result["issues"]:
            print(f"  - {issue}")
    return code


if __name__ == "__main__":
    sys.exit(main())