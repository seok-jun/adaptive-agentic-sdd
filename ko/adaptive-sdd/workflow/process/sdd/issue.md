# SDD issue

## Issue 본문 규약

신규 구현/버그 Issue의 필수 section과 canonical 본문 형식은 고정 W의 `process/issue-priority.md`의 `## 신규 Issue 필수 본문`이 Source of Truth다. 제품별 적용 조건은 `W/../project/issue-priority.md`를 읽는다. 이 문서는 같은 template을 복제하지 않는다.

본문 값과 `priority:*`, `grade:*` 라벨은 항상 일치해야 한다.

Issue 댓글은 `[CLAIM]`, `[RELEASE]`, 변경 이력을 기록할 수 있지만 **현재 목표·범위·경계·완료 기준을 댓글로만 변경하지 않는다.** 변경이 확정되면 본문도 같은 내용으로 갱신한다.

실행 Issue의 일반 댓글은 Agent ↔ Agent 작업 소통이다. AS-IS 근거, 리뷰 반론, path/symbol, 구현 발견, test/verification, handoff를 공유하며 Human의 상시 확인을 요구하지 않는다. Agent끼리의 합의는 Human Decision이 아니며 확정된 Decision을 암묵적으로 추가·변경하지 못한다.

- `[HUMAN DECISION REQUIRED]`: 작업 지시·확정된 설계 범위를 벗어나는 새 중요한 제품/설계 Decision이 필요할 때만 사용한다. 영향을 받는 작업을 STOP하고, 해당 Decision·실제 대안·trade-off를 Human View(Medium 이상은 `02-to-be.md`, Trivial/Small은 Issue)에 반영한 뒤 Human 결정 후 재개한다. Issue의 목표·범위·경계·완료 기준도 바뀌면 본문을 함께 갱신한다.
- `[IMPLEMENTATION SUMMARY]`: 구현 종료 시 댓글 하나에 확정 Decision 준수 여부, execution deviation, Human escalation 발생 여부, verification 결과, 남은 위험만 짧게 기록한다. 추가 Human 승인 gate가 아니다.

[일반 자동 격상](grade.md#일반-자동-격상) 및 P 적용 문서의 `### 자동 격상`의 모든 변경 카테고리는 반드시 Human Decision에 노출한다. 제품 동작 의미, acceptance 해석, 상위 contract가 바뀌거나 의미가 다른 합리적 경쟁 대안이 발견된 경우도 포함한다. **Decision 노출 의무와 추가 Human 결정 필요 여부는 별개다.** Medium은 Issue 목표·범위·경계 안의 결정을 SDD에 명시하고 기존 gate에 따라 진행하며, 노출 카테고리라는 이유만으로 `[HUMAN DECISION REQUIRED]`를 요구하지 않는다. Escalation은 위의 작업 지시·확정된 설계 범위를 벗어나는 새 중요한 결정에 적용한다. 이미 Issue/설계가 결정한 사항에는 결정을 다시 요구하지 않는다. 확정된 제품 의미·불변조건을 바꾸지 않는 구현 세부는 Agent 재량으로 계속한다.

위 두 댓글과 일반 소통의 역할만 구분한다. 기존 claim/release/token marker와 grade별 gate는 유지하며 `[EVIDENCE]`, `[REVIEW]`, `[RESOLVED]` 같은 추가 댓글 taxonomy, 새 문서나 승인 단계를 만들지 않는다. 기존 문서의 내용을 이관해 Human 필수 읽기와 중복을 줄이고 Agent 간 작업 소통량은 인위적으로 제한하지 않는다. Medium의 추가 승인 없는 SDD 진행과 Trivial/Small의 별도 SDD 생략도 유지한다.

## Legacy Issue 정규화

아래는 실행 Issue의 정규화다. 기존 Epic 관리 문서는 [기존 Epic 전환](epic.md#기존-epic-전환)을 따르며 실행 grade·코드 경로 부재로 조율이나 하위 조사를 막지 않는다. 기존 실행 Issue에 아래 항목 중 하나라도 없으면 코드 수정 전에 Issue를 정규화한다.

- Priority 본문 값과 `priority:*` 라벨
- SDD grade 본문 값과 `grade:*` 라벨
- 사용자 영향
- 목표
- 작업 범위
- 작업 경계의 `수정 허용` / `수정 금지`
- 완료 기준
- 의존성 / 차단 요소

정규화 단계에서는 제품 코드를 수정하지 않는다. 기존 Issue의 목표와 현재 architecture 문서를 기준으로 최소 경계를 작성하고, shared 경로가 필요하면 integration 작업으로 표시한다.

## 미결 사항과 단계별 의존성

리뷰 PASS는 해당 target에 대한 검토 결과이며 모든 결정의 완료나 다음 작업 전체의 착수 허가가 아니다. 작성자·조사·reviewer 중 누가 발견했든 미결 사항에는 **확인/결정할 내용, 담당, 결론을 필요로 하는 작업·단계**를 기존 Issue/SDD에 연결한다. 새 상태 라벨·별도 장부·질문 개수 gate는 만들지 않는다.

진입하려는 작업이 결론을 소비하면 해당 부분은 기다리고, 결론과 무관한 조사·작업은 진행할 수 있다. 예를 들어 배포 시점에만 필요한 결정은 독립적인 조사 착수를 막지 않지만, PLAN에서 동작을 선택해야 하는 질문을 배포까지 미룰 수는 없다. 미결 질문을 단순히 노출했다고 해결된 것으로 보거나, reviewer finding에 없다는 이유로 무시하지 않는다. 기존 grade별 리뷰와 사람 판단 요건은 유지한다.

여러 Issue에 공통인 질문은 Epic 담당 또는 기존 조정 담당이 원천·영향 Issue를 연결해 한 번에 묻는다. 이를 위해 Epic을 새로 만들 필요는 없다. 결정 뒤 담당은 관련 Issue/SDD의 미결 표시를 갱신하거나 확정 결정 참조로 대체하고, 활성 담당에게 전달한다. 과거 미결 기록은 이력으로 보존하되 현재 지시가 서로 다르게 남지 않도록 한다. 의미 변경이면 [계획 정정과 정책 전환](plan-change.md#계획-정정과-정책-전환)을 적용한다.
