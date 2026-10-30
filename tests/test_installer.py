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
import subprocess
import sys
import tempfile
import unicodedata
import unittest
from unittest import mock
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

    def command(self, name, *arguments):
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            result = installer.main([name, "--project-root", str(self.project), *arguments])
        return result, output.getvalue()

    def test_untagged_commit_upgrade_drops_previous_tag(self):
        self.assertEqual(self.command("render", "--source-tag", "v-test.1", "--source-commit", "a" * 40)[0], 0)
        self.assertEqual(self.command("render", "--source-commit", "b" * 40)[0], 0)
        source = installer.load_lock(self.project)["source"]
        self.assertNotIn("tag", source)
        self.assertEqual(source["commit"], "b" * 40)
        self.assertEqual(self.command("check")[0], 0)

    def test_same_source_render_preserves_tag_and_explicit_upgrade_replaces_pair(self):
        self.assertEqual(self.command("render", "--source-tag", "v-test.1", "--source-commit", "a" * 40)[0], 0)
        for arguments in ((), ("--source-commit", "a" * 40)):
            self.assertEqual(self.command("render", *arguments)[0], 0)
            self.assertEqual(installer.load_lock(self.project)["source"]["tag"], "v-test.1")
        self.assertEqual(self.command("render", "--source-tag", "v-test.2", "--source-commit", "b" * 40)[0], 0)
        source = installer.load_lock(self.project)["source"]
        self.assertEqual((source["tag"], source["commit"]), ("v-test.2", "b" * 40))

    def test_clear_source_tag_repairs_existing_identity_without_changing_commit(self):
        self.assertEqual(self.command("render", "--source-tag", "v-test.1", "--source-commit", "a" * 40)[0], 0)
        self.assertEqual(self.command("render", "--clear-source-tag")[0], 0)
        source = installer.load_lock(self.project)["source"]
        self.assertNotIn("tag", source)
        self.assertEqual(source["commit"], "a" * 40)
        self.assertEqual(self.command("check")[0], 0)

    def test_tag_without_commit_is_rejected_before_any_output_write(self):
        self.assertEqual(self.command("render", "--source-tag", "v-test.1", "--source-commit", "a" * 40)[0], 0)
        paths = [self.copy / "install.lock.json", self.project / "AGENTS.md"]
        before = {path: path.read_bytes() for path in paths}
        self.values["project"]["name"] = "Changed fictional library"
        self.save_values()
        code, _ = self.command("render", "--source-tag", "v-test.2")
        self.assertEqual(code, 2)
        self.assertEqual({path: path.read_bytes() for path in paths}, before)

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

    def test_split_rules_and_artifact_templates_are_verified_in_installed_copy(self):
        self.assertEqual(self.command("render")[0], 0)
        for relative in ("workflow/process/sdd/issue.md", "templates/sdd/01-as-is.md.tmpl"):
            path = self.copy / relative
            original = path.read_bytes()
            path.write_bytes(original + b"\ntampered\n")
            self.assertIn((relative, "DIFF"), installer.verify_copy(self.project))
            path.unlink()
            self.assertIn((relative, "MISSING"), installer.verify_copy(self.project))
            path.write_bytes(original)
        self.assertEqual(self.command("check")[0], 0)

    def external_install(self):
        product = self.project / "product"
        source = self.project / "harness"
        product.mkdir()
        shutil.copytree(SOURCE, source / ".adaptive-sdd")
        (source / ".adaptive-sdd/project.json").write_bytes(self.values_path.read_bytes())
        return source, product

    def external_command(self, name, product, source=None):
        args = [name, "--project-root", str(product)]
        if source:
            args += ["--harness-root", str(source)]
        with contextlib.redirect_stdout(io.StringIO()):
            return installer.main(args)

    def test_external_layout_and_connection_check(self):
        source, product = self.external_install()
        (product / "AGENTS.md").write_text("# Existing product policy\n", encoding="utf-8")
        self.assertEqual(self.external_command("render", product, source), 0)
        self.assertTrue((source / ".adaptive-sdd/project/build.md").is_file())
        self.assertFalse((product / ".adaptive-sdd").exists())
        self.assertFalse((source / ".agents").exists())
        self.assertTrue((product / ".agents/skills/implementing-issues/SKILL.md").is_file())
        self.assertTrue((product / "AGENTS.md").read_text(encoding="utf-8").startswith("# Existing product policy"))
        self.assertEqual(self.external_command("check", product), 0)
        self.assertEqual(self.external_command("check-evals", product), 0)
        connection = json.loads((product / installer.CONNECTION).read_bytes())
        self.assertEqual(connection["harness_root"], source.as_posix())
        self.assertEqual(installer.load_lock(source)["project_root"], product.as_posix())

    def test_entry_paths_resolve_without_a_fourth_role(self):
        for external in (False, True):
            with self.subTest(external=external):
                if external:
                    source, product = self.external_install()
                    self.assertEqual(self.external_command("render", product, source), 0)
                    bundle = (source / ".adaptive-sdd").as_posix()
                else:
                    source, product = self.project, self.project
                    self.assertEqual(self.command("render")[0], 0)
                    bundle = "P/.adaptive-sdd"
                for rel in ("AGENTS.md", ".agents/skills/implementing-issues/SKILL.md",
                            ".claude/skills/implementing-issues/SKILL.md"):
                    text = (product / rel).read_text(encoding="utf-8")
                    self.assertNotIn("`S`", text)
                    self.assertNotIn("S/.adaptive-sdd", text)
                    self.assertNotIn("{{", text)
                    for suffix in ("workflow", "methodology", "project.json", "project/"):
                        self.assertIn(bundle + "/" + suffix, text)
                        self.assertTrue((source / ".adaptive-sdd" / suffix).exists())
                # Fixed W references must resolve at either installation location.
                workflow = source / ".adaptive-sdd/workflow"
                for path in workflow.rglob("*.md"):
                    text = path.read_text(encoding="utf-8")
                    for relative in re.findall(r"`W/([^`*<>]+)`", text):
                        self.assertTrue((workflow / relative.split("#")[0]).exists(),
                                        (path, relative))

    def test_in_repo_outputs_are_identical_across_shell_hosts(self):
        with mock.patch.object(installer.sys, "platform", "win32"):
            self.assertEqual(self.command("render")[0], 0)
        with mock.patch.object(installer.sys, "platform", "linux"):
            code, output = self.command("check")
            self.assertEqual(code, 0, output)

    def test_generated_external_commands_execute_with_literal_paths(self):
        product = self.project / "product $literal 'space;"
        source = self.project / "harness $literal 'space;"
        product.mkdir()
        shutil.copytree(SOURCE, source / ".adaptive-sdd")
        values = json.loads(json.dumps(self.values))
        values.setdefault("skill_eval", {})["command"] = ""
        (source / ".adaptive-sdd/project.json").write_bytes(installer.canonical(values))
        self.assertEqual(self.external_command("render", product, source), 0)
        entry = (product / ".agents/skills/implementing-issues/SKILL.md").read_text(encoding="utf-8")
        eval_doc = (source / ".adaptive-sdd/project/skill-evals.md").read_text(encoding="utf-8")
        commands = [
            re.search(r"`(python -I -B [^\n]+?)`", entry).group(1),
            re.search(r"`(python -I -B [^\n]+?)`", eval_doc).group(1),
        ]
        if sys.platform == "win32":
            shell = shutil.which("pwsh") or shutil.which("powershell")
            self.assertIsNotNone(shell, "PowerShell is required to verify generated Windows commands")
            prefix = [shell, "-NoProfile", "-NonInteractive", "-Command"]
        else:
            prefix = ["/bin/sh", "-c"]
        for command in commands:
            with self.subTest(command=command):
                result = subprocess.run(prefix + [command], cwd=product, capture_output=True,
                                        text=True, encoding="utf-8", errors="replace", timeout=30)
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_external_connection_tamper_and_shared_harness_are_rejected(self):
        source, product = self.external_install()
        self.assertEqual(self.external_command("render", product, source), 0)
        other = self.project / "other-product"
        other.mkdir()
        self.assertEqual(self.external_command("render", other, source), 2)
        self.assertFalse((other / "AGENTS.md").exists())
        connection = product / installer.CONNECTION
        value = json.loads(connection.read_bytes())
        value["manifest_sha256"] = "0" * 64
        connection.write_bytes(installer.canonical(value))
        self.assertEqual(self.external_command("check", product), 2)

    def test_external_hand_edit_is_kept_and_detected(self):
        source, product = self.external_install()
        self.assertEqual(self.external_command("render", product, source), 0)
        entry = product / ".agents/skills/managing-issues/SKILL.md"
        content = entry.read_bytes() + b"\nmanual change\n"
        entry.write_bytes(content)
        self.assertEqual(self.external_command("check", product), 1)
        self.assertEqual(self.external_command("render", product, source), 3)
        self.assertEqual(entry.read_bytes(), content)

    def test_tracker_id_allocation_is_specific_to_adapter(self):
        for kind, source in (("github", "generated"), ("github", "external"),
                             ("local-docs", "generated"), ("local-docs", "external")):
            with self.subTest(kind=kind, source=source):
                self.values["tracker"].update(kind=kind, id_source=source,
                    repository="example/library", id_prefix="BOOK", id_format="EXT-<ticket>",
                    child_id_rule="Use external child tickets")
                self.save_values()
                self.assertEqual(self.command("render")[0], 0)
                self.assertEqual(self.command("check")[0], 0)
                tracker = (self.copy / "project/tracker.md").read_text(encoding="utf-8")
                if kind == "github":
                    self.assertIn("GitHub가 실제 발급한 Issue/PR 번호", tracker)
                    self.assertNotIn("가장 큰 번호 + 1", tracker)
                    self.assertNotIn("EXT-<ticket>", tracker)
                    self.assertNotIn("Use external child tickets", tracker)
                elif source == "generated":
                    self.assertIn("BOOK-<번호>", tracker)
                    self.assertIn("가장 큰 번호 + 1", tracker)
                else:
                    self.assertIn("EXT-<ticket>", tracker)
                    self.assertIn("Use external child tickets", tracker)
                    self.assertNotIn("가장 큰 번호 + 1", tracker)

    def test_nondefault_project_settings_render_and_check(self):
        self.values["git"] = {"remote": "upstream", "base_branch": "develop", "merge_branch": "release"}
        self.values["review"] = {"repository": self.project.as_posix(), "remote": "local-review", "branch": "reviews"}
        self.values["tracker"].update(id_source="external", id_format="BOOK-<ticket>", child_id_rule="Use approved parent-suffix IDs")
        self.values["build"]["checks"] = [{"scope": "behavior", "method": "manual", "actor": "human",
            "instructions": "Observe loan cancellation", "evidence": "target SHA and signed result", "required": "required"}]
        self.values["build"].update(test_mode="temporary", test_format="synthetic unit fixtures", test_preserve_at="../evidence")
        self.values["routing"]["role_defaults"] = [{"role": "IMPLEMENT", "model": "fictional-model", "reasoning": "high"}]
        self.values["routing"]["capabilities"] = [{"host": "fictional-host", "model": "fictional-model", "tier": "strong",
            "reasoning": "high", "source": "host record", "identity": "sample-identity", "valid_until": "2030-01-01T00:00:00Z"}]
        self.save_values()
        self.assertEqual(self.command("render")[0], 0)
        self.assertEqual(self.command("check")[0], 0)
        tracker = (self.copy / "project/tracker.md").read_text(encoding="utf-8")
        self.assertIn("BOOK-<ticket>", tracker)
        self.assertIn("`develop`", tracker)
        self.assertIn("`release`", tracker)
        self.assertNotIn("가장 큰 번호 + 1", tracker)
        build = (self.copy / "project/build.md").read_text(encoding="utf-8")
        self.assertIn("Observe loan cancellation", build)
        self.assertNotIn("검증 수단이 없으면", build)
        self.assertIn("../evidence", build)

    def test_invalid_settings_fail_before_output_writes(self):
        self.assertEqual(self.command("render")[0], 0)
        original = json.loads(json.dumps(self.values))
        lock = (self.copy / "install.lock.json").read_bytes()
        bad_settings = [
            ("git", {"remote": "origin;unsafe"}),
            ("tracker", dict(self.values["tracker"], id_source="external", id_format="")),
            ("review", {"repository": "relative/path"}),
            ("build", dict(self.values["build"], test_mode="temporary", test_preserve_at="")),
            ("build", dict(self.values["build"], checks=[{"scope": "x", "method": "unknown", "actor": "agent", "instructions": "x", "evidence": "x", "required": "required"}])),
        ]
        for invalid in ("publish/", "publish.lock", "publish//candidate", "publish/.hidden", "publish.lock/candidate"):
            bad_settings.extend([("review", {"branch": invalid}), ("git", {"base_branch": invalid})])
        for section, value in bad_settings:
            with self.subTest(section=section, value=value):
                self.values = json.loads(json.dumps(original))
                self.values[section] = value
                self.save_values()
                self.assertEqual(self.command("render")[0], 2)
                self.assertEqual((self.copy / "install.lock.json").read_bytes(), lock)

    def test_legacy_settings_have_compatible_defaults(self):
        legacy = json.loads(json.dumps(self.values))
        for key in ("git", "review"):
            legacy.pop(key, None)
        for section, keys in {"tracker": ("id_source", "id_format", "child_id_rule"), "build": ("checks", "test_mode", "test_format", "test_preserve_at"), "routing": ("role_defaults", "capabilities", "qualification_records"), "project": ("conversation_language", "conventions")}.items():
            for key in keys:
                legacy[section].pop(key, None)
        installer.validate_settings(legacy)
        cfg = installer.settings(legacy)
        self.assertEqual(cfg["git"], {"remote": "origin", "base_branch": "main", "merge_branch": "main"})
        self.assertEqual(cfg["build"]["test_mode"], "persistent")
        self.assertFalse(cfg["tracker_external_id"])


if __name__ == "__main__":
    unittest.main()
