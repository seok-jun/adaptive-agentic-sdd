# Adaptive Agentic SDD — 1.0 preview

[English](../README.md) | **한국어**

> **Preview.** 이 branch(`v1-preview`)에는 차세대 방법론의 1.0 preview가 있습니다. 효과는 측정하지 않았고, 1.0 전에 구조가 바뀔 수 있습니다. v0.2 방법론(영문)은 `main`과 태그 [`v0.2.0`](https://github.com/seok-jun/adaptive-agentic-sdd/tree/v0.2.0)에 그대로 있습니다. 한국어판 v0.2는 더 이상 제공하지 않습니다.

## 무엇인가

이 판의 파일은 저장소의 `ko/` 아래에 있습니다. 영문 원본은 저장소 최상위에 있으며, 두 판의 뜻이 다르면 영문이 기준입니다.

프로젝트가 복사해 고정하고, 프로젝트에 맞게 생성해 쓰는 공통 계층입니다. `adaptive-sdd/`가 고정 사본 전체입니다.

- `adaptive-sdd/methodology/` — 공통 원칙. `core.md`(최소 작업 흐름, 사람 판단 요건, 작업 기록과 관측), `adaptation.md`(관찰 근거로 지원을 고르고 다시 평가하는 규칙), `supports/ordered-changes.md`(기본 지원), `manifest.json`.
- `adaptive-sdd/workflow/` — 실행 절차와 Skill 4개(작업 정리·생성, 작업 격리, 설계와 구현, 검증과 종료), eval 체계(정적 검사, 행동 사례, 도구 간 비교, 채점과 결과 기록, 가상 대표 사례 30개, 사건을 진단 사례로 만드는 규칙), 작업 관리 방식 대응표(로컬 문서, GitHub). 한 제품에서 오래 다듬은 절차에서 제품 종속 부분만 덜어내 옮겼습니다.
- `adaptive-sdd/templates/` — 프로젝트 종속 파일의 틀. 설치 도구가 `project.json` 값으로 채웁니다.
- `adaptive-sdd/tools/install.py` — 설치 도구(Python 3.8 이상, 표준 라이브러리만). P 적용 문서, Claude Code·Codex용 Skill 입구, `AGENTS.md`·`CLAUDE.md`·`.gitattributes`의 표시 구간을 생성하고, 고정 사본과 생성물을 해시로 확인합니다.
- `adaptive-sdd/MANIFEST.json` — 고정 사본 전체 파일의 sha256.
- `docs/customization.md` — 사본을 두고, 프로젝트 값을 채우고, Agent에게 일을 시키는 방법.

개선 방식: 종료 기록 → `adaptation.md`에 따른 재검토 → 사건 사례 → 사람이 범위를 정한 비교 → 사람의 채택과 결정 기록.

실행 절차·Skill·eval·설치 도구의 영문판은 아직 없고 다음 preview에서 냅니다. 그때까지 이 부분은 한국어판이 유일한 원본입니다.

## 무엇이 아닌가

- **v0.2의 대체물이 아닙니다.** v0.2의 문서, starter, 템플릿을 옮겨 오지 않았습니다. v0.2는 `main`에 그대로 있습니다.
- **검증된 결과가 아닙니다.** 결과·재작업·비용에 대한 효과는 측정하지 않았습니다. 절차와 Skill은 한 제품에서 운영됐지만, 다른 프로젝트로 옮긴 형태는 이번이 처음입니다. 이 preview에서 확인한 것은 파일 무결성(manifest 해시), 설치 도구의 단위 테스트, 공개 전에 Windows에서 로컬로 만든 압축 파일로 가상 프로젝트에 한 번 설치해 본 것, 그리고 독립 검토 한 번뿐입니다.
- **강제 장치가 아닙니다.** Agent와 사람을 위한 안내이며, 보안 경계나 Agent 실행기가 아닙니다.

## 시작하기

[docs/customization.md](docs/customization.md)를 읽으세요. 요약하면 다음과 같습니다.

1. 태그 압축 파일을 받아 `ko/adaptive-sdd/`를 프로젝트의 `.adaptive-sdd/`로 바이트 그대로 복사합니다.
2. `install.py init`으로 `project.json`을 만들고, Agent가 초안을 쓰면 사람이 정합니다. 사람 판단 지점과 위임은 사람만 정합니다.
3. `install.py render`로 프로젝트 종속 파일을 생성하고 `install.py check`로 확인합니다.
4. Agent에게 Skill로 일을 시킵니다.

## 버전

- preview 태그: `v1.0.0-preview.N`. 공개한 태그는 옮기지 않습니다. 고칠 것이 있으면 새 태그로 냅니다.
- 사본은 태그 이름만이 아니라 태그, commit SHA, manifest 해시로 고정합니다.
- 버전을 올릴 때는 사본만 바꾸고 `project.json`과 작업 기록은 그대로 둔 뒤 다시 생성합니다.

## 라이선스

[MIT](../LICENSE)
