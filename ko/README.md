# Adaptive Agentic SDD — 1.0 preview.5

[English](../README.md) | **한국어**

> **Preview.** 이 릴리스는 `v1-preview` 브랜치의 `v1.0.0-preview.5`입니다. 같은 릴리스 태그의 파일과 안내를 사용합니다. 효과는 측정하지 않았고, 1.0 전에 구조가 바뀔 수 있습니다. v0.2 방법론(영문)은 `main`과 태그 [`v0.2.0`](https://github.com/seok-jun/adaptive-agentic-sdd/tree/v0.2.0)에 그대로 있습니다. 한국어판 v0.2는 더 이상 제공하지 않습니다.

preview.5에는 다음이 들어 있다.

- **실행 프로필 설정 3개** — `review.large_mode`(Large 설계 리뷰를 이중/1회로), `review.blind_reviewer_selection`(Review B 모델을 사람이 꼭 고를지), `sdd.medium_artifacts`(Medium SDD를 네 문서/한 장으로). 기본값은 이전 동작과 같고, M의 사람 판단 요건·등급 자동 격상·필수 검증·CODE Review·Large 병합의 사람 판단은 줄이지 않는다.
- **용어집**(`adaptive-sdd/workflow/glossary.md`)과 **Skill 4개의 쉬운 말 다듬기**. 규칙의 의미·순서·멈춤 조건은 바꾸지 않았다.
- **영문 전체판** — 저장소 최상위 `adaptive-sdd/`. 설치 도구는 두 판이 바이트까지 같고, 판별 문구는 각 번들의 `templates/strings.json`에 있다.
- **첫 행동 평가 실행 기록** — `docs/eval-results/2026-10-30/`. 아래 검증 범위를 본다.

## 무엇인가

이 판의 파일은 저장소의 `ko/` 아래에 있습니다. 영문 원본은 저장소 최상위에 있으며, 두 판의 뜻이 다르면 영문이 기준입니다.

프로젝트가 복사해 고정하고, 프로젝트에 맞게 생성해 쓰는 공통 계층입니다. `adaptive-sdd/`가 고정 사본 전체입니다.

- `adaptive-sdd/methodology/` — 공통 원칙. `core.md`(최소 작업 흐름, 사람 판단 요건, 작업 기록과 관측), `adaptation.md`(관찰 근거로 지원을 고르고 다시 평가하는 규칙), `supports/ordered-changes.md`(기본 지원), `manifest.json`.
- `adaptive-sdd/workflow/` — 실행 절차와 Skill 4개(작업 정리·생성, 작업 격리, 설계와 구현, 검증과 종료), [용어집](adaptive-sdd/workflow/glossary.md), eval 체계(정적 검사, 행동 사례, 도구 간 비교, 채점과 결과 기록, 가상 대표·정책 회귀 사례, 사건을 진단 사례로 만드는 규칙), 작업 관리 방식 대응표(로컬 문서, GitHub). 새 정책 사례는 기대 행동과 실행 결과를 구분합니다. 한 제품에서 오래 다듬은 절차에서 제품 종속 부분만 덜어내 옮겼습니다.
- `adaptive-sdd/templates/` — 프로젝트 종속 파일의 틀과 판별 문구(`strings.json`). 설치 도구가 `project.json` 값으로 채웁니다.
- `adaptive-sdd/tools/install.py` — 설치 도구(Python 3.8 이상, 표준 라이브러리만). P 적용 문서, Claude Code·Codex용 Skill 입구, `AGENTS.md`·`CLAUDE.md`·`.gitattributes`의 표시 구간을 생성하고, 고정 사본과 생성물을 해시로 확인합니다. 다른 판이 쓴 표시 구간도 알아봅니다.
- `adaptive-sdd/MANIFEST.json` — 고정 사본 전체 파일의 sha256.
- `docs/customization.md` — 사본을 두고, 프로젝트 값을 채우고, Agent에게 일을 시키는 방법.

개선 방식: 종료 기록 → `adaptation.md`에 따른 재검토 → 사건 사례 → 사람이 범위를 정한 비교 → 사람의 채택과 결정 기록.

preview.5부터 실행 절차·Skill·eval·템플릿의 영문판(저장소 최상위 `adaptive-sdd/`)이 있으며 영문이 원본입니다. 두 판은 같은 파일 구성·제목 구조·사례 ID를 갖고, 시험이 이를 대조합니다.

W 정책은 실행 등급을 Trivial·Small·Medium·Large 네 개로 구분합니다. Epic은 개별 추적이 필요한 Issue를 묶는 선택적 관리 단위이며 분해 전용 리뷰 gate를 두지 않습니다. 단일 Large 수행도 허용하고 공통 변경 검증·사람 판단 경계·전체 완료 근거는 유지합니다. 자세한 정책은 [Epic 관리 단위](adaptive-sdd/workflow/process/sdd/epic.md#epic-관리-단위)를 따릅니다.

## 무엇이 아닌가

- **v0.2의 대체물이 아닙니다.** v0.2의 문서, starter, 템플릿을 옮겨 오지 않았습니다. v0.2는 `main`에 그대로 있습니다.
- **검증된 결과가 아닙니다.** 결과·재작업·비용에 대한 효과는 측정하지 않았습니다. 절차와 Skill을 한 제품에서 운영한 경험이 일반화한 이 preview의 효과를 입증하지는 않습니다. 검사와 검토의 대상 revision은 아래 범위로 한정합니다.
- **강제 장치가 아닙니다.** Agent와 사람을 위한 안내이며, 보안 경계나 Agent 실행기가 아닙니다.

## 검증 범위

- **공개된 `v1.0.0-preview.2`:** manifest 검사, 설치 도구 단위 테스트, 로컬 압축 파일과 가상 프로젝트를 사용한 Windows 설치 시운전 한 번, 독립 검토 한 번이 해당 릴리스에 기록돼 있습니다. 이후 변경의 검증 근거로 확대하지 않습니다.
- **미출시 commit `068618bdda2f8d0571da3099f5e132e4ff17ff1e`, 2026-10-27 확인:** Windows·Python 3.14.7에서 실행 테스트 25개가 모두 통과했고, 양쪽 방법론 manifest와 51개 파일의 번들 manifest가 일치했습니다. 해당 commit으로 만든 ZIP을 임시 프로젝트에 설치해 `init`, `render`, `check`, `check-evals`가 통과했습니다. Skill 4개의 사례 60개는 구조 검사를 통과했으며, 모델 행동 평가로 실행한 결과는 아닙니다.
- **통합 후보, 2026-10-30 확인:** `5a81d647771cb56fcf1f1d84e94d580f2ca2d963`에 이번 변경의 설치 안내·검증 범위·변경 이력·관측 근거·manifest 보정을 합친 범위입니다. Windows·Python 3.14.7에서 실행 테스트 35개가 모두 통과했고, 양쪽 방법론 manifest와 64개 파일의 번들 manifest가 일치했습니다. 후보 ZIP을 임시 local-docs·GitHub adapter 프로젝트에 설치해 `init`, `render`, `check`, `check-evals`가 통과했습니다. Skill 4개의 사례 70개는 구조 검사만 수행했으며, 실제 GitHub tracker 작업과 모델 행동 평가는 실행하지 않았습니다.
- **preview.5 출시 커밋(`v1.0.0-preview.5` 태그가 가리키는 커밋), 2026-10-30 확인:** Windows·Python 3.14.7에서 실행 테스트 53개가 모두 통과했습니다. 두 번들 manifest(각 66개 파일)가 실제 파일과 일치하고, 두 판 모두 임시 프로젝트에서 `init`, `render`, `check`, `check-evals`(사례 76개)가 통과했습니다. `git diff --check`도 통과했습니다. 최초 샌드박스 실행은 Windows 임시 폴더 잠금(WinError 32)과 Git/MSYS 접근 거부로 실패해, 전체 테스트를 샌드박스 밖에서 다시 실행했습니다. 이번 출시 검증에서 과거 번역 리뷰나 모델 행동 평가를 다시 수행하지는 않았습니다. 당시 근거는 변경 이력과 [평가 기록](../docs/eval-results/2026-10-30/README.md)에 있습니다.
- **알려진 한계:** 양 언어의 `verification.md`에 첫 검증 순서가 명시돼 있지만, Claude는 `II-S02`의 첫 targeted 검증을 3회 모두 놓쳤습니다. `FI-S02`는 실패한 명령명이나 실패 로그를 제공하지 않고 그 명령명을 요구하므로, 3회 누락만으로 스킬 결함을 확정할 수 없습니다. 채점을 재검토할 원답변은 없습니다. 스킬 변경과 평가 사례 보정은 후속 판으로 미루고 기존 결과는 보존합니다. 행동 개선을 주장하지 않습니다.
- **리뷰와 남은 한계:** 이전 리뷰의 범위와 시점은 [CHANGELOG.md](../CHANGELOG.md)에 기록돼 있습니다. 그 번역 리뷰를 제외하면 위 검사는 새로운 독립 리뷰가 아닙니다. 실제 POSIX 실행, 실제 원격·host 통합, 결과·재작업·비용에 대한 효과는 아직 검증하지 않았습니다.

## 시작하기

[docs/customization.md](docs/customization.md)를 읽으세요. 요약하면 다음과 같습니다.

1. 설치 가이드에 따라 검토한 commit SHA의 압축 파일을 받아 `ko/adaptive-sdd/`를 프로젝트의 `.adaptive-sdd/`로 바이트 그대로 복사합니다.
2. `install.py init`으로 `project.json`을 만들고, Agent가 초안을 쓰면 사람이 정합니다. 사람 판단 지점·위임·실행 프로필은 사람만 정합니다.
3. `install.py render`로 프로젝트 종속 파일을 생성하고 `install.py check`로 확인합니다.
4. Agent에게 Skill로 일을 시킵니다.

이 가이드는 `v1.0.0-preview.5`를 다룹니다. 태그의 전체 commit SHA를 확인하고 압축 파일과 안내를 같은 버전으로 고정하세요. `v1.0.0-preview.2`에는 여기서 설명하는 외부 설치 기능이 없습니다.

## 버전

- 공개된 최신 preview: [`v1.0.0-preview.5`](https://github.com/seok-jun/adaptive-agentic-sdd/releases/tag/v1.0.0-preview.5).
- preview 태그: `v1.0.0-preview.N`. 공개한 태그는 옮기지 않습니다. 고칠 것이 있으면 새 태그로 냅니다.
- 사본은 태그 이름만이 아니라 태그, commit SHA, manifest 해시로 고정합니다.
- 버전을 올릴 때는 사본만 바꾸고 `project.json`과 작업 기록은 그대로 둔 뒤 다시 생성합니다.

## 라이선스

[MIT](../LICENSE)
