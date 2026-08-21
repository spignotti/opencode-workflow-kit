"""Integration tests for install.sh.

Runs against a fake curl and synthetic tarball in a temp directory.
No real network access. Stdlib only.
"""

import io
import os
import shutil
import stat
import subprocess
import tarfile
import tempfile
import unittest
from pathlib import Path


REPO = Path(__file__).resolve().parent.parent
INSTALL_SCRIPT = REPO / "install.sh"


def _write_installer_script(tmpdir, fake_bin_dir):
    """Create a patched install.sh that uses our fake curl."""
    script = INSTALL_SCRIPT.read_text()
    # Replace the real curl call with our fake curl
    patched = script.replace(
        'command -v "$cmd" >/dev/null 2>&1',
        f'command -v "$cmd" >/dev/null 2>&1 || [ "$cmd" = "curl" ]',
    )
    patched = patched.replace(
        "curl -fsSL -o",
        f"{fake_bin_dir}/curl-fake -o",
    )
    target = tmpdir / "install.sh"
    target.write_text(patched)
    target.chmod(target.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP)
    return target


def _create_fake_curl(tmpdir, archive_path):
    """Create a fake curl that copies our archive to the destination."""
    fake_bin = tmpdir / "bin"
    fake_bin.mkdir()
    curl_script = fake_bin / "curl-fake"
    curl_script.write_text(
        f"#!/usr/bin/env bash\n"
        f"set -euo pipefail\n"
        f"OUTFILE=\"\"\n"
        f"while [ $# -gt 0 ]; do\n"
        f'  case "$1" in\n'
        f"    -o) OUTFILE=\"$2\"; shift 2 ;;\n"
        f"    *) shift ;;\n"
        f"  esac\n"
        f"done\n"
        f'cp "{archive_path}" "$OUTFILE"\n',
    )
    curl_script.chmod(curl_script.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP)
    return fake_bin


def _make_archive(tmpdir, files=None):
    """Create a tar.gz archive with content mimicking a GitHub release."""
    files = files or {"AGENTS.md": "# Kit\n"}
    archive_path = tmpdir / "release.tar.gz"
    with tarfile.open(archive_path, "w:gz") as tar:
        for name, content in files.items():
            info = tarfile.TarInfo(name=f"opencode-workflow-kit-v1.0.0/{name}")
            data = io.BytesIO(content.encode())
            info.size = len(data.getvalue())
            tar.addfile(info, data)
    return archive_path


class InstallerTest(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.mkdtemp()
        self._tmpdir = Path(self._tmp)

    def tearDown(self):
        shutil.rmtree(self._tmp, ignore_errors=True)

    def _run(self, args=None, env=None):
        installer = _write_installer_script(self._tmpdir, self._tmpdir / "bin")
        archive = _make_archive(self._tmpdir)
        _create_fake_curl(self._tmpdir, archive)
        run_env = os.environ.copy()
        run_env["PATH"] = f"{self._tmpdir / 'bin'}:{run_env.get('PATH', '')}"
        run_env["TMPDIR"] = self._tmp
        if env:
            run_env.update(env)
        cmd = ["bash", str(installer)]
        if args:
            cmd += args
        return subprocess.run(cmd, capture_output=True, text=True, env=run_env)

    def test_default_install_succeeds(self):
        target = self._tmpdir / "opencode-workflow-kit"
        r = self._run(args=[str(target)])
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertTrue(target.is_dir())
        self.assertTrue((target / "AGENTS.md").exists())

    def test_custom_target_works(self):
        custom = self._tmpdir / "my-kit"
        r = self._run(args=[str(custom)])
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertTrue(custom.is_dir())
        self.assertTrue((custom / "AGENTS.md").exists())

    def test_existing_target_fails_untouched(self):
        target = self._tmpdir / "opencode-workflow-kit"
        target.mkdir()
        (target / "existing.txt").write_text("keep")
        r = self._run(args=[str(target)])
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("already exists", r.stderr)
        self.assertTrue((target / "existing.txt").exists())

    def test_no_target_on_download_failure(self):
        """Simulate curl failure: fake curl exits 1 when called."""
        fake_bin = self._tmpdir / "bin"
        fake_bin.mkdir()
        curl_script = fake_bin / "curl-fake"
        curl_script.write_text("#!/usr/bin/env bash\nexit 1\n")
        curl_script.chmod(curl_script.stat().st_mode | stat.S_IXUSR)
        # Patch the install script manually
        script = INSTALL_SCRIPT.read_text()
        script = script.replace(
            "command -v \"$cmd\" >/dev/null 2>&1",
            f"command -v \"$cmd\" >/dev/null 2>&1 || [ \"$cmd\" = \"curl\" ]",
        )
        script = script.replace("curl -fsSL -o", f"{fake_bin}/curl-fake -o")
        installer = self._tmpdir / "install.sh"
        installer.write_text(script)
        installer.chmod(installer.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP)
        run_env = os.environ.copy()
        run_env["PATH"] = f"{fake_bin}:{run_env.get('PATH', '')}"
        run_env["TMPDIR"] = self._tmp
        r = subprocess.run(["bash", str(installer)], capture_output=True, text=True, env=run_env)
        self.assertNotEqual(r.returncode, 0)
        target = self._tmpdir / "opencode-workflow-kit"
        self.assertFalse(target.exists())


if __name__ == "__main__":
    unittest.main()
