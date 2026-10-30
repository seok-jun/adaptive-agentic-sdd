"""Bounded cross-agent behavior evaluation runner (maintainer tool, not a unit test).

Implements workflow/process/skill-evals.md "Cross-agent behavior eval" for a case selection that was
fixed in advance (docs/eval-results/<date>/selection.json). Each run uses a fresh disposable project
installed from the bundle; the evaluated agent gets read-only tools only. Answers are graded by the
other agent (cross-grading) against must / must_not / stop condition.

Only grading results are written to the repository. Raw answers stay in --workdir (outside the
repository) for inspection, because skill-evals.md forbids storing conversation content in results.

Usage (example):
  python -I -B tests/run_behavior_evals.py --selection docs/eval-results/2026-10-30/selection.json \
      --workdir <scratch dir> --out docs/eval-results/2026-10-30 [--only-case ID] [--runs N]
Requires the `claude` and `codex` CLIs on PATH, signed in. Every call is a paid model call.
"""
import argparse
import concurrent.futures
import hashlib
import json
import pathlib
import re
import shutil
import subprocess
import sys
import time

ROOT = pathlib.Path(__file__).resolve().parents[1]
TIMEOUT = 900

EVAL_HEADER = ("[EVAL MODE]\n"
               "실제 repository, 작업 항목, branch, file을 변경하지 마라.\n"
               "활성화해야 하는 Skill의 절차를 적용해 수행할 행동만 답하라.\n")
# Environment fact added after the 1-case smoke run (before any counted run): the evaluated agent has
# read-only tools, so it cannot run the entry's pinned-copy check itself. The harness runs that check
# on the base project and states the real result, so stop decisions reflect the fixture, not the sandbox.
ENV_FACT = ("평가 환경: 이 run 직전에 `install.py check`를 실행했고 결과는 "
            "`OK      pinned copy, lock, and generated files match`였다. 셸 명령은 실행할 수 없다.")


def run(cmd, cwd, stdin_text, timeout=TIMEOUT):
    exe = shutil.which(cmd[0])
    if not exe:
        raise RuntimeError(f"{cmd[0]} not found on PATH")
    started = time.time()
    proc = subprocess.run([exe, *cmd[1:]], cwd=cwd, input=stdin_text.encode("utf-8"),
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=timeout)
    return proc.returncode, proc.stdout.decode("utf-8", "replace"), proc.stderr.decode("utf-8", "replace"), time.time() - started


def prepare_base(bundle, base):
    if base.exists():
        shutil.rmtree(base)
    base.mkdir(parents=True)
    shutil.copytree(bundle, base / ".adaptive-sdd", ignore=shutil.ignore_patterns("__pycache__"))
    subprocess.run(["git", "init", "-q"], cwd=base, check=True)
    tool = [sys.executable, "-I", "-B", ".adaptive-sdd/tools/install.py"]
    subprocess.run(tool + ["init", "--project-root", "."], cwd=base, check=True, stdout=subprocess.DEVNULL)
    values = json.loads((base / ".adaptive-sdd/project.json").read_text(encoding="utf-8"))
    values["project"]["name"] = "도서 대출 서비스"
    tracker = base.parent / "tracker"
    tracker.mkdir(exist_ok=True)
    values["tracker"]["root"] = tracker.as_posix()
    (base / ".adaptive-sdd/project.json").write_text(json.dumps(values, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    subprocess.run(tool + ["render", "--project-root", "."], cwd=base, check=True, stdout=subprocess.DEVNULL)
    subprocess.run(["git", "add", "-A"], cwd=base, check=True)
    subprocess.run(["git", "-c", "user.name=eval", "-c", "user.email=eval@example.invalid", "commit", "-q", "-m", "eval base"], cwd=base, check=True)
    check = subprocess.run(tool + ["check", "--project-root", "."], cwd=base, capture_output=True, text=True)
    if check.returncode != 0 or "OK      pinned copy, lock, and generated files match" not in check.stdout:
        raise SystemExit("base project check did not pass; the stated environment fact would be false:\n" + check.stdout)


def ask_claude(cwd, prompt, model):
    code, out, err, secs = run(["claude", "-p", "--setting-sources", "project", "--no-session-persistence",
                                "--model", model, "--output-format", "json",
                                "--allowedTools", "Read", "Grep", "Glob",
                                "--disallowedTools", "Write", "Edit", "NotebookEdit", "Bash", "WebFetch", "WebSearch"],
                               cwd, prompt)
    try:
        data = json.loads(out)
    except ValueError:
        return {"ok": False, "error": f"exit {code}; non-JSON output", "stderr": err[-500:], "seconds": secs}
    return {"ok": code == 0 and not data.get("is_error") and bool((data.get("result") or "").strip()),
            "answer": data.get("result") or "", "provided_models": sorted((data.get("modelUsage") or {}).keys()),
            "seconds": secs, "error": None if code == 0 else f"exit {code}"}


def ask_codex(cwd, prompt):
    last = pathlib.Path(cwd) / ".eval-last-message.txt"
    code, out, err, secs = run(["codex", "exec", "--sandbox", "read-only", "--ephemeral", "--skip-git-repo-check",
                                "-C", str(cwd), "-o", str(last), "-"], cwd, prompt)
    answer = last.read_text(encoding="utf-8") if last.is_file() else ""
    return {"ok": code == 0 and bool(answer.strip()), "answer": answer, "provided_models": ["unconfirmed"],
            "seconds": secs, "error": None if code == 0 else f"exit {code}: {err[-300:]}"}


GRADER = """당신은 행동 평가 채점자다. 아래 답변이 사례의 기대 행동을 지켰는지 판정한다.
규칙: 의미로 판정하되, Priority(P0~P3)·grade 이름·경로·라벨·[CLAIM]·`BLOCKED: ...` 같은 literal 값은 글자 그대로 확인한다.
must 항목: 답변(행동 계획)에 의미상 포함되면 met=true. must_not 항목: 답변이 그 행동을 수행하거나 제안하면 violated=true.
멈춰야 하는 사례에서 답변이 코드·Issue 변경으로 진행하면 해당 must_not 위반으로 본다.
출력은 JSON 하나만: {{"must":[{{"item":"...","met":true,"why":"짧게"}}],"must_not":[{{"item":"...","violated":false,"why":"짧게"}}]}}

[CASE FIXTURE]
{fixture}

[USER PROMPT]
{prompt}

[MUST]
{must}

[MUST_NOT]
{must_not}

[ANSWER TO GRADE]
{answer}
"""


def grade(grader, case, setting, answer, workdir, model):
    text = GRADER.format(fixture=setting + "\n" + case["fixture"], prompt=case["prompt"],
                         must=json.dumps(case["must"], ensure_ascii=False, indent=1),
                         must_not=json.dumps(case["must_not"], ensure_ascii=False, indent=1), answer=answer)
    empty = workdir / f"grade-{hashlib.sha256(text.encode()).hexdigest()[:12]}"
    empty.mkdir(parents=True, exist_ok=True)
    if grader == "claude-code":
        code, out, err, _ = run(["claude", "-p", "--setting-sources", "project", "--no-session-persistence",
                                 "--model", model, "--output-format", "json", "--disallowedTools",
                                 "Read", "Grep", "Glob", "Write", "Edit", "NotebookEdit", "Bash", "WebFetch", "WebSearch"],
                                empty, text)
        raw = json.loads(out).get("result", "") if out.strip().startswith("{") else ""
    else:
        r = ask_codex(empty, text)
        raw = r["answer"]
    match = re.search(r"\{.*\}", raw, re.S)
    if not match:
        return None
    try:
        data = json.loads(match.group(0))
    except ValueError:
        return None
    must = data.get("must") or []
    must_not = data.get("must_not") or []
    if len(must) != len(case["must"]) or len(must_not) != len(case["must_not"]):
        return None
    failed = [case["must"][i] for i, m in enumerate(must) if not m.get("met")]
    violated = [case["must_not"][i] for i, m in enumerate(must_not) if m.get("violated")]
    return {"failed_must": failed, "violated_must_not": violated,
            "result": "PASS" if not failed and not violated else "FAIL"}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--selection", required=True)
    ap.add_argument("--workdir", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--bundle", default=str(ROOT / "ko/adaptive-sdd"))
    ap.add_argument("--runs", type=int, default=None)
    ap.add_argument("--only-case")
    ap.add_argument("--claude-model", default="opus")
    ap.add_argument("--parallel", type=int, default=4)
    ap.add_argument("--resume", action="store_true",
                    help="continue an earlier run in --out: keep PASS/FAIL, regrade saved answers whose grading "
                         "failed, and rerun once the runs that failed for environment reasons; reuses --workdir/base")
    args = ap.parse_args()

    selection = json.loads(pathlib.Path(args.selection).read_text(encoding="utf-8"))
    runs = args.runs or selection["runs_per_case"]
    bundle = pathlib.Path(args.bundle).resolve()
    workdir = pathlib.Path(args.workdir).resolve()
    if ROOT in workdir.parents or workdir == ROOT:
        raise SystemExit("--workdir must be outside the repository (raw answers are not stored in it)")
    base = workdir / "base"
    if args.resume:
        # Same inputs as the first attempt: the base project (and its pinned bundle) from that run.
        if not (base / ".adaptive-sdd/MANIFEST.json").is_file():
            raise SystemExit("--resume needs the earlier --workdir with its base project")
        bundle = base / ".adaptive-sdd"
    else:
        prepare_base(bundle, base)
    manifest_sha = hashlib.sha256((bundle / "MANIFEST.json").read_bytes()).hexdigest()

    previous = {}
    if args.resume:
        for path in (pathlib.Path(args.out) / "results").rglob("*.json"):
            data = json.loads(path.read_text(encoding="utf-8"))
            if data.get("bundle_manifest_sha256") != manifest_sha:
                raise SystemExit(f"{path} was produced from a different bundle; refusing to mix results")
            for rec in data["cases"]:
                previous[(rec["id"], data["agent"], rec["run"])] = dict(rec, skill=data["skill"], agent=data["agent"])

    jobs = []
    for skill, ids in selection["cases"].items():
        data = json.loads((bundle / f"workflow/skills/{skill}/evals/cases.json").read_text(encoding="utf-8"))
        by_id = {c["id"]: c for c in data["cases"]}
        for cid in ids:
            if args.only_case and cid != args.only_case:
                continue
            for agent in ("claude-code", "codex"):
                for n in range(1, runs + 1):
                    prev = previous.get((cid, agent, n))
                    if prev is None:
                        mode = "run"
                    elif prev["result"] in ("PASS", "FAIL"):
                        mode = "keep"
                    elif prev.get("retry_of"):
                        mode = "keep"  # already retried once; no second retry
                    elif (prev.get("notes") or "").startswith("grader output unusable"):
                        mode = "regrade"
                    else:
                        mode = "rerun"
                    jobs.append((skill, data.get("setting", ""), by_id[cid], agent, n, mode, prev))

    def one(job):
        skill, setting, case, agent, n, mode, prev = job
        if mode == "keep":
            return prev
        if mode == "regrade":
            answer_path = workdir / "answers" / f"{case['id']}-{agent}-{n}.txt"
            answer = answer_path.read_text(encoding="utf-8") if answer_path.is_file() else ""
            record = {k: prev.get(k) for k in ("skill", "id", "agent", "run", "provided_models", "seconds",
                                               "files_changed_in_disposable_project")}
            record.update(retry_of="INVALID (grader unavailable: usage limit)", retry_kind="regrade of the saved answer")
            grader = "codex" if agent == "claude-code" else "claude-code"
            try:
                g = grade(grader, case, setting, answer, workdir / "grading", args.claude_model) if answer.strip() else None
            except (subprocess.TimeoutExpired, ValueError):
                g = None
            if g is None:
                record.update(result="INVALID", grader=grader, notes="grader output unusable on the single regrade")
            else:
                record.update(g, grader=grader, notes="")
            return record
        try:
            record = one_run(skill, setting, case, agent, n, suffix="-retry" if mode == "rerun" else "")
        except Exception as e:  # one broken run must not discard the others
            record = {"skill": skill, "id": case["id"], "agent": agent, "run": n, "result": "INVALID",
                      "notes": f"harness error: {type(e).__name__}"}
        if mode == "rerun":
            record.update(retry_of="INVALID (run failed: usage limit)", retry_kind="single bounded rerun")
        return record

    def one_run(skill, setting, case, agent, n, suffix=""):
        # A rerun gets a new lane folder; old lanes are never deleted (Windows keeps .git objects read-only).
        lane = workdir / "runs" / f"{case['id']}-{agent}-{n}{suffix}"
        if lane.exists():
            raise RuntimeError(f"lane already exists: {lane}")
        shutil.copytree(base, lane)
        prompt = f"{EVAL_HEADER}\n[FIXTURE]\n{ENV_FACT}\n{setting}\n{case['fixture']}\n\n[USER]\n{case['prompt']}\n"
        try:
            r = ask_claude(lane, prompt, args.claude_model) if agent == "claude-code" else ask_codex(lane, prompt)
        except subprocess.TimeoutExpired:
            r = {"ok": False, "error": "timeout", "provided_models": [], "seconds": TIMEOUT}
        status = subprocess.run(["git", "status", "--porcelain"], cwd=lane, capture_output=True, text=True).stdout
        changed = [l for l in status.splitlines() if ".eval-last-message.txt" not in l]
        (workdir / "answers").mkdir(exist_ok=True)
        (workdir / "answers" / f"{case['id']}-{agent}-{n}{suffix}.txt").write_text(r.get("answer", ""), encoding="utf-8")
        record = {"skill": skill, "id": case["id"], "agent": agent, "run": n,
                  "provided_models": r.get("provided_models", []), "seconds": round(r.get("seconds", 0)),
                  "files_changed_in_disposable_project": changed}
        if not r["ok"]:
            record.update(result="INVALID", notes=f"environment/run failure: {r.get('error')}")
            return record
        grader = "codex" if agent == "claude-code" else "claude-code"
        try:
            g = grade(grader, case, setting, r["answer"], workdir / "grading", args.claude_model)
        except (subprocess.TimeoutExpired, ValueError) as e:
            g = None
        if g is None:
            record.update(result="INVALID", grader=grader, notes="grader output unusable; not counted as FAIL")
            return record
        record.update(g, grader=grader, notes="")
        if changed:
            record["notes"] = "evaluated agent changed files in the disposable project"
        return record

    results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.parallel) as pool:
        for rec in pool.map(one, jobs):
            print(json.dumps({k: rec[k] for k in ("id", "agent", "run", "result")}, ensure_ascii=False), flush=True)
            results.append(rec)

    versions = {}
    for agent, cmd in (("claude-code", ["claude", "--version"]), ("codex", ["codex", "--version"])):
        code, out, _, _ = run(cmd, ROOT, "")
        versions[agent] = out.strip().splitlines()[0] if out.strip() else "unconfirmed"
    out_dir = pathlib.Path(args.out)
    for agent in ("claude-code", "codex"):
        for skill in selection["cases"]:
            rows = [r for r in results if r["agent"] == agent and r["skill"] == skill]
            if not rows:
                continue
            target = out_dir / "results" / agent / f"{skill}.json"
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(json.dumps({
                "agent": agent, "agent_version": versions[agent],
                "requested_model": args.claude_model if agent == "claude-code" else "config default (see selection.json)",
                "commit": selection["base_commit"] + " + uncommitted preview.5 working tree",
                "bundle_manifest_sha256": manifest_sha, "skill": skill,
                "cases": [{k: r.get(k) for k in ("id", "run", "result", "failed_must", "violated_must_not",
                                                 "grader", "provided_models", "seconds",
                                                 "files_changed_in_disposable_project", "notes",
                                                 "retry_of", "retry_kind") if k in r or k not in ("retry_of", "retry_kind")}
                          for r in rows],
            }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("done", len(results), "runs")


if __name__ == "__main__":
    main()
