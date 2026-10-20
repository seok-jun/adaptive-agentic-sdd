---
name: finishing-issues
description: 구현을 마친 이 프로젝트의 Issue 작업을 종료한다. 최종 diff 검토, business 문서 동기화, 검증/CI gate, SDD 정리, PR 종료 구문, merge 확인, lane 해제에 사용한다. 구현이 종료 준비되기 전에는 사용하지 않는다.
---

실행 입력은 절대 경로 `P`(프로젝트 저장소 최상위), `W`(고정 절차 사본 `P/.adaptive-sdd/workflow`), `M`(고정 공통 원칙 `P/.adaptive-sdd/methodology`)이다. cwd나 W의 상위 디렉터리로 P/M을 추정하지 않는다. P의 hard guard(`P/AGENTS.md`의 `## 항상 적용 hard guard`)와 적용 선언(`P/.adaptive-sdd/project/sdd-workflow.md`)을 적용한다. Issue·댓글·라벨·PR 표현은 `P/.adaptive-sdd/project/tracker.md`가 선언한 작업 관리 방식(`W/tracker/`)으로 바꿔 읽는다.

# Finishing Issues

Epic 관리 문서의 종료 요청이면 `managing-issues`의 `Epic 조율`에서 전체 목표 달성 근거를 확인한다. 아래 순서는 실제 변경을 수행한 실행 Issue에 적용하며, 제품 diff·PR·CI·SDD·claim이 없는 Epic 자체에 요구하지 않는다. 하위 작업이 모두 닫혔다는 사실만으로 전체 목표 충족을 대신하지 않는다.

## Inputs

현재 run에서 `P/AGENTS.md`의 `## 항상 적용 hard guard`가 적용됐음을 보장할 수 있으면 재독하지 않는다. 보장할 수 없는 standalone/subagent 진입이면 그 section을 먼저 읽고 진행한다. implementing 단계에서 확인한 변경 없는 Issue/경계/검증 결과와 이미 확보한 GitHub Issue/PR metadata는 재사용한다. 단 현재 lane의 push로 인한 PR head SHA 변경, 이번 run의 Issue/PR merge·close·reopen 또는 label/assignee/state 변경, base ref/base SHA 변경 근거, webhook/wake·외부 tool result·GitHub 상태 변경을 알리는 사용자 지시 같은 외부 상태 변경 신호, merge 직전과 merge 후 closure 확인 직전 boundary에서는 그 판정에 필요한 metadata만 다시 조회한다.

필수:
1. Current Issue body/labels
2. Current diff
3. `W/process/sdd-workflow.md` (공통 계약·수행법) / `P/.adaptive-sdd/project/sdd-workflow.md` (제품 적용·권한·검증)
4. Current PR/CI state when a PR exists. 상태·라벨·mergeability·head/base SHA만 필요하면 metadata-first로 조회하고 host/tool이 지원하는 metadata 전용 또는 field 한정 조회를 우선한다.
5. runtime behavior가 바뀌었다면 직접 관련된 business document

full PR/Issue body·comments·diff는 그 내용 자체가 판단 근거일 때만 읽는다. 예: acceptance criteria 재확인, review comment 내용 확인, 실제 diff 검토. 방금 자신이 작성한 PR/Issue 본문을 상태·mergeability·라벨·head/base 확인 목적으로 재조회하지 않고, metadata 조회 뒤 무조건 full read하는 이중 호출도 만들지 않는다. invalidation 뒤에도 필요한 metadata만 갱신하고, metadata로 안전하게 판정할 수 없을 때만 필요한 범위로 escalation하며 token 절감보다 correctness를 우선한다.

조건부:
- implementing phase가 Execution/Result Packet을 사용했거나 bounded review를 구성할 때 `W/skills/_shared/execution-routing.md`를 읽는다. 이 shared contract는 fixed pre-read 입력이 아니다.
- business document lifecycle exception이나 shared/root boundary 확인이 실제로 필요할 때만 `W/process/module-boundaries.md`의 공통 경계·lifecycle 계약과 `P/.adaptive-sdd/project/module-boundaries.md`의 실제 제품 경계를 읽는다.
- diff↔Issue, code↔business, instruction 간 충돌이 생길 때만 `W/process/agent-instruction-policy.md` (공통 계약·수행법) / `P/.adaptive-sdd/project/agent-instruction-policy.md` (제품 적용·권한·검증)를 읽는다.
- release는 `W/skills/parallel-development/SKILL.md`를 적용하되 같은 run의 claim metadata를 재사용한다.

## Finish in fixed order

### 1. Confirm actual change
1. 검토 대상의 base/head SHA와 current head의 전체 changed-file inventory를 직접 확인한다. worker가 고른 목록만 신뢰하지 않는다.
2. Result Packet의 base/head, inventory immutable identity, diff reference가 current head/diff와 일치하는지 확인하고 mismatch는 `STALE`로 처리한다.
3. diff를 읽는다.
4. behavior change와 formatting/comment/generated change를 구분한다.
   사람이 읽는 변경 문서는 [사람용 문서의 시각적 작성](../../process/agent-instruction-policy.md#사람용-문서의-시각적-작성)으로 같은 self/required review에서 확인한다. 첫 설명으로 변화·선택을 찾을 수 있는지, 필요한 관계가 보이는지, 그림·표의 조건·실패·미결이 본문과 같은지 본다. 의미 차이는 기존 source/범위/review 절차로 처리하며 별도 승인·review 회차나 그림 개수 gate를 추가하지 않는다. 단순 설명과 변경 없는 같은 run의 기준은 그대로 재사용한다.
5. 각 behavior change를 Issue acceptance criterion에 연결한다.
   - 반대 방향으로 기준 revision의 요구에서 최종 변경·검증을 대조해 빠진 진입점·조건도 찾는다. 테스트 제거·단언 약화·실행 제외·대상 변경은 최종 후보의 대체 근거와 공백을 SUMMARY에 드러낸다. 기존 입력의 PASS를 새 실행으로 쓰거나 최신 문서·CI의 일치만으로 기준 요구 충족을 대신하지 않는다. 미충족/필수 검증 공백은 기존 완료 gate로 처리한다.
   - Human Decision과 execution spec·diff의 일치도 확인한다. 사람이 결정하지 않은 새 중요한 결정/의미 변경이 있으면 `W/process/sdd-workflow.md` (공통 계약·수행법) / `P/.adaptive-sdd/project/sdd-workflow.md` (제품 적용·권한·검증)의 `[HUMAN DECISION REQUIRED]` 절차로 영향 작업과 closure를 중단한다. 일반 Agent 합의나 review PASS를 Human Decision으로 대체하지 않는다.
   - Large AS-IS와 PLAN 각각에서 Review A Contract Review와 Review B 근거가 해당 phase의 exact candidate에 유효한지 확인한다. 최초 Blind Audit 및 이후 target 차이·영향 판정·A/B 재확인 chain과 current-target prior finding 상태를 확인한다. 핵심 Decision/상위 계약/경계/감사 전제 변경이나 불명확한 영향이면 새 Blind Audit이 필요하고, 국소 변경이면 독립 후속 재확인을 최초 blind로 오기하지 않았는지 확인한다. 검토 결과 기록만 바뀌고 대상 bytes가 불변이면 새 blind를 요구하지 않는다. 이전 PASS를 복사한 stale chain은 closure를 막는다. unresolved Human Decision blocker와 unresolved Execution-contract blocker는 각각 0이어야 한다. Implementation finding과 Non-blocking observation이 남았다는 이유로 PLAN review 근거를 무효화하지 않는다. A/B actor/session은 document author 및 서로와 분리되어야 하며, B 최초 verdict가 A의 verdict/finding/detailed packet 또는 이전 B finding detail을 받지 않았고 최초 verdict가 고정된 뒤에만 prior ledger가 제공됐는지 확인한다. reconciliation은 각 이전 finding을 `resolved / unresolved / regressed / not-applicable`로 current exact candidate에서 직접 재검증하고 신규 finding과 분리해야 한다. B reviewer의 model + reasoning에 대한 Human 선택, REVIEW floor/role qualification과 availability도 확인한다. 선택 누락, silent fallback, stale target, anchoring, reconciliation 누락 또는 분리 실패가 있으면 implementation이 이미 진행됐어도 유효한 design review로 추정하지 않고 closure를 중단한다.
6. scope 밖 change는 allowed path 안에서 안전하게 제거하거나, 불가능하면 `BLOCKED`하고 closure를 진행하지 않는다.
7. Trivial은 `W/process/sdd-workflow.md` (공통 계약·수행법) / `P/.adaptive-sdd/project/sdd-workflow.md` (제품 적용·권한·검증)의 Trivial 조건을 다시 확인하고 targeted validation + diff ↔ 요청 범위를 self-review한다. Small은 diff ↔ 완료 기준을 self-review한다. Medium은 Verification Strategy의 `Independent Review` 판정을 적용하고, Large는 기존 bounded independent code review 1회 결과를 확인한다. Review B를 기본 CODE review에 추가하지 않으며 명시적 high-risk escalation 근거가 있을 때만 별도 code audit을 요구한다.

W·M 고정 사본(`P/.adaptive-sdd/workflow`, `P/.adaptive-sdd/methodology`)은 이 작업에서 수정하지 않는다. 고쳐야만 풀리는 문제는 공통 문제로 보고한다.

Trivial diff에서 실행 코드·테스트 기대값·build/dependency·schema·contract·CI/workflow 실행 의미 변경이 확인되면 Trivial로 완료하지 않고 최소 Small로 재판정한다.

required reviewer에게는 shared routing contract의 phase-aware Review Packet을 제공한다. AS-IS/PLAN Review A는 해당 phase에 실제로 존재하는 artifact와 upstream identity를 요구하고, CODE reviewer는 Issue acceptance, reviewed PLAN identity, base/head SHA, 독립 확인할 전체 inventory 또는 immutable reference, current diff와 필요한 hunk/public contract, commit-bound verification evidence identity, PLAN implementation finding handoff와 항목별 code+fixture resolution evidence를 받는다. applicable field는 nested value까지 nonempty여야 하되 PLAN에 implementation finding이 없으면 해당 list는 비어 있을 수 있다. CODE reviewer는 inventory 완전성과 PLAN handoff item 완전성을 독립 확인한 뒤 bounded diff/contracts에서 각 implementation finding의 code와 fixture 해결을 확인하고 solution discovery나 repository-wide 재탐색을 하지 않는다. implementation worker와 reviewer는 다른 agent/session이어야 한다. Packet target/head/diff/inventory/evidence가 current target과 다르거나 applicable acceptance/artifact/evidence가 비어 있으면 `STALE` 또는 `INVALID`이며, handoff item이 누락·unresolved이거나 required review 지적 사항이 unresolved이면 merge/complete로 진행하지 않는다. Implementation finding을 새 Human Decision으로 오인하지 않는다.

최초 Blind Audit Packet은 Review A 결과와 이전 B finding detail을 제외한 최소 phase/target/goal/ownership/omission 요청만 포함한다. 최초 verdict가 고정된 뒤에만 prior B finding identity와 resolution expectation ledger를 reconciliation 입력으로 제공한다. Review B는 design completeness gate이며 finishing 시 Human에게 detailed review 전체를 다시 읽히지 않는다.

인계에 문맥 전환이 기록됐다면 실제 host execution evidence, 최소 입력과 guard/claim/direct source 최신성 확인을 소비한다. 분리 미지원·압축 실패를 성공으로 가장하거나 필수 근거가 누락된 Result Packet으로 완료하지 않는다. 같은 영역의 2회 연속 정체로 중단된 blocker는 해결 또는 사람이 정한 범위 결정 근거 없이 closure하지 않는다. 로그 전문 재수집 대신 기존 Result/Review Packet의 불변 참조를 사용한다.

### 2. Synchronize business documents

runtime behavior가 바뀐 경우에만:
1. 직접 영향을 받는 `P/docs/domains/**` rule/topic을 찾는다.
2. Issue/SDD prose가 아니라 final code로 동작을 확인한다.
3. 같은 business file을 다른 active lane/PR이 수정하는지 확인한다.
4. conflict면 `BLOCKED: documentation lane conflict`.
5. 아니면 실제로 바뀐 rule만 갱신한다.

runtime/product behavior가 바뀌지 않았으면 business doc을 만들기 위해 수정하지 않는다.

### 3. Verify
P가 영향 분석 도구를 선언했으면 shared routing의 `공통 영향 결과 참조와 로컬 소비`에 따라 영향 결과를 현재 base/head·checkout·전체 입력에 대조한다. stale/불완전 결과로 검증을 줄이지 않으며 이전 SHA 리뷰를 현재 PASS로 승계하지 않는다. 변경분 재리뷰에도 전체 inventory·직접 소비자·이전 finding 재발·PLAN handoff를 확인하고, 아래 최종 검증을 그대로 수행한다. 선택·재실행·재조회 이유/시간과 실제 확보한 usage는 같은 계약의 metadata로 구분한다.

1. current diff와 required review finding이 안정화되고 verification-affecting input을 더 수정할 계획이 없는 stable final candidate인지 확인한다.
2. Issue가 요구한 검증과 `W/process/sdd-workflow.md` (공통 계약·수행법) / `P/.adaptive-sdd/project/sdd-workflow.md` (제품 적용·권한·검증)의 해당 grade/change-scope 기준이 만드는 required broad command set을 current candidate에서 실행한다.
3. 각 command의 PASS를 그 command가 검증한 candidate input에 연결한다. command가 소비하거나 assertion하는 production/test source, resource/manifest/runtime asset, build/dependency/configuration, schema/migration/contract, fixture/snapshot/generated input/test expectation이 바뀌면 해당 PASS를 invalidated한다.
4. broad verification 뒤 verification-affecting input이 바뀌면 affected test 또는 owning/direct-impact module의 targeted verification부터 실행하고, 안정화된 새 candidate에서 invalidated된 broad command를 다시 실행한다. 입력 불변 근거가 있는 command의 PASS만 재사용한다.
5. Issue/PR comment, review discussion, PR 설명 또는 non-runtime documentation만 바뀌면 runtime 빌드 검증 PASS를 불필요하게 invalidated하지 않는다. 다만 변경 입력을 소비하는 static validator나 Skill behavior eval은 다시 실행하며, runtime에서 소비되는 Markdown/resource/manifest/asset은 non-runtime 문서로 취급하지 않는다.
6. Trivial은 link/path/format/static validator 등 변경 종류에 맞는 targeted validation만 필수다. 빌드 도구 검증은 변경 영향 근거가 있을 때만 실행한다.
7. 빌드·테스트 명령 전 `W/skills/_shared/build-preflight.md`를 적용한다. required local 빌드 검증이면 intended process environment의 빌드 도구 version 결과(Gradle이면 `gradlew --version`)에서 실제 launcher/daemon JVM major version이 P 적용 문서 `build.md`의 `JDK major`와 같은지 확인한 뒤 같은 run의 JDK를 재사용한다. usable current Java/`JAVA_HOME`이라는 사실이나 선언과 다른 결과를 canonical PASS로 소비하지 않는다. 이미 설치된 선언 버전 JDK로 process-local 교정할 수 없으면 `BLOCKED: canonical build JDK unavailable`로 중단하고 미실행 command/근거를 기록한다. 자동 설치·다운로드·영속 환경 변경은 하지 않는다.
8. 선언과 다른 JVM에서 발생한 정적 분석/빌드 도구 failure는 product/code regression으로 확정하지 않고 환경 failure로 분리한 뒤, 선언 버전 JDK에서 같은 required command를 재실행해 결과를 판정한다. 원래 빌드 검증이 required가 아닌 non-runtime 문서·Skill·eval 변경에는 이 규칙을 이유로 전체 빌드 gate를 추가하지 않는다.
9. command/result를 기록하고 필요한 CI를 확인한다.
10. required failure는 incomplete다.
11. unrun check는 `미검증`이며 pass가 아니다. 단, grade 규칙상 필요하지 않은 빌드 도구 검증은 미검증 blocker가 아니다.
12. changed-file list가 Issue allowed/forbidden과 일치하는지 확인한다.
13. Device QA / Runtime QA metadata나 report를 merge gate로 확인하지 않는다. 선택적 기기 확인은 P가 선언한 경우의 비필수 참고일 뿐 미실행·report 부재·artifact 상태로 PR을 중단하지 않는다.
14. 외부 blocker는 상태와 재개 조건을 한 번 기록한다. 명시한 `P/.adaptive-sdd/project/sdd-workflow.md`의 mode 값이 `ENABLED`이고 authoritative goal tracker 값이 있으면 중단 직전에 `[WORKFLOW][TOKEN BLOCKED]`를 한 번 기록한다. blocker는 대화 내용을 재구성할 수 없는 category만 사용하고, 동일 blocker가 해소되지 않은 동안 자동 재확인하거나 checkpoint를 반복하지 않는다.
15. 직전 token lifecycle이 BLOCKED이고 새로운 사용자 지시 또는 상태 변경 근거로 실제 작업을 재개하면 `[WORKFLOW][TOKEN RESUME]`를 한 번 기록하고 직전 BLOCKED 댓글 URL을 `from`으로 연결한다. 근거가 없으면 RESUME을 기록하지 않고 재개하지 않는다.
16. Result Packet의 changed files, acceptance, verification은 nonempty여야 하고 scope/unresolved/escalation field와 `implementation_findings` list의 명시적 형식을 확인한다. 검토를 통과한 PLAN에 Implementation finding handoff가 있으면 모든 identity와 resolution expectation이 보존되고 각 item이 `resolved`이며 code evidence와 fixture/test evidence가 Result head에 결합됐는지 확인한다. 누락·unresolved·한쪽 evidence 부재·head mismatch는 incomplete 또는 `STALE`이다. verification item마다 실행 commit SHA, command, exit code/outcome, evidence kind, immutable evidence identity를 확인한다. command/exit/outcome 자기신고만으로 PASS 처리하지 않으며 evidence identity가 다른 commit에 결합되거나 Result head와 다르면 해당 검증은 `STALE`이다.

### 4. Remove temporary SDD

SDD 또는 로컬 결과에만 있는 발견 사건은 정리 전에 workflow의 `문제 발견 시 기록과 종료 연결`에 따라 기존 Issue에 보존한다. 검토를 통과한 SDD를 사건 장부로 수정하지 않는다. 보존 실패는 기존 인계/종료에 드러내며 수집을 새 완료 gate로 삼지 않는다.

Trivial/Small이면 해당 없음. SDD가 있는 경우에만:
1. business sync와 필요한 verification 뒤 current Issue의 SDD를 삭제한다. 검토한 설계 문서는 삭제 전 Git commit에서 계속 조회할 수 있다. 일부 삭제나 설계 수정을 정리로 숨기지 않는다.
2. `P/docs/README.md`와 다른 문서의 삭제된 SDD link를 제거한다.
3. historical review의 mutable status가 stale한 경우 status만 갱신한다.

business sync 전에 SDD를 삭제하지 않는다.

### 5. Prepare/verify PR closure
- 모든 등급에서 현재 작업의 발견 사건을 workflow의 `문제 발견 시 기록과 종료 연결`에 따라 같은 SUMMARY에 취합한다. 핵심 사실·단계/담당 metadata·조치/결과와 원본 참조를 함께 남기고 링크만 전달하지 않는다. 동일 사건을 중복 집계하거나 수정 후 성공으로 최초 실패를 지우지 않는다. 사건이 없으면 `발견한 문제` 절·빈 목록·정상 단계 기록을 추가하지 않는다. PR 이후 CI/리뷰의 새 사건도 최종 정리 전 같은 SUMMARY에 반영한다.
- PR scope가 Issue boundary/acceptance criteria와 일치해야 한다.
- 사람이 읽는 PR/완료 요약도 위 시각적 작성 기준으로 결과·핵심 변화부터 설명한다. 관계·전후 비교가 실제 판단에 필요한 경우에만 그림/표를 쓰고, 단순 결과는 짧은 문장으로 쓴다. Agent용 검증 inventory·명령은 필요한 근거로 연결하고, 실제 사람 관측 없이 이해 향상·시간 절감을 주장하지 않는다.
- 구현 종료 시 `W/process/sdd-workflow.md` (공통 계약·수행법) / `P/.adaptive-sdd/project/sdd-workflow.md` (제품 적용·권한·검증)의 `[IMPLEMENTATION SUMMARY]` 댓글 하나로 확정 Decision 준수, execution deviation, Human escalation, verification, 남은 위험을 짧게 기록한다. 이미 작성한 요약은 중복 생성하지 않고 필요한 경우 갱신한다. 새 문서나 추가 Human 승인 gate를 만들지 않으며 검증·required review를 대체하지 않는다.
- 같은 SUMMARY에 workflow의 `차세대 방법론의 적용과 개선 관측` 종료 항목을 연결한다. 실제 지원·관측 출처·수집 공백·비용 범위 또는 미수집·작성 모델 한 줄·다음 판단을 남기고, 인계나 외부 중단 시에는 시작 URL과 현재 관측/다음 조치를 보존한다. tracker unavailable을 다른 관측 생략으로 확대하지 않는다. 문서 읽기·합성 PASS·Agent 자기보고를 실제 수집 완주나 효과로 바꾸어 쓰지 않는다.
  작성 모델 한 줄은 workflow의 `작성 모델 기록` 형식과 host별 조회 위치를 따른다. 실제 제공값이 `미확인`이어도 확인한 요청값과 출처를 남기고, 역할·actor 식별자나 다른 작업·actor의 값을 모델 값으로 쓰지 않는다. 세션 기록에서는 모델 필드만 추출한다. 모델 줄의 누락이나 `미확인`으로 closure를 막지 않는다.
  시작 원본과 이미 보존한 결과를 직접 참조해 고정 정보의 본문 복사를 줄인다. 새 실패·요구 미충족·검증 축소·출처 상실·판단 변경은 현재 SUMMARY에 명시한다. 원본이 소실되거나 버전이 다르면 현재 확인한 적용 정보와 미확인 구간을 구별하며 요약으로 복구하지 않는다. 비용의 출처·수집 가능 여부는 현재 구간에서 확인한 뒤 같은 한계만 묶어 참조한다.
- PR body에 `Closes #{issue-number}`를 넣는다.
- Large PR은 `W/process/sdd-workflow.md` (공통 계약·수행법) / `P/.adaptive-sdd/project/sdd-workflow.md` (제품 적용·권한·검증)의 `사람 판단 지점`에 따라 사람이 그 PR을 직접 병합하거나 병합을 명시적으로 지시한 경우에만 병합한다. review PASS·CI 통과·일반 진행 지시만으로 병합하지 않는다.
- required CI/review gate가 끝나기 전에 완료로 표현하지 않는다.

### 6. Merge confirmation and release

merge 후:
1. PR merged 확인. merge 직전과 이 시점은 metadata freshness boundary이므로 merged 상태·mergeability·head/base SHA 중 판정에 필요한 metadata만 다시 조회한다.
2. Issue closed 확인. closed 여부와 라벨만 필요하면 Issue body/comments 전문을 다시 조회하지 않는다.
3. 제품 반영 완료와 local cleanup·ownership release를 분리한다. 실제 merged PR·closed Issue를 확인하고 아래 점검 뒤 `[PRODUCT COMPLETE]`를 한 번 작성한다. 첫 줄 태그 다음에 `product-complete: {"schema_version":1,"issue":N,"pull_request":PR,"merge_commit":"40자리 SHA"}`를 적고 실제 main 대상 PR의 closing reference와 merge SHA를 사용한다. local cleanup pending도 제품 완료를 취소하지 않는다. 같은 lifecycle의 완료 기록을 중복 생성하지 않는다.
   정리 전에 시작·SUMMARY·필요한 원본을 프로젝트의 지속 보존 위치에서 재조회하고, 최종 상태와 조회 결과를 기존 SUMMARY에 갱신한다. 조회 실패·부분 적용·미수집은 명시하고 기존 제품 완료 gate와 구별한다. 로컬 worktree 파일만을 후속 관측의 유일한 원본으로 남기지 않는다.
4. 관측 기록 점검 도구는 이 preview에 포함하지 않는다. `[PRODUCT COMPLETE]`에 `observation-check unavailable reason=not-shipped` 한 줄을 남기고 계속한다. 이 결과는 절차를 멈추지 않고 release·closure를 바꾸거나 `BLOCKED`·정지 조건이 되지 않는다.
   - 정상 1회 실행은 위 결과 한 줄만 기록한다. `missing`/`unavailable`을 없애거나 `confirmed`를 얻기 위해 기록을 맞춰 쓰거나 반복 실행하지 않는다. 이 규칙은 재실행을 의무화하거나 자동 재시도하는 절차가 아니다.
   - 실제 입력·환경 변경 또는 잘못된 실행 순서의 수정으로 재실행할 경우, **최초 원본 출력**을 먼저 기존 SUMMARY에 보존하고 무엇이 바뀌어 다시 실행하는지 짧게 기록한다. 이미 재실행했다면 확보된 최초 출력·사유·최종 출력을 같은 SUMMARY에 구분해 남긴다. PRODUCT COMPLETE에는 최종 출력 한 줄과 재실행 여부/사유 및 그 SUMMARY 참조를 남긴다. 최초 결과를 최종 결과로 덮어쓰거나 별도 로그·중앙 장부를 만들지 않는다.
   - 최초 출력이 유실됐으면 `최초 출력 확인 불가`와 사유를 남기고 추정 복원하지 않는다. 재실행의 `confirmed`도 기록 형식의 판정이며 독립적인 준수·효과 증거가 아니다. 결과·재실행·유실은 cleanup/release의 새 차단 조건이 아니다.
5. `parallel-development`의 no-artifact 예외를 먼저 판정한다. 해당 없으면 local worktree를 제거하기 전에 해당 worktree 안의 build/generated output을 P 적용 문서 `build.md`의 정리 명령으로 먼저 정리하고, worktree가 clean한지 확인한다. cleanup이 실패하면 registration 제거를 먼저 진행하지 않는다.
6. run-owned/generated임을 증명하지 못한 untracked diagnostic/unknown file은 사용자 state로 보존한다. 해당 파일을 삭제하거나 worktree remove/force cleanup하지 않고 registration 제거와 `[RELEASE]`를 중단하며 lane release incomplete로 보고한다.
7. Windows local worktree root는 P 적용 문서 `sdd-workflow.md`의 `worktree root`처럼 짧은 경로를 유지하고 Git long-path 지원을 사용한다.
8. worktree registration 제거 후에는 `git worktree list`에서 해당 경로가 사라졌는지와 physical directory가 실제로 사라졌는지를 각각 확인한다.
9. 보호 정책상 recursive delete가 허용되지 않을 때 수천 개 파일을 개별 shell command/loop로 삭제하는 우회 절차에 들어가지 않는다. 대량 잔여물이 남으면 `CLEANUP_BLOCKED`로 fail-closed하고 정확한 root, 잔여 파일 수, 최장 경로, registration 상태, local/remote branch 상태를 보고한다.
10. 소수의 run-owned/generated로 검증된 잔여 파일이나 빈 디렉터리만 남은 경우에만 canonical worktree root 하위에서 개별 정리를 허용한다.
11. registration 제거와 physical directory 제거가 모두 확인돼야 local cleanup complete다. cleanup 실패는 별도 pending으로 보고하며 제품 완료·관측 자격을 유지한다. local cleanup만의 후속 갱신은 `[LOCAL CLEANUP]`에 남겨 SUMMARY/제품 완료의 관측 fingerprint를 불필요하게 바꾸지 않는다.
12. registration/physical 부재가 모두 확인된 뒤 `parallel-development`의 ownership release를 적용한다. pending이면 exact path/재개 조건을 명시하고 lane release incomplete로 보고하되 제품 완료를 취소하지 않는다.
13. 제품 완료가 확인되면 local cleanup과 별개로 명시한 `P/.adaptive-sdd/project/sdd-workflow.md`의 mode 값이 `ENABLED`이고 authoritative goal tracker 값이 있으면 `[WORKFLOW][TOKEN END]`를 한 번 기록한다. 최초 START와 현재 값으로 `used = end - start`를 계산하고 결과는 `completed`로 둔다. 기존 END가 있으면 재기록하지 않는다.

`not-planned` 종료는 merge 절차 대신 최종 종료가 확정된 시점에 같은 END 형식을 사용하고 `result: not-planned`로 기록한다. BLOCKED 없이 끝난 Issue에는 BLOCKED/RESUME을 만들지 않는다. tracker 값이 없으면 숫자를 추정하거나 repository-wide 탐색하지 않고 checkpoint만 생략하며, verification·review gate는 그대로 수행한다.

## Incomplete conditions

다음 중 하나면 Issue를 complete라고 하지 않는다:
- acceptance criterion failed/unknown
- required CI failing
- required independent review unfinished 또는 unresolved finding
- Large AS-IS/PLAN Review A/B target·actor/session 분리·Blind Audit isolation·Human reviewer selection provenance가 누락되거나 stale
- 필요한 prior B finding reconciliation이 누락·stale이거나 unresolved Human Decision/Execution-contract blocker가 남음
- PLAN Implementation finding handoff가 Result/CODE Review Packet에서 누락되거나 code+fixture 해결이 미검증·unresolved·stale
- required business doc이 final code와 모순
- documentation lane conflict
- required SDD cleanup unfinished
- PR closing reference 없음
- unresolved BLOCKED
local cleanup의 `CLEANUP_BLOCKED`, registration/physical 잔여, unknown file은 **local cleanup incomplete**로 별도 보고하며 위 제품 완료 판정과 구분한다. unknown/user 파일 삭제 금지는 유지한다.

## Output

- changed files
- acceptance checklist
- business docs status
- verification / CI
- review
- SDD cleanup
- PR / Issue closure
- token diagnostic BLOCKED/RESUME/END 기록 또는 authoritative tracker unavailable
- lane/worktree release
- unverified / BLOCKED
- Result Packet base/head/inventory/diff freshness
- verification immutable evidence identity
- Review Packet inventory 독립 확인 / reviewer 분리
