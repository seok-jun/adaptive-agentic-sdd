"""Explicit, read-only task resolution for a user-owned external workflow (Python 3.8+).

No remote fetches, host configuration writes, automatic upgrades or workflow execution.
The connection is a deliberately small YAML subset: three unquoted scalar fields.
"""
import argparse
import json
import os
import pathlib
import re
import subprocess
import sys


class ConnectionError(Exception):
    pass


def require(condition, message):
    if not condition:
        raise ConnectionError(message)


def read_json(path):
    def unique(pairs):
        result = {}
        for key, value in pairs:
            require(key not in result, "duplicate JSON key")
            result[key] = value
        return result
    return json.loads(path.read_text(encoding="utf-8-sig"), object_pairs_hook=unique)


def token(value, label):
    require(isinstance(value, str) and re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]{0,79}", value),
            label + " must be a simple name")
    require(value not in (".", ".."), "invalid " + label)
    return value


def within(root, relative):
    require(isinstance(relative, str) and relative and "\\" not in relative,
            "expected a relative POSIX path")
    part = pathlib.PurePosixPath(relative)
    require(not part.is_absolute() and not any(x.lower() in (".", "..", ".git") or ":" in x for x in part.parts),
            "path must stay within its declared root")
    target = root.joinpath(*part.parts)
    for parent in (target,) + tuple(target.parents):
        if parent == root:
            break
        require(not parent.is_symlink(), "symlink paths are not supported")
    require(root in target.resolve().parents, "path escaped declared root")
    return target


def git(root, *args):
    # Keep user config locations (including trust/URL rewrites), but never inherit a
    # hook/wrapper's repository, index, object store or command-line config redirects.
    kept = {"GIT_CONFIG_GLOBAL", "GIT_CONFIG_SYSTEM", "GIT_CONFIG_NOSYSTEM"}
    env = {k: v for k, v in os.environ.items() if not k.upper().startswith("GIT_") or k.upper() in kept}
    env["GIT_NO_LAZY_FETCH"] = "1"
    result = subprocess.run(["git", "--no-optional-locks", "--literal-pathspecs", "-c", "core.fsmonitor=false", "-C", str(root), *args], capture_output=True, env=env,
                            encoding="utf-8", errors="strict", check=False)
    require(result.returncode == 0, "Git lookup failed: " + args[0])
    return result.stdout.strip()


def connection(path):
    fields = {}
    for line in path.read_text(encoding="utf-8-sig").splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        match = re.fullmatch(r"(methodology|version|commit): ([A-Za-z0-9._-]+)", line)
        require(match is not None, "connection requires only methodology, version, commit scalars")
        key, value = match.groups()
        require(key not in fields, "duplicate connection field")
        fields[key] = value
    require(set(fields) == {"methodology", "version", "commit"}, "incomplete connection")
    token(fields["methodology"], "methodology")
    token(fields["version"], "version")
    require(re.fullmatch(r"[0-9a-f]{40}", fields["commit"]), "commit must be a full SHA-1")
    return fields


def require_full_clone(root):
    # Old supported Git versions may ignore GIT_NO_LAZY_FETCH. Reject promisor
    # repositories before status can lazily retrieve a missing blob from a remote.
    keys = [line.partition("=")[0].lower() for line in git(root, "config", "--list").splitlines()]
    require(not any(key == "extensions.partialclone" or
                    (key.startswith("remote.") and key.endswith(".promisor")) for key in keys),
            "partial/promisor clones are unsupported; prepare a full local clone")


def resolve(product, area, config_path, selected, task=None, fresh_session=False):
    # Selection precedes every filesystem read, including connection/config existence checks.
    if not selected:
        return {"state": "INACTIVE", "reason": "methodology not selected"}
    token(area, "area")
    token(task, "task")
    require(fresh_session, "start in a fresh session; prior instructions cannot be unloaded")
    product = pathlib.Path(product).resolve(strict=True)
    require(product.is_dir(), "product root is not a directory")
    require(pathlib.Path(git(product, "rev-parse", "--show-toplevel")).resolve() == product,
            "product must be the checkout root")
    require_full_clone(product)
    conn = connection(within(product, ".agentics/" + area + ".yaml"))
    config_path = pathlib.Path(config_path).resolve(strict=True)
    require(product not in config_path.parents, "loader allowlist must be outside P")
    config = read_json(config_path)
    require(isinstance(config, dict) and type(config.get("schema")) is int and config["schema"] == 1,
            "unsupported loader schema")
    sources = config.get("sources")
    require(isinstance(sources, dict), "loader sources must be an object")
    source = sources.get(conn["methodology"])
    require(isinstance(source, dict), "methodology has no user-approved source mapping")
    require(set(source) == {"root", "origin"}, "source requires root and origin")
    require(isinstance(source["root"], str) and pathlib.Path(source["root"]).is_absolute(),
            "source root must be absolute")
    require(isinstance(source["origin"], str) and source["origin"], "source origin is required")
    root = pathlib.Path(source["root"]).resolve(strict=True)
    require(root != product and product not in root.parents and root not in product.parents,
            "workflow and product must be separate trees")
    require(pathlib.Path(git(root, "rev-parse", "--show-toplevel")).resolve() == root,
            "source must be the external workflow checkout root")
    require_full_clone(root)
    require(git(root, "remote", "get-url", "origin") == source["origin"], "source origin mismatch")
    require(git(root, "rev-parse", "HEAD") == conn["commit"], "selected workflow SHA mismatch")
    require(not git(root, "status", "--porcelain", "--untracked-files=all", "--ignored"),
            "selected workflow checkout must be clean, including ignored files")
    # Reject Git submodules and links rather than following content outside the selected commit.
    modes = git(root, "ls-files", "--stage").splitlines()
    require(all(line.startswith(("100644 ", "100755 ")) for line in modes),
            "workflow symlinks and submodules are unsupported")
    require(all(line.startswith("H ") for line in git(root, "ls-files", "-v").splitlines()),
            "assume-unchanged, skip-worktree and sparse W entries are unsupported")
    profile = read_json(within(root, "profile.json"))
    require(isinstance(profile, dict) and type(profile.get("schema")) is int and profile["schema"] == 1,
            "unsupported profile schema")
    require(profile.get("methodology") == conn["methodology"] and profile.get("version") == conn["version"],
            "profile identity differs from connection")
    entry = within(root, profile.get("entry"))
    require(entry.is_file(), "workflow entry unavailable")
    git(root, "ls-files", "--error-unmatch", "--", profile["entry"])
    paths = profile.get("paths")
    require(isinstance(paths, dict) and set(paths) == {"workflow", "supports"},
            "profile paths require workflow and supports (nullable)")
    workflow_dir = within(root, paths["workflow"])
    require(workflow_dir.is_dir(), "workflow directory unavailable")
    require(git(root, "ls-files", "--", paths["workflow"].rstrip("/") + "/"),
            "workflow directory must contain tracked files")
    supports_dir = None
    if paths["supports"] is not None:
        supports_dir = within(root, paths["supports"])
        require(supports_dir.is_dir(), "adopted supports directory unavailable")
        require(git(root, "ls-files", "--", paths["supports"].rstrip("/") + "/"),
                "supports directory must contain tracked files")
    facts = profile.get("product_sources")
    require(isinstance(facts, list) and facts, "declare product source references")
    for fact in facts:
        require(isinstance(fact, dict) and set(fact) == {"path", "revision", "kind"},
                "product source requires path, revision, kind")
        require(fact["kind"] in ("fact", "approved-rule", "authority"), "unknown product source kind")
        require(fact["revision"] == "task-start", "preview.8 resolves product sources at task-start")
        require(within(product, fact["path"]).is_file(), "product source unavailable")
    records = profile.get("records")
    require(isinstance(records, dict), "declare work record ownership and location")
    for key in ("location", "retention_owner", "revision_relation", "access_failure"):
        require(isinstance(records.get(key), str) and records[key].strip(), "missing records." + key)
    require(records["access_failure"] == "stop-dependent-work", "record failure must stop dependent work")
    require(git(root, "rev-parse", "HEAD") == conn["commit"] and
            not git(root, "status", "--porcelain", "--untracked-files=all", "--ignored"),
            "workflow changed during resolution")
    return {"state": "READY", "task": task, "area": area, "product": str(product),
            "product_revision": git(product, "rev-parse", "HEAD"),
            "product_dirty": bool(git(product, "status", "--porcelain", "--untracked-files=all")),
            "workflow_root": str(root), "workflow_commit": conn["commit"],
            "workflow_dir": str(workflow_dir),
            "methodology_dir": str(supports_dir) if supports_dir is not None else None,
            "entry": str(entry), "profile": str(root / "profile.json"),
            "product_sources": facts, "records": records,
            "next": "Read the entry and referenced product rules; verify records access before edits. READY is not proof of activation or compliance."}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--project-root")
    parser.add_argument("--area")
    parser.add_argument("--config")
    parser.add_argument("--task")
    parser.add_argument("--selected", action="store_true")
    parser.add_argument("--fresh-session", action="store_true")
    args = parser.parse_args(argv)
    try:
        if args.selected:
            require(all((args.project_root, args.area, args.config, args.task)), "selected task requires all inputs")
        result = resolve(args.project_root, args.area, args.config, args.selected, args.task, args.fresh_session)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    except (ConnectionError, OSError, ValueError, TypeError, KeyError) as error:
        print(json.dumps({"state": "BLOCKED", "reason": str(error)}, ensure_ascii=False))
        return 2


if __name__ == "__main__":
    sys.exit(main())
