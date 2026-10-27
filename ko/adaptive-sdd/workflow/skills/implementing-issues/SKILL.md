---
name: implementing-issues
description: 이 프로젝트의 승인된 작업 항목(Issue)을 Issue 번호나 명시한 참조로 받아 조사·설계·구현한다. 기존 Issue의 진행·구현·작업·마무리 요청에 사용하며, 현재 단계의 SDD·경계·검증 절차를 연결한다. 새 Issue만 작성할 때는 사용하지 않는다.
---

실행 입력은 절대 경로 `P`(프로젝트 저장소 최상위), `S`(설치 root, in-repo에서는 P), `W`(고정 절차 사본 `S/.adaptive-sdd/workflow`), `M`(고정 공통 원칙 `S/.adaptive-sdd/methodology`)이다. cwd나 W의 상위 디렉터리로 P/M을 추정하지 않는다. P의 hard guard와 적용 선언을 따르고, Issue·댓글·라벨·PR 표현은 `S/.adaptive-sdd/project/tracker.md`가 선언한 `W/tracker/` 방식으로 읽는다.

# Implementing Issues

## Issue dispatch

1. 명시된 Issue의 current body/labels를 먼저 읽는다. 전체 open Issue 목록부터 탐색하지 않는다.
2. Issue를 실행 기준으로 삼고 Priority·grade·단계별 의존성·allowed/forbidden·완료 기준·Visual Spec·공통 계약 참조를 유지한다. 이미 결정된 요구를 다시 탐색하거나 사용자에게 재입력시키지 않는다.
3. Epic 관리 문서이면 `managing-issues`의 `Epic 조율`로 작업 구성·의존성을 갱신하고 해당 하위 실행 Issue로 진입한다. 하위가 없으면 필요한 만큼 정의하고 조사한다. 관리 문서 자체에 구현 claim·실행 grade·AS-IS/PLAN/BREAKDOWN 리뷰를 요구하지 않는다.

## Inputs

현재 run에서 `P/AGENTS.md`의 `## 항상 적용 hard guard` 적용을 보장할 수 없으면 그 절부터 읽는다. 확인한 동일 버전은 재사용한다.

필수 입력은 current Issue, `W/process/sdd-workflow.md`의 현재 grade·진입 조건, `S/.adaptive-sdd/project/sdd-workflow.md`의 적용·권한·실제 경로다. 조사에는 Issue와 직접 연결된 business/architecture 문서, 대상 코드·직접 계약·caller/callee를 읽는다.

아래 원본은 **해당 행동을 수행할 때 필요한 절만** 읽는다. 이 목록을 선행 full-read 목록으로 사용하지 않는다.

| 행동 | 읽을 원본 |
| --- | --- |
| AS-IS·PLAN·change-plan 작성·수정 | `W/process/sdd-artifacts.md`의 해당 산출물·trade-off 절 |
| 구현 중 전제 오류·진행 중 정책 변경 | `W/process/sdd-artifacts.md`의 `계획 정정과 정책 전환` |
| Large AS-IS/PLAN 게시·리뷰·재확인 | `W/process/design-review.md`의 현재 phase와 target에 적용되는 절 |
| 검증 계획·실행·PASS 재사용·code review 판정 | `W/process/verification.md`와 P 적용 문서 `build.md`의 해당 검증 |
| 현재 role 진입·유지의 적격 확인, 모델·추론·위임·fallback 선택 | `W/skills/_shared/execution-routing.md`의 해당 role·선택 경로 |
| worker 인계·Result/Review 소비·선언된 영향 결과 사용 | `W/skills/_shared/execution-packets.md`의 해당 Packet·영향 결과 절 |
| SDD·테스트·코드 등 P 작업 파일 최초 쓰기의 claim·lane·격리 | `W/skills/parallel-development/SKILL.md`의 해당 절 |
| shared/root 경계·lifecycle artifact 판단 | W/P `module-boundaries.md`의 관련 경계 |
| 지시 충돌·code와 business의 불일치·승인 범위 해석 불가 | W/P `agent-instruction-policy.md`의 해당 충돌 절 |
| 사람용 현황·계획·변경 설명 작성 | `W/process/agent-instruction-policy.md`의 `사람용 문서의 시각적 작성` |

시작·문제 발견·중단·인계에는 `W/process/observations.md`의 해당 사건/단계 절을 적용한다. Token checkpoint는 `W/process/token-diagnostic.md`의 활성 조건과 현재 lifecycle event를 따른다. tracker unavailable은 checkpoint만 생략하는 사유이며 다른 관측을 생략하는 사유가 아니다.

## 입력 재사용과 조회

- 같은 run에서 읽은 변경 없는 Issue·정책·source·Issue/PR metadata는 재사용한다.
- review target SHA 변경, 현재 lane push에 따른 PR head 변경, Issue/PR merge·close·reopen·label/assignee/state 변경, base 변경 근거, webhook/wake·외부 tool 결과·사용자 지시의 외부 상태 변경 신호가 있으면 해당 판단에 필요한 입력만 갱신한다. merge 직전과 merge 후 closure 확인 직전에도 필요한 metadata를 재조회한다.
- 상태·라벨·mergeability·head/base SHA만 필요하면 metadata 전용/field 한정 조회를 우선한다. body·comments·diff는 그 내용이 판단 근거일 때만 읽고, metadata 조회 뒤 무조건 full-read하는 이중 호출을 만들지 않는다. metadata만으로 안전하게 판정할 수 없으면 필요한 범위를 추가로 읽는다.

## 조사와 제품 수정 진입

1. 현재 요청이 읽기 전용 조사인지 제품 수정인지 구분하고, dependencies/blockers가 필요한 단계를 확인한다. 조사 자체의 접근 권한·사람 판단 조건은 유지한다. 상위 미결 결론은 그것을 소비하는 구현·통합·배포를 기다리게 하며 조사 착수를 막지 않는다.
2. 읽기 전용 조사에는 수정 claim을 요구하지 않는다. 조사 경로의 중복 읽기는 수정 충돌이 아니다. SDD·테스트·코드 등 실행 Issue의 P 작업 파일을 처음 생성·수정·삭제하기 전에는 `parallel-development`로 lane·claim을 확보한다. 현재 단계의 지시·의존성·경계를 적용하며, SDD 작성 claim에 아직 작성하지 않은 AS-IS/PLAN의 PASS를 요구하지 않는다. tracker 기록과 Epic 관리 문서 자체의 기존 예외는 유지한다.
3. 제품 코드 수정 전에는 Issue의 필수 본문·Priority/grade와 라벨 일치·allowed/forbidden·완료 기준·현재 구현 의존성을 확인하고, `sdd-workflow.md`의 구현 시작 조건과 `parallel-development` claim을 충족한다. 불충족이면 제품 코드를 수정하지 않는다.
4. 각 원본이 정한 시작·변경 전 경계에서 `observations.md`의 시작 기록과 활성화된 `token-diagnostic.md`의 START를 적용한다. 재개·인계는 기존 시작 원본을 참조하며 새 작업의 관측을 이전 작업에서 상속하지 않는다.
5. 현재 phase/role에 진입할 때는 current/manual model을 그대로 유지하는 경우도 `execution-routing.md`의 해당 적격 경로를 확인한다. canonical DENY·실제 explicit record·fresh capability floor 확인을 model switch 유무로 생략하지 않는다. 같은 run의 해당 role에서 여전히 유효한 근거는 재사용하고 미래 phase의 concrete model PASS를 현재 착수 조건으로 요구하지 않는다.

## 조사·설계와 grade별 진행

상위·관련 분석은 `sdd-workflow.md`의 `기존 분석 재사용`에 따라 기준 revision·범위·전제·근거를 확인하고 부족하거나 바뀐 부분만 보완한다. 재사용이 해당 grade의 검토를 면제하지 않는다. 공통 변경은 소비 작업의 적용·호환성·전환 영향까지 담당 Issue의 범위와 검증에 포함한다.

1. 선언한 기준 revision의 code를 관찰한 AS-IS, current Issue를 요청한 TO-BE로 삼는다. 직접 관련 business 문서만 비교하며 문서와 다르다는 이유로 코드를 과거 동작에 맞추지 않는다. 기준 구현·외부 동작·운영 소비자가 판단에 영향을 주면 `sdd-artifacts.md`의 `판단에 필요한 조사`를 적용한다.
2. Issue와 architecture/완료 기준 충돌은 `agent-instruction-policy.md`로 판단하고 해소되지 않으면 `BLOCKED: instruction conflict`로 중단한다.
3. 저장소 파일의 최초 쓰기 전 lane·claim을 확보한 뒤 아래 순서에 맞춰 현재 산출물을 작성한다. 형식·Decision/실행 명세 구분·실제 경쟁 선택지의 trade-off는 `sdd-artifacts.md`를 따른다. 선택지를 만들기 위한 광범위 탐색은 하지 않는다.

| grade | 실행 순서 |
| --- | --- |
| Trivial | 조건을 확인하고 대상 text/metadata·직접 검증 근거만 조사한다. 별도 SDD·제품 AS-IS discovery를 추가하지 않으며 조건을 벗어나면 수정 전 최소 Small로 재판정한다. |
| Small | Issue를 계획으로 사용하며 별도 SDD 없이 진행한다. |
| Medium | 필요한 SDD·검증 계획을 작성하고 충돌이 없으면 추가 승인 없이 구현한다. |
| Large | AS-IS 작성 → 해당 phase의 유효한 design review → PLAN 작성 → 해당 phase의 유효한 design review → 구현 순서로 진행한다. |

Large의 게시·A/B·severity·blind 격리·재확인·반복 정체는 `design-review.md` 한 곳에서 판정한다. 각 phase의 current-target 근거와 `sdd-workflow.md`의 `미결 사항과 단계별 의존성`을 확인하고 결론이 필요한 작업만 진행한다. 누락·stale 근거를 과거 PASS로 대신하지 않는다. 재검토 전에는 같은 원본의 target 유지 조건부터 적용하며, 이 절차를 Medium 이하나 기본 CODE review에 추가하지 않는다.

제품 파일 수정 전에는 `verification.md`에 따라 기준 요구와 완료 기준을 검증에 대응시키고 grade별 `Independent Review` 판정을 확보한다. Medium 이상의 Human Decision Contract와 실행 명세는 `sdd-artifacts.md`를 따른다. 증명할 수 없는 완료 기준이나 허용 경계 밖 필수 검증은 `BLOCKED`다. 선택적 Device QA/Runtime QA를 구현·PR·merge gate로 만들지 않는다.

사람 판단은 P 적용 선언의 `사람 판단 지점`을 직접 확인한다. 새 중요한 제품/설계 Decision이나 확정 범위 변경은 `[HUMAN DECISION REQUIRED]`로 영향 작업을 멈추고, 사람이 밝힌 결정을 Human View와 필요한 Issue 본문에 반영한 뒤 재개한다. 파일 존재·Agent 합의·review PASS를 사람 결정으로 추정하지 않는다. 확정 의미·불변조건 안의 실행 세부는 계속 처리한다.

## Implement

구현·검증에서 PLAN 전제 오류를 발견하거나 진행 중 작업의 정책이 바뀌면 `sdd-artifacts.md`의 `계획 정정과 정책 전환`을 적용한다. SUMMARY 설명만 남기고 잘못된 PLAN을 실행 기준으로 유지하지 않는다.

1. current/manual 구현 역할을 유지하거나 위임·모델 전환할 때 `execution-routing.md`의 현재 role 적격 근거를 확인한다. 같은 run에서 확보한 유효한 해당 근거는 재사용한다. 미지원 fallback·required reviewer 분리·Human-selected B 선택 실패는 그 원본의 조건과 상태를 그대로 따른다.
2. Packet으로 인계받았다면 `execution-packets.md`의 `구현 진입의 문맥·최신성 확인`을 첫 edit 전에 수행한다. 필수 입력·guard·claim·직접 source를 증명하는 VALID 결과 없이 구현하지 않는다.
3. 제품 파일은 allowed에 포함되고 forbidden에 포함되지 않는 경로만 수정한다. acceptance 밖 기능·refactor·rename·formatting·dependency를 추가하지 않는다. W·M 고정 사본은 수정하지 않고 공통 문제로 보고한다.
4. shared/root integration-only 경로가 필요해지면 직접 수정하지 않고 `module-boundaries.md`에 따라 integration 의존성으로 전환한다. lifecycle artifact도 그 원본이 허용한 범위만 변경한다.
5. P build.md의 테스트 수명·수행 주체를 적용해 allowed 안의 직접 regression test 또는 선언된 동등 검증을 준비한다. temporary는 보존·재조회 후 제거하고 none은 대체 근거를 확보한다. `verification.md`의 구현 루프에 따라 직접 관련 검증부터 수행하며 concrete dependency·직접 영향·실제 실패 근거 없이 repository-wide 탐색이나 검증 확장을 하지 않는다.
6. required UI Visual Spec은 Issue에 고정된 immutable permalink를 사용한다. Trivial에서 실행 의미 변경이 필요해지면 최소 Small로 재판정한다.
7. PLAN Implementation finding은 `execution-packets.md`의 인계·Result 규칙으로 보존하고 current head의 code와 fixture/test 해결 근거를 확보한다. Non-blocking observation을 새 구현 gate로 승격하지 않는다.
8. 실제 문제 발견·해결은 `observations.md`로 기록하고 최초 문제와 조치/결과를 원본 참조와 함께 인계한다. 정상 단계에 사건 기록이나 추가 SDD·승인 gate를 만들지 않는다.

PLAN에서 구현 문맥을 전환할 때는 `execution-packets.md`의 `구현 진입의 문맥·최신성 확인`을 적용한다. 실제 전환 evidence·최소 입력·fallback 한계를 남기고 미지원 분리나 실패한 압축을 성공으로 기록하지 않는다. 진행 중인 IMPLEMENT lane을 소급 초기화하지 않는다.

## Verify and handoff

1. 선언된 영향 분석 결과를 사용하면 `execution-packets.md`의 `공통 영향 결과 참조와 로컬 소비`로 최신성·완전성을 확인한다. stale 결과로 Issue·grade 필수 검증을 줄이지 않는다.
2. `verification.md`의 현재 grade/change-scope·검증 시퀀싱·PASS 유효성을 적용한다. 실패 수정은 targeted부터 수행하고 안정화된 최종 후보에서 필요한 broad 검증을 완료한다.
3. 빌드·테스트 명령 전에는 `build-preflight.md`와 `verification.md`의 `검증 환경`을 적용하고 같은 run의 검증된 환경을 재사용한다. 실제 빌드 JVM·허용된 교정·재실행 결과를 확인하고 환경 차단이나 미실행을 PASS로 기록하지 않는다.
4. required failure나 미실행 검증을 PASS로 기록하지 않는다. grade상 필요하지 않은 빌드 검증이나 선택적 기기 report 부재를 새 blocker로 만들지 않는다. 수정·검증 때문에 forbidden 경로가 필요하면 중단한다.
5. diff와 전체 변경 경로를 Issue 경계·완료 기준에 대조한다. Packet 사용 시 `execution-packets.md`의 Result 검증으로 current head·inventory·검증 evidence·모든 PLAN handoff의 유효성을 확인한다. 누락·unresolved·stale이면 완료로 인계하지 않는다.
6. `finishing-issues`에 확인한 Issue·경계·검증·필수 review 근거와 compact Result를 전달한다. 공통 문서나 worker 로그를 처음부터 재수집하지 않는다. 관측 시작 원본·현재 결과·공백·다음 조치는 `observations.md`의 인계 형식으로 보존한다.

외부 중단·재개는 `token-diagnostic.md`의 BLOCKED/RESUME 조건과 `observations.md`의 인계를 적용한다. 동일 미해결 blocker를 자동 재확인하거나 checkpoint를 반복하지 않는다.

## Output

- Issue / grade / 현재 phase와 gate / claim·격리
- 실제 변경 경로 / 완료 기준 / 검증·필수 review 결과와 미검증
- 사람 판단·scope drift·BLOCKED 및 재개 조건
- 사용한 routing·Packet의 적격/유효 결과와 필요한 불변 근거 참조
- 관측 시작·사건·인계 참조와 활성 token lifecycle 기록 또는 미수집 이유
