# 일반 Trivial / Small 작업

명시적 선택 후 현재/수동 선택 Agent 한 명이 수행하는 작업에는 이 간결 경로를 쓴다. 이 경로에서는 네 Skill 본문 전체를 미리 읽는 대신 아래 절차를 따른다. 제품 규칙, 필수 리뷰·검증, claim, 병합 권한을 면제하지 않는다. 선택한 입구, task guard, M `core.md`, [등급 규칙](sdd/grade.md), 실제 P 원본, 해당 프로젝트 선언과 선택한 tracker adapter를 한 번 읽는다. 같은 세션의 바뀌지 않은 입력은 재사용한다. Medium/Large 설계나 packet·위임 문서를 미리 읽지 않는다.

## 적용 조건과 범위

- 등급 규칙과 P 매핑으로 Trivial의 모든 조건 또는 자동 격상 없는 단일 모듈 Small인지 확인한다. 범위·위험이 바뀌면 다시 판단하며 자동 등급을 임의로 낮추지 않는다.
- 모델 deny와 명시적 역량 요구를 적용한다. 일반 현재/수동 경로 예외는 [execution routing](../skills/_shared/execution-routing.md)에 있다. 자동 모델 선택이나 위임 권한이 아니다. 필수 독립 리뷰, 미결 권한, 다른 수행자, 더 높은 위험 단계가 있으면 해당 동작의 전체 Skill/계약을 읽고 진행하며 의존하는 작업만 멈춘다.
- 쓰기 전에 필수 검증, 제품 편집 경로, 기록 위치, 임시·빌드 출력 경로를 확인한다. 보조 스크립트·메시지 파일·캐시·컴파일 출력도 쓰기다. [task guard](../task-guard.md)를 따르며 OS 임시 폴더가 쓰기 가능하다는 사실은 허가가 아니다.
- M [변경 순서](../../methodology/supports/ordered-changes.md)에 따라 편집과 검증의 연결을 한 문장이나 짧은 목록으로 둔다. 실제 생성 조건이 없으면 별도 계획 파일, SDD, 그림, HTML을 만들지 않는다.

## 한 번 실행하고 한 번 기록

1. **작업 항목.** [우선순위와 필수 본문·라벨](issue-priority.md), [근거 기록 규칙](issue-writing-guide.md)을 적용한다. 기존 필수 절에는 짧게 쓰고 대화를 복사하지 않는다. 검증 가능한 AC와 실제 허용·금지 경로를 유지한다. 관련 중복/진행 작업만 찾고 생성한 항목의 정확성을 다시 확인한다.
2. **Lane과 claim.** 편집 전 저장소·remote, dirty 상태, branch/worktree 충돌과 다른 claim을 확인한다. 선언한 base branch를 fetch한 직후 `git rev-parse --verify 'FETCH_HEAD^{commit}'`로 SHA를 고정하고 그 값을 쓴다. 단독 격리 clone은 추가 worktree 없이 작업 branch를 쓸 수 있고, 동시 lane은 격리 worktree가 필요하다. tracker 매핑에 따라 claim을 배타적으로 획득하고 owner/status를 갱신한 다음 충돌을 다시 확인한다. 다른 소유자 상태는 보존한다. 기존 CLAIM 기록에 task/W/base 식별, 실제 읽은 원본, 기록·임시 경로와 적용 support를 남기며 별도 START 댓글은 필요 없다. 연결된 이전 관찰 또는 같은 경계의 최근 종료 항목 최대 하나를 확인하고, 없거나 조회 불가하면 그 사실만 남긴다.
3. **변경과 검증.** claim 경로만 편집한다. 소유 모듈 테스트부터 실행하고 최종 후보에서 P/Issue 필수 검증을 모두 수행하며 근거가 있으면 넓힌다. Trivial은 변경에 맞는 표적 검사를 한다. 범위·AC·실패·위험을 자체 리뷰한다. 검증 입력이 바뀌지 않은 PASS만 재사용하고 미실행·실패를 PASS로 만들지 않는다. 같은 수행자와 바뀌지 않은 작업에 매핑·계획·packet을 중복 생성하지 않는다.
4. **요약.** closing reference, branch/head/base, AC별 실제 결과, 명령·결과, 자체 리뷰, 남은 위험과 시작/claim 참조를 `[IMPLEMENTATION SUMMARY]` 한 곳에 쓴다. 이미 제공된 호스트/사람의 메타데이터로 [관찰](observations.md)의 모델 한 줄을 남긴다. 없는 모델·비용 정보는 `unconfirmed`/`not collected`로 두며 선택적 관측값을 채우려고 호스트 대화·설정 폴더를 탐색하지 않는다. 실제 문제의 최초 실패와 조치/결과를 보존하되 빈 문제 목록이나 정상 단계 서술을 반복하지 않는다. 고정 시작 정보는 복사하지 않고 참조한다.
5. **병합과 종료.** 병합 직전 현재 메타데이터, 선언한 대상·병합 가능 여부·필수 검증을 재확인하고 P의 병합 권한을 따른다. 허가된 병합 후 대상을 다시 fetch하고 tracker adapter의 실제 병합 확인(squash/rebase 식별 포함)을 수행한 뒤 일치하는 작업만 닫는다. 영속 시작/요약을 한 번 재조회하고 worktree에만 있는 근거를 보존하며 [finishing](../skills/finishing-issues/SKILL.md)의 실제 식별을 담은 `[PRODUCT COMPLETE]`를 남긴다. observation-check unavailable 한 줄은 비차단이다. 병합·닫힘·product-complete·release 표시는 각각 식별 가능하게 유지하되 tracker가 지원하면 실제 순서/식별을 보존한 기존 종료 갱신 하나에 묶을 수 있다. append-only tracker는 변하지 않은 SUMMARY 전체를 복사하는 대신 종료 기록에 최종 사실을 추가한다.
6. **정리와 해제.** 미커밋·untracked·ignored 내용과 다른 worktree를 확인한 뒤 정리 권한이 있는 자신의 lane/branch 산출물만 삭제한다. 영속 기록과 필수 근거는 보존한다. 배타적 claim을 유지한 채 소유권을 재확인하고 해제를 기록하며 자신의 메타데이터만 정리한 다음 해당 claim을 마지막으로 제거한다. 경쟁 claim을 해제하거나 정리 실패를 완료로 보고하지 않는다. 작업 범위를 종료하며 다른 작업은 새 선택/세션에서 시작한다.

## 필요한 경우 전체 절차로 전환

경쟁 claim, 동기화/base 변경, AC 변경, 필수 독립 리뷰, SDD, 실제 미결 지침·권한 충돌이나 격상이 있으면 관련 전체 Skill/계약을 쓴다. 기존 [검증](verification.md), [parallel-development](../skills/parallel-development/SKILL.md), [finishing](../skills/finishing-issues/SKILL.md) 조건은 해당 동작에 계속 적용된다. 확인한 입력이 같으면 재사용하고 준비 전체를 재시작하지 않는다. 요구를 몰래 없애서 충돌을 해결하지 않는다.
