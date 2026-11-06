"""Prevent historical demo/evaluation setup from deleting caller-owned paths."""
import importlib.util
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

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

    def test_legacy_cli_refuses_existing_work_or_output_before_selection_or_calls(self):
        runner = ROOT / "tests/run_behavior_evals.py"
        for occupied in ("work", "out"):
            with self.subTest(occupied=occupied):
                case = self.home / occupied
                case.mkdir()
                work, out = case / "work", case / "out"
                target = work if occupied == "work" else out
                target.mkdir()
                sentinel = target / "keep.txt"
                sentinel.write_bytes(b"existing result")
                result = subprocess.run([sys.executable, "-I", "-B", str(runner),
                    "--selection", str(case / "missing-selection.json"),
                    "--workdir", str(work), "--out", str(out)], capture_output=True, text=True)
                self.assertNotEqual(result.returncode, 0)
                self.assertIn("fresh --workdir and --out", result.stderr)
                self.assertEqual(sentinel.read_bytes(), b"existing result")
                self.assertFalse((work / "base").exists())

    def test_legacy_output_reservation_preserves_racing_creator(self):
        spec = importlib.util.spec_from_file_location("legacy_race", ROOT / "tests/run_behavior_evals.py")
        runner = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(runner)
        work, out = self.home / "fresh-work", self.home / "fresh-out"
        selection = self.home / "selection.json"
        selection.write_text('{"runs_per_case": 1, "cases": {}}', encoding="utf-8")
        original_mkdir = Path.mkdir
        def racing_mkdir(path, *args, **kwargs):
            if path == out and not path.exists():
                original_mkdir(path)
                (path / "winner.txt").write_bytes(b"other run")
            return original_mkdir(path, *args, **kwargs)
        argv = [str(runner.__file__), "--selection", str(selection),
                "--workdir", str(work), "--out", str(out)]
        with mock.patch.object(sys, "argv", argv), mock.patch.object(Path, "mkdir", racing_mkdir), \
                mock.patch.object(runner, "prepare_base") as prepare:
            with self.assertRaisesRegex(SystemExit, "another creator won"):
                runner.main()
            prepare.assert_not_called()
        self.assertEqual((out / "winner.txt").read_bytes(), b"other run")
        self.assertFalse((work / "base").exists())

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
