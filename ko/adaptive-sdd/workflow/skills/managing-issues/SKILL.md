---
name: managing-issues
description: 이 프로젝트의 작업 항목(Issue)을 생성·분류·우선순위 재조정·본문 재작성할 때 사용한다. Issue 생성, Priority/SDD grade 판정, 작업 경계, Mermaid 흐름 판단, UI/UX HTML Visual Spec 연결에 쓴다. 코드 구현에는 사용하지 않는다.
---

실행 입력은 절대 경로 `P`(프로젝트 저장소 최상위), `W`(고정 절차 사본 `P/.adaptive-sdd/workflow`), `M`(고정 공통 원칙 `P/.adaptive-sdd/methodology`)이다. cwd나 W의 상위 디렉터리로 P/M을 추정하지 않는다. P의 hard guard(`P/AGENTS.md`의 `## 항상 적용 hard guard`)와 적용 선언(`P/.adaptive-sdd/project/sdd-workflow.md`)을 적용한다. Issue·댓글·라벨·PR 표현은 `P/.adaptive-sdd/project/tracker.md`가 선언한 작업 관리 방식(`W/tracker/`)으로 바꿔 읽는다.

# Managing Issues

## Inputs

현재 run에서 `P/AGENTS.md`의 `## 항상 적용 hard guard`가 적용됐음을 보장할 수 있으면 재독하지 않는다. 보장할 수 없는 standalone/subagent 진입이면 그 section을 먼저 읽고 진행한다.

선행 입력:

1. 현재 사용자 요청
2. `W/process/issue-priority.md`의 `## Priority 판정 순서`·`## 증거가 부족할 때`와 `P/.adaptive-sdd/project/issue-priority.md`의 현재 단계·제품 적용. 신규 생성이면 W의 `## 신규 Issue 필수 본문`·`## 필수 라벨`, reprioritize면 W의 `## Priority 변경`
3. `W/process/sdd-workflow.md`의 `## SDD grade`·`### 일반 자동 격상`과 `P/.adaptive-sdd/project/sdd-workflow.md`의 제품별 `### 자동 격상`; legacy Issue 정규화가 필요할 때만 `## Legacy Issue 정규화`
4. `W/process/issue-writing-guide.md`의 `## 근거 기록 규칙`, `## Mermaid 생성 조건`, `## HTML Visual Spec 생성 조건`과 `P/.adaptive-sdd/project/issue-writing-guide.md`의 `## 근거 기록 규칙`(개인정보·허용 근거). HTML이 필요할 때만 제품 저장 위치·의존성 제한도 확인한다.
5. 기존 Issue 변경이면 그 Issue의 current body/labels/assignees/comments/linked PRs

heading/section 단위 조회를 지원하지 않는 host에서는 위 파일을 full-read해도 된다. section 조회가 가능한데 일반 프로젝트 이해를 이유로 세 파일 전체를 선행 로딩하지 않는다.

조건부:

- product/shared/root ownership 또는 integration 판단이 필요할 때만 `W/process/module-boundaries.md`의 공통 경계·lifecycle 계약과 `P/.adaptive-sdd/project/module-boundaries.md`의 실제 제품 경계.
- instruction conflict, code↔business drift, 모호한 scope가 실제로 생길 때만 `W/process/agent-instruction-policy.md` (공통 계약·수행법) / `P/.adaptive-sdd/project/agent-instruction-policy.md` (제품 적용·권한·검증).
- 같은 run에서 이미 확인한 변경 없는 입력은 재사용한다.

Issue 분류에 필요하지 않으면 product code를 넓게 탐색하지 않는다.

## Conversation-content gate

GitHub write 전후에 반드시:

- 대화 전체/부분 인용, 번역, 재구성 가능한 요약을 기록하지 않는다.
- 허용된 id/metadata/측정값/재구성 불가능한 범주명만 근거로 쓴다.
- 세부 allowlist는 `issue-writing-guide.md`의 `근거 기록 규칙`을 따른다.
- 금지 내용 없이 근거를 만들 수 없으면 `BLOCKED`.
- write 후 artifact를 다시 확인한다.
- 이미 금지 내용이 쓰였으면 편집하지 말고 artifact를 삭제 후 재생성한다.

## Create a new Issue

1. 요청을 독립적인 Issue-sized outcome으로 나눈다.
2. W 공통 Priority와 P 현재 단계·기능 사실로 Priority를 판정한다.
3. W 공통 grade/일반 자동 격상과 P 제품 매핑으로 SDD grade를 판정한다.
4. 실제 repository path를 확인해 allowed/forbidden을 작성한다. product/shared/root 경계 판단이 필요할 때만 `module-boundaries.md`를 읽는다.
5. `W/process/issue-priority.md`의 canonical 신규 Issue 본문 section을 사용한다.
6. 각 완료 기준이 자동 테스트/CI와 grade별 review로 판정 가능한 성공/실패 조건인지 확인한다. 모든 Issue에 별도 Verification Strategy section을 강제하지 않는다.
7. body와 일치하는 `priority:*`, `grade:*`를 각각 정확히 하나 적용한다.
8. Issue 사람용 설명을 작성/수정할 때 [사람용 문서의 시각적 작성](../../process/agent-instruction-policy.md#사람용-문서의-시각적-작성)을 적용한다. 핵심 변화부터 보여주고 정책 비교·소유/책임 경계도 필요한 표현으로 설명한다. 단순 변경은 한 문장으로 충분하다. 같은 단계에서 `issue-writing-guide.md`의 Mermaid/HTML Visual Spec 조건을 판정하며 HTML 생성·저장 조건을 확대하지 않는다. 변경 없는 같은 run의 기준은 재사용한다.
9. HTML 필요 시 W `issue-writing-guide.md`의 `HTML 최소 내용`, `Visual Spec 링크 규칙`, `디자인 PR 병합·배포·정리`를 P 적용 문서 `issue-writing-guide.md`의 `Visual Spec`이 선언한 저장·게시 방식에 맞춰 적용한다. 선언이 없으면 HTML Visual Spec을 만들지 않는다. 디자인 병합을 앱 승인/완료로 취급하지 않으며, 게시·정리 실패는 마지막 성공 단계와 남은 상태를 기록한다.
10. final Issue를 다시 조회해 section/labels/Visual Spec(해당 시)/conversation gate를 검증한다.

## Triage / reprioritize

1. current Issue와 필요한 최소 evidence만 읽는다.
2. Priority를 현재 규칙으로 재판정한다.
3. scope/risk가 바뀐 경우에만 grade를 재판정한다.
4. 값 변경 시 body와 label을 같은 작업에서 일치시킨다.
5. scope 변경 시 경계/Mermaid/Visual Spec/dependencies/acceptance criteria도 재판정한다.
6. 변경된 완료 기준이 자동 테스트/CI와 grade별 review로 판정 가능한지 확인한다.
7. final Issue를 다시 조회한다.

## Stop conditions

다음이면 `BLOCKED`하고 구현하지 않는다.

- required path 확인 불가
- `agent-instruction-policy.md`로도 해소되지 않는 지시 충돌
- 필수 Visual Spec/immutable link 생성 불가
- 문서 default까지 적용해도 Priority 결정 불가
- active lane scope 침범 필요
- conversation-content gate를 만족하는 evidence 생성 불가

## Output

Issue number/title, Priority/grade/labels, allowed/forbidden, Mermaid/Visual Spec, conversation-content check, dependencies/BLOCKED를 간결히 보고한다.
