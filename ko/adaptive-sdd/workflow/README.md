# 실행 절차(W)

이 폴더는 Issue부터 구현·검증·종료까지의 **공통 실행 절차**다. 한 제품에서 오래 운영하며 다듬은 절차를 제품 종속 부분만 덜어내 옮겼다. 제품마다 다른 사실·경로·명령·권한은 이 폴더에 두지 않고, 설치할 때 생성하는 **P 적용 문서**에 둔다.

## 세 root

| root | 설치된 프로젝트에서의 위치 | 소유 | 고치는가 |
| --- | --- | --- | --- |
| `P` | 프로젝트 저장소 최상위 | 프로젝트 | 프로젝트 규칙대로 |
| `W` | `P/.adaptive-sdd/workflow/` | 공통(이 폴더) | 고치지 않는다. 버전을 올릴 때 통째로 바꾼다 |
| `M` | `P/.adaptive-sdd/methodology/` | 공통 원칙(`core.md`, `adaptation.md`, 지원) | 고치지 않는다 |

P 적용 문서는 `P/.adaptive-sdd/project/` 아래에 설치 도구가 `P/.adaptive-sdd/project.json`의 값으로 생성한다. W 문서가 `P/.adaptive-sdd/project/<문서>`를 가리키면 그 생성물을 읽는다. 생성물을 손으로 고치지 않는다. 값을 바꾸려면 `project.json`을 고치고 다시 생성한다.

W 문서의 `P/AGENTS.md`의 `## 항상 적용 hard guard`는 설치 도구가 `AGENTS.md`에 넣은 표시 구간 안의 절이다.

## 작업 관리 방식

W 문서의 Issue·댓글·라벨·assignee·PR·closing reference 표현은 P 적용 문서 `tracker.md`가 선언한 방식으로 바꿔 읽는다.

- [로컬 문서](tracker/local-docs.md): 저장소 밖 공유 폴더의 작업 문서와 claim 파일
- [GitHub](tracker/github.md): GitHub Issue와 PR

선언한 방식의 대응표에 없는 기능을 전제하는 절차는 실행하지 않고 멈춘다.

## 문서 위치 기본값

W 문서에 나오는 `docs/domains/**`(business 문서), `docs/sdd/{feature}/`(SDD 작업 문서), `docs/reviews/**`(결정 기록), `docs/architecture/**`(구조 문서), `docs/README.md`(문서 목차)는 기본값이다. 실제 위치는 P 적용 문서 `sdd-workflow.md`의 `문서 역할` 표를 따른다.

## 읽는 순서

1. M의 `core.md`(공통 원칙과 사람 판단 요건)
2. P 적용 문서의 hard guard와 해당 단계 적용 선언
3. 해당 단계의 W 스킬과 그 입력 조건에 해당하는 W process 절. 같은 run에서 확인한 동일 버전은 재사용하며 링크를 따라 모든 문서를 선행 로딩하지 않는다.

스킬은 `skills/<이름>/SKILL.md`에 있다.

| 단계 | 스킬 |
| --- | --- |
| 작업 정리(Issue 생성·분류) | `managing-issues` |
| 작업 격리(claim·lane) | `parallel-development` |
| 설계와 구현 | `implementing-issues` |
| 검증과 종료 | `finishing-issues` |

실행 grade는 Trivial·Small·Medium·Large다. Epic은 선택적 관리 단위이며 생성·분해·전체 완료 조율은 `managing-issues`에서 수행한다. 하위 실행 Issue는 각각의 grade를 따르고 분해 리뷰를 조사 착수 조건으로 요구하지 않는다. 정책 원본은 [Epic 관리 단위](process/sdd-workflow.md#epic-관리-단위)다.

관측 재검토 스킬(`reviewing-observations`)은 다음 preview에서 옮긴다. 그 전까지 관측 재검토는 M의 `adaptation.md` 절차를 직접 따른다.

## 상세 규칙의 원본

[sdd-workflow](process/sdd-workflow.md#현재-단계에서-읽을-규칙)는 분류·진입·Epic 관리와 현재 단계의 읽기 경로를 소유한다. 스킬은 실행 순서와 필요한 결과를 연결하며 아래 규칙을 복제하지 않는다.

| 규칙 | 원본 |
| --- | --- |
| SDD 문서의 역할과 필수 내용 | [sdd-artifacts](process/sdd-artifacts.md) |
| 완료 기준·등급별 검증·PASS 재사용·검증 환경 | [verification](process/verification.md) |
| Large 설계 리뷰·원격 후보·재검토 | [design-review](process/design-review.md) |
| model·floor·qualification·fallback | [execution-routing](skills/_shared/execution-routing.md) |
| packet 필드·guard 근거·최신성·결과 소비 | [execution-packets](skills/_shared/execution-packets.md) |
| 시작·인계·종료 관측·실제 문제의 기록 | [observations](process/observations.md) |
| 활성화한 기간의 token checkpoint | [token-diagnostic](process/token-diagnostic.md) |
| Skill 평가·합성 packet 측정 | [skill-evals](process/skill-evals.md) |

## 원본과 변경

원본은 한 제품의 절차 저장소에서 2026-10-17 기준으로 가져왔다. 제품 이력 번호를 근거로 단 규칙은 규칙만 남겼다. 기기·에뮬레이터 절차, 제품 전용 도구(영향 분석기, 관측 helper, 연결 도구), 제품 모델 이름은 옮기지 않았고, 필요한 자리는 P 적용 문서가 선언한다.
