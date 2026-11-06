"""Prevent historical demo/evaluation setup from deleting caller-owned paths."""
import importlib.util
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


class DemoSetupSafetyTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="sdd-demo-guard-")
        self.addCleanup(self.temp.cleanup)
        self.home = Path(self.temp.name).resolve() / "home"
        self.home.mkdir()
        script = (ROOT / "docs/handoff/macos-first-use/setup.sh").read_text(encoding="utf-8")
        self.guard_source = script.split("<<'PY'\n", 1)[1].split("\nPY\n", 1)[0]

    def guard(self, target):
        return subprocess.run([sys.executable, "-I", "-B", "-c", self.guard_source, str(target), str(self.home)],
                              capture_output=True, text=True, encoding="utf-8")

    def test_home_and_traversal_are_refused(self):
        for target in (str(self.home), str(self.home) + "/", str(self.home) + "/..", str(self.home) + "/sub/.."):
            with self.subTest(target=target):
                self.assertNotEqual(self.guard(target).returncode, 0)
        self.assertTrue(self.home.is_dir())

    def test_existing_directory_and_file_are_preserved(self):
        owned = self.home / "Documents"
        owned.mkdir()
        sentinel = owned / "keep.txt"
        sentinel.write_bytes(b"user data")
        for target in (owned, sentinel):
            self.assertNotEqual(self.guard(target).returncode, 0)
        self.assertEqual(sentinel.read_bytes(), b"user data")

    def test_fresh_child_is_resolved_without_writes(self):
        target = self.home / "new demo"
        result = self.guard(target)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(Path(result.stdout.strip()), target)
        self.assertFalse(target.exists())

    def test_legacy_runner_refuses_existing_base_without_subprocesses(self):
        spec = importlib.util.spec_from_file_location("legacy_eval", ROOT / "tests/run_behavior_evals.py")
        runner = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(runner)
        base = self.home / "base"
        base.mkdir()
        sentinel = base / "keep.txt"
        sentinel.write_bytes(b"user data")
        with self.assertRaisesRegex(ValueError, "refusing to replace"):
            runner.prepare_base(self.home / "missing-bundle", base)
        self.assertEqual(sentinel.read_bytes(), b"user data")


if __name__ == "__main__":
    unittest.main()
