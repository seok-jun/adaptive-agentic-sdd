# 실행 절차(W)

일반 Trivial/Small 작업은 [간결 경로](process/small-work.md)로 시작한다. 적용 조건을 확인하면 네 Skill 전체를 미리 읽지 않고 필요한 단계만 수행한다. 격상·필수 리뷰·권한 조건은 유지한다.

> 권장 외부 적용 경로: 프로젝트가 소유하고 수정하는 외부 W를 작업별로 선택한다. 먼저 [작업 선택 계약](activation.md)을 읽는다. 아래 표는 이 경로를 설명하며, 기존 `install.py` 설치 경로는 표 다음에 따로 설명한다.

이 폴더는 Issue부터 구현·검증·종료까지의 **공통 실행 절차**다. 한 제품에서 오래 운영하며 다듬은 절차를 제품 종속 부분만 덜어내 옮겼다. 제품마다 다른 사실·경로·명령·권한은 이 폴더에 두지 않고, `W/../project/`의 **프로젝트 적용 문서**와 P 원본에 둔다.

## M·W·P 구조와 경로

| root | 위치(외부 적용) | 소유 | 고치는가 |
| --- | --- | --- | --- |
| `P` | 제품 저장소 | 프로젝트 | 프로젝트 규칙대로 |
| `W` | 작업에 선택된, 프로젝트가 소유하는 워크플로 저장소의 이 `workflow/` 폴더 | 프로젝트 | 고친다. 프로젝트의 검토와 commit을 거치며, 작업은 선택한 commit을 그대로 쓴다 |
| `M` | 같은 워크플로 저장소에 채택한 지원 문서(시작본의 `methodology/`) | 프로젝트(공통 방법론에서 시작) | 고친다. 호출하는 W 규칙과 함께 바꾸거나 제거한다 |

M은 방법론, W는 실행 절차, P는 제품 사실·설정·권한이다. P, W, M의 절대 경로는 resolver가 제공한다([작업 선택 계약](activation.md)). S는 별도 계층이나 Skill 입력이 아니다.

`W/../project/`는 같은 워크플로 저장소에서 W 옆에 있는 프로젝트 적용 문서 폴더다. W 문서가 `W/../project/<문서>`를 가리키면 그 문서를 읽는다. 프로젝트의 검토를 거쳐 직접 고칠 수 있다.

W 문서의 `P/AGENTS.md`의 `## 항상 적용 hard guard`는 P의 실제 공통 지침(있을 때)과 [task-guard.md](task-guard.md)를 뜻한다. AGENTS 구간을 만들지 않는다.

**기존 `install.py` 경로.** 프로젝트가 기존 설치 도구를 명시적으로 선택했으면 W와 M은 설치 사본이다(기본 `P/.adaptive-sdd/`, 또는 `--harness-root`로 고른 위치). 고치지 않고 버전을 올릴 때 통째로 바꾼다. 설치 도구가 `W/../project.json`의 값으로 `W/../project/`를 생성하므로, 생성물을 손으로 고치지 말고 JSON을 고친 뒤 다시 생성한다. hard guard는 설치 도구가 `AGENTS.md`에 넣은 표시 구간 안의 절이다.

## 작업 관리 방식

W 문서는 특정 작업 관리 도구에 묶이지 않는 용어를 쓴다. **Issue**는 작업 항목, **댓글**은 그 작업 기록의 항목, `priority:*`·`grade:*`·`status:*`·`type:epic`은 라벨 표기로 쓴 작업 항목의 **필드 값**, **assignee**는 담당자, **PR**은 선언한 병합 대상에 대한 변경 요청, **closing reference**는 그 변경과 완료되는 Issue의 연결이다(`Closes #N`은 그 W 표기다). 각 표현을 어떻게 저장하고 쓰는지는 문법·API를 포함해 P 적용 문서 `tracker.md`가 선언한 방식이 정한다. W는 GitHub 기능을 요구하지 않는다. 각 표현은 선언한 방식으로 바꿔 읽고, 그 방식이 대응하지 않는 작업은 멈춘다.

- [로컬 문서](tracker/local-docs.md): 저장소 밖 공유 폴더의 작업 문서와 claim 파일
- [GitHub](tracker/github.md): GitHub Issue와 PR

선언한 방식의 대응표에 없는 기능을 전제하는 절차는 실행하지 않고 멈춘다.

## 문서 위치 기본값

W 문서에 나오는 `docs/domains/**`(business 문서), `docs/sdd/{feature}/`(SDD 작업 문서), `docs/reviews/**`(결정 기록), `docs/architecture/**`(구조 문서), `docs/README.md`(문서 목차)는 기본값이다. 실제 위치는 P 적용 문서 `sdd-workflow.md`의 `문서 역할` 표를 따른다.

## 읽는 순서

처음 보는 용어는 [용어집](glossary.md)에서 한 줄 설명을 찾는다. 용어집은 규칙을 더하지 않는다.

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

실행 grade는 Trivial·Small·Medium·Large다. Epic은 선택적 관리 단위이며 생성·분해·전체 완료 조율은 `managing-issues`에서 수행한다. 하위 실행 Issue는 각각의 grade를 따르고 분해 리뷰를 조사 착수 조건으로 요구하지 않는다. 정책 원본은 [Epic 관리 단위](process/sdd/epic.md#epic-관리-단위)다.

관측 재검토 스킬(`reviewing-observations`)은 후속 릴리스에서 옮긴다. 그 전까지 관측 재검토는 M의 `adaptation.md` 절차를 직접 따른다.

## 상세 규칙의 원본

[sdd-workflow](process/sdd-workflow.md#현재-단계에서-읽을-규칙)는 현재 단계의 경로만 안내한다. 분류·진입·Issue·Epic·종료 규칙의 원본은 `process/sdd/`의 담당 파일이다. 스킬은 해당 파일을 직접 연결하며 규칙을 복제하지 않는다.

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
