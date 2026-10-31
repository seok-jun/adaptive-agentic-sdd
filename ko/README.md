# Adaptive Agentic SDD

**작은 변경은 짧게, 위험한 변경은 깊게.** Claude Code나 Codex로 기존 코드를 고칠 때 쓰는, 위험도에 맞춰 깊이가 달라지는 스펙 주도 개발(SDD)입니다.

[![Release](https://img.shields.io/github/v/release/seok-jun/adaptive-agentic-sdd?include_prereleases&label=release)](https://github.com/seok-jun/adaptive-agentic-sdd/releases) [![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](../LICENSE)

[English](../README.md) | **한국어**

대부분의 SDD 도구는 모든 변경에 같은 스펙 → 계획 → 작업 절차를 돌립니다. 그래서 한 줄짜리 수정에도 SDD가 워터폴처럼 느껴집니다. Adaptive SDD는 먼저 변경이 얼마나 위험한지 정하고, 그 위험에 필요한 계획·리뷰·검증만 적용합니다. 링크 수정은 자체 점검으로 끝나고, DB 마이그레이션은 분석 문서, 독립 설계 리뷰 두 번, 사람의 병합을 거칩니다.

> **Preview.** 이 릴리스는 `v1-preview` 브랜치의 `v1.0.0-preview.6`입니다. 결과·재작업·비용에 대한 효과는 측정하지 않았고, 1.0 전에 구조가 바뀔 수 있습니다. [상태와 근거](#상태와-근거)를 보세요.

이 판의 파일은 저장소의 `ko/` 아래에 있습니다. 영문판이 원본이며, 두 판의 뜻이 다르면 영문이 기준입니다.

## 깊이가 어떻게 달라지나

모든 실행 작업 항목은 네 등급 중 하나를 받습니다(작업 항목을 묶는 선택적 Epic은 등급이 없습니다). 등급은 파일 수가 아니라 위험으로 정하며, Agent는 자동 격상을 스스로 낮추지 못합니다.

| 등급 | 언제 | 설계 문서 | 구현 전 리뷰 | 변경 리뷰 |
| --- | --- | --- | --- | --- |
| **Trivial** | 실행 동작·계약·테스트·빌드·작업 흐름의 의미가 바뀌지 않음(오타, 링크, 주석) | 없음 | Trivial 조건 자체 점검 | 대상 검증 + 자체 리뷰 |
| **Small** | Trivial이 아니고, 한 모듈 안이며, 격상 조건이 없음 | 없음. 작업 항목이 곧 스펙 | 경계·검증 가능성 자체 리뷰 | 완료 기준 대비 자체 리뷰 |
| **Medium** | 두 개 이상의 모듈, 또는 프로젝트가 지정한 공유 계약 | SDD: 짧은 문서 네 개, 또는 프로젝트가 `condensed`를 고르면 한 장 | 범위를 정한 자체 리뷰. `REQUIRED`면 독립 리뷰 | `REQUIRED`면 독립 리뷰, 아니면 자체 리뷰 |
| **Large** | 보안, 개인정보, DB 스키마·마이그레이션, 백그라운드 재시도·스케줄, 과금·한도 | SDD: 문서 네 개 | AS-IS와 PLAN마다 Review A + 기본값으로 사람이 모델을 고르는 블라인드 Review B(프로젝트가 리뷰 1회로 바꾸거나 B 모델을 Agent가 고르게 할 수 있음) | 독립 코드 리뷰 1회. 사람이 병합하거나 그 병합을 명시적으로 지시 |

검증에 영향을 주는 변경 파일마다 그 파일을 소유한 모듈의 테스트를 먼저 실행하고, 근거가 있을 때만 넓힙니다. 문서만 바뀌는 Trivial은 그 변경에 맞는 대상 검증을 합니다. 필수 검사는 최종 후보에서 실행하며, 입력이 바뀌지 않은 PASS만 다시 씁니다. 정의: [등급](adaptive-sdd/workflow/process/sdd/grade.md), [리뷰 관문](adaptive-sdd/workflow/process/verification.md).

## 실제 흐름

설명을 위해 줄인 예시입니다. 실제 출력은 프로젝트 설정에 따라 다릅니다.

```text
나:    docs/setup.md의 깨진 링크를 고쳐 줘. Adaptive SDD로.
Agent: T-12를 만들었습니다. 등급: Trivial — 문서만 바뀌고 동작 변화 없음.
       T-12를 claim했습니다(허용 경로: docs/setup.md).
       링크를 고치고 대상이 열리는지 확인했습니다.
       자체 리뷰: diff가 요청 범위와 맞습니다.
       [IMPLEMENTATION SUMMARY] 기록. 병합 준비 완료, 병합 뒤 claim 해제.
```

```text
나:    payments 테이블에 환불 사유 컬럼을 추가해 줘. Adaptive SDD로.
Agent: T-31을 만들었습니다. 등급: Large — DB 스키마·마이그레이션(자동 격상).
       현재 코드와 스키마로 AS-IS 분석을 썼습니다.
       AS-IS Review A: PASS. Review B(블라인드): 리뷰 모델을 골라 주세요.
       ...
       PLAN 리뷰 통과. 허용 경로 안에서 구현했습니다.
       모듈 테스트 먼저, 최종 후보에서 필수 검사: PASS.
       독립 코드 리뷰: PASS. Large 변경은 직접 병합하거나 이 병합을 명시적으로 지시해 주셔야 해서 여기서 멈춥니다.
```

## 빠른 시작

Python 3.8 이상, Git, 그리고 Claude Code나 Codex가 필요합니다. 깨끗한 작업 트리에서 시작하세요(변경은 먼저 커밋하거나 stash).

Agent가 샌드박스 안에서 돌면 `.agents/`·`.claude/`에 쓰고 커밋할 수 있어야 합니다. Codex `workspace-write` 샌드박스에서는 `.agents/`와 `.git`이 읽기 전용이니, Codex를 `--add-dir <저장소>/.agents`로 시작하고 Git 쓰기가 거부되면 설치 커밋은 직접 하세요.

**1. 저장소 최상위에서 Agent에게 붙여 넣습니다.**

```text
이 저장소에 Adaptive Agentic SDD v1.0.0-preview.6 한국어판을 설치해 줘.
설치 안내: https://github.com/seok-jun/adaptive-agentic-sdd/blob/v1.0.0-preview.6/ko/docs/customization.md

1. 태그의 전체 commit SHA를 확인해:
   git ls-remote https://github.com/seok-jun/adaptive-agentic-sdd "refs/tags/v1.0.0-preview.6^{}"
   아무것도 출력되지 않으면 태그의 commit을 확인하지 못한 것이니 멈추고 알려 줘.
2. 그 commit의 압축 파일을 내려받아 ko/adaptive-sdd/ 폴더를 .adaptive-sdd/에 바이트 그대로 복사해.
   파일 쓰기 도구가 아니라 복사 명령을 써. 제품 코드는 고치지 마.
3. 실행해: python -I -B .adaptive-sdd/tools/install.py init --project-root .
4. 안내의 3절대로 이 저장소를 관찰한 뒤, 값마다 근거를 붙인 .adaptive-sdd/project.json 초안을 보여 줘.
   init은 예시값을 복사한다. 안내가 "사람" 또는 "사람만"으로 표시한 값은 예시값을 그대로 두지 말고 나에게 물어봐.
   아직 파일은 쓰지 마.
5. 내가 답하면 project.json을 쓰고, --source-tag v1.0.0-preview.6 --source-commit <SHA>로 render한 뒤
   check를 실행하고, local-docs를 골랐으면 tracker.root 아래에 items/와 claims/를 만들고,
   추가되거나 바뀐 파일을 모두 보여 줘.
```

영문판은 `adaptive-sdd/`와 [`docs/customization.md`](../docs/customization.md)를 씁니다.

**2. 질문에 답합니다.** 사람 판단 지점, 위임, 작업 항목을 둘 곳(`github`, 또는 저장소 밖 공유 폴더의 `local-docs`), worktree 폴더, 병합 방식, 리뷰 프로필은 사람만 정합니다. 가장 중요한 값은 변경 범위별 검증 명령(`build.verification`, 또는 수동 검증 `build.checks`)입니다. 선언된 검증 수단이 없으면 완료 기준을 증명할 수 없어 구현이 `BLOCKED`로 멈춥니다.

**3. 결과를 확인합니다.**

- `python -I -B .adaptive-sdd/tools/install.py check --project-root .`가 `OK      pinned copy, lock, and generated files match`를 출력합니다.
- `python -I -B .adaptive-sdd/tools/install.py check-evals --project-root .`가 `0 problem(s)`로 끝납니다.
- `git status`에 아래 경로만 나옵니다.

| 추가·변경 | 내용 |
| --- | --- |
| `.adaptive-sdd/` | 고정 사본, `project.json`, 생성된 프로젝트 문서, lock 파일 |
| `.claude/skills/<스킬 4개>/SKILL.md`, `.agents/skills/<스킬 4개>/SKILL.md` | Claude Code·Codex용 짧은 입구 파일(고른 도구만) |
| `AGENTS.md`, `CLAUDE.md`, `.gitattributes` | `adaptive-sdd:begin`부터 `adaptive-sdd:end`까지의 표시 구간 하나. 구간 밖의 기존 내용은 그대로 |

**되돌리기.** 커밋 전이면, 원래 있던 파일은 `git restore`로 되돌리고 `.adaptive-sdd/`, 설치기가 만든 스킬 입구 폴더, 설치기가 새로 만든 `AGENTS.md`·`CLAUDE.md`·`.gitattributes`를 지웁니다. 커밋 뒤면 설치 커밋을 revert하고, 설치를 push했다면 revert도 push합니다. 설치 뒤에 만든 브랜치에는 그 브랜치에서 revert하거나 revert가 들어간 브랜치를 그 브랜치에 병합할 때까지 설치가 남습니다. `local-docs` 작업 폴더의 기록은 저장소 밖에 있어 건드리지 않습니다.

## 첫 작업

```text
Adaptive SDD로 <한 모듈 안의 작은 변경> 작업 항목을 만들고, 구현하고, 종료해 줘.
```

작업 항목에 등급과 완료 기준이 있고, 첫 수정 전에 claim을 잡았고, 소유 모듈 테스트를 먼저 실행한 뒤 최종 후보에서 필수 검사가 통과했고, `[IMPLEMENTATION SUMMARY]`에 결정·검증·남은 위험이 남았고, 변경 요청이 작업 항목에 연결되면 병합 준비가 끝납니다. 병합은 설정한 사람이 합니다. Agent가 실제 병합을 확인하고 작업 항목을 닫고 `[PRODUCT COMPLETE]`를 기록하면 완료입니다. 실제 작업 뒤에는 [안내](docs/customization.md#3-agent에게-시키는-순서)의 개선 순서가 의견이 아니라 종료 기록으로 무엇을 바꿀지 정합니다.

## 들어 있는 것

- **스킬 4개:** `managing-issues`(작업 항목 생성·등급), `parallel-development`(claim과 격리된 worktree), `implementing-issues`(등급별 설계와 구현), `finishing-issues`(검증·종료·정리).
- **작업 관리:** GitHub Issue·PR, 또는 저장소 밖 공유 폴더의 작업 문서. 절차는 특정 도구에 묶이지 않는 용어를 쓰고, 각 [어댑터](adaptive-sdd/workflow/tracker/)가 대응시킵니다. 다른 도구용 어댑터는 아직 없습니다.
- **사람 판단 경계:** 범위 축소, 위임, Large 병합, 새 제품 결정은 Agent가 정하지 않고 멈춰서 묻습니다([core.md](adaptive-sdd/methodology/core.md)).
- **설치 도구**(Python 표준 라이브러리만): `project.json`으로 프로젝트별 파일을 만들고, 고정된 모든 파일을 해시로 확인합니다.
- **평가 도구:** 스킬마다 행동 사례, 도구 간 실행기, 기록된 사건을 시험 사례로 바꾸는 규칙([skill-evals.md](adaptive-sdd/workflow/process/skill-evals.md)).

## 상태와 근거

- **측정하지 않음:** 결과·재작업·비용에 대한 효과는 측정하지 않았습니다. 절차는 한 제품에서 다듬었고, 그것이 다른 곳에서의 효과를 증명하지는 않습니다.
- **행동 평가:** 첫 도구 간 기준선으로 한국어 사례 12개 × Claude Code·Codex × 3회를 실행했습니다(Claude Code PASS 21 / FAIL 14 / INVALID 1, Codex PASS 22 / FAIL 14) — [기록](../docs/eval-results/2026-10-30/README.md). 문구 수정 두 개를 사후 짝 비교한 결과 전체 개선은 관찰되지 않았습니다 — [기록](../docs/eval-results/2026-10-30-skill-comparison/paired-summary.md). 실패도 채점된 그대로 공개합니다. 기준선과 preview.6 작업 관리 확인에서는 평가 대상 프로젝트 안에서 정답 사례 파일을 읽을 수 있었으므로 깨끗한 근거가 아닙니다. 짝 비교에서는 그 파일을 제거했습니다.
- **이번 릴리스:** Windows·Python 3.12.2에서 실행 테스트 65개가 모두 통과했고, 두 번들 manifest(각 66개 파일)가 일치했으며, 리뷰한 후보(`277cfc5`)의 압축본이 두 판 × 두 작업 관리 방식 모두에서 `init`, `render`, `check`, `check-evals`(사례 77개)를 통과했습니다. 읽기 전용 독립 리뷰(Codex `gpt-6-astra`, high)는 출시 차단 문제를 찾지 않았고, 지적 사항은 고친 뒤 재확인했습니다. 이 README로 한 첫 사용 점검 두 번 중 Claude Code Agent는 설치, Small 작업 하나, 설치 되돌리기까지 끝냈고, Codex는 설치까지 했지만 샌드박스가 Git 쓰기를 막아 작업 단계에 가지 못했습니다. 바뀐 문구의 제한된 행동 확인은 약한 근거로 [기록](../docs/eval-results/2026-10-31-tracker-neutral/README.md)했습니다. POSIX 실행과 실제 GitHub tracker 작업은 하지 않았습니다.
- **모델 routing:** 일반 Trivial/Small 작업은 금지된 모델이 아니면 [routing 적격 규칙](adaptive-sdd/workflow/skills/_shared/execution-routing.md#두-축-routing)에 따라 현재 모델로 수행합니다. Medium 이상·독립 리뷰·위임에는 해당 모델의 관찰 근거가 필요하며 이름이나 선언만으로는 부족합니다([첫 사용 기록](../docs/eval-results/2026-10-31-first-use/README.md)).
- **보장이 아님:** Agent와 사람을 위한 안내이며, 보안 경계나 Agent 실행기가 아닙니다.

검사와 리뷰의 전체 이력은 [CHANGELOG.md](../CHANGELOG.md)에 있습니다.

## 버전

- Preview 태그는 `v1-preview` 브랜치의 `v1.0.0-preview.N`입니다. 공개한 태그는 옮기지 않고, 수정은 새 태그로 냅니다. 사본은 태그·commit SHA·manifest 해시로 고정합니다.
- 업그레이드할 때는 고정 사본만 바꾸고 `project.json`·작업 기록을 유지한 뒤 다시 render합니다([안내](docs/customization.md#버전-올리기)).
- 이전 v0.2 방법론(영문)은 `main`과 태그 [`v0.2.0`](https://github.com/seok-jun/adaptive-agentic-sdd/tree/v0.2.0)에 있습니다. v1은 v0.2에서 자동으로 업그레이드되지 않습니다.

## 라이선스

[MIT](../LICENSE)
