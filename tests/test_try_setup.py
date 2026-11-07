"""Offline, real-Git checks of the external-adoption try sandbox."""

import contextlib
import importlib.util
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "try/setup.py"
SPEC = importlib.util.spec_from_file_location("try_setup", SCRIPT)
setup = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(setup)

PRODUCT_FILES = {
    ".gitignore", ".agentics/default.yaml", "AGENTS.md", "README.md",
    "catalog/__init__.py", "catalog/search.py", "members/__init__.py", "members/registry.py",
    "docs/architecture.md", "docs/project-rules.md", "docs/authority.md",
    "tests/__init__.py", "tests/test_search.py", "tests/test_registry.py",
}
PROJECT_ROLES = {
    "agent-instruction-policy", "build", "execution-routing", "issue-priority",
    "issue-writing-guide", "module-boundaries", "sdd-workflow", "skill-evals", "tracker",
}


class TrySetupTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="sdd-try-")
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name).resolve()
        self.config = self.base / "user.gitconfig"
        self.template = self.base / "templates"
        self.template.mkdir()
        (self.template / "UNWANTED").write_text("must not be copied", encoding="utf-8")
        self.config.write_text(
            '[user]\n name = Other User\n email = other@example.invalid\n'
            '[commit]\n gpgSign = true\n[core]\n autocrlf = true\n fscache = true\n'
            '[init]\n defaultBranch = other\n templateDir = "' + self.template.as_posix() + '"\n',
            encoding="utf-8")
        env = {k: v for k, v in os.environ.items() if not k.upper().startswith("GIT_")}
        env.update(GIT_CONFIG_GLOBAL=str(self.config), GIT_CONFIG_NOSYSTEM="1",
                   PYTHONDONTWRITEBYTECODE="1", PYTHONIOENCODING="utf-8")
        self.patch_env = mock.patch.dict(os.environ, env, clear=True)
        self.patch_env.start()
        self.addCleanup(self.patch_env.stop)

    def command(self, args, cwd=None):
        return subprocess.run([str(arg) for arg in args], cwd=cwd, capture_output=True,
                              encoding="utf-8", errors="replace", env=os.environ.copy())

    def git(self, root, *args):
        result = self.command(["git", "-C", root, *args])
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        return result.stdout.strip()

    def test_both_editions_resolve_real_external_adoption(self):
        for lang in ("en", "ko"):
            with self.subTest(lang=lang):
                # Spaces, Unicode and an apostrophe exercise both filesystem and prompt quoting.
                parent = self.base / (lang + " 한 글's")
                parent.mkdir()
                target = parent / "adaptive-sdd-try"
                with self.config.open("a", encoding="utf-8") as stream:
                    stream.write('\n[url "' + target.as_uri() + '/"]\n insteadOf = '
                                 + target.as_posix() + '/\n')
                config_before = self.config.read_bytes()
                # Exercise the cwd default for English and the explicit TARGET for Korean.
                args = [sys.executable, "-I", "-B", SCRIPT]
                if lang == "ko":
                    args += [target, "--lang", lang]
                result = self.command(args, cwd=parent)
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                self.assertIn("READY", result.stdout)
                self.assertIn("START-HERE.md", result.stdout)
                self.assertEqual(self.config.read_bytes(), config_before)
                self.assertEqual(set(p.name for p in parent.iterdir()), {target.name})
                self.assertEqual(set(p.name for p in target.iterdir()), {
                    "product", "team-workflow", "remotes", "records", "user-config", "START-HERE.md"})
                product, workflow = target / "product", target / "team-workflow"
                self.assertEqual(set(self.git(product, "ls-files").splitlines()), PRODUCT_FILES)
                sha = self.git(workflow, "rev-parse", "HEAD")
                connection = (product / ".agentics/default.yaml").read_text(encoding="utf-8")
                self.assertEqual(connection, "methodology: try-team\nversion: try-1\ncommit: " + sha + "\n")
                for repo in (product, workflow):
                    self.assertEqual(self.git(repo, "branch", "--show-current"), "main")
                    self.assertEqual(self.git(repo, "status", "--porcelain", "--ignored", "--untracked-files=all"), "")
                    self.assertEqual(self.git(repo, "config", "--local", "core.autocrlf"), "false")
                    self.assertEqual(self.git(repo, "log", "-1", "--format=%an <%ae>"),
                                     "Adaptive SDD Demo <demo@example.invalid>")
                    self.assertFalse((repo / ".git/UNWANTED").exists())
                    remote = target / "remotes" / (repo.name + ".git")
                    self.assertEqual(self.git(remote, "rev-parse", "--is-bare-repository"), "true")
                    self.assertEqual(self.git(repo, "rev-parse", "HEAD"), self.git(remote, "rev-parse", "main"))
                self.assertFalse(any(p.is_symlink() for p in workflow.rglob("*")))
                project_docs = list((workflow / "project").glob("*.md"))
                self.assertEqual({p.stem for p in project_docs}, PROJECT_ROLES)
                for path in project_docs:
                    text = path.read_text(encoding="utf-8")
                    self.assertNotIn("{{", text)
                    if lang == "ko":
                        self.assertRegex(text, "[가-힣]")
                starter = ROOT / ("ko/adaptive-sdd" if lang == "ko" else "adaptive-sdd")
                for name in ("workflow", "methodology"):
                    originals = {p.relative_to(starter).as_posix(): p.read_bytes()
                                 for p in (starter / name).rglob("*") if p.is_file()}
                    copies = {p.relative_to(workflow).as_posix(): p.read_bytes()
                              for p in (workflow / name).rglob("*") if p.is_file()}
                    self.assertEqual(copies, originals)
                self.assertEqual((workflow / "LICENSE").read_bytes(), (starter / "LICENSE").read_bytes())
                self.assertEqual({p.name for p in (target / "records").iterdir()}, {"items", "claims"})
                self.assertEqual(list((target / "records/items").iterdir()), [])
                self.assertEqual(list((target / "records/claims").iterdir()), [])
                allowlist = json.loads((target / "user-config/agentics.json").read_text(encoding="utf-8"))
                self.assertEqual(allowlist["sources"]["try-team"], {
                    "root": str(workflow), "origin": self.git(workflow, "remote", "get-url", "origin")})
                self.assertTrue(allowlist["sources"]["try-team"]["origin"].startswith("file://"))
                resolved = self.command(setup.resolver_args(target))
                self.assertEqual(resolved.returncode, 0, resolved.stdout + resolved.stderr)
                state = json.loads(resolved.stdout)
                self.assertEqual(state["state"], "READY")
                self.assertEqual(state["workflow_commit"], sha)
                self.assertFalse(state["product_dirty"])
                self.assertEqual(state["records"]["location"], "local-docs: " + (target / "records").as_posix())
                for source in state["product_sources"]:
                    self.assertTrue((product / source["path"]).is_file())
                tests = self.command([sys.executable, "-B", "-m", "unittest", "discover", "-s", "tests", "-t", "."], cwd=product)
                self.assertEqual(tests.returncode, 0, tests.stdout + tests.stderr)
                self.assertIn("OK", tests.stderr)
                bug = self.command([sys.executable, "-B", "-c",
                    "from catalog.search import page; assert page([1, 2, 3, 4], 1, 3) == [1, 2]; "
                    "assert page([1, 2], 1, 1) == []"], cwd=product)
                self.assertEqual(bug.returncode, 0, bug.stderr)
                self.assertNotIn("Adaptive", (product / "AGENTS.md").read_text(encoding="utf-8"))
                start = (target / "START-HERE.md").read_text(encoding="utf-8")
                for expected in ("Trivial", "Small", "Large", "READY", "new-item", "default",
                                 "try-team", "codex --help", "--add-dir",
                                 str(ROOT / "adaptive-sdd/tools/agentics.py"), product.as_posix()):
                    self.assertIn(expected, start)

    def assert_refused(self, target, expected):
        result = self.command([sys.executable, "-I", "-B", SCRIPT, target])
        self.assertNotEqual(result.returncode, 0)
        self.assertIn(expected, result.stderr)

    def test_existing_targets_are_untouched(self):
        folder = self.base / "existing"
        folder.mkdir()
        sentinel = folder / "keep.txt"
        sentinel.write_bytes(b"keep me")
        before = {p.relative_to(self.base) for p in self.base.rglob("*")}
        for target in (folder, sentinel):
            with self.subTest(target=target):
                self.assert_refused(target, "already exists")
        self.assertEqual(sentinel.read_bytes(), b"keep me")
        self.assertEqual({p.relative_to(self.base) for p in self.base.rglob("*")}, before)

    def test_inside_checkout_and_missing_parent_create_nothing(self):
        for target in (ROOT / "try" / "must-not-exist-sandbox", ROOT / "try/../must-not-exist-sandbox"):
            self.assertFalse(target.exists())
            self.assert_refused(target, "outside this repository")
            self.assertFalse(target.exists())
        missing = self.base / "missing-parent"
        self.assert_refused(missing / "target", "parent must already exist")
        self.assertFalse(missing.exists())

    def test_symlinks_and_symlink_route_into_checkout_are_refused(self):
        link = self.base / "link"
        try:
            link.symlink_to(self.base / "absent", target_is_directory=True)
        except OSError as error:
            self.skipTest("Symlink creation unavailable: " + str(error))
        self.assert_refused(link, "already exists")
        self.assertTrue(link.is_symlink())
        alias = self.base / "checkout-alias"
        alias.symlink_to(ROOT, target_is_directory=True)
        self.assert_refused(alias / "must-not-exist-sandbox", "outside this repository")
        self.assertFalse((ROOT / "must-not-exist-sandbox").exists())

    def test_old_git_is_refused_before_creation(self):
        target = self.base / "old-git"
        stderr = io.StringIO()
        with mock.patch.object(setup, "run", return_value="git version 2.35.9"), contextlib.redirect_stderr(stderr):
            self.assertEqual(setup.main([str(target)]), 1)
        self.assertIn("Git 2.36+", stderr.getvalue())
        self.assertFalse(target.exists())

    def test_resolver_failure_is_reported_and_target_is_retained(self):
        target = self.base / "blocked"
        original_run = setup.run

        def blocked(args, **kwargs):
            if str(setup.RESOLVER) in [str(arg) for arg in args]:
                # Exercise a real resolver exit 2, not a simulated READY response.
                (target / "team-workflow/untracked.txt").write_text("fixture", encoding="utf-8")
            return original_run(args, **kwargs)

        stderr = io.StringIO()
        with mock.patch.object(setup, "run", side_effect=blocked), contextlib.redirect_stderr(stderr):
            self.assertEqual(setup.main([str(target)]), 1)
        self.assertIn('"state": "BLOCKED"', stderr.getvalue())
        self.assertIn("checkout must be clean", stderr.getvalue())
        self.assertIn("left in place", stderr.getvalue())
        self.assertTrue((target / "product/.agentics/default.yaml").is_file())
        self.assertTrue((target / "START-HERE.md").is_file())


if __name__ == "__main__":
    unittest.main()
