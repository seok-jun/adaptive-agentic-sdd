"""Adaptive Agentic SDD installer: render project-dependent files from a pinned copy.

Standard library only (Python 3.8+). The pinned copy lives in <project>/.adaptive-sdd/ and is never
modified by this tool. Project values live in <project>/.adaptive-sdd/project.json (human-owned).
Generated files are recorded in <project>/.adaptive-sdd/install.lock.json so that a later `check`
can re-render in memory and report hand-edits or drift without overwriting anything.
"""
import argparse
import hashlib
import json
import pathlib
import re
import shlex
import sys
from datetime import datetime

RENDERER_VERSION = "1"
EXECUTION_GRADES = ("Trivial", "Small", "Medium", "Large")
NL = "\n"
COPY_DIRNAME = ".adaptive-sdd"
CONNECTION = ".agentics/adaptive-sdd.json"
COPY_DIRS = ("methodology", "workflow", "templates", "tools")
TOOL_DIRS = {"claude-code": ".claude/skills", "codex": ".agents/skills"}
SKILLS = [
    ("managing-issues",
     "{name}의 작업 항목(Issue)을 생성·분류·우선순위 재조정·본문 재작성하고 선택적 Epic의 작업 구성·의존성을 조율할 때 사용한다. Priority/실행 grade 판정, 작업 경계, "
     "Mermaid·Visual Spec 판단에 쓴다. 코드 구현에는 사용하지 않는다."),
    ("implementing-issues",
     "{name}의 승인된 Issue를 번호나 명시한 참조로 받아 명시한 모듈 경계 안에서 구현한다. 기존 Issue의 진행·구현·마무리를 요청할 때 "
     "사용하며 SDD gate, 병렬 격리, 범위 제한 수정과 검증을 적용한다. 새 Issue만 작성할 때는 사용하지 않는다."),
    ("parallel-development",
     "{name}의 병렬 agent 작업의 claim·격리·동기화·해제·통합을 관리한다. Issue 코드 수정 전, branch/worktree 생성, 경로 충돌 확인, "
     "공유 contract 처리에 사용한다. Issue 초안만 작성할 때는 사용하지 않는다."),
    ("finishing-issues",
     "구현을 마친 {name}의 Issue 작업을 종료한다. 최종 diff 검토, business 문서 동기화, 검증, SDD 정리, 종료 기록, 병합 확인, "
     "lane 해제에 사용한다. 구현이 종료 준비되기 전에는 사용하지 않는다."),
]
MARKERS = {
    "md": ("<!-- adaptive-sdd:begin (생성 구간. 직접 고치지 않는다) -->", "<!-- adaptive-sdd:end -->"),
    "gitattributes": ("# adaptive-sdd:begin (생성 구간. 직접 고치지 않는다)", "# adaptive-sdd:end"),
}


class InstallError(Exception):
    pass


# ---------------------------------------------------------------- template engine
_TOKEN = re.compile(r"\{\{(#each|#if|else|/each|/if)?\s*([^}]*?)\s*\}\}")


def _parse(text):
    """Parse into a tree: list of str | ("var", path) | ("each"/"if", path, body, else_body)."""
    root = {"kind": None, "path": None, "body": [], "else": [], "in_else": False}
    stack = [root]

    def current():
        top = stack[-1]
        return top["else"] if top["in_else"] else top["body"]

    pos = 0
    for m in _TOKEN.finditer(text):
        if m.start() > pos:
            current().append(text[pos:m.start()])
        pos = m.end()
        tag, arg = m.group(1), m.group(2)
        if tag in ("#each", "#if"):
            stack.append({"kind": tag[1:], "path": arg, "body": [], "else": [], "in_else": False})
        elif tag == "else":
            top = stack[-1]
            if top["kind"] is None or top["in_else"]:
                raise InstallError("template: unexpected {{else}}")
            top["in_else"] = True
        elif tag in ("/each", "/if"):
            top = stack.pop()
            if top["kind"] != tag[1:]:
                raise InstallError(f"template: mismatched {tag}")
            current().append((top["kind"], top["path"], top["body"], top["else"]))
        else:
            current().append(("var", arg))
    if pos < len(text):
        current().append(text[pos:])
    if len(stack) != 1:
        raise InstallError("template: unclosed block")
    return root["body"]


def _lookup(path, ctx, item):
    if path == "this":
        return item
    if path.startswith("."):
        cur = item
        parts = path[1:].split(".")
    else:
        cur = ctx
        parts = path.split(".")
    for part in parts:
        if isinstance(cur, dict):
            cur = cur.get(part)
        else:
            return None
    return cur


def _truthy(v):
    if v is None or v is False:
        return False
    if isinstance(v, (str, list, dict)):
        return len(v) > 0
    return True


def _render_nodes(nodes, ctx, item):
    out = []
    for n in nodes:
        if isinstance(n, str):
            out.append(n)
        elif n[0] == "var":
            v = _lookup(n[1], ctx, item)
            if isinstance(v, (dict, list)):
                raise InstallError(f"template: {n[1]} is not a scalar")
            out.append("" if v is None else str(v))
        elif n[0] == "if":
            branch = n[2] if _truthy(_lookup(n[1], ctx, item)) else n[3]
            out.append(_render_nodes(branch, ctx, item))
        elif n[0] == "each":
            seq = _lookup(n[1], ctx, item)
            if _truthy(seq):
                if not isinstance(seq, list):
                    raise InstallError(f"template: {n[1]} is not a list")
                for el in seq:
                    out.append(_render_nodes(n[2], ctx, el))
            else:
                out.append(_render_nodes(n[3], ctx, item))
    return "".join(out)


def render_template(text, ctx):
    return _render_nodes(_parse(text), ctx, None)


# ---------------------------------------------------------------- helpers
def sha(data):
    return hashlib.sha256(data).hexdigest()


def canonical(value):
    return (json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + NL).encode("utf-8")


def read_text(path):
    data = path.read_bytes()
    if data.startswith(b"\xef\xbb\xbf"):
        data = data[3:]
    return data.decode("utf-8").replace("\r\n", NL)


def write_text(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(text.encode("utf-8"))


def copy_root(project_root):
    return project_root / COPY_DIRNAME


def roots(args):
    product = pathlib.Path(args.project_root).resolve()
    explicit = getattr(args, "harness_root", None)
    connection = product / CONNECTION
    if explicit:
        source = pathlib.Path(explicit).resolve()
    elif connection.is_file():
        data = json.loads(read_text(connection))
        if data.get("schema") != 1 or data.get("project_root") != product.as_posix():
            raise InstallError("external connection belongs to another checkout; use an explicit installation pair")
        value = data.get("harness_root")
        if not isinstance(value, str) or not pathlib.Path(value).is_absolute():
            raise InstallError("external connection needs an absolute harness_root")
        source = pathlib.Path(value).resolve()
        if data.get("manifest_sha256") != sha(manifest_path(source).read_bytes()):
            raise InstallError("external pin changed; explicitly render with --harness-root after reviewing the upgrade")
    else:
        source = product
    if source != product and (source in product.parents or product in source.parents):
        raise InstallError("external harness and product checkout must not contain each other")
    lock = load_lock(source)
    if lock and lock.get("project_root") not in (None, product.as_posix()):
        raise InstallError("harness is already bound to another checkout")
    return source, product


def output_root(source, product, relative):
    return source if relative.startswith(COPY_DIRNAME + "/") else product


def templates_dir(project_root):
    root = copy_root(project_root)
    for name in ("templates", "project-templates"):
        if (root / name).is_dir():
            return root / name
    raise InstallError(f"templates not found under {root}")


# ---------------------------------------------------------------- values
def load_values(project_root):
    path = copy_root(project_root) / "project.json"
    if not path.is_file():
        raise InstallError(f"missing {path}; run `init` first")
    try:
        values = json.loads(read_text(path))
    except ValueError as e:
        raise InstallError(f"project.json is not valid JSON: {e}")
    if not isinstance(values, dict) or values.get("schema") != 1:
        raise InstallError("project.json: schema must be 1")
    name = (values.get("project") or {}).get("name")
    if not isinstance(name, str) or not name.strip():
        raise InstallError("project.json: project.name is required")
    kind = (values.get("tracker") or {}).get("kind")
    if kind not in ("local-docs", "github"):
        raise InstallError("project.json: tracker.kind must be local-docs or github")
    tools = values.get("tools") or []
    if not tools or any(t not in TOOL_DIRS for t in tools):
        raise InstallError(f"project.json: tools must be a non-empty subset of {sorted(TOOL_DIRS)}")
    if (values["tracker"].get("merge_method") or "") not in ("", "merge", "squash", "rebase"):
        raise InstallError("project.json: tracker.merge_method must be merge, squash, rebase, or empty")
    for path, keys in LIST_SHAPES.items():
        _check_list(values, path, keys)
    for i, mapping in enumerate(values.get("grade_mapping") or []):
        if mapping["min_grade"] not in EXECUTION_GRADES:
            raise InstallError(
                f"project.json: grade_mapping[{i}].min_grade must be one of "
                f"{', '.join(EXECUTION_GRADES)}; Epic is an optional management type, "
                "not an execution grade. Reclassify the actual change; do not auto-convert it."
            )
    validate_settings(values)
    return values


def settings(values):
    result = json.loads(json.dumps(values))
    defaults = {
        "git": {"remote": "origin", "base_branch": "main", "merge_branch": "main"},
        "review": {"repository": "", "remote": "", "branch": ""},
        "tracker": {"id_source": "generated", "id_format": "", "child_id_rule": ""},
        "project": {"conversation_language": "", "conventions": ""},
        "build": {"test_mode": "persistent", "test_format": "", "test_preserve_at": ""},
        "routing": {"capabilities": [], "role_defaults": [], "qualification_records": ""},
    }
    for section, fields in defaults.items():
        target = result.setdefault(section, {})
        for key, value in fields.items():
            target.setdefault(key, value)
    for section, key in (("build", "checks"), ("routing", "capabilities"), ("routing", "role_defaults")):
        result[section][key] = result[section].get(key) or []
    result["tracker_external_id"] = result["tracker"]["id_source"] == "external"
    result["temporary_tests"] = result["build"]["test_mode"] == "temporary"
    result["no_new_tests"] = result["build"]["test_mode"] == "none"
    result["review"]["remote"] = result["review"]["remote"] or result["git"]["remote"]
    return result


def validate_settings(values):
    for section in ("git", "review", "project", "build", "tracker", "routing"):
        if section in values and not isinstance(values[section], dict):
            raise InstallError(f"project.json: {section} must be an object")
    cfg = settings(values)
    fields = {"git": ("remote", "base_branch", "merge_branch"),
              "review": ("repository", "remote", "branch"),
              "project": ("conversation_language", "conventions"),
              "tracker": ("id_source", "id_format", "child_id_rule"),
              "build": ("test_mode", "test_format", "test_preserve_at"),
              "routing": ("qualification_records",)}
    for section, keys in fields.items():
        for key in keys:
            value = cfg[section][key]
            if not isinstance(value, str) or any(c in value for c in "\r\n\x00"):
                raise InstallError(f"project.json: {section}.{key} must be a single-line string")
    def valid_git_name(value):
        return (bool(re.fullmatch(r"[A-Za-z0-9_][A-Za-z0-9_./-]*", value))
                and ".." not in value and "//" not in value
                and not value.endswith(("/", "."))
                and all(not part.startswith(".") and not part.endswith(".lock")
                        for part in value.split("/")))

    for key in fields["git"]:
        if not valid_git_name(cfg["git"][key]):
            raise InstallError(f"project.json: invalid git.{key}")
    if cfg["review"]["repository"] and not pathlib.Path(cfg["review"]["repository"]).is_absolute():
        raise InstallError("review.repository must be an absolute repository path")
    for key in ("remote", "branch"):
        value = cfg["review"][key]
        if value and not valid_git_name(value):
            raise InstallError(f"invalid review.{key}")
    if cfg["tracker"]["id_source"] not in ("generated", "external"):
        raise InstallError("tracker.id_source must be generated or external")
    if cfg["tracker_external_id"] and not cfg["tracker"]["id_format"].strip():
        raise InstallError("external IDs require tracker.id_format")
    if cfg["build"]["test_mode"] not in ("persistent", "temporary", "none"):
        raise InstallError("build.test_mode must be persistent, temporary, or none")
    if cfg["temporary_tests"] and not cfg["build"]["test_preserve_at"].strip():
        raise InstallError("temporary tests require build.test_preserve_at")
    for check in cfg["build"].get("checks", []):
        if check["method"] not in ("command", "manual") or check["actor"] not in ("agent", "human") or check["required"] not in ("required", "optional"):
            raise InstallError("invalid build.checks method/actor/required")
    for item in cfg["routing"]["capabilities"]:
        if item["tier"] not in ("cheap", "strong", "frontier"):
            raise InstallError("routing capability tier must be cheap, strong, or frontier")
        try:
            expiry = datetime.fromisoformat(item["valid_until"].replace("Z", "+00:00"))
            if expiry.tzinfo is None:
                raise ValueError()
        except ValueError:
            raise InstallError("capability valid_until needs an ISO timestamp with timezone")
    for item in cfg["routing"]["role_defaults"]:
        if item["role"] not in ("PLAN", "IMPLEMENT", "REVIEW", "TEST_DOCS", "FINISH"):
            raise InstallError("unknown routing role default")


# list fields: None = list of strings, tuple = list of objects with exactly these string keys
LIST_SHAPES = {
    "tracker.allowed_authors": None,
    "grade_mapping": ("change", "min_grade"),
    "human_judgment.points": None,
    "human_judgment.delegations": ("scope", "date", "confirmed_by"),
    "build.jdk_candidates": None,
    "build.verification": ("scope", "commands"),
    "build.checks": ("scope", "method", "actor", "instructions", "evidence", "required"),
    "build.instrumentation_paths": None,
    "modules.list": ("path", "role"),
    "modules.shared_contracts": None,
    "modules.root_integration": None,
    "modules.dependency_rules": None,
    "routing.deny_models": None,
    "routing.role_defaults": ("role", "model", "reasoning"),
    "routing.capabilities": ("host", "model", "tier", "reasoning", "source", "identity", "valid_until"),
    "priority.product_examples": ("input", "examples"),
    "evidence.allowed": None,
    "evidence.forbidden": None,
    "hard_guard_extra": None,
}


def _check_list(values, path, keys):
    node = values
    for part in path.split("."):
        node = node.get(part) if isinstance(node, dict) else None
    if node is None:
        return
    if not isinstance(node, list):
        raise InstallError(f"project.json: {path} must be a list")
    for i, item in enumerate(node):
        where = f"project.json: {path}[{i}]"
        if keys is None:
            if not isinstance(item, str) or not item.strip():
                raise InstallError(f"{where} must be a non-empty string")
            continue
        if not isinstance(item, dict) or set(item) != set(keys):
            raise InstallError(f"{where} must be an object with exactly the keys {list(keys)}")
        for k in keys:
            if not isinstance(item[k], str) or not item[k].strip():
                raise InstallError(f"{where}.{k} must be a non-empty string")


def values_digest(values):
    return sha(canonical(values))


# ---------------------------------------------------------------- outputs
def plan_outputs(project_root, values, product_root=None):
    """Return list of (relpath, kind, content). kind: file | block-md | block-gitattributes."""
    tdir = templates_dir(project_root)
    product_root = product_root or project_root
    ctx = settings(values)
    external = product_root != project_root
    ctx["external"] = external
    ctx["source_root"] = project_root.as_posix() if external else "P"
    # Generated commands target PowerShell on Windows and POSIX sh elsewhere.
    # Never interpolate an absolute path into shell-expanding double quotes.
    def shell_literal(value):
        if sys.platform == "win32":
            return "'" + value.replace("'", "''") + "'"
        return shlex.quote(value)

    ctx["command_shell"] = (("PowerShell" if sys.platform == "win32" else "POSIX sh")
                            if external else "PowerShell / POSIX sh")
    for action, key in (("check", "check_command"), ("check-evals", "check_evals_command")):
        if external:
            argv = [f"{project_root.as_posix()}/.adaptive-sdd/tools/install.py", action,
                    "--project-root", product_root.as_posix(), "--harness-root", project_root.as_posix()]
            ctx[key] = "python -I -B " + " ".join(shell_literal(arg) for arg in argv)
        else:
            ctx[key] = f"python -I -B .adaptive-sdd/tools/install.py {action} --project-root ."
    ctx["tool_dirs"] = [TOOL_DIRS[t] for t in values["tools"]]
    ctx["tracker_is_local"] = values["tracker"]["kind"] == "local-docs"
    outs = []
    for tmpl in sorted((tdir / "project").glob("*.md.tmpl")):
        rel = f"{COPY_DIRNAME}/project/{tmpl.name[:-5]}"
        outs.append((rel, "file", render_template(read_text(tmpl), ctx)))
    entry = read_text(tdir / "entry" / "SKILL.md.tmpl")
    for tool in values["tools"]:
        for name, desc in SKILLS:
            sctx = dict(ctx)
            # JSON string syntax is valid YAML, so a project name containing ": " cannot break the frontmatter
            sctx["skill"] = {"name": name,
                             "description": json.dumps(desc.format(name=values["project"]["name"]), ensure_ascii=False)}
            outs.append((f"{TOOL_DIRS[tool]}/{name}/SKILL.md", "file", render_template(entry, sctx)))
    outs.append(("AGENTS.md", "block-md", render_template(read_text(tdir / "blocks" / "AGENTS.block.md.tmpl"), ctx)))
    if "claude-code" in values["tools"]:
        outs.append(("CLAUDE.md", "block-md", render_template(read_text(tdir / "blocks" / "CLAUDE.block.md.tmpl"), ctx)))
    outs.append((".gitattributes", "block-gitattributes",
                 render_template(read_text(tdir / "blocks" / "gitattributes.block.tmpl"), ctx)))
    if external:
        outs.append((CONNECTION, "file", canonical({"schema": 1, "project_root": product_root.as_posix(),
                     "harness_root": project_root.as_posix(), "manifest_sha256": sha(manifest_path(project_root).read_bytes())}).decode("utf-8")))
    return [(rel, kind, content.strip(NL) + NL if kind.startswith("block-") else content)
            for rel, kind, content in outs]


def _markers(kind):
    return MARKERS["md"] if kind == "block-md" else MARKERS["gitattributes"]


def extract_block(text, kind):
    begin, end = _markers(kind)
    if text.count(begin) != 1 or text.count(end) != 1:
        return None
    s = text.index(begin) + len(begin)
    e = text.index(end)
    if e < s:
        return None
    return text[s:e].strip(NL) + NL


def merge_block(existing, block, kind):
    begin, end = _markers(kind)
    body = begin + NL + block.rstrip(NL) + NL + end + NL
    if existing is None or existing == "":
        return body
    if existing.count(begin) == 1 and existing.count(end) == 1:
        if existing.index(end) < existing.index(begin):
            raise InstallError("marker block is damaged (end before begin); fix the markers by hand")
        s = existing.index(begin)
        e = existing.index(end) + len(end)
        tail = existing[e:]
        if tail.startswith(NL):
            tail = tail[1:]
        return existing[:s] + body + tail
    if existing.count(begin) or existing.count(end):
        raise InstallError("marker block is damaged; fix the markers by hand")
    sep = "" if existing.endswith(NL) else NL
    return existing + sep + NL + body


def current_digest(project_root, rel, kind):
    path = project_root / rel
    if not path.is_file():
        return None
    text = read_text(path)
    if kind == "file":
        return sha(text.encode("utf-8"))
    block = extract_block(text, kind)
    return None if block is None else sha(block.encode("utf-8"))


# ---------------------------------------------------------------- manifest / lock
def manifest_path(project_root):
    return copy_root(project_root) / "MANIFEST.json"


def verify_copy(project_root):
    """Return list of (relpath, status) for the pinned copy."""
    mpath = manifest_path(project_root)
    if not mpath.is_file():
        return [("MANIFEST.json", "MISSING")]
    manifest = json.loads(read_text(mpath))
    results = []
    root = copy_root(project_root)
    listed = manifest.get("files", {})
    for rel, expected in sorted(listed.items()):
        p = root / rel
        if not p.is_file():
            results.append((rel, "MISSING"))
        else:
            results.append((rel, "OK" if sha(p.read_bytes()) == expected else "DIFF"))
    for top in COPY_DIRS:
        base = root / top
        if base.is_dir():
            for p in sorted(base.rglob("*")):
                rel = p.relative_to(root).as_posix()
                if p.is_file() and rel not in listed and "__pycache__" not in p.parts:
                    results.append((rel, "EXTRA"))
    return results


def lock_path(project_root):
    return copy_root(project_root) / "install.lock.json"


def load_lock(project_root):
    p = lock_path(project_root)
    return json.loads(read_text(p)) if p.is_file() else None


# ---------------------------------------------------------------- commands
def cmd_init(args):
    project_root, _ = roots(args)
    target = copy_root(project_root) / "project.json"
    if target.exists():
        print(f"exists: {target} (not overwritten)")
        return 0
    example = templates_dir(project_root) / "project.example.json"
    write_text(target, read_text(example))
    print(f"created: {target}")
    return 0


def cmd_render(args):
    project_root, product = roots(args)
    copy_status = verify_copy(project_root)
    bad = [r for r in copy_status if r[1] != "OK"]
    if bad:
        for rel, st in bad:
            print(f"{st:7} copy {rel}")
        raise InstallError("pinned copy does not match MANIFEST.json; render refused")
    values = load_values(project_root)
    old_lock = load_lock(project_root) or {}
    if args.source_tag and not args.source_commit:
        raise InstallError("--source-tag requires --source-commit; supply the verified tag/commit pair")
    source = dict(old_lock.get("source", {}))
    if args.clear_source_tag or (args.source_commit and args.source_commit != source.get("commit")):
        source.pop("tag", None)
    if args.source_tag:
        source["tag"] = args.source_tag
    if args.source_commit:
        source["commit"] = args.source_commit
    old_outputs = old_lock.get("outputs", {})
    accepted = set(args.accept_overwrite or [])
    outputs = {}
    skipped = []
    writes = []
    for rel, kind, content in plan_outputs(project_root, values, product):
        destination = output_root(project_root, product, rel)
        new_digest = sha(content.encode("utf-8"))
        cur = current_digest(destination, rel, kind)
        recorded = old_outputs.get(rel, {}).get("sha256")
        hand_edited = cur is not None and cur != recorded and cur != new_digest
        if hand_edited and rel not in accepted:
            skipped.append(rel)
            # a file the installer never wrote stays unowned (sha256 null) so a later render keeps it too
            outputs[rel] = {"kind": kind, "sha256": recorded}
            print(f"KEPT    {rel} (changed outside the installer; pass --accept-overwrite {rel} to replace)")
            continue
        path = destination / rel
        if kind == "file":
            writes.append((path, content.encode("utf-8")))
        else:
            raw = path.read_bytes() if path.is_file() else b""
            bom = raw.startswith(b"\xef\xbb\xbf")
            crlf = b"\r\n" in raw
            existing = read_text(path) if path.is_file() else None
            merged = merge_block(existing, content, kind)
            if crlf:
                merged = merged.replace(NL, "\r\n")
            writes.append((path, (b"\xef\xbb\xbf" if bom else b"") + merged.encode("utf-8")))
        outputs[rel] = {"kind": kind, "sha256": new_digest}
    # outputs from an earlier render that are no longer generated stay in the lock until a human removes them
    for rel, rec in sorted(old_outputs.items()):
        if rel not in outputs and (output_root(project_root, product, rel) / rel).is_file():
            outputs[rel] = dict(rec, stale=True)
            print(f"STALE   {rel} (no longer generated; the installer does not delete it)")
    # every output is computed before anything is written, so a merge error leaves the project untouched
    for path, data in writes:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
        print(f"WROTE   {path}")
    manifest_digest = sha(manifest_path(project_root).read_bytes())
    source["manifest_sha256"] = manifest_digest
    lock = {
        "schema": 1,
        "renderer_version": RENDERER_VERSION,
        "project_root": product.as_posix() if product != project_root else None,
        "source": source,
        "values_sha256": values_digest(values),
        "outputs": outputs,
    }
    write_text(lock_path(project_root), canonical(lock).decode("utf-8"))
    print(f"WROTE   {COPY_DIRNAME}/install.lock.json")
    if skipped:
        print(f"{len(skipped)} output(s) kept; see KEPT lines")
        return 3
    return 0


def cmd_check(args):
    project_root, product = roots(args)
    problems = 0
    for rel, st in verify_copy(project_root):
        if st != "OK":
            problems += 1
            print(f"{st:7} copy {rel}")
    lock = load_lock(project_root)
    if lock is None:
        print("MISSING install.lock.json (run render)")
        return 1
    if lock.get("source", {}).get("manifest_sha256") != sha(manifest_path(project_root).read_bytes()):
        problems += 1
        print("DIFF    lock source.manifest_sha256 != MANIFEST.json")
    values = load_values(project_root)
    if lock.get("values_sha256") != values_digest(values):
        problems += 1
        print("DIFF    project.json changed since last render (run render)")
    for rel, kind, content in plan_outputs(project_root, values, product):
        expected = sha(content.encode("utf-8"))
        cur = current_digest(output_root(project_root, product, rel), rel, kind)
        recorded = lock.get("outputs", {}).get(rel, {}).get("sha256")
        if cur is None:
            problems += 1
            print(f"MISSING {rel}")
        elif cur != expected or recorded != expected:
            problems += 1
            print(f"DIFF    {rel}")
    planned = {rel for rel, _, _ in plan_outputs(project_root, values, product)}
    for rel in sorted(set(lock.get("outputs", {})) - planned):
        if (output_root(project_root, product, rel) / rel).is_file():
            problems += 1
            print(f"STALE   {rel} (no longer generated; remove it or ask a human)")
    if lock.get("renderer_version") != RENDERER_VERSION:
        problems += 1
        print(f"DIFF    lock renderer_version {lock.get('renderer_version')} != {RENDERER_VERSION} (run render)")
    if problems == 0:
        print("OK      pinned copy, lock, and generated files match")
        return 0
    print(f"{problems} problem(s). Nothing was changed. Ask a human before overwriting.")
    return 1


CASE_KEYS = {"id", "prompt", "fixture", "must", "must_not"}
MIN_CASES_PER_SKILL = 5


def cmd_check_evals(args):
    project_root, _ = roots(args)
    skill_roots = [copy_root(project_root) / "workflow" / "skills"]
    problems = 0
    count = 0
    for root in skill_roots:
        for f in sorted(root.glob("*/evals/cases.json")):
            try:
                data = json.loads(read_text(f))
            except ValueError as e:
                problems += 1
                print(f"INVALID {f}: {e}")
                continue
            cases = data.get("cases") if isinstance(data, dict) else data
            if not isinstance(cases, list):
                problems += 1
                print(f"INVALID {f}: no case list")
                continue
            ids = set()
            if len(cases) < MIN_CASES_PER_SKILL:
                problems += 1
                print(f"INVALID {f}: {len(cases)} case(s), at least {MIN_CASES_PER_SKILL} required")
            for c in cases:
                count += 1
                if not isinstance(c, dict) or not CASE_KEYS.issubset(c):
                    problems += 1
                    print(f"INVALID {f}: case missing {sorted(CASE_KEYS)}")
                    continue
                if not isinstance(c["must"], list) or not isinstance(c["must_not"], list) or not c["must"]:
                    problems += 1
                    print(f"INVALID {f}: {c['id']}: must (non-empty) and must_not must be lists")
                if c["id"] in ids:
                    problems += 1
                    print(f"DUP     {f}: {c['id']}")
                ids.add(c["id"])
    for name, _ in SKILLS:
        skill_md = skill_roots[0] / name / "SKILL.md"
        if not skill_md.is_file():
            problems += 1
            print(f"MISSING {skill_md}")
            continue
        text = read_text(skill_md)
        head = text.split(NL)
        if not head or head[0] != "---" or "---" not in head[1:]:
            problems += 1
            print(f"INVALID {skill_md}: no frontmatter")
            continue
        front = head[1:head[1:].index("---") + 1]
        fields = dict(l.split(":", 1) for l in front if ":" in l)
        if fields.get("name", "").strip() != name:
            problems += 1
            print(f"INVALID {skill_md}: name != {name}")
        if not fields.get("description", "").strip():
            problems += 1
            print(f"INVALID {skill_md}: empty description")
    print(f"{count} case(s), {len(SKILLS)} skill(s), {problems} problem(s)")
    return 0 if problems == 0 else 1


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    for name in ("init", "render", "check", "check-evals"):
        p = sub.add_parser(name)
        p.add_argument("--project-root", required=True)
        p.add_argument("--harness-root", help="dedicated external installation root; omit for in-repo or an existing connection")
        if name == "render":
            p.add_argument("--accept-overwrite", action="append", metavar="RELPATH")
            tag = p.add_mutually_exclusive_group()
            tag.add_argument("--source-tag", help="verified tag name; requires --source-commit")
            tag.add_argument("--clear-source-tag", action="store_true", help="remove an old tag without changing the commit")
            p.add_argument("--source-commit")
    args = ap.parse_args(argv)
    try:
        return {"init": cmd_init, "render": cmd_render, "check": cmd_check, "check-evals": cmd_check_evals}[args.cmd](args)
    except InstallError as e:
        print(f"ERROR   {e}")
        return 2
    except (OSError, ValueError, TypeError) as e:
        print(f"ERROR   installation unavailable or invalid: {type(e).__name__}")
        return 2


if __name__ == "__main__":
    sys.exit(main())
