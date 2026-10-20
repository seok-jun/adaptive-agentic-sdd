"""Installer regression checks for grade policy and installed workflow references.

Run with: python -I -B -m unittest discover -s tests -v
Only synthetic projects under this checkout are written.
"""

import contextlib
import importlib.util
import io
import json
from pathlib import Path
import re
import shutil
import tempfile
import unicodedata
import unittest
from urllib.parse import unquote


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "ko" / "adaptive-sdd"
SPEC = importlib.util.spec_from_file_location("installer", SOURCE / "tools" / "install.py")
installer = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(installer)


def markdown_body(text):
    """Exclude examples in fenced code blocks from link/heading checks."""
    lines, fence = [], None
    for line in text.splitlines():
        marker = re.match(r"^\s*(`{3,}|~{3,})", line)
        if marker:
            char = marker.group(1)[0]
            fence = char if fence is None else (None if fence == char else fence)
        elif fence is None:
            lines.append(line)
    return "\n".join(lines)


def markdown_anchors(text):
    body = markdown_body(text)
    anchors = set(re.findall(r'<a\s+(?:id|name)=["\']([^"\']+)["\']', body))
    seen = {}
    for heading in re.findall(r"^#{1,6}\s+(.+?)(?:\s+#+)?$", body, re.MULTILINE):
        plain = re.sub(r"<[^>]+>", "", heading).lower()
        slug = "".join(
            char for char in plain
            if char in "-_ " or unicodedata.category(char)[0] not in "PS"
        ).replace(" ", "-")
        count = seen.get(slug, 0)
        seen[slug] = count + 1
        anchors.add(slug + (f"-{count}" if count else ""))
    return anchors


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

    def test_installed_workflow_and_project_links_resolve(self):
        code, output = self.command("render")
        self.assertEqual(code, 0, output)
        documents = list((self.copy / "workflow").rglob("*.md"))
        documents += list((self.copy / "project").rglob("*.md"))
        for document in documents:
            body = markdown_body(document.read_text(encoding="utf-8"))
            for reference in re.findall(r"\[[^\]\n]+\]\(([^)\s]+)\)", body):
                if re.match(r"\w+://|mailto:", reference) or any(c in reference for c in "{}<>"):
                    continue
                path, separator, fragment = unquote(reference).partition("#")
                target = (document.parent / path).resolve() if path else document
                with self.subTest(document=document.relative_to(self.copy), reference=reference):
                    self.assertTrue(target.is_file(), f"Missing installed target: {target}")
                    if separator:
                        self.assertIn(fragment, markdown_anchors(target.read_text(encoding="utf-8")))


if __name__ == "__main__":
    unittest.main()
