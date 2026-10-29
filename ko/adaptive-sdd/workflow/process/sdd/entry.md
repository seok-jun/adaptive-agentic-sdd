# SDD entry

현재 Issue 계약·사람 판단·미결 의존성은 [issue](issue.md), grade 판정은 [grade](grade.md)를 함께 적용한다. 이미 확인한 동일 버전은 다시 읽지 않는다.

## 공통 계약과 프로젝트 적용

아래 공통 단계·리뷰·검증 계약의 원본은 W다. 프로젝트가 선언한 적용 등급/프로필·사람 권한·실제 경로와 최소 검증 명령을 함께 읽는다. 원본 이관만으로 프로젝트의 기존 gate를 늘리거나 줄이지 않는다. `P`는 현재 프로젝트, `W`는 검증한 방법론이며 이 문서의 프로젝트 경로는 P 적용 문서가 선언한 실제 경로에 대응한다. 일반 실행 순서와 형식은 아래 계약을 사용한다.

## 구현 시작 조건

읽기 전용 조사에는 수정 claim이나 새 branch/worktree를 선행 요구하지 않는다. 같은 파일을 조사하는 것은 수정 경로 충돌이 아니다. 조사 자체의 접근 권한·사용자 지시·확정된 선행 조건을 확인하고 조사 기준 revision을 남긴다.

실행 Issue의 P 저장소 작업 파일을 처음 생성·수정·삭제하기 전에는 [parallel-development](../../skills/parallel-development/SKILL.md#읽기-전용-조사와-수정-진입)의 lane·claim을 확보한다. SDD·테스트·제품 코드도 포함한다. 현재 단계의 조건을 적용하므로 SDD 작성 claim에 아직 작성하지 않은 AS-IS/PLAN의 리뷰 PASS를 요구하지 않는다. tracker의 관리 기록과 Epic 관리 문서 자체는 기존 예외를 유지한다. 제품 구현에 진입할 때는 아래 조건과 해당 grade gate를 별도로 충족한다.

Trivial/Small/Medium Issue는 다음 조건을 모두 만족하면 구현을 시작할 수 있다.

- 현재 작업 지시가 해당 Issue 구현을 요청한다.
- 필수 본문 항목과 Priority/grade 라벨이 모두 존재하고 서로 일치한다.
- `status:blocked`가 없다.
- 다른 활성 lane의 `[CLAIM]` 또는 PR과 수정 허용 경로가 겹치지 않는다.
- 현재 lane이 `W/skills/parallel-development/SKILL.md`의 claim 절차를 완료했다.

조건 하나라도 충족하지 않으면 코드를 수정하지 않는다.

## grade별 산출물과 게이트

| grade | SDD 문서 | 구현 전 게이트 |
| --- | --- | --- |
| Trivial | 없음 | 범위가 Trivial 조건을 만족하는지 확인 후 진행 |
| Small | 없음 | 구현 시작 조건만 충족하면 진행 |
| Medium | 필요 | SDD 작성 후 구현까지 중간 승인 없이 진행 |
| Large | 필요 | AS-IS → required review → PLAN → required review → 구현. 사람 승인 단계 없음 |

### Trivial

별도 `docs/sdd/**` 디렉터리를 만들지 않는다. Issue 본문 또는 현재 사용자 지시가 작업 범위 역할을 하며, 대상 파일과 직접 검증 근거만 확인한다.

- repository-wide discovery를 하지 않는다.
- independent review는 요구하지 않는다.
- 변경 종류에 맞는 targeted validation과 최종 diff self-review는 생략하지 않는다.
- 빌드 도구 검증(P가 선언한 build/test 명령)은 변경이 그 결과에 영향을 주는 근거가 있을 때만 실행한다.
- 작업 중 Trivial 조건을 벗어나는 변경이 필요해지면 수정 전에 최소 Small로 재판정한다.

### Small

Issue 본문이 change plan 역할을 한다. 별도 `docs/sdd/**` 디렉터리를 만들지 않는다.

### Medium

`docs/sdd/{feature}/`를 작성한 뒤 구현을 계속한다. 별도의 중간 사용자 확인을 기다리지 않는다. 단, SDD를 작성하는 과정에서 Issue 목표·범위·경계가 서로 충돌하는 것을 발견하면 구현하지 않고 `BLOCKED`로 보고한다.

### Large

`README.md`·`01-as-is.md` → AS-IS required review → `02-to-be.md`·`change-plans/**` → PLAN required review → 구현으로 진행한다. [설계 리뷰](../design-review.md)의 원격 후보 게시·A/B 독립성·current-target 진행 조건을 적용한다. 구현 뒤 grade별 code review와 검증을 수행하고 Large 병합은 기존 사람 판단 규칙을 따른다.

## 기존 분석 재사용

하위 Issue의 AS-IS는 상위·관련 작업의 분석 원문과 기준 코드 revision, 적용 범위·전제, 근거를 먼저 확인한다. 현재 변경에도 유효한 사실은 참조하고 부족하거나 달라진 부분만 보완한다. phase나 문서 이름이 다르다는 이유로 같은 조사를 반복하지 않는다. 분석 재사용은 하위 Issue의 해당 grade 검토를 자동 면제하거나, 과거 검증·PASS를 새 target의 결과로 승계한다는 뜻이 아니다.

## Verification Strategy

완료 기준과 검증 수단의 대응, grade별 review, targeted·최종 검증 및 PASS 재사용은 [검증 계약](../verification.md)을 따른다. 실제 명령과 프로젝트의 필수 검증은 P의 `build.md`·Issue가 정한다.

## Grade별 review gate

[등급별 review gate](../verification.md#grade별-review-gate)가 원본이다. Large 설계 리뷰 순서와 재검토는 [설계 리뷰](../design-review.md)에 둔다. Epic 생성·분해에 이 실행 검증을 누적하지 않는다.

## SDD 작업 문서 구조

Medium·Large의 문서 구조와 Human Decision·Agent Execution Spec의 역할은 [SDD 작업 문서](../sdd-artifacts.md)를 따른다. Trivial·Small에는 별도 SDD를 만들지 않는다.

## 실행 routing과 packet

grade는 orchestration shape를 결정하고 phase risk·decision complexity는 model/reasoning tier를 결정한다.

- Trivial·Small은 current agent 한 명이 model switch/delegation 없이 끝낸다. current concrete model이 role DENIED이면 actor 수를 늘리지 않고 qualified replacement 한 명으로 교체한다.
- Medium은 단일 agent가 기본이며 unresolved PLAN decision 또는 required independent review phase만 bounded delegation한다.
- Large는 root/orchestrator가 검토를 통과한 설계와 경계를 소유하고 `PLAN / IMPLEMENT / REVIEW` phase routing을 사용할 수 있다.
- Epic의 실제 작업은 각 실행 Issue의 grade를 따르며 Epic 소속만으로 delegation·병렬 실행을 요구하지 않는다.

model capability·qualification·fallback은 [execution-routing](../../skills/_shared/execution-routing.md), derived cache의 필드·guard provenance·freshness·결과 소비는 [execution-packets](../../skills/_shared/execution-packets.md)가 원본이다. 해당 선택·전달 시점에 읽으며 모든 작업의 고정 선행 입력으로 추가하지 않는다.

### PLAN 확정 뒤 구현 문맥 인계

Large PLAN → IMPLEMENT는 [구현 진입의 문맥·최신성 확인](../../skills/_shared/execution-packets.md#구현-진입의-문맥최신성-확인)을 따른다. 검토한 결정·직접 계약·남은 finding·검증 의무를 전달하고 첫 edit 전에 현재 근거를 확인한다.

## 차세대 방법론의 적용과 개선 관측

모든 실행 grade의 시작·인계·SUMMARY·종료 기록은 [적용·개선 관측](../observations.md)을 따른다. 실제 문제 발견 시 사건을 연결하고, SUMMARY 작성 시 작성 모델을 남긴다. 관측 공백은 제품 완료의 새 gate가 아니다.

## 안정화 기간 token diagnostic

P의 mode가 `ENABLED`일 때만 [token-diagnostic](../token-diagnostic.md)의 START/BLOCKED/RESUME/END를 적용한다. tracker 부재로 생략하는 범위는 token checkpoint이며 일반 관측을 함께 생략하지 않는다.

## 병렬 작업

claim/release, branch/worktree, cloud sandbox의 실행 절차는 `W/skills/parallel-development/SKILL.md`가 canonical owner다. 모듈 ownership, shared/root integration 경계는 `S/.adaptive-sdd/project/module-boundaries.md`가 Source of Truth다.
