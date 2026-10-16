# Adaptive Agentic SDD — 1.0 preview

[English](../README.md) | **한국어**

> **Preview.** 이 branch(`v1-preview`)에는 차세대 방법론의 1.0 preview가 있습니다. 효과는 측정하지 않았고, 1.0 전에 구조가 바뀔 수 있습니다. v0.2 방법론(영문)은 `main`과 태그 [`v0.2.0`](https://github.com/seok-jun/adaptive-agentic-sdd/tree/v0.2.0)에 그대로 있습니다. 한국어판 v0.2는 더 이상 제공하지 않습니다.

## 무엇인가

이 판의 파일은 저장소의 `ko/` 아래에 있습니다. 영문 원본은 저장소 최상위에 있으며, 두 판의 뜻이 다르면 영문이 기준입니다.

프로젝트가 복사해 고정하고, 자기 어댑터로 조정해 쓰는 얇은 공통 계층입니다.

- `methodology/core.md` — 최소 작업 흐름, 사람 판단 요건, 작업 기록과 관측을 남기는 방법.
- `methodology/adaptation.md` — 모델 이름이나 자신감이 아니라 관찰 근거로 지원을 고르고 다시 평가하는 규칙.
- `methodology/supports/ordered-changes.md` — 기본 지원 하나: 요구와 연결한 변경 순서 목록.
- `methodology/manifest.json` — 세 문서의 sha256. 사본을 확인할 때 씁니다.
- `docs/customization.md` — 사본을 프로젝트에 두고, 어댑터를 채우고, Agent에게 일을 시키는 방법.

## 무엇이 아닌가

- **v0.2의 대체물이 아닙니다.** 위험 등급, 리뷰 gate, starter, 템플릿이 없습니다. 공통 계층 밖의 일은 프로젝트의 몫입니다.
- **검증된 결과가 아닙니다.** 결과·재작업·비용에 대한 효과는 측정하지 않았습니다. 이 preview에서 확인한 것은 파일 무결성(manifest 해시), 그리고 공개 전에 Windows에서 로컬로 만든 압축 파일로 복사·해시 대조·줄바꿈 고정과 Agent 첫 두 프롬프트(관찰, 어댑터 초안)를 한 번 따라 해 본 것뿐입니다.
- **강제 장치가 아닙니다.** Agent와 사람을 위한 안내이며, 보안 경계나 Agent 실행기가 아닙니다.

## 시작하기

[docs/customization.md](docs/customization.md)를 읽으세요. 요약하면 다음과 같습니다.

1. 태그 압축 파일을 받아 `ko/methodology/`와 `LICENSE`를 프로젝트에 바이트 그대로 복사합니다.
2. `manifest.json`과 해시를 대조하고 태그, commit SHA, manifest 해시를 기록합니다.
3. `.gitattributes`로 줄바꿈을 고정하고, 진입 파일에 몇 줄을 더하고, 어댑터를 작성합니다.
4. Agent에게 저장소를 관찰하고 어댑터 초안을 쓰게 합니다. 사람 판단 지점은 사람이 정합니다.

## 버전

- preview 태그: `v1.0.0-preview.N`. 공개한 태그는 옮기지 않습니다. 고칠 것이 있으면 새 태그로 냅니다.
- 사본은 태그 이름만이 아니라 태그, commit SHA, manifest 해시로 고정합니다.
- 버전을 올릴 때는 사본만 바꾸고 어댑터와 작업 기록은 그대로 둡니다.

## 라이선스

[MIT](../LICENSE)
