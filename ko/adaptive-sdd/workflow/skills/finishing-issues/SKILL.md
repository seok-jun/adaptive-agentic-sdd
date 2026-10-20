---
name: finishing-issues
description: 구현을 마친 이 프로젝트의 Issue 작업을 종료한다. 최종 diff 검토, business 문서 동기화, 검증·CI gate, SDD 정리, PR 종료 구문, merge 확인, lane 해제에 사용한다. 구현이 종료 준비되기 전에는 사용하지 않는다.
---

실행 입력은 절대 경로 `P`(프로젝트 저장소 최상위), `W`(고정 절차 사본 `P/.adaptive-sdd/workflow`), `M`(고정 공통 원칙 `P/.adaptive-sdd/methodology`)이다. cwd나 W의 상위 디렉터리로 P/M을 추정하지 않는다. P의 hard guard와 적용 선언을 따르고, Issue·댓글·라벨·PR 표현은 `P/.adaptive-sdd/project/tracker.md`가 선언한 `W/tracker/` 방식으로 읽는다.

# Finishing Issues

Epic 관리 문서의 종료는 `managing-issues`의 `Epic 조율`에서 전체 목표 달성 근거를 확인한다. 아래 제품 변경 종료 순서를 코드·PR·CI·SDD·claim이 없는 관리 문서 자체에 요구하지 않는다. 하위 종료 표시만으로 Epic을 닫지 않는다.

## Inputs

현재 run에서 `P/AGENTS.md`의 `## 항상 적용 hard guard` 적용을 보장할 수 없으면 그 절부터 읽는다. implementing에서 확인한 변경 없는 입력·검증 결과는 재사용한다. 조회·갱신은 `implementing-issues`의 `입력 재사용과 조회` 절을 적용하며 그 스킬 전체를 다시 읽지 않는다.

필수 입력은 current Issue body/labels, current diff, `W/process/sdd-workflow.md`의 현재 grade·종료 관련 진입 조건, P 적용 선언의 권한·경로·검증이다. PR이 있으면 필요한 PR/CI metadata를, runtime 동작이 바뀌었으면 직접 관련 business 문서를 읽는다.

아래 순서에서 필요한 원본의 **해당 절만** 읽는다.

| 행동 | 읽을 원본 |
| --- | --- |
| Large AS-IS/PLAN 근거 유효성 확인 | `W/process/design-review.md`의 current-target·다음 phase 조건·재확인 절 |
| 검증·grade별 code review·PASS 재사용 | `W/process/verification.md`와 P 적용 문서 `build.md`의 해당 검증 |
| Packet·구현 문맥 전환·선언된 영향 결과 소비 | `W/skills/_shared/execution-packets.md`의 해당 Packet·영향 결과 절 |
| current/manual 종료 역할의 진입·유지 또는 reviewer 배정의 적격 확인 | `W/skills/_shared/execution-routing.md`의 해당 role·선택 경로 |
| SDD의 Decision/실행 명세 확인 | `W/process/sdd-artifacts.md`의 해당 산출물 절 |
| business lifecycle·shared/root 경계 판단 | W/P `module-boundaries.md`의 관련 경계 |
| 지시·diff와 Issue·code와 business 충돌 | W/P `agent-instruction-policy.md`의 해당 충돌 절 |
| 관측 취합·SDD 삭제 전 보존·제품 완료 관측 | `W/process/observations.md`의 해당 단계 절 |
| 활성 token lifecycle의 중단·재개·종료 | `W/process/token-diagnostic.md`의 해당 event |
| worktree 정리·ownership 해제 | `W/skills/parallel-development/SKILL.md`의 Release와 해당 cleanup 절 |

종료 role에 진입할 때 current/manual model을 유지하는 경우도 `execution-routing.md`로 해당 역할의 canonical DENY·실제 explicit record·fresh capability floor를 확인한다. 같은 run의 해당 role에서 여전히 유효한 근거는 재사용하며, model switch가 없다는 이유로 이 확인을 생략하지 않는다.

## Finish in fixed order

### 1. Confirm actual change

1. base/head SHA와 current head의 **전체 changed-file inventory**를 직접 확인하고 diff를 읽는다. worker가 고른 목록만 신뢰하지 않는다. Result Packet을 받았다면 `execution-packets.md`로 current diff·inventory·근거의 유효성을 검증한다.
2. behavior change와 formatting/comment/generated change를 구분하고 각 실제 변경을 Issue 완료 기준에 연결한다. `verification.md`의 기준 요구 대응을 반대 방향으로도 확인해 빠진 진입점·조건, 검증 약화·미실행의 대체 근거와 공백을 SUMMARY에 드러낸다.
3. Human Decision·실행 명세·diff를 대조한다. 사람이 결정하지 않은 새 중요한 Decision이나 의미 변경이 있으면 P의 `[HUMAN DECISION REQUIRED]` 절차로 영향 작업과 closure를 중단한다. Agent 합의·review PASS를 사람 결정으로 대신하지 않는다.
4. Large는 `design-review.md`에 따라 AS-IS와 PLAN 각각의 current-target 근거가 유효하고 필요한 재확인·reconciliation이 완료됐는지 확인한다. 누락·stale PASS·분리/선택/격리 실패를 구현 진행 사실로 정당화하지 않으며, 유효한 근거가 없으면 closure를 중단한다. Human에게 상세 리뷰 전체를 다시 읽도록 요구하지 않는다.
5. scope 밖 변경은 allowed 안에서 안전하게 제거하거나 `BLOCKED`한다. W·M 고정 사본을 수정해야만 풀리면 공통 문제로 보고한다.

구현 문맥 전환 evidence와 fallback 한계도 해당 Packet 계약으로 소비한다. 필수 근거를 잃은 압축·인계를 성공으로 추정하지 않으며 로그 전문을 재수집하지 않는다. 반복 정체로 중단된 blocker는 `design-review.md`가 정한 해결·사람의 범위 결정 근거 없이 closure하지 않는다.

사람용 변경 문서와 아래 PR/완료 요약은 `agent-instruction-policy.md`의 `사람용 문서의 시각적 작성`을 같은 self/required review에서 확인한다. 추가 승인·리뷰 회차·그림 수 gate를 만들지 않고 단순 설명은 짧게 유지한다.

### 2. Synchronize business documents

runtime behavior가 바뀐 경우에만 직접 영향을 받는 P의 business rule/topic을 확인한다. Issue/SDD prose 대신 **final code**로 실제 동작을 확인하고 바뀐 기존 규칙만 갱신한다.

같은 business 파일을 다른 active lane/PR이 수정하면 `BLOCKED: documentation lane conflict`다. lifecycle 허용 범위는 `module-boundaries.md`를 따른다. runtime/product behavior가 바뀌지 않았으면 동기화를 위해 business 문서를 만들거나 수정하지 않는다.

### 3. Verify before SDD cleanup

1. 선언된 영향 분석 결과를 사용하면 `execution-packets.md`의 `공통 영향 결과 참조와 로컬 소비`로 최신성·완전성을 확인한다. stale 결과로 필수 검증을 줄이거나 이전 SHA의 review PASS를 승계하지 않는다.
2. SDD 삭제 전에 구현의 필수 검증 근거를 확인하고 누락·무효화된 검증을 수행한다. 입력 변경 뒤 targeted 재실행·필수 broad 재실행·입력 불변 PASS 재사용은 `verification.md`를 따른다. 이 시점의 확인을 정리 후 최종 후보의 CODE Review·완료 판정으로 대신하지 않는다. business 동기화 전 CODE Review가 있다면 과거 근거로 보존하고, 새 후보의 CODE Review는 5단계에서 판정한다.
3. 빌드·테스트 명령 전 `build-preflight.md`와 `verification.md`의 `검증 환경`을 적용한다. 환경 실패를 제품 회귀로 단정하지 않으며 선언된 실제 빌드 JVM 확인·허용된 process-local 교정 결과만 canonical 근거로 사용한다. 미실행·환경 차단을 PASS로 기록하지 않는다.
4. command/result와 필요한 CI를 확인한다. required failure·미실행 검증은 incomplete다. Trivial 등 해당 grade에 필요하지 않은 빌드나 선택적 Device QA/Runtime QA·report 부재를 새로운 gate로 만들지 않는다.
5. 전체 변경 경로가 Issue allowed/forbidden과 일치하는지 다시 확인한다. Result Packet이 있으면 `execution-packets.md`의 current-head 검증 evidence와 PLAN Implementation finding 해결 조건을 충족해야 한다. 명령 성공 자기신고만으로 PASS를 증명하지 않는다.
6. 외부 blocker는 상태·재개 조건을 기록하고 `observations.md`와 활성 `token-diagnostic.md`의 BLOCKED/RESUME을 적용한다. 해소 근거 없는 재개·자동 재확인·반복 checkpoint를 하지 않는다.

### 4. Remove temporary SDD

SDD·로컬 결과에만 있는 발견 사건은 삭제 전에 `observations.md`의 `문제 발견 시 기록과 종료 연결`로 기존 Issue에 보존한다. 검토한 SDD를 사건 장부로 수정하지 않는다. 보존 실패는 인계/종료에 드러내되 수집을 새 완료 gate로 만들지 않는다.

Trivial/Small은 해당 없음이다. SDD가 있으면:

1. business sync와 필요한 verification 뒤 **현재 Issue의 SDD만** 삭제한다. 검토 문서는 삭제 전 commit에서 계속 조회할 수 있어야 하며 일부 삭제·설계 수정을 정리로 숨기지 않는다.
2. P가 선언한 문서 목차와 관련 문서에서 삭제된 SDD 링크를 제거한다.
3. historical review의 mutable status가 stale하면 status만 갱신한다.

### 5. Prepare/verify PR closure

business 동기화, 현재 SDD 삭제, 링크·review status 정리처럼 예정된 저장소 파일 변경을 먼저 마친다. 그 결과를 commit하고 현재 base/head·전체 diff·inventory를 최종 리뷰 후보로 고정한다. 과거 CODE Review의 target과 다른 후보를 기존 PASS로 완료 처리하지 않는다.

1. CODE Review/self-review 전에 `verification.md`의 required broad command set에 대해 현재 후보에 유효한 PASS 근거를 확보한다. 3단계의 입력 불변 PASS는 실행 identity를 보존해 재사용하고, 정리한 문서를 소비하는 static validator 등 누락·무효화된 검증만 해당 계약의 순서로 실행한다. 검증 보정으로 파일이 바뀌면 새 후보와 그 검증 근거를 먼저 확정한다.
2. `verification.md`의 `Grade별 review gate`를 현재 후보에 적용한다. Trivial·Small은 해당 self-review, Medium은 `Independent Review` 판정, Large는 bounded independent code review 1회의 유효한 결과를 확인한다. Trivial 조건을 벗어나면 최소 Small로 재판정한다. 이미 같은 후보에서 유효한 리뷰는 재사용하며 기본 CODE review에 B를 추가하지 않는다.
3. required reviewer에게 앞서 확보한 검증 근거를 포함한 `execution-packets.md`의 current CODE Review Packet을 제공한다. reviewer는 검증 근거의 유효성·재사용 조건, 전체 inventory와 PLAN handoff의 완전성·current code/fixture 해결을 독립 확인한다. 삭제한 SDD의 검토 원문은 삭제 전 exact commit으로 참조한다. 필요한 근거가 없거나 필수 해결 finding·INVALID/STALE이 남으면 merge/complete로 진행하지 않는다.
4. 리뷰 후 현재 후보의 리뷰·검증 근거가 모두 유효한지 확인한다. 리뷰 finding 반영 등으로 저장소 파일이 바뀌면 새 후보를 고정하고 영향받은 검증을 갱신한 뒤 그 후보의 CODE Review/self-review 근거를 확보한다. 입력이 바뀌지 않은 검증은 반복하지 않으며 빌드 PASS 재사용을 이전 CODE Review target의 자동 승계로 확대하지 않는다.

아래 PR·SUMMARY 기록은 위 후보의 유효한 리뷰·검증 근거에 연결한다. PR metadata만 바뀌고 저장소 후보가 불변이면 같은 CODE Review를 다시 실행하지 않는다.

1. PR scope를 Issue 경계·완료 기준과 대조하고 body에 `Closes #{issue-number}`를 넣는다.
2. 기존 `[IMPLEMENTATION SUMMARY]` 하나에 Decision 준수·execution deviation·Human escalation·verification·남은 위험을 정리한다. 이미 있으면 갱신하며 새 문서·Human 승인 gate를 추가하지 않는다.
3. 같은 SUMMARY에 `observations.md`의 종료·작성 모델·발견 사건 규칙을 적용한다. 최초 문제·담당·조치/결과와 원본 참조를 보존하고 PR 이후 CI/review 사건도 취합한다. 사건이 없으면 빈 사건 목록을 만들지 않는다.
4. 관측 시작 원본·실제 지원과 사용·공백·비용 출처·작성 모델·다음 판단을 해당 원본 형식으로 연결한다. 모델 미확인이나 관측 미수집을 제품 closure gate로 만들지 않으며, 합성 PASS·자기보고를 효과 증거로 기록하지 않는다.
5. Large PR은 P의 사람 판단 지점에 따라 사람이 직접 병합하거나 그 PR 병합을 명시적으로 지시한 경우에만 병합한다. 일반 진행 지시·review PASS·CI 통과만으로 병합하지 않는다.
6. required CI/review와 나머지 완료 조건이 충족되기 전에 완료라고 표현하지 않는다.

### 6. Merge confirmation and release

1. merge 직전과 merge 후 closure 확인 경계에서 필요한 metadata를 갱신하고 실제 PR merged·Issue closed를 확인한다.
2. 정리 전에 관측 시작·SUMMARY·필요한 원본을 지속 보존 위치에서 재조회한다. 결과·조회 공백은 `observations.md`의 제품 완료 관측으로 SUMMARY에 남긴다. local worktree만을 후속 관측의 유일한 원본으로 남기지 않는다.
3. `observations.md`의 `종료 관측 점검`을 적용한다. 이 preview의 `observation-check unavailable reason=not-shipped` 결과와 필요한 최초 출력·재실행 이유를 준비하되 closure/release의 새 차단 조건으로 삼지 않는다.
4. 위 점검 결과와 실제 main 대상 PR의 closing reference·merge SHA로 `[PRODUCT COMPLETE]`를 한 번 기록한다. 첫 줄 태그 다음에 `product-complete: {"schema_version":1,"issue":N,"pull_request":PR,"merge_commit":"40자리 SHA"}`를 둔다. 제품 완료와 local cleanup·ownership release는 별개이며 같은 lifecycle의 완료 기록을 중복 생성하지 않는다.
5. `parallel-development`의 Release·Merged local worktree cleanup을 실행한다. registration 제거 전에는 run-owned/generated로 증명되지 않은 untracked diagnostic/unknown 파일이 없는지 확인한다. 그런 파일은 사용자 state로 보존하고 registration 제거·RELEASE를 중단해 lane release incomplete로 보고한다.
6. no-artifact 예외, 빌드 정리, registration·physical directory 각각의 부재 확인, 허용된 잔여 정리와 ownership release 순서는 그 원본을 따른다. 현재 claim·환경 근거를 재사용하고 force cleanup이나 대량 파일의 개별 삭제 loop로 보호 정책을 우회하지 않는다.
7. cleanup/release가 pending이면 정확한 경로·상태·재개 조건을 보고하되 제품 완료를 취소하지 않는다. cleanup만의 후속 갱신은 `[LOCAL CLEANUP]`에 남기고 제품 완료 기록을 다시 작성하지 않는다.
8. 제품 완료가 확인되면 local cleanup과 별개로 활성 `token-diagnostic.md`의 END를 적용한다. `not-planned`는 merge 대신 최종 종료 확정 시 같은 원본의 해당 종료 형식을 사용한다.

## Incomplete conditions

다음 조건이면 제품 Issue를 complete라고 하지 않는다.

- 완료 기준 failed/unknown, required CI 실패, required review 미완료 또는 필수 해결 finding 미해결
- `design-review.md`의 필수 current-target 근거 누락·stale, required reconciliation 미완료 또는 Human Decision/Execution-contract blocker 미해결
- `execution-packets.md`의 필수 PLAN handoff·code/fixture 해결·검증 근거 누락·unresolved·INVALID/STALE
- required business 문서가 final code와 모순되거나 documentation lane conflict
- required SDD 정리 미완료, PR closing reference 없음, 미해결 제품 작업 BLOCKED

`CLEANUP_BLOCKED`, registration/physical 잔여와 unknown 파일은 local cleanup incomplete로 별도 보고한다. 관측·모델 기록의 미확인과 비필수 기기 확인은 각 원본이 정한 비차단 조건을 유지한다. 사용자 파일 삭제 금지는 그대로 적용한다.

## Output

- 실제 변경 경로 / 완료 기준 결과 / business 문서 상태
- 검증·CI·필수 review 및 current-target·Packet 근거의 유효성
- SDD 정리 / PR·Issue·제품 완료 / 관측 취합 참조
- 활성 token BLOCKED/RESUME/END 기록 또는 미수집 이유
- local cleanup·lane release / 미검증·BLOCKED와 재개 조건
