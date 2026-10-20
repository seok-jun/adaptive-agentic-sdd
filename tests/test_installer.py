"""Installer regression checks for execution-grade / Epic policy migration.

Run with: python -I -B -m unittest discover -s tests -v
Only synthetic projects under this checkout are written.
"""

import contextlib
import importlib.util
import io
import json
from pathlib import Path
import shutil
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "ko" / "adaptive-sdd"
SPEC = importlib.util.spec_from_file_location("installer", SOURCE / "tools" / "install.py")
installer = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(installer)


class InstallerPolicyTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="sdd-policy-test-", dir=ROOT)
        self.project = Path(self.temp.name).resolve()
        self.assertIn(ROOT, self.project.parents)
        self.addCleanup(self.cleanup_project)
        self.copy = self.project / ".adaptive-sdd"
        shutil.copytree(SOURCE, self.copy)
        self.values = json.loads((self.copy / "templates" / "project.example.json").read_text(encoding="utf-8"))
        self.values["project"]["name"] = "Fictional library"
        self.values["tracker"]["root"] = (self.project / "tracker").as_posix()
        self.values_path = self.copy / "project.json"
        self.save_values()

    def cleanup_project(self):
        # Verify the recursive cleanup target remains under the checkout.
        if ROOT not in self.project.resolve().parents:
            raise RuntimeError("Test cleanup target escaped the checkout")
        self.temp.cleanup()

    def save_values(self):
        self.values_path.write_text(json.dumps(self.values, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    def command(self, name):
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            result = installer.main([name, "--project-root", str(self.project)])
        return result, output.getvalue()

    def test_all_execution_grades_load(self):
        self.values["grade_mapping"] = [
            {"change": "synthetic condition " + grade, "min_grade": grade}
            for grade in ("Trivial", "Small", "Medium", "Large")
        ]
        self.save_values()
        self.assertEqual(installer.load_values(self.project)["grade_mapping"], self.values["grade_mapping"])

    def test_management_type_and_unknown_grade_are_rejected(self):
        for grade in ("Epic", "Critical", "large"):
            with self.subTest(grade=grade):
                self.values["grade_mapping"] = [{"change": "synthetic condition", "min_grade": grade}]
                self.save_values()
                with self.assertRaises(installer.InstallError):
                    installer.load_values(self.project)

    def test_optional_grade_mapping_keeps_existing_empty_forms(self):
        self.values.pop("grade_mapping")
        self.save_values()
        self.assertNotIn("grade_mapping", installer.load_values(self.project))
        for value in (None, []):
            with self.subTest(value=value):
                self.values["grade_mapping"] = value
                self.save_values()
                self.assertEqual(installer.load_values(self.project)["grade_mapping"], value)

    def test_legacy_epic_mapping_cannot_partially_overwrite_installation(self):
        self.assertEqual(self.command("render")[0], 0)
        paths = [self.copy / "install.lock.json", self.copy / "project" / "sdd-workflow.md", self.project / "AGENTS.md"]
        before = {path: path.read_bytes() for path in paths}
        self.values["grade_mapping"] = [{"change": "new synthetic module", "min_grade": "Epic"}]
        self.save_values()
        code, _ = self.command("render")
        self.assertEqual(code, 2)
        self.assertEqual({path: path.read_bytes() for path in paths}, before)

    def test_render_check_for_both_trackers_and_merge_permissions(self):
        for tracker in ("local-docs", "github"):
            for manual_merge in (True, False):
                with self.subTest(tracker=tracker, manual_merge=manual_merge):
                    self.values["tracker"]["kind"] = tracker
                    self.values["human_judgment"]["large_epic_merge"] = manual_merge
                    self.save_values()
                    code, output = self.command("render")
                    self.assertEqual(code, 0, output)
                    code, output = self.command("check")
                    self.assertEqual(code, 0, output)
                    code, output = self.command("check-evals")
                    self.assertEqual(code, 0, output)
                    self.assertEqual(installer.load_values(self.project)["human_judgment"]["large_epic_merge"], manual_merge)
                    for tool in (".agents", ".claude"):
                        self.assertTrue((self.project / tool / "skills" / "managing-issues" / "SKILL.md").is_file())


if __name__ == "__main__":
    unittest.main()
