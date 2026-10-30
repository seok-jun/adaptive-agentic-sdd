"""Export and verify bounded review inputs from an exact Git commit.

This tool proves source/selection/content identity, not semantic redaction,
remote publication, reviewer permissions, or blind-review compliance.
Spec: [{"path": "docs/plan.md", "kind": "artifact"},
       {"path": "items/T-1.md", "kind": "tracker-body"}]
Python 3.8+, standard library and Git only. No shell pipelines or text recoding.
"""
import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import subprocess
import sys


class SnapshotError(Exception):
    pass


def digest(data):
    return hashlib.sha256(data).hexdigest()


def encoded(value):
    return (json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8")


def git(repo, *args):
    result = subprocess.run(
        ["git", "--no-replace-objects", "-C", str(repo), *args],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE,
    )
    if result.returncode:
        # Do not emit source content or uncontrolled repository diagnostics.
        raise SnapshotError("Git source lookup failed; check repository access and exact identity")
    return result.stdout


def select_body(data):
    """Keep exact source line bytes; ignore headings inside fenced examples."""
    lines = data.splitlines(keepends=True)
    headings, fence = [], None
    for index, line in enumerate(lines):
        text = line.decode("utf-8").lstrip("\ufeff").rstrip("\r\n")
        marker = re.match(r"^ {0,3}(`{3,}|~{3,})(.*)$", text)
        if fence:
            if marker and marker[1][0] == fence[0] and len(marker[1]) >= fence[1] and not marker[2].strip():
                fence = None
            continue
        if marker:
            fence = (marker[1][0], len(marker[1]))
            continue
        heading = re.match(r"^ {0,3}##\s+(.+?)\s*#*\s*$", text)
        if heading:
            headings.append((index, heading[1]))
    # Tracker document headings of each published edition (ko: 메타/기록, en: Meta/Records).
    meta = [i for i, title in headings if title in ("메타", "Meta")]
    records = [i for i, title in headings if title in ("기록", "Records")]
    if len(meta) != 1 or len(records) != 1 or meta[0] >= records[0]:
        raise SnapshotError("tracker-body needs one ordered metadata and records heading")
    meta_end = next((i for i, _ in headings if i > meta[0]), records[0])
    ranges = [(0, meta[0]), (meta_end, records[0])]
    ranges = [(start, end) for start, end in ranges if start < end]
    if not any(line.strip() for line in lines[meta_end:records[0]]):
        raise SnapshotError("tracker body is empty")
    return b"".join(b"".join(lines[start:end]) for start, end in ranges), [[start + 1, end] for start, end in ranges]


def prepare(repo, commit, spec):
    if not isinstance(commit, str) or not re.fullmatch(r"[0-9a-f]{40}|[0-9a-f]{64}", commit):
        raise SnapshotError("a full lowercase commit object ID is required")
    if git(repo, "cat-file", "-t", commit).strip() != b"commit":
        raise SnapshotError("source is not a commit")
    if not isinstance(spec, list) or not spec:
        raise SnapshotError("spec must be a nonempty list")
    entries, outputs, seen = [], {}, set()
    for number, item in enumerate(spec, 1):
        if not isinstance(item, dict) or set(item) != {"path", "kind"}:
            raise SnapshotError("each entry needs only path and kind")
        path, kind = item["path"], item["kind"]
        if (not isinstance(path, str) or not path or "\\" in path or ":" in path
                or any(ord(c) < 32 for c in path) or PurePosixPath(path).is_absolute()
                or any(p in ("", ".", "..") for p in path.split("/")) or path in seen):
            raise SnapshotError("source paths must be unique relative POSIX paths")
        if kind not in ("artifact", "tracker-body"):
            raise SnapshotError("unknown selection kind")
        seen.add(path)
        ref = commit + ":" + path
        if git(repo, "cat-file", "-t", ref).strip() != b"blob":
            raise SnapshotError("source is not a blob")
        source = git(repo, "cat-file", "blob", ref)
        source.decode("utf-8")  # Reject invalid text before creating any output.
        if kind == "tracker-body":
            output, ranges = select_body(source)
        else:
            output = source
            ranges = [[1, len(source.splitlines())]] if source else []
        name = f"files/{number:04d}.md"
        outputs[name] = output
        entries.append({"path": path, "kind": kind, "source_sha256": digest(source),
                        "selected_lines": ranges, "output": name, "sha256": digest(output)})
    return {"schema": 1, "commit": commit, "entries": entries}, outputs


def create(repo, commit, spec, output):
    manifest, files = prepare(repo, commit, spec)
    output.mkdir(parents=True, exist_ok=False)
    (output / "files").mkdir()
    for name, content in files.items():
        (output / name).write_bytes(content)
    # A partial write has no valid manifest and must not be used as review input.
    (output / "manifest.json").write_bytes(encoded(manifest))
    return digest(encoded(manifest))


def check(repo, bundle, expected_digest):
    manifest_bytes = (bundle / "manifest.json").read_bytes()
    if digest(manifest_bytes) != expected_digest:
        raise SnapshotError("manifest digest differs from the review packet")
    manifest = json.loads(manifest_bytes)
    spec = [{"path": item["path"], "kind": item["kind"]} for item in manifest["entries"]]
    expected, outputs = prepare(repo, manifest["commit"], spec)
    if manifest != expected:
        raise SnapshotError("manifest differs from exact source selection")
    if any(p.is_symlink() for p in bundle.rglob("*")) or bundle.is_symlink():
        raise SnapshotError("snapshot links are not permitted")
    actual = {p.relative_to(bundle).as_posix() for p in bundle.rglob("*") if p.is_file()}
    if actual != set(outputs) | {"manifest.json"}:
        raise SnapshotError("unexpected or missing snapshot files")
    for name, content in outputs.items():
        if (bundle / name).read_bytes() != content:
            raise SnapshotError("snapshot content differs from exact source selection")


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    export = commands.add_parser("create")
    export.add_argument("--repo", required=True)
    export.add_argument("--commit", required=True)
    export.add_argument("--spec", required=True)
    export.add_argument("--output", required=True)
    verify = commands.add_parser("check")
    verify.add_argument("--repo", required=True)
    verify.add_argument("--bundle", required=True)
    verify.add_argument("--manifest-sha256", required=True)
    args = parser.parse_args(argv)
    try:
        if args.command == "create":
            spec = json.loads(Path(args.spec).read_text(encoding="utf-8-sig"))
            print("manifest_sha256=" + create(Path(args.repo), args.commit, spec, Path(args.output)))
        else:
            check(Path(args.repo), Path(args.bundle), args.manifest_sha256)
            print("OK: exact source selection and snapshot bytes match")
        return 0
    except (SnapshotError, OSError, ValueError, KeyError, TypeError) as error:
        print("ERROR: " + (str(error) if isinstance(error, SnapshotError) else type(error).__name__))
        return 2


if __name__ == "__main__":
    sys.exit(main())
