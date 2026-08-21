"""Unit tests for the compact project contract checker.

Runs against synthetic project directories. Stdlib only.
"""

import importlib.util
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
CHECKER_PATH = REPO / "skills" / "project-contract" / "scripts" / "check_project_contract.py"
_spec = importlib.util.spec_from_file_location("check_project_contract", CHECKER_PATH)
_module = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_module)
checker = _module.check

MANIFEST = """# Technical Contract

`status`: active
`activation_reason`: manual
`opt_out_reason`: none

## Authority

Normative once active.

## Decisions

| ID | Decision | Status |
|---|---|---|
| DEC-0001 | accepted | accepted |

## Risk controls

| ID | Risk | Accepted control / decision | Required evidence | Decision ref |
|---|---|---|---|---|
| R-01 | failure | control | evidence | DEC-0001 |

## Open items

## Activation and change

- Activation: user approval; no blocking open items.
"""


class ContractCheckerTest(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)
        self.manifest = self.root / "TECHNICAL_CONTRACT.md"

    def tearDown(self):
        self._tmp.cleanup()

    def write_agents(self, body):
        (self.root / "AGENTS.md").write_text(body)

    def write_manifest(self, status_line="`status`: active"):
        content = MANIFEST.replace("`status`: active", status_line)
        self.manifest.write_text(content)

    def test_no_agents_missing(self):
        code, _ = checker(self.root)
        self.assertEqual(code, 2)

    def test_no_marker_not_required(self):
        self.write_agents("# Project\n")
        code, _ = checker(self.root)
        self.assertEqual(code, 0)

    def test_not_required_marker(self):
        self.write_agents(
            "# P\n\n## Project Contract\n\n"
            "Status: not-required\nManifest: TECHNICAL_CONTRACT.md\n"
            "Activation reason: none\nOpt-out reason: none\n")
        code, _ = checker(self.root)
        self.assertEqual(code, 0)

    def test_active_valid(self):
        self.write_agents(
            "# P\n\n## Project Contract\n\n"
            "Status: active\nManifest: TECHNICAL_CONTRACT.md\n"
            "Activation reason: manual\nOpt-out reason: none\n")
        self.write_manifest()
        code, result = checker(self.root)
        self.assertEqual(code, 0)
        self.assertEqual(result["status"], "active")

    def test_active_missing_manifest(self):
        self.write_agents(
            "# P\n\n## Project Contract\n\n"
            "Status: active\nManifest: TECHNICAL_CONTRACT.md\n"
            "Activation reason: manual\n")
        code, _ = checker(self.root)
        self.assertEqual(code, 2)

    def test_draft_not_actionable(self):
        self.write_agents(
            "# P\n\n## Project Contract\n\n"
            "Status: draft\nManifest: TECHNICAL_CONTRACT.md\n"
            "Activation reason: manual\n")
        self.write_manifest("`status`: draft")
        code, _ = checker(self.root)
        self.assertEqual(code, 2)

    def test_opted_out_ok(self):
        self.write_agents(
            "# P\n\n## Project Contract\n\n"
            "Status: opted-out\nManifest: TECHNICAL_CONTRACT.md\n"
            "Activation reason: none\nOpt-out reason: not needed\n")
        code, _ = checker(self.root)
        self.assertEqual(code, 0)

    def test_opted_out_without_reason(self):
        self.write_agents(
            "# P\n\n## Project Contract\n\n"
            "Status: opted-out\nManifest: TECHNICAL_CONTRACT.md\n"
            "Activation reason: none\nOpt-out reason: none\n")
        code, _ = checker(self.root)
        self.assertEqual(code, 2)

    def test_unsafe_manifest_path(self):
        self.write_agents(
            "# P\n\n## Project Contract\n\n"
            "Status: active\nManifest: ../outside/TECHNICAL_CONTRACT.md\n"
            "Activation reason: manual\n")
        code, _ = checker(self.root)
        self.assertEqual(code, 2)

    def test_status_mismatch(self):
        self.write_agents(
            "# P\n\n## Project Contract\n\n"
            "Status: active\nManifest: TECHNICAL_CONTRACT.md\n"
            "Activation reason: manual\n")
        self.write_manifest("`status`: draft")
        code, _ = checker(self.root)
        self.assertEqual(code, 2)


if __name__ == "__main__":
    unittest.main()