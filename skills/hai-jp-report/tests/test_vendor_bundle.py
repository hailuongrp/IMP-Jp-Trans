"""Exercise the offline vendor contract in disposable local repositories."""
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest


REPO = Path(__file__).resolve().parents[3]
HELPER = REPO / "dev" / "sync_hai_jp_vendor.py"
PIN = "03bc944a0c4a9f0b2a66eab065b30de5c529bf08"
VENDOR = Path("skills/hai-jp-report/vendor/natural-japanese")
LOCK = Path("skills/hai-jp-report/UPSTREAM.lock.json")


class VendorBundleChecks(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.base = tempfile.TemporaryDirectory()
        root = Path(cls.base.name)
        subprocess.run(["git", "init", "--quiet", str(root)], check=True)
        subprocess.run(["git", "-C", str(root), "fetch", "--quiet", "--no-tags",
                        str(REPO), PIN], check=True)
        shutil.copytree(REPO / "skills/natural-japanese", root / "skills/natural-japanese")
        shutil.copytree(REPO / VENDOR, root / VENDOR)
        shutil.copy2(REPO / "LICENSE", root / "LICENSE")
        shutil.copy2(REPO / LOCK, root / LOCK)

    @classmethod
    def tearDownClass(cls):
        cls.base.cleanup()

    def setUp(self):
        self.workspace = tempfile.TemporaryDirectory()
        self.addCleanup(self.workspace.cleanup)
        self.root = Path(self.workspace.name) / "repo"
        shutil.copytree(self.base.name, self.root)

    def run_helper(self, *args):
        env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
        return subprocess.run([sys.executable, str(HELPER), "--repo-root",
                               str(self.root), *args], capture_output=True,
                              text=True, env=env)

    def snapshot(self):
        return {p.relative_to(self.root).as_posix():
                (p.read_bytes(), p.stat().st_mode & 0o777)
                for p in self.root.rglob("*")
                if p.is_file() and ".git" not in p.relative_to(self.root).parts}

    def test_default_check_does_not_write(self):
        before = self.snapshot()
        result = self.run_helper()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(self.snapshot(), before)

    def test_changed_dependency_is_rejected_without_repair(self):
        path = self.root / VENDOR / "SKILL.md"
        path.write_bytes(path.read_bytes() + b"\nchanged\n")
        before = self.snapshot()
        result = self.run_helper("--check")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("checksum mismatch", result.stderr)
        self.assertEqual(self.snapshot(), before)

    def test_manifest_tampering_is_rejected(self):
        path = self.root / VENDOR / "UPSTREAM.json"
        manifest = json.loads(path.read_text())
        manifest["upstream"]["commit"] = "0" * 40
        path.write_text(json.dumps(manifest))
        self.assertNotEqual(self.run_helper().returncode, 0)

    def test_source_drift_blocks_sync(self):
        path = self.root / "skills/natural-japanese/SKILL.md"
        path.write_bytes(path.read_bytes() + b"\ndrift\n")
        before = self.snapshot()
        result = self.run_helper("--sync", "--commit", PIN)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Working upstream differs", result.stderr)
        self.assertEqual(self.snapshot(), before)

    def test_extra_file_and_empty_directory_are_rejected(self):
        path = self.root / VENDOR / ".unexpected"
        path.write_text("extra")
        self.assertNotEqual(self.run_helper().returncode, 0)
        path.unlink()
        path.mkdir()
        self.assertNotEqual(self.run_helper().returncode, 0)

    def test_symlink_is_rejected_before_sync_writes(self):
        outside = Path(self.workspace.name) / "outside.txt"
        outside.write_text("unchanged")
        path = self.root / VENDOR / "SKILL.md"
        path.unlink()
        path.symlink_to(outside)
        result = self.run_helper("--sync", "--commit", PIN)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Symlink", result.stderr)
        self.assertEqual(outside.read_text(), "unchanged")
        self.assertTrue(path.is_symlink())

    def test_sync_requires_the_exact_acknowledged_pin(self):
        before = self.snapshot()
        for args in [("--sync",), ("--sync", "--commit", "0" * 40)]:
            with self.subTest(args=args):
                self.assertNotEqual(self.run_helper(*args).returncode, 0)
                self.assertEqual(self.snapshot(), before)

    def test_sync_repairs_and_is_reproducible(self):
        path = self.root / VENDOR / "SKILL.md"
        path.write_text("damaged")
        result = self.run_helper("--sync", "--commit", PIN)
        self.assertEqual(result.returncode, 0, result.stderr)
        before = self.snapshot()
        result = self.run_helper("--sync", "--commit", PIN)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(self.snapshot(), before)
        self.assertEqual(self.run_helper().returncode, 0)

    def test_lock_source_and_bundle_drift_are_rejected(self):
        path = self.root / LOCK
        original = path.read_text()
        for key in ["source_commit", "source_tree_sha", "bundled_tree_sha"]:
            with self.subTest(key=key):
                lock = json.loads(original)
                lock[key] = "0" * 40
                path.write_text(json.dumps(lock))
                self.assertNotEqual(self.run_helper().returncode, 0)
        path.write_text("[]")
        self.assertNotEqual(self.run_helper().returncode, 0)

    def test_missing_file_and_changed_mode_are_rejected(self):
        path = self.root / VENDOR / "SKILL.md"
        original_mode = path.stat().st_mode & 0o777
        path.chmod(0o755)
        self.assertNotEqual(self.run_helper().returncode, 0)
        path.chmod(original_mode)
        path.unlink()
        self.assertNotEqual(self.run_helper().returncode, 0)
