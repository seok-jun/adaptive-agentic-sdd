# 일반 Trivial / Small 작업

명시적으로 선택한 작업을 현재/수동 선택 Agent 한 명이 수행할 때 이 간결 경로를 쓴다. Small은 한 구현 모듈 안의 동작 변경이며, 검증·사람 판단·소유권·병합 안전은 유지하고 작업 항목과 정상 경로의 세 기록만 가볍게 한다. 별도 SDD·계획·packet이나 기본 독립 리뷰는 필요 없다.

## 닫힌 읽기 집합

이 문서가 Trivial/Small 간결 절차를 소유한다. 적용되는 공통 workflow 요구는 모두 여기 직접 쓰거나 아래의 일상 읽기 절과 예외 조건으로 연결한다. 다른 공통 문서의 전달 링크도 이 집합으로 닫으며, 실제 제품 지침·권한·명시적 프로젝트 필수 검사는 면제하지 않는다. 예외로 전체 원본 문서를 열어도 이 경로의 간결 형식과 면제는 유지한다. Medium/Large에는 원본의 전체 절차가 계속 적용된다.

한 번 읽고 같은 세션의 바뀌지 않은 입력은 재사용한다.

- 선택한 입구와 [task guard](../task-guard.md), M [core](../../methodology/core.md)와 [변경 순서](../../methodology/supports/ordered-changes.md), [등급 규칙](sdd/grade.md).
- 선택한 profile, `W/../project/`의 해당 적용 문서 전부(`skill-evals.md`는 workflow/eval 작업 때만), 이 문서들이 가리키는 실제 P 원본. 프로젝트 고유 내용은 전부 적용하고 공통 절차 전달은 이 집합을 따른다. 등급을 정하기 전에 권위 있는 architecture 원본을 포함해 P의 구현 모듈·지정 공유 계약·통합 전용 경로를 확인한다. 매핑 누락은 미결 입력이며 Small의 근거가 아니다.
- [Priority 판정 순서와 근거 부족 처리](issue-priority.md), 이 문서의 간결 항목 예외, 선언한 [local-docs](../tracker/local-docs.md) 또는 [GitHub](../tracker/github.md) adapter의 매핑·간결 묶음·저장 및 소유 전제·한계. tracker 설정은 한 번 확인한 뒤 변경 여부만 확인한다. local-docs의 `tracker_root`는 lane worktree 밖에서 공유하는 local disk 또는 SMB여야 하며, 선언 작성자 확인과 백업의 한계를 유지한다. GitHub 토큰을 만들거나 찾아 등록하지 않는다.
- [Execution routing](../skills/_shared/execution-routing.md)의 두 축 routing·Host Capability Map·Model Role Qualification 중 현재/수동 자격, 낡거나 불완전한 기록, 신원 불명 부분만 읽는다. deny와 실제 명시 요구만 짧게 확인한다. 긍정 자격 기록이 없다는 사실만으로 막지는 않지만, deny를 판단할 수 없는 신원이나 불완전·만료된 명시 요구를 통과로 보지 않는다. 자동 모델 선택·위임 권한은 생기지 않는다.
- [근거 기록 규칙](issue-writing-guide.md#근거-기록-규칙), [사람용 문서의 시각적 작성](agent-instruction-policy.md#사람용-문서의-시각적-작성), Small 추가 절약 규칙을 포함한 [컨텍스트 / 토큰 효율](agent-instruction-policy.md#컨텍스트--토큰-효율). 아래 간결 작성 형식을 적용한다. 관측 예외는 여기 명시하며 작성 모델 절은 모델 평가를 명시적으로 요청했을 때만 읽는다.

## 간결 작업 항목

필요한 사실은 모두 유지하되 제목을 합칠 수 있다.

```text
Priority / grade: 각각 한 값(local-docs는 status와 함께 메타에만)
목표와 영향: 관찰 가능한 변화, 포함 동작, 현재 사용자 영향 한 문장
경계: 확인된 허용 경로; 금지 경로; 제외 동작
완료 기준: 판정 가능한 각 조건 -> 파일/심볼과 검사/근거, 편집 순서대로
의존성 / 결정: 선행 조건 또는 없음; 미결 질문 / 답할 사람 / 기다리는 작업
```

지원하면 생성 시, 아니면 생성 직후 priority와 grade를 각각 하나 설정하고 저장 결과를 다시 읽는다. local-docs는 priority/grade/status를 메타에만 저장하며 중복 값이 있다면 일치해야 한다. P0부터 P3까지 판정하고 P1/P2 근거 부족은 P2, 현재 영향 자체가 불확실하면 P3으로 둔다. 사용자가 지정한 작업에는 전체 대기열 비교가 필요 없다. 실제 다음 작업 선택 때만 프로젝트 대기열 조건과 선행 관계·등급·충돌·ID 순서를 적용한다.

관련 중복/진행 작업만 찾고 adapter 방식으로 ID를 얻는다. local-docs는 기존 파일이 있으면 생성이 실패해야 하며 검색 범위와 결과 수를 남긴다. 누락된 항목은 제품 편집 전에 보완한다. 확정된 목표·범위·경계·AC 변경은 댓글뿐 아니라 현재 본문에도 반영한다. 항목 자체가 계획이며 기존 AC 옆에 요구와 수정/검사를 연결하고 매핑을 복제하지 않는다. 미결 질문은 이 항목의 한 줄로 남기며 별도 장부나 새 라벨을 만들지 않는다.

## 실행 의무

1. **진입과 권한.** 코드 편집 전에 구현 지시, 현재 항목 재조회, 현재 단계의 선행 조건 충족, blocked 상태 없음, 허용 경로와 claim 확보를 확인한다. 선택만으로 구현 권한이 생기지 않는다. 선택한 W snapshot을 유지한다. 미결 사람 판단에 의존하는 작업만 멈추고 질문할 수 없으면 질문을 보존한다. 실제 결정과 범위·날짜·확인자가 있는 위임은 재사용하되 새로 만들거나 넓히지 않는다.
2. **등급, 쓰기 경계와 sandbox.**
   - **등급.** 변경하지 않은 등급 규칙의 Trivial 전체 조건 또는 단일 모듈 Small과 가장 높은 자동 격상을 적용한다. 범위·위험이 바뀌면 재등급하며 임의로 낮추지 않는다.
   - **쓰기 경계.** 읽기 전용 조사는 권한과 기준 revision만 확인하고 edit claim·새 lane을 만들지 않는다. 첫 작업 파일 쓰기 전에 편집·기록·임시/빌드 출력 경로를 확인한다. 스크립트·메시지·캐시·컴파일 출력도 쓰기다. 도구/stdin/메모리를 우선하고 디스크는 symlink/junction까지 해석하며 process 임시·캐시 설정도 허용 영역에 둔다. 다른 소유자의 변경을 보존하고 테스트에도 같은 경계를 적용한다.
   - **Sandbox.** 필요한 sandbox 강제를 실제 확인하고 미확인은 드러내며 거부된 쓰기를 우회하지 않는다.
3. **Lane과 claim.** 저장소·remote·dirty 상태·worktree·열린 미병합 작업 branch·경쟁 claim을 확인한다. 새 lane은 선언 base를 fetch한 직후 `git rev-parse --verify 'FETCH_HEAD^{commit}'`를 고정하고 그 SHA에서 생성한 HEAD가 같은지 확인한다. fetch 실패 때 멈추고 기존 진행 lane을 자동 재생성하지 않는다. 단독 격리 clone은 추가 worktree 없이 작업 branch를 쓴다. adapter의 배타적 획득 후 owner/status를 갱신하고 경쟁 claim을 다시 읽는다. 비어 있거나 읽을 수 없는 local claim도 충돌이다. GitHub는 CLAIM·assignee/status와 충돌 재조회를 사용한다. 획득에 지면 자기 시도만 해제하고 승자의 상태는 건드리지 않는다.
4. **구현과 검증.** 실제 source와 직접 계약에서 동작·이름을 확인한다. 구현 전에 기준 요구와 영향 경로를 AC 근거에 연결하고 회귀 테스트 또는 P가 선언한 동등 근거를 준비하며 검증 불가·경계 밖 검증은 차단한다. 자체 리뷰가 기본이며 독립 리뷰 판정은 명시적 예외일 때만 기록한다. 직접/소유 모듈 검사부터 시작하고 근거가 있을 때 넓히며 최종 후보에 모든 P/Issue 필수 검사와 CI의 유효한 성공 근거를 확보한다. Trivial은 적합한 표적 검사만 하고 build 영향이 없으면 기본 build를 요구하지 않는다. 불명·미실행·실패한 필수 검사는 미완료이며 선택적 QA는 새 AC가 아니다.
5. **후보와 리뷰.** 항목·head·상태가 바뀌면 영향 입력을 다시 읽는다. PASS는 바뀌지 않은 검증 입력에만 유효하며 테스트 삭제·단언 약화·검사 제외는 영향 판단과 대체 근거/공백 공개가 필요하다. 영향받은 표적 검사와 무효화된 필수 검사만 다시 하고 재사용을 새 실행으로 보고하지 않는다. 유효한 최종 검증 후 전체 변경 파일 목록과 관련 diff hunk를 직접 보되 diff 전체를 출력하지 않고, 기준 요구·범위·AC·실패·위험을 자체 리뷰한다. 후보 변경 후에는 영향 검증과 최종 리뷰를 갱신한다.
6. **문서와 작성.**
   - **문서 동기화.** 직접 사용자/백그라운드 진입점을 살펴 최종 코드에서 바뀐 업무 규칙만 직접 영향받는 기존 문서에 최종 검증 전에 반영하며 다른 lane의 문서 편집 충돌을 먼저 해결한다. 동작 변화가 없으면 동기화 문서를 만들지 않는다.
   - **작성.** 프로젝트 언어로 변화·검증·남은 문제를 짧게 설명하고 식별자·원래 도구 출력을 보존한다. 이해에 필요한 표/그림만 쓰며 별도 작성 품질 관문을 만들지 않는다. UTF-8로 먼저 읽고 현재 shell과 구조화된/portable 입력을 사용하며 실패 우회용 영구 host 설정 변경은 하지 않는다.
   - **근거 위생.** 요구에는 원본 ID와 revision/제공 시각, 결정에는 내용·범위·결정자·시각·출처를 남긴다. 보호 정보·대화/추론 원문·재구성 가능한 요약은 제외하고 합성 자료로 재현하며 실제 저장 내용을 확인한다. 금지 자료는 허가된 방식으로 제거하거나 사람에게 알린다.

## 세 기록 lifecycle

선언 adapter의 간결 묶음을 쓴다. 세 기록은 정상 경로이며 실패·정정·실제 인계의 상한이 아니다. 각 필드는 실제 시각·식별·근거를 유지하며 기록 통합으로 실행 시점을 앞당기지 않는다.

1. **CLAIM**은 두 tracker 모두 소유권(`agent`, `branch`, `allowed`, `forbidden`)과 시작 사실을 합친다: task, 선택한 W commit(legacy는 해당 pin), base, 현재 요구 원본과 영속 기록 위치. 읽은 문서/support/구간의 상세 목록은 방법론 평가 때만 남긴다. 과거 종료 작업 탐색이나 없다는 문구는 의무가 아니며 직접 연결된 알려진 결함·의존 사항은 일반 입력으로 확인한다.
2. **IMPLEMENTATION SUMMARY**는 `closes`, branch/head/base, AC 결과, 명령/결과(재사용·미실행 포함), 최종 자체 리뷰, 결정 준수/이탈, 사람에게 올린 판단, 남은 위험과 CLAIM 참조를 모은다. 실제 사건은 참조·담당자·최초 실패/근거·조치/결과로 짧게 보존한다. 빈 목록·정상 단계 행·예상된 실패 테스트의 자동 사건 집계는 만들지 않는다. 실제 보고하는 수치·사건에만 출처·범위·한계를 붙이고 사실·가설·미수집을 구별한다. 일반 모델 한 줄·미수집 비용 목록·support 평가·다음 방법론 판단은 요구하지 않는다. 명시적 모델/방법/비용 평가는 해당 원본을 열되, 그 경우에도 이 경로에서는 host 대화/설정 폴더를 탐색하지 않는다.
3. **CLOSED**는 `merged`, `closed`, `product-complete`, `cleanup`, `release`를 별도 필드로 표시한다. 아래 순서와 선언 adapter의 매핑을 따른다.

### 병합과 종료

1. 허가된 병합 직전 metadata·대상·병합 가능성·필수 검사·리뷰를 재조회한다. P의 병합 권한을 유지한다. GitHub PR base는 명시한다. local-docs merge method 누락·병합 가능성 확인 불가는 병합을 막는다.
2. 병합 후 대상을 다시 fetch한다. adapter에 따라 실제 병합과 closing reference를 확인한 뒤 closed 상태를 확정한다. merge-result SHA와 fetched tip을 구별한다. squash/rebase는 task head나 최신 tip이 아니라 나중에 `CLOSED.merged.main`에 저장할 관측된 merge-result 식별로 검사한다.
3. adapter에 따라 종료를 확인한다. local-docs는 병합 검증 성공과 일치하는 closing reference 확인 후 closed 메타를 갱신하고 다시 읽는다.
4. 제품 완료를 확정하고 adapter별 PRODUCT COMPLETE JSON을 정리와 독립적으로 한 번 보존한다. 앞서 발생한 실제 시각과 근거는 아래 정리/해제 순서에서 CLOSED로 묶는다.

여기에는 `observation-check unavailable reason=not-shipped` 문구가 필요 없다. 실제 관측 검사를 수행/재실행했다면 최초 출력·이유·최종 출력·유실을 보존한다.

작업 폴더 삭제 전에 영속 CLAIM/SUMMARY와 worktree에만 있는 필수 비민감 근거를 한 번 재조회한다. 조회 실패·유실은 남기되 관측 공백을 새 제품 관문으로 삼지 않는다. 인계·중단·병합 후 정리/해제 전에 미커밋/미push·PR·worktree 등록·local/remote branch 상태를 짧은 한 줄로 남긴다. 미완료면 정확한 경로·차단 사유·재개 조건·참조를 더한다. 인계하는 미병합 worktree를 지우거나 소유자 변경만으로 새 시작을 만들거나 같은 blocker를 자동 재조회하지 않는다.

### 정리와 해제

1. 정리 전에 미커밋·untracked·ignored 내용과 다른 worktree를 확인한다. 정리 권한이 있는 자기 산출물만 지운다.
2. 필수 정리 실패 시 제품 완료를 보존하고 CLOSED에 정리/해제 미완료를 기록하며 소유권을 유지한다.
3. 필수 정리 성공 후 일치하는 claim 아래 소유권을 재확인한다. 앞서 발생한 병합·종료·제품 완료·정리의 실제 시각/근거와 해제 **준비**를 담은 CLOSED를 추가한다.
4. 자기 metadata만 정리하고 제거를 확인한다. local-docs는 일치하는 배타적 claim을 마지막으로 삭제하고 부재를 확인한다. GitHub는 adapter의 최종 `CLOSED.release` 갱신으로 정확한 CLAIM을 종료한 뒤 해제와 metadata를 재조회한다. 과거 댓글은 보존한다.
5. 실제 해제 확인 뒤에만 성공을 보고한다. 준비 필드는 삭제나 최종 해제 증거가 아니다. 실패 시 제품 완료를 보존하고 해제 미완료로 보고하며 세 기록을 넘더라도 정정 항목을 추가한다.

local-docs는 작성자/시각/고유 ID를 가진 append-only 항목이며 추가 직전 재조회와 직후 ID 확인을 유지한다. 정정은 원본 참조/supersedes로 남기고 원본을 고치지 않는다. GitHub는 기존 댓글에 나중 사실과 시각을 갱신할 수 있다.

최종 보고는 SUMMARY에서 변경 파일·요구별 상태·검사/결과·미실행/이유·차단 사항을 재사용한다. 실패/미검증 AC가 있으면 제품 전체 완료가 아니며 관측 공백·선택적 QA·로컬 정리 실패는 별도 상태로 보고한다. 이 작업의 범위를 끝내며 다른 작업/영역/방법은 새 세션에서 선택한다.

## 예외 조건

조건이 생긴 원본 절만 읽으며 위 간결 대체와 명시적 P 요구를 유지한다.

| 조건 | 원본과 동작 |
| --- | --- |
| 경쟁 claim, 동시 수행자, 다른 checkout 생성(외부 전용 harness 연결 포함) | [parallel-development](../skills/parallel-development/SKILL.md)의 신규 lane 생성과 isolation / Claim. 공유 tracker·checkout 연결·Windows 짧은 경로를 확인하고 한 branch에 두 Agent가 commit하지 않는다 |
| 관련 base/merge branch 변경 | [Synchronization](../skills/parallel-development/SKILL.md#synchronization). 다음 push 전에 동기화하고 허용 경로에서만 충돌 해결·영향 검증을 하며 금지/공유 경로 충돌은 멈춘다 |
| 한 모듈 안이어도 공유 계약·root/통합 경로·경계 변경 | [module-boundaries](module-boundaries.md). 확장 전 경계 판단·통합 의존성·재등급 |
| 격상, 필수 독립 리뷰, SDD, 다른 수행자 또는 더 높은 위험 단계 | 해당 [구현](../skills/implementing-issues/SKILL.md)·[검증](verification.md)·[종료](../skills/finishing-issues/SKILL.md)·routing 전체 계약. 미해결 지적은 계속 차단 |
| 선언 build·test·cleanup 명령 실행 전 | 해당 [build-preflight](../skills/_shared/build-preflight.md)와 [검증 환경](verification.md#검증-환경). 바뀌지 않은 확인은 재사용하며 JVM build만 launcher/daemon JVM을 확인한다. process 범위 보정·제한된 탐색·임의 설치/다운로드/영구 설정 금지 유지 |
| 필수 수동/device/runtime 검사, temporary/none 테스트 정책 | [Verification Strategy](verification.md#verification-strategy). 실제 대상/절차/예상 및 관측 결과·확인자/시각/대상 식별을 확보하고 임시 근거는 보존·재조회 뒤 삭제한다. none도 필수 검사 면제가 아니다 |
| 전제 오류·AC 변경·정책 전환, 미결 단계 의존성 | [plan-change](sdd/plan-change.md) / [Issue 의존성](sdd/issue.md). 이전 지시·정정 이유·결정 참조·적용 시각으로 현재 항목과 기존 기록을 고치고 영향 검증/리뷰만 갱신한다. 별도 전환 문서·질문 장부는 만들지 않는다 |
| 참조 구현·외부 소비자·의존성 버전 동작이 판단에 영향 | [AS-IS 조사](sdd/as-is.md)의 판단에 필요한 조사. 해당 revision/버전 근거를 확인하되 조사만으로 SDD를 만들지 않는다 |
| 처리 순서 변경, 한 입력의 여러 실행 경로 분기, 비동기 흐름, 여러 상태 전이 AC, 세 구성요소 이상 호출 순서 | [Mermaid 생성 조건](issue-writing-guide.md#mermaid-생성-조건). 같은 경로를 명확히 보여주면 짧은 조건표나 입력→결과 예시로 대체할 수 있다. Trivial은 기존 흐름을 설명할 수 있지만 동작 변경은 재등급한다 |
| 사용자에게 보이는 UI/UX 변경 또는 명시적 화면 설계 요청 | 아래 [시각 자료](#시각-자료)와 [HTML 생성 조건](issue-writing-guide.md#html-visual-spec-생성-조건) |
| 기존 코드/문서 불일치 또는 업무 문서 lifecycle 예외 | [business 문서 갱신](sdd/completion.md#business-문서-갱신) / [module-boundaries](module-boundaries.md). 150자 분리/review topic 규칙은 Medium 이상에만 적용한다. 간결 경로는 기존 문서의 줄바꿈/목록으로 정리하고 길이만으로 파일을 만들지 않는다 |
| 명시적 프로젝트 review topic | [reviews](reviews/README.md). P가 허용하면 기존 Issue 결정 절로 제안/검토/결정·필수 승인을 보존한다. 등급만으로 topic을 만들지 않는다 |
| 등록된 local worktree 제거 | [Merged local worktree cleanup](../skills/parallel-development/SKILL.md#merged-local-worktree-cleanup). 정리 예외·Windows 요구·출처 불명 잔여물을 확인하고 등록과 실제 폴더 부재를 각각 확인한다. 강제 제거·대량 잔여물 우회 삭제 금지 |
| 선언된 영향 분석 결과 소비 | [execution-packets](../skills/_shared/execution-packets.md)의 영향 결과 소비. 최신성/완전성을 확인하고 필수 검증 축소 근거로 쓰지 않는다 |
| 명시적 방법론/모델 평가 또는 방법 판단이 필요한 실제 반복 문제 | [observations](observations.md)와 M adaptation의 해당 판단만 수행한다. 새 Issue·모델 호출·정책 변경 권한은 생기지 않는다 |
| 이 Trivial/Small의 명시적 비용 평가와 token diagnostic ENABLED | [token-diagnostic](token-diagnostic.md). 일반 간결 작업은 ENABLED여도 면제한다. 제공된 공식 값만 쓰고 추정/탐색·새 완료 관문은 없다 |
| 명시적 BUILD-PREFLIGHT-DIAG | [조건부 진단 모드](../skills/_shared/build-preflight.md#조건부-진단-모드). 비민감 기록 하나로 모으며 keyword 없이 추가 검색/재실행하지 않는다 |
| Encoding 또는 shell 실패 | [agent-instruction-policy](agent-instruction-policy.md)의 UTF-8 / shell 절차. 제한된 fallback만 쓰고 host/저장소 전체 검색은 하지 않는다 |
| 우선순위 변경 또는 실제 대기열 선택 | [issue-priority](issue-priority.md)의 Priority 변경 / 동일 Priority 안의 순서. 간결 필드를 사용한다 |
| Workflow/skill/eval 동작 변경 | 프로젝트 `skill-evals.md`와 [skill-evals](skill-evals.md). 직접 관련 사례·필수 정적 검사·허가된 격리 평가만 수행하며 전체 corpus는 요청 때만 실행한다 |

## 시각 자료

- **자료 선택.** 명시적 HTML 요청은 따른다. 그 외에는 프로젝트가 허용한 간단한 화면 자료/상태표로 대체할 수 있다. 저장소 선언 없이 HTML을 만들지 않는다.
- **고정 참조.** 필수 Visual Spec은 구현 전 접근 가능한 commit 고정 링크로 둔다. 기능은 Issue, UI는 HTML을 따른다. 고정 자료를 검사하고 접근을 확인한다.
- **선택적 발행과 정리.** 이 경로에서 별도 design PR/배포는 기본 의무가 아니다. 실제 발행 시 공개/검사/병합 권한과 design PR의 앱 종료 Closes 금지를 유지한다. 생성한 설계 branch/worktree는 원본의 링크 보존 정리를 따른다.
