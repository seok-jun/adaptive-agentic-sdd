#!/usr/bin/env python3
"""Create an offline external-adoption demo (Python 3.8+, Git 2.36+)."""

import argparse
import json
import os
from pathlib import Path
import re
import shlex
import shutil
import subprocess
import sys


CHECKOUT = Path(__file__).resolve().parents[1]
RESOLVER = CHECKOUT / "adaptive-sdd/tools/agentics.py"
TEST_COMMAND = "python -m unittest discover -s tests -t ."
ROLES = (
    "agent-instruction-policy", "build", "execution-routing", "issue-priority",
    "issue-writing-guide", "module-boundaries", "sdd-workflow", "skill-evals", "tracker",
)


class SetupError(Exception):
    pass


def environment(isolated_git=False):
    # Match the resolver's treatment of wrapper redirects. Never inherit an index,
    # object store, worktree, trace file or command-line config from another repo.
    kept = {"GIT_CONFIG_GLOBAL", "GIT_CONFIG_SYSTEM", "GIT_CONFIG_NOSYSTEM"}
    env = {k: v for k, v in os.environ.items()
           if not k.upper().startswith("GIT_") or k.upper() in kept}
    env.update(GIT_ALLOW_PROTOCOL="file", GIT_TERMINAL_PROMPT="0",
               GIT_NO_LAZY_FETCH="1", PYTHONDONTWRITEBYTECODE="1",
               PYTHONIOENCODING="utf-8")
    if isolated_git:
        # Only these child processes ignore user defaults; no user config is edited.
        env.update(GIT_CONFIG_GLOBAL=os.devnull, GIT_CONFIG_SYSTEM=os.devnull,
                   GIT_CONFIG_NOSYSTEM="1")
    return env


def run(args, cwd=None, isolated_git=False):
    result = subprocess.run([str(arg) for arg in args], cwd=cwd,
                            env=environment(isolated_git), capture_output=True,
                            encoding="utf-8", errors="replace")
    if result.returncode:
        raise SetupError("Command failed: {}\n{}{}".format(
            args[0], result.stdout, result.stderr))
    return result.stdout.strip()


def git(root, *args, effective=False):
    return run(["git", "-c", "core.fsmonitor=false", "-c", "core.longpaths=true", "-C", root, *args],
               isolated_git=not effective)


def write(root, name, content):
    path = root / name
    path.parent.mkdir(parents=True, exist_ok=True)
    # Exclusive creation also protects against accidental duplicate output names.
    with path.open("x", encoding="utf-8", newline="\n") as stream:
        stream.write(content.rstrip() + "\n" if content else "")


def write_json(root, name, value):
    write(root, name, json.dumps(value, ensure_ascii=False, indent=2))


def choose(lang, en, ko):
    return ko if lang == "ko" else en


def product_files(lang, target):
    records = (target / "records").as_posix()
    return {
        ".gitignore": "__pycache__/\n*.py[cod]\n",
        "catalog/__init__.py": "",
        "members/__init__.py": "",
        "tests/__init__.py": "",
        "catalog/search.py": '''"""Catalog search helpers."""


def page(items, number, size):
    """Return page number (1-based), with up to size items."""
    if number < 1 or size < 1:
        raise ValueError("number and size must be positive")
    start = (number - 1) * size
    end = start + size - 1
    return items[start:end]
''',
        "members/registry.py": '''"""Member registry helpers; no persistence or authentication."""


def normalize_email(email):
    return email.strip().lower()
''',
        "tests/test_search.py": '''import unittest

from catalog.search import page


class PageTests(unittest.TestCase):
    def test_rejects_non_positive(self):
        for number, size in ((0, 2), (1, 0), (-1, 2)):
            with self.subTest(number=number, size=size):
                with self.assertRaises(ValueError):
                    page([1, 2, 3], number, size)

    def test_empty_input(self):
        self.assertEqual(page([], 1, 3), [])
''',
        "tests/test_registry.py": '''import unittest

from members.registry import normalize_email


class NormalizeTests(unittest.TestCase):
    def test_strips_and_lowercases(self):
        self.assertEqual(normalize_email("  DEMO@EXAMPLE.INVALID "),
                         "demo@example.invalid")
''',
        "README.md": choose(lang, f'''# Tiny library

A disposable Python library. Read the [architecture](docs/archtecture.md).
`page(items, number, size)` uses 1-based page numbers and returns up to `size`
items. `normalize_email` strips whitespace and lowercases an email string.

Run from this folder: `{TEST_COMMAND}` (use `python3` on POSIX if needed).
''', f'''# 작은 라이브러리

부담 없이 실험할 Python 라이브러리입니다. [구조](docs/archtecture.md)를 읽어 보세요.
`page(items, number, size)`는 1부터 시작하는 페이지 번호로 최대 `size`개를
반환합니다. `normalize_email`은 이메일 문자열의 양끝 공백을 제거하고 소문자로 바꿉니다.

이 폴더에서 실행: `{TEST_COMMAND}` (POSIX에서는 필요하면 `python3` 사용).
'''),
        "AGENTS.md": choose(lang, "# Team rule\n\nAdd a regression test for every code bug fix.\n",
                            "# 팀 규칙\n\n코드 버그를 수정할 때마다 회귀 테스트를 추가하세요.\n"),
        "docs/architecture.md": choose(lang, f'''# Product facts

This is a Python 3.8+ standard-library-only library, with no packaging/build step.
The demo team owns both independent implementation modules:
- `catalog/`: pagination; its tests are `tests/test_search.py`.
- `members/`: email normalization only; its tests are `tests/test_registry.py`.

Neither module imports the other. There is no shared cross-module contract,
database, password storage, network service, CI, static analyzer or device test.
`README.md` describes intended behavior; code at the checked revision is observed behavior.
The full test command from the product root is `{TEST_COMMAND}`.
On POSIX, `python3` may replace `python` with the same arguments.
''', f'''# 제품 사실

Python 3.8+ 표준 라이브러리만 사용하며 별도 패키징/빌드 단계가 없습니다.
데모 팀이 다음 독립적인 구현 모듈을 모두 소유합니다.
- `catalog/`: 페이지 나누기. 테스트: `tests/test_search.py`.
- `members/`: 이메일 정규화만 담당. 테스트: `tests/test_registry.py`.

두 모듈은 서로 import하지 않습니다. 모듈 간 공유 계약, 데이터베이스, 비밀번호 저장,
네트워크 서비스, CI, 정적 분석기, 기기 테스트가 없습니다.
`README.md`는 의도한 동작, 확인한 리비전의 코드는 관찰된 현재 동작을 나타냅니다.
제품 루트에서 전체 테스트 명령은 `{TEST_COMMAND}`입니다.
POSIX에서는 같은 인자로 `python3`를 사용할 수 있습니다.
'''),
        "docs/project-rules.md": choose(lang, f'''# Approved demo rules

For every change run the full test command in `docs/architecture.md` on the final
candidate. For a README link fix also check that the relative destination exists.
Keep permanent unittest regression tests for code bug fixes, per `AGENTS.md`.
Record the command, result and verified revision in the work item. No CI is required.

The agent may create task branches, commit, push and merge Trivial/Small changes
into this demo's local `origin/main` after required checks and workflow gates pass.
Use merge commits (`git merge --no-ff`), not squash/rebase. Fetch and verify the
actual origin merge before closing the item. No independent review is added for
routine Trivial/Small work. Medium/Large merges require an explicit human instruction.
`origin` is the local bare repository `{(target / 'remotes/product.git').as_posix()}`.

Product edits belong to the claimed task paths in this product. There are no
integration-only paths; changing architecture or policy still needs human authority.
Records and claims belong to `{records}` using local-docs, with authors
`demo-agent` and `human`. The human user owns retention; there is no backup or
authentication, and lost records cannot be recovered. Use a local disk, not a sync folder.
The agent may create task scratch under `{(target / 'scratch').as_posix()}/<task-id>`
and point TMP/TEMP/TMPDIR there. Disable Python bytecode or keep caches there.
No other projects, user configuration, selected workflow files or network services
are authorized write targets. Host sandbox enforcement must be checked separately.
Only synthetic data and necessary requirements/settled decisions may enter artifacts;
do not copy conversation logs, real personal data, credentials or passwords.
''', f'''# 승인된 데모 규칙

모든 변경의 최종 후보에서 `docs/architecture.md`의 전체 테스트를 실행합니다.
README 링크 수정은 상대 경로 대상이 실제로 있는지도 확인합니다.
코드 버그 수정의 unittest 회귀 테스트는 `AGENTS.md`에 따라 제품에 영구 보존합니다.
작업 항목에 명령, 결과, 검증 리비전을 기록합니다. 별도 CI는 필요하지 않습니다.

에이전트는 필수 검사와 워크플로 gate를 통과한 Trivial/Small 변경의 작업 브랜치
생성, 커밋, push 및 이 데모의 로컬 `origin/main` 병합을 수행할 수 있습니다.
병합 커밋(`git merge --no-ff`)을 사용하며 squash/rebase는 사용하지 않습니다.
실제 origin 병합을 fetch하여 검증한 뒤 항목을 닫습니다. 통상 Trivial/Small에는
별도 독립 리뷰를 추가하지 않습니다. Medium/Large 병합에는 사람의 명시적 지시가 필요합니다.
`origin`은 로컬 bare 저장소 `{(target / 'remotes/product.git').as_posix()}`입니다.

제품 수정은 이 제품 내 claim된 작업 경로로 제한합니다. 통합 전용 경로는 없지만
구조나 정책 변경은 여전히 사람의 권한을 따릅니다.
기록과 claim은 `{records}`에 local-docs 방식으로 저장하며 작성자는
`demo-agent`, `human`입니다. 보존 책임은 사용자에게 있습니다. 백업과 인증은 없으며
잃은 기록은 복구할 수 없습니다. 동기화 폴더가 아닌 로컬 디스크를 사용합니다.
에이전트는 `{(target / 'scratch').as_posix()}/<task-id>`에 작업 임시 폴더를 만들고
TMP/TEMP/TMPDIR를 지정할 수 있습니다. Python 바이트코드를 끄거나 캐시도 그곳에 둡니다.
다른 프로젝트, 사용자 설정, 선택한 워크플로 파일, 네트워크 서비스는 쓰기 대상이 아닙니다.
호스트 샌드박스의 실제 강제 여부는 별도로 확인합니다.
합성 데이터와 필요한 요구사항/확정 결정만 기록하며 대화 로그, 실제 개인정보,
자격 증명이나 비밀번호는 복사하지 않습니다.
'''),
        "docs/authority.md": choose(lang, '''# Human authority

The human user decides product meaning, acceptance ambiguities, architecture,
scope cuts, delegations and Medium/Large merges. No delegation is recorded.
Use only the current agent/manual route; no automatic model switching or delegation.
Required independent review needs a human-arranged qualified separate session;
never replace it with self-review or assume permission to invoke another agent.

Password hashing/storage is deliberately undecided: purpose, data to retain,
storage boundary, algorithm/dependency, access and deletion policy need human
decisions. Stop dependent implementation with `[HUMAN DECISION REQUIRED]`, list
these questions, and await actual decisions. A request to try the example is not
approval of these choices. A Large merge requires the human to merge or explicitly
instruct that particular merge; passing tests/reviews or “continue” is insufficient.
''', '''# 사람의 결정 권한

사용자는 제품 의미, 인수 조건의 모호함, 구조, 범위 축소, 위임 및 Medium/Large 병합을
결정합니다. 기록된 위임은 없습니다. 현재 에이전트/수동 경로만 사용하며 모델 자동 전환이나
위임은 하지 않습니다. 필수 독립 리뷰는 사람이 적격한 별도 세션을 마련해야 합니다.
자체 리뷰로 대체하거나 다른 에이전트 호출 권한을 가정하지 않습니다.

비밀번호 해싱/저장은 의도적으로 미결정 상태입니다. 목적, 보존할 데이터, 저장 경계,
알고리즘/의존성, 접근 및 삭제 정책은 사람이 결정해야 합니다.
`[HUMAN DECISION REQUIRED]`로 의존하는 구현을 멈추고 질문을 나열한 뒤 실제 결정을
기다립니다. 예제를 시도하라는 요청은 이 선택들의 승인이 아닙니다.
Large 병합은 사람이 직접 하거나 해당 병합을 명시적으로 지시해야 합니다.
테스트/리뷰 통과나 일반적인 “계속 진행”만으로는 충분하지 않습니다.
'''),
    }


def project_docs(lang, target, product_origin):
    """External application docs: template fields, with P originals kept authoritative."""
    records = (target / "records").as_posix()
    docs = {
        "agent-instruction-policy": choose(lang, '''# Instructions and document mapping

P means the resolver's `product`; W procedure paths are relative to `workflow_dir`.
Read P sources at task-start and record the actual revision/content read, including
dirty content. These application documents reference originals, not replacement rules.

| Information | Original |
| --- | --- |
| Current request | Current user's explicit instruction; update the item if scope changes |
| Goal, scope, acceptance | Current local-docs item body, excluding Meta and Records |
| Common team rule | P `AGENTS.md`, plus selected W `task-guard.md` |
| Procedure | Selected W entry and applicable process/skill documents |
| Modules, ownership, dependencies, runtime | P `docs/architecture.md` and checked code revision |
| Intended behavior and document index | P `README.md` |
| Required checks and merge permissions | P `docs/project-rules.md` |
| Human authority and delegation | P `docs/authority.md` |
| Past decisions | Item Records; history cannot override current rules |
| SDD working evidence | Location chosen before its consuming phase; see `sdd-workflow.md` |

On a conflict stop dependent work and identify both sources; do not silently relax
P rules. Write human-facing artifacts in English. Preserve identifiers and tool output.
Read W `process/agent-instruction-policy.md` when its trigger applies.
Naming a tool or reviewer in an item does not authorize installation or invocation.
''', '''# 지시와 문서 매핑

P는 resolver의 `product`이며 W 절차 경로는 `workflow_dir` 기준입니다.
task-start에 P 원본을 읽고 실제 리비전/내용을 기록합니다. dirty 내용도 구분합니다.
이 적용 문서는 원본 참조이며 제품 규칙의 대체 원본이 아닙니다.

| 정보 | 원본 |
| --- | --- |
| 현재 요청 | 현재 사용자의 명시적 지시. 범위가 바뀌면 항목 본문도 갱신 |
| 목표, 범위, 인수 조건 | Meta와 Records를 제외한 현재 local-docs 항목 본문 |
| 공통 팀 규칙 | P `AGENTS.md` 및 선택한 W `task-guard.md` |
| 절차 | 선택한 W 진입점과 해당 process/skill 문서 |
| 모듈, 소유권, 의존성, 현재 동작 | P `docs/architecture.md` 및 확인한 코드 리비전 |
| 의도한 동작과 문서 색인 | P `README.md` |
| 필수 검사와 병합 권한 | P `docs/project-rules.md` |
| 사람의 권한과 위임 | P `docs/authority.md` |
| 과거 결정 | 항목 Records. 현재 규칙을 덮어쓰지 않음 |
| SDD 작업 근거 | 사용 단계 전에 위치 결정. `sdd-workflow.md` 참조 |

충돌하면 의존 작업을 멈추고 양쪽 원본을 밝힙니다. P 규칙을 임의로 완화하지 않습니다.
사람이 읽는 산출물은 한국어로 작성하되 식별자와 도구 출력은 유지합니다.
해당 조건에서 W `process/agent-instruction-policy.md`를 읽습니다.
항목에 도구나 리뷰어가 언급되었다고 설치/호출 권한이 생기지는 않습니다.
'''),
        "build": choose(lang, '''# Build and verification

P `docs/architecture.md` owns runtime, modules and the exact test command;
P `docs/project-rules.md` owns required checks and test lifetime. Read both.
Use that full unittest command from P on Windows; on POSIX the same arguments
with `python3` are allowed. No wrapper, JDK/candidates, build/clean command,
static analysis, instrumentation/device procedure or CI applies (see P facts).
Skip build cleanup with that reason. Keep bytecode disabled or in authorized scratch.

## Verification baseline
Every scope: run P's full test command. README link fixes additionally check the
destination. Actor: current agent; preserve command, output, candidate SHA and
acceptance mapping in the item. Missing required evidence is Unverified, never PASS.
Test mode: permanent unittest regression tests in P, as required by P `AGENTS.md`.
No temporary-test preservation policy or extra human verification gate is added.
''', '''# 빌드와 검증

실행 환경, 모듈 및 정확한 테스트 명령의 원본은 P `docs/architecture.md`,
필수 검사와 테스트 수명의 원본은 P `docs/project-rules.md`입니다. 둘 다 읽습니다.
Windows에서는 P에서 전체 unittest 명령을 실행합니다. POSIX에서는 같은 인자로
`python3`를 사용할 수 있습니다. 별도 래퍼, JDK/후보, 빌드/clean 명령, 정적 분석,
instrumentation/기기 절차, CI는 없습니다(P 사실 참조). 이 사유로 빌드 정리를 생략합니다.
바이트코드를 끄거나 승인된 임시 경로에 둡니다.

## Verification baseline
모든 범위에서 P의 전체 테스트를 실행합니다. README 링크 수정은 대상 존재도 확인합니다.
수행자는 현재 에이전트이며 항목에 명령, 출력, 후보 SHA와 인수 조건 대응을 보존합니다.
필수 근거 누락은 Unverified이며 PASS가 아닙니다.
테스트 모드는 P `AGENTS.md`에 따른 제품 내 영구 unittest 회귀 테스트입니다.
임시 테스트 보존 정책이나 추가 사람 검증 gate는 두지 않습니다.
'''),
        "execution-routing": choose(lang, '''# Execution routing

Current/manual only, under P `docs/authority.md`: no automatic model selection,
switching or delegation. No per-role model/reasoning preferences, capability table,
qualification records or impact tool are declared. Do not invent capability evidence.
P declares no model-specific ban; honor any explicit host/user deny as well.
Use the routine Trivial/Small exception in W `skills/_shared/execution-routing.md`.
Other roles need its actual host evidence/qualification and human arrangement;
stop the dependent phase if unavailable. Do not downgrade independent reviews.
Apply the full P verification baseline without impact-based reductions.
''', '''# 실행 라우팅

P `docs/authority.md`에 따라 current/manual만 사용하며 모델 자동 선택, 전환,
위임을 하지 않습니다. 역할별 모델/reasoning 선호, 능력 표, qualification 기록,
영향 분석 도구는 선언하지 않습니다. 능력 근거를 만들어내지 않습니다.
P에 모델별 금지는 없으며 호스트/사용자의 명시적 금지도 따릅니다.
통상 Trivial/Small은 W `skills/_shared/execution-routing.md`의 예외를 적용합니다.
다른 역할은 해당 절차의 실제 호스트 근거/qualification과 사람의 준비가 필요합니다.
없으면 의존 단계를 멈추며 독립 리뷰를 낮추지 않습니다.
영향 분석을 이유로 줄이지 않고 P의 전체 검증 기준을 적용합니다.
'''),
        "issue-priority": choose(lang, '''# Priority application

Stage: disposable learning demo; no production deployment. Implement only the
user-selected item, one at a time. Apply W `process/issue-priority.md` unchanged.
Pagination wrong results are a functional defect; a README broken link is a
documentation defect. Neither implies a production incident. Password storage
is a proposed capability, not evidence of an existing leak. Actual exposure or
data loss still uses common P0 conditions. Priority and execution grade differ.
Record impact evidence, not a hardcoded priority. Do not expand acceptance criteria
or raise a prerequisite's priority merely because another item depends on it.
''', '''# 우선순위 적용

단계는 운영 배포가 없는 일회성 학습 데모입니다. 사용자가 고른 항목만 하나씩 구현합니다.
W `process/issue-priority.md`를 그대로 적용합니다.
잘못된 페이지 결과는 기능 결함, README 깨진 링크는 문서 결함입니다. 운영 사고를
가정하지 않습니다. 비밀번호 저장은 제안된 기능이며 기존 유출의 근거가 아닙니다.
실제 노출이나 데이터 손실에는 공통 P0 조건이 적용됩니다. 우선순위와 실행 등급은 다릅니다.
우선순위를 고정하지 말고 영향 근거를 기록합니다. 인수 조건을 임의로 넓히거나
다른 항목의 선행 조건이라는 이유만으로 우선순위를 올리지 않습니다.
'''),
        "issue-writing-guide": choose(lang, '''# Issues and evidence

Use W `process/issue-writing-guide.md` and P `docs/project-rules.md` disclosure rules.
Reference originals: source paths/lines, synthetic inputs, commands/results, revisions,
measurements and non-reconstructable category names. Minimal necessary requirements
and settled human decisions may be summarized with source, scope and time.
Do not copy conversation logs, quotes/translations/reconstructable summaries, real
personal information, credentials or passwords into any artifact, including scratch.
Use synthetic `example.invalid` addresses. Check before writing and read back afterwards.
Correct records through the adapter; tell the human if protected content cannot be removed.
No Visual Spec repository, path, check or preview is declared. Do not create HTML
Visual Specs; use tables, short descriptions or Mermaid only when needed.
''', '''# 항목과 근거 작성

W `process/issue-writing-guide.md`와 P `docs/project-rules.md`의 공개 범위를 따릅니다.
원본을 참조합니다. 소스 경로/행, 합성 입력, 명령/결과, 리비전, 측정값과 복원 불가능한
범주명은 기록할 수 있습니다. 필요한 최소 요구사항과 확정된 사람의 결정은 출처, 범위,
시점을 붙여 요약할 수 있습니다. 대화 로그, 인용/번역/복원 가능한 요약, 실제 개인정보,
자격 증명, 비밀번호는 임시 파일을 포함한 어떤 산출물에도 복사하지 않습니다.
`example.invalid` 합성 주소를 사용합니다. 기록 전 점검하고 기록 후 다시 읽습니다.
adapter 방식으로 정정하며 보호 내용을 제거할 수 없으면 사람에게 알립니다.
Visual Spec 저장소, 경로, 검사, 미리보기는 선언하지 않습니다. HTML Visual Spec을
만들지 않으며 필요한 경우에만 표, 짧은 설명 또는 Mermaid를 사용합니다.
'''),
        "module-boundaries": choose(lang, '''# Module boundaries

Read P `docs/architecture.md` for the authoritative module list, ownership,
test ownership, dependency rules and shared-contract inventory. Read P
`docs/project-rules.md` for edit and integration boundaries. Do not duplicate
that inventory here. `catalog` and `members` are separate implementation modules;
their tests do not count as an extra implementation module for grading.
There is no project-designated shared contract or integration-only path in P.
Apply W `process/module-boundaries.md` and the highest applicable grade.
Changes to P architecture/dependencies require P authority, not this declaration.
''', '''# 모듈 경계

정식 모듈 목록, 소유권, 테스트 소유권, 의존 규칙과 공유 계약 목록은
P `docs/architecture.md`에서 읽습니다. 수정/통합 경계는 P `docs/project-rules.md`에서
읽습니다. 이 문서에 목록을 중복 보관하지 않습니다. `catalog`와 `members`는 별도 구현
모듈이며 해당 테스트는 등급 판정에서 추가 구현 모듈로 세지 않습니다.
P가 지정한 공유 계약이나 통합 전용 경로는 없습니다.
W `process/module-boundaries.md`와 적용 가능한 가장 높은 등급을 따릅니다.
P 구조/의존성 변경 권한은 이 선언이 아니라 P 권한 원본을 따릅니다.
'''),
        "sdd-workflow": choose(lang, '''# SDD application

Use selected W `process/sdd/grade.md`, `entry.md`, `issue.md` at their consuming steps.
Routine Trivial/Small uses `process/small-work.md`; no extra SDD or planning gate.
P `README.md` is the behavior document/index; `docs/architecture.md` owns structure.
Decisions persist in the item's Records. SDD working/published artifact locations
are not preselected: obtain the human's location/access decision before that phase,
reuse it later, and stop only dependent work. Never silently put SDD inside P.

| Demo change | Expected minimum grade |
| --- | --- |
| README link repair with no behavioral meaning change | Trivial |
| Pagination correction plus its regression tests, one implementation module | Small |
| Both implementation modules or a designated shared contract | Medium |
| Password hashing/storage, secrets or personal-data policy | Large |

Always apply the highest common trigger, including DB, retry/schedule and cost.
Apply the starter's grade gates without relaxing them. Human judgment/merge/delegation
authority comes from P `docs/authority.md`, and required checks from `build.md`'s P sources.
For password storage record `[HUMAN DECISION REQUIRED]` and stop dependent implementation
at P's unresolved decisions; do not manufacture choices from the example prompt.
Large AS-IS/PLAN has no additional human approval gate; actual human decisions and
qualified independent reviews remain required. No delegation is recorded in P.

| Execution profile | Value |
| --- | --- |
| review.large_mode | dual |
| review.blind_reviewer_selection | required |
| sdd.medium_artifacts | full |
| Token diagnostic mode | DISABLED |

Keep default review gates. The human must arrange required reviewers under current/manual
routing; never automatically spawn or substitute self-review. Worktree root is undeclared;
the demo uses one isolated clone/task branch. Choose a permitted root before additional
lanes. Scratch permission comes from P `docs/project-rules.md`; selected W is read-only.
Record the resolver's W commit and actual P source identities, not a legacy install lock.
''', '''# SDD 적용

사용 단계에 선택한 W `process/sdd/grade.md`, `entry.md`, `issue.md`를 읽습니다.
통상 Trivial/Small은 `process/small-work.md`를 사용하며 SDD나 계획 gate를 추가하지 않습니다.
P `README.md`는 동작 문서/색인, `docs/architecture.md`는 구조 원본입니다.
결정은 항목 Records에 보존합니다. SDD 작업/게시 산출물 위치는 미지정입니다.
해당 단계 전에 사람의 위치/접근 결정을 받고 재사용하며 의존 작업만 멈춥니다.
P 안에 SDD를 임의로 만들지 않습니다.

| 데모 변경 | 예상 최소 등급 |
| --- | --- |
| 동작 의미를 바꾸지 않는 README 링크 수정 | Trivial |
| 하나의 구현 모듈에서 페이지 오류와 회귀 테스트 수정 | Small |
| 두 구현 모듈 또는 지정된 공유 계약 변경 | Medium |
| 비밀번호 해싱/저장, 비밀정보나 개인정보 정책 변경 | Large |

DB, 재시도/일정, 비용을 포함한 공통 조건 중 가장 높은 등급을 적용합니다.
starter의 등급별 gate를 완화하지 않습니다. 사람의 판단/병합/위임 권한은
P `docs/authority.md`, 필수 검사는 `build.md`가 참조하는 P 원본을 따릅니다.
비밀번호 저장은 `[HUMAN DECISION REQUIRED]`를 기록하고 P의 미결정 사항에 의존하는
구현을 멈춥니다. 예제 요청으로부터 결정을 만들어내지 않습니다.
Large AS-IS/PLAN에 별도 사람 승인 gate를 추가하지 않습니다. 실제 사람의 결정과
적격 독립 리뷰는 유지합니다. P에 기록된 위임은 없습니다.

| 실행 프로필 | 값 |
| --- | --- |
| review.large_mode | dual |
| review.blind_reviewer_selection | required |
| sdd.medium_artifacts | full |
| Token diagnostic mode | DISABLED |

기본 리뷰 gate를 유지합니다. current/manual 경로에서 필요한 리뷰어는 사람이 준비하며
자동 호출이나 자체 리뷰 대체를 하지 않습니다. worktree 루트는 미지정이며 데모는
하나의 격리된 clone/작업 브랜치를 사용합니다. 추가 lane 전에 허용된 루트를 정합니다.
임시 경로 권한은 P `docs/project-rules.md`를 따릅니다. 선택한 W는 읽기 전용입니다.
legacy 설치 lock 대신 resolver의 W 커밋과 실제 읽은 P 원본의 식별값을 기록합니다.
'''),
        "skill-evals": choose(lang, '''# Skill evaluations

Use W `process/skill-evals.md` when evaluating a workflow change. Project incident
case storage and static check command are not declared: record static checks as
not run, never PASS. Choose an authorized case location before creating incident
cases, and reference the original item record. No incident cases are pre-created.
Copied W cases are project-owned; edit only in a separate W change with deliberate
expectations, never mid-task to obtain PASS. No legacy `install.py check-evals` applies.
This does not waive P tests or any required review.
''', '''# Skill 평가

워크플로 변경 평가에는 W `process/skill-evals.md`를 적용합니다.
프로젝트 incident case 위치와 정적 검사 명령은 미지정입니다. 정적 검사는
미실행으로 기록하며 PASS로 쓰지 않습니다. incident case 생성 전에 허용된 위치를
정하고 원래 항목 기록을 참조합니다. 미리 만드는 incident case는 없습니다.
복사한 W case는 프로젝트 소유입니다. 기대값은 별도 W 변경으로 신중히 바꾸며
작업 중 PASS를 얻으려고 바꾸지 않습니다. legacy `install.py check-evals`는 적용하지 않습니다.
P 테스트나 필수 리뷰를 면제하지 않습니다.
'''),
        "tracker": choose(lang, f'''# Work tracking

- Method: `local-docs`; read W `tracker/local-docs.md` before operations.
- tracker_root: `{records}` (outside both checkouts).
- ID source: `generated`; format `TRY-<number>`, maximum in items + 1 (start at 1).
  Create exclusively; retry numbering on collision. Children use the same sequence.
- Allowed authors: `demo-agent`, `human`, as declared in P `docs/project-rules.md`.
- Merge method: `merge`, under P's checks and authority, not an extra grant here.
- Code remote: `origin` (effective URL `{product_origin}`); base and merge branch: `main`.
- SDD publication: P, remote `origin`, current Issue branch; record product and
  publication refs separately and confirm reviewer access to the exact remote SHA.
  Artifact paths must be chosen before the phase, per `sdd-workflow.md`.

The adapter maps Issues/PRs to items/branches; do not use GitHub or network services.
Map provisional task label `new-item` to the allocated ID in the item. Use exclusive
claims and append-only Records. Execution grades are Trivial/Small/Medium/Large;
optional Epic management items have `type: epic`, child links and no grade.
Check access and authority before edits. On failure: `BLOCKED: tracker unavailable`;
unsupported operations: `BLOCKED: tracker operation unsupported`. Do not fall back
to P. Retention, local-disk restriction, author identity limits and no-backup policy
come from P `docs/project-rules.md`. No optional index or record Git repo is created.
''', f'''# 작업 추적

- 방식: `local-docs`. 조작 전에 W `tracker/local-docs.md`를 읽습니다.
- tracker_root: `{records}` (두 checkout 바깥).
- ID 원천: `generated`. 형식 `TRY-<number>`, items의 최댓값 + 1 (처음은 1).
  배타적으로 생성하며 충돌하면 번호를 다시 확인합니다. 자식도 같은 순번을 사용합니다.
- 허용 작성자: P `docs/project-rules.md`의 `demo-agent`, `human`.
- 병합 방식: `merge`. P의 검사와 권한을 따르며 이 선언이 권한을 추가하지 않습니다.
- 코드 remote: `origin` (실효 URL `{product_origin}`). 기준/병합 브랜치: `main`.
- SDD 게시: P, remote `origin`, 현재 Issue 브랜치. 제품/게시 참조는 구분해 기록하고
  리뷰어가 정확한 remote SHA를 읽을 수 있는지 확인합니다.
  산출물 경로는 `sdd-workflow.md`에 따라 사용 단계 전에 결정합니다.

adapter가 Issue/PR을 항목/브랜치로 매핑합니다. GitHub나 네트워크 서비스를 사용하지 않습니다.
임시 task label `new-item`과 발급된 ID의 대응을 항목에 기록합니다.
배타 claim과 append-only Records를 사용합니다. 실행 등급은 Trivial/Small/Medium/Large이며
선택적 Epic 관리 항목은 `type: epic`, 자식 링크를 가지며 등급은 없습니다.
수정 전에 접근/권한을 확인합니다. 실패하면 `BLOCKED: tracker unavailable`,
미지원 조작이면 `BLOCKED: tracker operation unsupported`로 멈추며 P로 우회하지 않습니다.
보존 책임, 로컬 디스크 제한, 작성자 식별 한계와 백업 없음은 P `docs/project-rules.md`를
따릅니다. 선택적인 색인이나 기록 Git 저장소는 만들지 않습니다.
'''),
    }
    return {role + ".md": docs[role] for role in ROLES}


def resolver_args(target):
    # -I ignores PYTHONIOENCODING; explicit UTF-8 also preserves non-ASCII paths
    # in captured resolver JSON on Windows systems with a legacy code page.
    return [sys.executable, "-I", "-B", "-X", "utf8", str(RESOLVER), "--selected", "--fresh-session",
            "--project-root", str(target / "product"), "--area", "default",
            "--task", "new-item", "--config", str(target / "user-config/agentics.json")]


def shell_command(args):
    if os.name == "nt":
        return "& " + " ".join("'" + str(arg).replace("'", "''") + "'" for arg in args)
    return " ".join(shlex.quote(str(arg)) for arg in args)


def start_here(lang, target):
    product = (target / "product").as_posix()
    root = target.as_posix()
    tree = """adaptive-sdd-try/  (your chosen TARGET)
  product/                 P: Python library, main -> local origin
  team-workflow/           W: selected, committed workflow
  remotes/product.git      local bare code remote
  remotes/team-workflow.git
  records/items/           local-docs work items
  records/claims/          exclusive claims
  user-config/agentics.json
  START-HERE.md
"""
    if lang == "ko":
        tree = tree.replace("your chosen TARGET", "선택한 TARGET").replace(
            "P: Python library, main -> local origin", "P: Python 라이브러리, main -> 로컬 origin").replace(
            "W: selected, committed workflow", "W: 선택한 커밋된 워크플로").replace(
            "local bare code remote", "로컬 bare 코드 remote").replace(
            "local-docs work items", "local-docs 작업 항목").replace("exclusive claims", "배타 claim")
    opening = choose(lang, """# Try Adaptive Agentic SDD

Your disposable product, workflow and local remotes are ready. Setup used no network.
Product tests passed and the real resolver returned READY. Keep the original checkout
available: the prompt below uses its resolver. Use a local disk, not a sync folder.

```text
""", """# Adaptive Agentic SDD 체험하기

실험용 제품, 워크플로와 로컬 remote가 준비됐습니다. 설정 과정은 네트워크를 쓰지 않았고,
제품 테스트와 실제 resolver의 READY 확인을 마쳤습니다. 아래 요청에서 원본 checkout의
resolver를 사용하므로 원본 폴더를 유지하세요. 동기화 폴더가 아닌 로컬 디스크를 사용하세요.

```text
""")
    cd = ("Set-Location -LiteralPath '" + product.replace("'", "''") + "'"
          if os.name == "nt" else "cd " + shlex.quote(product))
    checkout = CHECKOUT.as_posix()
    launch = cd + "\n" + shell_command(["claude", "--add-dir", root, "--add-dir", checkout])
    # Codex can read outside its writable roots, so only the sandbox root is made writable.
    codex = cd + "\n" + shell_command(["codex", "--add-dir", root])
    prompt = choose(lang, f'''I select workflow try-team for one new task in a fresh session.
Product: {product}
Sandbox root: {root}
Representative area: default. Task label: new-item.
Run this reviewed resolver command:
{shell_command(resolver_args(target))}
Stop unless it exits 0 with state READY. Read the resolved entry, task guard,
profile, referenced P originals and applicable project docs. Verify records access
and P authority before edits. Do not edit the workflow (W).
Do the work yourself in this session: no model switching and no delegation to
other agents (the current/manual route). If the task is Trivial or Small, follow the
short procedure (compact route) through a verified local merge and close.
Write only inside the sandbox paths P declares; say so if the host does not enforce them.
My task is: [replace this line with ONE example below]
''', f'''새 세션에서 하나의 새 작업에 워크플로 try-team을 선택합니다.
제품: {product}
샌드박스 루트: {root}
대표 area: default. Task label: new-item.
검토한 다음 resolver 명령을 실행하세요.
{shell_command(resolver_args(target))}
종료 코드 0과 state READY가 아니면 멈추세요. 해결된 entry, task guard, profile,
참조된 P 원본과 해당 project 문서를 읽으세요. 수정 전에 기록 접근과 P 권한을 확인하세요.
워크플로(W)는 수정하지 마세요.
이 세션에서 직접 작업하세요. 모델을 바꾸거나 다른 Agent에게 맡기지 마세요(current/manual 경로).
Trivial이나 Small이면 짧은 절차(compact route)를 따라 로컬 병합과 종료까지 검증하세요.
P가 정한 샌드박스 경로 안에만 쓰고, 호스트가 이를 강제하지 않으면 그렇다고 알려 주세요.
작업: [이 줄을 아래 예제 중 하나로 바꾸세요]
''')
    return opening + tree + "```\n\n" + choose(lang, f'''Open a **fresh session in `product/`**, with access to `{root}`.
For Claude Code:

```{'powershell' if os.name == 'nt' else 'sh'}
{launch}
```

For Codex:

```{'powershell' if os.name == 'nt' else 'sh'}
{codex}
```

Claude Code's `--add-dir` grants access to the sandbox root and this checkout (for the
resolver). Codex's `--add-dir` makes the sandbox root writable; Codex can already read
this checkout. If your Codex version lacks the flag, check `codex --help`. This folder
layout and READY do not enforce an OS sandbox; verify host permissions.

**Allow Git inside the sandbox.** To finish the Trivial or Small task, the agent runs
`git commit`, `git merge` and `git push` to the local remotes in `remotes/` (no network).
If your agent asks for permission, allow these commands; otherwise the task stops before merge.
Setup takes about a minute; one task usually takes a few minutes of agent time.

Paste this selection prompt, replacing its last line with one task. In short, it tells the
agent to confirm the workflow is READY, read the rules, do the work itself, and finish
small tasks with a local merge:

```text
{prompt}```

Choose one (start a fresh session for each):

- **Trivial:** Fix the broken architecture link in README.md without changing behavior.
- **Small:** Fix catalog.search.page so page([1, 2, 3, 4], 1, 3) returns [1, 2, 3].
  Add regression tests; keep the change within catalog and its tests.
- **Large:** Add password hashing and storage to members.
  Watch for the security/personal-data escalation: the agent should grade it Large and
  stop at the human decisions instead of building a finished feature.

Grades are expected outcomes, not overrides of the actual scope/risk rules. Records
stay in `records/`. The human owns retention; there is no backup. Nothing is published online.
''', f'''`{root}`에 접근할 수 있도록 **`product/`에서 새 세션**을 여세요.
Claude Code 예시:

```{'powershell' if os.name == 'nt' else 'sh'}
{launch}
```

Codex 예시:

```{'powershell' if os.name == 'nt' else 'sh'}
{codex}
```

Claude Code의 `--add-dir`은 샌드박스 루트와 resolver가 있는 이 checkout에 접근하게 합니다.
Codex의 `--add-dir`은 샌드박스 루트를 쓰기 가능하게 하며, 이 checkout은 원래 읽을 수 있습니다.
설치한 Codex에 이 옵션이 없으면 `codex --help`를 확인하세요. 폴더 구조와 READY만으로
OS 샌드박스가 강제되지는 않으므로 호스트 권한을 확인하세요.

**샌드박스 안의 Git 명령을 허용하세요.** Trivial이나 Small 작업을 끝내려면 Agent가
`git commit`, `git merge`, `git push`를 `remotes/`의 로컬 원격에 실행합니다(네트워크 없음).
Agent가 권한을 물으면 허용하세요. 허용하지 않으면 병합 전에 멈춥니다.
설정은 1분 정도, 작업 하나는 보통 Agent 시간으로 몇 분 걸립니다.

마지막 줄을 하나의 작업으로 바꾸고 다음 선택 요청을 붙여 넣으세요. 요약하면 워크플로가
READY인지 확인하고, 규칙을 읽고, 직접 작업하고, 작은 작업은 로컬 병합까지 끝내라는 요청입니다.

```text
{prompt}```

하나를 골라 보세요. 각 작업은 새 세션에서 시작합니다.

- **Trivial:** README.md의 깨진 구조 문서 링크를 동작 변경 없이 고쳐 주세요.
- **Small:** catalog.search.page를 고쳐 page([1, 2, 3, 4], 1, 3)이 [1, 2, 3]을
  반환하게 해 주세요. 회귀 테스트를 추가하고 catalog와 해당 테스트로 범위를 제한하세요.
- **Large:** members에 비밀번호 해싱과 저장을 추가해 주세요.
  보안/개인정보 등급 상승을 보는 예제입니다. 에이전트가 Large로 판정하고 기능을 완성하는
  대신 사람의 결정 지점에서 멈추는지 확인해 보세요.

예상 등급은 실제 범위/위험 규칙을 덮어쓰지 않습니다. 기록은 `records/`에 남습니다.
보존 책임은 사용자에게 있고 백업은 없습니다. 온라인으로 게시되는 것은 없습니다.
''')


def validate_target(requested):
    if os.path.lexists(str(requested)):
        raise SetupError("TARGET already exists; refusing to overwrite: " + str(requested))
    target = requested.resolve()
    if target == CHECKOUT or CHECKOUT in target.parents:
        raise SetupError("TARGET must be outside this repository checkout: " + str(target))
    if os.path.lexists(str(target)):
        raise SetupError("TARGET already exists; refusing to overwrite: " + str(target))
    if not target.parent.is_dir():
        raise SetupError("TARGET parent must already exist (nothing created): " + str(target.parent))
    return target


def init_repo(root, bare=False):
    # No template hooks, global defaults, signing, or alternate object format.
    args = ["init", "--quiet", "--template=", "--object-format=sha1", "--initial-branch=main"]
    if bare:
        args.append("--bare")
    git(root, *args)
    metadata = root if bare else root / ".git"
    # A real empty file works with Git for Windows' system core.fscache setting;
    # the Windows NUL device is not accepted as an excludes file in that mode.
    write(metadata, "info/demo-excludes", "")
    settings = {"user.name": "Adaptive SDD Demo", "user.email": "demo@example.invalid",
                "core.autocrlf": "false", "commit.gpgsign": "false",
                "tag.gpgsign": "false", "core.fsmonitor": "false", "core.longpaths": "true",
                "core.hooksPath": str(root / ("hooks-disabled" if bare else ".git/hooks-disabled")),
                "core.excludesFile": str(metadata / "info/demo-excludes")}
    for key, value in settings.items():
        git(root, "config", "--local", key, value)


def commit_and_push(root):
    git(root, "add", "--all")
    git(root, "commit", "--quiet", "-m", "Create disposable Adaptive SDD demo")
    git(root, "push", "--quiet", "--set-upstream", "origin", "main")
    return git(root, "rev-parse", "HEAD")


def setup(target, lang):
    starter = CHECKOUT / ("ko/adaptive-sdd" if lang == "ko" else "adaptive-sdd")
    version = run(["git", "--version"], isolated_git=True)
    match = re.search(r"\b(\d+)\.(\d+)(?:\.(\d+))?", version)
    if not match or tuple(int(x or 0) for x in match.groups()) < (2, 36, 0):
        raise SetupError("Git 2.36+ is required; found " + version)
    for name in ("workflow", "methodology", "LICENSE"):
        source = starter / name
        if not source.exists():
            raise SetupError("Starter is missing: " + str(source))
        if source.is_symlink() or any(p.is_symlink() for p in source.rglob("*")):
            raise SetupError("Starter symlinks are unsupported: " + str(source))
    if not RESOLVER.is_file():
        raise SetupError("Resolver is missing: " + str(RESOLVER))

    # Atomic reservation: no parents=True, reuse, overwrite or cleanup on failure.
    target.mkdir()
    product, workflow = target / "product", target / "team-workflow"
    for name in ("product", "team-workflow", "remotes/product.git",
                 "remotes/team-workflow.git", "records/items", "records/claims", "user-config"):
        (target / name).mkdir(parents=True, exist_ok=True)
    for root in (product, workflow):
        remote = target / "remotes" / (root.name + ".git")
        init_repo(remote, bare=True)
        init_repo(root)
        git(root, "remote", "add", "origin", remote.as_posix())

    for name, content in product_files(lang, target).items():
        write(product, name, content)
    for name in ("workflow", "methodology"):
        shutil.copytree(str(starter / name), str(workflow / name))
    shutil.copyfile(str(starter / "LICENSE"), str(workflow / "LICENSE"))
    product_origin = git(product, "remote", "get-url", "origin", effective=True)
    for name, content in project_docs(lang, target, product_origin).items():
        write(workflow / "project", name, content)
    write_json(workflow, "profile.json", {
        "schema": 1, "methodology": "try-team", "version": "try-1",
        "entry": "workflow/activation.md",
        "paths": {"workflow": "workflow", "supports": "methodology"},
        "product_sources": [{"path": path, "revision": "task-start", "kind": kind}
                            for path, kind in (("docs/architecture.md", "fact"),
                                               ("docs/project-rules.md", "approved-rule"),
                                               ("docs/authority.md", "authority"),
                                               ("AGENTS.md", "approved-rule"),
                                               ("README.md", "fact"))],
        "records": {"location": "local-docs: " + (target / "records").as_posix(),
                    "retention_owner": "human user",
                    "revision_relation": "Record P baseline/final SHA, actual source content read and selected W commit in each item",
                    "access_failure": "stop-dependent-work"},
    })
    sha = commit_and_push(workflow)
    write(product, ".agentics/default.yaml",
          "methodology: try-team\nversion: try-1\ncommit: " + sha + "\n")
    commit_and_push(product)
    write_json(target, "user-config/agentics.json", {
        "schema": 1, "sources": {"try-team": {"root": str(workflow),
            "origin": git(workflow, "remote", "get-url", "origin", effective=True)}}})
    write(target, "START-HERE.md", start_here(lang, target))

    # -B avoids cache writes; do not use -I for unittest because P must be importable.
    run([sys.executable, "-B", "-m", "unittest", "discover", "-s", "tests", "-t", "."], cwd=product)
    output = run(resolver_args(target))
    try:
        ready = json.loads(output).get("state") == "READY"
    except (ValueError, AttributeError):
        ready = False
    if not ready:
        raise SetupError("Resolver did not return READY:\n" + output)
    print(choose(lang, "Product tests passed. Resolver: READY.", "제품 테스트 통과. Resolver: READY."))
    print(choose(lang, "Ready — open ", "준비 완료 — 다음 문서를 여세요: ") + str(target / "START-HERE.md"))


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("target", nargs="?", default="adaptive-sdd-try", metavar="TARGET")
    parser.add_argument("--lang", choices=("en", "ko"), default="en")
    args = parser.parse_args(argv)
    target = None
    try:
        target = validate_target(Path(args.target).expanduser())
        setup(target, args.lang)
    except (SetupError, OSError, ValueError, RuntimeError) as error:
        print("Setup failed: " + str(error), file=sys.stderr)
        if target is not None and target.exists():
            print("TARGET was left in place for inspection; nothing was deleted: " + str(target), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
    sys.exit(main())
