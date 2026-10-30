"""Exercise exact Git snapshots with synthetic UTF-8 files and hidden records."""
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("snapshot", ROOT / "ko/adaptive-sdd/tools/review_snapshot.py")
snapshot = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(snapshot)


class ReviewSnapshotTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="sdd-snapshot-test-", dir=ROOT)
        self.root = Path(self.temp.name).resolve()
        self.addCleanup(self.cleanup)
        self.repo = self.root / "repo"
        self.repo.mkdir()
        self.run_git("init", "--quiet")
        self.body = "## 목표\r\n예약 취소 근거를 확인한다.\r\n```markdown\r\n## 기록\r\n설명용 예시\r\n```\r\n".encode("utf-8")
        self.source = ("# T-1 작업\r\n\r\n## 메타\r\nstatus: open\r\n".encode("utf-8") + self.body
                       + "## 기록\r\nA verdict: PASS\r\n이전 finding A-123\r\n".encode("utf-8"))
        (self.repo / "item.md").write_bytes(self.source)
        (self.repo / "plan.md").write_bytes("# 목표 계획\n변경 기준\n".encode("utf-8"))
        self.run_git("add", "--", "item.md", "plan.md")
        self.run_git("-c", "user.name=Snapshot Test", "-c", "user.email=snapshot@example.invalid", "-c", "commit.gpgsign=false", "commit", "--quiet", "-m", "Synthetic review fixture")
        self.commit = self.run_git("rev-parse", "HEAD").decode("ascii").strip()
        self.spec = [{"path": "item.md", "kind": "tracker-body"}, {"path": "plan.md", "kind": "artifact"}]
        self.bundle = self.root / "bundle"

    def cleanup(self):
        if ROOT not in self.root.resolve().parents:
            raise RuntimeError("cleanup escaped checkout")
        self.temp.cleanup()

    def run_git(self, *args):
        return subprocess.run(["git", "-c", "core.autocrlf=false", "-C", str(self.repo), *args],
                              check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout

    def test_exact_body_preserves_utf8_crlf_and_excludes_records(self):
        identity = snapshot.create(self.repo, self.commit, self.spec, self.bundle)
        output = (self.bundle / "files/0001.md").read_bytes()
        self.assertEqual(output, "# T-1 작업\r\n\r\n".encode("utf-8") + self.body)
        self.assertNotIn(b"A-123", output)
        self.assertNotIn(b"status: open", output)
        # Worktree changes do not alter the exact committed review candidate.
        (self.repo / "item.md").write_text("different working tree", encoding="utf-8")
        snapshot.check(self.repo, self.bundle, identity)

    def test_english_tracker_headings_are_recognized_and_records_hidden(self):
        source = (b"# T-2 Work\n\n## Meta\nstatus: open\n## Goal\nConfirm the cancellation evidence.\n"
                  b"## Records\nA verdict: PASS\nprior finding A-456\n")
        (self.repo / "item-en.md").write_bytes(source)
        self.run_git("add", "--", "item-en.md")
        self.run_git("-c", "user.name=Snapshot Test", "-c", "user.email=snapshot@example.invalid", "-c", "commit.gpgsign=false", "commit", "--quiet", "-m", "English fixture")
        commit = self.run_git("rev-parse", "HEAD").decode("ascii").strip()
        snapshot.create(self.repo, commit, [{"path": "item-en.md", "kind": "tracker-body"}], self.bundle)
        output = (self.bundle / "files/0001.md").read_bytes()
        self.assertEqual(output, b"# T-2 Work\n\n## Goal\nConfirm the cancellation evidence.\n")
        self.assertNotIn(b"A-456", output)
        self.assertNotIn(b"status: open", output)

    def test_mixed_or_duplicated_edition_headings_are_rejected(self):
        # Two metadata headings (one per edition) must not let a records section slip through.
        source = "# T-3\n\n## 메타\nstatus: open\n## Meta\nx\n## 목표\n본문\n## Records\nA verdict: PASS\n".encode("utf-8")
        (self.repo / "item-mixed.md").write_bytes(source)
        self.run_git("add", "--", "item-mixed.md")
        self.run_git("-c", "user.name=Snapshot Test", "-c", "user.email=snapshot@example.invalid", "-c", "commit.gpgsign=false", "commit", "--quiet", "-m", "Mixed fixture")
        commit = self.run_git("rev-parse", "HEAD").decode("ascii").strip()
        with self.assertRaises(snapshot.SnapshotError):
            snapshot.create(self.repo, commit, [{"path": "item-mixed.md", "kind": "tracker-body"}], self.bundle)

    def test_tampered_output_and_added_file_are_rejected(self):
        identity = snapshot.create(self.repo, self.commit, self.spec, self.bundle)
        path = self.bundle / "files/0001.md"
        original = path.read_bytes()
        path.write_bytes(original + b"changed")
        with self.assertRaises(snapshot.SnapshotError):
            snapshot.check(self.repo, self.bundle, identity)
        path.write_bytes(original)
        (self.bundle / "review-result.txt").write_text("A verdict", encoding="utf-8")
        with self.assertRaises(snapshot.SnapshotError):
            snapshot.check(self.repo, self.bundle, identity)

    def test_changed_manifest_cannot_keep_packet_identity(self):
        identity = snapshot.create(self.repo, self.commit, self.spec, self.bundle)
        manifest = self.bundle / "manifest.json"
        value = json.loads(manifest.read_bytes())
        value["entries"][0]["selected_lines"] = [[1, 1]]
        manifest.write_bytes(snapshot.encoded(value))
        with self.assertRaises(snapshot.SnapshotError):
            snapshot.check(self.repo, self.bundle, identity)
        # Even a newly reported digest cannot make a false selection match Git.
        with self.assertRaises(snapshot.SnapshotError):
            snapshot.check(self.repo, self.bundle, snapshot.digest(manifest.read_bytes()))

    def test_malformed_tracker_is_rejected_before_output(self):
        with self.assertRaises(snapshot.SnapshotError):
            snapshot.create(self.repo, self.commit, [{"path": "plan.md", "kind": "tracker-body"}], self.bundle)
        self.assertFalse(self.bundle.exists())
        with self.assertRaises(snapshot.SnapshotError):
            snapshot.select_body("# T\n## 메타\n## 기록\n결과\n".encode("utf-8"))

    def test_mutable_ref_and_unsafe_paths_are_rejected(self):
        with self.assertRaises(snapshot.SnapshotError):
            snapshot.create(self.repo, "HEAD", self.spec, self.bundle)
        for path in ("../plan.md", "/plan.md", "C:/plan.md", "a\\b", "plan.md\n"):
            with self.subTest(path=path), self.assertRaises(snapshot.SnapshotError):
                snapshot.create(self.repo, self.commit, [{"path": path, "kind": "artifact"}], self.bundle)
        self.assertFalse(self.bundle.exists())

    def test_existing_bundle_is_not_overwritten(self):
        identity = snapshot.create(self.repo, self.commit, self.spec, self.bundle)
        with self.assertRaises(FileExistsError):
            snapshot.create(self.repo, self.commit, self.spec, self.bundle)
        snapshot.check(self.repo, self.bundle, identity)

    def test_cli_accepts_bare_source_without_printing_excluded_content(self):
        bare = self.root / "source.git"
        cloned = subprocess.run(["git", "clone", "--quiet", "--bare", "--no-hardlinks", str(self.repo), str(bare)],
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        self.assertEqual(cloned.returncode, 0, cloned.stderr.decode("utf-8", errors="replace"))
        spec = self.root / "spec.json"
        spec.write_bytes(snapshot.encoded(self.spec))
        tool = str(ROOT / "ko/adaptive-sdd/tools/review_snapshot.py")
        created = subprocess.run([sys.executable, "-I", "-B", tool, "create", "--repo", str(bare),
                                  "--commit", self.commit, "--spec", str(spec), "--output", str(self.bundle)],
                                 check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        identity = created.stdout.decode("ascii").strip().split("=", 1)[1]
        checked = subprocess.run([sys.executable, "-I", "-B", tool, "check", "--repo", str(bare),
                                  "--bundle", str(self.bundle), "--manifest-sha256", identity],
                                 check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        self.assertIn(b"OK:", checked.stdout)
        self.assertNotIn(b"A-123", created.stdout + created.stderr + checked.stdout + checked.stderr)


if __name__ == "__main__":
    unittest.main()
