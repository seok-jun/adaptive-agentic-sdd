"""Integration checks for opt-in resolution; no agent or network is invoked."""
import contextlib
import importlib.util
import io
import json
import os
import shutil
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("agentics", ROOT / "adaptive-sdd/tools/agentics.py")
agentics = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(agentics)


class AgenticsTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix="agentics-")
        self.addCleanup(self.tmp.cleanup)
        self.base = Path(self.tmp.name).resolve()
        global_config = self.base / "empty-gitconfig"
        global_config.write_text("", encoding="utf-8")
        fixture_env = {k: v for k, v in os.environ.items() if not k.upper().startswith("GIT_")}
        fixture_env.update({"GIT_CONFIG_GLOBAL": str(global_config), "GIT_CONFIG_NOSYSTEM": "1"})
        self.env = patch.dict(os.environ, fixture_env, clear=True)
        self.env.start()
        self.addCleanup(self.env.stop)
        self.product = self.base / "product"
        self.workflow = self.base / "workflow"
        for root in (self.product, self.workflow):
            root.mkdir()
            self.git(root, "init", "-q")
            self.git(root, "config", "user.email", "fixture@example.invalid")
            self.git(root, "config", "user.name", "Fixture")
            self.git(root, "config", "core.autocrlf", "false")
            self.git(root, "config", "commit.gpgsign", "false")
        (self.product / "RULES.md").write_text("Product requirements\n", encoding="utf-8")
        self.commit(self.product)
        (self.workflow / "entry.md").write_text("Project-owned procedure\n", encoding="utf-8")
        (self.workflow / "procedure").mkdir()
        (self.workflow / "procedure/run.md").write_text("Project procedure\n", encoding="utf-8")
        self.profile = {"schema": 1, "methodology": "example-team", "version": "1",
                        "entry": "entry.md", "paths": {"workflow": "procedure", "supports": None}, "product_sources": [
                            {"path": "RULES.md", "revision": "task-start", "kind": "approved-rule"}],
                        "records": {"location": "existing-tracker", "retention_owner": "project-team",
                                    "revision_relation": "link product and W commits in the task record",
                                    "access_failure": "stop-dependent-work"}}
        self.save_profile()
        self.git(self.workflow, "remote", "add", "origin", "https://example.invalid/team/workflow.git")
        self.sha = self.commit(self.workflow)
        (self.product / ".agentics").mkdir()
        self.write_connection()
        self.config = self.base / "loader.json"
        self.config.write_text(json.dumps({"schema": 1, "sources": {"example-team": {
            "root": str(self.workflow), "origin": "https://example.invalid/team/workflow.git"}}}), encoding="utf-8")

    def git(self, root, *args):
        return subprocess.check_output(["git", "-C", str(root), *args], text=True, encoding="utf-8").strip()

    def commit(self, root):
        self.git(root, "add", ".")
        self.git(root, "commit", "-qm", "fixture")
        return self.git(root, "rev-parse", "HEAD")

    def save_profile(self):
        (self.workflow / "profile.json").write_text(json.dumps(self.profile), encoding="utf-8")

    def write_connection(self):
        (self.product / ".agentics/default.yaml").write_text(
            "methodology: example-team\nversion: 1\ncommit: " + self.sha + "\n", encoding="utf-8")

    def resolve(self):
        return agentics.resolve(self.product, "default", self.config, True, "task-1", True)

    def test_unselected_does_not_read_files_or_run_git(self):
        with patch.object(Path, "read_text", side_effect=AssertionError("read")), \
                patch.object(agentics, "git", side_effect=AssertionError("git")):
            self.assertEqual(agentics.resolve(None, None, None, False)["state"], "INACTIVE")

    def test_selection_is_read_only_and_does_not_require_upstream_m(self):
        def snapshot():
            return {str(p.relative_to(self.base)): p.read_bytes() for p in self.base.rglob("*")
                    if p.is_file() and ".git" not in p.parts}
        before = snapshot()
        result = self.resolve()
        self.assertEqual(result["state"], "READY")
        self.assertEqual(result["workflow_commit"], self.sha)
        self.assertEqual(before, snapshot())
        self.assertFalse((self.product / "AGENTS.md").exists())
        self.assertIsNone(result["methodology_dir"])
        self.assertEqual(result["workflow_dir"], str(self.workflow / "procedure"))

    def test_resolution_does_not_refresh_git_indexes(self):
        for root, name in ((self.product, "RULES.md"), (self.workflow, "entry.md")):
            stat = (root / name).stat()
            os.utime(root / name, (stat.st_atime + 10, stat.st_mtime + 10))
        before = [(root / ".git/index").read_bytes() for root in (self.product, self.workflow)]
        self.resolve()
        after = [(root / ".git/index").read_bytes() for root in (self.product, self.workflow)]
        self.assertEqual(before, after)

    def test_customizing_w_and_selecting_new_commit_needs_no_m_update(self):
        (self.workflow / "entry.md").write_text("Adapted team procedure\n", encoding="utf-8")
        self.sha = self.commit(self.workflow)
        with self.assertRaisesRegex(agentics.ConnectionError, "SHA mismatch"):
            self.resolve()
        self.write_connection()
        self.assertEqual(self.resolve()["state"], "READY")

    def test_same_connection_works_in_another_product_checkout(self):
        self.commit(self.product)
        other = self.base / "other"
        subprocess.check_call(["git", "clone", "-q", str(self.product), str(other)])
        self.assertEqual(agentics.resolve(other, "default", self.config, True, "task-2", True)["state"], "READY")

    def test_both_real_starters_resolve_without_legacy_installation(self):
        for edition in ("adaptive-sdd", "ko/adaptive-sdd"):
            with self.subTest(edition=edition):
                # Replace only the fixture-owned copied trees between edition checks.
                for name in ("workflow", "methodology"):
                    target = self.workflow / name
                    if target.exists():
                        self.assertIn(self.base, target.resolve().parents)
                        shutil.rmtree(target)
                    shutil.copytree(ROOT / edition / name, target)
                self.profile["entry"] = "workflow/activation.md"
                self.profile["paths"] = {"workflow": "workflow", "supports": "methodology"}
                self.save_profile()
                self.sha = self.commit(self.workflow)
                self.write_connection()
                self.assertEqual(self.resolve()["entry"], str(self.workflow / "workflow/activation.md"))
                self.assertEqual(self.resolve()["methodology_dir"], str(self.workflow / "methodology"))
                self.assertFalse((self.product / ".adaptive-sdd").exists())
                self.assertFalse((self.workflow / "install.lock.json").exists())

    def test_duplicate_json_keys_rejected(self):
        self.config.write_text('{"schema":1,"schema":1,"sources":{}}', encoding="utf-8")
        with self.assertRaisesRegex(agentics.ConnectionError, "duplicate JSON"):
            self.resolve()

    def test_missing_explicit_workflow_directory_rejected(self):
        self.profile["paths"]["workflow"] = "missing"
        self.save_profile()
        self.sha = self.commit(self.workflow)
        self.write_connection()
        with self.assertRaisesRegex(agentics.ConnectionError, "directory unavailable"):
            self.resolve()

    def test_git_metadata_entry_rejected(self):
        self.profile["entry"] = ".git/config"
        self.save_profile()
        self.sha = self.commit(self.workflow)
        self.write_connection()
        with self.assertRaisesRegex(agentics.ConnectionError, "within"):
            self.resolve()

    def test_index_hidden_changes_rejected(self):
        for flag in ("assume-unchanged", "skip-worktree"):
            with self.subTest(flag=flag):
                self.git(self.workflow, "update-index", "--" + flag, "entry.md")
                (self.workflow / "entry.md").write_text("hidden modification", encoding="utf-8")
                with self.assertRaisesRegex(agentics.ConnectionError, "unsupported"):
                    self.resolve()
                (self.workflow / "entry.md").write_text("Project-owned procedure\n", encoding="utf-8")
                self.git(self.workflow, "update-index", "--no-" + flag, "entry.md")

    def test_cli_ready_json(self):
        with contextlib.redirect_stdout(io.StringIO()) as output:
            code = agentics.main(["--selected", "--fresh-session", "--project-root", str(self.product),
                                  "--area", "default", "--config", str(self.config), "--task", "new-item"])
        self.assertEqual(code, 0)
        self.assertEqual(json.loads(output.getvalue())["state"], "READY")

    def test_config_inside_product_rejected(self):
        inside = self.product / "loader.json"
        inside.write_bytes(self.config.read_bytes())
        self.config = inside
        with self.assertRaisesRegex(agentics.ConnectionError, "outside P"):
            self.resolve()

    def test_repository_redirect_environment_is_ignored(self):
        with patch.dict(os.environ, {"GIT_DIR": str(self.product / ".git"),
                                     "GIT_WORK_TREE": str(self.product),
                                     "GIT_INDEX_FILE": str(self.base / "other-index"),
                                     "GIT_CONFIG_COUNT": "1", "GIT_CONFIG_KEY_0": "core.worktree",
                                     "GIT_CONFIG_VALUE_0": str(self.product)}):
            self.assertEqual(self.resolve()["state"], "READY")
        self.assertFalse((self.base / "other-index").exists())

    def test_empty_untracked_directory_cannot_be_workflow(self):
        (self.workflow / "empty").mkdir()
        self.profile["paths"]["workflow"] = "empty"
        self.save_profile()
        self.sha = self.commit(self.workflow)
        self.write_connection()
        with self.assertRaisesRegex(agentics.ConnectionError, "tracked files"):
            self.resolve()

    def test_partial_clone_rejected_before_any_status(self):
        original = agentics.git
        def no_status(root, *args):
            self.assertNotIn("status", args)
            return original(root, *args)
        for root in (self.product, self.workflow):
            with self.subTest(root=root):
                self.git(root, "config", "remote.origin.promisor", "true")
                with patch.object(agentics, "git", side_effect=no_status), \
                        self.assertRaisesRegex(agentics.ConnectionError, "partial/promisor"):
                    self.resolve()
                self.git(root, "config", "--unset", "remote.origin.promisor")

    def test_workflow_changed_during_resolution_rejected(self):
        original = agentics.read_json
        def racing_read(path):
            result = original(path)
            if path.name == "profile.json":
                (self.workflow / "entry.md").write_text("changed during lookup", encoding="utf-8")
            return result
        with patch.object(agentics, "read_json", side_effect=racing_read), \
                self.assertRaisesRegex(agentics.ConnectionError, "changed during"):
            self.resolve()

    def test_selected_failures_never_fall_back(self):
        for args, error in (([self.product, "missing", self.config, True, "task-1", True], OSError),
                            ([self.product, "default", self.config, True, "task-1", False], agentics.ConnectionError),
                            ([self.product, "../escape", self.config, True, "task-1", True], agentics.ConnectionError)):
            with self.subTest(args=args), self.assertRaises(error):
                agentics.resolve(*args)
        self.config.write_text('{"schema": 1, "sources": {}}', encoding="utf-8")
        with self.assertRaisesRegex(agentics.ConnectionError, "source mapping"):
            self.resolve()

    def test_dirty_and_ignored_workflow_content_rejected(self):
        (self.workflow / "extra.md").write_text("extra", encoding="utf-8")
        with self.assertRaisesRegex(agentics.ConnectionError, "clean"):
            self.resolve()
        (self.workflow / "extra.md").unlink()
        (self.workflow / ".git/info/exclude").write_text("hidden.txt\n", encoding="utf-8")
        (self.workflow / "hidden.txt").write_text("hidden", encoding="utf-8")
        with self.assertRaisesRegex(agentics.ConnectionError, "clean"):
            self.resolve()

    def test_changed_origin_and_profile_mismatch_rejected(self):
        self.git(self.workflow, "remote", "set-url", "origin", "https://example.invalid/other")
        with self.assertRaisesRegex(agentics.ConnectionError, "origin mismatch"):
            self.resolve()
        self.git(self.workflow, "remote", "set-url", "origin", "https://example.invalid/team/workflow.git")
        self.profile["version"] = "different"
        self.save_profile()
        self.sha = self.commit(self.workflow)
        self.write_connection()
        with self.assertRaisesRegex(agentics.ConnectionError, "identity"):
            self.resolve()

    def test_missing_product_source_and_record_decision_rejected(self):
        (self.product / "RULES.md").unlink()
        with self.assertRaisesRegex(agentics.ConnectionError, "source unavailable"):
            self.resolve()
        (self.product / "RULES.md").write_text("restored", encoding="utf-8")
        self.profile["records"]["retention_owner"] = ""
        self.save_profile()
        self.sha = self.commit(self.workflow)
        self.write_connection()
        with self.assertRaisesRegex(agentics.ConnectionError, "retention_owner"):
            self.resolve()

    def test_duplicate_and_path_escape_input_rejected(self):
        connection = self.product / ".agentics/default.yaml"
        with connection.open("a", encoding="utf-8") as f:
            f.write("version: 1\n")
        with self.assertRaisesRegex(agentics.ConnectionError, "duplicate"):
            self.resolve()
        self.write_connection()
        self.profile["entry"] = "../loader.json"
        self.save_profile()
        self.sha = self.commit(self.workflow)
        self.write_connection()
        with self.assertRaisesRegex(agentics.ConnectionError, "within"):
            self.resolve()

    def test_cli_reports_blocked_and_inactive(self):
        with contextlib.redirect_stdout(io.StringIO()) as output:
            self.assertEqual(agentics.main([]), 0)
        self.assertEqual(json.loads(output.getvalue())["state"], "INACTIVE")
        with contextlib.redirect_stdout(io.StringIO()) as output:
            self.assertEqual(agentics.main(["--selected"]), 2)
        self.assertEqual(json.loads(output.getvalue())["state"], "BLOCKED")


if __name__ == "__main__":
    unittest.main()
