"""Unit tests for scripts/validate_public_config.py.

Runs against synthetic kit layouts in temporary directories; the module-level
REPO constant is patched per test. Stdlib only.

The privacy scan covers every file in the kit, including tests, so banned
marker strings are constructed at runtime instead of written literally.
"""

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
_spec = importlib.util.spec_from_file_location(
    "validate_public_config", REPO / "scripts" / "validate_public_config.py")
v = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(v)

MK_A = "not" + "ion"
MK_B = "r" + "tk"
MK_C = "opencode-" + "go"


class ValidatorTest(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)
        v.REPO = self.root
        self.build_kit()

    def tearDown(self):
        v.REPO = Path(__file__).resolve().parent.parent
        self._tmp.cleanup()

    def build_kit(self):
        (self.root / "prompts").mkdir()
        (self.root / "agents").mkdir()
        (self.root / "commands").mkdir()
        (self.root / "skills").mkdir()
        (self.root / "AGENTS.md").write_text("# Rules\n")
        (self.root / "README.md").write_text("# Kit\n")
        (self.root / "SECURITY.md").write_text("# Security\n")
        (self.root / "opencode.json").write_text(json.dumps({
            "$schema": "https://opencode.ai/config.json",
            "agent": {
                "build": {"mode": "primary", "prompt": "{file:./prompts/build.md}"},
                "plan": {"mode": "primary", "prompt": "{file:./prompts/plan.md}"},
            },
        }))
        (self.root / "prompts" / "build.md").write_text("Build agent.\n")
        (self.root / "prompts" / "plan.md").write_text("Plan agent.\n")
        for name in v.AGENT_NAMES:
            (self.root / "agents" / f"{name}.md").write_text(
                "---\ndescription: test agent\nmode: subagent\n---\nBody.\n")
        (self.root / "commands" / "git.md").write_text(
            "---\ndescription: git workflow\ragent: build\n---\nLoad the `git-workflow` skill.\n")
        skill = self.root / "skills" / "git-workflow"
        skill.mkdir()
        (skill / "SKILL.md").write_text(
            "---\nname: git-workflow\ndescription: git workflow guidance\n---\nBody.\n")

    def test_valid_kit_passes(self):
        self.assertEqual(v.main(), None)

    def test_forbidden_config_key(self):
        config = json.loads((self.root / "opencode.json").read_text())
        config["model"] = "some/provider"
        (self.root / "opencode.json").write_text(json.dumps(config))
        with self.assertRaises(SystemExit) as ctx:
            v.main()
        self.assertEqual(ctx.exception.code, 1)

    def test_missing_prompt_target(self):
        (self.root / "prompts" / "plan.md").unlink()
        with self.assertRaises(SystemExit):
            v.main()

    def test_missing_agent_reference(self):
        (self.root / "prompts" / "plan.md").write_text("Use `auto-review` for reviews.\n")
        (self.root / "agents" / "auto-review.md").unlink()
        with self.assertRaises(SystemExit):
            v.main()

    def test_agent_model_assignment(self):
        (self.root / "agents" / "auto-review.md").write_text(
            "---\ndescription: x\nmodel: some/model\n---\n")
        with self.assertRaises(SystemExit):
            v.main()

    def test_command_missing_description(self):
        (self.root / "commands" / "git.md").write_text(
            "---\nagent: build\n---\nBody.\n")
        with self.assertRaises(SystemExit):
            v.main()

    def test_command_unknown_agent(self):
        (self.root / "commands" / "git.md").write_text(
            "---\ndescription: x\nagent: nope\n---\nBody.\n")
        with self.assertRaises(SystemExit):
            v.main()

    def test_skill_name_mismatch(self):
        skill = self.root / "skills" / "git-workflow"
        (skill / "SKILL.md").write_text(
            "---\nname: other-name\ndescription: x\n---\n")
        with self.assertRaises(SystemExit):
            v.main()

    def test_skill_missing_name(self):
        skill = self.root / "skills" / "git-workflow"
        (skill / "SKILL.md").write_text(
            "---\ndescription: x\n---\n")
        with self.assertRaises(SystemExit):
            v.main()

    def test_missing_skill_target(self):
        (self.root / "commands" / "git.md").write_text(
            "---\ndescription: x\nagent: build\n---\nLoad the `not-a-skill` skill.\n")
        with self.assertRaises(SystemExit):
            v.main()

    def test_privacy_violation(self):
        (self.root / "README.md").write_text(f"private {MK_A} reference\n")
        with self.assertRaises(SystemExit) as ctx:
            v.main()
        self.assertEqual(ctx.exception.code, 1)

    def test_privacy_violation_in_script(self):
        (self.root / "scripts").mkdir()
        (self.root / "scripts" / "tool.py").write_text(f"uses {MK_B}\n")
        with self.assertRaises(SystemExit):
            v.main()

    def test_provider_marker_in_skill(self):
        skill = self.root / "skills" / "git-workflow"
        (skill / "SKILL.md").write_text(
            "---\nname: git-workflow\ndescription: x\n---\n" + MK_C + "\n")
        with self.assertRaises(SystemExit):
            v.main()


if __name__ == "__main__":
    unittest.main()